from typing import Iterable, Union
from collections import namedtuple
import datetime as dt
import holidays as hol
import pandas as pd
import numpy as np

import qcfinancial as qcf

import qcf_wrappers as qcw

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
    """
    Retorna un calendario de en formato qcfinancial.
    """
    py_cal = hol.country_holidays(which_holidays, years=years)
    yrs = [y for y in years]
    qcf_cal = qcf.BusinessCalendar(qcf.QCDate(1, 1, yrs[0]), yrs[-1] - yrs[0])
    for d in py_cal.keys():
        qcf_cal.add_holiday(qcf.QCDate(d.isoformat()))
    if which_holidays == 'CL':
        for year in years:
            d = qcf.QCDate(31, 12, year)
            if d.week_day() == qcf.WeekDay.SAT:
                d = d.add_days(-1)
            if d.week_day() == qcf.WeekDay.SUN:
                d = d.add_days(-2)
            qcf_cal.add_holiday(d)
    return qcf_cal


def build_zero_coupon_curve(
    plazos: Iterable[int],
    tasas: Iterable[float],
    yf: qcw.YearFraction,
    wf: qcw.WealthFactor,
    interpolator=None,
) -> qcf.ZeroCouponCurve:
    """
    Construye un objeto de tipo `ZeroCouponCurve`.
    """
    _plazos = qcf.long_vec()
    for p in plazos:
        _plazos.append(int(p))

    _tasas = qcf.double_vec()
    for t in tasas:
        _tasas.append(t)

    return qcf.ZeroCouponCurve(
        qcf.QCLinearInterpolator(qcf.QCCurve(_plazos, _tasas)),
        qcf.QCInterestRate(
            0.0,
            yf.as_qcf(),
            wf.as_qcf(),
        ),
    )


def compute_uf_series(cpi_change_pct: float, month: Union[str, pd.Timestamp, dt.date], initial_uf: float) -> pd.Series:
    """
    Calcula la serie diaria de la UF para un período (del día 10 al día 9 del mes siguiente)
    usando una interpolación exponencial basada en la variación del IPC del mes anterior.

    Fórmula solicitada: uf(n) = uf(0) * (1 + pct_change)**(n / N)
    - N: número de días entre el día 9 del mes `month` y el día 9 del mes siguiente.
    - n: contador de días desde el día 9 (por convención, el día 10 corresponde a n = 1, y el día 9 siguiente a n = N).

    Importante respecto al parámetro `initial_uf`:
    - `initial_uf` es el valor de la UF el día 10 del mes `month` (n = 1).
    - Para cumplir la fórmula anterior, se infiere uf(0) = initial_uf / (1 + pct_change)**(1/N).

    Parámetros
    - cpi_change_pct: variación porcentual del IPC del mes anterior (por ejemplo, 0.003 para 0.3%).
    - month: mes al cual se aplica dicha variación. Acepta "YYYY-MM", pandas.Timestamp o date.
    - initial_uf: valor de la UF al día 10 de `month`.

    Retorna
    - pd.Series con índice de fechas (datetime64[ns]) desde el 10 de `month` hasta el 9 del siguiente mes (ambos inclusive),
      calculada como una progresión exponencial de razón diaria (1 + cpi_change_pct)**(1/N).
    """
    # Normalizar el mes a (año, mes)
    if isinstance(month, str):
        # Permitir "YYYY-MM" o "YYYY-MM-DD" (se ignora el día)
        try:
            ts = pd.to_datetime(month)
        except Exception as e:
            raise ValueError(f"Formato de `month` inválido: {month}") from e
        year, m = ts.year, ts.month
    elif isinstance(month, pd.Timestamp):
        year, m = month.year, month.month
    elif isinstance(month, dt.date):
        year, m = month.year, month.month
    else:
        raise TypeError("`month` debe ser str, pandas.Timestamp o datetime.date")

    # Fechas relevantes
    start = dt.date(year, m, 10)
    start_9 = dt.date(year, m, 9)
    # calcular siguiente mes (maneja diciembre)
    if m == 12:
        next_year, next_month = year + 1, 1
    else:
        next_year, next_month = year, m + 1
    end = dt.date(next_year, next_month, 9)

    # N: días entre día 9 y día 9 del mes siguiente
    N = (end - start_9).days
    print(N)
    if N <= 0:
        # Caso defensivo (no debería ocurrir)
        return pd.Series([], dtype=float)

    # Rango de fechas inclusivo (del 10 al 9 del mes siguiente)
    idx = pd.date_range(start=start, end=end, freq='D')

    # Mapear fechas a n = 1..N
    n_vals = pd.Series(range(1, len(idx) + 1), index=idx, dtype=float)

    # Ajustar uf(0) para que uf(1) == initial_uf
    one_plus = 1.0 + float(cpi_change_pct)
    # Si one_plus <= 0, la potencia puede ser problemática; mantenemos el comportamiento natural de pow
    # y evitamos división por cero con un pequeño manejo especial
    if one_plus == 0.0:
        # En este caso, la razón diaria es 0**(1/N)=0 y uf(1)=0, lo que contradice `initial_uf`.
        # Optamos por devolver una serie constante = initial_uf como salida segura.
        series = pd.Series(initial_uf, index=idx, dtype=float)
        series.name = 'UF'
        series = series.round(2)
        return series

    uf0 = initial_uf

    # Serie exponencial: uf(n) = uf0 * (1 + pct)**(n/N), con n=1..N
    series = uf0 * (one_plus ** (n_vals / N))
    series.name = 'UF'
    series = series.round(2)
    return series


