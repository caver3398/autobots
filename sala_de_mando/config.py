"""Carga la configuración (config.toml): salas, límites de riesgo y bots."""
from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class ConfigSala:
    nombre: str
    mercado: str  # "cripto" | "acciones"
    capital_inicial: float
    moneda: str
    activos: list[str]
    orden_max_pct: float = 10.0
    aprobacion_desde_pct: float = 5.0
    exposicion_max_pct: float = 60.0
    posiciones_max: int = 3
    comision_pct: float = 0.1
    deslizamiento_pct: float = 0.05
    perdida_diaria_max_pct: float = 3.0


@dataclass
class ConfigBot:
    nombre: str
    sala: str
    estrategia: str
    activos: list[str]
    tamano_pct: float = 4.0
    stop_pct: float = 3.0
    # "aprobacion": cada orden espera tu OK; "automatico": opera dentro de los límites.
    habilitacion: str = "aprobacion"
    params: dict = field(default_factory=dict)


@dataclass
class Config:
    base_de_datos: str
    intervalo_segundos: float
    respetar_horario_acciones: bool
    vencimiento_pendientes_min: float
    perdida_diaria_total_max_pct: float
    salas: dict[str, ConfigSala]
    bots: list[ConfigBot]

    def bot(self, nombre: str) -> ConfigBot | None:
        return next((b for b in self.bots if b.nombre == nombre), None)


def cargar(ruta: str | Path = "config.toml") -> Config:
    with open(ruta, "rb") as f:
        datos = tomllib.load(f)

    general = datos.get("general", {})
    riesgo = datos.get("riesgo", {})
    salas = {
        nombre: ConfigSala(nombre=nombre, **valores)
        for nombre, valores in datos.get("salas", {}).items()
    }
    bots = [ConfigBot(**b) for b in datos.get("bots", [])]

    config = Config(
        base_de_datos=general.get("base_de_datos", "sala_de_mando.db"),
        intervalo_segundos=general.get("intervalo_segundos", 60),
        respetar_horario_acciones=general.get("respetar_horario_acciones", True),
        vencimiento_pendientes_min=riesgo.get("vencimiento_pendientes_min", 30),
        perdida_diaria_total_max_pct=riesgo.get("perdida_diaria_total_max_pct", 3.0),
        salas=salas,
        bots=bots,
    )
    _validar(config)
    return config


def _validar(config: Config) -> None:
    nombres = set()
    for bot in config.bots:
        if bot.nombre in nombres:
            raise ValueError(f"Bot repetido: {bot.nombre}")
        nombres.add(bot.nombre)
        if bot.sala not in config.salas:
            raise ValueError(f"El bot {bot.nombre} apunta a una sala inexistente: {bot.sala}")
        if bot.habilitacion not in ("aprobacion", "automatico"):
            raise ValueError(f"Habilitación inválida para {bot.nombre}: {bot.habilitacion}")
        fuera = set(bot.activos) - set(config.salas[bot.sala].activos)
        if fuera:
            raise ValueError(
                f"El bot {bot.nombre} usa activos no habilitados en la sala {bot.sala}: {sorted(fuera)}"
            )
