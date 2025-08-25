# Curva SOFR

Se construye la curva cupón cero asociada a los swaps de SOFR vs tasa fija:

Se utiliza el procedimiento clásico que consiste en:

- Resolver el sistema de ecuaciones que iguala el valor presente de las patas fijas (en `start_date`) con el valor del nocional.
- Se considera como flujo el nocional al vencimiento.
- Es importante notar que para que estas ecuaciones sean válidas se debe suponer que el settlement lag es siempre igual a 0.


```python
import qcfinancial as qcf
import pandas as pd
import aux_functions as aux
```

## Data

La data se obtiene del asiguiente archivo Excel. En él, además de las tasas de los swaps, se ha registrado las características principales de estos contratos.


```python
data = pd.read_excel("./input/20240621_sofr_data.xlsx")
```


```python
data.style.format({'rate':'{:.4%}'})
```




<style type="text/css">
</style>
<table id="T_70e36">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_70e36_level0_col0" class="col_heading level0 col0" >ticket</th>
      <th id="T_70e36_level0_col1" class="col_heading level0 col1" >start_date</th>
      <th id="T_70e36_level0_col2" class="col_heading level0 col2" >tenor</th>
      <th id="T_70e36_level0_col3" class="col_heading level0 col3" >stub_period</th>
      <th id="T_70e36_level0_col4" class="col_heading level0 col4" >pay_freq</th>
      <th id="T_70e36_level0_col5" class="col_heading level0 col5" >settlement_lag</th>
      <th id="T_70e36_level0_col6" class="col_heading level0 col6" >bus_adj_rule</th>
      <th id="T_70e36_level0_col7" class="col_heading level0 col7" >yf</th>
      <th id="T_70e36_level0_col8" class="col_heading level0 col8" >wf</th>
      <th id="T_70e36_level0_col9" class="col_heading level0 col9" >rate</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_70e36_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_70e36_row0_col0" class="data row0 col0" >USOSFR1Z BGN Curncy</td>
      <td id="T_70e36_row0_col1" class="data row0 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row0_col2" class="data row0 col2" >7D</td>
      <td id="T_70e36_row0_col3" class="data row0 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row0_col4" class="data row0 col4" >2Y</td>
      <td id="T_70e36_row0_col5" class="data row0 col5" >2</td>
      <td id="T_70e36_row0_col6" class="data row0 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row0_col7" class="data row0 col7" >Act360</td>
      <td id="T_70e36_row0_col8" class="data row0 col8" >Lin</td>
      <td id="T_70e36_row0_col9" class="data row0 col9" >5.3342%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_70e36_row1_col0" class="data row1 col0" >USOSFR2Z BGN Curncy</td>
      <td id="T_70e36_row1_col1" class="data row1 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row1_col2" class="data row1 col2" >14D</td>
      <td id="T_70e36_row1_col3" class="data row1 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row1_col4" class="data row1 col4" >2Y</td>
      <td id="T_70e36_row1_col5" class="data row1 col5" >2</td>
      <td id="T_70e36_row1_col6" class="data row1 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row1_col7" class="data row1 col7" >Act360</td>
      <td id="T_70e36_row1_col8" class="data row1 col8" >Lin</td>
      <td id="T_70e36_row1_col9" class="data row1 col9" >5.3375%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_70e36_row2_col0" class="data row2 col0" >USOSFR3Z BGN Curncy</td>
      <td id="T_70e36_row2_col1" class="data row2 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row2_col2" class="data row2 col2" >21D</td>
      <td id="T_70e36_row2_col3" class="data row2 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row2_col4" class="data row2 col4" >2Y</td>
      <td id="T_70e36_row2_col5" class="data row2 col5" >2</td>
      <td id="T_70e36_row2_col6" class="data row2 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row2_col7" class="data row2 col7" >Act360</td>
      <td id="T_70e36_row2_col8" class="data row2 col8" >Lin</td>
      <td id="T_70e36_row2_col9" class="data row2 col9" >5.3415%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_70e36_row3_col0" class="data row3 col0" >USOSFRA BGN Curncy</td>
      <td id="T_70e36_row3_col1" class="data row3 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row3_col2" class="data row3 col2" >1M</td>
      <td id="T_70e36_row3_col3" class="data row3 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row3_col4" class="data row3 col4" >2Y</td>
      <td id="T_70e36_row3_col5" class="data row3 col5" >2</td>
      <td id="T_70e36_row3_col6" class="data row3 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row3_col7" class="data row3 col7" >Act360</td>
      <td id="T_70e36_row3_col8" class="data row3 col8" >Lin</td>
      <td id="T_70e36_row3_col9" class="data row3 col9" >5.3442%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_70e36_row4_col0" class="data row4 col0" >USOSFRB BGN Curncy</td>
      <td id="T_70e36_row4_col1" class="data row4 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row4_col2" class="data row4 col2" >2M</td>
      <td id="T_70e36_row4_col3" class="data row4 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row4_col4" class="data row4 col4" >2Y</td>
      <td id="T_70e36_row4_col5" class="data row4 col5" >2</td>
      <td id="T_70e36_row4_col6" class="data row4 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row4_col7" class="data row4 col7" >Act360</td>
      <td id="T_70e36_row4_col8" class="data row4 col8" >Lin</td>
      <td id="T_70e36_row4_col9" class="data row4 col9" >5.3454%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_70e36_row5_col0" class="data row5 col0" >USOSFRC BGN Curncy</td>
      <td id="T_70e36_row5_col1" class="data row5 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row5_col2" class="data row5 col2" >3M</td>
      <td id="T_70e36_row5_col3" class="data row5 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row5_col4" class="data row5 col4" >2Y</td>
      <td id="T_70e36_row5_col5" class="data row5 col5" >2</td>
      <td id="T_70e36_row5_col6" class="data row5 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row5_col7" class="data row5 col7" >Act360</td>
      <td id="T_70e36_row5_col8" class="data row5 col8" >Lin</td>
      <td id="T_70e36_row5_col9" class="data row5 col9" >5.3426%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_70e36_row6_col0" class="data row6 col0" >USOSFRD BGN Curncy</td>
      <td id="T_70e36_row6_col1" class="data row6 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row6_col2" class="data row6 col2" >4M</td>
      <td id="T_70e36_row6_col3" class="data row6 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row6_col4" class="data row6 col4" >2Y</td>
      <td id="T_70e36_row6_col5" class="data row6 col5" >2</td>
      <td id="T_70e36_row6_col6" class="data row6 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row6_col7" class="data row6 col7" >Act360</td>
      <td id="T_70e36_row6_col8" class="data row6 col8" >Lin</td>
      <td id="T_70e36_row6_col9" class="data row6 col9" >5.3171%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_70e36_row7_col0" class="data row7 col0" >USOSFRE BGN Curncy</td>
      <td id="T_70e36_row7_col1" class="data row7 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row7_col2" class="data row7 col2" >5M</td>
      <td id="T_70e36_row7_col3" class="data row7 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row7_col4" class="data row7 col4" >2Y</td>
      <td id="T_70e36_row7_col5" class="data row7 col5" >2</td>
      <td id="T_70e36_row7_col6" class="data row7 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row7_col7" class="data row7 col7" >Act360</td>
      <td id="T_70e36_row7_col8" class="data row7 col8" >Lin</td>
      <td id="T_70e36_row7_col9" class="data row7 col9" >5.2955%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_70e36_row8_col0" class="data row8 col0" >USOSFRF BGN Curncy</td>
      <td id="T_70e36_row8_col1" class="data row8 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row8_col2" class="data row8 col2" >6M</td>
      <td id="T_70e36_row8_col3" class="data row8 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row8_col4" class="data row8 col4" >2Y</td>
      <td id="T_70e36_row8_col5" class="data row8 col5" >2</td>
      <td id="T_70e36_row8_col6" class="data row8 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row8_col7" class="data row8 col7" >Act360</td>
      <td id="T_70e36_row8_col8" class="data row8 col8" >Lin</td>
      <td id="T_70e36_row8_col9" class="data row8 col9" >5.2714%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_70e36_row9_col0" class="data row9 col0" >USOSFRG BGN Curncy</td>
      <td id="T_70e36_row9_col1" class="data row9 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row9_col2" class="data row9 col2" >7M</td>
      <td id="T_70e36_row9_col3" class="data row9 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row9_col4" class="data row9 col4" >2Y</td>
      <td id="T_70e36_row9_col5" class="data row9 col5" >2</td>
      <td id="T_70e36_row9_col6" class="data row9 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row9_col7" class="data row9 col7" >Act360</td>
      <td id="T_70e36_row9_col8" class="data row9 col8" >Lin</td>
      <td id="T_70e36_row9_col9" class="data row9 col9" >5.2366%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row10" class="row_heading level0 row10" >10</th>
      <td id="T_70e36_row10_col0" class="data row10 col0" >USOSFRH BGN Curncy</td>
      <td id="T_70e36_row10_col1" class="data row10 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row10_col2" class="data row10 col2" >8M</td>
      <td id="T_70e36_row10_col3" class="data row10 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row10_col4" class="data row10 col4" >2Y</td>
      <td id="T_70e36_row10_col5" class="data row10 col5" >2</td>
      <td id="T_70e36_row10_col6" class="data row10 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row10_col7" class="data row10 col7" >Act360</td>
      <td id="T_70e36_row10_col8" class="data row10 col8" >Lin</td>
      <td id="T_70e36_row10_col9" class="data row10 col9" >5.1986%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row11" class="row_heading level0 row11" >11</th>
      <td id="T_70e36_row11_col0" class="data row11 col0" >USOSFRI BGN Curncy</td>
      <td id="T_70e36_row11_col1" class="data row11 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row11_col2" class="data row11 col2" >9M</td>
      <td id="T_70e36_row11_col3" class="data row11 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row11_col4" class="data row11 col4" >2Y</td>
      <td id="T_70e36_row11_col5" class="data row11 col5" >2</td>
      <td id="T_70e36_row11_col6" class="data row11 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row11_col7" class="data row11 col7" >Act360</td>
      <td id="T_70e36_row11_col8" class="data row11 col8" >Lin</td>
      <td id="T_70e36_row11_col9" class="data row11 col9" >5.1667%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row12" class="row_heading level0 row12" >12</th>
      <td id="T_70e36_row12_col0" class="data row12 col0" >USOSFRK BGN Curncy</td>
      <td id="T_70e36_row12_col1" class="data row12 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row12_col2" class="data row12 col2" >11M</td>
      <td id="T_70e36_row12_col3" class="data row12 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row12_col4" class="data row12 col4" >2Y</td>
      <td id="T_70e36_row12_col5" class="data row12 col5" >2</td>
      <td id="T_70e36_row12_col6" class="data row12 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row12_col7" class="data row12 col7" >Act360</td>
      <td id="T_70e36_row12_col8" class="data row12 col8" >Lin</td>
      <td id="T_70e36_row12_col9" class="data row12 col9" >5.0841%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row13" class="row_heading level0 row13" >13</th>
      <td id="T_70e36_row13_col0" class="data row13 col0" >USOSFR1 BGN Curncy</td>
      <td id="T_70e36_row13_col1" class="data row13 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row13_col2" class="data row13 col2" >12M</td>
      <td id="T_70e36_row13_col3" class="data row13 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row13_col4" class="data row13 col4" >2Y</td>
      <td id="T_70e36_row13_col5" class="data row13 col5" >2</td>
      <td id="T_70e36_row13_col6" class="data row13 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row13_col7" class="data row13 col7" >Act360</td>
      <td id="T_70e36_row13_col8" class="data row13 col8" >Lin</td>
      <td id="T_70e36_row13_col9" class="data row13 col9" >5.0477%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row14" class="row_heading level0 row14" >14</th>
      <td id="T_70e36_row14_col0" class="data row14 col0" >USOSFR1F BGN Curncy</td>
      <td id="T_70e36_row14_col1" class="data row14 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row14_col2" class="data row14 col2" >18M</td>
      <td id="T_70e36_row14_col3" class="data row14 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row14_col4" class="data row14 col4" >1Y</td>
      <td id="T_70e36_row14_col5" class="data row14 col5" >2</td>
      <td id="T_70e36_row14_col6" class="data row14 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row14_col7" class="data row14 col7" >Act360</td>
      <td id="T_70e36_row14_col8" class="data row14 col8" >Lin</td>
      <td id="T_70e36_row14_col9" class="data row14 col9" >4.7545%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row15" class="row_heading level0 row15" >15</th>
      <td id="T_70e36_row15_col0" class="data row15 col0" >USOSFR2 BGN Curncy</td>
      <td id="T_70e36_row15_col1" class="data row15 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row15_col2" class="data row15 col2" >2Y</td>
      <td id="T_70e36_row15_col3" class="data row15 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row15_col4" class="data row15 col4" >1Y</td>
      <td id="T_70e36_row15_col5" class="data row15 col5" >2</td>
      <td id="T_70e36_row15_col6" class="data row15 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row15_col7" class="data row15 col7" >Act360</td>
      <td id="T_70e36_row15_col8" class="data row15 col8" >Lin</td>
      <td id="T_70e36_row15_col9" class="data row15 col9" >4.5629%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row16" class="row_heading level0 row16" >16</th>
      <td id="T_70e36_row16_col0" class="data row16 col0" >USOSFR3 BGN Curncy</td>
      <td id="T_70e36_row16_col1" class="data row16 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row16_col2" class="data row16 col2" >3Y</td>
      <td id="T_70e36_row16_col3" class="data row16 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row16_col4" class="data row16 col4" >1Y</td>
      <td id="T_70e36_row16_col5" class="data row16 col5" >2</td>
      <td id="T_70e36_row16_col6" class="data row16 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row16_col7" class="data row16 col7" >Act360</td>
      <td id="T_70e36_row16_col8" class="data row16 col8" >Lin</td>
      <td id="T_70e36_row16_col9" class="data row16 col9" >4.2799%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row17" class="row_heading level0 row17" >17</th>
      <td id="T_70e36_row17_col0" class="data row17 col0" >USOSFR4 BGN Curncy</td>
      <td id="T_70e36_row17_col1" class="data row17 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row17_col2" class="data row17 col2" >4Y</td>
      <td id="T_70e36_row17_col3" class="data row17 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row17_col4" class="data row17 col4" >1Y</td>
      <td id="T_70e36_row17_col5" class="data row17 col5" >2</td>
      <td id="T_70e36_row17_col6" class="data row17 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row17_col7" class="data row17 col7" >Act360</td>
      <td id="T_70e36_row17_col8" class="data row17 col8" >Lin</td>
      <td id="T_70e36_row17_col9" class="data row17 col9" >4.1110%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row18" class="row_heading level0 row18" >18</th>
      <td id="T_70e36_row18_col0" class="data row18 col0" >USOSFR5 BGN Curncy</td>
      <td id="T_70e36_row18_col1" class="data row18 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row18_col2" class="data row18 col2" >5Y</td>
      <td id="T_70e36_row18_col3" class="data row18 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row18_col4" class="data row18 col4" >1Y</td>
      <td id="T_70e36_row18_col5" class="data row18 col5" >2</td>
      <td id="T_70e36_row18_col6" class="data row18 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row18_col7" class="data row18 col7" >Act360</td>
      <td id="T_70e36_row18_col8" class="data row18 col8" >Lin</td>
      <td id="T_70e36_row18_col9" class="data row18 col9" >4.0095%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row19" class="row_heading level0 row19" >19</th>
      <td id="T_70e36_row19_col0" class="data row19 col0" >USOSFR6 BGN Curncy</td>
      <td id="T_70e36_row19_col1" class="data row19 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row19_col2" class="data row19 col2" >6Y</td>
      <td id="T_70e36_row19_col3" class="data row19 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row19_col4" class="data row19 col4" >1Y</td>
      <td id="T_70e36_row19_col5" class="data row19 col5" >2</td>
      <td id="T_70e36_row19_col6" class="data row19 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row19_col7" class="data row19 col7" >Act360</td>
      <td id="T_70e36_row19_col8" class="data row19 col8" >Lin</td>
      <td id="T_70e36_row19_col9" class="data row19 col9" >3.9498%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row20" class="row_heading level0 row20" >20</th>
      <td id="T_70e36_row20_col0" class="data row20 col0" >USOSFR7 BGN Curncy</td>
      <td id="T_70e36_row20_col1" class="data row20 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row20_col2" class="data row20 col2" >7Y</td>
      <td id="T_70e36_row20_col3" class="data row20 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row20_col4" class="data row20 col4" >1Y</td>
      <td id="T_70e36_row20_col5" class="data row20 col5" >2</td>
      <td id="T_70e36_row20_col6" class="data row20 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row20_col7" class="data row20 col7" >Act360</td>
      <td id="T_70e36_row20_col8" class="data row20 col8" >Lin</td>
      <td id="T_70e36_row20_col9" class="data row20 col9" >3.9114%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row21" class="row_heading level0 row21" >21</th>
      <td id="T_70e36_row21_col0" class="data row21 col0" >USOSFR8 BGN Curncy</td>
      <td id="T_70e36_row21_col1" class="data row21 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row21_col2" class="data row21 col2" >8Y</td>
      <td id="T_70e36_row21_col3" class="data row21 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row21_col4" class="data row21 col4" >1Y</td>
      <td id="T_70e36_row21_col5" class="data row21 col5" >2</td>
      <td id="T_70e36_row21_col6" class="data row21 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row21_col7" class="data row21 col7" >Act360</td>
      <td id="T_70e36_row21_col8" class="data row21 col8" >Lin</td>
      <td id="T_70e36_row21_col9" class="data row21 col9" >3.8869%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row22" class="row_heading level0 row22" >22</th>
      <td id="T_70e36_row22_col0" class="data row22 col0" >USOSFR9 BGN Curncy</td>
      <td id="T_70e36_row22_col1" class="data row22 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row22_col2" class="data row22 col2" >9Y</td>
      <td id="T_70e36_row22_col3" class="data row22 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row22_col4" class="data row22 col4" >1Y</td>
      <td id="T_70e36_row22_col5" class="data row22 col5" >2</td>
      <td id="T_70e36_row22_col6" class="data row22 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row22_col7" class="data row22 col7" >Act360</td>
      <td id="T_70e36_row22_col8" class="data row22 col8" >Lin</td>
      <td id="T_70e36_row22_col9" class="data row22 col9" >3.8721%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row23" class="row_heading level0 row23" >23</th>
      <td id="T_70e36_row23_col0" class="data row23 col0" >USOSFR10 BGN Curncy</td>
      <td id="T_70e36_row23_col1" class="data row23 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row23_col2" class="data row23 col2" >10Y</td>
      <td id="T_70e36_row23_col3" class="data row23 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row23_col4" class="data row23 col4" >1Y</td>
      <td id="T_70e36_row23_col5" class="data row23 col5" >2</td>
      <td id="T_70e36_row23_col6" class="data row23 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row23_col7" class="data row23 col7" >Act360</td>
      <td id="T_70e36_row23_col8" class="data row23 col8" >Lin</td>
      <td id="T_70e36_row23_col9" class="data row23 col9" >3.8639%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row24" class="row_heading level0 row24" >24</th>
      <td id="T_70e36_row24_col0" class="data row24 col0" >USOSFR12 BGN Curncy</td>
      <td id="T_70e36_row24_col1" class="data row24 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row24_col2" class="data row24 col2" >12Y</td>
      <td id="T_70e36_row24_col3" class="data row24 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row24_col4" class="data row24 col4" >1Y</td>
      <td id="T_70e36_row24_col5" class="data row24 col5" >2</td>
      <td id="T_70e36_row24_col6" class="data row24 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row24_col7" class="data row24 col7" >Act360</td>
      <td id="T_70e36_row24_col8" class="data row24 col8" >Lin</td>
      <td id="T_70e36_row24_col9" class="data row24 col9" >3.8604%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row25" class="row_heading level0 row25" >25</th>
      <td id="T_70e36_row25_col0" class="data row25 col0" >USOSFR15 BGN Curncy</td>
      <td id="T_70e36_row25_col1" class="data row25 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row25_col2" class="data row25 col2" >15Y</td>
      <td id="T_70e36_row25_col3" class="data row25 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row25_col4" class="data row25 col4" >1Y</td>
      <td id="T_70e36_row25_col5" class="data row25 col5" >2</td>
      <td id="T_70e36_row25_col6" class="data row25 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row25_col7" class="data row25 col7" >Act360</td>
      <td id="T_70e36_row25_col8" class="data row25 col8" >Lin</td>
      <td id="T_70e36_row25_col9" class="data row25 col9" >3.8615%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row26" class="row_heading level0 row26" >26</th>
      <td id="T_70e36_row26_col0" class="data row26 col0" >USOSFR20 BGN Curncy</td>
      <td id="T_70e36_row26_col1" class="data row26 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row26_col2" class="data row26 col2" >20Y</td>
      <td id="T_70e36_row26_col3" class="data row26 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row26_col4" class="data row26 col4" >1Y</td>
      <td id="T_70e36_row26_col5" class="data row26 col5" >2</td>
      <td id="T_70e36_row26_col6" class="data row26 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row26_col7" class="data row26 col7" >Act360</td>
      <td id="T_70e36_row26_col8" class="data row26 col8" >Lin</td>
      <td id="T_70e36_row26_col9" class="data row26 col9" >3.8278%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row27" class="row_heading level0 row27" >27</th>
      <td id="T_70e36_row27_col0" class="data row27 col0" >USOSFR25 BGN Curncy</td>
      <td id="T_70e36_row27_col1" class="data row27 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row27_col2" class="data row27 col2" >25Y</td>
      <td id="T_70e36_row27_col3" class="data row27 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row27_col4" class="data row27 col4" >1Y</td>
      <td id="T_70e36_row27_col5" class="data row27 col5" >2</td>
      <td id="T_70e36_row27_col6" class="data row27 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row27_col7" class="data row27 col7" >Act360</td>
      <td id="T_70e36_row27_col8" class="data row27 col8" >Lin</td>
      <td id="T_70e36_row27_col9" class="data row27 col9" >3.7356%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row28" class="row_heading level0 row28" >28</th>
      <td id="T_70e36_row28_col0" class="data row28 col0" >USOSFR30 BGN Curncy</td>
      <td id="T_70e36_row28_col1" class="data row28 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row28_col2" class="data row28 col2" >30Y</td>
      <td id="T_70e36_row28_col3" class="data row28 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row28_col4" class="data row28 col4" >1Y</td>
      <td id="T_70e36_row28_col5" class="data row28 col5" >2</td>
      <td id="T_70e36_row28_col6" class="data row28 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row28_col7" class="data row28 col7" >Act360</td>
      <td id="T_70e36_row28_col8" class="data row28 col8" >Lin</td>
      <td id="T_70e36_row28_col9" class="data row28 col9" >3.6388%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row29" class="row_heading level0 row29" >29</th>
      <td id="T_70e36_row29_col0" class="data row29 col0" >USOSFR40 BGN Curncy</td>
      <td id="T_70e36_row29_col1" class="data row29 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row29_col2" class="data row29 col2" >40Y</td>
      <td id="T_70e36_row29_col3" class="data row29 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row29_col4" class="data row29 col4" >1Y</td>
      <td id="T_70e36_row29_col5" class="data row29 col5" >2</td>
      <td id="T_70e36_row29_col6" class="data row29 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row29_col7" class="data row29 col7" >Act360</td>
      <td id="T_70e36_row29_col8" class="data row29 col8" >Lin</td>
      <td id="T_70e36_row29_col9" class="data row29 col9" >3.4272%</td>
    </tr>
    <tr>
      <th id="T_70e36_level0_row30" class="row_heading level0 row30" >30</th>
      <td id="T_70e36_row30_col0" class="data row30 col0" >USOSFR50 BGN Curncy</td>
      <td id="T_70e36_row30_col1" class="data row30 col1" >2024-06-25 00:00:00</td>
      <td id="T_70e36_row30_col2" class="data row30 col2" >50Y</td>
      <td id="T_70e36_row30_col3" class="data row30 col3" >SHORT_FRONT</td>
      <td id="T_70e36_row30_col4" class="data row30 col4" >1Y</td>
      <td id="T_70e36_row30_col5" class="data row30 col5" >2</td>
      <td id="T_70e36_row30_col6" class="data row30 col6" >MOD_FOLLOW</td>
      <td id="T_70e36_row30_col7" class="data row30 col7" >Act360</td>
      <td id="T_70e36_row30_col8" class="data row30 col8" >Lin</td>
      <td id="T_70e36_row30_col9" class="data row30 col9" >3.2120%</td>
    </tr>
  </tbody>