def compute_icp_series(
    initial_icp: float,
    start_date: Union[str, pd.Timestamp, dt.date],
    end_date: Union[str, pd.Timestamp, dt.date],
    overnight_rate: float,
    day_count: qcw.YearFraction = qcw.YearFraction.ACT360,
) -> pd.Series:
    """
    Calcula la serie diaria del Índice Cámara Promedio (ICP) entre dos fechas,
    a partir de un ICP inicial y una tasa interbancaria overnight anual (plana).

    Supuestos y fórmula:
    - Se usa capitalización discreta diaria con base del day_count elegido.
    - Para D días transcurridos: ICP(t) = ICP0 * (1 + r / base)^(D), donde base=360 o 365.

    Parámetros:
    - initial_icp: valor del ICP en la fecha de inicio (start_date).
    - start_date, end_date: límites del período. end_date >= start_date.
    - overnight_rate: tasa anualizada (en unidad, p.ej. 0.08 para 8%).
    - day_count: base de días (por defecto ACT/360).

    Retorna:
    - pd.Series indexada por fecha, incluye start_date y end_date. El primer valor es initial_icp.
    """
    # Normalizar fechas
    s = pd.to_datetime(start_date).date() if not isinstance(start_date, dt.date) else start_date
    e = pd.to_datetime(end_date).date() if not isinstance(end_date, dt.date) else end_date
    if e < s:
        raise ValueError("end_date no puede ser anterior a start_date")

    # Base de días
    if day_count == qcw.YearFraction.ACT360:
        base = 360.0
    elif day_count == qcw.YearFraction.ACT365:
        base = 365.0
    else:
        # Por simplicidad, otras bases se aproximan a 365.
        base = 365.0

    idx = pd.date_range(start=s, end=e, freq='D')
    # días transcurridos desde start_date: 0,1,2,... (como ndarray para evitar devolver un Index)
    d = (idx - idx[0]).days.values.astype(float)
    factor_diario = 1.0 + float(overnight_rate) / base
    values = initial_icp * (factor_diario ** d)
    series = pd.Series(values, index=idx, name='ICP')
    return series


