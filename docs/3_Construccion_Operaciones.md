# Construcción de Operaciones

Para ejecutar todos los ejemplos se debe importar la librería. Se sugiere utilizar siempre el alias `qcf`. 


```python
import qcfinancial as qcf
from qcfinancial import FxFixingLagAppliesTo

import aux_functions as aux
import pandas as pd
```


```python
qcf.id()
```




    'version: 1.6.1, build: 2025-06-06 09:09'



## Legs

Los objetos de tipo `Leg` son una lista (o vector) de objetos `Cashflow` y representan una pata de un instrumento financiero. Un objeto de tipo `Leg` puede construirse *a mano* es decir, dando de alta cashflows y agregándolos uno a uno o con algunos métodos de conveniencia cuyo funcionamiento se mostrará.

### Construcción Manual

Se verá como construir un `Leg` con 2 `SimpleCashflow` de forma *manual*. En particular, este objeto `Leg` podría representar una operación FX por entrega física.

Primero se construye dos objetos de tipo `SimpleCashflow`:


```python
fecha_vencimiento = qcf.QCDate(23, 9, 2024)

simple_cashflow_1 = qcf.SimpleCashflow(
    fecha_vencimiento,    # fecha del flujo
    1_000,         # monto
    qcf.QCUSD()    # moneda
) 

simple_cashflow_2 = qcf.SimpleCashflow(
    fecha_vencimiento,    # fecha del flujo
    -900_000,      # monto
    qcf.QCCLP())   # moneda
```

Con esto, se construye un objeto de tipo `Leg`. En este momento el objeto está vacío.


```python
leg = qcf.Leg()
```


```python
leg.size()
```




    0



Agregamos los dos cashflows.


```python
leg.append_cashflow(simple_cashflow_1)
leg.append_cashflow(simple_cashflow_2)
```

Se observa el resultado (usamos la función del módulo `aux_functions` que a su vez depende del método `show`).


```python
df = aux.leg_as_dataframe(leg)
df.style.format(aux.format_dict)
```




<style type="text/css">
</style>
<table id="T_3ff1e">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_3ff1e_level0_col0" class="col_heading level0 col0" >fecha_pago</th>
      <th id="T_3ff1e_level0_col1" class="col_heading level0 col1" >monto</th>
      <th id="T_3ff1e_level0_col2" class="col_heading level0 col2" >moneda</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_3ff1e_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_3ff1e_row0_col0" class="data row0 col0" >2024-09-23</td>
      <td id="T_3ff1e_row0_col1" class="data row0 col1" >1,000.00</td>
      <td id="T_3ff1e_row0_col2" class="data row0 col2" >USD</td>
    </tr>
    <tr>
      <th id="T_3ff1e_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_3ff1e_row1_col0" class="data row1 col0" >2024-09-23</td>
      <td id="T_3ff1e_row1_col1" class="data row1 col1" >-900,000.00</td>
      <td id="T_3ff1e_row1_col2" class="data row1 col2" >CLP</td>
    </tr>
  </tbody>
</table>




Agregar todo tipo de cashflows a un mismo objeto `Leg` entrega mucha flexibilidad para construir operaciones con estructuras complicadas. Partiremos, sin embargo, explicando como construir objetos `Leg` a partir de cashflows del mismo tipo.

## Construcción Asistida de un `FixedRateLeg`

Se verá como construir objetos `Leg` donde cada `Cashflow` es un objeto de tipo `FixedRateCashflow`, todos con la misma tasa fija. En el primer ejemplo se construye un `Leg` de tipo *bullet*: una única amortización igual al capital vigente de todos los `FixedRateCasflow` en el último flujo.

Se requieren los siguientes parámetros, los cuales permitirán construir las variedades más comunes de `FixedRateLeg`, entre las cuales están las utilizadas en las operaciones estándar de mercado.

- `RecPay`: enum que indica si los flujos se reciben o pagan
- `QCDate`: fecha de inicio del primer flujo
- `QCDate`: fecha final del último flujo sin considerar ajustes de días feriados
- `BusyAdRules`: enum que representa el tipo de ajuste en la fecha final para días feriados (FOLLOW, MOD_FOLLOW)
- `Tenor`: la periodicidad de pago
- `QCInterestRateLeg::QCStubPeriod`: enum que representa el tipo de período irregular (si aplica)
- `QCBusinessCalendar`: calendario que aplica para los ajustes de fechas y fechas de pago
- `unsigned int`: lag de pago expresado en días
- `float`: nominal inicial
- `bool`: si es `True` significa que la amortización es un flujo de caja efectivo
- `QCInterestRate`: la tasa a aplicar en cada flujo
- `QCCurrency`: moneda del nominal y de los flujos
- `bool`: si es `True` fuerza a que las fechas de pago coincidan con las fechas finales. Esto para lograr una valorización acorde a las convenciones de los mercados de renta fija, en caso que la `Leg` represente un bono a tasa fija.
- `SettLagBehaviour`: este parámetro indica cómo se calcula un `settlement_date` cuando un `end_date` cae en un día festivo y no se ha definido un ajuste en las fechas finales. Las alternativas son dos, se calcula sumando el `settlement_lag` desde `end_date` o se calcula sumando `settlement_lag` a partir de la primera fecha hábil posterior a `end_date`.

El parámetro `SettLagBehaviour` se agregó en la versión 0.11.0 .

Vamos a un ejemplo.

Se da de alta los parámetros requeridos


```python
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(29, 7, 2024)
fecha_final = qcf.QCDate(29, 7, 2026)
bus_adj_rule = qcf.BusyAdjRules.FOLLOW
periodicidad = qcf.Tenor('6M')
periodo_irregular = qcf.StubPeriod.NO
calendario = aux.get_business_calendar('CL', range(2024, 2027))  # Se apoya en holidays
lag_pago = 0
nominal = 100_000_000.0
amort_es_flujo = True
valor_tasa = .05
tasa_cupon = qcf.QCInterestRate(valor_tasa, qcf.QCAct360(), qcf.QCLinearWf())
moneda = qcf.QCCLP()
es_bono = False
```

Este argumento tiene como valor por default `qcf.SettLagBehaviour.DONT_MOVE`. Aquí, por claridad, se define explícitamente.


```python
sett_lag_behaviour = qcf.SettLagBehaviour.DONT_MOVE
```

Se da de alta el objeto.


```python
fixed_rate_leg = qcf.LegFactory.build_bullet_fixed_rate_leg(
    rec_pay=rp,
    start_date=fecha_inicio,
    end_date=fecha_final,
    bus_adj_rule=bus_adj_rule,
    settlement_periodicity=periodicidad,
    settlement_stub_period=periodo_irregular,
    settlement_calendar=calendario,
    settlement_lag=lag_pago,
    initial_notional=nominal,
    amort_is_cashflow=amort_es_flujo,
    interest_rate=tasa_cupon,
    notional_currency=moneda,
    is_bond=es_bono,
    sett_lag_behaviour=sett_lag_behaviour,
)
```

Como en el capítulo anterior, se puede lograr una muy buena visualización del resultado utilizando un `pandas.Dataframe` de pandas y el método `show`.


```python
df = aux.leg_as_dataframe(fixed_rate_leg)
df.style.format(aux.format_dict)
```




<style type="text/css">
</style>
<table id="T_b3bd7">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_b3bd7_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_b3bd7_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_b3bd7_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_b3bd7_level0_col3" class="col_heading level0 col3" >nocional</th>
      <th id="T_b3bd7_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_b3bd7_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_b3bd7_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_b3bd7_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_b3bd7_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_b3bd7_level0_col9" class="col_heading level0 col9" >valor_tasa</th>
      <th id="T_b3bd7_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_b3bd7_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_b3bd7_row0_col0" class="data row0 col0" >2024-07-29</td>
      <td id="T_b3bd7_row0_col1" class="data row0 col1" >2025-01-29</td>
      <td id="T_b3bd7_row0_col2" class="data row0 col2" >2025-01-29</td>
      <td id="T_b3bd7_row0_col3" class="data row0 col3" >100,000,000.00</td>
      <td id="T_b3bd7_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_b3bd7_row0_col5" class="data row0 col5" >2,555,555.56</td>
      <td id="T_b3bd7_row0_col6" class="data row0 col6" >True</td>
      <td id="T_b3bd7_row0_col7" class="data row0 col7" >2,555,555.56</td>
      <td id="T_b3bd7_row0_col8" class="data row0 col8" >CLP</td>
      <td id="T_b3bd7_row0_col9" class="data row0 col9" >5.0000%</td>
      <td id="T_b3bd7_row0_col10" class="data row0 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_b3bd7_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_b3bd7_row1_col0" class="data row1 col0" >2025-01-29</td>
      <td id="T_b3bd7_row1_col1" class="data row1 col1" >2025-07-29</td>
      <td id="T_b3bd7_row1_col2" class="data row1 col2" >2025-07-29</td>
      <td id="T_b3bd7_row1_col3" class="data row1 col3" >100,000,000.00</td>
      <td id="T_b3bd7_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_b3bd7_row1_col5" class="data row1 col5" >2,513,888.89</td>
      <td id="T_b3bd7_row1_col6" class="data row1 col6" >True</td>
      <td id="T_b3bd7_row1_col7" class="data row1 col7" >2,513,888.89</td>
      <td id="T_b3bd7_row1_col8" class="data row1 col8" >CLP</td>
      <td id="T_b3bd7_row1_col9" class="data row1 col9" >5.0000%</td>
      <td id="T_b3bd7_row1_col10" class="data row1 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_b3bd7_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_b3bd7_row2_col0" class="data row2 col0" >2025-07-29</td>
      <td id="T_b3bd7_row2_col1" class="data row2 col1" >2026-01-29</td>
      <td id="T_b3bd7_row2_col2" class="data row2 col2" >2026-01-29</td>
      <td id="T_b3bd7_row2_col3" class="data row2 col3" >100,000,000.00</td>
      <td id="T_b3bd7_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_b3bd7_row2_col5" class="data row2 col5" >2,555,555.56</td>
      <td id="T_b3bd7_row2_col6" class="data row2 col6" >True</td>
      <td id="T_b3bd7_row2_col7" class="data row2 col7" >2,555,555.56</td>
      <td id="T_b3bd7_row2_col8" class="data row2 col8" >CLP</td>
      <td id="T_b3bd7_row2_col9" class="data row2 col9" >5.0000%</td>
      <td id="T_b3bd7_row2_col10" class="data row2 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_b3bd7_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_b3bd7_row3_col0" class="data row3 col0" >2026-01-29</td>
      <td id="T_b3bd7_row3_col1" class="data row3 col1" >2026-07-29</td>
      <td id="T_b3bd7_row3_col2" class="data row3 col2" >2026-07-29</td>
      <td id="T_b3bd7_row3_col3" class="data row3 col3" >100,000,000.00</td>
      <td id="T_b3bd7_row3_col4" class="data row3 col4" >100,000,000.00</td>
      <td id="T_b3bd7_row3_col5" class="data row3 col5" >2,513,888.89</td>
      <td id="T_b3bd7_row3_col6" class="data row3 col6" >True</td>
      <td id="T_b3bd7_row3_col7" class="data row3 col7" >102,513,888.89</td>
      <td id="T_b3bd7_row3_col8" class="data row3 col8" >CLP</td>
      <td id="T_b3bd7_row3_col9" class="data row3 col9" >5.0000%</td>
      <td id="T_b3bd7_row3_col10" class="data row3 col10" >LinAct360</td>
    </tr>
  </tbody>
</table>




### Otros `StubPeriod`

Período irregular corto al inicio (`qcf.StubPeriod.SHORTFRONT`)


```python
fecha_final = fecha_inicio.add_months(27)
periodo_irregular = qcf.StubPeriod.SHORTFRONT

fixed_rate_leg = qcf.LegFactory.build_bullet_fixed_rate_leg(
    rec_pay=rp,
    start_date=fecha_inicio,
    end_date=fecha_final,
    bus_adj_rule=bus_adj_rule,
    settlement_periodicity=periodicidad,
    settlement_stub_period=periodo_irregular,
    settlement_calendar=calendario,
    settlement_lag=lag_pago,
    initial_notional=nominal,
    amort_is_cashflow=amort_es_flujo,
    interest_rate=tasa_cupon,
    notional_currency=moneda,
    is_bond=es_bono,
    sett_lag_behaviour=sett_lag_behaviour,
)
```


```python
df = aux.leg_as_dataframe(fixed_rate_leg)
df.style.format(aux.format_dict)
```




<style type="text/css">
</style>
<table id="T_a62ec">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_a62ec_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_a62ec_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_a62ec_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_a62ec_level0_col3" class="col_heading level0 col3" >nocional</th>
      <th id="T_a62ec_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_a62ec_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_a62ec_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_a62ec_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_a62ec_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_a62ec_level0_col9" class="col_heading level0 col9" >valor_tasa</th>
      <th id="T_a62ec_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_a62ec_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_a62ec_row0_col0" class="data row0 col0" >2024-07-29</td>
      <td id="T_a62ec_row0_col1" class="data row0 col1" >2024-10-29</td>
      <td id="T_a62ec_row0_col2" class="data row0 col2" >2024-10-29</td>
      <td id="T_a62ec_row0_col3" class="data row0 col3" >100,000,000.00</td>
      <td id="T_a62ec_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_a62ec_row0_col5" class="data row0 col5" >1,277,777.78</td>
      <td id="T_a62ec_row0_col6" class="data row0 col6" >True</td>
      <td id="T_a62ec_row0_col7" class="data row0 col7" >1,277,777.78</td>
      <td id="T_a62ec_row0_col8" class="data row0 col8" >CLP</td>
      <td id="T_a62ec_row0_col9" class="data row0 col9" >5.0000%</td>
      <td id="T_a62ec_row0_col10" class="data row0 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a62ec_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_a62ec_row1_col0" class="data row1 col0" >2024-10-29</td>
      <td id="T_a62ec_row1_col1" class="data row1 col1" >2025-04-29</td>
      <td id="T_a62ec_row1_col2" class="data row1 col2" >2025-04-29</td>
      <td id="T_a62ec_row1_col3" class="data row1 col3" >100,000,000.00</td>
      <td id="T_a62ec_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_a62ec_row1_col5" class="data row1 col5" >2,527,777.78</td>
      <td id="T_a62ec_row1_col6" class="data row1 col6" >True</td>
      <td id="T_a62ec_row1_col7" class="data row1 col7" >2,527,777.78</td>
      <td id="T_a62ec_row1_col8" class="data row1 col8" >CLP</td>
      <td id="T_a62ec_row1_col9" class="data row1 col9" >5.0000%</td>
      <td id="T_a62ec_row1_col10" class="data row1 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a62ec_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_a62ec_row2_col0" class="data row2 col0" >2025-04-29</td>
      <td id="T_a62ec_row2_col1" class="data row2 col1" >2025-10-29</td>
      <td id="T_a62ec_row2_col2" class="data row2 col2" >2025-10-29</td>
      <td id="T_a62ec_row2_col3" class="data row2 col3" >100,000,000.00</td>
      <td id="T_a62ec_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_a62ec_row2_col5" class="data row2 col5" >2,541,666.67</td>
      <td id="T_a62ec_row2_col6" class="data row2 col6" >True</td>
      <td id="T_a62ec_row2_col7" class="data row2 col7" >2,541,666.67</td>
      <td id="T_a62ec_row2_col8" class="data row2 col8" >CLP</td>
      <td id="T_a62ec_row2_col9" class="data row2 col9" >5.0000%</td>
      <td id="T_a62ec_row2_col10" class="data row2 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a62ec_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_a62ec_row3_col0" class="data row3 col0" >2025-10-29</td>
      <td id="T_a62ec_row3_col1" class="data row3 col1" >2026-04-29</td>
      <td id="T_a62ec_row3_col2" class="data row3 col2" >2026-04-29</td>
      <td id="T_a62ec_row3_col3" class="data row3 col3" >100,000,000.00</td>
      <td id="T_a62ec_row3_col4" class="data row3 col4" >0.00</td>
      <td id="T_a62ec_row3_col5" class="data row3 col5" >2,527,777.78</td>
      <td id="T_a62ec_row3_col6" class="data row3 col6" >True</td>
      <td id="T_a62ec_row3_col7" class="data row3 col7" >2,527,777.78</td>
      <td id="T_a62ec_row3_col8" class="data row3 col8" >CLP</td>
      <td id="T_a62ec_row3_col9" class="data row3 col9" >5.0000%</td>
      <td id="T_a62ec_row3_col10" class="data row3 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a62ec_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_a62ec_row4_col0" class="data row4 col0" >2026-04-29</td>
      <td id="T_a62ec_row4_col1" class="data row4 col1" >2026-10-29</td>
      <td id="T_a62ec_row4_col2" class="data row4 col2" >2026-10-29</td>
      <td id="T_a62ec_row4_col3" class="data row4 col3" >100,000,000.00</td>
      <td id="T_a62ec_row4_col4" class="data row4 col4" >100,000,000.00</td>
      <td id="T_a62ec_row4_col5" class="data row4 col5" >2,541,666.67</td>
      <td id="T_a62ec_row4_col6" class="data row4 col6" >True</td>
      <td id="T_a62ec_row4_col7" class="data row4 col7" >102,541,666.67</td>
      <td id="T_a62ec_row4_col8" class="data row4 col8" >CLP</td>
      <td id="T_a62ec_row4_col9" class="data row4 col9" >5.0000%</td>
      <td id="T_a62ec_row4_col10" class="data row4 col10" >LinAct360</td>
    </tr>
  </tbody>
</table>




Período irregular corto al final (`qcf.StubPeriod.SHORTBACK`)


```python
periodo_irregular = qcf.StubPeriod.SHORTBACK

fixed_rate_leg = qcf.LegFactory.build_bullet_fixed_rate_leg(
    rec_pay=rp,
    start_date=fecha_inicio,
    end_date=fecha_final,
    bus_adj_rule=bus_adj_rule,
    settlement_periodicity=periodicidad,
    settlement_stub_period=periodo_irregular,
    settlement_calendar=calendario,
    settlement_lag=lag_pago,
    initial_notional=nominal,
    amort_is_cashflow=amort_es_flujo,
    interest_rate=tasa_cupon,
    notional_currency=moneda,
    is_bond=es_bono,
    sett_lag_behaviour=sett_lag_behaviour,
)
```


```python
df = aux.leg_as_dataframe(fixed_rate_leg)
df.style.format(aux.format_dict)
```




<style type="text/css">
</style>
<table id="T_e2953">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_e2953_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_e2953_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_e2953_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_e2953_level0_col3" class="col_heading level0 col3" >nocional</th>
      <th id="T_e2953_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_e2953_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_e2953_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_e2953_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_e2953_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_e2953_level0_col9" class="col_heading level0 col9" >valor_tasa</th>
      <th id="T_e2953_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_e2953_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_e2953_row0_col0" class="data row0 col0" >2024-07-29</td>
      <td id="T_e2953_row0_col1" class="data row0 col1" >2025-01-29</td>
      <td id="T_e2953_row0_col2" class="data row0 col2" >2025-01-29</td>
      <td id="T_e2953_row0_col3" class="data row0 col3" >100,000,000.00</td>
      <td id="T_e2953_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_e2953_row0_col5" class="data row0 col5" >2,555,555.56</td>
      <td id="T_e2953_row0_col6" class="data row0 col6" >True</td>
      <td id="T_e2953_row0_col7" class="data row0 col7" >2,555,555.56</td>
      <td id="T_e2953_row0_col8" class="data row0 col8" >CLP</td>
      <td id="T_e2953_row0_col9" class="data row0 col9" >5.0000%</td>
      <td id="T_e2953_row0_col10" class="data row0 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_e2953_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_e2953_row1_col0" class="data row1 col0" >2025-01-29</td>
      <td id="T_e2953_row1_col1" class="data row1 col1" >2025-07-29</td>
      <td id="T_e2953_row1_col2" class="data row1 col2" >2025-07-29</td>
      <td id="T_e2953_row1_col3" class="data row1 col3" >100,000,000.00</td>
      <td id="T_e2953_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_e2953_row1_col5" class="data row1 col5" >2,513,888.89</td>
      <td id="T_e2953_row1_col6" class="data row1 col6" >True</td>
      <td id="T_e2953_row1_col7" class="data row1 col7" >2,513,888.89</td>
      <td id="T_e2953_row1_col8" class="data row1 col8" >CLP</td>
      <td id="T_e2953_row1_col9" class="data row1 col9" >5.0000%</td>
      <td id="T_e2953_row1_col10" class="data row1 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_e2953_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_e2953_row2_col0" class="data row2 col0" >2025-07-29</td>
      <td id="T_e2953_row2_col1" class="data row2 col1" >2026-01-29</td>
      <td id="T_e2953_row2_col2" class="data row2 col2" >2026-01-29</td>
      <td id="T_e2953_row2_col3" class="data row2 col3" >100,000,000.00</td>
      <td id="T_e2953_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_e2953_row2_col5" class="data row2 col5" >2,555,555.56</td>
      <td id="T_e2953_row2_col6" class="data row2 col6" >True</td>
      <td id="T_e2953_row2_col7" class="data row2 col7" >2,555,555.56</td>
      <td id="T_e2953_row2_col8" class="data row2 col8" >CLP</td>
      <td id="T_e2953_row2_col9" class="data row2 col9" >5.0000%</td>
      <td id="T_e2953_row2_col10" class="data row2 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_e2953_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_e2953_row3_col0" class="data row3 col0" >2026-01-29</td>
      <td id="T_e2953_row3_col1" class="data row3 col1" >2026-07-29</td>
      <td id="T_e2953_row3_col2" class="data row3 col2" >2026-07-29</td>
      <td id="T_e2953_row3_col3" class="data row3 col3" >100,000,000.00</td>
      <td id="T_e2953_row3_col4" class="data row3 col4" >0.00</td>
      <td id="T_e2953_row3_col5" class="data row3 col5" >2,513,888.89</td>
      <td id="T_e2953_row3_col6" class="data row3 col6" >True</td>
      <td id="T_e2953_row3_col7" class="data row3 col7" >2,513,888.89</td>
      <td id="T_e2953_row3_col8" class="data row3 col8" >CLP</td>
      <td id="T_e2953_row3_col9" class="data row3 col9" >5.0000%</td>
      <td id="T_e2953_row3_col10" class="data row3 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_e2953_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_e2953_row4_col0" class="data row4 col0" >2026-07-29</td>
      <td id="T_e2953_row4_col1" class="data row4 col1" >2026-10-29</td>
      <td id="T_e2953_row4_col2" class="data row4 col2" >2026-10-29</td>
      <td id="T_e2953_row4_col3" class="data row4 col3" >100,000,000.00</td>
      <td id="T_e2953_row4_col4" class="data row4 col4" >100,000,000.00</td>
      <td id="T_e2953_row4_col5" class="data row4 col5" >1,277,777.78</td>
      <td id="T_e2953_row4_col6" class="data row4 col6" >True</td>
      <td id="T_e2953_row4_col7" class="data row4 col7" >101,277,777.78</td>
      <td id="T_e2953_row4_col8" class="data row4 col8" >CLP</td>
      <td id="T_e2953_row4_col9" class="data row4 col9" >5.0000%</td>
      <td id="T_e2953_row4_col10" class="data row4 col10" >LinAct360</td>
    </tr>
  </tbody>
</table>




Período irregular largo al principio (`qcf.StubPeriod.LONGFRONT`)


```python
periodo_irregular = qcf.StubPeriod.LONGFRONT

fixed_rate_leg = qcf.LegFactory.build_bullet_fixed_rate_leg(
    rec_pay=rp,
    start_date=fecha_inicio,
    end_date=fecha_final,
    bus_adj_rule=bus_adj_rule,
    settlement_periodicity=periodicidad,
    settlement_stub_period=periodo_irregular,
    settlement_calendar=calendario,
    settlement_lag=lag_pago,
    initial_notional=nominal,
    amort_is_cashflow=amort_es_flujo,
    interest_rate=tasa_cupon,
    notional_currency=moneda,
    is_bond=es_bono,
    sett_lag_behaviour=sett_lag_behaviour,
)
```


```python
df = aux.leg_as_dataframe(fixed_rate_leg)
df.style.format(aux.format_dict)
```




<style type="text/css">
</style>
<table id="T_66b91">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_66b91_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_66b91_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_66b91_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_66b91_level0_col3" class="col_heading level0 col3" >nocional</th>
      <th id="T_66b91_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_66b91_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_66b91_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_66b91_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_66b91_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_66b91_level0_col9" class="col_heading level0 col9" >valor_tasa</th>
      <th id="T_66b91_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_66b91_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_66b91_row0_col0" class="data row0 col0" >2024-07-29</td>
      <td id="T_66b91_row0_col1" class="data row0 col1" >2025-04-29</td>
      <td id="T_66b91_row0_col2" class="data row0 col2" >2025-04-29</td>
      <td id="T_66b91_row0_col3" class="data row0 col3" >100,000,000.00</td>
      <td id="T_66b91_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_66b91_row0_col5" class="data row0 col5" >3,805,555.56</td>
      <td id="T_66b91_row0_col6" class="data row0 col6" >True</td>
      <td id="T_66b91_row0_col7" class="data row0 col7" >3,805,555.56</td>
      <td id="T_66b91_row0_col8" class="data row0 col8" >CLP</td>
      <td id="T_66b91_row0_col9" class="data row0 col9" >5.0000%</td>
      <td id="T_66b91_row0_col10" class="data row0 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_66b91_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_66b91_row1_col0" class="data row1 col0" >2025-04-29</td>
      <td id="T_66b91_row1_col1" class="data row1 col1" >2025-10-29</td>
      <td id="T_66b91_row1_col2" class="data row1 col2" >2025-10-29</td>
      <td id="T_66b91_row1_col3" class="data row1 col3" >100,000,000.00</td>
      <td id="T_66b91_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_66b91_row1_col5" class="data row1 col5" >2,541,666.67</td>
      <td id="T_66b91_row1_col6" class="data row1 col6" >True</td>
      <td id="T_66b91_row1_col7" class="data row1 col7" >2,541,666.67</td>
      <td id="T_66b91_row1_col8" class="data row1 col8" >CLP</td>
      <td id="T_66b91_row1_col9" class="data row1 col9" >5.0000%</td>
      <td id="T_66b91_row1_col10" class="data row1 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_66b91_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_66b91_row2_col0" class="data row2 col0" >2025-10-29</td>
      <td id="T_66b91_row2_col1" class="data row2 col1" >2026-04-29</td>
      <td id="T_66b91_row2_col2" class="data row2 col2" >2026-04-29</td>
      <td id="T_66b91_row2_col3" class="data row2 col3" >100,000,000.00</td>
      <td id="T_66b91_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_66b91_row2_col5" class="data row2 col5" >2,527,777.78</td>
      <td id="T_66b91_row2_col6" class="data row2 col6" >True</td>
      <td id="T_66b91_row2_col7" class="data row2 col7" >2,527,777.78</td>
      <td id="T_66b91_row2_col8" class="data row2 col8" >CLP</td>
      <td id="T_66b91_row2_col9" class="data row2 col9" >5.0000%</td>
      <td id="T_66b91_row2_col10" class="data row2 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_66b91_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_66b91_row3_col0" class="data row3 col0" >2026-04-29</td>
      <td id="T_66b91_row3_col1" class="data row3 col1" >2026-10-29</td>
      <td id="T_66b91_row3_col2" class="data row3 col2" >2026-10-29</td>
      <td id="T_66b91_row3_col3" class="data row3 col3" >100,000,000.00</td>
      <td id="T_66b91_row3_col4" class="data row3 col4" >100,000,000.00</td>
      <td id="T_66b91_row3_col5" class="data row3 col5" >2,541,666.67</td>
      <td id="T_66b91_row3_col6" class="data row3 col6" >True</td>
      <td id="T_66b91_row3_col7" class="data row3 col7" >102,541,666.67</td>
      <td id="T_66b91_row3_col8" class="data row3 col8" >CLP</td>
      <td id="T_66b91_row3_col9" class="data row3 col9" >5.0000%</td>
      <td id="T_66b91_row3_col10" class="data row3 col10" >LinAct360</td>
    </tr>
  </tbody>
</table>




Período irregular largo al final (`qcf.StubPeriod.LONGBACK`)


```python
periodo_irregular = qcf.StubPeriod.LONGBACK

fixed_rate_leg = qcf.LegFactory.build_bullet_fixed_rate_leg(
    rec_pay=rp,
    start_date=fecha_inicio,
    end_date=fecha_final,
    bus_adj_rule=bus_adj_rule,
    settlement_periodicity=periodicidad,
    settlement_stub_period=periodo_irregular,
    settlement_calendar=calendario,
    settlement_lag=lag_pago,
    initial_notional=nominal,
    amort_is_cashflow=amort_es_flujo,
    interest_rate=tasa_cupon,
    notional_currency=moneda,
    is_bond=es_bono,
    sett_lag_behaviour=sett_lag_behaviour,
)
```


```python
df = aux.leg_as_dataframe(fixed_rate_leg)
df.style.format(aux.format_dict)
```




<style type="text/css">
</style>
<table id="T_fe6aa">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_fe6aa_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_fe6aa_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_fe6aa_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_fe6aa_level0_col3" class="col_heading level0 col3" >nocional</th>
      <th id="T_fe6aa_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_fe6aa_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_fe6aa_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_fe6aa_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_fe6aa_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_fe6aa_level0_col9" class="col_heading level0 col9" >valor_tasa</th>
      <th id="T_fe6aa_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_fe6aa_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_fe6aa_row0_col0" class="data row0 col0" >2024-07-29</td>
      <td id="T_fe6aa_row0_col1" class="data row0 col1" >2025-01-29</td>
      <td id="T_fe6aa_row0_col2" class="data row0 col2" >2025-01-29</td>
      <td id="T_fe6aa_row0_col3" class="data row0 col3" >100,000,000.00</td>
      <td id="T_fe6aa_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_fe6aa_row0_col5" class="data row0 col5" >2,555,555.56</td>
      <td id="T_fe6aa_row0_col6" class="data row0 col6" >True</td>
      <td id="T_fe6aa_row0_col7" class="data row0 col7" >2,555,555.56</td>
      <td id="T_fe6aa_row0_col8" class="data row0 col8" >CLP</td>
      <td id="T_fe6aa_row0_col9" class="data row0 col9" >5.0000%</td>
      <td id="T_fe6aa_row0_col10" class="data row0 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_fe6aa_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_fe6aa_row1_col0" class="data row1 col0" >2025-01-29</td>
      <td id="T_fe6aa_row1_col1" class="data row1 col1" >2025-07-29</td>
      <td id="T_fe6aa_row1_col2" class="data row1 col2" >2025-07-29</td>
      <td id="T_fe6aa_row1_col3" class="data row1 col3" >100,000,000.00</td>
      <td id="T_fe6aa_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_fe6aa_row1_col5" class="data row1 col5" >2,513,888.89</td>
      <td id="T_fe6aa_row1_col6" class="data row1 col6" >True</td>
      <td id="T_fe6aa_row1_col7" class="data row1 col7" >2,513,888.89</td>
      <td id="T_fe6aa_row1_col8" class="data row1 col8" >CLP</td>
      <td id="T_fe6aa_row1_col9" class="data row1 col9" >5.0000%</td>
      <td id="T_fe6aa_row1_col10" class="data row1 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_fe6aa_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_fe6aa_row2_col0" class="data row2 col0" >2025-07-29</td>
      <td id="T_fe6aa_row2_col1" class="data row2 col1" >2026-01-29</td>
      <td id="T_fe6aa_row2_col2" class="data row2 col2" >2026-01-29</td>
      <td id="T_fe6aa_row2_col3" class="data row2 col3" >100,000,000.00</td>
      <td id="T_fe6aa_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_fe6aa_row2_col5" class="data row2 col5" >2,555,555.56</td>
      <td id="T_fe6aa_row2_col6" class="data row2 col6" >True</td>
      <td id="T_fe6aa_row2_col7" class="data row2 col7" >2,555,555.56</td>
      <td id="T_fe6aa_row2_col8" class="data row2 col8" >CLP</td>
      <td id="T_fe6aa_row2_col9" class="data row2 col9" >5.0000%</td>
      <td id="T_fe6aa_row2_col10" class="data row2 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_fe6aa_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_fe6aa_row3_col0" class="data row3 col0" >2026-01-29</td>
      <td id="T_fe6aa_row3_col1" class="data row3 col1" >2026-10-29</td>
      <td id="T_fe6aa_row3_col2" class="data row3 col2" >2026-10-29</td>
      <td id="T_fe6aa_row3_col3" class="data row3 col3" >100,000,000.00</td>
      <td id="T_fe6aa_row3_col4" class="data row3 col4" >100,000,000.00</td>
      <td id="T_fe6aa_row3_col5" class="data row3 col5" >3,791,666.67</td>
      <td id="T_fe6aa_row3_col6" class="data row3 col6" >True</td>
      <td id="T_fe6aa_row3_col7" class="data row3 col7" >103,791,666.67</td>
      <td id="T_fe6aa_row3_col8" class="data row3 col8" >CLP</td>
      <td id="T_fe6aa_row3_col9" class="data row3 col9" >5.0000%</td>
      <td id="T_fe6aa_row3_col10" class="data row3 col10" >LinAct360</td>
    </tr>
  </tbody>
</table>




Período de gracia, usual en la cobertura de créditos (`qcf.StubPeriod.LONGFRONT3`)


```python
fecha_final = fecha_inicio.add_months(12 * 5)  # Swap de 5Y
periodo_irregular = qcf.StubPeriod.LONGFRONT3  # Una de varias opciones parecidas para alargar el primer período de intereses

fixed_rate_leg = qcf.LegFactory.build_bullet_fixed_rate_leg(
    rec_pay=rp,
    start_date=fecha_inicio,
    end_date=fecha_final,
    bus_adj_rule=bus_adj_rule,
    settlement_periodicity=periodicidad,
    settlement_stub_period=periodo_irregular,
    settlement_calendar=calendario,
    settlement_lag=lag_pago,
    initial_notional=nominal,
    amort_is_cashflow=amort_es_flujo,
    interest_rate=tasa_cupon,
    notional_currency=moneda,
    is_bond=es_bono,
    sett_lag_behaviour=sett_lag_behaviour,
)
```


```python
df = aux.leg_as_dataframe(fixed_rate_leg)
df.style.format(aux.format_dict)
```




