# Valorización y Sensibilidad

## Configuración

Para ejecutar todos los ejemplos se debe importar la librería. Se sugiere utilizar siempre el alias `qcf`. 


```python
import qcfinancial as qcf
```

Librerías adicionales.


```python
import pandas as pd
```

Para formateo de `pandas.DataFrames`.


```python
format_dict = {
    'nominal': '{0:,.2f}',
    'amort': '{0:,.2f}',
    'interes': '{0:,.2f}',
    'flujo': '{0:,.2f}',
    'amortizacion': '{0:,.2f}',
    'icp_inicial': '{0:,.2f}',
    'icp_final': '{0:,.2f}',
    'uf_inicial': '{0:,.2f}',
    'uf_final': '{0:,.2f}',
    'valor_tasa': '{0:,.4%}',
    'spread': '{0:,.4%}',
    'gearing': '{0:,.2f}',
    'amort_moneda_pago': '{0:,.2f}',
    'interes_moneda_pago': '{0:,.2f}',
    'valor_indice_fx': '{0:,.2f}'
}
```

## Construcción de la Curva

La construcción de una curva se hace en varios pasos.

### Vectores de `Float` e `Int`


```python
# Este es un vector de números enteros (grandes, de ahí la l (long))
lvec = qcf.long_vec()
```


```python
# Agregar un elemento
lvec.append(1000)
```


```python
# Este es un vector de números double.
vec = qcf.double_vec()
```


```python
# Agregar un elemento
vec.append(.025)
```


```python
# Obtener ese elemento
print("Tasa: {0:,.2%}".format(vec[0]))
```

    Tasa: 2.50%


### Objeto Curva

Es simplemente un `long_vec` que representa las abscisas de la curva y un `double_vec` que representa las ordenadas. Ambos vectores deben tener el mismo largo. 


```python
zcc = qcf.QCCurve(lvec, vec)
```

Un elemento de una curva se representa como un par abscisa, ordenada.


```python
zcc.get_values_at(0)
```




    (1000, 0.025)



Se obtiene el plazo en una posición de la curva.


```python
print(zcc.get_values_at(0))
```

    (1000, 0.025)


Se obtiene la tasa en una posición de la curva.


```python
zcc.get_values_at(0)[1]
```




    0.025



Se agrega un par (plazo, valor) a la curva.


```python
zcc.set_pair(100, .026)
```

Se verifica.


```python
# Plazo
zcc.get_values_at(1)[0]
```




    1000




```python
# Valor
zcc.get_values_at(1)[1]
```




    0.025



Se agrega un par más.


```python
zcc.set_pair(370, .03)
```

Se itera sobre la curva mostrando sus valores


```python
for i in range(0, zcc.get_length()):
    pair = zcc.get_values_at(i)
    print("Tenor: {0:} Valor: {1:.4%}".format(pair[0], pair[1]))
```

    Tenor: 100 Valor: 2.6000%
    Tenor: 370 Valor: 3.0000%
    Tenor: 1000 Valor: 2.5000%


Se define un interpolador. En este caso, un interpolador lineal.


```python
lin = qcf.QCLinearInterpolator(zcc)
```

Se hace una prueba.


```python
plazo = 120
print(f"Tasa a {plazo:.0f} días es igual a {lin.interpolate_at(plazo):.4%}")
```

    Tasa a 120 días es igual a 2.6296%


Para completar el proceso se define una fracción de año, un factor de capitalización y un tipo de tasa. Con estos objetos se termina de dar de alta una curva cero.


```python
yf = qcf.QCAct360()
wf = qcf.QCLinearWf()
tasa = qcf.QCInterestRate(.01, yf, wf)
```


```python
zz = qcf.ZeroCouponCurve(lin, tasa)
```

El interpolador permite obtener una tasa a cualquier plazo.


```python
plazo = 365
print("Tasa en {0:} es igual a {1:.4%}".format(plazo, zz.get_rate_at(plazo)))
```

    Tasa en 365 es igual a 2.9926%



```python
type(zz)
```




    qcfinancial.ZeroCouponCurve




```python
zz.get_discount_factor_at(1)
```




    0.9999277829934504



#### Otros métodos:

Tasa Forward


```python
d1 = 30
d2 = 90
print("Tasa forward entre los días {0:} y {1:}: {2:.4%}".format(
    d1, d2, zz.get_forward_rate(d1, d2)))
```

    Tasa forward entre los días 30 y 90: 2.5944%


Derivada del factor de capitalización de la Tasa Forward. El argumento representa el índice de la tasa de la curva.


```python
zz.fwd_wf_derivative_at(0)
```




    0.1659467849041197



## Valorizar

Se da de alta un objeto `PresentValue`.


```python
pv = qcf.PresentValue()
```

### Depósito a Plazo

Se utilizará como instrumento un depósito a plazo en CLP o USD. Este instrumento se modela como un `SimpleCashflow`. Este, a su vez se construye con un monto, una fecha y una moneda.


```python
# Con estas variables vamos a construir
fecha_vcto = qcf.QCDate(12, 1, 2021)
monto = 10_000_000.0
clp = qcf.QCCLP()

# Se construye el depósito
depo = qcf.SimpleCashflow(fecha_vcto, monto, clp)
```


```python
print("Monto del depósito: {0:,.0f}".format(depo.amount()))
```

    Monto del depósito: 10,000,000


Se define una fecha de valorización y se calcula el valor presente del depo.


```python
fecha_hoy = qcf.QCDate(17, 1, 2020)
print("Valor presente depo: {0:,.2f}".format(pv.pv(fecha_hoy, depo, zz)))
```

    Valor presente depo: 9,709,212.68


Se verifica *a mano* el resultado.


```python
plazo = fecha_hoy.day_diff(fecha_vcto)
print("Plazo:", plazo)
```

    Plazo: 361



```python
tasa_int = zz.get_rate_at(plazo)
print("Tasa: {0:,.4%}".format(tasa_int))
```

    Tasa: 2.9867%



```python
valor_presente = monto / (1 + tasa_int * plazo / 360)
print("Valor presente a mano: {0:,.2f}".format(valor_presente))
```

    Valor presente a mano: 9,709,212.68


### Renta Fija Local

Se muestra el ejemplo de valorización de un bono bullet a tasa fija con las convenciones de la Bolsa de Comercio. Para el ejemplo usamos las características del BTU0150326.

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

# Se da de alta el objeto
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

Construyamos dos curvas a partir de data real. Primero la curva CAMARACLP.


```python
curva = pd.read_excel("./input/curva_clp.xlsx")
curva.style.format({"tasa": "{0:,.4%}"})
```




<style type="text/css">
</style>
<table id="T_81392">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_81392_level0_col0" class="col_heading level0 col0" >curva</th>
      <th id="T_81392_level0_col1" class="col_heading level0 col1" >fecha</th>
      <th id="T_81392_level0_col2" class="col_heading level0 col2" >plazo</th>
      <th id="T_81392_level0_col3" class="col_heading level0 col3" >tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_81392_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_81392_row0_col0" class="data row0 col0" >CAMARACLP</td>
      <td id="T_81392_row0_col1" class="data row0 col1" >2020-03-05 00:00:00</td>
      <td id="T_81392_row0_col2" class="data row0 col2" >1</td>
      <td id="T_81392_row0_col3" class="data row0 col3" >1.7500%</td>
    </tr>
    <tr>
      <th id="T_81392_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_81392_row1_col0" class="data row1 col0" >CAMARACLP</td>
      <td id="T_81392_row1_col1" class="data row1 col1" >2020-03-05 00:00:00</td>
      <td id="T_81392_row1_col2" class="data row1 col2" >4</td>
      <td id="T_81392_row1_col3" class="data row1 col3" >1.7501%</td>
    </tr>
    <tr>
      <th id="T_81392_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_81392_row2_col0" class="data row2 col0" >CAMARACLP</td>
      <td id="T_81392_row2_col1" class="data row2 col1" >2020-03-05 00:00:00</td>
      <td id="T_81392_row2_col2" class="data row2 col2" >96</td>
      <td id="T_81392_row2_col3" class="data row2 col3" >1.4867%</td>
    </tr>
    <tr>
      <th id="T_81392_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_81392_row3_col0" class="data row3 col0" >CAMARACLP</td>
      <td id="T_81392_row3_col1" class="data row3 col1" >2020-03-05 00:00:00</td>
      <td id="T_81392_row3_col2" class="data row3 col2" >188</td>
      <td id="T_81392_row3_col3" class="data row3 col3" >1.3049%</td>
    </tr>
    <tr>
      <th id="T_81392_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_81392_row4_col0" class="data row4 col0" >CAMARACLP</td>
      <td id="T_81392_row4_col1" class="data row4 col1" >2020-03-05 00:00:00</td>
      <td id="T_81392_row4_col2" class="data row4 col2" >279</td>
      <td id="T_81392_row4_col3" class="data row4 col3" >1.2870%</td>
    </tr>
    <tr>
      <th id="T_81392_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_81392_row5_col0" class="data row5 col0" >CAMARACLP</td>
      <td id="T_81392_row5_col1" class="data row5 col1" >2020-03-05 00:00:00</td>
      <td id="T_81392_row5_col2" class="data row5 col2" >369</td>
      <td id="T_81392_row5_col3" class="data row5 col3" >1.3002%</td>
    </tr>
    <tr>
      <th id="T_81392_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_81392_row6_col0" class="data row6 col0" >CAMARACLP</td>
      <td id="T_81392_row6_col1" class="data row6 col1" >2020-03-05 00:00:00</td>
      <td id="T_81392_row6_col2" class="data row6 col2" >553</td>
      <td id="T_81392_row6_col3" class="data row6 col3" >1.3035%</td>
    </tr>
    <tr>
      <th id="T_81392_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_81392_row7_col0" class="data row7 col0" >CAMARACLP</td>
      <td id="T_81392_row7_col1" class="data row7 col1" >2020-03-05 00:00:00</td>
      <td id="T_81392_row7_col2" class="data row7 col2" >734</td>
      <td id="T_81392_row7_col3" class="data row7 col3" >1.2951%</td>
    </tr>
    <tr>
      <th id="T_81392_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_81392_row8_col0" class="data row8 col0" >CAMARACLP</td>
      <td id="T_81392_row8_col1" class="data row8 col1" >2020-03-05 00:00:00</td>
      <td id="T_81392_row8_col2" class="data row8 col2" >1099</td>
      <td id="T_81392_row8_col3" class="data row8 col3" >1.4440%</td>
    </tr>
    <tr>
      <th id="T_81392_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_81392_row9_col0" class="data row9 col0" >CAMARACLP</td>
      <td id="T_81392_row9_col1" class="data row9 col1" >2020-03-05 00:00:00</td>
      <td id="T_81392_row9_col2" class="data row9 col2" >1465</td>
      <td id="T_81392_row9_col3" class="data row9 col3" >1.6736%</td>
    </tr>
    <tr>
      <th id="T_81392_level0_row10" class="row_heading level0 row10" >10</th>
      <td id="T_81392_row10_col0" class="data row10 col0" >CAMARACLP</td>
      <td id="T_81392_row10_col1" class="data row10 col1" >2020-03-05 00:00:00</td>
      <td id="T_81392_row10_col2" class="data row10 col2" >1830</td>
      <td id="T_81392_row10_col3" class="data row10 col3" >1.9860%</td>
    </tr>
    <tr>
      <th id="T_81392_level0_row11" class="row_heading level0 row11" >11</th>
      <td id="T_81392_row11_col0" class="data row11 col0" >CAMARACLP</td>
      <td id="T_81392_row11_col1" class="data row11 col1" >2020-03-05 00:00:00</td>
      <td id="T_81392_row11_col2" class="data row11 col2" >2195</td>
      <td id="T_81392_row11_col3" class="data row11 col3" >2.2766%</td>
    </tr>
    <tr>
      <th id="T_81392_level0_row12" class="row_heading level0 row12" >12</th>
      <td id="T_81392_row12_col0" class="data row12 col0" >CAMARACLP</td>
      <td id="T_81392_row12_col1" class="data row12 col1" >2020-03-05 00:00:00</td>
      <td id="T_81392_row12_col2" class="data row12 col2" >2560</td>
      <td id="T_81392_row12_col3" class="data row12 col3" >2.5812%</td>
    </tr>
    <tr>
      <th id="T_81392_level0_row13" class="row_heading level0 row13" >13</th>
      <td id="T_81392_row13_col0" class="data row13 col0" >CAMARACLP</td>
      <td id="T_81392_row13_col1" class="data row13 col1" >2020-03-05 00:00:00</td>
      <td id="T_81392_row13_col2" class="data row13 col2" >2926</td>
      <td id="T_81392_row13_col3" class="data row13 col3" >2.8216%</td>
    </tr>
    <tr>
      <th id="T_81392_level0_row14" class="row_heading level0 row14" >14</th>
      <td id="T_81392_row14_col0" class="data row14 col0" >CAMARACLP</td>
      <td id="T_81392_row14_col1" class="data row14 col1" >2020-03-05 00:00:00</td>
      <td id="T_81392_row14_col2" class="data row14 col2" >3291</td>
      <td id="T_81392_row14_col3" class="data row14 col3" >3.0373%</td>
    </tr>
    <tr>
      <th id="T_81392_level0_row15" class="row_heading level0 row15" >15</th>
      <td id="T_81392_row15_col0" class="data row15 col0" >CAMARACLP</td>
      <td id="T_81392_row15_col1" class="data row15 col1" >2020-03-05 00:00:00</td>
      <td id="T_81392_row15_col2" class="data row15 col2" >3656</td>
      <td id="T_81392_row15_col3" class="data row15 col3" >3.2154%</td>
    </tr>
    <tr>
      <th id="T_81392_level0_row16" class="row_heading level0 row16" >16</th>
      <td id="T_81392_row16_col0" class="data row16 col0" >CAMARACLP</td>
      <td id="T_81392_row16_col1" class="data row16 col1" >2020-03-05 00:00:00</td>
      <td id="T_81392_row16_col2" class="data row16 col2" >4387</td>
      <td id="T_81392_row16_col3" class="data row16 col3" >3.4525%</td>
    </tr>
    <tr>
      <th id="T_81392_level0_row17" class="row_heading level0 row17" >17</th>
      <td id="T_81392_row17_col0" class="data row17 col0" >CAMARACLP</td>
      <td id="T_81392_row17_col1" class="data row17 col1" >2020-03-05 00:00:00</td>
      <td id="T_81392_row17_col2" class="data row17 col2" >5482</td>
      <td id="T_81392_row17_col3" class="data row17 col3" >3.7636%</td>
    </tr>
    <tr>
      <th id="T_81392_level0_row18" class="row_heading level0 row18" >18</th>
      <td id="T_81392_row18_col0" class="data row18 col0" >CAMARACLP</td>
      <td id="T_81392_row18_col1" class="data row18 col1" >2020-03-05 00:00:00</td>
      <td id="T_81392_row18_col2" class="data row18 col2" >7309</td>
      <td id="T_81392_row18_col3" class="data row18 col3" >4.1641%</td>
    </tr>
  </tbody>
</table>




Se da de alta un vector con los plazos (variable de tipo `long`) y un vector con las tasas (variable de tipo `double`).


```python
lvec1 = qcf.long_vec()
vec1 = qcf.double_vec()
for index, row in curva.iterrows():
    lvec1.append(int(row['plazo']))
    vec1.append(row['tasa'])
```

Luego, con una curva, un interpolador y un objeto `QCInterestRate`(que indica la convención de las tasas de la curva) se construye una curva cupón cero.


```python
zcc1 = qcf.QCCurve(lvec1, vec1)
lin1 = qcf.QCLinearInterpolator(zcc1)
zz1 = qcf.ZeroCouponCurve(lin1, tasa)
```

Luego, la curva LIBORUSD3M.


```python
curva_libor = pd.read_excel("./input/curva_usd.xlsx")
curva_libor.style.format({"tasa": "{0:,.4%}"})
```




<style type="text/css">
</style>
<table id="T_5283b">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_5283b_level0_col0" class="col_heading level0 col0" >curva</th>
      <th id="T_5283b_level0_col1" class="col_heading level0 col1" >fecha</th>
      <th id="T_5283b_level0_col2" class="col_heading level0 col2" >plazo</th>
      <th id="T_5283b_level0_col3" class="col_heading level0 col3" >tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_5283b_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_5283b_row0_col0" class="data row0 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row0_col1" class="data row0 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row0_col2" class="data row0 col2" >3</td>
      <td id="T_5283b_row0_col3" class="data row0 col3" >1.5362%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_5283b_row1_col0" class="data row1 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row1_col1" class="data row1 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row1_col2" class="data row1 col2" >4</td>
      <td id="T_5283b_row1_col3" class="data row1 col3" >1.1521%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_5283b_row2_col0" class="data row2 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row2_col1" class="data row2 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row2_col2" class="data row2 col2" >7</td>
      <td id="T_5283b_row2_col3" class="data row2 col3" >1.5536%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_5283b_row3_col0" class="data row3 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row3_col1" class="data row3 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row3_col2" class="data row3 col2" >14</td>
      <td id="T_5283b_row3_col3" class="data row3 col3" >1.5850%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_5283b_row4_col0" class="data row4 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row4_col1" class="data row4 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row4_col2" class="data row4 col2" >31</td>
      <td id="T_5283b_row4_col3" class="data row4 col3" >1.6595%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_5283b_row5_col0" class="data row5 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row5_col1" class="data row5 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row5_col2" class="data row5 col2" >60</td>
      <td id="T_5283b_row5_col3" class="data row5 col3" >1.7698%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_5283b_row6_col0" class="data row6 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row6_col1" class="data row6 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row6_col2" class="data row6 col2" >91</td>
      <td id="T_5283b_row6_col3" class="data row6 col3" >1.8010%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_5283b_row7_col0" class="data row7 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row7_col1" class="data row7 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row7_col2" class="data row7 col2" >123</td>
      <td id="T_5283b_row7_col3" class="data row7 col3" >1.7711%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_5283b_row8_col0" class="data row8 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row8_col1" class="data row8 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row8_col2" class="data row8 col2" >152</td>
      <td id="T_5283b_row8_col3" class="data row8 col3" >1.7542%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_5283b_row9_col0" class="data row9 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row9_col1" class="data row9 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row9_col2" class="data row9 col2" >182</td>
      <td id="T_5283b_row9_col3" class="data row9 col3" >1.7394%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row10" class="row_heading level0 row10" >10</th>
      <td id="T_5283b_row10_col0" class="data row10 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row10_col1" class="data row10 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row10_col2" class="data row10 col2" >213</td>
      <td id="T_5283b_row10_col3" class="data row10 col3" >1.7288%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row11" class="row_heading level0 row11" >11</th>
      <td id="T_5283b_row11_col0" class="data row11 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row11_col1" class="data row11 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row11_col2" class="data row11 col2" >244</td>
      <td id="T_5283b_row11_col3" class="data row11 col3" >1.7183%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row12" class="row_heading level0 row12" >12</th>
      <td id="T_5283b_row12_col0" class="data row12 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row12_col1" class="data row12 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row12_col2" class="data row12 col2" >276</td>
      <td id="T_5283b_row12_col3" class="data row12 col3" >1.7027%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row13" class="row_heading level0 row13" >13</th>
      <td id="T_5283b_row13_col0" class="data row13 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row13_col1" class="data row13 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row13_col2" class="data row13 col2" >305</td>
      <td id="T_5283b_row13_col3" class="data row13 col3" >1.6917%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row14" class="row_heading level0 row14" >14</th>
      <td id="T_5283b_row14_col0" class="data row14 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row14_col1" class="data row14 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row14_col2" class="data row14 col2" >335</td>
      <td id="T_5283b_row14_col3" class="data row14 col3" >1.6820%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row15" class="row_heading level0 row15" >15</th>
      <td id="T_5283b_row15_col0" class="data row15 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row15_col1" class="data row15 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row15_col2" class="data row15 col2" >367</td>
      <td id="T_5283b_row15_col3" class="data row15 col3" >1.6722%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row16" class="row_heading level0 row16" >16</th>
      <td id="T_5283b_row16_col0" class="data row16 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row16_col1" class="data row16 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row16_col2" class="data row16 col2" >549</td>
      <td id="T_5283b_row16_col3" class="data row16 col3" >1.6207%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row17" class="row_heading level0 row17" >17</th>
      <td id="T_5283b_row17_col0" class="data row17 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row17_col1" class="data row17 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row17_col2" class="data row17 col2" >731</td>
      <td id="T_5283b_row17_col3" class="data row17 col3" >1.5947%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row18" class="row_heading level0 row18" >18</th>
      <td id="T_5283b_row18_col0" class="data row18 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row18_col1" class="data row18 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row18_col2" class="data row18 col2" >1096</td>
      <td id="T_5283b_row18_col3" class="data row18 col3" >1.5788%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row19" class="row_heading level0 row19" >19</th>
      <td id="T_5283b_row19_col0" class="data row19 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row19_col1" class="data row19 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row19_col2" class="data row19 col2" >1461</td>
      <td id="T_5283b_row19_col3" class="data row19 col3" >1.5906%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row20" class="row_heading level0 row20" >20</th>
      <td id="T_5283b_row20_col0" class="data row20 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row20_col1" class="data row20 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row20_col2" class="data row20 col2" >1827</td>
      <td id="T_5283b_row20_col3" class="data row20 col3" >1.6190%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row21" class="row_heading level0 row21" >21</th>
      <td id="T_5283b_row21_col0" class="data row21 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row21_col1" class="data row21 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row21_col2" class="data row21 col2" >2558</td>
      <td id="T_5283b_row21_col3" class="data row21 col3" >1.7028%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row22" class="row_heading level0 row22" >22</th>
      <td id="T_5283b_row22_col0" class="data row22 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row22_col1" class="data row22 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row22_col2" class="data row22 col2" >3653</td>
      <td id="T_5283b_row22_col3" class="data row22 col3" >1.8533%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row23" class="row_heading level0 row23" >23</th>
      <td id="T_5283b_row23_col0" class="data row23 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row23_col1" class="data row23 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row23_col2" class="data row23 col2" >4385</td>
      <td id="T_5283b_row23_col3" class="data row23 col3" >1.9547%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row24" class="row_heading level0 row24" >24</th>
      <td id="T_5283b_row24_col0" class="data row24 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row24_col1" class="data row24 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row24_col2" class="data row24 col2" >5479</td>
      <td id="T_5283b_row24_col3" class="data row24 col3" >2.0893%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row25" class="row_heading level0 row25" >25</th>
      <td id="T_5283b_row25_col0" class="data row25 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row25_col1" class="data row25 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row25_col2" class="data row25 col2" >7305</td>
      <td id="T_5283b_row25_col3" class="data row25 col3" >2.2831%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row26" class="row_heading level0 row26" >26</th>
      <td id="T_5283b_row26_col0" class="data row26 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row26_col1" class="data row26 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row26_col2" class="data row26 col2" >9132</td>
      <td id="T_5283b_row26_col3" class="data row26 col3" >2.4306%</td>
    </tr>
    <tr>
      <th id="T_5283b_level0_row27" class="row_heading level0 row27" >27</th>
      <td id="T_5283b_row27_col0" class="data row27 col0" >LIBORUSD3MBBG</td>
      <td id="T_5283b_row27_col1" class="data row27 col1" >2020-01-22 00:00:00</td>
      <td id="T_5283b_row27_col2" class="data row27 col2" >10958</td>
      <td id="T_5283b_row27_col3" class="data row27 col3" >2.5576%</td>
    </tr>
  </tbody>
</table>





```python
lvec2 = qcf.long_vec()
vec2 = qcf.double_vec()
for index, row in curva_libor.iterrows():
    lvec2.append(int(row['plazo']))
    vec2.append(row['tasa'])

zcc2 = qcf.QCCurve(lvec2, vec2)
lin2 = qcf.QCLinearInterpolator(zcc2)
zz2 = qcf.ZeroCouponCurve(lin2, tasa)
```

Finalmente, la curva CAMARACLF.


```python
curva_camara_clf = pd.read_excel("./input/curva_clf.xlsx")
curva_camara_clf.style.format({"tasa": "{0:,.4%}"})
```




<style type="text/css">
</style>
<table id="T_b656b">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_b656b_level0_col0" class="col_heading level0 col0" >curva</th>
      <th id="T_b656b_level0_col1" class="col_heading level0 col1" >fecha</th>
      <th id="T_b656b_level0_col2" class="col_heading level0 col2" >plazo</th>
      <th id="T_b656b_level0_col3" class="col_heading level0 col3" >tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_b656b_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_b656b_row0_col0" class="data row0 col0" >CAMARACLF</td>
      <td id="T_b656b_row0_col1" class="data row0 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row0_col2" class="data row0 col2" >1</td>
      <td id="T_b656b_row0_col3" class="data row0 col3" >-5.6780%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_b656b_row1_col0" class="data row1 col0" >CAMARACLF</td>
      <td id="T_b656b_row1_col1" class="data row1 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row1_col2" class="data row1 col2" >4</td>
      <td id="T_b656b_row1_col3" class="data row1 col3" >-5.6744%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_b656b_row2_col0" class="data row2 col0" >CAMARACLF</td>
      <td id="T_b656b_row2_col1" class="data row2 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row2_col2" class="data row2 col2" >35</td>
      <td id="T_b656b_row2_col3" class="data row2 col3" >-0.9340%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_b656b_row3_col0" class="data row3 col0" >CAMARACLF</td>
      <td id="T_b656b_row3_col1" class="data row3 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row3_col2" class="data row3 col2" >64</td>
      <td id="T_b656b_row3_col3" class="data row3 col3" >-2.1183%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_b656b_row4_col0" class="data row4 col0" >CAMARACLF</td>
      <td id="T_b656b_row4_col1" class="data row4 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row4_col2" class="data row4 col2" >96</td>
      <td id="T_b656b_row4_col3" class="data row4 col3" >-2.0079%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_b656b_row5_col0" class="data row5 col0" >CAMARACLF</td>
      <td id="T_b656b_row5_col1" class="data row5 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row5_col2" class="data row5 col2" >126</td>
      <td id="T_b656b_row5_col3" class="data row5 col3" >-2.0762%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_b656b_row6_col0" class="data row6 col0" >CAMARACLF</td>
      <td id="T_b656b_row6_col1" class="data row6 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row6_col2" class="data row6 col2" >155</td>
      <td id="T_b656b_row6_col3" class="data row6 col3" >-1.9197%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_b656b_row7_col0" class="data row7 col0" >CAMARACLF</td>
      <td id="T_b656b_row7_col1" class="data row7 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row7_col2" class="data row7 col2" >188</td>
      <td id="T_b656b_row7_col3" class="data row7 col3" >-1.9347%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_b656b_row8_col0" class="data row8 col0" >CAMARACLF</td>
      <td id="T_b656b_row8_col1" class="data row8 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row8_col2" class="data row8 col2" >218</td>
      <td id="T_b656b_row8_col3" class="data row8 col3" >-1.7626%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_b656b_row9_col0" class="data row9 col0" >CAMARACLF</td>
      <td id="T_b656b_row9_col1" class="data row9 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row9_col2" class="data row9 col2" >249</td>
      <td id="T_b656b_row9_col3" class="data row9 col3" >-1.7987%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row10" class="row_heading level0 row10" >10</th>
      <td id="T_b656b_row10_col0" class="data row10 col0" >CAMARACLF</td>
      <td id="T_b656b_row10_col1" class="data row10 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row10_col2" class="data row10 col2" >279</td>
      <td id="T_b656b_row10_col3" class="data row10 col3" >-1.9335%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row11" class="row_heading level0 row11" >11</th>
      <td id="T_b656b_row11_col0" class="data row11 col0" >CAMARACLF</td>
      <td id="T_b656b_row11_col1" class="data row11 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row11_col2" class="data row11 col2" >309</td>
      <td id="T_b656b_row11_col3" class="data row11 col3" >-1.8159%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row12" class="row_heading level0 row12" >12</th>
      <td id="T_b656b_row12_col0" class="data row12 col0" >CAMARACLF</td>
      <td id="T_b656b_row12_col1" class="data row12 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row12_col2" class="data row12 col2" >341</td>
      <td id="T_b656b_row12_col3" class="data row12 col3" >-1.5940%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row13" class="row_heading level0 row13" >13</th>
      <td id="T_b656b_row13_col0" class="data row13 col0" >CAMARACLF</td>
      <td id="T_b656b_row13_col1" class="data row13 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row13_col2" class="data row13 col2" >369</td>
      <td id="T_b656b_row13_col3" class="data row13 col3" >-1.5994%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row14" class="row_heading level0 row14" >14</th>
      <td id="T_b656b_row14_col0" class="data row14 col0" >CAMARACLF</td>
      <td id="T_b656b_row14_col1" class="data row14 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row14_col2" class="data row14 col2" >400</td>
      <td id="T_b656b_row14_col3" class="data row14 col3" >-1.5068%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row15" class="row_heading level0 row15" >15</th>
      <td id="T_b656b_row15_col0" class="data row15 col0" >CAMARACLF</td>
      <td id="T_b656b_row15_col1" class="data row15 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row15_col2" class="data row15 col2" >428</td>
      <td id="T_b656b_row15_col3" class="data row15 col3" >-1.6115%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row16" class="row_heading level0 row16" >16</th>
      <td id="T_b656b_row16_col0" class="data row16 col0" >CAMARACLF</td>
      <td id="T_b656b_row16_col1" class="data row16 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row16_col2" class="data row16 col2" >461</td>
      <td id="T_b656b_row16_col3" class="data row16 col3" >-1.5923%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row17" class="row_heading level0 row17" >17</th>
      <td id="T_b656b_row17_col0" class="data row17 col0" >CAMARACLF</td>
      <td id="T_b656b_row17_col1" class="data row17 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row17_col2" class="data row17 col2" >491</td>
      <td id="T_b656b_row17_col3" class="data row17 col3" >-1.5780%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row18" class="row_heading level0 row18" >18</th>
      <td id="T_b656b_row18_col0" class="data row18 col0" >CAMARACLF</td>
      <td id="T_b656b_row18_col1" class="data row18 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row18_col2" class="data row18 col2" >522</td>
      <td id="T_b656b_row18_col3" class="data row18 col3" >-1.5186%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row19" class="row_heading level0 row19" >19</th>
      <td id="T_b656b_row19_col0" class="data row19 col0" >CAMARACLF</td>
      <td id="T_b656b_row19_col1" class="data row19 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row19_col2" class="data row19 col2" >553</td>
      <td id="T_b656b_row19_col3" class="data row19 col3" >-1.5533%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row20" class="row_heading level0 row20" >20</th>
      <td id="T_b656b_row20_col0" class="data row20 col0" >CAMARACLF</td>
      <td id="T_b656b_row20_col1" class="data row20 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row20_col2" class="data row20 col2" >582</td>
      <td id="T_b656b_row20_col3" class="data row20 col3" >-1.5649%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row21" class="row_heading level0 row21" >21</th>
      <td id="T_b656b_row21_col0" class="data row21 col0" >CAMARACLF</td>
      <td id="T_b656b_row21_col1" class="data row21 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row21_col2" class="data row21 col2" >734</td>
      <td id="T_b656b_row21_col3" class="data row21 col3" >-1.6594%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row22" class="row_heading level0 row22" >22</th>
      <td id="T_b656b_row22_col0" class="data row22 col0" >CAMARACLF</td>
      <td id="T_b656b_row22_col1" class="data row22 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row22_col2" class="data row22 col2" >1099</td>
      <td id="T_b656b_row22_col3" class="data row22 col3" >-1.4881%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row23" class="row_heading level0 row23" >23</th>
      <td id="T_b656b_row23_col0" class="data row23 col0" >CAMARACLF</td>
      <td id="T_b656b_row23_col1" class="data row23 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row23_col2" class="data row23 col2" >1465</td>
      <td id="T_b656b_row23_col3" class="data row23 col3" >-1.2740%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row24" class="row_heading level0 row24" >24</th>
      <td id="T_b656b_row24_col0" class="data row24 col0" >CAMARACLF</td>
      <td id="T_b656b_row24_col1" class="data row24 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row24_col2" class="data row24 col2" >1830</td>
      <td id="T_b656b_row24_col3" class="data row24 col3" >-1.0201%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row25" class="row_heading level0 row25" >25</th>
      <td id="T_b656b_row25_col0" class="data row25 col0" >CAMARACLF</td>
      <td id="T_b656b_row25_col1" class="data row25 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row25_col2" class="data row25 col2" >2195</td>
      <td id="T_b656b_row25_col3" class="data row25 col3" >-0.8009%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row26" class="row_heading level0 row26" >26</th>
      <td id="T_b656b_row26_col0" class="data row26 col0" >CAMARACLF</td>
      <td id="T_b656b_row26_col1" class="data row26 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row26_col2" class="data row26 col2" >2560</td>
      <td id="T_b656b_row26_col3" class="data row26 col3" >-0.5868%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row27" class="row_heading level0 row27" >27</th>
      <td id="T_b656b_row27_col0" class="data row27 col0" >CAMARACLF</td>
      <td id="T_b656b_row27_col1" class="data row27 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row27_col2" class="data row27 col2" >2926</td>
      <td id="T_b656b_row27_col3" class="data row27 col3" >-0.4145%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row28" class="row_heading level0 row28" >28</th>
      <td id="T_b656b_row28_col0" class="data row28 col0" >CAMARACLF</td>
      <td id="T_b656b_row28_col1" class="data row28 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row28_col2" class="data row28 col2" >3291</td>
      <td id="T_b656b_row28_col3" class="data row28 col3" >-0.3047%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row29" class="row_heading level0 row29" >29</th>
      <td id="T_b656b_row29_col0" class="data row29 col0" >CAMARACLF</td>
      <td id="T_b656b_row29_col1" class="data row29 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row29_col2" class="data row29 col2" >3656</td>
      <td id="T_b656b_row29_col3" class="data row29 col3" >-0.2242%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row30" class="row_heading level0 row30" >30</th>
      <td id="T_b656b_row30_col0" class="data row30 col0" >CAMARACLF</td>
      <td id="T_b656b_row30_col1" class="data row30 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row30_col2" class="data row30 col2" >4387</td>
      <td id="T_b656b_row30_col3" class="data row30 col3" >-0.1871%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row31" class="row_heading level0 row31" >31</th>
      <td id="T_b656b_row31_col0" class="data row31 col0" >CAMARACLF</td>
      <td id="T_b656b_row31_col1" class="data row31 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row31_col2" class="data row31 col2" >5482</td>
      <td id="T_b656b_row31_col3" class="data row31 col3" >-0.1056%</td>
    </tr>
    <tr>
      <th id="T_b656b_level0_row32" class="row_heading level0 row32" >32</th>
      <td id="T_b656b_row32_col0" class="data row32 col0" >CAMARACLF</td>
      <td id="T_b656b_row32_col1" class="data row32 col1" >2020-03-05 00:00:00</td>
      <td id="T_b656b_row32_col2" class="data row32 col2" >7309</td>
      <td id="T_b656b_row32_col3" class="data row32 col3" >-0.0639%</td>
    </tr>
  </tbody>
