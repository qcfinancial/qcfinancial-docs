# Valorización y Sensibilidad

## Configuración

Para ejecutar todos los ejemplos se debe importar la librería. Se sugiere utilizar siempre el alias `qcf`. 


```python
import qcfinancial as qcf
```


```python
qcf.id()
```




    'version: 0.10.0, build: 2024-06-09 10:20'



Librerías adicionales.


```python
import aux_functions as aux # Aquí se guardó la funcion leg_as_dataframe del notebook 3
from math import exp, log
import pandas as pd
import numpy as np
```


```python
pd.options.display.max_columns=300
```

Para formateo de `pandas.DataFrames`.


```python
format_dict = {
    'nominal': '{:,.2f}',
    'amort': '{:,.2f}',
    'interes': '{:,.2f}',
    'flujo': '{:,.2f}',
    'nocional': '{:,.2f}',
    'amortizacion': '{:,.2f}',
    'icp_inicial': '{:,.2f}',
    'icp_final': '{:,.2f}',
    'uf_inicial': '{:,.2f}',
    'uf_final': '{:,.2f}',
    'plazo': '{:,.0f}',
    'tasa': '{:,.4%}',
    'valor_tasa': '{:,.4%}',
    'valor_tasa_equivalente': '{:,.4%}',
    'spread': '{:,.4%}',
    'gearing': '{:,.2f}',
    'amort_moneda_pago': '{:,.2f}',
    'interes_moneda_pago': '{:,.2f}',
    'valor_indice_inicial': '{:,.2f}',
    'valor_indice_final': '{:,.2f}',
    'valor_indice_fx': '{:,.2f}',
    'flujo_en_clp': '{:,.2f}',
}
```

## Construcción de la Curva

La construcción de una curva se hace en varios pasos.

### Vectores de `Float` e `Int`

Este es un vector de números enteros (grandes, de ahí la l (long))


```python
lvec = qcf.long_vec()
```

Agregar un elemento.


```python
lvec.append(1000)
```

Este es un vector de números `float`.


```python
vec = qcf.double_vec()
```

Agregar un elemento.


```python
vec.append(.025)
```

Obtener ese elemento.


```python
print(f"Plazo: {lvec[0]:,.0f}")
print(f"Tasa: {vec[0]:,.2%}")
```

    Plazo: 1,000
    Tasa: 2.50%


### Objeto Curva

Es simplemente un `long_vec` que representa las abscisas de la curva y un `double_vec` que representa las ordenadas. Ambos vectores deben tener el mismo largo. 


```python
curva = qcf.QCCurve(lvec, vec)
```

Un elemento de una curva se representa como un par abscisa, ordenada.


```python
curva.get_values_at(0)
```




    (1000, 0.025)



Se obtiene el plazo en una posición de la curva.


```python
curva.get_values_at(0)[0]
```




    1000



Se obtiene la tasa en una posición de la curva.


```python
curva.get_values_at(0)[1]
```




    0.025



Se agrega un par (plazo, valor) a la curva.


```python
curva.set_pair(100, .026)
```

Se verifica. Notar que se debe usar el índice 0 ya que la curva se ordena automáticamente por plazos ascendentes.


```python
curva.get_values_at(0)[0]
```




    100




```python
curva.get_values_at(0)[1]
```




    0.026



Se agrega un par más.


```python
curva.set_pair(370, .03)
```

Se itera sobre la curva mostrando sus valores


```python
for i in range(curva.get_length()):
    pair = curva.get_values_at(i)
    print("Tenor: {0:,.0f} Valor: {1:.4%}".format(pair[0], pair[1]))
```

    Tenor: 100 Valor: 2.6000%
    Tenor: 370 Valor: 3.0000%
    Tenor: 1,000 Valor: 2.5000%


### Interpolador

Se agrega un interpolador. En este caso, un interpolador lineal.


```python
lin = qcf.QCLinearInterpolator(curva)
```

Se puede ahora obtener una tasa a un plazo cualquiera.


```python
plazo = 120
print(f"Tasa a {plazo:,.0f} días es igual a {lin.interpolate_at(plazo):.4%}")
```

    Tasa a 120 días es igual a 2.6296%


### Curva Cero Cupón

Para completar el proceso se define un objeto de tipo `QCInterestRate`. Con este objeto, que representa la convención de las tasas de interés asociadas a la curva, se termina de dar de alta una curva cero cupón.


```python
yf = qcf.QCAct365()
wf = qcf.QCContinousWf()
tasa = qcf.QCInterestRate(.0, yf, wf)
```


```python
zcc = qcf.ZeroCouponCurve(lin, tasa)
```

El interpolador permite obtener una tasa a cualquier plazo.


```python
plazo = 300
print(f"Tasa en {plazo:,.0f} es igual a {zcc.get_rate_at(plazo):.4%}")
```

    Tasa en 300 es igual a 2.8963%


#### Otros métodos:

Discount factor.


```python
print(f"Discount factor at {plazo}: {zcc.get_discount_factor_at(plazo):.6%}")
print(f"Check: {exp(-zcc.get_rate_at(plazo) * plazo / 365):.6%}")
```

    Discount factor at 300: 97.647593%
    Check: 97.647593%


Derivadas del factor de descuento respecto a los vértices de la curva.


```python
[zcc.wf_derivative_at(i) for i in range(zcc.get_length())]
```




    [0.21822330167566764, 0.6234951476447647, 0.0]



Tasa Forward


```python
d1 = 30
d2 = 90
print(f"Tasa forward entre los días {d1:,.0f} y {d2:,.0f}: {zcc.get_forward_rate(d1, d2):.4%}")
```

    Tasa forward entre los días 30 y 90: 2.6000%


Se verifica el cálculo.


```python
df1 = zcc.get_discount_factor_at(d1)
df2 = zcc.get_discount_factor_at(d2)
df12 = df1 / df2
print(f"Check: {log(df12) * 365 / (d2 - d1):.4%}")
```

    Check: 2.6000%


Derivadas del factor de capitalización de la tasa forward.


```python
[zcc.fwd_wf_derivative_at(i) for i in range(zcc.get_length())]
```




    [0.16508763600814624, 0.0, 0.0]



## Valorizar

Para valorizar es necesario dar de alta un objeto de tipo `PresentValue`.


```python
pv = qcf.PresentValue()
```

### Depósito a Plazo

Se utilizará como instrumento un depósito a plazo en CLP o USD. Este instrumento se modela como un `SimpleCashflow`. Este, a su vez se construye con un monto, una fecha y una moneda.


```python
fecha_vcto = qcf.QCDate(13, 1, 2025)
monto = 10_000_000.0
clp = qcf.QCCLP()

# Se construye el depósito
depo = qcf.SimpleCashflow(fecha_vcto, monto, clp)
```


```python
print(f"Monto del depósito: {depo.amount():,.0f}")
```

    Monto del depósito: 10,000,000


Se define una fecha de valorización y se calcula el valor presente del depo.


```python
fecha_hoy = qcf.QCDate(31, 1, 2024)
print(f"Valor presente depo: {pv.pv(fecha_hoy, depo, zcc):,.2f}")
```

    Valor presente depo: 9,721,044.77


Se verifica *a mano* el resultado.


```python
plazo = fecha_hoy.day_diff(fecha_vcto)
print("Plazo:", plazo)
```

    Plazo: 348



```python
tasa_int = zcc.get_rate_at(plazo)
print(f"Tasa: {tasa_int:,.4%}")
```

    Tasa: 2.9674%



```python
valor_presente = monto * exp(-tasa_int * plazo / 365)
print(f"Valor presente a mano: {valor_presente:,.2f}")
```

    Valor presente a mano: 9,721,044.77


### Renta Fija de Chile

Se muestra el ejemplo de valorización de un bono bullet a tasa fija con las convenciones de la Bolsa de Comercio de Santiago. Para el ejemplo usamos las características del BTU0150326.

Se dan de alta los parámetros requeridos para instanciar un objeto de tipo `FixedRateLeg`.


```python
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(1, 3, 2015)
fecha_final = qcf.QCDate(1, 3, 2026)
bus_adj_rule = qcf.BusyAdjRules.NO
periodicidad = qcf.Tenor('6M')
periodo_irregular = qcf.StubPeriod.NO
calendario = qcf.BusinessCalendar(fecha_inicio, 20)
lag_pago = 0
nominal = 100.0
amort_es_flujo = True
valor_tasa_fija = .015
tasa_cupon = qcf.QCInterestRate(
    valor_tasa_fija, 
    qcf.QC30360(),
    qcf.QCLinearWf()
)
moneda = qcf.QCCLP()
es_bono = True
```

Se da de alta el objeto.


```python
pata_bono = qcf.LegFactory.build_bullet_fixed_rate_leg(
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

Se da de alta el valor de la TERA y luego se construye un objeto de tipo `ChileanFixedRateBond`.


```python
tera = qcf.QCInterestRate(.015044, qcf.QCAct365(), qcf.QCCompoundWf())
bono_chileno = qcf.ChileanFixedRateBond(pata_bono, tera)
```

Se valoriza al 2021-09-28 a una TIR de mercado del 1.61%.


```python
fecha_valor = qcf.QCDate(28, 9, 2021)
tir = qcf.QCInterestRate(.0161, qcf.QCAct365(), qcf.QCCompoundWf())

valor_presente = bono_chileno.present_value(fecha_valor, tir)
precio = bono_chileno.precio(fecha_valor, tir)
valor_par = bono_chileno.valor_par(fecha_valor)

print(f'Valor presente: {valor_presente:,.8f}')
print(f'Precio: {precio:,.2%}')
print(f'Valor par: {valor_par:,.18f}')
```

    Valor presente: 99.67188455
    Precio: 99.56%
    Valor par: 100.110516628864033351


Con esto el valor a pagar es:


```python
valor_uf = 30_080.37
valor_pago = precio * valor_par * valor_uf
print(f'Valor a pagar: {valor_pago:,.0f}')
```

    Valor a pagar: 2,998,111


Con 4 decimales en el precio (4 decimales porcentuales, 6 decimales en el número):


```python
precio2 = bono_chileno.precio2(fecha_valor, tir, 6)
print(f'Precio a 4 decmales: {precio2:.4%}')
```

    Precio a 4 decmales: 99.5619%


La función `precio2` entrega el mismo resultado que la función precio cuando se utiliza con 2 decimales porcentuales.


```python
precio22 = bono_chileno.precio2(fecha_valor, tir, 4)
print(f'Precio a 4 decmales: {precio22:.4%}')
```

    Precio a 4 decmales: 99.5600%


Se muestran las diferencias con la convención de precio usual en mercados desarrollados.


```python
bono = qcf.FixedRateBond(pata_bono)
print(f'Valor presente: {bono.present_value(fecha_valor, tir):,.8f}')
print(f'Precio: {bono.price(fecha_valor, tir):,.8f}')
```

    Valor presente: 99.67188455
    Precio: 99.55938455


### Curvas Reales

Construyamos dos curvas a partir de data real. Primero una curva en CLP.


```python
curva_clp = pd.read_excel("./input/curva_clp.xlsx")
curva_clp.style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_287c4">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_287c4_level0_col0" class="col_heading level0 col0" >plazo</th>
      <th id="T_287c4_level0_col1" class="col_heading level0 col1" >tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_287c4_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_287c4_row0_col0" class="data row0 col0" >1</td>
      <td id="T_287c4_row0_col1" class="data row0 col1" >1.7500%</td>
    </tr>
    <tr>
      <th id="T_287c4_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_287c4_row1_col0" class="data row1 col0" >4</td>
      <td id="T_287c4_row1_col1" class="data row1 col1" >1.7501%</td>
    </tr>
    <tr>
      <th id="T_287c4_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_287c4_row2_col0" class="data row2 col0" >96</td>
      <td id="T_287c4_row2_col1" class="data row2 col1" >1.4867%</td>
    </tr>
    <tr>
      <th id="T_287c4_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_287c4_row3_col0" class="data row3 col0" >188</td>
      <td id="T_287c4_row3_col1" class="data row3 col1" >1.3049%</td>
    </tr>
    <tr>
      <th id="T_287c4_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_287c4_row4_col0" class="data row4 col0" >279</td>
      <td id="T_287c4_row4_col1" class="data row4 col1" >1.2870%</td>
    </tr>
    <tr>
      <th id="T_287c4_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_287c4_row5_col0" class="data row5 col0" >369</td>
      <td id="T_287c4_row5_col1" class="data row5 col1" >1.3002%</td>
    </tr>
    <tr>
      <th id="T_287c4_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_287c4_row6_col0" class="data row6 col0" >553</td>
      <td id="T_287c4_row6_col1" class="data row6 col1" >1.3035%</td>
    </tr>
    <tr>
      <th id="T_287c4_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_287c4_row7_col0" class="data row7 col0" >734</td>
      <td id="T_287c4_row7_col1" class="data row7 col1" >1.2951%</td>
    </tr>
    <tr>
      <th id="T_287c4_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_287c4_row8_col0" class="data row8 col0" >1,099</td>
      <td id="T_287c4_row8_col1" class="data row8 col1" >1.4440%</td>
    </tr>
    <tr>
      <th id="T_287c4_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_287c4_row9_col0" class="data row9 col0" >1,465</td>
      <td id="T_287c4_row9_col1" class="data row9 col1" >1.6736%</td>
    </tr>
    <tr>
      <th id="T_287c4_level0_row10" class="row_heading level0 row10" >10</th>
      <td id="T_287c4_row10_col0" class="data row10 col0" >1,830</td>
      <td id="T_287c4_row10_col1" class="data row10 col1" >1.9860%</td>
    </tr>
    <tr>
      <th id="T_287c4_level0_row11" class="row_heading level0 row11" >11</th>
      <td id="T_287c4_row11_col0" class="data row11 col0" >2,195</td>
      <td id="T_287c4_row11_col1" class="data row11 col1" >2.2766%</td>
    </tr>
    <tr>
      <th id="T_287c4_level0_row12" class="row_heading level0 row12" >12</th>
      <td id="T_287c4_row12_col0" class="data row12 col0" >2,560</td>
      <td id="T_287c4_row12_col1" class="data row12 col1" >2.5812%</td>
    </tr>
    <tr>
      <th id="T_287c4_level0_row13" class="row_heading level0 row13" >13</th>
      <td id="T_287c4_row13_col0" class="data row13 col0" >2,926</td>
      <td id="T_287c4_row13_col1" class="data row13 col1" >2.8216%</td>
    </tr>
    <tr>
      <th id="T_287c4_level0_row14" class="row_heading level0 row14" >14</th>
      <td id="T_287c4_row14_col0" class="data row14 col0" >3,291</td>
      <td id="T_287c4_row14_col1" class="data row14 col1" >3.0373%</td>
    </tr>
    <tr>
      <th id="T_287c4_level0_row15" class="row_heading level0 row15" >15</th>
      <td id="T_287c4_row15_col0" class="data row15 col0" >3,656</td>
      <td id="T_287c4_row15_col1" class="data row15 col1" >3.2154%</td>
    </tr>
    <tr>
      <th id="T_287c4_level0_row16" class="row_heading level0 row16" >16</th>
      <td id="T_287c4_row16_col0" class="data row16 col0" >4,387</td>
      <td id="T_287c4_row16_col1" class="data row16 col1" >3.4525%</td>
    </tr>
    <tr>
      <th id="T_287c4_level0_row17" class="row_heading level0 row17" >17</th>
      <td id="T_287c4_row17_col0" class="data row17 col0" >5,482</td>
      <td id="T_287c4_row17_col1" class="data row17 col1" >3.7636%</td>
    </tr>
    <tr>
      <th id="T_287c4_level0_row18" class="row_heading level0 row18" >18</th>
      <td id="T_287c4_row18_col0" class="data row18 col0" >7,309</td>
      <td id="T_287c4_row18_col1" class="data row18 col1" >4.1641%</td>
    </tr>
  </tbody>
