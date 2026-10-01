# Sala de mando

Oficina de trading **simulada** con bots organizados en salas (cripto y acciones) y una
**central de habilitaciones** por la que pasa cada orden. Ningún bot opera directo: proponen,
la central decide y, si corresponde, te pide aprobación.

> Todo opera **en papel** (dinero ficticio). No hay conexión a cuentas reales.
> Las estrategias incluidas son ejemplos simples para probar el circuito, no recomendaciones de inversión.

```
 Bots (estrategias) ──propuesta──►  CENTRAL DE HABILITACIONES ──aprobada──► Broker en papel
   Sala Cripto                       · reglas de riesgo                         (efectivo, posiciones,
   Sala Acciones                     · permisos por sala / bot / activo          comisiones, resultado)
                                     · cola de aprobación (tu OK)
                                     · pausas y kill switch
                                     · bitácora de todo
```

## Cómo decide la central

Cada propuesta termina en uno de tres estados:

| Resultado | Cuándo |
|---|---|
| **Rechazada** | Kill switch activo · sala o bot en pausa · activo no habilitado en la sala o para ese bot · mercado cerrado · la pérdida del día llegó al límite (de la sala o total) · la orden supera el máximo por orden · falta efectivo · la exposición quedaría por encima del máximo · ya hay demasiados activos abiertos |
| **Pendiente (espera tu OK)** | La orden supera el umbral de aprobación (por defecto 5 % del patrimonio de la sala) · el bot está en modo `aprobacion` |
| **Aprobada** | Pasa todo lo anterior: se ejecuta sola |

- Las **ventas** que cierran posiciones nunca necesitan tu OK (bajan el riesgo), y siguen permitidas aunque se haya alcanzado el límite de pérdida diaria.
- Lo que aprobás se ejecuta en el próximo ciclo **volviendo a chequear los límites** con el precio de ese momento.
- Una orden pendiente vence a los 30 minutos si no respondés.
- El **kill switch** cierra todas las posiciones, cancela las pendientes y bloquea compras hasta que lo reabras.

Todos los límites se cambian en [`config.toml`](config.toml).

## Instalación

Requiere Python 3.11 o más nuevo.

```bash
python -m venv .venv
source .venv/bin/activate          # En Windows: .venv\Scripts\activate
pip install -r requirements.txt    # solo para precios reales
```

## Uso

**Simulación sin internet** (precios inventados, ideal para probar):

```bash
python -m sala_de_mando correr --simulado --intervalo 1
```

**Precios reales** (Binance para cripto, Yahoo para acciones; la ejecución sigue en papel):

```bash
python -m sala_de_mando correr
```

Con la oficina corriendo, abrí **otra terminal** para manejarla:

```bash
python -m sala_de_mando estado                    # patrimonio, posiciones, bots
python -m sala_de_mando pendientes                # órdenes esperando tu OK
python -m sala_de_mando aprobar 12
python -m sala_de_mando rechazar 13
python -m sala_de_mando pausar sala cripto        # o: pausar bot Halcon
python -m sala_de_mando reanudar sala cripto
python -m sala_de_mando habilitar Halcon automatico   # o: aprobacion
python -m sala_de_mando kill                      # cierra todo
python -m sala_de_mando reabrir
python -m sala_de_mando ranking                   # resultado por bot
python -m sala_de_mando bitacora -n 50
```

La simulación y el modo con precios reales no se mezclan en la misma base de datos: para cambiar de
modo, cambiá `base_de_datos` en `config.toml` o borrá `sala_de_mando.db`.

## Bots incluidos

| Bot | Sala | Estrategia | Modo inicial |
|---|---|---|---|
| Tortuga | cripto | cruce de medias (10/30) | automático |
| Rebote | cripto | RSI en sobreventa | automático |
| Halcon | cripto | ruptura de máximos | con aprobación |
| Indice | acciones | cruce de medias (20/50) en SPY | automático, pero sus órdenes de 8 % superan el umbral de 5 % y esperan tu OK |
| Paciente | acciones | RSI en sobreventa | automático |
| Ruptor | acciones | ruptura de máximos | con aprobación |

Para agregar un bot, sumá un bloque `[[bots]]` en `config.toml`. Para una estrategia nueva, creá una
clase en `sala_de_mando/bots/estrategias.py` y registrala en `sala_de_mando/bots/__init__.py`.

## Desde Argentina: próximos pasos hacia operar de verdad

Hoy todo es en papel. Para conectar ejecución real habría que sumar un "ejecutor" por broker detrás de la
central (la central y las reglas no cambian):

- **Cripto:** Binance tiene una *testnet* (dinero ficticio con su motor real) y CCXT ya la soporta; es el paso natural antes de dinero real.
- **Acciones de EE.UU.:** Alpaca ofrece cuenta de práctica (*paper trading*) gratis con API. Para dinero real desde Argentina, Interactive Brokers acepta residentes argentinos.
- **CEDEARs y acciones locales (BYMA):** InvertirOnline (IOL) y Portfolio Personal Inversiones (PPI) tienen API. El horario de BYMA es distinto al de Nueva York.

Antes de elegir, revisá las condiciones vigentes de cada broker (requisitos de apertura, costos, acceso a la API) y el tratamiento impositivo.

## Hoja de ruta

1. **Fase 1 (esta):** central de habilitaciones, broker en papel, 6 bots, control por línea de comandos.
2. **Fase 2:** panel web "Sala de mando" (basado en el diseño) con aprobación con un clic, pausas y kill switch.
3. **Fase 3:** backtesting de cada estrategia antes de habilitarla, comité que propone pausar bots que pierden, ranking histórico.
4. **Fase 4:** ejecución en testnet / cuentas de práctica y, recién después, evaluar dinero real.

## Tests

```bash
pip install -r requirements-dev.txt
python -m pytest
```
