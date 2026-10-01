"""El ciclo de la oficina: en cada vuelta los bots miran el mercado y proponen."""
from __future__ import annotations

from . import bots as fabrica
from .almacen import Almacen
from .central import Central
from .config import Config
from .modelos import EstadoPropuesta, Propuesta, Veredicto

# Después de un rechazo, el bot espera esta cantidad de ciclos antes de insistir con el mismo activo.
ESPERA_TRAS_RECHAZO = 10


class Oficina:
    def __init__(self, cfg: Config, mercado, almacen: Almacen | None = None):
        self.cfg = cfg
        self.mercado = mercado
        self.db = almacen or Almacen(cfg.base_de_datos)
        self.central = Central(cfg, self.db)
        self.bots = [fabrica.crear(b) for b in cfg.bots]
        self.simbolos = sorted({s for sala in cfg.salas.values() for s in sala.activos})
        self.enfriamiento: dict[tuple[str, str], int] = {}

    def precios(self) -> dict[str, float]:
        return {s: self.mercado.precio(s) for s in self.simbolos}

    def ciclo(self) -> dict[str, float]:
        self.mercado.avanzar()
        precios = self.precios()
        self.db.escribir("ultimos_precios", precios)  # para los comandos de otra terminal
        self.central.actualizar_inicio_del_dia(precios)
        self.central.aplicar_kill_switch(precios)
        self.central.vencer_pendientes()
        self.central.procesar_aprobadas(precios)

        en_espera = {
            (p.bot, p.simbolo)
            for estado in (EstadoPropuesta.PENDIENTE, EstadoPropuesta.APROBADA_USUARIO)
            for p in self.db.propuestas(estado)
        }
        for bot in self.bots:
            patrimonio = self.central.patrimonio(bot.sala, precios)
            for simbolo in bot.activos:
                clave = (bot.nombre, simbolo)
                if clave in en_espera:
                    continue
                if self.enfriamiento.get(clave, 0) > 0:
                    self.enfriamiento[clave] -= 1
                    continue
                historial = self.mercado.historial(simbolo, bot.historia_necesaria)
                posicion = self.db.posicion(bot.sala, bot.nombre, simbolo)
                idea = bot.decidir(simbolo, historial, posicion, patrimonio)
                if not idea:
                    continue
                propuesta = Propuesta(
                    bot=bot.nombre, sala=bot.sala, simbolo=simbolo, lado=idea.lado,
                    cantidad=idea.cantidad, precio=precios[simbolo], motivo=idea.motivo,
                )
                if self.central.procesar(propuesta, precios).veredicto == Veredicto.RECHAZADA:
                    self.enfriamiento[clave] = ESPERA_TRAS_RECHAZO
        return precios
