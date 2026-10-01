"""Persistencia en SQLite: cuentas, posiciones, propuestas, operaciones, estado y bitácora.

Todo vive en la base para que el ciclo de la oficina y los comandos que corrés
desde otra terminal (aprobar, pausar, kill switch) vean el mismo estado.
"""
from __future__ import annotations

import json
import sqlite3
from datetime import datetime

from .modelos import EstadoPropuesta, Lado, Posicion, Propuesta, ahora

ESQUEMA = """
CREATE TABLE IF NOT EXISTS cuentas (
    sala TEXT PRIMARY KEY,
    efectivo REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS posiciones (
    sala TEXT NOT NULL,
    bot TEXT NOT NULL,
    simbolo TEXT NOT NULL,
    cantidad REAL NOT NULL,
    precio_promedio REAL NOT NULL,
    PRIMARY KEY (sala, bot, simbolo)
);
CREATE TABLE IF NOT EXISTS propuestas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    bot TEXT NOT NULL,
    sala TEXT NOT NULL,
    simbolo TEXT NOT NULL,
    lado TEXT NOT NULL,
    cantidad REAL NOT NULL,
    precio REAL NOT NULL,
    motivo TEXT NOT NULL,
    estado TEXT NOT NULL,
    decision TEXT NOT NULL DEFAULT ''
);
CREATE TABLE IF NOT EXISTS operaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    sala TEXT NOT NULL,
    bot TEXT NOT NULL,
    simbolo TEXT NOT NULL,
    lado TEXT NOT NULL,
    cantidad REAL NOT NULL,
    precio REAL NOT NULL,
    comision REAL NOT NULL,
    resultado REAL NOT NULL DEFAULT 0,
    propuesta_id INTEGER
);
CREATE TABLE IF NOT EXISTS estado (
    clave TEXT PRIMARY KEY,
    valor TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS bitacora (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ts TEXT NOT NULL,
    tipo TEXT NOT NULL,
    actor TEXT NOT NULL,
    mensaje TEXT NOT NULL
);
"""


