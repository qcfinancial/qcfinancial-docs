# Uso de `qcfinancial` (Parte 2)

Se importa `QC_Financial_3` que es la versión compilada para Python3.


```python
import qcfinancial as qcf
```

El siguiente diccionario se utiliza para dar formato a las columnas de los `pandas.DataFrames` que se utilizarán.


```python
format_dict = {'nominal': '{0:,.2f}', 'amort': '{0:,.2f}', 'interes': '{0:,.2f}', 'flujo': '{0:,.2f}',
               'icp_inicial': '{0:,.2f}', 'icp_final': '{0:,.2f}',
               'valor_tasa': '{0:,.4%}', 'spread': '{0:,.4%}', 'gearing': '{0:,.2f}',
               'amort_moneda_pago': '{0:,.2f}', 'interes_moneda_pago': '{0:,.2f}', 'valor_indice_fx': '{0:,.2f}'}
```

## Legs
Los objetos de tipo `Leg` son una lista (o vector) de objetos `Cashflow` y representan una pata de un instrumento financiero. un objeto de tipo `Leg` puede construirse *a mano* es decir, dando de alta cashflows y agregándolos uno a uno o con algunos métodos de conveniencia cuyo funcionamiento se mostrará.
### Construcción Manual
Se verá como construir un `Leg` con 2 `SimpleCashflow` de forma *manual*. En particular, este objeto `Leg` podría representar una operación FX por entrega física.


```python
fecha_vcto = qcf.QCDate(20, 9, 2018)

simple_cashflow_1 = qcf.SimpleCashflow(
    fecha_vcto,  # fecha del flujo
    100,         # monto
    qcf.QCCLP()  # moneda
) 

simple_cashflow_2 = qcf.SimpleCashflow(
    fecha_vcto,  # fecha del flujo
    -70000,      # monto
    qcf.QCUSD()  # moneda
)

leg = qcf.Leg()
leg.append_cashflow(simple_cashflow_1)
leg.append_cashflow(simple_cashflow_2)
```


```python
# Se observa el resultado
num = leg.size()
for i in range(0, num):
    print(qcf.show(leg.get_cashflow_at(i)))
```

    ('2018-09-20', 100.0, 'CLP')
    ('2018-09-20', -70000.0, 'USD')


### Construcción Asistida de un `FixedRateLeg`
Se verá como construir objetos `Leg` donde cada `Cashflow` es un objeto de tipo `FixedRateCashflow`, todos con la misma tasa fija. En el primer ejemplo se construye un `Leg` de tipo *bullet*: una única amortización igual al capital vigente de todos los `FixedRateCasflow` en el último flujo.
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
- `QCCurrency`: moneda del nominal y de los flujos
- `bool`: si es `True` fuerza a que las fechas de pago coincidan con las fechas finales. Esto para lograr una valorización acorde a las convenciones de los mercados de renta fija, en caso que la `Leg` represente un bono a tasa fija.

Vamos a un ejemplo. Cambiando los parámetros siguientes se puede visualizar el efecto de ellos en la construcción.


```python
# Se da de alta los parámetros requeridos
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(5, 11, 2019)
fecha_final = qcf.QCDate(31, 5, 2023)
bus_adj_rule = qcf.BusyAdjRules.MODFOLLOW
periodicidad = qcf.Tenor('6M')
periodo_irregular = qcf.StubPeriod.LONGFRONT
calendario = qcf.BusinessCalendar(fecha_inicio, 20)
calendario.add_holiday(qcf.QCDate(31, 12, 2019))
lag_pago = 0
nominal = 100000.0
amort_es_flujo = False
tasa_cupon = qcf.QCInterestRate(.03, qcf.QCAct360(), qcf.QCLinearWf())
moneda = qcf.QCCLF()
es_bono = False

# Se da de alta el objeto
fixed_rate_leg = qcf.LegFactory.build_bullet_fixed_rate_leg(
    rp,
    fecha_inicio,
    fecha_final,
    bus_adj_rule,
    periodicidad,
    periodo_irregular,
    calendario,
    lag_pago,
    nominal,
    amort_es_flujo,
    tasa_cupon,
    moneda,
    es_bono
)
```

Se puede lograr una visualización del resultado utilizando un Dataframe de pandas y el método `show`.


```python
# Se importa pandas de la forma usual
import pandas as pd

# Se define un list donde almacenar los resultados de la función show
tabla = []
for i in range(0, fixed_rate_leg.size()):
    tabla.append(qcf.show(fixed_rate_leg.get_cashflow_at(i)))

# Se utiliza tabla para inicializar el Dataframe
columnas = ['fecha_ini', 'fecha_fin', 'fecha_pago', 'nominal', 'amort', 'interes', 'amort_es_flujo', 'flujo', 'moneda',
            'valor_tasa', 'tipo_tasa']
df = pd.DataFrame(tabla, columns=columnas)

# Se despliega la data en este formato
df.style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_c6640">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_c6640_level0_col0" class="col_heading level0 col0" >fecha_ini</th>
      <th id="T_c6640_level0_col1" class="col_heading level0 col1" >fecha_fin</th>
      <th id="T_c6640_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_c6640_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_c6640_level0_col4" class="col_heading level0 col4" >amort</th>
      <th id="T_c6640_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_c6640_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_c6640_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_c6640_level0_col8" class="col_heading level0 col8" >moneda</th>
      <th id="T_c6640_level0_col9" class="col_heading level0 col9" >valor_tasa</th>
      <th id="T_c6640_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_c6640_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_c6640_row0_col0" class="data row0 col0" >2019-11-05</td>
      <td id="T_c6640_row0_col1" class="data row0 col1" >2020-05-29</td>
      <td id="T_c6640_row0_col2" class="data row0 col2" >2020-05-29</td>
      <td id="T_c6640_row0_col3" class="data row0 col3" >100,000.00</td>
      <td id="T_c6640_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_c6640_row0_col5" class="data row0 col5" >1,716.67</td>
      <td id="T_c6640_row0_col6" class="data row0 col6" >False</td>
      <td id="T_c6640_row0_col7" class="data row0 col7" >1,716.67</td>
      <td id="T_c6640_row0_col8" class="data row0 col8" >CLF</td>
      <td id="T_c6640_row0_col9" class="data row0 col9" >3.0000%</td>
      <td id="T_c6640_row0_col10" class="data row0 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_c6640_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_c6640_row1_col0" class="data row1 col0" >2020-05-29</td>
      <td id="T_c6640_row1_col1" class="data row1 col1" >2020-11-30</td>
      <td id="T_c6640_row1_col2" class="data row1 col2" >2020-11-30</td>
      <td id="T_c6640_row1_col3" class="data row1 col3" >100,000.00</td>
      <td id="T_c6640_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_c6640_row1_col5" class="data row1 col5" >1,541.67</td>
      <td id="T_c6640_row1_col6" class="data row1 col6" >False</td>
      <td id="T_c6640_row1_col7" class="data row1 col7" >1,541.67</td>
      <td id="T_c6640_row1_col8" class="data row1 col8" >CLF</td>
      <td id="T_c6640_row1_col9" class="data row1 col9" >3.0000%</td>
      <td id="T_c6640_row1_col10" class="data row1 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_c6640_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_c6640_row2_col0" class="data row2 col0" >2020-11-30</td>
      <td id="T_c6640_row2_col1" class="data row2 col1" >2021-05-31</td>
      <td id="T_c6640_row2_col2" class="data row2 col2" >2021-05-31</td>
      <td id="T_c6640_row2_col3" class="data row2 col3" >100,000.00</td>
      <td id="T_c6640_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_c6640_row2_col5" class="data row2 col5" >1,516.67</td>
      <td id="T_c6640_row2_col6" class="data row2 col6" >False</td>
      <td id="T_c6640_row2_col7" class="data row2 col7" >1,516.67</td>
      <td id="T_c6640_row2_col8" class="data row2 col8" >CLF</td>
      <td id="T_c6640_row2_col9" class="data row2 col9" >3.0000%</td>
      <td id="T_c6640_row2_col10" class="data row2 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_c6640_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_c6640_row3_col0" class="data row3 col0" >2021-05-31</td>
      <td id="T_c6640_row3_col1" class="data row3 col1" >2021-11-30</td>
      <td id="T_c6640_row3_col2" class="data row3 col2" >2021-11-30</td>
      <td id="T_c6640_row3_col3" class="data row3 col3" >100,000.00</td>
      <td id="T_c6640_row3_col4" class="data row3 col4" >0.00</td>
      <td id="T_c6640_row3_col5" class="data row3 col5" >1,525.00</td>
      <td id="T_c6640_row3_col6" class="data row3 col6" >False</td>
      <td id="T_c6640_row3_col7" class="data row3 col7" >1,525.00</td>
      <td id="T_c6640_row3_col8" class="data row3 col8" >CLF</td>
      <td id="T_c6640_row3_col9" class="data row3 col9" >3.0000%</td>
      <td id="T_c6640_row3_col10" class="data row3 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_c6640_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_c6640_row4_col0" class="data row4 col0" >2021-11-30</td>
      <td id="T_c6640_row4_col1" class="data row4 col1" >2022-05-31</td>
      <td id="T_c6640_row4_col2" class="data row4 col2" >2022-05-31</td>
      <td id="T_c6640_row4_col3" class="data row4 col3" >100,000.00</td>
      <td id="T_c6640_row4_col4" class="data row4 col4" >0.00</td>
      <td id="T_c6640_row4_col5" class="data row4 col5" >1,516.67</td>
      <td id="T_c6640_row4_col6" class="data row4 col6" >False</td>
      <td id="T_c6640_row4_col7" class="data row4 col7" >1,516.67</td>
      <td id="T_c6640_row4_col8" class="data row4 col8" >CLF</td>
      <td id="T_c6640_row4_col9" class="data row4 col9" >3.0000%</td>
      <td id="T_c6640_row4_col10" class="data row4 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_c6640_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_c6640_row5_col0" class="data row5 col0" >2022-05-31</td>
      <td id="T_c6640_row5_col1" class="data row5 col1" >2022-11-30</td>
      <td id="T_c6640_row5_col2" class="data row5 col2" >2022-11-30</td>
      <td id="T_c6640_row5_col3" class="data row5 col3" >100,000.00</td>
      <td id="T_c6640_row5_col4" class="data row5 col4" >0.00</td>
      <td id="T_c6640_row5_col5" class="data row5 col5" >1,525.00</td>
      <td id="T_c6640_row5_col6" class="data row5 col6" >False</td>
      <td id="T_c6640_row5_col7" class="data row5 col7" >1,525.00</td>
      <td id="T_c6640_row5_col8" class="data row5 col8" >CLF</td>
      <td id="T_c6640_row5_col9" class="data row5 col9" >3.0000%</td>
      <td id="T_c6640_row5_col10" class="data row5 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_c6640_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_c6640_row6_col0" class="data row6 col0" >2022-11-30</td>
      <td id="T_c6640_row6_col1" class="data row6 col1" >2023-05-31</td>
      <td id="T_c6640_row6_col2" class="data row6 col2" >2023-05-31</td>
      <td id="T_c6640_row6_col3" class="data row6 col3" >100,000.00</td>
      <td id="T_c6640_row6_col4" class="data row6 col4" >100,000.00</td>
      <td id="T_c6640_row6_col5" class="data row6 col5" >1,516.67</td>
      <td id="T_c6640_row6_col6" class="data row6 col6" >False</td>
      <td id="T_c6640_row6_col7" class="data row6 col7" >1,516.67</td>
      <td id="T_c6640_row6_col8" class="data row6 col8" >CLF</td>
      <td id="T_c6640_row6_col9" class="data row6 col9" >3.0000%</td>
      <td id="T_c6640_row6_col10" class="data row6 col10" >LinAct360</td>
    </tr>
  </tbody>
</table>




### Construcción Asistida de un `FixedRateLeg2`
Se verá como construir objetos `Leg` donde cada `Cashflow` es un objeto de tipo `FixedRateCashflow2`, todos con la misma tasa fija. En el primer ejemplo se construye un `Leg` de tipo *bullet*: una única amortización igual al capital vigente de todos los `FixedRateCasflow2` en el último flujo.
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
- `QCCurrency`: moneda del nominal y de los flujos
- `bool`: si es `True` fuerza a que las fechas de pago coincidan con las fechas finales. Esto para lograr una valorización acorde a las convenciones de los mercados de renta fija, en caso que la `Leg` represente un bono a tasa fija.

Vamos a un ejemplo. Cambiando los parámetros siguientes se puede visualizar el efecto de ellos en la construcción.


```python
# Se da de alta los parámetros requeridos
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(4, 4, 2018)
fecha_final = qcf.QCDate(1, 3, 2021) 
bus_adj_rule = qcf.BusyAdjRules.NO
periodicidad = qcf.Tenor('6M')
periodo_irregular = qcf.StubPeriod.SHORTFRONT
calendario = qcf.BusinessCalendar(fecha_inicio, 20)
calendario.add_holiday(qcf.QCDate(31, 12, 2018))
lag_pago = 0
nominal = 100000.0
amort_es_flujo = False
tasa_cupon = qcf.QCInterestRate(.03, qcf.QCAct360(), qcf.QCLinearWf())
moneda = qcf.QCCLF()
es_bono = False

# Se da de alta el objeto
fixed_rate_leg_2 = qcf.LegFactory.build_bullet_fixed_rate_leg_2(
    rp,
    fecha_inicio,
    fecha_final,
    bus_adj_rule,
    periodicidad,
    periodo_irregular,
    calendario,
    lag_pago,
    nominal,
    amort_es_flujo,
    tasa_cupon,
    moneda,
    es_bono
)
```


```python
tabla = []
for i in range(fixed_rate_leg_2.size()):
    tabla.append(qcf.show(fixed_rate_leg_2.get_cashflow_at(i)))
    
df2 = pd.DataFrame(tabla, columns=columnas)

# Se despliega la data en este formato
df2.style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_4abbc">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_4abbc_level0_col0" class="col_heading level0 col0" >fecha_ini</th>
      <th id="T_4abbc_level0_col1" class="col_heading level0 col1" >fecha_fin</th>
      <th id="T_4abbc_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_4abbc_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_4abbc_level0_col4" class="col_heading level0 col4" >amort</th>
      <th id="T_4abbc_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_4abbc_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_4abbc_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_4abbc_level0_col8" class="col_heading level0 col8" >moneda</th>
      <th id="T_4abbc_level0_col9" class="col_heading level0 col9" >valor_tasa</th>
      <th id="T_4abbc_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_4abbc_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_4abbc_row0_col0" class="data row0 col0" >2018-04-04</td>
      <td id="T_4abbc_row0_col1" class="data row0 col1" >2018-09-01</td>
      <td id="T_4abbc_row0_col2" class="data row0 col2" >2018-09-03</td>
      <td id="T_4abbc_row0_col3" class="data row0 col3" >100,000.00</td>
      <td id="T_4abbc_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_4abbc_row0_col5" class="data row0 col5" >1,250.00</td>
      <td id="T_4abbc_row0_col6" class="data row0 col6" >False</td>
      <td id="T_4abbc_row0_col7" class="data row0 col7" >1,250.00</td>
      <td id="T_4abbc_row0_col8" class="data row0 col8" >CLF</td>
      <td id="T_4abbc_row0_col9" class="data row0 col9" >3.0000%</td>
      <td id="T_4abbc_row0_col10" class="data row0 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4abbc_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_4abbc_row1_col0" class="data row1 col0" >2018-09-01</td>
      <td id="T_4abbc_row1_col1" class="data row1 col1" >2019-03-01</td>
      <td id="T_4abbc_row1_col2" class="data row1 col2" >2019-03-01</td>
      <td id="T_4abbc_row1_col3" class="data row1 col3" >100,000.00</td>
      <td id="T_4abbc_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_4abbc_row1_col5" class="data row1 col5" >1,508.33</td>
      <td id="T_4abbc_row1_col6" class="data row1 col6" >False</td>
      <td id="T_4abbc_row1_col7" class="data row1 col7" >1,508.33</td>
      <td id="T_4abbc_row1_col8" class="data row1 col8" >CLF</td>
      <td id="T_4abbc_row1_col9" class="data row1 col9" >3.0000%</td>
      <td id="T_4abbc_row1_col10" class="data row1 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4abbc_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_4abbc_row2_col0" class="data row2 col0" >2019-03-01</td>
      <td id="T_4abbc_row2_col1" class="data row2 col1" >2019-09-01</td>
      <td id="T_4abbc_row2_col2" class="data row2 col2" >2019-09-02</td>
      <td id="T_4abbc_row2_col3" class="data row2 col3" >100,000.00</td>
      <td id="T_4abbc_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_4abbc_row2_col5" class="data row2 col5" >1,533.33</td>
      <td id="T_4abbc_row2_col6" class="data row2 col6" >False</td>
      <td id="T_4abbc_row2_col7" class="data row2 col7" >1,533.33</td>
      <td id="T_4abbc_row2_col8" class="data row2 col8" >CLF</td>
      <td id="T_4abbc_row2_col9" class="data row2 col9" >3.0000%</td>
      <td id="T_4abbc_row2_col10" class="data row2 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4abbc_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_4abbc_row3_col0" class="data row3 col0" >2019-09-01</td>
      <td id="T_4abbc_row3_col1" class="data row3 col1" >2020-03-01</td>
      <td id="T_4abbc_row3_col2" class="data row3 col2" >2020-03-02</td>
      <td id="T_4abbc_row3_col3" class="data row3 col3" >100,000.00</td>
      <td id="T_4abbc_row3_col4" class="data row3 col4" >0.00</td>
      <td id="T_4abbc_row3_col5" class="data row3 col5" >1,516.67</td>
      <td id="T_4abbc_row3_col6" class="data row3 col6" >False</td>
      <td id="T_4abbc_row3_col7" class="data row3 col7" >1,516.67</td>
      <td id="T_4abbc_row3_col8" class="data row3 col8" >CLF</td>
      <td id="T_4abbc_row3_col9" class="data row3 col9" >3.0000%</td>
      <td id="T_4abbc_row3_col10" class="data row3 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4abbc_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_4abbc_row4_col0" class="data row4 col0" >2020-03-01</td>
      <td id="T_4abbc_row4_col1" class="data row4 col1" >2020-09-01</td>
      <td id="T_4abbc_row4_col2" class="data row4 col2" >2020-09-01</td>
      <td id="T_4abbc_row4_col3" class="data row4 col3" >100,000.00</td>
      <td id="T_4abbc_row4_col4" class="data row4 col4" >0.00</td>
      <td id="T_4abbc_row4_col5" class="data row4 col5" >1,533.33</td>
      <td id="T_4abbc_row4_col6" class="data row4 col6" >False</td>
      <td id="T_4abbc_row4_col7" class="data row4 col7" >1,533.33</td>
      <td id="T_4abbc_row4_col8" class="data row4 col8" >CLF</td>
      <td id="T_4abbc_row4_col9" class="data row4 col9" >3.0000%</td>
      <td id="T_4abbc_row4_col10" class="data row4 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4abbc_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_4abbc_row5_col0" class="data row5 col0" >2020-09-01</td>
      <td id="T_4abbc_row5_col1" class="data row5 col1" >2021-03-01</td>
      <td id="T_4abbc_row5_col2" class="data row5 col2" >2021-03-01</td>
      <td id="T_4abbc_row5_col3" class="data row5 col3" >100,000.00</td>
      <td id="T_4abbc_row5_col4" class="data row5 col4" >100,000.00</td>
      <td id="T_4abbc_row5_col5" class="data row5 col5" >1,508.33</td>
      <td id="T_4abbc_row5_col6" class="data row5 col6" >False</td>
      <td id="T_4abbc_row5_col7" class="data row5 col7" >1,508.33</td>
      <td id="T_4abbc_row5_col8" class="data row5 col8" >CLF</td>
      <td id="T_4abbc_row5_col9" class="data row5 col9" >3.0000%</td>
      <td id="T_4abbc_row5_col10" class="data row5 col10" >LinAct360</td>
    </tr>
  </tbody>
</table>




### Construcción Asistida de un `CustomAmortFixedRateLeg`
En este ejemplo se construye un `Leg` donde la estructura de amortizaciones es customizada.
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
- `bool`: si es `True` fuerza a que las fechas de pago coincidan con las fechas finales. Esto para lograr una valorización acorde a las convenciones de los mercados de renta fija, en caso que la `Leg` represente un bono a tasa fija.

Vamos a un ejemplo. Cambiando los parámetros siguientes se puede visualizar el efecto de ellos en la construcción.


```python
# Se da de alta los parámetros requeridos
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(31, 1, 1969)
fecha_final = qcf.QCDate(31, 1, 1974) 
bus_adj_rule = qcf.BusyAdjRules.MODFOLLOW
periodicidad = qcf.Tenor('6M')
periodo_irregular = qcf.StubPeriod.NO
calendario = qcf.BusinessCalendar(fecha_inicio, 20)
lag_pago = 0
custom_notional_amort = qcf.CustomNotionalAmort()
custom_notional_amort.set_size(10)
for i in range(0, 10):
    custom_notional_amort.set_notional_amort_at(i, 1000.0 - i * 100.0, 100.0)
amort_es_flujo = False
tasa_cupon = qcf.QCInterestRate(.03, qcf.QC30360(), qcf.QCLinearWf())
moneda = qcf.QCCLF()
es_bono = False
```


```python
# Se da de alta el objeto
fixed_rate_custom_leg = qcf.LegFactory.build_custom_amort_fixed_rate_leg(
    rp,
    fecha_inicio,
    fecha_final,
    bus_adj_rule,
    periodicidad,
    periodo_irregular,
    calendario,
    lag_pago,
    custom_notional_amort,
    amort_es_flujo,
    tasa_cupon,
    moneda
)
```


