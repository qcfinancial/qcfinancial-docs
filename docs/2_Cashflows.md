# Cashflows

Para ejecutar todos los ejemplos se debe importar la librería. Se sugiere utilizar siempre el alias `qcf`. 


```python
import qcfinancial as qcf
import pandas as pd
```

Se verifica la versión y build de `qcfinancial`.


```python
qcf.id()
```




    'version: 0.10.0, build: 2024-06-08 08:15'



Permite formatear los `DataFrames` que serán utilizados.


```python
format_dict = {
    'nocional':'{:,.2f}', 
    'nominal':'{:,.2f}', 
    'amortizacion':'{:,.2f}', 
    'amortizacion_moneda_pago':'{:,.2f}', 
    'interes':'{:,.2f}',
    'interes_moneda_pago':'{:,.2f}',
    'flujo':'{:,.2f}',
    'flujo_en_clp':'{:,.0f}',
    'flujo_moneda_pago':'{:,.2f}',
    'valor_tasa':'{:.6%}',
    'valor_tasa_equivalente':'{:.6%}',
    'spread':'{:.2%}',
    'valor_indice_inicial':'{:,.2f}',
    'valor_indice_final':'{:,.2f}',
}
```

## Simple Cashflow
Un objeto de tipo `SimpleCashflow` representa un flujo de caja cierto en una fecha y moneda. Para instanciar un objeto de este tipo se requiere:

- `QCDate`: fecha del flujo
- `float`: monto del flujo
- `QCCurrency`: moneda del flujo

Se define los parámetros.


```python
fecha1 = qcf.QCDate(24, 5, 2024)
monto = 1_000_000
clp = qcf.QCCLP()
```

Se instancia el objeto.


```python
simple_cashflow = qcf.SimpleCashflow(
    fecha1, 
    monto, 
    clp,
)
```


```python
simple_cashflow
```




    <qcfinancial.SimpleCashflow at 0x10ea9cb30>



### Métodos `amount`, `ccy` y `date`


```python
print(f"Monto: {simple_cashflow.amount():,.0f}")
print(f"Moneda: {simple_cashflow.ccy().get_iso_code()}")
print(f"Fecha: {simple_cashflow.date()}")
```

    Monto: 1,000,000
    Moneda: CLP
    Fecha: 2024-05-24


### Función `show`

Esta función envuelve de forma cómoda todo el flujo en un objeto `tuple`. La función `show` está sobregargada y admite todos los tipos de flujo de `qcfinancial`.


```python
qcf.show(simple_cashflow)
```




    ('2024-05-24', 1000000.0, 'CLP')



### Función `get_columns_names`

Para nombrar los elementos de la tupla anterior, se puede utilizar la función `get_column_names`.


```python
qcf.get_column_names('SimpleCashflow')
```




    ('fecha_pago', 'monto', 'moneda')



Con ella podemos, por ejemplo, estructurar aún más el output de `show` utilizando un `pandas.DataFrame`.


```python
df = pd.DataFrame([qcf.show(simple_cashflow)])
df.columns = list(qcf.get_column_names('SimpleCashflow'))
df.style.format({'monto':'{:,.0f}'})
```




<style type="text/css">
</style>
<table id="T_5684d">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_5684d_level0_col0" class="col_heading level0 col0" >fecha_pago</th>
      <th id="T_5684d_level0_col1" class="col_heading level0 col1" >monto</th>
      <th id="T_5684d_level0_col2" class="col_heading level0 col2" >moneda</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_5684d_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_5684d_row0_col0" class="data row0 col0" >2024-05-24</td>
      <td id="T_5684d_row0_col1" class="data row0 col1" >1,000,000</td>
      <td id="T_5684d_row0_col2" class="data row0 col2" >CLP</td>
    </tr>
  </tbody>
</table>




## Simple Multicurrency Cashflow

Un objeto de tipo `SimpleMultiCurrencyCashflow` representa un flujo de caja cierto en una fecha y moneda, el cual, sin embargo, se liquidará en una segunda moneda utilizando el valor de un índice de tipo de cambio. Para dar de alta uno de estos objetos se requiere:

- `QCDate`: fecha final
- `float`: nominal
- `QCCurrency`: la moneda del nominal
- `QCDate`: la fecha de publicación del `FXRateIndex` que se usará en la conversión
- `QCCurrency`: la moneda final del flujo
- `FXRateIndex`: el índice de tipo de cambio a utilizar
- `float`: el valor del índice de tipo de cambio

### Ejemplo 1

Se da de alta los objetos que el constructor necesita.


```python
usd = qcf.QCUSD()
usdclp = qcf.FXRate(usd, clp)
_1d = qcf.Tenor('1D')
scl = qcf.BusinessCalendar(qcf.QCDate(1, 2, 2024), 10)
usdclp_obs = qcf.FXRateIndex(usdclp, "USDOBS", _1d, _1d, scl)
fx_rate_value = 900.0
```

Se da de alta el cashflow.


```python
simple_mccy_cashflow = qcf.SimpleMultiCurrencyCashflow(
    fecha1, 
    monto, 
    clp, 
    fecha1, 
    usd, 
    usdclp_obs, 
    fx_rate_value
)
```

Este objeto hereda de `SimpleCashflow` y por lo tanto, los métodos `amount`, `date` y `ccy` siguen disponibles.


```python
print(f"Monto: {simple_mccy_cashflow.amount():,.2f}")
print(f"Fecha: {simple_mccy_cashflow.date()}")
print(f"Moneda: {simple_mccy_cashflow.ccy().get_iso_code()}")
```

    Monto: 1,000,000.00
    Fecha: 2024-05-24
    Moneda: CLP


Para obtener el monto en la moneda de pago y la moneda de pago están los métodos `settlement_amount` y `settlement_ccy`.


```python
print(f"Monto de pago: {simple_mccy_cashflow.settlement_amount():,.0f}")
print(f"Moneda de pago: {simple_mccy_cashflow.settlement_ccy().get_iso_code()}")
```

    Monto de pago: 1,111
    Moneda de pago: USD


El valor del índice de tipo de cambio se puede alterar con el método `set_fx_rate_index_value`.


```python
simple_mccy_cashflow.set_fx_rate_index_value(800.00)
print(f"Flujo: {simple_mccy_cashflow.settlement_amount():,.2f} {simple_mccy_cashflow.settlement_ccy().get_iso_code()}")
```

    Flujo: 1,250.00 USD


### Ejemplo 2

Aquí, las monedas están invertidas respecto al caso anterior. El valor del índice se usa de la forma correcta.


```python
simple_mccy_cashflow = qcf.SimpleMultiCurrencyCashflow(
    fecha1, 
    1_000_000, 
    usd, fecha1, 
    clp, 
    usdclp_obs, 
    fx_rate_value,
)
```

Se repite los cálculos del ejemplo anterior.


```python
print(f"Fecha: {simple_mccy_cashflow.date()}")
print(f"Nominal: {simple_mccy_cashflow.nominal():,.2f}")
print(f"Moneda nominal: {simple_mccy_cashflow.ccy().get_iso_code()}")
print(f"Flujo: {simple_mccy_cashflow.settlement_amount():,.0f}")
print(f"Moneda flujo: {simple_mccy_cashflow.settlement_ccy().get_iso_code()}")
```

    Fecha: 2024-05-24
    Nominal: 1,000,000.00
    Moneda nominal: USD
    Flujo: 900,000,000
    Moneda flujo: CLP


### Ejemplo 3

En este caso, hay inconsistencia entre las monedas y el tipo de cambio del índice y vemos que se produce un error.


```python
eur = qcf.QCEUR()
try:
    simple_mccy_cashflow = qcf.SimpleMultiCurrencyCashflow(
        fecha1,
        1_000_000,
        usd, 
        fecha1,
        eur,
        usdclp_obs,
        fx_rate_value,
    )
except ValueError as e:
    print("Error:", e)
```

    Error: Fx Rate Index provided is not compatible with nominal and settlement currency. 


### Funciones `show` y `get_columns`


```python
qcf.show(simple_mccy_cashflow)
```




    ('2024-05-24',
     1000000.0,
     'USD',
     '2024-05-24',
     'CLP',
     'USDOBS',
     900.0,
     1000000.0)




```python
qcf.get_column_names('SimpleMultiCurrencyCashflow')
```




    ('fecha_pago',
     'monto_nominal',
     'moneda_nominal',
     'fecha_fixing',
     'moneda_pago',
     'codigo_indice_fx',
     'valor_indice_fx',
     'monto_moneda_pago')



Con ella podemos, por ejemplo, estructurar aún más el output de `show` utilizando un `pandas.DataFrame`.


```python
df = pd.DataFrame([qcf.show(simple_mccy_cashflow)])
df.columns = list(qcf.get_column_names('SimpleMultiCurrencyCashflow'))
df.style.format({
    'monto_nominal':'{:,.0f}',
    'monto_moneda_pago':'{:,.0f}',
    'valor_indice_fx':'{:,.2f}'
})
```




<style type="text/css">
</style>
<table id="T_e4eb0">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_e4eb0_level0_col0" class="col_heading level0 col0" >fecha_pago</th>
      <th id="T_e4eb0_level0_col1" class="col_heading level0 col1" >monto_nominal</th>
      <th id="T_e4eb0_level0_col2" class="col_heading level0 col2" >moneda_nominal</th>
      <th id="T_e4eb0_level0_col3" class="col_heading level0 col3" >fecha_fixing</th>
      <th id="T_e4eb0_level0_col4" class="col_heading level0 col4" >moneda_pago</th>
      <th id="T_e4eb0_level0_col5" class="col_heading level0 col5" >codigo_indice_fx</th>
      <th id="T_e4eb0_level0_col6" class="col_heading level0 col6" >valor_indice_fx</th>
      <th id="T_e4eb0_level0_col7" class="col_heading level0 col7" >monto_moneda_pago</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_e4eb0_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_e4eb0_row0_col0" class="data row0 col0" >2024-05-24</td>
      <td id="T_e4eb0_row0_col1" class="data row0 col1" >1,000,000</td>
      <td id="T_e4eb0_row0_col2" class="data row0 col2" >USD</td>
      <td id="T_e4eb0_row0_col3" class="data row0 col3" >2024-05-24</td>
      <td id="T_e4eb0_row0_col4" class="data row0 col4" >CLP</td>
      <td id="T_e4eb0_row0_col5" class="data row0 col5" >USDOBS</td>
      <td id="T_e4eb0_row0_col6" class="data row0 col6" >900.00</td>
      <td id="T_e4eb0_row0_col7" class="data row0 col7" >1,000,000</td>
    </tr>
  </tbody>
</table>




## Fixed Rate Cashflow

Un objeto de tipo `FixedRateCashflow` representa un flujo de caja calculado a partir de la aplicación de una tasa prefijada, entre dos fechas prefijadas a un nominal prefijado. Para dar de alta uno de estos objetos se requiere:

- `QCDate`: fecha inicio (para la aplicación de la tasa)
- `QCDate`: fecha final (para la aplicación de la tasa)
- `QCDate`: fecha de pago
- `float`: nominal (monto al que se le aplica la tasa)
- `float`: amortización (eventual flujo de caja que corresponde a una porción del nominal)
- `bool`: indica si la amortización anterior es un flujo de caja o sólo una disminución de nominal
- `QCInterestRate`: la tasa de interés a aplicar (su valor y convenciones)
- `QCCurrency`: moneda del nominal y del flujo de caja

### Construcción

Se define los parámetros requeridos.


```python
fecha_inicio = qcf.QCDate(20, 5, 2024)
fecha_final = qcf.QCDate(20, 5, 2025)
fecha_pago = qcf.QCDate(22, 5, 2025)
valor_tasa_fija = .1
nominal = 1_000_000_000.0
amortizacion = 100_000_000.0
act360 = qcf.QCAct360()
lin_wf = qcf.QCLinearWf()
tasa = qcf.QCInterestRate(valor_tasa_fija, act360, lin_wf)
amort_is_cashflow = True
```

Se instancia el cashflow.


```python
fixed_rate_cashflow = qcf.FixedRateCashflow(
    fecha_inicio, 
    fecha_final, 
    fecha_pago, 
    nominal, 
    amortizacion, 
    amort_is_cashflow, 
    tasa, 
    clp,
)
```

### Getters


```python
print(f"Tipo de flujo: {fixed_rate_cashflow.get_type()}")
print(f"Fecha Inicio: {fixed_rate_cashflow.get_start_date()}")
print(f"Fecha Final: {fixed_rate_cashflow.get_end_date()}")
print(f"Fecha Pago: {fixed_rate_cashflow.get_settlement_date()}")
print(f"Moneda: {fixed_rate_cashflow.ccy().get_iso_code()}")
print(f"Nominal: {fixed_rate_cashflow.get_nominal():,.0f}")
print(f"Amortización: {fixed_rate_cashflow.get_amortization():,.0f}")

# Aquí además se usa un getter de QCInterestRate
print(f"Tasa de interés: {fixed_rate_cashflow.get_rate().get_value():.2%}")
```

    Tipo de flujo: FixedRateCashflow
    Fecha Inicio: 2024-05-20
    Fecha Final: 2025-05-20
    Fecha Pago: 2025-05-22
    Moneda: CLP
    Nominal: 1,000,000,000
    Amortización: 100,000,000
    Tasa de interés: 10.00%


### Setters

Cambiar el nominal.


```python
nuevo_nominal = 2_000_000_000.0
fixed_rate_cashflow.set_nominal(nuevo_nominal)
print(f"Nuevo nominal: {fixed_rate_cashflow.get_nominal():,.0f}")
```

    Nuevo nominal: 2,000,000,000


Cambiar la amortización.


```python
nueva_amortizacion = 200_000_000.0
fixed_rate_cashflow.set_amortization(nueva_amortizacion)
print(f"Nueva amortización: {fixed_rate_cashflow.get_amortization():,.0f}")
```

    Nueva amortización: 200,000,000


Cambiar el valor de la tasa.


```python
fixed_rate_cashflow.set_rate_value(new_rate_value:=.12)
print(f"Nuevo valor de la tasa: {fixed_rate_cashflow.get_rate().get_value():.2%}")
```

    Nuevo valor de la tasa: 12.00%


### Cálculos

Se devuelve el valor de la tasa fija al original.


```python
fixed_rate_cashflow.set_rate_value(valor_tasa_fija)
```

Método `amount`.


```python
print(f"Flujo Total: {fixed_rate_cashflow.amount():,.0f}")
```

    Flujo Total: 402,777,778


Vemos que el flujo incluye los intereses y la amortización (`amort_is_cashflow = True`). Podemos verificar a mano este resultado.


```python
dias_devengo = fecha_inicio.day_diff(fecha_final)
print(f"Días de devengo: {dias_devengo}")
print(f"Check: {fixed_rate_cashflow.get_nominal() * valor_tasa_fija * dias_devengo / 360 + fixed_rate_cashflow.get_amortization():,.0f}")
```

    Días de devengo: 365
    Check: 402,777,778


Método `accrued_interest`. Calcula el interés devengado a una cierta fecha.


