from __future__ import annotations

from dataclasses import dataclass

from ..config import ConfigBot
from ..modelos import Lado, Posicion


@dataclass
class Idea:
    lado: Lado
    cantidad: float
    motivo: str


class Bot:
    """Base de todos los bots. Solo compran y venden lo que compraron (sin cortos ni apalancamiento)."""

    historia_necesaria = 50

    def __init__(self, cfg: ConfigBot):
        self.cfg = cfg
        self.nombre = cfg.nombre
        self.sala = cfg.sala
        self.activos = cfg.activos
        self.p = cfg.params

    def decidir(self, simbolo: str, precios: list[float], posicion: Posicion | None,
                patrimonio_sala: float) -> Idea | None:
        if len(precios) < self.historia_necesaria:
            return None
        precio = precios[-1]
        if posicion:
            perdida = (posicion.precio_promedio - precio) / posicion.precio_promedio * 100
            if perdida >= self.cfg.stop_pct:
                return Idea(Lado.VENTA, posicion.cantidad, f"stop de pérdida ({perdida:.1f} %)")
            if self.salir(precios):
                return Idea(Lado.VENTA, posicion.cantidad, self.motivo_salida(precios))
            return None
        if self.entrar(precios):
            cantidad = patrimonio_sala * self.cfg.tamano_pct / 100 / precio
            return Idea(Lado.COMPRA, cantidad, self.motivo_entrada(precios))
        return None

    # Cada estrategia implementa estas cuatro.
    def entrar(self, precios: list[float]) -> bool:
        raise NotImplementedError

    def salir(self, precios: list[float]) -> bool:
        raise NotImplementedError

    def motivo_entrada(self, precios: list[float]) -> str:
        return "señal de entrada"

    def motivo_salida(self, precios: list[float]) -> str:
        return "señal de salida"
