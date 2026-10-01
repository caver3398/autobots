"""Sala de mando por línea de comandos.

    python -m sala_de_mando correr --simulado      # arranca la oficina
    python -m sala_de_mando estado                 # (en otra terminal) cómo va
    python -m sala_de_mando pendientes
    python -m sala_de_mando aprobar 12
"""
from __future__ import annotations

import argparse
import sys
import time
from collections import defaultdict
from datetime import datetime

from . import config as configuracion
from .almacen import Almacen
from .central import BUENOS_AIRES, Central
from .mercado import MercadoReal, MercadoSimulado
from .modelos import EstadoPropuesta
from .oficina import Oficina


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="sala_de_mando", description="Oficina de trading simulada")
    ap.add_argument("--config", default="config.toml")
    sub = ap.add_subparsers(dest="comando", required=True)

    c = sub.add_parser("correr", help="arranca el ciclo de la oficina")
    c.add_argument("--simulado", action="store_true", help="precios inventados, sin internet")
    c.add_argument("--ciclos", type=int, default=0, help="cantidad de ciclos (0 = sin fin)")
    c.add_argument("--intervalo", type=float, help="segundos entre ciclos (por defecto, el de config)")
    c.add_argument("--semilla", type=int, help="semilla del mercado simulado")

    sub.add_parser("estado", help="patrimonio, posiciones y controles")
    sub.add_parser("pendientes", help="órdenes que esperan tu aprobación")
    sub.add_parser("ranking", help="resultado por bot")
    a = sub.add_parser("aprobar")
    a.add_argument("id", type=int)
    r = sub.add_parser("rechazar")
    r.add_argument("id", type=int)
    for nombre in ("pausar", "reanudar"):
        x = sub.add_parser(nombre)
        x.add_argument("tipo", choices=["sala", "bot"])
        x.add_argument("nombre")
    h = sub.add_parser("habilitar", help="cambia cómo opera un bot")
    h.add_argument("bot")
    h.add_argument("modo", choices=["automatico", "aprobacion"])
    sub.add_parser("kill", help="cierra todo y bloquea nuevas operaciones")
    sub.add_parser("reabrir", help="desactiva el kill switch")
    b = sub.add_parser("bitacora", help="últimos eventos")
    b.add_argument("-n", type=int, default=30)

    args = ap.parse_args(argv)
    cfg = configuracion.cargar(args.config)

    if args.comando == "correr":
        return correr(cfg, args)

    db = Almacen(cfg.base_de_datos)
    central = Central(cfg, db)
    acciones = {
        "aprobar": lambda: central.aprobar(args.id),
        "rechazar": lambda: central.rechazar(args.id),
        "pausar": lambda: central.pausar(args.tipo, args.nombre, True),
        "reanudar": lambda: central.pausar(args.tipo, args.nombre, False),
        "habilitar": lambda: central.habilitar_bot(args.bot, args.modo),
        "kill": central.pedir_kill_switch,
        "reabrir": central.reabrir,
    }
    if args.comando in acciones:
        print(acciones[args.comando]())
    elif args.comando == "estado":
        mostrar_estado(cfg, central)
    elif args.comando == "pendientes":
        mostrar_pendientes(db)
    elif args.comando == "ranking":
        mostrar_ranking(cfg, db)
    elif args.comando == "bitacora":
        for e in db.bitacora(args.n):
            print(f"{hora(e['ts'])}  {e['tipo']:<10} {e['actor']:<12} {e['mensaje']}")
    return 0


def hora(ts: str | datetime) -> str:
    """Hora de Argentina para mostrar en pantalla."""
    momento = datetime.fromisoformat(ts) if isinstance(ts, str) else ts
    return momento.astimezone(BUENOS_AIRES).strftime("%H:%M:%S")


def correr(cfg, args) -> int:
    simbolos = sorted({s for sala in cfg.salas.values() for s in sala.activos})
    mercado = MercadoSimulado(simbolos, semilla=args.semilla) if args.simulado else MercadoReal(simbolos)
    if args.simulado:
        # En simulación los precios no siguen el reloj real: ignorar el horario de Nueva York.
        cfg.respetar_horario_acciones = False
    oficina = Oficina(cfg, mercado)
    modo = "simulado" if args.simulado else "real"
    modo_guardado = oficina.db.leer("modo")
    if modo_guardado and modo_guardado != modo:
        print(f"La base {cfg.base_de_datos} tiene operaciones en modo {modo_guardado}; no se mezclan con el modo {modo}.\n"
              f"Cambiá 'base_de_datos' en {args.config} o borrá ese archivo para empezar de cero.", file=sys.stderr)
        return 1
    oficina.db.escribir("modo", modo)
    intervalo = cfg.intervalo_segundos if args.intervalo is None else args.intervalo
    visto = (oficina.db.bitacora(1) or [{"id": 0}])[-1]["id"]
    print(f"Oficina abierta ({'simulada' if args.simulado else 'precios reales'}). Ctrl+C para salir.")
    n = 0
    try:
        while not args.ciclos or n < args.ciclos:
            try:
                oficina.ciclo()
            except Exception as e:  # un error de red no debe tirar la oficina
                print(f"[error en ciclo] {e}", file=sys.stderr)
            for e in oficina.db.con.execute("SELECT * FROM bitacora WHERE id > ? ORDER BY id", (visto,)):
                print(f"{hora(e['ts'])}  {e['actor']:<12} {e['mensaje']}")
                visto = e["id"]
            n += 1
            if intervalo:
                time.sleep(intervalo)
    except KeyboardInterrupt:
        pass
    print()
    mostrar_estado(cfg, oficina.central)
    return 0


