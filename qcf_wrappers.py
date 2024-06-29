from enum import Enum, auto
from pydantic import NonNegativeInt, BaseModel, validator
from pydantic.dataclasses import dataclass
from datetime import datetime

import qcfinancial as qcf


class Currency(str, Enum):
    """
    Identifica todas las divisas que se pueden utilizar con `qcfinancial`.
    """

    CLF = "CLF"
    CL2 = "CL2"
    CLP = "CLP"
    EUR = "EUR"
    USD = "USD"
    JPY = "JPY"
    GBP = "GBP"
    BRL = "BRL"
    MXN = "MXN"
    COP = "COP"
    CHF = "CHF"
    CAD = "CAD"
    CNY = "CNY"
    SEK = "SEK"
    NOK = "NOK"

    def as_qcf(self):
        """
        Retorna la divisa representada por `self` con el correspondiente objeto `qcfinancial`.
        """
        switcher = {
            self.CLF: qcf.QCCLF(),
            self.CL2: qcf.QCCLF2(),
            self.CLP: qcf.QCCLP(),
            self.EUR: qcf.QCEUR(),
            self.USD: qcf.QCUSD(),
            self.JPY: qcf.QCJPY(),
            self.GBP: qcf.QCGBP(),
            self.BRL: qcf.QCBRL(),
            self.MXN: qcf.QCMXN(),
            self.COP: qcf.QCCOP(),
            self.CHF: qcf.QCCHF(),
            self.CAD: qcf.QCCAD(),
            self.CNY: qcf.QCCNY(),
            self.SEK: qcf.QCSEK(),
            self.NOK: qcf.QCNOK(),
        }

        return switcher[self.value]

    def __str__(self):
        return self.as_qcf().get_iso_code()

    def __repr__(self):
        return self.__str__()


class BusAdjRules(str, Enum):
    """
    Representa los distintos algoritmos de ajuste de fecha disponibles en `qcfinancial`.

    Los valores disponibles son:

    - NO: no ajustar las fechas.

    - FOLLOW: si la fecha cae en un feriado, la fecha se desplaza al día hábil siguiente.

    - MOD_FOLLOW: si la fecha cae en feriado se desplaza al día hábil siguiente, excepto que el día hábil siguiente
    esté en el mes siguiente, en ese caso, la fecha se desplaza al día hábil anterior.

    - PREV: si la fecha cae en feriado, la fecha se desplaza al día hábil anterior.

    - MOD_PREV: si la fecha cae en feriado, la fecha se desplaza al día hábil anterior, excepto que el día hábil
    anterior esté en el mes anterior, en ese caso, la fecha se desplaza al día hábil siguiente.
    """

    NO = "NO"
    FOLLOW = "FOLLOW"
    MOD_FOLLOW = "MOD_FOLLOW"
    PREV = "PREV"
    MOD_PREV = "MOD_PREV"

    def as_qcf(self) -> qcf.BusyAdjRules:
        """
        Retorna la regla de ajuste de fecha representada por `self` con el correspondiente objeto `qcfinancial`.
        """
        switcher = {
            self.NO: qcf.BusyAdjRules.NO,
            self.FOLLOW: qcf.BusyAdjRules.FOLLOW,
            self.MOD_FOLLOW: qcf.BusyAdjRules.MODFOLLOW,
            self.PREV: qcf.BusyAdjRules.PREVIOUS,
            self.MOD_PREV: qcf.BusyAdjRules.MODPREVIOUS,
        }

        return switcher[self.value]

    def __str__(self):
        return str(self.value)