</table>




## Input

Se definen los inputs que son comunes a todas las operaciones. Notar que, contrariamente a lo que indican los datos, se establece que el settlement lag sea igual a 0. Esto para poder aplicar la condición que iguala el valor prersente de la pata fija en `start_date` al nocional.


```python
# Debe coincidir con la fecha de los datos
trade_date = qcf.QCDate(21, 6, 2024)
```


```python
# Convención de las tasas de las patas fijas
yf = qcf.QCAct360()
wf = qcf.QCLinearWf()
```


```python
# Los parámetros se organizan en un dict.
common_params = {
    "rec_pay": qcf.RecPay.RECEIVE,
    "start_date": qcf.QCDate(25, 6, 2024),
    "bus_adj_rule": qcf.BusyAdjRules.MODFOLLOW,
    "settlement_stub_period": qcf.StubPeriod.SHORTFRONT,
    "settlement_calendar": qcf.BusinessCalendar(trade_date, 50),
    "settlement_lag": 0,  # Se impone = 0
    "initial_notional": 1_000_000,
    "amort_is_cashflow": True,
    "notional_currency": qcf.QCUSD(),
    "is_bond": False,
    "sett_lag_behaviour": qcf.SettLagBehaviour.DONT_MOVE,
}
```

La siguiente celda es para facilitar la escritura del código que viene ya que nos recuerda cuáles son los argumentos de la función que construye patas fijas.