def mostrar_estado(cfg, central: Central) -> None:
    db = central.db
    precios = db.leer("ultimos_precios")
    if not precios:
        print("Todavía no corrió ningún ciclo. Usá: python -m sala_de_mando correr --simulado")
        return
    perdida, perdida_total = central.perdida_del_dia(precios)
    kill = db.leer("kill_switch")
    print(f"Kill switch: {'ACTIVO' if kill else 'no'}   ·   Resultado del día total: {-perdida_total:+.2f} %")
    for nombre, sala in cfg.salas.items():
        pat = central.patrimonio(nombre, precios)
        exp = central.expuesto(nombre, precios)
        pausa = "  [EN PAUSA]" if db.leer(f"pausa:sala:{nombre}") else ""
        print(f"\nSALA {nombre.upper()}{pausa}")
        print(f"  Patrimonio {pat:,.2f} {sala.moneda} (inicial {sala.capital_inicial:,.2f})  ·  "
              f"hoy {-perdida[nombre]:+.2f} % (límite -{sala.perdida_diaria_max_pct} %)  ·  "
              f"exposición {exp / pat * 100 if pat else 0:.1f} %")
        for p in db.posiciones(nombre):
            actual = precios[p.simbolo]
            var = (actual / p.precio_promedio - 1) * 100
            print(f"    {p.bot:<12} {p.simbolo:<10} {p.cantidad:.6g} @ {p.precio_promedio:,.2f} → {actual:,.2f} ({var:+.2f} %)")
    automaticos = central.bots_automaticos()
    print("\nBOTS")
    for b in cfg.bots:
        pausa = "  [EN PAUSA]" if db.leer(f"pausa:bot:{b.nombre}") else ""
        modo = "automático" if b.nombre in automaticos else "con aprobación"
        print(f"  {b.nombre:<12} {b.sala:<9} {b.estrategia:<14} {modo}{pausa}")
    pendientes = db.propuestas(EstadoPropuesta.PENDIENTE)
    if pendientes:
        print(f"\n{len(pendientes)} orden(es) esperan tu aprobación: python -m sala_de_mando pendientes")


def mostrar_pendientes(db: Almacen) -> None:
    pendientes = db.propuestas(EstadoPropuesta.PENDIENTE)
    if not pendientes:
        print("No hay nada esperando aprobación.")
        return
    for p in pendientes:
        decision = db.con.execute("SELECT decision FROM propuestas WHERE id=?", (p.id,)).fetchone()[0]
        print(f"#{p.id}  {hora(p.ts)[:5]}  {p.bot} · {p.lado.value} {p.cantidad:.6g} {p.simbolo} "
              f"(~{p.monto:,.2f}) · {p.motivo}\n      Por qué espera: {decision}")
    print("\nAprobar: python -m sala_de_mando aprobar ID   ·   Rechazar: python -m sala_de_mando rechazar ID")


def mostrar_ranking(cfg, db: Almacen) -> None:
    precios = db.leer("ultimos_precios") or {}
    filas = defaultdict(lambda: {"realizado": 0.0, "abierto": 0.0, "ops": 0, "ganadas": 0})
    for op in db.operaciones(100000):
        if op["lado"] == "venta":
            f = filas[op["bot"]]
            f["realizado"] += op["resultado"]
            f["ops"] += 1
            f["ganadas"] += op["resultado"] > 0
    for p in db.posiciones():
        filas[p.bot]["abierto"] += (precios.get(p.simbolo, p.precio_promedio) - p.precio_promedio) * p.cantidad
    orden = sorted(cfg.bots, key=lambda b: -(filas[b.nombre]["realizado"] + filas[b.nombre]["abierto"]))
    print(f"{'BOT':<12} {'SALA':<9} {'CERRADO':>10} {'ABIERTO':>10} {'OPS':>5} {'ACIERTO':>8}")
    for b in orden:
        f = filas[b.nombre]
        acierto = f"{f['ganadas'] / f['ops'] * 100:.0f} %" if f["ops"] else "-"
        print(f"{b.nombre:<12} {b.sala:<9} {f['realizado']:>+10.2f} {f['abierto']:>+10.2f} {f['ops']:>5} {acierto:>8}")


if __name__ == "__main__":
    sys.exit(main())