<style type="text/css">
</style>
<table id="T_265a1">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_265a1_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_265a1_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_265a1_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_265a1_level0_col3" class="col_heading level0 col3" >nocional</th>
      <th id="T_265a1_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_265a1_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_265a1_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_265a1_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_265a1_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_265a1_level0_col9" class="col_heading level0 col9" >valor_tasa</th>
      <th id="T_265a1_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_265a1_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_265a1_row0_col0" class="data row0 col0" >2024-07-29</td>
      <td id="T_265a1_row0_col1" class="data row0 col1" >2026-01-29</td>
      <td id="T_265a1_row0_col2" class="data row0 col2" >2026-01-29</td>
      <td id="T_265a1_row0_col3" class="data row0 col3" >100,000,000.00</td>
      <td id="T_265a1_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_265a1_row0_col5" class="data row0 col5" >7,625,000.00</td>
      <td id="T_265a1_row0_col6" class="data row0 col6" >True</td>
      <td id="T_265a1_row0_col7" class="data row0 col7" >7,625,000.00</td>
      <td id="T_265a1_row0_col8" class="data row0 col8" >CLP</td>
      <td id="T_265a1_row0_col9" class="data row0 col9" >5.0000%</td>
      <td id="T_265a1_row0_col10" class="data row0 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_265a1_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_265a1_row1_col0" class="data row1 col0" >2026-01-29</td>
      <td id="T_265a1_row1_col1" class="data row1 col1" >2026-07-29</td>
      <td id="T_265a1_row1_col2" class="data row1 col2" >2026-07-29</td>
      <td id="T_265a1_row1_col3" class="data row1 col3" >100,000,000.00</td>
      <td id="T_265a1_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_265a1_row1_col5" class="data row1 col5" >2,513,888.89</td>
      <td id="T_265a1_row1_col6" class="data row1 col6" >True</td>
      <td id="T_265a1_row1_col7" class="data row1 col7" >2,513,888.89</td>
      <td id="T_265a1_row1_col8" class="data row1 col8" >CLP</td>
      <td id="T_265a1_row1_col9" class="data row1 col9" >5.0000%</td>
      <td id="T_265a1_row1_col10" class="data row1 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_265a1_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_265a1_row2_col0" class="data row2 col0" >2026-07-29</td>
      <td id="T_265a1_row2_col1" class="data row2 col1" >2027-01-29</td>
      <td id="T_265a1_row2_col2" class="data row2 col2" >2027-01-29</td>
      <td id="T_265a1_row2_col3" class="data row2 col3" >100,000,000.00</td>
      <td id="T_265a1_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_265a1_row2_col5" class="data row2 col5" >2,555,555.56</td>
      <td id="T_265a1_row2_col6" class="data row2 col6" >True</td>
      <td id="T_265a1_row2_col7" class="data row2 col7" >2,555,555.56</td>
      <td id="T_265a1_row2_col8" class="data row2 col8" >CLP</td>
      <td id="T_265a1_row2_col9" class="data row2 col9" >5.0000%</td>
      <td id="T_265a1_row2_col10" class="data row2 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_265a1_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_265a1_row3_col0" class="data row3 col0" >2027-01-29</td>
      <td id="T_265a1_row3_col1" class="data row3 col1" >2027-07-29</td>
      <td id="T_265a1_row3_col2" class="data row3 col2" >2027-07-29</td>
      <td id="T_265a1_row3_col3" class="data row3 col3" >100,000,000.00</td>
      <td id="T_265a1_row3_col4" class="data row3 col4" >0.00</td>
      <td id="T_265a1_row3_col5" class="data row3 col5" >2,513,888.89</td>
      <td id="T_265a1_row3_col6" class="data row3 col6" >True</td>
      <td id="T_265a1_row3_col7" class="data row3 col7" >2,513,888.89</td>
      <td id="T_265a1_row3_col8" class="data row3 col8" >CLP</td>
      <td id="T_265a1_row3_col9" class="data row3 col9" >5.0000%</td>
      <td id="T_265a1_row3_col10" class="data row3 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_265a1_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_265a1_row4_col0" class="data row4 col0" >2027-07-29</td>
      <td id="T_265a1_row4_col1" class="data row4 col1" >2028-01-31</td>
      <td id="T_265a1_row4_col2" class="data row4 col2" >2028-01-31</td>
      <td id="T_265a1_row4_col3" class="data row4 col3" >100,000,000.00</td>
      <td id="T_265a1_row4_col4" class="data row4 col4" >0.00</td>
      <td id="T_265a1_row4_col5" class="data row4 col5" >2,583,333.33</td>
      <td id="T_265a1_row4_col6" class="data row4 col6" >True</td>
      <td id="T_265a1_row4_col7" class="data row4 col7" >2,583,333.33</td>
      <td id="T_265a1_row4_col8" class="data row4 col8" >CLP</td>
      <td id="T_265a1_row4_col9" class="data row4 col9" >5.0000%</td>
      <td id="T_265a1_row4_col10" class="data row4 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_265a1_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_265a1_row5_col0" class="data row5 col0" >2028-01-31</td>
      <td id="T_265a1_row5_col1" class="data row5 col1" >2028-07-31</td>
      <td id="T_265a1_row5_col2" class="data row5 col2" >2028-07-31</td>
      <td id="T_265a1_row5_col3" class="data row5 col3" >100,000,000.00</td>
      <td id="T_265a1_row5_col4" class="data row5 col4" >0.00</td>
      <td id="T_265a1_row5_col5" class="data row5 col5" >2,527,777.78</td>
      <td id="T_265a1_row5_col6" class="data row5 col6" >True</td>
      <td id="T_265a1_row5_col7" class="data row5 col7" >2,527,777.78</td>
      <td id="T_265a1_row5_col8" class="data row5 col8" >CLP</td>
      <td id="T_265a1_row5_col9" class="data row5 col9" >5.0000%</td>
      <td id="T_265a1_row5_col10" class="data row5 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_265a1_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_265a1_row6_col0" class="data row6 col0" >2028-07-31</td>
      <td id="T_265a1_row6_col1" class="data row6 col1" >2029-01-29</td>
      <td id="T_265a1_row6_col2" class="data row6 col2" >2029-01-29</td>
      <td id="T_265a1_row6_col3" class="data row6 col3" >100,000,000.00</td>
      <td id="T_265a1_row6_col4" class="data row6 col4" >0.00</td>
      <td id="T_265a1_row6_col5" class="data row6 col5" >2,527,777.78</td>
      <td id="T_265a1_row6_col6" class="data row6 col6" >True</td>
      <td id="T_265a1_row6_col7" class="data row6 col7" >2,527,777.78</td>
      <td id="T_265a1_row6_col8" class="data row6 col8" >CLP</td>
      <td id="T_265a1_row6_col9" class="data row6 col9" >5.0000%</td>
      <td id="T_265a1_row6_col10" class="data row6 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_265a1_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_265a1_row7_col0" class="data row7 col0" >2029-01-29</td>
      <td id="T_265a1_row7_col1" class="data row7 col1" >2029-07-30</td>
      <td id="T_265a1_row7_col2" class="data row7 col2" >2029-07-30</td>
      <td id="T_265a1_row7_col3" class="data row7 col3" >100,000,000.00</td>
      <td id="T_265a1_row7_col4" class="data row7 col4" >100,000,000.00</td>
      <td id="T_265a1_row7_col5" class="data row7 col5" >2,527,777.78</td>
      <td id="T_265a1_row7_col6" class="data row7 col6" >True</td>
      <td id="T_265a1_row7_col7" class="data row7 col7" >102,527,777.78</td>
      <td id="T_265a1_row7_col8" class="data row7 col8" >CLP</td>
      <td id="T_265a1_row7_col9" class="data row7 col9" >5.0000%</td>
      <td id="T_265a1_row7_col10" class="data row7 col10" >LinAct360</td>
    </tr>
  </tbody>
</table>




## Construcción Asistida de un `CustomAmortFixedRateLeg`

En este ejemplo se construye un `Leg` con cashflows a tasa fija donde la estructura de amortizaciones es customizada.
Se requieren los siguientes parámetros:

- `RecPay`: enum que indica si los flujos se reciben o pagan
- `QCDate`: fecha de inicio del primer flujo
- `QCDate`: fecha final del último flujo sin considerar ajustes de días feriados
- `BusyAdRules`: enum que representa el tipo de ajuste en la fecha final para días feriados
- `Tenor`: la periodicidad de pago
- `QCInterestRateLeg::QCStubPeriod`: enum que representa el tipo de período irregular (si aplica)
- `QCBusinessCalendar`: calendario que aplica para las fechas de pago
- `unsigned int`: lag de pago expresado en días
- `CustomNotionalAndAmort`: vector de capital vigente y amortizaciones customizado
- `bool`: si es `True` significa que la amortización es un flujo de caja efectivo
- `QCInterestRate`: la tasa a aplicar en cada flujo
- `QCCurrency`: moneda del nominal y de los flujos
- `SettLagBehaviour`: este parámetro indica cómo se calcula un `settlement_date` cuando un `end_date` cae en un día festivo.

Notar que este tipo de `Leg` no admite el parámetro `is_bond`. Se puede lograr el mismo efecto construyendo una pata bullet y luego customizando su amortización.

Vamos a un ejemplo.

Primero se da de alta los parámetros requeridos


```python
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(31, 1, 2024)
fecha_final = qcf.QCDate(31, 1, 2028) 

calendario = aux.get_business_calendar('US', range(2024, 2027))
bus_adj_rule = qcf.BusyAdjRules.NO
periodicidad = qcf.Tenor('6M')
periodo_irregular = qcf.StubPeriod.NO
lag_pago = 1

amort_es_flujo = True
valor_tasa = .05
tasa_cupon = qcf.QCInterestRate(
    valor_tasa, 
    qcf.QC30360(), 
    qcf.QCLinearWf()
)

moneda = qcf.QCCLP()
sett_lag_behaviour = qcf.SettLagBehaviour.DONT_MOVE
```

Aquí se da de alta el vector de capitales vigentes y amortizaciones. Cada elemento del vector es una tupla que continen el capital vigente y amortización del correspondiente cupón.


```python
custom_notional_amort = qcf.CustomNotionalAmort()
custom_notional_amort.set_size(8)  # De la fecha inicio, fecha final y periodicidad se deduce que serán 8 cupones
for i in range(0, 8):
    custom_notional_amort.set_notional_amort_at(i, 800.0 - i * 100.0, 100.0)
```

Se da de alta el objeto.


```python
fixed_rate_custom_leg = qcf.LegFactory.build_custom_amort_fixed_rate_leg(
    rec_pay=rp,
    start_date=fecha_inicio,
    end_date=fecha_final,
    bus_adj_rule=bus_adj_rule,
    settlement_periodicity=periodicidad,
    settlement_stub_period=periodo_irregular,
    settlement_calendar=calendario,
    settlement_lag=lag_pago,
    notional_and_amort=custom_notional_amort,
    amort_is_cashflow=amort_es_flujo,
    interest_rate=tasa_cupon,
    notional_currency=moneda,
    sett_lag_behaviour=sett_lag_behaviour,
)
```


```python
df = aux.leg_as_dataframe(fixed_rate_custom_leg)
df.style.format(aux.format_dict).set_properties(
    **{'background-color': '#FFCFC9', 'color':'black'},
    subset=['nocional','amortizacion', 'flujo']
).set_properties(
    **{'background-color': '#FFCFA9', 'color':'black'},
    subset=['flujo']
)
```




<style type="text/css">
#T_1ab63_row0_col3, #T_1ab63_row0_col4, #T_1ab63_row1_col3, #T_1ab63_row1_col4, #T_1ab63_row2_col3, #T_1ab63_row2_col4, #T_1ab63_row3_col3, #T_1ab63_row3_col4, #T_1ab63_row4_col3, #T_1ab63_row4_col4, #T_1ab63_row5_col3, #T_1ab63_row5_col4, #T_1ab63_row6_col3, #T_1ab63_row6_col4, #T_1ab63_row7_col3, #T_1ab63_row7_col4 {
  background-color: #FFCFC9;
  color: black;
}
#T_1ab63_row0_col7, #T_1ab63_row1_col7, #T_1ab63_row2_col7, #T_1ab63_row3_col7, #T_1ab63_row4_col7, #T_1ab63_row5_col7, #T_1ab63_row6_col7, #T_1ab63_row7_col7 {
  background-color: #FFCFC9;
  color: black;
  background-color: #FFCFA9;
  color: black;
}
</style>
<table id="T_1ab63">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_1ab63_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_1ab63_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_1ab63_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_1ab63_level0_col3" class="col_heading level0 col3" >nocional</th>
      <th id="T_1ab63_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_1ab63_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_1ab63_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_1ab63_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_1ab63_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_1ab63_level0_col9" class="col_heading level0 col9" >valor_tasa</th>
      <th id="T_1ab63_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_1ab63_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_1ab63_row0_col0" class="data row0 col0" >2024-01-31</td>
      <td id="T_1ab63_row0_col1" class="data row0 col1" >2024-07-31</td>
      <td id="T_1ab63_row0_col2" class="data row0 col2" >2024-08-01</td>
      <td id="T_1ab63_row0_col3" class="data row0 col3" >800.00</td>
      <td id="T_1ab63_row0_col4" class="data row0 col4" >100.00</td>
      <td id="T_1ab63_row0_col5" class="data row0 col5" >20.00</td>
      <td id="T_1ab63_row0_col6" class="data row0 col6" >True</td>
      <td id="T_1ab63_row0_col7" class="data row0 col7" >120.00</td>
      <td id="T_1ab63_row0_col8" class="data row0 col8" >CLP</td>
      <td id="T_1ab63_row0_col9" class="data row0 col9" >5.0000%</td>
      <td id="T_1ab63_row0_col10" class="data row0 col10" >Lin30360</td>
    </tr>
    <tr>
      <th id="T_1ab63_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_1ab63_row1_col0" class="data row1 col0" >2024-07-31</td>
      <td id="T_1ab63_row1_col1" class="data row1 col1" >2025-01-31</td>
      <td id="T_1ab63_row1_col2" class="data row1 col2" >2025-02-03</td>
      <td id="T_1ab63_row1_col3" class="data row1 col3" >700.00</td>
      <td id="T_1ab63_row1_col4" class="data row1 col4" >100.00</td>
      <td id="T_1ab63_row1_col5" class="data row1 col5" >17.50</td>
      <td id="T_1ab63_row1_col6" class="data row1 col6" >True</td>
      <td id="T_1ab63_row1_col7" class="data row1 col7" >117.50</td>
      <td id="T_1ab63_row1_col8" class="data row1 col8" >CLP</td>
      <td id="T_1ab63_row1_col9" class="data row1 col9" >5.0000%</td>
      <td id="T_1ab63_row1_col10" class="data row1 col10" >Lin30360</td>
    </tr>
    <tr>
      <th id="T_1ab63_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_1ab63_row2_col0" class="data row2 col0" >2025-01-31</td>
      <td id="T_1ab63_row2_col1" class="data row2 col1" >2025-07-31</td>
      <td id="T_1ab63_row2_col2" class="data row2 col2" >2025-08-01</td>
      <td id="T_1ab63_row2_col3" class="data row2 col3" >600.00</td>
      <td id="T_1ab63_row2_col4" class="data row2 col4" >100.00</td>
      <td id="T_1ab63_row2_col5" class="data row2 col5" >15.00</td>
      <td id="T_1ab63_row2_col6" class="data row2 col6" >True</td>
      <td id="T_1ab63_row2_col7" class="data row2 col7" >115.00</td>
      <td id="T_1ab63_row2_col8" class="data row2 col8" >CLP</td>
      <td id="T_1ab63_row2_col9" class="data row2 col9" >5.0000%</td>
      <td id="T_1ab63_row2_col10" class="data row2 col10" >Lin30360</td>
    </tr>
    <tr>
      <th id="T_1ab63_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_1ab63_row3_col0" class="data row3 col0" >2025-07-31</td>
      <td id="T_1ab63_row3_col1" class="data row3 col1" >2026-01-31</td>
      <td id="T_1ab63_row3_col2" class="data row3 col2" >2026-02-02</td>
      <td id="T_1ab63_row3_col3" class="data row3 col3" >500.00</td>
      <td id="T_1ab63_row3_col4" class="data row3 col4" >100.00</td>
      <td id="T_1ab63_row3_col5" class="data row3 col5" >12.50</td>
      <td id="T_1ab63_row3_col6" class="data row3 col6" >True</td>
      <td id="T_1ab63_row3_col7" class="data row3 col7" >112.50</td>
      <td id="T_1ab63_row3_col8" class="data row3 col8" >CLP</td>
      <td id="T_1ab63_row3_col9" class="data row3 col9" >5.0000%</td>
      <td id="T_1ab63_row3_col10" class="data row3 col10" >Lin30360</td>
    </tr>
    <tr>
      <th id="T_1ab63_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_1ab63_row4_col0" class="data row4 col0" >2026-01-31</td>
      <td id="T_1ab63_row4_col1" class="data row4 col1" >2026-07-31</td>
      <td id="T_1ab63_row4_col2" class="data row4 col2" >2026-08-03</td>
      <td id="T_1ab63_row4_col3" class="data row4 col3" >400.00</td>
      <td id="T_1ab63_row4_col4" class="data row4 col4" >100.00</td>
      <td id="T_1ab63_row4_col5" class="data row4 col5" >10.00</td>
      <td id="T_1ab63_row4_col6" class="data row4 col6" >True</td>
      <td id="T_1ab63_row4_col7" class="data row4 col7" >110.00</td>
      <td id="T_1ab63_row4_col8" class="data row4 col8" >CLP</td>
      <td id="T_1ab63_row4_col9" class="data row4 col9" >5.0000%</td>
      <td id="T_1ab63_row4_col10" class="data row4 col10" >Lin30360</td>
    </tr>
    <tr>
      <th id="T_1ab63_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_1ab63_row5_col0" class="data row5 col0" >2026-07-31</td>
      <td id="T_1ab63_row5_col1" class="data row5 col1" >2027-01-31</td>
      <td id="T_1ab63_row5_col2" class="data row5 col2" >2027-02-01</td>
      <td id="T_1ab63_row5_col3" class="data row5 col3" >300.00</td>
      <td id="T_1ab63_row5_col4" class="data row5 col4" >100.00</td>
      <td id="T_1ab63_row5_col5" class="data row5 col5" >7.50</td>
      <td id="T_1ab63_row5_col6" class="data row5 col6" >True</td>
      <td id="T_1ab63_row5_col7" class="data row5 col7" >107.50</td>
      <td id="T_1ab63_row5_col8" class="data row5 col8" >CLP</td>
      <td id="T_1ab63_row5_col9" class="data row5 col9" >5.0000%</td>
      <td id="T_1ab63_row5_col10" class="data row5 col10" >Lin30360</td>
    </tr>
    <tr>
      <th id="T_1ab63_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_1ab63_row6_col0" class="data row6 col0" >2027-01-31</td>
      <td id="T_1ab63_row6_col1" class="data row6 col1" >2027-07-31</td>
      <td id="T_1ab63_row6_col2" class="data row6 col2" >2027-08-02</td>
      <td id="T_1ab63_row6_col3" class="data row6 col3" >200.00</td>
      <td id="T_1ab63_row6_col4" class="data row6 col4" >100.00</td>
      <td id="T_1ab63_row6_col5" class="data row6 col5" >5.00</td>
      <td id="T_1ab63_row6_col6" class="data row6 col6" >True</td>
      <td id="T_1ab63_row6_col7" class="data row6 col7" >105.00</td>
      <td id="T_1ab63_row6_col8" class="data row6 col8" >CLP</td>
      <td id="T_1ab63_row6_col9" class="data row6 col9" >5.0000%</td>
      <td id="T_1ab63_row6_col10" class="data row6 col10" >Lin30360</td>
    </tr>
    <tr>
      <th id="T_1ab63_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_1ab63_row7_col0" class="data row7 col0" >2027-07-31</td>
      <td id="T_1ab63_row7_col1" class="data row7 col1" >2028-01-31</td>
      <td id="T_1ab63_row7_col2" class="data row7 col2" >2028-02-01</td>
      <td id="T_1ab63_row7_col3" class="data row7 col3" >100.00</td>
      <td id="T_1ab63_row7_col4" class="data row7 col4" >100.00</td>
      <td id="T_1ab63_row7_col5" class="data row7 col5" >2.50</td>
      <td id="T_1ab63_row7_col6" class="data row7 col6" >True</td>
      <td id="T_1ab63_row7_col7" class="data row7 col7" >102.50</td>
      <td id="T_1ab63_row7_col8" class="data row7 col8" >CLP</td>
      <td id="T_1ab63_row7_col9" class="data row7 col9" >5.0000%</td>
      <td id="T_1ab63_row7_col10" class="data row7 col10" >Lin30360</td>
    </tr>
  </tbody>
</table>




## Construcción Asistida de un `FixedRateMultiCurrencyLeg`

Se verá como construir objetos `Leg` donde cada `Cashflow` es un objeto de tipo `FixedRateMultiCurrencyCashflow`, todos con la misma tasa fija. En el primer ejemplo se construye un `Leg` de tipo *bullet*: una única amortización igual al capital vigente de todos los `FixedRateMultiCurrencyCasflow` en el último flujo.
Se requieren los siguientes parámetros:

- `RecPay`: enum que indica si los flujos se reciben o pagan
- `QCDate`: fecha de inicio del primer flujo
- `QCDate`: fecha final del último flujo sin considerar ajustes de días feriados
- `BusyAdRules`: enum que representa el tipo de ajuste en la fecha final para días feriados
- `Tenor`: la periodicidad de pago
- `QCInterestRateLeg::QCStubPeriod`: enum que representa el tipo de período irregular (si aplica)
- `QCBusinessCalendar`: calendario que aplica para las fechas de pago
- `unsigned int`: lag de pago expresado en días
- `float`: nominal inicial
- `bool`: si es `True` significa que la amortización es un flujo de caja efectivo
- `QCInterestRate`: la tasa a aplicar en cada flujo
- `QCCurrency`: moneda del nominal
- `bool`: si es `True` fuerza a que las fechas de pago coincidan con las fechas finales. Esto para lograr una valorización acorde a las convenciones de los mercados de renta fija, en caso que la `Leg` represente un bono a tasa fija.
- `SettLagBehaviour`: este parámetro indica cómo se calcula un `settlement_date` cuando un `end_date` cae en un día festivo.
---
**MultiCurrency**
- `QCCurrency`: moneda de los flujos
- `FXRateIndex`: índice con el cual se transforma cada flujo a la moneda de pago.
- `unsigned int`: lag de fijación del valor del índice de tipo de cambio.
- `FxFixingLagPivot`: este parámetro indica si el lag de fijación del índice FX se aplica sobre `end_date` o sobre `settlement_date`.
- `FxFixingLagAppliesTo`: indica si el lag se refiere a `FIXING_DATE` o `PUBISHING_DATE` del índice.

Vamos a un ejemplo.

Primero se debe dar de alta un FXRateIndex


```python
scl = aux.get_business_calendar('CL', range(2024, 2031))
ny = aux.get_business_calendar('US', range(2024, 2031))
scl_ny = scl + ny

usd = qcf.QCUSD()
clp = qcf.QCCLP()
usdclp = qcf.FXRate(usd, clp)
one_d = qcf.Tenor('1D')
usdclp_obs = qcf.FXRateIndex(
    usdclp, 
    'USDOBS', # Vamos a suponer que es el Dólar Observado
    one_d, 
    one_d, 
    scl,  # Es Santiago
)
```

Luego se dan de alta los otros parámetros requeridos para la construcción


```python
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(17, 7, 2024)
```

Vamos a aplicar un truco para el cálculo de la fecha final. Se define el plazo de la pata con un objeto de tipo `qcf.Tenor`.


```python
plazo = qcf.Tenor("6Y")
fecha_final = fecha_inicio.add_months(plazo.get_years() * 12 + plazo.get_months())
print(f"Fecha final: {fecha_final}")
```

    Fecha final: 2030-07-17


Vamos con el resto de parámetros.


```python
bus_adj_rule = qcf.BusyAdjRules.MODFOLLOW
periodicidad = qcf.Tenor('6M')
periodo_irregular = qcf.StubPeriod.NO
lag_pago = 1

valor_tasa = .03
tasa_cupon = qcf.QCInterestRate(
    valor_tasa, 
    qcf.QC30360(), 
    qcf.QCLinearWf()
)
es_bono = False
lag_pago = 0
sett_lag_behaviour = qcf.SettLagBehaviour.DONT_MOVE

fx_rate_index_fixing_lag = 2  # lag de fijación del índice FX
fx_fixing_lag_pivot = qcf.FxFixingLagPivot.END_DATE
fx_fixing_lag_applies_to = qcf.FxFixingLagAppliesTo.FIXING_DATE
```

Finalmente, se da de alta el objeto.


```python
fixed_rate_mccy_leg = qcf.LegFactory.build_bullet_fixed_rate_mccy_leg(
    rec_pay=rp,
    start_date=fecha_inicio,
    end_date=fecha_final,
    bus_adj_rule=bus_adj_rule,
    settlement_periodicity=periodicidad,
    settlement_stub_period=periodo_irregular,
    settlement_calendar=scl_ny,
    settlement_lag=lag_pago,
    initial_notional=nominal,
    amort_is_cashflow=amort_es_flujo,
    interest_rate=tasa_cupon,
    notional_currency=usd,
    is_bond=es_bono,
    sett_lag_behaviour=sett_lag_behaviour,
    # Parámetros MultiCurrency
    settlement_currency=clp,
    fx_rate_index=usdclp_obs,
    fx_rate_index_fixing_lag=fx_rate_index_fixing_lag,
    fx_fixing_lag_pivot=fx_fixing_lag_pivot,
    fx_fixing_lag_applies_to=fx_fixing_lag_applies_to
)
```


```python
scl_ny.shift(qcf.QCDate("2025-07-17"), -fx_rate_index_fixing_lag)
```




    2025-07-14



Visualización.


```python
df = aux.leg_as_dataframe(fixed_rate_mccy_leg)
df.style.format(aux.format_dict).set_properties(
    **{'background-color': '#FFCFC9', 'color':'black'},
    subset=['fecha_pago',]
).set_properties(
    **{'background-color': '#FFCFA9', 'color':'black'},
    subset=['fecha_fixing_fx']
)
```




<style type="text/css">
#T_faee0_row0_col2, #T_faee0_row1_col2, #T_faee0_row2_col2, #T_faee0_row3_col2, #T_faee0_row4_col2, #T_faee0_row5_col2, #T_faee0_row6_col2, #T_faee0_row7_col2, #T_faee0_row8_col2, #T_faee0_row9_col2, #T_faee0_row10_col2, #T_faee0_row11_col2 {
  background-color: #FFCFC9;
  color: black;
}
#T_faee0_row0_col11, #T_faee0_row1_col11, #T_faee0_row2_col11, #T_faee0_row3_col11, #T_faee0_row4_col11, #T_faee0_row5_col11, #T_faee0_row6_col11, #T_faee0_row7_col11, #T_faee0_row8_col11, #T_faee0_row9_col11, #T_faee0_row10_col11, #T_faee0_row11_col11 {
  background-color: #FFCFA9;
  color: black;
}
</style>
<table id="T_faee0">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_faee0_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_faee0_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_faee0_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_faee0_level0_col3" class="col_heading level0 col3" >nocional</th>
      <th id="T_faee0_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_faee0_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_faee0_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_faee0_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_faee0_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_faee0_level0_col9" class="col_heading level0 col9" >valor_tasa</th>
      <th id="T_faee0_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
      <th id="T_faee0_level0_col11" class="col_heading level0 col11" >fecha_fixing_fx</th>
      <th id="T_faee0_level0_col12" class="col_heading level0 col12" >moneda_pago</th>
      <th id="T_faee0_level0_col13" class="col_heading level0 col13" >indice_fx</th>
      <th id="T_faee0_level0_col14" class="col_heading level0 col14" >valor_indice_fx</th>
      <th id="T_faee0_level0_col15" class="col_heading level0 col15" >amortizacion_moneda_pago</th>
      <th id="T_faee0_level0_col16" class="col_heading level0 col16" >interes_moneda_pago</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_faee0_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_faee0_row0_col0" class="data row0 col0" >2024-07-17</td>
      <td id="T_faee0_row0_col1" class="data row0 col1" >2025-01-17</td>
      <td id="T_faee0_row0_col2" class="data row0 col2" >2025-01-17</td>
      <td id="T_faee0_row0_col3" class="data row0 col3" >100,000,000.00</td>
      <td id="T_faee0_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_faee0_row0_col5" class="data row0 col5" >1,500,000.00</td>
      <td id="T_faee0_row0_col6" class="data row0 col6" >True</td>
      <td id="T_faee0_row0_col7" class="data row0 col7" >1,500,000.00</td>
      <td id="T_faee0_row0_col8" class="data row0 col8" >USD</td>
      <td id="T_faee0_row0_col9" class="data row0 col9" >3.0000%</td>
      <td id="T_faee0_row0_col10" class="data row0 col10" >Lin30360</td>
      <td id="T_faee0_row0_col11" class="data row0 col11" >2025-01-16</td>
      <td id="T_faee0_row0_col12" class="data row0 col12" >CLP</td>
      <td id="T_faee0_row0_col13" class="data row0 col13" >USDOBS</td>
      <td id="T_faee0_row0_col14" class="data row0 col14" >1.00</td>
      <td id="T_faee0_row0_col15" class="data row0 col15" >0.00</td>
      <td id="T_faee0_row0_col16" class="data row0 col16" >1,500,000.00</td>
    </tr>
    <tr>
      <th id="T_faee0_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_faee0_row1_col0" class="data row1 col0" >2025-01-17</td>
      <td id="T_faee0_row1_col1" class="data row1 col1" >2025-07-17</td>
      <td id="T_faee0_row1_col2" class="data row1 col2" >2025-07-17</td>
      <td id="T_faee0_row1_col3" class="data row1 col3" >100,000,000.00</td>
      <td id="T_faee0_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_faee0_row1_col5" class="data row1 col5" >1,500,000.00</td>
      <td id="T_faee0_row1_col6" class="data row1 col6" >True</td>
      <td id="T_faee0_row1_col7" class="data row1 col7" >1,500,000.00</td>
      <td id="T_faee0_row1_col8" class="data row1 col8" >USD</td>
      <td id="T_faee0_row1_col9" class="data row1 col9" >3.0000%</td>
      <td id="T_faee0_row1_col10" class="data row1 col10" >Lin30360</td>
      <td id="T_faee0_row1_col11" class="data row1 col11" >2025-07-15</td>
      <td id="T_faee0_row1_col12" class="data row1 col12" >CLP</td>
      <td id="T_faee0_row1_col13" class="data row1 col13" >USDOBS</td>
      <td id="T_faee0_row1_col14" class="data row1 col14" >1.00</td>
      <td id="T_faee0_row1_col15" class="data row1 col15" >0.00</td>
      <td id="T_faee0_row1_col16" class="data row1 col16" >1,500,000.00</td>
    </tr>
    <tr>
      <th id="T_faee0_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_faee0_row2_col0" class="data row2 col0" >2025-07-17</td>
      <td id="T_faee0_row2_col1" class="data row2 col1" >2026-01-20</td>
      <td id="T_faee0_row2_col2" class="data row2 col2" >2026-01-20</td>
      <td id="T_faee0_row2_col3" class="data row2 col3" >100,000,000.00</td>
      <td id="T_faee0_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_faee0_row2_col5" class="data row2 col5" >1,525,000.00</td>
      <td id="T_faee0_row2_col6" class="data row2 col6" >True</td>
      <td id="T_faee0_row2_col7" class="data row2 col7" >1,525,000.00</td>
      <td id="T_faee0_row2_col8" class="data row2 col8" >USD</td>
      <td id="T_faee0_row2_col9" class="data row2 col9" >3.0000%</td>
      <td id="T_faee0_row2_col10" class="data row2 col10" >Lin30360</td>
      <td id="T_faee0_row2_col11" class="data row2 col11" >2026-01-16</td>
      <td id="T_faee0_row2_col12" class="data row2 col12" >CLP</td>
      <td id="T_faee0_row2_col13" class="data row2 col13" >USDOBS</td>
      <td id="T_faee0_row2_col14" class="data row2 col14" >1.00</td>
      <td id="T_faee0_row2_col15" class="data row2 col15" >0.00</td>
      <td id="T_faee0_row2_col16" class="data row2 col16" >1,525,000.00</td>
    </tr>
    <tr>
      <th id="T_faee0_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_faee0_row3_col0" class="data row3 col0" >2026-01-20</td>
      <td id="T_faee0_row3_col1" class="data row3 col1" >2026-07-17</td>
      <td id="T_faee0_row3_col2" class="data row3 col2" >2026-07-17</td>
      <td id="T_faee0_row3_col3" class="data row3 col3" >100,000,000.00</td>
      <td id="T_faee0_row3_col4" class="data row3 col4" >0.00</td>
      <td id="T_faee0_row3_col5" class="data row3 col5" >1,475,000.00</td>
      <td id="T_faee0_row3_col6" class="data row3 col6" >True</td>
      <td id="T_faee0_row3_col7" class="data row3 col7" >1,475,000.00</td>
      <td id="T_faee0_row3_col8" class="data row3 col8" >USD</td>
      <td id="T_faee0_row3_col9" class="data row3 col9" >3.0000%</td>
      <td id="T_faee0_row3_col10" class="data row3 col10" >Lin30360</td>
      <td id="T_faee0_row3_col11" class="data row3 col11" >2026-07-15</td>
      <td id="T_faee0_row3_col12" class="data row3 col12" >CLP</td>
      <td id="T_faee0_row3_col13" class="data row3 col13" >USDOBS</td>
      <td id="T_faee0_row3_col14" class="data row3 col14" >1.00</td>
      <td id="T_faee0_row3_col15" class="data row3 col15" >0.00</td>
      <td id="T_faee0_row3_col16" class="data row3 col16" >1,475,000.00</td>
    </tr>
    <tr>
      <th id="T_faee0_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_faee0_row4_col0" class="data row4 col0" >2026-07-17</td>
      <td id="T_faee0_row4_col1" class="data row4 col1" >2027-01-19</td>
      <td id="T_faee0_row4_col2" class="data row4 col2" >2027-01-19</td>
      <td id="T_faee0_row4_col3" class="data row4 col3" >100,000,000.00</td>
      <td id="T_faee0_row4_col4" class="data row4 col4" >0.00</td>
      <td id="T_faee0_row4_col5" class="data row4 col5" >1,516,666.67</td>
      <td id="T_faee0_row4_col6" class="data row4 col6" >True</td>
      <td id="T_faee0_row4_col7" class="data row4 col7" >1,516,666.67</td>
      <td id="T_faee0_row4_col8" class="data row4 col8" >USD</td>
      <td id="T_faee0_row4_col9" class="data row4 col9" >3.0000%</td>
      <td id="T_faee0_row4_col10" class="data row4 col10" >Lin30360</td>
      <td id="T_faee0_row4_col11" class="data row4 col11" >2027-01-15</td>
      <td id="T_faee0_row4_col12" class="data row4 col12" >CLP</td>
      <td id="T_faee0_row4_col13" class="data row4 col13" >USDOBS</td>
      <td id="T_faee0_row4_col14" class="data row4 col14" >1.00</td>
      <td id="T_faee0_row4_col15" class="data row4 col15" >0.00</td>
      <td id="T_faee0_row4_col16" class="data row4 col16" >1,516,666.67</td>
    </tr>
    <tr>
      <th id="T_faee0_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_faee0_row5_col0" class="data row5 col0" >2027-01-19</td>
      <td id="T_faee0_row5_col1" class="data row5 col1" >2027-07-19</td>
      <td id="T_faee0_row5_col2" class="data row5 col2" >2027-07-19</td>
      <td id="T_faee0_row5_col3" class="data row5 col3" >100,000,000.00</td>
      <td id="T_faee0_row5_col4" class="data row5 col4" >0.00</td>
      <td id="T_faee0_row5_col5" class="data row5 col5" >1,500,000.00</td>
      <td id="T_faee0_row5_col6" class="data row5 col6" >True</td>
      <td id="T_faee0_row5_col7" class="data row5 col7" >1,500,000.00</td>
      <td id="T_faee0_row5_col8" class="data row5 col8" >USD</td>
      <td id="T_faee0_row5_col9" class="data row5 col9" >3.0000%</td>
      <td id="T_faee0_row5_col10" class="data row5 col10" >Lin30360</td>
      <td id="T_faee0_row5_col11" class="data row5 col11" >2027-07-15</td>
      <td id="T_faee0_row5_col12" class="data row5 col12" >CLP</td>
      <td id="T_faee0_row5_col13" class="data row5 col13" >USDOBS</td>
      <td id="T_faee0_row5_col14" class="data row5 col14" >1.00</td>
      <td id="T_faee0_row5_col15" class="data row5 col15" >0.00</td>
      <td id="T_faee0_row5_col16" class="data row5 col16" >1,500,000.00</td>
    </tr>
    <tr>
      <th id="T_faee0_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_faee0_row6_col0" class="data row6 col0" >2027-07-19</td>
      <td id="T_faee0_row6_col1" class="data row6 col1" >2028-01-18</td>
      <td id="T_faee0_row6_col2" class="data row6 col2" >2028-01-18</td>
      <td id="T_faee0_row6_col3" class="data row6 col3" >100,000,000.00</td>
      <td id="T_faee0_row6_col4" class="data row6 col4" >0.00</td>
      <td id="T_faee0_row6_col5" class="data row6 col5" >1,491,666.67</td>
      <td id="T_faee0_row6_col6" class="data row6 col6" >True</td>
      <td id="T_faee0_row6_col7" class="data row6 col7" >1,491,666.67</td>
      <td id="T_faee0_row6_col8" class="data row6 col8" >USD</td>
      <td id="T_faee0_row6_col9" class="data row6 col9" >3.0000%</td>
      <td id="T_faee0_row6_col10" class="data row6 col10" >Lin30360</td>
      <td id="T_faee0_row6_col11" class="data row6 col11" >2028-01-14</td>
      <td id="T_faee0_row6_col12" class="data row6 col12" >CLP</td>
      <td id="T_faee0_row6_col13" class="data row6 col13" >USDOBS</td>
      <td id="T_faee0_row6_col14" class="data row6 col14" >1.00</td>
      <td id="T_faee0_row6_col15" class="data row6 col15" >0.00</td>
      <td id="T_faee0_row6_col16" class="data row6 col16" >1,491,666.67</td>
    </tr>
    <tr>
      <th id="T_faee0_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_faee0_row7_col0" class="data row7 col0" >2028-01-18</td>
      <td id="T_faee0_row7_col1" class="data row7 col1" >2028-07-17</td>
      <td id="T_faee0_row7_col2" class="data row7 col2" >2028-07-17</td>
      <td id="T_faee0_row7_col3" class="data row7 col3" >100,000,000.00</td>
      <td id="T_faee0_row7_col4" class="data row7 col4" >0.00</td>
      <td id="T_faee0_row7_col5" class="data row7 col5" >1,491,666.67</td>
      <td id="T_faee0_row7_col6" class="data row7 col6" >True</td>
      <td id="T_faee0_row7_col7" class="data row7 col7" >1,491,666.67</td>
      <td id="T_faee0_row7_col8" class="data row7 col8" >USD</td>
      <td id="T_faee0_row7_col9" class="data row7 col9" >3.0000%</td>
      <td id="T_faee0_row7_col10" class="data row7 col10" >Lin30360</td>
      <td id="T_faee0_row7_col11" class="data row7 col11" >2028-07-14</td>
      <td id="T_faee0_row7_col12" class="data row7 col12" >CLP</td>
      <td id="T_faee0_row7_col13" class="data row7 col13" >USDOBS</td>
      <td id="T_faee0_row7_col14" class="data row7 col14" >1.00</td>
      <td id="T_faee0_row7_col15" class="data row7 col15" >0.00</td>
      <td id="T_faee0_row7_col16" class="data row7 col16" >1,491,666.67</td>
    </tr>
    <tr>
      <th id="T_faee0_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_faee0_row8_col0" class="data row8 col0" >2028-07-17</td>
      <td id="T_faee0_row8_col1" class="data row8 col1" >2029-01-17</td>
      <td id="T_faee0_row8_col2" class="data row8 col2" >2029-01-17</td>
      <td id="T_faee0_row8_col3" class="data row8 col3" >100,000,000.00</td>
      <td id="T_faee0_row8_col4" class="data row8 col4" >0.00</td>
      <td id="T_faee0_row8_col5" class="data row8 col5" >1,500,000.00</td>
      <td id="T_faee0_row8_col6" class="data row8 col6" >True</td>
      <td id="T_faee0_row8_col7" class="data row8 col7" >1,500,000.00</td>
      <td id="T_faee0_row8_col8" class="data row8 col8" >USD</td>
      <td id="T_faee0_row8_col9" class="data row8 col9" >3.0000%</td>
      <td id="T_faee0_row8_col10" class="data row8 col10" >Lin30360</td>
      <td id="T_faee0_row8_col11" class="data row8 col11" >2029-01-15</td>
      <td id="T_faee0_row8_col12" class="data row8 col12" >CLP</td>
      <td id="T_faee0_row8_col13" class="data row8 col13" >USDOBS</td>
      <td id="T_faee0_row8_col14" class="data row8 col14" >1.00</td>
      <td id="T_faee0_row8_col15" class="data row8 col15" >0.00</td>
      <td id="T_faee0_row8_col16" class="data row8 col16" >1,500,000.00</td>
    </tr>
    <tr>
      <th id="T_faee0_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_faee0_row9_col0" class="data row9 col0" >2029-01-17</td>
      <td id="T_faee0_row9_col1" class="data row9 col1" >2029-07-17</td>
      <td id="T_faee0_row9_col2" class="data row9 col2" >2029-07-17</td>
      <td id="T_faee0_row9_col3" class="data row9 col3" >100,000,000.00</td>
      <td id="T_faee0_row9_col4" class="data row9 col4" >0.00</td>
      <td id="T_faee0_row9_col5" class="data row9 col5" >1,500,000.00</td>
      <td id="T_faee0_row9_col6" class="data row9 col6" >True</td>
      <td id="T_faee0_row9_col7" class="data row9 col7" >1,500,000.00</td>
      <td id="T_faee0_row9_col8" class="data row9 col8" >USD</td>
      <td id="T_faee0_row9_col9" class="data row9 col9" >3.0000%</td>
      <td id="T_faee0_row9_col10" class="data row9 col10" >Lin30360</td>
      <td id="T_faee0_row9_col11" class="data row9 col11" >2029-07-13</td>
      <td id="T_faee0_row9_col12" class="data row9 col12" >CLP</td>
      <td id="T_faee0_row9_col13" class="data row9 col13" >USDOBS</td>
      <td id="T_faee0_row9_col14" class="data row9 col14" >1.00</td>
      <td id="T_faee0_row9_col15" class="data row9 col15" >0.00</td>
      <td id="T_faee0_row9_col16" class="data row9 col16" >1,500,000.00</td>
    </tr>
    <tr>
      <th id="T_faee0_level0_row10" class="row_heading level0 row10" >10</th>
      <td id="T_faee0_row10_col0" class="data row10 col0" >2029-07-17</td>
      <td id="T_faee0_row10_col1" class="data row10 col1" >2030-01-17</td>
      <td id="T_faee0_row10_col2" class="data row10 col2" >2030-01-17</td>
      <td id="T_faee0_row10_col3" class="data row10 col3" >100,000,000.00</td>
      <td id="T_faee0_row10_col4" class="data row10 col4" >0.00</td>
      <td id="T_faee0_row10_col5" class="data row10 col5" >1,500,000.00</td>
      <td id="T_faee0_row10_col6" class="data row10 col6" >True</td>
      <td id="T_faee0_row10_col7" class="data row10 col7" >1,500,000.00</td>
      <td id="T_faee0_row10_col8" class="data row10 col8" >USD</td>
      <td id="T_faee0_row10_col9" class="data row10 col9" >3.0000%</td>
      <td id="T_faee0_row10_col10" class="data row10 col10" >Lin30360</td>
      <td id="T_faee0_row10_col11" class="data row10 col11" >2030-01-16</td>
      <td id="T_faee0_row10_col12" class="data row10 col12" >CLP</td>
      <td id="T_faee0_row10_col13" class="data row10 col13" >USDOBS</td>
      <td id="T_faee0_row10_col14" class="data row10 col14" >1.00</td>
      <td id="T_faee0_row10_col15" class="data row10 col15" >0.00</td>
      <td id="T_faee0_row10_col16" class="data row10 col16" >1,500,000.00</td>
    </tr>
    <tr>
      <th id="T_faee0_level0_row11" class="row_heading level0 row11" >11</th>
      <td id="T_faee0_row11_col0" class="data row11 col0" >2030-01-17</td>
      <td id="T_faee0_row11_col1" class="data row11 col1" >2030-07-17</td>
      <td id="T_faee0_row11_col2" class="data row11 col2" >2030-07-17</td>
      <td id="T_faee0_row11_col3" class="data row11 col3" >100,000,000.00</td>
      <td id="T_faee0_row11_col4" class="data row11 col4" >100,000,000.00</td>
      <td id="T_faee0_row11_col5" class="data row11 col5" >1,500,000.00</td>
      <td id="T_faee0_row11_col6" class="data row11 col6" >True</td>
      <td id="T_faee0_row11_col7" class="data row11 col7" >101,500,000.00</td>
      <td id="T_faee0_row11_col8" class="data row11 col8" >USD</td>
      <td id="T_faee0_row11_col9" class="data row11 col9" >3.0000%</td>
      <td id="T_faee0_row11_col10" class="data row11 col10" >Lin30360</td>
      <td id="T_faee0_row11_col11" class="data row11 col11" >2030-07-15</td>
      <td id="T_faee0_row11_col12" class="data row11 col12" >CLP</td>
      <td id="T_faee0_row11_col13" class="data row11 col13" >USDOBS</td>
      <td id="T_faee0_row11_col14" class="data row11 col14" >1.00</td>
      <td id="T_faee0_row11_col15" class="data row11 col15" >100,000,000.00</td>
      <td id="T_faee0_row11_col16" class="data row11 col16" >1,500,000.00</td>
    </tr>
  </tbody>
