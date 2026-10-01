"""Fuentes de precios y horario de mercado.

- MercadoSimulado: precios inventados (caminata aleatoria) para probar sin internet.
- MercadoReal: precios reales; cripto vía CCXT (Binance, datos públicos) y
  acciones vía yfinance (Yahoo). La ejecución sigue siendo en papel.
"""
from __future__ import annotations

import math
import random
from collections import deque
from datetime import datetime
from zoneinfo import ZoneInfo

NUEVA_YORK = ZoneInfo("America/New_York")

PRECIOS_INICIALES = {
    "BTC/USDT": 60000.0, "ETH/USDT": 3000.0, "SOL/USDT": 150.0,
    "SPY": 550.0, "AAPL": 220.0, "MSFT": 420.0, "NVDA": 120.0,
}


def mercado_abierto(mercado: str, momento: datetime | None = None) -> bool:
    """Cripto opera 24/7. Acciones de EE.UU.: lunes a viernes 9:30-16:00 de Nueva York.

    No contempla feriados de EE.UU.
    """
    if mercado == "cripto":
        return True
    momento = (momento or datetime.now(NUEVA_YORK)).astimezone(NUEVA_YORK)
    if momento.weekday() >= 5:
        return False
    minutos = momento.hour * 60 + momento.minute
    return 9 * 60 + 30 <= minutos < 16 * 60


class MercadoSimulado:
    def __init__(self, simbolos: list[str], semilla: int | None = None, historia: int = 300):
        self.rng = random.Random(semilla)
        self.t = 0
        self.series: dict[str, deque[float]] = {}
        for s in simbolos:
            precio = PRECIOS_INICIALES.get(s, 100.0)
            serie: deque[float] = deque(maxlen=historia)
            serie.append(precio)
            self.series[s] = serie
        # Precalienta para que los bots tengan historia desde el primer ciclo.
        for _ in range(historia - 1):
            self.avanzar()

    def avanzar(self) -> None:
        self.t += 1
        for s, serie in self.series.items():
            vol = 0.006 if "/" in s else 0.003  # cripto más volátil
            # Un poco de tendencia persistente para que haya movimientos aprovechables.
            deriva = 0.0003 * math.sin(self.t / 40 + sum(map(ord, s)) % 7)
            serie.append(serie[-1] * math.exp(deriva + self.rng.gauss(0, vol)))

    def precio(self, simbolo: str) -> float:
        return self.series[simbolo][-1]

    def historial(self, simbolo: str, n: int) -> list[float]:
        return list(self.series[simbolo])[-n:]


class MercadoReal:
    """Precios reales. Requiere `pip install ccxt yfinance` y acceso a internet."""

    def __init__(self, simbolos: list[str], intervalo: str = "5m"):
        self.simbolos = simbolos
        self.intervalo = intervalo
        self._cache: dict[str, list[float]] = {}
        self._exchange = None

    def avanzar(self) -> None:
        self._cache.clear()

    def precio(self, simbolo: str) -> float:
        return self.historial(simbolo, 1)[-1]

    def historial(self, simbolo: str, n: int) -> list[float]:
        if simbolo not in self._cache:
            self._cache[simbolo] = (
                self._cripto(simbolo) if "/" in simbolo else self._acciones(simbolo)
            )
        return self._cache[simbolo][-n:]

    def _cripto(self, simbolo: str) -> list[float]:
        if self._exchange is None:
            import ccxt

            self._exchange = ccxt.binance({"enableRateLimit": True})
        velas = self._exchange.fetch_ohlcv(simbolo, self.intervalo, limit=300)
        return [v[4] for v in velas]  # precio de cierre

    def _acciones(self, simbolo: str) -> list[float]:
        import yfinance as yf

        datos = yf.Ticker(simbolo).history(period="5d", interval=self.intervalo)
        return [float(x) for x in datos["Close"].tolist()]
