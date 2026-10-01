"""La central de habilitaciones: recibe propuestas, decide y ejecuta en papel.

También concentra los controles de la sala de mando: pausas, habilitar bots,
aprobar o rechazar pendientes y el kill switch.
"""
from __future__ import annotations

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from . import riesgo
from .almacen import Almacen
from .config import Config
from .modelos import EstadoPropuesta, Lado, Propuesta, Resultado, Veredicto, ahora

BUENOS_AIRES = ZoneInfo("America/Argentina/Buenos_Aires")


class Central:
    def __init__(self, cfg: Config, almacen: Almacen):
        self.cfg = cfg
        self.db = almacen
        for nombre, sala in cfg.salas.items():
            self.db.crear_cuenta_si_falta(nombre, sala.capital_inicial)

    # --- números de la oficina ---

    def patrimonio(self, sala: str, precios: dict[str, float]) -> float:
        return self.db.efectivo(sala) + self.expuesto(sala, precios)

    def expuesto(self, sala: str, precios: dict[str, float]) -> float:
        return sum(p.cantidad * precios[p.simbolo] for p in self.db.posiciones(sala))

    def actualizar_inicio_del_dia(self, precios: dict[str, float]) -> None:
        """Guarda el patrimonio al empezar cada día (hora de Buenos Aires) para medir la pérdida diaria."""
        hoy = datetime.now(BUENOS_AIRES).date().isoformat()
        inicio = self.db.leer("inicio_dia")
        if not inicio or inicio["fecha"] != hoy:
            self.db.escribir(
                "inicio_dia",
                {"fecha": hoy, "patrimonio": {s: self.patrimonio(s, precios) for s in self.cfg.salas}},
            )

    def perdida_del_dia(self, precios: dict[str, float]) -> tuple[dict[str, float], float]:
        """Pérdida del día en % por sala y total (positivo = pérdida)."""
        self.actualizar_inicio_del_dia(precios)
        inicio = self.db.leer("inicio_dia")["patrimonio"]
        por_sala, total_ini, total_hoy = {}, 0.0, 0.0
        for sala in self.cfg.salas:
            ini = inicio.get(sala) or self.cfg.salas[sala].capital_inicial
            hoy = self.patrimonio(sala, precios)
            por_sala[sala] = (ini - hoy) / ini * 100 if ini else 0.0
            total_ini += ini
            total_hoy += hoy
        total = (total_ini - total_hoy) / total_ini * 100 if total_ini else 0.0
        return por_sala, total

    def bots_automaticos(self) -> set[str]:
        return {
            b.nombre for b in self.cfg.bots
            if self.db.leer(f"habilitacion:{b.nombre}", b.habilitacion) == "automatico"
        }

    def foto(self, p: Propuesta, precios: dict[str, float]) -> riesgo.Foto:
        perdida_sala, perdida_total = self.perdida_del_dia(precios)
        pos = self.db.posicion(p.sala, p.bot, p.simbolo)
        return riesgo.Foto(
            kill_switch=bool(self.db.leer("kill_switch")),
            salas_pausadas={s for s in self.cfg.salas if self.db.leer(f"pausa:sala:{s}")},
            bots_pausados={b.nombre for b in self.cfg.bots if self.db.leer(f"pausa:bot:{b.nombre}")},
            bots_automaticos=self.bots_automaticos(),
            efectivo={s: self.db.efectivo(s) for s in self.cfg.salas},
            patrimonio={s: self.patrimonio(s, precios) for s in self.cfg.salas},
            expuesto={s: self.expuesto(s, precios) for s in self.cfg.salas},
            simbolos_abiertos={s: {x.simbolo for x in self.db.posiciones(s)} for s in self.cfg.salas},
            posicion_bot=pos.cantidad if pos else 0.0,
            perdida_dia_pct=perdida_sala,
            perdida_dia_total_pct=perdida_total,
        )

    # --- flujo de propuestas ---

    def procesar(self, p: Propuesta, precios: dict[str, float]) -> Resultado:
        res = riesgo.evaluar(p, self.cfg, self.foto(p, precios))
        detalle = "; ".join(res.motivos)
        if res.veredicto == Veredicto.APROBADA:
            self.db.guardar_propuesta(p, EstadoPropuesta.EJECUTADA, detalle)
            self._ejecutar(p, precios[p.simbolo])
        elif res.veredicto == Veredicto.PENDIENTE:
            self.db.guardar_propuesta(p, EstadoPropuesta.PENDIENTE, detalle)
            self.db.anotar("pendiente", p.bot, f"#{p.id} {self._texto(p)} espera tu OK: {detalle}")
        else:
            self.db.guardar_propuesta(p, EstadoPropuesta.RECHAZADA, detalle)
            self.db.anotar("rechazo", "Central", f"{p.bot}: {self._texto(p)} rechazada: {detalle}")
        return res

    def procesar_aprobadas(self, precios: dict[str, float]) -> None:
        """Ejecuta lo que aprobaste, volviendo a chequear los límites con el precio de ahora."""
        for p in self.db.propuestas(EstadoPropuesta.APROBADA_USUARIO):
            precio = precios[p.simbolo]
            if p.lado == Lado.COMPRA:
                # Mantiene el monto aprobado, no la cantidad, por si el precio se movió.
                p.cantidad = p.monto / precio
            else:
                pos = self.db.posicion(p.sala, p.bot, p.simbolo)
                p.cantidad = min(p.cantidad, pos.cantidad if pos else 0.0)
            p.precio = precio
            res = riesgo.evaluar(p, self.cfg, self.foto(p, precios), aprobada_por_usuario=True)
            if res.veredicto == Veredicto.RECHAZADA:
                detalle = "; ".join(res.motivos)
                self.db.cambiar_estado_propuesta(p.id, EstadoPropuesta.RECHAZADA, detalle)
                self.db.anotar("rechazo", "Central", f"#{p.id} aprobada por vos pero ya no entra en los límites: {detalle}")
            else:
                self.db.cambiar_estado_propuesta(p.id, EstadoPropuesta.EJECUTADA)
                self._ejecutar(p, precio)

    def vencer_pendientes(self) -> None:
        limite = ahora() - timedelta(minutes=self.cfg.vencimiento_pendientes_min)
        for p in self.db.propuestas(EstadoPropuesta.PENDIENTE):
            if p.ts < limite:
                self.db.cambiar_estado_propuesta(p.id, EstadoPropuesta.VENCIDA)
                self.db.anotar("vencida", "Central", f"#{p.id} venció sin respuesta")

    def _ejecutar(self, p: Propuesta, precio: float) -> None:
        sala = self.cfg.salas[p.sala]
        desliz = sala.deslizamiento_pct / 100
        llenado = precio * (1 + desliz) if p.lado == Lado.COMPRA else precio * (1 - desliz)
        comision = p.cantidad * llenado * sala.comision_pct / 100
        resultado = self.db.registrar_operacion(
            sala=p.sala, bot=p.bot, simbolo=p.simbolo, lado=p.lado, cantidad=p.cantidad,
            precio=llenado, comision=comision, propuesta_id=p.id,
        )
        extra = f" · resultado {resultado:+.2f} {sala.moneda}" if p.lado == Lado.VENTA else ""
        self.db.anotar("operacion", p.bot, f"{self._texto(p, llenado)} ({p.motivo}){extra}")

    @staticmethod
    def _texto(p: Propuesta, precio: float | None = None) -> str:
        return f"{p.lado.value} {p.cantidad:.6g} {p.simbolo} a {precio or p.precio:,.2f}"

    # --- controles de la sala de mando ---

    def aprobar(self, id_: int) -> str:
        return self._responder(id_, EstadoPropuesta.APROBADA_USUARIO, "aprobada; se ejecuta en el próximo ciclo")

    def rechazar(self, id_: int) -> str:
        return self._responder(id_, EstadoPropuesta.RECHAZADA, "rechazada por vos")

    def _responder(self, id_: int, estado: EstadoPropuesta, texto: str) -> str:
        encontrada = self.db.propuesta(id_)
        if not encontrada:
            return f"No existe la propuesta #{id_}"
        _, actual = encontrada
        if actual != EstadoPropuesta.PENDIENTE:
            return f"La propuesta #{id_} no está pendiente (estado: {actual.value})"
        self.db.cambiar_estado_propuesta(id_, estado)
        self.db.anotar("decision", "Vos", f"#{id_} {texto}")
        return f"#{id_} {texto}"

    def pausar(self, tipo: str, nombre: str, pausar: bool = True) -> str:
        if tipo == "sala" and nombre not in self.cfg.salas:
            return f"No existe la sala {nombre}"
        if tipo == "bot" and not self.cfg.bot(nombre):
            return f"No existe el bot {nombre}"
        clave = f"pausa:{tipo}:{nombre}"
        if pausar:
            self.db.escribir(clave, True)
        else:
            self.db.borrar(clave)
        texto = f"{tipo} {nombre} {'en pausa' if pausar else 'reanudada'}"
        self.db.anotar("control", "Vos", texto)
        return texto

    def habilitar_bot(self, nombre: str, modo: str) -> str:
        if not self.cfg.bot(nombre):
            return f"No existe el bot {nombre}"
        if modo not in ("automatico", "aprobacion"):
            return "El modo tiene que ser 'automatico' o 'aprobacion'"
        self.db.escribir(f"habilitacion:{nombre}", modo)
        texto = f"{nombre} ahora opera en modo {modo}"
        self.db.anotar("control", "Vos", texto)
        return texto

    def pedir_kill_switch(self) -> str:
        self.db.escribir("kill_switch", "solicitado")
        self.db.anotar("control", "Vos", "KILL SWITCH solicitado: se cierra todo en el próximo ciclo")
        return "Kill switch activado. Se cierran todas las posiciones en el próximo ciclo y no se abren nuevas."

    def reabrir(self) -> str:
        self.db.borrar("kill_switch")
        self.db.anotar("control", "Vos", "Oficina reabierta")
        return "Kill switch desactivado. Los bots pueden volver a operar."

    def aplicar_kill_switch(self, precios: dict[str, float]) -> None:
        if self.db.leer("kill_switch") != "solicitado":
            return
        for pos in self.db.posiciones():
            p = Propuesta(bot=pos.bot, sala=pos.sala, simbolo=pos.simbolo, lado=Lado.VENTA,
                          cantidad=pos.cantidad, precio=precios[pos.simbolo], motivo="kill switch")
            self.db.guardar_propuesta(p, EstadoPropuesta.EJECUTADA, "Kill switch")
            self._ejecutar(p, precios[pos.simbolo])
        for p in self.db.propuestas(EstadoPropuesta.PENDIENTE) + self.db.propuestas(EstadoPropuesta.APROBADA_USUARIO):
            self.db.cambiar_estado_propuesta(p.id, EstadoPropuesta.RECHAZADA, "Kill switch")
        self.db.escribir("kill_switch", "activo")
        self.db.anotar("control", "Central", "KILL SWITCH aplicado: todo cerrado")