</table>




Veamos el efecto de cambiar la opción `fix_fixing_lag_pivot`.


```python
fx_fixing_lag_pivot = qcf.FxFixingLagPivot.END_DATE

fixed_rate_mccy_leg = qcf.LegFactory.build_bullet_fixed_rate_mccy_leg(
    rec_pay=rp,
    start_date=fecha_inicio,
    end_date=fecha_final,
    bus_adj_rule=bus_adj_rule,
    settlement_periodicity=periodicidad,
    settlement_stub_period=periodo_irregular,
    settlement_calendar=calendario,
    settlement_lag=lag_pago,
    initial_notional=nominal,
    amort_is_cashflow=amort_es_flujo,
    interest_rate=tasa_cupon,
    notional_currency=usd,
    settlement_currency=clp,
    is_bond=es_bono,
    sett_lag_behaviour=sett_lag_behaviour,
    # Parámetros MultiCurrency
    fx_rate_index=usdclp_obs,
    fx_rate_index_fixing_lag=fx_rate_index_fixing_lag,
    fx_fixing_lag_pivot=fx_fixing_lag_pivot,
)
```


```python
df = aux.leg_as_dataframe(fixed_rate_mccy_leg)
df.style.format(aux.format_dict).set_properties(
    **{'background-color': '#FFCFC9', 'color':'black'},
    subset=['fecha_final',]
).set_properties(
    **{'background-color': '#FFCFA9', 'color':'black'},
    subset=['fecha_fixing_fx']
)
```




<style type="text/css">
#T_884e2_row0_col1, #T_884e2_row1_col1, #T_884e2_row2_col1, #T_884e2_row3_col1, #T_884e2_row4_col1, #T_884e2_row5_col1, #T_884e2_row6_col1, #T_884e2_row7_col1, #T_884e2_row8_col1, #T_884e2_row9_col1, #T_884e2_row10_col1, #T_884e2_row11_col1 {
  background-color: #FFCFC9;
  color: black;
}
#T_884e2_row0_col11, #T_884e2_row1_col11, #T_884e2_row2_col11, #T_884e2_row3_col11, #T_884e2_row4_col11, #T_884e2_row5_col11, #T_884e2_row6_col11, #T_884e2_row7_col11, #T_884e2_row8_col11, #T_884e2_row9_col11, #T_884e2_row10_col11, #T_884e2_row11_col11 {
  background-color: #FFCFA9;
  color: black;
}
</style>
<table id="T_884e2">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_884e2_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_884e2_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_884e2_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_884e2_level0_col3" class="col_heading level0 col3" >nocional</th>
      <th id="T_884e2_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_884e2_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_884e2_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_884e2_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_884e2_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_884e2_level0_col9" class="col_heading level0 col9" >valor_tasa</th>
      <th id="T_884e2_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
      <th id="T_884e2_level0_col11" class="col_heading level0 col11" >fecha_fixing_fx</th>
      <th id="T_884e2_level0_col12" class="col_heading level0 col12" >moneda_pago</th>
      <th id="T_884e2_level0_col13" class="col_heading level0 col13" >indice_fx</th>
      <th id="T_884e2_level0_col14" class="col_heading level0 col14" >valor_indice_fx</th>
      <th id="T_884e2_level0_col15" class="col_heading level0 col15" >amortizacion_moneda_pago</th>
      <th id="T_884e2_level0_col16" class="col_heading level0 col16" >interes_moneda_pago</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_884e2_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_884e2_row0_col0" class="data row0 col0" >2024-07-17</td>
      <td id="T_884e2_row0_col1" class="data row0 col1" >2025-01-17</td>
      <td id="T_884e2_row0_col2" class="data row0 col2" >2025-01-17</td>
      <td id="T_884e2_row0_col3" class="data row0 col3" >100,000,000.00</td>
      <td id="T_884e2_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_884e2_row0_col5" class="data row0 col5" >1,500,000.00</td>
      <td id="T_884e2_row0_col6" class="data row0 col6" >True</td>
      <td id="T_884e2_row0_col7" class="data row0 col7" >1,500,000.00</td>
      <td id="T_884e2_row0_col8" class="data row0 col8" >USD</td>
      <td id="T_884e2_row0_col9" class="data row0 col9" >3.0000%</td>
      <td id="T_884e2_row0_col10" class="data row0 col10" >Lin30360</td>
      <td id="T_884e2_row0_col11" class="data row0 col11" >2025-01-15</td>
      <td id="T_884e2_row0_col12" class="data row0 col12" >CLP</td>
      <td id="T_884e2_row0_col13" class="data row0 col13" >USDOBS</td>
      <td id="T_884e2_row0_col14" class="data row0 col14" >1.00</td>
      <td id="T_884e2_row0_col15" class="data row0 col15" >0.00</td>
      <td id="T_884e2_row0_col16" class="data row0 col16" >1,500,000.00</td>
    </tr>
    <tr>
      <th id="T_884e2_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_884e2_row1_col0" class="data row1 col0" >2025-01-17</td>
      <td id="T_884e2_row1_col1" class="data row1 col1" >2025-07-17</td>
      <td id="T_884e2_row1_col2" class="data row1 col2" >2025-07-17</td>
      <td id="T_884e2_row1_col3" class="data row1 col3" >100,000,000.00</td>
      <td id="T_884e2_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_884e2_row1_col5" class="data row1 col5" >1,500,000.00</td>
      <td id="T_884e2_row1_col6" class="data row1 col6" >True</td>
      <td id="T_884e2_row1_col7" class="data row1 col7" >1,500,000.00</td>
      <td id="T_884e2_row1_col8" class="data row1 col8" >USD</td>
      <td id="T_884e2_row1_col9" class="data row1 col9" >3.0000%</td>
      <td id="T_884e2_row1_col10" class="data row1 col10" >Lin30360</td>
      <td id="T_884e2_row1_col11" class="data row1 col11" >2025-07-15</td>
      <td id="T_884e2_row1_col12" class="data row1 col12" >CLP</td>
      <td id="T_884e2_row1_col13" class="data row1 col13" >USDOBS</td>
      <td id="T_884e2_row1_col14" class="data row1 col14" >1.00</td>
      <td id="T_884e2_row1_col15" class="data row1 col15" >0.00</td>
      <td id="T_884e2_row1_col16" class="data row1 col16" >1,500,000.00</td>
    </tr>
    <tr>
      <th id="T_884e2_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_884e2_row2_col0" class="data row2 col0" >2025-07-17</td>
      <td id="T_884e2_row2_col1" class="data row2 col1" >2026-01-20</td>
      <td id="T_884e2_row2_col2" class="data row2 col2" >2026-01-20</td>
      <td id="T_884e2_row2_col3" class="data row2 col3" >100,000,000.00</td>
      <td id="T_884e2_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_884e2_row2_col5" class="data row2 col5" >1,525,000.00</td>
      <td id="T_884e2_row2_col6" class="data row2 col6" >True</td>
      <td id="T_884e2_row2_col7" class="data row2 col7" >1,525,000.00</td>
      <td id="T_884e2_row2_col8" class="data row2 col8" >USD</td>
      <td id="T_884e2_row2_col9" class="data row2 col9" >3.0000%</td>
      <td id="T_884e2_row2_col10" class="data row2 col10" >Lin30360</td>
      <td id="T_884e2_row2_col11" class="data row2 col11" >2026-01-15</td>
      <td id="T_884e2_row2_col12" class="data row2 col12" >CLP</td>
      <td id="T_884e2_row2_col13" class="data row2 col13" >USDOBS</td>
      <td id="T_884e2_row2_col14" class="data row2 col14" >1.00</td>
      <td id="T_884e2_row2_col15" class="data row2 col15" >0.00</td>
      <td id="T_884e2_row2_col16" class="data row2 col16" >1,525,000.00</td>
    </tr>
    <tr>
      <th id="T_884e2_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_884e2_row3_col0" class="data row3 col0" >2026-01-20</td>
      <td id="T_884e2_row3_col1" class="data row3 col1" >2026-07-17</td>
      <td id="T_884e2_row3_col2" class="data row3 col2" >2026-07-17</td>
      <td id="T_884e2_row3_col3" class="data row3 col3" >100,000,000.00</td>
      <td id="T_884e2_row3_col4" class="data row3 col4" >0.00</td>
      <td id="T_884e2_row3_col5" class="data row3 col5" >1,475,000.00</td>
      <td id="T_884e2_row3_col6" class="data row3 col6" >True</td>
      <td id="T_884e2_row3_col7" class="data row3 col7" >1,475,000.00</td>
      <td id="T_884e2_row3_col8" class="data row3 col8" >USD</td>
      <td id="T_884e2_row3_col9" class="data row3 col9" >3.0000%</td>
      <td id="T_884e2_row3_col10" class="data row3 col10" >Lin30360</td>
      <td id="T_884e2_row3_col11" class="data row3 col11" >2026-07-15</td>
      <td id="T_884e2_row3_col12" class="data row3 col12" >CLP</td>
      <td id="T_884e2_row3_col13" class="data row3 col13" >USDOBS</td>
      <td id="T_884e2_row3_col14" class="data row3 col14" >1.00</td>
      <td id="T_884e2_row3_col15" class="data row3 col15" >0.00</td>
      <td id="T_884e2_row3_col16" class="data row3 col16" >1,475,000.00</td>
    </tr>
    <tr>
      <th id="T_884e2_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_884e2_row4_col0" class="data row4 col0" >2026-07-17</td>
      <td id="T_884e2_row4_col1" class="data row4 col1" >2027-01-18</td>
      <td id="T_884e2_row4_col2" class="data row4 col2" >2027-01-18</td>
      <td id="T_884e2_row4_col3" class="data row4 col3" >100,000,000.00</td>
      <td id="T_884e2_row4_col4" class="data row4 col4" >0.00</td>
      <td id="T_884e2_row4_col5" class="data row4 col5" >1,508,333.33</td>
      <td id="T_884e2_row4_col6" class="data row4 col6" >True</td>
      <td id="T_884e2_row4_col7" class="data row4 col7" >1,508,333.33</td>
      <td id="T_884e2_row4_col8" class="data row4 col8" >USD</td>
      <td id="T_884e2_row4_col9" class="data row4 col9" >3.0000%</td>
      <td id="T_884e2_row4_col10" class="data row4 col10" >Lin30360</td>
      <td id="T_884e2_row4_col11" class="data row4 col11" >2027-01-14</td>
      <td id="T_884e2_row4_col12" class="data row4 col12" >CLP</td>
      <td id="T_884e2_row4_col13" class="data row4 col13" >USDOBS</td>
      <td id="T_884e2_row4_col14" class="data row4 col14" >1.00</td>
      <td id="T_884e2_row4_col15" class="data row4 col15" >0.00</td>
      <td id="T_884e2_row4_col16" class="data row4 col16" >1,508,333.33</td>
    </tr>
    <tr>
      <th id="T_884e2_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_884e2_row5_col0" class="data row5 col0" >2027-01-18</td>
      <td id="T_884e2_row5_col1" class="data row5 col1" >2027-07-19</td>
      <td id="T_884e2_row5_col2" class="data row5 col2" >2027-07-19</td>
      <td id="T_884e2_row5_col3" class="data row5 col3" >100,000,000.00</td>
      <td id="T_884e2_row5_col4" class="data row5 col4" >0.00</td>
      <td id="T_884e2_row5_col5" class="data row5 col5" >1,508,333.33</td>
      <td id="T_884e2_row5_col6" class="data row5 col6" >True</td>
      <td id="T_884e2_row5_col7" class="data row5 col7" >1,508,333.33</td>
      <td id="T_884e2_row5_col8" class="data row5 col8" >USD</td>
      <td id="T_884e2_row5_col9" class="data row5 col9" >3.0000%</td>
      <td id="T_884e2_row5_col10" class="data row5 col10" >Lin30360</td>
      <td id="T_884e2_row5_col11" class="data row5 col11" >2027-07-15</td>
      <td id="T_884e2_row5_col12" class="data row5 col12" >CLP</td>
      <td id="T_884e2_row5_col13" class="data row5 col13" >USDOBS</td>
      <td id="T_884e2_row5_col14" class="data row5 col14" >1.00</td>
      <td id="T_884e2_row5_col15" class="data row5 col15" >0.00</td>
      <td id="T_884e2_row5_col16" class="data row5 col16" >1,508,333.33</td>
    </tr>
    <tr>
      <th id="T_884e2_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_884e2_row6_col0" class="data row6 col0" >2027-07-19</td>
      <td id="T_884e2_row6_col1" class="data row6 col1" >2028-01-17</td>
      <td id="T_884e2_row6_col2" class="data row6 col2" >2028-01-17</td>
      <td id="T_884e2_row6_col3" class="data row6 col3" >100,000,000.00</td>
      <td id="T_884e2_row6_col4" class="data row6 col4" >0.00</td>
      <td id="T_884e2_row6_col5" class="data row6 col5" >1,483,333.33</td>
      <td id="T_884e2_row6_col6" class="data row6 col6" >True</td>
      <td id="T_884e2_row6_col7" class="data row6 col7" >1,483,333.33</td>
      <td id="T_884e2_row6_col8" class="data row6 col8" >USD</td>
      <td id="T_884e2_row6_col9" class="data row6 col9" >3.0000%</td>
      <td id="T_884e2_row6_col10" class="data row6 col10" >Lin30360</td>
      <td id="T_884e2_row6_col11" class="data row6 col11" >2028-01-13</td>
      <td id="T_884e2_row6_col12" class="data row6 col12" >CLP</td>
      <td id="T_884e2_row6_col13" class="data row6 col13" >USDOBS</td>
      <td id="T_884e2_row6_col14" class="data row6 col14" >1.00</td>
      <td id="T_884e2_row6_col15" class="data row6 col15" >0.00</td>
      <td id="T_884e2_row6_col16" class="data row6 col16" >1,483,333.33</td>
    </tr>
    <tr>
      <th id="T_884e2_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_884e2_row7_col0" class="data row7 col0" >2028-01-17</td>
      <td id="T_884e2_row7_col1" class="data row7 col1" >2028-07-17</td>
      <td id="T_884e2_row7_col2" class="data row7 col2" >2028-07-17</td>
      <td id="T_884e2_row7_col3" class="data row7 col3" >100,000,000.00</td>
      <td id="T_884e2_row7_col4" class="data row7 col4" >0.00</td>
      <td id="T_884e2_row7_col5" class="data row7 col5" >1,500,000.00</td>
      <td id="T_884e2_row7_col6" class="data row7 col6" >True</td>
      <td id="T_884e2_row7_col7" class="data row7 col7" >1,500,000.00</td>
      <td id="T_884e2_row7_col8" class="data row7 col8" >USD</td>
      <td id="T_884e2_row7_col9" class="data row7 col9" >3.0000%</td>
      <td id="T_884e2_row7_col10" class="data row7 col10" >Lin30360</td>
      <td id="T_884e2_row7_col11" class="data row7 col11" >2028-07-13</td>
      <td id="T_884e2_row7_col12" class="data row7 col12" >CLP</td>
      <td id="T_884e2_row7_col13" class="data row7 col13" >USDOBS</td>
      <td id="T_884e2_row7_col14" class="data row7 col14" >1.00</td>
      <td id="T_884e2_row7_col15" class="data row7 col15" >0.00</td>
      <td id="T_884e2_row7_col16" class="data row7 col16" >1,500,000.00</td>
    </tr>
    <tr>
      <th id="T_884e2_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_884e2_row8_col0" class="data row8 col0" >2028-07-17</td>
      <td id="T_884e2_row8_col1" class="data row8 col1" >2029-01-17</td>
      <td id="T_884e2_row8_col2" class="data row8 col2" >2029-01-17</td>
      <td id="T_884e2_row8_col3" class="data row8 col3" >100,000,000.00</td>
      <td id="T_884e2_row8_col4" class="data row8 col4" >0.00</td>
      <td id="T_884e2_row8_col5" class="data row8 col5" >1,500,000.00</td>
      <td id="T_884e2_row8_col6" class="data row8 col6" >True</td>
      <td id="T_884e2_row8_col7" class="data row8 col7" >1,500,000.00</td>
      <td id="T_884e2_row8_col8" class="data row8 col8" >USD</td>
      <td id="T_884e2_row8_col9" class="data row8 col9" >3.0000%</td>
      <td id="T_884e2_row8_col10" class="data row8 col10" >Lin30360</td>
      <td id="T_884e2_row8_col11" class="data row8 col11" >2029-01-15</td>
      <td id="T_884e2_row8_col12" class="data row8 col12" >CLP</td>
      <td id="T_884e2_row8_col13" class="data row8 col13" >USDOBS</td>
      <td id="T_884e2_row8_col14" class="data row8 col14" >1.00</td>
      <td id="T_884e2_row8_col15" class="data row8 col15" >0.00</td>
      <td id="T_884e2_row8_col16" class="data row8 col16" >1,500,000.00</td>
    </tr>
    <tr>
      <th id="T_884e2_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_884e2_row9_col0" class="data row9 col0" >2029-01-17</td>
      <td id="T_884e2_row9_col1" class="data row9 col1" >2029-07-17</td>
      <td id="T_884e2_row9_col2" class="data row9 col2" >2029-07-17</td>
      <td id="T_884e2_row9_col3" class="data row9 col3" >100,000,000.00</td>
      <td id="T_884e2_row9_col4" class="data row9 col4" >0.00</td>
      <td id="T_884e2_row9_col5" class="data row9 col5" >1,500,000.00</td>
      <td id="T_884e2_row9_col6" class="data row9 col6" >True</td>
      <td id="T_884e2_row9_col7" class="data row9 col7" >1,500,000.00</td>
      <td id="T_884e2_row9_col8" class="data row9 col8" >USD</td>
      <td id="T_884e2_row9_col9" class="data row9 col9" >3.0000%</td>
      <td id="T_884e2_row9_col10" class="data row9 col10" >Lin30360</td>
      <td id="T_884e2_row9_col11" class="data row9 col11" >2029-07-13</td>
      <td id="T_884e2_row9_col12" class="data row9 col12" >CLP</td>
      <td id="T_884e2_row9_col13" class="data row9 col13" >USDOBS</td>
      <td id="T_884e2_row9_col14" class="data row9 col14" >1.00</td>
      <td id="T_884e2_row9_col15" class="data row9 col15" >0.00</td>
      <td id="T_884e2_row9_col16" class="data row9 col16" >1,500,000.00</td>
    </tr>
    <tr>
      <th id="T_884e2_level0_row10" class="row_heading level0 row10" >10</th>
      <td id="T_884e2_row10_col0" class="data row10 col0" >2029-07-17</td>
      <td id="T_884e2_row10_col1" class="data row10 col1" >2030-01-17</td>
      <td id="T_884e2_row10_col2" class="data row10 col2" >2030-01-17</td>
      <td id="T_884e2_row10_col3" class="data row10 col3" >100,000,000.00</td>
      <td id="T_884e2_row10_col4" class="data row10 col4" >0.00</td>
      <td id="T_884e2_row10_col5" class="data row10 col5" >1,500,000.00</td>
      <td id="T_884e2_row10_col6" class="data row10 col6" >True</td>
      <td id="T_884e2_row10_col7" class="data row10 col7" >1,500,000.00</td>
      <td id="T_884e2_row10_col8" class="data row10 col8" >USD</td>
      <td id="T_884e2_row10_col9" class="data row10 col9" >3.0000%</td>
      <td id="T_884e2_row10_col10" class="data row10 col10" >Lin30360</td>
      <td id="T_884e2_row10_col11" class="data row10 col11" >2030-01-15</td>
      <td id="T_884e2_row10_col12" class="data row10 col12" >CLP</td>
      <td id="T_884e2_row10_col13" class="data row10 col13" >USDOBS</td>
      <td id="T_884e2_row10_col14" class="data row10 col14" >1.00</td>
      <td id="T_884e2_row10_col15" class="data row10 col15" >0.00</td>
      <td id="T_884e2_row10_col16" class="data row10 col16" >1,500,000.00</td>
    </tr>
    <tr>
      <th id="T_884e2_level0_row11" class="row_heading level0 row11" >11</th>
      <td id="T_884e2_row11_col0" class="data row11 col0" >2030-01-17</td>
      <td id="T_884e2_row11_col1" class="data row11 col1" >2030-07-17</td>
      <td id="T_884e2_row11_col2" class="data row11 col2" >2030-07-17</td>
      <td id="T_884e2_row11_col3" class="data row11 col3" >100,000,000.00</td>
      <td id="T_884e2_row11_col4" class="data row11 col4" >100,000,000.00</td>
      <td id="T_884e2_row11_col5" class="data row11 col5" >1,500,000.00</td>
      <td id="T_884e2_row11_col6" class="data row11 col6" >True</td>
      <td id="T_884e2_row11_col7" class="data row11 col7" >101,500,000.00</td>
      <td id="T_884e2_row11_col8" class="data row11 col8" >USD</td>
      <td id="T_884e2_row11_col9" class="data row11 col9" >3.0000%</td>
      <td id="T_884e2_row11_col10" class="data row11 col10" >Lin30360</td>
      <td id="T_884e2_row11_col11" class="data row11 col11" >2030-07-15</td>
      <td id="T_884e2_row11_col12" class="data row11 col12" >CLP</td>
      <td id="T_884e2_row11_col13" class="data row11 col13" >USDOBS</td>
      <td id="T_884e2_row11_col14" class="data row11 col14" >1.00</td>
      <td id="T_884e2_row11_col15" class="data row11 col15" >100,000,000.00</td>
      <td id="T_884e2_row11_col16" class="data row11 col16" >1,500,000.00</td>
    </tr>
  </tbody>
</table>




## Construcción Asistida de un `CustomAmortFixedRateMultiCurrencyLeg`

Se verá como construir objetos `Leg` donde cada `Cashflow` es un objeto de tipo `FixedRateMultiCurrencyCashflow`, todos con la misma tasa fija. En este ejemplo se construye un `Leg` de tipo *custom_amort*: amortizaciones irregulares en cada `FixedRateMultiCurrencyCasflow`.
Se requieren los siguientes parámetros:

- `RecPay`: enum que indica si los flujos se reciben o pagan
- `QCDate`: fecha de inicio del primer flujo
- `QCDate`: fecha final del último flujo sin considerar ajustes de días feriados
- `BusyAdRules`: enum que representa el tipo de ajuste en la fecha final para días feriados
- `Tenor`: la periodicidad de pago
- `QCInterestRateLeg::QCStubPeriod`: enum que representa el tipo de período irregular (si aplica)
- `QCBusinessCalendar`: calendario que aplica para las fechas de pago
- `unsigned int`: lag de pago expresado en días
- `float`: nominal inicial
- `bool`: si es `True` significa que la amortización es un flujo de caja efectivo
- `QCInterestRate`: la tasa a aplicar en cada flujo
- `QCCurrency`: moneda del nominal
- `QCCurrency`: moneda de los flujos
- `FXRateIndex`: índice con el cual se transforma cada flujo a la moneda de pago.
- `bool`: si es `True` fuerza a que las fechas de pago coincidan con las fechas finales. Esto para lograr una valorización acorde a las convenciones de los mercados de renta fija, en caso que la `Leg` represente un bono a tasa fija.
- `SettLagBehaviour`: este parámetro indica cómo se calcula un `settlement_date` cuando un `end_date` cae en un día festivo.
- `FxFixingLagPivot`: este parámetro indica si el lag de fijación del índice FX se aplica sobre `end_date` o sobre `settlement_date`.

Vamos a un ejemplo

Primero se debe dar de alta un FXRateIndex


```python
usd = qcf.QCUSD()
clp = qcf.QCCLP()
usdclp = qcf.FXRate(usd, clp)
one_d = qcf.Tenor('1D')
usdclp_obs = qcf.FXRateIndex(
    usdclp, 
    'USDOBS', 
    one_d, 
    one_d, 
    calendario
)
```

Luego se dan de alta los otros parámetros requeridos para la construcción


```python
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(12, 7, 1968)
fecha_final = qcf.QCDate(12, 7, 1974) 
bus_adj_rule = qcf.BusyAdjRules.NO
periodicidad = qcf.Tenor('6M')
periodo_irregular = qcf.StubPeriod.NO
lag_pago = 1
es_bono = False
fx_rate_index_fixing_lag = 1
fx_fixing_lag_pivot = qcf.FxFixingLagPivot.SETTLEMENT_DATE
sett_lag_behaviour = qcf.SettLagBehaviour.DONT_MOVE
```

Se da de alta el vector de capitales vigentes y amortizaciones. Cada elemento del vector es el capital vigente y amortización del correspondiente cupón.


```python
custom_notional_amort = qcf.CustomNotionalAmort()
custom_notional_amort.set_size(12)  # De la fecha inicio y fecha final se deduce que serán 8 cupones
for i in range(0, 12):
    custom_notional_amort.set_notional_amort_at(i, 1200.0 - i * 100.0, 100.0)
```

Finalmente, se da de alta el objeto.


```python
fixed_rate_mccy_leg = qcf.LegFactory.build_custom_amort_fixed_rate_mccy_leg(
    rec_pay=rp,
    start_date=fecha_inicio,
    end_date=fecha_final,
    bus_adj_rule=bus_adj_rule,
    settlement_periodicity=periodicidad,
    settlement_stub_period=periodo_irregular,
    settlement_calendar=calendario,
    settlement_lag=lag_pago,
    notional_and_amort=custom_notional_amort,
    amort_is_cashflow=amort_es_flujo,
    interest_rate=tasa_cupon,
    notional_currency=usd,
    is_bond=es_bono,
    sett_lag_behaviour=sett_lag_behaviour,
    # Parámetros MultiCurrency
    settlement_currency=clp,
    fx_rate_index=usdclp_obs,
    fx_rate_index_fixing_lag=fx_rate_index_fixing_lag,
    fx_fixing_lag_pivot=fx_fixing_lag_pivot,
)
```

Visualización.


```python
aux.leg_as_dataframe(fixed_rate_mccy_leg).style.format(aux.format_dict).set_properties(
    **{'background-color': '#FFCFC9', 'color':'black'},
    subset=['nominal','amortizacion', 'flujo']
).set_properties(
    **{'background-color': '#FFCFA9', 'color':'black'},
    subset=['flujo']
)
```


    ---------------------------------------------------------------------------

    KeyError                                  Traceback (most recent call last)

    File ~/qcf_repos/qcfinancial-docs/.venv/lib/python3.12/site-packages/IPython/core/formatters.py:406, in BaseFormatter.__call__(self, obj)
        404     method = get_real_method(obj, self.print_method)
        405     if method is not None:
    --> 406         return method()
        407     return None
        408 else:


    File ~/qcf_repos/qcfinancial-docs/.venv/lib/python3.12/site-packages/pandas/io/formats/style.py:405, in Styler._repr_html_(self)
        400 """
        401 Hooks into Jupyter notebook rich display system, which calls _repr_html_ by
        402 default if an object is returned at the end of a cell.
        403 """
        404 if get_option("styler.render.repr") == "html":
    --> 405     return self.to_html()
        406 return None


    File ~/qcf_repos/qcfinancial-docs/.venv/lib/python3.12/site-packages/pandas/io/formats/style.py:1345, in Styler.to_html(self, buf, table_uuid, table_attributes, sparse_index, sparse_columns, bold_headers, caption, max_rows, max_columns, encoding, doctype_html, exclude_styles, **kwargs)
       1342     obj.set_caption(caption)
       1344 # Build HTML string..
    -> 1345 html = obj._render_html(
       1346     sparse_index=sparse_index,
       1347     sparse_columns=sparse_columns,
       1348     max_rows=max_rows,
       1349     max_cols=max_columns,
       1350     exclude_styles=exclude_styles,
       1351     encoding=encoding or get_option("styler.render.encoding"),
       1352     doctype_html=doctype_html,
       1353     **kwargs,
       1354 )
       1356 return save_to_buffer(
       1357     html, buf=buf, encoding=(encoding if buf is not None else None)
       1358 )


    File ~/qcf_repos/qcfinancial-docs/.venv/lib/python3.12/site-packages/pandas/io/formats/style_render.py:204, in StylerRenderer._render_html(self, sparse_index, sparse_columns, max_rows, max_cols, **kwargs)
        192 def _render_html(
        193     self,
        194     sparse_index: bool,
       (...)    198     **kwargs,
        199 ) -> str:
        200     """
        201     Renders the ``Styler`` including all applied styles to HTML.
        202     Generates a dict with necessary kwargs passed to jinja2 template.
        203     """
    --> 204     d = self._render(sparse_index, sparse_columns, max_rows, max_cols, "&nbsp;")
        205     d.update(kwargs)
        206     return self.template_html.render(
        207         **d,
        208         html_table_tpl=self.template_html_table,
        209         html_style_tpl=self.template_html_style,
        210     )


    File ~/qcf_repos/qcfinancial-docs/.venv/lib/python3.12/site-packages/pandas/io/formats/style_render.py:161, in StylerRenderer._render(self, sparse_index, sparse_columns, max_rows, max_cols, blank)
        147 def _render(
        148     self,
        149     sparse_index: bool,
       (...)    153     blank: str = "",
        154 ):
        155     """
        156     Computes and applies styles and then generates the general render dicts.
        157 
        158     Also extends the `ctx` and `ctx_index` attributes with those of concatenated
        159     stylers for use within `_translate_latex`
        160     """
    --> 161     self._compute()
        162     dxs = []
        163     ctx_len = len(self.index)


    File ~/qcf_repos/qcfinancial-docs/.venv/lib/python3.12/site-packages/pandas/io/formats/style_render.py:256, in StylerRenderer._compute(self)
        254 r = self
        255 for func, args, kwargs in self._todo:
    --> 256     r = func(self)(*args, **kwargs)
        257 return r


    File ~/qcf_repos/qcfinancial-docs/.venv/lib/python3.12/site-packages/pandas/io/formats/style.py:2027, in Styler._map(self, func, subset, **kwargs)
       2025     subset = IndexSlice[:]
       2026 subset = non_reducing_slice(subset)
    -> 2027 result = self.data.loc[subset].map(func)
       2028 self._update_ctx(result)
       2029 return self


    File ~/qcf_repos/qcfinancial-docs/.venv/lib/python3.12/site-packages/pandas/core/indexing.py:1184, in _LocationIndexer.__getitem__(self, key)
       1182     if self._is_scalar_access(key):
       1183         return self.obj._get_value(*key, takeable=self._takeable)
    -> 1184     return self._getitem_tuple(key)
       1185 else:
       1186     # we by definition only have the 0th axis
       1187     axis = self.axis or 0


    File ~/qcf_repos/qcfinancial-docs/.venv/lib/python3.12/site-packages/pandas/core/indexing.py:1377, in _LocIndexer._getitem_tuple(self, tup)
       1374 if self._multi_take_opportunity(tup):
       1375     return self._multi_take(tup)
    -> 1377 return self._getitem_tuple_same_dim(tup)


    File ~/qcf_repos/qcfinancial-docs/.venv/lib/python3.12/site-packages/pandas/core/indexing.py:1020, in _LocationIndexer._getitem_tuple_same_dim(self, tup)
       1017 if com.is_null_slice(key):
       1018     continue
    -> 1020 retval = getattr(retval, self.name)._getitem_axis(key, axis=i)
       1021 # We should never have retval.ndim < self.ndim, as that should
       1022 #  be handled by the _getitem_lowerdim call above.
       1023 assert retval.ndim == self.ndim


    File ~/qcf_repos/qcfinancial-docs/.venv/lib/python3.12/site-packages/pandas/core/indexing.py:1420, in _LocIndexer._getitem_axis(self, key, axis)
       1417     if hasattr(key, "ndim") and key.ndim > 1:
       1418         raise ValueError("Cannot index with multidimensional key")
    -> 1420     return self._getitem_iterable(key, axis=axis)
       1422 # nested tuple slicing
       1423 if is_nested_tuple(key, labels):


    File ~/qcf_repos/qcfinancial-docs/.venv/lib/python3.12/site-packages/pandas/core/indexing.py:1360, in _LocIndexer._getitem_iterable(self, key, axis)
       1357 self._validate_key(key, axis)
       1359 # A collection of keys
    -> 1360 keyarr, indexer = self._get_listlike_indexer(key, axis)
       1361 return self.obj._reindex_with_indexers(
       1362     {axis: [keyarr, indexer]}, copy=True, allow_dups=True
       1363 )


    File ~/qcf_repos/qcfinancial-docs/.venv/lib/python3.12/site-packages/pandas/core/indexing.py:1558, in _LocIndexer._get_listlike_indexer(self, key, axis)
       1555 ax = self.obj._get_axis(axis)
       1556 axis_name = self.obj._get_axis_name(axis)
    -> 1558 keyarr, indexer = ax._get_indexer_strict(key, axis_name)
       1560 return keyarr, indexer


    File ~/qcf_repos/qcfinancial-docs/.venv/lib/python3.12/site-packages/pandas/core/indexes/base.py:6212, in Index._get_indexer_strict(self, key, axis_name)
       6209 else:
       6210     keyarr, indexer, new_indexer = self._reindex_non_unique(keyarr)
    -> 6212 self._raise_if_missing(keyarr, indexer, axis_name)
       6214 keyarr = self.take(indexer)
       6215 if isinstance(key, Index):
       6216     # GH 42790 - Preserve name from an Index


    File ~/qcf_repos/qcfinancial-docs/.venv/lib/python3.12/site-packages/pandas/core/indexes/base.py:6264, in Index._raise_if_missing(self, key, indexer, axis_name)
       6261     raise KeyError(f"None of [{key}] are in the [{axis_name}]")
       6263 not_found = list(ensure_index(key)[missing_mask.nonzero()[0]].unique())
    -> 6264 raise KeyError(f"{not_found} not in index")


    KeyError: "['nominal'] not in index"





    <pandas.io.formats.style.Styler at 0x112f76480>



