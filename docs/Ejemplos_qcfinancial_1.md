# Objetos Fundamentales

Para ejecutar todos los ejemplos se debe importar la librería. Se sugiere utilizar siempre el alias `qcf`. 


```python
import qcfinancial as qcf
import pandas as pd
```

## Monedas

Objetos para representar una divisa. En estos momentos sólo las siguientes divisas están implementadas:

- BRL
- CAD
- CLF (esta es una representación del índice de inflación chileno UF como divisa)
- CLP
- EUR
- GBP
- JPY
- MXN
- USD

Si se requiere otra, solicitarlo ingresando un *issue* en el [git repo](https://github.com/adiaz-efaa/derivative-valuation-engine) del proyecto.

El constructor por default retorna USD.


```python
x = qcf.QCCurrency()
x.get_iso_code()
```




    'USD'



Alta de divisas CLP, USD y JPY (USD se puede instanciar también de forma explícita).


```python
clp = qcf.QCCLP()
usd = qcf.QCUSD()
jpy = qcf.QCJPY()
monedas = [clp, usd, jpy]
```

### Métodos: `get_name`, `get_iso_code`, `get_iso_number`, `get_decimal_places` y `amount`.

El método `amount`debe utilizarse cuando se debe pagar o recibir un monto resultado de un cálculo. De esta forma, el monto se redondea al número correcto de decimales en la divisa (que se obtiene con `get_decimal_places`). Por ejemplo, en CLP, se redondea a 0 decimales ya que en esta divisa no se utilizan los centavos.


```python
cantidad = 100.123456
for moneda in monedas:
    print("Nombre: {}".format(moneda.get_name()))
    print("Código ISO: {}".format(moneda.get_iso_code()))
    print("Número ISO: {}".format(moneda.get_iso_number()))
    print("Número de decimales: {}".format(moneda.get_decimal_places()))
    print(
        "Cantidad {} con el número correcto de decimales: {}".format(
            cantidad, moneda.amount(100.123456)
        )
    )
    print()
```

    Nombre: Chilean Peso
    Código ISO: CLP
    Número ISO: 152
    Número de decimales: 0
    Cantidad 100.123456 con el número correcto de decimales: 100.0
    
    Nombre: U. S. Dollar
    Código ISO: USD
    Número ISO: 840
    Número de decimales: 2
    Cantidad 100.123456 con el número correcto de decimales: 100.12
    
    Nombre: Japanese Yen
    Código ISO: JPY
    Número ISO: 392
    Número de decimales: 2
    Cantidad 100.123456 con el número correcto de decimales: 100.12


## Fechas
Las fechas se representan con objetos de tipo QCDate. Para inicializar un QCDate se requiere el día, el mes y el año de la fecha.  También se puede inicializar sin valor (default constructor) en cuyo caso se obtendrá el 12-1-1969.

### Constructores

Inicializar sin valor. Se muestra además los métodos `description()` y `__str__()`.


```python
fecha = qcf.QCDate()
print(fecha.description(True))
print(fecha.description(False))
print(fecha)
```

    12-01-1969
    1969-01-12
    1969-01-12


Inicializar con una fecha específica. En este caso, el contructor realiza una validación de los parámetros iniciales.


```python
fecha1 = qcf.QCDate(14, 9, 2018)  # día, mes, año
print("Método description: {}".format(fecha1.description(True)))
print("Print de Python: {}".format(fecha1))
```

    Método description: 14-09-2018
    Print de Python: 2018-09-14


Error al tratar de construir una fecha inválida.


```python
try:
    fecha0 = qcf.QCDate(31, 2, 2018)  # ¡¡¡ 31 de febrero !!!
except ValueError as e:
    print(e)
```

    Invalid day for month = 2


### Getters y Setters


```python
# Métodos: set_day, set_month, set_year
fecha1.set_day(17)
fecha1.set_month(10)
fecha1.set_year(2019)
print("Fecha: {}".format(fecha1.description(True)))
```

    Fecha: 17-10-2019



```python
# Métodos day, month, year, weekday
print("Día: {}".format(fecha1.day()))
print("Mes: {}".format(fecha1.month()))
print("Año: {}".format(fecha1.year()))
```

    Día: 17
    Mes: 10
    Año: 2019


### Método `week_day`

Retorna una variable de tipo `enum QC_Financial.WeekDay` que representa el día de la semana que corresponde a la fecha.


```python
dia_semana = fecha1.week_day()
print("Tipo del retorno: {}".format(type(dia_semana)))
print("Día de la semana: {}".format(dia_semana))
```

    Tipo del retorno: <class 'qcfinancial.WeekDay'>
    Día de la semana: WeekDay.THU


### Método `add_months`

Suma **n meses** a `fecha1` y retorna esa nueva fecha sin cambiar el valor de `fecha1`.


```python
num_meses = 1
fecha2 = fecha1.add_months(num_meses)
print("fecha1: {}".format(fecha1.description(True)))
print("fecha2: {}".format(fecha2.description(True)))
```

    fecha1: 17-10-2019
    fecha2: 17-11-2019


### Método `add_days`

Suma **n días** a `fecha1` sin cambiar el valor de `fecha1`.


```python
num_dias = 30
fecha3 = fecha1.add_days(num_dias)
print("fecha1: {}".format(fecha1.description(True)))
print("fecha3: {}".format(fecha3.description(True)))
```

    fecha1: 17-10-2019
    fecha3: 16-11-2019


### Método `day_dif`

Calcula la diferencia en días con otra fecha. Si la otra fecha es mayor el resultado es positivo, si no, es negativo.


```python
# Dado que fecha3 > fecha1 entonces el resultado es positivo
print("fecha1.day_diff(fecha3): {} (días)".format(fecha1.day_diff(fecha3)))

# Se invierten los roles y el resultado es negativo
print("fecha3.day_diff(fecha1): {} (días)".format(fecha3.day_diff(fecha1)))
```

    fecha1.day_diff(fecha3): 30 (días)
    fecha3.day_diff(fecha1): -30 (días)


### Orden en `QCDate`

El orden de `QCDate` permite que las fechas pueden compararse entre si.


```python
print("fecha1: {}".format(fecha1))
print("fecha2: {}".format(fecha2))
print("fecha1 == fecha2: {}".format(fecha1 == fecha2))
print("fecha1 != fecha2: {}".format(fecha1 != fecha2))
print("fecha1 < fecha2: {}".format(fecha1 < fecha2))
print("fecha1 <= fecha2: {}".format(fecha1 <= fecha2))
print("fecha1 > fecha2: {}".format(fecha1 > fecha2))
print("fecha1 >= fecha2: {}".format(fecha1 >= fecha2))
```

    fecha1: 2019-10-17
    fecha2: 2019-11-17
    fecha1 == fecha2: False
    fecha1 != fecha2: True
    fecha1 < fecha2: True
    fecha1 <= fecha2: True
    fecha1 > fecha2: False
    fecha1 >= fecha2: False


### Un objeto `QCDate` es *hashable*

Esto permite que las fechas puedan usarse como `key` en un `dict`de Python. El hash que se utiliza coincide con la representación como entero de uan fecha que se utiliza en Excel.


```python
print(fecha1.__hash__())
```

    43755


### Método `build_qcdate_from_string`

Se trata de un *factory method* que permite inicializar un objeto `QCDate` a partir de un `string`.
El formato del `string` debe ser yyyy&mm&dd donde & es un separador arbitrario.


```python
str1 = "2020-01-01"
str2 = "2020/01/02"
str3 = "2020&01&03"

fecha4 = qcf.build_qcdate_from_string(str1)
print((str1 + ": {}").format(fecha4.description(False)))

fecha4 = qcf.build_qcdate_from_string(str2)
print((str2 + ": {}").format(fecha4.description(False)))

fecha4 = qcf.build_qcdate_from_string(str3)
print((str3 + ": {}").format(fecha4.description(False)))
```

    2020-01-01: 2020-01-01
    2020/01/02: 2020-01-02
    2020&01&03: 2020-01-03


## Calendarios
Los calendarios se representan con objetos de tipo `BusinesssCalendar` y son **listas** de fechas arbitrarias que representan días feriados en alguna ciudad, país, región o unión de las anteriores. Para dar de alta un calendario se requiere una fecha inicial (`QCDate` y un número entero positivo que representa el plazo inicial total del calendario en años). El objeto `BusinessCalendar` incluye explícitamente todos los días 1 de enero y considera siempre como feriado los días sábado y domingo (aunque no pertenecen de forma explícita a la **lista**).   


```python
scl = qcf.BusinessCalendar(fecha1, 10)
for holiday in scl.get_holidays():
    print(holiday)
```


```python
# Método add_holiday. Agrega una fecha a la lista.
scl.add_holiday(qcf.QCDate(2, 1, 2018))
for holiday in scl.get_holidays():
    print(holiday)
```

    2018-01-02



```python
# Método next_busy_day. Dada una fecha, si ésta es hábil retorna la misma fecha,
## si, por el contrario, la fecha es inhábil, devuelve la siguiente fecha hábil del calendario.
print("next:", scl.next_busy_day(qcf.QCDate(15, 9, 2018)))  # es sábado
print("Se agrega el 17-9-2018 a la lista")
scl.add_holiday(qcf.QCDate(17, 9, 2018))
print("nuevo next:", scl.next_busy_day(qcf.QCDate(15, 9, 2018)))
```

    next: 2018-09-17
    Se agrega el 17-9-2018 a la lista
    nuevo next: 2018-09-18



```python
# Método mod_next_busy_day. Opera igual que la función anterior a menos que la función anterior retorne una fecha
# del mes siguiente, en ese caso retorna la fecha hábil anterior.
print("fecha: 2018-04-30")
abril30 = qcf.QCDate(30, 4, 2018)
scl.add_holiday(abril30)
print("next:", scl.next_busy_day(abril30))
print("mod next:", scl.mod_next_busy_day(qcf.QCDate(30, 4, 2018)))
print("abril30:", abril30)
```

    fecha: 2018-04-30
    next: 2018-05-01
    mod next: 2018-04-27
    abril30: 2018-04-30



```python
# Método prev_busy_day. Opera de forma análoga a mod_busy_day, pero retornando la fecha hábil anterior.
print("prev:", scl.prev_busy_day(abril30).iso_code())
```

    prev: 2018-04-27



```python
# Método shift. Suma un número n de días hábiles a una fecha.
mayo2 = qcf.QCDate(2, 5, 2018)
print(scl.shift(mayo2, -1))
print(scl.shift(abril30, 0))
print(scl.shift(abril30, 1))
print(scl.shift(abril30, 5))
```

    2018-05-01
    2018-04-30
    2018-05-01
    2018-05-07


## Fracciones de Año


```python
# Existen Act/360, Act/365, 30/360 y Act/30
act360 = qcf.QCAct360()
act365 = qcf.QCAct365()
t30360 = qcf.QC30360()
act30 = qcf.QCAct30()
yfs = [act360, act365, t30360, act30]
```


```python
# Métodos yf (sobrecargado) y count_days
for yf in yfs:
    print(yf.yf(30))
    print(yf.yf(fecha1, fecha3))
    print(yf.count_days(fecha1, fecha3))
    print()
```

    0.08333333333333333
    0.08333333333333333
    30
    
    0.0821917808219178
    0.0821917808219178
    30
    
    0.08333333333333333
    0.08055555555555556
    29
    
    1.0
    1.0
    30


## Factores de Capitalización


```python
# Existen: (yf es la fracción de año asociada a la tasa de valor r)
#    QCLinearWf     ---> (1 + r * yf)
#    QCCompundWf    ---> (1 + r)**yf
#    QCContinousWf  ---> exp(r * yf)
lin_wf = qcf.QCLinearWf()
com_wf = qcf.QCCompoundWf()
exp_wf = qcf.QCContinousWf()
```

## Tasas de Interés


```python
# Dar de alta una tasa de interés
tasa_lin_act360 = qcf.QCInterestRate(0.1, act360, lin_wf)
tasa_com_act365 = qcf.QCInterestRate(0.1, act365, com_wf)
tasas = [tasa_lin_act360, tasa_com_act365]
```


```python
# Métodos get_value, set_value, wf (sobrecargado), dwf (sobrecargado)
for tasa in tasas:
    print("get", tasa.get_value())
    tasa.set_value(0.12)
    print("get nuevo valor", tasa.get_value())
    print(
        "wf", tasa.wf(fecha1, fecha3)
    )  # Retorna el factor de capitalización entre las fechas
    print(
        "dwf", tasa.dwf(fecha1, fecha3)
    )  # Retorna la derivada del factor de capitalización respecto al valor de la tasa
    # entre las fechas
    print(
        "wf1", tasa.wf(365)
    )  # Retorna el factor de capitalización para el número de días
    print(
        "dwf1", tasa.dwf(365)
    )  # Retorna la derivada del factor de capitalización respecto al valor de la tasa
    # para el número de días
    print()
```

    get 0.1
    get nuevo valor 0.12
    wf 1.01
    dwf 0.08333333333333333
    wf1 1.1216666666666666
    dwf1 1.0138888888888888
    
    get 0.1
    get nuevo valor 0.12
    wf 1.0093582031654136
    dwf 0.07407227518337182
    wf1 1.12
    dwf1 1.0



```python
tasa_lin_act360.get_rate_from_wf(0.99, 100)
```




    -0.03600000000000003



### Tenor
Es una clase que representa el concepto de tenor (1D, 1M, 1Y ...).


```python
# Ejemplo de Tenor
one_d = qcf.Tenor("1d")
one_m = qcf.Tenor("1M")
one_y = qcf.Tenor("1y")
t1d1m1y = qcf.Tenor("1D1M1Y")
t2Y3M = qcf.Tenor("2yadv3m")
tenors = [one_d, one_m, one_y, t1d1m1y, t2Y3M]
```


```python
# Métodos get_string, get_years, get_months, get_years
for tenor in tenors:
    print("string:", tenor.get_string())
    print("dias:", tenor.get_days())
    print("meses:", tenor.get_months())
    print("años:", tenor.get_years())
    print()

# Método set_tenor
t2Y3M.set_tenor("1m32y")
print(t2Y3M.get_string())
```

    string: 1D
    dias: 1
    meses: 0
    años: 0
    
    string: 1M
    dias: 0
    meses: 1
    años: 0
    
    string: 1Y
    dias: 0
    meses: 0
    años: 1
    
    string: 1Y1M1D
    dias: 1
    meses: 1
    años: 1
    
    string: 2Y3M
    dias: 0
    meses: 3
    años: 2
    
    32Y1M


## FX Rate
Es una clase que representa el concepto de tipo de cambio entre dos monedas. Para dar de alta un FXRate se requiere:

- QCCurrency: la moneda fuerte del par.
- QCCurrency: la moneda débl del par.


```python
# Ejemplo. USDCLP. Método get_code. Se retorna el código del par según la convención usual.
usdclp = qcf.FXRate(usd, clp)
print("código:", usdclp.get_code())
```

    código: USDCLP


### FXRateIndex

Representa un índice de tipo de cambio.


```python
usdclp
```




    <qcfinancial.FXRate at 0x1211db5b0>



## Índices
Todo índice pertenece a un asset class. Los distintos asset class se representan con un el enum AssetClass. Los asset class disponibles son:

- InterestRate
- InterestRateVol
- Fx
- FxVol
- Equity
- EquityVol
- Commodity
- CommodityVol
- Credit
- CreditVol


```python
# AssetClass. Existen
print(qcf.AssetClass.InterestRate)
print(qcf.AssetClass.Fx)
```

    AssetClass.InterestRate
    AssetClass.Fx


Para dar de alta un FXRateIndex se requiere:

- `FXRate`: el FXRate correspoondiente.
- `str`: nombre del índice
- `Tenor`: la regla de fixing, es 1D como el USD Observado o es 0D como un ínidce de cierre de día.
- `Tenor`: la regla para la valuta. Es 1D como el USDCLP o 2D como el EURUSD.
- `BusinessCalendar`: el calendario adecuado para aplicar las reglas de fixing y valuta.



```python
# Ejemplo.
usdclp_obs = qcf.FXRateIndex(usdclp, "USDOBS", one_d, one_d, scl)
print("fecha de publicación:", fecha1.week_day(), fecha1)
print("fecha de fixing:", usdclp_obs.fixing_date(fecha1))
print("fecha de valuta:", usdclp_obs.value_date(fecha1))
```

    fecha de publicación: WeekDay.THU 2019-10-17
    fecha de fixing: 2019-10-16
    fecha de valuta: 2019-10-17



```python
result = usdclp_obs.convert(1000, qcf.QCUSD(), 700)
print(f"Monto en CLP es: {result:,.0f}")
```

    Monto en CLP es: 700,000


### QCCurrencyConverter

Este es un objeto que permite realizar conversiones de una moneda a otra.


```python
ccy_converter = qcf.QCCurrencyConverter()
```


```python
print(f'Monto en CLP: {ccy_converter.convert(1_000, usd, 800, usdclp_obs):,.0f}')
```

    Monto en CLP: 800,000



```python
print(f'Monto en USD: {ccy_converter.convert(800_000, clp, 800, usdclp_obs):,.0f}')
```

    Monto en USD: 1,000


#### Enum para Monedas


```python
qcf.QCCurrencyEnum.AUD
```




    <QCCurrencyEnum.AUD: 0>




```python
qcf.QCCurrencyEnum.USD
```




    <QCCurrencyEnum.USD: 17>



#### Enum para FXRates


```python
qcf.QCFxRateEnum.USDCLP
```




    <QCFxRateEnum.USDCLP: 14>




```python
qcf.QCFxRateEnum.EURUSD
```




    <QCFxRateEnum.EURUSD: 28>



Ambos `enum` se pueden utilizar con el método `convert`:


```python
print(f'Monto en USD: {ccy_converter.convert(800_000, qcf.QCCurrencyEnum.CLP, 800, qcf.QCFxRateEnum.USDCLP):,.0f}')
```

    Monto en USD: 1,000



```python
print(f'Monto en USD: {ccy_converter.convert(1_000, qcf.QCCurrencyEnum.USD, 800, qcf.QCFxRateEnum.USDCLP):,.0f}')
```

    Monto en USD: 800,000


## Time Series


```python
ts = qcf.time_series()
ts[fecha1] = 10.0
```


```python
type(ts)
```




    qcfinancial.time_series




```python
for k, v in ts.items():
    print(k, v)
```

    2019-10-17 10.0


## Cashflows

### Simple Cashflow
Un objeto de tipo `SimpleCashflow` representa un flujo de caja cierto en una fecha y moneda.


```python
# Como se inicializa un objeto SimpleCashflow.
simple_cashflow = qcf.SimpleCashflow(
    fecha1, 100, clp  # fecha del flujo  # monto
)  # moneda
```


```python
simple_cashflow
```




    <qcfinancial.SimpleCashflow at 0x109429670>




```python
# Métodos amount, ccy y date
print(simple_cashflow.amount())
print(simple_cashflow.ccy().get_iso_code())
print(simple_cashflow.date())
```

    100.0
    CLP
    2019-10-17


 Primer ejemplo de la función `show`. Envuelve de forma cómoda todo el flujo en una tupla. La función show está sobregargada y admite muchos tipos de flujo.


```python
qcf.show(simple_cashflow)
```




    ('2019-10-17', 100.0, 'CLP')



### Simple Multicurrency Cashflow
Un objeto de tipo `SimpleMultiCurrencyCashflow` representa un flujo de caja cierto en una fecha y moneda, que, sin embargo, se liquidará en una segunda moneda utilizando el valor de un índice de tipo de cambio. Para dar de alta uno de estos objetos se requiere:

- `QCDate`: fecha final
- `float`: nominal
- `QCCurrency`: la moneda del nominal
- `QCDate`: la fecha de publicación del `FXRateIndex` que se usará en la conversión
- `QCCurrency`: la moneda final del flujo
- `FXRateIndex`: el índice de tipo de cambio a utilizar
- `float`: el valor del índice de tipo de cambio


```python
# Ejemplo.
simple_mccy_cashflow = qcf.SimpleMultiCurrencyCashflow(
    fecha3, 700.00, clp, fecha3, usd, usdclp_obs, 700.00
)
print("fecha flujo:", simple_mccy_cashflow.date())
print("nominal:", simple_mccy_cashflow.nominal())
print("moneda nominal:", simple_mccy_cashflow.ccy().get_iso_code())
print("flujo:", simple_mccy_cashflow.amount())
print("moneda flujo:", simple_mccy_cashflow.settlement_ccy().get_iso_code())
```

    fecha flujo: 2019-11-16
    nominal: 700.0
    moneda nominal: CLP
    flujo: 1.0
    moneda flujo: USD



```python
# El valor del índice se puede alterar (existe un setter).
simple_mccy_cashflow.set_fx_rate_index_value(800.00)
print("flujo:", simple_mccy_cashflow.amount())
```

    flujo: 0.875



```python
# Ejemplo 2. Las monedas están invertidas respecto al caso anterior. El valor del índice se usa de la forma correcta.
simple_mccy_cashflow = qcf.SimpleMultiCurrencyCashflow(
    fecha3, 1, usd, fecha3, clp, usdclp_obs, 700.00
)
print("fecha flujo:", simple_mccy_cashflow.date())
print("nominal:", simple_mccy_cashflow.nominal())
print("moneda nominal:", simple_mccy_cashflow.ccy().get_iso_code())
print("flujo:", simple_mccy_cashflow.amount())
print("moneda flujo:", simple_mccy_cashflow.settlement_ccy().get_iso_code())
```

    fecha flujo: 2019-11-16
    nominal: 1.0
    moneda nominal: USD
    flujo: 700.0
    moneda flujo: CLP



```python
# Ejemplo 3. Hay inconsistencia entre las monedas y el tipo de cambio del índice.
eur = qcf.QCEUR()
try:
    simple_mccy_cashflow = qcf.SimpleMultiCurrencyCashflow(
        fecha3, 1, usd, fecha3, eur, usdclp_obs, 700.00
    )
except ValueError as e:
    print("Error:", e)
```

    Error: Fx Rate Index provided is not compatible with nominal and settlement currency. 



```python
# Función show
qcf.show(simple_mccy_cashflow)
```




    ('2019-11-16', 1.0, 'USD', '2019-11-16', 'CLP', 'USDOBS', 700.0, 700.0)




```python
simple_mccy_cashflow.get_type()
```




    'SimpleMultiCurrencyCashflow'



### Fixed Rate Cashflow
Un objeto de tipo `FixedRateCashflow` representa un flujo de caja calculado a partir de la aplicación de una tasa prefijada, entre dos fechas prefijadas a un nominal prefijado. Para dar de alta uno de estos objetos se requiere:

- `QCDate`: fecha inicio (para la aplicación de la tasa)
- `QCDate`: fecha final (para la aplicación de la tasa)
- `QCDate`: fecha de pago
- `float`: nominal (monto al que se le aplica la tasa)
- `float`: amortización (eventual flujo de caja que corresponde a una porción del nominal)
- `bool`: indica si la amortización anterior es un flujo de caja o sólo una disminución de nominal
- `QCInterestRate`: la tasa de interés a aplicar (su valor y convenciones)
- `QCCurrency`: moneda del nominal y del flujo de caja


```python
# Ejemplo
fecha_inicio = qcf.QCDate(20, 9, 2018)
fecha_final = qcf.QCDate(20, 9, 2019)
fecha_pago = qcf.QCDate(23, 9, 2019)
tasa = qcf.QCInterestRate(0.1, act360, lin_wf)
fixed_rate_cashflow = qcf.FixedRateCashflow(
    fecha_inicio, 
    fecha_final, 
    fecha_pago, 
    1_000_000_000.0, 
    100_000_000.0, 
    True, 
    tasa, 
    clp
)
```


```python
# Getters
print("Fecha Inicio:", fixed_rate_cashflow.get_start_date())
print("Fecha Final:", fixed_rate_cashflow.get_end_date())
print("Fecha Pago:", fixed_rate_cashflow.get_settlement_date())
print("Moneda:", fixed_rate_cashflow.ccy().get_iso_code())
print(f"Nominal: {fixed_rate_cashflow.get_nominal():,.0f}")
print(f"Amortización: {fixed_rate_cashflow.get_amortization():,.0f}")
```

    Fecha Inicio: 2018-09-20
    Fecha Final: 2019-09-20
    Fecha Pago: 2019-09-23
    Moneda: CLP
    Nominal: 1,000,000,000
    Amortización: 100,000,000



```python
# Setters
# TODO: set_rate
nuevo_nominal = 2_000_000_000.0
fixed_rate_cashflow.set_nominal(nuevo_nominal)
print(f"Nuevo nominal: {fixed_rate_cashflow.get_nominal():,.0f}")

nueva_amortizacion = 200_000_000.0
fixed_rate_cashflow.set_amortization(nueva_amortizacion)
print(f"Nueva amortización: {fixed_rate_cashflow.get_amortization():,.0f}")
```

    Nuevo nominal: 2,000,000,000
    Nueva amortización: 200,000,000



```python
# Cálculos
print(f"Flujo Total: {fixed_rate_cashflow.amount():,.0f}")
print(f"Check: {fixed_rate_cashflow.get_nominal() * 0.1 * 365.0 / 360 + fixed_rate_cashflow.get_amortization():,.0f}")
print()
fecha_intermedia = qcf.QCDate(2, 1, 2019)
print(f"Interés Devengado: {fixed_rate_cashflow.accrued_interest(fecha_intermedia):,.0f}")
print(f"Check: {fixed_rate_cashflow.get_nominal() * 0.1 * fecha_inicio.day_diff(fecha_intermedia) / 360.0:,.0f}")
```

    Flujo Total: 402,777,778
    Check: 402,777,778
    
    Interés Devengado: 57,777,778
    Check: 57,777,778



```python
# Función show
print(qcf.show(fixed_rate_cashflow))
```

    ('2018-09-20', '2019-09-20', '2019-09-23', 2000000000.0, 200000000.0, 202777777.77777794, True, 402777777.7777779, 'CLP', 0.1, 'LinAct360')



```python
print(f"Interés total: al {fixed_rate_cashflow.accrued_interest(fixed_rate_cashflow.get_end_date()):,.0f}")
```

    Interés total: al 202,777,778



```python
fixed_rate_cashflow.get_type()
```




    'FixedRateCashflow'



### Fixed Rate Multi Currency Cashflow
Un objeto de tipo `FixedRateMultiCurrencyCashflow` representa un flujo de caja a tasa fija (`FixedRateCashflow`) que se liquidará en una moneda distinta de la moneda del nominal utilizando el valor a una cierta fecha de un índice de tipo de cambio prefijado. Para dar de alta uno de estos objetos se requiere:

- `QCDate`: fecha inicio (para la aplicación de la tasa)
- `QCDate`: fecha final (para la aplicación de la tasa)
- `QCDate`: fecha de pago
- `float`: nominal (monto al que se le aplica la tasa)
- `float`: amortización (eventual flujo de caja que corresponde a una porción del nominal)
- `bool`: indica si la amortización anterior es un flujo de caja o sólo una disminución de nominal
- `QCInterestRate`: la tasa de interés a aplicar (su valor y convenciones)
- `QCCurrency`: moneda del nominal
- `QCDate`: fecha de publicación del índice de tipo de cambio
- `QCCurrency`: moneda en la que se liquida el flujo
- `FXRateIndex`: índice de tipo de cambio a utilizar
- `float`: valor del índice de tipo de cambio


```python
# Ejemplo
fecha_inicio = qcf.QCDate(20, 9, 2018)
fecha_final = qcf.QCDate(20, 9, 2019)
fecha_pago = qcf.QCDate(23, 9, 2019)
fecha_publicacion = qcf.QCDate(23, 9, 2019)
usd = qcf.QCUSD()
indice = usdclp_obs
valor_indice = 20.0
nominal = 1_000.0
amort = 1_000.0
fixed_rate_mccy_cashflow = qcf.FixedRateMultiCurrencyCashflow(
    fecha_inicio,
    fecha_final,
    fecha_pago,
    nominal,
    amort,
    False,
    tasa,
    usd,
    fecha_publicacion,
    clp,
    indice,
    valor_indice,
)
print(fixed_rate_mccy_cashflow)
```

    <qcfinancial.FixedRateMultiCurrencyCashflow object at 0x1212e6a30>


**TODO: get_rate.** Este getter no debe ser un getter tradicional, ya que no es necesario que retorne una referencia a todo el objeto ``QCInterestRate``, basta con el valor y la descripción de yf y wf asociado (mejor llamarlo get_rate_info).


```python
# Getters
print("Fecha Inicio:", fixed_rate_mccy_cashflow.get_start_date())
print("Fecha Final:", fixed_rate_mccy_cashflow.get_end_date())
print("Fecha Pago:", fixed_rate_mccy_cashflow.get_settlement_date())
print("Fecha Publicación Índice FX:", fixed_rate_mccy_cashflow.get_fx_publish_date())
print("Moneda del Nominal:", fixed_rate_mccy_cashflow.ccy())
print(f"Nominal: {fixed_rate_mccy_cashflow.get_nominal():,.0f}")
print(f"Amortización: {fixed_rate_mccy_cashflow.get_amortization():,.0f}")
print("Moneda de Liquidación:", fixed_rate_mccy_cashflow.settlement_currency())
```

    Fecha Inicio: 2018-09-20
    Fecha Final: 2019-09-20
    Fecha Pago: 2019-09-23



    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    Cell In[68], line 5
          3 print("Fecha Final:", fixed_rate_mccy_cashflow.get_end_date())
          4 print("Fecha Pago:", fixed_rate_mccy_cashflow.get_settlement_date())
    ----> 5 print("Fecha Publicación Índice FX:", fixed_rate_mccy_cashflow.get_fx_publish_date())
          6 print("Moneda del Nominal:", fixed_rate_mccy_cashflow.ccy())
          7 print(f"Nominal: {fixed_rate_mccy_cashflow.get_nominal():,.0f}")


    AttributeError: 'qcfinancial.FixedRateMultiCurrencyCashflow' object has no attribute 'get_fx_publish_date'


**TODO: set_rate_value.** Debe establecer el valor de la tasa de interés.


```python
# Setters
nuevo_nominal = 100.0
fixed_rate_mccy_cashflow.set_nominal(nuevo_nominal)
print(f"Nuevo nominal: {fixed_rate_mccy_cashflow.get_nominal():,.1f}")

nueva_amortizacion = 10.0
fixed_rate_mccy_cashflow.set_amortization(nueva_amortizacion)
print(f"Nueva amortización: {fixed_rate_mccy_cashflow.get_amortization():,.1f}")
```

    Nuevo nominal: 100.0
    Nueva amortización: 10.0



```python
# Cálculos
fixed_rate_mccy_cashflow.set_nominal(nominal)
fixed_rate_mccy_cashflow.set_amortization(amort)
print(f"Flujo Total: {fixed_rate_mccy_cashflow.amount():,.2f}")
print(f"Check: {(fixed_rate_mccy_cashflow.get_nominal() * 0.1 * 365.0 / 360) * valor_indice:,.2f}")
print()
fecha_intermedia = qcf.QCDate(2, 1, 2019)
print(f"Interés Devengado: {fixed_rate_mccy_cashflow.accrued_interest(fecha_intermedia):,.02f}")
print(f"Check: {fixed_rate_mccy_cashflow.get_nominal() * 0.1 * fecha_inicio.day_diff(fecha_intermedia) / 360.0:,.02f}")
```

    Flujo Total: 101.39
    Check: 2,027.78
    
    Interés Devengado: 28.89
    Check: 28.89



```python
ts = qcf.time_series()
```


```python
ts[fecha_inicio] = 10
```


```python
ts[fecha_inicio]
```




    10.0




```python
ts[fecha_intermedia] = 15
```


```python
print(fixed_rate_mccy_cashflow.accrued_interest(fecha_intermedia, fecha_inicio, ts))
```

    288.88888888888965



```python
print(fixed_rate_mccy_cashflow.accrued_interest(fecha_intermedia, fecha_intermedia, ts))
```

    433.33333333333445



```python
# Función show
print(qcf.show(fixed_rate_mccy_cashflow))
```

    ('2018-09-20', '2019-09-20', '2019-09-23', 1000.0, 1000.0, 101.38888888888897, False, 101.38888888888897, 'USD', 0.1, 'LinAct360', '2019-09-23', 'CLP', 'USDOBS', 20.0, 20000.0, 2027.7777777777794)



```python
fixed_rate_mccy_cashflow.get_type()
```




    'FixedRateMultiCurrencyCashflow'



### Fixed Rate Cashflow 2
Un objeto de tipo `FixedRateCashflow2` representa un flujo de caja calculado a partir de la aplicación de una tasa prefijada, entre dos fechas prefijadas a un nominal prefijado. Este tipo de cashflow puede ser *quantizado*, es decir, se puede cambiar su moneda de pago componiéndolo con un objeto adicional. Para dar de alta uno de estos objetos se requiere:

- `QCDate`: fecha inicio (para la aplicación de la tasa)
- `QCDate`: fecha final (para la aplicación de la tasa)
- `QCDate`: fecha de pago
- `float`: nominal (monto al que se le aplica la tasa)
- `float`: amortización (eventual flujo de caja que corresponde a una porción del nominal)
- `bool`: indica si la amortización anterior es un flujo de caja o sólo una disminución de nominal
- `QCInterestRate`: la tasa de interés a aplicar (su valor y convenciones)
- `QCCurrency`: moneda del nominal y del flujo de caja


```python
# Ejemplo
fecha_inicio = qcf.QCDate(20, 9, 2018)
fecha_final = qcf.QCDate(20, 9, 2019)
fecha_pago = qcf.QCDate(23, 9, 2019)
tasa = qcf.QCInterestRate(0.15, act360, lin_wf)
fixed_rate_cashflow_2 = qcf.FixedRateCashflow2(
    fecha_inicio, 
    fecha_final, 
    fecha_pago, 
    1_000_000_000.0,
    100_000_000.0, 
    True, 
    tasa, 
    clp
)
```


```python
print(f"Accrued Fixing: {fixed_rate_cashflow_2.accrued_fixing(fecha_inicio):.2%}")
```

    Accrued Fixing: 15.00%



```python
print(f"amount: {fixed_rate_cashflow_2.amount():,.0f}")
print("currency:", fixed_rate_cashflow_2.ccy().get_iso_code())
print("date:", fixed_rate_cashflow_2.date())
print("start date:", fixed_rate_cashflow_2.get_start_date())
print("end date:", fixed_rate_cashflow_2.get_end_date())
print("settlement date:", fixed_rate_cashflow_2.get_settlement_date())
print("fixing dates:")
for f in fixed_rate_cashflow_2.get_fixing_dates():
    print("\t", f)
print(f"nominal: {fixed_rate_cashflow_2.get_nominal():,.0f}")
print(f"amortization: {fixed_rate_cashflow_2.get_amortization():,.0f}")
print(f"interest (1st overload): {fixed_rate_cashflow_2.interest():,.0f}")

ts = qcf.time_series()
print(f"interest (2nd overload): {fixed_rate_cashflow_2.interest(ts):,.0f}")
print(f"fixing (1st overload): {fixed_rate_cashflow_2.fixing():.2%}")
print(f"fixing (2nd overload): {fixed_rate_cashflow_2.fixing(ts):.2%}")
fecha_intermedia = qcf.QCDate(20, 3, 2019)
print(f"accrued interest (1st overload): {fixed_rate_cashflow_2.accrued_interest(fecha_intermedia):,.0f}")
print(f"accrued interest (2nd overload): {fixed_rate_cashflow_2.accrued_interest(fecha_intermedia, ts):,.0f}")
print(f"accrued fixing (1st overload): {fixed_rate_cashflow_2.accrued_fixing(fecha_intermedia):.2%}")
print(f"accrued fixing (2nd overload): {fixed_rate_cashflow_2.accrued_fixing(fecha_intermedia, ts):,.2%}")
```

    amount: 252,083,333
    currency: CLP
    date: 2019-09-23
    start date: 2018-09-20
    end date: 2019-09-20
    settlement date: 2019-09-23
    fixing dates:
    	 2018-09-20
    nominal: 1,000,000,000
    amortization: 100,000,000
    interest (1st overload): 152,083,333
    interest (2nd overload): 152,083,333
    fixing (1st overload): 15.00%
    fixing (2nd overload): 15.00%
    accrued interest (1st overload): 75,416,667
    accrued interest (2nd overload): 75,416,667
    accrued fixing (1st overload): 15.00%
    accrued fixing (2nd overload): 15.00%



```python
fixed_rate_cashflow_2.get_type()
```




    'FixedRateCashflow2'




```python
qcf.show(fixed_rate_cashflow_2)
```




    ('2018-09-20',
     '2019-09-20',
     '2019-09-23',
     1000000000.0,
     100000000.0,
     152083333.33333334,
     True,
     252083333.33333334,
     'CLP',
     0.15,
     'LinAct360')



### Ibor Cashflow
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


**TODO: agregar end_date_adjustment al objeto (FOLLOW o MOD FOLLOW).** Esto debiera tener un correspondiente cambio en la BBDD de Front Desk.


```python
# Se define el índice
codigo = "LIBORUSD3M"
lin_act360 = qcf.QCInterestRate(0.0, act360, lin_wf)
fixing_lag = qcf.Tenor("2d")
tenor = qcf.Tenor("3m")
fixing_calendar = scl  # No es el calendario correcto, pero sirve para el ejemplo
settlement_calendar = scl  # Ídem arriba
libor_usd_3m = qcf.InterestRateIndex(
    codigo, 
    lin_act360, 
    fixing_lag, 
    tenor, 
    fixing_calendar, 
    settlement_calendar, 
    usd
)

# Getters
print("Tenor:", libor_usd_3m.get_tenor())
print("Tasa:", libor_usd_3m.get_rate())
print()

# Para construir un fixing en particular
libor_usd_3m.set_rate_value(0.01)
print("Fixing Tasa:", libor_usd_3m.get_rate())
fecha_fixing = qcf.QCDate(20, 9, 2018)
print("Fecha Inicio:", libor_usd_3m.get_start_date(fecha_fixing))
print("Fecha Final:", libor_usd_3m.get_end_date(fecha_fixing))
```

    Tenor: 3M
    Tasa: 0.000000 Act360 Lin
    
    Fixing Tasa: 0.010000 Act360 Lin
    Fecha Inicio: 2018-09-24
    Fecha Final: 2018-12-24



```python
libor_usd_3m.get_code()
```




    'LIBORUSD3M'




```python
libor_usd_3m.set_rate_value(0.1)
```


```python
print(libor_usd_3m.get_rate())
```

    0.100000 Act360 Lin



```python
libor_usd_3m.get_rate()
```




    <qcfinancial.QCInterestRate at 0x1217b87b0>



Con esto, veamos un ejemplo de construcción y uso de un `IborCashflow`.

**TODO:** Se debe crear un mecanismo de WARNING para las eventuales inconsistencias entre las fechas de inicio y fin del ``InterestRateIndex`` y las fechas de inicio y fin del ``IborCashflow``.


```python
# Ejemplo
fecha_inicio = qcf.QCDate(20, 9, 2018)
fecha_final = qcf.QCDate(20, 9, 2019)
fecha_pago = qcf.QCDate(23, 9, 2019)
fecha_fixing = qcf.QCDate(20, 9, 2018)
nominal = 1_000_000.0
amort = 100_000.0
spread = 0.0
gearing = 1.0
ibor_cashflow = qcf.IborCashflow(
    libor_usd_3m,
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


```python
# Getters
print("Fecha Fixing:\t", ibor_cashflow.get_fixing_date())
print("Fecha Inicio:\t", ibor_cashflow.get_start_date())
print("Fecha Final:\t", ibor_cashflow.get_end_date())
print("Fecha Pago:\t", ibor_cashflow.get_settlement_date())
print(f"Nominal:\t{ibor_cashflow.get_nominal():,.0f}")
print(f"Amortización:\t{ibor_cashflow.get_amortization():,.0f}")
print("Moneda:\t\t", ibor_cashflow.ccy())
print(f"Valor Tasa:\t{ibor_cashflow.get_interest_rate_value():.2%}")
```

    Fecha Fixing:	 2018-09-20
    Fecha Inicio:	 2018-09-20
    Fecha Final:	 2019-09-20
    Fecha Pago:	 2019-09-23
    Nominal:	1,000,000
    Amortización:	100,000
    Moneda:		 USD
    Valor Tasa:	10.00%



```python
# Setters
nuevo_nominal = 2_000_000.0
ibor_cashflow.set_nominal(nuevo_nominal)
print(f"Nominal:\t{ibor_cashflow.get_nominal():,.0f}")

nueva_amortizacion = 200_000.0
ibor_cashflow.set_amortization(nueva_amortizacion)
print(f"Amortización:\t{ibor_cashflow.get_amortization():,.0f}")

nuevo_valor_tasa = 0.02
ibor_cashflow.set_interest_rate_value(nuevo_valor_tasa)
print(f"Valor Tasa: {ibor_cashflow.get_interest_rate_value():.2%}")
```

    Nominal:	2,000,000
    Amortización:	200,000
    Valor Tasa: 2.00%



```python
# Cálculos
print(f"Flujo: {ibor_cashflow.amount():,.0f}")

fecha_devengo = qcf.QCDate(20, 7, 2019)
print(f"Interés Devengado al {fecha_devengo}: {ibor_cashflow.accrued_interest(fecha_devengo):,.0f}")
tasa = ibor_cashflow.get_interest_rate_value()

check = tasa * fecha_inicio.day_diff(fecha_devengo) / 360.0 * ibor_cashflow.get_nominal()
print(f"Check: {check:,.0f}")
```

    Flujo: 240,556
    Interés Devengado al 2019-07-20: 33,667
    Check: 33,667



```python
# Función show
print(qcf.show(ibor_cashflow))
```

    ('2018-09-20', '2019-09-20', '2018-09-20', '2019-09-23', 2000000.0, 200000.0, 40555.55555555568, True, 240555.55555555568, 'USD', 'LIBORUSD3M', 0.02, 0.0, 1.0, 'LinAct360')


### Ibor Cashflow 2
Un objeto de tipo `IborCashflow2` representa un flujo de caja calculado a partir de la aplicación de una tasa flotante fijada en una cierta fecha (Libor, Euribor, TAB, ...) , entre dos fechas prefijadas a un nominal prefijado. Para dar de alta uno de estos objetos se requiere:

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

A diferencia de un `IborCashflow`, un `IborCashflow2` puede quantizarse.


```python
# Ejemplo
fecha_inicio = qcf.QCDate(20, 9, 2018)
fecha_final = qcf.QCDate(20, 9, 2019)
fecha_pago = qcf.QCDate(23, 9, 2019)
fecha_fixing = qcf.QCDate(20, 9, 2018)
nominal = 1000000.0
amort = 100000.0
spread = 0.0
gearing = 1.0
ibor_cashflow_2 = qcf.IborCashflow2(
    libor_usd_3m,
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


```python
# Getters
print("Fecha Fixing:\t", ibor_cashflow_2.get_fixing_dates())
print("Fecha Inicio:\t", ibor_cashflow_2.get_start_date())
print("Fecha Final:\t", ibor_cashflow_2.get_end_date())
print("Fecha Pago:\t", ibor_cashflow_2.get_settlement_date())
print(f"Nominal:\t{ibor_cashflow_2.get_nominal():,.0f}")
print(f"Amortización:\t{ibor_cashflow_2.get_amortization():,.0f}")
print("Moneda:\t\t", ibor_cashflow_2.ccy())
print(f"Valor Tasa:\t{ibor_cashflow_2.fixing():.2%}")
```

    Fecha Fixing:	 DateList[20-9-2018]
    Fecha Inicio:	 2018-09-20
    Fecha Final:	 2019-09-20
    Fecha Pago:	 2019-09-23
    Nominal:	1,000,000
    Amortización:	100,000
    Moneda:		 USD
    Valor Tasa:	2.00%



```python
# Función show
qcf.show(ibor_cashflow_2)
```




    ('2018-09-20',
     '2019-09-20',
     '2018-09-20',
     '2019-09-23',
     1000000.0,
     100000.0,
     20277.77777777784,
     True,
     120277.77777777784,
     'USD',
     'LIBORUSD3M',
     0.02,
     0.0,
     1.0,
     'LinAct360')



### Ibor Multi Currency Cashflow
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



```python
# Ejemplo
fecha_inicio = qcf.QCDate(20, 9, 2019)
fecha_final = qcf.QCDate(20, 12, 2019)
fecha_pago = qcf.QCDate(20, 12, 2019)
fecha_fixing = qcf.QCDate(20, 9, 2019)
nominal = 100.0
amort = 100.0
spread = 0.02
gearing = 1.0
valor_indice = 10.0
fecha_publicacion = qcf.QCDate(20, 9, 2019)
libor_usd_3m.set_rate_value(0.01)
ibor_mccy_cashflow = qcf.IborMultiCurrencyCashflow(
    libor_usd_3m,
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
    fecha_publicacion,
    clp,
    indice,
    valor_indice,
)
print(ibor_mccy_cashflow)
```

    <qcfinancial.IborMultiCurrencyCashflow object at 0x1217dc2b0>



```python
ibor_mccy_cashflow.set_interest_rate_value(0.01)
```


```python
print(qcf.show(ibor_mccy_cashflow))
```

    ('2019-09-20', '2019-12-20', '2019-09-20', '2019-12-20', 100.0, 100.0, 0.7583333333333275, True, 1007.5833333333333, 'USD', 'LIBORUSD3M', 0.02, 1.0, 0.01, 'LinAct360', '2019-09-20', 'CLP', 'USDOBS', 10.0, 1000.0, 7.583333333333275)



```python
fecha_intermedia = qcf.QCDate(20, 10, 2019)
print(ibor_mccy_cashflow.accrued_interest(fecha_intermedia))
print(
    (0.01 + spread)
    * fecha_inicio.day_diff(fecha_intermedia)
    / 360.0
    * ibor_mccy_cashflow.get_nominal()
)
```

    0.24999999999999467
    0.24999999999999997



```python
ts[fecha_inicio] = 1
ts[fecha_intermedia] = 3
for k in ts:
    print(k)
print(fecha_intermedia.description(False))
print(ts[fecha_intermedia])
```

    2019-09-20
    2019-10-20
    2019-10-20
    3.0



```python
print(ibor_mccy_cashflow.accrued_interest(fecha_intermedia, fecha_intermedia, ts))
```

    0.749999999999984



```python
ibor_mccy_cashflow.get_type()
```




    'IborMultiCurrencyCashflow'




```python
qcf.show(ibor_mccy_cashflow)
```




    ('2019-09-20',
     '2019-12-20',
     '2019-09-20',
     '2019-12-20',
     100.0,
     100.0,
     0.7583333333333275,
     True,
     1007.5833333333333,
     'USD',
     'LIBORUSD3M',
     0.02,
     1.0,
     0.01,
     'LinAct360',
     '2019-09-20',
     'CLP',
     'USDOBS',
     10.0,
     1000.0,
     7.583333333333275)



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



### Overnight Index Cashflow
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


```python
# Ejemplo
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
valor_indice_final = 1 + .1234 * 4 / 360 # Suponemos un valor constante de 10% por 4 días del índice
```


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
)
```

#### Getters


```python
print("Fecha Inicio Devengo:", overnight_index_cashflow.get_start_date())
print("Fecha Final Devengo:", overnight_index_cashflow.get_end_date())

print("Fecha Inicio Índice:", overnight_index_cashflow.get_index_start_date())
print("Fecha Final Índice:", overnight_index_cashflow.get_index_end_date())

print("Fecha Pago:", overnight_index_cashflow.get_settlement_date())


print(f"Índice Fecha Inicio: {overnight_index_cashflow.get_start_date_index():,.8f}")
print(f"ïndice Fecha Final: {overnight_index_cashflow.get_end_date_index():,.8f}")

print()
print(f"Valor Tasa Equivalente Todo el Período: {overnight_index_cashflow.get_rate_value():.6%}")
check = round((
    valor_indice_final / valor_indice_inicio - 1
) * 360.0 / fecha_inicio_devengo.day_diff(fecha_final_devengo), num_decimales)
print(f"Check: {check:.6%}")
print()

print(f"Nominal: {overnight_index_cashflow.get_nominal():,.0f}")
print(f"Amortización: {overnight_index_cashflow.get_amortization():,.0f}")
print("Tipo de Tasa:", overnight_index_cashflow.get_type_of_rate())
print("Moneda:", overnight_index_cashflow.ccy())
```

    Fecha Inicio Devengo: 2023-11-13
    Fecha Final Devengo: 2023-11-18
    Fecha Inicio Índice: 2023-11-13
    Fecha Final Índice: 2023-11-17
    Fecha Pago: 2023-11-20
    Índice Fecha Inicio: 10,000.00000000
    ïndice Fecha Final: 10,010.00000000
    
    Valor Tasa Equivalente Todo el Período: 7.200000%
    Check: 9.872000%
    
    Nominal: 1,000,000,000
    Amortización: 100,000
    Tipo de Tasa: LinAct360
    Moneda: USD


#### Setters


```python
decimales_para_tasa_eq = 4
overnight_index_cashflow.set_eq_rate_decimal_places(decimales_para_tasa_eq)
print(f"Nueva Tasa Eq: {overnight_index_cashflow.get_rate_value():.4%}")
```

    Nueva Tasa Eq: 7.2000%



```python
new_notional = 123_456
overnight_index_cashflow.set_nominal(new_notional)
print(f"Nuevo Nocional: {overnight_index_cashflow.get_nominal():,.2f}")
```

    Nuevo Nocional: 123,456.00



```python
new_amortization = 100_000
overnight_index_cashflow.set_amortization(new_amortization)
print(f"Nueva Amortización: {overnight_index_cashflow.get_amortization():,.2f}")
```

    Nueva Amortización: 100,000.00



```python
nuevo_indice_inicio = 20_000.0
overnight_index_cashflow.set_start_date_index(nuevo_indice_inicio)
print(f"Nuevo Índice Inicio: {overnight_index_cashflow.get_start_date_index():,.2f}")
```

    Nuevo Índice Inicio: 20,000.00



```python
nuevo_indice_final = 20_010.0
overnight_index_cashflow.set_end_date_index(nuevo_indice_final)
print(f"Nuevo Índice Final: {overnight_index_cashflow.get_end_date_index():,.2f}")
print(f"Check Tas Eq. Final: {overnight_index_cashflow.get_rate_value():.4%}")
```

    Nuevo Índice Final: 20,010.00
    Check Tas Eq. Final: 3.6000%


#### Cálculos


```python
decimales_para_tasa = 8  # Se vuelve a 8 decimales de tasa
overnight_index_cashflow.set_eq_rate_decimal_places(decimales_para_tasa)

nuevo_indice_inicio = 10_000.0
overnight_index_cashflow.set_start_date_index(nuevo_indice_inicio)

nuevo_indice_final = 10_010.0
overnight_index_cashflow.set_end_date_index(nuevo_indice_final)

print(f"Flujo: {overnight_index_cashflow.amount():,.2f}")
print()
```

    Flujo: 100,123.46



```python
fecha_devengo = qcf.QCDate(16, 11, 2023)
indice_devengo = 10_005.0
tasa_devengo = overnight_index_cashflow.get_eq_rate(fecha_devengo, indice_devengo)
print(f"Tasa Eq. fijada al {fecha_devengo.description(True)}: {tasa_devengo:.2%}")
check = round((
    indice_devengo / nuevo_indice_inicio - 1
) * 360.0 / fecha_inicio_devengo.day_diff(fecha_devengo), decimales_para_tasa)
print(f"Check: {check:.2%}")
print()
```

    Tasa Eq. fijada al 16-11-2023: 6.00%
    Check: 6.00%



```python
data = qcf.time_series()
data[fecha_devengo] = indice_devengo
print(
    f"Interés Devengado al {fecha_devengo.description(True)}: {overnight_index_cashflow.accrued_interest(fecha_devengo, data):,.6f}")
check = new_notional * tasa_devengo * fecha_inicio_devengo.day_diff(fecha_devengo) / 360.0
print(f"Check: {check:,.6f}")
```

    Interés Devengado al 16-11-2023: 61.728000
    Check: 61.728000



```python
overnight_index_cashflow.get_type()
```




    'OvernightIndexCashflow'



#### Show


```python
data = [qcf.show(overnight_index_cashflow)]
pd.DataFrame(data, columns = qcf.get_column_names("OvernightIndexCashflow", ""))
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
      <th>fecha_inicial_devengo</th>
      <th>fecha_final_devengo</th>
      <th>fecha_inicial_indice</th>
      <th>fecha_final_indice</th>
      <th>fecha_pago</th>
      <th>nocional</th>
      <th>amortizacion</th>
      <th>amort_es_flujo</th>
      <th>moneda_nocional</th>
      <th>nombre_indice</th>
      <th>valor_indice_inicial</th>
      <th>valor_indice_final</th>
      <th>valor_tasa_equivalente</th>
      <th>tipo_tasa</th>
      <th>interes</th>
      <th>flujo</th>
      <th>spread</th>
      <th>gearing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2023-11-13</td>
      <td>2023-11-18</td>
      <td>2023-11-13</td>
      <td>2023-11-17</td>
      <td>2023-11-20</td>
      <td>123456.0</td>
      <td>100000.0</td>
      <td>True</td>
      <td>USD</td>
      <td>INDICE</td>
      <td>10000.0</td>
      <td>10010.0</td>
      <td>0.072</td>
      <td>LinAct360</td>
      <td>123.456</td>
      <td>100123.456</td>
      <td>0.0</td>
      <td>1.0</td>
    </tr>
  </tbody>
</table>
</div>



### Overnight Index Multi Currency Cashflow

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
---
Hasta acá son los mismos argumentos necesarios para construir un `OvernightIndexCAshflow`. Se añaden los siguientes argumentos:
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
valor_indice_final = 1 + .1234 * 4 / 360 # Suponemos un valor constante de 10% por 4 días del índice

# -------------------------------
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
    fecha_fixing_fx_index,
    moneda_pago,
    indice_fx,
)
```


```python
type(overnight_index_mccy_cashflow)
```




    qcfinancial.OvernightIndexMultiCurrencyCashflow



#### Función `show` 


```python
qcf.show(overnight_index_mccy_cashflow)
```




    ('2023-11-13',
     '2023-11-18',
     '2023-11-13',
     '2023-11-17',
     '2023-11-20',
     1000000000.0,
     100000000.0,
     True,
     'USD',
     'INDICE',
     1.0,
     1.0,
     0.0,
     'LinAct360',
     0.0,
     100000000.0,
     0.0,
     1.0,
     'CLP',
     'USDOBS',
     '2023-11-18',
     1.0,
     0.0,
     100000000.0,
     100000000.0)



Se envuelve el resultado en un `pd.DataFrame`.


```python
pd.DataFrame(
    [qcf.show(overnight_index_mccy_cashflow),],
    columns=qcf.get_column_names("OvernightIndexMultiCurrencyCashflow", "")
)
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
      <th>fecha_inicial_devengo</th>
      <th>fecha_final_devengo</th>
      <th>fecha_inicial_indice</th>
      <th>fecha_final_indice</th>
      <th>fecha_pago</th>
      <th>nocional</th>
      <th>amortizacion</th>
      <th>amort_es_flujo</th>
      <th>moneda_nocional</th>
      <th>nombre_indice</th>
      <th>...</th>
      <th>flujo</th>
      <th>spread</th>
      <th>gearing</th>
      <th>moneda_pago</th>
      <th>indice_fx</th>
      <th>fecha_fijacion_indice_fx</th>
      <th>valor_indice_fx</th>
      <th>interes_moneda_pago</th>
      <th>amortizacion_moneda_pago</th>
      <th>flujo_moneda_pago</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2023-11-13</td>
      <td>2023-11-18</td>
      <td>2023-11-13</td>
      <td>2023-11-17</td>
      <td>2023-11-20</td>
      <td>1.000000e+09</td>
      <td>100000000.0</td>
      <td>True</td>
      <td>USD</td>
      <td>INDICE</td>
      <td>...</td>
      <td>100000000.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>CLP</td>
      <td>USDOBS</td>
      <td>2023-11-18</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>100000000.0</td>
      <td>100000000.0</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 25 columns</p>