```python
# Se define un list donde almacenar los resultados de la función show
tabla = []
for i in range(0, fixed_rate_custom_leg.size()):
    tabla.append(qcf.show(fixed_rate_custom_leg.get_cashflow_at(i)))

# Se utiliza tabla para inicializar el Dataframe
columnas = ['fecha_ini', 'fecha_fin', 'fecha_pago', 'nominal', 'amort', 'interes', 'amort_es_flujo', 'flujo', 'moneda',
            'valor_tasa', 'tipo_tasa']
df3 = pd.DataFrame(tabla, columns=columnas)

# Se despliega la data en este formato
df3.style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_65ffd">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_65ffd_level0_col0" class="col_heading level0 col0" >fecha_ini</th>
      <th id="T_65ffd_level0_col1" class="col_heading level0 col1" >fecha_fin</th>
      <th id="T_65ffd_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_65ffd_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_65ffd_level0_col4" class="col_heading level0 col4" >amort</th>
      <th id="T_65ffd_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_65ffd_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_65ffd_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_65ffd_level0_col8" class="col_heading level0 col8" >moneda</th>
      <th id="T_65ffd_level0_col9" class="col_heading level0 col9" >valor_tasa</th>
      <th id="T_65ffd_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_65ffd_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_65ffd_row0_col0" class="data row0 col0" >1969-01-31</td>
      <td id="T_65ffd_row0_col1" class="data row0 col1" >1969-07-31</td>
      <td id="T_65ffd_row0_col2" class="data row0 col2" >1969-07-31</td>
      <td id="T_65ffd_row0_col3" class="data row0 col3" >1,000.00</td>
      <td id="T_65ffd_row0_col4" class="data row0 col4" >100.00</td>
      <td id="T_65ffd_row0_col5" class="data row0 col5" >15.00</td>
      <td id="T_65ffd_row0_col6" class="data row0 col6" >False</td>
      <td id="T_65ffd_row0_col7" class="data row0 col7" >15.00</td>
      <td id="T_65ffd_row0_col8" class="data row0 col8" >CLF</td>
      <td id="T_65ffd_row0_col9" class="data row0 col9" >3.0000%</td>
      <td id="T_65ffd_row0_col10" class="data row0 col10" >Lin30360</td>
    </tr>
    <tr>
      <th id="T_65ffd_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_65ffd_row1_col0" class="data row1 col0" >1969-07-31</td>
      <td id="T_65ffd_row1_col1" class="data row1 col1" >1970-01-30</td>
      <td id="T_65ffd_row1_col2" class="data row1 col2" >1970-01-30</td>
      <td id="T_65ffd_row1_col3" class="data row1 col3" >900.00</td>
      <td id="T_65ffd_row1_col4" class="data row1 col4" >100.00</td>
      <td id="T_65ffd_row1_col5" class="data row1 col5" >13.50</td>
      <td id="T_65ffd_row1_col6" class="data row1 col6" >False</td>
      <td id="T_65ffd_row1_col7" class="data row1 col7" >13.50</td>
      <td id="T_65ffd_row1_col8" class="data row1 col8" >CLF</td>
      <td id="T_65ffd_row1_col9" class="data row1 col9" >3.0000%</td>
      <td id="T_65ffd_row1_col10" class="data row1 col10" >Lin30360</td>
    </tr>
    <tr>
      <th id="T_65ffd_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_65ffd_row2_col0" class="data row2 col0" >1970-01-30</td>
      <td id="T_65ffd_row2_col1" class="data row2 col1" >1970-07-31</td>
      <td id="T_65ffd_row2_col2" class="data row2 col2" >1970-07-31</td>
      <td id="T_65ffd_row2_col3" class="data row2 col3" >800.00</td>
      <td id="T_65ffd_row2_col4" class="data row2 col4" >100.00</td>
      <td id="T_65ffd_row2_col5" class="data row2 col5" >12.00</td>
      <td id="T_65ffd_row2_col6" class="data row2 col6" >False</td>
      <td id="T_65ffd_row2_col7" class="data row2 col7" >12.00</td>
      <td id="T_65ffd_row2_col8" class="data row2 col8" >CLF</td>
      <td id="T_65ffd_row2_col9" class="data row2 col9" >3.0000%</td>
      <td id="T_65ffd_row2_col10" class="data row2 col10" >Lin30360</td>
    </tr>
    <tr>
      <th id="T_65ffd_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_65ffd_row3_col0" class="data row3 col0" >1970-07-31</td>
      <td id="T_65ffd_row3_col1" class="data row3 col1" >1971-01-29</td>
      <td id="T_65ffd_row3_col2" class="data row3 col2" >1971-01-29</td>
      <td id="T_65ffd_row3_col3" class="data row3 col3" >700.00</td>
      <td id="T_65ffd_row3_col4" class="data row3 col4" >100.00</td>
      <td id="T_65ffd_row3_col5" class="data row3 col5" >10.44</td>
      <td id="T_65ffd_row3_col6" class="data row3 col6" >False</td>
      <td id="T_65ffd_row3_col7" class="data row3 col7" >10.44</td>
      <td id="T_65ffd_row3_col8" class="data row3 col8" >CLF</td>
      <td id="T_65ffd_row3_col9" class="data row3 col9" >3.0000%</td>
      <td id="T_65ffd_row3_col10" class="data row3 col10" >Lin30360</td>
    </tr>
    <tr>
      <th id="T_65ffd_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_65ffd_row4_col0" class="data row4 col0" >1971-01-29</td>
      <td id="T_65ffd_row4_col1" class="data row4 col1" >1971-07-30</td>
      <td id="T_65ffd_row4_col2" class="data row4 col2" >1971-07-30</td>
      <td id="T_65ffd_row4_col3" class="data row4 col3" >600.00</td>
      <td id="T_65ffd_row4_col4" class="data row4 col4" >100.00</td>
      <td id="T_65ffd_row4_col5" class="data row4 col5" >9.05</td>
      <td id="T_65ffd_row4_col6" class="data row4 col6" >False</td>
      <td id="T_65ffd_row4_col7" class="data row4 col7" >9.05</td>
      <td id="T_65ffd_row4_col8" class="data row4 col8" >CLF</td>
      <td id="T_65ffd_row4_col9" class="data row4 col9" >3.0000%</td>
      <td id="T_65ffd_row4_col10" class="data row4 col10" >Lin30360</td>
    </tr>
    <tr>
      <th id="T_65ffd_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_65ffd_row5_col0" class="data row5 col0" >1971-07-30</td>
      <td id="T_65ffd_row5_col1" class="data row5 col1" >1972-01-31</td>
      <td id="T_65ffd_row5_col2" class="data row5 col2" >1972-01-31</td>
      <td id="T_65ffd_row5_col3" class="data row5 col3" >500.00</td>
      <td id="T_65ffd_row5_col4" class="data row5 col4" >100.00</td>
      <td id="T_65ffd_row5_col5" class="data row5 col5" >7.50</td>
      <td id="T_65ffd_row5_col6" class="data row5 col6" >False</td>
      <td id="T_65ffd_row5_col7" class="data row5 col7" >7.50</td>
      <td id="T_65ffd_row5_col8" class="data row5 col8" >CLF</td>
      <td id="T_65ffd_row5_col9" class="data row5 col9" >3.0000%</td>
      <td id="T_65ffd_row5_col10" class="data row5 col10" >Lin30360</td>
    </tr>
    <tr>
      <th id="T_65ffd_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_65ffd_row6_col0" class="data row6 col0" >1972-01-31</td>
      <td id="T_65ffd_row6_col1" class="data row6 col1" >1972-07-31</td>
      <td id="T_65ffd_row6_col2" class="data row6 col2" >1972-07-31</td>
      <td id="T_65ffd_row6_col3" class="data row6 col3" >400.00</td>
      <td id="T_65ffd_row6_col4" class="data row6 col4" >100.00</td>
      <td id="T_65ffd_row6_col5" class="data row6 col5" >6.00</td>
      <td id="T_65ffd_row6_col6" class="data row6 col6" >False</td>
      <td id="T_65ffd_row6_col7" class="data row6 col7" >6.00</td>
      <td id="T_65ffd_row6_col8" class="data row6 col8" >CLF</td>
      <td id="T_65ffd_row6_col9" class="data row6 col9" >3.0000%</td>
      <td id="T_65ffd_row6_col10" class="data row6 col10" >Lin30360</td>
    </tr>
    <tr>
      <th id="T_65ffd_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_65ffd_row7_col0" class="data row7 col0" >1972-07-31</td>
      <td id="T_65ffd_row7_col1" class="data row7 col1" >1973-01-31</td>
      <td id="T_65ffd_row7_col2" class="data row7 col2" >1973-01-31</td>
      <td id="T_65ffd_row7_col3" class="data row7 col3" >300.00</td>
      <td id="T_65ffd_row7_col4" class="data row7 col4" >100.00</td>
      <td id="T_65ffd_row7_col5" class="data row7 col5" >4.50</td>
      <td id="T_65ffd_row7_col6" class="data row7 col6" >False</td>
      <td id="T_65ffd_row7_col7" class="data row7 col7" >4.50</td>
      <td id="T_65ffd_row7_col8" class="data row7 col8" >CLF</td>
      <td id="T_65ffd_row7_col9" class="data row7 col9" >3.0000%</td>
      <td id="T_65ffd_row7_col10" class="data row7 col10" >Lin30360</td>
    </tr>
    <tr>
      <th id="T_65ffd_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_65ffd_row8_col0" class="data row8 col0" >1973-01-31</td>
      <td id="T_65ffd_row8_col1" class="data row8 col1" >1973-07-31</td>
      <td id="T_65ffd_row8_col2" class="data row8 col2" >1973-07-31</td>
      <td id="T_65ffd_row8_col3" class="data row8 col3" >200.00</td>
      <td id="T_65ffd_row8_col4" class="data row8 col4" >100.00</td>
      <td id="T_65ffd_row8_col5" class="data row8 col5" >3.00</td>
      <td id="T_65ffd_row8_col6" class="data row8 col6" >False</td>
      <td id="T_65ffd_row8_col7" class="data row8 col7" >3.00</td>
      <td id="T_65ffd_row8_col8" class="data row8 col8" >CLF</td>
      <td id="T_65ffd_row8_col9" class="data row8 col9" >3.0000%</td>
      <td id="T_65ffd_row8_col10" class="data row8 col10" >Lin30360</td>
    </tr>
    <tr>
      <th id="T_65ffd_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_65ffd_row9_col0" class="data row9 col0" >1973-07-31</td>
      <td id="T_65ffd_row9_col1" class="data row9 col1" >1974-01-31</td>
      <td id="T_65ffd_row9_col2" class="data row9 col2" >1974-01-31</td>
      <td id="T_65ffd_row9_col3" class="data row9 col3" >100.00</td>
      <td id="T_65ffd_row9_col4" class="data row9 col4" >100.00</td>
      <td id="T_65ffd_row9_col5" class="data row9 col5" >1.50</td>
      <td id="T_65ffd_row9_col6" class="data row9 col6" >False</td>
      <td id="T_65ffd_row9_col7" class="data row9 col7" >1.50</td>
      <td id="T_65ffd_row9_col8" class="data row9 col8" >CLF</td>
      <td id="T_65ffd_row9_col9" class="data row9 col9" >3.0000%</td>
      <td id="T_65ffd_row9_col10" class="data row9 col10" >Lin30360</td>
    </tr>
  </tbody>
</table>




### Construcción Asistida de un `FixedRateMultiCurrencyLeg`
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
- `QCCurrency`: moneda de los flujos
- `FXRateIndex`: índice con el cual se transforma cada flujo a la moneda de pago.
- `bool`: si es `True` fuerza a que las fechas de pago coincidan con las fechas finales. Esto para lograr una valorización acorde a las convenciones de los mercados de renta fija, en caso que la `Leg` represente un bono a tasa fija.

Vamos a un ejemplo. Cambiando los parámetros siguientes se puede visualizar el efecto de ellos en la construcción.


```python
# Primero se debe dar de alta un FXRateIndex
usd = qcf.QCUSD()
clp = qcf.QCCLP()
usdclp = qcf.FXRate(usd, clp)
one_d = qcf.Tenor('1D')
usdclp_obs = qcf.FXRateIndex(usdclp, 'USDOBS', one_d, one_d, calendario)

# Luego se dan de alta los otros parámetros requeridos para la construcción
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(31, 1, 1969)
fecha_final = qcf.QCDate(31, 1, 1974) 
bus_adj_rule = qcf.BusyAdjRules.MODFOLLOW
periodicidad = qcf.Tenor('6M')
periodo_irregular = qcf.StubPeriod.NO
lag_pago = 0
es_bono = False

# Se da de alta el objeto
fixed_rate_mccy_leg = qcf.LegFactory.build_bullet_fixed_rate_mccy_leg(
    rp,
    fecha_inicio,
    fecha_final,
    bus_adj_rule,
    periodicidad,
    periodo_irregular,
    calendario,
    lag_pago,
    nominal,
    amort_es_flujo,
    tasa_cupon,
    usd,
    clp,
    usdclp_obs,
    0,
    es_bono
)
```


```python
# Se define un list donde almacenar los resultados de la función show
tabla = []
for i in range(0, fixed_rate_mccy_leg.size()):
    tabla.append(qcf.show(fixed_rate_mccy_leg.get_cashflow_at(i)))

# Se utiliza tabla para inicializar el Dataframe
columnas = ['fecha_inicial', 'fecha__final', 'fecha__pago', 'nominal', 'amort', 'interes', 'amort_es_flujo', 'flujo', 'moneda_nominal',
            'valor_tasa', 'tipo_tasa', 'fecha_fijacion_fx', 'moneda_pago', 'indice_fx', 'valor_indice_fx', 'amort_moneda_pago',
           'interes_moneda_pago']
df4 = pd.DataFrame(tabla, columns=columnas)

# Se despliega la data en este formato
df4.style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_1282f">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_1282f_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_1282f_level0_col1" class="col_heading level0 col1" >fecha__final</th>
      <th id="T_1282f_level0_col2" class="col_heading level0 col2" >fecha__pago</th>
      <th id="T_1282f_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_1282f_level0_col4" class="col_heading level0 col4" >amort</th>
      <th id="T_1282f_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_1282f_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_1282f_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_1282f_level0_col8" class="col_heading level0 col8" >moneda_nominal</th>
      <th id="T_1282f_level0_col9" class="col_heading level0 col9" >valor_tasa</th>
      <th id="T_1282f_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
      <th id="T_1282f_level0_col11" class="col_heading level0 col11" >fecha_fijacion_fx</th>
      <th id="T_1282f_level0_col12" class="col_heading level0 col12" >moneda_pago</th>
      <th id="T_1282f_level0_col13" class="col_heading level0 col13" >indice_fx</th>
      <th id="T_1282f_level0_col14" class="col_heading level0 col14" >valor_indice_fx</th>
      <th id="T_1282f_level0_col15" class="col_heading level0 col15" >amort_moneda_pago</th>
      <th id="T_1282f_level0_col16" class="col_heading level0 col16" >interes_moneda_pago</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_1282f_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_1282f_row0_col0" class="data row0 col0" >1969-01-31</td>
      <td id="T_1282f_row0_col1" class="data row0 col1" >1969-07-31</td>
      <td id="T_1282f_row0_col2" class="data row0 col2" >1969-07-31</td>
      <td id="T_1282f_row0_col3" class="data row0 col3" >100,000.00</td>
      <td id="T_1282f_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_1282f_row0_col5" class="data row0 col5" >1,500.00</td>
      <td id="T_1282f_row0_col6" class="data row0 col6" >False</td>
      <td id="T_1282f_row0_col7" class="data row0 col7" >1,500.00</td>
      <td id="T_1282f_row0_col8" class="data row0 col8" >USD</td>
      <td id="T_1282f_row0_col9" class="data row0 col9" >3.0000%</td>
      <td id="T_1282f_row0_col10" class="data row0 col10" >Lin30360</td>
      <td id="T_1282f_row0_col11" class="data row0 col11" >1969-07-31</td>
      <td id="T_1282f_row0_col12" class="data row0 col12" >CLP</td>
      <td id="T_1282f_row0_col13" class="data row0 col13" >USDOBS</td>
      <td id="T_1282f_row0_col14" class="data row0 col14" >1.00</td>
      <td id="T_1282f_row0_col15" class="data row0 col15" >0.00</td>
      <td id="T_1282f_row0_col16" class="data row0 col16" >1,500.00</td>
    </tr>
    <tr>
      <th id="T_1282f_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_1282f_row1_col0" class="data row1 col0" >1969-07-31</td>
      <td id="T_1282f_row1_col1" class="data row1 col1" >1970-01-30</td>
      <td id="T_1282f_row1_col2" class="data row1 col2" >1970-01-30</td>
      <td id="T_1282f_row1_col3" class="data row1 col3" >100,000.00</td>
      <td id="T_1282f_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_1282f_row1_col5" class="data row1 col5" >1,500.00</td>
      <td id="T_1282f_row1_col6" class="data row1 col6" >False</td>
      <td id="T_1282f_row1_col7" class="data row1 col7" >1,500.00</td>
      <td id="T_1282f_row1_col8" class="data row1 col8" >USD</td>
      <td id="T_1282f_row1_col9" class="data row1 col9" >3.0000%</td>
      <td id="T_1282f_row1_col10" class="data row1 col10" >Lin30360</td>
      <td id="T_1282f_row1_col11" class="data row1 col11" >1970-01-30</td>
      <td id="T_1282f_row1_col12" class="data row1 col12" >CLP</td>
      <td id="T_1282f_row1_col13" class="data row1 col13" >USDOBS</td>
      <td id="T_1282f_row1_col14" class="data row1 col14" >1.00</td>
      <td id="T_1282f_row1_col15" class="data row1 col15" >0.00</td>
      <td id="T_1282f_row1_col16" class="data row1 col16" >1,500.00</td>
    </tr>
    <tr>
      <th id="T_1282f_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_1282f_row2_col0" class="data row2 col0" >1970-01-30</td>
      <td id="T_1282f_row2_col1" class="data row2 col1" >1970-07-31</td>
      <td id="T_1282f_row2_col2" class="data row2 col2" >1970-07-31</td>
      <td id="T_1282f_row2_col3" class="data row2 col3" >100,000.00</td>
      <td id="T_1282f_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_1282f_row2_col5" class="data row2 col5" >1,500.00</td>
      <td id="T_1282f_row2_col6" class="data row2 col6" >False</td>
      <td id="T_1282f_row2_col7" class="data row2 col7" >1,500.00</td>
      <td id="T_1282f_row2_col8" class="data row2 col8" >USD</td>
      <td id="T_1282f_row2_col9" class="data row2 col9" >3.0000%</td>
      <td id="T_1282f_row2_col10" class="data row2 col10" >Lin30360</td>
      <td id="T_1282f_row2_col11" class="data row2 col11" >1970-07-31</td>
      <td id="T_1282f_row2_col12" class="data row2 col12" >CLP</td>
      <td id="T_1282f_row2_col13" class="data row2 col13" >USDOBS</td>
      <td id="T_1282f_row2_col14" class="data row2 col14" >1.00</td>
      <td id="T_1282f_row2_col15" class="data row2 col15" >0.00</td>
      <td id="T_1282f_row2_col16" class="data row2 col16" >1,500.00</td>
    </tr>
    <tr>
      <th id="T_1282f_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_1282f_row3_col0" class="data row3 col0" >1970-07-31</td>
      <td id="T_1282f_row3_col1" class="data row3 col1" >1971-01-29</td>
      <td id="T_1282f_row3_col2" class="data row3 col2" >1971-01-29</td>
      <td id="T_1282f_row3_col3" class="data row3 col3" >100,000.00</td>
      <td id="T_1282f_row3_col4" class="data row3 col4" >0.00</td>
      <td id="T_1282f_row3_col5" class="data row3 col5" >1,491.67</td>
      <td id="T_1282f_row3_col6" class="data row3 col6" >False</td>
      <td id="T_1282f_row3_col7" class="data row3 col7" >1,491.67</td>
      <td id="T_1282f_row3_col8" class="data row3 col8" >USD</td>
      <td id="T_1282f_row3_col9" class="data row3 col9" >3.0000%</td>
      <td id="T_1282f_row3_col10" class="data row3 col10" >Lin30360</td>
      <td id="T_1282f_row3_col11" class="data row3 col11" >1971-01-29</td>
      <td id="T_1282f_row3_col12" class="data row3 col12" >CLP</td>
      <td id="T_1282f_row3_col13" class="data row3 col13" >USDOBS</td>
      <td id="T_1282f_row3_col14" class="data row3 col14" >1.00</td>
      <td id="T_1282f_row3_col15" class="data row3 col15" >0.00</td>
      <td id="T_1282f_row3_col16" class="data row3 col16" >1,491.67</td>
    </tr>
    <tr>
      <th id="T_1282f_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_1282f_row4_col0" class="data row4 col0" >1971-01-29</td>
      <td id="T_1282f_row4_col1" class="data row4 col1" >1971-07-30</td>
      <td id="T_1282f_row4_col2" class="data row4 col2" >1971-07-30</td>
      <td id="T_1282f_row4_col3" class="data row4 col3" >100,000.00</td>
      <td id="T_1282f_row4_col4" class="data row4 col4" >0.00</td>
      <td id="T_1282f_row4_col5" class="data row4 col5" >1,508.33</td>
      <td id="T_1282f_row4_col6" class="data row4 col6" >False</td>
      <td id="T_1282f_row4_col7" class="data row4 col7" >1,508.33</td>
      <td id="T_1282f_row4_col8" class="data row4 col8" >USD</td>
      <td id="T_1282f_row4_col9" class="data row4 col9" >3.0000%</td>
      <td id="T_1282f_row4_col10" class="data row4 col10" >Lin30360</td>
      <td id="T_1282f_row4_col11" class="data row4 col11" >1971-07-30</td>
      <td id="T_1282f_row4_col12" class="data row4 col12" >CLP</td>
      <td id="T_1282f_row4_col13" class="data row4 col13" >USDOBS</td>
      <td id="T_1282f_row4_col14" class="data row4 col14" >1.00</td>
      <td id="T_1282f_row4_col15" class="data row4 col15" >0.00</td>
      <td id="T_1282f_row4_col16" class="data row4 col16" >1,508.33</td>
    </tr>
    <tr>
      <th id="T_1282f_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_1282f_row5_col0" class="data row5 col0" >1971-07-30</td>
      <td id="T_1282f_row5_col1" class="data row5 col1" >1972-01-31</td>
      <td id="T_1282f_row5_col2" class="data row5 col2" >1972-01-31</td>
      <td id="T_1282f_row5_col3" class="data row5 col3" >100,000.00</td>
      <td id="T_1282f_row5_col4" class="data row5 col4" >0.00</td>
      <td id="T_1282f_row5_col5" class="data row5 col5" >1,500.00</td>
      <td id="T_1282f_row5_col6" class="data row5 col6" >False</td>
      <td id="T_1282f_row5_col7" class="data row5 col7" >1,500.00</td>
      <td id="T_1282f_row5_col8" class="data row5 col8" >USD</td>
      <td id="T_1282f_row5_col9" class="data row5 col9" >3.0000%</td>
      <td id="T_1282f_row5_col10" class="data row5 col10" >Lin30360</td>
      <td id="T_1282f_row5_col11" class="data row5 col11" >1972-01-31</td>
      <td id="T_1282f_row5_col12" class="data row5 col12" >CLP</td>
      <td id="T_1282f_row5_col13" class="data row5 col13" >USDOBS</td>
      <td id="T_1282f_row5_col14" class="data row5 col14" >1.00</td>
      <td id="T_1282f_row5_col15" class="data row5 col15" >0.00</td>
      <td id="T_1282f_row5_col16" class="data row5 col16" >1,500.00</td>
    </tr>
    <tr>
      <th id="T_1282f_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_1282f_row6_col0" class="data row6 col0" >1972-01-31</td>
      <td id="T_1282f_row6_col1" class="data row6 col1" >1972-07-31</td>
      <td id="T_1282f_row6_col2" class="data row6 col2" >1972-07-31</td>
      <td id="T_1282f_row6_col3" class="data row6 col3" >100,000.00</td>
      <td id="T_1282f_row6_col4" class="data row6 col4" >0.00</td>
      <td id="T_1282f_row6_col5" class="data row6 col5" >1,500.00</td>
      <td id="T_1282f_row6_col6" class="data row6 col6" >False</td>
      <td id="T_1282f_row6_col7" class="data row6 col7" >1,500.00</td>
      <td id="T_1282f_row6_col8" class="data row6 col8" >USD</td>
      <td id="T_1282f_row6_col9" class="data row6 col9" >3.0000%</td>
      <td id="T_1282f_row6_col10" class="data row6 col10" >Lin30360</td>
      <td id="T_1282f_row6_col11" class="data row6 col11" >1972-07-31</td>
      <td id="T_1282f_row6_col12" class="data row6 col12" >CLP</td>
      <td id="T_1282f_row6_col13" class="data row6 col13" >USDOBS</td>
      <td id="T_1282f_row6_col14" class="data row6 col14" >1.00</td>
      <td id="T_1282f_row6_col15" class="data row6 col15" >0.00</td>
      <td id="T_1282f_row6_col16" class="data row6 col16" >1,500.00</td>
    </tr>
    <tr>
      <th id="T_1282f_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_1282f_row7_col0" class="data row7 col0" >1972-07-31</td>
      <td id="T_1282f_row7_col1" class="data row7 col1" >1973-01-31</td>
      <td id="T_1282f_row7_col2" class="data row7 col2" >1973-01-31</td>
      <td id="T_1282f_row7_col3" class="data row7 col3" >100,000.00</td>
      <td id="T_1282f_row7_col4" class="data row7 col4" >0.00</td>
      <td id="T_1282f_row7_col5" class="data row7 col5" >1,500.00</td>
      <td id="T_1282f_row7_col6" class="data row7 col6" >False</td>
      <td id="T_1282f_row7_col7" class="data row7 col7" >1,500.00</td>
      <td id="T_1282f_row7_col8" class="data row7 col8" >USD</td>
      <td id="T_1282f_row7_col9" class="data row7 col9" >3.0000%</td>
      <td id="T_1282f_row7_col10" class="data row7 col10" >Lin30360</td>
      <td id="T_1282f_row7_col11" class="data row7 col11" >1973-01-31</td>
      <td id="T_1282f_row7_col12" class="data row7 col12" >CLP</td>
      <td id="T_1282f_row7_col13" class="data row7 col13" >USDOBS</td>
      <td id="T_1282f_row7_col14" class="data row7 col14" >1.00</td>
      <td id="T_1282f_row7_col15" class="data row7 col15" >0.00</td>
      <td id="T_1282f_row7_col16" class="data row7 col16" >1,500.00</td>
    </tr>
    <tr>
      <th id="T_1282f_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_1282f_row8_col0" class="data row8 col0" >1973-01-31</td>
      <td id="T_1282f_row8_col1" class="data row8 col1" >1973-07-31</td>
      <td id="T_1282f_row8_col2" class="data row8 col2" >1973-07-31</td>
      <td id="T_1282f_row8_col3" class="data row8 col3" >100,000.00</td>
      <td id="T_1282f_row8_col4" class="data row8 col4" >0.00</td>
      <td id="T_1282f_row8_col5" class="data row8 col5" >1,500.00</td>
      <td id="T_1282f_row8_col6" class="data row8 col6" >False</td>
      <td id="T_1282f_row8_col7" class="data row8 col7" >1,500.00</td>
      <td id="T_1282f_row8_col8" class="data row8 col8" >USD</td>
      <td id="T_1282f_row8_col9" class="data row8 col9" >3.0000%</td>
      <td id="T_1282f_row8_col10" class="data row8 col10" >Lin30360</td>
      <td id="T_1282f_row8_col11" class="data row8 col11" >1973-07-31</td>
      <td id="T_1282f_row8_col12" class="data row8 col12" >CLP</td>
      <td id="T_1282f_row8_col13" class="data row8 col13" >USDOBS</td>
      <td id="T_1282f_row8_col14" class="data row8 col14" >1.00</td>
      <td id="T_1282f_row8_col15" class="data row8 col15" >0.00</td>
      <td id="T_1282f_row8_col16" class="data row8 col16" >1,500.00</td>
    </tr>
    <tr>
      <th id="T_1282f_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_1282f_row9_col0" class="data row9 col0" >1973-07-31</td>
      <td id="T_1282f_row9_col1" class="data row9 col1" >1974-01-31</td>
      <td id="T_1282f_row9_col2" class="data row9 col2" >1974-01-31</td>
      <td id="T_1282f_row9_col3" class="data row9 col3" >100,000.00</td>
      <td id="T_1282f_row9_col4" class="data row9 col4" >100,000.00</td>
      <td id="T_1282f_row9_col5" class="data row9 col5" >1,500.00</td>
      <td id="T_1282f_row9_col6" class="data row9 col6" >False</td>
      <td id="T_1282f_row9_col7" class="data row9 col7" >1,500.00</td>
      <td id="T_1282f_row9_col8" class="data row9 col8" >USD</td>
      <td id="T_1282f_row9_col9" class="data row9 col9" >3.0000%</td>
      <td id="T_1282f_row9_col10" class="data row9 col10" >Lin30360</td>
      <td id="T_1282f_row9_col11" class="data row9 col11" >1974-01-31</td>
      <td id="T_1282f_row9_col12" class="data row9 col12" >CLP</td>
      <td id="T_1282f_row9_col13" class="data row9 col13" >USDOBS</td>
      <td id="T_1282f_row9_col14" class="data row9 col14" >1.00</td>
      <td id="T_1282f_row9_col15" class="data row9 col15" >100,000.00</td>
      <td id="T_1282f_row9_col16" class="data row9 col16" >1,500.00</td>
    </tr>
  </tbody>
</table>




### Construcción Asistida de un `BulletIborLeg`
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
- `gearing`: spread multiplicativo

Vamos a un ejemplo. Cambiando los parámetros anteriores se puede visualizar el efecto de ellos en la construcción. 

**NOTA:** para construir un `Leg` con `IborCashflow` y amortización customizada, sólo se debe cambiar el parámetro **nominal** por **CustomNotionalAndAmort** e invocar el método `qcf.LegFactory.build_custom_amort_ibor_leg(...)`.


```python
# Se da de alta los parámetros requeridos
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(31, 1, 1969)
fecha_final = qcf.QCDate(31, 1, 1971) 
bus_adj_rule = qcf.BusyAdjRules.MODFOLLOW
periodicidad_pago = qcf.Tenor('3M')
periodo_irregular_pago = qcf.StubPeriod.NO
calendario = qcf.BusinessCalendar(fecha_inicio, 20)
lag_pago = 0
periodicidad_fijacion = qcf.Tenor('3M')
periodo_irregular_fijacion = qcf.StubPeriod.NO

# vamos a usar el mismo calendario para pago y fijaciones
lag_de_fijacion = 2

# Definición del índice
codigo = 'LIBORUSD3M'
lin_act360 = qcf.QCInterestRate(.0, qcf.QCAct360(), qcf.QCLinearWf())
fixing_lag = qcf.Tenor('2d')
tenor = qcf.Tenor('3m')
fixing_calendar = calendario
settlement_calendar = calendario
usd = qcf.QCUSD()
libor_usd_3m = qcf.InterestRateIndex(
    codigo,
    lin_act360,
    fixing_lag,
    tenor,
    fixing_calendar,
    settlement_calendar,
    usd
)
# Fin índice

nominal = 1000000.0
amort_es_flujo = True 
moneda = usd
spread = .01
gearing = 1.0

ibor_leg = qcf.LegFactory.build_bullet_ibor2_leg(
    rp, 
    fecha_inicio, 
    fecha_final, 
    bus_adj_rule, 
    periodicidad_pago,
    periodo_irregular_pago, 
    calendario, lag_pago,
    periodicidad_fijacion, 
    periodo_irregular_fijacion,
    calendario, 
    lag_de_fijacion, 
    libor_usd_3m,
    nominal, 
    amort_es_flujo, 
    moneda, 
    spread, 
    gearing
)
```