## Construcción Asistida de un `BulletIborLeg`

En este ejemplo se construye un `Leg` con `IborCashflow` y amortización bullet.
Se requieren los siguientes parámetros:

- `RecPay`: enum que indica si los flujos se reciben o pagan
- `QCDate`: fecha de inicio del primer flujo
- `QCDate`: fecha final del último flujo sin considerar ajustes de días feriados
- `BusyAdRules`: enum que representa el tipo de ajuste en la fecha final para días feriados
- `Tenor`: la periodicidad de pago
- `QCInterestRateLeg::QCStubPeriod`: enum que representa el tipo de período irregular (si aplica)
- `QCBusinessCalendar`: calendario que aplica para las fechas de pago
- `unsigned int`: lag de pago expresado en días
- `Tenor`: periodicidad de fijación
- `QCInterestRateLeg::QCStubPeriod`: enum que representa el tipo de período irregular para el calendario de fijaciones
- `QCBusinessCalendar`: calendario que aplica para las fechas de fijación
- `unsigned int`: lag de fijación expresado en días
- `InterestRateIndex`: índice de tasa de interés utilizado en cada `IborCashflow`
- `float`: nominal
- `bool`: si es `True` significa que la amortización final es un flujo de caja efectivo
- `QCCurrency`: moneda del nominal y de los flujos
- `float`: spread aditivo
- `gearing`: spread multiplicativo (tasa * gearing + spread)
- `SettLagBehaviour`: este parámetro indica cómo se calcula un `settlement_date` cuando un `end_date` cae en un día festivo.

**NOTA:** para construir un `Leg` con `IborCashflow` y amortización customizada, sólo se debe cambiar el parámetro **nominal** por **CustomNotionalAndAmort** e invocar el método `qcf.LegFactory.build_custom_amort_ibor_leg(...)`.

Vamos a un ejemplo. Primero, se da de alta los parámetros requeridos. 


```python
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(15, 2, 2024)
fecha_final = qcf.QCDate(15, 2, 2026) 
bus_adj_rule = qcf.BusyAdjRules.NO
periodicidad_pago = qcf.Tenor('3M')
periodo_irregular_pago = qcf.StubPeriod.NO
calendario = aux.get_business_calendar('US', range(2024, 2035))
lag_pago = 1
periodicidad_fijacion = qcf.Tenor('3M')
periodo_irregular_fijacion = qcf.StubPeriod.NO
sett_lag_behaviour = qcf.SettLagBehaviour.MOVE_TO_WORKING_DAY

# Se utilizará el mismo calendario para pago y fijaciones
lag_de_fijacion = 2

nominal = 1_000_000.0
amort_es_flujo = True 
moneda = usd
spread = .01
gearing = 1.0
```

Se define el índice de tasa de interés.


```python
codigo = 'TERMSOFR3M'
lin_act360 = qcf.QCInterestRate(.0, qcf.QCAct360(), qcf.QCLinearWf())
fixing_lag = qcf.Tenor('2d')
tenor = qcf.Tenor('3m')
fixing_calendar = calendario
settlement_calendar = calendario
usd = qcf.QCUSD()
termsofr_3m = qcf.InterestRateIndex(
    codigo,
    lin_act360,
    fixing_lag,
    tenor,
    calendario,
    calendario,
    usd
)
```

Se da de alta el objeto, pero antes almacenaremos los parámetros en un `dict`. Esto permitirá una sintaxis un poco más liviana.


```python
params = dict(
    rec_pay=rp, 
    start_date=fecha_inicio, 
    end_date=fecha_final, 
    bus_adj_rule=bus_adj_rule, 
    settlement_periodicity=periodicidad_pago,
    settlement_stub_period=periodo_irregular_pago, 
    settlement_calendar=calendario, 
    settlement_lag=lag_pago,
    fixing_periodicity=periodicidad_fijacion, 
    fixing_stub_period=periodo_irregular_fijacion,
    fixing_calendar=calendario, 
    fixing_lag=lag_de_fijacion, 
    interest_rate_index=termsofr_3m,
    initial_notional=nominal, 
    amort_is_cashflow=amort_es_flujo, 
    notional_currency=moneda, 
    spread=spread, 
    gearing=gearing,
    sett_lag_behaviour=sett_lag_behaviour,
)
```


```python
ibor_leg = qcf.LegFactory.build_bullet_ibor_leg(**params)
```

Visualización. Notar que los flujos de intereses corresponden al spread de 1%. No están fijados los valores del índice en cada cupón.


```python
aux.leg_as_dataframe(ibor_leg).style.format(aux.format_dict)
```




<style type="text/css">
</style>
<table id="T_67383">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_67383_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_67383_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_67383_level0_col2" class="col_heading level0 col2" >fecha_fixing</th>
      <th id="T_67383_level0_col3" class="col_heading level0 col3" >fecha_pago</th>
      <th id="T_67383_level0_col4" class="col_heading level0 col4" >nocional</th>
      <th id="T_67383_level0_col5" class="col_heading level0 col5" >amortizacion</th>
      <th id="T_67383_level0_col6" class="col_heading level0 col6" >interes</th>
      <th id="T_67383_level0_col7" class="col_heading level0 col7" >amort_es_flujo</th>
      <th id="T_67383_level0_col8" class="col_heading level0 col8" >flujo</th>
      <th id="T_67383_level0_col9" class="col_heading level0 col9" >moneda_nocional</th>
      <th id="T_67383_level0_col10" class="col_heading level0 col10" >codigo_indice_tasa</th>
      <th id="T_67383_level0_col11" class="col_heading level0 col11" >valor_tasa</th>
      <th id="T_67383_level0_col12" class="col_heading level0 col12" >spread</th>
      <th id="T_67383_level0_col13" class="col_heading level0 col13" >gearing</th>
      <th id="T_67383_level0_col14" class="col_heading level0 col14" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_67383_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_67383_row0_col0" class="data row0 col0" >2024-02-15</td>
      <td id="T_67383_row0_col1" class="data row0 col1" >2024-05-15</td>
      <td id="T_67383_row0_col2" class="data row0 col2" >2024-02-13</td>
      <td id="T_67383_row0_col3" class="data row0 col3" >2024-05-16</td>
      <td id="T_67383_row0_col4" class="data row0 col4" >1,000,000.00</td>
      <td id="T_67383_row0_col5" class="data row0 col5" >0.00</td>
      <td id="T_67383_row0_col6" class="data row0 col6" >2,500.00</td>
      <td id="T_67383_row0_col7" class="data row0 col7" >True</td>
      <td id="T_67383_row0_col8" class="data row0 col8" >2,500.00</td>
      <td id="T_67383_row0_col9" class="data row0 col9" >USD</td>
      <td id="T_67383_row0_col10" class="data row0 col10" >TERMSOFR3M</td>
      <td id="T_67383_row0_col11" class="data row0 col11" >0.0000%</td>
      <td id="T_67383_row0_col12" class="data row0 col12" >1.0000%</td>
      <td id="T_67383_row0_col13" class="data row0 col13" >1.00</td>
      <td id="T_67383_row0_col14" class="data row0 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_67383_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_67383_row1_col0" class="data row1 col0" >2024-05-15</td>
      <td id="T_67383_row1_col1" class="data row1 col1" >2024-08-15</td>
      <td id="T_67383_row1_col2" class="data row1 col2" >2024-05-13</td>
      <td id="T_67383_row1_col3" class="data row1 col3" >2024-08-16</td>
      <td id="T_67383_row1_col4" class="data row1 col4" >1,000,000.00</td>
      <td id="T_67383_row1_col5" class="data row1 col5" >0.00</td>
      <td id="T_67383_row1_col6" class="data row1 col6" >2,555.56</td>
      <td id="T_67383_row1_col7" class="data row1 col7" >True</td>
      <td id="T_67383_row1_col8" class="data row1 col8" >2,555.56</td>
      <td id="T_67383_row1_col9" class="data row1 col9" >USD</td>
      <td id="T_67383_row1_col10" class="data row1 col10" >TERMSOFR3M</td>
      <td id="T_67383_row1_col11" class="data row1 col11" >0.0000%</td>
      <td id="T_67383_row1_col12" class="data row1 col12" >1.0000%</td>
      <td id="T_67383_row1_col13" class="data row1 col13" >1.00</td>
      <td id="T_67383_row1_col14" class="data row1 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_67383_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_67383_row2_col0" class="data row2 col0" >2024-08-15</td>
      <td id="T_67383_row2_col1" class="data row2 col1" >2024-11-15</td>
      <td id="T_67383_row2_col2" class="data row2 col2" >2024-08-13</td>
      <td id="T_67383_row2_col3" class="data row2 col3" >2024-11-18</td>
      <td id="T_67383_row2_col4" class="data row2 col4" >1,000,000.00</td>
      <td id="T_67383_row2_col5" class="data row2 col5" >0.00</td>
      <td id="T_67383_row2_col6" class="data row2 col6" >2,555.56</td>
      <td id="T_67383_row2_col7" class="data row2 col7" >True</td>
      <td id="T_67383_row2_col8" class="data row2 col8" >2,555.56</td>
      <td id="T_67383_row2_col9" class="data row2 col9" >USD</td>
      <td id="T_67383_row2_col10" class="data row2 col10" >TERMSOFR3M</td>
      <td id="T_67383_row2_col11" class="data row2 col11" >0.0000%</td>
      <td id="T_67383_row2_col12" class="data row2 col12" >1.0000%</td>
      <td id="T_67383_row2_col13" class="data row2 col13" >1.00</td>
      <td id="T_67383_row2_col14" class="data row2 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_67383_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_67383_row3_col0" class="data row3 col0" >2024-11-15</td>
      <td id="T_67383_row3_col1" class="data row3 col1" >2025-02-15</td>
      <td id="T_67383_row3_col2" class="data row3 col2" >2024-11-13</td>
      <td id="T_67383_row3_col3" class="data row3 col3" >2025-02-19</td>
      <td id="T_67383_row3_col4" class="data row3 col4" >1,000,000.00</td>
      <td id="T_67383_row3_col5" class="data row3 col5" >0.00</td>
      <td id="T_67383_row3_col6" class="data row3 col6" >2,555.56</td>
      <td id="T_67383_row3_col7" class="data row3 col7" >True</td>
      <td id="T_67383_row3_col8" class="data row3 col8" >2,555.56</td>
      <td id="T_67383_row3_col9" class="data row3 col9" >USD</td>
      <td id="T_67383_row3_col10" class="data row3 col10" >TERMSOFR3M</td>
      <td id="T_67383_row3_col11" class="data row3 col11" >0.0000%</td>
      <td id="T_67383_row3_col12" class="data row3 col12" >1.0000%</td>
      <td id="T_67383_row3_col13" class="data row3 col13" >1.00</td>
      <td id="T_67383_row3_col14" class="data row3 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_67383_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_67383_row4_col0" class="data row4 col0" >2025-02-15</td>
      <td id="T_67383_row4_col1" class="data row4 col1" >2025-05-15</td>
      <td id="T_67383_row4_col2" class="data row4 col2" >2025-02-12</td>
      <td id="T_67383_row4_col3" class="data row4 col3" >2025-05-16</td>
      <td id="T_67383_row4_col4" class="data row4 col4" >1,000,000.00</td>
      <td id="T_67383_row4_col5" class="data row4 col5" >0.00</td>
      <td id="T_67383_row4_col6" class="data row4 col6" >2,472.22</td>
      <td id="T_67383_row4_col7" class="data row4 col7" >True</td>
      <td id="T_67383_row4_col8" class="data row4 col8" >2,472.22</td>
      <td id="T_67383_row4_col9" class="data row4 col9" >USD</td>
      <td id="T_67383_row4_col10" class="data row4 col10" >TERMSOFR3M</td>
      <td id="T_67383_row4_col11" class="data row4 col11" >0.0000%</td>
      <td id="T_67383_row4_col12" class="data row4 col12" >1.0000%</td>
      <td id="T_67383_row4_col13" class="data row4 col13" >1.00</td>
      <td id="T_67383_row4_col14" class="data row4 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_67383_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_67383_row5_col0" class="data row5 col0" >2025-05-15</td>
      <td id="T_67383_row5_col1" class="data row5 col1" >2025-08-15</td>
      <td id="T_67383_row5_col2" class="data row5 col2" >2025-05-13</td>
      <td id="T_67383_row5_col3" class="data row5 col3" >2025-08-18</td>
      <td id="T_67383_row5_col4" class="data row5 col4" >1,000,000.00</td>
      <td id="T_67383_row5_col5" class="data row5 col5" >0.00</td>
      <td id="T_67383_row5_col6" class="data row5 col6" >2,555.56</td>
      <td id="T_67383_row5_col7" class="data row5 col7" >True</td>
      <td id="T_67383_row5_col8" class="data row5 col8" >2,555.56</td>
      <td id="T_67383_row5_col9" class="data row5 col9" >USD</td>
      <td id="T_67383_row5_col10" class="data row5 col10" >TERMSOFR3M</td>
      <td id="T_67383_row5_col11" class="data row5 col11" >0.0000%</td>
      <td id="T_67383_row5_col12" class="data row5 col12" >1.0000%</td>
      <td id="T_67383_row5_col13" class="data row5 col13" >1.00</td>
      <td id="T_67383_row5_col14" class="data row5 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_67383_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_67383_row6_col0" class="data row6 col0" >2025-08-15</td>
      <td id="T_67383_row6_col1" class="data row6 col1" >2025-11-15</td>
      <td id="T_67383_row6_col2" class="data row6 col2" >2025-08-13</td>
      <td id="T_67383_row6_col3" class="data row6 col3" >2025-11-18</td>
      <td id="T_67383_row6_col4" class="data row6 col4" >1,000,000.00</td>
      <td id="T_67383_row6_col5" class="data row6 col5" >0.00</td>
      <td id="T_67383_row6_col6" class="data row6 col6" >2,555.56</td>
      <td id="T_67383_row6_col7" class="data row6 col7" >True</td>
      <td id="T_67383_row6_col8" class="data row6 col8" >2,555.56</td>
      <td id="T_67383_row6_col9" class="data row6 col9" >USD</td>
      <td id="T_67383_row6_col10" class="data row6 col10" >TERMSOFR3M</td>
      <td id="T_67383_row6_col11" class="data row6 col11" >0.0000%</td>
      <td id="T_67383_row6_col12" class="data row6 col12" >1.0000%</td>
      <td id="T_67383_row6_col13" class="data row6 col13" >1.00</td>
      <td id="T_67383_row6_col14" class="data row6 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_67383_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_67383_row7_col0" class="data row7 col0" >2025-11-15</td>
      <td id="T_67383_row7_col1" class="data row7 col1" >2026-02-15</td>
      <td id="T_67383_row7_col2" class="data row7 col2" >2025-11-12</td>
      <td id="T_67383_row7_col3" class="data row7 col3" >2026-02-18</td>
      <td id="T_67383_row7_col4" class="data row7 col4" >1,000,000.00</td>
      <td id="T_67383_row7_col5" class="data row7 col5" >1,000,000.00</td>
      <td id="T_67383_row7_col6" class="data row7 col6" >2,555.56</td>
      <td id="T_67383_row7_col7" class="data row7 col7" >True</td>
      <td id="T_67383_row7_col8" class="data row7 col8" >1,002,555.56</td>
      <td id="T_67383_row7_col9" class="data row7 col9" >USD</td>
      <td id="T_67383_row7_col10" class="data row7 col10" >TERMSOFR3M</td>
      <td id="T_67383_row7_col11" class="data row7 col11" >0.0000%</td>
      <td id="T_67383_row7_col12" class="data row7 col12" >1.0000%</td>
      <td id="T_67383_row7_col13" class="data row7 col13" >1.00</td>
      <td id="T_67383_row7_col14" class="data row7 col14" >LinAct360</td>
    </tr>
  </tbody>
</table>




### Otras Combinaciones de Períodos Irregulares

Las distintas combinaciones de períodos irregulares (de pago y fijación) permiten obtener tablas de desarrollo con muchas características.

#### `SHORTFRONT` con `SHORTFRONT`


```python
params["start_date"] = qcf.QCDate(15, 3, 2024)
params["settlement_stub_period"] = qcf.StubPeriod.SHORTFRONT
params["fixing_stub_period"] = qcf.StubPeriod.SHORTFRONT
```


```python
ibor_leg = qcf.LegFactory.build_bullet_ibor_leg(**params)
```

En este caso, las fechas de fijación se sincronizan con las fechas de inicio de los cupones. Notar además que el primer cupón es de dos meses mientras que el índice es de 3M.


```python
aux.leg_as_dataframe(ibor_leg).style.format(aux.format_dict)
```




<style type="text/css">
</style>
<table id="T_a6299">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_a6299_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_a6299_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_a6299_level0_col2" class="col_heading level0 col2" >fecha_fixing</th>
      <th id="T_a6299_level0_col3" class="col_heading level0 col3" >fecha_pago</th>
      <th id="T_a6299_level0_col4" class="col_heading level0 col4" >nocional</th>
      <th id="T_a6299_level0_col5" class="col_heading level0 col5" >amortizacion</th>
      <th id="T_a6299_level0_col6" class="col_heading level0 col6" >interes</th>
      <th id="T_a6299_level0_col7" class="col_heading level0 col7" >amort_es_flujo</th>
      <th id="T_a6299_level0_col8" class="col_heading level0 col8" >flujo</th>
      <th id="T_a6299_level0_col9" class="col_heading level0 col9" >moneda_nocional</th>
      <th id="T_a6299_level0_col10" class="col_heading level0 col10" >codigo_indice_tasa</th>
      <th id="T_a6299_level0_col11" class="col_heading level0 col11" >valor_tasa</th>
      <th id="T_a6299_level0_col12" class="col_heading level0 col12" >spread</th>
      <th id="T_a6299_level0_col13" class="col_heading level0 col13" >gearing</th>
      <th id="T_a6299_level0_col14" class="col_heading level0 col14" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_a6299_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_a6299_row0_col0" class="data row0 col0" >2024-03-15</td>
      <td id="T_a6299_row0_col1" class="data row0 col1" >2024-05-15</td>
      <td id="T_a6299_row0_col2" class="data row0 col2" >2024-03-13</td>
      <td id="T_a6299_row0_col3" class="data row0 col3" >2024-05-16</td>
      <td id="T_a6299_row0_col4" class="data row0 col4" >1,000,000.00</td>
      <td id="T_a6299_row0_col5" class="data row0 col5" >0.00</td>
      <td id="T_a6299_row0_col6" class="data row0 col6" >1,694.44</td>
      <td id="T_a6299_row0_col7" class="data row0 col7" >True</td>
      <td id="T_a6299_row0_col8" class="data row0 col8" >1,694.44</td>
      <td id="T_a6299_row0_col9" class="data row0 col9" >USD</td>
      <td id="T_a6299_row0_col10" class="data row0 col10" >TERMSOFR3M</td>
      <td id="T_a6299_row0_col11" class="data row0 col11" >0.0000%</td>
      <td id="T_a6299_row0_col12" class="data row0 col12" >1.0000%</td>
      <td id="T_a6299_row0_col13" class="data row0 col13" >1.00</td>
      <td id="T_a6299_row0_col14" class="data row0 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a6299_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_a6299_row1_col0" class="data row1 col0" >2024-05-15</td>
      <td id="T_a6299_row1_col1" class="data row1 col1" >2024-08-15</td>
      <td id="T_a6299_row1_col2" class="data row1 col2" >2024-05-13</td>
      <td id="T_a6299_row1_col3" class="data row1 col3" >2024-08-16</td>
      <td id="T_a6299_row1_col4" class="data row1 col4" >1,000,000.00</td>
      <td id="T_a6299_row1_col5" class="data row1 col5" >0.00</td>
      <td id="T_a6299_row1_col6" class="data row1 col6" >2,555.56</td>
      <td id="T_a6299_row1_col7" class="data row1 col7" >True</td>
      <td id="T_a6299_row1_col8" class="data row1 col8" >2,555.56</td>
      <td id="T_a6299_row1_col9" class="data row1 col9" >USD</td>
      <td id="T_a6299_row1_col10" class="data row1 col10" >TERMSOFR3M</td>
      <td id="T_a6299_row1_col11" class="data row1 col11" >0.0000%</td>
      <td id="T_a6299_row1_col12" class="data row1 col12" >1.0000%</td>
      <td id="T_a6299_row1_col13" class="data row1 col13" >1.00</td>
      <td id="T_a6299_row1_col14" class="data row1 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a6299_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_a6299_row2_col0" class="data row2 col0" >2024-08-15</td>
      <td id="T_a6299_row2_col1" class="data row2 col1" >2024-11-15</td>
      <td id="T_a6299_row2_col2" class="data row2 col2" >2024-08-13</td>
      <td id="T_a6299_row2_col3" class="data row2 col3" >2024-11-18</td>
      <td id="T_a6299_row2_col4" class="data row2 col4" >1,000,000.00</td>
      <td id="T_a6299_row2_col5" class="data row2 col5" >0.00</td>
      <td id="T_a6299_row2_col6" class="data row2 col6" >2,555.56</td>
      <td id="T_a6299_row2_col7" class="data row2 col7" >True</td>
      <td id="T_a6299_row2_col8" class="data row2 col8" >2,555.56</td>
      <td id="T_a6299_row2_col9" class="data row2 col9" >USD</td>
      <td id="T_a6299_row2_col10" class="data row2 col10" >TERMSOFR3M</td>
      <td id="T_a6299_row2_col11" class="data row2 col11" >0.0000%</td>
      <td id="T_a6299_row2_col12" class="data row2 col12" >1.0000%</td>
      <td id="T_a6299_row2_col13" class="data row2 col13" >1.00</td>
      <td id="T_a6299_row2_col14" class="data row2 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a6299_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_a6299_row3_col0" class="data row3 col0" >2024-11-15</td>
      <td id="T_a6299_row3_col1" class="data row3 col1" >2025-02-15</td>
      <td id="T_a6299_row3_col2" class="data row3 col2" >2024-11-13</td>
      <td id="T_a6299_row3_col3" class="data row3 col3" >2025-02-19</td>
      <td id="T_a6299_row3_col4" class="data row3 col4" >1,000,000.00</td>
      <td id="T_a6299_row3_col5" class="data row3 col5" >0.00</td>
      <td id="T_a6299_row3_col6" class="data row3 col6" >2,555.56</td>
      <td id="T_a6299_row3_col7" class="data row3 col7" >True</td>
      <td id="T_a6299_row3_col8" class="data row3 col8" >2,555.56</td>
      <td id="T_a6299_row3_col9" class="data row3 col9" >USD</td>
      <td id="T_a6299_row3_col10" class="data row3 col10" >TERMSOFR3M</td>
      <td id="T_a6299_row3_col11" class="data row3 col11" >0.0000%</td>
      <td id="T_a6299_row3_col12" class="data row3 col12" >1.0000%</td>
      <td id="T_a6299_row3_col13" class="data row3 col13" >1.00</td>
      <td id="T_a6299_row3_col14" class="data row3 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a6299_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_a6299_row4_col0" class="data row4 col0" >2025-02-15</td>
      <td id="T_a6299_row4_col1" class="data row4 col1" >2025-05-15</td>
      <td id="T_a6299_row4_col2" class="data row4 col2" >2025-02-12</td>
      <td id="T_a6299_row4_col3" class="data row4 col3" >2025-05-16</td>
      <td id="T_a6299_row4_col4" class="data row4 col4" >1,000,000.00</td>
      <td id="T_a6299_row4_col5" class="data row4 col5" >0.00</td>
      <td id="T_a6299_row4_col6" class="data row4 col6" >2,472.22</td>
      <td id="T_a6299_row4_col7" class="data row4 col7" >True</td>
      <td id="T_a6299_row4_col8" class="data row4 col8" >2,472.22</td>
      <td id="T_a6299_row4_col9" class="data row4 col9" >USD</td>
      <td id="T_a6299_row4_col10" class="data row4 col10" >TERMSOFR3M</td>
      <td id="T_a6299_row4_col11" class="data row4 col11" >0.0000%</td>
      <td id="T_a6299_row4_col12" class="data row4 col12" >1.0000%</td>
      <td id="T_a6299_row4_col13" class="data row4 col13" >1.00</td>
      <td id="T_a6299_row4_col14" class="data row4 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a6299_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_a6299_row5_col0" class="data row5 col0" >2025-05-15</td>
      <td id="T_a6299_row5_col1" class="data row5 col1" >2025-08-15</td>
      <td id="T_a6299_row5_col2" class="data row5 col2" >2025-05-13</td>
      <td id="T_a6299_row5_col3" class="data row5 col3" >2025-08-18</td>
      <td id="T_a6299_row5_col4" class="data row5 col4" >1,000,000.00</td>
      <td id="T_a6299_row5_col5" class="data row5 col5" >0.00</td>
      <td id="T_a6299_row5_col6" class="data row5 col6" >2,555.56</td>
      <td id="T_a6299_row5_col7" class="data row5 col7" >True</td>
      <td id="T_a6299_row5_col8" class="data row5 col8" >2,555.56</td>
      <td id="T_a6299_row5_col9" class="data row5 col9" >USD</td>
      <td id="T_a6299_row5_col10" class="data row5 col10" >TERMSOFR3M</td>
      <td id="T_a6299_row5_col11" class="data row5 col11" >0.0000%</td>
      <td id="T_a6299_row5_col12" class="data row5 col12" >1.0000%</td>
      <td id="T_a6299_row5_col13" class="data row5 col13" >1.00</td>
      <td id="T_a6299_row5_col14" class="data row5 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a6299_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_a6299_row6_col0" class="data row6 col0" >2025-08-15</td>
      <td id="T_a6299_row6_col1" class="data row6 col1" >2025-11-15</td>
      <td id="T_a6299_row6_col2" class="data row6 col2" >2025-08-13</td>
      <td id="T_a6299_row6_col3" class="data row6 col3" >2025-11-18</td>
      <td id="T_a6299_row6_col4" class="data row6 col4" >1,000,000.00</td>
      <td id="T_a6299_row6_col5" class="data row6 col5" >0.00</td>
      <td id="T_a6299_row6_col6" class="data row6 col6" >2,555.56</td>
      <td id="T_a6299_row6_col7" class="data row6 col7" >True</td>
      <td id="T_a6299_row6_col8" class="data row6 col8" >2,555.56</td>
      <td id="T_a6299_row6_col9" class="data row6 col9" >USD</td>
      <td id="T_a6299_row6_col10" class="data row6 col10" >TERMSOFR3M</td>
      <td id="T_a6299_row6_col11" class="data row6 col11" >0.0000%</td>
      <td id="T_a6299_row6_col12" class="data row6 col12" >1.0000%</td>
      <td id="T_a6299_row6_col13" class="data row6 col13" >1.00</td>
      <td id="T_a6299_row6_col14" class="data row6 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a6299_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_a6299_row7_col0" class="data row7 col0" >2025-11-15</td>
      <td id="T_a6299_row7_col1" class="data row7 col1" >2026-02-15</td>
      <td id="T_a6299_row7_col2" class="data row7 col2" >2025-11-12</td>
      <td id="T_a6299_row7_col3" class="data row7 col3" >2026-02-18</td>
      <td id="T_a6299_row7_col4" class="data row7 col4" >1,000,000.00</td>
      <td id="T_a6299_row7_col5" class="data row7 col5" >1,000,000.00</td>
      <td id="T_a6299_row7_col6" class="data row7 col6" >2,555.56</td>
      <td id="T_a6299_row7_col7" class="data row7 col7" >True</td>
      <td id="T_a6299_row7_col8" class="data row7 col8" >1,002,555.56</td>
      <td id="T_a6299_row7_col9" class="data row7 col9" >USD</td>
      <td id="T_a6299_row7_col10" class="data row7 col10" >TERMSOFR3M</td>
      <td id="T_a6299_row7_col11" class="data row7 col11" >0.0000%</td>
      <td id="T_a6299_row7_col12" class="data row7 col12" >1.0000%</td>
      <td id="T_a6299_row7_col13" class="data row7 col13" >1.00</td>
      <td id="T_a6299_row7_col14" class="data row7 col14" >LinAct360</td>
    </tr>
  </tbody>
</table>




#### `SHORTFRONT` con `LONGBACK`


```python
params["start_date"] = qcf.QCDate(31, 1, 2024)
params["end_date"] = qcf.QCDate(31, 3, 2026) 
params["settlement_stub_period"] = qcf.StubPeriod.SHORTFRONT
params["fixing_stub_period"] = qcf.StubPeriod.LONGBACK

ibor_leg = qcf.LegFactory.build_bullet_ibor_leg(**params)
```

En este caso, las fechas de fijación también se desfasan respecto a las fechas de inicio de los cupones. Ahora las fechas de fijación de los **primeros dos cupones** coinciden.


```python
aux.leg_as_dataframe(ibor_leg).style.format(aux.format_dict)
```