class StubPeriods(str, Enum):
    """
    Representa los distintos ajustes de período irregular disponibles en `qcfinancial`.
    """

    NO = "NO"
    CORTO_INICIO = "CORTO INICIO"
    CORTO_FINAL = "CORTO FINAL"
    LARGO_INICIO = "LARGO INICIO"
    LARGO_FINAL = "LARGO FINAL"
    LARGO_INICIO_2 = "LARGO INICIO 2"
    LARGO_INICIO_3 = "LARGO INICIO 3"
    LARGO_INICIO_4 = "LARGO INICIO 4"
    LARGO_INICIO_5 = "LARGO INICIO 5"
    LARGO_INICIO_6 = "LARGO INICIO 6"
    LARGO_INICIO_7 = "LARGO INICIO 7"
    LARGO_INICIO_8 = "LARGO INICIO 8"
    LARGO_INICIO_9 = "LARGO INICIO 9"
    LARGO_INICIO_10 = "LARGO INICIO 10"
    LARGO_INICIO_11 = "LARGO INICIO 11"
    LARGO_INICIO_12 = "LARGO INICIO 12"
    LARGO_INICIO_13 = "LARGO INICIO 13"
    LARGO_INICIO_14 = "LARGO INICIO 14"

    def as_qcf(self):
        """
        Retorna la regla de ajuste de período irregular representada por `self` con el correspondiente objeto `QC_Financial_3`.
        """
        switcher = {
            self.NO: qcf.StubPeriod.NO,
            self.CORTO_INICIO: qcf.StubPeriod.SHORTFRONT,
            self.CORTO_FINAL: qcf.StubPeriod.SHORTBACK,
            self.LARGO_INICIO: qcf.StubPeriod.LONGFRONT,
            self.LARGO_FINAL: qcf.StubPeriod.LONGBACK,
            self.LARGO_INICIO_2: qcf.StubPeriod.LONGFRONT2,
            self.LARGO_INICIO_3: qcf.StubPeriod.LONGFRONT3,
            self.LARGO_INICIO_4: qcf.StubPeriod.LONGFRONT4,
            self.LARGO_INICIO_5: qcf.StubPeriod.LONGFRONT5,
            self.LARGO_INICIO_6: qcf.StubPeriod.LONGFRONT6,
            self.LARGO_INICIO_7: qcf.StubPeriod.LONGFRONT7,
            self.LARGO_INICIO_8: qcf.StubPeriod.LONGFRONT8,
            self.LARGO_INICIO_9: qcf.StubPeriod.LONGFRONT9,
            self.LARGO_INICIO_10: qcf.StubPeriod.LONGFRONT10,
            self.LARGO_INICIO_11: qcf.StubPeriod.LONGFRONT11,
            self.LARGO_INICIO_12: qcf.StubPeriod.LONGFRONT12,
            self.LARGO_INICIO_13: qcf.StubPeriod.LONGFRONT13,
            self.LARGO_INICIO_14: qcf.StubPeriod.LONGFRONT14,
        }

        return switcher[self.value]

    def __str__(self):
        return self.value.replace(" ", "-")


class YearFraction(Enum):
    """
    Identifica las distintas fracciones de año disponibles en `qcfinancial`.
    """

    ACT30 = auto()
    ACT360 = auto()
    ACT365 = auto()
    YF30360 = auto()

    def as_qcf(self) -> qcf.QCYearFraction:
        """
        Retorna la fracción de año representada por `self` como el correspondiente objeto `qcfinancial`.
        """
        switcher = {
            YearFraction.ACT30: qcf.QCAct30,
            YearFraction.ACT360: qcf.QCAct360,
            YearFraction.ACT365: qcf.QCAct365,
            YearFraction.YF30360: qcf.QC30360,
        }

        return switcher[self]()


class WealthFactor(Enum):
    """
    Identifica los distintos factores de capitalización disponibles en `qcfinancial`.
    """

    COM = auto()
    LIN = auto()
    CON = auto()

    def as_qcf(self) -> qcf.QCWealthFactor:
        """
        Retorna el factor de capitalización representado por `self` como el correspondiente objeto `qcfinancial`.
        """
        switcher = {
            WealthFactor.COM: qcf.QCCompoundWf,
            WealthFactor.LIN: qcf.QCLinearWf,
            WealthFactor.CON: qcf.QCContinousWf,
        }

        return switcher[self]()