```python
# Se define un list donde almacenar los resultados de la función show
tabla = []
for i in range(0, ibor_leg.size()):
    tabla.append(qcf.show(ibor_leg.get_cashflow_at(i)))

# Se utiliza tabla para inicializar el Dataframe
columnas = ['fecha_inicial', 'fecha__final', 'fecha_fixing', 'fecha__pago', 'nominal', 'amort', 'interes', 'amort_es_flujo', 'flujo',
            'moneda', 'codigo_indice', 'valor_tasa', 'spread', 'gearing', 'tipo_tasa']
df5 = pd.DataFrame(tabla, columns=columnas)

# Se despliega la data en este formato
df5.style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_b6042">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_b6042_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_b6042_level0_col1" class="col_heading level0 col1" >fecha__final</th>
      <th id="T_b6042_level0_col2" class="col_heading level0 col2" >fecha_fixing</th>
      <th id="T_b6042_level0_col3" class="col_heading level0 col3" >fecha__pago</th>
      <th id="T_b6042_level0_col4" class="col_heading level0 col4" >nominal</th>
      <th id="T_b6042_level0_col5" class="col_heading level0 col5" >amort</th>
      <th id="T_b6042_level0_col6" class="col_heading level0 col6" >interes</th>
      <th id="T_b6042_level0_col7" class="col_heading level0 col7" >amort_es_flujo</th>
      <th id="T_b6042_level0_col8" class="col_heading level0 col8" >flujo</th>
      <th id="T_b6042_level0_col9" class="col_heading level0 col9" >moneda</th>
      <th id="T_b6042_level0_col10" class="col_heading level0 col10" >codigo_indice</th>
      <th id="T_b6042_level0_col11" class="col_heading level0 col11" >valor_tasa</th>
      <th id="T_b6042_level0_col12" class="col_heading level0 col12" >spread</th>
      <th id="T_b6042_level0_col13" class="col_heading level0 col13" >gearing</th>
      <th id="T_b6042_level0_col14" class="col_heading level0 col14" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_b6042_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_b6042_row0_col0" class="data row0 col0" >1969-01-31</td>
      <td id="T_b6042_row0_col1" class="data row0 col1" >1969-04-30</td>
      <td id="T_b6042_row0_col2" class="data row0 col2" >1969-01-29</td>
      <td id="T_b6042_row0_col3" class="data row0 col3" >1969-04-30</td>
      <td id="T_b6042_row0_col4" class="data row0 col4" >1,000,000.00</td>
      <td id="T_b6042_row0_col5" class="data row0 col5" >0.00</td>
      <td id="T_b6042_row0_col6" class="data row0 col6" >2,472.22</td>
      <td id="T_b6042_row0_col7" class="data row0 col7" >True</td>
      <td id="T_b6042_row0_col8" class="data row0 col8" >2,472.22</td>
      <td id="T_b6042_row0_col9" class="data row0 col9" >USD</td>
      <td id="T_b6042_row0_col10" class="data row0 col10" >LIBORUSD3M</td>
      <td id="T_b6042_row0_col11" class="data row0 col11" >0.0000%</td>
      <td id="T_b6042_row0_col12" class="data row0 col12" >1.0000%</td>
      <td id="T_b6042_row0_col13" class="data row0 col13" >1.00</td>
      <td id="T_b6042_row0_col14" class="data row0 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_b6042_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_b6042_row1_col0" class="data row1 col0" >1969-04-30</td>
      <td id="T_b6042_row1_col1" class="data row1 col1" >1969-07-31</td>
      <td id="T_b6042_row1_col2" class="data row1 col2" >1969-04-28</td>
      <td id="T_b6042_row1_col3" class="data row1 col3" >1969-07-31</td>
      <td id="T_b6042_row1_col4" class="data row1 col4" >1,000,000.00</td>
      <td id="T_b6042_row1_col5" class="data row1 col5" >0.00</td>
      <td id="T_b6042_row1_col6" class="data row1 col6" >2,555.56</td>
      <td id="T_b6042_row1_col7" class="data row1 col7" >True</td>
      <td id="T_b6042_row1_col8" class="data row1 col8" >2,555.56</td>
      <td id="T_b6042_row1_col9" class="data row1 col9" >USD</td>
      <td id="T_b6042_row1_col10" class="data row1 col10" >LIBORUSD3M</td>
      <td id="T_b6042_row1_col11" class="data row1 col11" >0.0000%</td>
      <td id="T_b6042_row1_col12" class="data row1 col12" >1.0000%</td>
      <td id="T_b6042_row1_col13" class="data row1 col13" >1.00</td>
      <td id="T_b6042_row1_col14" class="data row1 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_b6042_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_b6042_row2_col0" class="data row2 col0" >1969-07-31</td>
      <td id="T_b6042_row2_col1" class="data row2 col1" >1969-10-31</td>
      <td id="T_b6042_row2_col2" class="data row2 col2" >1969-07-29</td>
      <td id="T_b6042_row2_col3" class="data row2 col3" >1969-10-31</td>
      <td id="T_b6042_row2_col4" class="data row2 col4" >1,000,000.00</td>
      <td id="T_b6042_row2_col5" class="data row2 col5" >0.00</td>
      <td id="T_b6042_row2_col6" class="data row2 col6" >2,555.56</td>
      <td id="T_b6042_row2_col7" class="data row2 col7" >True</td>
      <td id="T_b6042_row2_col8" class="data row2 col8" >2,555.56</td>
      <td id="T_b6042_row2_col9" class="data row2 col9" >USD</td>
      <td id="T_b6042_row2_col10" class="data row2 col10" >LIBORUSD3M</td>
      <td id="T_b6042_row2_col11" class="data row2 col11" >0.0000%</td>
      <td id="T_b6042_row2_col12" class="data row2 col12" >1.0000%</td>
      <td id="T_b6042_row2_col13" class="data row2 col13" >1.00</td>
      <td id="T_b6042_row2_col14" class="data row2 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_b6042_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_b6042_row3_col0" class="data row3 col0" >1969-10-31</td>
      <td id="T_b6042_row3_col1" class="data row3 col1" >1970-01-30</td>
      <td id="T_b6042_row3_col2" class="data row3 col2" >1969-10-29</td>
      <td id="T_b6042_row3_col3" class="data row3 col3" >1970-01-30</td>
      <td id="T_b6042_row3_col4" class="data row3 col4" >1,000,000.00</td>
      <td id="T_b6042_row3_col5" class="data row3 col5" >0.00</td>
      <td id="T_b6042_row3_col6" class="data row3 col6" >2,527.78</td>
      <td id="T_b6042_row3_col7" class="data row3 col7" >True</td>
      <td id="T_b6042_row3_col8" class="data row3 col8" >2,527.78</td>
      <td id="T_b6042_row3_col9" class="data row3 col9" >USD</td>
      <td id="T_b6042_row3_col10" class="data row3 col10" >LIBORUSD3M</td>
      <td id="T_b6042_row3_col11" class="data row3 col11" >0.0000%</td>
      <td id="T_b6042_row3_col12" class="data row3 col12" >1.0000%</td>
      <td id="T_b6042_row3_col13" class="data row3 col13" >1.00</td>
      <td id="T_b6042_row3_col14" class="data row3 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_b6042_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_b6042_row4_col0" class="data row4 col0" >1970-01-30</td>
      <td id="T_b6042_row4_col1" class="data row4 col1" >1970-04-30</td>
      <td id="T_b6042_row4_col2" class="data row4 col2" >1970-01-28</td>
      <td id="T_b6042_row4_col3" class="data row4 col3" >1970-04-30</td>
      <td id="T_b6042_row4_col4" class="data row4 col4" >1,000,000.00</td>
      <td id="T_b6042_row4_col5" class="data row4 col5" >0.00</td>
      <td id="T_b6042_row4_col6" class="data row4 col6" >2,500.00</td>
      <td id="T_b6042_row4_col7" class="data row4 col7" >True</td>
      <td id="T_b6042_row4_col8" class="data row4 col8" >2,500.00</td>
      <td id="T_b6042_row4_col9" class="data row4 col9" >USD</td>
      <td id="T_b6042_row4_col10" class="data row4 col10" >LIBORUSD3M</td>
      <td id="T_b6042_row4_col11" class="data row4 col11" >0.0000%</td>
      <td id="T_b6042_row4_col12" class="data row4 col12" >1.0000%</td>
      <td id="T_b6042_row4_col13" class="data row4 col13" >1.00</td>
      <td id="T_b6042_row4_col14" class="data row4 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_b6042_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_b6042_row5_col0" class="data row5 col0" >1970-04-30</td>
      <td id="T_b6042_row5_col1" class="data row5 col1" >1970-07-31</td>
      <td id="T_b6042_row5_col2" class="data row5 col2" >1970-04-28</td>
      <td id="T_b6042_row5_col3" class="data row5 col3" >1970-07-31</td>
      <td id="T_b6042_row5_col4" class="data row5 col4" >1,000,000.00</td>
      <td id="T_b6042_row5_col5" class="data row5 col5" >0.00</td>
      <td id="T_b6042_row5_col6" class="data row5 col6" >2,555.56</td>
      <td id="T_b6042_row5_col7" class="data row5 col7" >True</td>
      <td id="T_b6042_row5_col8" class="data row5 col8" >2,555.56</td>
      <td id="T_b6042_row5_col9" class="data row5 col9" >USD</td>
      <td id="T_b6042_row5_col10" class="data row5 col10" >LIBORUSD3M</td>
      <td id="T_b6042_row5_col11" class="data row5 col11" >0.0000%</td>
      <td id="T_b6042_row5_col12" class="data row5 col12" >1.0000%</td>
      <td id="T_b6042_row5_col13" class="data row5 col13" >1.00</td>
      <td id="T_b6042_row5_col14" class="data row5 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_b6042_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_b6042_row6_col0" class="data row6 col0" >1970-07-31</td>
      <td id="T_b6042_row6_col1" class="data row6 col1" >1970-10-30</td>
      <td id="T_b6042_row6_col2" class="data row6 col2" >1970-07-29</td>
      <td id="T_b6042_row6_col3" class="data row6 col3" >1970-10-30</td>
      <td id="T_b6042_row6_col4" class="data row6 col4" >1,000,000.00</td>
      <td id="T_b6042_row6_col5" class="data row6 col5" >0.00</td>
      <td id="T_b6042_row6_col6" class="data row6 col6" >2,527.78</td>
      <td id="T_b6042_row6_col7" class="data row6 col7" >True</td>
      <td id="T_b6042_row6_col8" class="data row6 col8" >2,527.78</td>
      <td id="T_b6042_row6_col9" class="data row6 col9" >USD</td>
      <td id="T_b6042_row6_col10" class="data row6 col10" >LIBORUSD3M</td>
      <td id="T_b6042_row6_col11" class="data row6 col11" >0.0000%</td>
      <td id="T_b6042_row6_col12" class="data row6 col12" >1.0000%</td>
      <td id="T_b6042_row6_col13" class="data row6 col13" >1.00</td>
      <td id="T_b6042_row6_col14" class="data row6 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_b6042_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_b6042_row7_col0" class="data row7 col0" >1970-10-30</td>
      <td id="T_b6042_row7_col1" class="data row7 col1" >1971-01-29</td>
      <td id="T_b6042_row7_col2" class="data row7 col2" >1970-10-28</td>
      <td id="T_b6042_row7_col3" class="data row7 col3" >1971-01-29</td>
      <td id="T_b6042_row7_col4" class="data row7 col4" >1,000,000.00</td>
      <td id="T_b6042_row7_col5" class="data row7 col5" >1,000,000.00</td>
      <td id="T_b6042_row7_col6" class="data row7 col6" >2,527.78</td>
      <td id="T_b6042_row7_col7" class="data row7 col7" >True</td>
      <td id="T_b6042_row7_col8" class="data row7 col8" >1,002,527.78</td>
      <td id="T_b6042_row7_col9" class="data row7 col9" >USD</td>
      <td id="T_b6042_row7_col10" class="data row7 col10" >LIBORUSD3M</td>
      <td id="T_b6042_row7_col11" class="data row7 col11" >0.0000%</td>
      <td id="T_b6042_row7_col12" class="data row7 col12" >1.0000%</td>
      <td id="T_b6042_row7_col13" class="data row7 col13" >1.00</td>
      <td id="T_b6042_row7_col14" class="data row7 col14" >LinAct360</td>
    </tr>
  </tbody>
</table>




### Construcción Asistida de un `BulletIborMultiCurrencyLeg`
En este ejemplo se construye un `Leg` con `IborMultiCurrencyCashflow` y amortización bullet.
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
- `InterestRateIndex`: índice de tasa de interés utilizado en cada `IborMultiCurrencyCashflow`
- `float`: nominal
- `bool`: si es `True` significa que la amortización final es un flujo de caja efectivo
- `QCCurrency`: moneda del nominal
- `float`: spread aditivo
- `gearing`: spread multiplicativo
- `QCCurrency`: moneda del nominal
- `QCCurrency`: moneda de pago los flujos
- `FXRateIndex`: índice con el cual se transforma cada flujo a la moneda de pago
- `int`: lag de fijación del FXRateIndex (respecto a settlement date)

Vamos a un ejemplo. Cambiando los parámetros anteriores se puede visualizar el efecto de ellos en la construcción. 


```python
ibor_mccy_leg = qcf.LegFactory.build_bullet_ibor_mccy_leg(
    rp, 
    fecha_inicio, 
    fecha_final, 
    bus_adj_rule, 
    periodicidad_pago,
    periodo_irregular_pago, 
    calendario, 
    lag_pago,
    periodicidad_fijacion, 
    periodo_irregular_fijacion,
    calendario, 
    lag_de_fijacion, 
    libor_usd_3m,
    nominal, 
    amort_es_flujo, 
    usd, 
    spread, 
    gearing,
    clp, 
    usdclp_obs, 
    0
)
```


```python
# Se define un list donde almacenar los resultados de la función show
tabla = []
for i in range(0, ibor_mccy_leg.size()):
    ibor_mccy_leg.get_cashflow_at(i).set_fx_rate_index_value(10.0)
    tabla.append(qcf.show(ibor_mccy_leg.get_cashflow_at(i)))

# Se utiliza tabla para inicializar el Dataframe
columnas = ['fecha_inicial', 'fecha__final', 'fecha_fixing', 'fecha__pago',
            'nominal', 'amort', 'interes', 'amort_es_flujo', 'flujo',
            'moneda_nominal', 'codigo_indice_tasa', 'spread', 'gearing', 'valor_tasa', 'tipo_tasa',
            'fecha_fijacion_fx', 'moneda_pago', 'codigo_indice_fx', 'valor_indice_fx',
            'amort_moneda_pago', 'interes_moneda_pago']
df6 = pd.DataFrame(tabla, columns=columnas)

# Se despliega la data en este formato
df6.style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_bf872">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_bf872_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_bf872_level0_col1" class="col_heading level0 col1" >fecha__final</th>
      <th id="T_bf872_level0_col2" class="col_heading level0 col2" >fecha_fixing</th>
      <th id="T_bf872_level0_col3" class="col_heading level0 col3" >fecha__pago</th>
      <th id="T_bf872_level0_col4" class="col_heading level0 col4" >nominal</th>
      <th id="T_bf872_level0_col5" class="col_heading level0 col5" >amort</th>
      <th id="T_bf872_level0_col6" class="col_heading level0 col6" >interes</th>
      <th id="T_bf872_level0_col7" class="col_heading level0 col7" >amort_es_flujo</th>
      <th id="T_bf872_level0_col8" class="col_heading level0 col8" >flujo</th>
      <th id="T_bf872_level0_col9" class="col_heading level0 col9" >moneda_nominal</th>
      <th id="T_bf872_level0_col10" class="col_heading level0 col10" >codigo_indice_tasa</th>
      <th id="T_bf872_level0_col11" class="col_heading level0 col11" >spread</th>
      <th id="T_bf872_level0_col12" class="col_heading level0 col12" >gearing</th>
      <th id="T_bf872_level0_col13" class="col_heading level0 col13" >valor_tasa</th>
      <th id="T_bf872_level0_col14" class="col_heading level0 col14" >tipo_tasa</th>
      <th id="T_bf872_level0_col15" class="col_heading level0 col15" >fecha_fijacion_fx</th>
      <th id="T_bf872_level0_col16" class="col_heading level0 col16" >moneda_pago</th>
      <th id="T_bf872_level0_col17" class="col_heading level0 col17" >codigo_indice_fx</th>
      <th id="T_bf872_level0_col18" class="col_heading level0 col18" >valor_indice_fx</th>
      <th id="T_bf872_level0_col19" class="col_heading level0 col19" >amort_moneda_pago</th>
      <th id="T_bf872_level0_col20" class="col_heading level0 col20" >interes_moneda_pago</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_bf872_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_bf872_row0_col0" class="data row0 col0" >1969-01-31</td>
      <td id="T_bf872_row0_col1" class="data row0 col1" >1969-04-30</td>
      <td id="T_bf872_row0_col2" class="data row0 col2" >1969-01-29</td>
      <td id="T_bf872_row0_col3" class="data row0 col3" >1969-04-30</td>
      <td id="T_bf872_row0_col4" class="data row0 col4" >1,000,000.00</td>
      <td id="T_bf872_row0_col5" class="data row0 col5" >0.00</td>
      <td id="T_bf872_row0_col6" class="data row0 col6" >2,472.22</td>
      <td id="T_bf872_row0_col7" class="data row0 col7" >True</td>
      <td id="T_bf872_row0_col8" class="data row0 col8" >24,722.22</td>
      <td id="T_bf872_row0_col9" class="data row0 col9" >USD</td>
      <td id="T_bf872_row0_col10" class="data row0 col10" >LIBORUSD3M</td>
      <td id="T_bf872_row0_col11" class="data row0 col11" >1.0000%</td>
      <td id="T_bf872_row0_col12" class="data row0 col12" >1.00</td>
      <td id="T_bf872_row0_col13" class="data row0 col13" >0.0000%</td>
      <td id="T_bf872_row0_col14" class="data row0 col14" >LinAct360</td>
      <td id="T_bf872_row0_col15" class="data row0 col15" >1969-04-30</td>
      <td id="T_bf872_row0_col16" class="data row0 col16" >CLP</td>
      <td id="T_bf872_row0_col17" class="data row0 col17" >USDOBS</td>
      <td id="T_bf872_row0_col18" class="data row0 col18" >10.00</td>
      <td id="T_bf872_row0_col19" class="data row0 col19" >0.00</td>
      <td id="T_bf872_row0_col20" class="data row0 col20" >24,722.22</td>
    </tr>
    <tr>
      <th id="T_bf872_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_bf872_row1_col0" class="data row1 col0" >1969-04-30</td>
      <td id="T_bf872_row1_col1" class="data row1 col1" >1969-07-31</td>
      <td id="T_bf872_row1_col2" class="data row1 col2" >1969-04-28</td>
      <td id="T_bf872_row1_col3" class="data row1 col3" >1969-07-31</td>
      <td id="T_bf872_row1_col4" class="data row1 col4" >1,000,000.00</td>
      <td id="T_bf872_row1_col5" class="data row1 col5" >0.00</td>
      <td id="T_bf872_row1_col6" class="data row1 col6" >2,555.56</td>
      <td id="T_bf872_row1_col7" class="data row1 col7" >True</td>
      <td id="T_bf872_row1_col8" class="data row1 col8" >25,555.56</td>
      <td id="T_bf872_row1_col9" class="data row1 col9" >USD</td>
      <td id="T_bf872_row1_col10" class="data row1 col10" >LIBORUSD3M</td>
      <td id="T_bf872_row1_col11" class="data row1 col11" >1.0000%</td>
      <td id="T_bf872_row1_col12" class="data row1 col12" >1.00</td>
      <td id="T_bf872_row1_col13" class="data row1 col13" >0.0000%</td>
      <td id="T_bf872_row1_col14" class="data row1 col14" >LinAct360</td>
      <td id="T_bf872_row1_col15" class="data row1 col15" >1969-07-31</td>
      <td id="T_bf872_row1_col16" class="data row1 col16" >CLP</td>
      <td id="T_bf872_row1_col17" class="data row1 col17" >USDOBS</td>
      <td id="T_bf872_row1_col18" class="data row1 col18" >10.00</td>
      <td id="T_bf872_row1_col19" class="data row1 col19" >0.00</td>
      <td id="T_bf872_row1_col20" class="data row1 col20" >25,555.56</td>
    </tr>
    <tr>
      <th id="T_bf872_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_bf872_row2_col0" class="data row2 col0" >1969-07-31</td>
      <td id="T_bf872_row2_col1" class="data row2 col1" >1969-10-31</td>
      <td id="T_bf872_row2_col2" class="data row2 col2" >1969-07-29</td>
      <td id="T_bf872_row2_col3" class="data row2 col3" >1969-10-31</td>
      <td id="T_bf872_row2_col4" class="data row2 col4" >1,000,000.00</td>
      <td id="T_bf872_row2_col5" class="data row2 col5" >0.00</td>
      <td id="T_bf872_row2_col6" class="data row2 col6" >2,555.56</td>
      <td id="T_bf872_row2_col7" class="data row2 col7" >True</td>
      <td id="T_bf872_row2_col8" class="data row2 col8" >25,555.56</td>
      <td id="T_bf872_row2_col9" class="data row2 col9" >USD</td>
      <td id="T_bf872_row2_col10" class="data row2 col10" >LIBORUSD3M</td>
      <td id="T_bf872_row2_col11" class="data row2 col11" >1.0000%</td>
      <td id="T_bf872_row2_col12" class="data row2 col12" >1.00</td>
      <td id="T_bf872_row2_col13" class="data row2 col13" >0.0000%</td>
      <td id="T_bf872_row2_col14" class="data row2 col14" >LinAct360</td>
      <td id="T_bf872_row2_col15" class="data row2 col15" >1969-10-31</td>
      <td id="T_bf872_row2_col16" class="data row2 col16" >CLP</td>
      <td id="T_bf872_row2_col17" class="data row2 col17" >USDOBS</td>
      <td id="T_bf872_row2_col18" class="data row2 col18" >10.00</td>
      <td id="T_bf872_row2_col19" class="data row2 col19" >0.00</td>
      <td id="T_bf872_row2_col20" class="data row2 col20" >25,555.56</td>
    </tr>
    <tr>
      <th id="T_bf872_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_bf872_row3_col0" class="data row3 col0" >1969-10-31</td>
      <td id="T_bf872_row3_col1" class="data row3 col1" >1970-01-30</td>
      <td id="T_bf872_row3_col2" class="data row3 col2" >1969-10-29</td>
      <td id="T_bf872_row3_col3" class="data row3 col3" >1970-01-30</td>
      <td id="T_bf872_row3_col4" class="data row3 col4" >1,000,000.00</td>
      <td id="T_bf872_row3_col5" class="data row3 col5" >0.00</td>
      <td id="T_bf872_row3_col6" class="data row3 col6" >2,527.78</td>
      <td id="T_bf872_row3_col7" class="data row3 col7" >True</td>
      <td id="T_bf872_row3_col8" class="data row3 col8" >25,277.78</td>
      <td id="T_bf872_row3_col9" class="data row3 col9" >USD</td>
      <td id="T_bf872_row3_col10" class="data row3 col10" >LIBORUSD3M</td>
      <td id="T_bf872_row3_col11" class="data row3 col11" >1.0000%</td>
      <td id="T_bf872_row3_col12" class="data row3 col12" >1.00</td>
      <td id="T_bf872_row3_col13" class="data row3 col13" >0.0000%</td>
      <td id="T_bf872_row3_col14" class="data row3 col14" >LinAct360</td>
      <td id="T_bf872_row3_col15" class="data row3 col15" >1970-01-30</td>
      <td id="T_bf872_row3_col16" class="data row3 col16" >CLP</td>
      <td id="T_bf872_row3_col17" class="data row3 col17" >USDOBS</td>
      <td id="T_bf872_row3_col18" class="data row3 col18" >10.00</td>
      <td id="T_bf872_row3_col19" class="data row3 col19" >0.00</td>
      <td id="T_bf872_row3_col20" class="data row3 col20" >25,277.78</td>
    </tr>
    <tr>
      <th id="T_bf872_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_bf872_row4_col0" class="data row4 col0" >1970-01-30</td>
      <td id="T_bf872_row4_col1" class="data row4 col1" >1970-04-30</td>
      <td id="T_bf872_row4_col2" class="data row4 col2" >1970-01-28</td>
      <td id="T_bf872_row4_col3" class="data row4 col3" >1970-04-30</td>
      <td id="T_bf872_row4_col4" class="data row4 col4" >1,000,000.00</td>
      <td id="T_bf872_row4_col5" class="data row4 col5" >0.00</td>
      <td id="T_bf872_row4_col6" class="data row4 col6" >2,500.00</td>
      <td id="T_bf872_row4_col7" class="data row4 col7" >True</td>
      <td id="T_bf872_row4_col8" class="data row4 col8" >25,000.00</td>
      <td id="T_bf872_row4_col9" class="data row4 col9" >USD</td>
      <td id="T_bf872_row4_col10" class="data row4 col10" >LIBORUSD3M</td>
      <td id="T_bf872_row4_col11" class="data row4 col11" >1.0000%</td>
      <td id="T_bf872_row4_col12" class="data row4 col12" >1.00</td>
      <td id="T_bf872_row4_col13" class="data row4 col13" >0.0000%</td>
      <td id="T_bf872_row4_col14" class="data row4 col14" >LinAct360</td>
      <td id="T_bf872_row4_col15" class="data row4 col15" >1970-04-30</td>
      <td id="T_bf872_row4_col16" class="data row4 col16" >CLP</td>
      <td id="T_bf872_row4_col17" class="data row4 col17" >USDOBS</td>
      <td id="T_bf872_row4_col18" class="data row4 col18" >10.00</td>
      <td id="T_bf872_row4_col19" class="data row4 col19" >0.00</td>
      <td id="T_bf872_row4_col20" class="data row4 col20" >25,000.00</td>
    </tr>
    <tr>
      <th id="T_bf872_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_bf872_row5_col0" class="data row5 col0" >1970-04-30</td>
      <td id="T_bf872_row5_col1" class="data row5 col1" >1970-07-31</td>
      <td id="T_bf872_row5_col2" class="data row5 col2" >1970-04-28</td>
      <td id="T_bf872_row5_col3" class="data row5 col3" >1970-07-31</td>
      <td id="T_bf872_row5_col4" class="data row5 col4" >1,000,000.00</td>
      <td id="T_bf872_row5_col5" class="data row5 col5" >0.00</td>
      <td id="T_bf872_row5_col6" class="data row5 col6" >2,555.56</td>
      <td id="T_bf872_row5_col7" class="data row5 col7" >True</td>
      <td id="T_bf872_row5_col8" class="data row5 col8" >25,555.56</td>
      <td id="T_bf872_row5_col9" class="data row5 col9" >USD</td>
      <td id="T_bf872_row5_col10" class="data row5 col10" >LIBORUSD3M</td>
      <td id="T_bf872_row5_col11" class="data row5 col11" >1.0000%</td>
      <td id="T_bf872_row5_col12" class="data row5 col12" >1.00</td>
      <td id="T_bf872_row5_col13" class="data row5 col13" >0.0000%</td>
      <td id="T_bf872_row5_col14" class="data row5 col14" >LinAct360</td>
      <td id="T_bf872_row5_col15" class="data row5 col15" >1970-07-31</td>
      <td id="T_bf872_row5_col16" class="data row5 col16" >CLP</td>
      <td id="T_bf872_row5_col17" class="data row5 col17" >USDOBS</td>
      <td id="T_bf872_row5_col18" class="data row5 col18" >10.00</td>
      <td id="T_bf872_row5_col19" class="data row5 col19" >0.00</td>
      <td id="T_bf872_row5_col20" class="data row5 col20" >25,555.56</td>
    </tr>
    <tr>
      <th id="T_bf872_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_bf872_row6_col0" class="data row6 col0" >1970-07-31</td>
      <td id="T_bf872_row6_col1" class="data row6 col1" >1970-10-30</td>
      <td id="T_bf872_row6_col2" class="data row6 col2" >1970-07-29</td>
      <td id="T_bf872_row6_col3" class="data row6 col3" >1970-10-30</td>
      <td id="T_bf872_row6_col4" class="data row6 col4" >1,000,000.00</td>
      <td id="T_bf872_row6_col5" class="data row6 col5" >0.00</td>
      <td id="T_bf872_row6_col6" class="data row6 col6" >2,527.78</td>
      <td id="T_bf872_row6_col7" class="data row6 col7" >True</td>
      <td id="T_bf872_row6_col8" class="data row6 col8" >25,277.78</td>
      <td id="T_bf872_row6_col9" class="data row6 col9" >USD</td>
      <td id="T_bf872_row6_col10" class="data row6 col10" >LIBORUSD3M</td>
      <td id="T_bf872_row6_col11" class="data row6 col11" >1.0000%</td>
      <td id="T_bf872_row6_col12" class="data row6 col12" >1.00</td>
      <td id="T_bf872_row6_col13" class="data row6 col13" >0.0000%</td>
      <td id="T_bf872_row6_col14" class="data row6 col14" >LinAct360</td>
      <td id="T_bf872_row6_col15" class="data row6 col15" >1970-10-30</td>
      <td id="T_bf872_row6_col16" class="data row6 col16" >CLP</td>
      <td id="T_bf872_row6_col17" class="data row6 col17" >USDOBS</td>
      <td id="T_bf872_row6_col18" class="data row6 col18" >10.00</td>
      <td id="T_bf872_row6_col19" class="data row6 col19" >0.00</td>
      <td id="T_bf872_row6_col20" class="data row6 col20" >25,277.78</td>
    </tr>
    <tr>
      <th id="T_bf872_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_bf872_row7_col0" class="data row7 col0" >1970-10-30</td>
      <td id="T_bf872_row7_col1" class="data row7 col1" >1971-01-29</td>
      <td id="T_bf872_row7_col2" class="data row7 col2" >1970-10-28</td>
      <td id="T_bf872_row7_col3" class="data row7 col3" >1971-01-29</td>
      <td id="T_bf872_row7_col4" class="data row7 col4" >1,000,000.00</td>
      <td id="T_bf872_row7_col5" class="data row7 col5" >1,000,000.00</td>
      <td id="T_bf872_row7_col6" class="data row7 col6" >2,527.78</td>
      <td id="T_bf872_row7_col7" class="data row7 col7" >True</td>
      <td id="T_bf872_row7_col8" class="data row7 col8" >10,025,277.78</td>
      <td id="T_bf872_row7_col9" class="data row7 col9" >USD</td>
      <td id="T_bf872_row7_col10" class="data row7 col10" >LIBORUSD3M</td>
      <td id="T_bf872_row7_col11" class="data row7 col11" >1.0000%</td>
      <td id="T_bf872_row7_col12" class="data row7 col12" >1.00</td>
      <td id="T_bf872_row7_col13" class="data row7 col13" >0.0000%</td>
      <td id="T_bf872_row7_col14" class="data row7 col14" >LinAct360</td>
      <td id="T_bf872_row7_col15" class="data row7 col15" >1971-01-29</td>
      <td id="T_bf872_row7_col16" class="data row7 col16" >CLP</td>
      <td id="T_bf872_row7_col17" class="data row7 col17" >USDOBS</td>
      <td id="T_bf872_row7_col18" class="data row7 col18" >10.00</td>
      <td id="T_bf872_row7_col19" class="data row7 col19" >10,000,000.00</td>
      <td id="T_bf872_row7_col20" class="data row7 col20" >25,277.78</td>
    </tr>
  </tbody>