</div>



#### Nuevo Setter

Valor del índice de tipo de cambio.


```python
overnight_index_mccy_cashflow.set_fx_rate_index_value(.5)
```

Ver el efecto en las últimas dos columnas.


```python
pd.DataFrame(
    [qcf.show(overnight_index_mccy_cashflow),],
    columns=qcf.get_column_names("OvernightIndexMultiCurrencyCashflow", "")
)
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
      <th>fecha_inicial_devengo</th>
      <th>fecha_final_devengo</th>
      <th>fecha_inicial_indice</th>
      <th>fecha_final_indice</th>
      <th>fecha_pago</th>
      <th>nocional</th>
      <th>amortizacion</th>
      <th>amort_es_flujo</th>
      <th>moneda_nocional</th>
      <th>nombre_indice</th>
      <th>...</th>
      <th>flujo</th>
      <th>spread</th>
      <th>gearing</th>
      <th>moneda_pago</th>
      <th>indice_fx</th>
      <th>fecha_fijacion_indice_fx</th>
      <th>valor_indice_fx</th>
      <th>interes_moneda_pago</th>
      <th>amortizacion_moneda_pago</th>
      <th>flujo_moneda_pago</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2023-11-13</td>
      <td>2023-11-18</td>
      <td>2023-11-13</td>
      <td>2023-11-17</td>
      <td>2023-11-20</td>
      <td>1.000000e+09</td>
      <td>100000000.0</td>
      <td>True</td>
      <td>USD</td>
      <td>INDICE</td>
      <td>...</td>
      <td>100000000.0</td>
      <td>0.0</td>
      <td>1.0</td>
      <td>CLP</td>
      <td>USDOBS</td>
      <td>2023-11-18</td>
      <td>0.5</td>
      <td>0.0</td>
      <td>50000000.0</td>
      <td>50000000.0</td>
    </tr>
  </tbody>
</table>
<p>1 rows × 25 columns</p>
</div>



#### Nuevos Getters


```python
overnight_index_mccy_cashflow.get_fx_rate_index()
```




    <qcfinancial.FXRateIndex at 0x108e613b0>




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




    0.5



#### Nuevos Cálculos

Primero se fijan los valores del índice overnight.


```python
overnight_index_mccy_cashflow.set_start_date_index(100)
overnight_index_mccy_cashflow.accrued_interest(fecha_final_devengo, 102)
```




    20000000.00000002




```python
overnight_index_mccy_cashflow.settlement_ccy_interest()
```




    -495000000.0




```python
overnight_index_mccy_cashflow.settlement_ccy_amortization()
```




    50000000.0




```python
overnight_index_mccy_cashflow.settlement_ccy_amount()
```




    -445000000.0



### Icp Clf Cashflow
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


```python
# Ejemplo
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


