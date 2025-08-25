# Cashflows

Para ejecutar todos los ejemplos se debe importar la librería. Se sugiere utilizar siempre el alias `qcf`. 


```python
import qcfinancial as qcf
import aux_functions as aux
import pandas as pd
```


```python
qcf.id()
```

## Simple Cashflow

Un objeto de tipo `SimpleCashflow` representa un flujo de caja cierto en una fecha y moneda. Para instanciar un objeto de este tipo se requiere:

- `QCDate`: fecha del flujo
- `float`: monto del flujo
- `QCCurrency`: moneda del flujo

Veamos un ejemplo. Primero se define los parámetros.


```python
fecha1 = qcf.QCDate(24, 8, 2024)
monto = 1_000_000
clp = qcf.QCCLP()
```

Luego, se instancia el objeto.


```python
simple_cashflow = qcf.SimpleCashflow(
    fecha1, 
    monto, 
    clp,
)
```

### Métodos `amount`, `ccy` y `date`

Permiten obtener el monto, la moneda y la fecha del flujo.


```python
print(f"Monto: {simple_cashflow.amount():,.0f}")
```


```python
print(f"Moneda: {simple_cashflow.ccy()}")
```


```python
print(f"Fecha: {simple_cashflow.date()}")
```

### Método `is_expired`

Todos los cashflows tienen el método de conveniencia `is_expired` que sirve para indicar si un flujo ya ocurrió o está vencido.


```python
simple_cashflow.is_expired(qcf.QCDate("2024-09-01"))
```

Notar que **no** se considera vencido si la fecha de referencia es menor o igual a la fecha de vencimiento.


```python
simple_cashflow.is_expired(fecha1)
```


```python
simple_cashflow.is_expired(qcf.QCDate("2024-01-01"))
```

### Función `show`

Esta función envuelve de forma cómoda todo el flujo en un objeto `tuple`. La función `show` está sobrecargada y admite todos los tipos de flujo de `qcfinancial`.


```python
qcf.show(simple_cashflow)
```

### Función `get_column_names`

Para nombrar los elementos de la tupla anterior, se puede utilizar la función `get_column_names`.


```python
qcf.get_column_names('SimpleCashflow')
```

Con ella podemos, por ejemplo, estructurar aún más el output de `show` utilizando un `pandas.DataFrame`.


```python
df = pd.DataFrame([qcf.show(simple_cashflow)])
df.columns = list(qcf.get_column_names('SimpleCashflow'))
df.style.format({'monto':'{:,.0f}'})
```

## Simple Multicurrency Cashflow

Un objeto de tipo `SimpleMultiCurrencyCashflow` representa un flujo de caja cierto en una fecha y moneda, el cual, sin embargo, se liquidará en una segunda moneda utilizando el valor de un índice de tipo de cambio a una fecha futura. Para dar de alta uno de estos objetos se requiere:

- `QCDate`: fecha final
- `float`: monto nominal
- `QCCurrency`: la moneda del monto nominal
- `QCDate`: la fecha de publicación del `FXRateIndex` que se usará en la conversión
- `QCCurrency`: la moneda final del flujo
- `FXRateIndex`: el índice de tipo de cambio a utilizar
- `float`: el valor del índice de tipo de cambio

### Ejemplo 1

Se da de alta los objetos que el constructor del índice de tipo de cambio necesita.


```python
# moneda
usd = qcf.QCUSD()

# tipo de cambio
usdclp = qcf.FXRate(usd, clp)

# tenor
_1d = qcf.Tenor('1D')
```

Aquí utilizamos `aux.get_business_calendar` para apoyarnos en la librería `holidays` y obtener el calendario de Santiago.


```python
# calendario Santiago
scl = aux.get_business_calendar("CL", range(2024, 2035))

# dólar observado
usdclp_obs = qcf.FXRateIndex(usdclp, "USDOBS", _1d, _1d, scl)

# valor del índice
fx_rate_value = 900.0
```

Se da de alta el cashflow.


```python
simple_mccy_cashflow = qcf.SimpleMultiCurrencyCashflow(
    fecha1, 
    monto, 
    clp,  # nominal en CLP
    fecha1, 
    usd,  # pago en USD
    usdclp_obs, 
    fx_rate_value
)
```

Este objeto hereda de `SimpleCashflow` y por lo tanto, los métodos `amount`, `date` y `ccy` siguen disponibles.


```python
print(f"Monto: {simple_mccy_cashflow.amount():,.2f}")
print(f"Fecha: {simple_mccy_cashflow.date()}")
print(f"Moneda: {simple_mccy_cashflow.ccy()}")
```

Para obtener el monto en la moneda de pago y la moneda de pago están los métodos `settlement_amount` y `settlement_ccy`.


```python
print(f"Monto de pago: {simple_mccy_cashflow.settlement_amount():,.0f}")
```


```python
print(f"Moneda de pago: {simple_mccy_cashflow.settlement_ccy()}")
```

El valor del índice de tipo de cambio se puede alterar con el método `set_fx_rate_index_value`.


```python
simple_mccy_cashflow.set_fx_rate_index_value(800.00)
print(f"Flujo: {simple_mccy_cashflow.settlement_amount():,.2f} {simple_mccy_cashflow.settlement_ccy()}")
```

### Ejemplo 2

Aquí, las monedas están invertidas respecto al caso anterior. El valor del índice se usa de la forma correcta.


