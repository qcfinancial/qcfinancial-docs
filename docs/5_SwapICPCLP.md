# Configurar un SwapICPCLP de Mercado

Se muestra una forma posible de configurar una operación de Swap ICPCLP de mercado. Se definirán algunos parámetros por default y sólo será necesario especificar el nocional, el plazo, el valor de la tasa fija y si ésta se recibe o se paga para obtener la estructura completa.

Para ejecutar todos los ejemplos se debe importar la librería. Se sugiere utilizar siempre el alias `qcf`. 


```python
import qcfinancial as qcf
import aux_functions as aux
```

Se verifica la versión y build de `qcfinancial`.

## Parámetros por Default de la Operación

Se comienza estableciendo una fecha de trade y dando de alta un `dict` con los parámetros por default comunes y los específicos de ambas patas.


```python
trade_date = qcf.QCDate(14, 6, 2024)
```


```python
both_default_values = {
    "bus_adj_rule": qcf.BusyAdjRules.MODFOLLOW,
    "settlement_calendar": qcf.BusinessCalendar(trade_date, 20),
    "settlement_stub_period": qcf.StubPeriod.NO,
    "settlement_lag": 1,
    "amort_is_cashflow": False,
    "notional_currency": qcf.QCCLP(),
    "sett_lag_behaviour": qcf.SettLagBehaviour.DONT_MOVE
}

icpclp_default_values = {
    "fix_adj_rule": qcf.BusyAdjRules.MODFOLLOW,
    "fixing_calendar": qcf.BusinessCalendar(trade_date, 20),
    "dates_for_eq_rate": qcf.DatesForEquivalentRate.ACCRUAL,
    "interest_rate": qcf.QCInterestRate(.0, qcf.QCAct360(), qcf.QCLinearWf()),
    "eq_rate_decimal_places": 4,
}

fixed_rate_default_values = {
    "is_bond":False,  
}
```

## Pata Fija

Se da de alta los parámetros variables de la pata fija. Notar la utilización del parámetro auxiliar `maturity` que permite calcular la fecha final.


```python
str_maturity = "1Y"
maturity = qcf.Tenor(str_maturity)
meses = maturity.get_months() + 12 * maturity.get_years()
```

Se da de alta el objeto.


```python
fixed_rate_value = .03
fixed_rate_leg_other_values = {
    "settlement_periodicity": qcf.Tenor('2Y') if str_maturity in ['1M', '2M', '3M', '6M', '9M', '12M', '1Y', '18M'] else qcf.Tenor('6M'),
    "rec_pay": qcf.RecPay.RECEIVE,
    "initial_notional": 1_000_000_000.0,
    "start_date": (start_date:=qcf.QCDate(18, 6, 2024)),
    "end_date": start_date.add_months(meses),
    "interest_rate": qcf.QCInterestRate(fixed_rate_value, qcf.QCAct360(), qcf.QCLinearWf()),  
}
```


```python
fixed_rate_leg = qcf.LegFactory.build_bullet_fixed_rate_leg(
    **(both_default_values | fixed_rate_default_values | fixed_rate_leg_other_values)
)
```

Se visualiza el resultado.


```python
aux.leg_as_dataframe(fixed_rate_leg).style.format(aux.format_dict)
```




<style type="text/css">
</style>
<table id="T_951fe">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_951fe_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_951fe_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_951fe_level0_col2" class="col_heading level0 col2" >fecha_pago</th>
      <th id="T_951fe_level0_col3" class="col_heading level0 col3" >nocional</th>
      <th id="T_951fe_level0_col4" class="col_heading level0 col4" >amortizacion</th>
      <th id="T_951fe_level0_col5" class="col_heading level0 col5" >interes</th>
      <th id="T_951fe_level0_col6" class="col_heading level0 col6" >amort_es_flujo</th>
      <th id="T_951fe_level0_col7" class="col_heading level0 col7" >flujo</th>
      <th id="T_951fe_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_951fe_level0_col9" class="col_heading level0 col9" >valor_tasa</th>
      <th id="T_951fe_level0_col10" class="col_heading level0 col10" >tipo_tasa</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_951fe_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_951fe_row0_col0" class="data row0 col0" >2024-06-18</td>
      <td id="T_951fe_row0_col1" class="data row0 col1" >2025-06-18</td>
      <td id="T_951fe_row0_col2" class="data row0 col2" >2025-06-19</td>
      <td id="T_951fe_row0_col3" class="data row0 col3" >1,000,000,000.00</td>
      <td id="T_951fe_row0_col4" class="data row0 col4" >1,000,000,000.00</td>
      <td id="T_951fe_row0_col5" class="data row0 col5" >30,416,666.67</td>
      <td id="T_951fe_row0_col6" class="data row0 col6" >False</td>
      <td id="T_951fe_row0_col7" class="data row0 col7" >30,416,666.67</td>
      <td id="T_951fe_row0_col8" class="data row0 col8" >CLP</td>
      <td id="T_951fe_row0_col9" class="data row0 col9" >3.0000%</td>
      <td id="T_951fe_row0_col10" class="data row0 col10" >LinAct360</td>
    </tr>
  </tbody>