```python
for p in qcf.LegFactory.build_bullet_fixed_rate_leg.__doc__.split(','):
    print(p)
```

    build_bullet_fixed_rate_leg(rec_pay: qcfinancial.RecPay
     start_date: qcfinancial.QCDate
     end_date: qcfinancial.QCDate
     bus_adj_rule: qcfinancial.BusyAdjRules
     settlement_periodicity: qcfinancial.Tenor
     settlement_stub_period: qcfinancial.StubPeriod
     settlement_calendar: qcfinancial.BusinessCalendar
     settlement_lag: typing.SupportsInt
     initial_notional: typing.SupportsFloat
     amort_is_cashflow: bool
     interest_rate: qcfinancial.QCInterestRate
     notional_currency: qcfinancial.QCCurrency
     is_bond: bool
     sett_lag_behaviour: qcfinancial.SettLagBehaviour = <SettLagBehaviour.DONT_MOVE: 1>) -> qcfinancial.Leg
    
    Builds a Leg containing only cashflows of type FixedRateCashflow. Amortization is BULLET
    


En el siguiente loop, se construyen todas las patas fijas.


```python
# Aquí se almacenarán los resultados
fixed_rate_legs = []

# Se recorre el DataFrame con la data
for t in data.itertuples():
    # Madurez del contrato
    tenor = qcf.Tenor(t.tenor)
    
    # Se calcula el número de meses de la madurez
    months = tenor.get_months() + 12 * tenor.get_years()

    # Se calcula la fecha final del swap sin aplicar todavía ajustes de calendario
    if (days:=tenor.get_days()) > 0:
        end_date = common_params["start_date"].add_days(days)
    else:
        end_date = common_params["start_date"].add_months(months)

    # Se define un dict con los parámetros propios de cada contrato
    other_params = {
        "end_date": end_date,
        "settlement_periodicity": qcf.Tenor(t.pay_freq),
        "interest_rate": qcf.QCInterestRate(t.rate, yf, wf),
    }

    # Se construye y almacena la pata fija correspondiente
    fixed_rate_legs.append(
        qcf.LegFactory.build_bullet_fixed_rate_leg(
            **(common_params | other_params),
        )
    )
```