```python
simple_mccy_cashflow = qcf.SimpleMultiCurrencyCashflow(
    fecha1, 
    1_000_000, 
    usd,  # nominal en USD
    fecha1, 
    clp,  # pago en CLP
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

### Ejemplo 3

En este caso, hay inconsistencia entre las monedas y el tipo de cambio del índice y vemos que se produce un error.


```python
eur = qcf.QCEUR()
try:
    simple_mccy_cashflow = qcf.SimpleMultiCurrencyCashflow(
        fecha1,
        1_000_000,
        usd,         # nominal en USD
        fecha1,
        eur,         # pago en EUR
        usdclp_obs,  # ¡usamos el dólar observado!
        fx_rate_value,
    )
except ValueError as e:
    print("Error:", e)
```

### Funciones `show` y `get_columns`


```python
qcf.show(simple_mccy_cashflow)
```


```python
qcf.get_column_names('SimpleMultiCurrencyCashflow')
```

Nuevamente, usando estas funciones podemos visualizar el flujo utilizando un `pandas.DataFrame`.


```python
df = pd.DataFrame([qcf.show(simple_mccy_cashflow)])
df.columns = list(qcf.get_column_names('SimpleMultiCurrencyCashflow'))
df.style.format({
    'monto_nominal':'{:,.0f}',
    'monto_moneda_pago':'{:,.0f}',
    'valor_indice_fx':'{:,.2f}'
})
```

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
nominal = 1_000_000_000.0
amortizacion = 100_000_000.0
amort_is_cashflow = False
```

Se define la yearFraction, wealthFunction el valor de la tasa y finalmente la tasa de interés.


```python
act360 = qcf.QCAct360()
lin_wf = qcf.QCLinearWf()
valor_tasa_fija = .1
tasa = qcf.QCInterestRate(valor_tasa_fija, act360, lin_wf)
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
print(f"Moneda: {fixed_rate_cashflow.ccy()}") # __str__ devuelve el ISO Code de la moneda
print(f"Nominal: {fixed_rate_cashflow.get_nominal():,.0f}")
print(f"Amortización: {fixed_rate_cashflow.get_amortization():,.0f}")
print(f"Tasa de interés: {fixed_rate_cashflow.get_rate()}")
```

Para obtener el valor de la tasa fija, se usa además un getter de `QCInterestRate`.


```python
print(f"Tasa de interés: {fixed_rate_cashflow.get_rate().get_value():.2%}")
```

### Setters

Cambiar el nominal.


```python
nuevo_nominal = 2_000_000_000.0
fixed_rate_cashflow.set_nominal(nuevo_nominal)
print(f"Nuevo nominal: {fixed_rate_cashflow.get_nominal():,.0f}")
```

Cambiar la amortización.


```python
nueva_amortizacion = 200_000_000.0
fixed_rate_cashflow.set_amortization(nueva_amortizacion)
print(f"Nueva amortización: {fixed_rate_cashflow.get_amortization():,.0f}")
```

Cambiar el valor de la tasa.


```python
fixed_rate_cashflow.set_rate_value(new_rate_value:=.12)
print(f"Nuevo valor de la tasa: {fixed_rate_cashflow.get_rate().get_value():.2%}")
```

### Cálculos

Se devuelve el valor de la tasa fija al original.


```python
fixed_rate_cashflow.set_rate_value(valor_tasa_fija)
```

Método `amount`.


```python
print(f"Flujo Total: {fixed_rate_cashflow.amount():,.0f}")
```

Vemos que el flujo incluye los intereses, pero no la amortización (`amort_is_cashflow = False`). Podemos verificar a mano este resultado.


```python
dias_devengo = fecha_inicio.day_diff(fecha_final)
print(f"Días de devengo: {dias_devengo}")
print(f"Check: {fixed_rate_cashflow.get_nominal() * valor_tasa_fija * dias_devengo / 360:,.0f}")
```

Método `accrued_interest`. Calcula el interés devengado a una cierta fecha.


```python
fecha_intermedia = qcf.QCDate(15, 1, 2025)
print(f"Interés Devengado: {fixed_rate_cashflow.accrued_interest(fecha_intermedia):,.0f}")
dias_devengo = fecha_inicio.day_diff(fecha_intermedia)
print(f"Días de devengo: {dias_devengo}")
print(f"Check: {fixed_rate_cashflow.get_nominal() * valor_tasa_fija * dias_devengo / 360.0:,.0f}")
```

Con este método, utilizando la fecha final del flujo se puede obtener el interés total.


```python
print(f"Interés total: al {fixed_rate_cashflow.accrued_interest(fixed_rate_cashflow.get_end_date()):,.0f}")
```

### Función `show`


```python
print(qcf.show(fixed_rate_cashflow))
```

### Función `get_column_names`


```python
qcf.get_column_names(fixed_rate_cashflow.get_type())
```

Nuevamente, juntando las últimas dos funciones se obtiene una representación tabular del flujo usando `pandas.DataFrame`.


```python
df = pd.DataFrame(
    [qcf.show(fixed_rate_cashflow)], 
    columns=qcf.get_column_names(fixed_rate_cashflow.get_type())
)
df.style.format({
    'nominal':'{:,.0f}', 
    'amortizacion':'{:,.0f}', 
    'interes':'{:,.0f}', 
    'flujo':'{:,.0f}',
    'valor_tasa':'{:.2%}'
})
```

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