</table>




Se da de alta un vector con los plazos (variable de tipo `long`) y un vector con las tasas (variable de tipo `double`).


```python
lvec1 = qcf.long_vec()
vec1 = qcf.double_vec()
for t in curva_clp.itertuples():
    lvec1.append(int(t.plazo))
    vec1.append(t.tasa)
```

Luego, con una curva, un interpolador y un objeto `QCInterestRate`(que indica la convención de las tasas de la curva) se construye una curva cupón cero.


```python
curva1 = qcf.QCCurve(lvec1, vec1)
lin1 = qcf.QCLinearInterpolator(curva1)
zcc_clp = qcf.ZeroCouponCurve(lin1, tasa)
```

Luego, una curva en USD.


```python
curva_usd = pd.read_excel("./input/curva_usd.xlsx")
curva_usd.style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_ea577">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_ea577_level0_col0" class="col_heading level0 col0" >plazo</th>
      <th id="T_ea577_level0_col1" class="col_heading level0 col1" >tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_ea577_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_ea577_row0_col0" class="data row0 col0" >3</td>
      <td id="T_ea577_row0_col1" class="data row0 col1" >1.5362%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_ea577_row1_col0" class="data row1 col0" >4</td>
      <td id="T_ea577_row1_col1" class="data row1 col1" >1.1521%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_ea577_row2_col0" class="data row2 col0" >7</td>
      <td id="T_ea577_row2_col1" class="data row2 col1" >1.5536%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_ea577_row3_col0" class="data row3 col0" >14</td>
      <td id="T_ea577_row3_col1" class="data row3 col1" >1.5850%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_ea577_row4_col0" class="data row4 col0" >31</td>
      <td id="T_ea577_row4_col1" class="data row4 col1" >1.6595%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_ea577_row5_col0" class="data row5 col0" >60</td>
      <td id="T_ea577_row5_col1" class="data row5 col1" >1.7698%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_ea577_row6_col0" class="data row6 col0" >91</td>
      <td id="T_ea577_row6_col1" class="data row6 col1" >1.8010%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_ea577_row7_col0" class="data row7 col0" >123</td>
      <td id="T_ea577_row7_col1" class="data row7 col1" >1.7711%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_ea577_row8_col0" class="data row8 col0" >152</td>
      <td id="T_ea577_row8_col1" class="data row8 col1" >1.7542%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_ea577_row9_col0" class="data row9 col0" >182</td>
      <td id="T_ea577_row9_col1" class="data row9 col1" >1.7394%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row10" class="row_heading level0 row10" >10</th>
      <td id="T_ea577_row10_col0" class="data row10 col0" >213</td>
      <td id="T_ea577_row10_col1" class="data row10 col1" >1.7288%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row11" class="row_heading level0 row11" >11</th>
      <td id="T_ea577_row11_col0" class="data row11 col0" >244</td>
      <td id="T_ea577_row11_col1" class="data row11 col1" >1.7183%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row12" class="row_heading level0 row12" >12</th>
      <td id="T_ea577_row12_col0" class="data row12 col0" >276</td>
      <td id="T_ea577_row12_col1" class="data row12 col1" >1.7027%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row13" class="row_heading level0 row13" >13</th>
      <td id="T_ea577_row13_col0" class="data row13 col0" >305</td>
      <td id="T_ea577_row13_col1" class="data row13 col1" >1.6917%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row14" class="row_heading level0 row14" >14</th>
      <td id="T_ea577_row14_col0" class="data row14 col0" >335</td>
      <td id="T_ea577_row14_col1" class="data row14 col1" >1.6820%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row15" class="row_heading level0 row15" >15</th>
      <td id="T_ea577_row15_col0" class="data row15 col0" >367</td>
      <td id="T_ea577_row15_col1" class="data row15 col1" >1.6722%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row16" class="row_heading level0 row16" >16</th>
      <td id="T_ea577_row16_col0" class="data row16 col0" >549</td>
      <td id="T_ea577_row16_col1" class="data row16 col1" >1.6207%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row17" class="row_heading level0 row17" >17</th>
      <td id="T_ea577_row17_col0" class="data row17 col0" >731</td>
      <td id="T_ea577_row17_col1" class="data row17 col1" >1.5947%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row18" class="row_heading level0 row18" >18</th>
      <td id="T_ea577_row18_col0" class="data row18 col0" >1,096</td>
      <td id="T_ea577_row18_col1" class="data row18 col1" >1.5788%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row19" class="row_heading level0 row19" >19</th>
      <td id="T_ea577_row19_col0" class="data row19 col0" >1,461</td>
      <td id="T_ea577_row19_col1" class="data row19 col1" >1.5906%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row20" class="row_heading level0 row20" >20</th>
      <td id="T_ea577_row20_col0" class="data row20 col0" >1,827</td>
      <td id="T_ea577_row20_col1" class="data row20 col1" >1.6190%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row21" class="row_heading level0 row21" >21</th>
      <td id="T_ea577_row21_col0" class="data row21 col0" >2,558</td>
      <td id="T_ea577_row21_col1" class="data row21 col1" >1.7028%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row22" class="row_heading level0 row22" >22</th>
      <td id="T_ea577_row22_col0" class="data row22 col0" >3,653</td>
      <td id="T_ea577_row22_col1" class="data row22 col1" >1.8533%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row23" class="row_heading level0 row23" >23</th>
      <td id="T_ea577_row23_col0" class="data row23 col0" >4,385</td>
      <td id="T_ea577_row23_col1" class="data row23 col1" >1.9547%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row24" class="row_heading level0 row24" >24</th>
      <td id="T_ea577_row24_col0" class="data row24 col0" >5,479</td>
      <td id="T_ea577_row24_col1" class="data row24 col1" >2.0893%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row25" class="row_heading level0 row25" >25</th>
      <td id="T_ea577_row25_col0" class="data row25 col0" >7,305</td>
      <td id="T_ea577_row25_col1" class="data row25 col1" >2.2831%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row26" class="row_heading level0 row26" >26</th>
      <td id="T_ea577_row26_col0" class="data row26 col0" >9,132</td>
      <td id="T_ea577_row26_col1" class="data row26 col1" >2.4306%</td>
    </tr>
    <tr>
      <th id="T_ea577_level0_row27" class="row_heading level0 row27" >27</th>
      <td id="T_ea577_row27_col0" class="data row27 col0" >10,958</td>
      <td id="T_ea577_row27_col1" class="data row27 col1" >2.5576%</td>
    </tr>
  </tbody>
</table>




Se encapasulará todo el procedimiento anterior en una función que dado un `DataFrame` construya un objeto `ZeroCouponCurve`.


```python
def zcc_from_df(df: pd.DataFrame, tasa: qcf.QCInterestRate) -> qcf.ZeroCouponCurve:
    lvec = qcf.long_vec()
    vec = qcf.double_vec()
    for t in df.itertuples():
        lvec.append(int(t.plazo))
        vec.append(t.tasa)
    curva = qcf.QCCurve(lvec, vec)
    lin = qcf.QCLinearInterpolator(curva)
    return qcf.ZeroCouponCurve(lin, tasa)
```


```python
zcc_usd = zcc_from_df(curva_usd, tasa)
```

Finalmente, una curva en CLF.


```python
curva_clf = pd.read_excel("./input/curva_clf.xlsx")
curva_clf.style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_f5c3d">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_f5c3d_level0_col0" class="col_heading level0 col0" >plazo</th>
      <th id="T_f5c3d_level0_col1" class="col_heading level0 col1" >tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_f5c3d_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_f5c3d_row0_col0" class="data row0 col0" >1</td>
      <td id="T_f5c3d_row0_col1" class="data row0 col1" >-5.6780%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_f5c3d_row1_col0" class="data row1 col0" >4</td>
      <td id="T_f5c3d_row1_col1" class="data row1 col1" >-5.6744%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_f5c3d_row2_col0" class="data row2 col0" >35</td>
      <td id="T_f5c3d_row2_col1" class="data row2 col1" >-0.9340%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_f5c3d_row3_col0" class="data row3 col0" >64</td>
      <td id="T_f5c3d_row3_col1" class="data row3 col1" >-2.1183%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_f5c3d_row4_col0" class="data row4 col0" >96</td>
      <td id="T_f5c3d_row4_col1" class="data row4 col1" >-2.0079%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_f5c3d_row5_col0" class="data row5 col0" >126</td>
      <td id="T_f5c3d_row5_col1" class="data row5 col1" >-2.0762%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_f5c3d_row6_col0" class="data row6 col0" >155</td>
      <td id="T_f5c3d_row6_col1" class="data row6 col1" >-1.9197%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_f5c3d_row7_col0" class="data row7 col0" >188</td>
      <td id="T_f5c3d_row7_col1" class="data row7 col1" >-1.9347%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_f5c3d_row8_col0" class="data row8 col0" >218</td>
      <td id="T_f5c3d_row8_col1" class="data row8 col1" >-1.7626%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_f5c3d_row9_col0" class="data row9 col0" >249</td>
      <td id="T_f5c3d_row9_col1" class="data row9 col1" >-1.7987%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row10" class="row_heading level0 row10" >10</th>
      <td id="T_f5c3d_row10_col0" class="data row10 col0" >279</td>
      <td id="T_f5c3d_row10_col1" class="data row10 col1" >-1.9335%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row11" class="row_heading level0 row11" >11</th>
      <td id="T_f5c3d_row11_col0" class="data row11 col0" >309</td>
      <td id="T_f5c3d_row11_col1" class="data row11 col1" >-1.8159%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row12" class="row_heading level0 row12" >12</th>
      <td id="T_f5c3d_row12_col0" class="data row12 col0" >341</td>
      <td id="T_f5c3d_row12_col1" class="data row12 col1" >-1.5940%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row13" class="row_heading level0 row13" >13</th>
      <td id="T_f5c3d_row13_col0" class="data row13 col0" >369</td>
      <td id="T_f5c3d_row13_col1" class="data row13 col1" >-1.5994%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row14" class="row_heading level0 row14" >14</th>
      <td id="T_f5c3d_row14_col0" class="data row14 col0" >400</td>
      <td id="T_f5c3d_row14_col1" class="data row14 col1" >-1.5068%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row15" class="row_heading level0 row15" >15</th>
      <td id="T_f5c3d_row15_col0" class="data row15 col0" >428</td>
      <td id="T_f5c3d_row15_col1" class="data row15 col1" >-1.6115%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row16" class="row_heading level0 row16" >16</th>
      <td id="T_f5c3d_row16_col0" class="data row16 col0" >461</td>
      <td id="T_f5c3d_row16_col1" class="data row16 col1" >-1.5923%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row17" class="row_heading level0 row17" >17</th>
      <td id="T_f5c3d_row17_col0" class="data row17 col0" >491</td>
      <td id="T_f5c3d_row17_col1" class="data row17 col1" >-1.5780%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row18" class="row_heading level0 row18" >18</th>
      <td id="T_f5c3d_row18_col0" class="data row18 col0" >522</td>
      <td id="T_f5c3d_row18_col1" class="data row18 col1" >-1.5186%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row19" class="row_heading level0 row19" >19</th>
      <td id="T_f5c3d_row19_col0" class="data row19 col0" >553</td>
      <td id="T_f5c3d_row19_col1" class="data row19 col1" >-1.5533%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row20" class="row_heading level0 row20" >20</th>
      <td id="T_f5c3d_row20_col0" class="data row20 col0" >582</td>
      <td id="T_f5c3d_row20_col1" class="data row20 col1" >-1.5649%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row21" class="row_heading level0 row21" >21</th>
      <td id="T_f5c3d_row21_col0" class="data row21 col0" >734</td>
      <td id="T_f5c3d_row21_col1" class="data row21 col1" >-1.6594%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row22" class="row_heading level0 row22" >22</th>
      <td id="T_f5c3d_row22_col0" class="data row22 col0" >1,099</td>
      <td id="T_f5c3d_row22_col1" class="data row22 col1" >-1.4881%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row23" class="row_heading level0 row23" >23</th>
      <td id="T_f5c3d_row23_col0" class="data row23 col0" >1,465</td>
      <td id="T_f5c3d_row23_col1" class="data row23 col1" >-1.2740%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row24" class="row_heading level0 row24" >24</th>
      <td id="T_f5c3d_row24_col0" class="data row24 col0" >1,830</td>
      <td id="T_f5c3d_row24_col1" class="data row24 col1" >-1.0201%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row25" class="row_heading level0 row25" >25</th>
      <td id="T_f5c3d_row25_col0" class="data row25 col0" >2,195</td>
      <td id="T_f5c3d_row25_col1" class="data row25 col1" >-0.8009%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row26" class="row_heading level0 row26" >26</th>
      <td id="T_f5c3d_row26_col0" class="data row26 col0" >2,560</td>
      <td id="T_f5c3d_row26_col1" class="data row26 col1" >-0.5868%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row27" class="row_heading level0 row27" >27</th>
      <td id="T_f5c3d_row27_col0" class="data row27 col0" >2,926</td>
      <td id="T_f5c3d_row27_col1" class="data row27 col1" >-0.4145%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row28" class="row_heading level0 row28" >28</th>
      <td id="T_f5c3d_row28_col0" class="data row28 col0" >3,291</td>
      <td id="T_f5c3d_row28_col1" class="data row28 col1" >-0.3047%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row29" class="row_heading level0 row29" >29</th>
      <td id="T_f5c3d_row29_col0" class="data row29 col0" >3,656</td>
      <td id="T_f5c3d_row29_col1" class="data row29 col1" >-0.2242%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row30" class="row_heading level0 row30" >30</th>
      <td id="T_f5c3d_row30_col0" class="data row30 col0" >4,387</td>
      <td id="T_f5c3d_row30_col1" class="data row30 col1" >-0.1871%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row31" class="row_heading level0 row31" >31</th>
      <td id="T_f5c3d_row31_col0" class="data row31 col0" >5,482</td>
      <td id="T_f5c3d_row31_col1" class="data row31 col1" >-0.1056%</td>
    </tr>
    <tr>
      <th id="T_f5c3d_level0_row32" class="row_heading level0 row32" >32</th>
      <td id="T_f5c3d_row32_col0" class="data row32 col0" >7,309</td>
      <td id="T_f5c3d_row32_col1" class="data row32 col1" >-0.0639%</td>
    </tr>
  </tbody>
</table>





```python
zcc_clf = zcc_from_df(curva_clf, tasa)
```

#### Curvas para Sensibilidad

Para calcular sensibilidad a la curva cero cupón, se define qué vértice de la curva se quiere desplazar y el monto en puntos básicos del desplazamiento.


```python
vertice = 15
bp = 1
```

Se construyen las curvas con ese vértice 1 punto básico más arriba y 1 punto básico más abajo. Para esto se define una función auxiliar.


