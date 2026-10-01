from datetime import datetime, timedelta
from pathlib import Path

import pytest

from sala_de_mando import config as configuracion
from sala_de_mando.almacen import Almacen
from sala_de_mando.central import Central
from sala_de_mando.mercado import NUEVA_YORK, MercadoSimulado, mercado_abierto
from sala_de_mando.modelos import EstadoPropuesta, Lado, Propuesta, Veredicto, ahora
from sala_de_mando.oficina import Oficina

CONFIG = Path(__file__).resolve().parent.parent / "config.toml"
P = {"BTC/USDT": 50000.0, "ETH/USDT": 2500.0, "SOL/USDT": 100.0,
     "SPY": 500.0, "AAPL": 200.0, "MSFT": 400.0, "NVDA": 100.0}


@pytest.fixture
def cfg():
    c = configuracion.cargar(CONFIG)
    c.respetar_horario_acciones = False
    return c


@pytest.fixture
def central(cfg):
    return Central(cfg, Almacen(":memory:"))


def propuesta(bot="Tortuga", simbolo="BTC/USDT", lado=Lado.COMPRA, monto=200.0, sala="cripto"):
    return Propuesta(bot=bot, sala=sala, simbolo=simbolo, lado=lado,
                     cantidad=monto / P[simbolo], precio=P[simbolo], motivo="test")


def test_compra_chica_de_bot_automatico_se_ejecuta(central):
    res = central.procesar(propuesta(monto=200), P)  # 4 % de 5000
    assert res.veredicto == Veredicto.APROBADA
    assert central.db.posicion("cripto", "Tortuga", "BTC/USDT").cantidad == pytest.approx(200 / 50000)
    assert central.db.efectivo("cripto") < 5000 - 200


def test_orden_grande_espera_aprobacion(central):
    res = central.procesar(propuesta(monto=400), P)  # 8 %: entre 5 % y 10 %
    assert res.veredicto == Veredicto.PENDIENTE
    assert central.db.posiciones() == []


def test_orden_que_supera_maximo_se_rechaza(central):
    res = central.procesar(propuesta(monto=600), P)  # 12 %
    assert res.veredicto == Veredicto.RECHAZADA
    assert any("supera el máximo" in m for m in res.motivos)


def test_bot_en_modo_aprobacion_espera_ok(central):
    res = central.procesar(propuesta(bot="Halcon", monto=100), P)
    assert res.veredicto == Veredicto.PENDIENTE
    assert any("aprobación manual" in m for m in res.motivos)


def test_habilitar_bot_lo_vuelve_automatico(central):
    central.habilitar_bot("Halcon", "automatico")
    assert central.procesar(propuesta(bot="Halcon", monto=100), P).veredicto == Veredicto.APROBADA


def test_activo_no_habilitado_para_el_bot(central):
    res = central.procesar(propuesta(simbolo="SOL/USDT"), P)  # Tortuga solo opera BTC y ETH
    assert res.veredicto == Veredicto.RECHAZADA


def test_bot_no_puede_operar_en_otra_sala(central):
    res = central.procesar(propuesta(bot="Tortuga", simbolo="SPY", sala="acciones"), P)
    assert res.veredicto == Veredicto.RECHAZADA


def test_pausas(central):
    central.pausar("sala", "cripto")
    assert central.procesar(propuesta(), P).veredicto == Veredicto.RECHAZADA
    central.pausar("sala", "cripto", False)
    central.pausar("bot", "Tortuga")
    assert central.procesar(propuesta(), P).veredicto == Veredicto.RECHAZADA
    central.pausar("bot", "Tortuga", False)
    assert central.procesar(propuesta(), P).veredicto == Veredicto.APROBADA


def test_exposicion_maxima(central, cfg):
    cfg.salas["cripto"].orden_max_pct = 100
    cfg.salas["cripto"].aprobacion_desde_pct = 100
    assert central.procesar(propuesta(monto=2500), P).veredicto == Veredicto.APROBADA  # 50 %
    res = central.procesar(propuesta(simbolo="ETH/USDT", monto=600), P)  # llevaría a 62 %
    assert res.veredicto == Veredicto.RECHAZADA
    assert any("exposición" in m for m in res.motivos)


def test_perdida_diaria_bloquea_compras_pero_no_ventas(central):
    central.procesar(propuesta(monto=200), P)
    central.actualizar_inicio_del_dia(P)
    inicio = central.db.leer("inicio_dia")
    inicio["patrimonio"]["cripto"] = 6000  # simula que hoy se perdió ~17 %
    central.db.escribir("inicio_dia", inicio)

    assert central.procesar(propuesta(simbolo="ETH/USDT"), P).veredicto == Veredicto.RECHAZADA
    cantidad = central.db.posicion("cripto", "Tortuga", "BTC/USDT").cantidad
    venta = Propuesta(bot="Tortuga", sala="cripto", simbolo="BTC/USDT", lado=Lado.VENTA,
                      cantidad=cantidad, precio=P["BTC/USDT"], motivo="test")
    assert central.procesar(venta, P).veredicto == Veredicto.APROBADA
    assert central.db.posiciones() == []