```python
fecha_intermedia = qcf.QCDate(15, 1, 2025)
print(f"Interés Devengado: {fixed_rate_cashflow.accrued_interest(fecha_intermedia):,.0f}")
dias_devengo = fecha_inicio.day_diff(fecha_intermedia)
print(f"Días de devengo: {dias_devengo}")
print(f"Check: {fixed_rate_cashflow.get_nominal() * valor_tasa_fija * dias_devengo / 360.0:,.0f}")
```

    Interés Devengado: 133,333,333
    Días de devengo: 240
    Check: 133,333,333


### Función `show`


```python
print(qcf.show(fixed_rate_cashflow))
```

    ('2024-05-20', '2025-05-20', '2025-05-22', 2000000000.0, 200000000.0, 202777777.77777794, True, 402777777.7777779, 'CLP', 0.1, 'LinAct360')



```python
print(f"Interés total: al {fixed_rate_cashflow.accrued_interest(fixed_rate_cashflow.get_end_date()):,.0f}")
```

    Interés total: al 202,777,778


### Función `get_column_names`


```python
qcf.get_column_names(fixed_rate_cashflow.get_type())
```




    ('fecha_inicial',
     'fecha_final',
     'fecha_pago',
     'nominal',
     'amortizacion',
     'interes',
     'amort_es_flujo',
     'flujo',
     'moneda',
     'valor_tasa',
     'tipo_tasa')



Juntando las últimas dos funciones se obtiene una representación tabular del flujo usando `pandas.DataFrame`.


```python
df = pd.DataFrame([qcf.show(fixed_rate_cashflow)], columns=qcf.get_column_names(fixed_rate_cashflow.get_type()))
df.style.format({
    'nominal':'{:,.0f}', 
    'amortizacion':'{:,.0f}', 
    'interes':'{:,.0f}', 
    'flujo':'{:,.0f}',
    'valor_tasa':'{:.2%}'
})
```




<style type="text/css">
</style>
<table id="T_af3ad">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_af3ad_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_af3ad_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_af3ad_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_af3ad_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_af3ad_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_af3ad_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_af3ad_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_af3ad_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_af3ad_level0_col8" class="col_heading level0 col8" >moneda</th>
      <th id="T_af3ad_level0_col9" class="col_heading level0 col9" >valor_tasa</th>
      <th id="T_af3ad_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_af3ad_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_af3ad_row0_col0" class="data row0 col0" >2024-05-20</td>
      <td id="T_af3ad_row0_col1" class="data row0 col1" >2025-05-20</td>
      <td id="T_af3ad_row0_col2" class="data row0 col2" >2025-05-22</td>
      <td id="T_af3ad_row0_col3" class="data row0 col3" >2,000,000,000</td>
      <td id="T_af3ad_row0_col4" class="data row0 col4" >200,000,000</td>
      <td id="T_af3ad_row0_col5" class="data row0 col5" >202,777,778</td>
      <td id="T_af3ad_row0_col6" class="data row0 col6" >True</td>
      <td id="T_af3ad_row0_col7" class="data row0 col7" >402,777,778</td>
      <td id="T_af3ad_row0_col8" class="data row0 col8" >CLP</td>
      <td id="T_af3ad_row0_col9" class="data row0 col9" >10.00%</td>
      <td id="T_af3ad_row0_col10" class="data row0 col10" >LinAct360</td>
    </tr>
  </tbody>
</table>




## Fixed Rate Multi Currency Cashflow

Un objeto de tipo `FixedRateMultiCurrencyCashflow` representa un flujo de caja a tasa fija (`FixedRateCashflow`) que se liquidará en una moneda distinta de la moneda del nominal utilizando el valor a una cierta fecha de un índice de tipo de cambio prefijado. Para dar de alta uno de estos objetos se requiere:

- `QCDate`: fecha inicio (para la aplicación de la tasa)
- `QCDate`: fecha final (para la aplicación de la tasa)
- `QCDate`: fecha de pago
- `float`: nominal (monto al que se le aplica la tasa)
- `float`: amortización (eventual flujo de caja que corresponde a una porción del nominal)
- `bool`: indica si la amortización anterior es un flujo de caja o sólo una disminución de nominal
- `QCInterestRate`: la tasa de interés a aplicar (su valor y convenciones)
- `QCCurrency`: moneda del nominal
- `QCDate`: fecha de fijación del índice de tipo de cambio
- `QCCurrency`: moneda en la que se liquida el flujo
- `FXRateIndex`: índice de tipo de cambio a utilizar
- `float`: valor del índice de tipo de cambio

### Construcción

Cuando coinciden, se usan los mismos parámetros que en el ejemplo anterior.


```python
fecha_fijacion = fecha_final
usd = qcf.QCUSD()
indice = usdclp_obs
valor_indice = 900.0
nominal = 1_000_000.0
amort = 100_000.0
amort_is_cashflow = False
```

Se instancia el objeto.


```python
fixed_rate_mccy_cashflow = qcf.FixedRateMultiCurrencyCashflow(
    fecha_inicio,
    fecha_final,
    fecha_pago,
    nominal,
    amort,
    False,
    tasa,
    usd,
    fecha_fijacion,
    clp,
    indice,
    valor_indice,
)
```

### Getters

La clase `FixedRateMultiCurrencyCashflow` es una subclase de `FixedRateCashflow` y por lo tanto, hereda todos sus métodos y variables.


```python
print(f"Fecha Inicio: {fixed_rate_mccy_cashflow.get_start_date()}")
print(f"Fecha Final: {fixed_rate_mccy_cashflow.get_end_date()}")
print(f"Fecha Pago: {fixed_rate_mccy_cashflow.get_settlement_date()}")
print(f"Fecha Fijación Índice FX: {fixed_rate_mccy_cashflow.get_fx_fixing_date()}")
print(f"Moneda del Nominal: {fixed_rate_mccy_cashflow.ccy()}")
print(f"Nominal: {fixed_rate_mccy_cashflow.get_nominal():,.0f}")
print(f"Amortización: {fixed_rate_mccy_cashflow.get_amortization():,.0f}")
print(f"Moneda de Liquidación: {fixed_rate_mccy_cashflow.settlement_currency()}")

# Aquí se usa un getter de QCInterestRate
print(f"Tasa de interés: {fixed_rate_mccy_cashflow.get_rate().get_value():.2%}")
```

    Fecha Inicio: 2024-05-20
    Fecha Final: 2025-05-20
    Fecha Pago: 2025-05-22
    Fecha Fijación Índice FX: 2025-05-20
    Moneda del Nominal: USD
    Nominal: 1,000,000
    Amortización: 100,000
    Moneda de Liquidación: CLP
    Tasa de interés: 10.00%


### Setters

Nuevo nominal.


```python
nuevo_nominal = 100.0
fixed_rate_mccy_cashflow.set_nominal(nuevo_nominal)
print(f"Nuevo nominal: {fixed_rate_mccy_cashflow.get_nominal():,.1f}")
```

    Nuevo nominal: 100.0


Nueva amortización.


```python
nueva_amortizacion = 10.0
fixed_rate_mccy_cashflow.set_amortization(nueva_amortizacion)
print(f"Nueva amortización: {fixed_rate_mccy_cashflow.get_amortization():,.1f}")
```

    Nueva amortización: 10.0


Cambiar el valor de la tasa.


```python
fixed_rate_mccy_cashflow.set_rate_value(new_rate_value)
print(f"Nuevo valor de la tasa: {fixed_rate_mccy_cashflow.get_rate().get_value():.2%}")
```

    Nuevo valor de la tasa: 12.00%


### Cálculos

Se vuelve al nominal, amortización y valor de la tasa iniciales.


```python
fixed_rate_mccy_cashflow.set_nominal(nominal)
fixed_rate_mccy_cashflow.set_amortization(amort)
fixed_rate_mccy_cashflow.set_rate_value(valor_tasa_fija)
```

Método `amount`. En este caso no se incluye la amortización (`amort_is_cashflow = False`).


```python
print(f"Flujo Total: {fixed_rate_mccy_cashflow.amount():,.2f}")
dias_devengo = fecha_inicio.day_diff(fecha_final)
print(f"Check: {fixed_rate_mccy_cashflow.get_nominal() * valor_tasa_fija * dias_devengo / 360:,.2f}")
```

    Flujo Total: 101,388.89
    Check: 101,388.89


Método `accrued_interest`.


```python
fecha_intermedia = qcf.QCDate(15, 1, 2025)
print(f"Interés Devengado: {(interes_devengado:=fixed_rate_mccy_cashflow.accrued_interest(fecha_intermedia)):,.02f}")
print(f"Check: {fixed_rate_mccy_cashflow.get_nominal() * valor_tasa_fija * fecha_inicio.day_diff(fecha_intermedia) / 360.0:,.02f}")
```

    Interés Devengado: 66,666.67
    Check: 66,666.67


Método `accrued_interest_in_sett_currency`. Retorna el interés devengado en moneda de pago. Para esto requiere de un objeto de tipo `time_series` que contenga el valor del índice a la fecha de devengo solicitada.


```python
ts = qcf.time_series()
ts[fecha_inicio] = 900
ts[fecha_intermedia] = 950
```


```python
print(f"Interés devengado en moneda de pago: {fixed_rate_mccy_cashflow.accrued_interest_in_sett_ccy(fecha_intermedia, ts):,.2f}")
print(f"Check: {interes_devengado * ts[fecha_intermedia]:,.2f}")
```

    Interés devengado en moneda de pago: 63,333,333.33
    Check: 63,333,333.33


### Funciones `show` y `get_column_names`


```python
from IPython.display import display, HTML
display(HTML("<style>.jp-OutputArea-output {display:flex}</style>"))
```


<style>.jp-OutputArea-output {display:flex}</style>


Juntando estas dos funciones se obtiene una representación tabular del flujo usando `pandas.DataFrame`.


```python
df = pd.DataFrame([qcf.show(fixed_rate_mccy_cashflow)], columns=qcf.get_column_names(fixed_rate_mccy_cashflow.get_type()))
df.style.format({
    'nominal':'{:,.2f}', 
    'amortizacion':'{:,.2f}', 
    'amortizacion_moneda_pago':'{:,.0f}', 
    'interes':'{:,.2f}', 
    'interes_moneda_pago':'{:,.0f}', 
    'flujo':'{:,.0f}',
    'valor_tasa':'{:.2%}',
    'valor_indice_fx':'{:.2f}'
})
```




<style type="text/css">
</style>
<table id="T_ce9e1">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_ce9e1_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_ce9e1_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_ce9e1_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_ce9e1_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_ce9e1_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_ce9e1_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_ce9e1_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_ce9e1_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_ce9e1_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_ce9e1_level0_col9" class="col_heading level0 col9" >valor_tasa</th>
      <th id="T_ce9e1_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
      <th id="T_ce9e1_level0_col11" class="col_heading level0 col11" >fecha_fixing_fx</th>
      <th id="T_ce9e1_level0_col12" class="col_heading level0 col12" >moneda_pago</th>
      <th id="T_ce9e1_level0_col13" class="col_heading level0 col13" >indice_fx</th>
      <th id="T_ce9e1_level0_col14" class="col_heading level0 col14" >valor_indice_fx</th>
      <th id="T_ce9e1_level0_col15" class="col_heading level0 col15" >amortizacion_moneda_pago</th>
      <th id="T_ce9e1_level0_col16" class="col_heading level0 col16" >interes_moneda_pago</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_ce9e1_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_ce9e1_row0_col0" class="data row0 col0" >2024-05-20</td>
      <td id="T_ce9e1_row0_col1" class="data row0 col1" >2025-05-20</td>
      <td id="T_ce9e1_row0_col2" class="data row0 col2" >2025-05-22</td>
      <td id="T_ce9e1_row0_col3" class="data row0 col3" >1,000,000.00</td>
      <td id="T_ce9e1_row0_col4" class="data row0 col4" >100,000.00</td>
      <td id="T_ce9e1_row0_col5" class="data row0 col5" >101,388.89</td>
      <td id="T_ce9e1_row0_col6" class="data row0 col6" >False</td>
      <td id="T_ce9e1_row0_col7" class="data row0 col7" >101,389</td>
      <td id="T_ce9e1_row0_col8" class="data row0 col8" >USD</td>
      <td id="T_ce9e1_row0_col9" class="data row0 col9" >10.00%</td>
      <td id="T_ce9e1_row0_col10" class="data row0 col10" >LinAct360</td>
      <td id="T_ce9e1_row0_col11" class="data row0 col11" >2025-05-20</td>
      <td id="T_ce9e1_row0_col12" class="data row0 col12" >CLP</td>
      <td id="T_ce9e1_row0_col13" class="data row0 col13" >USDOBS</td>
      <td id="T_ce9e1_row0_col14" class="data row0 col14" >900.00</td>
      <td id="T_ce9e1_row0_col15" class="data row0 col15" >90,000,000</td>
      <td id="T_ce9e1_row0_col16" class="data row0 col16" >91,250,000</td>
    </tr>
  </tbody>
</table>




## Ibor Cashflow

Un objeto de tipo `IborCashflow` representa un flujo de caja calculado a partir de la aplicación de una tasa flotante fijada en una cierta fecha (Libor, Euribor, TAB, ...) , entre dos fechas prefijadas a un nominal prefijado. Para dar de alta uno de estos objetos se requiere:

- `InterestRateIndex`: el índice de tasa de interés prefijado
- `QCDate`: fecha inicio (para la aplicación de la tasa)
- `QCDate`: fecha final (para la aplicación de la tasa)
- `QCDate`: fecha de fijación del índice de tasa de interés 
- `QCDate`: fecha de pago
- `float`: nominal (monto al que se le aplica la tasa)
- `float`: amortización (eventual flujo de caja que corresponde a una porción del nominal)
- `bool`: indica si la amortización anterior es un flujo de caja o sólo una disminución de nominal
- `QCCurrency`: moneda del nominal y del flujo de caja
- `float`: spread aditivo a aplicar a la fijación del índice
- `float`: spread multiplicativo o gearing a aplicar a la fijación del índice

Para dar de alta un `InterestRateIndex` se requiere:

- `str`: código del índice
- `QCInterestRate`: un objeto tasa de interés que contenga las convenciones del índice
- `Tenor`: el lag de inicio del índice respecto a la fecha de fixing (por ejemplo 2d para Libor USD)
- `Tenor`: el tenor del índice (3M por ejemplo para Libor USD 3M)
- `QCBusinessCalendar`: el calendario de fixing
- `QCBusinessCalendar`: el calendario de pago
- `QCCurrency`: la moneda a la que corresponde el índice (por ejemplo EUR para EURIBOR 3M)


### Construcción

Se define primero el índice de tasa de interés.


```python
codigo = "TERMSOFR6M"
lin_act360 = qcf.QCInterestRate(0.0, act360, lin_wf)
fixing_lag = qcf.Tenor("2D")
tenor = qcf.Tenor("6M")
fixing_calendar = scl  # No es el calendario correcto, pero sirve para el ejemplo
settlement_calendar = scl  # Ídem arriba
term_sofr_6m = qcf.InterestRateIndex(
    codigo, 
    lin_act360, 
    fixing_lag, 
    tenor, 
    fixing_calendar, 
    settlement_calendar, 
    usd
)
```