```python
def curvas_sens(
    df: pd.DataFrame, 
    tasa: qcf.QCInterestRate, 
    vertice: int, 
    bp: float
) -> tuple[qcf.ZeroCouponCurve, qcf.ZeroCouponCurve]:
    bp /= 10_000
    lvec = qcf.long_vec()
    vec_sens_up = qcf.double_vec()
    vec_sens_down = qcf.double_vec()
    for t in df.itertuples():
        lvec.append(int(t.plazo))
        if t.Index == vertice:
            vec_sens_up.append(t.tasa + bp)
            vec_sens_down.append(t.tasa - bp)
        else:
            vec_sens_up.append(t.tasa)
            vec_sens_down.append(t.tasa)

    zcc_sens_up = qcf.QCCurve(lvec, vec_sens_up)
    lin_sens_up = qcf.QCLinearInterpolator(zcc_sens_up)
    zz_sens_up = qcf.ZeroCouponCurve(lin_sens_up, tasa)

    zcc_sens_down = qcf.QCCurve(lvec, vec_sens_down)
    lin_sens_down = qcf.QCLinearInterpolator(zcc_sens_down)
    zz_sens_down = qcf.ZeroCouponCurve(lin_sens_down, tasa)
    
    return zz_sens_up, zz_sens_down
```


```python
zcc_clp_up, zcc_clp_down = curvas_sens(curva_clp, tasa, vertice, bp)
zcc_usd_up, zcc_usd_down = curvas_sens(curva_usd, tasa, vertice, bp)
zcc_clf_up, zcc_clf_down = curvas_sens(curva_clf, tasa, vertice, bp)
```

### FixedRateCashflow Leg

Se da de alta una pata fija:


```python
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(31, 1, 2024)
fecha_final = qcf.QCDate(31, 1, 2025)
bus_adj_rule = qcf.BusyAdjRules.MODFOLLOW
periodicidad = qcf.Tenor('6M')
periodo_irregular = qcf.StubPeriod.SHORTFRONT
calendario = qcf.BusinessCalendar(fecha_inicio, 20)
lag_pago = 0
nominal = 20_000_000.0
amort_es_flujo = True
valor_tasa_fija = .01774
tasa_cupon = qcf.QCInterestRate(
    valor_tasa_fija, 
    qcf.QC30360(), 
    qcf.QCLinearWf()
)
moneda = qcf.QCUSD()
es_bono = False

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


```python
aux.leg_as_dataframe(fixed_rate_leg).style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_0db0a">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_0db0a_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_0db0a_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_0db0a_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_0db0a_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_0db0a_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_0db0a_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_0db0a_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_0db0a_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_0db0a_level0_col8" class="col_heading level0 col8" >moneda</th>
      <th id="T_0db0a_level0_col9" class="col_heading level0 col9" >valor_tasa</th>
      <th id="T_0db0a_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_0db0a_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_0db0a_row0_col0" class="data row0 col0" >2024-01-31</td>
      <td id="T_0db0a_row0_col1" class="data row0 col1" >2024-07-31</td>
      <td id="T_0db0a_row0_col2" class="data row0 col2" >2024-07-31</td>
      <td id="T_0db0a_row0_col3" class="data row0 col3" >20,000,000.00</td>
      <td id="T_0db0a_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_0db0a_row0_col5" class="data row0 col5" >177,400.00</td>
      <td id="T_0db0a_row0_col6" class="data row0 col6" >True</td>
      <td id="T_0db0a_row0_col7" class="data row0 col7" >177,400.00</td>
      <td id="T_0db0a_row0_col8" class="data row0 col8" >USD</td>
      <td id="T_0db0a_row0_col9" class="data row0 col9" >1.7740%</td>
      <td id="T_0db0a_row0_col10" class="data row0 col10" >Lin30360</td>
    </tr>
    <tr>
      <th id="T_0db0a_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_0db0a_row1_col0" class="data row1 col0" >2024-07-31</td>
      <td id="T_0db0a_row1_col1" class="data row1 col1" >2025-01-31</td>
      <td id="T_0db0a_row1_col2" class="data row1 col2" >2025-01-31</td>
      <td id="T_0db0a_row1_col3" class="data row1 col3" >20,000,000.00</td>
      <td id="T_0db0a_row1_col4" class="data row1 col4" >20,000,000.00</td>
      <td id="T_0db0a_row1_col5" class="data row1 col5" >177,400.00</td>
      <td id="T_0db0a_row1_col6" class="data row1 col6" >True</td>
      <td id="T_0db0a_row1_col7" class="data row1 col7" >20,177,400.00</td>
      <td id="T_0db0a_row1_col8" class="data row1 col8" >USD</td>
      <td id="T_0db0a_row1_col9" class="data row1 col9" >1.7740%</td>
      <td id="T_0db0a_row1_col10" class="data row1 col10" >Lin30360</td>
    </tr>
  </tbody>
</table>




Se calcula ahora el valor presente:


```python
vp_fija = pv.pv(fecha_hoy, fixed_rate_leg, zcc_usd)
print(f"Valor presente de la pata fija es: {vp_fija:,.0f}")
```

    Valor presente de la pata fija es: 20,017,705


Al calcular el valor presente, también se calculan las derivadas del valor presente respecto a cada uno de los vértices de la curva.


```python
der = pv.get_derivatives()
```

Con esas derivadas, se puede calcular la sensibilidad a la curva cupón cero a un movimiento de 1 punto básico.


```python
i = 0
total = 0
for d in der:
    total += d * bp / 10_000
    print(f"Sensibilidad en {i}: {d * bp / 10_000:0,.0f}")
    i += 1
print(f"Sensibilidad total: {total:,.0f}")
```

    Sensibilidad en 0: 0
    Sensibilidad en 1: 0
    Sensibilidad en 2: 0
    Sensibilidad en 3: 0
    Sensibilidad en 4: 0
    Sensibilidad en 5: 0
    Sensibilidad en 6: 0
    Sensibilidad en 7: 0
    Sensibilidad en 8: 0
    Sensibilidad en 9: -9
    Sensibilidad en 10: 0
    Sensibilidad en 11: 0
    Sensibilidad en 12: 0
    Sensibilidad en 13: 0
    Sensibilidad en 14: -62
    Sensibilidad en 15: -1,927
    Sensibilidad en 16: 0
    Sensibilidad en 17: 0
    Sensibilidad en 18: 0
    Sensibilidad en 19: 0
    Sensibilidad en 20: 0
    Sensibilidad en 21: 0
    Sensibilidad en 22: 0
    Sensibilidad en 23: 0
    Sensibilidad en 24: 0
    Sensibilidad en 25: 0
    Sensibilidad en 26: 0
    Sensibilidad en 27: 0
    Sensibilidad total: -1,998


Se puede verificar la sensibilidad por diferencias finitas.

Se calcula el valor presente con las curvas desplazadas.


```python
vp_fija_sens_up = pv.pv(fecha_hoy, fixed_rate_leg, zcc_usd_up)
vp_fija_sens_down = pv.pv(fecha_hoy, fixed_rate_leg, zcc_usd_down)
print(f"Valor presente up de la pata fija es: {vp_fija_sens_up:,.4f}")
print(f"Valor presente down de la pata fija es: {vp_fija_sens_down:,.4f}")
```

    Valor presente up de la pata fija es: 20,015,777.5553
    Valor presente down de la pata fija es: 20,019,632.4437


Finalmente, se calcula la sensibilidad (usando la aproximación central por diferencias finitas).


```python
print(f"Sensibilidad por diferencias finitas: {(vp_fija_sens_up - vp_fija_sens_down) / 2:,.0f}")
```

    Sensibilidad por diferencias finitas: -1,927


### OvernightIndex Leg

Se da de alta una pata OvernightIndex.


```python
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(10,1,2019)
fecha_final = qcf.QCDate(10,7,2029)
bus_adj_rule = qcf.BusyAdjRules.FOLLOW
fix_adj_rule = qcf.BusyAdjRules.PREVIOUS
dates_for_eq_rate = qcf.DatesForEquivalentRate.ACCRUAL
periodicidad_pago = qcf.Tenor('2Y')
periodo_irregular_pago = qcf.StubPeriod.SHORTFRONT
calendario = qcf.BusinessCalendar(fecha_inicio, 20)
lag_pago = 0
nominal = 38_000_000_000.0
amort_es_flujo = True
spread = .0
gearing = 1.0

overnight_index_leg = qcf.LegFactory.build_bullet_overnight_index_leg(
    rec_pay=rp,
    start_date=fecha_inicio,
    end_date=fecha_final,
    bus_adj_rule=bus_adj_rule,
    fix_adj_rule=fix_adj_rule,
    settlement_periodicity=periodicidad_pago,
    stub_period=periodo_irregular_pago,
    settlement_calendar=calendario,
    fixing_calendar=calendario,
    settlement_lag=lag_pago,
    initial_notional=nominal,
    amort_is_cashflow=amort_es_flujo,
    spread=spread,
    gearing=gearing,
    interest_rate=qcf.QCInterestRate(0.0, qcf.QCAct360(), qcf.QCLinearWf()),
    index_name='ICPCLP',
    eq_rate_decimal_places=2,
    notional_currency=qcf.QCCLP(),
    dates_for_eq_rate=dates_for_eq_rate,
)
```


```python
aux.leg_as_dataframe(overnight_index_leg).style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_f4938">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_f4938_level0_col0" class="col_heading level0 col0" >fecha_inicial_devengo</th>
      <th id="T_f4938_level0_col1" class="col_heading level0 col1" >fecha_final_devengo</th>
      <th id="T_f4938_level0_col2" class="col_heading level0 col2" >fecha_inicial_indice</th>
      <th id="T_f4938_level0_col3" class="col_heading level0 col3" >fecha_final_indice</th>
      <th id="T_f4938_level0_col4" class="col_heading level0 col4" >fecha_pago</th>
      <th id="T_f4938_level0_col5" class="col_heading level0 col5" >nocional</th>
      <th id="T_f4938_level0_col6" class="col_heading level0 col6" >amortizacion</th>
      <th id="T_f4938_level0_col7" class="col_heading level0 col7" >amort_es_flujo</th>
      <th id="T_f4938_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_f4938_level0_col9" class="col_heading level0 col9" >nombre_indice</th>
      <th id="T_f4938_level0_col10" class="col_heading level0 col10" >valor_indice_inicial</th>
      <th id="T_f4938_level0_col11" class="col_heading level0 col11" >valor_indice_final</th>
      <th id="T_f4938_level0_col12" class="col_heading level0 col12" >valor_tasa_equivalente</th>
      <th id="T_f4938_level0_col13" class="col_heading level0 col13" >tipo_tasa</th>
      <th id="T_f4938_level0_col14" class="col_heading level0 col14" >interes</th>
      <th id="T_f4938_level0_col15" class="col_heading level0 col15" >flujo</th>
      <th id="T_f4938_level0_col16" class="col_heading level0 col16" >spread</th>
      <th id="T_f4938_level0_col17" class="col_heading level0 col17" >gearing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_f4938_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_f4938_row0_col0" class="data row0 col0" >2019-01-10</td>
      <td id="T_f4938_row0_col1" class="data row0 col1" >2019-07-10</td>
      <td id="T_f4938_row0_col2" class="data row0 col2" >2019-01-10</td>
      <td id="T_f4938_row0_col3" class="data row0 col3" >2019-07-10</td>
      <td id="T_f4938_row0_col4" class="data row0 col4" >2019-07-10</td>
      <td id="T_f4938_row0_col5" class="data row0 col5" >38,000,000,000.00</td>
      <td id="T_f4938_row0_col6" class="data row0 col6" >0.00</td>
      <td id="T_f4938_row0_col7" class="data row0 col7" >True</td>
      <td id="T_f4938_row0_col8" class="data row0 col8" >CLP</td>
      <td id="T_f4938_row0_col9" class="data row0 col9" >ICPCLP</td>
      <td id="T_f4938_row0_col10" class="data row0 col10" >1.00</td>
      <td id="T_f4938_row0_col11" class="data row0 col11" >1.00</td>
      <td id="T_f4938_row0_col12" class="data row0 col12" >0.0000%</td>
      <td id="T_f4938_row0_col13" class="data row0 col13" >LinAct360</td>
      <td id="T_f4938_row0_col14" class="data row0 col14" >0.00</td>
      <td id="T_f4938_row0_col15" class="data row0 col15" >0.00</td>
      <td id="T_f4938_row0_col16" class="data row0 col16" >0.0000%</td>
      <td id="T_f4938_row0_col17" class="data row0 col17" >1.00</td>
    </tr>
    <tr>
      <th id="T_f4938_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_f4938_row1_col0" class="data row1 col0" >2019-07-10</td>
      <td id="T_f4938_row1_col1" class="data row1 col1" >2021-07-12</td>
      <td id="T_f4938_row1_col2" class="data row1 col2" >2019-07-10</td>
      <td id="T_f4938_row1_col3" class="data row1 col3" >2021-07-12</td>
      <td id="T_f4938_row1_col4" class="data row1 col4" >2021-07-12</td>
      <td id="T_f4938_row1_col5" class="data row1 col5" >38,000,000,000.00</td>
      <td id="T_f4938_row1_col6" class="data row1 col6" >0.00</td>
      <td id="T_f4938_row1_col7" class="data row1 col7" >True</td>
      <td id="T_f4938_row1_col8" class="data row1 col8" >CLP</td>
      <td id="T_f4938_row1_col9" class="data row1 col9" >ICPCLP</td>
      <td id="T_f4938_row1_col10" class="data row1 col10" >1.00</td>
      <td id="T_f4938_row1_col11" class="data row1 col11" >1.00</td>
      <td id="T_f4938_row1_col12" class="data row1 col12" >0.0000%</td>
      <td id="T_f4938_row1_col13" class="data row1 col13" >LinAct360</td>
      <td id="T_f4938_row1_col14" class="data row1 col14" >0.00</td>
      <td id="T_f4938_row1_col15" class="data row1 col15" >0.00</td>
      <td id="T_f4938_row1_col16" class="data row1 col16" >0.0000%</td>
      <td id="T_f4938_row1_col17" class="data row1 col17" >1.00</td>
    </tr>
    <tr>
      <th id="T_f4938_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_f4938_row2_col0" class="data row2 col0" >2021-07-12</td>
      <td id="T_f4938_row2_col1" class="data row2 col1" >2023-07-10</td>
      <td id="T_f4938_row2_col2" class="data row2 col2" >2021-07-12</td>
      <td id="T_f4938_row2_col3" class="data row2 col3" >2023-07-10</td>
      <td id="T_f4938_row2_col4" class="data row2 col4" >2023-07-10</td>
      <td id="T_f4938_row2_col5" class="data row2 col5" >38,000,000,000.00</td>
      <td id="T_f4938_row2_col6" class="data row2 col6" >0.00</td>
      <td id="T_f4938_row2_col7" class="data row2 col7" >True</td>
      <td id="T_f4938_row2_col8" class="data row2 col8" >CLP</td>
      <td id="T_f4938_row2_col9" class="data row2 col9" >ICPCLP</td>
      <td id="T_f4938_row2_col10" class="data row2 col10" >1.00</td>
      <td id="T_f4938_row2_col11" class="data row2 col11" >1.00</td>
      <td id="T_f4938_row2_col12" class="data row2 col12" >0.0000%</td>
      <td id="T_f4938_row2_col13" class="data row2 col13" >LinAct360</td>
      <td id="T_f4938_row2_col14" class="data row2 col14" >0.00</td>
      <td id="T_f4938_row2_col15" class="data row2 col15" >0.00</td>
      <td id="T_f4938_row2_col16" class="data row2 col16" >0.0000%</td>
      <td id="T_f4938_row2_col17" class="data row2 col17" >1.00</td>
    </tr>
    <tr>
      <th id="T_f4938_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_f4938_row3_col0" class="data row3 col0" >2023-07-10</td>
      <td id="T_f4938_row3_col1" class="data row3 col1" >2025-07-10</td>
      <td id="T_f4938_row3_col2" class="data row3 col2" >2023-07-10</td>
      <td id="T_f4938_row3_col3" class="data row3 col3" >2025-07-10</td>
      <td id="T_f4938_row3_col4" class="data row3 col4" >2025-07-10</td>
      <td id="T_f4938_row3_col5" class="data row3 col5" >38,000,000,000.00</td>
      <td id="T_f4938_row3_col6" class="data row3 col6" >0.00</td>
      <td id="T_f4938_row3_col7" class="data row3 col7" >True</td>
      <td id="T_f4938_row3_col8" class="data row3 col8" >CLP</td>
      <td id="T_f4938_row3_col9" class="data row3 col9" >ICPCLP</td>
      <td id="T_f4938_row3_col10" class="data row3 col10" >1.00</td>
      <td id="T_f4938_row3_col11" class="data row3 col11" >1.00</td>
      <td id="T_f4938_row3_col12" class="data row3 col12" >0.0000%</td>
      <td id="T_f4938_row3_col13" class="data row3 col13" >LinAct360</td>
      <td id="T_f4938_row3_col14" class="data row3 col14" >0.00</td>
      <td id="T_f4938_row3_col15" class="data row3 col15" >0.00</td>
      <td id="T_f4938_row3_col16" class="data row3 col16" >0.0000%</td>
      <td id="T_f4938_row3_col17" class="data row3 col17" >1.00</td>
    </tr>
    <tr>
      <th id="T_f4938_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_f4938_row4_col0" class="data row4 col0" >2025-07-10</td>
      <td id="T_f4938_row4_col1" class="data row4 col1" >2027-07-12</td>
      <td id="T_f4938_row4_col2" class="data row4 col2" >2025-07-10</td>
      <td id="T_f4938_row4_col3" class="data row4 col3" >2027-07-12</td>
      <td id="T_f4938_row4_col4" class="data row4 col4" >2027-07-12</td>
      <td id="T_f4938_row4_col5" class="data row4 col5" >38,000,000,000.00</td>
      <td id="T_f4938_row4_col6" class="data row4 col6" >0.00</td>
      <td id="T_f4938_row4_col7" class="data row4 col7" >True</td>
      <td id="T_f4938_row4_col8" class="data row4 col8" >CLP</td>
      <td id="T_f4938_row4_col9" class="data row4 col9" >ICPCLP</td>
      <td id="T_f4938_row4_col10" class="data row4 col10" >1.00</td>
      <td id="T_f4938_row4_col11" class="data row4 col11" >1.00</td>
      <td id="T_f4938_row4_col12" class="data row4 col12" >0.0000%</td>
      <td id="T_f4938_row4_col13" class="data row4 col13" >LinAct360</td>
      <td id="T_f4938_row4_col14" class="data row4 col14" >0.00</td>
      <td id="T_f4938_row4_col15" class="data row4 col15" >0.00</td>
      <td id="T_f4938_row4_col16" class="data row4 col16" >0.0000%</td>
      <td id="T_f4938_row4_col17" class="data row4 col17" >1.00</td>
    </tr>
    <tr>
      <th id="T_f4938_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_f4938_row5_col0" class="data row5 col0" >2027-07-12</td>
      <td id="T_f4938_row5_col1" class="data row5 col1" >2029-07-10</td>
      <td id="T_f4938_row5_col2" class="data row5 col2" >2027-07-12</td>
      <td id="T_f4938_row5_col3" class="data row5 col3" >2029-07-10</td>
      <td id="T_f4938_row5_col4" class="data row5 col4" >2029-07-10</td>
      <td id="T_f4938_row5_col5" class="data row5 col5" >38,000,000,000.00</td>
      <td id="T_f4938_row5_col6" class="data row5 col6" >38,000,000,000.00</td>
      <td id="T_f4938_row5_col7" class="data row5 col7" >True</td>
      <td id="T_f4938_row5_col8" class="data row5 col8" >CLP</td>
      <td id="T_f4938_row5_col9" class="data row5 col9" >ICPCLP</td>
      <td id="T_f4938_row5_col10" class="data row5 col10" >1.00</td>
      <td id="T_f4938_row5_col11" class="data row5 col11" >1.00</td>
      <td id="T_f4938_row5_col12" class="data row5 col12" >0.0000%</td>
      <td id="T_f4938_row5_col13" class="data row5 col13" >LinAct360</td>
      <td id="T_f4938_row5_col14" class="data row5 col14" >0.00</td>
      <td id="T_f4938_row5_col15" class="data row5 col15" >38,000,000,000.00</td>
      <td id="T_f4938_row5_col16" class="data row5 col16" >0.0000%</td>
      <td id="T_f4938_row5_col17" class="data row5 col17" >1.00</td>
    </tr>
  </tbody>
</table>




Notar que al dar de alta un Leg con OvernightIndexCashflow, los valores futuros de los índeces son los default (=1.0). Por lo tanto, el primer paso para valorizar estos cashflows, es calcular los valores forward de los índices.

Se da de alta un objeto de tipo `ForwardRates`.


```python
fwd_rates = qcf.ForwardRates()
```

Se calculan los índices forward.


```python
icp_val = 18_890.34 # icp a la fecha de proceso
fecha_hoy = qcf.QCDate(5, 3, 2020)