</table>




### Construcción Asistida de un `IcpClpLeg`
En este ejemplo se construye un `Leg` con `IcpClpCashflow` y amortización bullet.
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
- `gearing`: spread multiplicativo

Vamos a un ejemplo. Cambiando los parámetros anteriores se puede visualizar el efecto de ellos en la construcción. 

**NOTA:** para construir un `Leg` con `IcpClpCashflow` y amortización customizada, sólo se debe cambiar el parámetro **nominal** por **CustomNotionalAndAmort** e invocar el método `qcf.LegFactory.build_custom_amort_icp_clp_leg(...)`.


```python
# Se da de alta los parámetros requeridos
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(31, 1, 1969)
fecha_final = qcf.QCDate(31, 1, 1974) 
bus_adj_rule = qcf.BusyAdjRules.MODFOLLOW
periodicidad_pago = qcf.Tenor('3M')
periodo_irregular_pago = qcf.StubPeriod.NO
calendario = qcf.BusinessCalendar(fecha_inicio, 20)
lag_pago = 0
nominal = 1000000.0
amort_es_flujo = True 
spread = .01
gearing = 1.0

icp_clp_leg = qcf.LegFactory.build_bullet_icp_clp_leg(
    rp, 
    fecha_inicio, 
    fecha_final, 
    bus_adj_rule, 
    periodicidad_pago,
    periodo_irregular_pago, 
    calendario, 
    lag_pago,
    nominal, 
    amort_es_flujo, 
    spread, 
    gearing
)
```


```python
# Se define un list donde almacenar los resultados de la función show
tabla = []
for i in range(0, icp_clp_leg.size()):
    tabla.append(qcf.show(icp_clp_leg.get_cashflow_at(i)))

# Se utiliza tabla para inicializar el Dataframe
columnas = ['fecha_inicial', 'fecha__final', 'fecha__pago', 'nominal', 'amort', 'amort_es_flujo', 'flujo',
            'moneda', 'icp_inicial', 'icp_final', 'valor_tasa', 'interes', 'spread', 'gearing', 'tipo_tasa']
df7 = pd.DataFrame(tabla, columns=columnas)

# Se despliega la data en este formato
df7.style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_279bf">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_279bf_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_279bf_level0_col1" class="col_heading level0 col1" >fecha__final</th>
      <th id="T_279bf_level0_col2" class="col_heading level0 col2" >fecha__pago</th>
      <th id="T_279bf_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_279bf_level0_col4" class="col_heading level0 col4" >amort</th>
      <th id="T_279bf_level0_col5" class="col_heading level0 col5" >amort_es_flujo</th>
      <th id="T_279bf_level0_col6" class="col_heading level0 col6" >flujo</th>
      <th id="T_279bf_level0_col7" class="col_heading level0 col7" >moneda</th>
      <th id="T_279bf_level0_col8" class="col_heading level0 col8" >icp_inicial</th>
      <th id="T_279bf_level0_col9" class="col_heading level0 col9" >icp_final</th>
      <th id="T_279bf_level0_col10" class="col_heading level0 col10" >valor_tasa</th>
      <th id="T_279bf_level0_col11" class="col_heading level0 col11" >interes</th>
      <th id="T_279bf_level0_col12" class="col_heading level0 col12" >spread</th>
      <th id="T_279bf_level0_col13" class="col_heading level0 col13" >gearing</th>
      <th id="T_279bf_level0_col14" class="col_heading level0 col14" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_279bf_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_279bf_row0_col0" class="data row0 col0" >1969-01-31</td>
      <td id="T_279bf_row0_col1" class="data row0 col1" >1969-04-30</td>
      <td id="T_279bf_row0_col2" class="data row0 col2" >1969-04-30</td>
      <td id="T_279bf_row0_col3" class="data row0 col3" >1,000,000.00</td>
      <td id="T_279bf_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_279bf_row0_col5" class="data row0 col5" >True</td>
      <td id="T_279bf_row0_col6" class="data row0 col6" >2,472.22</td>
      <td id="T_279bf_row0_col7" class="data row0 col7" >CLP</td>
      <td id="T_279bf_row0_col8" class="data row0 col8" >10,000.00</td>
      <td id="T_279bf_row0_col9" class="data row0 col9" >10,000.00</td>
      <td id="T_279bf_row0_col10" class="data row0 col10" >0.0000%</td>
      <td id="T_279bf_row0_col11" class="data row0 col11" >2,472.22</td>
      <td id="T_279bf_row0_col12" class="data row0 col12" >1.0000%</td>
      <td id="T_279bf_row0_col13" class="data row0 col13" >1.00</td>
      <td id="T_279bf_row0_col14" class="data row0 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_279bf_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_279bf_row1_col0" class="data row1 col0" >1969-04-30</td>
      <td id="T_279bf_row1_col1" class="data row1 col1" >1969-07-31</td>
      <td id="T_279bf_row1_col2" class="data row1 col2" >1969-07-31</td>
      <td id="T_279bf_row1_col3" class="data row1 col3" >1,000,000.00</td>
      <td id="T_279bf_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_279bf_row1_col5" class="data row1 col5" >True</td>
      <td id="T_279bf_row1_col6" class="data row1 col6" >2,555.56</td>
      <td id="T_279bf_row1_col7" class="data row1 col7" >CLP</td>
      <td id="T_279bf_row1_col8" class="data row1 col8" >10,000.00</td>
      <td id="T_279bf_row1_col9" class="data row1 col9" >10,000.00</td>
      <td id="T_279bf_row1_col10" class="data row1 col10" >0.0000%</td>
      <td id="T_279bf_row1_col11" class="data row1 col11" >2,555.56</td>
      <td id="T_279bf_row1_col12" class="data row1 col12" >1.0000%</td>
      <td id="T_279bf_row1_col13" class="data row1 col13" >1.00</td>
      <td id="T_279bf_row1_col14" class="data row1 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_279bf_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_279bf_row2_col0" class="data row2 col0" >1969-07-31</td>
      <td id="T_279bf_row2_col1" class="data row2 col1" >1969-10-31</td>
      <td id="T_279bf_row2_col2" class="data row2 col2" >1969-10-31</td>
      <td id="T_279bf_row2_col3" class="data row2 col3" >1,000,000.00</td>
      <td id="T_279bf_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_279bf_row2_col5" class="data row2 col5" >True</td>
      <td id="T_279bf_row2_col6" class="data row2 col6" >2,555.56</td>
      <td id="T_279bf_row2_col7" class="data row2 col7" >CLP</td>
      <td id="T_279bf_row2_col8" class="data row2 col8" >10,000.00</td>
      <td id="T_279bf_row2_col9" class="data row2 col9" >10,000.00</td>
      <td id="T_279bf_row2_col10" class="data row2 col10" >0.0000%</td>
      <td id="T_279bf_row2_col11" class="data row2 col11" >2,555.56</td>
      <td id="T_279bf_row2_col12" class="data row2 col12" >1.0000%</td>
      <td id="T_279bf_row2_col13" class="data row2 col13" >1.00</td>
      <td id="T_279bf_row2_col14" class="data row2 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_279bf_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_279bf_row3_col0" class="data row3 col0" >1969-10-31</td>
      <td id="T_279bf_row3_col1" class="data row3 col1" >1970-01-30</td>
      <td id="T_279bf_row3_col2" class="data row3 col2" >1970-01-30</td>
      <td id="T_279bf_row3_col3" class="data row3 col3" >1,000,000.00</td>
      <td id="T_279bf_row3_col4" class="data row3 col4" >0.00</td>
      <td id="T_279bf_row3_col5" class="data row3 col5" >True</td>
      <td id="T_279bf_row3_col6" class="data row3 col6" >2,527.78</td>
      <td id="T_279bf_row3_col7" class="data row3 col7" >CLP</td>
      <td id="T_279bf_row3_col8" class="data row3 col8" >10,000.00</td>
      <td id="T_279bf_row3_col9" class="data row3 col9" >10,000.00</td>
      <td id="T_279bf_row3_col10" class="data row3 col10" >0.0000%</td>
      <td id="T_279bf_row3_col11" class="data row3 col11" >2,527.78</td>
      <td id="T_279bf_row3_col12" class="data row3 col12" >1.0000%</td>
      <td id="T_279bf_row3_col13" class="data row3 col13" >1.00</td>
      <td id="T_279bf_row3_col14" class="data row3 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_279bf_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_279bf_row4_col0" class="data row4 col0" >1970-01-30</td>
      <td id="T_279bf_row4_col1" class="data row4 col1" >1970-04-30</td>
      <td id="T_279bf_row4_col2" class="data row4 col2" >1970-04-30</td>
      <td id="T_279bf_row4_col3" class="data row4 col3" >1,000,000.00</td>
      <td id="T_279bf_row4_col4" class="data row4 col4" >0.00</td>
      <td id="T_279bf_row4_col5" class="data row4 col5" >True</td>
      <td id="T_279bf_row4_col6" class="data row4 col6" >2,500.00</td>
      <td id="T_279bf_row4_col7" class="data row4 col7" >CLP</td>
      <td id="T_279bf_row4_col8" class="data row4 col8" >10,000.00</td>
      <td id="T_279bf_row4_col9" class="data row4 col9" >10,000.00</td>
      <td id="T_279bf_row4_col10" class="data row4 col10" >0.0000%</td>
      <td id="T_279bf_row4_col11" class="data row4 col11" >2,500.00</td>
      <td id="T_279bf_row4_col12" class="data row4 col12" >1.0000%</td>
      <td id="T_279bf_row4_col13" class="data row4 col13" >1.00</td>
      <td id="T_279bf_row4_col14" class="data row4 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_279bf_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_279bf_row5_col0" class="data row5 col0" >1970-04-30</td>
      <td id="T_279bf_row5_col1" class="data row5 col1" >1970-07-31</td>
      <td id="T_279bf_row5_col2" class="data row5 col2" >1970-07-31</td>
      <td id="T_279bf_row5_col3" class="data row5 col3" >1,000,000.00</td>
      <td id="T_279bf_row5_col4" class="data row5 col4" >0.00</td>
      <td id="T_279bf_row5_col5" class="data row5 col5" >True</td>
      <td id="T_279bf_row5_col6" class="data row5 col6" >2,555.56</td>
      <td id="T_279bf_row5_col7" class="data row5 col7" >CLP</td>
      <td id="T_279bf_row5_col8" class="data row5 col8" >10,000.00</td>
      <td id="T_279bf_row5_col9" class="data row5 col9" >10,000.00</td>
      <td id="T_279bf_row5_col10" class="data row5 col10" >0.0000%</td>
      <td id="T_279bf_row5_col11" class="data row5 col11" >2,555.56</td>
      <td id="T_279bf_row5_col12" class="data row5 col12" >1.0000%</td>
      <td id="T_279bf_row5_col13" class="data row5 col13" >1.00</td>
      <td id="T_279bf_row5_col14" class="data row5 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_279bf_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_279bf_row6_col0" class="data row6 col0" >1970-07-31</td>
      <td id="T_279bf_row6_col1" class="data row6 col1" >1970-10-30</td>
      <td id="T_279bf_row6_col2" class="data row6 col2" >1970-10-30</td>
      <td id="T_279bf_row6_col3" class="data row6 col3" >1,000,000.00</td>
      <td id="T_279bf_row6_col4" class="data row6 col4" >0.00</td>
      <td id="T_279bf_row6_col5" class="data row6 col5" >True</td>
      <td id="T_279bf_row6_col6" class="data row6 col6" >2,527.78</td>
      <td id="T_279bf_row6_col7" class="data row6 col7" >CLP</td>
      <td id="T_279bf_row6_col8" class="data row6 col8" >10,000.00</td>
      <td id="T_279bf_row6_col9" class="data row6 col9" >10,000.00</td>
      <td id="T_279bf_row6_col10" class="data row6 col10" >0.0000%</td>
      <td id="T_279bf_row6_col11" class="data row6 col11" >2,527.78</td>
      <td id="T_279bf_row6_col12" class="data row6 col12" >1.0000%</td>
      <td id="T_279bf_row6_col13" class="data row6 col13" >1.00</td>
      <td id="T_279bf_row6_col14" class="data row6 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_279bf_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_279bf_row7_col0" class="data row7 col0" >1970-10-30</td>
      <td id="T_279bf_row7_col1" class="data row7 col1" >1971-01-29</td>
      <td id="T_279bf_row7_col2" class="data row7 col2" >1971-01-29</td>
      <td id="T_279bf_row7_col3" class="data row7 col3" >1,000,000.00</td>
      <td id="T_279bf_row7_col4" class="data row7 col4" >0.00</td>
      <td id="T_279bf_row7_col5" class="data row7 col5" >True</td>
      <td id="T_279bf_row7_col6" class="data row7 col6" >2,527.78</td>
      <td id="T_279bf_row7_col7" class="data row7 col7" >CLP</td>
      <td id="T_279bf_row7_col8" class="data row7 col8" >10,000.00</td>
      <td id="T_279bf_row7_col9" class="data row7 col9" >10,000.00</td>
      <td id="T_279bf_row7_col10" class="data row7 col10" >0.0000%</td>
      <td id="T_279bf_row7_col11" class="data row7 col11" >2,527.78</td>
      <td id="T_279bf_row7_col12" class="data row7 col12" >1.0000%</td>
      <td id="T_279bf_row7_col13" class="data row7 col13" >1.00</td>
      <td id="T_279bf_row7_col14" class="data row7 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_279bf_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_279bf_row8_col0" class="data row8 col0" >1971-01-29</td>
      <td id="T_279bf_row8_col1" class="data row8 col1" >1971-04-30</td>
      <td id="T_279bf_row8_col2" class="data row8 col2" >1971-04-30</td>
      <td id="T_279bf_row8_col3" class="data row8 col3" >1,000,000.00</td>
      <td id="T_279bf_row8_col4" class="data row8 col4" >0.00</td>
      <td id="T_279bf_row8_col5" class="data row8 col5" >True</td>
      <td id="T_279bf_row8_col6" class="data row8 col6" >2,527.78</td>
      <td id="T_279bf_row8_col7" class="data row8 col7" >CLP</td>
      <td id="T_279bf_row8_col8" class="data row8 col8" >10,000.00</td>
      <td id="T_279bf_row8_col9" class="data row8 col9" >10,000.00</td>
      <td id="T_279bf_row8_col10" class="data row8 col10" >0.0000%</td>
      <td id="T_279bf_row8_col11" class="data row8 col11" >2,527.78</td>
      <td id="T_279bf_row8_col12" class="data row8 col12" >1.0000%</td>
      <td id="T_279bf_row8_col13" class="data row8 col13" >1.00</td>
      <td id="T_279bf_row8_col14" class="data row8 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_279bf_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_279bf_row9_col0" class="data row9 col0" >1971-04-30</td>
      <td id="T_279bf_row9_col1" class="data row9 col1" >1971-07-30</td>
      <td id="T_279bf_row9_col2" class="data row9 col2" >1971-07-30</td>
      <td id="T_279bf_row9_col3" class="data row9 col3" >1,000,000.00</td>
      <td id="T_279bf_row9_col4" class="data row9 col4" >0.00</td>
      <td id="T_279bf_row9_col5" class="data row9 col5" >True</td>
      <td id="T_279bf_row9_col6" class="data row9 col6" >2,527.78</td>
      <td id="T_279bf_row9_col7" class="data row9 col7" >CLP</td>
      <td id="T_279bf_row9_col8" class="data row9 col8" >10,000.00</td>
      <td id="T_279bf_row9_col9" class="data row9 col9" >10,000.00</td>
      <td id="T_279bf_row9_col10" class="data row9 col10" >0.0000%</td>
      <td id="T_279bf_row9_col11" class="data row9 col11" >2,527.78</td>
      <td id="T_279bf_row9_col12" class="data row9 col12" >1.0000%</td>
      <td id="T_279bf_row9_col13" class="data row9 col13" >1.00</td>
      <td id="T_279bf_row9_col14" class="data row9 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_279bf_level0_row10" class="row_heading level0 row10" >10</th>
      <td id="T_279bf_row10_col0" class="data row10 col0" >1971-07-30</td>
      <td id="T_279bf_row10_col1" class="data row10 col1" >1971-10-29</td>
      <td id="T_279bf_row10_col2" class="data row10 col2" >1971-10-29</td>
      <td id="T_279bf_row10_col3" class="data row10 col3" >1,000,000.00</td>
      <td id="T_279bf_row10_col4" class="data row10 col4" >0.00</td>
      <td id="T_279bf_row10_col5" class="data row10 col5" >True</td>
      <td id="T_279bf_row10_col6" class="data row10 col6" >2,527.78</td>
      <td id="T_279bf_row10_col7" class="data row10 col7" >CLP</td>
      <td id="T_279bf_row10_col8" class="data row10 col8" >10,000.00</td>
      <td id="T_279bf_row10_col9" class="data row10 col9" >10,000.00</td>
      <td id="T_279bf_row10_col10" class="data row10 col10" >0.0000%</td>
      <td id="T_279bf_row10_col11" class="data row10 col11" >2,527.78</td>
      <td id="T_279bf_row10_col12" class="data row10 col12" >1.0000%</td>
      <td id="T_279bf_row10_col13" class="data row10 col13" >1.00</td>
      <td id="T_279bf_row10_col14" class="data row10 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_279bf_level0_row11" class="row_heading level0 row11" >11</th>
      <td id="T_279bf_row11_col0" class="data row11 col0" >1971-10-29</td>
      <td id="T_279bf_row11_col1" class="data row11 col1" >1972-01-31</td>
      <td id="T_279bf_row11_col2" class="data row11 col2" >1972-01-31</td>
      <td id="T_279bf_row11_col3" class="data row11 col3" >1,000,000.00</td>
      <td id="T_279bf_row11_col4" class="data row11 col4" >0.00</td>
      <td id="T_279bf_row11_col5" class="data row11 col5" >True</td>
      <td id="T_279bf_row11_col6" class="data row11 col6" >2,611.11</td>
      <td id="T_279bf_row11_col7" class="data row11 col7" >CLP</td>
      <td id="T_279bf_row11_col8" class="data row11 col8" >10,000.00</td>
      <td id="T_279bf_row11_col9" class="data row11 col9" >10,000.00</td>
      <td id="T_279bf_row11_col10" class="data row11 col10" >0.0000%</td>
      <td id="T_279bf_row11_col11" class="data row11 col11" >2,611.11</td>
      <td id="T_279bf_row11_col12" class="data row11 col12" >1.0000%</td>
      <td id="T_279bf_row11_col13" class="data row11 col13" >1.00</td>
      <td id="T_279bf_row11_col14" class="data row11 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_279bf_level0_row12" class="row_heading level0 row12" >12</th>
      <td id="T_279bf_row12_col0" class="data row12 col0" >1972-01-31</td>
      <td id="T_279bf_row12_col1" class="data row12 col1" >1972-04-28</td>
      <td id="T_279bf_row12_col2" class="data row12 col2" >1972-04-28</td>
      <td id="T_279bf_row12_col3" class="data row12 col3" >1,000,000.00</td>
      <td id="T_279bf_row12_col4" class="data row12 col4" >0.00</td>
      <td id="T_279bf_row12_col5" class="data row12 col5" >True</td>
      <td id="T_279bf_row12_col6" class="data row12 col6" >2,444.44</td>
      <td id="T_279bf_row12_col7" class="data row12 col7" >CLP</td>
      <td id="T_279bf_row12_col8" class="data row12 col8" >10,000.00</td>
      <td id="T_279bf_row12_col9" class="data row12 col9" >10,000.00</td>
      <td id="T_279bf_row12_col10" class="data row12 col10" >0.0000%</td>
      <td id="T_279bf_row12_col11" class="data row12 col11" >2,444.44</td>
      <td id="T_279bf_row12_col12" class="data row12 col12" >1.0000%</td>
      <td id="T_279bf_row12_col13" class="data row12 col13" >1.00</td>
      <td id="T_279bf_row12_col14" class="data row12 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_279bf_level0_row13" class="row_heading level0 row13" >13</th>
      <td id="T_279bf_row13_col0" class="data row13 col0" >1972-04-28</td>
      <td id="T_279bf_row13_col1" class="data row13 col1" >1972-07-31</td>
      <td id="T_279bf_row13_col2" class="data row13 col2" >1972-07-31</td>
      <td id="T_279bf_row13_col3" class="data row13 col3" >1,000,000.00</td>
      <td id="T_279bf_row13_col4" class="data row13 col4" >0.00</td>
      <td id="T_279bf_row13_col5" class="data row13 col5" >True</td>
      <td id="T_279bf_row13_col6" class="data row13 col6" >2,611.11</td>
      <td id="T_279bf_row13_col7" class="data row13 col7" >CLP</td>
      <td id="T_279bf_row13_col8" class="data row13 col8" >10,000.00</td>
      <td id="T_279bf_row13_col9" class="data row13 col9" >10,000.00</td>
      <td id="T_279bf_row13_col10" class="data row13 col10" >0.0000%</td>
      <td id="T_279bf_row13_col11" class="data row13 col11" >2,611.11</td>
      <td id="T_279bf_row13_col12" class="data row13 col12" >1.0000%</td>
      <td id="T_279bf_row13_col13" class="data row13 col13" >1.00</td>
      <td id="T_279bf_row13_col14" class="data row13 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_279bf_level0_row14" class="row_heading level0 row14" >14</th>
      <td id="T_279bf_row14_col0" class="data row14 col0" >1972-07-31</td>
      <td id="T_279bf_row14_col1" class="data row14 col1" >1972-10-31</td>
      <td id="T_279bf_row14_col2" class="data row14 col2" >1972-10-31</td>
      <td id="T_279bf_row14_col3" class="data row14 col3" >1,000,000.00</td>
      <td id="T_279bf_row14_col4" class="data row14 col4" >0.00</td>
      <td id="T_279bf_row14_col5" class="data row14 col5" >True</td>
      <td id="T_279bf_row14_col6" class="data row14 col6" >2,555.56</td>
      <td id="T_279bf_row14_col7" class="data row14 col7" >CLP</td>
      <td id="T_279bf_row14_col8" class="data row14 col8" >10,000.00</td>
      <td id="T_279bf_row14_col9" class="data row14 col9" >10,000.00</td>
      <td id="T_279bf_row14_col10" class="data row14 col10" >0.0000%</td>
      <td id="T_279bf_row14_col11" class="data row14 col11" >2,555.56</td>
      <td id="T_279bf_row14_col12" class="data row14 col12" >1.0000%</td>
      <td id="T_279bf_row14_col13" class="data row14 col13" >1.00</td>
      <td id="T_279bf_row14_col14" class="data row14 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_279bf_level0_row15" class="row_heading level0 row15" >15</th>
      <td id="T_279bf_row15_col0" class="data row15 col0" >1972-10-31</td>
      <td id="T_279bf_row15_col1" class="data row15 col1" >1973-01-31</td>
      <td id="T_279bf_row15_col2" class="data row15 col2" >1973-01-31</td>
      <td id="T_279bf_row15_col3" class="data row15 col3" >1,000,000.00</td>
      <td id="T_279bf_row15_col4" class="data row15 col4" >0.00</td>
      <td id="T_279bf_row15_col5" class="data row15 col5" >True</td>
      <td id="T_279bf_row15_col6" class="data row15 col6" >2,555.56</td>
      <td id="T_279bf_row15_col7" class="data row15 col7" >CLP</td>
      <td id="T_279bf_row15_col8" class="data row15 col8" >10,000.00</td>
      <td id="T_279bf_row15_col9" class="data row15 col9" >10,000.00</td>
      <td id="T_279bf_row15_col10" class="data row15 col10" >0.0000%</td>
      <td id="T_279bf_row15_col11" class="data row15 col11" >2,555.56</td>
      <td id="T_279bf_row15_col12" class="data row15 col12" >1.0000%</td>
      <td id="T_279bf_row15_col13" class="data row15 col13" >1.00</td>
      <td id="T_279bf_row15_col14" class="data row15 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_279bf_level0_row16" class="row_heading level0 row16" >16</th>
      <td id="T_279bf_row16_col0" class="data row16 col0" >1973-01-31</td>
      <td id="T_279bf_row16_col1" class="data row16 col1" >1973-04-30</td>
      <td id="T_279bf_row16_col2" class="data row16 col2" >1973-04-30</td>
      <td id="T_279bf_row16_col3" class="data row16 col3" >1,000,000.00</td>
      <td id="T_279bf_row16_col4" class="data row16 col4" >0.00</td>
      <td id="T_279bf_row16_col5" class="data row16 col5" >True</td>
      <td id="T_279bf_row16_col6" class="data row16 col6" >2,472.22</td>
      <td id="T_279bf_row16_col7" class="data row16 col7" >CLP</td>
      <td id="T_279bf_row16_col8" class="data row16 col8" >10,000.00</td>
      <td id="T_279bf_row16_col9" class="data row16 col9" >10,000.00</td>
      <td id="T_279bf_row16_col10" class="data row16 col10" >0.0000%</td>
      <td id="T_279bf_row16_col11" class="data row16 col11" >2,472.22</td>
      <td id="T_279bf_row16_col12" class="data row16 col12" >1.0000%</td>
      <td id="T_279bf_row16_col13" class="data row16 col13" >1.00</td>
      <td id="T_279bf_row16_col14" class="data row16 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_279bf_level0_row17" class="row_heading level0 row17" >17</th>
      <td id="T_279bf_row17_col0" class="data row17 col0" >1973-04-30</td>
      <td id="T_279bf_row17_col1" class="data row17 col1" >1973-07-31</td>
      <td id="T_279bf_row17_col2" class="data row17 col2" >1973-07-31</td>
      <td id="T_279bf_row17_col3" class="data row17 col3" >1,000,000.00</td>
      <td id="T_279bf_row17_col4" class="data row17 col4" >0.00</td>
      <td id="T_279bf_row17_col5" class="data row17 col5" >True</td>
      <td id="T_279bf_row17_col6" class="data row17 col6" >2,555.56</td>
      <td id="T_279bf_row17_col7" class="data row17 col7" >CLP</td>
      <td id="T_279bf_row17_col8" class="data row17 col8" >10,000.00</td>
      <td id="T_279bf_row17_col9" class="data row17 col9" >10,000.00</td>
      <td id="T_279bf_row17_col10" class="data row17 col10" >0.0000%</td>
      <td id="T_279bf_row17_col11" class="data row17 col11" >2,555.56</td>
      <td id="T_279bf_row17_col12" class="data row17 col12" >1.0000%</td>
      <td id="T_279bf_row17_col13" class="data row17 col13" >1.00</td>
      <td id="T_279bf_row17_col14" class="data row17 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_279bf_level0_row18" class="row_heading level0 row18" >18</th>
      <td id="T_279bf_row18_col0" class="data row18 col0" >1973-07-31</td>
      <td id="T_279bf_row18_col1" class="data row18 col1" >1973-10-31</td>
      <td id="T_279bf_row18_col2" class="data row18 col2" >1973-10-31</td>
      <td id="T_279bf_row18_col3" class="data row18 col3" >1,000,000.00</td>
      <td id="T_279bf_row18_col4" class="data row18 col4" >0.00</td>
      <td id="T_279bf_row18_col5" class="data row18 col5" >True</td>
      <td id="T_279bf_row18_col6" class="data row18 col6" >2,555.56</td>
      <td id="T_279bf_row18_col7" class="data row18 col7" >CLP</td>
      <td id="T_279bf_row18_col8" class="data row18 col8" >10,000.00</td>
      <td id="T_279bf_row18_col9" class="data row18 col9" >10,000.00</td>
      <td id="T_279bf_row18_col10" class="data row18 col10" >0.0000%</td>
      <td id="T_279bf_row18_col11" class="data row18 col11" >2,555.56</td>
      <td id="T_279bf_row18_col12" class="data row18 col12" >1.0000%</td>
      <td id="T_279bf_row18_col13" class="data row18 col13" >1.00</td>
      <td id="T_279bf_row18_col14" class="data row18 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_279bf_level0_row19" class="row_heading level0 row19" >19</th>
      <td id="T_279bf_row19_col0" class="data row19 col0" >1973-10-31</td>
      <td id="T_279bf_row19_col1" class="data row19 col1" >1974-01-31</td>
      <td id="T_279bf_row19_col2" class="data row19 col2" >1974-01-31</td>
      <td id="T_279bf_row19_col3" class="data row19 col3" >1,000,000.00</td>
      <td id="T_279bf_row19_col4" class="data row19 col4" >1,000,000.00</td>
      <td id="T_279bf_row19_col5" class="data row19 col5" >True</td>
      <td id="T_279bf_row19_col6" class="data row19 col6" >1,002,555.56</td>
      <td id="T_279bf_row19_col7" class="data row19 col7" >CLP</td>
      <td id="T_279bf_row19_col8" class="data row19 col8" >10,000.00</td>
      <td id="T_279bf_row19_col9" class="data row19 col9" >10,000.00</td>
      <td id="T_279bf_row19_col10" class="data row19 col10" >0.0000%</td>
      <td id="T_279bf_row19_col11" class="data row19 col11" >2,555.56</td>
      <td id="T_279bf_row19_col12" class="data row19 col12" >1.0000%</td>
      <td id="T_279bf_row19_col13" class="data row19 col13" >1.00</td>
      <td id="T_279bf_row19_col14" class="data row19 col14" >LinAct360</td>
    </tr>
  </tbody>
</table>




### Construcción Asistida de un `IcpClp2Leg`


En este ejemplo se construye un `Leg` con `IcpClpCashflow2` y amortización bullet.
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
- `gearing`: spread multiplicativo

Vamos a un ejemplo. Cambiando los parámetros anteriores se puede visualizar el efecto de ellos en la construcción. 

**NOTA:** para construir un `Leg` con `IcpClpCashflow2` y amortización customizada, sólo se debe cambiar el parámetro **nominal** por **CustomNotionalAndAmort** e invocar el método `qcf.LegFactory.build_custom_amort_icp_clp2_leg(...)`.


```python
# Se da de alta los parámetros requeridos
icp_clp2_leg = qcf.LegFactory.build_bullet_icp_clp2_leg(
    rp, 
    fecha_inicio, 
    fecha_final, 
    bus_adj_rule, 
    periodicidad_pago,
    periodo_irregular_pago, 
    calendario, 
    lag_pago,
    nominal, 
    amort_es_flujo, 
    spread, 
    gearing, 
    True
)
```


```python
# Se define un list donde almacenar los resultados de la función show
tabla = []
for i in range(0, icp_clp2_leg.size()):
    tabla.append(qcf.show(icp_clp2_leg.get_cashflow_at(i)))