<style type="text/css">
</style>
<table id="T_cbbff">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_cbbff_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_cbbff_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_cbbff_level0_col2" class="col_heading level0 col2" >fecha_fixing</th>
      <th id="T_cbbff_level0_col3" class="col_heading level0 col3" >fecha_pago</th>
      <th id="T_cbbff_level0_col4" class="col_heading level0 col4" >nocional</th>
      <th id="T_cbbff_level0_col5" class="col_heading level0 col5" >amortizacion</th>
      <th id="T_cbbff_level0_col6" class="col_heading level0 col6" >interes</th>
      <th id="T_cbbff_level0_col7" class="col_heading level0 col7" >amort_es_flujo</th>
      <th id="T_cbbff_level0_col8" class="col_heading level0 col8" >flujo</th>
      <th id="T_cbbff_level0_col9" class="col_heading level0 col9" >moneda_nocional</th>
      <th id="T_cbbff_level0_col10" class="col_heading level0 col10" >codigo_indice_tasa</th>
      <th id="T_cbbff_level0_col11" class="col_heading level0 col11" >valor_tasa</th>
      <th id="T_cbbff_level0_col12" class="col_heading level0 col12" >spread</th>
      <th id="T_cbbff_level0_col13" class="col_heading level0 col13" >gearing</th>
      <th id="T_cbbff_level0_col14" class="col_heading level0 col14" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_cbbff_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_cbbff_row0_col0" class="data row0 col0" >2024-01-31</td>
      <td id="T_cbbff_row0_col1" class="data row0 col1" >2024-03-31</td>
      <td id="T_cbbff_row0_col2" class="data row0 col2" >2024-01-29</td>
      <td id="T_cbbff_row0_col3" class="data row0 col3" >2024-04-02</td>
      <td id="T_cbbff_row0_col4" class="data row0 col4" >1,000,000.00</td>
      <td id="T_cbbff_row0_col5" class="data row0 col5" >0.00</td>
      <td id="T_cbbff_row0_col6" class="data row0 col6" >1,666.67</td>
      <td id="T_cbbff_row0_col7" class="data row0 col7" >True</td>
      <td id="T_cbbff_row0_col8" class="data row0 col8" >1,666.67</td>
      <td id="T_cbbff_row0_col9" class="data row0 col9" >USD</td>
      <td id="T_cbbff_row0_col10" class="data row0 col10" >TERMSOFR3M</td>
      <td id="T_cbbff_row0_col11" class="data row0 col11" >0.0000%</td>
      <td id="T_cbbff_row0_col12" class="data row0 col12" >1.0000%</td>
      <td id="T_cbbff_row0_col13" class="data row0 col13" >1.00</td>
      <td id="T_cbbff_row0_col14" class="data row0 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cbbff_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_cbbff_row1_col0" class="data row1 col0" >2024-03-31</td>
      <td id="T_cbbff_row1_col1" class="data row1 col1" >2024-06-30</td>
      <td id="T_cbbff_row1_col2" class="data row1 col2" >2024-01-29</td>
      <td id="T_cbbff_row1_col3" class="data row1 col3" >2024-07-02</td>
      <td id="T_cbbff_row1_col4" class="data row1 col4" >1,000,000.00</td>
      <td id="T_cbbff_row1_col5" class="data row1 col5" >0.00</td>
      <td id="T_cbbff_row1_col6" class="data row1 col6" >2,527.78</td>
      <td id="T_cbbff_row1_col7" class="data row1 col7" >True</td>
      <td id="T_cbbff_row1_col8" class="data row1 col8" >2,527.78</td>
      <td id="T_cbbff_row1_col9" class="data row1 col9" >USD</td>
      <td id="T_cbbff_row1_col10" class="data row1 col10" >TERMSOFR3M</td>
      <td id="T_cbbff_row1_col11" class="data row1 col11" >0.0000%</td>
      <td id="T_cbbff_row1_col12" class="data row1 col12" >1.0000%</td>
      <td id="T_cbbff_row1_col13" class="data row1 col13" >1.00</td>
      <td id="T_cbbff_row1_col14" class="data row1 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cbbff_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_cbbff_row2_col0" class="data row2 col0" >2024-06-30</td>
      <td id="T_cbbff_row2_col1" class="data row2 col1" >2024-09-30</td>
      <td id="T_cbbff_row2_col2" class="data row2 col2" >2024-04-26</td>
      <td id="T_cbbff_row2_col3" class="data row2 col3" >2024-10-01</td>
      <td id="T_cbbff_row2_col4" class="data row2 col4" >1,000,000.00</td>
      <td id="T_cbbff_row2_col5" class="data row2 col5" >0.00</td>
      <td id="T_cbbff_row2_col6" class="data row2 col6" >2,555.56</td>
      <td id="T_cbbff_row2_col7" class="data row2 col7" >True</td>
      <td id="T_cbbff_row2_col8" class="data row2 col8" >2,555.56</td>
      <td id="T_cbbff_row2_col9" class="data row2 col9" >USD</td>
      <td id="T_cbbff_row2_col10" class="data row2 col10" >TERMSOFR3M</td>
      <td id="T_cbbff_row2_col11" class="data row2 col11" >0.0000%</td>
      <td id="T_cbbff_row2_col12" class="data row2 col12" >1.0000%</td>
      <td id="T_cbbff_row2_col13" class="data row2 col13" >1.00</td>
      <td id="T_cbbff_row2_col14" class="data row2 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cbbff_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_cbbff_row3_col0" class="data row3 col0" >2024-09-30</td>
      <td id="T_cbbff_row3_col1" class="data row3 col1" >2024-12-31</td>
      <td id="T_cbbff_row3_col2" class="data row3 col2" >2024-07-29</td>
      <td id="T_cbbff_row3_col3" class="data row3 col3" >2025-01-02</td>
      <td id="T_cbbff_row3_col4" class="data row3 col4" >1,000,000.00</td>
      <td id="T_cbbff_row3_col5" class="data row3 col5" >0.00</td>
      <td id="T_cbbff_row3_col6" class="data row3 col6" >2,555.56</td>
      <td id="T_cbbff_row3_col7" class="data row3 col7" >True</td>
      <td id="T_cbbff_row3_col8" class="data row3 col8" >2,555.56</td>
      <td id="T_cbbff_row3_col9" class="data row3 col9" >USD</td>
      <td id="T_cbbff_row3_col10" class="data row3 col10" >TERMSOFR3M</td>
      <td id="T_cbbff_row3_col11" class="data row3 col11" >0.0000%</td>
      <td id="T_cbbff_row3_col12" class="data row3 col12" >1.0000%</td>
      <td id="T_cbbff_row3_col13" class="data row3 col13" >1.00</td>
      <td id="T_cbbff_row3_col14" class="data row3 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cbbff_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_cbbff_row4_col0" class="data row4 col0" >2024-12-31</td>
      <td id="T_cbbff_row4_col1" class="data row4 col1" >2025-03-31</td>
      <td id="T_cbbff_row4_col2" class="data row4 col2" >2024-10-29</td>
      <td id="T_cbbff_row4_col3" class="data row4 col3" >2025-04-01</td>
      <td id="T_cbbff_row4_col4" class="data row4 col4" >1,000,000.00</td>
      <td id="T_cbbff_row4_col5" class="data row4 col5" >0.00</td>
      <td id="T_cbbff_row4_col6" class="data row4 col6" >2,500.00</td>
      <td id="T_cbbff_row4_col7" class="data row4 col7" >True</td>
      <td id="T_cbbff_row4_col8" class="data row4 col8" >2,500.00</td>
      <td id="T_cbbff_row4_col9" class="data row4 col9" >USD</td>
      <td id="T_cbbff_row4_col10" class="data row4 col10" >TERMSOFR3M</td>
      <td id="T_cbbff_row4_col11" class="data row4 col11" >0.0000%</td>
      <td id="T_cbbff_row4_col12" class="data row4 col12" >1.0000%</td>
      <td id="T_cbbff_row4_col13" class="data row4 col13" >1.00</td>
      <td id="T_cbbff_row4_col14" class="data row4 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cbbff_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_cbbff_row5_col0" class="data row5 col0" >2025-03-31</td>
      <td id="T_cbbff_row5_col1" class="data row5 col1" >2025-06-30</td>
      <td id="T_cbbff_row5_col2" class="data row5 col2" >2025-01-29</td>
      <td id="T_cbbff_row5_col3" class="data row5 col3" >2025-07-01</td>
      <td id="T_cbbff_row5_col4" class="data row5 col4" >1,000,000.00</td>
      <td id="T_cbbff_row5_col5" class="data row5 col5" >0.00</td>
      <td id="T_cbbff_row5_col6" class="data row5 col6" >2,527.78</td>
      <td id="T_cbbff_row5_col7" class="data row5 col7" >True</td>
      <td id="T_cbbff_row5_col8" class="data row5 col8" >2,527.78</td>
      <td id="T_cbbff_row5_col9" class="data row5 col9" >USD</td>
      <td id="T_cbbff_row5_col10" class="data row5 col10" >TERMSOFR3M</td>
      <td id="T_cbbff_row5_col11" class="data row5 col11" >0.0000%</td>
      <td id="T_cbbff_row5_col12" class="data row5 col12" >1.0000%</td>
      <td id="T_cbbff_row5_col13" class="data row5 col13" >1.00</td>
      <td id="T_cbbff_row5_col14" class="data row5 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cbbff_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_cbbff_row6_col0" class="data row6 col0" >2025-06-30</td>
      <td id="T_cbbff_row6_col1" class="data row6 col1" >2025-09-30</td>
      <td id="T_cbbff_row6_col2" class="data row6 col2" >2025-04-28</td>
      <td id="T_cbbff_row6_col3" class="data row6 col3" >2025-10-01</td>
      <td id="T_cbbff_row6_col4" class="data row6 col4" >1,000,000.00</td>
      <td id="T_cbbff_row6_col5" class="data row6 col5" >0.00</td>
      <td id="T_cbbff_row6_col6" class="data row6 col6" >2,555.56</td>
      <td id="T_cbbff_row6_col7" class="data row6 col7" >True</td>
      <td id="T_cbbff_row6_col8" class="data row6 col8" >2,555.56</td>
      <td id="T_cbbff_row6_col9" class="data row6 col9" >USD</td>
      <td id="T_cbbff_row6_col10" class="data row6 col10" >TERMSOFR3M</td>
      <td id="T_cbbff_row6_col11" class="data row6 col11" >0.0000%</td>
      <td id="T_cbbff_row6_col12" class="data row6 col12" >1.0000%</td>
      <td id="T_cbbff_row6_col13" class="data row6 col13" >1.00</td>
      <td id="T_cbbff_row6_col14" class="data row6 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cbbff_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_cbbff_row7_col0" class="data row7 col0" >2025-09-30</td>
      <td id="T_cbbff_row7_col1" class="data row7 col1" >2025-12-31</td>
      <td id="T_cbbff_row7_col2" class="data row7 col2" >2025-07-29</td>
      <td id="T_cbbff_row7_col3" class="data row7 col3" >2026-01-02</td>
      <td id="T_cbbff_row7_col4" class="data row7 col4" >1,000,000.00</td>
      <td id="T_cbbff_row7_col5" class="data row7 col5" >0.00</td>
      <td id="T_cbbff_row7_col6" class="data row7 col6" >2,555.56</td>
      <td id="T_cbbff_row7_col7" class="data row7 col7" >True</td>
      <td id="T_cbbff_row7_col8" class="data row7 col8" >2,555.56</td>
      <td id="T_cbbff_row7_col9" class="data row7 col9" >USD</td>
      <td id="T_cbbff_row7_col10" class="data row7 col10" >TERMSOFR3M</td>
      <td id="T_cbbff_row7_col11" class="data row7 col11" >0.0000%</td>
      <td id="T_cbbff_row7_col12" class="data row7 col12" >1.0000%</td>
      <td id="T_cbbff_row7_col13" class="data row7 col13" >1.00</td>
      <td id="T_cbbff_row7_col14" class="data row7 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cbbff_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_cbbff_row8_col0" class="data row8 col0" >2025-12-31</td>
      <td id="T_cbbff_row8_col1" class="data row8 col1" >2026-03-31</td>
      <td id="T_cbbff_row8_col2" class="data row8 col2" >2025-10-29</td>
      <td id="T_cbbff_row8_col3" class="data row8 col3" >2026-04-01</td>
      <td id="T_cbbff_row8_col4" class="data row8 col4" >1,000,000.00</td>
      <td id="T_cbbff_row8_col5" class="data row8 col5" >1,000,000.00</td>
      <td id="T_cbbff_row8_col6" class="data row8 col6" >2,500.00</td>
      <td id="T_cbbff_row8_col7" class="data row8 col7" >True</td>
      <td id="T_cbbff_row8_col8" class="data row8 col8" >1,002,500.00</td>
      <td id="T_cbbff_row8_col9" class="data row8 col9" >USD</td>
      <td id="T_cbbff_row8_col10" class="data row8 col10" >TERMSOFR3M</td>
      <td id="T_cbbff_row8_col11" class="data row8 col11" >0.0000%</td>
      <td id="T_cbbff_row8_col12" class="data row8 col12" >1.0000%</td>
      <td id="T_cbbff_row8_col13" class="data row8 col13" >1.00</td>
      <td id="T_cbbff_row8_col14" class="data row8 col14" >LinAct360</td>
    </tr>
  </tbody>
</table>




## Construcción Asistida de un `BulletIborMultiCurrencyLeg`

Se construye un `Leg` con `IborMultiCurrencyCashflow` y amortización bullet.
Se requieren los siguientes parámetros:

- `RecPay`: enum que indica si los flujos se reciben o pagan
- `QCDate`: fecha de inicio del primer flujo
- `QCDate`: fecha final del último flujo sin considerar ajustes de días feriados
- `BusyAdRules`: enum que representa el tipo de ajuste en la fecha final para días feriados
- `Tenor`: la periodicidad de pago
- `QCInterestRateLeg::QCStubPeriod`: enum que representa el tipo de período irregular (si aplica)
- `QCBusinessCalendar`: calendario que aplica para las fechas de pago
- `unsigned int`: lag de pago expresado en días
- `Tenor`: periodicidad de fijación
- `QCInterestRateLeg::QCStubPeriod`: enum que representa el tipo de período irregular para el calendario de fijaciones
- `QCBusinessCalendar`: calendario que aplica para las fechas de fijación
- `unsigned int`: lag de fijación expresado en días
- `InterestRateIndex`: índice de tasa de interés utilizado en cada `IborCashflow`
- `float`: nominal
- `bool`: si es `True` significa que la amortización final es un flujo de caja efectivo
- `QCCurrency`: moneda del nominal y de los flujos
- `float`: spread aditivo
- `gearing`: spread multiplicativo (tasa * gearing + spread)
- `SettLagBehaviour`: este parámetro indica cómo se calcula un `settlement_date` cuando un `end_date` cae en un día festivo.
---
**MultiCurrency**
- `QCCurrency`: moneda de pago los flujos
- `FXRateIndex`: índice con el cual se transforma cada flujo a la moneda de pago
- `int`: lag de fijación del `FXRateIndex`.
- `FxFixingLagPivot`: este parámetro indica si el lag de fijación del índice FX se aplica sobre `end_date` o sobre `settlement_date`.
- `FxFixingLagAppliesTo`: indica si el lag se refiere a `FIXING_DATE` o `PUBISHING_DATE` del índice.

Vamos a un ejemplo.


```python
ibor_mccy_leg = qcf.LegFactory.build_bullet_ibor_mccy_leg(
    rec_pay=rp, 
    start_date=fecha_inicio, 
    end_date=fecha_final, 
    bus_adj_rule=bus_adj_rule, 
    settlement_periodicity=periodicidad_pago,
    settlement_stub_period=periodo_irregular_pago, 
    settlement_calendar=calendario, 
    settlement_lag=lag_pago,
    fixing_periodicity=periodicidad_fijacion, 
    fixing_stub_period=periodo_irregular_fijacion,
    fixing_calendar=calendario, 
    fixing_lag=lag_de_fijacion, 
    interest_rate_index=termsofr_3m,
    initial_notional=nominal, 
    amort_is_cashflow=amort_es_flujo, 
    notional_currency=clp, 
    spread=spread, 
    gearing=gearing,
    sett_lag_behaviour=sett_lag_behaviour,
    # Parámetros MultiCurrency
    settlement_currency=usd, 
    fx_rate_index=usdclp_obs, 
    fx_rate_index_fixing_lag=fx_rate_index_fixing_lag,
    fx_fixing_lag_pivot=fx_fixing_lag_pivot,
    fx_fixing_lag_applies_to=qcf.FxFixingLagAppliesTo.PUBLISHING_DATE,
)
```


```python
aux.leg_as_dataframe(ibor_mccy_leg).style.format(aux.format_dict)
```




<style type="text/css">
</style>
<table id="T_84c2f">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_84c2f_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_84c2f_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_84c2f_level0_col2" class="col_heading level0 col2" >fecha_fixing</th>
      <th id="T_84c2f_level0_col3" class="col_heading level0 col3" >fecha_pago</th>
      <th id="T_84c2f_level0_col4" class="col_heading level0 col4" >nocional</th>
      <th id="T_84c2f_level0_col5" class="col_heading level0 col5" >amortizacion</th>
      <th id="T_84c2f_level0_col6" class="col_heading level0 col6" >interes</th>
      <th id="T_84c2f_level0_col7" class="col_heading level0 col7" >amort_es_flujo</th>
      <th id="T_84c2f_level0_col8" class="col_heading level0 col8" >flujo</th>
      <th id="T_84c2f_level0_col9" class="col_heading level0 col9" >moneda_nocional</th>
      <th id="T_84c2f_level0_col10" class="col_heading level0 col10" >codigo_indice_tasa</th>
      <th id="T_84c2f_level0_col11" class="col_heading level0 col11" >spread</th>
      <th id="T_84c2f_level0_col12" class="col_heading level0 col12" >gearing</th>
      <th id="T_84c2f_level0_col13" class="col_heading level0 col13" >valor_tasa</th>
      <th id="T_84c2f_level0_col14" class="col_heading level0 col14" >tipo_tasa</th>
      <th id="T_84c2f_level0_col15" class="col_heading level0 col15" >fecha_fixing_fx</th>
      <th id="T_84c2f_level0_col16" class="col_heading level0 col16" >moneda_pago</th>
      <th id="T_84c2f_level0_col17" class="col_heading level0 col17" >codigo_indice_fx</th>
      <th id="T_84c2f_level0_col18" class="col_heading level0 col18" >valor_indice_fx</th>
      <th id="T_84c2f_level0_col19" class="col_heading level0 col19" >amortizacion_moneda_pago</th>
      <th id="T_84c2f_level0_col20" class="col_heading level0 col20" >interes_moneda_pago</th>
      <th id="T_84c2f_level0_col21" class="col_heading level0 col21" >flujo_moneda_pago</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_84c2f_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_84c2f_row0_col0" class="data row0 col0" >2024-02-15</td>
      <td id="T_84c2f_row0_col1" class="data row0 col1" >2024-05-15</td>
      <td id="T_84c2f_row0_col2" class="data row0 col2" >2024-02-13</td>
      <td id="T_84c2f_row0_col3" class="data row0 col3" >2024-05-16</td>
      <td id="T_84c2f_row0_col4" class="data row0 col4" >1,000,000.00</td>
      <td id="T_84c2f_row0_col5" class="data row0 col5" >0.00</td>
      <td id="T_84c2f_row0_col6" class="data row0 col6" >2,500.00</td>
      <td id="T_84c2f_row0_col7" class="data row0 col7" >True</td>
      <td id="T_84c2f_row0_col8" class="data row0 col8" >2,500.00</td>
      <td id="T_84c2f_row0_col9" class="data row0 col9" >CLP</td>
      <td id="T_84c2f_row0_col10" class="data row0 col10" >TERMSOFR3M</td>
      <td id="T_84c2f_row0_col11" class="data row0 col11" >1.0000%</td>
      <td id="T_84c2f_row0_col12" class="data row0 col12" >1.00</td>
      <td id="T_84c2f_row0_col13" class="data row0 col13" >0.0000%</td>
      <td id="T_84c2f_row0_col14" class="data row0 col14" >LinAct360</td>
      <td id="T_84c2f_row0_col15" class="data row0 col15" >2024-05-15</td>
      <td id="T_84c2f_row0_col16" class="data row0 col16" >USD</td>
      <td id="T_84c2f_row0_col17" class="data row0 col17" >USDOBS</td>
      <td id="T_84c2f_row0_col18" class="data row0 col18" >1.00</td>
      <td id="T_84c2f_row0_col19" class="data row0 col19" >0.00</td>
      <td id="T_84c2f_row0_col20" class="data row0 col20" >2,500.00</td>
      <td id="T_84c2f_row0_col21" class="data row0 col21" >2,500.00</td>
    </tr>
    <tr>
      <th id="T_84c2f_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_84c2f_row1_col0" class="data row1 col0" >2024-05-15</td>
      <td id="T_84c2f_row1_col1" class="data row1 col1" >2024-08-15</td>
      <td id="T_84c2f_row1_col2" class="data row1 col2" >2024-05-13</td>
      <td id="T_84c2f_row1_col3" class="data row1 col3" >2024-08-16</td>
      <td id="T_84c2f_row1_col4" class="data row1 col4" >1,000,000.00</td>
      <td id="T_84c2f_row1_col5" class="data row1 col5" >0.00</td>
      <td id="T_84c2f_row1_col6" class="data row1 col6" >2,555.56</td>
      <td id="T_84c2f_row1_col7" class="data row1 col7" >True</td>
      <td id="T_84c2f_row1_col8" class="data row1 col8" >2,555.56</td>
      <td id="T_84c2f_row1_col9" class="data row1 col9" >CLP</td>
      <td id="T_84c2f_row1_col10" class="data row1 col10" >TERMSOFR3M</td>
      <td id="T_84c2f_row1_col11" class="data row1 col11" >1.0000%</td>
      <td id="T_84c2f_row1_col12" class="data row1 col12" >1.00</td>
      <td id="T_84c2f_row1_col13" class="data row1 col13" >0.0000%</td>
      <td id="T_84c2f_row1_col14" class="data row1 col14" >LinAct360</td>
      <td id="T_84c2f_row1_col15" class="data row1 col15" >2024-08-15</td>
      <td id="T_84c2f_row1_col16" class="data row1 col16" >USD</td>
      <td id="T_84c2f_row1_col17" class="data row1 col17" >USDOBS</td>
      <td id="T_84c2f_row1_col18" class="data row1 col18" >1.00</td>
      <td id="T_84c2f_row1_col19" class="data row1 col19" >0.00</td>
      <td id="T_84c2f_row1_col20" class="data row1 col20" >2,555.56</td>
      <td id="T_84c2f_row1_col21" class="data row1 col21" >2,555.56</td>
    </tr>
    <tr>
      <th id="T_84c2f_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_84c2f_row2_col0" class="data row2 col0" >2024-08-15</td>
      <td id="T_84c2f_row2_col1" class="data row2 col1" >2024-11-15</td>
      <td id="T_84c2f_row2_col2" class="data row2 col2" >2024-08-13</td>
      <td id="T_84c2f_row2_col3" class="data row2 col3" >2024-11-18</td>
      <td id="T_84c2f_row2_col4" class="data row2 col4" >1,000,000.00</td>
      <td id="T_84c2f_row2_col5" class="data row2 col5" >0.00</td>
      <td id="T_84c2f_row2_col6" class="data row2 col6" >2,555.56</td>
      <td id="T_84c2f_row2_col7" class="data row2 col7" >True</td>
      <td id="T_84c2f_row2_col8" class="data row2 col8" >2,555.56</td>
      <td id="T_84c2f_row2_col9" class="data row2 col9" >CLP</td>
      <td id="T_84c2f_row2_col10" class="data row2 col10" >TERMSOFR3M</td>
      <td id="T_84c2f_row2_col11" class="data row2 col11" >1.0000%</td>
      <td id="T_84c2f_row2_col12" class="data row2 col12" >1.00</td>
      <td id="T_84c2f_row2_col13" class="data row2 col13" >0.0000%</td>
      <td id="T_84c2f_row2_col14" class="data row2 col14" >LinAct360</td>
      <td id="T_84c2f_row2_col15" class="data row2 col15" >2024-11-15</td>
      <td id="T_84c2f_row2_col16" class="data row2 col16" >USD</td>
      <td id="T_84c2f_row2_col17" class="data row2 col17" >USDOBS</td>
      <td id="T_84c2f_row2_col18" class="data row2 col18" >1.00</td>
      <td id="T_84c2f_row2_col19" class="data row2 col19" >0.00</td>
      <td id="T_84c2f_row2_col20" class="data row2 col20" >2,555.56</td>
      <td id="T_84c2f_row2_col21" class="data row2 col21" >2,555.56</td>
    </tr>
    <tr>
      <th id="T_84c2f_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_84c2f_row3_col0" class="data row3 col0" >2024-11-15</td>
      <td id="T_84c2f_row3_col1" class="data row3 col1" >2025-02-15</td>
      <td id="T_84c2f_row3_col2" class="data row3 col2" >2024-11-13</td>
      <td id="T_84c2f_row3_col3" class="data row3 col3" >2025-02-19</td>
      <td id="T_84c2f_row3_col4" class="data row3 col4" >1,000,000.00</td>
      <td id="T_84c2f_row3_col5" class="data row3 col5" >0.00</td>
      <td id="T_84c2f_row3_col6" class="data row3 col6" >2,555.56</td>
      <td id="T_84c2f_row3_col7" class="data row3 col7" >True</td>
      <td id="T_84c2f_row3_col8" class="data row3 col8" >2,555.56</td>
      <td id="T_84c2f_row3_col9" class="data row3 col9" >CLP</td>
      <td id="T_84c2f_row3_col10" class="data row3 col10" >TERMSOFR3M</td>
      <td id="T_84c2f_row3_col11" class="data row3 col11" >1.0000%</td>
      <td id="T_84c2f_row3_col12" class="data row3 col12" >1.00</td>
      <td id="T_84c2f_row3_col13" class="data row3 col13" >0.0000%</td>
      <td id="T_84c2f_row3_col14" class="data row3 col14" >LinAct360</td>
      <td id="T_84c2f_row3_col15" class="data row3 col15" >2025-02-18</td>
      <td id="T_84c2f_row3_col16" class="data row3 col16" >USD</td>
      <td id="T_84c2f_row3_col17" class="data row3 col17" >USDOBS</td>
      <td id="T_84c2f_row3_col18" class="data row3 col18" >1.00</td>
      <td id="T_84c2f_row3_col19" class="data row3 col19" >0.00</td>
      <td id="T_84c2f_row3_col20" class="data row3 col20" >2,555.56</td>
      <td id="T_84c2f_row3_col21" class="data row3 col21" >2,555.56</td>
    </tr>
    <tr>
      <th id="T_84c2f_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_84c2f_row4_col0" class="data row4 col0" >2025-02-15</td>
      <td id="T_84c2f_row4_col1" class="data row4 col1" >2025-05-15</td>
      <td id="T_84c2f_row4_col2" class="data row4 col2" >2025-02-12</td>
      <td id="T_84c2f_row4_col3" class="data row4 col3" >2025-05-16</td>
      <td id="T_84c2f_row4_col4" class="data row4 col4" >1,000,000.00</td>
      <td id="T_84c2f_row4_col5" class="data row4 col5" >0.00</td>
      <td id="T_84c2f_row4_col6" class="data row4 col6" >2,472.22</td>
      <td id="T_84c2f_row4_col7" class="data row4 col7" >True</td>
      <td id="T_84c2f_row4_col8" class="data row4 col8" >2,472.22</td>
      <td id="T_84c2f_row4_col9" class="data row4 col9" >CLP</td>
      <td id="T_84c2f_row4_col10" class="data row4 col10" >TERMSOFR3M</td>
      <td id="T_84c2f_row4_col11" class="data row4 col11" >1.0000%</td>
      <td id="T_84c2f_row4_col12" class="data row4 col12" >1.00</td>
      <td id="T_84c2f_row4_col13" class="data row4 col13" >0.0000%</td>
      <td id="T_84c2f_row4_col14" class="data row4 col14" >LinAct360</td>
      <td id="T_84c2f_row4_col15" class="data row4 col15" >2025-05-15</td>
      <td id="T_84c2f_row4_col16" class="data row4 col16" >USD</td>
      <td id="T_84c2f_row4_col17" class="data row4 col17" >USDOBS</td>
      <td id="T_84c2f_row4_col18" class="data row4 col18" >1.00</td>
      <td id="T_84c2f_row4_col19" class="data row4 col19" >0.00</td>
      <td id="T_84c2f_row4_col20" class="data row4 col20" >2,472.22</td>
      <td id="T_84c2f_row4_col21" class="data row4 col21" >2,472.22</td>
    </tr>
    <tr>
      <th id="T_84c2f_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_84c2f_row5_col0" class="data row5 col0" >2025-05-15</td>
      <td id="T_84c2f_row5_col1" class="data row5 col1" >2025-08-15</td>
      <td id="T_84c2f_row5_col2" class="data row5 col2" >2025-05-13</td>
      <td id="T_84c2f_row5_col3" class="data row5 col3" >2025-08-18</td>
      <td id="T_84c2f_row5_col4" class="data row5 col4" >1,000,000.00</td>
      <td id="T_84c2f_row5_col5" class="data row5 col5" >0.00</td>
      <td id="T_84c2f_row5_col6" class="data row5 col6" >2,555.56</td>
      <td id="T_84c2f_row5_col7" class="data row5 col7" >True</td>
      <td id="T_84c2f_row5_col8" class="data row5 col8" >2,555.56</td>
      <td id="T_84c2f_row5_col9" class="data row5 col9" >CLP</td>
      <td id="T_84c2f_row5_col10" class="data row5 col10" >TERMSOFR3M</td>
      <td id="T_84c2f_row5_col11" class="data row5 col11" >1.0000%</td>
      <td id="T_84c2f_row5_col12" class="data row5 col12" >1.00</td>
      <td id="T_84c2f_row5_col13" class="data row5 col13" >0.0000%</td>
      <td id="T_84c2f_row5_col14" class="data row5 col14" >LinAct360</td>
      <td id="T_84c2f_row5_col15" class="data row5 col15" >2025-08-15</td>
      <td id="T_84c2f_row5_col16" class="data row5 col16" >USD</td>
      <td id="T_84c2f_row5_col17" class="data row5 col17" >USDOBS</td>
      <td id="T_84c2f_row5_col18" class="data row5 col18" >1.00</td>
      <td id="T_84c2f_row5_col19" class="data row5 col19" >0.00</td>
      <td id="T_84c2f_row5_col20" class="data row5 col20" >2,555.56</td>
      <td id="T_84c2f_row5_col21" class="data row5 col21" >2,555.56</td>
    </tr>
    <tr>
      <th id="T_84c2f_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_84c2f_row6_col0" class="data row6 col0" >2025-08-15</td>
      <td id="T_84c2f_row6_col1" class="data row6 col1" >2025-11-15</td>
      <td id="T_84c2f_row6_col2" class="data row6 col2" >2025-08-13</td>
      <td id="T_84c2f_row6_col3" class="data row6 col3" >2025-11-18</td>
      <td id="T_84c2f_row6_col4" class="data row6 col4" >1,000,000.00</td>
      <td id="T_84c2f_row6_col5" class="data row6 col5" >0.00</td>
      <td id="T_84c2f_row6_col6" class="data row6 col6" >2,555.56</td>
      <td id="T_84c2f_row6_col7" class="data row6 col7" >True</td>
      <td id="T_84c2f_row6_col8" class="data row6 col8" >2,555.56</td>
      <td id="T_84c2f_row6_col9" class="data row6 col9" >CLP</td>
      <td id="T_84c2f_row6_col10" class="data row6 col10" >TERMSOFR3M</td>
      <td id="T_84c2f_row6_col11" class="data row6 col11" >1.0000%</td>
      <td id="T_84c2f_row6_col12" class="data row6 col12" >1.00</td>
      <td id="T_84c2f_row6_col13" class="data row6 col13" >0.0000%</td>
      <td id="T_84c2f_row6_col14" class="data row6 col14" >LinAct360</td>
      <td id="T_84c2f_row6_col15" class="data row6 col15" >2025-11-17</td>
      <td id="T_84c2f_row6_col16" class="data row6 col16" >USD</td>
      <td id="T_84c2f_row6_col17" class="data row6 col17" >USDOBS</td>
      <td id="T_84c2f_row6_col18" class="data row6 col18" >1.00</td>
      <td id="T_84c2f_row6_col19" class="data row6 col19" >0.00</td>
      <td id="T_84c2f_row6_col20" class="data row6 col20" >2,555.56</td>
      <td id="T_84c2f_row6_col21" class="data row6 col21" >2,555.56</td>
    </tr>
    <tr>
      <th id="T_84c2f_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_84c2f_row7_col0" class="data row7 col0" >2025-11-15</td>
      <td id="T_84c2f_row7_col1" class="data row7 col1" >2026-02-15</td>
      <td id="T_84c2f_row7_col2" class="data row7 col2" >2025-11-12</td>
      <td id="T_84c2f_row7_col3" class="data row7 col3" >2026-02-18</td>
      <td id="T_84c2f_row7_col4" class="data row7 col4" >1,000,000.00</td>
      <td id="T_84c2f_row7_col5" class="data row7 col5" >1,000,000.00</td>
      <td id="T_84c2f_row7_col6" class="data row7 col6" >2,555.56</td>
      <td id="T_84c2f_row7_col7" class="data row7 col7" >True</td>
      <td id="T_84c2f_row7_col8" class="data row7 col8" >1,002,555.56</td>
      <td id="T_84c2f_row7_col9" class="data row7 col9" >CLP</td>
      <td id="T_84c2f_row7_col10" class="data row7 col10" >TERMSOFR3M</td>
      <td id="T_84c2f_row7_col11" class="data row7 col11" >1.0000%</td>
      <td id="T_84c2f_row7_col12" class="data row7 col12" >1.00</td>
      <td id="T_84c2f_row7_col13" class="data row7 col13" >0.0000%</td>
      <td id="T_84c2f_row7_col14" class="data row7 col14" >LinAct360</td>
      <td id="T_84c2f_row7_col15" class="data row7 col15" >2026-02-17</td>
      <td id="T_84c2f_row7_col16" class="data row7 col16" >USD</td>
      <td id="T_84c2f_row7_col17" class="data row7 col17" >USDOBS</td>
      <td id="T_84c2f_row7_col18" class="data row7 col18" >1.00</td>
      <td id="T_84c2f_row7_col19" class="data row7 col19" >1,000,000.00</td>
      <td id="T_84c2f_row7_col20" class="data row7 col20" >2,555.56</td>
      <td id="T_84c2f_row7_col21" class="data row7 col21" >1,002,555.56</td>
    </tr>
  </tbody>
</table>




Fijemos el valor del tipo de cambio en los cashflows para ver el efecto en las últimas dos columnas.


```python
for cashflow in ibor_mccy_leg.get_cashflows():
    cashflow.set_fx_rate_index_value(900.0)
```


```python
aux.leg_as_dataframe(ibor_mccy_leg).style.format(aux.format_dict).set_properties(
    **{'background-color': '#FFCFC9', 'color':'black'},
    subset=['valor_indice_fx','amortizacion_moneda_pago', 'interes_moneda_pago'],
)
```