for i in range(overnight_index_leg.size()):
    cashflow = overnight_index_leg.get_cashflow_at(i)
    if cashflow.get_start_date() <= fecha_hoy <= cashflow.get_end_date():
        index = i

icp_fecha_inicio_cupon_vigente = 18_376.69
overnight_index_leg.get_cashflow_at(index).set_start_date_index(icp_fecha_inicio_cupon_vigente)

fwd_rates.set_rates_overnight_index_leg(fecha_hoy, icp_val, overnight_index_leg, zcc_clp)
```


```python
aux.leg_as_dataframe(overnight_index_leg).style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_732bb">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_732bb_level0_col0" class="col_heading level0 col0" >fecha_inicial_devengo</th>
      <th id="T_732bb_level0_col1" class="col_heading level0 col1" >fecha_final_devengo</th>
      <th id="T_732bb_level0_col2" class="col_heading level0 col2" >fecha_inicial_indice</th>
      <th id="T_732bb_level0_col3" class="col_heading level0 col3" >fecha_final_indice</th>
      <th id="T_732bb_level0_col4" class="col_heading level0 col4" >fecha_pago</th>
      <th id="T_732bb_level0_col5" class="col_heading level0 col5" >nocional</th>
      <th id="T_732bb_level0_col6" class="col_heading level0 col6" >amortizacion</th>
      <th id="T_732bb_level0_col7" class="col_heading level0 col7" >amort_es_flujo</th>
      <th id="T_732bb_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_732bb_level0_col9" class="col_heading level0 col9" >nombre_indice</th>
      <th id="T_732bb_level0_col10" class="col_heading level0 col10" >valor_indice_inicial</th>
      <th id="T_732bb_level0_col11" class="col_heading level0 col11" >valor_indice_final</th>
      <th id="T_732bb_level0_col12" class="col_heading level0 col12" >valor_tasa_equivalente</th>
      <th id="T_732bb_level0_col13" class="col_heading level0 col13" >tipo_tasa</th>
      <th id="T_732bb_level0_col14" class="col_heading level0 col14" >interes</th>
      <th id="T_732bb_level0_col15" class="col_heading level0 col15" >flujo</th>
      <th id="T_732bb_level0_col16" class="col_heading level0 col16" >spread</th>
      <th id="T_732bb_level0_col17" class="col_heading level0 col17" >gearing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_732bb_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_732bb_row0_col0" class="data row0 col0" >2019-01-10</td>
      <td id="T_732bb_row0_col1" class="data row0 col1" >2019-07-10</td>
      <td id="T_732bb_row0_col2" class="data row0 col2" >2019-01-10</td>
      <td id="T_732bb_row0_col3" class="data row0 col3" >2019-07-10</td>
      <td id="T_732bb_row0_col4" class="data row0 col4" >2019-07-10</td>
      <td id="T_732bb_row0_col5" class="data row0 col5" >38,000,000,000.00</td>
      <td id="T_732bb_row0_col6" class="data row0 col6" >0.00</td>
      <td id="T_732bb_row0_col7" class="data row0 col7" >True</td>
      <td id="T_732bb_row0_col8" class="data row0 col8" >CLP</td>
      <td id="T_732bb_row0_col9" class="data row0 col9" >ICPCLP</td>
      <td id="T_732bb_row0_col10" class="data row0 col10" >1.00</td>
      <td id="T_732bb_row0_col11" class="data row0 col11" >1.00</td>
      <td id="T_732bb_row0_col12" class="data row0 col12" >0.0000%</td>
      <td id="T_732bb_row0_col13" class="data row0 col13" >LinAct360</td>
      <td id="T_732bb_row0_col14" class="data row0 col14" >0.00</td>
      <td id="T_732bb_row0_col15" class="data row0 col15" >0.00</td>
      <td id="T_732bb_row0_col16" class="data row0 col16" >0.0000%</td>
      <td id="T_732bb_row0_col17" class="data row0 col17" >1.00</td>
    </tr>
    <tr>
      <th id="T_732bb_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_732bb_row1_col0" class="data row1 col0" >2019-07-10</td>
      <td id="T_732bb_row1_col1" class="data row1 col1" >2021-07-12</td>
      <td id="T_732bb_row1_col2" class="data row1 col2" >2019-07-10</td>
      <td id="T_732bb_row1_col3" class="data row1 col3" >2021-07-12</td>
      <td id="T_732bb_row1_col4" class="data row1 col4" >2021-07-12</td>
      <td id="T_732bb_row1_col5" class="data row1 col5" >38,000,000,000.00</td>
      <td id="T_732bb_row1_col6" class="data row1 col6" >0.00</td>
      <td id="T_732bb_row1_col7" class="data row1 col7" >True</td>
      <td id="T_732bb_row1_col8" class="data row1 col8" >CLP</td>
      <td id="T_732bb_row1_col9" class="data row1 col9" >ICPCLP</td>
      <td id="T_732bb_row1_col10" class="data row1 col10" >18,376.69</td>
      <td id="T_732bb_row1_col11" class="data row1 col11" >19,226.28</td>
      <td id="T_732bb_row1_col12" class="data row1 col12" >2.0000%</td>
      <td id="T_732bb_row1_col13" class="data row1 col13" >LinAct360</td>
      <td id="T_732bb_row1_col14" class="data row1 col14" >1,547,444,444.44</td>
      <td id="T_732bb_row1_col15" class="data row1 col15" >1,547,444,444.44</td>
      <td id="T_732bb_row1_col16" class="data row1 col16" >0.0000%</td>
      <td id="T_732bb_row1_col17" class="data row1 col17" >1.00</td>
    </tr>
    <tr>
      <th id="T_732bb_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_732bb_row2_col0" class="data row2 col0" >2021-07-12</td>
      <td id="T_732bb_row2_col1" class="data row2 col1" >2023-07-10</td>
      <td id="T_732bb_row2_col2" class="data row2 col2" >2021-07-12</td>
      <td id="T_732bb_row2_col3" class="data row2 col3" >2023-07-10</td>
      <td id="T_732bb_row2_col4" class="data row2 col4" >2023-07-10</td>
      <td id="T_732bb_row2_col5" class="data row2 col5" >38,000,000,000.00</td>
      <td id="T_732bb_row2_col6" class="data row2 col6" >0.00</td>
      <td id="T_732bb_row2_col7" class="data row2 col7" >True</td>
      <td id="T_732bb_row2_col8" class="data row2 col8" >CLP</td>
      <td id="T_732bb_row2_col9" class="data row2 col9" >ICPCLP</td>
      <td id="T_732bb_row2_col10" class="data row2 col10" >19,226.28</td>
      <td id="T_732bb_row2_col11" class="data row2 col11" >19,877.30</td>
      <td id="T_732bb_row2_col12" class="data row2 col12" >2.0000%</td>
      <td id="T_732bb_row2_col13" class="data row2 col13" >LinAct360</td>
      <td id="T_732bb_row2_col14" class="data row2 col14" >1,536,888,888.89</td>
      <td id="T_732bb_row2_col15" class="data row2 col15" >1,536,888,888.89</td>
      <td id="T_732bb_row2_col16" class="data row2 col16" >0.0000%</td>
      <td id="T_732bb_row2_col17" class="data row2 col17" >1.00</td>
    </tr>
    <tr>
      <th id="T_732bb_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_732bb_row3_col0" class="data row3 col0" >2023-07-10</td>
      <td id="T_732bb_row3_col1" class="data row3 col1" >2025-07-10</td>
      <td id="T_732bb_row3_col2" class="data row3 col2" >2023-07-10</td>
      <td id="T_732bb_row3_col3" class="data row3 col3" >2025-07-10</td>
      <td id="T_732bb_row3_col4" class="data row3 col4" >2025-07-10</td>
      <td id="T_732bb_row3_col5" class="data row3 col5" >38,000,000,000.00</td>
      <td id="T_732bb_row3_col6" class="data row3 col6" >0.00</td>
      <td id="T_732bb_row3_col7" class="data row3 col7" >True</td>
      <td id="T_732bb_row3_col8" class="data row3 col8" >CLP</td>
      <td id="T_732bb_row3_col9" class="data row3 col9" >ICPCLP</td>
      <td id="T_732bb_row3_col10" class="data row3 col10" >19,877.30</td>
      <td id="T_732bb_row3_col11" class="data row3 col11" >21,118.61</td>
      <td id="T_732bb_row3_col12" class="data row3 col12" >3.0000%</td>
      <td id="T_732bb_row3_col13" class="data row3 col13" >LinAct360</td>
      <td id="T_732bb_row3_col14" class="data row3 col14" >2,314,833,333.33</td>
      <td id="T_732bb_row3_col15" class="data row3 col15" >2,314,833,333.33</td>
      <td id="T_732bb_row3_col16" class="data row3 col16" >0.0000%</td>
      <td id="T_732bb_row3_col17" class="data row3 col17" >1.00</td>
    </tr>
    <tr>
      <th id="T_732bb_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_732bb_row4_col0" class="data row4 col0" >2025-07-10</td>
      <td id="T_732bb_row4_col1" class="data row4 col1" >2027-07-12</td>
      <td id="T_732bb_row4_col2" class="data row4 col2" >2025-07-10</td>
      <td id="T_732bb_row4_col3" class="data row4 col3" >2027-07-12</td>
      <td id="T_732bb_row4_col4" class="data row4 col4" >2027-07-12</td>
      <td id="T_732bb_row4_col5" class="data row4 col5" >38,000,000,000.00</td>
      <td id="T_732bb_row4_col6" class="data row4 col6" >0.00</td>
      <td id="T_732bb_row4_col7" class="data row4 col7" >True</td>
      <td id="T_732bb_row4_col8" class="data row4 col8" >CLP</td>
      <td id="T_732bb_row4_col9" class="data row4 col9" >ICPCLP</td>
      <td id="T_732bb_row4_col10" class="data row4 col10" >21,118.61</td>
      <td id="T_732bb_row4_col11" class="data row4 col11" >22,978.68</td>
      <td id="T_732bb_row4_col12" class="data row4 col12" >4.0000%</td>
      <td id="T_732bb_row4_col13" class="data row4 col13" >LinAct360</td>
      <td id="T_732bb_row4_col14" class="data row4 col14" >3,090,666,666.67</td>
      <td id="T_732bb_row4_col15" class="data row4 col15" >3,090,666,666.67</td>
      <td id="T_732bb_row4_col16" class="data row4 col16" >0.0000%</td>
      <td id="T_732bb_row4_col17" class="data row4 col17" >1.00</td>
    </tr>
    <tr>
      <th id="T_732bb_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_732bb_row5_col0" class="data row5 col0" >2027-07-12</td>
      <td id="T_732bb_row5_col1" class="data row5 col1" >2029-07-10</td>
      <td id="T_732bb_row5_col2" class="data row5 col2" >2027-07-12</td>
      <td id="T_732bb_row5_col3" class="data row5 col3" >2029-07-10</td>
      <td id="T_732bb_row5_col4" class="data row5 col4" >2029-07-10</td>
      <td id="T_732bb_row5_col5" class="data row5 col5" >38,000,000,000.00</td>
      <td id="T_732bb_row5_col6" class="data row5 col6" >38,000,000,000.00</td>
      <td id="T_732bb_row5_col7" class="data row5 col7" >True</td>
      <td id="T_732bb_row5_col8" class="data row5 col8" >CLP</td>
      <td id="T_732bb_row5_col9" class="data row5 col9" >ICPCLP</td>
      <td id="T_732bb_row5_col10" class="data row5 col10" >22,978.68</td>
      <td id="T_732bb_row5_col11" class="data row5 col11" >25,238.13</td>
      <td id="T_732bb_row5_col12" class="data row5 col12" >5.0000%</td>
      <td id="T_732bb_row5_col13" class="data row5 col13" >LinAct360</td>
      <td id="T_732bb_row5_col14" class="data row5 col14" >3,847,500,000.00</td>
      <td id="T_732bb_row5_col15" class="data row5 col15" >41,847,500,000.00</td>
      <td id="T_732bb_row5_col16" class="data row5 col16" >0.0000%</td>
      <td id="T_732bb_row5_col17" class="data row5 col17" >1.00</td>
    </tr>
  </tbody>