Se muestra la estructura de un par de patas fijas.


```python
aux.leg_as_dataframe(fixed_rate_legs[0]).style.format(aux.format_dict)
```




<style type="text/css">
</style>
<table id="T_760d4">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_760d4_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_760d4_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_760d4_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_760d4_level0_col3" class="col_heading level0 col3" >nocional</th>
      <th id="T_760d4_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_760d4_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_760d4_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_760d4_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_760d4_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_760d4_level0_col9" class="col_heading level0 col9" >valor_tasa</th>
      <th id="T_760d4_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_760d4_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_760d4_row0_col0" class="data row0 col0" >2024-06-25</td>
      <td id="T_760d4_row0_col1" class="data row0 col1" >2024-07-02</td>
      <td id="T_760d4_row0_col2" class="data row0 col2" >2024-07-02</td>
      <td id="T_760d4_row0_col3" class="data row0 col3" >1,000,000.00</td>
      <td id="T_760d4_row0_col4" class="data row0 col4" >1,000,000.00</td>
      <td id="T_760d4_row0_col5" class="data row0 col5" >1,037.21</td>
      <td id="T_760d4_row0_col6" class="data row0 col6" >True</td>
      <td id="T_760d4_row0_col7" class="data row0 col7" >1,001,037.21</td>
      <td id="T_760d4_row0_col8" class="data row0 col8" >USD</td>
      <td id="T_760d4_row0_col9" class="data row0 col9" >5.3342%</td>
      <td id="T_760d4_row0_col10" class="data row0 col10" >LinAct360</td>
    </tr>
  </tbody>