</table>





```python
lvec3 = qcf.long_vec()
vec3 = qcf.double_vec()
for index, row in curva_camara_clf.iterrows():
    lvec3.append(int(row['plazo']))
    vec3.append(row['tasa'])

zcc3 = qcf.QCCurve(lvec3, vec3)
lin3 = qcf.QCLinearInterpolator(zcc3)
zz3 = qcf.ZeroCouponCurve(lin3, tasa)
```

#### Curvas para Sensibilidad

Se define que vértice de la curva se quiere desplazar.


```python
vertice = 13
```

Se construyen las curvas con ese vértice 1 punto básico más arriba y 1 punto básico más abajo.


```python
bp = .0001
vec_sens_up = qcf.double_vec()
vec_sens_down = qcf.double_vec()
for index, row in curva.iterrows():
    if index == vertice:
        vec_sens_up.append(row['tasa'] + bp)
        vec_sens_down.append(row['tasa'] - bp)
    else:
        vec_sens_up.append(row['tasa'])
        vec_sens_down.append(row['tasa'])

zcc_sens_up = qcf.QCCurve(lvec1, vec_sens_up)
lin_sens_up = qcf.QCLinearInterpolator(zcc_sens_up)
zz_sens_up = qcf.ZeroCouponCurve(lin_sens_up, tasa)

zcc_sens_down = qcf.QCCurve(lvec1, vec_sens_down)
lin_sens_down = qcf.QCLinearInterpolator(zcc_sens_down)
zz_sens_down = qcf.ZeroCouponCurve(lin_sens_down, tasa)
```


```python
vec2_sens_up = qcf.double_vec()
vec2_sens_down = qcf.double_vec()
for index, row in curva_libor.iterrows():
    if index == vertice:
        vec2_sens_up.append(row['tasa'] + bp)
        vec2_sens_down.append(row['tasa'] - bp)
    else:
        vec2_sens_up.append(row['tasa'])
        vec2_sens_down.append(row['tasa'])

zcc2_sens_up = qcf.QCCurve(lvec2, vec2_sens_up)
lin2_sens_up = qcf.QCLinearInterpolator(zcc2_sens_up)
zz2_sens_up = qcf.ZeroCouponCurve(lin2_sens_up, tasa)

zcc2_sens_down = qcf.QCCurve(lvec2, vec2_sens_down)
lin2_sens_down = qcf.QCLinearInterpolator(zcc2_sens_down)
zz2_sens_down = qcf.ZeroCouponCurve(lin2_sens_down, tasa)
```


```python
vec3_sens_up = qcf.double_vec()
vec3_sens_down = qcf.double_vec()
for index, row in curva_camara_clf.iterrows():
    if index == vertice:
        vec3_sens_up.append(row['tasa'] + bp)
        vec3_sens_down.append(row['tasa'] - bp)
    else:
        vec3_sens_up.append(row['tasa'])
        vec3_sens_down.append(row['tasa'])

zcc3_sens_up = qcf.QCCurve(lvec3, vec3_sens_up)
lin3_sens_up = qcf.QCLinearInterpolator(zcc3_sens_up)
zz3_sens_up = qcf.ZeroCouponCurve(lin3_sens_up, tasa)

zcc3_sens_down = qcf.QCCurve(lvec3, vec3_sens_down)
lin3_sens_down = qcf.QCLinearInterpolator(zcc3_sens_down)
zz3_sens_down = qcf.ZeroCouponCurve(lin3_sens_down, tasa)
```

### FixedRateCashflow Leg

Se da de alta una pata fija:


```python
# Se da de alta los parámetros requeridos
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(12, 11, 2019)
fecha_final = qcf.QCDate(12, 11, 2020)
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


```python
# Se define un list donde almacenar los resultados de la función show
tabla = []
for i in range(0, fixed_rate_leg.size()):
    tabla.append(qcf.show(fixed_rate_leg.get_cashflow_at(i)))

# Se utiliza tabla para inicializar el Dataframe
columnas = list(qcf.get_column_names("FixedRateCashflow", ""))
df = pd.DataFrame(tabla, columns=columnas)

# Se despliega la data en este formato
df.style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_a0a05">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_a0a05_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_a0a05_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_a0a05_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_a0a05_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_a0a05_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_a0a05_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_a0a05_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_a0a05_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_a0a05_level0_col8" class="col_heading level0 col8" >moneda</th>
      <th id="T_a0a05_level0_col9" class="col_heading level0 col9" >valor_tasa</th>
      <th id="T_a0a05_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_a0a05_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_a0a05_row0_col0" class="data row0 col0" >2019-11-12</td>
      <td id="T_a0a05_row0_col1" class="data row0 col1" >2020-05-12</td>
      <td id="T_a0a05_row0_col2" class="data row0 col2" >2020-05-12</td>
      <td id="T_a0a05_row0_col3" class="data row0 col3" >20,000,000.00</td>
      <td id="T_a0a05_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_a0a05_row0_col5" class="data row0 col5" >177,400.00</td>
      <td id="T_a0a05_row0_col6" class="data row0 col6" >True</td>
      <td id="T_a0a05_row0_col7" class="data row0 col7" >177,400.00</td>
      <td id="T_a0a05_row0_col8" class="data row0 col8" >USD</td>
      <td id="T_a0a05_row0_col9" class="data row0 col9" >1.7740%</td>
      <td id="T_a0a05_row0_col10" class="data row0 col10" >Lin30360</td>
    </tr>
    <tr>
      <th id="T_a0a05_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_a0a05_row1_col0" class="data row1 col0" >2020-05-12</td>
      <td id="T_a0a05_row1_col1" class="data row1 col1" >2020-11-12</td>
      <td id="T_a0a05_row1_col2" class="data row1 col2" >2020-11-12</td>
      <td id="T_a0a05_row1_col3" class="data row1 col3" >20,000,000.00</td>
      <td id="T_a0a05_row1_col4" class="data row1 col4" >20,000,000.00</td>
      <td id="T_a0a05_row1_col5" class="data row1 col5" >177,400.00</td>
      <td id="T_a0a05_row1_col6" class="data row1 col6" >True</td>
      <td id="T_a0a05_row1_col7" class="data row1 col7" >20,177,400.00</td>
      <td id="T_a0a05_row1_col8" class="data row1 col8" >USD</td>
      <td id="T_a0a05_row1_col9" class="data row1 col9" >1.7740%</td>
      <td id="T_a0a05_row1_col10" class="data row1 col10" >Lin30360</td>
    </tr>
  </tbody>
</table>




Se calcula ahora el valor presente:


```python
vp_fija = pv.pv(fecha_hoy, fixed_rate_leg, zz2)
print("Valor presente de la pata fija es: {0:,.0f}".format(vp_fija))
```

    Valor presente de la pata fija es: 20,072,981


Al calcular el valor presente, también se calculan las derivadas del valor presente respecto a cada uno de los vértices de la curva.


```python
der = pv.get_derivatives()
```

Con esas derivadas, se puede calcular la sensibilidad a la curva cupón cero a un movimiento de 1 punto básico.


```python
i = 0
bp = .0001
total = 0
for d in der:
    total += d * bp
    print("Sensibilidad en {0:}: {1:0,.0f}".format(i, d * bp))
    i += 1
print("Sensibilidad total: {0:,.0f}".format(total))
```

    Sensibilidad en 0: 0
    Sensibilidad en 1: 0
    Sensibilidad en 2: 0
    Sensibilidad en 3: 0
    Sensibilidad en 4: 0
    Sensibilidad en 5: 0
    Sensibilidad en 6: -1
    Sensibilidad en 7: -4
    Sensibilidad en 8: 0
    Sensibilidad en 9: 0
    Sensibilidad en 10: 0
    Sensibilidad en 11: 0
    Sensibilidad en 12: -282
    Sensibilidad en 13: -1,353
    Sensibilidad en 14: 0
    Sensibilidad en 15: 0
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
    Sensibilidad total: -1,641


Se puede verificar la sensibilidad por diferencias finitas.

Se calcula el valor presente con las curvas desplazadas.


```python
vp_fija_sens_up = pv.pv(fecha_hoy, fixed_rate_leg, zz2_sens_up)
vp_fija_sens_down = pv.pv(fecha_hoy, fixed_rate_leg, zz2_sens_down)
print("Valor presente up de la pata fija es: {0:,.0f}".format(vp_fija_sens_up))
print("Valor presente down de la pata fija es: {0:,.0f}".format(
    vp_fija_sens_down))
```

    Valor presente up de la pata fija es: 20,071,628
    Valor presente down de la pata fija es: 20,074,334


Finalmente, se calcula la sensibilidad (usando la aproximación central por diferencias finitas).


```python
print("Sensibilidad por diferencias finitas: {0:,.0f}".format(
    (vp_fija_sens_up - vp_fija_sens_down) / 2))
```

    Sensibilidad por diferencias finitas: -1,353


Tanto el VP como la sensibilidad coinciden con lo que muestra FD en la pata fija de la operación 2879.

### IcpClpCashflow2 Leg


```python
# Se da de alta los parámetros requeridos
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(10,1,2019)
fecha_final = qcf.QCDate(10,7,2029)
bus_adj_rule = qcf.BusyAdjRules.FOLLOW
periodicidad_pago = qcf.Tenor('2Y')
periodo_irregular_pago = qcf.StubPeriod.SHORTFRONT
calendario = qcf.BusinessCalendar(fecha_inicio, 20)
lag_pago = 0
nominal = 38_000_000_000.0
amort_es_flujo = True
spread = .0
gearing = 1.0

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
columnas = list(qcf.get_column_names("IcpClpCashflow2", ""))
df9 = pd.DataFrame(tabla, columns=columnas)

# Se despliega la data en este formato
df9.style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_5faa0">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_5faa0_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_5faa0_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_5faa0_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_5faa0_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_5faa0_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_5faa0_level0_col5" class="col_heading level0 col5" >amort_es_flujo</th>
      <th id="T_5faa0_level0_col6" class="col_heading level0 col6" >flujo</th>
      <th id="T_5faa0_level0_col7" class="col_heading level0 col7" >moneda</th>
      <th id="T_5faa0_level0_col8" class="col_heading level0 col8" >icp_inicial</th>
      <th id="T_5faa0_level0_col9" class="col_heading level0 col9" >icp_final</th>
      <th id="T_5faa0_level0_col10" class="col_heading level0 col10" >valor_tasa</th>
      <th id="T_5faa0_level0_col11" class="col_heading level0 col11" >interes</th>
      <th id="T_5faa0_level0_col12" class="col_heading level0 col12" >spread</th>
      <th id="T_5faa0_level0_col13" class="col_heading level0 col13" >gearing</th>
      <th id="T_5faa0_level0_col14" class="col_heading level0 col14" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_5faa0_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_5faa0_row0_col0" class="data row0 col0" >2019-01-10</td>
      <td id="T_5faa0_row0_col1" class="data row0 col1" >2019-07-10</td>
      <td id="T_5faa0_row0_col2" class="data row0 col2" >2019-07-10</td>
      <td id="T_5faa0_row0_col3" class="data row0 col3" >38,000,000,000.00</td>
      <td id="T_5faa0_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_5faa0_row0_col5" class="data row0 col5" >True</td>
      <td id="T_5faa0_row0_col6" class="data row0 col6" >0.00</td>
      <td id="T_5faa0_row0_col7" class="data row0 col7" >CLP</td>
      <td id="T_5faa0_row0_col8" class="data row0 col8" >10,000.00</td>
      <td id="T_5faa0_row0_col9" class="data row0 col9" >10,000.00</td>
      <td id="T_5faa0_row0_col10" class="data row0 col10" >0.0000%</td>
      <td id="T_5faa0_row0_col11" class="data row0 col11" >0.00</td>
      <td id="T_5faa0_row0_col12" class="data row0 col12" >0.0000%</td>
      <td id="T_5faa0_row0_col13" class="data row0 col13" >1.00</td>
      <td id="T_5faa0_row0_col14" class="data row0 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_5faa0_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_5faa0_row1_col0" class="data row1 col0" >2019-07-10</td>
      <td id="T_5faa0_row1_col1" class="data row1 col1" >2021-07-12</td>
      <td id="T_5faa0_row1_col2" class="data row1 col2" >2021-07-12</td>
      <td id="T_5faa0_row1_col3" class="data row1 col3" >38,000,000,000.00</td>
      <td id="T_5faa0_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_5faa0_row1_col5" class="data row1 col5" >True</td>
      <td id="T_5faa0_row1_col6" class="data row1 col6" >0.00</td>
      <td id="T_5faa0_row1_col7" class="data row1 col7" >CLP</td>
      <td id="T_5faa0_row1_col8" class="data row1 col8" >10,000.00</td>
      <td id="T_5faa0_row1_col9" class="data row1 col9" >10,000.00</td>
      <td id="T_5faa0_row1_col10" class="data row1 col10" >0.0000%</td>
      <td id="T_5faa0_row1_col11" class="data row1 col11" >0.00</td>
      <td id="T_5faa0_row1_col12" class="data row1 col12" >0.0000%</td>
      <td id="T_5faa0_row1_col13" class="data row1 col13" >1.00</td>
      <td id="T_5faa0_row1_col14" class="data row1 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_5faa0_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_5faa0_row2_col0" class="data row2 col0" >2021-07-12</td>
      <td id="T_5faa0_row2_col1" class="data row2 col1" >2023-07-10</td>
      <td id="T_5faa0_row2_col2" class="data row2 col2" >2023-07-10</td>
      <td id="T_5faa0_row2_col3" class="data row2 col3" >38,000,000,000.00</td>
      <td id="T_5faa0_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_5faa0_row2_col5" class="data row2 col5" >True</td>
      <td id="T_5faa0_row2_col6" class="data row2 col6" >0.00</td>
      <td id="T_5faa0_row2_col7" class="data row2 col7" >CLP</td>
      <td id="T_5faa0_row2_col8" class="data row2 col8" >10,000.00</td>
      <td id="T_5faa0_row2_col9" class="data row2 col9" >10,000.00</td>
      <td id="T_5faa0_row2_col10" class="data row2 col10" >0.0000%</td>
      <td id="T_5faa0_row2_col11" class="data row2 col11" >0.00</td>
      <td id="T_5faa0_row2_col12" class="data row2 col12" >0.0000%</td>
      <td id="T_5faa0_row2_col13" class="data row2 col13" >1.00</td>
      <td id="T_5faa0_row2_col14" class="data row2 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_5faa0_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_5faa0_row3_col0" class="data row3 col0" >2023-07-10</td>
      <td id="T_5faa0_row3_col1" class="data row3 col1" >2025-07-10</td>
      <td id="T_5faa0_row3_col2" class="data row3 col2" >2025-07-10</td>
      <td id="T_5faa0_row3_col3" class="data row3 col3" >38,000,000,000.00</td>
      <td id="T_5faa0_row3_col4" class="data row3 col4" >0.00</td>
      <td id="T_5faa0_row3_col5" class="data row3 col5" >True</td>
      <td id="T_5faa0_row3_col6" class="data row3 col6" >0.00</td>
      <td id="T_5faa0_row3_col7" class="data row3 col7" >CLP</td>
      <td id="T_5faa0_row3_col8" class="data row3 col8" >10,000.00</td>
      <td id="T_5faa0_row3_col9" class="data row3 col9" >10,000.00</td>
      <td id="T_5faa0_row3_col10" class="data row3 col10" >0.0000%</td>
      <td id="T_5faa0_row3_col11" class="data row3 col11" >0.00</td>
      <td id="T_5faa0_row3_col12" class="data row3 col12" >0.0000%</td>
      <td id="T_5faa0_row3_col13" class="data row3 col13" >1.00</td>
      <td id="T_5faa0_row3_col14" class="data row3 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_5faa0_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_5faa0_row4_col0" class="data row4 col0" >2025-07-10</td>
      <td id="T_5faa0_row4_col1" class="data row4 col1" >2027-07-12</td>
      <td id="T_5faa0_row4_col2" class="data row4 col2" >2027-07-12</td>
      <td id="T_5faa0_row4_col3" class="data row4 col3" >38,000,000,000.00</td>
      <td id="T_5faa0_row4_col4" class="data row4 col4" >0.00</td>
      <td id="T_5faa0_row4_col5" class="data row4 col5" >True</td>
      <td id="T_5faa0_row4_col6" class="data row4 col6" >0.00</td>
      <td id="T_5faa0_row4_col7" class="data row4 col7" >CLP</td>
      <td id="T_5faa0_row4_col8" class="data row4 col8" >10,000.00</td>
      <td id="T_5faa0_row4_col9" class="data row4 col9" >10,000.00</td>
      <td id="T_5faa0_row4_col10" class="data row4 col10" >0.0000%</td>
      <td id="T_5faa0_row4_col11" class="data row4 col11" >0.00</td>
      <td id="T_5faa0_row4_col12" class="data row4 col12" >0.0000%</td>
      <td id="T_5faa0_row4_col13" class="data row4 col13" >1.00</td>
      <td id="T_5faa0_row4_col14" class="data row4 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_5faa0_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_5faa0_row5_col0" class="data row5 col0" >2027-07-12</td>
      <td id="T_5faa0_row5_col1" class="data row5 col1" >2029-07-10</td>
      <td id="T_5faa0_row5_col2" class="data row5 col2" >2029-07-10</td>
      <td id="T_5faa0_row5_col3" class="data row5 col3" >38,000,000,000.00</td>
      <td id="T_5faa0_row5_col4" class="data row5 col4" >38,000,000,000.00</td>
      <td id="T_5faa0_row5_col5" class="data row5 col5" >True</td>
      <td id="T_5faa0_row5_col6" class="data row5 col6" >38,000,000,000.00</td>
      <td id="T_5faa0_row5_col7" class="data row5 col7" >CLP</td>
      <td id="T_5faa0_row5_col8" class="data row5 col8" >10,000.00</td>
      <td id="T_5faa0_row5_col9" class="data row5 col9" >10,000.00</td>
      <td id="T_5faa0_row5_col10" class="data row5 col10" >0.0000%</td>
      <td id="T_5faa0_row5_col11" class="data row5 col11" >0.00</td>
      <td id="T_5faa0_row5_col12" class="data row5 col12" >0.0000%</td>
      <td id="T_5faa0_row5_col13" class="data row5 col13" >1.00</td>
      <td id="T_5faa0_row5_col14" class="data row5 col14" >LinAct360</td>
    </tr>
  </tbody>
</table>




Notar que al dar de alta un Leg con IcpClpCashflow2, los valores futuros de los ICP son los default (=10,000.00). Por lo tanto, el primer paso para valorizar estos cashflows, es calcular los valores forward de los índices.

Se comienza dando de alta un objeto de tipo `ForwardRates`.


```python
fwd_rates = qcf.ForwardRates()
```

Se calculan los índices forward.


```python
icp_val = 18_890.34 # icp a la fecha de proceso
fecha_hoy = qcf.QCDate(5, 3, 2020)

for i in range(icp_clp2_leg.size()):
    cashflow = icp_clp2_leg.get_cashflow_at(i)
    if cashflow.get_start_date() <= fecha_hoy <= cashflow.get_end_date():
            index = i

icp_fecha_inicio_cupon_vigente = 18_376.69
icp_clp2_leg.get_cashflow_at(index).set_start_date_icp(icp_fecha_inicio_cupon_vigente)

fwd_rates.set_rates_icp_clp_leg(fecha_hoy, icp_val, icp_clp2_leg, zz1)
```


```python
# Se define un list donde almacenar los resultados de la función show
tabla = []
for i in range(0, icp_clp2_leg.size()):
    tabla.append(qcf.show(icp_clp2_leg.get_cashflow_at(i)))

# Se utiliza tabla para inicializar el Dataframe
columnas = list(qcf.get_column_names("IcpClpCashflow2", ""))
df9 = pd.DataFrame(tabla, columns=columnas)

# Se despliega la data en este formato
df9.style.format(format_dict)
```




<style type="text/css">
</style>
<table id="T_d49fd">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_d49fd_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_d49fd_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_d49fd_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_d49fd_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_d49fd_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_d49fd_level0_col5" class="col_heading level0 col5" >amort_es_flujo</th>
      <th id="T_d49fd_level0_col6" class="col_heading level0 col6" >flujo</th>
      <th id="T_d49fd_level0_col7" class="col_heading level0 col7" >moneda</th>
      <th id="T_d49fd_level0_col8" class="col_heading level0 col8" >icp_inicial</th>
      <th id="T_d49fd_level0_col9" class="col_heading level0 col9" >icp_final</th>
      <th id="T_d49fd_level0_col10" class="col_heading level0 col10" >valor_tasa</th>
      <th id="T_d49fd_level0_col11" class="col_heading level0 col11" >interes</th>
      <th id="T_d49fd_level0_col12" class="col_heading level0 col12" >spread</th>
      <th id="T_d49fd_level0_col13" class="col_heading level0 col13" >gearing</th>
      <th id="T_d49fd_level0_col14" class="col_heading level0 col14" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_d49fd_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_d49fd_row0_col0" class="data row0 col0" >2019-01-10</td>
      <td id="T_d49fd_row0_col1" class="data row0 col1" >2019-07-10</td>
      <td id="T_d49fd_row0_col2" class="data row0 col2" >2019-07-10</td>
      <td id="T_d49fd_row0_col3" class="data row0 col3" >38,000,000,000.00</td>
      <td id="T_d49fd_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_d49fd_row0_col5" class="data row0 col5" >True</td>
      <td id="T_d49fd_row0_col6" class="data row0 col6" >0.00</td>
      <td id="T_d49fd_row0_col7" class="data row0 col7" >CLP</td>
      <td id="T_d49fd_row0_col8" class="data row0 col8" >10,000.00</td>
      <td id="T_d49fd_row0_col9" class="data row0 col9" >10,000.00</td>
      <td id="T_d49fd_row0_col10" class="data row0 col10" >0.0000%</td>
      <td id="T_d49fd_row0_col11" class="data row0 col11" >0.00</td>
      <td id="T_d49fd_row0_col12" class="data row0 col12" >0.0000%</td>
      <td id="T_d49fd_row0_col13" class="data row0 col13" >1.00</td>
      <td id="T_d49fd_row0_col14" class="data row0 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_d49fd_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_d49fd_row1_col0" class="data row1 col0" >2019-07-10</td>
      <td id="T_d49fd_row1_col1" class="data row1 col1" >2021-07-12</td>
      <td id="T_d49fd_row1_col2" class="data row1 col2" >2021-07-12</td>
      <td id="T_d49fd_row1_col3" class="data row1 col3" >38,000,000,000.00</td>
      <td id="T_d49fd_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_d49fd_row1_col5" class="data row1 col5" >True</td>
      <td id="T_d49fd_row1_col6" class="data row1 col6" >1,760,277,860.28</td>
      <td id="T_d49fd_row1_col7" class="data row1 col7" >CLP</td>
      <td id="T_d49fd_row1_col8" class="data row1 col8" >18,376.69</td>
      <td id="T_d49fd_row1_col9" class="data row1 col9" >19,227.96</td>
      <td id="T_d49fd_row1_col10" class="data row1 col10" >2.2800%</td>
      <td id="T_d49fd_row1_col11" class="data row1 col11" >1,764,086,666.67</td>
      <td id="T_d49fd_row1_col12" class="data row1 col12" >0.0000%</td>
      <td id="T_d49fd_row1_col13" class="data row1 col13" >1.00</td>
      <td id="T_d49fd_row1_col14" class="data row1 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_d49fd_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_d49fd_row2_col0" class="data row2 col0" >2021-07-12</td>
      <td id="T_d49fd_row2_col1" class="data row2 col1" >2023-07-10</td>
      <td id="T_d49fd_row2_col2" class="data row2 col2" >2023-07-10</td>
      <td id="T_d49fd_row2_col3" class="data row2 col3" >38,000,000,000.00</td>
      <td id="T_d49fd_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_d49fd_row2_col5" class="data row2 col5" >True</td>
      <td id="T_d49fd_row2_col6" class="data row2 col6" >1,260,461,341.38</td>
      <td id="T_d49fd_row2_col7" class="data row2 col7" >CLP</td>
      <td id="T_d49fd_row2_col8" class="data row2 col8" >19,227.96</td>
      <td id="T_d49fd_row2_col9" class="data row2 col9" >19,865.75</td>
      <td id="T_d49fd_row2_col10" class="data row2 col10" >1.6400%</td>
      <td id="T_d49fd_row2_col11" class="data row2 col11" >1,260,248,888.89</td>
      <td id="T_d49fd_row2_col12" class="data row2 col12" >0.0000%</td>
      <td id="T_d49fd_row2_col13" class="data row2 col13" >1.00</td>
      <td id="T_d49fd_row2_col14" class="data row2 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_d49fd_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_d49fd_row3_col0" class="data row3 col0" >2023-07-10</td>
      <td id="T_d49fd_row3_col1" class="data row3 col1" >2025-07-10</td>
      <td id="T_d49fd_row3_col2" class="data row3 col2" >2025-07-10</td>
      <td id="T_d49fd_row3_col3" class="data row3 col3" >38,000,000,000.00</td>
      <td id="T_d49fd_row3_col4" class="data row3 col4" >0.00</td>
      <td id="T_d49fd_row3_col5" class="data row3 col5" >True</td>
      <td id="T_d49fd_row3_col6" class="data row3 col6" >2,219,270,452.18</td>
      <td id="T_d49fd_row3_col7" class="data row3 col7" >CLP</td>
      <td id="T_d49fd_row3_col8" class="data row3 col8" >19,865.75</td>
      <td id="T_d49fd_row3_col9" class="data row3 col9" >21,025.94</td>
      <td id="T_d49fd_row3_col10" class="data row3 col10" >2.8800%</td>
      <td id="T_d49fd_row3_col11" class="data row3 col11" >2,222,240,000.00</td>
      <td id="T_d49fd_row3_col12" class="data row3 col12" >0.0000%</td>
      <td id="T_d49fd_row3_col13" class="data row3 col13" >1.00</td>
      <td id="T_d49fd_row3_col14" class="data row3 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_d49fd_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_d49fd_row4_col0" class="data row4 col0" >2025-07-10</td>
      <td id="T_d49fd_row4_col1" class="data row4 col1" >2027-07-12</td>
      <td id="T_d49fd_row4_col2" class="data row4 col2" >2027-07-12</td>
      <td id="T_d49fd_row4_col3" class="data row4 col3" >38,000,000,000.00</td>
      <td id="T_d49fd_row4_col4" class="data row4 col4" >0.00</td>
      <td id="T_d49fd_row4_col5" class="data row4 col5" >True</td>
      <td id="T_d49fd_row4_col6" class="data row4 col6" >2,921,878,806.15</td>
      <td id="T_d49fd_row4_col7" class="data row4 col7" >CLP</td>
      <td id="T_d49fd_row4_col8" class="data row4 col8" >21,025.94</td>
      <td id="T_d49fd_row4_col9" class="data row4 col9" >22,642.66</td>
      <td id="T_d49fd_row4_col10" class="data row4 col10" >3.7800%</td>
      <td id="T_d49fd_row4_col11" class="data row4 col11" >2,920,680,000.00</td>
      <td id="T_d49fd_row4_col12" class="data row4 col12" >0.0000%</td>
      <td id="T_d49fd_row4_col13" class="data row4 col13" >1.00</td>
      <td id="T_d49fd_row4_col14" class="data row4 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_d49fd_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_d49fd_row5_col0" class="data row5 col0" >2027-07-12</td>
      <td id="T_d49fd_row5_col1" class="data row5 col1" >2029-07-10</td>
      <td id="T_d49fd_row5_col2" class="data row5 col2" >2029-07-10</td>
      <td id="T_d49fd_row5_col3" class="data row5 col3" >38,000,000,000.00</td>
      <td id="T_d49fd_row5_col4" class="data row5 col4" >38,000,000,000.00</td>
      <td id="T_d49fd_row5_col5" class="data row5 col5" >True</td>
      <td id="T_d49fd_row5_col6" class="data row5 col6" >41,014,662,342.55</td>
      <td id="T_d49fd_row5_col7" class="data row5 col7" >CLP</td>
      <td id="T_d49fd_row5_col8" class="data row5 col8" >22,642.66</td>
      <td id="T_d49fd_row5_col9" class="data row5 col9" >24,438.98</td>
      <td id="T_d49fd_row5_col10" class="data row5 col10" >3.9200%</td>
      <td id="T_d49fd_row5_col11" class="data row5 col11" >3,016,440,000.00</td>
      <td id="T_d49fd_row5_col12" class="data row5 col12" >0.0000%</td>
      <td id="T_d49fd_row5_col13" class="data row5 col13" >1.00</td>
      <td id="T_d49fd_row5_col14" class="data row5 col14" >LinAct360</td>
    </tr>
  </tbody>
</table>




Con esto, podemos calcular el valor presente.


```python
vp_icp_clp = pv.pv(fecha_hoy, icp_clp2_leg, zz1)
print("Valor presente pata ICPCLP: {0:,.0f}".format(vp_icp_clp))
```

    Valor presente pata ICPCLP: 39,062,144,488



```python
csh = icp_clp2_leg.get_cashflow_at(5)
```


```python
pv.pv(fecha_hoy, csh, zz1)
```




    31702674802.50826



También en este caso es posible calcular la sensibilidad a la curva de descuento.


```python
der = pv.get_derivatives()
i = 0
bp = .0001
for d in der:
    print("Sensibilidad en {0:}: {1:0,.0f}".format(i, d * bp))
    i += 1
