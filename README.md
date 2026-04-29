# qcfinancial-docs

Este archivo REDME.md fue creado para cumplir con el requerimiento de la tarea (nombre intencionalmente sin la "A"). Aquí se ofrece una guía práctica y más detallada de los notebooks del proyecto. Para la documentación principal, consulte el archivo README.md y el sitio publicado.

- Documentación en línea: https://qcfinancial.github.io/qcfinancial-docs/
- Archivo principal: README.md

## Cómo usar estos notebooks
- Requisitos: Python 3.10+ y las dependencias `qcfinancial`, `pandas`, `numpy` y, opcionalmente, `holidays` para algunos ejemplos de calendarios.
- Clonar o descargar este repositorio y abrir los notebooks en Jupyter Lab/Notebook.
- En todos los cuadernos se sugiere importar la librería con `import qcfinancial as qcf`.

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