</table>





```python
aux.leg_as_dataframe(fixed_rate_legs[14]).style.format(aux.format_dict)
```




<style type="text/css">
</style>
<table id="T_f1290">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_f1290_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_f1290_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_f1290_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_f1290_level0_col3" class="col_heading level0 col3" >nocional</th>
      <th id="T_f1290_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_f1290_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_f1290_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_f1290_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_f1290_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_f1290_level0_col9" class="col_heading level0 col9" >valor_tasa</th>
      <th id="T_f1290_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_f1290_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_f1290_row0_col0" class="data row0 col0" >2024-06-25</td>
      <td id="T_f1290_row0_col1" class="data row0 col1" >2024-12-25</td>
      <td id="T_f1290_row0_col2" class="data row0 col2" >2024-12-25</td>
      <td id="T_f1290_row0_col3" class="data row0 col3" >1,000,000.00</td>
      <td id="T_f1290_row0_col4" class="data row0 col4" >0.00</td>
      <td id="T_f1290_row0_col5" class="data row0 col5" >24,168.71</td>
      <td id="T_f1290_row0_col6" class="data row0 col6" >True</td>
      <td id="T_f1290_row0_col7" class="data row0 col7" >24,168.71</td>
      <td id="T_f1290_row0_col8" class="data row0 col8" >USD</td>
      <td id="T_f1290_row0_col9" class="data row0 col9" >4.7545%</td>
      <td id="T_f1290_row0_col10" class="data row0 col10" >LinAct360</td>
    </tr>
    <tr>
      <th id="T_f1290_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_f1290_row1_col0" class="data row1 col0" >2024-12-25</td>
      <td id="T_f1290_row1_col1" class="data row1 col1" >2025-12-25</td>
      <td id="T_f1290_row1_col2" class="data row1 col2" >2025-12-25</td>
      <td id="T_f1290_row1_col3" class="data row1 col3" >1,000,000.00</td>
      <td id="T_f1290_row1_col4" class="data row1 col4" >1,000,000.00</td>
      <td id="T_f1290_row1_col5" class="data row1 col5" >48,205.35</td>
      <td id="T_f1290_row1_col6" class="data row1 col6" >True</td>
      <td id="T_f1290_row1_col7" class="data row1 col7" >1,048,205.35</td>
      <td id="T_f1290_row1_col8" class="data row1 col8" >USD</td>
      <td id="T_f1290_row1_col9" class="data row1 col9" >4.7545%</td>
      <td id="T_f1290_row1_col10" class="data row1 col10" >LinAct360</td>
    </tr>
  </tbody>