Cuando coinciden, se usan los mismos parámetros que en el ejemplo anterior y agregamos los nuevos parámetros requeridos.


```python
fecha_fijacion = fecha_final
usd = qcf.QCUSD()
indice = usdclp_obs
valor_indice = 900.0
nominal = 1_000_000.0
amort = 100_000.0
amort_is_cashflow = True
```

Se instancia el objeto.


```python
fixed_rate_mccy_cashflow = qcf.FixedRateMultiCurrencyCashflow(
    fecha_inicio,
    fecha_final,
    fecha_pago,
    nominal,
    amort,
    amort_is_cashflow,
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
print(f"Tipo de flujo: {fixed_rate_mccy_cashflow.get_type()}")
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

### Setters

Nuevo nominal.


```python
nuevo_nominal = 100.0
fixed_rate_mccy_cashflow.set_nominal(nuevo_nominal)
print(f"Nuevo nominal: {fixed_rate_mccy_cashflow.get_nominal():,.1f}")
```

Nueva amortización.


```python
nueva_amortizacion = 10.0
fixed_rate_mccy_cashflow.set_amortization(nueva_amortizacion)
print(f"Nueva amortización: {fixed_rate_mccy_cashflow.get_amortization():,.1f}")
```

Cambiar el valor de la tasa.


```python
fixed_rate_mccy_cashflow.set_rate_value(new_rate_value)
print(f"Nuevo valor de la tasa: {fixed_rate_mccy_cashflow.get_rate().get_value():.2%}")
```

### Cálculos

Se vuelve al nominal, amortización y valor de la tasa iniciales.


```python
fixed_rate_mccy_cashflow.set_nominal(nominal)
fixed_rate_mccy_cashflow.set_amortization(amort)
fixed_rate_mccy_cashflow.set_rate_value(valor_tasa_fija)
```

Método `amount`. En este caso sí se incluye la amortización (`amort_is_cashflow = True`).


```python
print(f"Flujo Total: {fixed_rate_mccy_cashflow.amount():,.2f}")
dias_devengo = fecha_inicio.day_diff(fecha_final)
print(
    f"Check: {fixed_rate_mccy_cashflow.get_nominal() * valor_tasa_fija * dias_devengo / 360 + fixed_rate_mccy_cashflow.get_amortization():,.2f}"
)
```

Método `accrued_interest`.


```python
fecha_intermedia = qcf.QCDate(15, 1, 2025)
print(f"Interés Devengado: {(interes_devengado:=fixed_rate_mccy_cashflow.accrued_interest(fecha_intermedia)):,.02f}")
print(f"Check: {fixed_rate_mccy_cashflow.get_nominal() * valor_tasa_fija * fecha_inicio.day_diff(fecha_intermedia) / 360.0:,.02f}")
```

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

### Funciones `show` y `get_column_names`

Juntando estas dos funciones se obtiene una representación tabular del flujo usando `pandas.DataFrame`.


```python
df = pd.DataFrame(
    [qcf.show(fixed_rate_mccy_cashflow)], 
    columns=qcf.get_column_names(fixed_rate_mccy_cashflow.get_type())
)
df.style.format({
    'nominal':'{:,.2f}', 
    'amortizacion':'{:,.2f}', 
    'amortizacion_moneda_pago':'{:,.0f}', 
    'interes':'{:,.2f}', 
    'interes_moneda_pago':'{:,.0f}', 
    'flujo':'{:,.2f}',
    'valor_tasa':'{:.2%}',
    'valor_indice_fx':'{:.2f}'
})
```

## Ibor Cashflow

Un objeto de tipo `IborCashflow` representa un flujo de caja calculado a partir de la aplicación de una tasa flotante fijada en una cierta fecha (TERMSOFR, Euribor, ...) , entre dos fechas prefijadas a un nominal prefijado. Para dar de alta uno de estos objetos se requiere:

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
fixing_calendar = aux.get_business_calendar('US', range(2024, 2035))
settlement_calendar = fixing_calendar
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

Para fijar el valor del índice en una fecha en particular.


```python
term_sofr_6m.set_rate_value(0.01)
print(f"Fixing Tasa: {term_sofr_6m.get_rate().get_value():.2%}")
```


```python
fecha_fixing = qcf.QCDate(20, 9, 2018)
print(f"Fecha Inicio: {term_sofr_6m.get_start_date(fecha_fixing)}")
print(f"Fecha Final: {term_sofr_6m.get_end_date(fecha_fixing)}")
```

Con esto, veamos un ejemplo de construcción y uso de un `IborCashflow`.


```python
fecha_inicio = qcf.QCDate(20, 9, 2018)
fecha_final = qcf.QCDate(20, 9, 2019)
fecha_pago = qcf.QCDate(23, 9, 2019)
fecha_fixing = qcf.QCDate(18, 9, 2018)
nominal = 1_000_000.0
amort = 100_000.0
amort_is_cashflow = True
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
    amort_is_cashflow,
    usd,
    spread,
    gearing,
)
```

### Getters


```python
print(f"Tipo Cashflow:\t{ibor_cashflow.get_type()}")
print(f"Fecha Fixing:\t{ibor_cashflow.get_fixing_date()}")
print(f"Fecha Inicio:\t{ibor_cashflow.get_start_date()}")
print(f"Fecha Final:\t{ibor_cashflow.get_end_date()}")
print(f"Fecha Pago:\t{ibor_cashflow.get_settlement_date()}")
print(f"Nominal:\t{ibor_cashflow.get_nominal():,.0f}")
print(f"Amortización:\t{ibor_cashflow.get_amortization():,.0f}")
print(f"Moneda:\t\t{ibor_cashflow.ccy()}")
print(f"Valor Tasa:\t{ibor_cashflow.get_interest_rate_value():.2%}")
print(f"Valor Spread:\t{ibor_cashflow.get_spread():.2%}")
print(f"Valor Gearing:\t{ibor_cashflow.get_gearing():.2f}")
```

### Setters

Nuevo nominal.


```python
nuevo_nominal = 2_000_000.0
ibor_cashflow.set_nominal(nuevo_nominal)
print(f"Nominal: {ibor_cashflow.get_nominal():,.0f}")
```

Nueva amortización.


```python
nueva_amortizacion = 200_000.0
ibor_cashflow.set_amortization(nueva_amortizacion)
print(f"Amortización: {ibor_cashflow.get_amortization():,.0f}")
```

Cambia el valor del índice.


```python
ibor_cashflow.set_interest_rate_value(nuevo_valor_indice:=.02)
print(f"Valor Tasa: {ibor_cashflow.get_interest_rate_value():.2%}")
```

Cambia el valor del spread.


```python
ibor_cashflow.set_spread(.01)
print(f"Valor Spread: {ibor_cashflow.get_spread():.2%}")
```

Cambia el valor del gearing.


```python
ibor_cashflow.set_gearing(1.2)
print(f"Valor Spread: {ibor_cashflow.get_gearing():.2}")
```

### Cálculos

Método `amount`. Retorna el flujo total incluyendo la amortización si corresponde.


```python
print(f"Flujo: {ibor_cashflow.amount():,.2f}")
```

Método `accrued_interest`. Retorna el interés devengado a una cierta fecha.


```python
fecha_devengo = qcf.QCDate(20, 7, 2019)
print(f"Interés Devengado al {fecha_devengo}: {ibor_cashflow.accrued_interest(fecha_devengo):,.2f}")

