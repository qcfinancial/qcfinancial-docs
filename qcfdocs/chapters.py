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
    slug: str          # output filename stem, e.g. "1_objetos_fundamentales" -> .html
    title: str         # display title (also the notebook's first H1)
    notebook: str      # source .ipynb stem (no extension)
    src_md: str        # generated markdown stem under docs/ (no extension)

    @property
    def html_name(self) -> str:
        return f"{self.slug}.html"

    @property
    def md_name(self) -> str:
        return f"{self.src_md}.md"

    @property
    def ipynb_name(self) -> str:
        return f"{self.notebook}.ipynb"

    @property
    def num2(self) -> str:
        return f"{self.number:02d}"


# Chapters 1-4: the prototyped set with TRANSFORM_SPEC validation counts.
CHAPTERS: list[Chapter] = [
    Chapter(1, "1_objetos_fundamentales", "Objetos Fundamentales",
            "1_Objetos_Fundamentales", "1_Objetos_Fundamentales"),
    Chapter(2, "2_cashflows", "Cashflows",
            "2_Cashflows", "2_Cashflows"),
    Chapter(3, "3_construccion_operaciones", "Construcción de Operaciones",
            "3_Construccion_Operaciones", "3_Construccion_Operaciones"),
    Chapter(4, "4_valorizacion_sensibilidad", "Valorización y Sensibilidad",
            "4_Valorizacion_Sensibilidad", "4_Valorizacion_Sensibilidad"),
]