</table>




## Curva Inicial

La curva cero cupón se construye usando bootstrapping y el algoritmo de Newton-Raphson. En el siguiente loop se construye la curva inicial. Newton-Raphson comenzará sus iteraciones desde cada punto de esta curva.


```python
# Se define los vectores de plazos y tasas
plazos = qcf.long_vec()
tasas = qcf.double_vec()

# Para rellenarlos se utiliza la información contenida 
# en las patas fijas.
for leg in fixed_rate_legs:
    # Número de cupones de la pata
    num_cup = leg.size()

    # Último cashflow de la pata
    cashflow = leg.get_cashflow_at(num_cup - 1)

    # Se calcula el número de días desde start_date 
    # hasta la última settlement_date
    plazo = common_params["start_date"].day_diff(cashflow.get_settlement_date())
    plazos.append(plazo)

    # Se obtiene el valor de la tasa fija
    tasa = cashflow.get_rate().get_value()
    tasas.append(tasa)

# Con la información anterior, se termina de construir la curva
curva = qcf.QCCurve(plazos, tasas)
interpolator = qcf.QCLinearInterpolator(curva)
initial_zcc = qcf.ZeroCouponCurve(
    interpolator, 
    rate:=(qcf.QCInterestRate(
        0.0, 
        qcf.QCAct365(), 
        qcf.QCContinousWf()
    ))
)
```

## Bootstrapping

Se procede ahora a aplicar el bootstrapping. Se comienza dando de alta el objeto `PresentValue` de `qcfinancial`que permite valorizar todo tipo de patas.


```python
pv = qcf.PresentValue()
```

El siguiente loop ejecuta el bootstrapping.


```python
# Se resuelve la ecuación:
# VP(pata_fija(i), z1,...,z(i),...,zN) - nocional = 0, para todo i
for i, leg in enumerate(fixed_rate_legs):
    
    # Se define la función objetivo
    def obj(zcc):
        # VP - nocional
        return pv.pv(common_params["start_date"], leg, zcc) - common_params["initial_notional"]
    
    # Aquí comienza la resolución
    error = 1_000
    epsilon = .00001
    x = initial_zcc.get_rate_at(i)  # Valor inicial para Newton-Raphson
    new_zcc = initial_zcc  # En new_zcc se almacena el resultado
    
    # Se aplica Newton-Raphson
    while error > epsilon:
        x = x - obj(new_zcc) / pv.get_derivatives()[i]  # La derivada del VP se calcula al momento de valorizar 
        tasas[i] = x
        # Se reconstruye la curva con el valor de la iteración
        curva = qcf.QCCurve(plazos, tasas)
        interpolator = qcf.QCLinearInterpolator(curva)
        new_zcc = qcf.ZeroCouponCurve(
            interpolator, 
            rate,
        )
        # Se calcula el nuevo error
        error = abs(obj(new_zcc))
```

Una vez ejecutado el bootstrapping, verificamos que, para cada pata, se cumple la condición deseada.


```python
check = []
for i, leg in enumerate(fixed_rate_legs):
    check.append({
        "leg_number": i, 
        "present_value": pv.pv(common_params['start_date'], leg, new_zcc),
    })
df_check = pd.DataFrame(check)
df_check.style.format({"present_value": "{:,.4f}"})
```