# Se utiliza tabla para inicializar el Dataframe
columnas = ['fecha_inicial', 'fecha__final', 'fecha__pago', 'nominal', 'amort', 'amort_es_flujo', 'flujo',
            'moneda', 'icp_inicial', 'icp_final', 'valor_tasa', 'interes', 'spread', 'gearing', 'tipo_tasa']
df9 = pd.DataFrame(tabla, columns=columnas)

# Se despliega la data en este formato
df9.style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_4f6ea">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_4f6ea_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_4f6ea_level0_col1" class="col_heading level0 col1" >fecha__final</th>
      <th id="T_4f6ea_level0_col2" class="col_heading level0 col2" >fecha__pago</th>
      <th id="T_4f6ea_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_4f6ea_level0_col4" class="col_heading level0 col4" >amort</th>
      <th id="T_4f6ea_level0_col5" class="col_heading level0 col5" >amort_es_flujo</th>
      <th id="T_4f6ea_level0_col6" class="col_heading level0 col6" >flujo</th>
      <th id="T_4f6ea_level0_col7" class="col_heading level0 col7" >moneda</th>
      <th id="T_4f6ea_level0_col8" class="col_heading level0 col8" >icp_inicial</th>
      <th id="T_4f6ea_level0_col9" class="col_heading level0 col9" >icp_final</th>
      <th id="T_4f6ea_level0_col10" class="col_heading level0 col10" >valor_tasa</th>
      <th id="T_4f6ea_level0_col11" class="col_heading level0 col11" >interes</th>
      <th id="T_4f6ea_level0_col12" class="col_heading level0 col12" >spread</th>
      <th id="T_4f6ea_level0_col13" class="col_heading level0 col13" >gearing</th>
      <th id="T_4f6ea_level0_col14" class="col_heading level0 col14" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_4f6ea_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_4f6ea_row0_col0" class="data row0 col0" >1969-01-31</td>
      <td id="T_4f6ea_row0_col1" class="data row0 col1" >1969-04-30</td>
      <td id="T_4f6ea_row0_col2" class="data row0 col2" >1969-04-30</td>
      <td id="T_4f6ea_row0_col3" class="data row0 col3" >1,000,000.00</td>
      <td id="T_4f6ea_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_4f6ea_row0_col5" class="data row0 col5" >True</td>
      <td id="T_4f6ea_row0_col6" class="data row0 col6" >2,472.22</td>
      <td id="T_4f6ea_row0_col7" class="data row0 col7" >CLP</td>
      <td id="T_4f6ea_row0_col8" class="data row0 col8" >10,000.00</td>
      <td id="T_4f6ea_row0_col9" class="data row0 col9" >10,000.00</td>
      <td id="T_4f6ea_row0_col10" class="data row0 col10" >0.0000%</td>
      <td id="T_4f6ea_row0_col11" class="data row0 col11" >2,472.22</td>
      <td id="T_4f6ea_row0_col12" class="data row0 col12" >1.0000%</td>
      <td id="T_4f6ea_row0_col13" class="data row0 col13" >1.00</td>
      <td id="T_4f6ea_row0_col14" class="data row0 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4f6ea_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_4f6ea_row1_col0" class="data row1 col0" >1969-04-30</td>
      <td id="T_4f6ea_row1_col1" class="data row1 col1" >1969-07-31</td>
      <td id="T_4f6ea_row1_col2" class="data row1 col2" >1969-07-31</td>
      <td id="T_4f6ea_row1_col3" class="data row1 col3" >1,000,000.00</td>
      <td id="T_4f6ea_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_4f6ea_row1_col5" class="data row1 col5" >True</td>
      <td id="T_4f6ea_row1_col6" class="data row1 col6" >2,555.56</td>
      <td id="T_4f6ea_row1_col7" class="data row1 col7" >CLP</td>
      <td id="T_4f6ea_row1_col8" class="data row1 col8" >10,000.00</td>
      <td id="T_4f6ea_row1_col9" class="data row1 col9" >10,000.00</td>
      <td id="T_4f6ea_row1_col10" class="data row1 col10" >0.0000%</td>
      <td id="T_4f6ea_row1_col11" class="data row1 col11" >2,555.56</td>
      <td id="T_4f6ea_row1_col12" class="data row1 col12" >1.0000%</td>
      <td id="T_4f6ea_row1_col13" class="data row1 col13" >1.00</td>
      <td id="T_4f6ea_row1_col14" class="data row1 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4f6ea_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_4f6ea_row2_col0" class="data row2 col0" >1969-07-31</td>
      <td id="T_4f6ea_row2_col1" class="data row2 col1" >1969-10-31</td>
      <td id="T_4f6ea_row2_col2" class="data row2 col2" >1969-10-31</td>
      <td id="T_4f6ea_row2_col3" class="data row2 col3" >1,000,000.00</td>
      <td id="T_4f6ea_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_4f6ea_row2_col5" class="data row2 col5" >True</td>
      <td id="T_4f6ea_row2_col6" class="data row2 col6" >2,555.56</td>
      <td id="T_4f6ea_row2_col7" class="data row2 col7" >CLP</td>
      <td id="T_4f6ea_row2_col8" class="data row2 col8" >10,000.00</td>
      <td id="T_4f6ea_row2_col9" class="data row2 col9" >10,000.00</td>
      <td id="T_4f6ea_row2_col10" class="data row2 col10" >0.0000%</td>
      <td id="T_4f6ea_row2_col11" class="data row2 col11" >2,555.56</td>
      <td id="T_4f6ea_row2_col12" class="data row2 col12" >1.0000%</td>
      <td id="T_4f6ea_row2_col13" class="data row2 col13" >1.00</td>
      <td id="T_4f6ea_row2_col14" class="data row2 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4f6ea_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_4f6ea_row3_col0" class="data row3 col0" >1969-10-31</td>
      <td id="T_4f6ea_row3_col1" class="data row3 col1" >1970-01-30</td>
      <td id="T_4f6ea_row3_col2" class="data row3 col2" >1970-01-30</td>
      <td id="T_4f6ea_row3_col3" class="data row3 col3" >1,000,000.00</td>
      <td id="T_4f6ea_row3_col4" class="data row3 col4" >0.00</td>
      <td id="T_4f6ea_row3_col5" class="data row3 col5" >True</td>
      <td id="T_4f6ea_row3_col6" class="data row3 col6" >2,527.78</td>
      <td id="T_4f6ea_row3_col7" class="data row3 col7" >CLP</td>
      <td id="T_4f6ea_row3_col8" class="data row3 col8" >10,000.00</td>
      <td id="T_4f6ea_row3_col9" class="data row3 col9" >10,000.00</td>
      <td id="T_4f6ea_row3_col10" class="data row3 col10" >0.0000%</td>
      <td id="T_4f6ea_row3_col11" class="data row3 col11" >2,527.78</td>
      <td id="T_4f6ea_row3_col12" class="data row3 col12" >1.0000%</td>
      <td id="T_4f6ea_row3_col13" class="data row3 col13" >1.00</td>
      <td id="T_4f6ea_row3_col14" class="data row3 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4f6ea_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_4f6ea_row4_col0" class="data row4 col0" >1970-01-30</td>
      <td id="T_4f6ea_row4_col1" class="data row4 col1" >1970-04-30</td>
      <td id="T_4f6ea_row4_col2" class="data row4 col2" >1970-04-30</td>
      <td id="T_4f6ea_row4_col3" class="data row4 col3" >1,000,000.00</td>
      <td id="T_4f6ea_row4_col4" class="data row4 col4" >0.00</td>
      <td id="T_4f6ea_row4_col5" class="data row4 col5" >True</td>
      <td id="T_4f6ea_row4_col6" class="data row4 col6" >2,500.00</td>
      <td id="T_4f6ea_row4_col7" class="data row4 col7" >CLP</td>
      <td id="T_4f6ea_row4_col8" class="data row4 col8" >10,000.00</td>
      <td id="T_4f6ea_row4_col9" class="data row4 col9" >10,000.00</td>
      <td id="T_4f6ea_row4_col10" class="data row4 col10" >0.0000%</td>
      <td id="T_4f6ea_row4_col11" class="data row4 col11" >2,500.00</td>
      <td id="T_4f6ea_row4_col12" class="data row4 col12" >1.0000%</td>
      <td id="T_4f6ea_row4_col13" class="data row4 col13" >1.00</td>
      <td id="T_4f6ea_row4_col14" class="data row4 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4f6ea_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_4f6ea_row5_col0" class="data row5 col0" >1970-04-30</td>
      <td id="T_4f6ea_row5_col1" class="data row5 col1" >1970-07-31</td>
      <td id="T_4f6ea_row5_col2" class="data row5 col2" >1970-07-31</td>
      <td id="T_4f6ea_row5_col3" class="data row5 col3" >1,000,000.00</td>
      <td id="T_4f6ea_row5_col4" class="data row5 col4" >0.00</td>
      <td id="T_4f6ea_row5_col5" class="data row5 col5" >True</td>
      <td id="T_4f6ea_row5_col6" class="data row5 col6" >2,555.56</td>
      <td id="T_4f6ea_row5_col7" class="data row5 col7" >CLP</td>
      <td id="T_4f6ea_row5_col8" class="data row5 col8" >10,000.00</td>
      <td id="T_4f6ea_row5_col9" class="data row5 col9" >10,000.00</td>
      <td id="T_4f6ea_row5_col10" class="data row5 col10" >0.0000%</td>
      <td id="T_4f6ea_row5_col11" class="data row5 col11" >2,555.56</td>
      <td id="T_4f6ea_row5_col12" class="data row5 col12" >1.0000%</td>
      <td id="T_4f6ea_row5_col13" class="data row5 col13" >1.00</td>
      <td id="T_4f6ea_row5_col14" class="data row5 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4f6ea_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_4f6ea_row6_col0" class="data row6 col0" >1970-07-31</td>
      <td id="T_4f6ea_row6_col1" class="data row6 col1" >1970-10-30</td>
      <td id="T_4f6ea_row6_col2" class="data row6 col2" >1970-10-30</td>
      <td id="T_4f6ea_row6_col3" class="data row6 col3" >1,000,000.00</td>
      <td id="T_4f6ea_row6_col4" class="data row6 col4" >0.00</td>
      <td id="T_4f6ea_row6_col5" class="data row6 col5" >True</td>
      <td id="T_4f6ea_row6_col6" class="data row6 col6" >2,527.78</td>
      <td id="T_4f6ea_row6_col7" class="data row6 col7" >CLP</td>
      <td id="T_4f6ea_row6_col8" class="data row6 col8" >10,000.00</td>
      <td id="T_4f6ea_row6_col9" class="data row6 col9" >10,000.00</td>
      <td id="T_4f6ea_row6_col10" class="data row6 col10" >0.0000%</td>
      <td id="T_4f6ea_row6_col11" class="data row6 col11" >2,527.78</td>
      <td id="T_4f6ea_row6_col12" class="data row6 col12" >1.0000%</td>
      <td id="T_4f6ea_row6_col13" class="data row6 col13" >1.00</td>
      <td id="T_4f6ea_row6_col14" class="data row6 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4f6ea_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_4f6ea_row7_col0" class="data row7 col0" >1970-10-30</td>
      <td id="T_4f6ea_row7_col1" class="data row7 col1" >1971-01-29</td>
      <td id="T_4f6ea_row7_col2" class="data row7 col2" >1971-01-29</td>
      <td id="T_4f6ea_row7_col3" class="data row7 col3" >1,000,000.00</td>
      <td id="T_4f6ea_row7_col4" class="data row7 col4" >0.00</td>
      <td id="T_4f6ea_row7_col5" class="data row7 col5" >True</td>
      <td id="T_4f6ea_row7_col6" class="data row7 col6" >2,527.78</td>
      <td id="T_4f6ea_row7_col7" class="data row7 col7" >CLP</td>
      <td id="T_4f6ea_row7_col8" class="data row7 col8" >10,000.00</td>
      <td id="T_4f6ea_row7_col9" class="data row7 col9" >10,000.00</td>
      <td id="T_4f6ea_row7_col10" class="data row7 col10" >0.0000%</td>
      <td id="T_4f6ea_row7_col11" class="data row7 col11" >2,527.78</td>
      <td id="T_4f6ea_row7_col12" class="data row7 col12" >1.0000%</td>
      <td id="T_4f6ea_row7_col13" class="data row7 col13" >1.00</td>
      <td id="T_4f6ea_row7_col14" class="data row7 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4f6ea_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_4f6ea_row8_col0" class="data row8 col0" >1971-01-29</td>
      <td id="T_4f6ea_row8_col1" class="data row8 col1" >1971-04-30</td>
      <td id="T_4f6ea_row8_col2" class="data row8 col2" >1971-04-30</td>
      <td id="T_4f6ea_row8_col3" class="data row8 col3" >1,000,000.00</td>
      <td id="T_4f6ea_row8_col4" class="data row8 col4" >0.00</td>
      <td id="T_4f6ea_row8_col5" class="data row8 col5" >True</td>
      <td id="T_4f6ea_row8_col6" class="data row8 col6" >2,527.78</td>
      <td id="T_4f6ea_row8_col7" class="data row8 col7" >CLP</td>
      <td id="T_4f6ea_row8_col8" class="data row8 col8" >10,000.00</td>
      <td id="T_4f6ea_row8_col9" class="data row8 col9" >10,000.00</td>
      <td id="T_4f6ea_row8_col10" class="data row8 col10" >0.0000%</td>
      <td id="T_4f6ea_row8_col11" class="data row8 col11" >2,527.78</td>
      <td id="T_4f6ea_row8_col12" class="data row8 col12" >1.0000%</td>
      <td id="T_4f6ea_row8_col13" class="data row8 col13" >1.00</td>
      <td id="T_4f6ea_row8_col14" class="data row8 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4f6ea_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_4f6ea_row9_col0" class="data row9 col0" >1971-04-30</td>
      <td id="T_4f6ea_row9_col1" class="data row9 col1" >1971-07-30</td>
      <td id="T_4f6ea_row9_col2" class="data row9 col2" >1971-07-30</td>
      <td id="T_4f6ea_row9_col3" class="data row9 col3" >1,000,000.00</td>
      <td id="T_4f6ea_row9_col4" class="data row9 col4" >0.00</td>
      <td id="T_4f6ea_row9_col5" class="data row9 col5" >True</td>
      <td id="T_4f6ea_row9_col6" class="data row9 col6" >2,527.78</td>
      <td id="T_4f6ea_row9_col7" class="data row9 col7" >CLP</td>
      <td id="T_4f6ea_row9_col8" class="data row9 col8" >10,000.00</td>
      <td id="T_4f6ea_row9_col9" class="data row9 col9" >10,000.00</td>
      <td id="T_4f6ea_row9_col10" class="data row9 col10" >0.0000%</td>
      <td id="T_4f6ea_row9_col11" class="data row9 col11" >2,527.78</td>
      <td id="T_4f6ea_row9_col12" class="data row9 col12" >1.0000%</td>
      <td id="T_4f6ea_row9_col13" class="data row9 col13" >1.00</td>
      <td id="T_4f6ea_row9_col14" class="data row9 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4f6ea_level0_row10" class="row_heading level0 row10" >10</th>
      <td id="T_4f6ea_row10_col0" class="data row10 col0" >1971-07-30</td>
      <td id="T_4f6ea_row10_col1" class="data row10 col1" >1971-10-29</td>
      <td id="T_4f6ea_row10_col2" class="data row10 col2" >1971-10-29</td>
      <td id="T_4f6ea_row10_col3" class="data row10 col3" >1,000,000.00</td>
      <td id="T_4f6ea_row10_col4" class="data row10 col4" >0.00</td>
      <td id="T_4f6ea_row10_col5" class="data row10 col5" >True</td>
      <td id="T_4f6ea_row10_col6" class="data row10 col6" >2,527.78</td>
      <td id="T_4f6ea_row10_col7" class="data row10 col7" >CLP</td>
      <td id="T_4f6ea_row10_col8" class="data row10 col8" >10,000.00</td>
      <td id="T_4f6ea_row10_col9" class="data row10 col9" >10,000.00</td>
      <td id="T_4f6ea_row10_col10" class="data row10 col10" >0.0000%</td>
      <td id="T_4f6ea_row10_col11" class="data row10 col11" >2,527.78</td>
      <td id="T_4f6ea_row10_col12" class="data row10 col12" >1.0000%</td>
      <td id="T_4f6ea_row10_col13" class="data row10 col13" >1.00</td>
      <td id="T_4f6ea_row10_col14" class="data row10 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4f6ea_level0_row11" class="row_heading level0 row11" >11</th>
      <td id="T_4f6ea_row11_col0" class="data row11 col0" >1971-10-29</td>
      <td id="T_4f6ea_row11_col1" class="data row11 col1" >1972-01-31</td>
      <td id="T_4f6ea_row11_col2" class="data row11 col2" >1972-01-31</td>
      <td id="T_4f6ea_row11_col3" class="data row11 col3" >1,000,000.00</td>
      <td id="T_4f6ea_row11_col4" class="data row11 col4" >0.00</td>
      <td id="T_4f6ea_row11_col5" class="data row11 col5" >True</td>
      <td id="T_4f6ea_row11_col6" class="data row11 col6" >2,611.11</td>
      <td id="T_4f6ea_row11_col7" class="data row11 col7" >CLP</td>
      <td id="T_4f6ea_row11_col8" class="data row11 col8" >10,000.00</td>
      <td id="T_4f6ea_row11_col9" class="data row11 col9" >10,000.00</td>
      <td id="T_4f6ea_row11_col10" class="data row11 col10" >0.0000%</td>
      <td id="T_4f6ea_row11_col11" class="data row11 col11" >2,611.11</td>
      <td id="T_4f6ea_row11_col12" class="data row11 col12" >1.0000%</td>
      <td id="T_4f6ea_row11_col13" class="data row11 col13" >1.00</td>
      <td id="T_4f6ea_row11_col14" class="data row11 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4f6ea_level0_row12" class="row_heading level0 row12" >12</th>
      <td id="T_4f6ea_row12_col0" class="data row12 col0" >1972-01-31</td>
      <td id="T_4f6ea_row12_col1" class="data row12 col1" >1972-04-28</td>
      <td id="T_4f6ea_row12_col2" class="data row12 col2" >1972-04-28</td>
      <td id="T_4f6ea_row12_col3" class="data row12 col3" >1,000,000.00</td>
      <td id="T_4f6ea_row12_col4" class="data row12 col4" >0.00</td>
      <td id="T_4f6ea_row12_col5" class="data row12 col5" >True</td>
      <td id="T_4f6ea_row12_col6" class="data row12 col6" >2,444.44</td>
      <td id="T_4f6ea_row12_col7" class="data row12 col7" >CLP</td>
      <td id="T_4f6ea_row12_col8" class="data row12 col8" >10,000.00</td>
      <td id="T_4f6ea_row12_col9" class="data row12 col9" >10,000.00</td>
      <td id="T_4f6ea_row12_col10" class="data row12 col10" >0.0000%</td>
      <td id="T_4f6ea_row12_col11" class="data row12 col11" >2,444.44</td>
      <td id="T_4f6ea_row12_col12" class="data row12 col12" >1.0000%</td>
      <td id="T_4f6ea_row12_col13" class="data row12 col13" >1.00</td>
      <td id="T_4f6ea_row12_col14" class="data row12 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4f6ea_level0_row13" class="row_heading level0 row13" >13</th>
      <td id="T_4f6ea_row13_col0" class="data row13 col0" >1972-04-28</td>
      <td id="T_4f6ea_row13_col1" class="data row13 col1" >1972-07-31</td>
      <td id="T_4f6ea_row13_col2" class="data row13 col2" >1972-07-31</td>
      <td id="T_4f6ea_row13_col3" class="data row13 col3" >1,000,000.00</td>
      <td id="T_4f6ea_row13_col4" class="data row13 col4" >0.00</td>
      <td id="T_4f6ea_row13_col5" class="data row13 col5" >True</td>
      <td id="T_4f6ea_row13_col6" class="data row13 col6" >2,611.11</td>
      <td id="T_4f6ea_row13_col7" class="data row13 col7" >CLP</td>
      <td id="T_4f6ea_row13_col8" class="data row13 col8" >10,000.00</td>
      <td id="T_4f6ea_row13_col9" class="data row13 col9" >10,000.00</td>
      <td id="T_4f6ea_row13_col10" class="data row13 col10" >0.0000%</td>
      <td id="T_4f6ea_row13_col11" class="data row13 col11" >2,611.11</td>
      <td id="T_4f6ea_row13_col12" class="data row13 col12" >1.0000%</td>
      <td id="T_4f6ea_row13_col13" class="data row13 col13" >1.00</td>
      <td id="T_4f6ea_row13_col14" class="data row13 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4f6ea_level0_row14" class="row_heading level0 row14" >14</th>
      <td id="T_4f6ea_row14_col0" class="data row14 col0" >1972-07-31</td>
      <td id="T_4f6ea_row14_col1" class="data row14 col1" >1972-10-31</td>
      <td id="T_4f6ea_row14_col2" class="data row14 col2" >1972-10-31</td>
      <td id="T_4f6ea_row14_col3" class="data row14 col3" >1,000,000.00</td>
      <td id="T_4f6ea_row14_col4" class="data row14 col4" >0.00</td>
      <td id="T_4f6ea_row14_col5" class="data row14 col5" >True</td>
      <td id="T_4f6ea_row14_col6" class="data row14 col6" >2,555.56</td>
      <td id="T_4f6ea_row14_col7" class="data row14 col7" >CLP</td>
      <td id="T_4f6ea_row14_col8" class="data row14 col8" >10,000.00</td>
      <td id="T_4f6ea_row14_col9" class="data row14 col9" >10,000.00</td>
      <td id="T_4f6ea_row14_col10" class="data row14 col10" >0.0000%</td>
      <td id="T_4f6ea_row14_col11" class="data row14 col11" >2,555.56</td>
      <td id="T_4f6ea_row14_col12" class="data row14 col12" >1.0000%</td>
      <td id="T_4f6ea_row14_col13" class="data row14 col13" >1.00</td>
      <td id="T_4f6ea_row14_col14" class="data row14 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4f6ea_level0_row15" class="row_heading level0 row15" >15</th>
      <td id="T_4f6ea_row15_col0" class="data row15 col0" >1972-10-31</td>
      <td id="T_4f6ea_row15_col1" class="data row15 col1" >1973-01-31</td>
      <td id="T_4f6ea_row15_col2" class="data row15 col2" >1973-01-31</td>
      <td id="T_4f6ea_row15_col3" class="data row15 col3" >1,000,000.00</td>
      <td id="T_4f6ea_row15_col4" class="data row15 col4" >0.00</td>
      <td id="T_4f6ea_row15_col5" class="data row15 col5" >True</td>
      <td id="T_4f6ea_row15_col6" class="data row15 col6" >2,555.56</td>
      <td id="T_4f6ea_row15_col7" class="data row15 col7" >CLP</td>
      <td id="T_4f6ea_row15_col8" class="data row15 col8" >10,000.00</td>
      <td id="T_4f6ea_row15_col9" class="data row15 col9" >10,000.00</td>
      <td id="T_4f6ea_row15_col10" class="data row15 col10" >0.0000%</td>
      <td id="T_4f6ea_row15_col11" class="data row15 col11" >2,555.56</td>
      <td id="T_4f6ea_row15_col12" class="data row15 col12" >1.0000%</td>
      <td id="T_4f6ea_row15_col13" class="data row15 col13" >1.00</td>
      <td id="T_4f6ea_row15_col14" class="data row15 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4f6ea_level0_row16" class="row_heading level0 row16" >16</th>
      <td id="T_4f6ea_row16_col0" class="data row16 col0" >1973-01-31</td>
      <td id="T_4f6ea_row16_col1" class="data row16 col1" >1973-04-30</td>
      <td id="T_4f6ea_row16_col2" class="data row16 col2" >1973-04-30</td>
      <td id="T_4f6ea_row16_col3" class="data row16 col3" >1,000,000.00</td>
      <td id="T_4f6ea_row16_col4" class="data row16 col4" >0.00</td>
      <td id="T_4f6ea_row16_col5" class="data row16 col5" >True</td>
      <td id="T_4f6ea_row16_col6" class="data row16 col6" >2,472.22</td>
      <td id="T_4f6ea_row16_col7" class="data row16 col7" >CLP</td>
      <td id="T_4f6ea_row16_col8" class="data row16 col8" >10,000.00</td>
      <td id="T_4f6ea_row16_col9" class="data row16 col9" >10,000.00</td>
      <td id="T_4f6ea_row16_col10" class="data row16 col10" >0.0000%</td>
      <td id="T_4f6ea_row16_col11" class="data row16 col11" >2,472.22</td>
      <td id="T_4f6ea_row16_col12" class="data row16 col12" >1.0000%</td>
      <td id="T_4f6ea_row16_col13" class="data row16 col13" >1.00</td>
      <td id="T_4f6ea_row16_col14" class="data row16 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4f6ea_level0_row17" class="row_heading level0 row17" >17</th>
      <td id="T_4f6ea_row17_col0" class="data row17 col0" >1973-04-30</td>
      <td id="T_4f6ea_row17_col1" class="data row17 col1" >1973-07-31</td>
      <td id="T_4f6ea_row17_col2" class="data row17 col2" >1973-07-31</td>
      <td id="T_4f6ea_row17_col3" class="data row17 col3" >1,000,000.00</td>
      <td id="T_4f6ea_row17_col4" class="data row17 col4" >0.00</td>
      <td id="T_4f6ea_row17_col5" class="data row17 col5" >True</td>
      <td id="T_4f6ea_row17_col6" class="data row17 col6" >2,555.56</td>
      <td id="T_4f6ea_row17_col7" class="data row17 col7" >CLP</td>
      <td id="T_4f6ea_row17_col8" class="data row17 col8" >10,000.00</td>
      <td id="T_4f6ea_row17_col9" class="data row17 col9" >10,000.00</td>
      <td id="T_4f6ea_row17_col10" class="data row17 col10" >0.0000%</td>
      <td id="T_4f6ea_row17_col11" class="data row17 col11" >2,555.56</td>
      <td id="T_4f6ea_row17_col12" class="data row17 col12" >1.0000%</td>
      <td id="T_4f6ea_row17_col13" class="data row17 col13" >1.00</td>
      <td id="T_4f6ea_row17_col14" class="data row17 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4f6ea_level0_row18" class="row_heading level0 row18" >18</th>
      <td id="T_4f6ea_row18_col0" class="data row18 col0" >1973-07-31</td>
      <td id="T_4f6ea_row18_col1" class="data row18 col1" >1973-10-31</td>
      <td id="T_4f6ea_row18_col2" class="data row18 col2" >1973-10-31</td>
      <td id="T_4f6ea_row18_col3" class="data row18 col3" >1,000,000.00</td>
      <td id="T_4f6ea_row18_col4" class="data row18 col4" >0.00</td>
      <td id="T_4f6ea_row18_col5" class="data row18 col5" >True</td>
      <td id="T_4f6ea_row18_col6" class="data row18 col6" >2,555.56</td>
      <td id="T_4f6ea_row18_col7" class="data row18 col7" >CLP</td>
      <td id="T_4f6ea_row18_col8" class="data row18 col8" >10,000.00</td>
      <td id="T_4f6ea_row18_col9" class="data row18 col9" >10,000.00</td>
      <td id="T_4f6ea_row18_col10" class="data row18 col10" >0.0000%</td>
      <td id="T_4f6ea_row18_col11" class="data row18 col11" >2,555.56</td>
      <td id="T_4f6ea_row18_col12" class="data row18 col12" >1.0000%</td>
      <td id="T_4f6ea_row18_col13" class="data row18 col13" >1.00</td>
      <td id="T_4f6ea_row18_col14" class="data row18 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_4f6ea_level0_row19" class="row_heading level0 row19" >19</th>
      <td id="T_4f6ea_row19_col0" class="data row19 col0" >1973-10-31</td>
      <td id="T_4f6ea_row19_col1" class="data row19 col1" >1974-01-31</td>
      <td id="T_4f6ea_row19_col2" class="data row19 col2" >1974-01-31</td>
      <td id="T_4f6ea_row19_col3" class="data row19 col3" >1,000,000.00</td>
      <td id="T_4f6ea_row19_col4" class="data row19 col4" >1,000,000.00</td>
      <td id="T_4f6ea_row19_col5" class="data row19 col5" >True</td>
      <td id="T_4f6ea_row19_col6" class="data row19 col6" >1,002,555.56</td>
      <td id="T_4f6ea_row19_col7" class="data row19 col7" >CLP</td>
      <td id="T_4f6ea_row19_col8" class="data row19 col8" >10,000.00</td>
      <td id="T_4f6ea_row19_col9" class="data row19 col9" >10,000.00</td>
      <td id="T_4f6ea_row19_col10" class="data row19 col10" >0.0000%</td>
      <td id="T_4f6ea_row19_col11" class="data row19 col11" >2,555.56</td>
      <td id="T_4f6ea_row19_col12" class="data row19 col12" >1.0000%</td>
      <td id="T_4f6ea_row19_col13" class="data row19 col13" >1.00</td>
      <td id="T_4f6ea_row19_col14" class="data row19 col14" >LinAct360</td>
    </tr>
  </tbody>
