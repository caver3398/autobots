"""Reglas de la central de habilitaciones.

Cada propuesta pasa por todas las reglas. Un rechazo gana sobre todo; si nada la
rechaza pero alguna regla pide tu OK, queda pendiente; si no, se aprueba sola.
Las ventas que reducen una posición nunca necesitan aprobación: bajan el riesgo.
"""
from __future__ import annotations

from dataclasses import dataclass

from .config import Config
from .mercado import mercado_abierto
from .modelos import Lado, Propuesta, Resultado, Veredicto


@dataclass
class Foto:
    """Estado de la oficina en el momento de evaluar."""

    kill_switch: bool
    salas_pausadas: set[str]
    bots_pausados: set[str]
    bots_automaticos: set[str]  # bots habilitados para operar sin pedir OK
    efectivo: dict[str, float]  # por sala
    patrimonio: dict[str, float]  # por sala, a precio de mercado
    expuesto: dict[str, float]  # por sala, valor de las posiciones abiertas
    simbolos_abiertos: dict[str, set[str]]  # por sala
    posicion_bot: float  # cantidad que tiene el bot en ese símbolo
    perdida_dia_pct: dict[str, float]  # por sala; positivo = pérdida
    perdida_dia_total_pct: float


def evaluar(p: Propuesta, cfg: Config, foto: Foto, aprobada_por_usuario: bool = False) -> Resultado:
    rechazos: list[str] = []
    pedir_ok: list[str] = []
    sala = cfg.salas.get(p.sala)
    bot = cfg.bot(p.bot)

    if foto.kill_switch:
        rechazos.append("Kill switch activo")
    if sala is None:
        return Resultado(Veredicto.RECHAZADA, [f"Sala inexistente: {p.sala}"])
    if bot is None or bot.sala != p.sala:
        return Resultado(Veredicto.RECHAZADA, [f"Bot {p.bot} no pertenece a la sala {p.sala}"])
    if p.sala in foto.salas_pausadas:
        rechazos.append(f"Sala {p.sala} en pausa")
    if p.bot in foto.bots_pausados:
        rechazos.append(f"Bot {p.bot} en pausa")
    if p.simbolo not in sala.activos:
        rechazos.append(f"{p.simbolo} no está habilitado en la sala {p.sala}")
    elif p.simbolo not in bot.activos:
        rechazos.append(f"{p.bot} no está habilitado para operar {p.simbolo}")
    if cfg.respetar_horario_acciones and not mercado_abierto(sala.mercado):
        rechazos.append("Mercado cerrado")
    if p.cantidad <= 0 or p.precio <= 0:
        rechazos.append("Cantidad o precio inválidos")

    if p.lado == Lado.VENTA:
        if p.cantidad > foto.posicion_bot + 1e-12:
            rechazos.append(
                f"Venta de {p.cantidad:g} supera la posición del bot ({foto.posicion_bot:g})"
            )
    else:
        patrimonio = foto.patrimonio[p.sala]
        pct = p.monto / patrimonio * 100 if patrimonio > 0 else 100.0
        costo = p.monto * (1 + (sala.comision_pct + sala.deslizamiento_pct) / 100)

        if foto.perdida_dia_pct[p.sala] >= sala.perdida_diaria_max_pct:
            rechazos.append(
                f"Pérdida del día en {p.sala} ({foto.perdida_dia_pct[p.sala]:.2f} %) "
                f"alcanzó el límite de {sala.perdida_diaria_max_pct} %"
            )
        if foto.perdida_dia_total_pct >= cfg.perdida_diaria_total_max_pct:
            rechazos.append(
                f"Pérdida del día total ({foto.perdida_dia_total_pct:.2f} %) "
                f"alcanzó el límite de {cfg.perdida_diaria_total_max_pct} %"
            )
        if pct > sala.orden_max_pct:
            rechazos.append(f"Orden de {pct:.1f} % del patrimonio supera el máximo de {sala.orden_max_pct} %")
        if costo > foto.efectivo[p.sala]:
            rechazos.append(f"Efectivo insuficiente ({foto.efectivo[p.sala]:.2f} {sala.moneda})")
        exposicion = (foto.expuesto[p.sala] + p.monto) / patrimonio * 100 if patrimonio > 0 else 100.0
        if exposicion > sala.exposicion_max_pct:
            rechazos.append(
                f"La exposición quedaría en {exposicion:.1f} %, máximo {sala.exposicion_max_pct} %"
            )
        abiertos = foto.simbolos_abiertos[p.sala]
        if p.simbolo not in abiertos and len(abiertos) >= sala.posiciones_max:
            rechazos.append(f"Ya hay {len(abiertos)} activos abiertos en {p.sala} (máximo {sala.posiciones_max})")

        if not aprobada_por_usuario:
            if pct >= sala.aprobacion_desde_pct:
                pedir_ok.append(f"Orden de {pct:.1f} % del patrimonio (requiere OK desde {sala.aprobacion_desde_pct} %)")
            if p.bot not in foto.bots_automaticos:
                pedir_ok.append(f"{p.bot} opera con aprobación manual")

    if rechazos:
        return Resultado(Veredicto.RECHAZADA, rechazos)
    if pedir_ok:
        return Resultado(Veredicto.PENDIENTE, pedir_ok)
    return Resultado(Veredicto.APROBADA, ["Dentro de todos los límites"])