```python
# Getters
print("Fecha Inicio:", icp_clf_cashflow.get_start_date())
print("Fecha Final:", icp_clf_cashflow.get_end_date())

print(f"ICP Fecha Inicio: {icp_clf_cashflow.get_start_date_icp():,.2f}")
print(f"ICP Fecha Final: {icp_clf_cashflow.get_end_date_icp():,.2f}")

print(f"UF Fecha Inicio: {icp_clf_cashflow.get_start_date_uf():,.2f}")
print(f"UF Fecha Final: {icp_clf_cashflow.get_end_date_uf():,.2f}")

print(f"Valor TRA Todo el Período: {icp_clf_cashflow.get_rate_value():.4%}")
tna = icp_clf_cashflow.get_tna(fecha_final, 10_250.0)
dias = fecha_inicio.day_diff(fecha_final)
tra = ((1 + tna * dias / 360.0) * 35_000.0 / 35_500.0 - 1) * 360.0 / dias
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



```python
# Setters
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



```python
icp_clf_cashflow.get_type()
```




    'IcpClfCashflow'




```python
qcf.show(icp_clf_cashflow)
```




    ('2018-09-20',
     '2019-09-20',
     '2019-09-23',
     100000.0,
     10000.0,
     True,
     11056.338028169024,
     'CLF',
     20000.0,
     20500.0,
     35000.0,
     35500.0,
     0.01046054,
     1060.582527777787,
     0.0,
     1.0,
     'LinAct360')



