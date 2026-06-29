# qcfinancial-docs

Este archivo REDME.md fue creado para cumplir con el requerimiento de la tarea (nombre intencionalmente sin la "A"). Aquí se ofrece una guía práctica y más detallada de los notebooks del proyecto. Para la documentación principal, consulte el archivo README.md y el sitio publicado.

- Documentación en línea: https://qcfinancial.github.io/qcfinancial-docs/
- Archivo principal: README.md

## Cómo usar estos notebooks

El proyecto se gestiona con [uv](https://docs.astral.sh/uv/) (Python 3.12). Hay
**dos superficies de instalación** y es importante distinguirlas:

- `uv sync` instala únicamente las herramientas para **construir el sitio**
  (nbconvert, jupyterlab, etc.). El conversor es Python puro y **no** instala
  `qcfinancial`. Con esto **los notebooks no se pueden ejecutar**.
- `uv sync --extra notebooks` instala además la **superficie de ejecución de los
  notebooks** (`qcfinancial`, `pandas`, `numpy`, `holidays`, `openpyxl`,
  `pydantic`). **Este es el comando que debe usar quien clone el repo para correr
  los cuadernos.**

```bash
git clone <repo>
cd qcfinancial-docs
uv sync --extra notebooks   # imprescindible para ejecutar los notebooks
uv run jupyter lab
```

> **Nota sobre `qcfinancial`:** es una extensión compilada y publica *wheels*
> solo para algunas plataformas. Si `uv sync --extra notebooks` falla porque no
> hay *wheel* para su sistema, deberá obtener el módulo compilado
> (`qcfinancial.cpython-*.so`) por otra vía y colocarlo en la raíz del repo.

- En todos los cuadernos se sugiere importar la librería con `import qcfinancial as qcf`.
- Los notebooks leen datos de `./input` por ruta relativa: ejecútelos desde la raíz del repo.

## Resumen de notebooks
A continuación, un breve resumen de cada notebook, con enlaces directos dentro del repo:

1. 1_Objetos_Fundamentales.ipynb — Introducción a los objetos base de qcfinancial: monedas (QCCurrency), fechas (QCDate), tasas, y utilidades varias.
   - Enlace: ./1_Objetos_Fundamentales.ipynb

2. 2_Cashflows.ipynb — Flujo de caja simples y multicurrency; funciones `show` y `get_column_names`; formateo con pandas.
   - Enlace: ./2_Cashflows.ipynb

3. 3_Construccion_Operaciones.ipynb — Construcción de operaciones a partir de patas (Legs): ejemplos con `FixedRateLeg` y parámetros clave (RecPay, Tenor, StubPeriod, calendarios, etc.).
   - Enlace: ./3_Construccion_Operaciones.ipynb

4. 4_Valorizacion_Sensibilidad.ipynb — Curvas cero cupón, valorización de patas y cálculo de sensibilidades. Incluye vectores numéricos, curvas e interpoladores.
   - Enlace: ./4_Valorizacion_Sensibilidad.ipynb

5. 5_SwapICPCLP.ipynb — Configuración de un swap de mercado ICPCLP vs tasa fija, con valores por defecto y construcción de ambas patas.
   - Enlace: ./5_SwapICPCLP.ipynb

6. 6_Curva_SOFR.ipynb — Construcción de la curva cero de SOFR a partir de swaps vs fija usando bootstrapping y Newton-Raphson.
   - Enlace: ./6_Curva_SOFR.ipynb

7. 7_Templates_unfinished.ipynb — Borrador de plantillas para construcción asistida de operaciones, patrones de clases y envoltorios (`qcf_wrappers`).
   - Enlace: ./7_Templates_unfinished.ipynb

8. 90_Valorizacion_Sensibilidad_Tests.ipynb — Variante de pruebas para valorización y sensibilidad, con estructuras similares al notebook 4.
   - Enlace: ./90_Valorizacion_Sensibilidad_Tests.ipynb

9. 98_Pruebas_Construccion_Operaciones.ipynb — Pruebas y ejemplos adicionales de construcción de patas y operaciones; útil para validar parámetros y casos borde.
   - Enlace: ./98_Pruebas_Construccion_Operaciones.ipynb

10. 99_Ejemplo_Forward_BTU.ipynb — Ejemplo de valorización de un forward de BTU (bono CLP), cálculo de VP, precio y M2M a una fecha de valorización.
    - Enlace: ./99_Ejemplo_Forward_BTU.ipynb

11. Ejemplos_qcfinancial_2b.ipynb — Conjunto adicional de ejemplos de uso de la librería (según disponibilidad del cuaderno).
    - Enlace: ./Ejemplos_qcfinancial_2b.ipynb

## Archivos auxiliares
- aux_functions.py — Funciones de apoyo (por ejemplo, `leg_as_dataframe`, utilidades de formateo y calendarios).
- qcf_wrappers.py — Envoltorios y utilidades para simplificar la construcción de objetos (utilizado en algunos notebooks).

## Notas
- Algunos ejemplos requieren datos de `./input` (por ejemplo, 6_Curva_SOFR.ipynb usa `20240621_sofr_data.xlsx`).
- Los notebooks marcados como "Templates" o "Pruebas" pueden contener código experimental o dependencias opcionales.

Última actualización: 2025-09-23 15:19

---

# qcfinancial-docs (English)

This `REDME.md` file was created to fulfill the task requirement (the name
intentionally omits the "A"). It offers a practical, more detailed guide to the
project's notebooks. For the main documentation, see the `README.md` file and the
published site.

- Online documentation: https://qcfinancial.github.io/qcfinancial-docs/
- Main file: README.md

## How to use these notebooks

The project is managed with [uv](https://docs.astral.sh/uv/) (Python 3.12). There
are **two installation surfaces**, and it is important to tell them apart:

- `uv sync` installs only the tooling to **build the site** (nbconvert,
  jupyterlab, etc.). The converter is pure Python and does **not** install
  `qcfinancial`. With this, **the notebooks cannot be run**.
- `uv sync --extra notebooks` additionally installs the **notebook execution
  surface** (`qcfinancial`, `pandas`, `numpy`, `holidays`, `openpyxl`,
  `pydantic`). **This is the command anyone cloning the repo must use to run the
  notebooks.**

```bash
git clone <repo>
cd qcfinancial-docs
uv sync --extra notebooks   # required to run the notebooks
uv run jupyter lab
```

> **Note on `qcfinancial`:** it is a compiled extension and publishes *wheels*
> only for some platforms. If `uv sync --extra notebooks` fails because there is
> no *wheel* for your system, you must obtain the compiled module
> (`qcfinancial.cpython-*.so`) by other means and place it at the repo root.

- In every notebook, the library is meant to be imported with `import qcfinancial as qcf`.
- The notebooks read data from `./input` by relative path: run them from the repo root.

## Notebook summary
Below is a short summary of each notebook, with direct links inside the repo:

1. 1_Objetos_Fundamentales.ipynb — Introduction to qcfinancial's base objects: currencies (QCCurrency), dates (QCDate), rates, and assorted utilities.
   - Link: ./1_Objetos_Fundamentales.ipynb

2. 2_Cashflows.ipynb — Simple and multicurrency cashflows; `show` and `get_column_names` functions; formatting with pandas.
   - Link: ./2_Cashflows.ipynb

3. 3_Construccion_Operaciones.ipynb — Building trades from legs (Legs): examples with `FixedRateLeg` and key parameters (RecPay, Tenor, StubPeriod, calendars, etc.).
   - Link: ./3_Construccion_Operaciones.ipynb

4. 4_Valorizacion_Sensibilidad.ipynb — Zero-coupon curves, leg valuation, and sensitivity calculation. Includes numeric vectors, curves, and interpolators.
   - Link: ./4_Valorizacion_Sensibilidad.ipynb

5. 5_SwapICPCLP.ipynb — Setup of a market ICPCLP-vs-fixed-rate swap, with default values and construction of both legs.
   - Link: ./5_SwapICPCLP.ipynb

6. 6_Curva_SOFR.ipynb — Construction of the SOFR zero curve from fixed-vs-float swaps using bootstrapping and Newton-Raphson.
   - Link: ./6_Curva_SOFR.ipynb

7. 7_Templates_unfinished.ipynb — Draft templates for assisted trade construction, class patterns, and wrappers (`qcf_wrappers`).
   - Link: ./7_Templates_unfinished.ipynb

8. 90_Valorizacion_Sensibilidad_Tests.ipynb — Test variant for valuation and sensitivity, with structures similar to notebook 4.
   - Link: ./90_Valorizacion_Sensibilidad_Tests.ipynb

9. 98_Pruebas_Construccion_Operaciones.ipynb — Additional tests and examples of leg and trade construction; useful for validating parameters and edge cases.
   - Link: ./98_Pruebas_Construccion_Operaciones.ipynb

10. 99_Ejemplo_Forward_BTU.ipynb — Example valuing a BTU forward (CLP bond): present value, price, and M2M at a valuation date.
    - Link: ./99_Ejemplo_Forward_BTU.ipynb

11. Ejemplos_qcfinancial_2b.ipynb — Additional set of library usage examples (subject to notebook availability).
    - Link: ./Ejemplos_qcfinancial_2b.ipynb

## Auxiliary files
- aux_functions.py — Helper functions (e.g., `leg_as_dataframe`, formatting and calendar utilities).
- qcf_wrappers.py — Wrappers and utilities to simplify object construction (used in some notebooks).

## Notes
- Some examples require data from `./input` (e.g., 6_Curva_SOFR.ipynb uses `20240621_sofr_data.xlsx`).
- Notebooks marked "Templates" or "Pruebas" (Tests) may contain experimental code or optional dependencies.

Last updated: 2025-09-23 15:19