def compute_icp_between_dates(
    initial_icp: float,
    start_date: Union[str, pd.Timestamp, dt.date],
    end_date: Union[str, pd.Timestamp, dt.date],
    overnight_rate: float,
    day_count: qcw.YearFraction = qcw.YearFraction.ACT360,
) -> float:
    """
    Retorna el valor del ICP en end_date, capitalizando diariamente la tasa overnight
    plana indicada, con base ACT/360 por defecto.

    Equivalente a tomar el último valor de compute_icp_series(...).
    """
    series = compute_icp_series(initial_icp, start_date, end_date, overnight_rate, day_count)
    return float(series.iloc[-1])


def compute_uf_series_from_cpi_changes(
    initial_uf_at_9th: float,
    start_month: Union[str, pd.Timestamp, dt.date],
    cpi_changes_pct: Iterable[float],
    include_initial_9th: bool = True,
) -> pd.Series:
    """
    Calcula la serie de la UF encadenando períodos mensuales consecutivos, usando
    `compute_uf_series` y una lista de variaciones porcentuales de IPC.

    Convención de UF/IPC utilizada en Chile:
    - Entre el 10 de un mes M y el 9 del mes M+1, la UF varía conforme al IPC del mes M-1.
    - Por ejemplo, del 10-ene al 9-feb se usa el IPC de diciembre.

    Parámetros
    - initial_uf_at_9th: valor de la UF el día 9 del `start_month` (fecha anterior
      al inicio del primer tramo de interpolación, que arranca el 10).
    - start_month: mes inicial de la serie UF deseada ("YYYY-MM" o fecha). El primer
      tramo cubre del 10 de `start_month` al 9 del mes siguiente.
    - cpi_changes_pct: lista/iterable con las variaciones de IPC (en unidades, ej 0.003 para 0.3%),
      una por cada tramo mensual. La i-ésima variación se aplica del 10 de (start_month + i)
      al 9 del mes siguiente, es decir, corresponde al IPC del mes inmediatamente anterior
      a ese tramo.
    - include_initial_9th: si True, el resultado incluirá un primer punto en el índice con la
      fecha 9 de `start_month` y valor `initial_uf_at_9th`.

    Retorna
    - pd.Series con índice diario concatenado, cubriendo desde el 10 del `start_month` hasta
      el 9 del mes posterior al último tramo incluido. Si `include_initial_9th` es True, agrega
      además el 9 del `start_month` al inicio.

    Ejemplo
    >>> # UF para ene, feb y mar 2025, usando IPC dic-2024, ene-2025 y feb-2025
    >>> compute_uf_series_from_cpi_changes(
    ...     initial_uf_at_9th=valor_uf_2025_01_09,
    ...     start_month="2025-01",
    ...     cpi_changes_pct=[ipc_dic_2024, ipc_ene_2025, ipc_feb_2025],
    ... )
    """
    # Normalizar `start_month` a (año, mes)
    if isinstance(start_month, str):
        ts = pd.to_datetime(start_month)
        year, month = ts.year, ts.month
    elif isinstance(start_month, pd.Timestamp):
        year, month = start_month.year, start_month.month
    elif isinstance(start_month, dt.date):
        year, month = start_month.year, start_month.month
    else:
        raise TypeError("`start_month` debe ser str, pandas.Timestamp o datetime.date")

    def add_months(y: int, m: int, k: int) -> tuple[int, int]:
        """Devuelve (año, mes) luego de sumar k meses a (y, m)."""
        total = (y * 12 + (m - 1)) + k
        ny = total // 12
        nm = (total % 12) + 1
        return ny, nm

    pieces = []
    current_uf_at_9th = float(initial_uf_at_9th)

    # Opción para incluir el 9 del mes inicial
    if include_initial_9th:
        start_9 = dt.date(year, month, 9)
        pieces.append(pd.Series([current_uf_at_9th], index=pd.to_datetime([start_9]), name='UF'))

    for i, cpi in enumerate(cpi_changes_pct):
        y_i, m_i = add_months(year, month, i)
        # Construye serie del 10 de (y_i, m_i) al 9 del siguiente mes
        # compute_uf_series interpreta `initial_uf` como el valor del día 9 previo para que el 10
        # resulte en UF9 * (1 + cpi)^(1/N), acorde con la convención del propio cálculo implementado.
        s = compute_uf_series(float(cpi), dt.date(y_i, m_i, 1), current_uf_at_9th)
        pieces.append(s)
        # El último valor de s es el 9 del mes siguiente: pasa a ser el UF@9th para el próximo tramo
        current_uf_at_9th = float(s.iloc[-1])

    if not pieces:
        return pd.Series([], dtype=float, name='UF')

    out = pd.concat(pieces)
    out.name = 'UF'
    # En caso de seguridad, ordenar y eliminar duplicados preservando el primero
    out = out[~out.index.duplicated(keep='first')].sort_index()
    return out