</table>




Se puede customizar la amortización de la siguiente forma:


```python
cna = qcf.CustomNotionalAmort()
cna.set_size(19)
```


```python
cna.set_notional_amort_at(0, 1000000, 0)
for i in range(1, icp_clp2_leg.size()):
    prev_amort = cna.get_amort_at(i - 1)
    prev_notional = cna.get_notional_at(i - 1)
    if i == 10 or i == icp_clp2_leg.size() - 1:
        cna.set_notional_amort_at(i, prev_notional - prev_amort, 500000)
    else:
        cna.set_notional_amort_at(i, prev_notional - prev_amort, 0)

for i in range(icp_clp2_leg.size()):
    cshflw = icp_clp2_leg.get_cashflow_at(i)
    cshflw.set_nominal(cna.get_notional_at(i))
    cshflw.set_amortization(cna.get_amort_at(i))
```


```python
# Se define un list donde almacenar los resultados de la función show
tabla = []
for i in range(0, icp_clp2_leg.size()):
    tabla.append(qcf.show(icp_clp2_leg.get_cashflow_at(i)))

# Se utiliza tabla para inicializar el Dataframe
columnas = ['fecha_inicial', 'fecha__final', 'fecha__pago', 'nominal', 'amort', 'amort_es_flujo', 'flujo',
            'moneda', 'icp_inicial', 'icp_final', 'valor_tasa', 'interes', 'spread', 'gearing', 'tipo_tasa']
df9 = pd.DataFrame(tabla, columns=columnas)

# Se despliega la data en este formato
df9.style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_56310">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_56310_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_56310_level0_col1" class="col_heading level0 col1" >fecha__final</th>
      <th id="T_56310_level0_col2" class="col_heading level0 col2" >fecha__pago</th>
      <th id="T_56310_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_56310_level0_col4" class="col_heading level0 col4" >amort</th>
      <th id="T_56310_level0_col5" class="col_heading level0 col5" >amort_es_flujo</th>
      <th id="T_56310_level0_col6" class="col_heading level0 col6" >flujo</th>
      <th id="T_56310_level0_col7" class="col_heading level0 col7" >moneda</th>
      <th id="T_56310_level0_col8" class="col_heading level0 col8" >icp_inicial</th>
      <th id="T_56310_level0_col9" class="col_heading level0 col9" >icp_final</th>
      <th id="T_56310_level0_col10" class="col_heading level0 col10" >valor_tasa</th>
      <th id="T_56310_level0_col11" class="col_heading level0 col11" >interes</th>
      <th id="T_56310_level0_col12" class="col_heading level0 col12" >spread</th>
      <th id="T_56310_level0_col13" class="col_heading level0 col13" >gearing</th>
      <th id="T_56310_level0_col14" class="col_heading level0 col14" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_56310_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_56310_row0_col0" class="data row0 col0" >1969-01-31</td>
      <td id="T_56310_row0_col1" class="data row0 col1" >1969-04-30</td>
      <td id="T_56310_row0_col2" class="data row0 col2" >1969-04-30</td>
      <td id="T_56310_row0_col3" class="data row0 col3" >1,000,000.00</td>
      <td id="T_56310_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_56310_row0_col5" class="data row0 col5" >True</td>
      <td id="T_56310_row0_col6" class="data row0 col6" >2,472.22</td>
      <td id="T_56310_row0_col7" class="data row0 col7" >CLP</td>
      <td id="T_56310_row0_col8" class="data row0 col8" >10,000.00</td>
      <td id="T_56310_row0_col9" class="data row0 col9" >10,000.00</td>
      <td id="T_56310_row0_col10" class="data row0 col10" >0.0000%</td>
      <td id="T_56310_row0_col11" class="data row0 col11" >2,472.22</td>
      <td id="T_56310_row0_col12" class="data row0 col12" >1.0000%</td>
      <td id="T_56310_row0_col13" class="data row0 col13" >1.00</td>
      <td id="T_56310_row0_col14" class="data row0 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_56310_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_56310_row1_col0" class="data row1 col0" >1969-04-30</td>
      <td id="T_56310_row1_col1" class="data row1 col1" >1969-07-31</td>
      <td id="T_56310_row1_col2" class="data row1 col2" >1969-07-31</td>
      <td id="T_56310_row1_col3" class="data row1 col3" >1,000,000.00</td>
      <td id="T_56310_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_56310_row1_col5" class="data row1 col5" >True</td>
      <td id="T_56310_row1_col6" class="data row1 col6" >2,555.56</td>
      <td id="T_56310_row1_col7" class="data row1 col7" >CLP</td>
      <td id="T_56310_row1_col8" class="data row1 col8" >10,000.00</td>
      <td id="T_56310_row1_col9" class="data row1 col9" >10,000.00</td>
      <td id="T_56310_row1_col10" class="data row1 col10" >0.0000%</td>
      <td id="T_56310_row1_col11" class="data row1 col11" >2,555.56</td>
      <td id="T_56310_row1_col12" class="data row1 col12" >1.0000%</td>
      <td id="T_56310_row1_col13" class="data row1 col13" >1.00</td>
      <td id="T_56310_row1_col14" class="data row1 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_56310_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_56310_row2_col0" class="data row2 col0" >1969-07-31</td>
      <td id="T_56310_row2_col1" class="data row2 col1" >1969-10-31</td>
      <td id="T_56310_row2_col2" class="data row2 col2" >1969-10-31</td>
      <td id="T_56310_row2_col3" class="data row2 col3" >1,000,000.00</td>
      <td id="T_56310_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_56310_row2_col5" class="data row2 col5" >True</td>
      <td id="T_56310_row2_col6" class="data row2 col6" >2,555.56</td>
      <td id="T_56310_row2_col7" class="data row2 col7" >CLP</td>
      <td id="T_56310_row2_col8" class="data row2 col8" >10,000.00</td>
      <td id="T_56310_row2_col9" class="data row2 col9" >10,000.00</td>
      <td id="T_56310_row2_col10" class="data row2 col10" >0.0000%</td>
      <td id="T_56310_row2_col11" class="data row2 col11" >2,555.56</td>
      <td id="T_56310_row2_col12" class="data row2 col12" >1.0000%</td>
      <td id="T_56310_row2_col13" class="data row2 col13" >1.00</td>
      <td id="T_56310_row2_col14" class="data row2 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_56310_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_56310_row3_col0" class="data row3 col0" >1969-10-31</td>
      <td id="T_56310_row3_col1" class="data row3 col1" >1970-01-30</td>
      <td id="T_56310_row3_col2" class="data row3 col2" >1970-01-30</td>
      <td id="T_56310_row3_col3" class="data row3 col3" >1,000,000.00</td>
      <td id="T_56310_row3_col4" class="data row3 col4" >0.00</td>
      <td id="T_56310_row3_col5" class="data row3 col5" >True</td>
      <td id="T_56310_row3_col6" class="data row3 col6" >2,527.78</td>
      <td id="T_56310_row3_col7" class="data row3 col7" >CLP</td>
      <td id="T_56310_row3_col8" class="data row3 col8" >10,000.00</td>
      <td id="T_56310_row3_col9" class="data row3 col9" >10,000.00</td>
      <td id="T_56310_row3_col10" class="data row3 col10" >0.0000%</td>
      <td id="T_56310_row3_col11" class="data row3 col11" >2,527.78</td>
      <td id="T_56310_row3_col12" class="data row3 col12" >1.0000%</td>
      <td id="T_56310_row3_col13" class="data row3 col13" >1.00</td>
      <td id="T_56310_row3_col14" class="data row3 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_56310_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_56310_row4_col0" class="data row4 col0" >1970-01-30</td>
      <td id="T_56310_row4_col1" class="data row4 col1" >1970-04-30</td>
      <td id="T_56310_row4_col2" class="data row4 col2" >1970-04-30</td>
      <td id="T_56310_row4_col3" class="data row4 col3" >1,000,000.00</td>
      <td id="T_56310_row4_col4" class="data row4 col4" >0.00</td>
      <td id="T_56310_row4_col5" class="data row4 col5" >True</td>
      <td id="T_56310_row4_col6" class="data row4 col6" >2,500.00</td>
      <td id="T_56310_row4_col7" class="data row4 col7" >CLP</td>
      <td id="T_56310_row4_col8" class="data row4 col8" >10,000.00</td>
      <td id="T_56310_row4_col9" class="data row4 col9" >10,000.00</td>
      <td id="T_56310_row4_col10" class="data row4 col10" >0.0000%</td>
      <td id="T_56310_row4_col11" class="data row4 col11" >2,500.00</td>
      <td id="T_56310_row4_col12" class="data row4 col12" >1.0000%</td>
      <td id="T_56310_row4_col13" class="data row4 col13" >1.00</td>
      <td id="T_56310_row4_col14" class="data row4 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_56310_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_56310_row5_col0" class="data row5 col0" >1970-04-30</td>
      <td id="T_56310_row5_col1" class="data row5 col1" >1970-07-31</td>
      <td id="T_56310_row5_col2" class="data row5 col2" >1970-07-31</td>
      <td id="T_56310_row5_col3" class="data row5 col3" >1,000,000.00</td>
      <td id="T_56310_row5_col4" class="data row5 col4" >0.00</td>
      <td id="T_56310_row5_col5" class="data row5 col5" >True</td>
      <td id="T_56310_row5_col6" class="data row5 col6" >2,555.56</td>
      <td id="T_56310_row5_col7" class="data row5 col7" >CLP</td>
      <td id="T_56310_row5_col8" class="data row5 col8" >10,000.00</td>
      <td id="T_56310_row5_col9" class="data row5 col9" >10,000.00</td>
      <td id="T_56310_row5_col10" class="data row5 col10" >0.0000%</td>
      <td id="T_56310_row5_col11" class="data row5 col11" >2,555.56</td>
      <td id="T_56310_row5_col12" class="data row5 col12" >1.0000%</td>
      <td id="T_56310_row5_col13" class="data row5 col13" >1.00</td>
      <td id="T_56310_row5_col14" class="data row5 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_56310_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_56310_row6_col0" class="data row6 col0" >1970-07-31</td>
      <td id="T_56310_row6_col1" class="data row6 col1" >1970-10-30</td>
      <td id="T_56310_row6_col2" class="data row6 col2" >1970-10-30</td>
      <td id="T_56310_row6_col3" class="data row6 col3" >1,000,000.00</td>
      <td id="T_56310_row6_col4" class="data row6 col4" >0.00</td>
      <td id="T_56310_row6_col5" class="data row6 col5" >True</td>
      <td id="T_56310_row6_col6" class="data row6 col6" >2,527.78</td>
      <td id="T_56310_row6_col7" class="data row6 col7" >CLP</td>
      <td id="T_56310_row6_col8" class="data row6 col8" >10,000.00</td>
      <td id="T_56310_row6_col9" class="data row6 col9" >10,000.00</td>
      <td id="T_56310_row6_col10" class="data row6 col10" >0.0000%</td>
      <td id="T_56310_row6_col11" class="data row6 col11" >2,527.78</td>
      <td id="T_56310_row6_col12" class="data row6 col12" >1.0000%</td>
      <td id="T_56310_row6_col13" class="data row6 col13" >1.00</td>
      <td id="T_56310_row6_col14" class="data row6 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_56310_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_56310_row7_col0" class="data row7 col0" >1970-10-30</td>
      <td id="T_56310_row7_col1" class="data row7 col1" >1971-01-29</td>
      <td id="T_56310_row7_col2" class="data row7 col2" >1971-01-29</td>
      <td id="T_56310_row7_col3" class="data row7 col3" >1,000,000.00</td>
      <td id="T_56310_row7_col4" class="data row7 col4" >0.00</td>
      <td id="T_56310_row7_col5" class="data row7 col5" >True</td>
      <td id="T_56310_row7_col6" class="data row7 col6" >2,527.78</td>
      <td id="T_56310_row7_col7" class="data row7 col7" >CLP</td>
      <td id="T_56310_row7_col8" class="data row7 col8" >10,000.00</td>
      <td id="T_56310_row7_col9" class="data row7 col9" >10,000.00</td>
      <td id="T_56310_row7_col10" class="data row7 col10" >0.0000%</td>
      <td id="T_56310_row7_col11" class="data row7 col11" >2,527.78</td>
      <td id="T_56310_row7_col12" class="data row7 col12" >1.0000%</td>
      <td id="T_56310_row7_col13" class="data row7 col13" >1.00</td>
      <td id="T_56310_row7_col14" class="data row7 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_56310_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_56310_row8_col0" class="data row8 col0" >1971-01-29</td>
      <td id="T_56310_row8_col1" class="data row8 col1" >1971-04-30</td>
      <td id="T_56310_row8_col2" class="data row8 col2" >1971-04-30</td>
      <td id="T_56310_row8_col3" class="data row8 col3" >1,000,000.00</td>
      <td id="T_56310_row8_col4" class="data row8 col4" >0.00</td>
      <td id="T_56310_row8_col5" class="data row8 col5" >True</td>
      <td id="T_56310_row8_col6" class="data row8 col6" >2,527.78</td>
      <td id="T_56310_row8_col7" class="data row8 col7" >CLP</td>
      <td id="T_56310_row8_col8" class="data row8 col8" >10,000.00</td>
      <td id="T_56310_row8_col9" class="data row8 col9" >10,000.00</td>
      <td id="T_56310_row8_col10" class="data row8 col10" >0.0000%</td>
      <td id="T_56310_row8_col11" class="data row8 col11" >2,527.78</td>
      <td id="T_56310_row8_col12" class="data row8 col12" >1.0000%</td>
      <td id="T_56310_row8_col13" class="data row8 col13" >1.00</td>
      <td id="T_56310_row8_col14" class="data row8 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_56310_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_56310_row9_col0" class="data row9 col0" >1971-04-30</td>
      <td id="T_56310_row9_col1" class="data row9 col1" >1971-07-30</td>
      <td id="T_56310_row9_col2" class="data row9 col2" >1971-07-30</td>
      <td id="T_56310_row9_col3" class="data row9 col3" >1,000,000.00</td>
      <td id="T_56310_row9_col4" class="data row9 col4" >0.00</td>
      <td id="T_56310_row9_col5" class="data row9 col5" >True</td>
      <td id="T_56310_row9_col6" class="data row9 col6" >2,527.78</td>
      <td id="T_56310_row9_col7" class="data row9 col7" >CLP</td>
      <td id="T_56310_row9_col8" class="data row9 col8" >10,000.00</td>
      <td id="T_56310_row9_col9" class="data row9 col9" >10,000.00</td>
      <td id="T_56310_row9_col10" class="data row9 col10" >0.0000%</td>
      <td id="T_56310_row9_col11" class="data row9 col11" >2,527.78</td>
      <td id="T_56310_row9_col12" class="data row9 col12" >1.0000%</td>
      <td id="T_56310_row9_col13" class="data row9 col13" >1.00</td>
      <td id="T_56310_row9_col14" class="data row9 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_56310_level0_row10" class="row_heading level0 row10" >10</th>
      <td id="T_56310_row10_col0" class="data row10 col0" >1971-07-30</td>
      <td id="T_56310_row10_col1" class="data row10 col1" >1971-10-29</td>
      <td id="T_56310_row10_col2" class="data row10 col2" >1971-10-29</td>
      <td id="T_56310_row10_col3" class="data row10 col3" >1,000,000.00</td>
      <td id="T_56310_row10_col4" class="data row10 col4" >500,000.00</td>
      <td id="T_56310_row10_col5" class="data row10 col5" >True</td>
      <td id="T_56310_row10_col6" class="data row10 col6" >502,527.78</td>
      <td id="T_56310_row10_col7" class="data row10 col7" >CLP</td>
      <td id="T_56310_row10_col8" class="data row10 col8" >10,000.00</td>
      <td id="T_56310_row10_col9" class="data row10 col9" >10,000.00</td>
      <td id="T_56310_row10_col10" class="data row10 col10" >0.0000%</td>
      <td id="T_56310_row10_col11" class="data row10 col11" >2,527.78</td>
      <td id="T_56310_row10_col12" class="data row10 col12" >1.0000%</td>
      <td id="T_56310_row10_col13" class="data row10 col13" >1.00</td>
      <td id="T_56310_row10_col14" class="data row10 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_56310_level0_row11" class="row_heading level0 row11" >11</th>
      <td id="T_56310_row11_col0" class="data row11 col0" >1971-10-29</td>
      <td id="T_56310_row11_col1" class="data row11 col1" >1972-01-31</td>
      <td id="T_56310_row11_col2" class="data row11 col2" >1972-01-31</td>
      <td id="T_56310_row11_col3" class="data row11 col3" >500,000.00</td>
      <td id="T_56310_row11_col4" class="data row11 col4" >0.00</td>
      <td id="T_56310_row11_col5" class="data row11 col5" >True</td>
      <td id="T_56310_row11_col6" class="data row11 col6" >1,305.56</td>
      <td id="T_56310_row11_col7" class="data row11 col7" >CLP</td>
      <td id="T_56310_row11_col8" class="data row11 col8" >10,000.00</td>
      <td id="T_56310_row11_col9" class="data row11 col9" >10,000.00</td>
      <td id="T_56310_row11_col10" class="data row11 col10" >0.0000%</td>
      <td id="T_56310_row11_col11" class="data row11 col11" >1,305.56</td>
      <td id="T_56310_row11_col12" class="data row11 col12" >1.0000%</td>
      <td id="T_56310_row11_col13" class="data row11 col13" >1.00</td>
      <td id="T_56310_row11_col14" class="data row11 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_56310_level0_row12" class="row_heading level0 row12" >12</th>
      <td id="T_56310_row12_col0" class="data row12 col0" >1972-01-31</td>
      <td id="T_56310_row12_col1" class="data row12 col1" >1972-04-28</td>
      <td id="T_56310_row12_col2" class="data row12 col2" >1972-04-28</td>
      <td id="T_56310_row12_col3" class="data row12 col3" >500,000.00</td>
      <td id="T_56310_row12_col4" class="data row12 col4" >0.00</td>
      <td id="T_56310_row12_col5" class="data row12 col5" >True</td>
      <td id="T_56310_row12_col6" class="data row12 col6" >1,222.22</td>
      <td id="T_56310_row12_col7" class="data row12 col7" >CLP</td>
      <td id="T_56310_row12_col8" class="data row12 col8" >10,000.00</td>
      <td id="T_56310_row12_col9" class="data row12 col9" >10,000.00</td>
      <td id="T_56310_row12_col10" class="data row12 col10" >0.0000%</td>
      <td id="T_56310_row12_col11" class="data row12 col11" >1,222.22</td>
      <td id="T_56310_row12_col12" class="data row12 col12" >1.0000%</td>
      <td id="T_56310_row12_col13" class="data row12 col13" >1.00</td>
      <td id="T_56310_row12_col14" class="data row12 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_56310_level0_row13" class="row_heading level0 row13" >13</th>
      <td id="T_56310_row13_col0" class="data row13 col0" >1972-04-28</td>
      <td id="T_56310_row13_col1" class="data row13 col1" >1972-07-31</td>
      <td id="T_56310_row13_col2" class="data row13 col2" >1972-07-31</td>
      <td id="T_56310_row13_col3" class="data row13 col3" >500,000.00</td>
      <td id="T_56310_row13_col4" class="data row13 col4" >0.00</td>
      <td id="T_56310_row13_col5" class="data row13 col5" >True</td>
      <td id="T_56310_row13_col6" class="data row13 col6" >1,305.56</td>
      <td id="T_56310_row13_col7" class="data row13 col7" >CLP</td>
      <td id="T_56310_row13_col8" class="data row13 col8" >10,000.00</td>
      <td id="T_56310_row13_col9" class="data row13 col9" >10,000.00</td>
      <td id="T_56310_row13_col10" class="data row13 col10" >0.0000%</td>
      <td id="T_56310_row13_col11" class="data row13 col11" >1,305.56</td>
      <td id="T_56310_row13_col12" class="data row13 col12" >1.0000%</td>
      <td id="T_56310_row13_col13" class="data row13 col13" >1.00</td>
      <td id="T_56310_row13_col14" class="data row13 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_56310_level0_row14" class="row_heading level0 row14" >14</th>
      <td id="T_56310_row14_col0" class="data row14 col0" >1972-07-31</td>
      <td id="T_56310_row14_col1" class="data row14 col1" >1972-10-31</td>
      <td id="T_56310_row14_col2" class="data row14 col2" >1972-10-31</td>
      <td id="T_56310_row14_col3" class="data row14 col3" >500,000.00</td>
      <td id="T_56310_row14_col4" class="data row14 col4" >0.00</td>
      <td id="T_56310_row14_col5" class="data row14 col5" >True</td>
      <td id="T_56310_row14_col6" class="data row14 col6" >1,277.78</td>
      <td id="T_56310_row14_col7" class="data row14 col7" >CLP</td>
      <td id="T_56310_row14_col8" class="data row14 col8" >10,000.00</td>
      <td id="T_56310_row14_col9" class="data row14 col9" >10,000.00</td>
      <td id="T_56310_row14_col10" class="data row14 col10" >0.0000%</td>
      <td id="T_56310_row14_col11" class="data row14 col11" >1,277.78</td>
      <td id="T_56310_row14_col12" class="data row14 col12" >1.0000%</td>
      <td id="T_56310_row14_col13" class="data row14 col13" >1.00</td>
      <td id="T_56310_row14_col14" class="data row14 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_56310_level0_row15" class="row_heading level0 row15" >15</th>
      <td id="T_56310_row15_col0" class="data row15 col0" >1972-10-31</td>
      <td id="T_56310_row15_col1" class="data row15 col1" >1973-01-31</td>
      <td id="T_56310_row15_col2" class="data row15 col2" >1973-01-31</td>
      <td id="T_56310_row15_col3" class="data row15 col3" >500,000.00</td>
      <td id="T_56310_row15_col4" class="data row15 col4" >0.00</td>
      <td id="T_56310_row15_col5" class="data row15 col5" >True</td>
      <td id="T_56310_row15_col6" class="data row15 col6" >1,277.78</td>
      <td id="T_56310_row15_col7" class="data row15 col7" >CLP</td>
      <td id="T_56310_row15_col8" class="data row15 col8" >10,000.00</td>
      <td id="T_56310_row15_col9" class="data row15 col9" >10,000.00</td>
      <td id="T_56310_row15_col10" class="data row15 col10" >0.0000%</td>
      <td id="T_56310_row15_col11" class="data row15 col11" >1,277.78</td>
      <td id="T_56310_row15_col12" class="data row15 col12" >1.0000%</td>
      <td id="T_56310_row15_col13" class="data row15 col13" >1.00</td>
      <td id="T_56310_row15_col14" class="data row15 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_56310_level0_row16" class="row_heading level0 row16" >16</th>
      <td id="T_56310_row16_col0" class="data row16 col0" >1973-01-31</td>
      <td id="T_56310_row16_col1" class="data row16 col1" >1973-04-30</td>
      <td id="T_56310_row16_col2" class="data row16 col2" >1973-04-30</td>
      <td id="T_56310_row16_col3" class="data row16 col3" >500,000.00</td>
      <td id="T_56310_row16_col4" class="data row16 col4" >0.00</td>
      <td id="T_56310_row16_col5" class="data row16 col5" >True</td>
      <td id="T_56310_row16_col6" class="data row16 col6" >1,236.11</td>
      <td id="T_56310_row16_col7" class="data row16 col7" >CLP</td>
      <td id="T_56310_row16_col8" class="data row16 col8" >10,000.00</td>
      <td id="T_56310_row16_col9" class="data row16 col9" >10,000.00</td>
      <td id="T_56310_row16_col10" class="data row16 col10" >0.0000%</td>
      <td id="T_56310_row16_col11" class="data row16 col11" >1,236.11</td>
      <td id="T_56310_row16_col12" class="data row16 col12" >1.0000%</td>
      <td id="T_56310_row16_col13" class="data row16 col13" >1.00</td>
      <td id="T_56310_row16_col14" class="data row16 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_56310_level0_row17" class="row_heading level0 row17" >17</th>
      <td id="T_56310_row17_col0" class="data row17 col0" >1973-04-30</td>
      <td id="T_56310_row17_col1" class="data row17 col1" >1973-07-31</td>
      <td id="T_56310_row17_col2" class="data row17 col2" >1973-07-31</td>
      <td id="T_56310_row17_col3" class="data row17 col3" >500,000.00</td>
      <td id="T_56310_row17_col4" class="data row17 col4" >0.00</td>
      <td id="T_56310_row17_col5" class="data row17 col5" >True</td>
      <td id="T_56310_row17_col6" class="data row17 col6" >1,277.78</td>
      <td id="T_56310_row17_col7" class="data row17 col7" >CLP</td>
      <td id="T_56310_row17_col8" class="data row17 col8" >10,000.00</td>
      <td id="T_56310_row17_col9" class="data row17 col9" >10,000.00</td>
      <td id="T_56310_row17_col10" class="data row17 col10" >0.0000%</td>
      <td id="T_56310_row17_col11" class="data row17 col11" >1,277.78</td>
      <td id="T_56310_row17_col12" class="data row17 col12" >1.0000%</td>
      <td id="T_56310_row17_col13" class="data row17 col13" >1.00</td>
      <td id="T_56310_row17_col14" class="data row17 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_56310_level0_row18" class="row_heading level0 row18" >18</th>
      <td id="T_56310_row18_col0" class="data row18 col0" >1973-07-31</td>
      <td id="T_56310_row18_col1" class="data row18 col1" >1973-10-31</td>
      <td id="T_56310_row18_col2" class="data row18 col2" >1973-10-31</td>
      <td id="T_56310_row18_col3" class="data row18 col3" >500,000.00</td>
      <td id="T_56310_row18_col4" class="data row18 col4" >0.00</td>
      <td id="T_56310_row18_col5" class="data row18 col5" >True</td>
      <td id="T_56310_row18_col6" class="data row18 col6" >1,277.78</td>
      <td id="T_56310_row18_col7" class="data row18 col7" >CLP</td>
      <td id="T_56310_row18_col8" class="data row18 col8" >10,000.00</td>
      <td id="T_56310_row18_col9" class="data row18 col9" >10,000.00</td>
      <td id="T_56310_row18_col10" class="data row18 col10" >0.0000%</td>
      <td id="T_56310_row18_col11" class="data row18 col11" >1,277.78</td>
      <td id="T_56310_row18_col12" class="data row18 col12" >1.0000%</td>
      <td id="T_56310_row18_col13" class="data row18 col13" >1.00</td>
      <td id="T_56310_row18_col14" class="data row18 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_56310_level0_row19" class="row_heading level0 row19" >19</th>
      <td id="T_56310_row19_col0" class="data row19 col0" >1973-10-31</td>
      <td id="T_56310_row19_col1" class="data row19 col1" >1974-01-31</td>
      <td id="T_56310_row19_col2" class="data row19 col2" >1974-01-31</td>
      <td id="T_56310_row19_col3" class="data row19 col3" >500,000.00</td>
      <td id="T_56310_row19_col4" class="data row19 col4" >500,000.00</td>
      <td id="T_56310_row19_col5" class="data row19 col5" >True</td>
      <td id="T_56310_row19_col6" class="data row19 col6" >501,277.78</td>
      <td id="T_56310_row19_col7" class="data row19 col7" >CLP</td>
      <td id="T_56310_row19_col8" class="data row19 col8" >10,000.00</td>
      <td id="T_56310_row19_col9" class="data row19 col9" >10,000.00</td>
      <td id="T_56310_row19_col10" class="data row19 col10" >0.0000%</td>
      <td id="T_56310_row19_col11" class="data row19 col11" >1,277.78</td>
      <td id="T_56310_row19_col12" class="data row19 col12" >1.0000%</td>
      <td id="T_56310_row19_col13" class="data row19 col13" >1.00</td>
      <td id="T_56310_row19_col14" class="data row19 col14" >LinAct360</td>
    </tr>
  </tbody>
</table>




### Construcción Asistida de un `IcpClfLeg`
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
- `gearing`: spread multiplicativo

Vamos a un ejemplo. Cambiando los parámetros anteriores se puede visualizar el efecto de ellos en la construcción. 

**NOTA:** para construir un `Leg` con `IcpClfCashflow` y amortización customizada, sólo se debe cambiar el parámetro **nominal** por **CustomNotionalAndAmort** e invocar el método `qcf.LegFactory.build_custom_amort_icp_clf_leg(...)`.


```python
# Se da de alta los parámetros requeridos
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(31, 1, 1969)
fecha_final = qcf.QCDate(31, 1, 1974)
bus_adj_rule = qcf.BusyAdjRules.MODFOLLOW
periodicidad_pago = qcf.Tenor('3M')
periodo_irregular_pago = qcf.StubPeriod.NO
calendario = qcf.BusinessCalendar(fecha_inicio, 20)
lag_pago = 0
nominal = 1000000.0
amort_es_flujo = True
spread = .01
gearing = 1.0