Getters del objeto `InterestRateIndex`.


```python
print(f"Code: {term_sofr_6m.get_code()}")
print(f"Tenor: {term_sofr_6m.get_tenor()}")
print(f"Tasa: {term_sofr_6m.get_rate()}")
```

    Code: TERMSOFR6M
    Tenor: 6M
    Tasa: 0.000000 Act360 Lin


Para fijar el valor del índice en una fecha en particular.


```python
term_sofr_6m.set_rate_value(0.01)
print(f"Fixing Tasa: {term_sofr_6m.get_rate().get_value():.2%}")
fecha_fixing = qcf.QCDate(20, 9, 2018)
print(f"Fecha Inicio: {term_sofr_6m.get_start_date(fecha_fixing)}")
print(f"Fecha Final: {term_sofr_6m.get_end_date(fecha_fixing)}")
```

    Fixing Tasa: 1.00%
    Fecha Inicio: 2018-09-24
    Fecha Final: 2019-03-25


Con esto, veamos un ejemplo de construcción y uso de un `IborCashflow`.


```python
fecha_inicio = qcf.QCDate(20, 9, 2018)
fecha_final = qcf.QCDate(20, 9, 2019)
fecha_pago = qcf.QCDate(23, 9, 2019)
fecha_fixing = qcf.QCDate(20, 9, 2018)
nominal = 1_000_000.0
amort = 100_000.0
spread = 0.0
gearing = 1.0

ibor_cashflow = qcf.IborCashflow(
    term_sofr_6m,
    fecha_inicio,
    fecha_final,
    fecha_fixing,
    fecha_pago,
    nominal,
    amort,
    True,
    usd,
    spread,
    gearing,
)
```

### Getters


```python
print(f"Fecha Fixing:\t{ibor_cashflow.get_fixing_date()}")
print(f"Fecha Inicio:\t{ibor_cashflow.get_start_date()}")
print(f"Fecha Final:\t{ibor_cashflow.get_end_date()}")
print(f"Fecha Pago:\t{ibor_cashflow.get_settlement_date()}")
print(f"Nominal:\t{ibor_cashflow.get_nominal():,.0f}")
print(f"Amortización:\t{ibor_cashflow.get_amortization():,.0f}")
print(f"Moneda:\t\t{ibor_cashflow.ccy()}")
print(f"Valor Tasa:\t{ibor_cashflow.get_interest_rate_value():.2%}")
print(f"Valor Spread:\t{ibor_cashflow.get_spread():.2%}")
```

    Fecha Fixing:	2018-09-20
    Fecha Inicio:	2018-09-20
    Fecha Final:	2019-09-20
    Fecha Pago:	2019-09-23
    Nominal:	1,000,000
    Amortización:	100,000
    Moneda:		USD
    Valor Tasa:	1.00%
    Valor Spread:	0.00%


### Setters

Nuevo nominal.


```python
nuevo_nominal = 2_000_000.0
ibor_cashflow.set_nominal(nuevo_nominal)
print(f"Nominal: {ibor_cashflow.get_nominal():,.0f}")
```

    Nominal: 2,000,000


Nueva amortización.


```python
nueva_amortizacion = 200_000.0
ibor_cashflow.set_amortization(nueva_amortizacion)
print(f"Amortización: {ibor_cashflow.get_amortization():,.0f}")
```

    Amortización: 200,000


Cambia el valor del índice.


```python
ibor_cashflow.set_interest_rate_value(nuevo_valor_indice:=.02)
print(f"Valor Tasa: {ibor_cashflow.get_interest_rate_value():.2%}")
```

    Valor Tasa: 2.00%


Cambia el valor del sepread.


```python
ibor_cashflow.set_spread(.01)
print(f"Valor Spread: {ibor_cashflow.get_spread():.2%}")
```

    Valor Spread: 1.00%


### Cálculos

Método `amount`. Retorna el flujo total incluyendo la amortización si corresponde.


```python
print(f"Flujo: {ibor_cashflow.amount():,.2f}")
```

    Flujo: 240,555.56


Método `accrued_interest`. Retorna el interés devengado a una cierta fecha.


```python
fecha_devengo = qcf.QCDate(20, 7, 2019)
print(f"Interés Devengado al {fecha_devengo}: {ibor_cashflow.accrued_interest(fecha_devengo):,.2f}")

# La tasa es el valor del índice más el spread
tasa = ibor_cashflow.get_interest_rate_value() + ibor_cashflow.get_spread()

check = tasa * fecha_inicio.day_diff(fecha_devengo) / 360.0 * ibor_cashflow.get_nominal()
print(f"Check: {check:,.2f}")
```

    Interés Devengado al 2019-07-20: 50,500.00
    Check: 50,500.00


### Funciones `show` y `get_column_names`

Al igual que en casos anteriores, juntando estas dos funciones se obtiene una representación tabular del flujo usando `pandas.DataFrame`.


```python
df = pd.DataFrame([qcf.show(ibor_cashflow)], columns=qcf.get_column_names(ibor_cashflow.get_type()))
df.style.format({
    'nominal':'{:,.2f}', 
    'amortizacion':'{:,.2f}', 
    'interes':'{:,.2f}', 
    'flujo':'{:,.2f}',
    'valor_tasa':'{:.2%}',
    'spread':'{:.2%}',
})
```




<style type="text/css">
</style>
<table id="T_625d7">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_625d7_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_625d7_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_625d7_level0_col2" class="col_heading level0 col2" >fecha_fixing</th>
      <th id="T_625d7_level0_col3" class="col_heading level0 col3" >fecha_pago</th>
      <th id="T_625d7_level0_col4" class="col_heading level0 col4" >nominal</th>
      <th id="T_625d7_level0_col5" class="col_heading level0 col5" >amortizacion</th>
      <th id="T_625d7_level0_col6" class="col_heading level0 col6" >interes</th>
      <th id="T_625d7_level0_col7" class="col_heading level0 col7" >amort_es_flujo</th>
      <th id="T_625d7_level0_col8" class="col_heading level0 col8" >flujo</th>
      <th id="T_625d7_level0_col9" class="col_heading level0 col9" >moneda</th>
      <th id="T_625d7_level0_col10" class="col_heading level0 col10" >codigo_indice_tasa</th>
      <th id="T_625d7_level0_col11" class="col_heading level0 col11" >valor_tasa</th>
      <th id="T_625d7_level0_col12" class="col_heading level0 col12" >spread</th>
      <th id="T_625d7_level0_col13" class="col_heading level0 col13" >gearing</th>
      <th id="T_625d7_level0_col14" class="col_heading level0 col14" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_625d7_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_625d7_row0_col0" class="data row0 col0" >2018-09-20</td>
      <td id="T_625d7_row0_col1" class="data row0 col1" >2019-09-20</td>
      <td id="T_625d7_row0_col2" class="data row0 col2" >2018-09-20</td>
      <td id="T_625d7_row0_col3" class="data row0 col3" >2019-09-23</td>
      <td id="T_625d7_row0_col4" class="data row0 col4" >2,000,000.00</td>
      <td id="T_625d7_row0_col5" class="data row0 col5" >200,000.00</td>
      <td id="T_625d7_row0_col6" class="data row0 col6" >40,555.56</td>
      <td id="T_625d7_row0_col7" class="data row0 col7" >True</td>
      <td id="T_625d7_row0_col8" class="data row0 col8" >240,555.56</td>
      <td id="T_625d7_row0_col9" class="data row0 col9" >USD</td>
      <td id="T_625d7_row0_col10" class="data row0 col10" >TERMSOFR6M</td>
      <td id="T_625d7_row0_col11" class="data row0 col11" >2.00%</td>
      <td id="T_625d7_row0_col12" class="data row0 col12" >1.00%</td>
      <td id="T_625d7_row0_col13" class="data row0 col13" >1.000000</td>
      <td id="T_625d7_row0_col14" class="data row0 col14" >LinAct360</td>
    </tr>
  </tbody>
</table>




## Ibor Multi Currency Cashflow

Un objeto de tipo `IborMultiCurrencyCashflow` representa un flujo de caja a tasa variable (`IborCashflow`) que se liquidará en una moneda distinta de la moneda del nominal utilizando el valor a una cierta fecha de un índice de tipo de cambio prefijado. Para dar de alta uno de estos objetos se requiere:

- `InterestRateIndex`: el índice de tasa de interés prefijado
- `QCDate`: fecha inicio (para la aplicación de la tasa)
- `QCDate`: fecha final (para la aplicación de la tasa)
- `QCDate`: fecha de fijación del índice de tasa de interés 
- `QCDate`: fecha de pago
- `float`: nominal (monto al que se le aplica la tasa)
- `float`: amortización (eventual flujo de caja que corresponde a una porción del nominal)
- `bool`: indica si la amortización anterior es un flujo de caja o sólo una disminución de nominal
- `QCCurrency`: moneda del nominal y del flujo de caja
- `float`: spread aditivo a aplicar a la fijación del índice
- `float`: spread multiplicativo o gearing a aplicar a la fijación del índice
- `QCDate`: fecha de publicación del índice de tipo de cambio
- `QCCurrency`: moneda en la que se liquida el flujo
- `FXRateIndex`: índice de tipo de cambio a utilizar
- `float`: valor del índice de tipo de cambio

### Construcción

Parámetros iniciales.


```python
fecha_inicio = qcf.QCDate(20, 9, 2019)
fecha_final = qcf.QCDate(20, 12, 2019)
fecha_pago = qcf.QCDate(20, 12, 2019)
fecha_fixing = qcf.QCDate(20, 9, 2019)
nominal = 10_000_000.0
amort = 1_000_000.0
spread = 0.02
gearing = 1.0
valor_indice_fx = 900.0
fecha_publicacion = qcf.QCDate(20, 9, 2019)
term_sofr_6m.set_rate_value(0.01)
amort_is_cashflow = True
```

Se da de alta el objeto.


```python
ibor_mccy_cashflow = qcf.IborMultiCurrencyCashflow(
    term_sofr_6m,
    fecha_inicio,
    fecha_final,
    fecha_fixing,
    fecha_pago,
    nominal,
    amort,
    amort_is_cashflow,
    usd,
    spread,
    gearing,
    fecha_publicacion,
    clp,
    indice,
    valor_indice,
)
```

### Getters

El objeto `IborMultiCurrencyCashflow` es una subclase de `IborCashflow` y por lo tanto, hereda todos sus métodos y variables.


```python
print(f"Fecha Fixing:\t {ibor_mccy_cashflow.get_fixing_date()}")
print(f"Fecha Inicio:\t {ibor_mccy_cashflow.get_start_date()}")
print(f"Fecha Final:\t {ibor_mccy_cashflow.get_end_date()}")
print(f"Fecha Pago:\t {ibor_mccy_cashflow.get_settlement_date()}")
print(f"Nominal:\t {ibor_mccy_cashflow.get_nominal():,.0f}")
print(f"Amortización:\t {ibor_mccy_cashflow.get_amortization():,.0f}")
print(f"Moneda:\t\t {ibor_mccy_cashflow.ccy()}")
print(f"Valor Tasa:\t {ibor_mccy_cashflow.get_interest_rate_value():.2%}")
print(f"Valor Spread:\t {ibor_mccy_cashflow.get_spread():.2%}")
```

    Fecha Fixing:	 2019-09-20
    Fecha Inicio:	 2019-09-20
    Fecha Final:	 2019-12-20
    Fecha Pago:	 2019-12-20
    Nominal:	 10,000,000
    Amortización:	 1,000,000
    Moneda:		 USD
    Valor Tasa:	 1.00%
    Valor Spread:	 2.00%


Adicionalmente tenemos:


```python
print(f"Fecha Fixing FX: {ibor_mccy_cashflow.get_fx_fixing_date()}")
print(f"Valor Índice FX: {ibor_mccy_cashflow.get_fx_rate_index_value():,.2f}")
```

    Fecha Fixing FX: 2019-09-20
    Valor Índice FX: 900.00


### Setters

Nuevo nominal.


```python
nuevo_nominal = 2_000_000.0
ibor_mccy_cashflow.set_nominal(nuevo_nominal)
print(f"Nominal: {ibor_mccy_cashflow.get_nominal():,.0f}")
```

    Nominal: 2,000,000


Nueva amortización.


```python
nueva_amortizacion = 200_000.0
ibor_mccy_cashflow.set_amortization(nueva_amortizacion)
print(f"Amortización: {ibor_mccy_cashflow.get_amortization():,.0f}")
```

    Amortización: 200,000


Cambia el valor del índice de tasa de interés.


```python
ibor_mccy_cashflow.set_interest_rate_value(nuevo_valor_indice:=.02)
print(f"Valor Tasa: {ibor_mccy_cashflow.get_interest_rate_value():.2%}")
```

    Valor Tasa: 2.00%


Nuevo valor para el índice FX.


```python
ibor_mccy_cashflow.set_fx_rate_index_value(950.0)
print(f"Valor Índice FX: {ibor_mccy_cashflow.get_fx_rate_index_value():,.2f}")
```

    Valor Índice FX: 950.00


### Cálculos

Método `amount`. Retorna el flujo total incluyendo la amortización si corresponde.


```python
print(f"Flujo: {ibor_mccy_cashflow.amount():,.2f}")
check = ibor_mccy_cashflow.get_nominal() * fecha_inicio.day_diff(fecha_final) / 360.0 * (
    ibor_mccy_cashflow.get_interest_rate_value() + spread) + ibor_mccy_cashflow.get_amortization()
print(f"Check: {check:,.2f}")
```

    Flujo: 220,222.22
    Check: 220,222.22


Método `accrued_interest`. Retorna el interés devengado a una cierta fecha.


```python
fecha_devengo = qcf.QCDate(20, 10, 2019)
print(f"Interés Devengado al {fecha_devengo}: {ibor_mccy_cashflow.accrued_interest(fecha_devengo):,.2f}")

tasa = ibor_mccy_cashflow.get_interest_rate_value() + ibor_mccy_cashflow.get_spread()

check = tasa * fecha_inicio.day_diff(fecha_devengo) / 360.0 * ibor_cashflow.get_nominal()
print(f"Check: {check:,.2f}")
```

    Interés Devengado al 2019-10-20: 6,666.67
    Check: 6,666.67


Se agrega el método `accrued_interest_in_sett_ccy` que retorna el interés devengo en moneda de pago. Para utilizarlo se requiere un objeto de tipo `time_series`.


```python
ts[fecha_inicio] = 800.0
ts[fecha_devengo] = 950.0
```


```python
print(f"Interés devengado en moneda de pago: {ibor_mccy_cashflow.accrued_interest_in_sett_ccy(fecha_devengo, ts):,.0f}")
print(f"Check: {check * 950.0:,.0f}")
```

    Interés devengado en moneda de pago: 6,333,333
    Check: 6,333,333


### Funciones `show` y `get_column_names`