</table>




Con esto, podemos calcular el valor presente.


```python
vp_on_index_leg = pv.pv(fecha_hoy, overnight_index_leg, zcc_clp)
print(f"Valor presente pata ON Index Leg: {vp_on_index_leg:,.0f}")
```

    Valor presente pata ON Index Leg: 39,062,144,488


También en este caso es posible calcular la sensibilidad a la curva de descuento.


```python
der = pv.get_derivatives()
i = 0
for d in der:
    print(f"Sensibilidad en {i:}: {d * bp / 10_000:0,.0f}")
    i += 1
sens_disc = [d * bp / 10_000 for d in der]
print()
print("Sensibilidad de descuento: {0:,.0f} CLP".format(sum(sens_disc)))
```

    Sensibilidad en 0: 0
    Sensibilidad en 1: 0
    Sensibilidad en 2: 0
    Sensibilidad en 3: 0
    Sensibilidad en 4: 0
    Sensibilidad en 5: -74,910
    Sensibilidad en 6: -158,708
    Sensibilidad en 7: 0
    Sensibilidad en 8: -271,813
    Sensibilidad en 9: -137,584
    Sensibilidad en 10: -753,029
    Sensibilidad en 11: -382,738
    Sensibilidad en 12: -1,332,749
    Sensibilidad en 13: -691,260
    Sensibilidad en 14: -19,372,761
    Sensibilidad en 15: -9,846,486
    Sensibilidad en 16: 0
    Sensibilidad en 17: 0
    Sensibilidad en 18: 0
    
    Sensibilidad de descuento: -33,022,037 CLP


La estructura es la misma que para una pata fija, lo que indica que se debe también incluir la sensibilidad a la curva de proyección.


```python
result = []
for i in range(overnight_index_leg.size()):
    cshflw = overnight_index_leg.get_cashflow_at(i)
    amt_der = cshflw.get_amount_derivatives()
    df = zcc_clp.get_discount_factor_at(fecha_hoy.day_diff(cshflw.get_settlement_date()))
    amt_der = [a * bp / 10_000  * df for a in amt_der]
    if len(amt_der) > 0:
        result.append(np.array(amt_der))
total = result[0] * 0

for r in result:
    total += r

for i in range(len(total)):
    print("Sensibilidad en {0:}: {1:0,.0f}".format(i, total[i]))

print()
print("Sensibilidad de proyección: {0:,.0f} CLP".format(sum(total)))
```

    Sensibilidad en 0: 0
    Sensibilidad en 1: 0
    Sensibilidad en 2: 0
    Sensibilidad en 3: 0
    Sensibilidad en 4: 0
    Sensibilidad en 5: 74,910
    Sensibilidad en 6: 158,708
    Sensibilidad en 7: 0
    Sensibilidad en 8: 271,813
    Sensibilidad en 9: 137,584
    Sensibilidad en 10: 753,029
    Sensibilidad en 11: 382,738
    Sensibilidad en 12: 1,332,749
    Sensibilidad en 13: 691,260
    Sensibilidad en 14: 19,372,761
    Sensibilidad en 15: 9,846,486
    Sensibilidad en 16: 0
    Sensibilidad en 17: 0
    Sensibilidad en 18: 0
    
    Sensibilidad de proyección: 33,022,037 CLP


Como se espera de una pata OvernightIndex (con lag de pago igual a 0 y spread igual a 0), ambas sensibilidades se cancelan.

#### Se verifica la sensibilidad de proyección por diferencias finitas:


```python
fwd_rates.set_rates_overnight_index_leg(fecha_hoy, icp_val, overnight_index_leg, zcc_clp_up)
vp_on_index_leg_up = pv.pv(fecha_hoy, overnight_index_leg, zcc_clp)

fwd_rates.set_rates_overnight_index_leg(fecha_hoy, icp_val, overnight_index_leg, zcc_clp_down)
vp_on_index_leg_down = pv.pv(fecha_hoy, overnight_index_leg, zcc_clp)

print(f"Sensibilidad en vértice {vertice}: {(vp_on_index_leg_up - vp_on_index_leg_down) / 2:,.0f} CLP")
```

    Sensibilidad en vértice 15: 9,846,486 CLP


### IborCashflow Leg

Se da de alta una pata de tipo IborCashflow.


```python
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(12, 11, 2019)
fecha_final = qcf.QCDate(12, 5, 2021)
bus_adj_rule = qcf.BusyAdjRules.MODFOLLOW
periodicidad_pago = qcf.Tenor('6M')
periodo_irregular_pago = qcf.StubPeriod.NO
calendario = qcf.BusinessCalendar(fecha_inicio, 20)
lag_pago = 0
periodicidad_fijacion = qcf.Tenor('6M')
periodo_irregular_fijacion = qcf.StubPeriod.NO

# vamos a usar el mismo calendario para pago y fijaciones
lag_de_fijacion = 2

# Definición del índice
codigo = 'TERSOFR6M'
lin_act360 = qcf.QCInterestRate(.0, qcf.QCAct360(), qcf.QCLinearWf())
fixing_lag = qcf.Tenor('2d')
tenor = qcf.Tenor('6m')
fixing_calendar = calendario
settlement_calendar = calendario
usd = qcf.QCUSD()
termsofr_6m = qcf.InterestRateIndex(
    codigo,
    lin_act360,
    fixing_lag,
    tenor,
    fixing_calendar,
    settlement_calendar,
    usd
)
# Fin índice

nominal = 20_000_000.0
amort_es_flujo = True
moneda = usd
spread = .0
gearing = 1.0

ibor_leg = qcf.LegFactory.build_bullet_ibor_leg(
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
    termsofr_6m,
    nominal, 
    amort_es_flujo, 
    moneda, 
    spread, 
    gearing
)
```


```python
aux.leg_as_dataframe(ibor_leg).style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_3c73b">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_3c73b_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_3c73b_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_3c73b_level0_col2" class="col_heading level0 col2" >fecha_fixing</th>
      <th id="T_3c73b_level0_col3" class="col_heading level0 col3" >fecha_pago</th>
      <th id="T_3c73b_level0_col4" class="col_heading level0 col4" >nominal</th>
      <th id="T_3c73b_level0_col5" class="col_heading level0 col5" >amortizacion</th>
      <th id="T_3c73b_level0_col6" class="col_heading level0 col6" >interes</th>
      <th id="T_3c73b_level0_col7" class="col_heading level0 col7" >amort_es_flujo</th>
      <th id="T_3c73b_level0_col8" class="col_heading level0 col8" >flujo</th>
      <th id="T_3c73b_level0_col9" class="col_heading level0 col9" >moneda</th>
      <th id="T_3c73b_level0_col10" class="col_heading level0 col10" >codigo_indice_tasa</th>
      <th id="T_3c73b_level0_col11" class="col_heading level0 col11" >valor_tasa</th>
      <th id="T_3c73b_level0_col12" class="col_heading level0 col12" >spread</th>
      <th id="T_3c73b_level0_col13" class="col_heading level0 col13" >gearing</th>
      <th id="T_3c73b_level0_col14" class="col_heading level0 col14" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_3c73b_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_3c73b_row0_col0" class="data row0 col0" >2019-11-12</td>
      <td id="T_3c73b_row0_col1" class="data row0 col1" >2020-05-12</td>
      <td id="T_3c73b_row0_col2" class="data row0 col2" >2019-11-08</td>
      <td id="T_3c73b_row0_col3" class="data row0 col3" >2020-05-12</td>
      <td id="T_3c73b_row0_col4" class="data row0 col4" >20,000,000.00</td>
      <td id="T_3c73b_row0_col5" class="data row0 col5" >0.00</td>
      <td id="T_3c73b_row0_col6" class="data row0 col6" >0.00</td>
      <td id="T_3c73b_row0_col7" class="data row0 col7" >True</td>
      <td id="T_3c73b_row0_col8" class="data row0 col8" >0.00</td>
      <td id="T_3c73b_row0_col9" class="data row0 col9" >USD</td>
      <td id="T_3c73b_row0_col10" class="data row0 col10" >TERSOFR6M</td>
      <td id="T_3c73b_row0_col11" class="data row0 col11" >0.0000%</td>
      <td id="T_3c73b_row0_col12" class="data row0 col12" >0.0000%</td>
      <td id="T_3c73b_row0_col13" class="data row0 col13" >1.00</td>
      <td id="T_3c73b_row0_col14" class="data row0 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_3c73b_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_3c73b_row1_col0" class="data row1 col0" >2020-05-12</td>
      <td id="T_3c73b_row1_col1" class="data row1 col1" >2020-11-12</td>
      <td id="T_3c73b_row1_col2" class="data row1 col2" >2020-05-08</td>
      <td id="T_3c73b_row1_col3" class="data row1 col3" >2020-11-12</td>
      <td id="T_3c73b_row1_col4" class="data row1 col4" >20,000,000.00</td>
      <td id="T_3c73b_row1_col5" class="data row1 col5" >0.00</td>
      <td id="T_3c73b_row1_col6" class="data row1 col6" >0.00</td>
      <td id="T_3c73b_row1_col7" class="data row1 col7" >True</td>
      <td id="T_3c73b_row1_col8" class="data row1 col8" >0.00</td>
      <td id="T_3c73b_row1_col9" class="data row1 col9" >USD</td>
      <td id="T_3c73b_row1_col10" class="data row1 col10" >TERSOFR6M</td>
      <td id="T_3c73b_row1_col11" class="data row1 col11" >0.0000%</td>
      <td id="T_3c73b_row1_col12" class="data row1 col12" >0.0000%</td>
      <td id="T_3c73b_row1_col13" class="data row1 col13" >1.00</td>
      <td id="T_3c73b_row1_col14" class="data row1 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_3c73b_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_3c73b_row2_col0" class="data row2 col0" >2020-11-12</td>
      <td id="T_3c73b_row2_col1" class="data row2 col1" >2021-05-12</td>
      <td id="T_3c73b_row2_col2" class="data row2 col2" >2020-11-10</td>
      <td id="T_3c73b_row2_col3" class="data row2 col3" >2021-05-12</td>
      <td id="T_3c73b_row2_col4" class="data row2 col4" >20,000,000.00</td>
      <td id="T_3c73b_row2_col5" class="data row2 col5" >20,000,000.00</td>
      <td id="T_3c73b_row2_col6" class="data row2 col6" >0.00</td>
      <td id="T_3c73b_row2_col7" class="data row2 col7" >True</td>
      <td id="T_3c73b_row2_col8" class="data row2 col8" >20,000,000.00</td>
      <td id="T_3c73b_row2_col9" class="data row2 col9" >USD</td>
      <td id="T_3c73b_row2_col10" class="data row2 col10" >TERSOFR6M</td>
      <td id="T_3c73b_row2_col11" class="data row2 col11" >0.0000%</td>
      <td id="T_3c73b_row2_col12" class="data row2 col12" >0.0000%</td>
      <td id="T_3c73b_row2_col13" class="data row2 col13" >1.00</td>
      <td id="T_3c73b_row2_col14" class="data row2 col14" >LinAct360</td>
    </tr>
  </tbody>
</table>





```python
valor_termsofr_6m = 0.02
fecha_hoy = qcf.QCDate(25, 2, 2020)
ibor_leg.get_cashflow_at(0).set_interest_rate_value(valor_termsofr_6m)
fwd_rates.set_rates_ibor_leg1(fecha_hoy, ibor_leg, zcc_usd)
```


```python
aux.leg_as_dataframe(ibor_leg).style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_104d5">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_104d5_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_104d5_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_104d5_level0_col2" class="col_heading level0 col2" >fecha_fixing</th>
      <th id="T_104d5_level0_col3" class="col_heading level0 col3" >fecha_pago</th>
      <th id="T_104d5_level0_col4" class="col_heading level0 col4" >nominal</th>
      <th id="T_104d5_level0_col5" class="col_heading level0 col5" >amortizacion</th>
      <th id="T_104d5_level0_col6" class="col_heading level0 col6" >interes</th>
      <th id="T_104d5_level0_col7" class="col_heading level0 col7" >amort_es_flujo</th>
      <th id="T_104d5_level0_col8" class="col_heading level0 col8" >flujo</th>
      <th id="T_104d5_level0_col9" class="col_heading level0 col9" >moneda</th>
      <th id="T_104d5_level0_col10" class="col_heading level0 col10" >codigo_indice_tasa</th>
      <th id="T_104d5_level0_col11" class="col_heading level0 col11" >valor_tasa</th>
      <th id="T_104d5_level0_col12" class="col_heading level0 col12" >spread</th>
      <th id="T_104d5_level0_col13" class="col_heading level0 col13" >gearing</th>
      <th id="T_104d5_level0_col14" class="col_heading level0 col14" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_104d5_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_104d5_row0_col0" class="data row0 col0" >2019-11-12</td>
      <td id="T_104d5_row0_col1" class="data row0 col1" >2020-05-12</td>
      <td id="T_104d5_row0_col2" class="data row0 col2" >2019-11-08</td>
      <td id="T_104d5_row0_col3" class="data row0 col3" >2020-05-12</td>
      <td id="T_104d5_row0_col4" class="data row0 col4" >20,000,000.00</td>
      <td id="T_104d5_row0_col5" class="data row0 col5" >0.00</td>
      <td id="T_104d5_row0_col6" class="data row0 col6" >202,222.22</td>
      <td id="T_104d5_row0_col7" class="data row0 col7" >True</td>
      <td id="T_104d5_row0_col8" class="data row0 col8" >202,222.22</td>
      <td id="T_104d5_row0_col9" class="data row0 col9" >USD</td>
      <td id="T_104d5_row0_col10" class="data row0 col10" >TERSOFR6M</td>
      <td id="T_104d5_row0_col11" class="data row0 col11" >2.0000%</td>
      <td id="T_104d5_row0_col12" class="data row0 col12" >0.0000%</td>
      <td id="T_104d5_row0_col13" class="data row0 col13" >1.00</td>
      <td id="T_104d5_row0_col14" class="data row0 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_104d5_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_104d5_row1_col0" class="data row1 col0" >2020-05-12</td>
      <td id="T_104d5_row1_col1" class="data row1 col1" >2020-11-12</td>
      <td id="T_104d5_row1_col2" class="data row1 col2" >2020-05-08</td>
      <td id="T_104d5_row1_col3" class="data row1 col3" >2020-11-12</td>
      <td id="T_104d5_row1_col4" class="data row1 col4" >20,000,000.00</td>
      <td id="T_104d5_row1_col5" class="data row1 col5" >0.00</td>
      <td id="T_104d5_row1_col6" class="data row1 col6" >169,878.64</td>
      <td id="T_104d5_row1_col7" class="data row1 col7" >True</td>
      <td id="T_104d5_row1_col8" class="data row1 col8" >169,878.64</td>
      <td id="T_104d5_row1_col9" class="data row1 col9" >USD</td>
      <td id="T_104d5_row1_col10" class="data row1 col10" >TERSOFR6M</td>
      <td id="T_104d5_row1_col11" class="data row1 col11" >1.6619%</td>
      <td id="T_104d5_row1_col12" class="data row1 col12" >0.0000%</td>
      <td id="T_104d5_row1_col13" class="data row1 col13" >1.00</td>
      <td id="T_104d5_row1_col14" class="data row1 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_104d5_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_104d5_row2_col0" class="data row2 col0" >2020-11-12</td>
      <td id="T_104d5_row2_col1" class="data row2 col1" >2021-05-12</td>
      <td id="T_104d5_row2_col2" class="data row2 col2" >2020-11-10</td>
      <td id="T_104d5_row2_col3" class="data row2 col3" >2021-05-12</td>
      <td id="T_104d5_row2_col4" class="data row2 col4" >20,000,000.00</td>
      <td id="T_104d5_row2_col5" class="data row2 col5" >20,000,000.00</td>
      <td id="T_104d5_row2_col6" class="data row2 col6" >155,899.59</td>
      <td id="T_104d5_row2_col7" class="data row2 col7" >True</td>
      <td id="T_104d5_row2_col8" class="data row2 col8" >20,155,899.59</td>
      <td id="T_104d5_row2_col9" class="data row2 col9" >USD</td>
      <td id="T_104d5_row2_col10" class="data row2 col10" >TERSOFR6M</td>
      <td id="T_104d5_row2_col11" class="data row2 col11" >1.5504%</td>
      <td id="T_104d5_row2_col12" class="data row2 col12" >0.0000%</td>
      <td id="T_104d5_row2_col13" class="data row2 col13" >1.00</td>
      <td id="T_104d5_row2_col14" class="data row2 col14" >LinAct360</td>
    </tr>
  </tbody>
