# Objetos Fundamentales

Para ejecutar todos los ejemplos se debe importar la librería. Se sugiere utilizar siempre el alias `qcf`. 


```python
import qcfinancial as qcf
```

## Monedas

Las divisas se representan con objetos de tipo `QCCurrency` y sus subclases. En estos momentos, de forma explícita, están implementadas las siguientes divisas:


```python
for fx in qcf.QCCurrencyEnum.__dict__['__entries']:
    print(fx)
```

    AUD
    BRL
    CAD
    CHF
    CLF
    CL2
    CLP
    CNY
    COP
    DKK
    EUR
    GBP
    HKD
    JPY
    MXN
    NOK
    PEN
    SEK
    USD


Si se requiere otra, solicitarlo ingresando un *issue* en el [git repo](https://github.com/qcfinancial/qcfinancial.git) del proyecto.

Nota: La divisa `CL2` corresponde a CLF, pero usando solamente dos decimales.

El constructor por default retorna USD.


```python
x = qcf.QCCurrency()
print(f"ISO Code: {x.get_iso_code()}")
```

    ISO Code: USD


Alta de divisas CLP, USD y JPY (USD se puede instanciar también de forma explícita).


```python
monedas = [
    clp:=qcf.QCCLP(),
    usd:=qcf.QCUSD(),
    jpy:=qcf.QCJPY(),
]
```

Sin usar las subclases se puede instanciar una divisa que no esté implementada, por ejemplo para el peso argentino ARS:


```python
ars = qcf.QCCurrency('Peso argentino', 'ARS', 32, 0)
monedas.append(ars)
```

### Métodos: `get_name`, `get_iso_code`, `get_iso_number`, `get_decimal_places` y `amount`.

El método `amount`debe utilizarse cuando se debe pagar o recibir un monto resultado de un cálculo. De esta forma, el monto se redondea al número correcto de decimales en la divisa (que se obtiene con `get_decimal_places`). Por ejemplo, en CLP, se redondea a 0 decimales ya que en esta divisa no se utilizan los centavos.


```python
cantidad = 100.123456
for moneda in monedas:
    print(f"Nombre: {format(moneda.get_name())}")
    print(f"Código ISO: {moneda.get_iso_code()}")
    print(f"Número ISO: {moneda.get_iso_number()}")
    print(f"Número de decimales: {moneda.get_decimal_places()}")
    print(f"Cantidad {cantidad} con el número correcto de decimales: {moneda.amount(cantidad):.4f}")
    print()
```

    Nombre: Chilean Peso
    Código ISO: CLP
    Número ISO: 152
    Número de decimales: 0
    Cantidad 100.123456 con el número correcto de decimales: 100.0000
    
    Nombre: U. S. Dollar
    Código ISO: USD
    Número ISO: 840
    Número de decimales: 2
    Cantidad 100.123456 con el número correcto de decimales: 100.1200
    
    Nombre: Japanese Yen
    Código ISO: JPY
    Número ISO: 392
    Número de decimales: 2
    Cantidad 100.123456 con el número correcto de decimales: 100.1200
    
    Nombre: Peso argentino
    Código ISO: ARS
    Número ISO: 32
    Número de decimales: 0
    Cantidad 100.123456 con el número correcto de decimales: 100.0000
    


Más adelante, cuando veamos el concepto de índice, veremos como disponer de un objeto moneda simplifica la conversión de montos de una moneda a otra.

## Fechas

Las fechas se representan con objetos de tipo `QCDate`. Para inicializar un `QCDate` se requiere el día, el mes y el año de la fecha. También se puede inicializar sin valor (default constructor) en cuyo caso se obtendrá el 12-01-1969.

### Constructores

Inicializar sin valor.


```python
fecha = qcf.QCDate()
print(f"Fecha: {fecha}")
```

    Fecha: 1969-01-12


Inicializar con una fecha específica. En este caso, el contructor realiza una validación de los parámetros iniciales.


```python
fecha1 = qcf.QCDate(14, 9, 2024)  # día, mes, año
print(f"Fecha: {fecha1}")
```

    Fecha: 2024-09-14


Error al tratar de construir una fecha inválida.


```python
try:
    fecha0 = qcf.QCDate(31, 2, 2024)  # ¡¡¡ 31 de febrero !!!
except ValueError as e:
    print(e)
```

    Invalid day for month = 2


### Métodos `description`, `iso_code` y `__str__`


```python
print(f"description(True): {fecha.description(True)}")
print(f"description(False): {fecha.description(False)}")
print(f"iso_code(): {fecha.iso_code()}")
print(f"__str__: {fecha}")
```

    description(True): 12-01-1969
    description(False): 1969-01-12
    iso_code(): 1969-01-12
    __str__: 1969-01-12


### Getters y Setters

Métodos: `set_day`, `set_month` y `set_year`.


```python
fecha1.set_day(17)
fecha1.set_month(10)
fecha1.set_year(2024)
print(f"Fecha: {fecha1}")
```

    Fecha: 2024-10-17


Métodos `day`, `month` y `year`.


```python
print(f"Día: {fecha1.day()}")
print(f"Mes: {fecha1.month()}")
print(f"Año: {fecha1.year()}")
```

    Día: 17
    Mes: 10
    Año: 2024


### Método `week_day`

Retorna una variable de tipo `enum QC_Financial.WeekDay` que representa el día de la semana al que corresponde a la fecha.


```python
dia_semana = fecha1.week_day()
print(f"Tipo del retorno: {type(dia_semana)}")
print(f"Día de la semana: {dia_semana}")
```

    Tipo del retorno: <class 'qcfinancial.WeekDay'>
    Día de la semana: WeekDay.THU


### Método `add_months`

Suma **n meses** a `fecha1` y retorna esa nueva fecha sin cambiar el valor de `fecha1`.


```python
num_meses = 12
fecha2 = fecha1.add_months(num_meses)
print(f"fecha1: {fecha1}")
print(f"fecha2: {fecha2}")
```

    fecha1: 2024-10-17
    fecha2: 2025-10-17


### Método `add_days`

Suma **n días** a `fecha1` sin cambiar el valor de `fecha1`.


```python
num_dias = 30
fecha3 = fecha1.add_days(num_dias)
print(f"fecha1: {fecha1}")
print(f"fecha3: {fecha3}")
```

    fecha1: 2024-10-17
    fecha3: 2024-11-16


### Método `day_diff`

Calcula la diferencia en días con otra fecha. Si la otra fecha es mayor el resultado es positivo, si no, es negativo.


```python
# Dado que fecha3 > fecha1 entonces el resultado es positivo
print(f"fecha1.day_diff(fecha3): {fecha1.day_diff(fecha3)} (días)")

# Se invierten los roles y el resultado es negativo
print(f"fecha3.day_diff(fecha1): {fecha3.day_diff(fecha1)} (días)")
```

    fecha1.day_diff(fecha3): 30 (días)
    fecha3.day_diff(fecha1): -30 (días)


### Orden en `QCDate`

El orden de `QCDate` permite que las fechas pueden compararse entre si.


```python
print(f"fecha1: {fecha1}")
print(f"fecha2: {fecha2}")
print(f"fecha1 == fecha2: {fecha1 == fecha2}")
print(f"fecha1 != fecha2: {fecha1 != fecha2}")
print(f"fecha1 < fecha2: {fecha1 < fecha2}")
print(f"fecha1 <= fecha2: {fecha1 <= fecha2}")
print(f"fecha1 > fecha2: {fecha1 > fecha2}")
print(f"fecha1 >= fecha2: {fecha1 >= fecha2}")
```

    fecha1: 2024-10-17
    fecha2: 2025-10-17
    fecha1 == fecha2: False
    fecha1 != fecha2: True
    fecha1 < fecha2: True
    fecha1 <= fecha2: True
    fecha1 > fecha2: False
    fecha1 >= fecha2: False


### Un objeto `QCDate` es *hashable*

Esto permite que las fechas puedan usarse como `key` en un `dict`de Python. El hash que se utiliza coincide con la representación como entero de una fecha que se utiliza en Excel.


```python
print(fecha1.__hash__())
```

    45582


Por ejemplo, una serie de tiempo:


```python
serie_de_tiempo = {
    qcf.QCDate(22, 5, 2024): 100.01,
    qcf.QCDate(23, 5, 2024): 100.02,
    qcf.QCDate(24, 5, 2024): 100.03,
}
print(f"Valor al: {qcf.QCDate(23, 5, 2024)} es {serie_de_tiempo[qcf.QCDate(23, 5, 2024)]}")
```

    Valor al: 2024-05-23 es 100.02


### Método `build_qcdate_from_string`

Se trata de un *factory method* que permite inicializar un objeto `QCDate` a partir de un `string`.
El formato del `string` debe ser yyyy&mm&dd donde & es un separador arbitrario.


```python
str1 = "2020-01-01"
str2 = "2020/01/02"
str3 = "2020&01&03"

fecha4 = qcf.build_qcdate_from_string(str1)
print(f"{str1}: {fecha4}")

fecha4 = qcf.build_qcdate_from_string(str2)
print(f"{str2}: {fecha4}")

fecha4 = qcf.build_qcdate_from_string(str3)
print(f"{str3}: {fecha4}")
```

    2020-01-01: 2020-01-01
    2020/01/02: 2020-01-02
    2020&01&03: 2020-01-03


## Calendarios

Para construir correctamente la tabla de desarrollo de un bono o de las patas de un swap, es necesario conocer los calendarios que se debe aplicar en cada caso. 

Sólo así es posible determinar qué fechas de pago, de inicio y fin de devengo y otras son admisibles.

Los calendarios se representan con objetos de tipo `BusinesssCalendar` y son **listas** de fechas arbitrarias que representan días feriados en alguna ciudad, país, región o unión de las anteriores. 

Para dar de alta un calendario se requiere:

- una fecha inicial (`QCDate`)
- y un número entero positivo que representa el plazo inicial total del calendario en años.

El objeto `BusinessCalendar` incluye explícitamente todos los días 1 de enero y considera siempre como feriado los días sábado y domingo (aunque no pertenecen de forma explícita a la **lista**).

En el siguiente loop, por ejemplo, no se imprime nada.


```python
fecha_inicio_calendario = qcf.QCDate(1, 1, 2024)
scl = qcf.BusinessCalendar(fecha1, 10)
```


```python
for holiday in scl.get_holidays():
    print(holiday)
```

### Método `add_holiday`

Agrega una fecha a la lista.


```python
scl.add_holiday(qcf.QCDate(18, 9, 2024))
```


```python
for holiday in scl.get_holidays():
    print(holiday)
```

    2024-09-18


### Método `next_busy_day`

Dada una fecha, si ésta es hábil retorna la misma fecha, si, por el contrario, la fecha es inhábil, devuelve la siguiente fecha hábil del calendario.

Veamos qué ocurre si aplicamos este método al 18-09-2024, fecha que acabamos de incluir.


```python
print(f"Next para el {(sept18 := qcf.QCDate(18, 9, 2024))}: {scl.next_busy_day(sept18)}")
```

    Next para el 2024-09-18: 2024-09-19


Agregamos ahora el 19-09-2024 y vemos el nuevo resultado.


```python
print("Se agrega el 19-9-2024 a la lista")
scl.add_holiday(qcf.QCDate(19, 9, 2024))
next = scl.next_busy_day(qcf.QCDate(18, 9, 2024))
print(f"Nuevo next para el {sept18}: {next.week_day()}, {next}")
```

    Se agrega el 19-9-2024 a la lista
    Nuevo next para el 2024-09-18: WeekDay.FRI, 2024-09-20


Pero el 2024, el 20 de septiembre también es feriado. Incluyámoslo y veamos el efecto.


```python
print("Se agrega el 20-9-2024 a la lista")
scl.add_holiday(qcf.QCDate(20, 9, 2024))
next = scl.next_busy_day(qcf.QCDate(18, 9, 2024))
print(f"Nuevo next para el {sept18}: {next.week_day()}, {next}")
```

    Se agrega el 20-9-2024 a la lista
    Nuevo next para el 2024-09-18: WeekDay.MON, 2024-09-23


### Método `mod_next_busy_day`

Opera igual que la función anterior a menos que ésta retorne una fecha del mes siguiente, en ese caso retorna la fecha hábil anterior.

Probemos el comportamiento usando el 30-04-2024.


```python
abril30 = qcf.QCDate(30, 4, 2024)
print(f"Abril 30: {abril30.week_day()}, {abril30}")
```

    Abril 30: WeekDay.TUE, 2024-04-30


Vemos que es un martes y no es feriado, por lo tanto al aplicar `next_busy_day` no hay cambio de fecha:


```python
print(f"Next para el {abril30}: {scl.next_busy_day(abril30)}")
```

    Next para el 2024-04-30: 2024-04-30


Ahora, si lo agregamos al calendario, sí se produce el cambio de fecha.


```python
scl.add_holiday(abril30)
print(f"Next para el {abril30}: {scl.next_busy_day(abril30)}")
```

    Next para el 2024-04-30: 2024-05-01


Y vemos además que nos cambiamos de mes, pero si aplicamos `mod_next_busy_day` vemos que el resultado es el día hábil anterior.


```python
print(f"Mod next para el {abril30}: {scl.mod_next_busy_day(abril30)}")
```

    Mod next para el 2024-04-30: 2024-04-29


### Método `prev_busy_day`

Opera de forma análoga a `busy_day`, pero retornando la fecha hábil anterior.


```python
print("prev:", scl.prev_busy_day(abril30))
```

    prev: 2024-04-29


### Método `shift`

Suma un número *n* (positivo o negativo) de días hábiles a una fecha.

Veamos algunos ejemplos.


```python
print(f"Fecha inicial: {abril30}")
shifted = scl.shift(abril30, 0)
print(f"n = 0, {shifted.week_day()}, {shifted}")

shifted = scl.shift(abril30, 1)
print(f"n = 1, {shifted.week_day()}, {shifted}")

shifted = scl.shift(abril30, 5)
print(f"n = 5, {shifted.week_day()}, {shifted}")
```

    Fecha inicial: 2024-04-30
    n = 0, WeekDay.TUE, 2024-04-30
    n = 1, WeekDay.WED, 2024-05-01
    n = 5, WeekDay.TUE, 2024-05-07


Veamos en particular qué ocurre cuando usamos un número negativo.


```python
mayo2 = qcf.QCDate(2, 5, 2024)
print(f"n = -1: {scl.shift(mayo2, -1)}")
```

    n = -1: 2024-05-01


Agreguemos el 2024-05-01 a los feriados de `scl` y veamos cómo cambia el primer resultado.


```python
scl.add_holiday(qcf.QCDate(1, 5, 2024))
print(f"n = -1: {scl.shift(mayo2, -1)}")
```

    n = -1: 2024-04-29


Se va al 29 de abril porque también agregamos como feriado el 30 de abril.

### Integración con `holidays`

`holidays` es una muy buena librería en Python puro que provee los feriados de más de 100 países, ciudades y mercados. Cuando no se está conectado a una BBDD y se quiere dar de alta un calendario, integrar `holidays` con `qcf.BusinessCalendar` es una muy buena opción.

En el siguiente ejemplo, se construye el calendario de Santiago.


```python
import holidays as hol
```


```python
scl = us_holidays = hol.CL(years=range(2024, 2045))
```

Vemos que `scl` es un objeto similar a un Python `dict`.


```python
for i, d in enumerate(scl.items()):
    if i < 10:
        print(d[0], d[1])
```

    2024-01-01 New Year's Day
    2024-03-29 Good Friday
    2024-03-30 Holy Saturday
    2024-05-01 Labor Day
    2024-05-21 Navy Day
    2024-06-20 National Day of Indigenous Peoples
    2024-06-29 Saint Peter and Saint Paul's Day
    2024-07-16 Our Lady of Mount Carmel
    2024-08-15 Assumption Day
    2024-09-18 Independence Day


Damos de alta un objeto de tipo `qcf.BusinessCalendar`.


```python
qcf_scl = qcf.BusinessCalendar(qcf.QCDate(1, 2, 2024), 20)
```

Y luego lo poblamos con las fechas de `scl`.


```python
for d in scl.keys():
    qcf_scl.add_holiday(qcf.QCDate(d.isoformat()))
```

Este procedimiento puede encapsularse fácilmente en una función, de hecho, la agregaremos al módulo `aux_functions` para seguir utilizándola más adelante.


```python
def get_business_calendar(which_holidays: str, years: range) -> qcf.BusinessCalendar:
    py_cal = hol.country_holidays(which_holidays, years=years)
    yrs = [y for y in years]
    qcf_cal = qcf.BusinessCalendar(qcf.QCDate(1, 1, yrs[0]), yrs[-1] - yrs[0])
    for d in py_cal.keys():
        qcf_cal.add_holiday(qcf.QCDate(d.isoformat()))
    return qcf_cal
```

Ejemplo:


```python
ny = get_business_calendar('US', range(2024, 2045))
```


```python
for i, d in enumerate(ny.get_holidays()):
    if i < 10:
        print(d)
```

    2024-01-01
    2024-01-15
    2024-02-19
    2024-05-27
    2024-06-19
    2024-07-04
    2024-09-02
    2024-10-14
    2024-11-11
    2024-11-28


## Fracciones de Año

Las fracciones de año corresponden a las distintas formas de medir un intervalo de tiempo entre dos fechas que comúnmente se utiliza en los productos de tasa de interés.

En `qcfinancial` están definidas las más utilizadas.


```python
yfs = [
    act360 := qcf.QCAct360(),
    act365 := qcf.QCAct365(),
    act30 := qcf.QCAct30(),
    t30360 := qcf.QC30360(),
    t3030 := qcf.QC3030(),
    
    # Corresponde a depósitos a plazo en CLP
    act30 := qcf.QCAct30(),

    # La utilizan los bonos del tesoro americano
    actact := qcf.QCActAct(),
]
```

### Métodos `yf` y `count_days`

El método `yf`, que retorna el valor de la fracción de año, está sobrecargado, se puede calcular usando como argumentos un número de días o un par de fechas (`QCDate`).


```python
print(f"\nfecha1: {fecha1} y fecha3: {fecha3}")
print("---------------------------------------\n")
for yf in yfs:
    print(type(yf))
    print(f"yf(30): {yf.yf(30):.6f}")
    print(f"yf.yf(fecha1, fecha3): {yf.yf(fecha1, fecha3):.6f}")
    print(f"yf.yf.count_days(fecha1, fecha3): {yf.count_days(fecha1, fecha3):.0f}")
    print()
```

    
    fecha1: 2024-10-17 y fecha3: 2024-11-16
    ---------------------------------------
    
    <class 'qcfinancial.QCAct360'>
    yf(30): 0.083333
    yf.yf(fecha1, fecha3): 0.083333
    yf.yf.count_days(fecha1, fecha3): 30
    
    <class 'qcfinancial.QCAct365'>
    yf(30): 0.082192
    yf.yf(fecha1, fecha3): 0.082192
    yf.yf.count_days(fecha1, fecha3): 30
    
    <class 'qcfinancial.QCAct30'>
    yf(30): 1.000000
    yf.yf(fecha1, fecha3): 1.000000
    yf.yf.count_days(fecha1, fecha3): 30
    
    <class 'qcfinancial.QC30360'>
    yf(30): 0.083333
    yf.yf(fecha1, fecha3): 0.080556
    yf.yf.count_days(fecha1, fecha3): 29
    
    <class 'qcfinancial.QC3030'>
    yf(30): 1.000000
    yf.yf(fecha1, fecha3): 0.966667
    yf.yf.count_days(fecha1, fecha3): 29
    
    <class 'qcfinancial.QCAct30'>
    yf(30): 1.000000
    yf.yf(fecha1, fecha3): 1.000000
    yf.yf.count_days(fecha1, fecha3): 30
    
    <class 'qcfinancial.QCActAct'>
    yf(30): 0.082192
    yf.yf(fecha1, fecha3): 0.082192
    yf.yf.count_days(fecha1, fecha3): 30
    


## Funciones y Factores de Capitalización

Las funciones de capitalización representan las distintas formas en que se puede usar el valor de una tasa de interés para calcular o traer a valor presente un flujo de caja futuro. Al resultado de la función de capitalización lo llamamos *factor de capitalización*.

Están disponibles los siguientes 3 tipos de funciones (donde $yf$ es la fracción de año asociada a la tasa de valor $r$):

- QCLinearWf:     $\rightarrow 1 + r \cdot yf$

- QCCompoundWf:    $\rightarrow \left(1 + r \right)^{yf}$

- QCContinousWf:  $\rightarrow exp(r \cdot yf)$


```python
wfs = [
    lin_wf:=qcf.QCLinearWf(),
    com_wf:=qcf.QCCompoundWf(),
    exp_wf:=qcf.QCContinousWf(),
]
```

### Método `wf`

Este método permite calcular el factor de capitalización a partir del valor de una tasa y el valor de una fracción de año.


```python
r = .1   # Valor de la tasa
yf = .5  # Fracción de año

for wf in wfs:
    print(f"Función: {wf}. Factor: {wf.wf(r, yf):6f}")
```

    Función: Lin. Factor: 1.050000
    Función: Com. Factor: 1.048809
    Función: Exp. Factor: 1.051271


### Método `rate`

Dada una función de capitalización, permite obtener la tasa de interés correspondiente a un factor de capitalización y fracción de año.

En este caso el factor de capitalización es 1.1, la fracción de año es 1.0 y la función de capitalización es Linear.


```python
print(f"Tasa equivalente: {wfs[0].rate(1.1, 1.0):.4%}")
```

    Tasa equivalente: 10.0000%


## Tasas de Interés

Utilizando un número real, una fracción de año y una función de capitalización, se puede dar de alta (instanciar) un objeto de tipo `QCInterestRate` que representa una tasa de interés (ver por ejemplo el video [Convenciones de Tasas](https://youtu.be/AdCMPKBFwgg?si=8v4wT1WER_poqEBg)).


```python
r0 = 0.1
tasas = [
    tasa_lin_act360 := qcf.QCInterestRate(0.1, act360, lin_wf),
    tasa_com_act365 := qcf.QCInterestRate(0.1, act365, com_wf),
    tasa_exp_act365 := qcf.QCInterestRate(0.1, act365, exp_wf),
]
```

### Métodos `get_value` y `set_value`

Permiten obtener y definir el valor de la tasa de interés.


```python
for tasa in tasas:
    print(f"Descripción: {tasa}") # Está definido el método __str__
    
    # Se obtiene el valor de la tasa utilizando get_value
    print("Obtener valor:", tasa.get_value())
    
    # Se utiliza set_value para cambiar el valor de la tasa
    r1 = 0.12
    tasa.set_value(r1)
    print("Obtener nuevo valor:", tasa.get_value())
    print()
```

    Descripción: 0.100000 Act360 Lin
    Obtener valor: 0.1
    Obtener nuevo valor: 0.12
    
    Descripción: 0.100000 Act365 Com
    Obtener valor: 0.1
    Obtener nuevo valor: 0.12
    
    Descripción: 0.100000 Act365 Exp
    Obtener valor: 0.1
    Obtener nuevo valor: 0.12
    


### Métodos `wf` y `dwf`

Tanto `wf` como `dwf`son métodos sobrecargados. El primero permite calcular el valor del factor de capitalización de la tasa de interés utilizando un número de días o un par de fechas, mientras que el segundo calcula la derivada del factor de capitalización respecto a la tasa de interés. 

¿Cómo se realiza el cálculo de la derivada? Veamos un ejemplo:

Consideremos una tasa de interés cuya función de capitalización es $g$. De ese modo el factor de capitalización $wf$ para un valor de tasa $r$ y una fracción de año $yf$ está dado por:

$$wf = g\left(r,yf\right)$$

En muchas situaciones nos interesará saber como cambia el factor de capitalización cuando el valor $r$ de la tasa cambia. Cuando el cambio de valor, es pequeño, digamos un punto básico, resulta conveniente calcular el cambio de valor en $wf$, $\Delta wf$ usando la derivada de la función $g$ respecto a $r$, más precisamente:

$$\Delta wf = \frac{dg\left(r,yf\right)}{dr}\left(r_0,yf\right)\cdot\delta$$

Donde $r_0$ es el valor inicial de la tasa y $\delta$ es el cambio en su valor.

Tenemos que:

- Si $g=1+r\cdot yf$ entonces $\Delta wf = yf\cdot\delta$

- Si $g=\left(1+r\right)^{yf}$ entonces $\Delta wf = yf\cdot\left(1+r_0\right)^{yf-1}\cdot\delta$

- Si $g=exp\left(r\cdot yf\right)$ entonces $\Delta wf = yf\cdot exp\left(r_0\cdot yf\right)\cdot\delta$

Calculemos `wf` y `dwf` usando un par de fechas.


```python
for i, tasa in enumerate(tasas):
    # Retorna el factor de capitalización entre las fechas
    print(f"wf(fecha1, fecha3): {tasa.wf(fecha1, fecha3):.8f}")

    # Retorna la derivada del factor de capitalización respecto al valor de la tasa entre las fechas
    print(f"dwf(fecha1, fecha3): {tasa.dwf(fecha1, fecha3):.8f}")

    # Para verificar se calcula "a mano" la derivada
    match i:
        case 0:
            print(f"Check: {tasa.yf(fecha1, fecha3):.8f}")
        case 1:
            yf_ = tasa.yf(fecha1, fecha3)
            print(f"Check: {tasa.yf(fecha1, fecha3) * (1 + r1)**(yf_ - 1):.8f}")
        case 2:
            print(f"Check: {tasa.yf(fecha1, fecha3) * tasa.wf(fecha1, fecha3):.8f}")
    
    print()
```

    wf(fecha1, fecha3): 1.01000000
    dwf(fecha1, fecha3): 0.08333333
    Check: 0.08333333
    
    wf(fecha1, fecha3): 1.00935820
    dwf(fecha1, fecha3): 0.07407228
    Check: 0.07407228
    
    wf(fecha1, fecha3): 1.00991181
    dwf(fecha1, fecha3): 0.08300645
    Check: 0.08300645
    


Veamos ahora la sobrecarga y utilicemos un número de días.


```python
dias = 400
for i, tasa in enumerate(tasas):
    # Retorna el factor de capitalización entre las fechas
    print(f"wf(dias): {tasa.wf(dias):.8F}")

    # Retorna la derivada del factor de capitalización respecto al valor de la tasa entre las fechas
    print(f"dwf(dias): {tasa.dwf(dias):.8f}")

    # Para verificar se calcula "a mano" la derivada
    match i:
        case 0:
            print(f"Check: {dias / 360:.8f}")
        case 1:
            yf_ = dias / 365
            print(f"Check: {yf_ * (1 + r1)**(yf_ - 1):.8f}")
        case 2:
            print(f"Check: {dias / 365 * tasa.wf(dias):.8f}")
    
    print()
```

    wf(dias): 1.13333333
    dwf(dias): 1.11111111
    Check: 1.11111111
    
    wf(dias): 1.13223756
    dwf(dias): 1.10786454
    Check: 1.10786454
    
    wf(dias): 1.14054572
    dwf(dias): 1.24991312
    Check: 1.24991312
    


### Método `get_rate_from_wf`

Este método permite calcular la tasa de interés correspondiente a un dado factor de capitalización, utilizando la función de capitalización y la fracción de año de la tasa. El intervalo de tiempo de la tasa se puede especificar con un par de fechas o con un número de días.

Veamos un ejemplo:


```python
factor = 1.0025
dias = 31
for tasa in tasas:
    aux = f"{tasa}"[-10:]
    print(f"Tasa: {aux}")
    print(f"get_rate_from_wf(factor, fecha1, fecha3): {tasa.get_rate_from_wf(factor, fecha1, fecha3):.4%}")
    print(f"get_rate_from_wf(factor, dias): {tasa.get_rate_from_wf(factor, dias):.4%}\n")

```

    Tasa: Act360 Lin
    get_rate_from_wf(factor, fecha1, fecha3): 3.0000%
    get_rate_from_wf(factor, dias): 2.9032%
    
    Tasa: Act365 Com
    get_rate_from_wf(factor, fecha1, fecha3): 3.0845%
    get_rate_from_wf(factor, dias): 2.9835%
    
    Tasa: Act365 Exp
    get_rate_from_wf(factor, fecha1, fecha3): 3.0379%
    get_rate_from_wf(factor, dias): 2.9399%
    


## Tenor

Es una clase que representa el concepto de plazo estructurado o tenor (1D, 1M, 1Y ...).

### Ejemplos


```python
tenors = [
    _1d := qcf.Tenor("1d"),
    _1m := qcf.Tenor("1M"),
    _1y := qcf.Tenor("1y"),
    _1d_1m_1y := qcf.Tenor("1D1M1Y"),

    # Notar que, en este caso, el constructor es capaz de eliminar
    # los espacios y la substr nyse
    _2y_3m := qcf.Tenor("2y nyse 3m"),  
]
```

### Métodos `get_string`, `get_days`, `get_months` y `get_years`


```python
for tenor in tenors:
    print(f"string: {tenor.get_string()}")
    print(f"dias: {tenor.get_days()}")
    print(f"meses: {tenor.get_months()}")
    print(f"años: {tenor.get_years()}\n")
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
    


### Método `set_tenor`


```python
for i, tenor in enumerate(tenors):
    tenor.set_tenor(f"{i}d{i}m{i}y")
    print(f"string: {tenor.get_string()}\n")
```

    string: 0D
    
    string: 1Y1M1D
    
    string: 2Y2M2D
    
    string: 3Y3M3D
    
    string: 4Y4M4D
    


## FX Rate

Es una clase que representa el concepto de tipo de cambio entre dos monedas. Para dar de alta un FXRate se requiere:

- QCCurrency: la moneda fuerte del par.

- QCCurrency: la moneda débl del par.

### Ejemplo: USDCLP


```python
usdclp = qcf.FXRate(usd, clp)
```

Utilizando el método `get_code` se puede obtener el código del par según la convención usual.


```python
print(f"Código: {usdclp.get_code()}")
```

    Código: USDCLP


## FX Rate Index

Esta clase representa un índice de tipo de cambio, por ejemplo, el dólar observado que publica el Banco Central de Chile.

Para dar de alta un FXRateIndex se requiere:

- `FXRate`: el FXRate correspondiente.
- `str`: nombre del índice
- `Tenor`: la regla de fixing, es 1D como el USD Observado o es 0D como un índice de cierre de día.
- `Tenor`: la regla para la valuta. Es 1D como el USDCLP o 2D como el EURUSD.
- `BusinessCalendar`: el calendario adecuado para aplicar las reglas de fixing y valuta.

### Ejemplo


```python
_1d.set_tenor("1d")
usdclp_obs = qcf.FXRateIndex(usdclp, "USDOBS", _1d, _1d, qcf_scl)
```

### Métodos `fixing_date` y `value_date`

El método `fixing_date` retorna la fecha de fixing del índice dada la fecha de publicación. Por su parte, `value_date` retorna la fecha de la valuta dada la fecha de publicación.


```python
print(f"Fecha de publicación: {fecha1.week_day()}, {fecha1}")
print(f"Fecha de fixing: {usdclp_obs.fixing_date(fecha1)}")
print(f"Fecha de valuta: {usdclp_obs.value_date(fecha1)}")
```

    Fecha de publicación: WeekDay.THU, 2024-10-17
    Fecha de fixing: 2024-10-16
    Fecha de valuta: 2024-10-17


Notar que la fecha de fixing se calcula aplicando la regla de fixing a la fecha de publicación, mientras que la fecha de valuta se calcula aplicando la regla de valuta a la fecha de fixing.

### Método `convert`

El método `convert` permite pasar rápidamente de una moneda a la otra (de las que forman el par del índice) usando un valor para el índice.

Veamos un ejemplo:


```python
monto_usd = 1_000_000
monto_clp = 900_000_000
valor_usdclp_obs = 900.00

result = usdclp_obs.convert(monto_usd, qcf.QCUSD(), valor_usdclp_obs)
print(f"Monto en CLP es: {result:,.0f}")

result = usdclp_obs.convert(monto_clp, qcf.QCCLP(), valor_usdclp_obs)
print(f"Monto en USD es: {result:,.0f}")
```

    Monto en CLP es: 900,000,000
    Monto en USD es: 1,000,000


Esta función es cómoda porque evita tener que controlar en el propio código si la divisa del monto a convertir es la fuerte o la débil del par.

## QCCurrencyConverter

Este es un objeto que permite realizar conversiones de una moneda a otra con un poco más de generalidad que en el caso anterior.


```python
ccy_converter = qcf.QCCurrencyConverter()
```

### Método `convert`

El método `convert` se puede utilizar con dos conjuntos distintos de argumentos:

- `float`: que representa el monto en una divisa a convertir,
- `QCCurrency`: que representa la divisa del monto anterior
- `float`: que representa el valor del tipo de cambio a utilizar en la convención de mercado del par
- `FXRateIndex`: que representa el par de monedas entre las cuales se realiza la conversión

Por ejemplo:


```python
print(f'Monto en CLP: {ccy_converter.convert(monto_usd, usd, 900, usdclp_obs):,.0f}')
print(f'Monto en USD: {ccy_converter.convert(monto_clp, clp, 900, usdclp_obs):,.0f}')
```

    Monto en CLP: 900,000,000
    Monto en USD: 1,000,000


Para el segundo método se introducen dos `enum` definidos en `QCCurrencyConverter`:

#### Enum para Monedas


```python
qcf.QCCurrencyEnum.CLP
```




    <QCCurrencyEnum.CLP: 6>




```python
qcf.QCCurrencyEnum.USD
```




    <QCCurrencyEnum.USD: 18>



#### Enum para FXRates


```python
qcf.QCFxRateEnum.USDCLP
```




    <QCFxRateEnum.USDCLP: 15>




```python
qcf.QCFxRateEnum.EURUSD
```




    <QCFxRateEnum.EURUSD: 31>



Con estos `enum` el segundo conjunto de argumentos para el método `convert` es:

- float: que representa el monto en una divisa a convertir,
- QCCurrencyEnum: que representa la divisa del monto anterior
- float: que representa el valor del tipo de cambio a utilizar en la convención de mercado del par
- QCFxRateEnum: que representa el par de monedas entre las cuales se realiza la conversión

Por ejemplo:


```python
print(f'Monto en USD: {ccy_converter.convert(monto_clp, qcf.QCCurrencyEnum.CLP, 900, qcf.QCFxRateEnum.USDCLP):,.0f}')
print(f'Monto en CLP: {ccy_converter.convert(monto_usd, qcf.QCCurrencyEnum.USD, 900, qcf.QCFxRateEnum.USDCLP):,.0f}')
```

    Monto en USD: 1,000,000
    Monto en CLP: 900,000,000


Las divisas disponibles en `QCCurrencyEnum` son las mismas que en `QCCurrency`:


```python
qcf.QCCurrencyEnum.AUD
```




    <QCCurrencyEnum.AUD: 0>




```python
qcf.QCCurrencyEnum.BRL
```




    <QCCurrencyEnum.BRL: 1>




```python
qcf.QCCurrencyEnum.PEN
```




    <QCCurrencyEnum.PEN: 16>



Los pares de divisas en `QCFxRateEnum` son los pares de las divisas versus el USD (en su convención de mercado) y las divisas versus CLP, que aunque no son pares líquidos, son útiles cuando se quiere expresar montos en cualquier divisa en CLP.


```python
qcf.QCFxRateEnum.USDCLP
```




    <QCFxRateEnum.USDCLP: 15>




```python
qcf.QCFxRateEnum.EURUSD
```




    <QCFxRateEnum.EURUSD: 31>




```python
qcf.QCFxRateEnum.EURCLP
```




    <QCFxRateEnum.EURCLP: 32>



## Time Series

Este es un objeto que permite almacenar series de tiempo financieras y se utilizarán más adelante en el fixing y valorización de flujos de caja de tasa de interés. Su estructura interna es muy similar a la de un objeto `dict[datetime.date, float]` en Python, sólo se debe reemplazar la `key` del `dict` por un objeto de tipo `QCCDate`.

### Ejemplo


```python
ts = qcf.time_series()
ts[fecha1] = 10.0
```


```python
type(ts)
```




    qcfinancial.time_series




```python
ts[fecha1]
```




    10.0




```python
for k, v in ts.items():
    print(k, v)
```

    2024-10-17 10.0

