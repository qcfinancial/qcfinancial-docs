import qcfinancial as qcf
import holidays as hol
import pandas as pd

format_dict = {
    'nominal': '{0:,.2f}', 
    'nocional': '{0:,.2f}', 
    'amort': '{0:,.2f}', 
    'amortizacion': '{0:,.2f}', 
    'interes': '{0:,.2f}',
    'monto': '{0:,.2f}',
    'flujo': '{0:,.2f}',
    'flujo_moneda_pago': '{0:,.2f}',
    'flujo_en_clp': '{0:,.2f}',
    'icp_inicial': '{0:,.2f}', 
    'icp_final': '{0:,.2f}',
    'uf_inicial': '{0:,.2f}', 
    'uf_final': '{0:,.2f}',
    'valor_tasa': '{0:,.4%}', 
    'valor_tasa_equivalente': '{0:,.4%}', 
    'spread': '{0:,.4%}', 
    'gearing': '{0:,.2f}',
    'amortizacion_moneda_pago': '{0:,.2f}', 
    'interes_moneda_pago': '{0:,.2f}', 
    'valor_indice_fx': '{0:,.2f}'
}

def leg_as_dataframe(leg: qcf.Leg):
    """
    Envuelve un objeto qcf.Leg en un pd.DataFrame
    """
    if leg.size() == 0:
        raise ValueError("No cashflows")
    type_cashflows = leg.get_cashflow_at(0).get_type()
    tabla = [qcf.show(leg.get_cashflow_at(i)) for i in range(0, leg.size())]
    df = pd.DataFrame(tabla, columns=qcf.get_column_names(type_cashflows, ''))
    return df


def get_business_calendar(which_holidays: str, years: range) -> qcf.BusinessCalendar:
    py_cal = hol.country_holidays(which_holidays, years=years)
    yrs = [y for y in years]
    qcf_cal = qcf.BusinessCalendar(qcf.QCDate(1, 1, yrs[0]), yrs[-1] - yrs[0])
    for d in py_cal.keys():
        qcf_cal.add_holiday(qcf.QCDate(d.isoformat()))
    return qcf_cal