</table>




## Pata OvernightIndex

Se da de alta los parámetros variables de la pata OvernightIndex. Notar que se reutilizan algunos de los parámetros de la pata fija.


```python
rp = qcf.RecPay.RECEIVE if fixed_rate_leg_other_values['rec_pay'] == qcf.RecPay.PAY else qcf.RecPay.RECEIVE

icpclp_leg_other_values = {
    "rec_pay": rp,
    "initial_notional": fixed_rate_leg_other_values["initial_notional"],
    "start_date": fixed_rate_leg_other_values["start_date"],
    "end_date": fixed_rate_leg_other_values["end_date"],
    "settlement_periodicity": fixed_rate_leg_other_values["settlement_periodicity"],
    "interest_rate": qcf.QCInterestRate(0.0, qcf.QCAct360(), qcf.QCLinearWf()),
    "index_name": "ICPCLP",
    "spread": 0.0,
    "gearing": 1.0,
}
```

Finalmente, se da de alta el objeto.


```python
on_index_leg = qcf.LegFactory.build_bullet_overnight_index_leg(
    **(both_default_values | icpclp_default_values | icpclp_leg_other_values)
)
```

Se visualiza.


```python
aux.leg_as_dataframe(on_index_leg).style.format(aux.format_dict)
```




<style type="text/css">
</style>
<table id="T_278a8">
  <thead>
    <tr>
      <th class="blank level0" >&nbsp;</th>
      <th id="T_278a8_level0_col0" class="col_heading level0 col0" >fecha_inicial</th>
      <th id="T_278a8_level0_col1" class="col_heading level0 col1" >fecha_final</th>
      <th id="T_278a8_level0_col2" class="col_heading level0 col2" >fecha_inicial_indice</th>
      <th id="T_278a8_level0_col3" class="col_heading level0 col3" >fecha_final_indice</th>
      <th id="T_278a8_level0_col4" class="col_heading level0 col4" >fecha_pago</th>
      <th id="T_278a8_level0_col5" class="col_heading level0 col5" >nocional</th>
      <th id="T_278a8_level0_col6" class="col_heading level0 col6" >amortizacion</th>
      <th id="T_278a8_level0_col7" class="col_heading level0 col7" >amort_es_flujo</th>
      <th id="T_278a8_level0_col8" class="col_heading level0 col8" >moneda_nocional</th>
      <th id="T_278a8_level0_col9" class="col_heading level0 col9" >nombre_indice</th>
      <th id="T_278a8_level0_col10" class="col_heading level0 col10" >valor_indice_inicial</th>
      <th id="T_278a8_level0_col11" class="col_heading level0 col11" >valor_indice_final</th>
      <th id="T_278a8_level0_col12" class="col_heading level0 col12" >valor_tasa</th>
      <th id="T_278a8_level0_col13" class="col_heading level0 col13" >tipo_tasa</th>
      <th id="T_278a8_level0_col14" class="col_heading level0 col14" >interes</th>
      <th id="T_278a8_level0_col15" class="col_heading level0 col15" >flujo</th>
      <th id="T_278a8_level0_col16" class="col_heading level0 col16" >spread</th>
      <th id="T_278a8_level0_col17" class="col_heading level0 col17" >gearing</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th id="T_278a8_level0_row0" class="row_heading level0 row0" >0</th>
      <td id="T_278a8_row0_col0" class="data row0 col0" >2024-06-18</td>
      <td id="T_278a8_row0_col1" class="data row0 col1" >2025-06-18</td>
      <td id="T_278a8_row0_col2" class="data row0 col2" >2024-06-18</td>
      <td id="T_278a8_row0_col3" class="data row0 col3" >2025-06-18</td>
      <td id="T_278a8_row0_col4" class="data row0 col4" >2025-06-19</td>
      <td id="T_278a8_row0_col5" class="data row0 col5" >1,000,000,000.00</td>
      <td id="T_278a8_row0_col6" class="data row0 col6" >1,000,000,000.00</td>
      <td id="T_278a8_row0_col7" class="data row0 col7" >False</td>
      <td id="T_278a8_row0_col8" class="data row0 col8" >CLP</td>
      <td id="T_278a8_row0_col9" class="data row0 col9" >ICPCLP</td>
      <td id="T_278a8_row0_col10" class="data row0 col10" >1.000000</td>
      <td id="T_278a8_row0_col11" class="data row0 col11" >1.000000</td>
      <td id="T_278a8_row0_col12" class="data row0 col12" >0.0000%</td>
      <td id="T_278a8_row0_col13" class="data row0 col13" >LinAct360</td>
      <td id="T_278a8_row0_col14" class="data row0 col14" >0.00</td>
      <td id="T_278a8_row0_col15" class="data row0 col15" >0.00</td>
      <td id="T_278a8_row0_col16" class="data row0 col16" >0.0000%</td>
      <td id="T_278a8_row0_col17" class="data row0 col17" >1.00</td>
    </tr>
  </tbody>
</table>



