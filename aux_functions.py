import qcfinancial as qcf
import pandas as pd

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
