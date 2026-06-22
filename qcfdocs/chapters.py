"""Chapter manifest -- the single source of truth for the docs site.

Drives nbconvert targets (notebook -> ``docs/<src_md>``), the sidebar nav,
the prev/next pager, the page title, and output filenames. Add chapters 5-6
here when their notebooks are ready; ``number`` controls ordering and the
two-digit nav badge.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Chapter:
    number: int
    slug: str                  # output filename stem, e.g. "2_cashflows" -> .html
    title: str                 # short label for the sidebar nav
    src_md: str                # source markdown stem under docs/ (no extension)
    notebook: str | None = None  # source .ipynb stem; None for hand-written pages (e.g. the home)

    @property
    def html_name(self) -> str:
        return f"{self.slug}.html"

    @property
    def md_name(self) -> str:
        return f"{self.src_md}.md"

    @property
    def ipynb_name(self) -> str | None:
        return f"{self.notebook}.ipynb" if self.notebook else None

    @property
    def num2(self) -> str:
        return f"{self.number:02d}"


# Chapter 0 is the hand-written landing page (docs/0_index.md -> index.html, no
# notebook). Chapters 1-6 are generated from the chapter notebooks. The sidebar
# `title` is a short label; each page's H1 comes from the document's own first
# heading (so e.g. ch5 reads "Configurar un SwapICPCLP de Mercado").
CHAPTERS: list[Chapter] = [
    Chapter(0, "index", "Inicio", "0_index"),
    Chapter(1, "1_objetos_fundamentales", "Objetos Fundamentales",
            "1_Objetos_Fundamentales", "1_Objetos_Fundamentales"),
    Chapter(2, "2_cashflows", "Cashflows",
            "2_Cashflows", "2_Cashflows"),
    Chapter(3, "3_construccion_operaciones", "Construcción de Operaciones",
            "3_Construccion_Operaciones", "3_Construccion_Operaciones"),
    Chapter(4, "4_valorizacion_sensibilidad", "Valorización y Sensibilidad",
            "4_Valorizacion_Sensibilidad", "4_Valorizacion_Sensibilidad"),
    Chapter(5, "5_swapicpclp", "Swap ICPCLP",
            "5_SwapICPCLP", "5_SwapICPCLP"),
    Chapter(6, "6_curva_sofr", "Curva SOFR",
            "6_Curva_SOFR", "6_Curva_SOFR"),
]