# La tasa es el valor del índice más el spread
tasa = ibor_cashflow.get_interest_rate_value() * ibor_cashflow.get_gearing() + ibor_cashflow.get_spread()

check = tasa * fecha_inicio.day_diff(fecha_devengo) / 360.0 * ibor_cashflow.get_nominal()
print(f"Check: {check:,.2f}")
```

### Funciones `show` y `get_column_names`

Al igual que en casos anteriores, juntando estas dos funciones se obtiene una representación tabular del flujo usando `pandas.DataFrame`.


```python
df = pd.DataFrame(
    [qcf.show(ibor_cashflow)], 
    columns=qcf.get_column_names(ibor_cashflow.get_type())
)
df.style.format({
    'nominal':'{:,.2f}', 
    'amortizacion':'{:,.2f}', 
    'interes':'{:,.2f}', 
    'flujo':'{:,.2f}',
    'valor_tasa':'{:.2%}',
    'spread':'{:.2%}',
    'gearing':'{:.2f}',
})
```

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

Parámetros iniciales, sólo agregamos los parámetros relacionados al MultiCurrency y fijamos el valor del índice de tasa de interés en 1.00%.


```python
valor_indice_fx = 900.0
fecha_publicacion = qcf.QCDate(20, 9, 2019)
term_sofr_6m.set_rate_value(0.01)
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
print(f"Tipo Cashflow:\t {ibor_mccy_cashflow.get_type()}")
print(f"Fecha Fixing:\t {ibor_mccy_cashflow.get_fixing_date()}")
print(f"Fecha Inicio:\t {ibor_mccy_cashflow.get_start_date()}")
print(f"Fecha Final:\t {ibor_mccy_cashflow.get_end_date()}")
print(f"Fecha Pago:\t {ibor_mccy_cashflow.get_settlement_date()}")
print(f"Nominal:\t {ibor_mccy_cashflow.get_nominal():,.0f}")
print(f"Amortización:\t {ibor_mccy_cashflow.get_amortization():,.0f}")
print(f"Moneda:\t\t {ibor_mccy_cashflow.ccy()}")
print(f"Valor Tasa:\t {ibor_mccy_cashflow.get_interest_rate_value():.2%}")
print(f"Valor Spread:\t {ibor_mccy_cashflow.get_spread():.2%}")
print(f"Valor Gearing:\t {ibor_mccy_cashflow.get_gearing():.2f}")
```

Adicionalmente tenemos:


```python
print(f"Fecha Fixing FX: {ibor_mccy_cashflow.get_fx_fixing_date()}")
print(f"Valor Índice FX: {ibor_mccy_cashflow.get_fx_rate_index_value():,.2f}")
```

### Setters

Nuevo nominal.


```python
nuevo_nominal = 2_000_000.0
ibor_mccy_cashflow.set_nominal(nuevo_nominal)
print(f"Nominal: {ibor_mccy_cashflow.get_nominal():,.0f}")
```

Nueva amortización.


```python
nueva_amortizacion = 200_000.0
ibor_mccy_cashflow.set_amortization(nueva_amortizacion)
print(f"Amortización: {ibor_mccy_cashflow.get_amortization():,.0f}")
```

Cambia el valor del índice de tasa de interés.


```python
ibor_mccy_cashflow.set_interest_rate_value(nuevo_valor_indice:=.02)
print(f"Valor Tasa: {ibor_mccy_cashflow.get_interest_rate_value():.2%}")
```

Nuevo valor para el índice FX.


```python
ibor_mccy_cashflow.set_fx_rate_index_value(950.0)
print(f"Valor Índice FX: {ibor_mccy_cashflow.get_fx_rate_index_value():,.2f}")
```

### Cálculos

Método `amount`. Retorna el flujo total incluyendo la amortización si corresponde.


```python
print(f"Flujo: {ibor_mccy_cashflow.amount():,.2f}")
check = ibor_mccy_cashflow.get_nominal() * fecha_inicio.day_diff(fecha_final) / 360.0 * (
    ibor_mccy_cashflow.get_interest_rate_value() * ibor_mccy_cashflow.get_gearing() + spread) + ibor_mccy_cashflow.get_amortization()