class TypeOfRate(str, Enum):
    """
    `Enum` que identifica distintos tipos de tasa (factor de capitalización + fracción de año).

    La clase hereda también de `str` lo que permite construir el objeto con los siguientes `str`:

    - 'LIN_ACT/360'
    - 'LIN_30/360'
    - 'LIN_ACT/365'
    - 'LIN_ACT/30'
    - 'COM_ACT/365'
    - 'COM_ACT/360'
    - 'COM_30/360'
    - 'CON_ACT/365'
    """

    LINACT360 = "LIN_ACT/360"
    LIN30360 = "LIN_30/360"
    LINACT365 = "LIN_ACT/365"
    LINACT30 = "LIN_ACT/30"
    COMACT365 = "COM_ACT/365"
    COMACT360 = "COM_ACT/360"
    COM30360 = "COM_30/360"
    CONACT365 = "CON_ACT/365"

    def as_qcf(self):
        """
        Retorna `self` en formato `Qcf.QCInterestRate`. El valor de la tasa es 0.
        """
        switcher = {
            self.LINACT360: qcf.QCInterestRate(
                0.0,
                YearFraction.ACT360.as_qcf(),
                WealthFactor.LIN.as_qcf(),
            ),
            self.LIN30360: qcf.QCInterestRate(
                0.0,
                YearFraction.YF30360.as_qcf(),
                WealthFactor.LIN.as_qcf(),
            ),
            self.LINACT365: qcf.QCInterestRate(
                0.0,
                YearFraction.ACT365.as_qcf(),
                WealthFactor.LIN.as_qcf(),
            ),
            self.LINACT30: qcf.QCInterestRate(
                0.0,
                YearFraction.ACT30.as_qcf(),
                WealthFactor.LIN.as_qcf(),
            ),
            self.COMACT365: qcf.QCInterestRate(
                0.0,
                YearFraction.ACT365.as_qcf(),
                WealthFactor.COM.as_qcf(),
            ),
            self.COMACT360: qcf.QCInterestRate(
                0.0,
                YearFraction.ACT360.as_qcf(),
                WealthFactor.COM.as_qcf(),
            ),
            self.COM30360: qcf.QCInterestRate(
                0.0,
                YearFraction.YF30360.as_qcf(),
                WealthFactor.COM.as_qcf(),
            ),
            self.CONACT365: qcf.QCInterestRate(
                0.0,
                YearFraction.ACT365.as_qcf(),
                WealthFactor.CON.as_qcf(),
            ),
        }
        return switcher[self.value]

    def as_qcf_with_value(self, rate_value: float):
        """
        Retorna `self` en formato `Qcf.QCInterestRate` con el valor de tasa especificado.

        Parameters:
        -----------
        rate_value: float
            El valor de la tasa

        Returns:
        --------
        `Qcf.QCInterestRate`.
        """
        result = self.as_qcf()
        result.set_value(rate_value)
        return result

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()


class AP(str, Enum):
    """
    Representa un Activo o un Pasivo.
    """

    A = "A"
    P = "P"

    def __str__(self):
        return str(self.value)

    def as_qcf(self):
        if self.value == "A":
            return qcf.RecPay.RECEIVE
        else:
            return qcf.RecPay.PAY


class DatesForEquivalentRate(str, Enum):
    """
    Envuelve en análogo class enum de qcfinancial que indica si el cálculo de la tasa equivalente en un
    OvernightIndexCashflow se hace con las fechas de ACCRUAL o INDEX.
    """

    ACCRUAL = "ACCRUAL"
    INDEX = "INDEX"

    def __str__(self):
        return str(self.value)

    def as_qcf(self):
        if self.value == "ACCRUAL":
            return qcf.DatesForEquivalentRate.ACCRUAL
        else:
            return qcf.DatesForEquivalentRate.INDEX