icp_clf_leg = qcf.LegFactory.build_bullet_icp_clf_leg(
    rp,
    fecha_inicio,
    fecha_final,
    bus_adj_rule,
    periodicidad_pago,
    periodo_irregular_pago,
    calendario,
    lag_pago,
    nominal,
    amort_es_flujo,
    spread,
    gearing
)
```


```python
# Se define un list donde almacenar los resultados de la función show
tabla = []
for i in range(0, icp_clf_leg.size()):
    tabla.append(qcf.show(icp_clf_leg.get_cashflow_at(i)))

# Se utiliza tabla para inicializar el Dataframe
columnas = ['fecha_inicial', 'fecha__final', 'fecha__pago', 'nominal', 'amort', 'amort_es_flujo', 'flujo',
            'moneda', 'icp_inicial', 'icp_final', 'uf_inicial', 'uf_final',
            'valor_tasa', 'interes', 'spread', 'gearing', 'tipo_tasa']
df8 = pd.DataFrame(tabla, columns=columnas)

# Se despliega la data en este formato
df8.style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_82262">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_82262_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_82262_level0_col1" class="col_heading level0 col1" >fecha__final</th>
      <th id="T_82262_level0_col2" class="col_heading level0 col2" >fecha__pago</th>
      <th id="T_82262_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_82262_level0_col4" class="col_heading level0 col4" >amort</th>
      <th id="T_82262_level0_col5" class="col_heading level0 col5" >amort_es_flujo</th>
      <th id="T_82262_level0_col6" class="col_heading level0 col6" >flujo</th>
      <th id="T_82262_level0_col7" class="col_heading level0 col7" >moneda</th>
      <th id="T_82262_level0_col8" class="col_heading level0 col8" >icp_inicial</th>
      <th id="T_82262_level0_col9" class="col_heading level0 col9" >icp_final</th>
      <th id="T_82262_level0_col10" class="col_heading level0 col10" >uf_inicial</th>
      <th id="T_82262_level0_col11" class="col_heading level0 col11" >uf_final</th>
      <th id="T_82262_level0_col12" class="col_heading level0 col12" >valor_tasa</th>
      <th id="T_82262_level0_col13" class="col_heading level0 col13" >interes</th>
      <th id="T_82262_level0_col14" class="col_heading level0 col14" >spread</th>
      <th id="T_82262_level0_col15" class="col_heading level0 col15" >gearing</th>
      <th id="T_82262_level0_col16" class="col_heading level0 col16" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_82262_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_82262_row0_col0" class="data row0 col0" >1969-01-31</td>
      <td id="T_82262_row0_col1" class="data row0 col1" >1969-04-30</td>
      <td id="T_82262_row0_col2" class="data row0 col2" >1969-04-30</td>
      <td id="T_82262_row0_col3" class="data row0 col3" >1,000,000.00</td>
      <td id="T_82262_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_82262_row0_col5" class="data row0 col5" >True</td>
      <td id="T_82262_row0_col6" class="data row0 col6" >2,472.22</td>
      <td id="T_82262_row0_col7" class="data row0 col7" >CLF</td>
      <td id="T_82262_row0_col8" class="data row0 col8" >10,000.00</td>
      <td id="T_82262_row0_col9" class="data row0 col9" >10,000.00</td>
      <td id="T_82262_row0_col10" class="data row0 col10" >35000.000000</td>
      <td id="T_82262_row0_col11" class="data row0 col11" >35000.000000</td>
      <td id="T_82262_row0_col12" class="data row0 col12" >1.0000%</td>
      <td id="T_82262_row0_col13" class="data row0 col13" >2,472.22</td>
      <td id="T_82262_row0_col14" class="data row0 col14" >1.0000%</td>
      <td id="T_82262_row0_col15" class="data row0 col15" >1.00</td>
      <td id="T_82262_row0_col16" class="data row0 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_82262_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_82262_row1_col0" class="data row1 col0" >1969-04-30</td>
      <td id="T_82262_row1_col1" class="data row1 col1" >1969-07-31</td>
      <td id="T_82262_row1_col2" class="data row1 col2" >1969-07-31</td>
      <td id="T_82262_row1_col3" class="data row1 col3" >1,000,000.00</td>
      <td id="T_82262_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_82262_row1_col5" class="data row1 col5" >True</td>
      <td id="T_82262_row1_col6" class="data row1 col6" >2,555.56</td>
      <td id="T_82262_row1_col7" class="data row1 col7" >CLF</td>
      <td id="T_82262_row1_col8" class="data row1 col8" >10,000.00</td>
      <td id="T_82262_row1_col9" class="data row1 col9" >10,000.00</td>
      <td id="T_82262_row1_col10" class="data row1 col10" >35000.000000</td>
      <td id="T_82262_row1_col11" class="data row1 col11" >35000.000000</td>
      <td id="T_82262_row1_col12" class="data row1 col12" >1.0000%</td>
      <td id="T_82262_row1_col13" class="data row1 col13" >2,555.56</td>
      <td id="T_82262_row1_col14" class="data row1 col14" >1.0000%</td>
      <td id="T_82262_row1_col15" class="data row1 col15" >1.00</td>
      <td id="T_82262_row1_col16" class="data row1 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_82262_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_82262_row2_col0" class="data row2 col0" >1969-07-31</td>
      <td id="T_82262_row2_col1" class="data row2 col1" >1969-10-31</td>
      <td id="T_82262_row2_col2" class="data row2 col2" >1969-10-31</td>
      <td id="T_82262_row2_col3" class="data row2 col3" >1,000,000.00</td>
      <td id="T_82262_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_82262_row2_col5" class="data row2 col5" >True</td>
      <td id="T_82262_row2_col6" class="data row2 col6" >2,555.56</td>
      <td id="T_82262_row2_col7" class="data row2 col7" >CLF</td>
      <td id="T_82262_row2_col8" class="data row2 col8" >10,000.00</td>
      <td id="T_82262_row2_col9" class="data row2 col9" >10,000.00</td>
      <td id="T_82262_row2_col10" class="data row2 col10" >35000.000000</td>
      <td id="T_82262_row2_col11" class="data row2 col11" >35000.000000</td>
      <td id="T_82262_row2_col12" class="data row2 col12" >1.0000%</td>
      <td id="T_82262_row2_col13" class="data row2 col13" >2,555.56</td>
      <td id="T_82262_row2_col14" class="data row2 col14" >1.0000%</td>
      <td id="T_82262_row2_col15" class="data row2 col15" >1.00</td>
      <td id="T_82262_row2_col16" class="data row2 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_82262_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_82262_row3_col0" class="data row3 col0" >1969-10-31</td>
      <td id="T_82262_row3_col1" class="data row3 col1" >1970-01-30</td>
      <td id="T_82262_row3_col2" class="data row3 col2" >1970-01-30</td>
      <td id="T_82262_row3_col3" class="data row3 col3" >1,000,000.00</td>
      <td id="T_82262_row3_col4" class="data row3 col4" >0.00</td>
      <td id="T_82262_row3_col5" class="data row3 col5" >True</td>
      <td id="T_82262_row3_col6" class="data row3 col6" >2,527.78</td>
      <td id="T_82262_row3_col7" class="data row3 col7" >CLF</td>
      <td id="T_82262_row3_col8" class="data row3 col8" >10,000.00</td>
      <td id="T_82262_row3_col9" class="data row3 col9" >10,000.00</td>
      <td id="T_82262_row3_col10" class="data row3 col10" >35000.000000</td>
      <td id="T_82262_row3_col11" class="data row3 col11" >35000.000000</td>
      <td id="T_82262_row3_col12" class="data row3 col12" >1.0000%</td>
      <td id="T_82262_row3_col13" class="data row3 col13" >2,527.78</td>
      <td id="T_82262_row3_col14" class="data row3 col14" >1.0000%</td>
      <td id="T_82262_row3_col15" class="data row3 col15" >1.00</td>
      <td id="T_82262_row3_col16" class="data row3 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_82262_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_82262_row4_col0" class="data row4 col0" >1970-01-30</td>
      <td id="T_82262_row4_col1" class="data row4 col1" >1970-04-30</td>
      <td id="T_82262_row4_col2" class="data row4 col2" >1970-04-30</td>
      <td id="T_82262_row4_col3" class="data row4 col3" >1,000,000.00</td>
      <td id="T_82262_row4_col4" class="data row4 col4" >0.00</td>
      <td id="T_82262_row4_col5" class="data row4 col5" >True</td>
      <td id="T_82262_row4_col6" class="data row4 col6" >2,500.00</td>
      <td id="T_82262_row4_col7" class="data row4 col7" >CLF</td>
      <td id="T_82262_row4_col8" class="data row4 col8" >10,000.00</td>
      <td id="T_82262_row4_col9" class="data row4 col9" >10,000.00</td>
      <td id="T_82262_row4_col10" class="data row4 col10" >35000.000000</td>
      <td id="T_82262_row4_col11" class="data row4 col11" >35000.000000</td>
      <td id="T_82262_row4_col12" class="data row4 col12" >1.0000%</td>
      <td id="T_82262_row4_col13" class="data row4 col13" >2,500.00</td>
      <td id="T_82262_row4_col14" class="data row4 col14" >1.0000%</td>
      <td id="T_82262_row4_col15" class="data row4 col15" >1.00</td>
      <td id="T_82262_row4_col16" class="data row4 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_82262_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_82262_row5_col0" class="data row5 col0" >1970-04-30</td>
      <td id="T_82262_row5_col1" class="data row5 col1" >1970-07-31</td>
      <td id="T_82262_row5_col2" class="data row5 col2" >1970-07-31</td>
      <td id="T_82262_row5_col3" class="data row5 col3" >1,000,000.00</td>
      <td id="T_82262_row5_col4" class="data row5 col4" >0.00</td>
      <td id="T_82262_row5_col5" class="data row5 col5" >True</td>
      <td id="T_82262_row5_col6" class="data row5 col6" >2,555.56</td>
      <td id="T_82262_row5_col7" class="data row5 col7" >CLF</td>
      <td id="T_82262_row5_col8" class="data row5 col8" >10,000.00</td>
      <td id="T_82262_row5_col9" class="data row5 col9" >10,000.00</td>
      <td id="T_82262_row5_col10" class="data row5 col10" >35000.000000</td>
      <td id="T_82262_row5_col11" class="data row5 col11" >35000.000000</td>
      <td id="T_82262_row5_col12" class="data row5 col12" >1.0000%</td>
      <td id="T_82262_row5_col13" class="data row5 col13" >2,555.56</td>
      <td id="T_82262_row5_col14" class="data row5 col14" >1.0000%</td>
      <td id="T_82262_row5_col15" class="data row5 col15" >1.00</td>
      <td id="T_82262_row5_col16" class="data row5 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_82262_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_82262_row6_col0" class="data row6 col0" >1970-07-31</td>
      <td id="T_82262_row6_col1" class="data row6 col1" >1970-10-30</td>
      <td id="T_82262_row6_col2" class="data row6 col2" >1970-10-30</td>
      <td id="T_82262_row6_col3" class="data row6 col3" >1,000,000.00</td>
      <td id="T_82262_row6_col4" class="data row6 col4" >0.00</td>
      <td id="T_82262_row6_col5" class="data row6 col5" >True</td>
      <td id="T_82262_row6_col6" class="data row6 col6" >2,527.78</td>
      <td id="T_82262_row6_col7" class="data row6 col7" >CLF</td>
      <td id="T_82262_row6_col8" class="data row6 col8" >10,000.00</td>
      <td id="T_82262_row6_col9" class="data row6 col9" >10,000.00</td>
      <td id="T_82262_row6_col10" class="data row6 col10" >35000.000000</td>
      <td id="T_82262_row6_col11" class="data row6 col11" >35000.000000</td>
      <td id="T_82262_row6_col12" class="data row6 col12" >1.0000%</td>
      <td id="T_82262_row6_col13" class="data row6 col13" >2,527.78</td>
      <td id="T_82262_row6_col14" class="data row6 col14" >1.0000%</td>
      <td id="T_82262_row6_col15" class="data row6 col15" >1.00</td>
      <td id="T_82262_row6_col16" class="data row6 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_82262_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_82262_row7_col0" class="data row7 col0" >1970-10-30</td>
      <td id="T_82262_row7_col1" class="data row7 col1" >1971-01-29</td>
      <td id="T_82262_row7_col2" class="data row7 col2" >1971-01-29</td>
      <td id="T_82262_row7_col3" class="data row7 col3" >1,000,000.00</td>
      <td id="T_82262_row7_col4" class="data row7 col4" >0.00</td>
      <td id="T_82262_row7_col5" class="data row7 col5" >True</td>
      <td id="T_82262_row7_col6" class="data row7 col6" >2,527.78</td>
      <td id="T_82262_row7_col7" class="data row7 col7" >CLF</td>
      <td id="T_82262_row7_col8" class="data row7 col8" >10,000.00</td>
      <td id="T_82262_row7_col9" class="data row7 col9" >10,000.00</td>
      <td id="T_82262_row7_col10" class="data row7 col10" >35000.000000</td>
      <td id="T_82262_row7_col11" class="data row7 col11" >35000.000000</td>
      <td id="T_82262_row7_col12" class="data row7 col12" >1.0000%</td>
      <td id="T_82262_row7_col13" class="data row7 col13" >2,527.78</td>
      <td id="T_82262_row7_col14" class="data row7 col14" >1.0000%</td>
      <td id="T_82262_row7_col15" class="data row7 col15" >1.00</td>
      <td id="T_82262_row7_col16" class="data row7 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_82262_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_82262_row8_col0" class="data row8 col0" >1971-01-29</td>
      <td id="T_82262_row8_col1" class="data row8 col1" >1971-04-30</td>
      <td id="T_82262_row8_col2" class="data row8 col2" >1971-04-30</td>
      <td id="T_82262_row8_col3" class="data row8 col3" >1,000,000.00</td>
      <td id="T_82262_row8_col4" class="data row8 col4" >0.00</td>
      <td id="T_82262_row8_col5" class="data row8 col5" >True</td>
      <td id="T_82262_row8_col6" class="data row8 col6" >2,527.78</td>
      <td id="T_82262_row8_col7" class="data row8 col7" >CLF</td>
      <td id="T_82262_row8_col8" class="data row8 col8" >10,000.00</td>
      <td id="T_82262_row8_col9" class="data row8 col9" >10,000.00</td>
      <td id="T_82262_row8_col10" class="data row8 col10" >35000.000000</td>
      <td id="T_82262_row8_col11" class="data row8 col11" >35000.000000</td>
      <td id="T_82262_row8_col12" class="data row8 col12" >1.0000%</td>
      <td id="T_82262_row8_col13" class="data row8 col13" >2,527.78</td>
      <td id="T_82262_row8_col14" class="data row8 col14" >1.0000%</td>
      <td id="T_82262_row8_col15" class="data row8 col15" >1.00</td>
      <td id="T_82262_row8_col16" class="data row8 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_82262_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_82262_row9_col0" class="data row9 col0" >1971-04-30</td>
      <td id="T_82262_row9_col1" class="data row9 col1" >1971-07-30</td>
      <td id="T_82262_row9_col2" class="data row9 col2" >1971-07-30</td>
      <td id="T_82262_row9_col3" class="data row9 col3" >1,000,000.00</td>
      <td id="T_82262_row9_col4" class="data row9 col4" >0.00</td>
      <td id="T_82262_row9_col5" class="data row9 col5" >True</td>
      <td id="T_82262_row9_col6" class="data row9 col6" >2,527.78</td>
      <td id="T_82262_row9_col7" class="data row9 col7" >CLF</td>
      <td id="T_82262_row9_col8" class="data row9 col8" >10,000.00</td>
      <td id="T_82262_row9_col9" class="data row9 col9" >10,000.00</td>
      <td id="T_82262_row9_col10" class="data row9 col10" >35000.000000</td>
      <td id="T_82262_row9_col11" class="data row9 col11" >35000.000000</td>
      <td id="T_82262_row9_col12" class="data row9 col12" >1.0000%</td>
      <td id="T_82262_row9_col13" class="data row9 col13" >2,527.78</td>
      <td id="T_82262_row9_col14" class="data row9 col14" >1.0000%</td>
      <td id="T_82262_row9_col15" class="data row9 col15" >1.00</td>
      <td id="T_82262_row9_col16" class="data row9 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_82262_level0_row10" class="row_heading level0 row10" >10</th>
      <td id="T_82262_row10_col0" class="data row10 col0" >1971-07-30</td>
      <td id="T_82262_row10_col1" class="data row10 col1" >1971-10-29</td>
      <td id="T_82262_row10_col2" class="data row10 col2" >1971-10-29</td>
      <td id="T_82262_row10_col3" class="data row10 col3" >1,000,000.00</td>
      <td id="T_82262_row10_col4" class="data row10 col4" >0.00</td>
      <td id="T_82262_row10_col5" class="data row10 col5" >True</td>
      <td id="T_82262_row10_col6" class="data row10 col6" >2,527.78</td>
      <td id="T_82262_row10_col7" class="data row10 col7" >CLF</td>
      <td id="T_82262_row10_col8" class="data row10 col8" >10,000.00</td>
      <td id="T_82262_row10_col9" class="data row10 col9" >10,000.00</td>
      <td id="T_82262_row10_col10" class="data row10 col10" >35000.000000</td>
      <td id="T_82262_row10_col11" class="data row10 col11" >35000.000000</td>
      <td id="T_82262_row10_col12" class="data row10 col12" >1.0000%</td>
      <td id="T_82262_row10_col13" class="data row10 col13" >2,527.78</td>
      <td id="T_82262_row10_col14" class="data row10 col14" >1.0000%</td>
      <td id="T_82262_row10_col15" class="data row10 col15" >1.00</td>
      <td id="T_82262_row10_col16" class="data row10 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_82262_level0_row11" class="row_heading level0 row11" >11</th>
      <td id="T_82262_row11_col0" class="data row11 col0" >1971-10-29</td>
      <td id="T_82262_row11_col1" class="data row11 col1" >1972-01-31</td>
      <td id="T_82262_row11_col2" class="data row11 col2" >1972-01-31</td>
      <td id="T_82262_row11_col3" class="data row11 col3" >1,000,000.00</td>
      <td id="T_82262_row11_col4" class="data row11 col4" >0.00</td>
      <td id="T_82262_row11_col5" class="data row11 col5" >True</td>
      <td id="T_82262_row11_col6" class="data row11 col6" >2,611.11</td>
      <td id="T_82262_row11_col7" class="data row11 col7" >CLF</td>
      <td id="T_82262_row11_col8" class="data row11 col8" >10,000.00</td>
      <td id="T_82262_row11_col9" class="data row11 col9" >10,000.00</td>
      <td id="T_82262_row11_col10" class="data row11 col10" >35000.000000</td>
      <td id="T_82262_row11_col11" class="data row11 col11" >35000.000000</td>
      <td id="T_82262_row11_col12" class="data row11 col12" >1.0000%</td>
      <td id="T_82262_row11_col13" class="data row11 col13" >2,611.11</td>
      <td id="T_82262_row11_col14" class="data row11 col14" >1.0000%</td>
      <td id="T_82262_row11_col15" class="data row11 col15" >1.00</td>
      <td id="T_82262_row11_col16" class="data row11 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_82262_level0_row12" class="row_heading level0 row12" >12</th>
      <td id="T_82262_row12_col0" class="data row12 col0" >1972-01-31</td>
      <td id="T_82262_row12_col1" class="data row12 col1" >1972-04-28</td>
      <td id="T_82262_row12_col2" class="data row12 col2" >1972-04-28</td>
      <td id="T_82262_row12_col3" class="data row12 col3" >1,000,000.00</td>
      <td id="T_82262_row12_col4" class="data row12 col4" >0.00</td>
      <td id="T_82262_row12_col5" class="data row12 col5" >True</td>
      <td id="T_82262_row12_col6" class="data row12 col6" >2,444.44</td>
      <td id="T_82262_row12_col7" class="data row12 col7" >CLF</td>
      <td id="T_82262_row12_col8" class="data row12 col8" >10,000.00</td>
      <td id="T_82262_row12_col9" class="data row12 col9" >10,000.00</td>
      <td id="T_82262_row12_col10" class="data row12 col10" >35000.000000</td>
      <td id="T_82262_row12_col11" class="data row12 col11" >35000.000000</td>
      <td id="T_82262_row12_col12" class="data row12 col12" >1.0000%</td>
      <td id="T_82262_row12_col13" class="data row12 col13" >2,444.44</td>
      <td id="T_82262_row12_col14" class="data row12 col14" >1.0000%</td>
      <td id="T_82262_row12_col15" class="data row12 col15" >1.00</td>
      <td id="T_82262_row12_col16" class="data row12 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_82262_level0_row13" class="row_heading level0 row13" >13</th>
      <td id="T_82262_row13_col0" class="data row13 col0" >1972-04-28</td>
      <td id="T_82262_row13_col1" class="data row13 col1" >1972-07-31</td>
      <td id="T_82262_row13_col2" class="data row13 col2" >1972-07-31</td>
      <td id="T_82262_row13_col3" class="data row13 col3" >1,000,000.00</td>
      <td id="T_82262_row13_col4" class="data row13 col4" >0.00</td>
      <td id="T_82262_row13_col5" class="data row13 col5" >True</td>
      <td id="T_82262_row13_col6" class="data row13 col6" >2,611.11</td>
      <td id="T_82262_row13_col7" class="data row13 col7" >CLF</td>
      <td id="T_82262_row13_col8" class="data row13 col8" >10,000.00</td>
      <td id="T_82262_row13_col9" class="data row13 col9" >10,000.00</td>
      <td id="T_82262_row13_col10" class="data row13 col10" >35000.000000</td>
      <td id="T_82262_row13_col11" class="data row13 col11" >35000.000000</td>
      <td id="T_82262_row13_col12" class="data row13 col12" >1.0000%</td>
      <td id="T_82262_row13_col13" class="data row13 col13" >2,611.11</td>
      <td id="T_82262_row13_col14" class="data row13 col14" >1.0000%</td>
      <td id="T_82262_row13_col15" class="data row13 col15" >1.00</td>
      <td id="T_82262_row13_col16" class="data row13 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_82262_level0_row14" class="row_heading level0 row14" >14</th>
      <td id="T_82262_row14_col0" class="data row14 col0" >1972-07-31</td>
      <td id="T_82262_row14_col1" class="data row14 col1" >1972-10-31</td>
      <td id="T_82262_row14_col2" class="data row14 col2" >1972-10-31</td>
      <td id="T_82262_row14_col3" class="data row14 col3" >1,000,000.00</td>
      <td id="T_82262_row14_col4" class="data row14 col4" >0.00</td>
      <td id="T_82262_row14_col5" class="data row14 col5" >True</td>
      <td id="T_82262_row14_col6" class="data row14 col6" >2,555.56</td>
      <td id="T_82262_row14_col7" class="data row14 col7" >CLF</td>
      <td id="T_82262_row14_col8" class="data row14 col8" >10,000.00</td>
      <td id="T_82262_row14_col9" class="data row14 col9" >10,000.00</td>
      <td id="T_82262_row14_col10" class="data row14 col10" >35000.000000</td>
      <td id="T_82262_row14_col11" class="data row14 col11" >35000.000000</td>
      <td id="T_82262_row14_col12" class="data row14 col12" >1.0000%</td>
      <td id="T_82262_row14_col13" class="data row14 col13" >2,555.56</td>
      <td id="T_82262_row14_col14" class="data row14 col14" >1.0000%</td>
      <td id="T_82262_row14_col15" class="data row14 col15" >1.00</td>
      <td id="T_82262_row14_col16" class="data row14 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_82262_level0_row15" class="row_heading level0 row15" >15</th>
      <td id="T_82262_row15_col0" class="data row15 col0" >1972-10-31</td>
      <td id="T_82262_row15_col1" class="data row15 col1" >1973-01-31</td>
      <td id="T_82262_row15_col2" class="data row15 col2" >1973-01-31</td>
      <td id="T_82262_row15_col3" class="data row15 col3" >1,000,000.00</td>
      <td id="T_82262_row15_col4" class="data row15 col4" >0.00</td>
      <td id="T_82262_row15_col5" class="data row15 col5" >True</td>
      <td id="T_82262_row15_col6" class="data row15 col6" >2,555.56</td>
      <td id="T_82262_row15_col7" class="data row15 col7" >CLF</td>
      <td id="T_82262_row15_col8" class="data row15 col8" >10,000.00</td>
      <td id="T_82262_row15_col9" class="data row15 col9" >10,000.00</td>
      <td id="T_82262_row15_col10" class="data row15 col10" >35000.000000</td>
      <td id="T_82262_row15_col11" class="data row15 col11" >35000.000000</td>
      <td id="T_82262_row15_col12" class="data row15 col12" >1.0000%</td>
      <td id="T_82262_row15_col13" class="data row15 col13" >2,555.56</td>
      <td id="T_82262_row15_col14" class="data row15 col14" >1.0000%</td>
      <td id="T_82262_row15_col15" class="data row15 col15" >1.00</td>
      <td id="T_82262_row15_col16" class="data row15 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_82262_level0_row16" class="row_heading level0 row16" >16</th>
      <td id="T_82262_row16_col0" class="data row16 col0" >1973-01-31</td>
      <td id="T_82262_row16_col1" class="data row16 col1" >1973-04-30</td>
      <td id="T_82262_row16_col2" class="data row16 col2" >1973-04-30</td>
      <td id="T_82262_row16_col3" class="data row16 col3" >1,000,000.00</td>
      <td id="T_82262_row16_col4" class="data row16 col4" >0.00</td>
      <td id="T_82262_row16_col5" class="data row16 col5" >True</td>
      <td id="T_82262_row16_col6" class="data row16 col6" >2,472.22</td>
      <td id="T_82262_row16_col7" class="data row16 col7" >CLF</td>
      <td id="T_82262_row16_col8" class="data row16 col8" >10,000.00</td>
      <td id="T_82262_row16_col9" class="data row16 col9" >10,000.00</td>
      <td id="T_82262_row16_col10" class="data row16 col10" >35000.000000</td>
      <td id="T_82262_row16_col11" class="data row16 col11" >35000.000000</td>
      <td id="T_82262_row16_col12" class="data row16 col12" >1.0000%</td>
      <td id="T_82262_row16_col13" class="data row16 col13" >2,472.22</td>
      <td id="T_82262_row16_col14" class="data row16 col14" >1.0000%</td>
      <td id="T_82262_row16_col15" class="data row16 col15" >1.00</td>
      <td id="T_82262_row16_col16" class="data row16 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_82262_level0_row17" class="row_heading level0 row17" >17</th>
      <td id="T_82262_row17_col0" class="data row17 col0" >1973-04-30</td>
      <td id="T_82262_row17_col1" class="data row17 col1" >1973-07-31</td>
      <td id="T_82262_row17_col2" class="data row17 col2" >1973-07-31</td>
      <td id="T_82262_row17_col3" class="data row17 col3" >1,000,000.00</td>
      <td id="T_82262_row17_col4" class="data row17 col4" >0.00</td>
      <td id="T_82262_row17_col5" class="data row17 col5" >True</td>
      <td id="T_82262_row17_col6" class="data row17 col6" >2,555.56</td>
      <td id="T_82262_row17_col7" class="data row17 col7" >CLF</td>
      <td id="T_82262_row17_col8" class="data row17 col8" >10,000.00</td>
      <td id="T_82262_row17_col9" class="data row17 col9" >10,000.00</td>
      <td id="T_82262_row17_col10" class="data row17 col10" >35000.000000</td>
      <td id="T_82262_row17_col11" class="data row17 col11" >35000.000000</td>
      <td id="T_82262_row17_col12" class="data row17 col12" >1.0000%</td>
      <td id="T_82262_row17_col13" class="data row17 col13" >2,555.56</td>
      <td id="T_82262_row17_col14" class="data row17 col14" >1.0000%</td>
      <td id="T_82262_row17_col15" class="data row17 col15" >1.00</td>
      <td id="T_82262_row17_col16" class="data row17 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_82262_level0_row18" class="row_heading level0 row18" >18</th>
      <td id="T_82262_row18_col0" class="data row18 col0" >1973-07-31</td>
      <td id="T_82262_row18_col1" class="data row18 col1" >1973-10-31</td>
      <td id="T_82262_row18_col2" class="data row18 col2" >1973-10-31</td>
      <td id="T_82262_row18_col3" class="data row18 col3" >1,000,000.00</td>
      <td id="T_82262_row18_col4" class="data row18 col4" >0.00</td>
      <td id="T_82262_row18_col5" class="data row18 col5" >True</td>
      <td id="T_82262_row18_col6" class="data row18 col6" >2,555.56</td>
      <td id="T_82262_row18_col7" class="data row18 col7" >CLF</td>
      <td id="T_82262_row18_col8" class="data row18 col8" >10,000.00</td>
      <td id="T_82262_row18_col9" class="data row18 col9" >10,000.00</td>
      <td id="T_82262_row18_col10" class="data row18 col10" >35000.000000</td>
      <td id="T_82262_row18_col11" class="data row18 col11" >35000.000000</td>
      <td id="T_82262_row18_col12" class="data row18 col12" >1.0000%</td>
      <td id="T_82262_row18_col13" class="data row18 col13" >2,555.56</td>
      <td id="T_82262_row18_col14" class="data row18 col14" >1.0000%</td>
      <td id="T_82262_row18_col15" class="data row18 col15" >1.00</td>
      <td id="T_82262_row18_col16" class="data row18 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_82262_level0_row19" class="row_heading level0 row19" >19</th>
      <td id="T_82262_row19_col0" class="data row19 col0" >1973-10-31</td>
      <td id="T_82262_row19_col1" class="data row19 col1" >1974-01-31</td>
      <td id="T_82262_row19_col2" class="data row19 col2" >1974-01-31</td>
      <td id="T_82262_row19_col3" class="data row19 col3" >1,000,000.00</td>
      <td id="T_82262_row19_col4" class="data row19 col4" >1,000,000.00</td>
      <td id="T_82262_row19_col5" class="data row19 col5" >True</td>
      <td id="T_82262_row19_col6" class="data row19 col6" >1,002,555.56</td>
      <td id="T_82262_row19_col7" class="data row19 col7" >CLF</td>
      <td id="T_82262_row19_col8" class="data row19 col8" >10,000.00</td>
      <td id="T_82262_row19_col9" class="data row19 col9" >10,000.00</td>
      <td id="T_82262_row19_col10" class="data row19 col10" >35000.000000</td>
      <td id="T_82262_row19_col11" class="data row19 col11" >35000.000000</td>
      <td id="T_82262_row19_col12" class="data row19 col12" >1.0000%</td>
      <td id="T_82262_row19_col13" class="data row19 col13" >2,555.56</td>
      <td id="T_82262_row19_col14" class="data row19 col14" >1.0000%</td>
      <td id="T_82262_row19_col15" class="data row19 col15" >1.00</td>
      <td id="T_82262_row19_col16" class="data row19 col16" >LinAct360</td>
    </tr>
  </tbody>