print(f"Check: {check:,.2f}")
```

Método `accrued_interest`. Retorna el interés devengado a una cierta fecha.


```python
fecha_devengo = qcf.QCDate(20, 7, 2019)
print(f"Interés Devengado al {fecha_devengo}: {ibor_mccy_cashflow.accrued_interest(fecha_devengo):,.2f}")

tasa = ibor_mccy_cashflow.get_interest_rate_value() * ibor_mccy_cashflow.get_gearing() + ibor_mccy_cashflow.get_spread()

check = tasa * fecha_inicio.day_diff(fecha_devengo) / 360.0 * ibor_cashflow.get_nominal()
print(f"Check: {check:,.2f}")
```

Se agrega el método `accrued_interest_in_sett_ccy` que retorna el interés devengado en moneda de pago. Para utilizarlo se requiere un objeto de tipo `time_series`.


```python
ts[fecha_inicio] = 800.0
ts[fecha_devengo] = 950.0
```


```python
print(f"Interés devengado en moneda de pago: {ibor_mccy_cashflow.accrued_interest_in_sett_ccy(fecha_devengo, ts):,.0f}")
print(f"Check: {check * 950.0:,.0f}")
```

### Funciones `show` y `get_column_names`

Al igual que en casos anteriores, juntando estas dos funciones se obtiene una representación tabular del flujo usando `pandas.DataFrame`.


```python
df = pd.DataFrame(
    [qcf.show(ibor_mccy_cashflow)], 
    columns=qcf.get_column_names(ibor_mccy_cashflow.get_type())
)
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

## Overnight Index Cashflow