```

    Sensibilidad en 0: -0
    Sensibilidad en 1: -0
    Sensibilidad en 2: -0
    Sensibilidad en 3: -0
    Sensibilidad en 4: -0
    Sensibilidad en 5: -0
    Sensibilidad en 6: -0
    Sensibilidad en 7: -0
    Sensibilidad en 8: -0
    Sensibilidad en 9: -0
    Sensibilidad en 10: -0
    Sensibilidad en 11: -0
    Sensibilidad en 12: -0
    Sensibilidad en 13: -0
    Sensibilidad en 14: -15,407,642
    Sensibilidad en 15: -7,831,157
    Sensibilidad en 16: -0
    Sensibilidad en 17: -0
    Sensibilidad en 18: -0


Podemos ver la sensibilidad total:


```python
sens_disc = [d * bp for d in der]
print("Sensibilidad de descuento: {0:,.0f} CLP".format(sum(sens_disc)))
```

    Sensibilidad de descuento: -23,238,799 CLP


La estructura es la misma que para una pata fija, lo que indica que se debe también incluir la sensibilidad a la curva de proyección.


```python
import numpy as np
bp = .0001
result = []
for i in range(icp_clp2_leg.size()):
    cshflw = icp_clp2_leg.get_cashflow_at(i)
    amt_der = cshflw.get_amount_derivatives()
    df = zz1.get_discount_factor_at(fecha_hoy.day_diff(cshflw.get_settlement_date()))
    amt_der = [a * bp * df for a in amt_der]
    if len(amt_der) > 0:
        result.append(np.array(amt_der))
total = result[0] * 0

for r in result:
    total += r

for i in range(len(total)):
    print("Sensibilidad en {0:}: {1:0,.0f}".format(i, total[i]))

print("Sensibilidad de proyección: {0:,.0f} CLP".format(sum(total)))
```

    Sensibilidad en 0: 0
    Sensibilidad en 1: 0
    Sensibilidad en 2: 0
    Sensibilidad en 3: 0
    Sensibilidad en 4: 0
    Sensibilidad en 5: 74,757
    Sensibilidad en 6: 158,384
    Sensibilidad en 7: 0
    Sensibilidad en 8: 256,858
    Sensibilidad en 9: 130,015
    Sensibilidad en 10: 644,319
    Sensibilidad en 11: 327,485
    Sensibilidad en 12: 998,768
    Sensibilidad en 13: 518,033
    Sensibilidad en 14: 15,407,642
    Sensibilidad en 15: 7,831,157
    Sensibilidad en 16: 0
    Sensibilidad en 17: 0
    Sensibilidad en 18: 0
    Sensibilidad de proyección: 26,347,418 CLP


Como se espera de una pata ICPCLP (con lag de pago igual a 0 y spread igual a 0), ambas sensibilidades se cancelan.

#### Se verifica la sensibilidad de proyección por diferencias finitas:


```python
fwd_rates.set_rates_icp_clp_leg(fecha_hoy, icp_val, icp_clp2_leg, zz_sens_up)
vp_icp_clp_up = pv.pv(fecha_hoy, icp_clp2_leg, zz1)

fwd_rates.set_rates_icp_clp_leg(fecha_hoy, icp_val, icp_clp2_leg, zz_sens_down)
vp_icp_clp_down = pv.pv(fecha_hoy, icp_clp2_leg, zz1)

print("Sensibilidad en vértice {0:}: {1:,.0f} CLP".format(
    vertice, (vp_icp_clp_up - vp_icp_clp_down) / 2))
```

    Sensibilidad en vértice 13: 518,033 CLP


### IborCashflow2 Leg


```python
### Se da de alta los parámetros requeridos
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(12, 11, 2019)
fecha_final = qcf.QCDate(12, 11, 2029)
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

nominal = 20_000_000.0
amort_es_flujo = True
moneda = usd
spread = .0
gearing = 1.0