### Compounded Overnight Rate Cashflow

Un objeto de tipo `CompoundedOvernightRateCashflow` representa un flujo de caja calculado como un cupón de la pata flotante de un OIS sobre cualquier índice overnight (SOFR, FF, EONIA). Para dar de alta uno de estos objetos se requiere:

- `InterestRateIndex`: el índice de tasa de interés prefijado
- `QCDate`: fecha inicio (para la aplicación de la tasa)
- `QCDate`: fecha final (para la aplicación de la tasa)
- `QCDate`: fecha de pago
- `DateList`: fechas de fixing del índice
- `float`: nominal (monto al que se le aplica la tasa)
- `float`: amortización (eventual flujo de caja que corresponde a una porción del nominal)
- `bool`: indica si la amortización anterior es un flujo de caja o sólo una disminución de nominal
- `QCCurrency`: moneda del nocional de la operación
- `float`: spread aditivo a aplicar a la fijación de la TRA
- `float`: spread multiplicativo o gearing a aplicar a la fijación de la TRA
- `bool`: si `True` la tasa equivalente se calcula en convención Lin Act/360. En caso contrario es Lin 30/360
- `unsigned int`: número de decimales a usar en el cálculo de la tasa equivalente. Por ejemplo para 0.12345678% este valor debe ser 10.
- `unsigned int`: número de días de lookback
- `unsigned int`: número de días de lockout