Al igual que en casos anteriores, juntando estas dos funciones se obtiene una representación tabular del flujo usando `pandas.DataFrame`.


```python
df = pd.DataFrame([qcf.show(ibor_mccy_cashflow)], columns=qcf.get_column_names(ibor_mccy_cashflow.get_type()))
df.style.format({
    'nocional':'{:,.2f}', 
    'amortizacion':'{:,.2f}', 
    'amortizacion_moneda_pago':'{:,.2f}', 
    'interes':'{:,.2f}',
    'interes_moneda_pago':'{:,.2f}',
    'flujo':'{:,.2f}',
    'flujo_moneda_pago':'{:,.2f}',
    'valor_tasa':'{:.2%}',
    'spread':'{:.2%}',
    'valor_indice_fx':'{:,.2f}',
})
```




<style type="text/css">
</style>
<table id="T_ffaca">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_ffaca_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_ffaca_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_ffaca_level0_col2" class="col_heading level0 col2" >fecha_fixing</th>
      <th id="T_ffaca_level0_col3" class="col_heading level0 col3" >fecha_pago</th>
      <th id="T_ffaca_level0_col4" class="col_heading level0 col4" >nocional</th>
      <th id="T_ffaca_level0_col5" class="col_heading level0 col5" >amortizacion</th>
      <th id="T_ffaca_level0_col6" class="col_heading level0 col6" >interes</th>
      <th id="T_ffaca_level0_col7" class="col_heading level0 col7" >amort_es_flujo</th>
      <th id="T_ffaca_level0_col8" class="col_heading level0 col8" >flujo</th>
      <th id="T_ffaca_level0_col9" class="col_heading level0 col9" >moneda_nocional</th>
      <th id="T_ffaca_level0_col10" class="col_heading level0 col10" >codigo_indice_tasa</th>
      <th id="T_ffaca_level0_col11" class="col_heading level0 col11" >spread</th>
      <th id="T_ffaca_level0_col12" class="col_heading level0 col12" >gearing</th>
      <th id="T_ffaca_level0_col13" class="col_heading level0 col13" >valor_tasa</th>
      <th id="T_ffaca_level0_col14" class="col_heading level0 col14" >tipo_tasa</th>
      <th id="T_ffaca_level0_col15" class="col_heading level0 col15" >fecha_fixing_fx</th>
      <th id="T_ffaca_level0_col16" class="col_heading level0 col16" >moneda_pago</th>
      <th id="T_ffaca_level0_col17" class="col_heading level0 col17" >codigo_indice_fx</th>
      <th id="T_ffaca_level0_col18" class="col_heading level0 col18" >valor_indice_fx</th>
      <th id="T_ffaca_level0_col19" class="col_heading level0 col19" >amortizacion_moneda_pago</th>
      <th id="T_ffaca_level0_col20" class="col_heading level0 col20" >interes_moneda_pago</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_ffaca_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_ffaca_row0_col0" class="data row0 col0" >2019-09-20</td>
      <td id="T_ffaca_row0_col1" class="data row0 col1" >2019-12-20</td>
      <td id="T_ffaca_row0_col2" class="data row0 col2" >2019-09-20</td>
      <td id="T_ffaca_row0_col3" class="data row0 col3" >2019-12-20</td>
      <td id="T_ffaca_row0_col4" class="data row0 col4" >2,000,000.00</td>
      <td id="T_ffaca_row0_col5" class="data row0 col5" >200,000.00</td>
      <td id="T_ffaca_row0_col6" class="data row0 col6" >20,222.22</td>
      <td id="T_ffaca_row0_col7" class="data row0 col7" >True</td>
      <td id="T_ffaca_row0_col8" class="data row0 col8" >220,222.22</td>
      <td id="T_ffaca_row0_col9" class="data row0 col9" >USD</td>
      <td id="T_ffaca_row0_col10" class="data row0 col10" >TERMSOFR6M</td>
      <td id="T_ffaca_row0_col11" class="data row0 col11" >2.00%</td>
      <td id="T_ffaca_row0_col12" class="data row0 col12" >1.000000</td>
      <td id="T_ffaca_row0_col13" class="data row0 col13" >2.00%</td>
      <td id="T_ffaca_row0_col14" class="data row0 col14" >LinAct360</td>
      <td id="T_ffaca_row0_col15" class="data row0 col15" >2019-09-20</td>
      <td id="T_ffaca_row0_col16" class="data row0 col16" >CLP</td>
      <td id="T_ffaca_row0_col17" class="data row0 col17" >USDOBS</td>
      <td id="T_ffaca_row0_col18" class="data row0 col18" >950.00</td>
      <td id="T_ffaca_row0_col19" class="data row0 col19" >190,000,000.00</td>
      <td id="T_ffaca_row0_col20" class="data row0 col20" >19,211,111.11</td>
    </tr>
  </tbody>
</table>




### Icp Clp Cashflow
Un objeto de tipo `IcpClpCashflow` representa un flujo de caja calculado como un cupón de la pata flotante de un swap ICP (cámara promedio) de Chile. Para dar de alta uno de estos objetos se requiere:

- `QCDate`: fecha inicio (para la aplicación de la tasa)
- `QCDate`: fecha final (para la aplicación de la tasa)
- `QCDate`: fecha de pago
- `float`: nominal (monto al que se le aplica la tasa)
- `float`: amortización (eventual flujo de caja que corresponde a una porción del nominal)
- `bool`: indica si la amortización anterior es un flujo de caja o sólo una disminución de nominal
- `float`: spread aditivo a aplicar a la fijación de la TNA
- `float`: spread multiplicativo o gearing a aplicar a la fijación de la TNA
- `float`: el valor del ICP a fecha de inicio (u otro valor arbitrario si el valor es desconocido)
- `float`: el valor del ICP a fecha final (u otro valor arbitrario si el valor es desconocido)

Recordar que TNA significa **Tasa Nominal Anual** y se determina utilizando los valores del índice ICP en la fecha de inicio y fecha final del `IcpClpCashflow`.


```python
# Ejemplo
fecha_inicio = qcf.QCDate(20, 9, 2018)
fecha_final = qcf.QCDate(20, 9, 2019)
fecha_pago = qcf.QCDate(23, 9, 2019)
nominal = 1_000_000_000.0
amort = 100_000_000.0
spread = 0.0
gearing = 1.0
icp_clp_cashflow = qcf.IcpClpCashflow(
    fecha_inicio,
    fecha_final,
    fecha_pago,
    nominal,
    amort,
    True,
    spread,
    gearing,
    10_000.0,
    10_250.0,
)
```


```python
# Getters
print("Fecha Inicio:", icp_clp_cashflow.get_start_date())
print("Fecha Final:", icp_clp_cashflow.get_end_date())
print(f"ICP Fecha Inicio: {icp_clp_cashflow.get_start_date_icp():,.2f}")
print(f"ICP Fecha Final: {icp_clp_cashflow.get_end_date_icp():,.2f}")
print(f"Valor TNA Todo el Período: {icp_clp_cashflow.get_rate_value():.2%}")
check = round((10250.0 / 10000 - 1) * 360.0 / fecha_inicio.day_diff(fecha_final), 4)
print(f"Check: {check:.2%}")
print(f"Nominal: {icp_clp_cashflow.get_nominal():,.0f}")
print(f"Amortización: {icp_clp_cashflow.get_amortization():,.0f}")
print("Tipo de Tasa:", icp_clp_cashflow.get_type_of_rate())
print("Moneda:", icp_clp_cashflow.ccy())
```

    Fecha Inicio: 2018-09-20
    Fecha Final: 2019-09-20
    ICP Fecha Inicio: 10,000.00
    ICP Fecha Final: 10,250.00
    Valor TNA Todo el Período: 2.47%
    Check: 2.47%
    Nominal: 1,000,000,000
    Amortización: 100,000,000
    Tipo de Tasa: LinAct360
    Moneda: CLP



```python
# Setters
decimales_para_tna = 6
icp_clp_cashflow.set_tna_decimal_places(decimales_para_tna)
print(f"Nueva TNA: {icp_clp_cashflow.get_rate_value():.4%}")

nuevo_nominal = 100
icp_clp_cashflow.set_nominal(nuevo_nominal)
print("Nuevo Nominal:", icp_clp_cashflow.get_nominal())

nueva_amortizacion = 10
icp_clp_cashflow.set_amortization(nueva_amortizacion)
print("Nueva Amortización:", icp_clp_cashflow.get_amortization())

nuevo_icp_inicio = 20_000
icp_clp_cashflow.set_start_date_icp(nuevo_icp_inicio)
print(f"Nuevo ICP Inicio: {icp_clp_cashflow.get_start_date_icp():,.2f}")

nuevo_icp_final = 20_600
icp_clp_cashflow.set_end_date_icp(nuevo_icp_final)
print(f"Nuevo ICP Final: {icp_clp_cashflow.get_end_date_icp():,.2f}")
print(f"Check TNA Final: {icp_clp_cashflow.get_rate_value():.4%}")
```

    Nueva TNA: 2.4658%
    Nuevo Nominal: 100.0
    Nueva Amortización: 10.0
    Nuevo ICP Inicio: 20,000.00
    Nuevo ICP Final: 20,600.00
    Check TNA Final: 2.9589%



```python
# Cálculos
decimales_para_tna = 4  # Se vuelve a 4 decimales de tasa
icp_clp_cashflow.set_tna_decimal_places(decimales_para_tna)

nuevo_icp_inicio = 10_000.0
icp_clp_cashflow.set_start_date_icp(nuevo_icp_inicio)

nuevo_icp_final = 10_250.0
icp_clp_cashflow.set_end_date_icp(nuevo_icp_final)

print(f"Flujo: {icp_clp_cashflow.amount():,.0f}")

fecha_devengo = qcf.QCDate(29, 3, 2019)
icp_devengo = 10_125.0
tna_devengo = icp_clp_cashflow.get_tna(fecha_devengo, icp_devengo)
print(f"TNA fijada a {fecha_devengo.description(True)}: {tna_devengo:.2%}")
check = round(
    (icp_devengo / nuevo_icp_inicio - 1) * 360.0 / fecha_inicio.day_diff(fecha_devengo),
    decimales_para_tna,
)
print(f"Check: {check:.2%}")
print(f"Interés Devengado al {fecha_devengo.description(True)}: {icp_clp_cashflow.accrued_interest(fecha_devengo, icp_devengo):,.4f}")
print(f"Check: {100 * tna_devengo * fecha_inicio.day_diff(fecha_devengo) / 360.0:,.4f}")
```

    Flujo: 13
    TNA fijada a 29-03-2019: 2.37%
    Check: 2.37%
    Interés Devengado al 29-03-2019: 1.2508
    Check: 1.2508



```python
print(qcf.show(icp_clp_cashflow))
```

    ('2018-09-20', '2019-09-20', '2019-09-23', 100.0, 10.0, True, 12.504305555555565, 'CLP', 10000.0, 10250.0, 0.0237, 2.504305555555564, 0.0, 1.0, 'LinAct360')



```python
icp_clp_cashflow.get_type()
```




    'IcpClpCashflow'



### Icp Clp Cashflow 2
Un objeto de tipo `IcpClpCashflow2` representa un flujo de caja calculado como un cupón de la pata flotante de un swap ICP (cámara promedio) de Chile. Este tipo de cashflow puede ser *quantizado*, es decir, se puede cambiar su moneda de pago componiéndolo con un objeto adicional. Para dar de alta uno de estos objetos se requiere:

- `QCDate`: fecha inicio (para la aplicación de la tasa)
- `QCDate`: fecha final (para la aplicación de la tasa)
- `QCDate`: fecha de pago
- `float`: nominal (monto al que se le aplica la tasa)
- `float`: amortización (eventual flujo de caja que corresponde a una porción del nominal)
- `bool`: indica si la amortización anterior es un flujo de caja o sólo una disminución de nominal
- `float`: spread aditivo a aplicar a la fijación de la TNA
- `float`: spread multiplicativo o gearing a aplicar a la fijación de la TNA
- `float`: el valor del ICP a fecha de inicio (u otro valor arbitrario si el valor es desconocido)
- `float`: el valor del ICP a fecha final (u otro valor arbitrario si el valor es desconocido)

Recordar que TNA significa **Tasa Nominal Anual** y se determina utilizando los valores del índice ICP en la fecha de inicio y fecha final del `IcpClpCashflow`.


```python
# Ejemplo
fecha_inicio = qcf.QCDate(20, 9, 2018)
fecha_final = qcf.QCDate(20, 9, 2019)
fecha_pago = qcf.QCDate(23, 9, 2019)
nominal = 1_000_000_000.0
amort = 100_000_000.0
spread = 0.0
gearing = 1.0
icp_clp_cashflow2 = qcf.IcpClpCashflow2(
    fecha_inicio,
    fecha_final,
    fecha_pago,
    nominal,
    amort,
    True,
    spread,
    gearing,
    True,
    10_000.0,
    10_250.0,
)
```


```python
# Getters
print("Fecha Inicio:", icp_clp_cashflow2.get_start_date())
print("Fecha Final:", icp_clp_cashflow2.get_end_date())
print(f"ICP Fecha Inicio: {icp_clp_cashflow2.get_start_date_icp():,.2f}")
print(f"ICP Fecha Final: {icp_clp_cashflow2.get_end_date_icp():,.2f}")

print()
print(f"Valor TNA Todo el Período: {icp_clp_cashflow2.get_rate_value():.2%}")
check = round((10250.0 / 10000 - 1) * 360.0 / fecha_inicio.day_diff(fecha_final), 4)
print(f"Check: {check:.2%}")
print()

print(f"Nominal: {icp_clp_cashflow2.get_nominal():,.0f}")
print(f"Amortización: {icp_clp_cashflow2.get_amortization():,.0f}")
print("Tipo de Tasa:", icp_clp_cashflow2.get_type_of_rate())
print("Moneda:", icp_clp_cashflow2.ccy())
```

    Fecha Inicio: 2018-09-20
    Fecha Final: 2019-09-20
    ICP Fecha Inicio: 10,000.00
    ICP Fecha Final: 10,250.00
    
    Valor TNA Todo el Período: 2.47%
    Check: 2.47%
    
    Nominal: 1,000,000,000
    Amortización: 100,000,000
    Tipo de Tasa: LinAct360
    Moneda: CLP



```python
# Setters
decimales_para_tna = 6
icp_clp_cashflow2.set_tna_decimal_places(decimales_para_tna)
print(f"Nueva TNA: {icp_clp_cashflow2.get_rate_value():.4%}")

nuevo_nominal = 100
icp_clp_cashflow2.set_nominal(nuevo_nominal)
print(f"Nuevo Nominal: {icp_clp_cashflow2.get_nominal():,.0f}")

nueva_amortizacion = 10
icp_clp_cashflow2.set_amortization(nueva_amortizacion)
print(f"Nueva Amortización: {icp_clp_cashflow2.get_amortization():,.0f}")

nuevo_icp_inicio = 20_000.0
icp_clp_cashflow2.set_start_date_icp(nuevo_icp_inicio)
print(f"Nuevo ICP Inicio: {icp_clp_cashflow2.get_start_date_icp():,.2f}")

nuevo_icp_final = 20_000.0
icp_clp_cashflow2.set_end_date_icp(nuevo_icp_final)
print(f"Nuevo ICP Final: {icp_clp_cashflow2.get_end_date_icp():,.2f}")
print(f"Check TNA Final: {icp_clp_cashflow2.get_rate_value():.4%}")
```

    Nueva TNA: 2.4658%
    Nuevo Nominal: 100
    Nueva Amortización: 10
    Nuevo ICP Inicio: 20,000.00
    Nuevo ICP Final: 20,000.00
    Check TNA Final: 0.0000%