# Es la op 2879 en FD
ibor_leg = qcf.LegFactory.build_bullet_ibor2_leg(
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
<table id="T_cd292">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_cd292_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_cd292_level0_col1" class="col_heading level0 col1" >fecha__final</th>
      <th id="T_cd292_level0_col2" class="col_heading level0 col2" >fecha_fixing</th>
      <th id="T_cd292_level0_col3" class="col_heading level0 col3" >fecha__pago</th>
      <th id="T_cd292_level0_col4" class="col_heading level0 col4" >nominal</th>
      <th id="T_cd292_level0_col5" class="col_heading level0 col5" >amort</th>
      <th id="T_cd292_level0_col6" class="col_heading level0 col6" >interes</th>
      <th id="T_cd292_level0_col7" class="col_heading level0 col7" >amort_es_flujo</th>
      <th id="T_cd292_level0_col8" class="col_heading level0 col8" >flujo</th>
      <th id="T_cd292_level0_col9" class="col_heading level0 col9" >moneda</th>
      <th id="T_cd292_level0_col10" class="col_heading level0 col10" >codigo_indice</th>
      <th id="T_cd292_level0_col11" class="col_heading level0 col11" >valor_tasa</th>
      <th id="T_cd292_level0_col12" class="col_heading level0 col12" >spread</th>
      <th id="T_cd292_level0_col13" class="col_heading level0 col13" >gearing</th>
      <th id="T_cd292_level0_col14" class="col_heading level0 col14" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_cd292_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_cd292_row0_col0" class="data row0 col0" >2019-11-12</td>
      <td id="T_cd292_row0_col1" class="data row0 col1" >2020-02-12</td>
      <td id="T_cd292_row0_col2" class="data row0 col2" >2019-11-08</td>
      <td id="T_cd292_row0_col3" class="data row0 col3" >2020-02-12</td>
      <td id="T_cd292_row0_col4" class="data row0 col4" >20,000,000.00</td>
      <td id="T_cd292_row0_col5" class="data row0 col5" >0.00</td>
      <td id="T_cd292_row0_col6" class="data row0 col6" >0.00</td>
      <td id="T_cd292_row0_col7" class="data row0 col7" >True</td>
      <td id="T_cd292_row0_col8" class="data row0 col8" >0.00</td>
      <td id="T_cd292_row0_col9" class="data row0 col9" >USD</td>
      <td id="T_cd292_row0_col10" class="data row0 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row0_col11" class="data row0 col11" >0.0000%</td>
      <td id="T_cd292_row0_col12" class="data row0 col12" >0.0000%</td>
      <td id="T_cd292_row0_col13" class="data row0 col13" >1.00</td>
      <td id="T_cd292_row0_col14" class="data row0 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_cd292_row1_col0" class="data row1 col0" >2020-02-12</td>
      <td id="T_cd292_row1_col1" class="data row1 col1" >2020-05-12</td>
      <td id="T_cd292_row1_col2" class="data row1 col2" >2020-02-10</td>
      <td id="T_cd292_row1_col3" class="data row1 col3" >2020-05-12</td>
      <td id="T_cd292_row1_col4" class="data row1 col4" >20,000,000.00</td>
      <td id="T_cd292_row1_col5" class="data row1 col5" >0.00</td>
      <td id="T_cd292_row1_col6" class="data row1 col6" >0.00</td>
      <td id="T_cd292_row1_col7" class="data row1 col7" >True</td>
      <td id="T_cd292_row1_col8" class="data row1 col8" >0.00</td>
      <td id="T_cd292_row1_col9" class="data row1 col9" >USD</td>
      <td id="T_cd292_row1_col10" class="data row1 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row1_col11" class="data row1 col11" >0.0000%</td>
      <td id="T_cd292_row1_col12" class="data row1 col12" >0.0000%</td>
      <td id="T_cd292_row1_col13" class="data row1 col13" >1.00</td>
      <td id="T_cd292_row1_col14" class="data row1 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_cd292_row2_col0" class="data row2 col0" >2020-05-12</td>
      <td id="T_cd292_row2_col1" class="data row2 col1" >2020-08-12</td>
      <td id="T_cd292_row2_col2" class="data row2 col2" >2020-05-08</td>
      <td id="T_cd292_row2_col3" class="data row2 col3" >2020-08-12</td>
      <td id="T_cd292_row2_col4" class="data row2 col4" >20,000,000.00</td>
      <td id="T_cd292_row2_col5" class="data row2 col5" >0.00</td>
      <td id="T_cd292_row2_col6" class="data row2 col6" >0.00</td>
      <td id="T_cd292_row2_col7" class="data row2 col7" >True</td>
      <td id="T_cd292_row2_col8" class="data row2 col8" >0.00</td>
      <td id="T_cd292_row2_col9" class="data row2 col9" >USD</td>
      <td id="T_cd292_row2_col10" class="data row2 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row2_col11" class="data row2 col11" >0.0000%</td>
      <td id="T_cd292_row2_col12" class="data row2 col12" >0.0000%</td>
      <td id="T_cd292_row2_col13" class="data row2 col13" >1.00</td>
      <td id="T_cd292_row2_col14" class="data row2 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_cd292_row3_col0" class="data row3 col0" >2020-08-12</td>
      <td id="T_cd292_row3_col1" class="data row3 col1" >2020-11-12</td>
      <td id="T_cd292_row3_col2" class="data row3 col2" >2020-08-10</td>
      <td id="T_cd292_row3_col3" class="data row3 col3" >2020-11-12</td>
      <td id="T_cd292_row3_col4" class="data row3 col4" >20,000,000.00</td>
      <td id="T_cd292_row3_col5" class="data row3 col5" >0.00</td>
      <td id="T_cd292_row3_col6" class="data row3 col6" >0.00</td>
      <td id="T_cd292_row3_col7" class="data row3 col7" >True</td>
      <td id="T_cd292_row3_col8" class="data row3 col8" >0.00</td>
      <td id="T_cd292_row3_col9" class="data row3 col9" >USD</td>
      <td id="T_cd292_row3_col10" class="data row3 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row3_col11" class="data row3 col11" >0.0000%</td>
      <td id="T_cd292_row3_col12" class="data row3 col12" >0.0000%</td>
      <td id="T_cd292_row3_col13" class="data row3 col13" >1.00</td>
      <td id="T_cd292_row3_col14" class="data row3 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_cd292_row4_col0" class="data row4 col0" >2020-11-12</td>
      <td id="T_cd292_row4_col1" class="data row4 col1" >2021-02-12</td>
      <td id="T_cd292_row4_col2" class="data row4 col2" >2020-11-10</td>
      <td id="T_cd292_row4_col3" class="data row4 col3" >2021-02-12</td>
      <td id="T_cd292_row4_col4" class="data row4 col4" >20,000,000.00</td>
      <td id="T_cd292_row4_col5" class="data row4 col5" >0.00</td>
      <td id="T_cd292_row4_col6" class="data row4 col6" >0.00</td>
      <td id="T_cd292_row4_col7" class="data row4 col7" >True</td>
      <td id="T_cd292_row4_col8" class="data row4 col8" >0.00</td>
      <td id="T_cd292_row4_col9" class="data row4 col9" >USD</td>
      <td id="T_cd292_row4_col10" class="data row4 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row4_col11" class="data row4 col11" >0.0000%</td>
      <td id="T_cd292_row4_col12" class="data row4 col12" >0.0000%</td>
      <td id="T_cd292_row4_col13" class="data row4 col13" >1.00</td>
      <td id="T_cd292_row4_col14" class="data row4 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_cd292_row5_col0" class="data row5 col0" >2021-02-12</td>
      <td id="T_cd292_row5_col1" class="data row5 col1" >2021-05-12</td>
      <td id="T_cd292_row5_col2" class="data row5 col2" >2021-02-10</td>
      <td id="T_cd292_row5_col3" class="data row5 col3" >2021-05-12</td>
      <td id="T_cd292_row5_col4" class="data row5 col4" >20,000,000.00</td>
      <td id="T_cd292_row5_col5" class="data row5 col5" >0.00</td>
      <td id="T_cd292_row5_col6" class="data row5 col6" >0.00</td>
      <td id="T_cd292_row5_col7" class="data row5 col7" >True</td>
      <td id="T_cd292_row5_col8" class="data row5 col8" >0.00</td>
      <td id="T_cd292_row5_col9" class="data row5 col9" >USD</td>
      <td id="T_cd292_row5_col10" class="data row5 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row5_col11" class="data row5 col11" >0.0000%</td>
      <td id="T_cd292_row5_col12" class="data row5 col12" >0.0000%</td>
      <td id="T_cd292_row5_col13" class="data row5 col13" >1.00</td>
      <td id="T_cd292_row5_col14" class="data row5 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_cd292_row6_col0" class="data row6 col0" >2021-05-12</td>
      <td id="T_cd292_row6_col1" class="data row6 col1" >2021-08-12</td>
      <td id="T_cd292_row6_col2" class="data row6 col2" >2021-05-10</td>
      <td id="T_cd292_row6_col3" class="data row6 col3" >2021-08-12</td>
      <td id="T_cd292_row6_col4" class="data row6 col4" >20,000,000.00</td>
      <td id="T_cd292_row6_col5" class="data row6 col5" >0.00</td>
      <td id="T_cd292_row6_col6" class="data row6 col6" >0.00</td>
      <td id="T_cd292_row6_col7" class="data row6 col7" >True</td>
      <td id="T_cd292_row6_col8" class="data row6 col8" >0.00</td>
      <td id="T_cd292_row6_col9" class="data row6 col9" >USD</td>
      <td id="T_cd292_row6_col10" class="data row6 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row6_col11" class="data row6 col11" >0.0000%</td>
      <td id="T_cd292_row6_col12" class="data row6 col12" >0.0000%</td>
      <td id="T_cd292_row6_col13" class="data row6 col13" >1.00</td>
      <td id="T_cd292_row6_col14" class="data row6 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_cd292_row7_col0" class="data row7 col0" >2021-08-12</td>
      <td id="T_cd292_row7_col1" class="data row7 col1" >2021-11-12</td>
      <td id="T_cd292_row7_col2" class="data row7 col2" >2021-08-10</td>
      <td id="T_cd292_row7_col3" class="data row7 col3" >2021-11-12</td>
      <td id="T_cd292_row7_col4" class="data row7 col4" >20,000,000.00</td>
      <td id="T_cd292_row7_col5" class="data row7 col5" >0.00</td>
      <td id="T_cd292_row7_col6" class="data row7 col6" >0.00</td>
      <td id="T_cd292_row7_col7" class="data row7 col7" >True</td>
      <td id="T_cd292_row7_col8" class="data row7 col8" >0.00</td>
      <td id="T_cd292_row7_col9" class="data row7 col9" >USD</td>
      <td id="T_cd292_row7_col10" class="data row7 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row7_col11" class="data row7 col11" >0.0000%</td>
      <td id="T_cd292_row7_col12" class="data row7 col12" >0.0000%</td>
      <td id="T_cd292_row7_col13" class="data row7 col13" >1.00</td>
      <td id="T_cd292_row7_col14" class="data row7 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_cd292_row8_col0" class="data row8 col0" >2021-11-12</td>
      <td id="T_cd292_row8_col1" class="data row8 col1" >2022-02-14</td>
      <td id="T_cd292_row8_col2" class="data row8 col2" >2021-11-10</td>
      <td id="T_cd292_row8_col3" class="data row8 col3" >2022-02-14</td>
      <td id="T_cd292_row8_col4" class="data row8 col4" >20,000,000.00</td>
      <td id="T_cd292_row8_col5" class="data row8 col5" >0.00</td>
      <td id="T_cd292_row8_col6" class="data row8 col6" >0.00</td>
      <td id="T_cd292_row8_col7" class="data row8 col7" >True</td>
      <td id="T_cd292_row8_col8" class="data row8 col8" >0.00</td>
      <td id="T_cd292_row8_col9" class="data row8 col9" >USD</td>
      <td id="T_cd292_row8_col10" class="data row8 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row8_col11" class="data row8 col11" >0.0000%</td>
      <td id="T_cd292_row8_col12" class="data row8 col12" >0.0000%</td>
      <td id="T_cd292_row8_col13" class="data row8 col13" >1.00</td>
      <td id="T_cd292_row8_col14" class="data row8 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_cd292_row9_col0" class="data row9 col0" >2022-02-14</td>
      <td id="T_cd292_row9_col1" class="data row9 col1" >2022-05-12</td>
      <td id="T_cd292_row9_col2" class="data row9 col2" >2022-02-10</td>
      <td id="T_cd292_row9_col3" class="data row9 col3" >2022-05-12</td>
      <td id="T_cd292_row9_col4" class="data row9 col4" >20,000,000.00</td>
      <td id="T_cd292_row9_col5" class="data row9 col5" >0.00</td>
      <td id="T_cd292_row9_col6" class="data row9 col6" >0.00</td>
      <td id="T_cd292_row9_col7" class="data row9 col7" >True</td>
      <td id="T_cd292_row9_col8" class="data row9 col8" >0.00</td>
      <td id="T_cd292_row9_col9" class="data row9 col9" >USD</td>
      <td id="T_cd292_row9_col10" class="data row9 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row9_col11" class="data row9 col11" >0.0000%</td>
      <td id="T_cd292_row9_col12" class="data row9 col12" >0.0000%</td>
      <td id="T_cd292_row9_col13" class="data row9 col13" >1.00</td>
      <td id="T_cd292_row9_col14" class="data row9 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row10" class="row_heading level0 row10" >10</th>
      <td id="T_cd292_row10_col0" class="data row10 col0" >2022-05-12</td>
      <td id="T_cd292_row10_col1" class="data row10 col1" >2022-08-12</td>
      <td id="T_cd292_row10_col2" class="data row10 col2" >2022-05-10</td>
      <td id="T_cd292_row10_col3" class="data row10 col3" >2022-08-12</td>
      <td id="T_cd292_row10_col4" class="data row10 col4" >20,000,000.00</td>
      <td id="T_cd292_row10_col5" class="data row10 col5" >0.00</td>
      <td id="T_cd292_row10_col6" class="data row10 col6" >0.00</td>
      <td id="T_cd292_row10_col7" class="data row10 col7" >True</td>
      <td id="T_cd292_row10_col8" class="data row10 col8" >0.00</td>
      <td id="T_cd292_row10_col9" class="data row10 col9" >USD</td>
      <td id="T_cd292_row10_col10" class="data row10 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row10_col11" class="data row10 col11" >0.0000%</td>
      <td id="T_cd292_row10_col12" class="data row10 col12" >0.0000%</td>
      <td id="T_cd292_row10_col13" class="data row10 col13" >1.00</td>
      <td id="T_cd292_row10_col14" class="data row10 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row11" class="row_heading level0 row11" >11</th>
      <td id="T_cd292_row11_col0" class="data row11 col0" >2022-08-12</td>
      <td id="T_cd292_row11_col1" class="data row11 col1" >2022-11-14</td>
      <td id="T_cd292_row11_col2" class="data row11 col2" >2022-08-10</td>
      <td id="T_cd292_row11_col3" class="data row11 col3" >2022-11-14</td>
      <td id="T_cd292_row11_col4" class="data row11 col4" >20,000,000.00</td>
      <td id="T_cd292_row11_col5" class="data row11 col5" >0.00</td>
      <td id="T_cd292_row11_col6" class="data row11 col6" >0.00</td>
      <td id="T_cd292_row11_col7" class="data row11 col7" >True</td>
      <td id="T_cd292_row11_col8" class="data row11 col8" >0.00</td>
      <td id="T_cd292_row11_col9" class="data row11 col9" >USD</td>
      <td id="T_cd292_row11_col10" class="data row11 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row11_col11" class="data row11 col11" >0.0000%</td>
      <td id="T_cd292_row11_col12" class="data row11 col12" >0.0000%</td>
      <td id="T_cd292_row11_col13" class="data row11 col13" >1.00</td>
      <td id="T_cd292_row11_col14" class="data row11 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row12" class="row_heading level0 row12" >12</th>
      <td id="T_cd292_row12_col0" class="data row12 col0" >2022-11-14</td>
      <td id="T_cd292_row12_col1" class="data row12 col1" >2023-02-13</td>
      <td id="T_cd292_row12_col2" class="data row12 col2" >2022-11-10</td>
      <td id="T_cd292_row12_col3" class="data row12 col3" >2023-02-13</td>
      <td id="T_cd292_row12_col4" class="data row12 col4" >20,000,000.00</td>
      <td id="T_cd292_row12_col5" class="data row12 col5" >0.00</td>
      <td id="T_cd292_row12_col6" class="data row12 col6" >0.00</td>
      <td id="T_cd292_row12_col7" class="data row12 col7" >True</td>
      <td id="T_cd292_row12_col8" class="data row12 col8" >0.00</td>
      <td id="T_cd292_row12_col9" class="data row12 col9" >USD</td>
      <td id="T_cd292_row12_col10" class="data row12 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row12_col11" class="data row12 col11" >0.0000%</td>
      <td id="T_cd292_row12_col12" class="data row12 col12" >0.0000%</td>
      <td id="T_cd292_row12_col13" class="data row12 col13" >1.00</td>
      <td id="T_cd292_row12_col14" class="data row12 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row13" class="row_heading level0 row13" >13</th>
      <td id="T_cd292_row13_col0" class="data row13 col0" >2023-02-13</td>
      <td id="T_cd292_row13_col1" class="data row13 col1" >2023-05-12</td>
      <td id="T_cd292_row13_col2" class="data row13 col2" >2023-02-09</td>
      <td id="T_cd292_row13_col3" class="data row13 col3" >2023-05-12</td>
      <td id="T_cd292_row13_col4" class="data row13 col4" >20,000,000.00</td>
      <td id="T_cd292_row13_col5" class="data row13 col5" >0.00</td>
      <td id="T_cd292_row13_col6" class="data row13 col6" >0.00</td>
      <td id="T_cd292_row13_col7" class="data row13 col7" >True</td>
      <td id="T_cd292_row13_col8" class="data row13 col8" >0.00</td>
      <td id="T_cd292_row13_col9" class="data row13 col9" >USD</td>
      <td id="T_cd292_row13_col10" class="data row13 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row13_col11" class="data row13 col11" >0.0000%</td>
      <td id="T_cd292_row13_col12" class="data row13 col12" >0.0000%</td>
      <td id="T_cd292_row13_col13" class="data row13 col13" >1.00</td>
      <td id="T_cd292_row13_col14" class="data row13 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row14" class="row_heading level0 row14" >14</th>
      <td id="T_cd292_row14_col0" class="data row14 col0" >2023-05-12</td>
      <td id="T_cd292_row14_col1" class="data row14 col1" >2023-08-14</td>
      <td id="T_cd292_row14_col2" class="data row14 col2" >2023-05-10</td>
      <td id="T_cd292_row14_col3" class="data row14 col3" >2023-08-14</td>
      <td id="T_cd292_row14_col4" class="data row14 col4" >20,000,000.00</td>
      <td id="T_cd292_row14_col5" class="data row14 col5" >0.00</td>
      <td id="T_cd292_row14_col6" class="data row14 col6" >0.00</td>
      <td id="T_cd292_row14_col7" class="data row14 col7" >True</td>
      <td id="T_cd292_row14_col8" class="data row14 col8" >0.00</td>
      <td id="T_cd292_row14_col9" class="data row14 col9" >USD</td>
      <td id="T_cd292_row14_col10" class="data row14 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row14_col11" class="data row14 col11" >0.0000%</td>
      <td id="T_cd292_row14_col12" class="data row14 col12" >0.0000%</td>
      <td id="T_cd292_row14_col13" class="data row14 col13" >1.00</td>
      <td id="T_cd292_row14_col14" class="data row14 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row15" class="row_heading level0 row15" >15</th>
      <td id="T_cd292_row15_col0" class="data row15 col0" >2023-08-14</td>
      <td id="T_cd292_row15_col1" class="data row15 col1" >2023-11-13</td>
      <td id="T_cd292_row15_col2" class="data row15 col2" >2023-08-10</td>
      <td id="T_cd292_row15_col3" class="data row15 col3" >2023-11-13</td>
      <td id="T_cd292_row15_col4" class="data row15 col4" >20,000,000.00</td>
      <td id="T_cd292_row15_col5" class="data row15 col5" >0.00</td>
      <td id="T_cd292_row15_col6" class="data row15 col6" >0.00</td>
      <td id="T_cd292_row15_col7" class="data row15 col7" >True</td>
      <td id="T_cd292_row15_col8" class="data row15 col8" >0.00</td>
      <td id="T_cd292_row15_col9" class="data row15 col9" >USD</td>
      <td id="T_cd292_row15_col10" class="data row15 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row15_col11" class="data row15 col11" >0.0000%</td>
      <td id="T_cd292_row15_col12" class="data row15 col12" >0.0000%</td>
      <td id="T_cd292_row15_col13" class="data row15 col13" >1.00</td>
      <td id="T_cd292_row15_col14" class="data row15 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row16" class="row_heading level0 row16" >16</th>
      <td id="T_cd292_row16_col0" class="data row16 col0" >2023-11-13</td>
      <td id="T_cd292_row16_col1" class="data row16 col1" >2024-02-12</td>
      <td id="T_cd292_row16_col2" class="data row16 col2" >2023-11-09</td>
      <td id="T_cd292_row16_col3" class="data row16 col3" >2024-02-12</td>
      <td id="T_cd292_row16_col4" class="data row16 col4" >20,000,000.00</td>
      <td id="T_cd292_row16_col5" class="data row16 col5" >0.00</td>
      <td id="T_cd292_row16_col6" class="data row16 col6" >0.00</td>
      <td id="T_cd292_row16_col7" class="data row16 col7" >True</td>
      <td id="T_cd292_row16_col8" class="data row16 col8" >0.00</td>
      <td id="T_cd292_row16_col9" class="data row16 col9" >USD</td>
      <td id="T_cd292_row16_col10" class="data row16 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row16_col11" class="data row16 col11" >0.0000%</td>
      <td id="T_cd292_row16_col12" class="data row16 col12" >0.0000%</td>
      <td id="T_cd292_row16_col13" class="data row16 col13" >1.00</td>
      <td id="T_cd292_row16_col14" class="data row16 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row17" class="row_heading level0 row17" >17</th>
      <td id="T_cd292_row17_col0" class="data row17 col0" >2024-02-12</td>
      <td id="T_cd292_row17_col1" class="data row17 col1" >2024-05-13</td>
      <td id="T_cd292_row17_col2" class="data row17 col2" >2024-02-08</td>
      <td id="T_cd292_row17_col3" class="data row17 col3" >2024-05-13</td>
      <td id="T_cd292_row17_col4" class="data row17 col4" >20,000,000.00</td>
      <td id="T_cd292_row17_col5" class="data row17 col5" >0.00</td>
      <td id="T_cd292_row17_col6" class="data row17 col6" >0.00</td>
      <td id="T_cd292_row17_col7" class="data row17 col7" >True</td>
      <td id="T_cd292_row17_col8" class="data row17 col8" >0.00</td>
      <td id="T_cd292_row17_col9" class="data row17 col9" >USD</td>
      <td id="T_cd292_row17_col10" class="data row17 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row17_col11" class="data row17 col11" >0.0000%</td>
      <td id="T_cd292_row17_col12" class="data row17 col12" >0.0000%</td>
      <td id="T_cd292_row17_col13" class="data row17 col13" >1.00</td>
      <td id="T_cd292_row17_col14" class="data row17 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row18" class="row_heading level0 row18" >18</th>
      <td id="T_cd292_row18_col0" class="data row18 col0" >2024-05-13</td>
      <td id="T_cd292_row18_col1" class="data row18 col1" >2024-08-12</td>
      <td id="T_cd292_row18_col2" class="data row18 col2" >2024-05-09</td>
      <td id="T_cd292_row18_col3" class="data row18 col3" >2024-08-12</td>
      <td id="T_cd292_row18_col4" class="data row18 col4" >20,000,000.00</td>
      <td id="T_cd292_row18_col5" class="data row18 col5" >0.00</td>
      <td id="T_cd292_row18_col6" class="data row18 col6" >0.00</td>
      <td id="T_cd292_row18_col7" class="data row18 col7" >True</td>
      <td id="T_cd292_row18_col8" class="data row18 col8" >0.00</td>
      <td id="T_cd292_row18_col9" class="data row18 col9" >USD</td>
      <td id="T_cd292_row18_col10" class="data row18 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row18_col11" class="data row18 col11" >0.0000%</td>
      <td id="T_cd292_row18_col12" class="data row18 col12" >0.0000%</td>
      <td id="T_cd292_row18_col13" class="data row18 col13" >1.00</td>
      <td id="T_cd292_row18_col14" class="data row18 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row19" class="row_heading level0 row19" >19</th>
      <td id="T_cd292_row19_col0" class="data row19 col0" >2024-08-12</td>
      <td id="T_cd292_row19_col1" class="data row19 col1" >2024-11-12</td>
      <td id="T_cd292_row19_col2" class="data row19 col2" >2024-08-08</td>
      <td id="T_cd292_row19_col3" class="data row19 col3" >2024-11-12</td>
      <td id="T_cd292_row19_col4" class="data row19 col4" >20,000,000.00</td>
      <td id="T_cd292_row19_col5" class="data row19 col5" >0.00</td>
      <td id="T_cd292_row19_col6" class="data row19 col6" >0.00</td>
      <td id="T_cd292_row19_col7" class="data row19 col7" >True</td>
      <td id="T_cd292_row19_col8" class="data row19 col8" >0.00</td>
      <td id="T_cd292_row19_col9" class="data row19 col9" >USD</td>
      <td id="T_cd292_row19_col10" class="data row19 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row19_col11" class="data row19 col11" >0.0000%</td>
      <td id="T_cd292_row19_col12" class="data row19 col12" >0.0000%</td>
      <td id="T_cd292_row19_col13" class="data row19 col13" >1.00</td>
      <td id="T_cd292_row19_col14" class="data row19 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row20" class="row_heading level0 row20" >20</th>
      <td id="T_cd292_row20_col0" class="data row20 col0" >2024-11-12</td>
      <td id="T_cd292_row20_col1" class="data row20 col1" >2025-02-12</td>
      <td id="T_cd292_row20_col2" class="data row20 col2" >2024-11-08</td>
      <td id="T_cd292_row20_col3" class="data row20 col3" >2025-02-12</td>
      <td id="T_cd292_row20_col4" class="data row20 col4" >20,000,000.00</td>
      <td id="T_cd292_row20_col5" class="data row20 col5" >0.00</td>
      <td id="T_cd292_row20_col6" class="data row20 col6" >0.00</td>
      <td id="T_cd292_row20_col7" class="data row20 col7" >True</td>
      <td id="T_cd292_row20_col8" class="data row20 col8" >0.00</td>
      <td id="T_cd292_row20_col9" class="data row20 col9" >USD</td>
      <td id="T_cd292_row20_col10" class="data row20 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row20_col11" class="data row20 col11" >0.0000%</td>
      <td id="T_cd292_row20_col12" class="data row20 col12" >0.0000%</td>
      <td id="T_cd292_row20_col13" class="data row20 col13" >1.00</td>
      <td id="T_cd292_row20_col14" class="data row20 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row21" class="row_heading level0 row21" >21</th>
      <td id="T_cd292_row21_col0" class="data row21 col0" >2025-02-12</td>
      <td id="T_cd292_row21_col1" class="data row21 col1" >2025-05-12</td>
      <td id="T_cd292_row21_col2" class="data row21 col2" >2025-02-10</td>
      <td id="T_cd292_row21_col3" class="data row21 col3" >2025-05-12</td>
      <td id="T_cd292_row21_col4" class="data row21 col4" >20,000,000.00</td>
      <td id="T_cd292_row21_col5" class="data row21 col5" >0.00</td>
      <td id="T_cd292_row21_col6" class="data row21 col6" >0.00</td>
      <td id="T_cd292_row21_col7" class="data row21 col7" >True</td>
      <td id="T_cd292_row21_col8" class="data row21 col8" >0.00</td>
      <td id="T_cd292_row21_col9" class="data row21 col9" >USD</td>
      <td id="T_cd292_row21_col10" class="data row21 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row21_col11" class="data row21 col11" >0.0000%</td>
      <td id="T_cd292_row21_col12" class="data row21 col12" >0.0000%</td>
      <td id="T_cd292_row21_col13" class="data row21 col13" >1.00</td>
      <td id="T_cd292_row21_col14" class="data row21 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row22" class="row_heading level0 row22" >22</th>
      <td id="T_cd292_row22_col0" class="data row22 col0" >2025-05-12</td>
      <td id="T_cd292_row22_col1" class="data row22 col1" >2025-08-12</td>
      <td id="T_cd292_row22_col2" class="data row22 col2" >2025-05-08</td>
      <td id="T_cd292_row22_col3" class="data row22 col3" >2025-08-12</td>
      <td id="T_cd292_row22_col4" class="data row22 col4" >20,000,000.00</td>
      <td id="T_cd292_row22_col5" class="data row22 col5" >0.00</td>
      <td id="T_cd292_row22_col6" class="data row22 col6" >0.00</td>
      <td id="T_cd292_row22_col7" class="data row22 col7" >True</td>
      <td id="T_cd292_row22_col8" class="data row22 col8" >0.00</td>
      <td id="T_cd292_row22_col9" class="data row22 col9" >USD</td>
      <td id="T_cd292_row22_col10" class="data row22 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row22_col11" class="data row22 col11" >0.0000%</td>
      <td id="T_cd292_row22_col12" class="data row22 col12" >0.0000%</td>
      <td id="T_cd292_row22_col13" class="data row22 col13" >1.00</td>
      <td id="T_cd292_row22_col14" class="data row22 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row23" class="row_heading level0 row23" >23</th>
      <td id="T_cd292_row23_col0" class="data row23 col0" >2025-08-12</td>
      <td id="T_cd292_row23_col1" class="data row23 col1" >2025-11-12</td>
      <td id="T_cd292_row23_col2" class="data row23 col2" >2025-08-08</td>
      <td id="T_cd292_row23_col3" class="data row23 col3" >2025-11-12</td>
      <td id="T_cd292_row23_col4" class="data row23 col4" >20,000,000.00</td>
      <td id="T_cd292_row23_col5" class="data row23 col5" >0.00</td>
      <td id="T_cd292_row23_col6" class="data row23 col6" >0.00</td>
      <td id="T_cd292_row23_col7" class="data row23 col7" >True</td>
      <td id="T_cd292_row23_col8" class="data row23 col8" >0.00</td>
      <td id="T_cd292_row23_col9" class="data row23 col9" >USD</td>
      <td id="T_cd292_row23_col10" class="data row23 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row23_col11" class="data row23 col11" >0.0000%</td>
      <td id="T_cd292_row23_col12" class="data row23 col12" >0.0000%</td>
      <td id="T_cd292_row23_col13" class="data row23 col13" >1.00</td>
      <td id="T_cd292_row23_col14" class="data row23 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row24" class="row_heading level0 row24" >24</th>
      <td id="T_cd292_row24_col0" class="data row24 col0" >2025-11-12</td>
      <td id="T_cd292_row24_col1" class="data row24 col1" >2026-02-12</td>
      <td id="T_cd292_row24_col2" class="data row24 col2" >2025-11-10</td>
      <td id="T_cd292_row24_col3" class="data row24 col3" >2026-02-12</td>
      <td id="T_cd292_row24_col4" class="data row24 col4" >20,000,000.00</td>
      <td id="T_cd292_row24_col5" class="data row24 col5" >0.00</td>
      <td id="T_cd292_row24_col6" class="data row24 col6" >0.00</td>
      <td id="T_cd292_row24_col7" class="data row24 col7" >True</td>
      <td id="T_cd292_row24_col8" class="data row24 col8" >0.00</td>
      <td id="T_cd292_row24_col9" class="data row24 col9" >USD</td>
      <td id="T_cd292_row24_col10" class="data row24 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row24_col11" class="data row24 col11" >0.0000%</td>
      <td id="T_cd292_row24_col12" class="data row24 col12" >0.0000%</td>
      <td id="T_cd292_row24_col13" class="data row24 col13" >1.00</td>
      <td id="T_cd292_row24_col14" class="data row24 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row25" class="row_heading level0 row25" >25</th>
      <td id="T_cd292_row25_col0" class="data row25 col0" >2026-02-12</td>
      <td id="T_cd292_row25_col1" class="data row25 col1" >2026-05-12</td>
      <td id="T_cd292_row25_col2" class="data row25 col2" >2026-02-10</td>
      <td id="T_cd292_row25_col3" class="data row25 col3" >2026-05-12</td>
      <td id="T_cd292_row25_col4" class="data row25 col4" >20,000,000.00</td>
      <td id="T_cd292_row25_col5" class="data row25 col5" >0.00</td>
      <td id="T_cd292_row25_col6" class="data row25 col6" >0.00</td>
      <td id="T_cd292_row25_col7" class="data row25 col7" >True</td>
      <td id="T_cd292_row25_col8" class="data row25 col8" >0.00</td>
      <td id="T_cd292_row25_col9" class="data row25 col9" >USD</td>
      <td id="T_cd292_row25_col10" class="data row25 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row25_col11" class="data row25 col11" >0.0000%</td>
      <td id="T_cd292_row25_col12" class="data row25 col12" >0.0000%</td>
      <td id="T_cd292_row25_col13" class="data row25 col13" >1.00</td>
      <td id="T_cd292_row25_col14" class="data row25 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row26" class="row_heading level0 row26" >26</th>
      <td id="T_cd292_row26_col0" class="data row26 col0" >2026-05-12</td>
      <td id="T_cd292_row26_col1" class="data row26 col1" >2026-08-12</td>
      <td id="T_cd292_row26_col2" class="data row26 col2" >2026-05-08</td>
      <td id="T_cd292_row26_col3" class="data row26 col3" >2026-08-12</td>
      <td id="T_cd292_row26_col4" class="data row26 col4" >20,000,000.00</td>
      <td id="T_cd292_row26_col5" class="data row26 col5" >0.00</td>
      <td id="T_cd292_row26_col6" class="data row26 col6" >0.00</td>
      <td id="T_cd292_row26_col7" class="data row26 col7" >True</td>
      <td id="T_cd292_row26_col8" class="data row26 col8" >0.00</td>
      <td id="T_cd292_row26_col9" class="data row26 col9" >USD</td>
      <td id="T_cd292_row26_col10" class="data row26 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row26_col11" class="data row26 col11" >0.0000%</td>
      <td id="T_cd292_row26_col12" class="data row26 col12" >0.0000%</td>
      <td id="T_cd292_row26_col13" class="data row26 col13" >1.00</td>
      <td id="T_cd292_row26_col14" class="data row26 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row27" class="row_heading level0 row27" >27</th>
      <td id="T_cd292_row27_col0" class="data row27 col0" >2026-08-12</td>
      <td id="T_cd292_row27_col1" class="data row27 col1" >2026-11-12</td>
      <td id="T_cd292_row27_col2" class="data row27 col2" >2026-08-10</td>
      <td id="T_cd292_row27_col3" class="data row27 col3" >2026-11-12</td>
      <td id="T_cd292_row27_col4" class="data row27 col4" >20,000,000.00</td>
      <td id="T_cd292_row27_col5" class="data row27 col5" >0.00</td>
      <td id="T_cd292_row27_col6" class="data row27 col6" >0.00</td>
      <td id="T_cd292_row27_col7" class="data row27 col7" >True</td>
      <td id="T_cd292_row27_col8" class="data row27 col8" >0.00</td>
      <td id="T_cd292_row27_col9" class="data row27 col9" >USD</td>
      <td id="T_cd292_row27_col10" class="data row27 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row27_col11" class="data row27 col11" >0.0000%</td>
      <td id="T_cd292_row27_col12" class="data row27 col12" >0.0000%</td>
      <td id="T_cd292_row27_col13" class="data row27 col13" >1.00</td>
      <td id="T_cd292_row27_col14" class="data row27 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row28" class="row_heading level0 row28" >28</th>
      <td id="T_cd292_row28_col0" class="data row28 col0" >2026-11-12</td>
      <td id="T_cd292_row28_col1" class="data row28 col1" >2027-02-12</td>
      <td id="T_cd292_row28_col2" class="data row28 col2" >2026-11-10</td>
      <td id="T_cd292_row28_col3" class="data row28 col3" >2027-02-12</td>
      <td id="T_cd292_row28_col4" class="data row28 col4" >20,000,000.00</td>
      <td id="T_cd292_row28_col5" class="data row28 col5" >0.00</td>
      <td id="T_cd292_row28_col6" class="data row28 col6" >0.00</td>
      <td id="T_cd292_row28_col7" class="data row28 col7" >True</td>
      <td id="T_cd292_row28_col8" class="data row28 col8" >0.00</td>
      <td id="T_cd292_row28_col9" class="data row28 col9" >USD</td>
      <td id="T_cd292_row28_col10" class="data row28 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row28_col11" class="data row28 col11" >0.0000%</td>
      <td id="T_cd292_row28_col12" class="data row28 col12" >0.0000%</td>
      <td id="T_cd292_row28_col13" class="data row28 col13" >1.00</td>
      <td id="T_cd292_row28_col14" class="data row28 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row29" class="row_heading level0 row29" >29</th>
      <td id="T_cd292_row29_col0" class="data row29 col0" >2027-02-12</td>
      <td id="T_cd292_row29_col1" class="data row29 col1" >2027-05-12</td>
      <td id="T_cd292_row29_col2" class="data row29 col2" >2027-02-10</td>
      <td id="T_cd292_row29_col3" class="data row29 col3" >2027-05-12</td>
      <td id="T_cd292_row29_col4" class="data row29 col4" >20,000,000.00</td>
      <td id="T_cd292_row29_col5" class="data row29 col5" >0.00</td>
      <td id="T_cd292_row29_col6" class="data row29 col6" >0.00</td>
      <td id="T_cd292_row29_col7" class="data row29 col7" >True</td>
      <td id="T_cd292_row29_col8" class="data row29 col8" >0.00</td>
      <td id="T_cd292_row29_col9" class="data row29 col9" >USD</td>
      <td id="T_cd292_row29_col10" class="data row29 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row29_col11" class="data row29 col11" >0.0000%</td>
      <td id="T_cd292_row29_col12" class="data row29 col12" >0.0000%</td>
      <td id="T_cd292_row29_col13" class="data row29 col13" >1.00</td>
      <td id="T_cd292_row29_col14" class="data row29 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row30" class="row_heading level0 row30" >30</th>
      <td id="T_cd292_row30_col0" class="data row30 col0" >2027-05-12</td>
      <td id="T_cd292_row30_col1" class="data row30 col1" >2027-08-12</td>
      <td id="T_cd292_row30_col2" class="data row30 col2" >2027-05-10</td>
      <td id="T_cd292_row30_col3" class="data row30 col3" >2027-08-12</td>
      <td id="T_cd292_row30_col4" class="data row30 col4" >20,000,000.00</td>
      <td id="T_cd292_row30_col5" class="data row30 col5" >0.00</td>
      <td id="T_cd292_row30_col6" class="data row30 col6" >0.00</td>
      <td id="T_cd292_row30_col7" class="data row30 col7" >True</td>
      <td id="T_cd292_row30_col8" class="data row30 col8" >0.00</td>
      <td id="T_cd292_row30_col9" class="data row30 col9" >USD</td>
      <td id="T_cd292_row30_col10" class="data row30 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row30_col11" class="data row30 col11" >0.0000%</td>
      <td id="T_cd292_row30_col12" class="data row30 col12" >0.0000%</td>
      <td id="T_cd292_row30_col13" class="data row30 col13" >1.00</td>
      <td id="T_cd292_row30_col14" class="data row30 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row31" class="row_heading level0 row31" >31</th>
      <td id="T_cd292_row31_col0" class="data row31 col0" >2027-08-12</td>
      <td id="T_cd292_row31_col1" class="data row31 col1" >2027-11-12</td>
      <td id="T_cd292_row31_col2" class="data row31 col2" >2027-08-10</td>
      <td id="T_cd292_row31_col3" class="data row31 col3" >2027-11-12</td>
      <td id="T_cd292_row31_col4" class="data row31 col4" >20,000,000.00</td>
      <td id="T_cd292_row31_col5" class="data row31 col5" >0.00</td>
      <td id="T_cd292_row31_col6" class="data row31 col6" >0.00</td>
      <td id="T_cd292_row31_col7" class="data row31 col7" >True</td>
      <td id="T_cd292_row31_col8" class="data row31 col8" >0.00</td>
      <td id="T_cd292_row31_col9" class="data row31 col9" >USD</td>
      <td id="T_cd292_row31_col10" class="data row31 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row31_col11" class="data row31 col11" >0.0000%</td>
      <td id="T_cd292_row31_col12" class="data row31 col12" >0.0000%</td>
      <td id="T_cd292_row31_col13" class="data row31 col13" >1.00</td>
      <td id="T_cd292_row31_col14" class="data row31 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row32" class="row_heading level0 row32" >32</th>
      <td id="T_cd292_row32_col0" class="data row32 col0" >2027-11-12</td>
      <td id="T_cd292_row32_col1" class="data row32 col1" >2028-02-14</td>
      <td id="T_cd292_row32_col2" class="data row32 col2" >2027-11-10</td>
      <td id="T_cd292_row32_col3" class="data row32 col3" >2028-02-14</td>
      <td id="T_cd292_row32_col4" class="data row32 col4" >20,000,000.00</td>
      <td id="T_cd292_row32_col5" class="data row32 col5" >0.00</td>
      <td id="T_cd292_row32_col6" class="data row32 col6" >0.00</td>
      <td id="T_cd292_row32_col7" class="data row32 col7" >True</td>
      <td id="T_cd292_row32_col8" class="data row32 col8" >0.00</td>
      <td id="T_cd292_row32_col9" class="data row32 col9" >USD</td>
      <td id="T_cd292_row32_col10" class="data row32 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row32_col11" class="data row32 col11" >0.0000%</td>
      <td id="T_cd292_row32_col12" class="data row32 col12" >0.0000%</td>
      <td id="T_cd292_row32_col13" class="data row32 col13" >1.00</td>
      <td id="T_cd292_row32_col14" class="data row32 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row33" class="row_heading level0 row33" >33</th>
      <td id="T_cd292_row33_col0" class="data row33 col0" >2028-02-14</td>
      <td id="T_cd292_row33_col1" class="data row33 col1" >2028-05-12</td>
      <td id="T_cd292_row33_col2" class="data row33 col2" >2028-02-10</td>
      <td id="T_cd292_row33_col3" class="data row33 col3" >2028-05-12</td>
      <td id="T_cd292_row33_col4" class="data row33 col4" >20,000,000.00</td>
      <td id="T_cd292_row33_col5" class="data row33 col5" >0.00</td>
      <td id="T_cd292_row33_col6" class="data row33 col6" >0.00</td>
      <td id="T_cd292_row33_col7" class="data row33 col7" >True</td>
      <td id="T_cd292_row33_col8" class="data row33 col8" >0.00</td>
      <td id="T_cd292_row33_col9" class="data row33 col9" >USD</td>
      <td id="T_cd292_row33_col10" class="data row33 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row33_col11" class="data row33 col11" >0.0000%</td>
      <td id="T_cd292_row33_col12" class="data row33 col12" >0.0000%</td>
      <td id="T_cd292_row33_col13" class="data row33 col13" >1.00</td>
      <td id="T_cd292_row33_col14" class="data row33 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row34" class="row_heading level0 row34" >34</th>
      <td id="T_cd292_row34_col0" class="data row34 col0" >2028-05-12</td>
      <td id="T_cd292_row34_col1" class="data row34 col1" >2028-08-14</td>
      <td id="T_cd292_row34_col2" class="data row34 col2" >2028-05-10</td>
      <td id="T_cd292_row34_col3" class="data row34 col3" >2028-08-14</td>
      <td id="T_cd292_row34_col4" class="data row34 col4" >20,000,000.00</td>
      <td id="T_cd292_row34_col5" class="data row34 col5" >0.00</td>
      <td id="T_cd292_row34_col6" class="data row34 col6" >0.00</td>
      <td id="T_cd292_row34_col7" class="data row34 col7" >True</td>
      <td id="T_cd292_row34_col8" class="data row34 col8" >0.00</td>
      <td id="T_cd292_row34_col9" class="data row34 col9" >USD</td>
      <td id="T_cd292_row34_col10" class="data row34 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row34_col11" class="data row34 col11" >0.0000%</td>
      <td id="T_cd292_row34_col12" class="data row34 col12" >0.0000%</td>
      <td id="T_cd292_row34_col13" class="data row34 col13" >1.00</td>
      <td id="T_cd292_row34_col14" class="data row34 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row35" class="row_heading level0 row35" >35</th>
      <td id="T_cd292_row35_col0" class="data row35 col0" >2028-08-14</td>
      <td id="T_cd292_row35_col1" class="data row35 col1" >2028-11-13</td>
      <td id="T_cd292_row35_col2" class="data row35 col2" >2028-08-10</td>
      <td id="T_cd292_row35_col3" class="data row35 col3" >2028-11-13</td>
      <td id="T_cd292_row35_col4" class="data row35 col4" >20,000,000.00</td>
      <td id="T_cd292_row35_col5" class="data row35 col5" >0.00</td>
      <td id="T_cd292_row35_col6" class="data row35 col6" >0.00</td>
      <td id="T_cd292_row35_col7" class="data row35 col7" >True</td>
      <td id="T_cd292_row35_col8" class="data row35 col8" >0.00</td>
      <td id="T_cd292_row35_col9" class="data row35 col9" >USD</td>
      <td id="T_cd292_row35_col10" class="data row35 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row35_col11" class="data row35 col11" >0.0000%</td>
      <td id="T_cd292_row35_col12" class="data row35 col12" >0.0000%</td>
      <td id="T_cd292_row35_col13" class="data row35 col13" >1.00</td>
      <td id="T_cd292_row35_col14" class="data row35 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row36" class="row_heading level0 row36" >36</th>
      <td id="T_cd292_row36_col0" class="data row36 col0" >2028-11-13</td>
      <td id="T_cd292_row36_col1" class="data row36 col1" >2029-02-12</td>
      <td id="T_cd292_row36_col2" class="data row36 col2" >2028-11-09</td>
      <td id="T_cd292_row36_col3" class="data row36 col3" >2029-02-12</td>
      <td id="T_cd292_row36_col4" class="data row36 col4" >20,000,000.00</td>
      <td id="T_cd292_row36_col5" class="data row36 col5" >0.00</td>
      <td id="T_cd292_row36_col6" class="data row36 col6" >0.00</td>
      <td id="T_cd292_row36_col7" class="data row36 col7" >True</td>
      <td id="T_cd292_row36_col8" class="data row36 col8" >0.00</td>
      <td id="T_cd292_row36_col9" class="data row36 col9" >USD</td>
      <td id="T_cd292_row36_col10" class="data row36 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row36_col11" class="data row36 col11" >0.0000%</td>
      <td id="T_cd292_row36_col12" class="data row36 col12" >0.0000%</td>
      <td id="T_cd292_row36_col13" class="data row36 col13" >1.00</td>
      <td id="T_cd292_row36_col14" class="data row36 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row37" class="row_heading level0 row37" >37</th>
      <td id="T_cd292_row37_col0" class="data row37 col0" >2029-02-12</td>
      <td id="T_cd292_row37_col1" class="data row37 col1" >2029-05-14</td>
      <td id="T_cd292_row37_col2" class="data row37 col2" >2029-02-08</td>
      <td id="T_cd292_row37_col3" class="data row37 col3" >2029-05-14</td>
      <td id="T_cd292_row37_col4" class="data row37 col4" >20,000,000.00</td>
      <td id="T_cd292_row37_col5" class="data row37 col5" >0.00</td>
      <td id="T_cd292_row37_col6" class="data row37 col6" >0.00</td>
      <td id="T_cd292_row37_col7" class="data row37 col7" >True</td>
      <td id="T_cd292_row37_col8" class="data row37 col8" >0.00</td>
      <td id="T_cd292_row37_col9" class="data row37 col9" >USD</td>
      <td id="T_cd292_row37_col10" class="data row37 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row37_col11" class="data row37 col11" >0.0000%</td>
      <td id="T_cd292_row37_col12" class="data row37 col12" >0.0000%</td>
      <td id="T_cd292_row37_col13" class="data row37 col13" >1.00</td>
      <td id="T_cd292_row37_col14" class="data row37 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row38" class="row_heading level0 row38" >38</th>
      <td id="T_cd292_row38_col0" class="data row38 col0" >2029-05-14</td>
      <td id="T_cd292_row38_col1" class="data row38 col1" >2029-08-13</td>
      <td id="T_cd292_row38_col2" class="data row38 col2" >2029-05-10</td>
      <td id="T_cd292_row38_col3" class="data row38 col3" >2029-08-13</td>
      <td id="T_cd292_row38_col4" class="data row38 col4" >20,000,000.00</td>
      <td id="T_cd292_row38_col5" class="data row38 col5" >0.00</td>
      <td id="T_cd292_row38_col6" class="data row38 col6" >0.00</td>
      <td id="T_cd292_row38_col7" class="data row38 col7" >True</td>
      <td id="T_cd292_row38_col8" class="data row38 col8" >0.00</td>
      <td id="T_cd292_row38_col9" class="data row38 col9" >USD</td>
      <td id="T_cd292_row38_col10" class="data row38 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row38_col11" class="data row38 col11" >0.0000%</td>
      <td id="T_cd292_row38_col12" class="data row38 col12" >0.0000%</td>
      <td id="T_cd292_row38_col13" class="data row38 col13" >1.00</td>
      <td id="T_cd292_row38_col14" class="data row38 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_cd292_level0_row39" class="row_heading level0 row39" >39</th>
      <td id="T_cd292_row39_col0" class="data row39 col0" >2029-08-13</td>
      <td id="T_cd292_row39_col1" class="data row39 col1" >2029-11-12</td>
      <td id="T_cd292_row39_col2" class="data row39 col2" >2029-08-09</td>
      <td id="T_cd292_row39_col3" class="data row39 col3" >2029-11-12</td>
      <td id="T_cd292_row39_col4" class="data row39 col4" >20,000,000.00</td>
      <td id="T_cd292_row39_col5" class="data row39 col5" >20,000,000.00</td>
      <td id="T_cd292_row39_col6" class="data row39 col6" >0.00</td>
      <td id="T_cd292_row39_col7" class="data row39 col7" >True</td>
      <td id="T_cd292_row39_col8" class="data row39 col8" >20,000,000.00</td>
      <td id="T_cd292_row39_col9" class="data row39 col9" >USD</td>
      <td id="T_cd292_row39_col10" class="data row39 col10" >LIBORUSD3M</td>
      <td id="T_cd292_row39_col11" class="data row39 col11" >0.0000%</td>
      <td id="T_cd292_row39_col12" class="data row39 col12" >0.0000%</td>
      <td id="T_cd292_row39_col13" class="data row39 col13" >1.00</td>
      <td id="T_cd292_row39_col14" class="data row39 col14" >LinAct360</td>
    </tr>
  </tbody>
</table>





```python
libor = 0.0190063
fecha_hoy = qcf.QCDate(25, 2, 2020)
ibor_leg.get_cashflow_at(0).set_rate_value(libor)
fwd_rates.set_rates_ibor_leg(fecha_hoy, ibor_leg, zz2)
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
<table id="T_a5ea1">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_a5ea1_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_a5ea1_level0_col1" class="col_heading level0 col1" >fecha__final</th>
      <th id="T_a5ea1_level0_col2" class="col_heading level0 col2" >fecha_fixing</th>
      <th id="T_a5ea1_level0_col3" class="col_heading level0 col3" >fecha__pago</th>
      <th id="T_a5ea1_level0_col4" class="col_heading level0 col4" >nominal</th>
      <th id="T_a5ea1_level0_col5" class="col_heading level0 col5" >amort</th>
      <th id="T_a5ea1_level0_col6" class="col_heading level0 col6" >interes</th>
      <th id="T_a5ea1_level0_col7" class="col_heading level0 col7" >amort_es_flujo</th>
      <th id="T_a5ea1_level0_col8" class="col_heading level0 col8" >flujo</th>
      <th id="T_a5ea1_level0_col9" class="col_heading level0 col9" >moneda</th>
      <th id="T_a5ea1_level0_col10" class="col_heading level0 col10" >codigo_indice</th>
      <th id="T_a5ea1_level0_col11" class="col_heading level0 col11" >valor_tasa</th>
      <th id="T_a5ea1_level0_col12" class="col_heading level0 col12" >spread</th>
      <th id="T_a5ea1_level0_col13" class="col_heading level0 col13" >gearing</th>
      <th id="T_a5ea1_level0_col14" class="col_heading level0 col14" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_a5ea1_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_a5ea1_row0_col0" class="data row0 col0" >2019-11-12</td>
      <td id="T_a5ea1_row0_col1" class="data row0 col1" >2020-02-12</td>
      <td id="T_a5ea1_row0_col2" class="data row0 col2" >2019-11-08</td>
      <td id="T_a5ea1_row0_col3" class="data row0 col3" >2020-02-12</td>
      <td id="T_a5ea1_row0_col4" class="data row0 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row0_col5" class="data row0 col5" >0.00</td>
      <td id="T_a5ea1_row0_col6" class="data row0 col6" >97,143.31</td>
      <td id="T_a5ea1_row0_col7" class="data row0 col7" >True</td>
      <td id="T_a5ea1_row0_col8" class="data row0 col8" >97,143.31</td>
      <td id="T_a5ea1_row0_col9" class="data row0 col9" >USD</td>
      <td id="T_a5ea1_row0_col10" class="data row0 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row0_col11" class="data row0 col11" >1.9006%</td>
      <td id="T_a5ea1_row0_col12" class="data row0 col12" >0.0000%</td>
      <td id="T_a5ea1_row0_col13" class="data row0 col13" >1.00</td>
      <td id="T_a5ea1_row0_col14" class="data row0 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_a5ea1_row1_col0" class="data row1 col0" >2020-02-12</td>
      <td id="T_a5ea1_row1_col1" class="data row1 col1" >2020-05-12</td>
      <td id="T_a5ea1_row1_col2" class="data row1 col2" >2020-02-10</td>
      <td id="T_a5ea1_row1_col3" class="data row1 col3" >2020-05-12</td>
      <td id="T_a5ea1_row1_col4" class="data row1 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row1_col5" class="data row1 col5" >0.00</td>
      <td id="T_a5ea1_row1_col6" class="data row1 col6" >0.00</td>
      <td id="T_a5ea1_row1_col7" class="data row1 col7" >True</td>
      <td id="T_a5ea1_row1_col8" class="data row1 col8" >0.00</td>
      <td id="T_a5ea1_row1_col9" class="data row1 col9" >USD</td>
      <td id="T_a5ea1_row1_col10" class="data row1 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row1_col11" class="data row1 col11" >0.0000%</td>
      <td id="T_a5ea1_row1_col12" class="data row1 col12" >0.0000%</td>
      <td id="T_a5ea1_row1_col13" class="data row1 col13" >1.00</td>
      <td id="T_a5ea1_row1_col14" class="data row1 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_a5ea1_row2_col0" class="data row2 col0" >2020-05-12</td>
      <td id="T_a5ea1_row2_col1" class="data row2 col1" >2020-08-12</td>
      <td id="T_a5ea1_row2_col2" class="data row2 col2" >2020-05-08</td>
      <td id="T_a5ea1_row2_col3" class="data row2 col3" >2020-08-12</td>
      <td id="T_a5ea1_row2_col4" class="data row2 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row2_col5" class="data row2 col5" >0.00</td>
      <td id="T_a5ea1_row2_col6" class="data row2 col6" >87,136.92</td>
      <td id="T_a5ea1_row2_col7" class="data row2 col7" >True</td>
      <td id="T_a5ea1_row2_col8" class="data row2 col8" >87,136.92</td>
      <td id="T_a5ea1_row2_col9" class="data row2 col9" >USD</td>
      <td id="T_a5ea1_row2_col10" class="data row2 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row2_col11" class="data row2 col11" >1.7049%</td>
      <td id="T_a5ea1_row2_col12" class="data row2 col12" >0.0000%</td>
      <td id="T_a5ea1_row2_col13" class="data row2 col13" >1.00</td>
      <td id="T_a5ea1_row2_col14" class="data row2 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_a5ea1_row3_col0" class="data row3 col0" >2020-08-12</td>
      <td id="T_a5ea1_row3_col1" class="data row3 col1" >2020-11-12</td>
      <td id="T_a5ea1_row3_col2" class="data row3 col2" >2020-08-10</td>
      <td id="T_a5ea1_row3_col3" class="data row3 col3" >2020-11-12</td>
      <td id="T_a5ea1_row3_col4" class="data row3 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row3_col5" class="data row3 col5" >0.00</td>
      <td id="T_a5ea1_row3_col6" class="data row3 col6" >83,357.57</td>
      <td id="T_a5ea1_row3_col7" class="data row3 col7" >True</td>
      <td id="T_a5ea1_row3_col8" class="data row3 col8" >83,357.57</td>
      <td id="T_a5ea1_row3_col9" class="data row3 col9" >USD</td>
      <td id="T_a5ea1_row3_col10" class="data row3 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row3_col11" class="data row3 col11" >1.6309%</td>
      <td id="T_a5ea1_row3_col12" class="data row3 col12" >0.0000%</td>
      <td id="T_a5ea1_row3_col13" class="data row3 col13" >1.00</td>
      <td id="T_a5ea1_row3_col14" class="data row3 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_a5ea1_row4_col0" class="data row4 col0" >2020-11-12</td>
      <td id="T_a5ea1_row4_col1" class="data row4 col1" >2021-02-12</td>
      <td id="T_a5ea1_row4_col2" class="data row4 col2" >2020-11-10</td>
      <td id="T_a5ea1_row4_col3" class="data row4 col3" >2021-02-12</td>
      <td id="T_a5ea1_row4_col4" class="data row4 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row4_col5" class="data row4 col5" >0.00</td>
      <td id="T_a5ea1_row4_col6" class="data row4 col6" >79,834.14</td>
      <td id="T_a5ea1_row4_col7" class="data row4 col7" >True</td>
      <td id="T_a5ea1_row4_col8" class="data row4 col8" >79,834.14</td>
      <td id="T_a5ea1_row4_col9" class="data row4 col9" >USD</td>
      <td id="T_a5ea1_row4_col10" class="data row4 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row4_col11" class="data row4 col11" >1.5620%</td>
      <td id="T_a5ea1_row4_col12" class="data row4 col12" >0.0000%</td>
      <td id="T_a5ea1_row4_col13" class="data row4 col13" >1.00</td>
      <td id="T_a5ea1_row4_col14" class="data row4 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_a5ea1_row5_col0" class="data row5 col0" >2021-02-12</td>
      <td id="T_a5ea1_row5_col1" class="data row5 col1" >2021-05-12</td>
      <td id="T_a5ea1_row5_col2" class="data row5 col2" >2021-02-10</td>
      <td id="T_a5ea1_row5_col3" class="data row5 col3" >2021-05-12</td>
      <td id="T_a5ea1_row5_col4" class="data row5 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row5_col5" class="data row5 col5" >0.00</td>
      <td id="T_a5ea1_row5_col6" class="data row5 col6" >75,388.80</td>
      <td id="T_a5ea1_row5_col7" class="data row5 col7" >True</td>
      <td id="T_a5ea1_row5_col8" class="data row5 col8" >75,388.80</td>
      <td id="T_a5ea1_row5_col9" class="data row5 col9" >USD</td>
      <td id="T_a5ea1_row5_col10" class="data row5 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row5_col11" class="data row5 col11" >1.5247%</td>
      <td id="T_a5ea1_row5_col12" class="data row5 col12" >0.0000%</td>
      <td id="T_a5ea1_row5_col13" class="data row5 col13" >1.00</td>
      <td id="T_a5ea1_row5_col14" class="data row5 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_a5ea1_row6_col0" class="data row6 col0" >2021-05-12</td>
      <td id="T_a5ea1_row6_col1" class="data row6 col1" >2021-08-12</td>
      <td id="T_a5ea1_row6_col2" class="data row6 col2" >2021-05-10</td>
      <td id="T_a5ea1_row6_col3" class="data row6 col3" >2021-08-12</td>
      <td id="T_a5ea1_row6_col4" class="data row6 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row6_col5" class="data row6 col5" >0.00</td>
      <td id="T_a5ea1_row6_col6" class="data row6 col6" >75,147.35</td>
      <td id="T_a5ea1_row6_col7" class="data row6 col7" >True</td>
      <td id="T_a5ea1_row6_col8" class="data row6 col8" >75,147.35</td>
      <td id="T_a5ea1_row6_col9" class="data row6 col9" >USD</td>
      <td id="T_a5ea1_row6_col10" class="data row6 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row6_col11" class="data row6 col11" >1.4703%</td>
      <td id="T_a5ea1_row6_col12" class="data row6 col12" >0.0000%</td>
      <td id="T_a5ea1_row6_col13" class="data row6 col13" >1.00</td>
      <td id="T_a5ea1_row6_col14" class="data row6 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_a5ea1_row7_col0" class="data row7 col0" >2021-08-12</td>
      <td id="T_a5ea1_row7_col1" class="data row7 col1" >2021-11-12</td>
      <td id="T_a5ea1_row7_col2" class="data row7 col2" >2021-08-10</td>
      <td id="T_a5ea1_row7_col3" class="data row7 col3" >2021-11-12</td>
      <td id="T_a5ea1_row7_col4" class="data row7 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row7_col5" class="data row7 col5" >0.00</td>
      <td id="T_a5ea1_row7_col6" class="data row7 col6" >75,919.01</td>
      <td id="T_a5ea1_row7_col7" class="data row7 col7" >True</td>
      <td id="T_a5ea1_row7_col8" class="data row7 col8" >75,919.01</td>
      <td id="T_a5ea1_row7_col9" class="data row7 col9" >USD</td>
      <td id="T_a5ea1_row7_col10" class="data row7 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row7_col11" class="data row7 col11" >1.4854%</td>
      <td id="T_a5ea1_row7_col12" class="data row7 col12" >0.0000%</td>
      <td id="T_a5ea1_row7_col13" class="data row7 col13" >1.00</td>
      <td id="T_a5ea1_row7_col14" class="data row7 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_a5ea1_row8_col0" class="data row8 col0" >2021-11-12</td>
      <td id="T_a5ea1_row8_col1" class="data row8 col1" >2022-02-14</td>
      <td id="T_a5ea1_row8_col2" class="data row8 col2" >2021-11-10</td>
      <td id="T_a5ea1_row8_col3" class="data row8 col3" >2022-02-14</td>
      <td id="T_a5ea1_row8_col4" class="data row8 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row8_col5" class="data row8 col5" >0.00</td>
      <td id="T_a5ea1_row8_col6" class="data row8 col6" >76,541.33</td>
      <td id="T_a5ea1_row8_col7" class="data row8 col7" >True</td>
      <td id="T_a5ea1_row8_col8" class="data row8 col8" >76,541.33</td>
      <td id="T_a5ea1_row8_col9" class="data row8 col9" >USD</td>
      <td id="T_a5ea1_row8_col10" class="data row8 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row8_col11" class="data row8 col11" >1.4657%</td>
      <td id="T_a5ea1_row8_col12" class="data row8 col12" >0.0000%</td>
      <td id="T_a5ea1_row8_col13" class="data row8 col13" >1.00</td>
      <td id="T_a5ea1_row8_col14" class="data row8 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_a5ea1_row9_col0" class="data row9 col0" >2022-02-14</td>
      <td id="T_a5ea1_row9_col1" class="data row9 col1" >2022-05-12</td>
      <td id="T_a5ea1_row9_col2" class="data row9 col2" >2022-02-10</td>
      <td id="T_a5ea1_row9_col3" class="data row9 col3" >2022-05-12</td>
      <td id="T_a5ea1_row9_col4" class="data row9 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row9_col5" class="data row9 col5" >0.00</td>
      <td id="T_a5ea1_row9_col6" class="data row9 col6" >72,657.16</td>
      <td id="T_a5ea1_row9_col7" class="data row9 col7" >True</td>
      <td id="T_a5ea1_row9_col8" class="data row9 col8" >72,657.16</td>
      <td id="T_a5ea1_row9_col9" class="data row9 col9" >USD</td>
      <td id="T_a5ea1_row9_col10" class="data row9 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row9_col11" class="data row9 col11" >1.5033%</td>
      <td id="T_a5ea1_row9_col12" class="data row9 col12" >0.0000%</td>
      <td id="T_a5ea1_row9_col13" class="data row9 col13" >1.00</td>
      <td id="T_a5ea1_row9_col14" class="data row9 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row10" class="row_heading level0 row10" >10</th>
      <td id="T_a5ea1_row10_col0" class="data row10 col0" >2022-05-12</td>
      <td id="T_a5ea1_row10_col1" class="data row10 col1" >2022-08-12</td>
      <td id="T_a5ea1_row10_col2" class="data row10 col2" >2022-05-10</td>
      <td id="T_a5ea1_row10_col3" class="data row10 col3" >2022-08-12</td>
      <td id="T_a5ea1_row10_col4" class="data row10 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row10_col5" class="data row10 col5" >0.00</td>
      <td id="T_a5ea1_row10_col6" class="data row10 col6" >76,607.00</td>
      <td id="T_a5ea1_row10_col7" class="data row10 col7" >True</td>
      <td id="T_a5ea1_row10_col8" class="data row10 col8" >76,607.00</td>
      <td id="T_a5ea1_row10_col9" class="data row10 col9" >USD</td>
      <td id="T_a5ea1_row10_col10" class="data row10 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row10_col11" class="data row10 col11" >1.4988%</td>
      <td id="T_a5ea1_row10_col12" class="data row10 col12" >0.0000%</td>
      <td id="T_a5ea1_row10_col13" class="data row10 col13" >1.00</td>
      <td id="T_a5ea1_row10_col14" class="data row10 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row11" class="row_heading level0 row11" >11</th>
      <td id="T_a5ea1_row11_col0" class="data row11 col0" >2022-08-12</td>
      <td id="T_a5ea1_row11_col1" class="data row11 col1" >2022-11-14</td>
      <td id="T_a5ea1_row11_col2" class="data row11 col2" >2022-08-10</td>
      <td id="T_a5ea1_row11_col3" class="data row11 col3" >2022-11-14</td>
      <td id="T_a5ea1_row11_col4" class="data row11 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row11_col5" class="data row11 col5" >0.00</td>
      <td id="T_a5ea1_row11_col6" class="data row11 col6" >77,567.48</td>
      <td id="T_a5ea1_row11_col7" class="data row11 col7" >True</td>
      <td id="T_a5ea1_row11_col8" class="data row11 col8" >77,567.48</td>
      <td id="T_a5ea1_row11_col9" class="data row11 col9" >USD</td>
      <td id="T_a5ea1_row11_col10" class="data row11 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row11_col11" class="data row11 col11" >1.4853%</td>
      <td id="T_a5ea1_row11_col12" class="data row11 col12" >0.0000%</td>
      <td id="T_a5ea1_row11_col13" class="data row11 col13" >1.00</td>
      <td id="T_a5ea1_row11_col14" class="data row11 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row12" class="row_heading level0 row12" >12</th>
      <td id="T_a5ea1_row12_col0" class="data row12 col0" >2022-11-14</td>
      <td id="T_a5ea1_row12_col1" class="data row12 col1" >2023-02-13</td>
      <td id="T_a5ea1_row12_col2" class="data row12 col2" >2022-11-10</td>
      <td id="T_a5ea1_row12_col3" class="data row12 col3" >2023-02-13</td>
      <td id="T_a5ea1_row12_col4" class="data row12 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row12_col5" class="data row12 col5" >0.00</td>
      <td id="T_a5ea1_row12_col6" class="data row12 col6" >74,410.06</td>
      <td id="T_a5ea1_row12_col7" class="data row12 col7" >True</td>
      <td id="T_a5ea1_row12_col8" class="data row12 col8" >74,410.06</td>
      <td id="T_a5ea1_row12_col9" class="data row12 col9" >USD</td>
      <td id="T_a5ea1_row12_col10" class="data row12 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row12_col11" class="data row12 col11" >1.4718%</td>
      <td id="T_a5ea1_row12_col12" class="data row12 col12" >0.0000%</td>
      <td id="T_a5ea1_row12_col13" class="data row12 col13" >1.00</td>
      <td id="T_a5ea1_row12_col14" class="data row12 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row13" class="row_heading level0 row13" >13</th>
      <td id="T_a5ea1_row13_col0" class="data row13 col0" >2023-02-13</td>
      <td id="T_a5ea1_row13_col1" class="data row13 col1" >2023-05-12</td>
      <td id="T_a5ea1_row13_col2" class="data row13 col2" >2023-02-09</td>
      <td id="T_a5ea1_row13_col3" class="data row13 col3" >2023-05-12</td>
      <td id="T_a5ea1_row13_col4" class="data row13 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row13_col5" class="data row13 col5" >0.00</td>
      <td id="T_a5ea1_row13_col6" class="data row13 col6" >74,928.43</td>
      <td id="T_a5ea1_row13_col7" class="data row13 col7" >True</td>
      <td id="T_a5ea1_row13_col8" class="data row13 col8" >74,928.43</td>
      <td id="T_a5ea1_row13_col9" class="data row13 col9" >USD</td>
      <td id="T_a5ea1_row13_col10" class="data row13 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row13_col11" class="data row13 col11" >1.5326%</td>
      <td id="T_a5ea1_row13_col12" class="data row13 col12" >0.0000%</td>
      <td id="T_a5ea1_row13_col13" class="data row13 col13" >1.00</td>
      <td id="T_a5ea1_row13_col14" class="data row13 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row14" class="row_heading level0 row14" >14</th>
      <td id="T_a5ea1_row14_col0" class="data row14 col0" >2023-05-12</td>
      <td id="T_a5ea1_row14_col1" class="data row14 col1" >2023-08-14</td>
      <td id="T_a5ea1_row14_col2" class="data row14 col2" >2023-05-10</td>
      <td id="T_a5ea1_row14_col3" class="data row14 col3" >2023-08-14</td>
      <td id="T_a5ea1_row14_col4" class="data row14 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row14_col5" class="data row14 col5" >0.00</td>
      <td id="T_a5ea1_row14_col6" class="data row14 col6" >80,562.98</td>
      <td id="T_a5ea1_row14_col7" class="data row14 col7" >True</td>
      <td id="T_a5ea1_row14_col8" class="data row14 col8" >80,562.98</td>
      <td id="T_a5ea1_row14_col9" class="data row14 col9" >USD</td>
      <td id="T_a5ea1_row14_col10" class="data row14 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row14_col11" class="data row14 col11" >1.5427%</td>
      <td id="T_a5ea1_row14_col12" class="data row14 col12" >0.0000%</td>
      <td id="T_a5ea1_row14_col13" class="data row14 col13" >1.00</td>
      <td id="T_a5ea1_row14_col14" class="data row14 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row15" class="row_heading level0 row15" >15</th>
      <td id="T_a5ea1_row15_col0" class="data row15 col0" >2023-08-14</td>
      <td id="T_a5ea1_row15_col1" class="data row15 col1" >2023-11-13</td>
      <td id="T_a5ea1_row15_col2" class="data row15 col2" >2023-08-10</td>
      <td id="T_a5ea1_row15_col3" class="data row15 col3" >2023-11-13</td>
      <td id="T_a5ea1_row15_col4" class="data row15 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row15_col5" class="data row15 col5" >0.00</td>
      <td id="T_a5ea1_row15_col6" class="data row15 col6" >77,966.23</td>
      <td id="T_a5ea1_row15_col7" class="data row15 col7" >True</td>
      <td id="T_a5ea1_row15_col8" class="data row15 col8" >77,966.23</td>
      <td id="T_a5ea1_row15_col9" class="data row15 col9" >USD</td>
      <td id="T_a5ea1_row15_col10" class="data row15 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row15_col11" class="data row15 col11" >1.5422%</td>
      <td id="T_a5ea1_row15_col12" class="data row15 col12" >0.0000%</td>
      <td id="T_a5ea1_row15_col13" class="data row15 col13" >1.00</td>
      <td id="T_a5ea1_row15_col14" class="data row15 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row16" class="row_heading level0 row16" >16</th>
      <td id="T_a5ea1_row16_col0" class="data row16 col0" >2023-11-13</td>
      <td id="T_a5ea1_row16_col1" class="data row16 col1" >2024-02-12</td>
      <td id="T_a5ea1_row16_col2" class="data row16 col2" >2023-11-09</td>
      <td id="T_a5ea1_row16_col3" class="data row16 col3" >2024-02-12</td>
      <td id="T_a5ea1_row16_col4" class="data row16 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row16_col5" class="data row16 col5" >0.00</td>
      <td id="T_a5ea1_row16_col6" class="data row16 col6" >77,943.52</td>
      <td id="T_a5ea1_row16_col7" class="data row16 col7" >True</td>
      <td id="T_a5ea1_row16_col8" class="data row16 col8" >77,943.52</td>
      <td id="T_a5ea1_row16_col9" class="data row16 col9" >USD</td>
      <td id="T_a5ea1_row16_col10" class="data row16 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row16_col11" class="data row16 col11" >1.5417%</td>
      <td id="T_a5ea1_row16_col12" class="data row16 col12" >0.0000%</td>
      <td id="T_a5ea1_row16_col13" class="data row16 col13" >1.00</td>
      <td id="T_a5ea1_row16_col14" class="data row16 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row17" class="row_heading level0 row17" >17</th>
      <td id="T_a5ea1_row17_col0" class="data row17 col0" >2024-02-12</td>
      <td id="T_a5ea1_row17_col1" class="data row17 col1" >2024-05-13</td>
      <td id="T_a5ea1_row17_col2" class="data row17 col2" >2024-02-08</td>
      <td id="T_a5ea1_row17_col3" class="data row17 col3" >2024-05-13</td>
      <td id="T_a5ea1_row17_col4" class="data row17 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row17_col5" class="data row17 col5" >0.00</td>
      <td id="T_a5ea1_row17_col6" class="data row17 col6" >80,765.17</td>
      <td id="T_a5ea1_row17_col7" class="data row17 col7" >True</td>
      <td id="T_a5ea1_row17_col8" class="data row17 col8" >80,765.17</td>
      <td id="T_a5ea1_row17_col9" class="data row17 col9" >USD</td>
      <td id="T_a5ea1_row17_col10" class="data row17 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row17_col11" class="data row17 col11" >1.5976%</td>
      <td id="T_a5ea1_row17_col12" class="data row17 col12" >0.0000%</td>
      <td id="T_a5ea1_row17_col13" class="data row17 col13" >1.00</td>
      <td id="T_a5ea1_row17_col14" class="data row17 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row18" class="row_heading level0 row18" >18</th>
      <td id="T_a5ea1_row18_col0" class="data row18 col0" >2024-05-13</td>
      <td id="T_a5ea1_row18_col1" class="data row18 col1" >2024-08-12</td>
      <td id="T_a5ea1_row18_col2" class="data row18 col2" >2024-05-09</td>
      <td id="T_a5ea1_row18_col3" class="data row18 col3" >2024-08-12</td>
      <td id="T_a5ea1_row18_col4" class="data row18 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row18_col5" class="data row18 col5" >0.00</td>
      <td id="T_a5ea1_row18_col6" class="data row18 col6" >81,557.64</td>
      <td id="T_a5ea1_row18_col7" class="data row18 col7" >True</td>
      <td id="T_a5ea1_row18_col8" class="data row18 col8" >81,557.64</td>
      <td id="T_a5ea1_row18_col9" class="data row18 col9" >USD</td>
      <td id="T_a5ea1_row18_col10" class="data row18 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row18_col11" class="data row18 col11" >1.6132%</td>
      <td id="T_a5ea1_row18_col12" class="data row18 col12" >0.0000%</td>
      <td id="T_a5ea1_row18_col13" class="data row18 col13" >1.00</td>
      <td id="T_a5ea1_row18_col14" class="data row18 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row19" class="row_heading level0 row19" >19</th>
      <td id="T_a5ea1_row19_col0" class="data row19 col0" >2024-08-12</td>
      <td id="T_a5ea1_row19_col1" class="data row19 col1" >2024-11-12</td>
      <td id="T_a5ea1_row19_col2" class="data row19 col2" >2024-08-08</td>
      <td id="T_a5ea1_row19_col3" class="data row19 col3" >2024-11-12</td>
      <td id="T_a5ea1_row19_col4" class="data row19 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row19_col5" class="data row19 col5" >0.00</td>
      <td id="T_a5ea1_row19_col6" class="data row19 col6" >82,792.65</td>
      <td id="T_a5ea1_row19_col7" class="data row19 col7" >True</td>
      <td id="T_a5ea1_row19_col8" class="data row19 col8" >82,792.65</td>
      <td id="T_a5ea1_row19_col9" class="data row19 col9" >USD</td>
      <td id="T_a5ea1_row19_col10" class="data row19 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row19_col11" class="data row19 col11" >1.6199%</td>
      <td id="T_a5ea1_row19_col12" class="data row19 col12" >0.0000%</td>
      <td id="T_a5ea1_row19_col13" class="data row19 col13" >1.00</td>
      <td id="T_a5ea1_row19_col14" class="data row19 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row20" class="row_heading level0 row20" >20</th>
      <td id="T_a5ea1_row20_col0" class="data row20 col0" >2024-11-12</td>
      <td id="T_a5ea1_row20_col1" class="data row20 col1" >2025-02-12</td>
      <td id="T_a5ea1_row20_col2" class="data row20 col2" >2024-11-08</td>
      <td id="T_a5ea1_row20_col3" class="data row20 col3" >2025-02-12</td>
      <td id="T_a5ea1_row20_col4" class="data row20 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row20_col5" class="data row20 col5" >0.00</td>
      <td id="T_a5ea1_row20_col6" class="data row20 col6" >83,129.55</td>
      <td id="T_a5ea1_row20_col7" class="data row20 col7" >True</td>
      <td id="T_a5ea1_row20_col8" class="data row20 col8" >83,129.55</td>
      <td id="T_a5ea1_row20_col9" class="data row20 col9" >USD</td>
      <td id="T_a5ea1_row20_col10" class="data row20 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row20_col11" class="data row20 col11" >1.6264%</td>
      <td id="T_a5ea1_row20_col12" class="data row20 col12" >0.0000%</td>
      <td id="T_a5ea1_row20_col13" class="data row20 col13" >1.00</td>
      <td id="T_a5ea1_row20_col14" class="data row20 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row21" class="row_heading level0 row21" >21</th>
      <td id="T_a5ea1_row21_col0" class="data row21 col0" >2025-02-12</td>
      <td id="T_a5ea1_row21_col1" class="data row21 col1" >2025-05-12</td>
      <td id="T_a5ea1_row21_col2" class="data row21 col2" >2025-02-10</td>
      <td id="T_a5ea1_row21_col3" class="data row21 col3" >2025-05-12</td>
      <td id="T_a5ea1_row21_col4" class="data row21 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row21_col5" class="data row21 col5" >0.00</td>
      <td id="T_a5ea1_row21_col6" class="data row21 col6" >83,469.23</td>
      <td id="T_a5ea1_row21_col7" class="data row21 col7" >True</td>
      <td id="T_a5ea1_row21_col8" class="data row21 col8" >83,469.23</td>
      <td id="T_a5ea1_row21_col9" class="data row21 col9" >USD</td>
      <td id="T_a5ea1_row21_col10" class="data row21 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row21_col11" class="data row21 col11" >1.6881%</td>
      <td id="T_a5ea1_row21_col12" class="data row21 col12" >0.0000%</td>
      <td id="T_a5ea1_row21_col13" class="data row21 col13" >1.00</td>
      <td id="T_a5ea1_row21_col14" class="data row21 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row22" class="row_heading level0 row22" >22</th>
      <td id="T_a5ea1_row22_col0" class="data row22 col0" >2025-05-12</td>
      <td id="T_a5ea1_row22_col1" class="data row22 col1" >2025-08-12</td>
      <td id="T_a5ea1_row22_col2" class="data row22 col2" >2025-05-08</td>
      <td id="T_a5ea1_row22_col3" class="data row22 col3" >2025-08-12</td>
      <td id="T_a5ea1_row22_col4" class="data row22 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row22_col5" class="data row22 col5" >0.00</td>
      <td id="T_a5ea1_row22_col6" class="data row22 col6" >87,360.07</td>
      <td id="T_a5ea1_row22_col7" class="data row22 col7" >True</td>
      <td id="T_a5ea1_row22_col8" class="data row22 col8" >87,360.07</td>
      <td id="T_a5ea1_row22_col9" class="data row22 col9" >USD</td>
      <td id="T_a5ea1_row22_col10" class="data row22 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row22_col11" class="data row22 col11" >1.7092%</td>
      <td id="T_a5ea1_row22_col12" class="data row22 col12" >0.0000%</td>
      <td id="T_a5ea1_row22_col13" class="data row22 col13" >1.00</td>
      <td id="T_a5ea1_row22_col14" class="data row22 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row23" class="row_heading level0 row23" >23</th>
      <td id="T_a5ea1_row23_col0" class="data row23 col0" >2025-08-12</td>
      <td id="T_a5ea1_row23_col1" class="data row23 col1" >2025-11-12</td>
      <td id="T_a5ea1_row23_col2" class="data row23 col2" >2025-08-08</td>
      <td id="T_a5ea1_row23_col3" class="data row23 col3" >2025-11-12</td>
      <td id="T_a5ea1_row23_col4" class="data row23 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row23_col5" class="data row23 col5" >0.00</td>
      <td id="T_a5ea1_row23_col6" class="data row23 col6" >87,967.87</td>
      <td id="T_a5ea1_row23_col7" class="data row23 col7" >True</td>
      <td id="T_a5ea1_row23_col8" class="data row23 col8" >87,967.87</td>
      <td id="T_a5ea1_row23_col9" class="data row23 col9" >USD</td>
      <td id="T_a5ea1_row23_col10" class="data row23 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row23_col11" class="data row23 col11" >1.7211%</td>
      <td id="T_a5ea1_row23_col12" class="data row23 col12" >0.0000%</td>
      <td id="T_a5ea1_row23_col13" class="data row23 col13" >1.00</td>
      <td id="T_a5ea1_row23_col14" class="data row23 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row24" class="row_heading level0 row24" >24</th>
      <td id="T_a5ea1_row24_col0" class="data row24 col0" >2025-11-12</td>
      <td id="T_a5ea1_row24_col1" class="data row24 col1" >2026-02-12</td>
      <td id="T_a5ea1_row24_col2" class="data row24 col2" >2025-11-10</td>
      <td id="T_a5ea1_row24_col3" class="data row24 col3" >2026-02-12</td>
      <td id="T_a5ea1_row24_col4" class="data row24 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row24_col5" class="data row24 col5" >0.00</td>
      <td id="T_a5ea1_row24_col6" class="data row24 col6" >88,566.05</td>
      <td id="T_a5ea1_row24_col7" class="data row24 col7" >True</td>
      <td id="T_a5ea1_row24_col8" class="data row24 col8" >88,566.05</td>
      <td id="T_a5ea1_row24_col9" class="data row24 col9" >USD</td>
      <td id="T_a5ea1_row24_col10" class="data row24 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row24_col11" class="data row24 col11" >1.7328%</td>
      <td id="T_a5ea1_row24_col12" class="data row24 col12" >0.0000%</td>
      <td id="T_a5ea1_row24_col13" class="data row24 col13" >1.00</td>
      <td id="T_a5ea1_row24_col14" class="data row24 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row25" class="row_heading level0 row25" >25</th>
      <td id="T_a5ea1_row25_col0" class="data row25 col0" >2026-02-12</td>
      <td id="T_a5ea1_row25_col1" class="data row25 col1" >2026-05-12</td>
      <td id="T_a5ea1_row25_col2" class="data row25 col2" >2026-02-10</td>
      <td id="T_a5ea1_row25_col3" class="data row25 col3" >2026-05-12</td>
      <td id="T_a5ea1_row25_col4" class="data row25 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row25_col5" class="data row25 col5" >0.00</td>
      <td id="T_a5ea1_row25_col6" class="data row25 col6" >86,231.99</td>
      <td id="T_a5ea1_row25_col7" class="data row25 col7" >True</td>
      <td id="T_a5ea1_row25_col8" class="data row25 col8" >86,231.99</td>
      <td id="T_a5ea1_row25_col9" class="data row25 col9" >USD</td>
      <td id="T_a5ea1_row25_col10" class="data row25 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row25_col11" class="data row25 col11" >1.7440%</td>
      <td id="T_a5ea1_row25_col12" class="data row25 col12" >0.0000%</td>
      <td id="T_a5ea1_row25_col13" class="data row25 col13" >1.00</td>
      <td id="T_a5ea1_row25_col14" class="data row25 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row26" class="row_heading level0 row26" >26</th>
      <td id="T_a5ea1_row26_col0" class="data row26 col0" >2026-05-12</td>
      <td id="T_a5ea1_row26_col1" class="data row26 col1" >2026-08-12</td>
      <td id="T_a5ea1_row26_col2" class="data row26 col2" >2026-05-08</td>
      <td id="T_a5ea1_row26_col3" class="data row26 col3" >2026-08-12</td>
      <td id="T_a5ea1_row26_col4" class="data row26 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row26_col5" class="data row26 col5" >0.00</td>
      <td id="T_a5ea1_row26_col6" class="data row26 col6" >89,714.97</td>
      <td id="T_a5ea1_row26_col7" class="data row26 col7" >True</td>
      <td id="T_a5ea1_row26_col8" class="data row26 col8" >89,714.97</td>
      <td id="T_a5ea1_row26_col9" class="data row26 col9" >USD</td>
      <td id="T_a5ea1_row26_col10" class="data row26 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row26_col11" class="data row26 col11" >1.7553%</td>
      <td id="T_a5ea1_row26_col12" class="data row26 col12" >0.0000%</td>
      <td id="T_a5ea1_row26_col13" class="data row26 col13" >1.00</td>
      <td id="T_a5ea1_row26_col14" class="data row26 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row27" class="row_heading level0 row27" >27</th>
      <td id="T_a5ea1_row27_col0" class="data row27 col0" >2026-08-12</td>
      <td id="T_a5ea1_row27_col1" class="data row27 col1" >2026-11-12</td>
      <td id="T_a5ea1_row27_col2" class="data row27 col2" >2026-08-10</td>
      <td id="T_a5ea1_row27_col3" class="data row27 col3" >2026-11-12</td>
      <td id="T_a5ea1_row27_col4" class="data row27 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row27_col5" class="data row27 col5" >0.00</td>
      <td id="T_a5ea1_row27_col6" class="data row27 col6" >90,284.84</td>
      <td id="T_a5ea1_row27_col7" class="data row27 col7" >True</td>
      <td id="T_a5ea1_row27_col8" class="data row27 col8" >90,284.84</td>
      <td id="T_a5ea1_row27_col9" class="data row27 col9" >USD</td>
      <td id="T_a5ea1_row27_col10" class="data row27 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row27_col11" class="data row27 col11" >1.7664%</td>
      <td id="T_a5ea1_row27_col12" class="data row27 col12" >0.0000%</td>
      <td id="T_a5ea1_row27_col13" class="data row27 col13" >1.00</td>
      <td id="T_a5ea1_row27_col14" class="data row27 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row28" class="row_heading level0 row28" >28</th>
      <td id="T_a5ea1_row28_col0" class="data row28 col0" >2026-11-12</td>
      <td id="T_a5ea1_row28_col1" class="data row28 col1" >2027-02-12</td>
      <td id="T_a5ea1_row28_col2" class="data row28 col2" >2026-11-10</td>
      <td id="T_a5ea1_row28_col3" class="data row28 col3" >2027-02-12</td>
      <td id="T_a5ea1_row28_col4" class="data row28 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row28_col5" class="data row28 col5" >0.00</td>
      <td id="T_a5ea1_row28_col6" class="data row28 col6" >90,845.26</td>
      <td id="T_a5ea1_row28_col7" class="data row28 col7" >True</td>
      <td id="T_a5ea1_row28_col8" class="data row28 col8" >90,845.26</td>
      <td id="T_a5ea1_row28_col9" class="data row28 col9" >USD</td>
      <td id="T_a5ea1_row28_col10" class="data row28 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row28_col11" class="data row28 col11" >1.7774%</td>
      <td id="T_a5ea1_row28_col12" class="data row28 col12" >0.0000%</td>
      <td id="T_a5ea1_row28_col13" class="data row28 col13" >1.00</td>
      <td id="T_a5ea1_row28_col14" class="data row28 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row29" class="row_heading level0 row29" >29</th>
      <td id="T_a5ea1_row29_col0" class="data row29 col0" >2027-02-12</td>
      <td id="T_a5ea1_row29_col1" class="data row29 col1" >2027-05-12</td>
      <td id="T_a5ea1_row29_col2" class="data row29 col2" >2027-02-10</td>
      <td id="T_a5ea1_row29_col3" class="data row29 col3" >2027-05-12</td>
      <td id="T_a5ea1_row29_col4" class="data row29 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row29_col5" class="data row29 col5" >0.00</td>
      <td id="T_a5ea1_row29_col6" class="data row29 col6" >90,645.79</td>
      <td id="T_a5ea1_row29_col7" class="data row29 col7" >True</td>
      <td id="T_a5ea1_row29_col8" class="data row29 col8" >90,645.79</td>
      <td id="T_a5ea1_row29_col9" class="data row29 col9" >USD</td>
      <td id="T_a5ea1_row29_col10" class="data row29 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row29_col11" class="data row29 col11" >1.8333%</td>
      <td id="T_a5ea1_row29_col12" class="data row29 col12" >0.0000%</td>
      <td id="T_a5ea1_row29_col13" class="data row29 col13" >1.00</td>
      <td id="T_a5ea1_row29_col14" class="data row29 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row30" class="row_heading level0 row30" >30</th>
      <td id="T_a5ea1_row30_col0" class="data row30 col0" >2027-05-12</td>
      <td id="T_a5ea1_row30_col1" class="data row30 col1" >2027-08-12</td>
      <td id="T_a5ea1_row30_col2" class="data row30 col2" >2027-05-10</td>
      <td id="T_a5ea1_row30_col3" class="data row30 col3" >2027-08-12</td>
      <td id="T_a5ea1_row30_col4" class="data row30 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row30_col5" class="data row30 col5" >0.00</td>
      <td id="T_a5ea1_row30_col6" class="data row30 col6" >94,825.45</td>
      <td id="T_a5ea1_row30_col7" class="data row30 col7" >True</td>
      <td id="T_a5ea1_row30_col8" class="data row30 col8" >94,825.45</td>
      <td id="T_a5ea1_row30_col9" class="data row30 col9" >USD</td>
      <td id="T_a5ea1_row30_col10" class="data row30 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row30_col11" class="data row30 col11" >1.8553%</td>
      <td id="T_a5ea1_row30_col12" class="data row30 col12" >0.0000%</td>
      <td id="T_a5ea1_row30_col13" class="data row30 col13" >1.00</td>
      <td id="T_a5ea1_row30_col14" class="data row30 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row31" class="row_heading level0 row31" >31</th>
      <td id="T_a5ea1_row31_col0" class="data row31 col0" >2027-08-12</td>
      <td id="T_a5ea1_row31_col1" class="data row31 col1" >2027-11-12</td>
      <td id="T_a5ea1_row31_col2" class="data row31 col2" >2027-08-10</td>
      <td id="T_a5ea1_row31_col3" class="data row31 col3" >2027-11-12</td>
      <td id="T_a5ea1_row31_col4" class="data row31 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row31_col5" class="data row31 col5" >0.00</td>
      <td id="T_a5ea1_row31_col6" class="data row31 col6" >95,521.58</td>
      <td id="T_a5ea1_row31_col7" class="data row31 col7" >True</td>
      <td id="T_a5ea1_row31_col8" class="data row31 col8" >95,521.58</td>
      <td id="T_a5ea1_row31_col9" class="data row31 col9" >USD</td>
      <td id="T_a5ea1_row31_col10" class="data row31 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row31_col11" class="data row31 col11" >1.8689%</td>
      <td id="T_a5ea1_row31_col12" class="data row31 col12" >0.0000%</td>
      <td id="T_a5ea1_row31_col13" class="data row31 col13" >1.00</td>
      <td id="T_a5ea1_row31_col14" class="data row31 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row32" class="row_heading level0 row32" >32</th>
      <td id="T_a5ea1_row32_col0" class="data row32 col0" >2027-11-12</td>
      <td id="T_a5ea1_row32_col1" class="data row32 col1" >2028-02-14</td>
      <td id="T_a5ea1_row32_col2" class="data row32 col2" >2027-11-10</td>
      <td id="T_a5ea1_row32_col3" class="data row32 col3" >2028-02-14</td>
      <td id="T_a5ea1_row32_col4" class="data row32 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row32_col5" class="data row32 col5" >0.00</td>
      <td id="T_a5ea1_row32_col6" class="data row32 col6" >98,309.76</td>
      <td id="T_a5ea1_row32_col7" class="data row32 col7" >True</td>
      <td id="T_a5ea1_row32_col8" class="data row32 col8" >98,309.76</td>
      <td id="T_a5ea1_row32_col9" class="data row32 col9" >USD</td>
      <td id="T_a5ea1_row32_col10" class="data row32 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row32_col11" class="data row32 col11" >1.8825%</td>
      <td id="T_a5ea1_row32_col12" class="data row32 col12" >0.0000%</td>
      <td id="T_a5ea1_row32_col13" class="data row32 col13" >1.00</td>
      <td id="T_a5ea1_row32_col14" class="data row32 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row33" class="row_heading level0 row33" >33</th>
      <td id="T_a5ea1_row33_col0" class="data row33 col0" >2028-02-14</td>
      <td id="T_a5ea1_row33_col1" class="data row33 col1" >2028-05-12</td>
      <td id="T_a5ea1_row33_col2" class="data row33 col2" >2028-02-10</td>
      <td id="T_a5ea1_row33_col3" class="data row33 col3" >2028-05-12</td>
      <td id="T_a5ea1_row33_col4" class="data row33 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row33_col5" class="data row33 col5" >0.00</td>
      <td id="T_a5ea1_row33_col6" class="data row33 col6" >92,673.72</td>
      <td id="T_a5ea1_row33_col7" class="data row33 col7" >True</td>
      <td id="T_a5ea1_row33_col8" class="data row33 col8" >92,673.72</td>
      <td id="T_a5ea1_row33_col9" class="data row33 col9" >USD</td>
      <td id="T_a5ea1_row33_col10" class="data row33 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row33_col11" class="data row33 col11" >1.8956%</td>
      <td id="T_a5ea1_row33_col12" class="data row33 col12" >0.0000%</td>
      <td id="T_a5ea1_row33_col13" class="data row33 col13" >1.00</td>
      <td id="T_a5ea1_row33_col14" class="data row33 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row34" class="row_heading level0 row34" >34</th>
      <td id="T_a5ea1_row34_col0" class="data row34 col0" >2028-05-12</td>
      <td id="T_a5ea1_row34_col1" class="data row34 col1" >2028-08-14</td>
      <td id="T_a5ea1_row34_col2" class="data row34 col2" >2028-05-10</td>
      <td id="T_a5ea1_row34_col3" class="data row34 col3" >2028-08-14</td>
      <td id="T_a5ea1_row34_col4" class="data row34 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row34_col5" class="data row34 col5" >0.00</td>
      <td id="T_a5ea1_row34_col6" class="data row34 col6" >99,656.47</td>
      <td id="T_a5ea1_row34_col7" class="data row34 col7" >True</td>
      <td id="T_a5ea1_row34_col8" class="data row34 col8" >99,656.47</td>
      <td id="T_a5ea1_row34_col9" class="data row34 col9" >USD</td>
      <td id="T_a5ea1_row34_col10" class="data row34 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row34_col11" class="data row34 col11" >1.9083%</td>
      <td id="T_a5ea1_row34_col12" class="data row34 col12" >0.0000%</td>
      <td id="T_a5ea1_row34_col13" class="data row34 col13" >1.00</td>
      <td id="T_a5ea1_row34_col14" class="data row34 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row35" class="row_heading level0 row35" >35</th>
      <td id="T_a5ea1_row35_col0" class="data row35 col0" >2028-08-14</td>
      <td id="T_a5ea1_row35_col1" class="data row35 col1" >2028-11-13</td>
      <td id="T_a5ea1_row35_col2" class="data row35 col2" >2028-08-10</td>
      <td id="T_a5ea1_row35_col3" class="data row35 col3" >2028-11-13</td>
      <td id="T_a5ea1_row35_col4" class="data row35 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row35_col5" class="data row35 col5" >0.00</td>
      <td id="T_a5ea1_row35_col6" class="data row35 col6" >97,119.25</td>
      <td id="T_a5ea1_row35_col7" class="data row35 col7" >True</td>
      <td id="T_a5ea1_row35_col8" class="data row35 col8" >97,119.25</td>
      <td id="T_a5ea1_row35_col9" class="data row35 col9" >USD</td>
      <td id="T_a5ea1_row35_col10" class="data row35 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row35_col11" class="data row35 col11" >1.9210%</td>
      <td id="T_a5ea1_row35_col12" class="data row35 col12" >0.0000%</td>
      <td id="T_a5ea1_row35_col13" class="data row35 col13" >1.00</td>
      <td id="T_a5ea1_row35_col14" class="data row35 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row36" class="row_heading level0 row36" >36</th>
      <td id="T_a5ea1_row36_col0" class="data row36 col0" >2028-11-13</td>
      <td id="T_a5ea1_row36_col1" class="data row36 col1" >2029-02-12</td>
      <td id="T_a5ea1_row36_col2" class="data row36 col2" >2028-11-09</td>
      <td id="T_a5ea1_row36_col3" class="data row36 col3" >2029-02-12</td>
      <td id="T_a5ea1_row36_col4" class="data row36 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row36_col5" class="data row36 col5" >0.00</td>
      <td id="T_a5ea1_row36_col6" class="data row36 col6" >97,742.18</td>
      <td id="T_a5ea1_row36_col7" class="data row36 col7" >True</td>
      <td id="T_a5ea1_row36_col8" class="data row36 col8" >97,742.18</td>
      <td id="T_a5ea1_row36_col9" class="data row36 col9" >USD</td>
      <td id="T_a5ea1_row36_col10" class="data row36 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row36_col11" class="data row36 col11" >1.9334%</td>
      <td id="T_a5ea1_row36_col12" class="data row36 col12" >0.0000%</td>
      <td id="T_a5ea1_row36_col13" class="data row36 col13" >1.00</td>
      <td id="T_a5ea1_row36_col14" class="data row36 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row37" class="row_heading level0 row37" >37</th>
      <td id="T_a5ea1_row37_col0" class="data row37 col0" >2029-02-12</td>
      <td id="T_a5ea1_row37_col1" class="data row37 col1" >2029-05-14</td>
      <td id="T_a5ea1_row37_col2" class="data row37 col2" >2029-02-08</td>
      <td id="T_a5ea1_row37_col3" class="data row37 col3" >2029-05-14</td>
      <td id="T_a5ea1_row37_col4" class="data row37 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row37_col5" class="data row37 col5" >0.00</td>
      <td id="T_a5ea1_row37_col6" class="data row37 col6" >98,347.80</td>
      <td id="T_a5ea1_row37_col7" class="data row37 col7" >True</td>
      <td id="T_a5ea1_row37_col8" class="data row37 col8" >98,347.80</td>
      <td id="T_a5ea1_row37_col9" class="data row37 col9" >USD</td>
      <td id="T_a5ea1_row37_col10" class="data row37 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row37_col11" class="data row37 col11" >1.9453%</td>
      <td id="T_a5ea1_row37_col12" class="data row37 col12" >0.0000%</td>
      <td id="T_a5ea1_row37_col13" class="data row37 col13" >1.00</td>
      <td id="T_a5ea1_row37_col14" class="data row37 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row38" class="row_heading level0 row38" >38</th>
      <td id="T_a5ea1_row38_col0" class="data row38 col0" >2029-05-14</td>
      <td id="T_a5ea1_row38_col1" class="data row38 col1" >2029-08-13</td>
      <td id="T_a5ea1_row38_col2" class="data row38 col2" >2029-05-10</td>
      <td id="T_a5ea1_row38_col3" class="data row38 col3" >2029-08-13</td>
      <td id="T_a5ea1_row38_col4" class="data row38 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row38_col5" class="data row38 col5" >0.00</td>
      <td id="T_a5ea1_row38_col6" class="data row38 col6" >98,954.09</td>
      <td id="T_a5ea1_row38_col7" class="data row38 col7" >True</td>
      <td id="T_a5ea1_row38_col8" class="data row38 col8" >98,954.09</td>
      <td id="T_a5ea1_row38_col9" class="data row38 col9" >USD</td>
      <td id="T_a5ea1_row38_col10" class="data row38 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row38_col11" class="data row38 col11" >1.9573%</td>
      <td id="T_a5ea1_row38_col12" class="data row38 col12" >0.0000%</td>
      <td id="T_a5ea1_row38_col13" class="data row38 col13" >1.00</td>
      <td id="T_a5ea1_row38_col14" class="data row38 col14" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_a5ea1_level0_row39" class="row_heading level0 row39" >39</th>
      <td id="T_a5ea1_row39_col0" class="data row39 col0" >2029-08-13</td>
      <td id="T_a5ea1_row39_col1" class="data row39 col1" >2029-11-12</td>
      <td id="T_a5ea1_row39_col2" class="data row39 col2" >2029-08-09</td>
      <td id="T_a5ea1_row39_col3" class="data row39 col3" >2029-11-12</td>
      <td id="T_a5ea1_row39_col4" class="data row39 col4" >20,000,000.00</td>
      <td id="T_a5ea1_row39_col5" class="data row39 col5" >20,000,000.00</td>
      <td id="T_a5ea1_row39_col6" class="data row39 col6" >99,543.20</td>
      <td id="T_a5ea1_row39_col7" class="data row39 col7" >True</td>
      <td id="T_a5ea1_row39_col8" class="data row39 col8" >20,099,543.20</td>
      <td id="T_a5ea1_row39_col9" class="data row39 col9" >USD</td>
      <td id="T_a5ea1_row39_col10" class="data row39 col10" >LIBORUSD3M</td>
      <td id="T_a5ea1_row39_col11" class="data row39 col11" >1.9690%</td>
      <td id="T_a5ea1_row39_col12" class="data row39 col12" >0.0000%</td>
      <td id="T_a5ea1_row39_col13" class="data row39 col13" >1.00</td>
      <td id="T_a5ea1_row39_col14" class="data row39 col14" >LinAct360</td>
    </tr>
  </tbody>
</table>





```python
which_cashflow = 1
d1 = fecha_hoy.day_diff(ibor_leg.get_cashflow_at(which_cashflow).get_start_date())
d2 = fecha_hoy.day_diff(ibor_leg.get_cashflow_at(which_cashflow).get_end_date())
print("d1: {0:,.0f}".format(d1))
print("d2: {0:,.0f}".format(d2))
crv = zz2
w1 = 1 / crv.get_discount_factor_at(d1)
w2 = 1 / crv.get_discount_factor_at(d2)
print("Factor forward: {0:.4%}".format(w2 / w1))
print("Tasa forward: {0:.4%}".format((w2 / w1 - 1) * 360 / (d2 - d1)))
print("Curve method {0:.4%}".format(crv.get_forward_rate_with_rate(libor_usd_3m.get_rate(), d1, d2)))
```

    d1: -13
    d2: 77
    Factor forward: 100.4379%
    Tasa forward: 1.7517%
    Curve method 1.5288%



```python
vp_ibor = pv.pv(fecha_hoy, ibor_leg, zz2)
print("Valor presente pata IBOR: {0:,.0f}".format(vp_ibor))
```

    Valor presente pata IBOR: 19,923,921



```python
der = pv.get_derivatives()
i = 0
bp = .0001
for d in der:
    print("Sensibilidad en {0:}: {1:0,.0f}".format(i, d * bp))
    i += 1
print("Sensibilidad de descuento: {0:,.0f} USD".format(sum(der) * bp))
```

    Sensibilidad en 0: 0
    Sensibilidad en 1: 0
    Sensibilidad en 2: 0
    Sensibilidad en 3: 0
    Sensibilidad en 4: 0
    Sensibilidad en 5: 0
    Sensibilidad en 6: 0
    Sensibilidad en 7: 0
    Sensibilidad en 8: -2
    Sensibilidad en 9: -2
    Sensibilidad en 10: 0
    Sensibilidad en 11: -3
    Sensibilidad en 12: -3
    Sensibilidad en 13: 0
    Sensibilidad en 14: -3
    Sensibilidad en 15: -10
    Sensibilidad en 16: -21
    Sensibilidad en 17: -47
    Sensibilidad en 18: -85
    Sensibilidad en 19: -114
    Sensibilidad en 20: -234
    Sensibilidad en 21: -1,895
    Sensibilidad en 22: -13,122
    Sensibilidad en 23: 0
    Sensibilidad en 24: 0
    Sensibilidad en 25: 0
    Sensibilidad en 26: 0
    Sensibilidad en 27: 0
    Sensibilidad de descuento: -15,541 USD


#### Se verifica la sensibilidad de descuento por diferencias finitas.


```python
vp_ibor_up = pv.pv(fecha_hoy, ibor_leg, zz2_sens_up)
print("Valor presente up pata IBOR: {0:,.0f}".format(vp_ibor_up))

vp_ibor_down = pv.pv(fecha_hoy, ibor_leg, zz2_sens_down)
print("Valor presente down pata IBOR: {0:,.0f}".format(vp_ibor_down))

print("Sensibilidad de descuento en el vértice {0:}: {1:,.0f}".format(vertice, (vp_ibor_up - vp_ibor_down) / 2))
```

    Valor presente up pata IBOR: 19,923,921
    Valor presente down pata IBOR: 19,923,921
    Sensibilidad de descuento en el vértice 13: 0


Se calcula también la sensibilidad a la curva de proyección.


```python
import numpy as np
bp = .0001
result = []

for i in range(ibor_leg.size()):
    cshflw = ibor_leg.get_cashflow_at(i)
    df = zz2.get_discount_factor_at(fecha_hoy.day_diff(cshflw.get_settlement_date()))
    amt_der = cshflw.get_amount_derivatives()
    if len(amt_der) > 0:
        amt_der = [a * bp * df for a in amt_der]
        result.append(np.array(amt_der))

total = result[0] * 0
for r in result:
    total += r

for i in range(len(total)):
    print("Sensibilidad en {0:}: {1:0,.0f}".format(i, total[i]))

print("Sensibilidad de proyección: {0:,.0f} USD".format(sum(total)))
```

    Sensibilidad en 0: 0
    Sensibilidad en 1: 0
    Sensibilidad en 2: 0
    Sensibilidad en 3: 0
    Sensibilidad en 4: 0
    Sensibilidad en 5: -192
    Sensibilidad en 6: -233
    Sensibilidad en 7: 0
    Sensibilidad en 8: 2
    Sensibilidad en 9: 2
    Sensibilidad en 10: 0
    Sensibilidad en 11: 3
    Sensibilidad en 12: 3
    Sensibilidad en 13: 0
    Sensibilidad en 14: 3
    Sensibilidad en 15: 10
    Sensibilidad en 16: 21
    Sensibilidad en 17: 1
    Sensibilidad en 18: 81
    Sensibilidad en 19: 193
    Sensibilidad en 20: 258
    Sensibilidad en 21: 1,820
    Sensibilidad en 22: 13,222
    Sensibilidad en 23: 0
    Sensibilidad en 24: 0
    Sensibilidad en 25: 0
    Sensibilidad en 26: 0
    Sensibilidad en 27: 0
    Sensibilidad de proyección: 15,194 USD


#### Se verifica la sensibilidad de proyección por diferencias finitas.


```python
fwd_rates.set_rates_ibor_leg(fecha_hoy, ibor_leg, zz2_sens_up)
vp_ibor_up = pv.pv(fecha_hoy, ibor_leg, zz2)
print("Valor presente up pata IBOR: {0:,.0f}".format(vp_ibor_up))

fwd_rates.set_rates_ibor_leg(fecha_hoy, ibor_leg, zz2_sens_down)
vp_ibor_down = pv.pv(fecha_hoy, ibor_leg, zz2)
print("Valor presente down pata IBOR: {0:,.0f}".format(vp_ibor_down))

print("Sensibilidad de proyección en el vértice {0:}: {1:,.0f}".format(vertice, (vp_ibor_up - vp_ibor_down) / 2))
```

    Valor presente up pata IBOR: 19,923,921
    Valor presente down pata IBOR: 19,923,921
    Sensibilidad de proyección en el vértice 13: 0


### IcpClfCashflow Leg


```python
# Se da de alta los parámetros requeridos
rp = qcf.RecPay.RECEIVE
fecha_inicio = qcf.QCDate(31, 5, 2018)
fecha_final = qcf.QCDate(9, 5, 2026) 
bus_adj_rule = qcf.BusyAdjRules.FOLLOW
periodicidad_pago = qcf.Tenor('6M')
periodo_irregular_pago = qcf.StubPeriod.SHORTFRONT
calendario = qcf.BusinessCalendar(fecha_inicio, 20)
lag_pago = 0
nominal = 6000_00.0
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
<table id="T_65f3d">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_65f3d_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_65f3d_level0_col1" class="col_heading level0 col1" >fecha__final</th>
      <th id="T_65f3d_level0_col2" class="col_heading level0 col2" >fecha__pago</th>
      <th id="T_65f3d_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_65f3d_level0_col4" class="col_heading level0 col4" >amort</th>
      <th id="T_65f3d_level0_col5" class="col_heading level0 col5" >amort_es_flujo</th>
      <th id="T_65f3d_level0_col6" class="col_heading level0 col6" >flujo</th>
      <th id="T_65f3d_level0_col7" class="col_heading level0 col7" >moneda</th>
      <th id="T_65f3d_level0_col8" class="col_heading level0 col8" >icp_inicial</th>
      <th id="T_65f3d_level0_col9" class="col_heading level0 col9" >icp_final</th>
      <th id="T_65f3d_level0_col10" class="col_heading level0 col10" >uf_inicial</th>
      <th id="T_65f3d_level0_col11" class="col_heading level0 col11" >uf_final</th>
      <th id="T_65f3d_level0_col12" class="col_heading level0 col12" >valor_tasa</th>
      <th id="T_65f3d_level0_col13" class="col_heading level0 col13" >interes</th>
      <th id="T_65f3d_level0_col14" class="col_heading level0 col14" >spread</th>
      <th id="T_65f3d_level0_col15" class="col_heading level0 col15" >gearing</th>
      <th id="T_65f3d_level0_col16" class="col_heading level0 col16" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_65f3d_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_65f3d_row0_col0" class="data row0 col0" >2018-05-31</td>
      <td id="T_65f3d_row0_col1" class="data row0 col1" >2018-11-09</td>
      <td id="T_65f3d_row0_col2" class="data row0 col2" >2018-11-09</td>
      <td id="T_65f3d_row0_col3" class="data row0 col3" >600,000.00</td>
      <td id="T_65f3d_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_65f3d_row0_col5" class="data row0 col5" >True</td>
      <td id="T_65f3d_row0_col6" class="data row0 col6" >0.00</td>
      <td id="T_65f3d_row0_col7" class="data row0 col7" >CLF</td>
      <td id="T_65f3d_row0_col8" class="data row0 col8" >10,000.00</td>
      <td id="T_65f3d_row0_col9" class="data row0 col9" >10,000.00</td>
      <td id="T_65f3d_row0_col10" class="data row0 col10" >35,000.00</td>
      <td id="T_65f3d_row0_col11" class="data row0 col11" >35,000.00</td>
      <td id="T_65f3d_row0_col12" class="data row0 col12" >0.0000%</td>
      <td id="T_65f3d_row0_col13" class="data row0 col13" >0.00</td>
      <td id="T_65f3d_row0_col14" class="data row0 col14" >0.0000%</td>
      <td id="T_65f3d_row0_col15" class="data row0 col15" >1.00</td>
      <td id="T_65f3d_row0_col16" class="data row0 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_65f3d_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_65f3d_row1_col0" class="data row1 col0" >2018-11-09</td>
      <td id="T_65f3d_row1_col1" class="data row1 col1" >2019-05-09</td>
      <td id="T_65f3d_row1_col2" class="data row1 col2" >2019-05-09</td>
      <td id="T_65f3d_row1_col3" class="data row1 col3" >600,000.00</td>
      <td id="T_65f3d_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_65f3d_row1_col5" class="data row1 col5" >True</td>
      <td id="T_65f3d_row1_col6" class="data row1 col6" >0.00</td>
      <td id="T_65f3d_row1_col7" class="data row1 col7" >CLF</td>
      <td id="T_65f3d_row1_col8" class="data row1 col8" >10,000.00</td>
      <td id="T_65f3d_row1_col9" class="data row1 col9" >10,000.00</td>
      <td id="T_65f3d_row1_col10" class="data row1 col10" >35,000.00</td>
      <td id="T_65f3d_row1_col11" class="data row1 col11" >35,000.00</td>
      <td id="T_65f3d_row1_col12" class="data row1 col12" >0.0000%</td>
      <td id="T_65f3d_row1_col13" class="data row1 col13" >0.00</td>
      <td id="T_65f3d_row1_col14" class="data row1 col14" >0.0000%</td>
      <td id="T_65f3d_row1_col15" class="data row1 col15" >1.00</td>
      <td id="T_65f3d_row1_col16" class="data row1 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_65f3d_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_65f3d_row2_col0" class="data row2 col0" >2019-05-09</td>
      <td id="T_65f3d_row2_col1" class="data row2 col1" >2019-11-11</td>
      <td id="T_65f3d_row2_col2" class="data row2 col2" >2019-11-11</td>
      <td id="T_65f3d_row2_col3" class="data row2 col3" >600,000.00</td>
      <td id="T_65f3d_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_65f3d_row2_col5" class="data row2 col5" >True</td>
      <td id="T_65f3d_row2_col6" class="data row2 col6" >0.00</td>
      <td id="T_65f3d_row2_col7" class="data row2 col7" >CLF</td>
      <td id="T_65f3d_row2_col8" class="data row2 col8" >10,000.00</td>
      <td id="T_65f3d_row2_col9" class="data row2 col9" >10,000.00</td>
      <td id="T_65f3d_row2_col10" class="data row2 col10" >35,000.00</td>
      <td id="T_65f3d_row2_col11" class="data row2 col11" >35,000.00</td>
      <td id="T_65f3d_row2_col12" class="data row2 col12" >0.0000%</td>
      <td id="T_65f3d_row2_col13" class="data row2 col13" >0.00</td>
      <td id="T_65f3d_row2_col14" class="data row2 col14" >0.0000%</td>
      <td id="T_65f3d_row2_col15" class="data row2 col15" >1.00</td>
      <td id="T_65f3d_row2_col16" class="data row2 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_65f3d_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_65f3d_row3_col0" class="data row3 col0" >2019-11-11</td>
      <td id="T_65f3d_row3_col1" class="data row3 col1" >2020-05-11</td>
      <td id="T_65f3d_row3_col2" class="data row3 col2" >2020-05-11</td>
      <td id="T_65f3d_row3_col3" class="data row3 col3" >600,000.00</td>
      <td id="T_65f3d_row3_col4" class="data row3 col4" >0.00</td>
      <td id="T_65f3d_row3_col5" class="data row3 col5" >True</td>
      <td id="T_65f3d_row3_col6" class="data row3 col6" >0.00</td>
      <td id="T_65f3d_row3_col7" class="data row3 col7" >CLF</td>
      <td id="T_65f3d_row3_col8" class="data row3 col8" >10,000.00</td>
      <td id="T_65f3d_row3_col9" class="data row3 col9" >10,000.00</td>
      <td id="T_65f3d_row3_col10" class="data row3 col10" >35,000.00</td>
      <td id="T_65f3d_row3_col11" class="data row3 col11" >35,000.00</td>
      <td id="T_65f3d_row3_col12" class="data row3 col12" >0.0000%</td>
      <td id="T_65f3d_row3_col13" class="data row3 col13" >0.00</td>
      <td id="T_65f3d_row3_col14" class="data row3 col14" >0.0000%</td>
      <td id="T_65f3d_row3_col15" class="data row3 col15" >1.00</td>
      <td id="T_65f3d_row3_col16" class="data row3 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_65f3d_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_65f3d_row4_col0" class="data row4 col0" >2020-05-11</td>
      <td id="T_65f3d_row4_col1" class="data row4 col1" >2020-11-09</td>
      <td id="T_65f3d_row4_col2" class="data row4 col2" >2020-11-09</td>
      <td id="T_65f3d_row4_col3" class="data row4 col3" >600,000.00</td>
      <td id="T_65f3d_row4_col4" class="data row4 col4" >0.00</td>
      <td id="T_65f3d_row4_col5" class="data row4 col5" >True</td>
      <td id="T_65f3d_row4_col6" class="data row4 col6" >0.00</td>
      <td id="T_65f3d_row4_col7" class="data row4 col7" >CLF</td>
      <td id="T_65f3d_row4_col8" class="data row4 col8" >10,000.00</td>
      <td id="T_65f3d_row4_col9" class="data row4 col9" >10,000.00</td>
      <td id="T_65f3d_row4_col10" class="data row4 col10" >35,000.00</td>
      <td id="T_65f3d_row4_col11" class="data row4 col11" >35,000.00</td>
      <td id="T_65f3d_row4_col12" class="data row4 col12" >0.0000%</td>
      <td id="T_65f3d_row4_col13" class="data row4 col13" >0.00</td>
      <td id="T_65f3d_row4_col14" class="data row4 col14" >0.0000%</td>
      <td id="T_65f3d_row4_col15" class="data row4 col15" >1.00</td>
      <td id="T_65f3d_row4_col16" class="data row4 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_65f3d_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_65f3d_row5_col0" class="data row5 col0" >2020-11-09</td>
      <td id="T_65f3d_row5_col1" class="data row5 col1" >2021-05-10</td>
      <td id="T_65f3d_row5_col2" class="data row5 col2" >2021-05-10</td>
      <td id="T_65f3d_row5_col3" class="data row5 col3" >600,000.00</td>
      <td id="T_65f3d_row5_col4" class="data row5 col4" >0.00</td>
      <td id="T_65f3d_row5_col5" class="data row5 col5" >True</td>
      <td id="T_65f3d_row5_col6" class="data row5 col6" >0.00</td>
      <td id="T_65f3d_row5_col7" class="data row5 col7" >CLF</td>
      <td id="T_65f3d_row5_col8" class="data row5 col8" >10,000.00</td>
      <td id="T_65f3d_row5_col9" class="data row5 col9" >10,000.00</td>
      <td id="T_65f3d_row5_col10" class="data row5 col10" >35,000.00</td>
      <td id="T_65f3d_row5_col11" class="data row5 col11" >35,000.00</td>
      <td id="T_65f3d_row5_col12" class="data row5 col12" >0.0000%</td>
      <td id="T_65f3d_row5_col13" class="data row5 col13" >0.00</td>
      <td id="T_65f3d_row5_col14" class="data row5 col14" >0.0000%</td>
      <td id="T_65f3d_row5_col15" class="data row5 col15" >1.00</td>
      <td id="T_65f3d_row5_col16" class="data row5 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_65f3d_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_65f3d_row6_col0" class="data row6 col0" >2021-05-10</td>
      <td id="T_65f3d_row6_col1" class="data row6 col1" >2021-11-09</td>
      <td id="T_65f3d_row6_col2" class="data row6 col2" >2021-11-09</td>
      <td id="T_65f3d_row6_col3" class="data row6 col3" >600,000.00</td>
      <td id="T_65f3d_row6_col4" class="data row6 col4" >0.00</td>
      <td id="T_65f3d_row6_col5" class="data row6 col5" >True</td>
      <td id="T_65f3d_row6_col6" class="data row6 col6" >0.00</td>
      <td id="T_65f3d_row6_col7" class="data row6 col7" >CLF</td>
      <td id="T_65f3d_row6_col8" class="data row6 col8" >10,000.00</td>
      <td id="T_65f3d_row6_col9" class="data row6 col9" >10,000.00</td>
      <td id="T_65f3d_row6_col10" class="data row6 col10" >35,000.00</td>
      <td id="T_65f3d_row6_col11" class="data row6 col11" >35,000.00</td>
      <td id="T_65f3d_row6_col12" class="data row6 col12" >0.0000%</td>
      <td id="T_65f3d_row6_col13" class="data row6 col13" >0.00</td>
      <td id="T_65f3d_row6_col14" class="data row6 col14" >0.0000%</td>
      <td id="T_65f3d_row6_col15" class="data row6 col15" >1.00</td>
      <td id="T_65f3d_row6_col16" class="data row6 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_65f3d_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_65f3d_row7_col0" class="data row7 col0" >2021-11-09</td>
      <td id="T_65f3d_row7_col1" class="data row7 col1" >2022-05-09</td>
      <td id="T_65f3d_row7_col2" class="data row7 col2" >2022-05-09</td>
      <td id="T_65f3d_row7_col3" class="data row7 col3" >600,000.00</td>
      <td id="T_65f3d_row7_col4" class="data row7 col4" >0.00</td>
      <td id="T_65f3d_row7_col5" class="data row7 col5" >True</td>
      <td id="T_65f3d_row7_col6" class="data row7 col6" >0.00</td>
      <td id="T_65f3d_row7_col7" class="data row7 col7" >CLF</td>
      <td id="T_65f3d_row7_col8" class="data row7 col8" >10,000.00</td>
      <td id="T_65f3d_row7_col9" class="data row7 col9" >10,000.00</td>
      <td id="T_65f3d_row7_col10" class="data row7 col10" >35,000.00</td>
      <td id="T_65f3d_row7_col11" class="data row7 col11" >35,000.00</td>
      <td id="T_65f3d_row7_col12" class="data row7 col12" >0.0000%</td>
      <td id="T_65f3d_row7_col13" class="data row7 col13" >0.00</td>
      <td id="T_65f3d_row7_col14" class="data row7 col14" >0.0000%</td>
      <td id="T_65f3d_row7_col15" class="data row7 col15" >1.00</td>
      <td id="T_65f3d_row7_col16" class="data row7 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_65f3d_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_65f3d_row8_col0" class="data row8 col0" >2022-05-09</td>
      <td id="T_65f3d_row8_col1" class="data row8 col1" >2022-11-09</td>
      <td id="T_65f3d_row8_col2" class="data row8 col2" >2022-11-09</td>
      <td id="T_65f3d_row8_col3" class="data row8 col3" >600,000.00</td>
      <td id="T_65f3d_row8_col4" class="data row8 col4" >0.00</td>
      <td id="T_65f3d_row8_col5" class="data row8 col5" >True</td>
      <td id="T_65f3d_row8_col6" class="data row8 col6" >0.00</td>
      <td id="T_65f3d_row8_col7" class="data row8 col7" >CLF</td>
      <td id="T_65f3d_row8_col8" class="data row8 col8" >10,000.00</td>
      <td id="T_65f3d_row8_col9" class="data row8 col9" >10,000.00</td>
      <td id="T_65f3d_row8_col10" class="data row8 col10" >35,000.00</td>
      <td id="T_65f3d_row8_col11" class="data row8 col11" >35,000.00</td>
      <td id="T_65f3d_row8_col12" class="data row8 col12" >0.0000%</td>
      <td id="T_65f3d_row8_col13" class="data row8 col13" >0.00</td>
      <td id="T_65f3d_row8_col14" class="data row8 col14" >0.0000%</td>
      <td id="T_65f3d_row8_col15" class="data row8 col15" >1.00</td>
      <td id="T_65f3d_row8_col16" class="data row8 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_65f3d_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_65f3d_row9_col0" class="data row9 col0" >2022-11-09</td>
      <td id="T_65f3d_row9_col1" class="data row9 col1" >2023-05-09</td>
      <td id="T_65f3d_row9_col2" class="data row9 col2" >2023-05-09</td>
      <td id="T_65f3d_row9_col3" class="data row9 col3" >600,000.00</td>
      <td id="T_65f3d_row9_col4" class="data row9 col4" >0.00</td>
      <td id="T_65f3d_row9_col5" class="data row9 col5" >True</td>
      <td id="T_65f3d_row9_col6" class="data row9 col6" >0.00</td>
      <td id="T_65f3d_row9_col7" class="data row9 col7" >CLF</td>
      <td id="T_65f3d_row9_col8" class="data row9 col8" >10,000.00</td>
      <td id="T_65f3d_row9_col9" class="data row9 col9" >10,000.00</td>
      <td id="T_65f3d_row9_col10" class="data row9 col10" >35,000.00</td>
      <td id="T_65f3d_row9_col11" class="data row9 col11" >35,000.00</td>
      <td id="T_65f3d_row9_col12" class="data row9 col12" >0.0000%</td>
      <td id="T_65f3d_row9_col13" class="data row9 col13" >0.00</td>
      <td id="T_65f3d_row9_col14" class="data row9 col14" >0.0000%</td>
      <td id="T_65f3d_row9_col15" class="data row9 col15" >1.00</td>
      <td id="T_65f3d_row9_col16" class="data row9 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_65f3d_level0_row10" class="row_heading level0 row10" >10</th>
      <td id="T_65f3d_row10_col0" class="data row10 col0" >2023-05-09</td>
      <td id="T_65f3d_row10_col1" class="data row10 col1" >2023-11-09</td>
      <td id="T_65f3d_row10_col2" class="data row10 col2" >2023-11-09</td>
      <td id="T_65f3d_row10_col3" class="data row10 col3" >600,000.00</td>
      <td id="T_65f3d_row10_col4" class="data row10 col4" >0.00</td>
      <td id="T_65f3d_row10_col5" class="data row10 col5" >True</td>
      <td id="T_65f3d_row10_col6" class="data row10 col6" >0.00</td>
      <td id="T_65f3d_row10_col7" class="data row10 col7" >CLF</td>
      <td id="T_65f3d_row10_col8" class="data row10 col8" >10,000.00</td>
      <td id="T_65f3d_row10_col9" class="data row10 col9" >10,000.00</td>
      <td id="T_65f3d_row10_col10" class="data row10 col10" >35,000.00</td>
      <td id="T_65f3d_row10_col11" class="data row10 col11" >35,000.00</td>
      <td id="T_65f3d_row10_col12" class="data row10 col12" >0.0000%</td>
      <td id="T_65f3d_row10_col13" class="data row10 col13" >0.00</td>
      <td id="T_65f3d_row10_col14" class="data row10 col14" >0.0000%</td>
      <td id="T_65f3d_row10_col15" class="data row10 col15" >1.00</td>
      <td id="T_65f3d_row10_col16" class="data row10 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_65f3d_level0_row11" class="row_heading level0 row11" >11</th>
      <td id="T_65f3d_row11_col0" class="data row11 col0" >2023-11-09</td>
      <td id="T_65f3d_row11_col1" class="data row11 col1" >2024-05-09</td>
      <td id="T_65f3d_row11_col2" class="data row11 col2" >2024-05-09</td>
      <td id="T_65f3d_row11_col3" class="data row11 col3" >600,000.00</td>
      <td id="T_65f3d_row11_col4" class="data row11 col4" >0.00</td>
      <td id="T_65f3d_row11_col5" class="data row11 col5" >True</td>
      <td id="T_65f3d_row11_col6" class="data row11 col6" >0.00</td>
      <td id="T_65f3d_row11_col7" class="data row11 col7" >CLF</td>
      <td id="T_65f3d_row11_col8" class="data row11 col8" >10,000.00</td>
      <td id="T_65f3d_row11_col9" class="data row11 col9" >10,000.00</td>
      <td id="T_65f3d_row11_col10" class="data row11 col10" >35,000.00</td>
      <td id="T_65f3d_row11_col11" class="data row11 col11" >35,000.00</td>
      <td id="T_65f3d_row11_col12" class="data row11 col12" >0.0000%</td>
      <td id="T_65f3d_row11_col13" class="data row11 col13" >0.00</td>
      <td id="T_65f3d_row11_col14" class="data row11 col14" >0.0000%</td>
      <td id="T_65f3d_row11_col15" class="data row11 col15" >1.00</td>
      <td id="T_65f3d_row11_col16" class="data row11 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_65f3d_level0_row12" class="row_heading level0 row12" >12</th>
      <td id="T_65f3d_row12_col0" class="data row12 col0" >2024-05-09</td>
      <td id="T_65f3d_row12_col1" class="data row12 col1" >2024-11-11</td>
      <td id="T_65f3d_row12_col2" class="data row12 col2" >2024-11-11</td>
      <td id="T_65f3d_row12_col3" class="data row12 col3" >600,000.00</td>
      <td id="T_65f3d_row12_col4" class="data row12 col4" >0.00</td>
      <td id="T_65f3d_row12_col5" class="data row12 col5" >True</td>
      <td id="T_65f3d_row12_col6" class="data row12 col6" >0.00</td>
      <td id="T_65f3d_row12_col7" class="data row12 col7" >CLF</td>
      <td id="T_65f3d_row12_col8" class="data row12 col8" >10,000.00</td>
      <td id="T_65f3d_row12_col9" class="data row12 col9" >10,000.00</td>
      <td id="T_65f3d_row12_col10" class="data row12 col10" >35,000.00</td>
      <td id="T_65f3d_row12_col11" class="data row12 col11" >35,000.00</td>
      <td id="T_65f3d_row12_col12" class="data row12 col12" >0.0000%</td>
      <td id="T_65f3d_row12_col13" class="data row12 col13" >0.00</td>
      <td id="T_65f3d_row12_col14" class="data row12 col14" >0.0000%</td>
      <td id="T_65f3d_row12_col15" class="data row12 col15" >1.00</td>
      <td id="T_65f3d_row12_col16" class="data row12 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_65f3d_level0_row13" class="row_heading level0 row13" >13</th>
      <td id="T_65f3d_row13_col0" class="data row13 col0" >2024-11-11</td>
      <td id="T_65f3d_row13_col1" class="data row13 col1" >2025-05-09</td>
      <td id="T_65f3d_row13_col2" class="data row13 col2" >2025-05-09</td>
      <td id="T_65f3d_row13_col3" class="data row13 col3" >600,000.00</td>
      <td id="T_65f3d_row13_col4" class="data row13 col4" >0.00</td>
      <td id="T_65f3d_row13_col5" class="data row13 col5" >True</td>
      <td id="T_65f3d_row13_col6" class="data row13 col6" >0.00</td>
      <td id="T_65f3d_row13_col7" class="data row13 col7" >CLF</td>
      <td id="T_65f3d_row13_col8" class="data row13 col8" >10,000.00</td>
      <td id="T_65f3d_row13_col9" class="data row13 col9" >10,000.00</td>
      <td id="T_65f3d_row13_col10" class="data row13 col10" >35,000.00</td>
      <td id="T_65f3d_row13_col11" class="data row13 col11" >35,000.00</td>
      <td id="T_65f3d_row13_col12" class="data row13 col12" >0.0000%</td>
      <td id="T_65f3d_row13_col13" class="data row13 col13" >0.00</td>
      <td id="T_65f3d_row13_col14" class="data row13 col14" >0.0000%</td>
      <td id="T_65f3d_row13_col15" class="data row13 col15" >1.00</td>
      <td id="T_65f3d_row13_col16" class="data row13 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_65f3d_level0_row14" class="row_heading level0 row14" >14</th>
      <td id="T_65f3d_row14_col0" class="data row14 col0" >2025-05-09</td>
      <td id="T_65f3d_row14_col1" class="data row14 col1" >2025-11-10</td>
      <td id="T_65f3d_row14_col2" class="data row14 col2" >2025-11-10</td>
      <td id="T_65f3d_row14_col3" class="data row14 col3" >600,000.00</td>
      <td id="T_65f3d_row14_col4" class="data row14 col4" >0.00</td>
      <td id="T_65f3d_row14_col5" class="data row14 col5" >True</td>
      <td id="T_65f3d_row14_col6" class="data row14 col6" >0.00</td>
      <td id="T_65f3d_row14_col7" class="data row14 col7" >CLF</td>
      <td id="T_65f3d_row14_col8" class="data row14 col8" >10,000.00</td>
      <td id="T_65f3d_row14_col9" class="data row14 col9" >10,000.00</td>
      <td id="T_65f3d_row14_col10" class="data row14 col10" >35,000.00</td>
      <td id="T_65f3d_row14_col11" class="data row14 col11" >35,000.00</td>
      <td id="T_65f3d_row14_col12" class="data row14 col12" >0.0000%</td>
      <td id="T_65f3d_row14_col13" class="data row14 col13" >0.00</td>
      <td id="T_65f3d_row14_col14" class="data row14 col14" >0.0000%</td>
      <td id="T_65f3d_row14_col15" class="data row14 col15" >1.00</td>
      <td id="T_65f3d_row14_col16" class="data row14 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_65f3d_level0_row15" class="row_heading level0 row15" >15</th>
      <td id="T_65f3d_row15_col0" class="data row15 col0" >2025-11-10</td>
      <td id="T_65f3d_row15_col1" class="data row15 col1" >2026-05-11</td>
      <td id="T_65f3d_row15_col2" class="data row15 col2" >2026-05-11</td>
      <td id="T_65f3d_row15_col3" class="data row15 col3" >600,000.00</td>
      <td id="T_65f3d_row15_col4" class="data row15 col4" >600,000.00</td>
      <td id="T_65f3d_row15_col5" class="data row15 col5" >True</td>
      <td id="T_65f3d_row15_col6" class="data row15 col6" >600,000.00</td>
      <td id="T_65f3d_row15_col7" class="data row15 col7" >CLF</td>
      <td id="T_65f3d_row15_col8" class="data row15 col8" >10,000.00</td>
      <td id="T_65f3d_row15_col9" class="data row15 col9" >10,000.00</td>
      <td id="T_65f3d_row15_col10" class="data row15 col10" >35,000.00</td>
      <td id="T_65f3d_row15_col11" class="data row15 col11" >35,000.00</td>
      <td id="T_65f3d_row15_col12" class="data row15 col12" >0.0000%</td>
      <td id="T_65f3d_row15_col13" class="data row15 col13" >0.00</td>
      <td id="T_65f3d_row15_col14" class="data row15 col14" >0.0000%</td>
      <td id="T_65f3d_row15_col15" class="data row15 col15" >1.00</td>
      <td id="T_65f3d_row15_col16" class="data row15 col16" >LinAct360</td>
    </tr>
  </tbody>
</table>





```python
icp_hoy = 18_882.07
uf_hoy = 28440.19
fwd_rates.set_rates_icp_clf_leg(fecha_hoy, icp_hoy, uf_hoy, icp_clf_leg, zz1, zz1, zz3)
cshflw = icp_clf_leg.get_cashflow_at(3)
cshflw.set_start_date_uf(28080.26)
cshflw.set_start_date_icp(18786.13)
```


```python
print(fecha_hoy)
```

    2020-02-25



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
<table id="T_71c95">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_71c95_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_71c95_level0_col1" class="col_heading level0 col1" >fecha__final</th>
      <th id="T_71c95_level0_col2" class="col_heading level0 col2" >fecha__pago</th>
      <th id="T_71c95_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_71c95_level0_col4" class="col_heading level0 col4" >amort</th>
      <th id="T_71c95_level0_col5" class="col_heading level0 col5" >amort_es_flujo</th>
      <th id="T_71c95_level0_col6" class="col_heading level0 col6" >flujo</th>
      <th id="T_71c95_level0_col7" class="col_heading level0 col7" >moneda</th>
      <th id="T_71c95_level0_col8" class="col_heading level0 col8" >icp_inicial</th>
      <th id="T_71c95_level0_col9" class="col_heading level0 col9" >icp_final</th>
      <th id="T_71c95_level0_col10" class="col_heading level0 col10" >uf_inicial</th>
      <th id="T_71c95_level0_col11" class="col_heading level0 col11" >uf_final</th>
      <th id="T_71c95_level0_col12" class="col_heading level0 col12" >valor_tasa</th>
      <th id="T_71c95_level0_col13" class="col_heading level0 col13" >interes</th>
      <th id="T_71c95_level0_col14" class="col_heading level0 col14" >spread</th>
      <th id="T_71c95_level0_col15" class="col_heading level0 col15" >gearing</th>
      <th id="T_71c95_level0_col16" class="col_heading level0 col16" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_71c95_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_71c95_row0_col0" class="data row0 col0" >2018-05-31</td>
      <td id="T_71c95_row0_col1" class="data row0 col1" >2018-11-09</td>
      <td id="T_71c95_row0_col2" class="data row0 col2" >2018-11-09</td>
      <td id="T_71c95_row0_col3" class="data row0 col3" >600,000.00</td>
      <td id="T_71c95_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_71c95_row0_col5" class="data row0 col5" >True</td>
      <td id="T_71c95_row0_col6" class="data row0 col6" >0.00</td>
      <td id="T_71c95_row0_col7" class="data row0 col7" >CLF</td>
      <td id="T_71c95_row0_col8" class="data row0 col8" >10,000.00</td>
      <td id="T_71c95_row0_col9" class="data row0 col9" >10,000.00</td>
      <td id="T_71c95_row0_col10" class="data row0 col10" >35,000.00</td>
      <td id="T_71c95_row0_col11" class="data row0 col11" >35,000.00</td>
      <td id="T_71c95_row0_col12" class="data row0 col12" >0.0000%</td>
      <td id="T_71c95_row0_col13" class="data row0 col13" >0.00</td>
      <td id="T_71c95_row0_col14" class="data row0 col14" >0.0000%</td>
      <td id="T_71c95_row0_col15" class="data row0 col15" >1.00</td>
      <td id="T_71c95_row0_col16" class="data row0 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_71c95_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_71c95_row1_col0" class="data row1 col0" >2018-11-09</td>
      <td id="T_71c95_row1_col1" class="data row1 col1" >2019-05-09</td>
      <td id="T_71c95_row1_col2" class="data row1 col2" >2019-05-09</td>
      <td id="T_71c95_row1_col3" class="data row1 col3" >600,000.00</td>
      <td id="T_71c95_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_71c95_row1_col5" class="data row1 col5" >True</td>
      <td id="T_71c95_row1_col6" class="data row1 col6" >0.00</td>
      <td id="T_71c95_row1_col7" class="data row1 col7" >CLF</td>
      <td id="T_71c95_row1_col8" class="data row1 col8" >10,000.00</td>
      <td id="T_71c95_row1_col9" class="data row1 col9" >10,000.00</td>
      <td id="T_71c95_row1_col10" class="data row1 col10" >35,000.00</td>
      <td id="T_71c95_row1_col11" class="data row1 col11" >35,000.00</td>
      <td id="T_71c95_row1_col12" class="data row1 col12" >0.0000%</td>
      <td id="T_71c95_row1_col13" class="data row1 col13" >0.00</td>
      <td id="T_71c95_row1_col14" class="data row1 col14" >0.0000%</td>
      <td id="T_71c95_row1_col15" class="data row1 col15" >1.00</td>
      <td id="T_71c95_row1_col16" class="data row1 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_71c95_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_71c95_row2_col0" class="data row2 col0" >2019-05-09</td>
      <td id="T_71c95_row2_col1" class="data row2 col1" >2019-11-11</td>
      <td id="T_71c95_row2_col2" class="data row2 col2" >2019-11-11</td>
      <td id="T_71c95_row2_col3" class="data row2 col3" >600,000.00</td>
      <td id="T_71c95_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_71c95_row2_col5" class="data row2 col5" >True</td>
      <td id="T_71c95_row2_col6" class="data row2 col6" >0.00</td>
      <td id="T_71c95_row2_col7" class="data row2 col7" >CLF</td>
      <td id="T_71c95_row2_col8" class="data row2 col8" >10,000.00</td>
      <td id="T_71c95_row2_col9" class="data row2 col9" >10,000.00</td>
      <td id="T_71c95_row2_col10" class="data row2 col10" >35,000.00</td>
      <td id="T_71c95_row2_col11" class="data row2 col11" >35,000.00</td>
      <td id="T_71c95_row2_col12" class="data row2 col12" >0.0000%</td>
      <td id="T_71c95_row2_col13" class="data row2 col13" >0.00</td>
      <td id="T_71c95_row2_col14" class="data row2 col14" >0.0000%</td>
      <td id="T_71c95_row2_col15" class="data row2 col15" >1.00</td>
      <td id="T_71c95_row2_col16" class="data row2 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_71c95_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_71c95_row3_col0" class="data row3 col0" >2019-11-11</td>
      <td id="T_71c95_row3_col1" class="data row3 col1" >2020-05-11</td>
      <td id="T_71c95_row3_col2" class="data row3 col2" >2020-05-11</td>
      <td id="T_71c95_row3_col3" class="data row3 col3" >600,000.00</td>
      <td id="T_71c95_row3_col4" class="data row3 col4" >0.00</td>
      <td id="T_71c95_row3_col5" class="data row3 col5" >True</td>
      <td id="T_71c95_row3_col6" class="data row3 col6" >-7,178.78</td>
      <td id="T_71c95_row3_col7" class="data row3 col7" >CLF</td>
      <td id="T_71c95_row3_col8" class="data row3 col8" >18,786.13</td>
      <td id="T_71c95_row3_col9" class="data row3 col9" >18,943.62</td>
      <td id="T_71c95_row3_col10" class="data row3 col10" >28,080.26</td>
      <td id="T_71c95_row3_col11" class="data row3 col11" >28,658.55</td>
      <td id="T_71c95_row3_col12" class="data row3 col12" >-2.3649%</td>
      <td id="T_71c95_row3_col13" class="data row3 col13" >-7,173.53</td>
      <td id="T_71c95_row3_col14" class="data row3 col14" >0.0000%</td>
      <td id="T_71c95_row3_col15" class="data row3 col15" >1.00</td>
      <td id="T_71c95_row3_col16" class="data row3 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_71c95_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_71c95_row4_col0" class="data row4 col0" >2020-05-11</td>
      <td id="T_71c95_row4_col1" class="data row4 col1" >2020-11-09</td>
      <td id="T_71c95_row4_col2" class="data row4 col2" >2020-11-09</td>
      <td id="T_71c95_row4_col3" class="data row4 col3" >600,000.00</td>
      <td id="T_71c95_row4_col4" class="data row4 col4" >0.00</td>
      <td id="T_71c95_row4_col5" class="data row4 col5" >True</td>
      <td id="T_71c95_row4_col6" class="data row4 col6" >-5,300.72</td>
      <td id="T_71c95_row4_col7" class="data row4 col7" >CLF</td>
      <td id="T_71c95_row4_col8" class="data row4 col8" >18,943.62</td>
      <td id="T_71c95_row4_col9" class="data row4 col9" >19,056.79</td>
      <td id="T_71c95_row4_col10" class="data row4 col10" >28,658.55</td>
      <td id="T_71c95_row4_col11" class="data row4 col11" >29,086.73</td>
      <td id="T_71c95_row4_col12" class="data row4 col12" >-1.7492%</td>
      <td id="T_71c95_row4_col13" class="data row4 col13" >-5,305.91</td>
      <td id="T_71c95_row4_col14" class="data row4 col14" >0.0000%</td>
      <td id="T_71c95_row4_col15" class="data row4 col15" >1.00</td>
      <td id="T_71c95_row4_col16" class="data row4 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_71c95_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_71c95_row5_col0" class="data row5 col0" >2020-11-09</td>
      <td id="T_71c95_row5_col1" class="data row5 col1" >2021-05-10</td>
      <td id="T_71c95_row5_col2" class="data row5 col2" >2021-05-10</td>
      <td id="T_71c95_row5_col3" class="data row5 col3" >600,000.00</td>
      <td id="T_71c95_row5_col4" class="data row5 col4" >0.00</td>
      <td id="T_71c95_row5_col5" class="data row5 col5" >True</td>
      <td id="T_71c95_row5_col6" class="data row5 col6" >-3,909.59</td>
      <td id="T_71c95_row5_col7" class="data row5 col7" >CLF</td>
      <td id="T_71c95_row5_col8" class="data row5 col8" >19,056.79</td>
      <td id="T_71c95_row5_col9" class="data row5 col9" >19,182.42</td>
      <td id="T_71c95_row5_col10" class="data row5 col10" >29,086.73</td>
      <td id="T_71c95_row5_col11" class="data row5 col11" >29,470.52</td>
      <td id="T_71c95_row5_col12" class="data row5 col12" >-1.2929%</td>
      <td id="T_71c95_row5_col13" class="data row5 col13" >-3,921.80</td>
      <td id="T_71c95_row5_col14" class="data row5 col14" >0.0000%</td>
      <td id="T_71c95_row5_col15" class="data row5 col15" >1.00</td>
      <td id="T_71c95_row5_col16" class="data row5 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_71c95_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_71c95_row6_col0" class="data row6 col0" >2021-05-10</td>
      <td id="T_71c95_row6_col1" class="data row6 col1" >2021-11-09</td>
      <td id="T_71c95_row6_col2" class="data row6 col2" >2021-11-09</td>
      <td id="T_71c95_row6_col3" class="data row6 col3" >600,000.00</td>
      <td id="T_71c95_row6_col4" class="data row6 col4" >0.00</td>
      <td id="T_71c95_row6_col5" class="data row6 col5" >True</td>
      <td id="T_71c95_row6_col6" class="data row6 col6" >-4,842.13</td>
      <td id="T_71c95_row6_col7" class="data row6 col7" >CLF</td>
      <td id="T_71c95_row6_col8" class="data row6 col8" >19,182.42</td>
      <td id="T_71c95_row6_col9" class="data row6 col9" >19,306.95</td>
      <td id="T_71c95_row6_col10" class="data row6 col10" >29,470.52</td>
      <td id="T_71c95_row6_col11" class="data row6 col11" >29,903.16</td>
      <td id="T_71c95_row6_col12" class="data row6 col12" >-1.5847%</td>
      <td id="T_71c95_row6_col13" class="data row6 col13" >-4,833.34</td>
      <td id="T_71c95_row6_col14" class="data row6 col14" >0.0000%</td>
      <td id="T_71c95_row6_col15" class="data row6 col15" >1.00</td>
      <td id="T_71c95_row6_col16" class="data row6 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_71c95_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_71c95_row7_col0" class="data row7 col0" >2021-11-09</td>
      <td id="T_71c95_row7_col1" class="data row7 col1" >2022-05-09</td>
      <td id="T_71c95_row7_col2" class="data row7 col2" >2022-05-09</td>
      <td id="T_71c95_row7_col3" class="data row7 col3" >600,000.00</td>
      <td id="T_71c95_row7_col4" class="data row7 col4" >0.00</td>
      <td id="T_71c95_row7_col5" class="data row7 col5" >True</td>
      <td id="T_71c95_row7_col6" class="data row7 col6" >-5,431.38</td>
      <td id="T_71c95_row7_col7" class="data row7 col7" >CLF</td>
      <td id="T_71c95_row7_col8" class="data row7 col8" >19,306.95</td>
      <td id="T_71c95_row7_col9" class="data row7 col9" >19,440.27</td>
      <td id="T_71c95_row7_col10" class="data row7 col10" >29,903.16</td>
      <td id="T_71c95_row7_col11" class="data row7 col11" >30,384.70</td>
      <td id="T_71c95_row7_col12" class="data row7 col12" >-1.8038%</td>
      <td id="T_71c95_row7_col13" class="data row7 col13" >-5,441.46</td>
      <td id="T_71c95_row7_col14" class="data row7 col14" >0.0000%</td>
      <td id="T_71c95_row7_col15" class="data row7 col15" >1.00</td>
      <td id="T_71c95_row7_col16" class="data row7 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_71c95_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_71c95_row8_col0" class="data row8 col0" >2022-05-09</td>
      <td id="T_71c95_row8_col1" class="data row8 col1" >2022-11-09</td>
      <td id="T_71c95_row8_col2" class="data row8 col2" >2022-11-09</td>
      <td id="T_71c95_row8_col3" class="data row8 col3" >600,000.00</td>
      <td id="T_71c95_row8_col4" class="data row8 col4" >0.00</td>
      <td id="T_71c95_row8_col5" class="data row8 col5" >True</td>
      <td id="T_71c95_row8_col6" class="data row8 col6" >-3,700.83</td>
      <td id="T_71c95_row8_col7" class="data row8 col7" >CLF</td>
      <td id="T_71c95_row8_col8" class="data row8 col8" >19,440.27</td>
      <td id="T_71c95_row8_col9" class="data row8 col9" >19,606.92</td>
      <td id="T_71c95_row8_col10" class="data row8 col10" >30,384.70</td>
      <td id="T_71c95_row8_col11" class="data row8 col11" >30,835.35</td>
      <td id="T_71c95_row8_col12" class="data row8 col12" >-1.2040%</td>
      <td id="T_71c95_row8_col13" class="data row8 col13" >-3,692.27</td>
      <td id="T_71c95_row8_col14" class="data row8 col14" >0.0000%</td>
      <td id="T_71c95_row8_col15" class="data row8 col15" >1.00</td>
      <td id="T_71c95_row8_col16" class="data row8 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_71c95_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_71c95_row9_col0" class="data row9 col0" >2022-11-09</td>
      <td id="T_71c95_row9_col1" class="data row9 col1" >2023-05-09</td>
      <td id="T_71c95_row9_col2" class="data row9 col2" >2023-05-09</td>
      <td id="T_71c95_row9_col3" class="data row9 col3" >600,000.00</td>
      <td id="T_71c95_row9_col4" class="data row9 col4" >0.00</td>
      <td id="T_71c95_row9_col5" class="data row9 col5" >True</td>
      <td id="T_71c95_row9_col6" class="data row9 col6" >-2,958.63</td>
      <td id="T_71c95_row9_col7" class="data row9 col7" >CLF</td>
      <td id="T_71c95_row9_col8" class="data row9 col8" >19,606.92</td>
      <td id="T_71c95_row9_col9" class="data row9 col9" >19,794.39</td>
      <td id="T_71c95_row9_col10" class="data row9 col10" >30,835.35</td>
      <td id="T_71c95_row9_col11" class="data row9 col11" >31,284.45</td>
      <td id="T_71c95_row9_col12" class="data row9 col12" >-0.9825%</td>
      <td id="T_71c95_row9_col13" class="data row9 col13" >-2,963.88</td>
      <td id="T_71c95_row9_col14" class="data row9 col14" >0.0000%</td>
      <td id="T_71c95_row9_col15" class="data row9 col15" >1.00</td>
      <td id="T_71c95_row9_col16" class="data row9 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_71c95_level0_row10" class="row_heading level0 row10" >10</th>
      <td id="T_71c95_row10_col0" class="data row10 col0" >2023-05-09</td>
      <td id="T_71c95_row10_col1" class="data row10 col1" >2023-11-09</td>
      <td id="T_71c95_row10_col2" class="data row10 col2" >2023-11-09</td>
      <td id="T_71c95_row10_col3" class="data row10 col3" >600,000.00</td>
      <td id="T_71c95_row10_col4" class="data row10 col4" >0.00</td>
      <td id="T_71c95_row10_col5" class="data row10 col5" >True</td>
      <td id="T_71c95_row10_col6" class="data row10 col6" >-2,109.44</td>
      <td id="T_71c95_row10_col7" class="data row10 col7" >CLF</td>
      <td id="T_71c95_row10_col8" class="data row10 col8" >19,794.39</td>
      <td id="T_71c95_row10_col9" class="data row10 col9" >20,019.87</td>
      <td id="T_71c95_row10_col10" class="data row10 col10" >31,284.45</td>
      <td id="T_71c95_row10_col11" class="data row10 col11" >31,752.45</td>
      <td id="T_71c95_row10_col12" class="data row10 col12" >-0.6866%</td>
      <td id="T_71c95_row10_col13" class="data row10 col13" >-2,105.57</td>
      <td id="T_71c95_row10_col14" class="data row10 col14" >0.0000%</td>
      <td id="T_71c95_row10_col15" class="data row10 col15" >1.00</td>
      <td id="T_71c95_row10_col16" class="data row10 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_71c95_level0_row11" class="row_heading level0 row11" >11</th>
      <td id="T_71c95_row11_col0" class="data row11 col0" >2023-11-09</td>
      <td id="T_71c95_row11_col1" class="data row11 col1" >2024-05-09</td>
      <td id="T_71c95_row11_col2" class="data row11 col2" >2024-05-09</td>
      <td id="T_71c95_row11_col3" class="data row11 col3" >600,000.00</td>
      <td id="T_71c95_row11_col4" class="data row11 col4" >0.00</td>
      <td id="T_71c95_row11_col5" class="data row11 col5" >True</td>
      <td id="T_71c95_row11_col6" class="data row11 col6" >-1,201.71</td>
      <td id="T_71c95_row11_col7" class="data row11 col7" >CLF</td>
      <td id="T_71c95_row11_col8" class="data row11 col8" >20,019.87</td>
      <td id="T_71c95_row11_col9" class="data row11 col9" >20,277.70</td>
      <td id="T_71c95_row11_col10" class="data row11 col10" >31,752.45</td>
      <td id="T_71c95_row11_col11" class="data row11 col11" >32,225.93</td>
      <td id="T_71c95_row11_col12" class="data row11 col12" >-0.3937%</td>
      <td id="T_71c95_row11_col13" class="data row11 col13" >-1,194.22</td>
      <td id="T_71c95_row11_col14" class="data row11 col14" >0.0000%</td>
      <td id="T_71c95_row11_col15" class="data row11 col15" >1.00</td>
      <td id="T_71c95_row11_col16" class="data row11 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_71c95_level0_row12" class="row_heading level0 row12" >12</th>
      <td id="T_71c95_row12_col0" class="data row12 col0" >2024-05-09</td>
      <td id="T_71c95_row12_col1" class="data row12 col1" >2024-11-11</td>
      <td id="T_71c95_row12_col2" class="data row12 col2" >2024-11-11</td>
      <td id="T_71c95_row12_col3" class="data row12 col3" >600,000.00</td>
      <td id="T_71c95_row12_col4" class="data row12 col4" >0.00</td>
      <td id="T_71c95_row12_col5" class="data row12 col5" >True</td>
      <td id="T_71c95_row12_col6" class="data row12 col6" >-92.82</td>
      <td id="T_71c95_row12_col7" class="data row12 col7" >CLF</td>
      <td id="T_71c95_row12_col8" class="data row12 col8" >20,277.70</td>
      <td id="T_71c95_row12_col9" class="data row12 col9" >20,590.52</td>
      <td id="T_71c95_row12_col10" class="data row12 col10" >32,225.93</td>
      <td id="T_71c95_row12_col11" class="data row12 col11" >32,728.13</td>
      <td id="T_71c95_row12_col12" class="data row12 col12" >-0.0258%</td>
      <td id="T_71c95_row12_col13" class="data row12 col13" >-79.98</td>
      <td id="T_71c95_row12_col14" class="data row12 col14" >0.0000%</td>
      <td id="T_71c95_row12_col15" class="data row12 col15" >1.00</td>
      <td id="T_71c95_row12_col16" class="data row12 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_71c95_level0_row13" class="row_heading level0 row13" >13</th>
      <td id="T_71c95_row13_col0" class="data row13 col0" >2024-11-11</td>
      <td id="T_71c95_row13_col1" class="data row13 col1" >2025-05-09</td>
      <td id="T_71c95_row13_col2" class="data row13 col2" >2025-05-09</td>
      <td id="T_71c95_row13_col3" class="data row13 col3" >600,000.00</td>
      <td id="T_71c95_row13_col4" class="data row13 col4" >0.00</td>
      <td id="T_71c95_row13_col5" class="data row13 col5" >True</td>
      <td id="T_71c95_row13_col6" class="data row13 col6" >488.22</td>
      <td id="T_71c95_row13_col7" class="data row13 col7" >CLF</td>
      <td id="T_71c95_row13_col8" class="data row13 col8" >20,590.52</td>
      <td id="T_71c95_row13_col9" class="data row13 col9" >20,916.74</td>
      <td id="T_71c95_row13_col10" class="data row13 col10" >32,728.13</td>
      <td id="T_71c95_row13_col11" class="data row13 col11" >33,219.63</td>
      <td id="T_71c95_row13_col12" class="data row13 col12" >0.1672%</td>
      <td id="T_71c95_row13_col13" class="data row13 col13" >498.81</td>
      <td id="T_71c95_row13_col14" class="data row13 col14" >0.0000%</td>
      <td id="T_71c95_row13_col15" class="data row13 col15" >1.00</td>
      <td id="T_71c95_row13_col16" class="data row13 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_71c95_level0_row14" class="row_heading level0 row14" >14</th>
      <td id="T_71c95_row14_col0" class="data row14 col0" >2025-05-09</td>
      <td id="T_71c95_row14_col1" class="data row14 col1" >2025-11-10</td>
      <td id="T_71c95_row14_col2" class="data row14 col2" >2025-11-10</td>
      <td id="T_71c95_row14_col3" class="data row14 col3" >600,000.00</td>
      <td id="T_71c95_row14_col4" class="data row14 col4" >0.00</td>
      <td id="T_71c95_row14_col5" class="data row14 col5" >True</td>
      <td id="T_71c95_row14_col6" class="data row14 col6" >892.29</td>
      <td id="T_71c95_row14_col7" class="data row14 col7" >CLF</td>
      <td id="T_71c95_row14_col8" class="data row14 col8" >20,916.74</td>
      <td id="T_71c95_row14_col9" class="data row14 col9" >21,275.98</td>
      <td id="T_71c95_row14_col10" class="data row14 col10" >33,219.63</td>
      <td id="T_71c95_row14_col11" class="data row14 col11" >33,739.98</td>
      <td id="T_71c95_row14_col12" class="data row14 col12" >0.2874%</td>
      <td id="T_71c95_row14_col13" class="data row14 col13" >886.15</td>
      <td id="T_71c95_row14_col14" class="data row14 col14" >0.0000%</td>
      <td id="T_71c95_row14_col15" class="data row14 col15" >1.00</td>
      <td id="T_71c95_row14_col16" class="data row14 col16" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_71c95_level0_row15" class="row_heading level0 row15" >15</th>
      <td id="T_71c95_row15_col0" class="data row15 col0" >2025-11-10</td>
      <td id="T_71c95_row15_col1" class="data row15 col1" >2026-05-11</td>
      <td id="T_71c95_row15_col2" class="data row15 col2" >2026-05-11</td>
      <td id="T_71c95_row15_col3" class="data row15 col3" >600,000.00</td>
      <td id="T_71c95_row15_col4" class="data row15 col4" >600,000.00</td>
      <td id="T_71c95_row15_col5" class="data row15 col5" >True</td>
      <td id="T_71c95_row15_col6" class="data row15 col6" >601,540.00</td>
      <td id="T_71c95_row15_col7" class="data row15 col7" >CLF</td>
      <td id="T_71c95_row15_col8" class="data row15 col8" >21,275.98</td>
      <td id="T_71c95_row15_col9" class="data row15 col9" >21,660.54</td>
      <td id="T_71c95_row15_col10" class="data row15 col10" >33,739.98</td>
      <td id="T_71c95_row15_col11" class="data row15 col11" >34,261.88</td>
      <td id="T_71c95_row15_col12" class="data row15 col12" >0.5124%</td>
      <td id="T_71c95_row15_col13" class="data row15 col13" >1,554.28</td>
      <td id="T_71c95_row15_col14" class="data row15 col14" >0.0000%</td>
      <td id="T_71c95_row15_col15" class="data row15 col15" >1.00</td>
      <td id="T_71c95_row15_col16" class="data row15 col16" >LinAct360</td>
    </tr>
  </tbody>
</table>





```python
vp_icp_clf = pv.pv(fecha_hoy, icp_clf_leg, zz3)
print("Valor presente en UF: {0:,.2f}".format(vp_icp_clf))
print("Valor presente en CLP: {0:,.0f}".format(vp_icp_clf * uf_hoy))
```

    Valor presente en UF: 595,431.99
    Valor presente en CLP: 16,934,198,846



```python
print("Dif %: {0:.4%}".format(12_940.56/12_943.45-1))
```

    Dif %: -0.0223%



```python
der = pv.get_derivatives()
i = 0
bp = .0001
for d in der:
    print("Sensibilidad en {0:}: {1:0,.2f}".format(i, d * bp))
    i += 1
print("Sensibilidad de descuento: {0:,.2f} CLF".format(sum(der) * bp))
```

    Sensibilidad en 0: 0.00
    Sensibilidad en 1: 0.00
    Sensibilidad en 2: 0.00
    Sensibilidad en 3: 0.10
    Sensibilidad en 4: 0.06
    Sensibilidad en 5: 0.00
    Sensibilidad en 6: 0.00
    Sensibilidad en 7: 0.00
    Sensibilidad en 8: 0.00
    Sensibilidad en 9: 0.27
    Sensibilidad en 10: 0.12
    Sensibilidad en 11: 0.00
    Sensibilidad en 12: 0.00
    Sensibilidad en 13: 0.00
    Sensibilidad en 14: 0.00
    Sensibilidad en 15: 0.32
    Sensibilidad en 16: 0.18
    Sensibilidad en 17: 0.00
    Sensibilidad en 18: 0.00
    Sensibilidad en 19: 0.00
    Sensibilidad en 20: 0.65
    Sensibilidad en 21: 1.63
    Sensibilidad en 22: 2.15
    Sensibilidad en 23: 1.29
    Sensibilidad en 24: -0.26
    Sensibilidad en 25: -335.81
    Sensibilidad en 26: -82.41
    Sensibilidad en 27: 0.00
    Sensibilidad en 28: 0.00
    Sensibilidad en 29: 0.00
    Sensibilidad en 30: 0.00
    Sensibilidad en 31: 0.00
    Sensibilidad en 32: 0.00
    Sensibilidad de descuento: -411.73 CLF



```python
bp = .0001
result = []

for i in range(icp_clf_leg.size()):
    cshflw = icp_clf_leg.get_cashflow_at(i)
    df = zz3.get_discount_factor_at(fecha_hoy.day_diff(cshflw.date()))
    amt_der = cshflw.get_amount_ufclf_derivatives()
    if len(amt_der) > 0:
        amt_der = [a * bp * df for a in amt_der]
        result.append(np.array(amt_der))

total = result[0] * 0
for r in result:
    total += r

for i in range(len(total)):
    print("Sensibilidad en {0:}: {1:0,.2f}".format(i, total[i]))
```

    Sensibilidad en 0: 0.00
    Sensibilidad en 1: 0.00
    Sensibilidad en 2: 0.00
    Sensibilidad en 3: -0.10
    Sensibilidad en 4: -0.06
    Sensibilidad en 5: 0.00
    Sensibilidad en 6: 0.00
    Sensibilidad en 7: 0.00
    Sensibilidad en 8: 0.00
    Sensibilidad en 9: -0.27
    Sensibilidad en 10: -0.12
    Sensibilidad en 11: 0.00
    Sensibilidad en 12: 0.00
    Sensibilidad en 13: 0.00
    Sensibilidad en 14: 0.00
    Sensibilidad en 15: -0.32
    Sensibilidad en 16: -0.18
    Sensibilidad en 17: 0.00
    Sensibilidad en 18: 0.00
    Sensibilidad en 19: 0.00
    Sensibilidad en 20: -0.65
    Sensibilidad en 21: -1.63
    Sensibilidad en 22: -2.15
    Sensibilidad en 23: -1.29
    Sensibilidad en 24: 0.26
    Sensibilidad en 25: 335.81
    Sensibilidad en 26: 82.41
    Sensibilidad en 27: 0.00
    Sensibilidad en 28: 0.00
    Sensibilidad en 29: 0.00
    Sensibilidad en 30: 0.00
    Sensibilidad en 31: 0.00
    Sensibilidad en 32: 0.00


### CompoundedOvernightRate Leg


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
ts = qcf.time_series()
ts[qcf.QCDate(27, 12, 2021)] = .01
ts[qcf.QCDate(28, 12, 2021)] = .02
ts[qcf.QCDate(29, 12, 2021)] = .03
ts[qcf.QCDate(30, 12, 2021)] = .04
ts[qcf.QCDate(31, 12, 2021)] = .04
```

#### Valor Presente


```python
fwd_rates.set_rates_compounded_overnight_leg(
    fecha_inicio,
    cor_leg,
    zz1,
    ts
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
<table id="T_ca016">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_ca016_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_ca016_level0_col1" class="col_heading level0 col1" >fecha__final</th>
      <th id="T_ca016_level0_col2" class="col_heading level0 col2" >fecha__pago</th>
      <th id="T_ca016_level0_col3" class="col_heading level0 col3" >nominal</th>
      <th id="T_ca016_level0_col4" class="col_heading level0 col4" >amort</th>
      <th id="T_ca016_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_ca016_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_ca016_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_ca016_level0_col8" class="col_heading level0 col8" >moneda</th>
      <th id="T_ca016_level0_col9" class="col_heading level0 col9" >indice</th>
      <th id="T_ca016_level0_col10" class="col_heading level0 col10" >valor_tasa</th>
      <th id="T_ca016_level0_col11" class="col_heading level0 col11" >spread</th>
      <th id="T_ca016_level0_col12" class="col_heading level0 col12" >gearing</th>
      <th id="T_ca016_level0_col13" class="col_heading level0 col13" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_ca016_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_ca016_row0_col0" class="data row0 col0" >2022-01-03</td>
      <td id="T_ca016_row0_col1" class="data row0 col1" >2022-04-04</td>
      <td id="T_ca016_row0_col2" class="data row0 col2" >2022-04-04</td>
      <td id="T_ca016_row0_col3" class="data row0 col3" >1,000,000.00</td>
      <td id="T_ca016_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_ca016_row0_col5" class="data row0 col5" >2,527.78</td>
      <td id="T_ca016_row0_col6" class="data row0 col6" >True</td>
      <td id="T_ca016_row0_col7" class="data row0 col7" >6,322.09</td>
      <td id="T_ca016_row0_col8" class="data row0 col8" >USD</td>
      <td id="T_ca016_row0_col9" class="data row0 col9" >OISTEST</td>
      <td id="T_ca016_row0_col10" class="data row0 col10" >1.5010%</td>
      <td id="T_ca016_row0_col11" class="data row0 col11" >1.0000%</td>
      <td id="T_ca016_row0_col12" class="data row0 col12" >1.00</td>
      <td id="T_ca016_row0_col13" class="data row0 col13" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_ca016_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_ca016_row1_col0" class="data row1 col0" >2022-04-04</td>
      <td id="T_ca016_row1_col1" class="data row1 col1" >2022-07-04</td>
      <td id="T_ca016_row1_col2" class="data row1 col2" >2022-07-04</td>
      <td id="T_ca016_row1_col3" class="data row1 col3" >1,000,000.00</td>
      <td id="T_ca016_row1_col4" class="data row1 col4" >0.00</td>
      <td id="T_ca016_row1_col5" class="data row1 col5" >2,527.78</td>
      <td id="T_ca016_row1_col6" class="data row1 col6" >True</td>
      <td id="T_ca016_row1_col7" class="data row1 col7" >5,379.73</td>
      <td id="T_ca016_row1_col8" class="data row1 col8" >USD</td>
      <td id="T_ca016_row1_col9" class="data row1 col9" >OISTEST</td>
      <td id="T_ca016_row1_col10" class="data row1 col10" >1.1282%</td>
      <td id="T_ca016_row1_col11" class="data row1 col11" >1.0000%</td>
      <td id="T_ca016_row1_col12" class="data row1 col12" >1.00</td>
      <td id="T_ca016_row1_col13" class="data row1 col13" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_ca016_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_ca016_row2_col0" class="data row2 col0" >2022-07-04</td>
      <td id="T_ca016_row2_col1" class="data row2 col1" >2022-10-03</td>
      <td id="T_ca016_row2_col2" class="data row2 col2" >2022-10-03</td>
      <td id="T_ca016_row2_col3" class="data row2 col3" >1,000,000.00</td>
      <td id="T_ca016_row2_col4" class="data row2 col4" >0.00</td>
      <td id="T_ca016_row2_col5" class="data row2 col5" >2,527.78</td>
      <td id="T_ca016_row2_col6" class="data row2 col6" >True</td>
      <td id="T_ca016_row2_col7" class="data row2 col7" >5,618.72</td>
      <td id="T_ca016_row2_col8" class="data row2 col8" >USD</td>
      <td id="T_ca016_row2_col9" class="data row2 col9" >OISTEST</td>
      <td id="T_ca016_row2_col10" class="data row2 col10" >1.2228%</td>
      <td id="T_ca016_row2_col11" class="data row2 col11" >1.0000%</td>
      <td id="T_ca016_row2_col12" class="data row2 col12" >1.00</td>
      <td id="T_ca016_row2_col13" class="data row2 col13" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_ca016_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_ca016_row3_col0" class="data row3 col0" >2022-10-03</td>
      <td id="T_ca016_row3_col1" class="data row3 col1" >2023-01-03</td>
      <td id="T_ca016_row3_col2" class="data row3 col2" >2023-01-03</td>
      <td id="T_ca016_row3_col3" class="data row3 col3" >1,000,000.00</td>
      <td id="T_ca016_row3_col4" class="data row3 col4" >1,000,000.00</td>
      <td id="T_ca016_row3_col5" class="data row3 col5" >2,555.56</td>
      <td id="T_ca016_row3_col6" class="data row3 col6" >True</td>
      <td id="T_ca016_row3_col7" class="data row3 col7" >1,005,930.44</td>
      <td id="T_ca016_row3_col8" class="data row3 col8" >USD</td>
      <td id="T_ca016_row3_col9" class="data row3 col9" >OISTEST</td>
      <td id="T_ca016_row3_col10" class="data row3 col10" >1.3206%</td>
      <td id="T_ca016_row3_col11" class="data row3 col11" >1.0000%</td>
      <td id="T_ca016_row3_col12" class="data row3 col12" >1.00</td>
      <td id="T_ca016_row3_col13" class="data row3 col13" >LinAct360</td>
    </tr>
  </tbody>
</table>





```python
print(f'{pv.pv(fecha_inicio, cor_leg, zz1):,.0f}')
```

    1,010,055



```python
pres_value = 0.0
for i in range(0, cor_leg.size()):
    cshflw = cor_leg.get_cashflow_at(i)
    print(f'{cshflw.amount():,.2f}, {cshflw.get_amortization()}')
    temp = pv.pv(fecha_inicio, cshflw, zz1)
    # print(f'{temp:,.0f}')
    pres_value += temp
print(f'{pres_value:,.0f}')
```

    6,322.09, 0.0
    5,379.73, 0.0
    5,618.72, 0.0
    1,005,930.44, 1000000.0
    1,010,055


#### Sensibilidad


```python
pips = .0001 # 1 punto básico
```

##### Curva de Proyección

Estas derivadas se deben obtener inmediatamente después de calcular el valor presente.


```python
proj_sens_by_cashflow = np.array([np.array(
    np.array(cor_leg.get_cashflow_at(i).get_amount_derivatives()) *
    zz1.get_discount_factor_at(fecha_inicio.day_diff(cor_leg.get_cashflow_at(i).get_settlement_date())) * pips)
                             for i in range(cor_leg.size())])
proj_sens = np.sum(proj_sens_by_cashflow, axis=0)
```

##### Curva de Descuento


```python
disc_der = np.array(pv.get_derivatives()) * pips
```