El efecto de lookback y lockout aún no está implementado.

#### Constructor

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


```python
fixing_dates = qcf.DateList()
```


```python
fixing_dates.append(qcf.QCDate(27, 12, 2021))
fixing_dates.append(qcf.QCDate(28, 12, 2021))
fixing_dates.append(qcf.QCDate(29, 12, 2021))
fixing_dates.append(qcf.QCDate(30, 12, 2021))
```


```python
cor_cashflow = qcf.CompoundedOvernightRateCashflow(
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
    True,
    8,
    0,
    0,
)
```

#### Getters


```python
cor_cashflow.get_start_date().description(False)
```




    '2021-12-27'




```python
cor_cashflow.get_end_date().description(False)
```




    '2021-12-31'




```python
cor_cashflow.get_settlement_date().description(False)
```




    '2021-12-31'




```python
for d in cor_cashflow.get_fixing_dates():
    print(d)
```

    2021-12-27
    2021-12-28
    2021-12-29
    2021-12-30



```python
print(f"Nominal: {cor_cashflow.get_nominal():,.0f}")
```

    Nominal: 10,000,000



```python
print(f"Amortization: {cor_cashflow.get_amortization():,.0f}")
```

    Amortization: 100,000



```python
cor_cashflow.get_initial_currency().get_iso_code()
```




    'CLP'