```python
# Cálculos
decimales_para_tna = 4  # Se vuelve a 4 decimales de tasa
icp_clp_cashflow2.set_tna_decimal_places(decimales_para_tna)

nuevo_icp_inicio = 10_000.0
icp_clp_cashflow2.set_start_date_icp(nuevo_icp_inicio)

nuevo_icp_final = 10_250.0
icp_clp_cashflow2.set_end_date_icp(nuevo_icp_final)

print(f"Flujo: {icp_clp_cashflow2.amount():,.2f}")
print()

fecha_devengo = qcf.QCDate(29, 3, 2019)
icp_devengo = 10_125.0
tna_devengo = icp_clp_cashflow2.get_tna(fecha_devengo, icp_devengo)
print(f"TNA fijada al {fecha_devengo.description(True)}: {tna_devengo:.2%}")
check = round((icp_devengo / nuevo_icp_inicio - 1) * 360.0 / fecha_inicio.day_diff(fecha_devengo), decimales_para_tna)
print(f"Check: {check:.2%}")
print()

data = qcf.time_series()
data[fecha_devengo] = icp_devengo
print(f"Interés Devengado al {fecha_devengo.description(True)}: {icp_clp_cashflow2.accrued_interest(fecha_devengo, data):,.6f}")
check = 100 * tna_devengo * fecha_inicio.day_diff(fecha_devengo) / 360.0
print(f"Check: {check:,.6f}")
```

    Flujo: 12.50
    
    TNA fijada al 29-03-2019: 2.37%
    Check: 2.37%
    
    Interés Devengado al 29-03-2019: 1.250833
    Check: 1.250833



```python
print(qcf.show(icp_clp_cashflow2))
```

    ('2018-09-20', '2019-09-20', '2019-09-23', 100.0, 10.0, True, 12.499999999999991, 'CLP', 10000.0, 10250.0, 0.0247, 2.504305555555564, 0.0, 1.0, 'LinAct360')



```python
icp_clp_cashflow2.get_type()
```




    'IcpClpCashflow'



## Overnight Index Cashflow

Un objeto de tipo `OvernightIndexCashflow` representa un flujo de caja del tipo de la pata flotante de un swap ICP (cámara promedio) de Chile usando cualquier tipo de índice similar (por ejemplo SOFRINDX) y cualquier moneda. Adicionalmente, permite definir en forma independiente a `start_date` y `end_date` las fechas inicial y final utilizadas para los valores del índice. Esto puede resultar útil cuando una de estas operaciones se utiliza para cubrir créditos o bonos a tasa fija. Para dar de alta uno de estos objetos se requiere:

- `QCDate`: fecha inicio devengo (para la aplicación de la tasa)
- `QCDate`: fecha final devengo (para la aplicación de la tasa)
- `QCDate`: fecha inicio índice (para el valor del índice)
- `QCDate`: fecha final índice (para el valor del índice)
- `QCDate`: fecha de pago
- `QCCurrency`: moneda del nocional
- `float`: nocional (monto al que se le aplica la tasa)
- `float`: amortización (eventual flujo de caja que corresponde a una porción del nominal)
- `bool`: indica si la amortización anterior es un flujo de caja o sólo una disminución de nominal
- `float`: spread aditivo a aplicar a la fijación de la tasa equivalente (TNA en el caso de un ICPCLP)
- `float`: spread multiplicativo o gearing a aplicar a la fijación de la tasa equivalente
- `QCInterestRate`: con este objeto se especifica en qué convención se calcula la tasa equivalente
- `string`: nombre del índice overnight a utilizar
- `unsigned int`: número de decimales a utilizar para determinar la tasa equivalente
- `DatesForEquivalentRate`: enum que indica qué fechas se utilizan en el cálculo de la tasa equivalente.

### Construcción

Alta de parámetros iniciales.


```python
# Fecha inicio de devengo es un domingo
fecha_inicio_devengo = qcf.QCDate(12, 11, 2023)

# Fecha final de devengo es sábado
fecha_final_devengo = qcf.QCDate(18, 11, 2023)

# Estas fechas deben corresponder a días hábiles
# En ambos casos vamos a la fecha hábil siguiente
fecha_inicio_indice = qcf.QCDate(13, 11, 2023)
fecha_final_indice = qcf.QCDate(20, 11, 2023)

# La fecha de pago es el lunes siguiente
fecha_pago = qcf.QCDate(20, 11, 2023)

# Se usan las fechas de inicio y fin de devengo para
# el cálculo de la tasa equivalente
dates_for_eq_rate = qcf.DatesForEquivalentRate.ACCRUAL

moneda_nocional = qcf.QCUSD()
nocional = 1_000_000_000.0
amort = 100_000_000.0
amort_es_flujo = True
spread = 0.0
gearing = 1.0
tasa = qcf.QCInterestRate(0.0, qcf.QCAct360(), qcf.QCLinearWf())
nombre_indice = 'INDICE'
num_decimales = 8
valor_indice_inicio = 1.0
valor_indice_final = 1 + .1234 * 4 / 360 # Suponemos un valor constante de 10% por 4 días del índice
```

Se da de alta el objeto.


```python
overnight_index_cashflow = qcf.OvernightIndexCashflow(
    fecha_inicio_devengo,
    fecha_final_devengo,
    fecha_inicio_indice,
    fecha_final_indice,
    fecha_pago,
    moneda_nocional,
    nocional,
    amort,
    amort_es_flujo,
    spread,
    gearing,
    tasa,
    nombre_indice,
    num_decimales,
    dates_for_eq_rate,
)
```

### Getters


```python
print(f"Type of Cashflow: {overnight_index_cashflow.get_type()}")
print(f"Nominal: {overnight_index_cashflow.get_nominal():,.0f}")
print(f"Amortización: {overnight_index_cashflow.get_amortization():,.0f}")
print(f"Fecha Inicio Devengo: {overnight_index_cashflow.get_start_date()}")
print(f"Fecha Final Devengo: {overnight_index_cashflow.get_end_date()}")
print(f"Fecha Inicio Índice: {overnight_index_cashflow.get_index_start_date()}")
print(f"Fecha Final Índice: {overnight_index_cashflow.get_index_end_date()}")
print(f"Fecha Pago: {overnight_index_cashflow.get_settlement_date()}")
print(f"Valor Índice Fecha Inicio: {overnight_index_cashflow.get_start_date_index():,.8f}")
print(f"Valor ïndice Fecha Final: {overnight_index_cashflow.get_end_date_index():,.8f}")
print(f"Valor Tasa Eq: {overnight_index_cashflow.get_rate_value():.4%}")
print(f"Tipo de Tasa: {overnight_index_cashflow.get_type_of_rate()}")
print(f"Moneda: {overnight_index_cashflow.ccy()}")
```

    Type of Cashflow: OvernightIndexCashflow
    Nominal: 1,000,000,000
    Amortización: 100,000,000
    Fecha Inicio Devengo: 2023-11-12
    Fecha Final Devengo: 2023-11-18
    Fecha Inicio Índice: 2023-11-13
    Fecha Final Índice: 2023-11-20
    Fecha Pago: 2023-11-20
    Valor Índice Fecha Inicio: 1.00000000
    Valor ïndice Fecha Final: 1.00000000
    Valor Tasa Eq: 0.0000%
    Tipo de Tasa: LinAct360
    Moneda: USD


### Setters

Se fijan los valores inicial y final del índice.


```python
valor_indice_inicio = 10_000.0
overnight_index_cashflow.set_start_date_index(valor_indice_inicio)
print(f"Valor Índice Fecha Inicio: {overnight_index_cashflow.get_start_date_index():,.2f}")

valor_indice_final = 10_000.0 * (1 + .051234 * 7 / 360.0)
overnight_index_cashflow.set_end_date_index(valor_indice_final)
print(f"Valor ïndice Fecha Final: {overnight_index_cashflow.get_end_date_index():,.2f}")
```

    Valor Índice Fecha Inicio: 10,000.00
    Valor ïndice Fecha Final: 10,009.96


Decimales para el cálculo de la tasa equivalente.


```python
decimales_para_tasa_eq = 4
overnight_index_cashflow.set_eq_rate_decimal_places(decimales_para_tasa_eq)
print(f"Nueva Tasa Eq: {overnight_index_cashflow.get_rate_value():.4%}")
```

    Nueva Tasa Eq: 5.9800%



```python
decimales_para_tasa_eq = 6
overnight_index_cashflow.set_eq_rate_decimal_places(decimales_para_tasa_eq)
print(f"Nueva Tasa Eq: {overnight_index_cashflow.get_rate_value():.4%}")
```

    Nueva Tasa Eq: 5.9773%


Nuevo nocional.


```python
new_notional = 123_456
overnight_index_cashflow.set_nominal(new_notional)
print(f"Nuevo Nocional: {overnight_index_cashflow.get_nominal():,.2f}")
```

    Nuevo Nocional: 123,456.00


Nueva amortización.


```python
new_amortization = 100_000
overnight_index_cashflow.set_amortization(new_amortization)
print(f"Nueva Amortización: {overnight_index_cashflow.get_amortization():,.2f}")
```

    Nueva Amortización: 100,000.00


### Cálculos

Tasa equivalente del período.


```python
print(f"Valor Tasa Equivalente Todo el Período: {overnight_index_cashflow.get_rate_value():.6%}")
check = round((
    valor_indice_final / valor_indice_inicio - 1
) * 360.0 / fecha_inicio_devengo.day_diff(fecha_final_devengo), decimales_para_tasa_eq)
print(f"Check: {check:.6%}")
```

    Valor Tasa Equivalente Todo el Período: 5.977300%
    Check: 5.977300%


Se cambian las fechas utilizadas para el cálculo de la tasa equivalente.


```python
overnight_index_cashflow.set_dates_for_eq_rate(qcf.DatesForEquivalentRate.INDEX)
print(f"Valor Tasa Equivalente Todo el Período: {overnight_index_cashflow.get_rate_value():.6%}")
check = round((
    valor_indice_final / valor_indice_inicio - 1
) * 360.0 / fecha_inicio_indice.day_diff(fecha_final_indice), decimales_para_tasa_eq)
print(f"Check: {check:.6%}")
```

    Valor Tasa Equivalente Todo el Período: 5.123400%
    Check: 5.123400%


Método `accrued_interest`. Este método tiene dos sobrecargas. En la primera, el valor del índice se entrega explícitamente. En el ejemplo se utilizan las dos opciones para el parámetro `dates_for_eq_rate`.


```python
# Volvemos el nocional y la amortización al valor inicial
overnight_index_cashflow.set_nominal(nocional)
overnight_index_cashflow.set_amortization(amort)

fecha_devengo = qcf.QCDate(17, 11, 2023)
valor_indice_devengo = 10_000.0 * (1 + .051234 * 4 / 360)

overnight_index_cashflow.set_dates_for_eq_rate(qcf.DatesForEquivalentRate.ACCRUAL)
print(f"Interés devengado (dates_for_eq_rate = ACCRUAL): {overnight_index_cashflow.accrued_interest(fecha_devengo, valor_indice_devengo): ,.4f}")
tasa = round((
    valor_indice_devengo / valor_indice_inicio - 1
) * 360.0 / fecha_inicio_devengo.day_diff(fecha_devengo), decimales_para_tasa_eq)
print(f"Check: {nocional * fecha_inicio_devengo.day_diff(fecha_devengo) * tasa / 360.0:,.4f}\n")

overnight_index_cashflow.set_dates_for_eq_rate(qcf.DatesForEquivalentRate.INDEX)
print(f"Interés devengado (dates_for_eq_rate = INDEX): {overnight_index_cashflow.accrued_interest(fecha_devengo, valor_indice_devengo): ,.4f}")
tasa = round((
    valor_indice_devengo / valor_indice_inicio - 1
) * 360.0 / fecha_inicio_indice.day_diff(fecha_devengo), decimales_para_tasa_eq)
print(f"Check: {nocional * fecha_inicio_devengo.day_diff(fecha_devengo) * tasa / 360.0:,.4f}")
```

    Interés devengado (dates_for_eq_rate = ACCRUAL):  569,263.8889
    Check: 569,263.8889
    
    Interés devengado (dates_for_eq_rate = INDEX):  711,583.3333
    Check: 711,583.3333


La segunda sobrecarga de `accrued_interest` permite empaquetar el valor del índice a fecha de devengo en un objeto de tipo `time_series`.


```python
data = qcf.time_series()
data[fecha_devengo] = valor_indice_devengo

overnight_index_cashflow.set_dates_for_eq_rate(qcf.DatesForEquivalentRate.ACCRUAL)

# El segundo parámetro de accrued_interest es ahora data
print(f"Interés devengado (dates_for_eq_rate = ACCRUAL): {overnight_index_cashflow.accrued_interest(fecha_devengo, data): ,.4f}")

# En este caso, en los dias para el cálculo de la tasa equivalente
# coinciden con los días de devengo, aunque cualquiera de las dos
# fechas de devengo sea inhábil.
dias_calculo_tasa_eq = fecha_inicio_devengo.day_diff(fecha_devengo)
tasa = (valor_indice_devengo / valor_indice_inicio - 1) * 360.0 / dias_calculo_tasa_eq
tasa = round(tasa, decimales_para_tasa_eq)

dias_devengo = dias_calculo_tasa_eq
print(f"Check: {nocional * tasa * dias_devengo / 360.0:,.4f}\n")

overnight_index_cashflow.set_dates_for_eq_rate(qcf.DatesForEquivalentRate.INDEX)

# El segundo parámetro de accrued_interest es ahora data
print(f"Interés devengado (dates_for_eq_rate = INDEX): {overnight_index_cashflow.accrued_interest(fecha_devengo, data): ,.4f}")

# En este caso, en los días para el cálculo de la tasa equivalente 
# se utiliza las fecha de inicio del índice.
dias_calculo_tasa_eq = fecha_inicio_indice.day_diff(fecha_devengo)
tasa = (valor_indice_devengo / valor_indice_inicio - 1) * 360.0 / dias_calculo_tasa_eq
tasa = round(tasa, decimales_para_tasa_eq)

# Para el devengo siempre se utiliza, los días de devengo
print(f"Check: {nocional * tasa * dias_devengo / 360.0:,.4f}\n")
```

    Interés devengado (dates_for_eq_rate = ACCRUAL):  569,263.8889
    Check: 569,263.8889
    
    Interés devengado (dates_for_eq_rate = INDEX):  711,583.3333
    Check: 711,583.3333
    