def sens_proyeccion(fecha_hoy, overnight_index_leg_, zcc_clp, bp, fwd):
    """
    Calcula la sensibilidad proyectada (vectorial) de una pierna indexada a tasa overnight
    ante un desplazamiento paralelo de bp puntos base, descontada a valor presente.

    Para cada cashflow de la pierna, se obtiene su vector de derivadas del monto con
    respecto a los nodos/subyacentes relevantes (vía `get_amount_derivatives()`), se
    escala por bp/10_000 y se multiplica por el factor de descuento correspondiente a
    su fecha de liquidación. Luego, se suman todos los vectores de derivadas de los
    cashflows, retornando la sensibilidad total como un único vector.

    Parámetros
    - fecha_hoy: fecha a la cual se realiza el cálculo
    - overnight_index_leg_: objeto de pata (por ejemplo, qcf.Leg o similar) que expone
      `size()`, `get_cashflow_at(i)`, y cuyos cashflows exponen `get_amount_derivatives()`
      y `get_settlement_date()`.
    - zcc_clp: curva de descuento (por ejemplo, ZeroCouponCurve) que expone
      `get_discount_factor_at(days)` para obtener el factor de descuento según días desde hoy.
    - bp: desplazamiento paralelo en puntos base (float), p.ej. 1.0 para 1 bp, 25.0 para 25 bps.

    Retorna
    - numpy.ndarray con la suma elemento a elemento de las derivadas descontadas para
      todos los cashflows de la pierna. La dimensión del vector coincide con la longitud
      de `get_amount_derivatives()` de los cashflows (se asume consistente entre ellos).

    Notas
    - Requiere `numpy` importado como `np` en el ámbito del módulo.
    - No se realizan validaciones adicionales; se asume que todos los vectores de derivadas
      tienen la misma longitud para que la suma sea válida.
    """
    result = []
    fwd.set_rates_overnight_index_leg(fecha_hoy, 25_000.0, overnight_index_leg_, zcc_clp)
    for i in range(overnight_index_leg_.size()):
        cashflow = overnight_index_leg_.get_cashflow_at(i)
        amt_der = cashflow.get_amount_derivatives()
        df = zcc_clp.get_discount_factor_at(fecha_hoy.day_diff(cashflow.get_settlement_date()))
        amt_der = [a * bp / 10_000 * df for a in amt_der]
        if len(amt_der) > 0:
            result.append(np.array(amt_der))

    total = result[0] * 0

    for r in result:
        total += r

    return total


def encuentra_tir_swap(fecha, pata, tir_inicial, objetivo, pv):
    tasa = tir_inicial
    delta = 1_000_000_000.0
    while abs(delta) > 0.0001:
        pv_swap = pv.pv(fecha, pata, qcf.QCInterestRate(tasa, qcf.QCAct365(), qcf.QCCompoundWf()))
        # print(pv_swap)
        delta = pv_swap - objetivo
        # print(delta)
        der = sum([s for s in pv.get_derivatives()])
        tasa -= (pv_swap - objetivo) / der
        # print(tasa)
    return tasa


