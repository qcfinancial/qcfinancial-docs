#!/bin/bash
set -e

NOTEBOOKS=(
    "1_Objetos_Fundamentales"
    "2_Cashflows"
    "3_Construccion_Operaciones"
    "4_Valorizacion_Sensibilidad"
    "5_SwapICPCLP"
    "6_Curva_SOFR"
)

source .venv/bin/activate

for nb in "${NOTEBOOKS[@]}"; do
    echo "Converting ${nb}.ipynb ..."
    jupyter nbconvert --to markdown "${nb}.ipynb"
    mv "${nb}.md" docs/
done

echo "Done. All notebooks converted and moved to docs/"