Método `amount`


```python
overnight_index_cashflow.set_dates_for_eq_rate(qcf.DatesForEquivalentRate.ACCRUAL)
print(f"Amount (ACCRUAL): {overnight_index_cashflow.amount():,.4f}")
dias_calculo_tasa_eq = fecha_inicio_devengo.day_diff(fecha_final_devengo)
tasa = (valor_indice_final / valor_indice_inicio - 1) * 360.0 / dias_calculo_tasa_eq
dias_devengo = dias_calculo_tasa_eq
print(f"Check: {nocional * (1 + tasa * dias_devengo / 360.0):,.4f}\n")

overnight_index_cashflow.set_dates_for_eq_rate(qcf.DatesForEquivalentRate.INDEX)
print(f"Amount (INDEX): {overnight_index_cashflow.amount():,.4f}")
dias_calculo_tasa_eq = fecha_inicio_indice.day_diff(fecha_final_indice)
tasa = (valor_indice_final / valor_indice_inicio - 1) * 360.0 / dias_calculo_tasa_eq
print(f"Check: {nocional * (1 + tasa * dias_devengo / 360.0):,.4f}\n")
```

    Amount (ACCRUAL): 100,996,216.6667
    Check: 1,000,996,216.6667
    
    Amount (INDEX): 100,853,900.0000
    Check: 1,000,853,900.0000
    


### Funciones `show` y `get_column_names`

Al igual que en casos anteriores, juntando estas dos funciones se obtiene una representación tabular del flujo usando `pandas.DataFrame`.


```python
df = pd.DataFrame([qcf.show(overnight_index_cashflow)], columns=qcf.get_column_names(overnight_index_cashflow.get_type()))
df.style.format({
    'nocional':'{:,.2f}', 
    'amortizacion':'{:,.2f}', 
    'amortizacion_moneda_pago':'{:,.2f}', 
    'interes':'{:,.2f}',
    'interes_moneda_pago':'{:,.2f}',
    'flujo':'{:,.2f}',
    'flujo_moneda_pago':'{:,.2f}',
    'valor_tasa_equivalente':'{:.6%}',
    'spread':'{:.2%}',
    'valor_indice_inicial':'{:,.2f}',
    'valor_indice_final':'{:,.2f}',
})
```




<style type="text/css">
</style>
<table id="T_4da74">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_4da74_level0_col0" class="col_heading level0 col0" >fecha_inicial_devengo</th>
      <th id="T_4da74_level0_col1" class="col_heading level0 col1" >fecha_final_devengo</th>
      <th id="T_4da74_level0_col2" class="col_heading level0 col2" >fecha_inicial_indice</th>
      <th id="T_4da74_level0_col3" class="col_heading level0 col3" >fecha_final_indice</th>
      <th id="T_4da74_level0_col4" class="col_heading level0 col4" >fecha_pago</th>
      <th id="T_4da74_level0_col5" class="col_heading level0 col5" >nocional</th>
      <th id="T_4da74_level0_col6" class="col_heading level0 col6" >amortizacion</th>
      <th id="T_4da74_level0_col7" class="col_heading level0 col7" >amort_es_flujo</th>
      <th id="T_4da74_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_4da74_level0_col9" class="col_heading level0 col9" >nombre_indice</th>
      <th id="T_4da74_level0_col10" class="col_heading level0 col10" >valor_indice_inicial</th>
      <th id="T_4da74_level0_col11" class="col_heading level0 col11" >valor_indice_final</th>
      <th id="T_4da74_level0_col12" class="col_heading level0 col12" >valor_tasa_equivalente</th>
      <th id="T_4da74_level0_col13" class="col_heading level0 col13" >tipo_tasa</th>
      <th id="T_4da74_level0_col14" class="col_heading level0 col14" >interes</th>
      <th id="T_4da74_level0_col15" class="col_heading level0 col15" >flujo</th>
      <th id="T_4da74_level0_col16" class="col_heading level0 col16" >spread</th>
      <th id="T_4da74_level0_col17" class="col_heading level0 col17" >gearing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_4da74_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_4da74_row0_col0" class="data row0 col0" >2023-11-12</td>
      <td id="T_4da74_row0_col1" class="data row0 col1" >2023-11-18</td>
      <td id="T_4da74_row0_col2" class="data row0 col2" >2023-11-13</td>
      <td id="T_4da74_row0_col3" class="data row0 col3" >2023-11-20</td>
      <td id="T_4da74_row0_col4" class="data row0 col4" >2023-11-20</td>
      <td id="T_4da74_row0_col5" class="data row0 col5" >1,000,000,000.00</td>
      <td id="T_4da74_row0_col6" class="data row0 col6" >100,000,000.00</td>
      <td id="T_4da74_row0_col7" class="data row0 col7" >True</td>
      <td id="T_4da74_row0_col8" class="data row0 col8" >USD</td>
      <td id="T_4da74_row0_col9" class="data row0 col9" >INDICE</td>
      <td id="T_4da74_row0_col10" class="data row0 col10" >10,000.00</td>
      <td id="T_4da74_row0_col11" class="data row0 col11" >10,009.96</td>
      <td id="T_4da74_row0_col12" class="data row0 col12" >5.123400%</td>
      <td id="T_4da74_row0_col13" class="data row0 col13" >LinAct360</td>
      <td id="T_4da74_row0_col14" class="data row0 col14" >1,195,466.67</td>
      <td id="T_4da74_row0_col15" class="data row0 col15" >101,195,466.67</td>
      <td id="T_4da74_row0_col16" class="data row0 col16" >0.00%</td>
      <td id="T_4da74_row0_col17" class="data row0 col17" >1.000000</td>
    </tr>
  </tbody>
</table>




## Overnight Index Multi Currency Cashflow

Un objeto de tipo `OvernightIndexMultiCurrencyCashflow` hereda de `OvernightIndexCashflow` y representa un flujo de caja del tipo de la pata flotante de un swap ICP (cámara promedio) de Chile usando cualquier tipo de índice similar (por ejemplo SOFRINDX), cualquier moneda de nocional, pero con flujos de caja en una moneda distinta a la del nocional, por ejemplo un ICPCLP con contraparte en US que compensa en USD. Al heredar de `OvernightIndexCashflow`, también permite definir en forma independiente a `start_date` y `end_date` las fechas inicial y final utilizadas para los valores del índice. Para dar de alta uno de estos objetos se requiere:

- `QCDate`: fecha inicio devengo (para la aplicación de la tasa)
- `QCDate`: fecha final devengo (para la aplicación de la tasa)
- `QCDate`: fecha inicio índice (para el valor del índice)
- `QCDate`: fecha final índice (para el valor del índice)
- `QCDate`: fecha de pago
- `QCCurrency`: moneda del nocional
- `float`: nocional (monto al que se le aplica la tasa)
- `float`: amortización (eventual flujo de caja que corresponde a una porción del nominal)
- `bool`: indica si la amortización anterior es un flujo de caja o sólo una disminución de nominal
- `float`: spread aditivo a aplicar a la fijación de la tasa equivalente (TNA en el caso de un ICPCLP)
- `float`: spread multiplicativo o gearing a aplicar a la fijación de la tasa equivalente
- `QCInterestRate`: con este objeto se especifica en qué convención se calcula la tasa equivalente
- `string`: nombre del índice overnight a utilizar
- `unsigned int`: número de decimales a utilizar para determinar la tasa equivalente
- `DatesForEquivalentRate`: enum que indica qué fechas se utilizan en el cálculo de la tasa equivalente.
  
Hasta acá son los mismos argumentos necesarios para construir un `OvernightIndexCashflow`. Se añaden los siguientes argumentos:
- `QCDate`: fecha de fixing del índice de tipo de cambio. Esta fecha se refiere a la fecha de publicación del índice, no a la fecha de fixing en sentido financiero.
- `QCCurrency`: moneda de pago de los flujos de caja
- `FXRateIndex>`: índice de tipo de cambio utilizado para la conversión de los flujos a moneda de pago

#### Ejemplo


```python
fecha_inicio_devengo = qcf.QCDate(13, 11, 2023)

# Notar que la fecha final de devengo es sábado
fecha_final_devengo = qcf.QCDate(18, 11, 2023)

fecha_inicio_indice = qcf.QCDate(13, 11, 2023)

# Notar que la fecha final de índice es el viernes
fecha_final_indice = qcf.QCDate(17, 11, 2023)

# La fecha de pago es el lunes siguiente
fecha_pago = qcf.QCDate(20, 11, 2023)

moneda_nocional = qcf.QCUSD()
nocional = 1_000_000_000.0
amort = 100_000_000.0
amort_es_flujo = True
spread = 0.0
gearing = 1.0
tasa = qcf.QCInterestRate(0.0, qcf.QCAct360(), qcf.QCLinearWf())
nombre_indice = 'INDICE'
num_decimales = 8
valor_indice_inicio = 1.0
valor_indice_final = 1 + .1234 * 4 / 360 # Suponemos un valor constante de 12.34% por 4 días del índice
dates_for_eq_rate = qcf.DatesForEquivalentRate.ACCRUAL

# -----------------------------------------------
fecha_fixing_fx_index = fecha_final_devengo
moneda_pago = qcf.QCCLP()
indice_fx = usdclp_obs
```


```python
overnight_index_mccy_cashflow = qcf.OvernightIndexMultiCurrencyCashflow(
    fecha_inicio_devengo,
    fecha_final_devengo,
    fecha_inicio_indice,
    fecha_final_indice,
    fecha_pago,
    moneda_nocional,
    nocional,
    amort,
    amort_es_flujo,
    spread,
    gearing,
    tasa,
    nombre_indice,
    num_decimales,
    dates_for_eq_rate,
    fecha_fixing_fx_index,
    moneda_pago,
    indice_fx,
)
```


```python
type(overnight_index_mccy_cashflow)
```




    qcfinancial.OvernightIndexMultiCurrencyCashflow



#### Nuevos Getters


```python
overnight_index_mccy_cashflow.get_fx_rate_index()
```




    <qcfinancial.FXRateIndex at 0x10d861bf0>




```python
overnight_index_mccy_cashflow.get_type()
```




    'OvernightIndexMultiCurrencyCashflow'




```python
overnight_index_mccy_cashflow.get_fx_rate_index_code()
```




    'USDOBS'




```python
overnight_index_mccy_cashflow.get_fx_rate_index_value()
```




    900.0



#### Nuevos Cálculos

Primero se fijan los valores del índice overnight.


```python
overnight_index_mccy_cashflow.set_start_date_index(valor_indice_inicio)
overnight_index_mccy_cashflow.set_end_date_index(valor_indice_final)
```


```python
print(f"Amount: {overnight_index_mccy_cashflow.amount():,.2f}")
```

    Amount: 101,371,111.11



```python
print(f"Interés en moneda de pago: {overnight_index_mccy_cashflow.settlement_ccy_interest():,.0f}")
```

    Interés en moneda de pago: 1,233,999,999



```python
print(f"Amortización en moneda de pago {overnight_index_mccy_cashflow.settlement_ccy_amortization():,.0f}")
```

    Amortización en moneda de pago 90,000,000,000


#### Funciones `show` y `get_column_names`

Se envuelve el resultado de la función `show` en un `pd.DataFrame`.


