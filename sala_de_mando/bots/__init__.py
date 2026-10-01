"""Bots: cada uno mira precios y propone. La central decide si se ejecuta."""
from __future__ import annotations

from ..config import ConfigBot
from .base import Bot, Idea
from .estrategias import CruceMedias, ReversionRSI, Ruptura

ESTRATEGIAS: dict[str, type[Bot]] = {
    "cruce_medias": CruceMedias,
    "reversion_rsi": ReversionRSI,
    "ruptura": Ruptura,
}


def crear(cfg: ConfigBot) -> Bot:
    if cfg.estrategia not in ESTRATEGIAS:
        raise ValueError(
            f"Estrategia desconocida para {cfg.nombre}: {cfg.estrategia}. "
            f"Disponibles: {', '.join(ESTRATEGIAS)}"
        )
    return ESTRATEGIAS[cfg.estrategia](cfg)


__all__ = ["Bot", "Idea", "crear", "ESTRATEGIAS"]