```python
print(f"Spread: {cor_cashflow.get_spread():.2%}")
```

    Spread: 0.10%



```python
cor_cashflow.get_gearing()
```




    1.0




```python
cor_cashflow.get_type()
```




    'CompoundedOvernightRateCashflow'




```python
cor_cashflow.get_eq_rate_decimal_places()
```




    8




```python
derivs = cor_cashflow.get_amount_derivatives()
```


```python
len(derivs)
```




    2




```python
for der in derivs:
    print(der)
```

    0.0
    0.0


#### Setters


```python
cor_cashflow.set_nominal(1_000)
print(f"Nominal: {cor_cashflow.get_nominal():,.0f}")
```

    Nominal: 1,000



```python
cor_cashflow.set_amortization(0)
cor_cashflow.get_amortization()
```




    0.0



Se reversa el ejemplo.


```python
cor_cashflow.set_nominal(10_000_000.0)
cor_cashflow.set_amortization(100_000.0)
```

#### Accrued Fixing

Para el cálculo de `accrued_fixing` se requiere un objeto de tipo `TimeSeries` que contenga los datos históricos del índice overnight.


```python
cor_cashflow.accrued_fixing(qcf.QCDate(29, 12, 2021))
```


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    Cell In[243], line 1
    ----> 1 cor_cashflow.accrued_fixing(qcf.QCDate(29, 12, 2021))


    ValueError: A TimeSeries object with overnight rate values is needed.



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
print(f"Accrued fixing: {cor_cashflow.accrued_fixing(qcf.QCDate(29, 12, 2021), ts):.6%}")
```

    Accrued fixing: 1.500028%



```python
check = ((1 + 0.01 / 360) * (1 + 0.02 / 360.0) - 1) * 360 / 2.0
print(f"Check: {check:.6%}")
```

    Check: 1.500028%


#### Accrued Interest

Para el cálculo de `accrued_interest` se requiere un objeto de tipo `TimeSeries` que contenga los datos históricos del índice overnight.


```python
cor_cashflow.accrued_interest(qcf.QCDate(29, 12, 2021))
```


    ---------------------------------------------------------------------------

    ValueError                                Traceback (most recent call last)

    Cell In[248], line 1
    ----> 1 cor_cashflow.accrued_interest(qcf.QCDate(29, 12, 2021))


    ValueError: A TimeSeries object with overnight rate values is needed.



```python
print(f"Accrued interest: {cor_cashflow.accrued_interest(qcf.QCDate(29, 12, 2021), ts):,.2f}")
```

    Accrued interest: 888.90



```python
check = (
    cor_cashflow.get_nominal()
    * (cor_cashflow.accrued_fixing(qcf.QCDate(29, 12, 2021), ts) + spread)
    * 2
    / 360.0
)
print(f"Check: {check:,.2f}")
```

    Check: 888.90



```python
print(f"Amount: {cor_cashflow.amount():,.2f}")
```

    Amount: 100,111.11



```python
cor_cashflow.date().description(False)
```




    '2021-12-31'




```python
print(f"Interest: {cor_cashflow.interest():,.2f}")
```

    Interest: 111.11



```python
cor_cashflow.is_expired(qcf.QCDate(29, 12, 2021))
```




    False




```python
cor_cashflow.is_expired(qcf.QCDate(31, 12, 2021))
```




    True




```python
cor_cashflow.is_expired(qcf.QCDate(1, 1, 2022))
```




    True




```python
cor_cashflow.get_type()
```




    'CompoundedOvernightRateCashflow'




```python
qcf.show(cor_cashflow)
```




    ('2021-12-27',
     '2021-12-31',
     '2021-12-31',
     10000000.0,
     100000.0,
     888.9044444448934,
     True,
     100111.11111111184,
     'CLP',
     'OITEST',
     0.0,
     0.001,
     1.0,
     'LinAct360')