</table>




Se verifica la tasa forward del segundo cashflow.


```python
which_cashflow = 1
d1 = fecha_hoy.day_diff(ibor_leg.get_cashflow_at(which_cashflow).get_start_date())
d2 = fecha_hoy.day_diff(ibor_leg.get_cashflow_at(which_cashflow).get_end_date())
print(f"d1: {d1:,.0f}")
print(f"d2: {d2:,.0f}")
crv = zcc_usd
w1 = 1 / crv.get_discount_factor_at(d1)
w2 = 1 / crv.get_discount_factor_at(d2)
print(f"Factor forward: {w2 / w1:.4%}")
print(f"Tasa forward: {(w2 / w1 - 1) * 360 / (d2 - d1):.4%}")
print(f"Curve method {crv.get_forward_rate_with_rate(termsofr_6m.get_rate(), d1, d2):.4%}")
```

    d1: 77
    d2: 261
    Factor forward: 100.8494%
    Tasa forward: 1.6619%
    Curve method 1.6619%


Cálculo de valor presente.


```python
vp_ibor = pv.pv(fecha_hoy, ibor_leg, zcc_usd)
print(f"Valor presente pata IBOR: {vp_ibor:,.0f}")
```

    Valor presente pata IBOR: 20,126,209


Derivadas del valor presente.


```python
der = pv.get_derivatives()
i = 0
for d in der:
    print(f"Sensibilidad en {i}: {d * bp / 10_000:0,.0f}")
    i += 1
print()
print(f"Sensibilidad de descuento: {sum(der) * bp / 10_000:,.0f} USD")
```

    Sensibilidad en 0: 0
    Sensibilidad en 1: 0
    Sensibilidad en 2: 0
    Sensibilidad en 3: 0
    Sensibilidad en 4: 0
    Sensibilidad en 5: -2
    Sensibilidad en 6: -2
    Sensibilidad en 7: 0
    Sensibilidad en 8: 0
    Sensibilidad en 9: 0
    Sensibilidad en 10: 0
    Sensibilidad en 11: -6
    Sensibilidad en 12: -6
    Sensibilidad en 13: 0
    Sensibilidad en 14: 0
    Sensibilidad en 15: -1,407
    Sensibilidad en 16: -986
    Sensibilidad en 17: 0
    Sensibilidad en 18: 0
    Sensibilidad en 19: 0
    Sensibilidad en 20: 0
    Sensibilidad en 21: 0
    Sensibilidad en 22: 0
    Sensibilidad en 23: 0
    Sensibilidad en 24: 0
    Sensibilidad en 25: 0
    Sensibilidad en 26: 0
    Sensibilidad en 27: 0
    
    Sensibilidad de descuento: -2,409 USD


#### Se verifica la sensibilidad de descuento por diferencias finitas.


```python
vp_ibor_up = pv.pv(fecha_hoy, ibor_leg, zcc_usd_up)
print(f"Valor presente up pata IBOR: {vp_ibor_up:,.0f}")

vp_ibor_down = pv.pv(fecha_hoy, ibor_leg, zcc_usd_down)
print(f"Valor presente down pata IBOR: {vp_ibor_down:,.0f}")

print(f"Sensibilidad de descuento en el vértice {vertice}: {(vp_ibor_up - vp_ibor_down) / 2:,.0f}")
```

    Valor presente up pata IBOR: 20,124,803
    Valor presente down pata IBOR: 20,127,616
    Sensibilidad de descuento en el vértice 15: -1,407


Se calcula también la sensibilidad a la curva de proyección.


```python
result = []

for i in range(ibor_leg.size()):
    cshflw = ibor_leg.get_cashflow_at(i)
    df = zcc_usd.get_discount_factor_at(fecha_hoy.day_diff(cshflw.get_settlement_date()))
    amt_der = cshflw.get_amount_derivatives()
    if len(amt_der) > 0:
        amt_der = [a * bp / 10_000 * df for a in amt_der]
        result.append(np.array(amt_der))

total = result[0] * 0
for r in result:
    total += r

for i in range(len(total)):
    print(f"Sensibilidad en {i}: {total[i]:0,.0f}")
print()
print(f"Sensibilidad de proyección: {sum(total):,.0f} USD")
```

    Sensibilidad en 0: 0
    Sensibilidad en 1: 0
    Sensibilidad en 2: 0
    Sensibilidad en 3: 0
    Sensibilidad en 4: 0
    Sensibilidad en 5: -190
    Sensibilidad en 6: -231
    Sensibilidad en 7: 0
    Sensibilidad en 8: 0
    Sensibilidad en 9: 0
    Sensibilidad en 10: 0
    Sensibilidad en 11: 6
    Sensibilidad en 12: 6
    Sensibilidad en 13: 0
    Sensibilidad en 14: 0
    Sensibilidad en 15: 1,407
    Sensibilidad en 16: 986
    Sensibilidad en 17: 0
    Sensibilidad en 18: 0
    Sensibilidad en 19: 0
    Sensibilidad en 20: 0
    Sensibilidad en 21: 0
    Sensibilidad en 22: 0
    Sensibilidad en 23: 0
    Sensibilidad en 24: 0
    Sensibilidad en 25: 0
    Sensibilidad en 26: 0
    Sensibilidad en 27: 0
    
    Sensibilidad de proyección: 1,984 USD


#### Se verifica la sensibilidad de proyección por diferencias finitas.


```python
fwd_rates.set_rates_ibor_leg1(fecha_hoy, ibor_leg, zcc_usd_up)
vp_ibor_up = pv.pv(fecha_hoy, ibor_leg, zcc_usd)
print(f"Valor presente up pata IBOR: {vp_ibor_up:,.0f}")

fwd_rates.set_rates_ibor_leg1(fecha_hoy, ibor_leg, zcc_usd_down)
vp_ibor_down = pv.pv(fecha_hoy, ibor_leg, zcc_usd)
print(f"Valor presente down pata IBOR: {vp_ibor_down:,.0f}")

print(f"Sensibilidad de proyección en el vértice {vertice}: {(vp_ibor_up - vp_ibor_down) / 2:,.0f}")
```

    Valor presente up pata IBOR: 20,127,616
    Valor presente down pata IBOR: 20,124,803
    Sensibilidad de proyección en el vértice 15: 1,407


### IcpClfCashflow Leg

Se da de alta una pata de tipo IcpClfCashflow.