```python
df = pd.DataFrame(
    [qcf.show(overnight_index_mccy_cashflow),],
    columns=qcf.get_column_names("OvernightIndexMultiCurrencyCashflow", "")
)
df.style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_89a2c">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_89a2c_level0_col0" class="col_heading level0 col0" >fecha_inicial_devengo</th>
      <th id="T_89a2c_level0_col1" class="col_heading level0 col1" >fecha_final_devengo</th>
      <th id="T_89a2c_level0_col2" class="col_heading level0 col2" >fecha_inicial_indice</th>
      <th id="T_89a2c_level0_col3" class="col_heading level0 col3" >fecha_final_indice</th>
      <th id="T_89a2c_level0_col4" class="col_heading level0 col4" >fecha_pago</th>
      <th id="T_89a2c_level0_col5" class="col_heading level0 col5" >nocional</th>
      <th id="T_89a2c_level0_col6" class="col_heading level0 col6" >amortizacion</th>
      <th id="T_89a2c_level0_col7" class="col_heading level0 col7" >amort_es_flujo</th>
      <th id="T_89a2c_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_89a2c_level0_col9" class="col_heading level0 col9" >nombre_indice</th>
      <th id="T_89a2c_level0_col10" class="col_heading level0 col10" >valor_indice_inicial</th>
      <th id="T_89a2c_level0_col11" class="col_heading level0 col11" >valor_indice_final</th>
      <th id="T_89a2c_level0_col12" class="col_heading level0 col12" >valor_tasa_equivalente</th>
      <th id="T_89a2c_level0_col13" class="col_heading level0 col13" >tipo_tasa</th>
      <th id="T_89a2c_level0_col14" class="col_heading level0 col14" >interes</th>
      <th id="T_89a2c_level0_col15" class="col_heading level0 col15" >flujo</th>
      <th id="T_89a2c_level0_col16" class="col_heading level0 col16" >spread</th>
      <th id="T_89a2c_level0_col17" class="col_heading level0 col17" >gearing</th>
      <th id="T_89a2c_level0_col18" class="col_heading level0 col18" >moneda_pago</th>
      <th id="T_89a2c_level0_col19" class="col_heading level0 col19" >indice_fx</th>
      <th id="T_89a2c_level0_col20" class="col_heading level0 col20" >fecha_fijacion_indice_fx</th>
      <th id="T_89a2c_level0_col21" class="col_heading level0 col21" >valor_indice_fx</th>
      <th id="T_89a2c_level0_col22" class="col_heading level0 col22" >interes_moneda_pago</th>
      <th id="T_89a2c_level0_col23" class="col_heading level0 col23" >amortizacion_moneda_pago</th>
      <th id="T_89a2c_level0_col24" class="col_heading level0 col24" >flujo_moneda_pago</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_89a2c_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_89a2c_row0_col0" class="data row0 col0" >2023-11-13</td>
      <td id="T_89a2c_row0_col1" class="data row0 col1" >2023-11-18</td>
      <td id="T_89a2c_row0_col2" class="data row0 col2" >2023-11-13</td>
      <td id="T_89a2c_row0_col3" class="data row0 col3" >2023-11-17</td>
      <td id="T_89a2c_row0_col4" class="data row0 col4" >2023-11-20</td>
      <td id="T_89a2c_row0_col5" class="data row0 col5" >1,000,000,000.00</td>
      <td id="T_89a2c_row0_col6" class="data row0 col6" >100,000,000.00</td>
      <td id="T_89a2c_row0_col7" class="data row0 col7" >True</td>
      <td id="T_89a2c_row0_col8" class="data row0 col8" >USD</td>
      <td id="T_89a2c_row0_col9" class="data row0 col9" >INDICE</td>
      <td id="T_89a2c_row0_col10" class="data row0 col10" >1.00</td>
      <td id="T_89a2c_row0_col11" class="data row0 col11" >1.00</td>
      <td id="T_89a2c_row0_col12" class="data row0 col12" >9.872000%</td>
      <td id="T_89a2c_row0_col13" class="data row0 col13" >LinAct360</td>
      <td id="T_89a2c_row0_col14" class="data row0 col14" >1,371,111.11</td>
      <td id="T_89a2c_row0_col15" class="data row0 col15" >101,371,111.11</td>
      <td id="T_89a2c_row0_col16" class="data row0 col16" >0.00%</td>
      <td id="T_89a2c_row0_col17" class="data row0 col17" >1.000000</td>
      <td id="T_89a2c_row0_col18" class="data row0 col18" >CLP</td>
      <td id="T_89a2c_row0_col19" class="data row0 col19" >USDOBS</td>
      <td id="T_89a2c_row0_col20" class="data row0 col20" >2023-11-18</td>
      <td id="T_89a2c_row0_col21" class="data row0 col21" >900.000000</td>
      <td id="T_89a2c_row0_col22" class="data row0 col22" >1,233,999,999.00</td>
      <td id="T_89a2c_row0_col23" class="data row0 col23" >90,000,000,000.00</td>
      <td id="T_89a2c_row0_col24" class="data row0 col24" >91,233,999,999.00</td>
    </tr>
  </tbody>
</table>




#### Nuevo Setter

Valor del índice de tipo de cambio.


```python
overnight_index_mccy_cashflow.set_fx_rate_index_value(900.0)
```

Ver el efecto en las últimas dos columnas.


```python
pd.DataFrame(
    [qcf.show(overnight_index_mccy_cashflow),],
    columns=qcf.get_column_names("OvernightIndexMultiCurrencyCashflow", "")
).style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_eaa85">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_eaa85_level0_col0" class="col_heading level0 col0" >fecha_inicial_devengo</th>
      <th id="T_eaa85_level0_col1" class="col_heading level0 col1" >fecha_final_devengo</th>
      <th id="T_eaa85_level0_col2" class="col_heading level0 col2" >fecha_inicial_indice</th>
      <th id="T_eaa85_level0_col3" class="col_heading level0 col3" >fecha_final_indice</th>
      <th id="T_eaa85_level0_col4" class="col_heading level0 col4" >fecha_pago</th>
      <th id="T_eaa85_level0_col5" class="col_heading level0 col5" >nocional</th>
      <th id="T_eaa85_level0_col6" class="col_heading level0 col6" >amortizacion</th>
      <th id="T_eaa85_level0_col7" class="col_heading level0 col7" >amort_es_flujo</th>
      <th id="T_eaa85_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_eaa85_level0_col9" class="col_heading level0 col9" >nombre_indice</th>
      <th id="T_eaa85_level0_col10" class="col_heading level0 col10" >valor_indice_inicial</th>
      <th id="T_eaa85_level0_col11" class="col_heading level0 col11" >valor_indice_final</th>
      <th id="T_eaa85_level0_col12" class="col_heading level0 col12" >valor_tasa_equivalente</th>
      <th id="T_eaa85_level0_col13" class="col_heading level0 col13" >tipo_tasa</th>
      <th id="T_eaa85_level0_col14" class="col_heading level0 col14" >interes</th>
      <th id="T_eaa85_level0_col15" class="col_heading level0 col15" >flujo</th>
      <th id="T_eaa85_level0_col16" class="col_heading level0 col16" >spread</th>
      <th id="T_eaa85_level0_col17" class="col_heading level0 col17" >gearing</th>
      <th id="T_eaa85_level0_col18" class="col_heading level0 col18" >moneda_pago</th>
      <th id="T_eaa85_level0_col19" class="col_heading level0 col19" >indice_fx</th>
      <th id="T_eaa85_level0_col20" class="col_heading level0 col20" >fecha_fijacion_indice_fx</th>
      <th id="T_eaa85_level0_col21" class="col_heading level0 col21" >valor_indice_fx</th>
      <th id="T_eaa85_level0_col22" class="col_heading level0 col22" >interes_moneda_pago</th>
      <th id="T_eaa85_level0_col23" class="col_heading level0 col23" >amortizacion_moneda_pago</th>
      <th id="T_eaa85_level0_col24" class="col_heading level0 col24" >flujo_moneda_pago</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_eaa85_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_eaa85_row0_col0" class="data row0 col0" >2023-11-13</td>
      <td id="T_eaa85_row0_col1" class="data row0 col1" >2023-11-18</td>
      <td id="T_eaa85_row0_col2" class="data row0 col2" >2023-11-13</td>
      <td id="T_eaa85_row0_col3" class="data row0 col3" >2023-11-17</td>
      <td id="T_eaa85_row0_col4" class="data row0 col4" >2023-11-20</td>
      <td id="T_eaa85_row0_col5" class="data row0 col5" >1,000,000,000.00</td>
      <td id="T_eaa85_row0_col6" class="data row0 col6" >100,000,000.00</td>
      <td id="T_eaa85_row0_col7" class="data row0 col7" >True</td>
      <td id="T_eaa85_row0_col8" class="data row0 col8" >USD</td>
      <td id="T_eaa85_row0_col9" class="data row0 col9" >INDICE</td>
      <td id="T_eaa85_row0_col10" class="data row0 col10" >1.00</td>
      <td id="T_eaa85_row0_col11" class="data row0 col11" >1.00</td>
      <td id="T_eaa85_row0_col12" class="data row0 col12" >0.000000%</td>
      <td id="T_eaa85_row0_col13" class="data row0 col13" >LinAct360</td>
      <td id="T_eaa85_row0_col14" class="data row0 col14" >0.00</td>
      <td id="T_eaa85_row0_col15" class="data row0 col15" >100,000,000.00</td>
      <td id="T_eaa85_row0_col16" class="data row0 col16" >0.00%</td>
      <td id="T_eaa85_row0_col17" class="data row0 col17" >1.000000</td>
      <td id="T_eaa85_row0_col18" class="data row0 col18" >CLP</td>
      <td id="T_eaa85_row0_col19" class="data row0 col19" >USDOBS</td>
      <td id="T_eaa85_row0_col20" class="data row0 col20" >2023-11-18</td>
      <td id="T_eaa85_row0_col21" class="data row0 col21" >900.000000</td>
      <td id="T_eaa85_row0_col22" class="data row0 col22" >0.00</td>
      <td id="T_eaa85_row0_col23" class="data row0 col23" >90,000,000,000.00</td>
      <td id="T_eaa85_row0_col24" class="data row0 col24" >90,000,000,000.00</td>
    </tr>
  </tbody>
</table>




## Compounded Overnight Rate Cashflow 2

Un objeto de tipo `CompoundedOvernightRateCashflow2` representa un flujo de caja calculado como un cupón de la pata flotante de un OIS sobre cualquier índice overnight (SOFR, FF, EONIA). Para dar de alta uno de estos objetos se requiere:

- `InterestRateIndex`: el índice de tasa de interés prefijado
- `QCDate`: fecha inicio (para la aplicación de la tasa)
- `QCDate`: fecha final (para la aplicación de la tasa)
- `QCDate`: fecha de pago
- `DateList`: fechas de fixing del índice
- `float`: nominal (monto al que se le aplica la tasa)
- `float`: amortización (eventual flujo de caja que corresponde a una porción del nominal)
- `bool`: indica si la amortización anterior es un flujo de caja o sólo una disminución de nominal
- `QCCurrency`: moneda del nocional de la operación
- `float`: spread aditivo a aplicar a la fijación de la tasa equivalente
- `float`: spread multiplicativo o gearing a aplicar a la fijación de la tasa equivalente
- `QCInterestRate`: permite especificar cuál es la convención de cálculo de la tasa equivalente
- `unsigned int`: número de decimales a usar en el cálculo de la tasa equivalente. Por ejemplo para 0.12345678% este valor debe ser 10.
- `unsigned int`: número de días de lookback
- `unsigned int`: número de días de lockout

El efecto de lookback y lockout aún no está implementado.

### Constructor

Se da de alta un índice overnight ficiticio de test.


```python
codigo = "OITEST"
lin_act360 = qcf.QCInterestRate(0.0, act360, lin_wf)
fixing_lag = qcf.Tenor("0d")
tenor = qcf.Tenor("1d")
fixing_calendar = scl
settlement_calendar = scl
oitest = qcf.InterestRateIndex(
    codigo, 
    lin_act360, 
    fixing_lag, 
    tenor, 
    fixing_calendar, 
    settlement_calendar, 
    usd
)
```

Al dar de alta directamente este cashflow es necesario entregar explícitamente las fechas de fijación. En el capítulo relacionado a construcción de `qcf.Leg` veremos cómo este proceso se simplifica.


```python
fixing_dates = qcf.DateList()
```


```python
fixing_dates.append(qcf.QCDate(27, 12, 2021))
fixing_dates.append(qcf.QCDate(28, 12, 2021))
fixing_dates.append(qcf.QCDate(29, 12, 2021))
fixing_dates.append(qcf.QCDate(30, 12, 2021))
```

Se da de alta el cashflow.


```python
cor_cashflow_2 = qcf.CompoundedOvernightRateCashflow2(
    oitest,
    qcf.QCDate(27, 12, 2021),
    qcf.QCDate(31, 12, 2021),
    qcf.QCDate(2, 1, 2022),
    fixing_dates,
    10_000_000.0,
    100_000.0,
    True,
    qcf.QCCLP(),
    spread:=0.001,
    1.0,
    qcf.QCInterestRate(0.0, qcf.QCAct360(), qcf.QCLinearWf()),
    8,
    0,
    0,
)
```

### Getters


```python
print(f"Type of cashflow: {cor_cashflow_2.get_type()}")
print(f"Fecha Inicio: {cor_cashflow_2.get_start_date()}")
print(f"Fecha Final: {cor_cashflow_2.get_end_date()}")
print(f"Fecha Pago: {cor_cashflow_2.get_settlement_date()}")
print(f"Nocional: {cor_cashflow_2.get_nominal():,.0f}")
print(f"Amortización: {cor_cashflow_2.get_amortization():,.0f}")
print(f"Moneda del nocional: {cor_cashflow_2.ccy().get_iso_code()}")
print(f"Spread: {cor_cashflow_2.get_spread():.2%}")
print(f"Gearing: {cor_cashflow_2.get_gearing():.2f}")
print(f"Número de decimales de tasa: {cor_cashflow_2.get_eq_rate_decimal_places()}")
```

    Type of cashflow: CompoundedOvernightRateCashflow2
    Fecha Inicio: 2021-12-27
    Fecha Final: 2021-12-31
    Fecha Pago: 2022-01-02
    Nocional: 10,000,000
    Amortización: 100,000
    Moneda del nocional: CLP
    Spread: 0.10%
    Gearing: 1.00
    Número de decimales de tasa: 8



```python
print("Fechas de fijación")
for d in cor_cashflow_2.get_fixing_dates():
    print(d)
```

    Fechas de fijación
    2021-12-27
    2021-12-28
    2021-12-29
    2021-12-30


### Setters


```python
cor_cashflow_2.set_notional(1_000)
print(f"Nocional: {cor_cashflow_2.get_nominal():,.0f}")
```

    Nocional: 1,000



```python
cor_cashflow_2.set_amortization(0)
cor_cashflow_2.get_amortization()
```




    0.0



Se reversa el ejemplo.


```python
cor_cashflow_2.set_notional(10_000_000.0)
cor_cashflow_2.set_amortization(100_000.0)
```

### Cálculos

El `accrued_fixing` corresponde a la fijación de tasa equivalente en una fecha anterior a la fecha final del cashflow. Para el cálculo de `accrued_fixing` se requiere un objeto de tipo `TimeSeries` que contenga los datos históricos del índice overnight.


```python
ts = qcf.time_series()
```


```python
ts[qcf.QCDate(27, 12, 2021)] = 0.01
ts[qcf.QCDate(28, 12, 2021)] = 0.02
ts[qcf.QCDate(29, 12, 2021)] = 0.03
ts[qcf.QCDate(30, 12, 2021)] = 0.04
```


```python
print(f"Accrued fixing: {cor_cashflow_2.accrued_fixing(qcf.QCDate(29, 12, 2021), ts):.6%}")
```

    Accrued fixing: 1.500028%



```python
check = ((1 + 0.01 / 360) * (1 + 0.02 / 360.0) - 1) * 360 / 2.0
print(f"Check: {check:.6%}")
```

    Check: 1.500028%


El `accrued_interest` corresponde a los intereses devengados en una fecha anterior a la fecha final del cashflow. Para el cálculo de `accrued_interest` se requiere un objeto de tipo `TimeSeries` que contenga los datos históricos del índice overnight.


```python
print(f"Accrued interest: {cor_cashflow_2.accrued_interest(qcf.QCDate(29, 12, 2021), ts):,.2f}")
```

    Accrued interest: 888.90



```python
check = (
    cor_cashflow_2.get_nominal()
    * (cor_cashflow_2.accrued_fixing(qcf.QCDate(29, 12, 2021), ts) + spread)
    * 2
    / 360.0
)
print(f"Check: {check:,.2f}")
```

    Check: 888.90


Otros.


```python
print(f"Amount: {cor_cashflow_2.amount():,.2f}")
print(f"Interés del spread: {cor_cashflow_2.interest_from_spread():,.2f}")
```

    Amount: 100,111.11
    Interés del spread: 111.11


### Método `is_expired`

Un `CompoundedOvernightRateCashflow` se considera vencido en una fecha posterior a la fecha de pago.


```python
print(f"Fecha Pago: {cor_cashflow_2.get_settlement_date()}")
```

    Fecha Pago: 2022-01-02



```python
cor_cashflow_2.is_expired(qcf.QCDate(29, 12, 2021))
```




    False




```python
cor_cashflow_2.is_expired(qcf.QCDate(2, 1, 2022))
```




    False




```python
cor_cashflow_2.is_expired(qcf.QCDate(3, 1, 2022))
```




    True



### Funciones `show` y `get_column_names`