def test_venta_mayor_a_la_posicion_se_rechaza(central):
    res = central.procesar(propuesta(lado=Lado.VENTA, monto=100), P)
    assert res.veredicto == Veredicto.RECHAZADA


def test_aprobar_ejecuta_en_el_proximo_ciclo(central):
    central.procesar(propuesta(monto=400), P)
    id_ = central.db.propuestas(EstadoPropuesta.PENDIENTE)[0].id
    assert "aprobada" in central.aprobar(id_)
    assert central.db.posiciones() == []
    central.procesar_aprobadas(P)
    assert central.db.propuesta(id_)[1] == EstadoPropuesta.EJECUTADA
    assert central.db.posicion("cripto", "Tortuga", "BTC/USDT") is not None


def test_aprobada_se_revalida_con_el_kill_switch(central):
    central.procesar(propuesta(monto=400), P)
    id_ = central.db.propuestas(EstadoPropuesta.PENDIENTE)[0].id
    central.aprobar(id_)
    central.db.escribir("kill_switch", "activo")
    central.procesar_aprobadas(P)
    assert central.db.propuesta(id_)[1] == EstadoPropuesta.RECHAZADA
    assert central.db.posiciones() == []


def test_pendiente_vence(central):
    p = propuesta(monto=400)
    p.ts = ahora() - timedelta(hours=2)
    central.procesar(p, P)
    central.vencer_pendientes()
    assert central.db.propuesta(p.id)[1] == EstadoPropuesta.VENCIDA


def test_kill_switch_cierra_todo_y_bloquea(central):
    central.procesar(propuesta(monto=200), P)
    central.procesar(propuesta(bot="Paciente", simbolo="AAPL", sala="acciones", monto=200), P)
    central.procesar(propuesta(monto=400), P)  # queda pendiente
    central.pedir_kill_switch()
    central.aplicar_kill_switch(P)
    assert central.db.posiciones() == []
    assert central.db.propuestas(EstadoPropuesta.PENDIENTE) == []
    assert central.procesar(propuesta(), P).veredicto == Veredicto.RECHAZADA
    central.reabrir()
    assert central.procesar(propuesta(), P).veredicto == Veredicto.APROBADA


def test_resultado_de_compra_y_venta():
    db = Almacen(":memory:")
    db.crear_cuenta_si_falta("cripto", 1000)
    db.registrar_operacion(sala="cripto", bot="b", simbolo="X", lado=Lado.COMPRA,
                           cantidad=2, precio=100, comision=1, propuesta_id=None)
    assert db.efectivo("cripto") == pytest.approx(799)
    r = db.registrar_operacion(sala="cripto", bot="b", simbolo="X", lado=Lado.VENTA,
                               cantidad=2, precio=110, comision=1, propuesta_id=None)
    assert r == pytest.approx(19)
    assert db.efectivo("cripto") == pytest.approx(1018)
    assert db.posiciones() == []


def test_horario_de_acciones():
    martes = datetime(2026, 9, 29, 10, 0, tzinfo=NUEVA_YORK)
    assert mercado_abierto("acciones", martes)
    assert not mercado_abierto("acciones", martes.replace(hour=17))
    assert not mercado_abierto("acciones", datetime(2026, 10, 3, 12, 0, tzinfo=NUEVA_YORK))  # sábado
    assert mercado_abierto("cripto", datetime(2026, 10, 3, 3, 0, tzinfo=NUEVA_YORK))


def test_simulacion_completa_respeta_los_limites(cfg):
    oficina = Oficina(cfg, MercadoSimulado(oficina_simbolos(cfg), semilla=1), Almacen(":memory:"))
    for _ in range(500):
        oficina.ciclo()
        for sala in cfg.salas:
            assert oficina.db.efectivo(sala) >= 0
    assert len(oficina.db.operaciones()) > 0
    for p in oficina.db.posiciones():
        bot = cfg.bot(p.bot)
        assert p.simbolo in bot.activos and p.sala == bot.sala


def oficina_simbolos(cfg):
    return sorted({s for sala in cfg.salas.values() for s in sala.activos})


def test_config_rechaza_bot_con_activo_no_habilitado(tmp_path):
    ruta = tmp_path / "c.toml"
    ruta.write_text(CONFIG.read_text().replace('activos = ["SPY"]', 'activos = ["TSLA"]'))
    with pytest.raises(ValueError, match="no habilitados"):
        configuracion.cargar(ruta)