Un objeto de tipo `OvernightIndexCashflow` representa un flujo de caja del tipo de la pata flotante de un swap ICPCLP (cámara promedio) de Chile usando cualquier tipo de índice similar (por ejemplo SOFRINDX) y cualquier moneda. Adicionalmente, permite definir en forma independiente a `start_date` y `end_date` las fechas inicial y final utilizadas para los valores del índice. Esto puede resultar útil cuando una de estas operaciones se utiliza para cubrir créditos o bonos a tasa fija y tiene, por lo tanto, vencimientos en fechas inhábiles. Para dar de alta uno de estos objetos se requiere:

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
num_decimales = 8 # decimales como número <-> 6 decimales como porcentaje
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
print(f"Tipo Cashflow:\t\t\t{overnight_index_cashflow.get_type()}")
print(f"Nominal:\t\t\t{overnight_index_cashflow.get_nominal():,.0f}")
print(f"Amortización:\t\t\t{overnight_index_cashflow.get_amortization():,.0f}")
print(f"Fecha Inicio Devengo:\t\t{overnight_index_cashflow.get_start_date()}")
print(f"Fecha Final Devengo:\t\t{overnight_index_cashflow.get_end_date()}")
print(f"Fecha Inicio Índice:\t\t{overnight_index_cashflow.get_index_start_date()}")
print(f"Fecha Final Índice:\t\t{overnight_index_cashflow.get_index_end_date()}")
print(f"Fecha Pago:\t\t\t{overnight_index_cashflow.get_settlement_date()}")
print(f"Valor Índice Fecha Inicio:\t{overnight_index_cashflow.get_start_date_index():,.8f}")
print(f"Valor Índice Fecha Final:\t{overnight_index_cashflow.get_end_date_index():,.8f}")
print(f"Valor Tasa Eq:\t\t\t{overnight_index_cashflow.get_rate_value():.4%}")
print(f"Tipo de Tasa:\t\t\t{overnight_index_cashflow.get_type_of_rate()}")
print(f"Moneda:\t\t\t\t{overnight_index_cashflow.ccy()}")
```

### Setters

Se fijan los valores inicial y final del índice.


```python
valor_indice_inicio = 10_000.0
overnight_index_cashflow.set_start_date_index(valor_indice_inicio)
print(f"Valor Índice Fecha Inicio: {overnight_index_cashflow.get_start_date_index():,.2f}")
```


```python
valor_indice_final = valor_indice_inicio * (1 + .051234 * 7 / 360.0)
overnight_index_cashflow.set_end_date_index(valor_indice_final)
print(f"Valor Índice Fecha Final: {overnight_index_cashflow.get_end_date_index():,.8f}")
```

Decimales para el cálculo de la tasa equivalente.


```python
decimales_para_tasa_eq = 4
overnight_index_cashflow.set_eq_rate_decimal_places(decimales_para_tasa_eq)
print(f"Nueva Tasa Eq: {overnight_index_cashflow.get_rate_value():.4%}")
```


```python
decimales_para_tasa_eq = 6
overnight_index_cashflow.set_eq_rate_decimal_places(decimales_para_tasa_eq)
print(f"Nueva Tasa Eq: {overnight_index_cashflow.get_rate_value():.4%}")
```

Nuevo nocional.


```python
new_notional = 123_456
overnight_index_cashflow.set_nominal(new_notional)
print(f"Nuevo Nocional: {overnight_index_cashflow.get_nominal():,.2f}")
```

Nueva amortización.


```python
new_amortization = 100_000
overnight_index_cashflow.set_amortization(new_amortization)
print(f"Nueva Amortización: {overnight_index_cashflow.get_amortization():,.2f}")
```

### Cálculos

Tasa equivalente del período.


```python
print(f"Valor Tasa Equivalente Todo el Período: {overnight_index_cashflow.get_rate_value():.4%}")
check = round((
    valor_indice_final / valor_indice_inicio - 1
) * 360.0 / fecha_inicio_devengo.day_diff(fecha_final_devengo), decimales_para_tasa_eq)
print(f"Check: {check:.4%}")
```

Se cambian las fechas utilizadas para el cálculo de la tasa equivalente.


```python
overnight_index_cashflow.set_dates_for_eq_rate(qcf.DatesForEquivalentRate.INDEX)
print(f"Valor Tasa Equivalente Todo el Período: {overnight_index_cashflow.get_rate_value():.4%}")
check = round((
    valor_indice_final / valor_indice_inicio - 1
) * 360.0 / fecha_inicio_indice.day_diff(fecha_final_indice), decimales_para_tasa_eq)
print(f"Check: {check:.4%}")
```

Método `accrued_interest`. Este método tiene dos sobrecargas. En la primera, el valor del índice se entrega explícitamente. En el ejemplo se utilizan las dos opciones para el parámetro `dates_for_eq_rate`.


```python
# Volvemos el nocional y la amortización al valor inicial
overnight_index_cashflow.set_nominal(nocional)
overnight_index_cashflow.set_amortization(amort)
```


```python
fecha_devengo = qcf.QCDate(17, 11, 2023)
valor_indice_devengo = 10_000.0 * (1 + .051234 * 4 / 360)
```


```python
overnight_index_cashflow.set_dates_for_eq_rate(qcf.DatesForEquivalentRate.ACCRUAL)
print(f"Interés devengado (dates_for_eq_rate = ACCRUAL): {overnight_index_cashflow.accrued_interest(fecha_devengo, valor_indice_devengo): ,.4f}")
tasa = round((
    valor_indice_devengo / valor_indice_inicio - 1
) * 360.0 / fecha_inicio_devengo.day_diff(fecha_devengo), decimales_para_tasa_eq)
print(f"Check: {nocional * fecha_inicio_devengo.day_diff(fecha_devengo) * tasa / 360.0:,.4f}\n")
```


```python
overnight_index_cashflow.set_dates_for_eq_rate(qcf.DatesForEquivalentRate.INDEX)
print(f"Interés devengado (dates_for_eq_rate = INDEX): {overnight_index_cashflow.accrued_interest(fecha_devengo, valor_indice_devengo): ,.4f}")
tasa = round((
    valor_indice_devengo / valor_indice_inicio - 1
) * 360.0 / fecha_inicio_indice.day_diff(fecha_devengo), decimales_para_tasa_eq)
print(f"Check: {nocional * fecha_inicio_devengo.day_diff(fecha_devengo) * tasa / 360.0:,.4f}")
```

La segunda sobrecarga de `accrued_interest` permite empaquetar el valor del índice a fecha de devengo en un objeto de tipo `time_series`.


```python
data = qcf.time_series()
data[fecha_devengo] = valor_indice_devengo

overnight_index_cashflow.set_dates_for_eq_rate(qcf.DatesForEquivalentRate.ACCRUAL)
```


```python
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
```


```python
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

Método `amount`


```python
overnight_index_cashflow.set_dates_for_eq_rate(qcf.DatesForEquivalentRate.ACCRUAL)
print(f"Amount (ACCRUAL): {overnight_index_cashflow.amount():,.4f}")
dias_calculo_tasa_eq = fecha_inicio_devengo.day_diff(fecha_final_devengo)
tasa = (valor_indice_final / valor_indice_inicio - 1) * 360.0 / dias_calculo_tasa_eq
dias_devengo = dias_calculo_tasa_eq
print(f"Check: {nocional * (1 + tasa * dias_devengo / 360.0):,.4f}\n")
```


```python
overnight_index_cashflow.set_dates_for_eq_rate(qcf.DatesForEquivalentRate.INDEX)
print(f"Amount (INDEX): {overnight_index_cashflow.amount():,.4f}")
dias_calculo_tasa_eq = fecha_inicio_indice.day_diff(fecha_final_indice)
tasa = (valor_indice_final / valor_indice_inicio - 1) * 360.0 / dias_calculo_tasa_eq
print(f"Check: {nocional * (1 + tasa * dias_devengo / 360.0):,.4f}\n")
```

### Funciones `show` y `get_column_names`

Al igual que en casos anteriores, juntando estas dos funciones se obtiene una representación tabular del flujo usando `pandas.DataFrame`.