<style type="text/css">
#T_aa3c4_row0_col18, #T_aa3c4_row0_col19, #T_aa3c4_row0_col20, #T_aa3c4_row1_col18, #T_aa3c4_row1_col19, #T_aa3c4_row1_col20, #T_aa3c4_row2_col18, #T_aa3c4_row2_col19, #T_aa3c4_row2_col20, #T_aa3c4_row3_col18, #T_aa3c4_row3_col19, #T_aa3c4_row3_col20, #T_aa3c4_row4_col18, #T_aa3c4_row4_col19, #T_aa3c4_row4_col20, #T_aa3c4_row5_col18, #T_aa3c4_row5_col19, #T_aa3c4_row5_col20, #T_aa3c4_row6_col18, #T_aa3c4_row6_col19, #T_aa3c4_row6_col20, #T_aa3c4_row7_col18, #T_aa3c4_row7_col19, #T_aa3c4_row7_col20 {
  background-color: #FFCFC9;
  color: black;
}
</style>
<table id="T_aa3c4">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_aa3c4_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_aa3c4_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_aa3c4_level0_col2" class="col_heading level0 col2" >fecha_fixing</th>
      <th id="T_aa3c4_level0_col3" class="col_heading level0 col3" >fecha_pago</th>
      <th id="T_aa3c4_level0_col4" class="col_heading level0 col4" >nocional</th>
      <th id="T_aa3c4_level0_col5" class="col_heading level0 col5" >amortizacion</th>
      <th id="T_aa3c4_level0_col6" class="col_heading level0 col6" >interes</th>
      <th id="T_aa3c4_level0_col7" class="col_heading level0 col7" >amort_es_flujo</th>
      <th id="T_aa3c4_level0_col8" class="col_heading level0 col8" >flujo</th>
      <th id="T_aa3c4_level0_col9" class="col_heading level0 col9" >moneda_nocional</th>
      <th id="T_aa3c4_level0_col10" class="col_heading level0 col10" >codigo_indice_tasa</th>
      <th id="T_aa3c4_level0_col11" class="col_heading level0 col11" >spread</th>
      <th id="T_aa3c4_level0_col12" class="col_heading level0 col12" >gearing</th>
      <th id="T_aa3c4_level0_col13" class="col_heading level0 col13" >valor_tasa</th>
      <th id="T_aa3c4_level0_col14" class="col_heading level0 col14" >tipo_tasa</th>
      <th id="T_aa3c4_level0_col15" class="col_heading level0 col15" >fecha_fixing_fx</th>
      <th id="T_aa3c4_level0_col16" class="col_heading level0 col16" >moneda_pago</th>
      <th id="T_aa3c4_level0_col17" class="col_heading level0 col17" >codigo_indice_fx</th>
      <th id="T_aa3c4_level0_col18" class="col_heading level0 col18" >valor_indice_fx</th>
      <th id="T_aa3c4_level0_col19" class="col_heading level0 col19" >amortizacion_moneda_pago</th>
      <th id="T_aa3c4_level0_col20" class="col_heading level0 col20" >interes_moneda_pago</th>
      <th id="T_aa3c4_level0_col21" class="col_heading level0 col21" >flujo_moneda_pago</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_aa3c4_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_aa3c4_row0_col0" class="data row0 col0" >2024-02-15</td>
      <td id="T_aa3c4_row0_col1" class="data row0 col1" >2024-05-15</td>
      <td id="T_aa3c4_row0_col2" class="data row0 col2" >2024-02-13</td>
      <td id="T_aa3c4_row0_col3" class="data row0 col3" >2024-05-16</td>
      <td id="T_aa3c4_row0_col4" class="data row0 col4" >1,000,000.00</td>
      <td id="T_aa3c4_row0_col5" class="data row0 col5" >0.00</td>
      <td id="T_aa3c4_row0_col6" class="data row0 col6" >2,500.00</td>
      <td id="T_aa3c4_row0_col7" class="data row0 col7" >True</td>
      <td id="T_aa3c4_row0_col8" class="data row0 col8" >2,500.00</td>
      <td id="T_aa3c4_row0_col9" class="data row0 col9" >CLP</td>
      <td id="T_aa3c4_row0_col10" class="data row0 col10" >TERMSOFR3M</td>
      <td id="T_aa3c4_row0_col11" class="data row0 col11" >1.0000%</td>
      <td id="T_aa3c4_row0_col12" class="data row0 col12" >1.00</td>
      <td id="T_aa3c4_row0_col13" class="data row0 col13" >0.0000%</td>
      <td id="T_aa3c4_row0_col14" class="data row0 col14" >LinAct360</td>
      <td id="T_aa3c4_row0_col15" class="data row0 col15" >2024-05-15</td>
      <td id="T_aa3c4_row0_col16" class="data row0 col16" >USD</td>
      <td id="T_aa3c4_row0_col17" class="data row0 col17" >USDOBS</td>
      <td id="T_aa3c4_row0_col18" class="data row0 col18" >900.00</td>
      <td id="T_aa3c4_row0_col19" class="data row0 col19" >0.00</td>
      <td id="T_aa3c4_row0_col20" class="data row0 col20" >2.78</td>
      <td id="T_aa3c4_row0_col21" class="data row0 col21" >2.78</td>
    </tr>
    <tr>
      <th id="T_aa3c4_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_aa3c4_row1_col0" class="data row1 col0" >2024-05-15</td>
      <td id="T_aa3c4_row1_col1" class="data row1 col1" >2024-08-15</td>
      <td id="T_aa3c4_row1_col2" class="data row1 col2" >2024-05-13</td>
      <td id="T_aa3c4_row1_col3" class="data row1 col3" >2024-08-16</td>
      <td id="T_aa3c4_row1_col4" class="data row1 col4" >1,000,000.00</td>
      <td id="T_aa3c4_row1_col5" class="data row1 col5" >0.00</td>
      <td id="T_aa3c4_row1_col6" class="data row1 col6" >2,555.56</td>
      <td id="T_aa3c4_row1_col7" class="data row1 col7" >True</td>
      <td id="T_aa3c4_row1_col8" class="data row1 col8" >2,555.56</td>
      <td id="T_aa3c4_row1_col9" class="data row1 col9" >CLP</td>
      <td id="T_aa3c4_row1_col10" class="data row1 col10" >TERMSOFR3M</td>
      <td id="T_aa3c4_row1_col11" class="data row1 col11" >1.0000%</td>
      <td id="T_aa3c4_row1_col12" class="data row1 col12" >1.00</td>
      <td id="T_aa3c4_row1_col13" class="data row1 col13" >0.0000%</td>
      <td id="T_aa3c4_row1_col14" class="data row1 col14" >LinAct360</td>
      <td id="T_aa3c4_row1_col15" class="data row1 col15" >2024-08-15</td>
      <td id="T_aa3c4_row1_col16" class="data row1 col16" >USD</td>
      <td id="T_aa3c4_row1_col17" class="data row1 col17" >USDOBS</td>
      <td id="T_aa3c4_row1_col18" class="data row1 col18" >900.00</td>
      <td id="T_aa3c4_row1_col19" class="data row1 col19" >0.00</td>
      <td id="T_aa3c4_row1_col20" class="data row1 col20" >2.84</td>
      <td id="T_aa3c4_row1_col21" class="data row1 col21" >2.84</td>
    </tr>
    <tr>
      <th id="T_aa3c4_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_aa3c4_row2_col0" class="data row2 col0" >2024-08-15</td>
      <td id="T_aa3c4_row2_col1" class="data row2 col1" >2024-11-15</td>
      <td id="T_aa3c4_row2_col2" class="data row2 col2" >2024-08-13</td>
      <td id="T_aa3c4_row2_col3" class="data row2 col3" >2024-11-18</td>
      <td id="T_aa3c4_row2_col4" class="data row2 col4" >1,000,000.00</td>
      <td id="T_aa3c4_row2_col5" class="data row2 col5" >0.00</td>
      <td id="T_aa3c4_row2_col6" class="data row2 col6" >2,555.56</td>
      <td id="T_aa3c4_row2_col7" class="data row2 col7" >True</td>
      <td id="T_aa3c4_row2_col8" class="data row2 col8" >2,555.56</td>
      <td id="T_aa3c4_row2_col9" class="data row2 col9" >CLP</td>
      <td id="T_aa3c4_row2_col10" class="data row2 col10" >TERMSOFR3M</td>
      <td id="T_aa3c4_row2_col11" class="data row2 col11" >1.0000%</td>
      <td id="T_aa3c4_row2_col12" class="data row2 col12" >1.00</td>
      <td id="T_aa3c4_row2_col13" class="data row2 col13" >0.0000%</td>
      <td id="T_aa3c4_row2_col14" class="data row2 col14" >LinAct360</td>
      <td id="T_aa3c4_row2_col15" class="data row2 col15" >2024-11-15</td>
      <td id="T_aa3c4_row2_col16" class="data row2 col16" >USD</td>
      <td id="T_aa3c4_row2_col17" class="data row2 col17" >USDOBS</td>
      <td id="T_aa3c4_row2_col18" class="data row2 col18" >900.00</td>
      <td id="T_aa3c4_row2_col19" class="data row2 col19" >0.00</td>
      <td id="T_aa3c4_row2_col20" class="data row2 col20" >2.84</td>
      <td id="T_aa3c4_row2_col21" class="data row2 col21" >2.84</td>
    </tr>
    <tr>
      <th id="T_aa3c4_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_aa3c4_row3_col0" class="data row3 col0" >2024-11-15</td>
      <td id="T_aa3c4_row3_col1" class="data row3 col1" >2025-02-15</td>
      <td id="T_aa3c4_row3_col2" class="data row3 col2" >2024-11-13</td>
      <td id="T_aa3c4_row3_col3" class="data row3 col3" >2025-02-19</td>
      <td id="T_aa3c4_row3_col4" class="data row3 col4" >1,000,000.00</td>
      <td id="T_aa3c4_row3_col5" class="data row3 col5" >0.00</td>
      <td id="T_aa3c4_row3_col6" class="data row3 col6" >2,555.56</td>
      <td id="T_aa3c4_row3_col7" class="data row3 col7" >True</td>
      <td id="T_aa3c4_row3_col8" class="data row3 col8" >2,555.56</td>
      <td id="T_aa3c4_row3_col9" class="data row3 col9" >CLP</td>
      <td id="T_aa3c4_row3_col10" class="data row3 col10" >TERMSOFR3M</td>
      <td id="T_aa3c4_row3_col11" class="data row3 col11" >1.0000%</td>
      <td id="T_aa3c4_row3_col12" class="data row3 col12" >1.00</td>
      <td id="T_aa3c4_row3_col13" class="data row3 col13" >0.0000%</td>
      <td id="T_aa3c4_row3_col14" class="data row3 col14" >LinAct360</td>
      <td id="T_aa3c4_row3_col15" class="data row3 col15" >2025-02-18</td>
      <td id="T_aa3c4_row3_col16" class="data row3 col16" >USD</td>
      <td id="T_aa3c4_row3_col17" class="data row3 col17" >USDOBS</td>
      <td id="T_aa3c4_row3_col18" class="data row3 col18" >900.00</td>
      <td id="T_aa3c4_row3_col19" class="data row3 col19" >0.00</td>
      <td id="T_aa3c4_row3_col20" class="data row3 col20" >2.84</td>
      <td id="T_aa3c4_row3_col21" class="data row3 col21" >2.84</td>
    </tr>
    <tr>
      <th id="T_aa3c4_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_aa3c4_row4_col0" class="data row4 col0" >2025-02-15</td>
      <td id="T_aa3c4_row4_col1" class="data row4 col1" >2025-05-15</td>
      <td id="T_aa3c4_row4_col2" class="data row4 col2" >2025-02-12</td>
      <td id="T_aa3c4_row4_col3" class="data row4 col3" >2025-05-16</td>
      <td id="T_aa3c4_row4_col4" class="data row4 col4" >1,000,000.00</td>
      <td id="T_aa3c4_row4_col5" class="data row4 col5" >0.00</td>
      <td id="T_aa3c4_row4_col6" class="data row4 col6" >2,472.22</td>
      <td id="T_aa3c4_row4_col7" class="data row4 col7" >True</td>
      <td id="T_aa3c4_row4_col8" class="data row4 col8" >2,472.22</td>
      <td id="T_aa3c4_row4_col9" class="data row4 col9" >CLP</td>
      <td id="T_aa3c4_row4_col10" class="data row4 col10" >TERMSOFR3M</td>
      <td id="T_aa3c4_row4_col11" class="data row4 col11" >1.0000%</td>
      <td id="T_aa3c4_row4_col12" class="data row4 col12" >1.00</td>
      <td id="T_aa3c4_row4_col13" class="data row4 col13" >0.0000%</td>
      <td id="T_aa3c4_row4_col14" class="data row4 col14" >LinAct360</td>
      <td id="T_aa3c4_row4_col15" class="data row4 col15" >2025-05-15</td>
      <td id="T_aa3c4_row4_col16" class="data row4 col16" >USD</td>
      <td id="T_aa3c4_row4_col17" class="data row4 col17" >USDOBS</td>
      <td id="T_aa3c4_row4_col18" class="data row4 col18" >900.00</td>
      <td id="T_aa3c4_row4_col19" class="data row4 col19" >0.00</td>
      <td id="T_aa3c4_row4_col20" class="data row4 col20" >2.75</td>
      <td id="T_aa3c4_row4_col21" class="data row4 col21" >2.75</td>
    </tr>
    <tr>
      <th id="T_aa3c4_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_aa3c4_row5_col0" class="data row5 col0" >2025-05-15</td>
      <td id="T_aa3c4_row5_col1" class="data row5 col1" >2025-08-15</td>
      <td id="T_aa3c4_row5_col2" class="data row5 col2" >2025-05-13</td>
      <td id="T_aa3c4_row5_col3" class="data row5 col3" >2025-08-18</td>
      <td id="T_aa3c4_row5_col4" class="data row5 col4" >1,000,000.00</td>
      <td id="T_aa3c4_row5_col5" class="data row5 col5" >0.00</td>
      <td id="T_aa3c4_row5_col6" class="data row5 col6" >2,555.56</td>
      <td id="T_aa3c4_row5_col7" class="data row5 col7" >True</td>
      <td id="T_aa3c4_row5_col8" class="data row5 col8" >2,555.56</td>
      <td id="T_aa3c4_row5_col9" class="data row5 col9" >CLP</td>
      <td id="T_aa3c4_row5_col10" class="data row5 col10" >TERMSOFR3M</td>
      <td id="T_aa3c4_row5_col11" class="data row5 col11" >1.0000%</td>
      <td id="T_aa3c4_row5_col12" class="data row5 col12" >1.00</td>
      <td id="T_aa3c4_row5_col13" class="data row5 col13" >0.0000%</td>
      <td id="T_aa3c4_row5_col14" class="data row5 col14" >LinAct360</td>
      <td id="T_aa3c4_row5_col15" class="data row5 col15" >2025-08-15</td>
      <td id="T_aa3c4_row5_col16" class="data row5 col16" >USD</td>
      <td id="T_aa3c4_row5_col17" class="data row5 col17" >USDOBS</td>
      <td id="T_aa3c4_row5_col18" class="data row5 col18" >900.00</td>
      <td id="T_aa3c4_row5_col19" class="data row5 col19" >0.00</td>
      <td id="T_aa3c4_row5_col20" class="data row5 col20" >2.84</td>
      <td id="T_aa3c4_row5_col21" class="data row5 col21" >2.84</td>
    </tr>
    <tr>
      <th id="T_aa3c4_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_aa3c4_row6_col0" class="data row6 col0" >2025-08-15</td>
      <td id="T_aa3c4_row6_col1" class="data row6 col1" >2025-11-15</td>
      <td id="T_aa3c4_row6_col2" class="data row6 col2" >2025-08-13</td>
      <td id="T_aa3c4_row6_col3" class="data row6 col3" >2025-11-18</td>
      <td id="T_aa3c4_row6_col4" class="data row6 col4" >1,000,000.00</td>
      <td id="T_aa3c4_row6_col5" class="data row6 col5" >0.00</td>
      <td id="T_aa3c4_row6_col6" class="data row6 col6" >2,555.56</td>
      <td id="T_aa3c4_row6_col7" class="data row6 col7" >True</td>
      <td id="T_aa3c4_row6_col8" class="data row6 col8" >2,555.56</td>
      <td id="T_aa3c4_row6_col9" class="data row6 col9" >CLP</td>
      <td id="T_aa3c4_row6_col10" class="data row6 col10" >TERMSOFR3M</td>
      <td id="T_aa3c4_row6_col11" class="data row6 col11" >1.0000%</td>
      <td id="T_aa3c4_row6_col12" class="data row6 col12" >1.00</td>
      <td id="T_aa3c4_row6_col13" class="data row6 col13" >0.0000%</td>
      <td id="T_aa3c4_row6_col14" class="data row6 col14" >LinAct360</td>
      <td id="T_aa3c4_row6_col15" class="data row6 col15" >2025-11-17</td>
      <td id="T_aa3c4_row6_col16" class="data row6 col16" >USD</td>
      <td id="T_aa3c4_row6_col17" class="data row6 col17" >USDOBS</td>
      <td id="T_aa3c4_row6_col18" class="data row6 col18" >900.00</td>
      <td id="T_aa3c4_row6_col19" class="data row6 col19" >0.00</td>
      <td id="T_aa3c4_row6_col20" class="data row6 col20" >2.84</td>
      <td id="T_aa3c4_row6_col21" class="data row6 col21" >2.84</td>
    </tr>
    <tr>
      <th id="T_aa3c4_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_aa3c4_row7_col0" class="data row7 col0" >2025-11-15</td>
      <td id="T_aa3c4_row7_col1" class="data row7 col1" >2026-02-15</td>
      <td id="T_aa3c4_row7_col2" class="data row7 col2" >2025-11-12</td>
      <td id="T_aa3c4_row7_col3" class="data row7 col3" >2026-02-18</td>
      <td id="T_aa3c4_row7_col4" class="data row7 col4" >1,000,000.00</td>
      <td id="T_aa3c4_row7_col5" class="data row7 col5" >1,000,000.00</td>
      <td id="T_aa3c4_row7_col6" class="data row7 col6" >2,555.56</td>
      <td id="T_aa3c4_row7_col7" class="data row7 col7" >True</td>
      <td id="T_aa3c4_row7_col8" class="data row7 col8" >1,002,555.56</td>
      <td id="T_aa3c4_row7_col9" class="data row7 col9" >CLP</td>
      <td id="T_aa3c4_row7_col10" class="data row7 col10" >TERMSOFR3M</td>
      <td id="T_aa3c4_row7_col11" class="data row7 col11" >1.0000%</td>
      <td id="T_aa3c4_row7_col12" class="data row7 col12" >1.00</td>
      <td id="T_aa3c4_row7_col13" class="data row7 col13" >0.0000%</td>
      <td id="T_aa3c4_row7_col14" class="data row7 col14" >LinAct360</td>
      <td id="T_aa3c4_row7_col15" class="data row7 col15" >2026-02-17</td>
      <td id="T_aa3c4_row7_col16" class="data row7 col16" >USD</td>
      <td id="T_aa3c4_row7_col17" class="data row7 col17" >USDOBS</td>
      <td id="T_aa3c4_row7_col18" class="data row7 col18" >900.00</td>
      <td id="T_aa3c4_row7_col19" class="data row7 col19" >1,111.11</td>
      <td id="T_aa3c4_row7_col20" class="data row7 col20" >2.84</td>
      <td id="T_aa3c4_row7_col21" class="data row7 col21" >1,113.95</td>
    </tr>
  </tbody>
</table>




## Construcción Asistida de un `OvernightIndexLeg`

En este ejemplo se construye un `Leg` con `OvernightIndexCashflow` y amortización bullet.
Se requieren los siguientes parámetros:

- `RecPay`: enum que indica si los flujos se reciben o pagan
- `QCDate`: fecha de inicio del primer flujo
- `QCDate`: fecha final del último flujo sin considerar ajustes de días feriados
- `BusyAdRules`: enum que representa el tipo de ajuste en la fecha final para días feriados
- `BusyAdRules`: tipo de ajuste en la fecha de fijación de los valores inicial y final del índice en cada cupón
- `Tenor`: la periodicidad de pago
- `QCInterestRateLeg::QCStubPeriod`: enum que representa el tipo de período irregular (si aplica)
- `QCBusinessCalendar`: calendario que aplica para las fechas de pago
- `QCBusinessCalendar`: calendario que aplica para las fechas de fijación del índice
- `unsigned int`: lag de pago expresado en días
- `float`: nominal
- `bool`: si es `True` significa que la amortización final es un flujo de caja efectivo
- `float`: spread aditivo
- `float`: spread multiplicativo o gearing (tasa * gearing + spread)
- `QCInterestRate`: representa el tipo de tasa que se usará que se usará para la tasa equivalente
- `string`: nombre del índice overnight a utilizar
- `unsigned int`: número de decimales de la tasa equivalente
- `QCCurrency`: moneda del nocional
- `DatesForEquivalentRate`: enum que indica qué fechas se utilizan en el cálculo de la tasa equivalente (fechas de devengo o de índice)
- `SettLagBehaviour`: este parámetro indica cómo se calcula un `settlement_date` cuando un `end_date` cae en un día festivo.

**NOTA:** para construir un `Leg` con `OvernightIndexCashflow` y amortización customizada, sólo se debe cambiar el parámetro **nominal** por **CustomNotionalAndAmort** e invocar el método `qcf.LegFactory.build_custom_amort_overnight_index_leg(...)`.

Vamos al ejemplo. Primeramente, se da de alta los parámetros requeridos


```python
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(31, 1, 2024)
fecha_final = qcf.QCDate(31, 1, 2029) 
bus_adj_rule = qcf.BusyAdjRules.NO
index_adj_rule = qcf.BusyAdjRules.FOLLOW
periodicidad_pago = qcf.Tenor('6M')
periodo_irregular_pago = qcf.StubPeriod.NO
calendario = aux.get_business_calendar('CL', range(2024, 2035))
num_decimales_tasa_eq = 8
lag_pago = 0
nominal = 100_000_000.0
amort_es_flujo = True 
spread = .01
gearing = 1.0
interest_rate=qcf.QCInterestRate(0.0, qcf.QCAct360(), qcf.QCLinearWf())
nombre_indice = 'ICPCLP'
dates_for_eq_rate = qcf.DatesForEquivalentRate.ACCRUAL
sett_lag_behaviour = qcf.SettLagBehaviour.MOVE_TO_WORKING_DAY
```

Finalmente, se da de alta el objeto.


```python
on_index_leg = qcf.LegFactory.build_bullet_overnight_index_leg(
    rec_pay=rp, 
    start_date=fecha_inicio,
    end_date=fecha_final, 
    bus_adj_rule=bus_adj_rule, 
    fix_adj_rule=index_adj_rule,
    settlement_periodicity=periodicidad_pago,
    settlement_stub_period=periodo_irregular_pago, 
    settlement_calendar=calendario, 
    fixing_calendar=calendario,
    settlement_lag=lag_pago,
    initial_notional=nominal, 
    amort_is_cashflow=amort_es_flujo, 
    spread=spread, 
    gearing=gearing,
    interest_rate=interest_rate,
    index_name=nombre_indice,
    eq_rate_decimal_places=num_decimales_tasa_eq,
    notional_currency=clp,
    dates_for_eq_rate=dates_for_eq_rate,
    sett_lag_behaviour=sett_lag_behaviour,
)
```

Se visualiza.


```python
aux.leg_as_dataframe(on_index_leg).style.format(aux.format_dict)
```




<style type="text/css">
</style>
<table id="T_b61c6">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_b61c6_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_b61c6_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_b61c6_level0_col2" class="col_heading level0 col2" >fecha_inicial_indice</th>
      <th id="T_b61c6_level0_col3" class="col_heading level0 col3" >fecha_final_indice</th>
      <th id="T_b61c6_level0_col4" class="col_heading level0 col4" >fecha_pago</th>
      <th id="T_b61c6_level0_col5" class="col_heading level0 col5" >nocional</th>
      <th id="T_b61c6_level0_col6" class="col_heading level0 col6" >amortizacion</th>
      <th id="T_b61c6_level0_col7" class="col_heading level0 col7" >amort_es_flujo</th>
      <th id="T_b61c6_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_b61c6_level0_col9" class="col_heading level0 col9" >nombre_indice</th>
      <th id="T_b61c6_level0_col10" class="col_heading level0 col10" >valor_indice_inicial</th>
      <th id="T_b61c6_level0_col11" class="col_heading level0 col11" >valor_indice_final</th>
      <th id="T_b61c6_level0_col12" class="col_heading level0 col12" >valor_tasa</th>
      <th id="T_b61c6_level0_col13" class="col_heading level0 col13" >tipo_tasa</th>
      <th id="T_b61c6_level0_col14" class="col_heading level0 col14" >interes</th>
      <th id="T_b61c6_level0_col15" class="col_heading level0 col15" >flujo</th>
      <th id="T_b61c6_level0_col16" class="col_heading level0 col16" >spread</th>
      <th id="T_b61c6_level0_col17" class="col_heading level0 col17" >gearing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_b61c6_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_b61c6_row0_col0" class="data row0 col0" >2024-01-31</td>
      <td id="T_b61c6_row0_col1" class="data row0 col1" >2024-07-31</td>
      <td id="T_b61c6_row0_col2" class="data row0 col2" >2024-01-31</td>
      <td id="T_b61c6_row0_col3" class="data row0 col3" >2024-07-31</td>
      <td id="T_b61c6_row0_col4" class="data row0 col4" >2024-07-31</td>
      <td id="T_b61c6_row0_col5" class="data row0 col5" >100,000,000.00</td>
      <td id="T_b61c6_row0_col6" class="data row0 col6" >0.00</td>
      <td id="T_b61c6_row0_col7" class="data row0 col7" >True</td>
      <td id="T_b61c6_row0_col8" class="data row0 col8" >CLP</td>
      <td id="T_b61c6_row0_col9" class="data row0 col9" >ICPCLP</td>
      <td id="T_b61c6_row0_col10" class="data row0 col10" >1.000000</td>
      <td id="T_b61c6_row0_col11" class="data row0 col11" >1.000000</td>
      <td id="T_b61c6_row0_col12" class="data row0 col12" >0.0000%</td>
      <td id="T_b61c6_row0_col13" class="data row0 col13" >LinAct360</td>
      <td id="T_b61c6_row0_col14" class="data row0 col14" >505,556.00</td>
      <td id="T_b61c6_row0_col15" class="data row0 col15" >505,556.00</td>
      <td id="T_b61c6_row0_col16" class="data row0 col16" >1.0000%</td>
      <td id="T_b61c6_row0_col17" class="data row0 col17" >1.00</td>
    </tr>
    <tr>
      <th id="T_b61c6_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_b61c6_row1_col0" class="data row1 col0" >2024-07-31</td>
      <td id="T_b61c6_row1_col1" class="data row1 col1" >2025-01-31</td>
      <td id="T_b61c6_row1_col2" class="data row1 col2" >2024-07-31</td>
      <td id="T_b61c6_row1_col3" class="data row1 col3" >2025-01-31</td>
      <td id="T_b61c6_row1_col4" class="data row1 col4" >2025-01-31</td>
      <td id="T_b61c6_row1_col5" class="data row1 col5" >100,000,000.00</td>
      <td id="T_b61c6_row1_col6" class="data row1 col6" >0.00</td>
      <td id="T_b61c6_row1_col7" class="data row1 col7" >True</td>
      <td id="T_b61c6_row1_col8" class="data row1 col8" >CLP</td>
      <td id="T_b61c6_row1_col9" class="data row1 col9" >ICPCLP</td>
      <td id="T_b61c6_row1_col10" class="data row1 col10" >1.000000</td>
      <td id="T_b61c6_row1_col11" class="data row1 col11" >1.000000</td>
      <td id="T_b61c6_row1_col12" class="data row1 col12" >0.0000%</td>
      <td id="T_b61c6_row1_col13" class="data row1 col13" >LinAct360</td>
      <td id="T_b61c6_row1_col14" class="data row1 col14" >511,111.00</td>
      <td id="T_b61c6_row1_col15" class="data row1 col15" >511,111.00</td>
      <td id="T_b61c6_row1_col16" class="data row1 col16" >1.0000%</td>
      <td id="T_b61c6_row1_col17" class="data row1 col17" >1.00</td>
    </tr>
    <tr>
      <th id="T_b61c6_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_b61c6_row2_col0" class="data row2 col0" >2025-01-31</td>
      <td id="T_b61c6_row2_col1" class="data row2 col1" >2025-07-31</td>
      <td id="T_b61c6_row2_col2" class="data row2 col2" >2025-01-31</td>
      <td id="T_b61c6_row2_col3" class="data row2 col3" >2025-07-31</td>
      <td id="T_b61c6_row2_col4" class="data row2 col4" >2025-07-31</td>
      <td id="T_b61c6_row2_col5" class="data row2 col5" >100,000,000.00</td>
      <td id="T_b61c6_row2_col6" class="data row2 col6" >0.00</td>
      <td id="T_b61c6_row2_col7" class="data row2 col7" >True</td>
      <td id="T_b61c6_row2_col8" class="data row2 col8" >CLP</td>
      <td id="T_b61c6_row2_col9" class="data row2 col9" >ICPCLP</td>
      <td id="T_b61c6_row2_col10" class="data row2 col10" >1.000000</td>
      <td id="T_b61c6_row2_col11" class="data row2 col11" >1.000000</td>
      <td id="T_b61c6_row2_col12" class="data row2 col12" >0.0000%</td>
      <td id="T_b61c6_row2_col13" class="data row2 col13" >LinAct360</td>
      <td id="T_b61c6_row2_col14" class="data row2 col14" >502,778.00</td>
      <td id="T_b61c6_row2_col15" class="data row2 col15" >502,778.00</td>
      <td id="T_b61c6_row2_col16" class="data row2 col16" >1.0000%</td>
      <td id="T_b61c6_row2_col17" class="data row2 col17" >1.00</td>
    </tr>
    <tr>
      <th id="T_b61c6_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_b61c6_row3_col0" class="data row3 col0" >2025-07-31</td>
      <td id="T_b61c6_row3_col1" class="data row3 col1" >2026-01-31</td>
      <td id="T_b61c6_row3_col2" class="data row3 col2" >2025-07-31</td>
      <td id="T_b61c6_row3_col3" class="data row3 col3" >2026-02-02</td>
      <td id="T_b61c6_row3_col4" class="data row3 col4" >2026-02-02</td>
      <td id="T_b61c6_row3_col5" class="data row3 col5" >100,000,000.00</td>
      <td id="T_b61c6_row3_col6" class="data row3 col6" >0.00</td>
      <td id="T_b61c6_row3_col7" class="data row3 col7" >True</td>
      <td id="T_b61c6_row3_col8" class="data row3 col8" >CLP</td>
      <td id="T_b61c6_row3_col9" class="data row3 col9" >ICPCLP</td>
      <td id="T_b61c6_row3_col10" class="data row3 col10" >1.000000</td>
      <td id="T_b61c6_row3_col11" class="data row3 col11" >1.000000</td>
      <td id="T_b61c6_row3_col12" class="data row3 col12" >0.0000%</td>
      <td id="T_b61c6_row3_col13" class="data row3 col13" >LinAct360</td>
      <td id="T_b61c6_row3_col14" class="data row3 col14" >511,111.00</td>
      <td id="T_b61c6_row3_col15" class="data row3 col15" >511,111.00</td>
      <td id="T_b61c6_row3_col16" class="data row3 col16" >1.0000%</td>
      <td id="T_b61c6_row3_col17" class="data row3 col17" >1.00</td>
    </tr>
    <tr>
      <th id="T_b61c6_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_b61c6_row4_col0" class="data row4 col0" >2026-01-31</td>
      <td id="T_b61c6_row4_col1" class="data row4 col1" >2026-07-31</td>
      <td id="T_b61c6_row4_col2" class="data row4 col2" >2026-02-02</td>
      <td id="T_b61c6_row4_col3" class="data row4 col3" >2026-07-31</td>
      <td id="T_b61c6_row4_col4" class="data row4 col4" >2026-07-31</td>
      <td id="T_b61c6_row4_col5" class="data row4 col5" >100,000,000.00</td>
      <td id="T_b61c6_row4_col6" class="data row4 col6" >0.00</td>
      <td id="T_b61c6_row4_col7" class="data row4 col7" >True</td>
      <td id="T_b61c6_row4_col8" class="data row4 col8" >CLP</td>
      <td id="T_b61c6_row4_col9" class="data row4 col9" >ICPCLP</td>
      <td id="T_b61c6_row4_col10" class="data row4 col10" >1.000000</td>
      <td id="T_b61c6_row4_col11" class="data row4 col11" >1.000000</td>
      <td id="T_b61c6_row4_col12" class="data row4 col12" >0.0000%</td>
      <td id="T_b61c6_row4_col13" class="data row4 col13" >LinAct360</td>
      <td id="T_b61c6_row4_col14" class="data row4 col14" >502,778.00</td>
      <td id="T_b61c6_row4_col15" class="data row4 col15" >502,778.00</td>
      <td id="T_b61c6_row4_col16" class="data row4 col16" >1.0000%</td>
      <td id="T_b61c6_row4_col17" class="data row4 col17" >1.00</td>
    </tr>
    <tr>
      <th id="T_b61c6_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_b61c6_row5_col0" class="data row5 col0" >2026-07-31</td>
      <td id="T_b61c6_row5_col1" class="data row5 col1" >2027-01-31</td>
      <td id="T_b61c6_row5_col2" class="data row5 col2" >2026-07-31</td>
      <td id="T_b61c6_row5_col3" class="data row5 col3" >2027-02-01</td>
      <td id="T_b61c6_row5_col4" class="data row5 col4" >2027-02-01</td>
      <td id="T_b61c6_row5_col5" class="data row5 col5" >100,000,000.00</td>
      <td id="T_b61c6_row5_col6" class="data row5 col6" >0.00</td>
      <td id="T_b61c6_row5_col7" class="data row5 col7" >True</td>
      <td id="T_b61c6_row5_col8" class="data row5 col8" >CLP</td>
      <td id="T_b61c6_row5_col9" class="data row5 col9" >ICPCLP</td>
      <td id="T_b61c6_row5_col10" class="data row5 col10" >1.000000</td>
      <td id="T_b61c6_row5_col11" class="data row5 col11" >1.000000</td>
      <td id="T_b61c6_row5_col12" class="data row5 col12" >0.0000%</td>
      <td id="T_b61c6_row5_col13" class="data row5 col13" >LinAct360</td>
      <td id="T_b61c6_row5_col14" class="data row5 col14" >511,111.00</td>
      <td id="T_b61c6_row5_col15" class="data row5 col15" >511,111.00</td>
      <td id="T_b61c6_row5_col16" class="data row5 col16" >1.0000%</td>
      <td id="T_b61c6_row5_col17" class="data row5 col17" >1.00</td>
    </tr>
    <tr>
      <th id="T_b61c6_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_b61c6_row6_col0" class="data row6 col0" >2027-01-31</td>
      <td id="T_b61c6_row6_col1" class="data row6 col1" >2027-07-31</td>
      <td id="T_b61c6_row6_col2" class="data row6 col2" >2027-02-01</td>
      <td id="T_b61c6_row6_col3" class="data row6 col3" >2027-08-02</td>
      <td id="T_b61c6_row6_col4" class="data row6 col4" >2027-08-02</td>
      <td id="T_b61c6_row6_col5" class="data row6 col5" >100,000,000.00</td>
      <td id="T_b61c6_row6_col6" class="data row6 col6" >0.00</td>
      <td id="T_b61c6_row6_col7" class="data row6 col7" >True</td>
      <td id="T_b61c6_row6_col8" class="data row6 col8" >CLP</td>
      <td id="T_b61c6_row6_col9" class="data row6 col9" >ICPCLP</td>
      <td id="T_b61c6_row6_col10" class="data row6 col10" >1.000000</td>
      <td id="T_b61c6_row6_col11" class="data row6 col11" >1.000000</td>
      <td id="T_b61c6_row6_col12" class="data row6 col12" >0.0000%</td>
      <td id="T_b61c6_row6_col13" class="data row6 col13" >LinAct360</td>
      <td id="T_b61c6_row6_col14" class="data row6 col14" >502,778.00</td>
      <td id="T_b61c6_row6_col15" class="data row6 col15" >502,778.00</td>
      <td id="T_b61c6_row6_col16" class="data row6 col16" >1.0000%</td>
      <td id="T_b61c6_row6_col17" class="data row6 col17" >1.00</td>
    </tr>
    <tr>
      <th id="T_b61c6_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_b61c6_row7_col0" class="data row7 col0" >2027-07-31</td>
      <td id="T_b61c6_row7_col1" class="data row7 col1" >2028-01-31</td>
      <td id="T_b61c6_row7_col2" class="data row7 col2" >2027-08-02</td>
      <td id="T_b61c6_row7_col3" class="data row7 col3" >2028-01-31</td>
      <td id="T_b61c6_row7_col4" class="data row7 col4" >2028-01-31</td>
      <td id="T_b61c6_row7_col5" class="data row7 col5" >100,000,000.00</td>
      <td id="T_b61c6_row7_col6" class="data row7 col6" >0.00</td>
      <td id="T_b61c6_row7_col7" class="data row7 col7" >True</td>
      <td id="T_b61c6_row7_col8" class="data row7 col8" >CLP</td>
      <td id="T_b61c6_row7_col9" class="data row7 col9" >ICPCLP</td>
      <td id="T_b61c6_row7_col10" class="data row7 col10" >1.000000</td>
      <td id="T_b61c6_row7_col11" class="data row7 col11" >1.000000</td>
      <td id="T_b61c6_row7_col12" class="data row7 col12" >0.0000%</td>
      <td id="T_b61c6_row7_col13" class="data row7 col13" >LinAct360</td>
      <td id="T_b61c6_row7_col14" class="data row7 col14" >511,111.00</td>
      <td id="T_b61c6_row7_col15" class="data row7 col15" >511,111.00</td>
      <td id="T_b61c6_row7_col16" class="data row7 col16" >1.0000%</td>
      <td id="T_b61c6_row7_col17" class="data row7 col17" >1.00</td>
    </tr>
    <tr>
      <th id="T_b61c6_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_b61c6_row8_col0" class="data row8 col0" >2028-01-31</td>
      <td id="T_b61c6_row8_col1" class="data row8 col1" >2028-07-31</td>
      <td id="T_b61c6_row8_col2" class="data row8 col2" >2028-01-31</td>
      <td id="T_b61c6_row8_col3" class="data row8 col3" >2028-07-31</td>
      <td id="T_b61c6_row8_col4" class="data row8 col4" >2028-07-31</td>
      <td id="T_b61c6_row8_col5" class="data row8 col5" >100,000,000.00</td>
      <td id="T_b61c6_row8_col6" class="data row8 col6" >0.00</td>
      <td id="T_b61c6_row8_col7" class="data row8 col7" >True</td>
      <td id="T_b61c6_row8_col8" class="data row8 col8" >CLP</td>
      <td id="T_b61c6_row8_col9" class="data row8 col9" >ICPCLP</td>
      <td id="T_b61c6_row8_col10" class="data row8 col10" >1.000000</td>
      <td id="T_b61c6_row8_col11" class="data row8 col11" >1.000000</td>
      <td id="T_b61c6_row8_col12" class="data row8 col12" >0.0000%</td>
      <td id="T_b61c6_row8_col13" class="data row8 col13" >LinAct360</td>
      <td id="T_b61c6_row8_col14" class="data row8 col14" >505,556.00</td>
      <td id="T_b61c6_row8_col15" class="data row8 col15" >505,556.00</td>
      <td id="T_b61c6_row8_col16" class="data row8 col16" >1.0000%</td>
      <td id="T_b61c6_row8_col17" class="data row8 col17" >1.00</td>
    </tr>
    <tr>
      <th id="T_b61c6_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_b61c6_row9_col0" class="data row9 col0" >2028-07-31</td>
      <td id="T_b61c6_row9_col1" class="data row9 col1" >2029-01-31</td>
      <td id="T_b61c6_row9_col2" class="data row9 col2" >2028-07-31</td>
      <td id="T_b61c6_row9_col3" class="data row9 col3" >2029-01-31</td>
      <td id="T_b61c6_row9_col4" class="data row9 col4" >2029-01-31</td>
      <td id="T_b61c6_row9_col5" class="data row9 col5" >100,000,000.00</td>
      <td id="T_b61c6_row9_col6" class="data row9 col6" >100,000,000.00</td>
      <td id="T_b61c6_row9_col7" class="data row9 col7" >True</td>
      <td id="T_b61c6_row9_col8" class="data row9 col8" >CLP</td>
      <td id="T_b61c6_row9_col9" class="data row9 col9" >ICPCLP</td>
      <td id="T_b61c6_row9_col10" class="data row9 col10" >1.000000</td>
      <td id="T_b61c6_row9_col11" class="data row9 col11" >1.000000</td>
      <td id="T_b61c6_row9_col12" class="data row9 col12" >0.0000%</td>
      <td id="T_b61c6_row9_col13" class="data row9 col13" >LinAct360</td>
      <td id="T_b61c6_row9_col14" class="data row9 col14" >511,111.00</td>
      <td id="T_b61c6_row9_col15" class="data row9 col15" >100,511,111.00</td>
      <td id="T_b61c6_row9_col16" class="data row9 col16" >1.0000%</td>
      <td id="T_b61c6_row9_col17" class="data row9 col17" >1.00</td>
    </tr>
  </tbody>
</table>




## Construcción Asistida de un `OvernightIndexMultiCurrencyLeg`

En este ejemplo se construye un `Leg` con `OvernightIndexMultiCurrencyCashflow` y amortización bullet.
Se requieren los siguientes parámetros:

- `RecPay`: enum que indica si los flujos se reciben o pagan
- `QCDate`: fecha de inicio del primer flujo
- `QCDate`: fecha final del último flujo sin considerar ajustes de días feriados
- `BusyAdRules`: enum que representa el tipo de ajuste en la fecha final para días feriados
- `BusyAdRules`: tipo de ajuste en la fecha de fijación de los valores inicial y final del índice en cada cupón
- `Tenor`: la periodicidad de pago
- `QCInterestRateLeg::QCStubPeriod`: enum que representa el tipo de período irregular (si aplica)
- `QCBusinessCalendar`: calendario que aplica para las fechas de pago
- `QCBusinessCalendar`: calendario que aplica para las fechas de fijación del índice
- `unsigned int`: lag de pago expresado en días
- `float`: nominal
- `bool`: si es `True` significa que la amortización final es un flujo de caja efectivo
- `float`: spread aditivo
- `float`: spread multiplicativo
- `QCInterestRate`: representa el tipo de tasa que se usará que se usará para la tasa equivalente
- `string`: nombre del índice overnight a utilizar
- `unsigned int`: número de decimales de la tasa equivalente
- `QCCurrency`: moneda del nocional
- `DatesForEquivalentRate`: enum que indica qué fechas se utilizan en el cálculo de la tasa equivalente (fechas de devengo o de índice)
- `SettLagBehaviour`: este parámetro indica cómo se calcula un `settlement_date` cuando un `end_date` cae en un día festivo.
---
**MultiCurrency**
- `QCCurrency`: moneda de pago los flujos
- `FXRateIndex`: índice con el cual se transforma cada flujo a la moneda de pago
- `int`: lag de fijación del FXRateIndex (respecto a settlement date)
- `FxFixingLagPivot`: este parámetro indica si el lag de fijación del índice FX se aplica sobre `end_date` o sobre `settlement_date`.
- `FxFixingLagAppliesTo`: indica si el lag se refiere a `FIXING_DATE` o `PUBISHING_DATE` del índice.

**NOTA:** para construir un `Leg` con `OvernightIndexMultiCurrencyCashflow` y amortización customizada, sólo se debe cambiar el parámetro **nominal** por **CustomNotionalAndAmort** e invocar el método `qcf.LegFactory.build_custom_amort_overnight_index_multi_currency_leg(...)`.

Vamos al ejemplo. Primeramente, se da de alta los parámetros requeridos.


```python
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(31, 1, 2024)
fecha_final = qcf.QCDate(31, 1, 2029) 
bus_adj_rule = qcf.BusyAdjRules.NO
index_adj_rule = qcf.BusyAdjRules.MODFOLLOW
periodicidad_pago = qcf.Tenor('6M')
periodo_irregular_pago = qcf.StubPeriod.NO
calendario = qcf.BusinessCalendar(fecha_inicio, 20)
num_decimales_tasa_eq = 8
lag_pago = 0
nominal = 100_000_000.0
amort_es_flujo = True 
spread = .01
gearing = 1.0
interest_rate = qcf.QCInterestRate(0.0, qcf.QCAct360(), qcf.QCLinearWf())
dates_for_eq_rate = qcf.DatesForEquivalentRate.ACCRUAL
nombre_indice = 'ICPCLP'
fx_rate_index_fixing_lag = 2
sett_lag_behaviour = qcf.SettLagBehaviour.MOVE_TO_WORKING_DAY
fx_fixing_lag_pivot = qcf.FxFixingLagPivot.SETTLEMENT_DATE
```