def vp_swap_spread(
        fecha,
        pata_bono,
        tir_mercado_bono,
        tir_compra_bono,
        pata_fija_swap,
        curva_descuento_fija_swap,
        pata_icpclp_swap,
        curva_proyeccion_icpclp,
        curva_descuento_icpclp,
        uf,
        icp_inicial,
        icp_fecha,
        pv,
        fwd,
):
    # Bono
    pv_bono = pv.pv(fecha, pata_bono, tir_mercado_bono) * uf
    sens_bono = sum([s for s in pv.get_derivatives()]) * .0001 * uf

    pv_compra_bono = pv.pv(fecha, pata_bono, tir_compra_bono) * uf
    ajuste_valor_mercado_bono = pv_bono - pv_compra_bono

    # Pata fija swap
    pv_pata_fija_swap = pv.pv(fecha, pata_fija_swap, curva_descuento_fija_swap) * uf
    sens_pata_fija_swap = sum([s for s in pv.get_derivatives()]) * .0001 * uf

    cashflow_fija = pata_fija_swap.get_cashflow_at(0)
    accrued_interest_fija_swap = cashflow_fija.accrued_interest(fecha) * uf

    # Pata ICPCLP
    cashflow_icpclp = pata_icpclp_swap.get_cashflow_at(0)
    cashflow_icpclp.set_start_date_index(icp_inicial)
    accrued_interest_icpclp_swap = cashflow_icpclp.accrued_interest(fecha, icp_fecha)

    fwd.set_rates_overnight_index_leg(fecha, icp_fecha, pata_icpclp_swap, curva_proyeccion_icpclp)
    pv_pata_icpclp = pv.pv(fecha, pata_icpclp_swap, curva_descuento_icpclp)
    sens_proyeccion_pata_icpclp_swap = sens_proyeccion(fecha, pata_icpclp_swap, curva_proyeccion_icpclp, 1.0, fwd)
    sens_descuento_pata_icpclp_swap = sum([s for s in pv.get_derivatives()]) * .0001

    Resultado = namedtuple(
        'Resultado',
        [
            'pv_bono',
            'pv_compra_bono',
            'ajuste_valor_mercado_bono',
            'sens_bono',
            'pv_pata_fija_swap',
            'sens_pata_fija_swap',
            'accrued_value_fija_swap',
            'pv_pata_icpclp',
            'sens_proyeccion_pata_icpclp_swap',
            'sens_descuento_pata_icpclp_swap',
            'accrued_value_icpclp_swap',
            'valor_presente_total',
        ]
    )
    print(cashflow_icpclp.get_nominal())
    return Resultado(
        pv_bono=pv_bono,
        sens_bono=sens_bono,
        pv_compra_bono=pv_compra_bono,
        ajuste_valor_mercado_bono=ajuste_valor_mercado_bono,
        pv_pata_fija_swap=pv_pata_fija_swap,
        sens_pata_fija_swap=sens_pata_fija_swap,
        accrued_value_fija_swap=accrued_interest_fija_swap + cashflow_fija.get_nominal() * uf,
        pv_pata_icpclp=pv_pata_icpclp,
        sens_proyeccion_pata_icpclp_swap=sum([s for s in sens_proyeccion_pata_icpclp_swap]),
        sens_descuento_pata_icpclp_swap=sens_descuento_pata_icpclp_swap,
        accrued_value_icpclp_swap=accrued_interest_icpclp_swap + cashflow_icpclp.get_nominal(),
        valor_presente_total=pv_bono + pv_pata_fija_swap + pv_pata_icpclp,
    )


def make_tir(valor_tir):
    return qcf.QCInterestRate(valor_tir, qcf.QCAct365(), qcf.QCCompoundWf())