class FXRate(str, Enum):
    """
    Representa los distintos tipos de cambio disponibles en qcfinancial.
    """

    USDCLP = "USDCLP"
    USDCLF = "USDCLF"
    CLFCLP = "CLFCLP"
    CL2CLP = "CL2CLP"
    EURUSD = "EURUSD"
    EURCLP = "EURCLP"
    CLPUSD = "CLPUSD"
    CLFUSD = "CLFUSD"
    CLPCLF = "CLPCLF"
    CLPCL2 = "CLPCL2"
    USDEUR = "USDEUR"
    CLPEUR = "CLPEUR"
    NFXNFX = "NFXNFX"
    USDUSD = "USDUSD"
    CLPCLP = "CLPCLP"
    EUREUR = "EUREUR"
    CLFCLF = "CLFCLF"
    CNYUSD = "CNYUSD"
    CNYCLP = "CNYCLP"
    USDNOK = "USDNOK"
    NOKCLP = "NOKCLP"
    USDSEK = "USDSEK"
    SEKCLP = "SEKCLP"
    USDCOP = "USDCOP"
    COPCLP = "COPCLP"
    USDJPY = "USDJPY"
    JPYCLP = "JPYCLP"

    def __str__(self):
        return str(self.value)

    def mkt(self):
        switcher = {
            "USDCLP": "USDCLP",
            "CLPUSD": "USDCLP",
            "USDCLF": "USDCLF",
            "CLFUSD": "USDCLF",
            "CLFCLP": "CLFCLP",
            "CLPCLF": "CLFCLP",
            "CL2CLP": "CL2CLP",
            "CLPCL2": "CL2CLP",
            "EURUSD": "EURUSD",
            "USDEUR": "EURUSD",
            "EURCLP": "EURCLP",
            "CLPEUR": "EURCLP",
            "NFXNFX": "NFXNFX",
            "USDUSD": "USDUSD",
            "CLPCLP": "CLPCLP",
            "EUREUR": "EUREUR",
            "CLFCLF": "CLFCLF",
            "CNYUSD": "CNYUSD",
            "USDCNY": "USDCNY",
            "CNYCLP": "CNYCLP",
            "CLPCNY": "CNYCLP",
            "USDCOP": "USDCOP",
            "COPUSD": "USDCOP",
            "COPCLP": "COPCLP",
            "CLPCOP": "COPCLP",
            "USDNOK": "USDNOK",
            "NOKUSD": "USDNOK",
            "NOKCLP": "NOKCLP",
            "CLPNOK": "NOKCLP",
            "USDSEK": "USDSEK",
            "SEKUSD": "USDSEK",
            "SEKCLP": "SEKCLP",
            "CLPSEK": "SEKCLP",
            "USDJPY": "USDJPY",
            "JPYUSD": "USDJPY",
            "CLPJPY": "JPYCLP",
            "JPYCLP": "JPYCLP",
        }

        return switcher[self.value]


class SettLagBehaviour(str, Enum):
    DONT_MOVE = "DONT_MOVE"
    MOVE_TO_WORKING_DAY = "MOVE_TO_WORKING_DAY"

    def __str__(self):
        return str(self.value)

    def as_qcf(self):
        match self.value:
            case "DONT_MOVE":
                return qcf.SettLagBehaviour.DONT_MOVE
            case "MOVE_TO_WORKING_DAY":
                return qcf.SettLagBehaviour.MOVE_TO_WORKING_DAY
            case _:
                return qcf.SettLagBehaviour.DONT_MOVE


@dataclass
class Tenor:
    agnos: NonNegativeInt
    meses: NonNegativeInt
    dias: NonNegativeInt

    def as_qcf(self):
        return qcf.Tenor(f"{self.agnos}Y{self.meses}M{self.dias}D")

    def total_months(self):
        return self.agnos * 12 + self.meses

    def __hash__(self):
        return self.dias + self.meses * 30 + self.agnos * 12 * 30

    def __lt__(self, other):
        return self.__hash__() < other.__hash__()

    def __str__(self):
        str_agnos = f"{self.agnos}Y" if self.agnos > 0 else ""
        str_meses = f"{self.meses}M" if self.meses > 0 else ""
        str_dias = f"{self.dias}D" if self.dias > 0 else ""
        return f"{str_agnos}{str_meses}{str_dias}"

    def __repr__(self):
        return self.__str__()


def build_tenor_from_str(tenor: str) -> Tenor:
    ten = qcf.Tenor(tenor)
    return Tenor(
        dias=ten.get_days(),
        meses=ten.get_months(),
        agnos=ten.get_years(),
    )


class Fecha(BaseModel):
    fecha: str

    @validator("fecha")
    def valid_iso_format(cls, v):
        try:
            qcf.build_qcdate_from_string(v)
        except Exception as e:
            raise ValueError(f"No es un formato iso de fecha válido. {str(e)}")
        return v

    def as_py_date(self):
        return datetime.strptime(self.fecha, "%Y-%m-%d").date()

    def as_qcf(self):
        return qcf.build_qcdate_from_string(self.fecha)

    def as_tag(self):
        return self.fecha.replace("-", "")

    def __hash__(self):
        return hash(self.fecha)


def get_end_date(start_date: Fecha, tenor: Tenor) -> Fecha:
    """
    Calcula una fecha final a partir de una fecha inicial y un Tenor.

    Parameters
    ----------
    start_date (Fecha): Fecha inicial
    tenor (Tenor): Tenor que se suma a `start_date`.

    Returns
    -------
    Fecha: Fecha final calculada

    """
    qcf_date = start_date.as_qcf()
    meses = tenor.meses + tenor.agnos * 12
    temp_date = qcf_date.add_months(meses)
    return Fecha(
        fecha=temp_date.add_days(tenor.dias).description(False)
    )