```python
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(31, 5, 2018)
fecha_final = qcf.QCDate(31, 3, 2021) 
bus_adj_rule = qcf.BusyAdjRules.FOLLOW
periodicidad_pago = qcf.Tenor('6M')
periodo_irregular_pago = qcf.StubPeriod.SHORTFRONT
calendario = qcf.BusinessCalendar(fecha_inicio, 20)
lag_pago = 0
nominal = 300_000.0
amort_es_flujo = True 
spread = .0
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
aux.leg_as_dataframe(icp_clf_leg).style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_47697">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_47697_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_47697_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_47697_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_47697_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_47697_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_47697_level0_col5" class="col_heading level0 col5" >amort_es_flujo</th>
      <th id="T_47697_level0_col6" class="col_heading level0 col6" >flujo</th>
      <th id="T_47697_level0_col7" class="col_heading level0 col7" >moneda</th>
      <th id="T_47697_level0_col8" class="col_heading level0 col8" >icp_inicial</th>
      <th id="T_47697_level0_col9" class="col_heading level0 col9" >icp_final</th>
      <th id="T_47697_level0_col10" class="col_heading level0 col10" >uf_inicial</th>
      <th id="T_47697_level0_col11" class="col_heading level0 col11" >uf_final</th>
      <th id="T_47697_level0_col12" class="col_heading level0 col12" >valor_tasa</th>
      <th id="T_47697_level0_col13" class="col_heading level0 col13" >interes</th>
      <th id="T_47697_level0_col14" class="col_heading level0 col14" >spread</th>
      <th id="T_47697_level0_col15" class="col_heading level0 col15" >gearing</th>
      <th id="T_47697_level0_col16" class="col_heading level0 col16" >tipo_tasa</th>
      <th id="T_47697_level0_col17" class="col_heading level0 col17" >flujo_en_clp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_47697_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_47697_row0_col0" class="data row0 col0" >2018-05-31</td>
      <td id="T_47697_row0_col1" class="data row0 col1" >2018-10-31</td>
      <td id="T_47697_row0_col2" class="data row0 col2" >2018-10-31</td>
      <td id="T_47697_row0_col3" class="data row0 col3" >300,000.00</td>
      <td id="T_47697_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_47697_row0_col5" class="data row0 col5" >True</td>
      <td id="T_47697_row0_col6" class="data row0 col6" >0.00</td>
      <td id="T_47697_row0_col7" class="data row0 col7" >CLF</td>
      <td id="T_47697_row0_col8" class="data row0 col8" >10,000.00</td>
      <td id="T_47697_row0_col9" class="data row0 col9" >10,000.00</td>
      <td id="T_47697_row0_col10" class="data row0 col10" >35,000.00</td>
      <td id="T_47697_row0_col11" class="data row0 col11" >35,000.00</td>
      <td id="T_47697_row0_col12" class="data row0 col12" >0.0000%</td>
      <td id="T_47697_row0_col13" class="data row0 col13" >0.00</td>
      <td id="T_47697_row0_col14" class="data row0 col14" >0.0000%</td>
      <td id="T_47697_row0_col15" class="data row0 col15" >1.00</td>
      <td id="T_47697_row0_col16" class="data row0 col16" >LinAct360</td>
      <td id="T_47697_row0_col17" class="data row0 col17" >0.00</td>
    </tr>
    <tr>
      <th id="T_47697_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_47697_row1_col0" class="data row1 col0" >2018-10-31</td>
      <td id="T_47697_row1_col1" class="data row1 col1" >2019-04-30</td>
      <td id="T_47697_row1_col2" class="data row1 col2" >2019-04-30</td>
      <td id="T_47697_row1_col3" class="data row1 col3" >300,000.00</td>
      <td id="T_47697_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_47697_row1_col5" class="data row1 col5" >True</td>
      <td id="T_47697_row1_col6" class="data row1 col6" >0.00</td>
      <td id="T_47697_row1_col7" class="data row1 col7" >CLF</td>
      <td id="T_47697_row1_col8" class="data row1 col8" >10,000.00</td>
      <td id="T_47697_row1_col9" class="data row1 col9" >10,000.00</td>
      <td id="T_47697_row1_col10" class="data row1 col10" >35,000.00</td>
      <td id="T_47697_row1_col11" class="data row1 col11" >35,000.00</td>
      <td id="T_47697_row1_col12" class="data row1 col12" >0.0000%</td>
      <td id="T_47697_row1_col13" class="data row1 col13" >0.00</td>
      <td id="T_47697_row1_col14" class="data row1 col14" >0.0000%</td>
      <td id="T_47697_row1_col15" class="data row1 col15" >1.00</td>
      <td id="T_47697_row1_col16" class="data row1 col16" >LinAct360</td>
      <td id="T_47697_row1_col17" class="data row1 col17" >0.00</td>
    </tr>
    <tr>
      <th id="T_47697_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_47697_row2_col0" class="data row2 col0" >2019-04-30</td>
      <td id="T_47697_row2_col1" class="data row2 col1" >2019-10-31</td>
      <td id="T_47697_row2_col2" class="data row2 col2" >2019-10-31</td>
      <td id="T_47697_row2_col3" class="data row2 col3" >300,000.00</td>
      <td id="T_47697_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_47697_row2_col5" class="data row2 col5" >True</td>
      <td id="T_47697_row2_col6" class="data row2 col6" >0.00</td>
      <td id="T_47697_row2_col7" class="data row2 col7" >CLF</td>
      <td id="T_47697_row2_col8" class="data row2 col8" >10,000.00</td>
      <td id="T_47697_row2_col9" class="data row2 col9" >10,000.00</td>
      <td id="T_47697_row2_col10" class="data row2 col10" >35,000.00</td>
      <td id="T_47697_row2_col11" class="data row2 col11" >35,000.00</td>
      <td id="T_47697_row2_col12" class="data row2 col12" >0.0000%</td>
      <td id="T_47697_row2_col13" class="data row2 col13" >0.00</td>
      <td id="T_47697_row2_col14" class="data row2 col14" >0.0000%</td>
      <td id="T_47697_row2_col15" class="data row2 col15" >1.00</td>
      <td id="T_47697_row2_col16" class="data row2 col16" >LinAct360</td>
      <td id="T_47697_row2_col17" class="data row2 col17" >0.00</td>
    </tr>
    <tr>
      <th id="T_47697_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_47697_row3_col0" class="data row3 col0" >2019-10-31</td>
      <td id="T_47697_row3_col1" class="data row3 col1" >2020-04-30</td>
      <td id="T_47697_row3_col2" class="data row3 col2" >2020-04-30</td>
      <td id="T_47697_row3_col3" class="data row3 col3" >300,000.00</td>
      <td id="T_47697_row3_col4" class="data row3 col4" >0.00</td>
      <td id="T_47697_row3_col5" class="data row3 col5" >True</td>
      <td id="T_47697_row3_col6" class="data row3 col6" >0.00</td>
      <td id="T_47697_row3_col7" class="data row3 col7" >CLF</td>
      <td id="T_47697_row3_col8" class="data row3 col8" >10,000.00</td>
      <td id="T_47697_row3_col9" class="data row3 col9" >10,000.00</td>
      <td id="T_47697_row3_col10" class="data row3 col10" >35,000.00</td>
      <td id="T_47697_row3_col11" class="data row3 col11" >35,000.00</td>
      <td id="T_47697_row3_col12" class="data row3 col12" >0.0000%</td>
      <td id="T_47697_row3_col13" class="data row3 col13" >0.00</td>
      <td id="T_47697_row3_col14" class="data row3 col14" >0.0000%</td>
      <td id="T_47697_row3_col15" class="data row3 col15" >1.00</td>
      <td id="T_47697_row3_col16" class="data row3 col16" >LinAct360</td>
      <td id="T_47697_row3_col17" class="data row3 col17" >0.00</td>
    </tr>
    <tr>
      <th id="T_47697_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_47697_row4_col0" class="data row4 col0" >2020-04-30</td>
      <td id="T_47697_row4_col1" class="data row4 col1" >2020-11-02</td>
      <td id="T_47697_row4_col2" class="data row4 col2" >2020-11-02</td>
      <td id="T_47697_row4_col3" class="data row4 col3" >300,000.00</td>
      <td id="T_47697_row4_col4" class="data row4 col4" >0.00</td>
      <td id="T_47697_row4_col5" class="data row4 col5" >True</td>
      <td id="T_47697_row4_col6" class="data row4 col6" >0.00</td>
      <td id="T_47697_row4_col7" class="data row4 col7" >CLF</td>
      <td id="T_47697_row4_col8" class="data row4 col8" >10,000.00</td>
      <td id="T_47697_row4_col9" class="data row4 col9" >10,000.00</td>
      <td id="T_47697_row4_col10" class="data row4 col10" >35,000.00</td>
      <td id="T_47697_row4_col11" class="data row4 col11" >35,000.00</td>
      <td id="T_47697_row4_col12" class="data row4 col12" >0.0000%</td>
      <td id="T_47697_row4_col13" class="data row4 col13" >0.00</td>
      <td id="T_47697_row4_col14" class="data row4 col14" >0.0000%</td>
      <td id="T_47697_row4_col15" class="data row4 col15" >1.00</td>
      <td id="T_47697_row4_col16" class="data row4 col16" >LinAct360</td>
      <td id="T_47697_row4_col17" class="data row4 col17" >0.00</td>
    </tr>
    <tr>
      <th id="T_47697_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_47697_row5_col0" class="data row5 col0" >2020-11-02</td>
      <td id="T_47697_row5_col1" class="data row5 col1" >2021-04-30</td>
      <td id="T_47697_row5_col2" class="data row5 col2" >2021-04-30</td>
      <td id="T_47697_row5_col3" class="data row5 col3" >300,000.00</td>
      <td id="T_47697_row5_col4" class="data row5 col4" >300,000.00</td>
      <td id="T_47697_row5_col5" class="data row5 col5" >True</td>
      <td id="T_47697_row5_col6" class="data row5 col6" >300,000.00</td>
      <td id="T_47697_row5_col7" class="data row5 col7" >CLF</td>
      <td id="T_47697_row5_col8" class="data row5 col8" >10,000.00</td>
      <td id="T_47697_row5_col9" class="data row5 col9" >10,000.00</td>
      <td id="T_47697_row5_col10" class="data row5 col10" >35,000.00</td>
      <td id="T_47697_row5_col11" class="data row5 col11" >35,000.00</td>
      <td id="T_47697_row5_col12" class="data row5 col12" >0.0000%</td>
      <td id="T_47697_row5_col13" class="data row5 col13" >0.00</td>
      <td id="T_47697_row5_col14" class="data row5 col14" >0.0000%</td>
      <td id="T_47697_row5_col15" class="data row5 col15" >1.00</td>
      <td id="T_47697_row5_col16" class="data row5 col16" >LinAct360</td>
      <td id="T_47697_row5_col17" class="data row5 col17" >10,500,000,000.00</td>
    </tr>
  </tbody>
</table>





```python
icp_hoy = 18_882.07
uf_hoy = 28_440.19
fwd_rates.set_rates_icp_clf_leg(fecha_hoy, icp_hoy, uf_hoy, icp_clf_leg, zcc_clp, zcc_clp, zcc_clf)
cshflw = icp_clf_leg.get_cashflow_at(3)
cshflw.set_start_date_uf(28_080.26)
cshflw.set_start_date_icp(18_786.13)
```


```python
aux.leg_as_dataframe(icp_clf_leg).style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_ed163">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_ed163_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_ed163_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_ed163_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_ed163_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_ed163_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_ed163_level0_col5" class="col_heading level0 col5" >amort_es_flujo</th>
      <th id="T_ed163_level0_col6" class="col_heading level0 col6" >flujo</th>
      <th id="T_ed163_level0_col7" class="col_heading level0 col7" >moneda</th>
      <th id="T_ed163_level0_col8" class="col_heading level0 col8" >icp_inicial</th>
      <th id="T_ed163_level0_col9" class="col_heading level0 col9" >icp_final</th>
      <th id="T_ed163_level0_col10" class="col_heading level0 col10" >uf_inicial</th>
      <th id="T_ed163_level0_col11" class="col_heading level0 col11" >uf_final</th>
      <th id="T_ed163_level0_col12" class="col_heading level0 col12" >valor_tasa</th>
      <th id="T_ed163_level0_col13" class="col_heading level0 col13" >interes</th>
      <th id="T_ed163_level0_col14" class="col_heading level0 col14" >spread</th>
      <th id="T_ed163_level0_col15" class="col_heading level0 col15" >gearing</th>
      <th id="T_ed163_level0_col16" class="col_heading level0 col16" >tipo_tasa</th>
      <th id="T_ed163_level0_col17" class="col_heading level0 col17" >flujo_en_clp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_ed163_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_ed163_row0_col0" class="data row0 col0" >2018-05-31</td>
      <td id="T_ed163_row0_col1" class="data row0 col1" >2018-10-31</td>
      <td id="T_ed163_row0_col2" class="data row0 col2" >2018-10-31</td>
      <td id="T_ed163_row0_col3" class="data row0 col3" >300,000.00</td>
      <td id="T_ed163_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_ed163_row0_col5" class="data row0 col5" >True</td>
      <td id="T_ed163_row0_col6" class="data row0 col6" >0.00</td>
      <td id="T_ed163_row0_col7" class="data row0 col7" >CLF</td>
      <td id="T_ed163_row0_col8" class="data row0 col8" >10,000.00</td>
      <td id="T_ed163_row0_col9" class="data row0 col9" >10,000.00</td>
      <td id="T_ed163_row0_col10" class="data row0 col10" >35,000.00</td>
      <td id="T_ed163_row0_col11" class="data row0 col11" >35,000.00</td>
      <td id="T_ed163_row0_col12" class="data row0 col12" >0.0000%</td>
      <td id="T_ed163_row0_col13" class="data row0 col13" >0.00</td>
      <td id="T_ed163_row0_col14" class="data row0 col14" >0.0000%</td>
      <td id="T_ed163_row0_col15" class="data row0 col15" >1.00</td>
      <td id="T_ed163_row0_col16" class="data row0 col16" >LinAct360</td>
      <td id="T_ed163_row0_col17" class="data row0 col17" >0.00</td>
    </tr>
    <tr>
      <th id="T_ed163_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_ed163_row1_col0" class="data row1 col0" >2018-10-31</td>
      <td id="T_ed163_row1_col1" class="data row1 col1" >2019-04-30</td>
      <td id="T_ed163_row1_col2" class="data row1 col2" >2019-04-30</td>
      <td id="T_ed163_row1_col3" class="data row1 col3" >300,000.00</td>
      <td id="T_ed163_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_ed163_row1_col5" class="data row1 col5" >True</td>
      <td id="T_ed163_row1_col6" class="data row1 col6" >0.00</td>
      <td id="T_ed163_row1_col7" class="data row1 col7" >CLF</td>
      <td id="T_ed163_row1_col8" class="data row1 col8" >10,000.00</td>
      <td id="T_ed163_row1_col9" class="data row1 col9" >10,000.00</td>
      <td id="T_ed163_row1_col10" class="data row1 col10" >35,000.00</td>
      <td id="T_ed163_row1_col11" class="data row1 col11" >35,000.00</td>
      <td id="T_ed163_row1_col12" class="data row1 col12" >0.0000%</td>
      <td id="T_ed163_row1_col13" class="data row1 col13" >0.00</td>
      <td id="T_ed163_row1_col14" class="data row1 col14" >0.0000%</td>
      <td id="T_ed163_row1_col15" class="data row1 col15" >1.00</td>
      <td id="T_ed163_row1_col16" class="data row1 col16" >LinAct360</td>
      <td id="T_ed163_row1_col17" class="data row1 col17" >0.00</td>
    </tr>
    <tr>
      <th id="T_ed163_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_ed163_row2_col0" class="data row2 col0" >2019-04-30</td>
      <td id="T_ed163_row2_col1" class="data row2 col1" >2019-10-31</td>
      <td id="T_ed163_row2_col2" class="data row2 col2" >2019-10-31</td>
      <td id="T_ed163_row2_col3" class="data row2 col3" >300,000.00</td>
      <td id="T_ed163_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_ed163_row2_col5" class="data row2 col5" >True</td>
      <td id="T_ed163_row2_col6" class="data row2 col6" >0.00</td>
      <td id="T_ed163_row2_col7" class="data row2 col7" >CLF</td>
      <td id="T_ed163_row2_col8" class="data row2 col8" >10,000.00</td>
      <td id="T_ed163_row2_col9" class="data row2 col9" >10,000.00</td>
      <td id="T_ed163_row2_col10" class="data row2 col10" >35,000.00</td>
      <td id="T_ed163_row2_col11" class="data row2 col11" >35,000.00</td>
      <td id="T_ed163_row2_col12" class="data row2 col12" >0.0000%</td>
      <td id="T_ed163_row2_col13" class="data row2 col13" >0.00</td>
      <td id="T_ed163_row2_col14" class="data row2 col14" >0.0000%</td>
      <td id="T_ed163_row2_col15" class="data row2 col15" >1.00</td>
      <td id="T_ed163_row2_col16" class="data row2 col16" >LinAct360</td>
      <td id="T_ed163_row2_col17" class="data row2 col17" >0.00</td>
    </tr>
    <tr>
      <th id="T_ed163_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_ed163_row3_col0" class="data row3 col0" >2019-10-31</td>
      <td id="T_ed163_row3_col1" class="data row3 col1" >2020-04-30</td>
      <td id="T_ed163_row3_col2" class="data row3 col2" >2020-04-30</td>
      <td id="T_ed163_row3_col3" class="data row3 col3" >300,000.00</td>
      <td id="T_ed163_row3_col4" class="data row3 col4" >0.00</td>
      <td id="T_ed163_row3_col5" class="data row3 col5" >True</td>
      <td id="T_ed163_row3_col6" class="data row3 col6" >-3,401.28</td>
      <td id="T_ed163_row3_col7" class="data row3 col7" >CLF</td>
      <td id="T_ed163_row3_col8" class="data row3 col8" >18,786.13</td>
      <td id="T_ed163_row3_col9" class="data row3 col9" >18,935.12</td>
      <td id="T_ed163_row3_col10" class="data row3 col10" >28,080.26</td>
      <td id="T_ed163_row3_col11" class="data row3 col11" >28,627.71</td>
      <td id="T_ed163_row3_col12" class="data row3 col12" >-2.2426%</td>
      <td id="T_ed163_row3_col13" class="data row3 col13" >-3,401.28</td>
      <td id="T_ed163_row3_col14" class="data row3 col14" >0.0000%</td>
      <td id="T_ed163_row3_col15" class="data row3 col15" >1.00</td>
      <td id="T_ed163_row3_col16" class="data row3 col16" >LinAct360</td>
      <td id="T_ed163_row3_col17" class="data row3 col17" >-97,370,764.00</td>
    </tr>
    <tr>
      <th id="T_ed163_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_ed163_row4_col0" class="data row4 col0" >2020-04-30</td>
      <td id="T_ed163_row4_col1" class="data row4 col1" >2020-11-02</td>
      <td id="T_ed163_row4_col2" class="data row4 col2" >2020-11-02</td>
      <td id="T_ed163_row4_col3" class="data row4 col3" >300,000.00</td>
      <td id="T_ed163_row4_col4" class="data row4 col4" >0.00</td>
      <td id="T_ed163_row4_col5" class="data row4 col5" >True</td>
      <td id="T_ed163_row4_col6" class="data row4 col6" >-2,589.43</td>
      <td id="T_ed163_row4_col7" class="data row4 col7" >CLF</td>
      <td id="T_ed163_row4_col8" class="data row4 col8" >18,935.12</td>
      <td id="T_ed163_row4_col9" class="data row4 col9" >19,050.65</td>
      <td id="T_ed163_row4_col10" class="data row4 col10" >28,627.71</td>
      <td id="T_ed163_row4_col11" class="data row4 col11" >29,053.02</td>
      <td id="T_ed163_row4_col12" class="data row4 col12" >-1.6706%</td>
      <td id="T_ed163_row4_col13" class="data row4 col13" >-2,589.43</td>
      <td id="T_ed163_row4_col14" class="data row4 col14" >0.0000%</td>
      <td id="T_ed163_row4_col15" class="data row4 col15" >1.00</td>
      <td id="T_ed163_row4_col16" class="data row4 col16" >LinAct360</td>
      <td id="T_ed163_row4_col17" class="data row4 col17" >-75,230,762.00</td>
    </tr>
    <tr>
      <th id="T_ed163_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_ed163_row5_col0" class="data row5 col0" >2020-11-02</td>
      <td id="T_ed163_row5_col1" class="data row5 col1" >2021-04-30</td>
      <td id="T_ed163_row5_col2" class="data row5 col2" >2021-04-30</td>
      <td id="T_ed163_row5_col3" class="data row5 col3" >300,000.00</td>
      <td id="T_ed163_row5_col4" class="data row5 col4" >300,000.00</td>
      <td id="T_ed163_row5_col5" class="data row5 col5" >True</td>
      <td id="T_ed163_row5_col6" class="data row5 col6" >298,044.72</td>
      <td id="T_ed163_row5_col7" class="data row5 col7" >CLF</td>
      <td id="T_ed163_row5_col8" class="data row5 col8" >19,050.65</td>
      <td id="T_ed163_row5_col9" class="data row5 col9" >19,173.77</td>
      <td id="T_ed163_row5_col10" class="data row5 col10" >29,053.02</td>
      <td id="T_ed163_row5_col11" class="data row5 col11" >29,432.64</td>
      <td id="T_ed163_row5_col12" class="data row5 col12" >-1.3108%</td>
      <td id="T_ed163_row5_col13" class="data row5 col13" >-1,955.28</td>
      <td id="T_ed163_row5_col14" class="data row5 col14" >0.0000%</td>
      <td id="T_ed163_row5_col15" class="data row5 col15" >1.00</td>
      <td id="T_ed163_row5_col16" class="data row5 col16" >LinAct360</td>
      <td id="T_ed163_row5_col17" class="data row5 col17" >8,772,243,383.00</td>
    </tr>
  </tbody>