class Almacen:
    def __init__(self, ruta: str):
        self.con = sqlite3.connect(ruta, timeout=30, isolation_level=None)
        self.con.row_factory = sqlite3.Row
        self.con.execute("PRAGMA journal_mode=WAL")
        self.con.executescript(ESQUEMA)

    # --- estado general (pausas, kill switch, inicio del día) ---

    def leer(self, clave: str, defecto=None):
        fila = self.con.execute("SELECT valor FROM estado WHERE clave=?", (clave,)).fetchone()
        return json.loads(fila["valor"]) if fila else defecto

    def escribir(self, clave: str, valor) -> None:
        self.con.execute(
            "INSERT INTO estado(clave, valor) VALUES(?, ?) "
            "ON CONFLICT(clave) DO UPDATE SET valor=excluded.valor",
            (clave, json.dumps(valor)),
        )

    def borrar(self, clave: str) -> None:
        self.con.execute("DELETE FROM estado WHERE clave=?", (clave,))

    # --- bitácora ---

    def anotar(self, tipo: str, actor: str, mensaje: str) -> None:
        self.con.execute(
            "INSERT INTO bitacora(ts, tipo, actor, mensaje) VALUES(?, ?, ?, ?)",
            (ahora().isoformat(), tipo, actor, mensaje),
        )

    def bitacora(self, limite: int = 30) -> list[sqlite3.Row]:
        filas = self.con.execute(
            "SELECT * FROM bitacora ORDER BY id DESC LIMIT ?", (limite,)
        ).fetchall()
        return list(reversed(filas))

    # --- cuentas y posiciones ---

    def crear_cuenta_si_falta(self, sala: str, efectivo: float) -> None:
        self.con.execute(
            "INSERT OR IGNORE INTO cuentas(sala, efectivo) VALUES(?, ?)", (sala, efectivo)
        )

    def efectivo(self, sala: str) -> float:
        fila = self.con.execute("SELECT efectivo FROM cuentas WHERE sala=?", (sala,)).fetchone()
        return fila["efectivo"] if fila else 0.0

    def posiciones(self, sala: str | None = None, bot: str | None = None) -> list[Posicion]:
        consulta, args = "SELECT * FROM posiciones WHERE cantidad > 0", []
        if sala:
            consulta += " AND sala=?"
            args.append(sala)
        if bot:
            consulta += " AND bot=?"
            args.append(bot)
        return [
            Posicion(f["sala"], f["bot"], f["simbolo"], f["cantidad"], f["precio_promedio"])
            for f in self.con.execute(consulta, args)
        ]

    def posicion(self, sala: str, bot: str, simbolo: str) -> Posicion | None:
        f = self.con.execute(
            "SELECT * FROM posiciones WHERE sala=? AND bot=? AND simbolo=? AND cantidad > 0",
            (sala, bot, simbolo),
        ).fetchone()
        return Posicion(f["sala"], f["bot"], f["simbolo"], f["cantidad"], f["precio_promedio"]) if f else None

    def registrar_operacion(
        self,
        *,
        sala: str,
        bot: str,
        simbolo: str,
        lado: Lado,
        cantidad: float,
        precio: float,
        comision: float,
        propuesta_id: int | None,
    ) -> float:
        """Mueve efectivo y posición en una sola transacción. Devuelve el resultado realizado."""
        resultado = 0.0
        with self._transaccion():
            pos = self.posicion(sala, bot, simbolo)
            if lado == Lado.COMPRA:
                cant_prev = pos.cantidad if pos else 0.0
                prom_prev = pos.precio_promedio if pos else 0.0
                nueva = cant_prev + cantidad
                promedio = (cant_prev * prom_prev + cantidad * precio) / nueva
                self._guardar_posicion(sala, bot, simbolo, nueva, promedio)
                self.con.execute(
                    "UPDATE cuentas SET efectivo = efectivo - ? WHERE sala=?",
                    (cantidad * precio + comision, sala),
                )
            else:
                resultado = (precio - pos.precio_promedio) * cantidad - comision
                self._guardar_posicion(sala, bot, simbolo, pos.cantidad - cantidad, pos.precio_promedio)
                self.con.execute(
                    "UPDATE cuentas SET efectivo = efectivo + ? WHERE sala=?",
                    (cantidad * precio - comision, sala),
                )
            self.con.execute(
                "INSERT INTO operaciones(ts, sala, bot, simbolo, lado, cantidad, precio, comision, resultado, propuesta_id) "
                "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (ahora().isoformat(), sala, bot, simbolo, lado.value, cantidad, precio, comision, resultado, propuesta_id),
            )
        return resultado

    def _guardar_posicion(self, sala, bot, simbolo, cantidad, promedio) -> None:
        if cantidad <= 1e-12:
            self.con.execute(
                "DELETE FROM posiciones WHERE sala=? AND bot=? AND simbolo=?", (sala, bot, simbolo)
            )
            return
        self.con.execute(
            "INSERT INTO posiciones(sala, bot, simbolo, cantidad, precio_promedio) VALUES(?, ?, ?, ?, ?) "
            "ON CONFLICT(sala, bot, simbolo) DO UPDATE SET cantidad=excluded.cantidad, "
            "precio_promedio=excluded.precio_promedio",
            (sala, bot, simbolo, cantidad, promedio),
        )

    def operaciones(self, limite: int = 1000) -> list[sqlite3.Row]:
        return self.con.execute(
            "SELECT * FROM operaciones ORDER BY id DESC LIMIT ?", (limite,)
        ).fetchall()

    # --- propuestas ---

    def guardar_propuesta(self, p: Propuesta, estado: EstadoPropuesta, decision: str) -> int:
        cur = self.con.execute(
            "INSERT INTO propuestas(ts, bot, sala, simbolo, lado, cantidad, precio, motivo, estado, decision) "
            "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (p.ts.isoformat(), p.bot, p.sala, p.simbolo, p.lado.value, p.cantidad, p.precio,
             p.motivo, estado.value, decision),
        )
        p.id = cur.lastrowid
        return p.id

    def cambiar_estado_propuesta(self, id_: int, estado: EstadoPropuesta, decision: str | None = None) -> None:
        if decision is None:
            self.con.execute("UPDATE propuestas SET estado=? WHERE id=?", (estado.value, id_))
        else:
            self.con.execute(
                "UPDATE propuestas SET estado=?, decision=? WHERE id=?", (estado.value, decision, id_)
            )

    def propuestas(self, estado: EstadoPropuesta) -> list[Propuesta]:
        filas = self.con.execute(
            "SELECT * FROM propuestas WHERE estado=? ORDER BY id", (estado.value,)
        ).fetchall()
        return [self._a_propuesta(f) for f in filas]

    def propuesta(self, id_: int) -> tuple[Propuesta, EstadoPropuesta] | None:
        f = self.con.execute("SELECT * FROM propuestas WHERE id=?", (id_,)).fetchone()
        return (self._a_propuesta(f), EstadoPropuesta(f["estado"])) if f else None

    @staticmethod
    def _a_propuesta(f: sqlite3.Row) -> Propuesta:
        return Propuesta(
            id=f["id"], ts=datetime.fromisoformat(f["ts"]), bot=f["bot"], sala=f["sala"],
            simbolo=f["simbolo"], lado=Lado(f["lado"]), cantidad=f["cantidad"],
            precio=f["precio"], motivo=f["motivo"],
        )

    def _transaccion(self):
        return _Transaccion(self.con)


class _Transaccion:
    def __init__(self, con: sqlite3.Connection):
        self.con = con

    def __enter__(self):
        self.con.execute("BEGIN IMMEDIATE")

    def __exit__(self, tipo, *_):
        self.con.execute("ROLLBACK" if tipo else "COMMIT")