```python
df = pd.DataFrame(
    [qcf.show(overnight_index_cashflow)], 
    columns=qcf.get_column_names(overnight_index_cashflow.get_type())
)
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

## Overnight Index Multi Currency Cashflow

Un objeto de tipo `OvernightIndexMultiCurrencyCashflow` hereda de `OvernightIndexCashflow` y representa un flujo de caja del tipo de la pata flotante de un swap ICPCLP (cámara promedio) de Chile usando cualquier tipo de índice similar (por ejemplo SOFRINDX), cualquier moneda de nocional, pero con flujos de caja en una moneda distinta a la del nocional, por ejemplo un ICPCLP con contraparte en USA que compensa en USD. Al heredar de `OvernightIndexCashflow`, también permite definir en forma independiente a `start_date` y `end_date` las fechas inicial y final utilizadas para los valores del índice. Para dar de alta uno de estos objetos se requiere:

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
- `FXRateIndex`: índice de tipo de cambio utilizado para la conversión de los flujos a moneda de pago

### Ejemplo


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
nocional = 10_000_000.0
amort = 1_000_000.0
amort_es_flujo = True
spread = 0.0
gearing = 1.0
tasa = qcf.QCInterestRate(0.0, qcf.QCAct360(), qcf.QCLinearWf())
nombre_indice = 'INDICE'
num_decimales = 8
dates_for_eq_rate = qcf.DatesForEquivalentRate.ACCRUAL
```

Parámetros para la parte MultiCurrency.


```python
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

#### Nuevos Getters


```python
print(f"Tipo de flujo: {overnight_index_mccy_cashflow.get_type()}")
```

Este *getter* retorna todo el objeto `FXRateIndex`.


```python
overnight_index_mccy_cashflow.get_fx_rate_index()
```


```python
print(f"Código del índice FX: {overnight_index_mccy_cashflow.get_fx_rate_index_code()}")
```


```python
print(f"Valor del índice FX: {overnight_index_mccy_cashflow.get_fx_rate_index_value():,.2f}")
```

#### Nuevos Cálculos

Primero se fijan los valores del índice overnight.


```python
valor_indice_inicio = 1.0
valor_indice_final = 1 + .1234 * 4 / 360 # Suponemos un valor constante de 12.34% por 4 días del índice
```


```python
overnight_index_mccy_cashflow.set_start_date_index(valor_indice_inicio)
overnight_index_mccy_cashflow.set_end_date_index(valor_indice_final)
```


```python
print(f"Amount: {overnight_index_mccy_cashflow.amount():,.2f}")
```


```python
print(f"Interés en moneda de pago: {overnight_index_mccy_cashflow.settlement_ccy_interest():,.0f}")
```


```python
print(f"Amortización en moneda de pago {overnight_index_mccy_cashflow.settlement_ccy_amortization():,.0f}")
```

#### Funciones `show` y `get_column_names`

Se envuelve el resultado de la función `show` en un `pd.DataFrame`.


```python
df = pd.DataFrame(
    [qcf.show(overnight_index_mccy_cashflow),],
    columns=qcf.get_column_names("OvernightIndexMultiCurrencyCashflow", "")
)
df.style.format(aux.format_dict)
```

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
).style.format(aux.format_dict)
```

## Compounded Overnight Rate Cashflow 2

Un objeto de tipo `CompoundedOvernightRateCashflow2` representa un flujo de caja calculado como un cupón de la pata flotante de un OIS sobre cualquier índice overnight (SOFR, FF, ESTR). Para dar de alta uno de estos objetos se requiere:

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
fixing_calendar = aux.get_business_calendar("US", range(2024, 2035))
settlement_calendar = fixing_calendar
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

Damos de alta las variables que faltan.


```python
fecha_inicio = qcf.QCDate(27, 12, 2021)
fecha_final = qcf.QCDate(31, 12, 2021)
fecha_pago = qcf.QCDate(2, 1, 2022)
nocional = 10_000_000.0
amortizacion = 100_000.0
amort_is_cashflow = True
notional_currency = qcf.QCUSD()
spread = 0.001
gearing = 1.5
interest_rate = qcf.QCInterestRate(0.0, qcf.QCAct360(), qcf.QCLinearWf())
eq_rate_decimal_places = 8
```

Se da de alta el cashflow.


```python
cor_cashflow_2 = qcf.CompoundedOvernightRateCashflow2(
    oitest,
    fecha_inicio,
    fecha_final,
    fecha_pago,
    fixing_dates,
    nocional,
    amortizacion,
    amort_is_cashflow,
    notional_currency,
    spread,
    gearing,
    interest_rate,
    eq_rate_decimal_places,
    lookback := 0,
    lockout := 0,
)
```

### Getters


```python
print(f"Type of cashflow:\t\t{cor_cashflow_2.get_type()}")
print(f"Fecha Inicio:\t\t\t{cor_cashflow_2.get_start_date()}")
print(f"Fecha Final:\t\t\t{cor_cashflow_2.get_end_date()}")
print(f"Fecha Pago:\t\t\t{cor_cashflow_2.get_settlement_date()}")
print(f"Nocional:\t\t\t{cor_cashflow_2.get_nominal():,.0f}")
print(f"Amortización:\t\t\t{cor_cashflow_2.get_amortization():,.0f}")
print(f"Moneda del nocional:\t\t{cor_cashflow_2.ccy()}")
print(f"Spread:\t\t\t\t{cor_cashflow_2.get_spread():.2%}")
print(f"Gearing:\t\t\t{cor_cashflow_2.get_gearing():.2f}")
print(f"Número de decimales de tasa:\t{cor_cashflow_2.get_eq_rate_decimal_places()}")
```


