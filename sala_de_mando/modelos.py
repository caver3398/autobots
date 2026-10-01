"""Tipos básicos que viajan entre bots, la central y el broker."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class Lado(str, Enum):
    COMPRA = "compra"
    VENTA = "venta"


class Veredicto(str, Enum):
    APROBADA = "aprobada"
    RECHAZADA = "rechazada"
    PENDIENTE = "pendiente"  # espera tu aprobación


class EstadoPropuesta(str, Enum):
    PENDIENTE = "pendiente"
    APROBADA_USUARIO = "aprobada_usuario"  # la aprobaste; se ejecuta en el próximo ciclo
    EJECUTADA = "ejecutada"
    RECHAZADA = "rechazada"
    VENCIDA = "vencida"


def ahora() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Propuesta:
    """Lo que un bot pide hacer. Ningún bot opera sin pasar por la central."""

    bot: str
    sala: str
    simbolo: str
    lado: Lado
    cantidad: float
    precio: float  # precio de referencia al momento de proponer
    motivo: str
    id: int | None = None
    ts: datetime = field(default_factory=ahora)

    @property
    def monto(self) -> float:
        return self.cantidad * self.precio


@dataclass
class Resultado:
    veredicto: Veredicto
    motivos: list[str]


@dataclass
class Posicion:
    sala: str
    bot: str
    simbolo: str
    cantidad: float
    precio_promedio: float