</table>





```python
vp_icp_clf = pv.pv(fecha_hoy, icp_clf_leg, zcc_clf)
print(f"Valor presente en UF: {vp_icp_clf:,.2f}")
print(f"Valor presente en CLP: {vp_icp_clf * uf_hoy:,.0f}")
```

    Valor presente en UF: 297,715.99
    Valor presente en CLP: 8,467,099,423


#### Sensibilidad de Descuento


```python
der = pv.get_derivatives()
i = 0
for d in der:
    print(f"Sensibilidad en {i}: {d * bp / 10_000:0,.2f}")
    i += 1
print()
print(f"Sensibilidad de descuento: {sum(der) * bp / 10_000:,.2f} CLF")
```

    Sensibilidad en 0: 0.00
    Sensibilidad en 1: 0.00
    Sensibilidad en 2: 0.00
    Sensibilidad en 3: 0.06
    Sensibilidad en 4: 0.00
    Sensibilidad en 5: 0.00
    Sensibilidad en 6: 0.00
    Sensibilidad en 7: 0.00
    Sensibilidad en 8: 0.00
    Sensibilidad en 9: 0.17
    Sensibilidad en 10: 0.01
    Sensibilidad en 11: 0.00
    Sensibilidad en 12: 0.00
    Sensibilidad en 13: 0.00
    Sensibilidad en 14: 0.00
    Sensibilidad en 15: -33.62
    Sensibilidad en 16: -2.17
    Sensibilidad en 17: 0.00
    Sensibilidad en 18: 0.00
    Sensibilidad en 19: 0.00
    Sensibilidad en 20: 0.00
    Sensibilidad en 21: 0.00
    Sensibilidad en 22: 0.00
    Sensibilidad en 23: 0.00
    Sensibilidad en 24: 0.00
    Sensibilidad en 25: 0.00
    Sensibilidad en 26: 0.00
    Sensibilidad en 27: 0.00
    Sensibilidad en 28: 0.00
    Sensibilidad en 29: 0.00
    Sensibilidad en 30: 0.00
    Sensibilidad en 31: 0.00
    Sensibilidad en 32: 0.00
    
    Sensibilidad de descuento: -35.54 CLF


#### Sensibilidad de Proyección


```python
result = []
for i in range(icp_clf_leg.size()):
    cshflw = icp_clf_leg.get_cashflow_at(i)
    df = zcc_clf.get_discount_factor_at(fecha_hoy.day_diff(cshflw.date()))
    amt_der = cshflw.get_amount_ufclf_derivatives()
    if len(amt_der) > 0:
        amt_der = [a * bp / 10_000 * df for a in amt_der]
        result.append(np.array(amt_der))

total = result[0] * 0
for r in result:
    total += r

for i in range(len(total)):
    print(f"Sensibilidad en {i}: {total[i]:0,.2f}")
```

    Sensibilidad en 0: 0.00
    Sensibilidad en 1: 0.00
    Sensibilidad en 2: 0.00
    Sensibilidad en 3: -0.06
    Sensibilidad en 4: -0.00
    Sensibilidad en 5: 0.00
    Sensibilidad en 6: 0.00
    Sensibilidad en 7: 0.00
    Sensibilidad en 8: 0.00
    Sensibilidad en 9: -0.17
    Sensibilidad en 10: -0.01
    Sensibilidad en 11: 0.00
    Sensibilidad en 12: 0.00
    Sensibilidad en 13: 0.00
    Sensibilidad en 14: 0.00
    Sensibilidad en 15: 33.62
    Sensibilidad en 16: 2.17
    Sensibilidad en 17: 0.00
    Sensibilidad en 18: 0.00
    Sensibilidad en 19: 0.00
    Sensibilidad en 20: 0.00
    Sensibilidad en 21: 0.00
    Sensibilidad en 22: 0.00
    Sensibilidad en 23: 0.00
    Sensibilidad en 24: 0.00
    Sensibilidad en 25: 0.00
    Sensibilidad en 26: 0.00
    Sensibilidad en 27: 0.00
    Sensibilidad en 28: 0.00
    Sensibilidad en 29: 0.00
    Sensibilidad en 30: 0.00
    Sensibilidad en 31: 0.00
    Sensibilidad en 32: 0.00


### CompoundedOvernightRate Leg

Se da de alta una pata de tipo CompoundedOvernightRate.


```python
rp = qcf.RecPay.PAY
fecha_inicio = qcf.QCDate(31, 3, 2020)
fecha_final = qcf.QCDate(31, 1, 2023)
bus_adj_rule = qcf.BusyAdjRules.MODFOLLOW
periodicidad_pago = qcf.Tenor('12M')
periodo_irregular_pago = qcf.StubPeriod.SHORTFRONT
calendario = qcf.BusinessCalendar(fecha_inicio, 20)
lag_pago = 0
lookback = 2

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

nominal = 5_500_000.0
amort_es_flujo = True
moneda = usd
spread = .0
gearing = 1.0

cor_leg = qcf.LegFactory.build_bullet_compounded_overnight_rate_leg_2(
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
    qcf.QCInterestRate(0.0, qcf.QCAct360(), qcf.QCLinearWf()),
    10,
    lookback,
    0
)
```

#### Valor Presente


```python
ts = qcf.time_series()
fwd_rates.set_rates_compounded_overnight_leg2(
    fecha_hoy,
    cor_leg,
    zcc_usd,
    ts
)
```


```python
aux.leg_as_dataframe(cor_leg).style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_97b1e">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_97b1e_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_97b1e_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_97b1e_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_97b1e_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_97b1e_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_97b1e_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_97b1e_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_97b1e_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_97b1e_level0_col8" class="col_heading level0 col8" >moneda</th>
      <th id="T_97b1e_level0_col9" class="col_heading level0 col9" >codigo_indice_tasa</th>
      <th id="T_97b1e_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
      <th id="T_97b1e_level0_col11" class="col_heading level0 col11" >valor_tasa</th>
      <th id="T_97b1e_level0_col12" class="col_heading level0 col12" >spread</th>
      <th id="T_97b1e_level0_col13" class="col_heading level0 col13" >gearing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_97b1e_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_97b1e_row0_col0" class="data row0 col0" >2020-03-31</td>
      <td id="T_97b1e_row0_col1" class="data row0 col1" >2021-01-29</td>
      <td id="T_97b1e_row0_col2" class="data row0 col2" >2021-01-29</td>
      <td id="T_97b1e_row0_col3" class="data row0 col3" >-5,500,000.00</td>
      <td id="T_97b1e_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_97b1e_row0_col5" class="data row0 col5" >-0.00</td>
      <td id="T_97b1e_row0_col6" class="data row0 col6" >True</td>
      <td id="T_97b1e_row0_col7" class="data row0 col7" >-77,568.07</td>
      <td id="T_97b1e_row0_col8" class="data row0 col8" >USD</td>
      <td id="T_97b1e_row0_col9" class="data row0 col9" >OISTEST</td>
      <td id="T_97b1e_row0_col10" class="data row0 col10" >LinAct360</td>
      <td id="T_97b1e_row0_col11" class="data row0 col11" >1.6701%</td>
      <td id="T_97b1e_row0_col12" class="data row0 col12" >0.0000%</td>
      <td id="T_97b1e_row0_col13" class="data row0 col13" >1.00</td>
    </tr>
    <tr>
      <th id="T_97b1e_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_97b1e_row1_col0" class="data row1 col0" >2021-01-29</td>
      <td id="T_97b1e_row1_col1" class="data row1 col1" >2022-01-31</td>
      <td id="T_97b1e_row1_col2" class="data row1 col2" >2022-01-31</td>
      <td id="T_97b1e_row1_col3" class="data row1 col3" >-5,500,000.00</td>
      <td id="T_97b1e_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_97b1e_row1_col5" class="data row1 col5" >-0.00</td>
      <td id="T_97b1e_row1_col6" class="data row1 col6" >True</td>
      <td id="T_97b1e_row1_col7" class="data row1 col7" >-84,818.39</td>
      <td id="T_97b1e_row1_col8" class="data row1 col8" >USD</td>
      <td id="T_97b1e_row1_col9" class="data row1 col9" >OISTEST</td>
      <td id="T_97b1e_row1_col10" class="data row1 col10" >LinAct360</td>
      <td id="T_97b1e_row1_col11" class="data row1 col11" >1.5127%</td>
      <td id="T_97b1e_row1_col12" class="data row1 col12" >0.0000%</td>
      <td id="T_97b1e_row1_col13" class="data row1 col13" >1.00</td>
    </tr>
    <tr>
      <th id="T_97b1e_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_97b1e_row2_col0" class="data row2 col0" >2022-01-31</td>
      <td id="T_97b1e_row2_col1" class="data row2 col1" >2023-01-31</td>
      <td id="T_97b1e_row2_col2" class="data row2 col2" >2023-01-31</td>
      <td id="T_97b1e_row2_col3" class="data row2 col3" >-5,500,000.00</td>
      <td id="T_97b1e_row2_col4" class="data row2 col4" >-5,500,000.00</td>
      <td id="T_97b1e_row2_col5" class="data row2 col5" >-0.00</td>
      <td id="T_97b1e_row2_col6" class="data row2 col6" >True</td>
      <td id="T_97b1e_row2_col7" class="data row2 col7" >-5,585,601.26</td>
      <td id="T_97b1e_row2_col8" class="data row2 col8" >USD</td>
      <td id="T_97b1e_row2_col9" class="data row2 col9" >OISTEST</td>
      <td id="T_97b1e_row2_col10" class="data row2 col10" >LinAct360</td>
      <td id="T_97b1e_row2_col11" class="data row2 col11" >1.5351%</td>
      <td id="T_97b1e_row2_col12" class="data row2 col12" >0.0000%</td>
      <td id="T_97b1e_row2_col13" class="data row2 col13" >1.00</td>
    </tr>
  </tbody>
</table>





```python
print(f'Valor presente: {pv.pv(fecha_hoy, cor_leg, zcc_usd):,.0f}')
```

    Valor presente: -5,491,175


#### Sensibilidad de Proyección


```python
proj_sens_by_cashflow = np.array([np.array(
    np.array(cor_leg.get_cashflow_at(i).get_amount_derivatives()) *
    zcc_usd.get_discount_factor_at(fecha_hoy.day_diff(cor_leg.get_cashflow_at(i).get_settlement_date())) * bp / 10_000)
                             for i in range(cor_leg.size())])
proj_sens = np.sum(proj_sens_by_cashflow, axis=0)
for i, s in enumerate(proj_sens):
     print(f"Sensibilidad en {i}: {s:0,.2f}")
```

    Sensibilidad en 0: 0.00
    Sensibilidad en 1: 0.00
    Sensibilidad en 2: 0.00
    Sensibilidad en 3: 0.00
    Sensibilidad en 4: 45.39
    Sensibilidad en 5: 7.26
    Sensibilidad en 6: 0.00
    Sensibilidad en 7: 0.00
    Sensibilidad en 8: 0.00
    Sensibilidad en 9: 0.00
    Sensibilidad en 10: 0.00
    Sensibilidad en 11: 0.00
    Sensibilidad en 12: 0.00
    Sensibilidad en 13: 0.00
    Sensibilidad en 14: -6.21
    Sensibilidad en 15: -0.89
    Sensibilidad en 16: -2.18
    Sensibilidad en 17: -120.89
    Sensibilidad en 18: -1,457.54
    Sensibilidad en 19: 0.00
    Sensibilidad en 20: 0.00
    Sensibilidad en 21: 0.00
    Sensibilidad en 22: 0.00
    Sensibilidad en 23: 0.00
    Sensibilidad en 24: 0.00
    Sensibilidad en 25: 0.00
    Sensibilidad en 26: 0.00
    Sensibilidad en 27: 0.00


Verifica sensibilidad de proyección.


```python
fwd_rates.set_rates_compounded_overnight_leg2(fecha_hoy, cor_leg, zcc_usd_up, ts)
vp_cor_up = pv.pv(fecha_hoy, cor_leg, zcc_usd)
print(f"Valor presente up pata CompoundedOvernightRate: {vp_cor_up:,.0f}")

fwd_rates.set_rates_compounded_overnight_leg2(fecha_hoy, cor_leg, zcc_usd_down, ts)
vp_cor_down = pv.pv(fecha_hoy, cor_leg, zcc_usd)
print(f"Valor presente down pata CompoundedOvernightRate: {vp_cor_down:,.0f}")

print(f"Sensibilidad de proyección en el vértice {vertice}: {(vp_cor_up - vp_cor_down) / 2:,.2f}")
```

    Valor presente up pata CompoundedOvernightRate: -5,491,175
    Valor presente down pata CompoundedOvernightRate: -5,491,174
    Sensibilidad de proyección en el vértice 15: -0.89


#### Sensibilidad de Descuento


```python
disc_der = np.array(pv.get_derivatives()) * bp / 10_000
for i, s in enumerate(disc_der):
    print(f"Sensibilidad en {i}: {s:0,.2f}")
```

    Sensibilidad en 0: 0.00
    Sensibilidad en 1: 0.00
    Sensibilidad en 2: 0.00
    Sensibilidad en 3: 0.00
    Sensibilidad en 4: 0.00
    Sensibilidad en 5: 0.00
    Sensibilidad en 6: 0.00
    Sensibilidad en 7: 0.00
    Sensibilidad en 8: 0.00
    Sensibilidad en 9: 0.00
    Sensibilidad en 10: 0.00
    Sensibilidad en 11: 0.00
    Sensibilidad en 12: 0.00
    Sensibilidad en 13: 0.00
    Sensibilidad en 14: 6.20
    Sensibilidad en 15: 0.89
    Sensibilidad en 16: 2.19
    Sensibilidad en 17: 120.90
    Sensibilidad en 18: 1,457.54
    Sensibilidad en 19: 0.00
    Sensibilidad en 20: 0.00
    Sensibilidad en 21: 0.00
    Sensibilidad en 22: 0.00
    Sensibilidad en 23: 0.00
    Sensibilidad en 24: 0.00
    Sensibilidad en 25: 0.00
    Sensibilidad en 26: 0.00
    Sensibilidad en 27: 0.00


Verifica la sensibilidad de descuento.


```python
fwd_rates.set_rates_compounded_overnight_leg2(fecha_hoy, cor_leg, zcc_usd, ts)
vp_cor_up = pv.pv(fecha_hoy, cor_leg, zcc_usd_up)
print(f"Valor presente up pata CompoundedOvernightRate: {vp_cor_up:,.2f}")

fwd_rates.set_rates_compounded_overnight_leg2(fecha_hoy, cor_leg, zcc_usd, ts)
vp_cor_down = pv.pv(fecha_hoy, cor_leg, zcc_usd_down)
print(f"Valor presente down pata CompoundedOvernightRate: {vp_cor_down:,.2f}")

print(f"Sensibilidad de descuento en el vértice {vertice}: {(vp_cor_up - vp_cor_down) / 2:,.2f}")
```

    Valor presente up pata CompoundedOvernightRate: -5,491,174
    Valor presente down pata CompoundedOvernightRate: -5,491,175
    Sensibilidad de descuento en el vértice 15: 0.89