<style type="text/css">
</style>
<table id="T_42e1a">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_42e1a_level0_col0" class="col_heading level0 col0" >leg_number</th>
      <th id="T_42e1a_level0_col1" class="col_heading level0 col1" >present_value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_42e1a_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_42e1a_row0_col0" class="data row0 col0" >0</td>
      <td id="T_42e1a_row0_col1" class="data row0 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_42e1a_row1_col0" class="data row1 col0" >1</td>
      <td id="T_42e1a_row1_col1" class="data row1 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_42e1a_row2_col0" class="data row2 col0" >2</td>
      <td id="T_42e1a_row2_col1" class="data row2 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_42e1a_row3_col0" class="data row3 col0" >3</td>
      <td id="T_42e1a_row3_col1" class="data row3 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_42e1a_row4_col0" class="data row4 col0" >4</td>
      <td id="T_42e1a_row4_col1" class="data row4 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_42e1a_row5_col0" class="data row5 col0" >5</td>
      <td id="T_42e1a_row5_col1" class="data row5 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_42e1a_row6_col0" class="data row6 col0" >6</td>
      <td id="T_42e1a_row6_col1" class="data row6 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_42e1a_row7_col0" class="data row7 col0" >7</td>
      <td id="T_42e1a_row7_col1" class="data row7 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_42e1a_row8_col0" class="data row8 col0" >8</td>
      <td id="T_42e1a_row8_col1" class="data row8 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_42e1a_row9_col0" class="data row9 col0" >9</td>
      <td id="T_42e1a_row9_col1" class="data row9 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row10" class="row_heading level0 row10" >10</th>
      <td id="T_42e1a_row10_col0" class="data row10 col0" >10</td>
      <td id="T_42e1a_row10_col1" class="data row10 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row11" class="row_heading level0 row11" >11</th>
      <td id="T_42e1a_row11_col0" class="data row11 col0" >11</td>
      <td id="T_42e1a_row11_col1" class="data row11 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row12" class="row_heading level0 row12" >12</th>
      <td id="T_42e1a_row12_col0" class="data row12 col0" >12</td>
      <td id="T_42e1a_row12_col1" class="data row12 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row13" class="row_heading level0 row13" >13</th>
      <td id="T_42e1a_row13_col0" class="data row13 col0" >13</td>
      <td id="T_42e1a_row13_col1" class="data row13 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row14" class="row_heading level0 row14" >14</th>
      <td id="T_42e1a_row14_col0" class="data row14 col0" >14</td>
      <td id="T_42e1a_row14_col1" class="data row14 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row15" class="row_heading level0 row15" >15</th>
      <td id="T_42e1a_row15_col0" class="data row15 col0" >15</td>
      <td id="T_42e1a_row15_col1" class="data row15 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row16" class="row_heading level0 row16" >16</th>
      <td id="T_42e1a_row16_col0" class="data row16 col0" >16</td>
      <td id="T_42e1a_row16_col1" class="data row16 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row17" class="row_heading level0 row17" >17</th>
      <td id="T_42e1a_row17_col0" class="data row17 col0" >17</td>
      <td id="T_42e1a_row17_col1" class="data row17 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row18" class="row_heading level0 row18" >18</th>
      <td id="T_42e1a_row18_col0" class="data row18 col0" >18</td>
      <td id="T_42e1a_row18_col1" class="data row18 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row19" class="row_heading level0 row19" >19</th>
      <td id="T_42e1a_row19_col0" class="data row19 col0" >19</td>
      <td id="T_42e1a_row19_col1" class="data row19 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row20" class="row_heading level0 row20" >20</th>
      <td id="T_42e1a_row20_col0" class="data row20 col0" >20</td>
      <td id="T_42e1a_row20_col1" class="data row20 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row21" class="row_heading level0 row21" >21</th>
      <td id="T_42e1a_row21_col0" class="data row21 col0" >21</td>
      <td id="T_42e1a_row21_col1" class="data row21 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row22" class="row_heading level0 row22" >22</th>
      <td id="T_42e1a_row22_col0" class="data row22 col0" >22</td>
      <td id="T_42e1a_row22_col1" class="data row22 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row23" class="row_heading level0 row23" >23</th>
      <td id="T_42e1a_row23_col0" class="data row23 col0" >23</td>
      <td id="T_42e1a_row23_col1" class="data row23 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row24" class="row_heading level0 row24" >24</th>
      <td id="T_42e1a_row24_col0" class="data row24 col0" >24</td>
      <td id="T_42e1a_row24_col1" class="data row24 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row25" class="row_heading level0 row25" >25</th>
      <td id="T_42e1a_row25_col0" class="data row25 col0" >25</td>
      <td id="T_42e1a_row25_col1" class="data row25 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row26" class="row_heading level0 row26" >26</th>
      <td id="T_42e1a_row26_col0" class="data row26 col0" >26</td>
      <td id="T_42e1a_row26_col1" class="data row26 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row27" class="row_heading level0 row27" >27</th>
      <td id="T_42e1a_row27_col0" class="data row27 col0" >27</td>
      <td id="T_42e1a_row27_col1" class="data row27 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row28" class="row_heading level0 row28" >28</th>
      <td id="T_42e1a_row28_col0" class="data row28 col0" >28</td>
      <td id="T_42e1a_row28_col1" class="data row28 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row29" class="row_heading level0 row29" >29</th>
      <td id="T_42e1a_row29_col0" class="data row29 col0" >29</td>
      <td id="T_42e1a_row29_col1" class="data row29 col1" >1,000,000.0000</td>
    </tr>
    <tr>
      <th id="T_42e1a_level0_row30" class="row_heading level0 row30" >30</th>
      <td id="T_42e1a_row30_col0" class="data row30 col0" >30</td>
      <td id="T_42e1a_row30_col1" class="data row30 col1" >1,000,000.0000</td>
    </tr>
  </tbody>
</table>




Finalmente, se despliega los valores de la curva obtenida.


```python
df_curva = pd.concat([pd.DataFrame(plazos), pd.DataFrame(tasas)], axis=1)
df_curva.columns = ['plazo', 'tasa']
df_curva.style.format({'tasa':'{:.4%}'})
```