```python
pd.DataFrame([qcf.show(cor_cashflow_2)], columns=qcf.get_column_names("CompoundedOvernightRateCashflow2", ""))
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fecha_inicial</th>
      <th>fecha_final</th>
      <th>fecha_pago</th>
      <th>nominal</th>
      <th>amortizacion</th>
      <th>interes</th>
      <th>amort_es_flujo</th>
      <th>flujo</th>
      <th>moneda</th>
      <th>codigo_indice_tasa</th>
      <th>tipo_tasa</th>
      <th>valor_tasa</th>
      <th>spread</th>
      <th>gearing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2021-12-27</td>
      <td>2021-12-31</td>
      <td>2022-01-02</td>
      <td>10000000.0</td>
      <td>100000.0</td>
      <td>888.904444</td>
      <td>True</td>
      <td>100111.111111</td>
      <td>CLP</td>
      <td>OITEST</td>
      <td>LinAct360</td>
      <td>0.0</td>
      <td>0.001</td>
      <td>1.0</td>
    </tr>
  </tbody>
</table>
</div>



## Compounded Overnight Rate Multi Currency Cashflow 2

Un objeto de tipo `CompoundedOvernightRateMultiCurrencyCashflow2` representa un flujo de caja calculado como un cupón de la pata flotante de un OIS sobre cualquier índice overnight (SOFR, FF, EONIA) con la característica adicional de liquidar sus flujos en una moneda distina a la del nocional. Para dar de alta uno de estos objetos se requiere:

- `InterestRateIndex`: el índice de tasa de interés prefijado
- `QCDate`: fecha inicio (para la aplicación de la tasa)
- `QCDate`: fecha final (para la aplicación de la tasa)
- `QCDate`: fecha de pago
- `DateList`: fechas de fixing del índice
- `float`: nominal (monto al que se le aplica la tasa)
- `float`: amortización (eventual flujo de caja que corresponde a una porción del nominal)
- `bool`: indica si la amortización anterior es un flujo de caja o sólo una disminución de nominal
- `QCCurrency`: moneda del nocional de la operación
- `float`: spread aditivo a aplicar a la fijación de la tasa equivalente
- `float`: spread multiplicativo o gearing a aplicar a la fijación de la tasa equivalente
- `QCInterestRate`: permite especificar cuál es la convención de cálculo de la tasa equivalente
- `unsigned int`: número de decimales a usar en el cálculo de la tasa equivalente. Por ejemplo para 0.12345678% este valor debe ser 10.
- `unsigned int`: número de días de lookback
- `unsigned int`: número de días de lockout

Estos argumentos son los heredados de un `CompoundedOvernightRateCashflow`. También en este caso, el efecto de lookback y lockout aún no está implementado.

A estos argumentos se debe agregar:

- `QCDate`: fecha de fixing del índice de tipo de cambio. Esta fecha se refiere a la fecha de publicación del índice, no a la fecha de fixing en sentido financiero.
- `QCCurrency`: moneda de pago de los flujos de caja
- `FXRateIndex>`: índice de tipo de cambio utilizado para la conversión de los flujos a moneda de pago

### Constructor

Se da de alta un índice overnight ficiticio de test.


```python
codigo = "OITEST"
lin_act360 = qcf.QCInterestRate(0.0, act360, lin_wf)
fixing_lag = qcf.Tenor("0d")
tenor = qcf.Tenor("1d")
fixing_calendar = scl
settlement_calendar = scl
oitest = qcf.InterestRateIndex(
    codigo, 
    lin_act360, 
    fixing_lag, 
    tenor, 
    fixing_calendar, 
    settlement_calendar, 
    usd
)
```

Al dar de alta directamente este cashflow es necesario entregar explícitamente las fechas de fijación. En el capítulo relacionado a construcción de `qcf.Leg` veremos cómo este proceso se simplifica.


```python
fixing_dates = qcf.DateList()
```


```python
fixing_dates.append(qcf.QCDate(27, 12, 2021))
fixing_dates.append(qcf.QCDate(28, 12, 2021))
fixing_dates.append(qcf.QCDate(29, 12, 2021))
fixing_dates.append(qcf.QCDate(30, 12, 2021))
```

Se da de alta el objeto.


```python
cor_cashflow_mccy_2 = qcf.CompoundedOvernightRateMultiCurrencyCashflow2(
    oitest,
    qcf.QCDate(27, 12, 2021),
    qcf.QCDate(31, 12, 2021),
    qcf.QCDate(31, 12, 2021),
    fixing_dates,
    10_000_000.0,
    100_000.0,
    True,
    qcf.QCCLP(),
    spread:=0.001,
    1.0,
    qcf.QCInterestRate(0.0, qcf.QCAct360(), qcf.QCLinearWf()),
    8,
    0,
    0,
    qcf.QCDate(31, 12, 2021),
    qcf.QCUSD(),
    usdclp_obs,
)
```

### Nuevos Getters


```python
print(f"Fx Rate Index: {cor_cashflow_mccy_2.get_fx_rate_index()}")
print(f"Fx Rate Index Value: {cor_cashflow_mccy_2.get_fx_rate_index_value()}")
print(f"Fx Rate Index Code: {cor_cashflow_mccy_2.get_fx_rate_index_code()}")
print(f"Fx Rate Index Fxing Date: {cor_cashflow_mccy_2.get_fx_rate_index_fixing_date()}")
```

    Fx Rate Index: <qcfinancial.FXRateIndex object at 0x10d861bf0>
    Fx Rate Index Value: 1.0
    Fx Rate Index Code: USDOBS
    Fx Rate Index Fxing Date: 2021-12-31


### Nuevo Setter


```python
cor_cashflow_mccy_2.set_fx_rate_index_value(2.0)
print(f"Fx Rate Index Value: {cor_cashflow_mccy_2.get_fx_rate_index_value()}")
```

    Fx Rate Index Value: 2.0


### Nuevos Cálculos


```python
print(f"Interest: {cor_cashflow_mccy_2.interest(ts):,.2f}")
```

    Interest: 2,889.16



```python
print(f"To settlement currency: {cor_cashflow_mccy_2.to_settlement_currency(cor_cashflow_mccy_2.interest(ts)):,.0f}")
```

    To settlement currency: 1,445


### Funciones `show` y `get_column_names`


```python
pd.DataFrame([qcf.show(cor_cashflow_mccy_2)], columns=qcf.get_column_names("CompoundedOvernightRateMultiCurrencyCashflow2", ""))
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>fecha_inicial</th>
      <th>fecha_final</th>
      <th>fecha_pago</th>
      <th>nominal</th>
      <th>amortizacion</th>
      <th>interes</th>
      <th>amort_es_flujo</th>
      <th>flujo</th>
      <th>moneda</th>
      <th>codigo_indice_tasa</th>
      <th>...</th>
      <th>spread</th>
      <th>gearing</th>
      <th>valor_tasa</th>
      <th>moneda_pago</th>
      <th>fx_rate_index</th>
      <th>fecha_fixing_fx</th>
      <th>valor_indice_fx</th>
      <th>interes_moneda_pago</th>
      <th>amortizacion_moneda_pago</th>
      <th>flujo_moneda_pago</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2021-12-27</td>
      <td>2021-12-31</td>
      <td>2021-12-31</td>
      <td>10000000.0</td>
      <td>100000.0</td>
      <td>2889.158889</td>
      <td>True</td>
      <td>102889.158961</td>
      <td>CLP</td>
      <td>OITEST</td>
      <td>...</td>
      <td>0.001</td>
      <td>1.0</td>
      <td>0.025002</td>
      <td>USD</td>
      <td>USDOBS</td>
      <td>2021-12-31</td>
      <td>2.0</td>
      <td>1444.579444</td>
      <td>50000.0</td>
      <td>51444.579444</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 21 columns</p>
</div>



## Icp Clf Cashflow

Un objeto de tipo `IcpClfCashflow` representa un flujo de caja calculado como un cupón de la pata flotante de un swap ICP (cámara promedio) en UF de Chile. Para dar de alta uno de estos objetos se requiere:

- `QCDate`: fecha inicio (para la aplicación de la tasa)
- `QCDate`: fecha final (para la aplicación de la tasa)
- `QCDate`: fecha de pago
- `float`: nominal (monto al que se le aplica la tasa)
- `float`: amortización (eventual flujo de caja que corresponde a una porción del nominal)
- `bool`: indica si la amortización anterior es un flujo de caja o sólo una disminución de nominal
- `float`: spread aditivo a aplicar a la fijación de la TRA
- `float`: spread multiplicativo o gearing a aplicar a la fijación de la TRA
- `vector<float>`: objeto `double_vec` (en Python) que contiene ICP Inicio, ICP Final, UF Inicio, UF Final (se debe respetar el orden)

Recordar que TRA significa **Tasa Real Anual** y se determina utilizando los valores del índice ICP y los valores de la UF en la fecha de inicio y fecha final del `IcpClfCashflow`.

### Constructor

Parámetros iniciales.


```python
fecha_inicio = qcf.QCDate(20, 9, 2018)
fecha_final = qcf.QCDate(20, 9, 2019)
fecha_pago = qcf.QCDate(23, 9, 2019)
nominal = 300_000.0
amort = 100_000.0
spread = 0.0
gearing = 1.0

icp_uf = qcf.double_vec()
# Los primeros dos valores corresponden a icp_inicial e icp_final.
# Los segundos dos valores corresponden a uf_inicial y uf_final
icp_uf.append(10_000.0)
icp_uf.append(10_250.0)
icp_uf.append(35_000.0)
icp_uf.append(35_500.0)
```

Alta del objeto.


```python
icp_clf_cashflow = qcf.IcpClfCashflow(
    fecha_inicio, 
    fecha_final, 
    fecha_pago, 
    nominal, 
    amort, 
    True, 
    spread, 
    gearing, 
    icp_uf
)
```

### Getters


```python
print("Fecha Inicio:", icp_clf_cashflow.get_start_date())
print("Fecha Final:", icp_clf_cashflow.get_end_date())

print(f"ICP Fecha Inicio: {icp_clf_cashflow.get_start_date_icp():,.2f}")
print(f"ICP Fecha Final: {icp_clf_cashflow.get_end_date_icp():,.2f}")

print(f"UF Fecha Inicio: {icp_clf_cashflow.get_start_date_uf():,.2f}")
print(f"UF Fecha Final: {icp_clf_cashflow.get_end_date_uf():,.2f}")

print(f"Valor TRA Todo el Período: {icp_clf_cashflow.get_rate_value():.4%}")
tna = icp_clf_cashflow.get_tna(fecha_final, 10_250.0)
dias = fecha_inicio.day_diff(fecha_final)
tra = ((1 + tna * dias / 360.0) * icp_uf[2]/ icp_uf[3] - 1) * 360.0 / dias
print(f"Check TRA: {round(tra, 6):.4%}")

print(f"Nominal: {icp_clf_cashflow.get_nominal():,.0f}")
print(f"Amortización: {icp_clf_cashflow.get_amortization():,.0f}")
print("Tipo de Tasa:", icp_clf_cashflow.get_type_of_rate())
print("Moneda:", icp_clf_cashflow.ccy())
```

    Fecha Inicio: 2018-09-20
    Fecha Final: 2019-09-20
    ICP Fecha Inicio: 10,000.00
    ICP Fecha Final: 10,250.00
    UF Fecha Inicio: 35,000.00
    UF Fecha Final: 35,500.00
    Valor TRA Todo el Período: 1.0461%
    Check TRA: 1.0461%
    Nominal: 300,000
    Amortización: 100,000
    Tipo de Tasa: LinAct360
    Moneda: CLF


### Setters


```python
decimales_para_tra = 8
icp_clf_cashflow.set_tra_decimal_places(decimales_para_tra)
print(f"Nueva TRA: {icp_clf_cashflow.get_rate_value():.6%}")

nuevo_nominal = 100_000.0
icp_clf_cashflow.set_nominal(nuevo_nominal)
print(f"Nuevo Nominal: {icp_clf_cashflow.get_nominal():,.0f}")

nueva_amortizacion = 10_000.0
icp_clf_cashflow.set_amortization(nueva_amortizacion)
print(f"Nueva Amortización: {icp_clf_cashflow.get_amortization():,.0f}")

nuevo_icp_inicio = 20_000.0
icp_clf_cashflow.set_start_date_icp(nuevo_icp_inicio)
print(f"Nuevo ICP Inicio: {icp_clf_cashflow.get_start_date_icp():,.2f}")

nuevo_icp_final = 20_500.0
icp_clf_cashflow.set_end_date_icp(nuevo_icp_final)
print(f"Nuevo ICP Final: {icp_clf_cashflow.get_end_date_icp():,.2f}")
print(f"Check TNA Final: {icp_clf_cashflow.get_tna(fecha_final, nuevo_icp_final):.6%}")
```

    Nueva TRA: 1.046054%
    Nuevo Nominal: 100,000
    Nueva Amortización: 10,000
    Nuevo ICP Inicio: 20,000.00
    Nuevo ICP Final: 20,500.00
    Check TNA Final: 2.470000%


### Funciones `show` y `get_column_names`


```python
df = pd.DataFrame([qcf.show(icp_clf_cashflow)], columns=qcf.get_column_names("IcpClfCashflow", ""))
format_dict['icp_inicial'] = '{:,.2f}'
format_dict['icp_final'] = '{:,.2f}'
format_dict['uf_inicial'] = '{:,.2f}'
format_dict['uf_final'] = '{:,.2f}'
df.style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_96602">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_96602_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_96602_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_96602_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_96602_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_96602_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_96602_level0_col5" class="col_heading level0 col5" >amort_es_flujo</th>
      <th id="T_96602_level0_col6" class="col_heading level0 col6" >flujo</th>
      <th id="T_96602_level0_col7" class="col_heading level0 col7" >moneda</th>
      <th id="T_96602_level0_col8" class="col_heading level0 col8" >icp_inicial</th>
      <th id="T_96602_level0_col9" class="col_heading level0 col9" >icp_final</th>
      <th id="T_96602_level0_col10" class="col_heading level0 col10" >uf_inicial</th>
      <th id="T_96602_level0_col11" class="col_heading level0 col11" >uf_final</th>
      <th id="T_96602_level0_col12" class="col_heading level0 col12" >valor_tasa</th>
      <th id="T_96602_level0_col13" class="col_heading level0 col13" >interes</th>
      <th id="T_96602_level0_col14" class="col_heading level0 col14" >spread</th>
      <th id="T_96602_level0_col15" class="col_heading level0 col15" >gearing</th>
      <th id="T_96602_level0_col16" class="col_heading level0 col16" >tipo_tasa</th>
      <th id="T_96602_level0_col17" class="col_heading level0 col17" >flujo_en_clp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_96602_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_96602_row0_col0" class="data row0 col0" >2018-09-20</td>
      <td id="T_96602_row0_col1" class="data row0 col1" >2019-09-20</td>
      <td id="T_96602_row0_col2" class="data row0 col2" >2019-09-23</td>
      <td id="T_96602_row0_col3" class="data row0 col3" >100,000.00</td>
      <td id="T_96602_row0_col4" class="data row0 col4" >10,000.00</td>
      <td id="T_96602_row0_col5" class="data row0 col5" >True</td>
      <td id="T_96602_row0_col6" class="data row0 col6" >11,060.58</td>
      <td id="T_96602_row0_col7" class="data row0 col7" >CLF</td>
      <td id="T_96602_row0_col8" class="data row0 col8" >20,000.00</td>
      <td id="T_96602_row0_col9" class="data row0 col9" >20,500.00</td>
      <td id="T_96602_row0_col10" class="data row0 col10" >35,000.00</td>
      <td id="T_96602_row0_col11" class="data row0 col11" >35,500.00</td>
      <td id="T_96602_row0_col12" class="data row0 col12" >1.046054%</td>
      <td id="T_96602_row0_col13" class="data row0 col13" >1,060.58</td>
      <td id="T_96602_row0_col14" class="data row0 col14" >0.00%</td>
      <td id="T_96602_row0_col15" class="data row0 col15" >1.000000</td>
      <td id="T_96602_row0_col16" class="data row0 col16" >LinAct360</td>
      <td id="T_96602_row0_col17" class="data row0 col17" >392,650,680</td>
    </tr>
  </tbody>
</table>