Finalmente, se da de alta el objeto.


```python
on_index_mccy_leg = qcf.LegFactory.build_bullet_overnight_index_multi_currency_leg(
    rec_pay=rp, 
    start_date=fecha_inicio,
    end_date=fecha_final, 
    bus_adj_rule=bus_adj_rule, 
    fix_adj_rule=index_adj_rule,
    settlement_periodicity=periodicidad_pago,
    settlement_stub_period=periodo_irregular_pago, 
    settlement_calendar=calendario, 
    fixing_calendar=calendario,
    settlement_lag=lag_pago,
    initial_notional=nominal, 
    amort_is_cashflow=amort_es_flujo, 
    spread=spread, 
    gearing=gearing,
    interest_rate=interest_rate,
    index_name=nombre_indice,
    eq_rate_decimal_places=num_decimales_tasa_eq,
    notional_currency=clp,
    dates_for_eq_rate=dates_for_eq_rate,
    sett_lag_behaviour=sett_lag_behaviour,
    # Parámetros MultiCurrency
    settlement_currency=usd,
    fx_rate_index=usdclp_obs,
    fx_rate_index_fixing_lag=fx_rate_index_fixing_lag,
    fx_fixing_lag_pivot=fx_fixing_lag_pivot,
    fx_fixing_lag_applies_to=qcf.FxFixingLagAppliesTo.PUBLISHING_DATE,
)
```

Se visualiza.


```python
aux.leg_as_dataframe(on_index_mccy_leg).style.format(aux.format_dict)
```




<style type="text/css">
</style>
<table id="T_4fb11">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_4fb11_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_4fb11_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_4fb11_level0_col2" class="col_heading level0 col2" >fecha_inicial_indice</th>
      <th id="T_4fb11_level0_col3" class="col_heading level0 col3" >fecha_final_indice</th>
      <th id="T_4fb11_level0_col4" class="col_heading level0 col4" >fecha_pago</th>
      <th id="T_4fb11_level0_col5" class="col_heading level0 col5" >nocional</th>
      <th id="T_4fb11_level0_col6" class="col_heading level0 col6" >amortizacion</th>
      <th id="T_4fb11_level0_col7" class="col_heading level0 col7" >amort_es_flujo</th>
      <th id="T_4fb11_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_4fb11_level0_col9" class="col_heading level0 col9" >nombre_indice</th>
      <th id="T_4fb11_level0_col10" class="col_heading level0 col10" >valor_indice_inicial</th>
      <th id="T_4fb11_level0_col11" class="col_heading level0 col11" >valor_indice_final</th>
      <th id="T_4fb11_level0_col12" class="col_heading level0 col12" >valor_tasa</th>
      <th id="T_4fb11_level0_col13" class="col_heading level0 col13" >tipo_tasa</th>
      <th id="T_4fb11_level0_col14" class="col_heading level0 col14" >interes</th>
      <th id="T_4fb11_level0_col15" class="col_heading level0 col15" >flujo</th>
      <th id="T_4fb11_level0_col16" class="col_heading level0 col16" >spread</th>
      <th id="T_4fb11_level0_col17" class="col_heading level0 col17" >gearing</th>
      <th id="T_4fb11_level0_col18" class="col_heading level0 col18" >moneda_pago</th>
      <th id="T_4fb11_level0_col19" class="col_heading level0 col19" >indice_fx</th>
      <th id="T_4fb11_level0_col20" class="col_heading level0 col20" >fecha_fixing_fx</th>
      <th id="T_4fb11_level0_col21" class="col_heading level0 col21" >valor_indice_fx</th>
      <th id="T_4fb11_level0_col22" class="col_heading level0 col22" >interes_moneda_pago</th>
      <th id="T_4fb11_level0_col23" class="col_heading level0 col23" >amortizacion_moneda_pago</th>
      <th id="T_4fb11_level0_col24" class="col_heading level0 col24" >flujo_moneda_pago</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_4fb11_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_4fb11_row0_col0" class="data row0 col0" >2024-01-31</td>
      <td id="T_4fb11_row0_col1" class="data row0 col1" >2024-07-31</td>
      <td id="T_4fb11_row0_col2" class="data row0 col2" >2024-01-31</td>
      <td id="T_4fb11_row0_col3" class="data row0 col3" >2024-07-31</td>
      <td id="T_4fb11_row0_col4" class="data row0 col4" >2024-07-31</td>
      <td id="T_4fb11_row0_col5" class="data row0 col5" >100,000,000.00</td>
      <td id="T_4fb11_row0_col6" class="data row0 col6" >0.00</td>
      <td id="T_4fb11_row0_col7" class="data row0 col7" >True</td>
      <td id="T_4fb11_row0_col8" class="data row0 col8" >CLP</td>
      <td id="T_4fb11_row0_col9" class="data row0 col9" >ICPCLP</td>
      <td id="T_4fb11_row0_col10" class="data row0 col10" >1.000000</td>
      <td id="T_4fb11_row0_col11" class="data row0 col11" >1.000000</td>
      <td id="T_4fb11_row0_col12" class="data row0 col12" >0.0000%</td>
      <td id="T_4fb11_row0_col13" class="data row0 col13" >LinAct360</td>
      <td id="T_4fb11_row0_col14" class="data row0 col14" >505,556.00</td>
      <td id="T_4fb11_row0_col15" class="data row0 col15" >505,556.00</td>
      <td id="T_4fb11_row0_col16" class="data row0 col16" >1.0000%</td>
      <td id="T_4fb11_row0_col17" class="data row0 col17" >1.00</td>
      <td id="T_4fb11_row0_col18" class="data row0 col18" >USD</td>
      <td id="T_4fb11_row0_col19" class="data row0 col19" >USDOBS</td>
      <td id="T_4fb11_row0_col20" class="data row0 col20" >2024-07-29</td>
      <td id="T_4fb11_row0_col21" class="data row0 col21" >1.00</td>
      <td id="T_4fb11_row0_col22" class="data row0 col22" >505,556.00</td>
      <td id="T_4fb11_row0_col23" class="data row0 col23" >0.00</td>
      <td id="T_4fb11_row0_col24" class="data row0 col24" >505,556.00</td>
    </tr>
    <tr>
      <th id="T_4fb11_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_4fb11_row1_col0" class="data row1 col0" >2024-07-31</td>
      <td id="T_4fb11_row1_col1" class="data row1 col1" >2025-01-31</td>
      <td id="T_4fb11_row1_col2" class="data row1 col2" >2024-07-31</td>
      <td id="T_4fb11_row1_col3" class="data row1 col3" >2025-01-31</td>
      <td id="T_4fb11_row1_col4" class="data row1 col4" >2025-01-31</td>
      <td id="T_4fb11_row1_col5" class="data row1 col5" >100,000,000.00</td>
      <td id="T_4fb11_row1_col6" class="data row1 col6" >0.00</td>
      <td id="T_4fb11_row1_col7" class="data row1 col7" >True</td>
      <td id="T_4fb11_row1_col8" class="data row1 col8" >CLP</td>
      <td id="T_4fb11_row1_col9" class="data row1 col9" >ICPCLP</td>
      <td id="T_4fb11_row1_col10" class="data row1 col10" >1.000000</td>
      <td id="T_4fb11_row1_col11" class="data row1 col11" >1.000000</td>
      <td id="T_4fb11_row1_col12" class="data row1 col12" >0.0000%</td>
      <td id="T_4fb11_row1_col13" class="data row1 col13" >LinAct360</td>
      <td id="T_4fb11_row1_col14" class="data row1 col14" >511,111.00</td>
      <td id="T_4fb11_row1_col15" class="data row1 col15" >511,111.00</td>
      <td id="T_4fb11_row1_col16" class="data row1 col16" >1.0000%</td>
      <td id="T_4fb11_row1_col17" class="data row1 col17" >1.00</td>
      <td id="T_4fb11_row1_col18" class="data row1 col18" >USD</td>
      <td id="T_4fb11_row1_col19" class="data row1 col19" >USDOBS</td>
      <td id="T_4fb11_row1_col20" class="data row1 col20" >2025-01-29</td>
      <td id="T_4fb11_row1_col21" class="data row1 col21" >1.00</td>
      <td id="T_4fb11_row1_col22" class="data row1 col22" >511,111.00</td>
      <td id="T_4fb11_row1_col23" class="data row1 col23" >0.00</td>
      <td id="T_4fb11_row1_col24" class="data row1 col24" >511,111.00</td>
    </tr>
    <tr>
      <th id="T_4fb11_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_4fb11_row2_col0" class="data row2 col0" >2025-01-31</td>
      <td id="T_4fb11_row2_col1" class="data row2 col1" >2025-07-31</td>
      <td id="T_4fb11_row2_col2" class="data row2 col2" >2025-01-31</td>
      <td id="T_4fb11_row2_col3" class="data row2 col3" >2025-07-31</td>
      <td id="T_4fb11_row2_col4" class="data row2 col4" >2025-07-31</td>
      <td id="T_4fb11_row2_col5" class="data row2 col5" >100,000,000.00</td>
      <td id="T_4fb11_row2_col6" class="data row2 col6" >0.00</td>
      <td id="T_4fb11_row2_col7" class="data row2 col7" >True</td>
      <td id="T_4fb11_row2_col8" class="data row2 col8" >CLP</td>
      <td id="T_4fb11_row2_col9" class="data row2 col9" >ICPCLP</td>
      <td id="T_4fb11_row2_col10" class="data row2 col10" >1.000000</td>
      <td id="T_4fb11_row2_col11" class="data row2 col11" >1.000000</td>
      <td id="T_4fb11_row2_col12" class="data row2 col12" >0.0000%</td>
      <td id="T_4fb11_row2_col13" class="data row2 col13" >LinAct360</td>
      <td id="T_4fb11_row2_col14" class="data row2 col14" >502,778.00</td>
      <td id="T_4fb11_row2_col15" class="data row2 col15" >502,778.00</td>
      <td id="T_4fb11_row2_col16" class="data row2 col16" >1.0000%</td>
      <td id="T_4fb11_row2_col17" class="data row2 col17" >1.00</td>
      <td id="T_4fb11_row2_col18" class="data row2 col18" >USD</td>
      <td id="T_4fb11_row2_col19" class="data row2 col19" >USDOBS</td>
      <td id="T_4fb11_row2_col20" class="data row2 col20" >2025-07-29</td>
      <td id="T_4fb11_row2_col21" class="data row2 col21" >1.00</td>
      <td id="T_4fb11_row2_col22" class="data row2 col22" >502,778.00</td>
      <td id="T_4fb11_row2_col23" class="data row2 col23" >0.00</td>
      <td id="T_4fb11_row2_col24" class="data row2 col24" >502,778.00</td>
    </tr>
    <tr>
      <th id="T_4fb11_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_4fb11_row3_col0" class="data row3 col0" >2025-07-31</td>
      <td id="T_4fb11_row3_col1" class="data row3 col1" >2026-01-31</td>
      <td id="T_4fb11_row3_col2" class="data row3 col2" >2025-07-31</td>
      <td id="T_4fb11_row3_col3" class="data row3 col3" >2026-01-30</td>
      <td id="T_4fb11_row3_col4" class="data row3 col4" >2026-02-02</td>
      <td id="T_4fb11_row3_col5" class="data row3 col5" >100,000,000.00</td>
      <td id="T_4fb11_row3_col6" class="data row3 col6" >0.00</td>
      <td id="T_4fb11_row3_col7" class="data row3 col7" >True</td>
      <td id="T_4fb11_row3_col8" class="data row3 col8" >CLP</td>
      <td id="T_4fb11_row3_col9" class="data row3 col9" >ICPCLP</td>
      <td id="T_4fb11_row3_col10" class="data row3 col10" >1.000000</td>
      <td id="T_4fb11_row3_col11" class="data row3 col11" >1.000000</td>
      <td id="T_4fb11_row3_col12" class="data row3 col12" >0.0000%</td>
      <td id="T_4fb11_row3_col13" class="data row3 col13" >LinAct360</td>
      <td id="T_4fb11_row3_col14" class="data row3 col14" >511,111.00</td>
      <td id="T_4fb11_row3_col15" class="data row3 col15" >511,111.00</td>
      <td id="T_4fb11_row3_col16" class="data row3 col16" >1.0000%</td>
      <td id="T_4fb11_row3_col17" class="data row3 col17" >1.00</td>
      <td id="T_4fb11_row3_col18" class="data row3 col18" >USD</td>
      <td id="T_4fb11_row3_col19" class="data row3 col19" >USDOBS</td>
      <td id="T_4fb11_row3_col20" class="data row3 col20" >2026-01-29</td>
      <td id="T_4fb11_row3_col21" class="data row3 col21" >1.00</td>
      <td id="T_4fb11_row3_col22" class="data row3 col22" >511,111.00</td>
      <td id="T_4fb11_row3_col23" class="data row3 col23" >0.00</td>
      <td id="T_4fb11_row3_col24" class="data row3 col24" >511,111.00</td>
    </tr>
    <tr>
      <th id="T_4fb11_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_4fb11_row4_col0" class="data row4 col0" >2026-01-31</td>
      <td id="T_4fb11_row4_col1" class="data row4 col1" >2026-07-31</td>
      <td id="T_4fb11_row4_col2" class="data row4 col2" >2026-01-30</td>
      <td id="T_4fb11_row4_col3" class="data row4 col3" >2026-07-31</td>
      <td id="T_4fb11_row4_col4" class="data row4 col4" >2026-07-31</td>
      <td id="T_4fb11_row4_col5" class="data row4 col5" >100,000,000.00</td>
      <td id="T_4fb11_row4_col6" class="data row4 col6" >0.00</td>
      <td id="T_4fb11_row4_col7" class="data row4 col7" >True</td>
      <td id="T_4fb11_row4_col8" class="data row4 col8" >CLP</td>
      <td id="T_4fb11_row4_col9" class="data row4 col9" >ICPCLP</td>
      <td id="T_4fb11_row4_col10" class="data row4 col10" >1.000000</td>
      <td id="T_4fb11_row4_col11" class="data row4 col11" >1.000000</td>
      <td id="T_4fb11_row4_col12" class="data row4 col12" >0.0000%</td>
      <td id="T_4fb11_row4_col13" class="data row4 col13" >LinAct360</td>
      <td id="T_4fb11_row4_col14" class="data row4 col14" >502,778.00</td>
      <td id="T_4fb11_row4_col15" class="data row4 col15" >502,778.00</td>
      <td id="T_4fb11_row4_col16" class="data row4 col16" >1.0000%</td>
      <td id="T_4fb11_row4_col17" class="data row4 col17" >1.00</td>
      <td id="T_4fb11_row4_col18" class="data row4 col18" >USD</td>
      <td id="T_4fb11_row4_col19" class="data row4 col19" >USDOBS</td>
      <td id="T_4fb11_row4_col20" class="data row4 col20" >2026-07-29</td>
      <td id="T_4fb11_row4_col21" class="data row4 col21" >1.00</td>
      <td id="T_4fb11_row4_col22" class="data row4 col22" >502,778.00</td>
      <td id="T_4fb11_row4_col23" class="data row4 col23" >0.00</td>
      <td id="T_4fb11_row4_col24" class="data row4 col24" >502,778.00</td>
    </tr>
    <tr>
      <th id="T_4fb11_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_4fb11_row5_col0" class="data row5 col0" >2026-07-31</td>
      <td id="T_4fb11_row5_col1" class="data row5 col1" >2027-01-31</td>
      <td id="T_4fb11_row5_col2" class="data row5 col2" >2026-07-31</td>
      <td id="T_4fb11_row5_col3" class="data row5 col3" >2027-01-29</td>
      <td id="T_4fb11_row5_col4" class="data row5 col4" >2027-02-01</td>
      <td id="T_4fb11_row5_col5" class="data row5 col5" >100,000,000.00</td>
      <td id="T_4fb11_row5_col6" class="data row5 col6" >0.00</td>
      <td id="T_4fb11_row5_col7" class="data row5 col7" >True</td>
      <td id="T_4fb11_row5_col8" class="data row5 col8" >CLP</td>
      <td id="T_4fb11_row5_col9" class="data row5 col9" >ICPCLP</td>
      <td id="T_4fb11_row5_col10" class="data row5 col10" >1.000000</td>
      <td id="T_4fb11_row5_col11" class="data row5 col11" >1.000000</td>
      <td id="T_4fb11_row5_col12" class="data row5 col12" >0.0000%</td>
      <td id="T_4fb11_row5_col13" class="data row5 col13" >LinAct360</td>
      <td id="T_4fb11_row5_col14" class="data row5 col14" >511,111.00</td>
      <td id="T_4fb11_row5_col15" class="data row5 col15" >511,111.00</td>
      <td id="T_4fb11_row5_col16" class="data row5 col16" >1.0000%</td>
      <td id="T_4fb11_row5_col17" class="data row5 col17" >1.00</td>
      <td id="T_4fb11_row5_col18" class="data row5 col18" >USD</td>
      <td id="T_4fb11_row5_col19" class="data row5 col19" >USDOBS</td>
      <td id="T_4fb11_row5_col20" class="data row5 col20" >2027-01-28</td>
      <td id="T_4fb11_row5_col21" class="data row5 col21" >1.00</td>
      <td id="T_4fb11_row5_col22" class="data row5 col22" >511,111.00</td>
      <td id="T_4fb11_row5_col23" class="data row5 col23" >0.00</td>
      <td id="T_4fb11_row5_col24" class="data row5 col24" >511,111.00</td>
    </tr>
    <tr>
      <th id="T_4fb11_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_4fb11_row6_col0" class="data row6 col0" >2027-01-31</td>
      <td id="T_4fb11_row6_col1" class="data row6 col1" >2027-07-31</td>
      <td id="T_4fb11_row6_col2" class="data row6 col2" >2027-01-29</td>
      <td id="T_4fb11_row6_col3" class="data row6 col3" >2027-07-30</td>
      <td id="T_4fb11_row6_col4" class="data row6 col4" >2027-08-02</td>
      <td id="T_4fb11_row6_col5" class="data row6 col5" >100,000,000.00</td>
      <td id="T_4fb11_row6_col6" class="data row6 col6" >0.00</td>
      <td id="T_4fb11_row6_col7" class="data row6 col7" >True</td>
      <td id="T_4fb11_row6_col8" class="data row6 col8" >CLP</td>
      <td id="T_4fb11_row6_col9" class="data row6 col9" >ICPCLP</td>
      <td id="T_4fb11_row6_col10" class="data row6 col10" >1.000000</td>
      <td id="T_4fb11_row6_col11" class="data row6 col11" >1.000000</td>
      <td id="T_4fb11_row6_col12" class="data row6 col12" >0.0000%</td>
      <td id="T_4fb11_row6_col13" class="data row6 col13" >LinAct360</td>
      <td id="T_4fb11_row6_col14" class="data row6 col14" >502,778.00</td>
      <td id="T_4fb11_row6_col15" class="data row6 col15" >502,778.00</td>
      <td id="T_4fb11_row6_col16" class="data row6 col16" >1.0000%</td>
      <td id="T_4fb11_row6_col17" class="data row6 col17" >1.00</td>
      <td id="T_4fb11_row6_col18" class="data row6 col18" >USD</td>
      <td id="T_4fb11_row6_col19" class="data row6 col19" >USDOBS</td>
      <td id="T_4fb11_row6_col20" class="data row6 col20" >2027-07-29</td>
      <td id="T_4fb11_row6_col21" class="data row6 col21" >1.00</td>
      <td id="T_4fb11_row6_col22" class="data row6 col22" >502,778.00</td>
      <td id="T_4fb11_row6_col23" class="data row6 col23" >0.00</td>
      <td id="T_4fb11_row6_col24" class="data row6 col24" >502,778.00</td>
    </tr>
    <tr>
      <th id="T_4fb11_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_4fb11_row7_col0" class="data row7 col0" >2027-07-31</td>
      <td id="T_4fb11_row7_col1" class="data row7 col1" >2028-01-31</td>
      <td id="T_4fb11_row7_col2" class="data row7 col2" >2027-07-30</td>
      <td id="T_4fb11_row7_col3" class="data row7 col3" >2028-01-31</td>
      <td id="T_4fb11_row7_col4" class="data row7 col4" >2028-01-31</td>
      <td id="T_4fb11_row7_col5" class="data row7 col5" >100,000,000.00</td>
      <td id="T_4fb11_row7_col6" class="data row7 col6" >0.00</td>
      <td id="T_4fb11_row7_col7" class="data row7 col7" >True</td>
      <td id="T_4fb11_row7_col8" class="data row7 col8" >CLP</td>
      <td id="T_4fb11_row7_col9" class="data row7 col9" >ICPCLP</td>
      <td id="T_4fb11_row7_col10" class="data row7 col10" >1.000000</td>
      <td id="T_4fb11_row7_col11" class="data row7 col11" >1.000000</td>
      <td id="T_4fb11_row7_col12" class="data row7 col12" >0.0000%</td>
      <td id="T_4fb11_row7_col13" class="data row7 col13" >LinAct360</td>
      <td id="T_4fb11_row7_col14" class="data row7 col14" >511,111.00</td>
      <td id="T_4fb11_row7_col15" class="data row7 col15" >511,111.00</td>
      <td id="T_4fb11_row7_col16" class="data row7 col16" >1.0000%</td>
      <td id="T_4fb11_row7_col17" class="data row7 col17" >1.00</td>
      <td id="T_4fb11_row7_col18" class="data row7 col18" >USD</td>
      <td id="T_4fb11_row7_col19" class="data row7 col19" >USDOBS</td>
      <td id="T_4fb11_row7_col20" class="data row7 col20" >2028-01-27</td>
      <td id="T_4fb11_row7_col21" class="data row7 col21" >1.00</td>
      <td id="T_4fb11_row7_col22" class="data row7 col22" >511,111.00</td>
      <td id="T_4fb11_row7_col23" class="data row7 col23" >0.00</td>
      <td id="T_4fb11_row7_col24" class="data row7 col24" >511,111.00</td>
    </tr>
    <tr>
      <th id="T_4fb11_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_4fb11_row8_col0" class="data row8 col0" >2028-01-31</td>
      <td id="T_4fb11_row8_col1" class="data row8 col1" >2028-07-31</td>
      <td id="T_4fb11_row8_col2" class="data row8 col2" >2028-01-31</td>
      <td id="T_4fb11_row8_col3" class="data row8 col3" >2028-07-31</td>
      <td id="T_4fb11_row8_col4" class="data row8 col4" >2028-07-31</td>
      <td id="T_4fb11_row8_col5" class="data row8 col5" >100,000,000.00</td>
      <td id="T_4fb11_row8_col6" class="data row8 col6" >0.00</td>
      <td id="T_4fb11_row8_col7" class="data row8 col7" >True</td>
      <td id="T_4fb11_row8_col8" class="data row8 col8" >CLP</td>
      <td id="T_4fb11_row8_col9" class="data row8 col9" >ICPCLP</td>
      <td id="T_4fb11_row8_col10" class="data row8 col10" >1.000000</td>
      <td id="T_4fb11_row8_col11" class="data row8 col11" >1.000000</td>
      <td id="T_4fb11_row8_col12" class="data row8 col12" >0.0000%</td>
      <td id="T_4fb11_row8_col13" class="data row8 col13" >LinAct360</td>
      <td id="T_4fb11_row8_col14" class="data row8 col14" >505,556.00</td>
      <td id="T_4fb11_row8_col15" class="data row8 col15" >505,556.00</td>
      <td id="T_4fb11_row8_col16" class="data row8 col16" >1.0000%</td>
      <td id="T_4fb11_row8_col17" class="data row8 col17" >1.00</td>
      <td id="T_4fb11_row8_col18" class="data row8 col18" >USD</td>
      <td id="T_4fb11_row8_col19" class="data row8 col19" >USDOBS</td>
      <td id="T_4fb11_row8_col20" class="data row8 col20" >2028-07-27</td>
      <td id="T_4fb11_row8_col21" class="data row8 col21" >1.00</td>
      <td id="T_4fb11_row8_col22" class="data row8 col22" >505,556.00</td>
      <td id="T_4fb11_row8_col23" class="data row8 col23" >0.00</td>
      <td id="T_4fb11_row8_col24" class="data row8 col24" >505,556.00</td>
    </tr>
    <tr>
      <th id="T_4fb11_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_4fb11_row9_col0" class="data row9 col0" >2028-07-31</td>
      <td id="T_4fb11_row9_col1" class="data row9 col1" >2029-01-31</td>
      <td id="T_4fb11_row9_col2" class="data row9 col2" >2028-07-31</td>
      <td id="T_4fb11_row9_col3" class="data row9 col3" >2029-01-31</td>
      <td id="T_4fb11_row9_col4" class="data row9 col4" >2029-01-31</td>
      <td id="T_4fb11_row9_col5" class="data row9 col5" >100,000,000.00</td>
      <td id="T_4fb11_row9_col6" class="data row9 col6" >100,000,000.00</td>
      <td id="T_4fb11_row9_col7" class="data row9 col7" >True</td>
      <td id="T_4fb11_row9_col8" class="data row9 col8" >CLP</td>
      <td id="T_4fb11_row9_col9" class="data row9 col9" >ICPCLP</td>
      <td id="T_4fb11_row9_col10" class="data row9 col10" >1.000000</td>
      <td id="T_4fb11_row9_col11" class="data row9 col11" >1.000000</td>
      <td id="T_4fb11_row9_col12" class="data row9 col12" >0.0000%</td>
      <td id="T_4fb11_row9_col13" class="data row9 col13" >LinAct360</td>
      <td id="T_4fb11_row9_col14" class="data row9 col14" >511,111.00</td>
      <td id="T_4fb11_row9_col15" class="data row9 col15" >100,511,111.00</td>
      <td id="T_4fb11_row9_col16" class="data row9 col16" >1.0000%</td>
      <td id="T_4fb11_row9_col17" class="data row9 col17" >1.00</td>
      <td id="T_4fb11_row9_col18" class="data row9 col18" >USD</td>
      <td id="T_4fb11_row9_col19" class="data row9 col19" >USDOBS</td>
      <td id="T_4fb11_row9_col20" class="data row9 col20" >2029-01-29</td>
      <td id="T_4fb11_row9_col21" class="data row9 col21" >1.00</td>
      <td id="T_4fb11_row9_col22" class="data row9 col22" >511,111.00</td>
      <td id="T_4fb11_row9_col23" class="data row9 col23" >100,000,000.00</td>
      <td id="T_4fb11_row9_col24" class="data row9 col24" >100,511,111.00</td>
    </tr>
  </tbody>
</table>




## Construcción Asistida de un `CompoundedOvernightRateLeg`

En este ejemplo se construye un `Leg` con `CompoundedOvernightRateCashflow2` y amortización bullet.
Se requieren los siguientes parámetros:

- `RecPay`: enum que indica si los flujos se reciben o pagan
- `QCDate`: fecha de inicio del primer flujo
- `QCDate`: fecha final del último flujo sin considerar ajustes de días feriados
- `BusyAdRules`: enum que representa el tipo de ajuste en la fecha final para días feriados
- `Tenor`: la periodicidad de pago
- `QCInterestRateLeg::QCStubPeriod`: enum que representa el tipo de período irregular (si aplica)
- `QCBusinessCalendar`: calendario que aplica para las fechas de pago
- `unsigned int`: lag de pago expresado en días
- `QCBusinessCalendar`: calendario que aplica para las fechas de fijación de la tasa overnight
- `QCInterestRateIndex`: índice overnight a utilizar
- `float`: nominal
- `bool`: si es `True` significa que la amortización final es un flujo de caja efectivo
- `QCCurrency`: moneda del nocional
- `float`: spread aditivo
- `float`: spread multiplicativo o gearing (tasa * gearing + spread)
- `QCInterestRate`: representa el tipo de tasa que se usará que se usará para la tasa equivalente
- `unsigned int`: número de decimales de la tasa equivalente
- `unsigned int`: lookback (no implementado)
- `unsigned int`: lockout (no implementado)
- `SettLagBehaviour`: este parámetro indica cómo se calcula un `settlement_date` cuando un `end_date` cae en un día festivo.

**NOTA:** para construir un `Leg` con `CompoundedOvernightRateCashflow` y amortización customizada, sólo se debe cambiar el parámetro **nominal** por **CustomNotionalAndAmort** e invocar el método `qcf.LegFactory.build_custom_amort_compounded_overnight_rate_leg_2(...)`.

Vamos al ejemplo. Primeramente, se da de alta los parámetros requeridos


```python
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(31, 1, 2024)
fecha_final = qcf.QCDate(31, 1, 2028)
bus_adj_rule = qcf.BusyAdjRules.MODFOLLOW
periodicidad_pago = qcf.Tenor('1Y')
periodo_irregular_pago = qcf.StubPeriod.NO
calendario = aux.get_business_calendar('US', range(2024, 2035))
lag_pago = 2
nominal = 10_000_000.0
amort_es_flujo = True
moneda = usd
spread = .01
gearing = 1.0
eq_rate_decimal_places = 8
lookback = 0 
lockout = 0
sett_lag_behaviour = qcf.SettLagBehaviour.MOVE_TO_WORKING_DAY
```

Se define el índice.


```python
codigo = 'SOFRRATE'
lin_act360 = qcf.QCInterestRate(.0, qcf.QCAct360(), qcf.QCLinearWf())
fixing_lag = qcf.Tenor('0d')
tenor = qcf.Tenor('1d')
fixing_calendar = calendario
settlement_calendar = calendario
usd = qcf.QCUSD()
oistest = qcf.InterestRateIndex(
    codigo,
    lin_act360,
    fixing_lag,
    tenor,
    fixing_calendar,
    settlement_calendar,
    usd
)
```

Finalmente, se da de alta el objeto.


```python
cor_leg = qcf.LegFactory.build_bullet_compounded_overnight_rate_leg_2(
    rec_pay=rp,
    start_date=fecha_inicio,
    end_date=fecha_final,
    bus_adj_rule=bus_adj_rule,
    settlement_periodicity=periodicidad_pago,
    settlement_stub_period=periodo_irregular_pago,
    settlement_calendar=calendario,
    settlement_lag=lag_pago,
    fixing_calendar=calendario,
    interest_rate_index=oistest,
    initial_notional=nominal,
    amort_is_cashflow=amort_es_flujo,
    notional_currency=usd,
    spread=spread,
    gearing=gearing,
    interest_rate=lin_act360,
    eq_rate_decimal_places=8,
    lookback=lookback,
    lockout=lockout,
    sett_lag_behaviour=sett_lag_behaviour,
)
```


```python
aux.leg_as_dataframe(cor_leg).style.format(aux.format_dict)
```




<style type="text/css">
</style>
<table id="T_3a07c">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_3a07c_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_3a07c_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_3a07c_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_3a07c_level0_col3" class="col_heading level0 col3" >nocional</th>
      <th id="T_3a07c_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_3a07c_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_3a07c_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_3a07c_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_3a07c_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_3a07c_level0_col9" class="col_heading level0 col9" >codigo_indice_tasa</th>
      <th id="T_3a07c_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
      <th id="T_3a07c_level0_col11" class="col_heading level0 col11" >valor_tasa</th>
      <th id="T_3a07c_level0_col12" class="col_heading level0 col12" >spread</th>
      <th id="T_3a07c_level0_col13" class="col_heading level0 col13" >gearing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_3a07c_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_3a07c_row0_col0" class="data row0 col0" >2024-01-31</td>
      <td id="T_3a07c_row0_col1" class="data row0 col1" >2025-01-31</td>
      <td id="T_3a07c_row0_col2" class="data row0 col2" >2025-02-04</td>
      <td id="T_3a07c_row0_col3" class="data row0 col3" >10,000,000.00</td>
      <td id="T_3a07c_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_3a07c_row0_col5" class="data row0 col5" >101,666.67</td>
      <td id="T_3a07c_row0_col6" class="data row0 col6" >True</td>
      <td id="T_3a07c_row0_col7" class="data row0 col7" >101,666.67</td>
      <td id="T_3a07c_row0_col8" class="data row0 col8" >USD</td>
      <td id="T_3a07c_row0_col9" class="data row0 col9" >SOFRRATE</td>
      <td id="T_3a07c_row0_col10" class="data row0 col10" >LinAct360</td>
      <td id="T_3a07c_row0_col11" class="data row0 col11" >0.0000%</td>
      <td id="T_3a07c_row0_col12" class="data row0 col12" >1.0000%</td>
      <td id="T_3a07c_row0_col13" class="data row0 col13" >1.00</td>
    </tr>
    <tr>
      <th id="T_3a07c_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_3a07c_row1_col0" class="data row1 col0" >2025-01-31</td>
      <td id="T_3a07c_row1_col1" class="data row1 col1" >2026-01-30</td>
      <td id="T_3a07c_row1_col2" class="data row1 col2" >2026-02-03</td>
      <td id="T_3a07c_row1_col3" class="data row1 col3" >10,000,000.00</td>
      <td id="T_3a07c_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_3a07c_row1_col5" class="data row1 col5" >101,111.11</td>
      <td id="T_3a07c_row1_col6" class="data row1 col6" >True</td>
      <td id="T_3a07c_row1_col7" class="data row1 col7" >101,111.11</td>
      <td id="T_3a07c_row1_col8" class="data row1 col8" >USD</td>
      <td id="T_3a07c_row1_col9" class="data row1 col9" >SOFRRATE</td>
      <td id="T_3a07c_row1_col10" class="data row1 col10" >LinAct360</td>
      <td id="T_3a07c_row1_col11" class="data row1 col11" >0.0000%</td>
      <td id="T_3a07c_row1_col12" class="data row1 col12" >1.0000%</td>
      <td id="T_3a07c_row1_col13" class="data row1 col13" >1.00</td>
    </tr>
    <tr>
      <th id="T_3a07c_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_3a07c_row2_col0" class="data row2 col0" >2026-01-30</td>
      <td id="T_3a07c_row2_col1" class="data row2 col1" >2027-01-29</td>
      <td id="T_3a07c_row2_col2" class="data row2 col2" >2027-02-02</td>
      <td id="T_3a07c_row2_col3" class="data row2 col3" >10,000,000.00</td>
      <td id="T_3a07c_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_3a07c_row2_col5" class="data row2 col5" >101,111.11</td>
      <td id="T_3a07c_row2_col6" class="data row2 col6" >True</td>
      <td id="T_3a07c_row2_col7" class="data row2 col7" >101,111.11</td>
      <td id="T_3a07c_row2_col8" class="data row2 col8" >USD</td>
      <td id="T_3a07c_row2_col9" class="data row2 col9" >SOFRRATE</td>
      <td id="T_3a07c_row2_col10" class="data row2 col10" >LinAct360</td>
      <td id="T_3a07c_row2_col11" class="data row2 col11" >0.0000%</td>
      <td id="T_3a07c_row2_col12" class="data row2 col12" >1.0000%</td>
      <td id="T_3a07c_row2_col13" class="data row2 col13" >1.00</td>
    </tr>
    <tr>
      <th id="T_3a07c_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_3a07c_row3_col0" class="data row3 col0" >2027-01-29</td>
      <td id="T_3a07c_row3_col1" class="data row3 col1" >2028-01-31</td>
      <td id="T_3a07c_row3_col2" class="data row3 col2" >2028-02-02</td>
      <td id="T_3a07c_row3_col3" class="data row3 col3" >10,000,000.00</td>
      <td id="T_3a07c_row3_col4" class="data row3 col4" >10,000,000.00</td>
      <td id="T_3a07c_row3_col5" class="data row3 col5" >101,944.44</td>
      <td id="T_3a07c_row3_col6" class="data row3 col6" >True</td>
      <td id="T_3a07c_row3_col7" class="data row3 col7" >10,101,944.44</td>
      <td id="T_3a07c_row3_col8" class="data row3 col8" >USD</td>
      <td id="T_3a07c_row3_col9" class="data row3 col9" >SOFRRATE</td>
      <td id="T_3a07c_row3_col10" class="data row3 col10" >LinAct360</td>
      <td id="T_3a07c_row3_col11" class="data row3 col11" >0.0000%</td>
      <td id="T_3a07c_row3_col12" class="data row3 col12" >1.0000%</td>
      <td id="T_3a07c_row3_col13" class="data row3 col13" >1.00</td>
    </tr>
  </tbody>
</table>




## Construcción Asistida de un `CompoundedOvernightRateMultiCurrencyLeg`

En este ejemplo se construye un `Leg` con `CompoundedOvernightRateMultiCurrencyCashflow2` y amortización bullet.
Se requieren los siguientes parámetros:

- `RecPay`: enum que indica si los flujos se reciben o pagan
- `QCDate`: fecha de inicio del primer flujo
- `QCDate`: fecha final del último flujo sin considerar ajustes de días feriados
- `BusyAdRules`: enum que representa el tipo de ajuste en la fecha final para días feriados
- `Tenor`: la periodicidad de pago
- `QCInterestRateLeg::QCStubPeriod`: enum que representa el tipo de período irregular (si aplica)
- `QCBusinessCalendar`: calendario que aplica para las fechas de pago
- `unsigned int`: lag de pago expresado en días
- `QCBusinessCalendar`: calendario que aplica para las fechas de fijación de la tasa overnight
- `QCInterestRateIndex`: índice overnight a utilizar
- `float`: nominal
- `bool`: si es `True` significa que la amortización final es un flujo de caja efectivo
- `QCCurrency`: moneda del nocional
- `float`: spread aditivo
- `float`: spread multiplicativo
- `QCInterestRate`: representa el tipo de tasa que se usará que se usará para la tasa equivalente
- `unsigned int`: número de decimales de la tasa equivalente
- `unsigned int`: lookback (no implementado)
- `unsigned int`: lockout (no implementado)
- `SettLagBehaviour`: este parámetro indica cómo se calcula un `settlement_date` cuando un `end_date` cae en un día festivo.
---
**MultiCurrency**
- `QCCurrency`: moneda de pago los flujos
- `FXRateIndex`: índice con el cual se transforma cada flujo a la moneda de pago
- `int`: lag de fijación del FXRateIndex (respecto a settlement date)
- `FxFixingLagPivot`: este parámetro indica si el lag de fijación del índice FX se aplica sobre `end_date` o sobre `settlement_date`.
- `FxFixingLagAppliesTo`: indica si el lag se refiere a `FIXING_DATE` o `PUBISHING_DATE` del índice.

**NOTA:** para construir un `Leg` con `CompoundedOvernightRateMultiCurrencyCashflow` y amortización customizada, sólo se debe cambiar el parámetro **nominal** por **CustomNotionalAndAmort** e invocar el método `qcf.LegFactory.build_custom_amort_compounded_overnight_rate_multi_currency_leg_2(...)`.

Vamos al ejemplo. Primeramente, se da de alta los parámetros requeridos


```python
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(31, 1, 2024)
fecha_final = qcf.QCDate(31, 1, 2028)
bus_adj_rule = qcf.BusyAdjRules.NO
periodicidad_pago = qcf.Tenor('6M')
periodo_irregular_pago = qcf.StubPeriod.NO
calendario = qcf.BusinessCalendar(fecha_inicio, 20)
lag_pago = 2
nominal = 1000000.0
amort_es_flujo = True
moneda = usd
spread = .01
gearing = 1.0
eq_rate_decimal_places = 8
lookback = 0
lockout = 0
fx_rate_index_fixing_lag = 1
sett_lag_behaviour = qcf.SettLagBehaviour.MOVE_TO_WORKING_DAY
fx_fixing_lag_pivot = qcf.FxFixingLagPivot.SETTLEMENT_DATE
```

Se define el índice.


```python
codigo = 'OISTEST'
lin_act360 = qcf.QCInterestRate(.0, qcf.QCAct360(), qcf.QCLinearWf())
fixing_lag = qcf.Tenor('0d')
tenor = qcf.Tenor('1d')
fixing_calendar = calendario
settlement_calendar = calendario
usd = qcf.QCUSD()
oistest = qcf.InterestRateIndex(
    codigo,
    lin_act360,
    fixing_lag,
    tenor,
    fixing_calendar,
    settlement_calendar,
    usd
)
```

Finalmente, se da de alta el objeto.


```python
cor_mccy_leg = qcf.LegFactory.build_bullet_compounded_overnight_rate_mccy_leg_2(
    rec_pay=rp,
    start_date=fecha_inicio,
    end_date=fecha_final,
    bus_adj_rule=bus_adj_rule,
    settlement_periodicity=periodicidad_pago,
    settlement_stub_period=periodo_irregular_pago,
    settlement_calendar=calendario,
    settlement_lag=lag_pago,
    fixing_calendar=calendario,
    interest_rate_index=oistest,
    initial_notional=nominal,
    amort_is_cashflow=amort_es_flujo,
    notional_currency=usd,
    spread=spread,
    gearing=gearing,
    interest_rate=lin_act360,
    eq_rate_decimal_places=8,
    lookback=lookback,
    lockout=lockout,
    sett_lag_behaviour=sett_lag_behaviour,
    # Parámetros MultiCurrency
    fx_rate_index_fixing_lag=fx_rate_index_fixing_lag,
    settlement_currency=usd,
    fx_rate_index=usdclp_obs,
    fx_fixing_lag_pivot=fx_fixing_lag_pivot,
    fx_fixing_lag_applies_to=qcf.FxFixingLagAppliesTo.FIXING_DATE,
)
```


```python
aux.leg_as_dataframe(cor_mccy_leg).style.format(aux.format_dict)
```




<style type="text/css">
</style>
<table id="T_369c3">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_369c3_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_369c3_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_369c3_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_369c3_level0_col3" class="col_heading level0 col3" >nocional</th>
      <th id="T_369c3_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_369c3_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_369c3_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_369c3_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_369c3_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_369c3_level0_col9" class="col_heading level0 col9" >codigo_indice_tasa</th>
      <th id="T_369c3_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
      <th id="T_369c3_level0_col11" class="col_heading level0 col11" >spread</th>
      <th id="T_369c3_level0_col12" class="col_heading level0 col12" >gearing</th>
      <th id="T_369c3_level0_col13" class="col_heading level0 col13" >valor_tasa</th>
      <th id="T_369c3_level0_col14" class="col_heading level0 col14" >moneda_pago</th>
      <th id="T_369c3_level0_col15" class="col_heading level0 col15" >fx_rate_index</th>
      <th id="T_369c3_level0_col16" class="col_heading level0 col16" >fecha_fixing_fx</th>
      <th id="T_369c3_level0_col17" class="col_heading level0 col17" >valor_indice_fx</th>
      <th id="T_369c3_level0_col18" class="col_heading level0 col18" >interes_moneda_pago</th>
      <th id="T_369c3_level0_col19" class="col_heading level0 col19" >amortizacion_moneda_pago</th>
      <th id="T_369c3_level0_col20" class="col_heading level0 col20" >flujo_moneda_pago</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_369c3_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_369c3_row0_col0" class="data row0 col0" >2024-01-31</td>
      <td id="T_369c3_row0_col1" class="data row0 col1" >2024-07-31</td>
      <td id="T_369c3_row0_col2" class="data row0 col2" >2024-08-02</td>
      <td id="T_369c3_row0_col3" class="data row0 col3" >1,000,000.00</td>
      <td id="T_369c3_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_369c3_row0_col5" class="data row0 col5" >5,055.56</td>
      <td id="T_369c3_row0_col6" class="data row0 col6" >True</td>
      <td id="T_369c3_row0_col7" class="data row0 col7" >5,055.56</td>
      <td id="T_369c3_row0_col8" class="data row0 col8" >USD</td>
      <td id="T_369c3_row0_col9" class="data row0 col9" >OISTEST</td>
      <td id="T_369c3_row0_col10" class="data row0 col10" >LinAct360</td>
      <td id="T_369c3_row0_col11" class="data row0 col11" >1.0000%</td>
      <td id="T_369c3_row0_col12" class="data row0 col12" >1.00</td>
      <td id="T_369c3_row0_col13" class="data row0 col13" >0.0000%</td>
      <td id="T_369c3_row0_col14" class="data row0 col14" >USD</td>
      <td id="T_369c3_row0_col15" class="data row0 col15" >USDOBS</td>
      <td id="T_369c3_row0_col16" class="data row0 col16" >2024-08-02</td>
      <td id="T_369c3_row0_col17" class="data row0 col17" >1.00</td>
      <td id="T_369c3_row0_col18" class="data row0 col18" >5,055.56</td>
      <td id="T_369c3_row0_col19" class="data row0 col19" >0.00</td>
      <td id="T_369c3_row0_col20" class="data row0 col20" >5,055.56</td>
    </tr>
    <tr>
      <th id="T_369c3_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_369c3_row1_col0" class="data row1 col0" >2024-07-31</td>
      <td id="T_369c3_row1_col1" class="data row1 col1" >2025-01-31</td>
      <td id="T_369c3_row1_col2" class="data row1 col2" >2025-02-04</td>
      <td id="T_369c3_row1_col3" class="data row1 col3" >1,000,000.00</td>
      <td id="T_369c3_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_369c3_row1_col5" class="data row1 col5" >5,111.11</td>
      <td id="T_369c3_row1_col6" class="data row1 col6" >True</td>
      <td id="T_369c3_row1_col7" class="data row1 col7" >5,111.11</td>
      <td id="T_369c3_row1_col8" class="data row1 col8" >USD</td>
      <td id="T_369c3_row1_col9" class="data row1 col9" >OISTEST</td>
      <td id="T_369c3_row1_col10" class="data row1 col10" >LinAct360</td>
      <td id="T_369c3_row1_col11" class="data row1 col11" >1.0000%</td>
      <td id="T_369c3_row1_col12" class="data row1 col12" >1.00</td>
      <td id="T_369c3_row1_col13" class="data row1 col13" >0.0000%</td>
      <td id="T_369c3_row1_col14" class="data row1 col14" >USD</td>
      <td id="T_369c3_row1_col15" class="data row1 col15" >USDOBS</td>
      <td id="T_369c3_row1_col16" class="data row1 col16" >2025-02-04</td>
      <td id="T_369c3_row1_col17" class="data row1 col17" >1.00</td>
      <td id="T_369c3_row1_col18" class="data row1 col18" >5,111.11</td>
      <td id="T_369c3_row1_col19" class="data row1 col19" >0.00</td>
      <td id="T_369c3_row1_col20" class="data row1 col20" >5,111.11</td>
    </tr>
    <tr>
      <th id="T_369c3_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_369c3_row2_col0" class="data row2 col0" >2025-01-31</td>
      <td id="T_369c3_row2_col1" class="data row2 col1" >2025-07-31</td>
      <td id="T_369c3_row2_col2" class="data row2 col2" >2025-08-04</td>
      <td id="T_369c3_row2_col3" class="data row2 col3" >1,000,000.00</td>
      <td id="T_369c3_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_369c3_row2_col5" class="data row2 col5" >5,027.78</td>
      <td id="T_369c3_row2_col6" class="data row2 col6" >True</td>
      <td id="T_369c3_row2_col7" class="data row2 col7" >5,027.78</td>
      <td id="T_369c3_row2_col8" class="data row2 col8" >USD</td>
      <td id="T_369c3_row2_col9" class="data row2 col9" >OISTEST</td>
      <td id="T_369c3_row2_col10" class="data row2 col10" >LinAct360</td>
      <td id="T_369c3_row2_col11" class="data row2 col11" >1.0000%</td>
      <td id="T_369c3_row2_col12" class="data row2 col12" >1.00</td>
      <td id="T_369c3_row2_col13" class="data row2 col13" >0.0000%</td>
      <td id="T_369c3_row2_col14" class="data row2 col14" >USD</td>
      <td id="T_369c3_row2_col15" class="data row2 col15" >USDOBS</td>
      <td id="T_369c3_row2_col16" class="data row2 col16" >2025-08-04</td>
      <td id="T_369c3_row2_col17" class="data row2 col17" >1.00</td>
      <td id="T_369c3_row2_col18" class="data row2 col18" >5,027.78</td>
      <td id="T_369c3_row2_col19" class="data row2 col19" >0.00</td>
      <td id="T_369c3_row2_col20" class="data row2 col20" >5,027.78</td>
    </tr>
    <tr>
      <th id="T_369c3_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_369c3_row3_col0" class="data row3 col0" >2025-07-31</td>
      <td id="T_369c3_row3_col1" class="data row3 col1" >2026-01-31</td>
      <td id="T_369c3_row3_col2" class="data row3 col2" >2026-02-04</td>
      <td id="T_369c3_row3_col3" class="data row3 col3" >1,000,000.00</td>
      <td id="T_369c3_row3_col4" class="data row3 col4" >0.00</td>
      <td id="T_369c3_row3_col5" class="data row3 col5" >5,111.11</td>
      <td id="T_369c3_row3_col6" class="data row3 col6" >True</td>
      <td id="T_369c3_row3_col7" class="data row3 col7" >5,111.11</td>
      <td id="T_369c3_row3_col8" class="data row3 col8" >USD</td>
      <td id="T_369c3_row3_col9" class="data row3 col9" >OISTEST</td>
      <td id="T_369c3_row3_col10" class="data row3 col10" >LinAct360</td>
      <td id="T_369c3_row3_col11" class="data row3 col11" >1.0000%</td>
      <td id="T_369c3_row3_col12" class="data row3 col12" >1.00</td>
      <td id="T_369c3_row3_col13" class="data row3 col13" >0.0000%</td>
      <td id="T_369c3_row3_col14" class="data row3 col14" >USD</td>
      <td id="T_369c3_row3_col15" class="data row3 col15" >USDOBS</td>
      <td id="T_369c3_row3_col16" class="data row3 col16" >2026-02-04</td>
      <td id="T_369c3_row3_col17" class="data row3 col17" >1.00</td>
      <td id="T_369c3_row3_col18" class="data row3 col18" >5,111.11</td>
      <td id="T_369c3_row3_col19" class="data row3 col19" >0.00</td>
      <td id="T_369c3_row3_col20" class="data row3 col20" >5,111.11</td>
    </tr>
    <tr>
      <th id="T_369c3_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_369c3_row4_col0" class="data row4 col0" >2026-01-31</td>
      <td id="T_369c3_row4_col1" class="data row4 col1" >2026-07-31</td>
      <td id="T_369c3_row4_col2" class="data row4 col2" >2026-08-04</td>
      <td id="T_369c3_row4_col3" class="data row4 col3" >1,000,000.00</td>
      <td id="T_369c3_row4_col4" class="data row4 col4" >0.00</td>
      <td id="T_369c3_row4_col5" class="data row4 col5" >5,027.78</td>
      <td id="T_369c3_row4_col6" class="data row4 col6" >True</td>
      <td id="T_369c3_row4_col7" class="data row4 col7" >5,027.78</td>
      <td id="T_369c3_row4_col8" class="data row4 col8" >USD</td>
      <td id="T_369c3_row4_col9" class="data row4 col9" >OISTEST</td>
      <td id="T_369c3_row4_col10" class="data row4 col10" >LinAct360</td>
      <td id="T_369c3_row4_col11" class="data row4 col11" >1.0000%</td>
      <td id="T_369c3_row4_col12" class="data row4 col12" >1.00</td>
      <td id="T_369c3_row4_col13" class="data row4 col13" >0.0000%</td>
      <td id="T_369c3_row4_col14" class="data row4 col14" >USD</td>
      <td id="T_369c3_row4_col15" class="data row4 col15" >USDOBS</td>
      <td id="T_369c3_row4_col16" class="data row4 col16" >2026-08-04</td>
      <td id="T_369c3_row4_col17" class="data row4 col17" >1.00</td>
      <td id="T_369c3_row4_col18" class="data row4 col18" >5,027.78</td>
      <td id="T_369c3_row4_col19" class="data row4 col19" >0.00</td>
      <td id="T_369c3_row4_col20" class="data row4 col20" >5,027.78</td>
    </tr>
    <tr>
      <th id="T_369c3_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_369c3_row5_col0" class="data row5 col0" >2026-07-31</td>
      <td id="T_369c3_row5_col1" class="data row5 col1" >2027-01-31</td>
      <td id="T_369c3_row5_col2" class="data row5 col2" >2027-02-03</td>
      <td id="T_369c3_row5_col3" class="data row5 col3" >1,000,000.00</td>
      <td id="T_369c3_row5_col4" class="data row5 col4" >0.00</td>
      <td id="T_369c3_row5_col5" class="data row5 col5" >5,111.11</td>
      <td id="T_369c3_row5_col6" class="data row5 col6" >True</td>
      <td id="T_369c3_row5_col7" class="data row5 col7" >5,111.11</td>
      <td id="T_369c3_row5_col8" class="data row5 col8" >USD</td>
      <td id="T_369c3_row5_col9" class="data row5 col9" >OISTEST</td>
      <td id="T_369c3_row5_col10" class="data row5 col10" >LinAct360</td>
      <td id="T_369c3_row5_col11" class="data row5 col11" >1.0000%</td>
      <td id="T_369c3_row5_col12" class="data row5 col12" >1.00</td>
      <td id="T_369c3_row5_col13" class="data row5 col13" >0.0000%</td>
      <td id="T_369c3_row5_col14" class="data row5 col14" >USD</td>
      <td id="T_369c3_row5_col15" class="data row5 col15" >USDOBS</td>
      <td id="T_369c3_row5_col16" class="data row5 col16" >2027-02-03</td>
      <td id="T_369c3_row5_col17" class="data row5 col17" >1.00</td>
      <td id="T_369c3_row5_col18" class="data row5 col18" >5,111.11</td>
      <td id="T_369c3_row5_col19" class="data row5 col19" >0.00</td>
      <td id="T_369c3_row5_col20" class="data row5 col20" >5,111.11</td>
    </tr>
    <tr>
      <th id="T_369c3_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_369c3_row6_col0" class="data row6 col0" >2027-01-31</td>
      <td id="T_369c3_row6_col1" class="data row6 col1" >2027-07-31</td>
      <td id="T_369c3_row6_col2" class="data row6 col2" >2027-08-04</td>
      <td id="T_369c3_row6_col3" class="data row6 col3" >1,000,000.00</td>
      <td id="T_369c3_row6_col4" class="data row6 col4" >0.00</td>
      <td id="T_369c3_row6_col5" class="data row6 col5" >5,027.78</td>
      <td id="T_369c3_row6_col6" class="data row6 col6" >True</td>
      <td id="T_369c3_row6_col7" class="data row6 col7" >5,027.78</td>
      <td id="T_369c3_row6_col8" class="data row6 col8" >USD</td>
      <td id="T_369c3_row6_col9" class="data row6 col9" >OISTEST</td>
      <td id="T_369c3_row6_col10" class="data row6 col10" >LinAct360</td>
      <td id="T_369c3_row6_col11" class="data row6 col11" >1.0000%</td>
      <td id="T_369c3_row6_col12" class="data row6 col12" >1.00</td>
      <td id="T_369c3_row6_col13" class="data row6 col13" >0.0000%</td>
      <td id="T_369c3_row6_col14" class="data row6 col14" >USD</td>
      <td id="T_369c3_row6_col15" class="data row6 col15" >USDOBS</td>
      <td id="T_369c3_row6_col16" class="data row6 col16" >2027-08-04</td>
      <td id="T_369c3_row6_col17" class="data row6 col17" >1.00</td>
      <td id="T_369c3_row6_col18" class="data row6 col18" >5,027.78</td>
      <td id="T_369c3_row6_col19" class="data row6 col19" >0.00</td>
      <td id="T_369c3_row6_col20" class="data row6 col20" >5,027.78</td>
    </tr>
    <tr>
      <th id="T_369c3_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_369c3_row7_col0" class="data row7 col0" >2027-07-31</td>
      <td id="T_369c3_row7_col1" class="data row7 col1" >2028-01-31</td>
      <td id="T_369c3_row7_col2" class="data row7 col2" >2028-02-02</td>
      <td id="T_369c3_row7_col3" class="data row7 col3" >1,000,000.00</td>
      <td id="T_369c3_row7_col4" class="data row7 col4" >1,000,000.00</td>
      <td id="T_369c3_row7_col5" class="data row7 col5" >5,111.11</td>
      <td id="T_369c3_row7_col6" class="data row7 col6" >True</td>
      <td id="T_369c3_row7_col7" class="data row7 col7" >1,005,111.11</td>
      <td id="T_369c3_row7_col8" class="data row7 col8" >USD</td>
      <td id="T_369c3_row7_col9" class="data row7 col9" >OISTEST</td>
      <td id="T_369c3_row7_col10" class="data row7 col10" >LinAct360</td>
      <td id="T_369c3_row7_col11" class="data row7 col11" >1.0000%</td>
      <td id="T_369c3_row7_col12" class="data row7 col12" >1.00</td>
      <td id="T_369c3_row7_col13" class="data row7 col13" >0.0000%</td>
      <td id="T_369c3_row7_col14" class="data row7 col14" >USD</td>
      <td id="T_369c3_row7_col15" class="data row7 col15" >USDOBS</td>
      <td id="T_369c3_row7_col16" class="data row7 col16" >2028-02-02</td>
      <td id="T_369c3_row7_col17" class="data row7 col17" >1.00</td>
      <td id="T_369c3_row7_col18" class="data row7 col18" >5,111.11</td>
      <td id="T_369c3_row7_col19" class="data row7 col19" >1,000,000.00</td>
      <td id="T_369c3_row7_col20" class="data row7 col20" >1,005,111.11</td>
    </tr>
  </tbody>
</table>




## Construcción Asistida de un `IcpClfLeg`
En este ejemplo se construye un `Leg` con `IcpClfCashflow` y amortización bullet.
Se requieren los siguientes parámetros:

- `RecPay`: enum que indica si los flujos se reciben o pagan
- `QCDate`: fecha de inicio del primer flujo
- `QCDate`: fecha final del último flujo sin considerar ajustes de días feriados
- `BusyAdRules`: enum que representa el tipo de ajuste en la fecha final para días feriados
- `Tenor`: la periodicidad de pago
- `QCInterestRateLeg::QCStubPeriod`: enum que representa el tipo de período irregular (si aplica)
- `QCBusinessCalendar`: calendario que aplica para las fechas de pago
- `unsigned int`: lag de pago expresado en días
- `float`: nominal
- `bool`: si es `True` significa que la amortización final es un flujo de caja efectivo
- `float`: spread aditivo
- `gearing`: spread multiplicativo o gearing (tasa * geraing + spread)

**NOTA:** para construir un `Leg` con `IcpClfCashflow` y amortización customizada, sólo se debe cambiar el parámetro **nominal** por **CustomNotionalAndAmort** e invocar el método `qcf.LegFactory.build_custom_amort_icp_clf_leg(...)`.

Vamos al ejemplo.

Se da de alta los parámetros requeridos


```python
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(31, 1, 2024)
fecha_final = qcf.QCDate(31, 1, 2028)
bus_adj_rule = qcf.BusyAdjRules.MODFOLLOW
periodicidad_pago = qcf.Tenor('6M')
periodo_irregular_pago = qcf.StubPeriod.NO
calendario = qcf.BusinessCalendar(fecha_inicio, 20)
lag_pago = 2
nominal = 300_000.0
amort_es_flujo = True
spread = .01
gearing = 1.0
```

Se da de alta el objeto.


```python
icp_clf_leg = qcf.LegFactory.build_bullet_icp_clf_leg(
    rec_pay=rp,
    start_date=fecha_inicio,
    end_date=fecha_final,
    bus_adj_rule=bus_adj_rule,
    settlement_periodicity=periodicidad_pago,
    settlement_stub_period=periodo_irregular_pago,
    settlement_calendar=calendario,
    settlement_lag=lag_pago,
    initial_notional=nominal,
    amort_is_cashflow=amort_es_flujo,
    spread=spread,
    gearing=gearing
)
```


```python
aux.leg_as_dataframe(icp_clf_leg).style.format(aux.format_dict)
```




<style type="text/css">
</style>
<table id="T_1ac97">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_1ac97_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_1ac97_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_1ac97_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_1ac97_level0_col3" class="col_heading level0 col3" >nocional</th>
      <th id="T_1ac97_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_1ac97_level0_col5" class="col_heading level0 col5" >amort_es_flujo</th>
      <th id="T_1ac97_level0_col6" class="col_heading level0 col6" >flujo</th>
      <th id="T_1ac97_level0_col7" class="col_heading level0 col7" >moneda_nocional</th>
      <th id="T_1ac97_level0_col8" class="col_heading level0 col8" >icp_inicial</th>
      <th id="T_1ac97_level0_col9" class="col_heading level0 col9" >icp_final</th>
      <th id="T_1ac97_level0_col10" class="col_heading level0 col10" >uf_inicial</th>
      <th id="T_1ac97_level0_col11" class="col_heading level0 col11" >uf_final</th>
      <th id="T_1ac97_level0_col12" class="col_heading level0 col12" >valor_tasa</th>
      <th id="T_1ac97_level0_col13" class="col_heading level0 col13" >interes</th>
      <th id="T_1ac97_level0_col14" class="col_heading level0 col14" >spread</th>
      <th id="T_1ac97_level0_col15" class="col_heading level0 col15" >gearing</th>
      <th id="T_1ac97_level0_col16" class="col_heading level0 col16" >tipo_tasa</th>
      <th id="T_1ac97_level0_col17" class="col_heading level0 col17" >flujo_en_clp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_1ac97_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_1ac97_row0_col0" class="data row0 col0" >2024-01-31</td>
      <td id="T_1ac97_row0_col1" class="data row0 col1" >2024-07-31</td>
      <td id="T_1ac97_row0_col2" class="data row0 col2" >2024-08-02</td>
      <td id="T_1ac97_row0_col3" class="data row0 col3" >300,000.00</td>
      <td id="T_1ac97_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_1ac97_row0_col5" class="data row0 col5" >True</td>
      <td id="T_1ac97_row0_col6" class="data row0 col6" >1,516.67</td>
      <td id="T_1ac97_row0_col7" class="data row0 col7" >CLF</td>
      <td id="T_1ac97_row0_col8" class="data row0 col8" >10,000.00</td>
      <td id="T_1ac97_row0_col9" class="data row0 col9" >10,000.00</td>
      <td id="T_1ac97_row0_col10" class="data row0 col10" >35,000.00</td>
      <td id="T_1ac97_row0_col11" class="data row0 col11" >35,000.00</td>
      <td id="T_1ac97_row0_col12" class="data row0 col12" >1.0000%</td>
      <td id="T_1ac97_row0_col13" class="data row0 col13" >1,516.67</td>
      <td id="T_1ac97_row0_col14" class="data row0 col14" >1.0000%</td>
      <td id="T_1ac97_row0_col15" class="data row0 col15" >1.00</td>
      <td id="T_1ac97_row0_col16" class="data row0 col16" >LinAct360</td>
      <td id="T_1ac97_row0_col17" class="data row0 col17" >53,083,333.00</td>
    </tr>
    <tr>
      <th id="T_1ac97_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_1ac97_row1_col0" class="data row1 col0" >2024-07-31</td>
      <td id="T_1ac97_row1_col1" class="data row1 col1" >2025-01-31</td>
      <td id="T_1ac97_row1_col2" class="data row1 col2" >2025-02-04</td>
      <td id="T_1ac97_row1_col3" class="data row1 col3" >300,000.00</td>
      <td id="T_1ac97_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_1ac97_row1_col5" class="data row1 col5" >True</td>
      <td id="T_1ac97_row1_col6" class="data row1 col6" >1,533.33</td>
      <td id="T_1ac97_row1_col7" class="data row1 col7" >CLF</td>
      <td id="T_1ac97_row1_col8" class="data row1 col8" >10,000.00</td>
      <td id="T_1ac97_row1_col9" class="data row1 col9" >10,000.00</td>
      <td id="T_1ac97_row1_col10" class="data row1 col10" >35,000.00</td>
      <td id="T_1ac97_row1_col11" class="data row1 col11" >35,000.00</td>
      <td id="T_1ac97_row1_col12" class="data row1 col12" >1.0000%</td>
      <td id="T_1ac97_row1_col13" class="data row1 col13" >1,533.33</td>
      <td id="T_1ac97_row1_col14" class="data row1 col14" >1.0000%</td>
      <td id="T_1ac97_row1_col15" class="data row1 col15" >1.00</td>
      <td id="T_1ac97_row1_col16" class="data row1 col16" >LinAct360</td>
      <td id="T_1ac97_row1_col17" class="data row1 col17" >53,666,667.00</td>
    </tr>
    <tr>
      <th id="T_1ac97_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_1ac97_row2_col0" class="data row2 col0" >2025-01-31</td>
      <td id="T_1ac97_row2_col1" class="data row2 col1" >2025-07-31</td>
      <td id="T_1ac97_row2_col2" class="data row2 col2" >2025-08-04</td>
      <td id="T_1ac97_row2_col3" class="data row2 col3" >300,000.00</td>
      <td id="T_1ac97_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_1ac97_row2_col5" class="data row2 col5" >True</td>
      <td id="T_1ac97_row2_col6" class="data row2 col6" >1,508.33</td>
      <td id="T_1ac97_row2_col7" class="data row2 col7" >CLF</td>
      <td id="T_1ac97_row2_col8" class="data row2 col8" >10,000.00</td>
      <td id="T_1ac97_row2_col9" class="data row2 col9" >10,000.00</td>
      <td id="T_1ac97_row2_col10" class="data row2 col10" >35,000.00</td>
      <td id="T_1ac97_row2_col11" class="data row2 col11" >35,000.00</td>
      <td id="T_1ac97_row2_col12" class="data row2 col12" >1.0000%</td>
      <td id="T_1ac97_row2_col13" class="data row2 col13" >1,508.33</td>
      <td id="T_1ac97_row2_col14" class="data row2 col14" >1.0000%</td>
      <td id="T_1ac97_row2_col15" class="data row2 col15" >1.00</td>
      <td id="T_1ac97_row2_col16" class="data row2 col16" >LinAct360</td>
      <td id="T_1ac97_row2_col17" class="data row2 col17" >52,791,667.00</td>
    </tr>
    <tr>
      <th id="T_1ac97_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_1ac97_row3_col0" class="data row3 col0" >2025-07-31</td>
      <td id="T_1ac97_row3_col1" class="data row3 col1" >2026-01-30</td>
      <td id="T_1ac97_row3_col2" class="data row3 col2" >2026-02-03</td>
      <td id="T_1ac97_row3_col3" class="data row3 col3" >300,000.00</td>
      <td id="T_1ac97_row3_col4" class="data row3 col4" >0.00</td>
      <td id="T_1ac97_row3_col5" class="data row3 col5" >True</td>
      <td id="T_1ac97_row3_col6" class="data row3 col6" >1,525.00</td>
      <td id="T_1ac97_row3_col7" class="data row3 col7" >CLF</td>
      <td id="T_1ac97_row3_col8" class="data row3 col8" >10,000.00</td>
      <td id="T_1ac97_row3_col9" class="data row3 col9" >10,000.00</td>
      <td id="T_1ac97_row3_col10" class="data row3 col10" >35,000.00</td>
      <td id="T_1ac97_row3_col11" class="data row3 col11" >35,000.00</td>
      <td id="T_1ac97_row3_col12" class="data row3 col12" >1.0000%</td>
      <td id="T_1ac97_row3_col13" class="data row3 col13" >1,525.00</td>
      <td id="T_1ac97_row3_col14" class="data row3 col14" >1.0000%</td>
      <td id="T_1ac97_row3_col15" class="data row3 col15" >1.00</td>
      <td id="T_1ac97_row3_col16" class="data row3 col16" >LinAct360</td>
      <td id="T_1ac97_row3_col17" class="data row3 col17" >53,375,000.00</td>
    </tr>
    <tr>
      <th id="T_1ac97_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_1ac97_row4_col0" class="data row4 col0" >2026-01-30</td>
      <td id="T_1ac97_row4_col1" class="data row4 col1" >2026-07-31</td>
      <td id="T_1ac97_row4_col2" class="data row4 col2" >2026-08-04</td>
      <td id="T_1ac97_row4_col3" class="data row4 col3" >300,000.00</td>
      <td id="T_1ac97_row4_col4" class="data row4 col4" >0.00</td>
      <td id="T_1ac97_row4_col5" class="data row4 col5" >True</td>
      <td id="T_1ac97_row4_col6" class="data row4 col6" >1,516.67</td>
      <td id="T_1ac97_row4_col7" class="data row4 col7" >CLF</td>
      <td id="T_1ac97_row4_col8" class="data row4 col8" >10,000.00</td>
      <td id="T_1ac97_row4_col9" class="data row4 col9" >10,000.00</td>
      <td id="T_1ac97_row4_col10" class="data row4 col10" >35,000.00</td>
      <td id="T_1ac97_row4_col11" class="data row4 col11" >35,000.00</td>
      <td id="T_1ac97_row4_col12" class="data row4 col12" >1.0000%</td>
      <td id="T_1ac97_row4_col13" class="data row4 col13" >1,516.67</td>
      <td id="T_1ac97_row4_col14" class="data row4 col14" >1.0000%</td>
      <td id="T_1ac97_row4_col15" class="data row4 col15" >1.00</td>
      <td id="T_1ac97_row4_col16" class="data row4 col16" >LinAct360</td>
      <td id="T_1ac97_row4_col17" class="data row4 col17" >53,083,333.00</td>
    </tr>
    <tr>
      <th id="T_1ac97_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_1ac97_row5_col0" class="data row5 col0" >2026-07-31</td>
      <td id="T_1ac97_row5_col1" class="data row5 col1" >2027-01-29</td>
      <td id="T_1ac97_row5_col2" class="data row5 col2" >2027-02-02</td>
      <td id="T_1ac97_row5_col3" class="data row5 col3" >300,000.00</td>
      <td id="T_1ac97_row5_col4" class="data row5 col4" >0.00</td>
      <td id="T_1ac97_row5_col5" class="data row5 col5" >True</td>
      <td id="T_1ac97_row5_col6" class="data row5 col6" >1,516.67</td>
      <td id="T_1ac97_row5_col7" class="data row5 col7" >CLF</td>
      <td id="T_1ac97_row5_col8" class="data row5 col8" >10,000.00</td>
      <td id="T_1ac97_row5_col9" class="data row5 col9" >10,000.00</td>
      <td id="T_1ac97_row5_col10" class="data row5 col10" >35,000.00</td>
      <td id="T_1ac97_row5_col11" class="data row5 col11" >35,000.00</td>
      <td id="T_1ac97_row5_col12" class="data row5 col12" >1.0000%</td>
      <td id="T_1ac97_row5_col13" class="data row5 col13" >1,516.67</td>
      <td id="T_1ac97_row5_col14" class="data row5 col14" >1.0000%</td>
      <td id="T_1ac97_row5_col15" class="data row5 col15" >1.00</td>
      <td id="T_1ac97_row5_col16" class="data row5 col16" >LinAct360</td>
      <td id="T_1ac97_row5_col17" class="data row5 col17" >53,083,333.00</td>
    </tr>
    <tr>
      <th id="T_1ac97_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_1ac97_row6_col0" class="data row6 col0" >2027-01-29</td>
      <td id="T_1ac97_row6_col1" class="data row6 col1" >2027-07-30</td>
      <td id="T_1ac97_row6_col2" class="data row6 col2" >2027-08-03</td>
      <td id="T_1ac97_row6_col3" class="data row6 col3" >300,000.00</td>
      <td id="T_1ac97_row6_col4" class="data row6 col4" >0.00</td>
      <td id="T_1ac97_row6_col5" class="data row6 col5" >True</td>
      <td id="T_1ac97_row6_col6" class="data row6 col6" >1,516.67</td>
      <td id="T_1ac97_row6_col7" class="data row6 col7" >CLF</td>
      <td id="T_1ac97_row6_col8" class="data row6 col8" >10,000.00</td>
      <td id="T_1ac97_row6_col9" class="data row6 col9" >10,000.00</td>
      <td id="T_1ac97_row6_col10" class="data row6 col10" >35,000.00</td>
      <td id="T_1ac97_row6_col11" class="data row6 col11" >35,000.00</td>
      <td id="T_1ac97_row6_col12" class="data row6 col12" >1.0000%</td>
      <td id="T_1ac97_row6_col13" class="data row6 col13" >1,516.67</td>
      <td id="T_1ac97_row6_col14" class="data row6 col14" >1.0000%</td>
      <td id="T_1ac97_row6_col15" class="data row6 col15" >1.00</td>
      <td id="T_1ac97_row6_col16" class="data row6 col16" >LinAct360</td>
      <td id="T_1ac97_row6_col17" class="data row6 col17" >53,083,333.00</td>
    </tr>
    <tr>
      <th id="T_1ac97_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_1ac97_row7_col0" class="data row7 col0" >2027-07-30</td>
      <td id="T_1ac97_row7_col1" class="data row7 col1" >2028-01-31</td>
      <td id="T_1ac97_row7_col2" class="data row7 col2" >2028-02-02</td>
      <td id="T_1ac97_row7_col3" class="data row7 col3" >300,000.00</td>
      <td id="T_1ac97_row7_col4" class="data row7 col4" >300,000.00</td>
      <td id="T_1ac97_row7_col5" class="data row7 col5" >True</td>
      <td id="T_1ac97_row7_col6" class="data row7 col6" >301,541.67</td>
      <td id="T_1ac97_row7_col7" class="data row7 col7" >CLF</td>
      <td id="T_1ac97_row7_col8" class="data row7 col8" >10,000.00</td>
      <td id="T_1ac97_row7_col9" class="data row7 col9" >10,000.00</td>
      <td id="T_1ac97_row7_col10" class="data row7 col10" >35,000.00</td>
      <td id="T_1ac97_row7_col11" class="data row7 col11" >35,000.00</td>
      <td id="T_1ac97_row7_col12" class="data row7 col12" >1.0000%</td>
      <td id="T_1ac97_row7_col13" class="data row7 col13" >1,541.67</td>
      <td id="T_1ac97_row7_col14" class="data row7 col14" >1.0000%</td>
      <td id="T_1ac97_row7_col15" class="data row7 col15" >1.00</td>
      <td id="T_1ac97_row7_col16" class="data row7 col16" >LinAct360</td>
      <td id="T_1ac97_row7_col17" class="data row7 col17" >10,553,958,333.00</td>
    </tr>
  </tbody>
</table>