</table>




### Construcción Asistida de un `CompoundedOvernightRateLeg`


```python
# Se da de alta los parámetros requeridos
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(3, 1, 2022)
fecha_final = qcf.QCDate(3, 1, 2023)
bus_adj_rule = qcf.BusyAdjRules.MODFOLLOW
periodicidad_pago = qcf.Tenor('3M')
periodo_irregular_pago = qcf.StubPeriod.NO
calendario = qcf.BusinessCalendar(fecha_inicio, 20)
lag_pago = 0

######################################################################
# Definición del índice

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
    usd)

# Fin índice
######################################################################

nominal = 1000000.0
amort_es_flujo = True
moneda = usd
spread = .01
gearing = 1.0

cor_leg = qcf.LegFactory.build_bullet_compounded_overnight_rate_leg(
    rp,
    fecha_inicio,
    fecha_final,
    bus_adj_rule,
    periodicidad_pago,
    periodo_irregular_pago,
    calendario,
    lag_pago,
    calendario,
    oistest,
    nominal,
    amort_es_flujo,
    usd,
    spread,
    gearing,
    True,
    8,
    0,
    0
)
```


```python
# Se define un list donde almacenar los resultados de la función show
tabla = []
for i in range(0, cor_leg.size()):
    tabla.append(qcf.show(cor_leg.get_cashflow_at(i)))

# Se utiliza tabla para inicializar el Dataframe
columnas = ['fecha_inicial', 'fecha__final', 'fecha__pago', 'nominal', 'amort', 'interes', 'amort_es_flujo', 'flujo',
            'moneda', 'indice', 'valor_tasa', 'spread', 'gearing', 'tipo_tasa']
df9 = pd.DataFrame(tabla, columns=columnas)

# Se despliega la data en este formato
df9.style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_725b9">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_725b9_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_725b9_level0_col1" class="col_heading level0 col1" >fecha__final</th>
      <th id="T_725b9_level0_col2" class="col_heading level0 col2" >fecha__pago</th>
      <th id="T_725b9_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_725b9_level0_col4" class="col_heading level0 col4" >amort</th>
      <th id="T_725b9_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_725b9_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_725b9_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_725b9_level0_col8" class="col_heading level0 col8" >moneda</th>
      <th id="T_725b9_level0_col9" class="col_heading level0 col9" >indice</th>
      <th id="T_725b9_level0_col10" class="col_heading level0 col10" >valor_tasa</th>
      <th id="T_725b9_level0_col11" class="col_heading level0 col11" >spread</th>
      <th id="T_725b9_level0_col12" class="col_heading level0 col12" >gearing</th>
      <th id="T_725b9_level0_col13" class="col_heading level0 col13" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_725b9_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_725b9_row0_col0" class="data row0 col0" >2022-01-03</td>
      <td id="T_725b9_row0_col1" class="data row0 col1" >2022-04-04</td>
      <td id="T_725b9_row0_col2" class="data row0 col2" >2022-04-04</td>
      <td id="T_725b9_row0_col3" class="data row0 col3" >1,000,000.00</td>
      <td id="T_725b9_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_725b9_row0_col5" class="data row0 col5" >2,527.78</td>
      <td id="T_725b9_row0_col6" class="data row0 col6" >True</td>
      <td id="T_725b9_row0_col7" class="data row0 col7" >2,527.78</td>
      <td id="T_725b9_row0_col8" class="data row0 col8" >USD</td>
      <td id="T_725b9_row0_col9" class="data row0 col9" >OISTEST</td>
      <td id="T_725b9_row0_col10" class="data row0 col10" >0.0000%</td>
      <td id="T_725b9_row0_col11" class="data row0 col11" >1.0000%</td>
      <td id="T_725b9_row0_col12" class="data row0 col12" >1.00</td>
      <td id="T_725b9_row0_col13" class="data row0 col13" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_725b9_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_725b9_row1_col0" class="data row1 col0" >2022-04-04</td>
      <td id="T_725b9_row1_col1" class="data row1 col1" >2022-07-04</td>
      <td id="T_725b9_row1_col2" class="data row1 col2" >2022-07-04</td>
      <td id="T_725b9_row1_col3" class="data row1 col3" >1,000,000.00</td>
      <td id="T_725b9_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_725b9_row1_col5" class="data row1 col5" >2,527.78</td>
      <td id="T_725b9_row1_col6" class="data row1 col6" >True</td>
      <td id="T_725b9_row1_col7" class="data row1 col7" >2,527.78</td>
      <td id="T_725b9_row1_col8" class="data row1 col8" >USD</td>
      <td id="T_725b9_row1_col9" class="data row1 col9" >OISTEST</td>
      <td id="T_725b9_row1_col10" class="data row1 col10" >0.0000%</td>
      <td id="T_725b9_row1_col11" class="data row1 col11" >1.0000%</td>
      <td id="T_725b9_row1_col12" class="data row1 col12" >1.00</td>
      <td id="T_725b9_row1_col13" class="data row1 col13" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_725b9_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_725b9_row2_col0" class="data row2 col0" >2022-07-04</td>
      <td id="T_725b9_row2_col1" class="data row2 col1" >2022-10-03</td>
      <td id="T_725b9_row2_col2" class="data row2 col2" >2022-10-03</td>
      <td id="T_725b9_row2_col3" class="data row2 col3" >1,000,000.00</td>
      <td id="T_725b9_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_725b9_row2_col5" class="data row2 col5" >2,527.78</td>
      <td id="T_725b9_row2_col6" class="data row2 col6" >True</td>
      <td id="T_725b9_row2_col7" class="data row2 col7" >2,527.78</td>
      <td id="T_725b9_row2_col8" class="data row2 col8" >USD</td>
      <td id="T_725b9_row2_col9" class="data row2 col9" >OISTEST</td>
      <td id="T_725b9_row2_col10" class="data row2 col10" >0.0000%</td>
      <td id="T_725b9_row2_col11" class="data row2 col11" >1.0000%</td>
      <td id="T_725b9_row2_col12" class="data row2 col12" >1.00</td>
      <td id="T_725b9_row2_col13" class="data row2 col13" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_725b9_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_725b9_row3_col0" class="data row3 col0" >2022-10-03</td>
      <td id="T_725b9_row3_col1" class="data row3 col1" >2023-01-03</td>
      <td id="T_725b9_row3_col2" class="data row3 col2" >2023-01-03</td>
      <td id="T_725b9_row3_col3" class="data row3 col3" >1,000,000.00</td>
      <td id="T_725b9_row3_col4" class="data row3 col4" >1,000,000.00</td>
      <td id="T_725b9_row3_col5" class="data row3 col5" >2,555.56</td>
      <td id="T_725b9_row3_col6" class="data row3 col6" >True</td>
      <td id="T_725b9_row3_col7" class="data row3 col7" >1,002,555.56</td>
      <td id="T_725b9_row3_col8" class="data row3 col8" >USD</td>
      <td id="T_725b9_row3_col9" class="data row3 col9" >OISTEST</td>
      <td id="T_725b9_row3_col10" class="data row3 col10" >0.0000%</td>
      <td id="T_725b9_row3_col11" class="data row3 col11" >1.0000%</td>
      <td id="T_725b9_row3_col12" class="data row3 col12" >1.00</td>
      <td id="T_725b9_row3_col13" class="data row3 col13" >LinAct360</td>
    </tr>
  </tbody>
</table>