```python
print("Fechas de fijación:")
for d in cor_cashflow_2.get_fixing_dates():
    print(d)
```

### Setters


```python
cor_cashflow_2.set_notional(1_000)
print(f"Nocional: {cor_cashflow_2.get_nominal():,.0f}")
```


```python
cor_cashflow_2.set_amortization(0)
print(f"Amortización: {cor_cashflow_2.get_amortization()}")
```

Se reversa el ejemplo.


```python
cor_cashflow_2.set_notional(nocional)
cor_cashflow_2.set_amortization(amortizacion)
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


```python
check = ((1 + 0.01 / 360) * (1 + 0.02 / 360.0) - 1) * 360 / 2.0
print(f"Check: {check:.6%}")
```

El `accrued_interest` corresponde a los intereses devengados en una fecha anterior a la fecha final del cashflow. Para el cálculo de `accrued_interest` también se requiere un objeto de tipo `TimeSeries` que contenga los datos históricos del índice overnight.


```python
print(f"Accrued interest: {cor_cashflow_2.accrued_interest(qcf.QCDate(29, 12, 2021), ts):,.2f}")
```


```python
check = (
    cor_cashflow_2.get_nominal()
    * (cor_cashflow_2.accrued_fixing(qcf.QCDate(29, 12, 2021), ts) * gearing + spread) * 2 / 360.0
)
print(f"Check: {check:,.2f}")
```

Para que el método `amount` retorne el resultado correcto, es necesario ejecutar primero el método `fixings` que realiza la fijación de todas las tasas overnight necesarias.


```python
fixing = cor_cashflow_2.fixing(ts)
print(f"Fixing: {fixing:.6%}")
```

De esa forma.


```python
print(f"Amount: {cor_cashflow_2.amount():,.2f}")
```


```python
check = ((1 + 0.01 / 360) * (1 + 0.02 / 360.0) * (1 + 0.03 / 360.0) * (1 + 0.04 / 360.0) - 1) * 360 / 4.0
print(f"Check: {nocional * (check * gearing + spread) * 4 / 360 + amortizacion:,.2f}")
```

Se puede calcular el interés que depende del spread.


```python
print(f"Interés del spread: {cor_cashflow_2.interest_from_spread():,.2f}")
```


```python
print(f"Check: {nocional * spread * 4 / 360:,.2f}")
```

### Funciones `show` y `get_column_names`


```python
df = pd.DataFrame(
    [qcf.show(cor_cashflow_2)], 
    columns=qcf.get_column_names("CompoundedOvernightRateCashflow2", "")
)
df.style.format(aux.format_dict)
```

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
- `FXRateIndex`: índice de tipo de cambio utilizado para la conversión de los flujos a moneda de pago

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

Damos de alta las variables que faltan.


```python
fecha_inicio = qcf.QCDate(27, 12, 2021)
fecha_final = qcf.QCDate(31, 12, 2021)
fecha_pago = qcf.QCDate(2, 1, 2022)
nocional = 10_000_000.0
amortizacion = 100_000.0
amort_is_cashflow = True
notional_currency = qcf.QCUSD()
spread = 0.001
gearing = 1.5
interest_rate = qcf.QCInterestRate(0.0, qcf.QCAct360(), qcf.QCLinearWf())
eq_rate_decimal_places = 8
# ---------------------Para el MultiCurrency ----------------------------
fecha_fixing_fx = fecha_pago
moneda_pago = qcf.QCCLP()
```

Se da de alta el objeto.


```python
cor_cashflow_mccy_2 = qcf.CompoundedOvernightRateMultiCurrencyCashflow2(
    oitest,
    fecha_inicio,
    fecha_final,
    fecha_pago,
    fixing_dates,
    nocional,
    amortizacion,
    amort_is_cashflow,
    notional_currency,
    spread,
    gearing,
    interest_rate,
    eq_rate_decimal_places,
    lookback,
    lockout,
    fecha_fixing_fx,
    moneda_pago,
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

### Nuevo Setter


```python
cor_cashflow_mccy_2.set_fx_rate_index_value(900.0)
print(f"Fx Rate Index Value: {cor_cashflow_mccy_2.get_fx_rate_index_value()}")
```

### Nuevos Cálculos


```python
print(f"Interest: {cor_cashflow_mccy_2.interest(ts):,.2f}")
```


```python
print(f"To settlement currency: {cor_cashflow_mccy_2.to_settlement_currency(cor_cashflow_mccy_2.interest(ts)):,.0f}")
```

### Funciones `show` y `get_column_names`


```python
df = pd.DataFrame(
    [qcf.show(cor_cashflow_mccy_2)],
    columns=qcf.get_column_names("CompoundedOvernightRateMultiCurrencyCashflow2", "")
)
df.style.format(aux.format_dict)
```

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

### Funciones `show` y `get_column_names`


```python
df = pd.DataFrame([qcf.show(icp_clf_cashflow)], columns=qcf.get_column_names("IcpClfCashflow", ""))
df.style.format(aux.format_dict)
```
