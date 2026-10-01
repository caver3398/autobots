"""Tres estrategias clásicas y simples, para probar el circuito completo.

No son recomendaciones de inversión: sirven de punto de partida y para medir.
"""
from __future__ import annotations

from .base import Bot


def media(valores: list[float]) -> float:
    return sum(valores) / len(valores)


def rsi(precios: list[float], periodo: int = 14) -> float:
    cambios = [b - a for a, b in zip(precios[-periodo - 1:-1], precios[-periodo:])]
    suba = sum(c for c in cambios if c > 0) / periodo
    baja = -sum(c for c in cambios if c < 0) / periodo
    if baja == 0:
        return 100.0
    return 100 - 100 / (1 + suba / baja)


class CruceMedias(Bot):
    """Compra cuando la media rápida cruza hacia arriba a la lenta; vende al cruce contrario."""

    def __init__(self, cfg):
        super().__init__(cfg)
        self.rapida = int(self.p.get("rapida", 10))
        self.lenta = int(self.p.get("lenta", 30))
        self.historia_necesaria = self.lenta + 1

    def _medias(self, precios, desplazamiento=0):
        fin = len(precios) - desplazamiento
        return media(precios[fin - self.rapida:fin]), media(precios[fin - self.lenta:fin])

    def entrar(self, precios):
        r0, l0 = self._medias(precios, 1)
        r1, l1 = self._medias(precios)
        return r0 <= l0 and r1 > l1

    def salir(self, precios):
        r, l = self._medias(precios)
        return r < l

    def motivo_entrada(self, precios):
        return f"media {self.rapida} cruzó arriba de la media {self.lenta}"

    def motivo_salida(self, precios):
        return f"media {self.rapida} quedó debajo de la media {self.lenta}"


class ReversionRSI(Bot):
    """Compra cuando el RSI marca sobreventa y vende cuando se normaliza."""

    def __init__(self, cfg):
        super().__init__(cfg)
        self.periodo = int(self.p.get("periodo", 14))
        self.compra_bajo = float(self.p.get("compra_bajo", 30))
        self.vende_sobre = float(self.p.get("vende_sobre", 55))
        self.historia_necesaria = self.periodo + 1

    def entrar(self, precios):
        return rsi(precios, self.periodo) < self.compra_bajo

    def salir(self, precios):
        return rsi(precios, self.periodo) > self.vende_sobre

    def motivo_entrada(self, precios):
        return f"RSI {rsi(precios, self.periodo):.0f}: sobreventa"

    def motivo_salida(self, precios):
        return f"RSI {rsi(precios, self.periodo):.0f}: rebote completado"


class Ruptura(Bot):
    """Compra cuando el precio supera el máximo de N períodos; vende si pierde el mínimo de M."""

    def __init__(self, cfg):
        super().__init__(cfg)
        self.entrada = int(self.p.get("entrada", 40))
        self.salida = int(self.p.get("salida", 20))
        self.historia_necesaria = max(self.entrada, self.salida) + 1

    def entrar(self, precios):
        return precios[-1] > max(precios[-self.entrada - 1:-1])

    def salir(self, precios):
        return precios[-1] < min(precios[-self.salida - 1:-1])

    def motivo_entrada(self, precios):
        return f"rompió el máximo de {self.entrada} períodos"

    def motivo_salida(self, precios):
        return f"perdió el mínimo de {self.salida} períodos"