<style type="text/css">
</style>
<table id="T_f325c">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_f325c_level0_col0" class="col_heading level0 col0" >plazo</th>
      <th id="T_f325c_level0_col1" class="col_heading level0 col1" >tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_f325c_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_f325c_row0_col0" class="data row0 col0" >7</td>
      <td id="T_f325c_row0_col1" class="data row0 col1" >5.4055%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row1" class="row_heading level0 row1" >1</th>
      <td id="T_f325c_row1_col0" class="data row1 col0" >14</td>
      <td id="T_f325c_row1_col1" class="data row1 col1" >5.4060%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row2" class="row_heading level0 row2" >2</th>
      <td id="T_f325c_row2_col0" class="data row2 col0" >21</td>
      <td id="T_f325c_row2_col1" class="data row2 col1" >5.4073%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row3" class="row_heading level0 row3" >3</th>
      <td id="T_f325c_row3_col0" class="data row3 col0" >30</td>
      <td id="T_f325c_row3_col1" class="data row3 col1" >5.4064%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row4" class="row_heading level0 row4" >4</th>
      <td id="T_f325c_row4_col0" class="data row4 col0" >62</td>
      <td id="T_f325c_row4_col1" class="data row4 col1" >5.3948%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row5" class="row_heading level0 row5" >5</th>
      <td id="T_f325c_row5_col0" class="data row5 col0" >92</td>
      <td id="T_f325c_row5_col1" class="data row5 col1" >5.3802%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row6" class="row_heading level0 row6" >6</th>
      <td id="T_f325c_row6_col0" class="data row6 col0" >122</td>
      <td id="T_f325c_row6_col1" class="data row6 col1" >5.3430%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row7" class="row_heading level0 row7" >7</th>
      <td id="T_f325c_row7_col0" class="data row7 col0" >153</td>
      <td id="T_f325c_row7_col1" class="data row7 col1" >5.3095%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row8" class="row_heading level0 row8" >8</th>
      <td id="T_f325c_row8_col0" class="data row8 col0" >183</td>
      <td id="T_f325c_row8_col1" class="data row8 col1" >5.2743%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row9" class="row_heading level0 row9" >9</th>
      <td id="T_f325c_row9_col0" class="data row9 col0" >216</td>
      <td id="T_f325c_row9_col1" class="data row9 col1" >5.2276%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row10" class="row_heading level0 row10" >10</th>
      <td id="T_f325c_row10_col0" class="data row10 col0" >245</td>
      <td id="T_f325c_row10_col1" class="data row10 col1" >5.1797%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row11" class="row_heading level0 row11" >11</th>
      <td id="T_f325c_row11_col0" class="data row11 col0" >273</td>
      <td id="T_f325c_row11_col1" class="data row11 col1" >5.1384%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row12" class="row_heading level0 row12" >12</th>
      <td id="T_f325c_row12_col0" class="data row12 col0" >335</td>
      <td id="T_f325c_row12_col1" class="data row12 col1" >5.0365%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row13" class="row_heading level0 row13" >13</th>
      <td id="T_f325c_row13_col0" class="data row13 col0" >365</td>
      <td id="T_f325c_row13_col1" class="data row13 col1" >4.9912%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row14" class="row_heading level0 row14" >14</th>
      <td id="T_f325c_row14_col0" class="data row14 col0" >548</td>
      <td id="T_f325c_row14_col1" class="data row14 col1" >4.7223%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row15" class="row_heading level0 row15" >15</th>
      <td id="T_f325c_row15_col0" class="data row15 col0" >730</td>
      <td id="T_f325c_row15_col1" class="data row15 col1" >4.5116%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row16" class="row_heading level0 row16" >16</th>
      <td id="T_f325c_row16_col0" class="data row16 col0" >1095</td>
      <td id="T_f325c_row16_col1" class="data row16 col1" >4.2290%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row17" class="row_heading level0 row17" >17</th>
      <td id="T_f325c_row17_col0" class="data row17 col0" >1462</td>
      <td id="T_f325c_row17_col1" class="data row17 col1" >4.0595%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row18" class="row_heading level0 row18" >18</th>
      <td id="T_f325c_row18_col0" class="data row18 col0" >1826</td>
      <td id="T_f325c_row18_col1" class="data row18 col1" >3.9577%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row19" class="row_heading level0 row19" >19</th>
      <td id="T_f325c_row19_col0" class="data row19 col0" >2191</td>
      <td id="T_f325c_row19_col1" class="data row19 col1" >3.8983%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row20" class="row_heading level0 row20" >20</th>
      <td id="T_f325c_row20_col0" class="data row20 col0" >2556</td>
      <td id="T_f325c_row20_col1" class="data row20 col1" >3.8604%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row21" class="row_heading level0 row21" >21</th>
      <td id="T_f325c_row21_col0" class="data row21 col0" >2922</td>
      <td id="T_f325c_row21_col1" class="data row21 col1" >3.8367%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row22" class="row_heading level0 row22" >22</th>
      <td id="T_f325c_row22_col0" class="data row22 col0" >3289</td>
      <td id="T_f325c_row22_col1" class="data row22 col1" >3.8231%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row23" class="row_heading level0 row23" >23</th>
      <td id="T_f325c_row23_col0" class="data row23 col0" >3653</td>
      <td id="T_f325c_row23_col1" class="data row23 col1" >3.8163%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row24" class="row_heading level0 row24" >24</th>
      <td id="T_f325c_row24_col0" class="data row24 col0" >4383</td>
      <td id="T_f325c_row24_col1" class="data row24 col1" >3.8166%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row25" class="row_heading level0 row25" >25</th>
      <td id="T_f325c_row25_col0" class="data row25 col0" >5480</td>
      <td id="T_f325c_row25_col1" class="data row25 col1" >3.8225%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row26" class="row_heading level0 row26" >26</th>
      <td id="T_f325c_row26_col0" class="data row26 col0" >7307</td>
      <td id="T_f325c_row26_col1" class="data row26 col1" >3.7822%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row27" class="row_heading level0 row27" >27</th>
      <td id="T_f325c_row27_col0" class="data row27 col0" >9131</td>
      <td id="T_f325c_row27_col1" class="data row27 col1" >3.6529%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row28" class="row_heading level0 row28" >28</th>
      <td id="T_f325c_row28_col0" class="data row28 col0" >10957</td>
      <td id="T_f325c_row28_col1" class="data row28 col1" >3.5115%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row29" class="row_heading level0 row29" >29</th>
      <td id="T_f325c_row29_col0" class="data row29 col0" >14610</td>
      <td id="T_f325c_row29_col1" class="data row29 col1" >3.1854%</td>
    </tr>
    <tr>
      <th id="T_f325c_level0_row30" class="row_heading level0 row30" >30</th>
      <td id="T_f325c_row30_col0" class="data row30 col0" >18262</td>
      <td id="T_f325c_row30_col1" class="data row30 col1" >2.8431%</td>
    </tr>
  </tbody>
</table>





```python

```
