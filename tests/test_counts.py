"""Pin the Python converter to the approved reference implementation.

The site converter (:mod:`qcfdocs.convert`) is a 1:1 port of
``new-site/transform.reference.js``. Two checks guard it:

* **Golden parity** -- over the committed ``sample_notebook.md`` the port must
  reproduce ``sample_output_ch1.html`` byte-for-byte (the fragment the reference
  JS produces, the approved prototype output).
* **Spec counts** -- the same sample must yield the ``TRANSFORM_SPEC.md`` block
  counts for chapter 01 (code / text-out / DataFrame / H2 / H3 = 77/58/0/11/32).

The live ``docs/*.md`` are intentionally NOT asserted against fixed numbers: they
are regenerated from the notebooks and drift as the notebooks evolve. A loose
sanity test (every chapter parses and has the expected block kinds) covers them.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from qcfdocs.chapters import CHAPTERS
from qcfdocs.convert import render_notebook

ROOT = Path(__file__).resolve().parent.parent
REFERENCE = ROOT / "new-site" / "reference"
DOCS = ROOT / "docs"


def _counts(html: str) -> tuple[int, int, int, int, int]:
    return (
        html.count("nb-cell--code"),
        html.count('class="nb-out"'),   # text outputs (nb-df distinguishes DataFrames)
        html.count('class="nb-df"'),
        html.count('class="nb-h2"'),
        html.count('class="nb-h3"'),
    )


def test_golden_parity():
    """Port output == reference JS output, byte-for-byte, on the bundled sample."""
    md = (REFERENCE / "sample_notebook.md").read_text(encoding="utf-8")
    gold = (REFERENCE / "sample_output_ch1.html").read_text(encoding="utf-8")
    rendered = render_notebook(md)
    assert rendered.html.strip() == gold.strip()
    assert rendered.title == "Objetos Fundamentales"


def test_spec_counts_on_sample():
    """The bundled sample reproduces the TRANSFORM_SPEC.md chapter-01 counts."""
    md = (REFERENCE / "sample_notebook.md").read_text(encoding="utf-8")
    assert _counts(render_notebook(md).html) == (77, 58, 0, 11, 32)


@pytest.mark.parametrize("ch", CHAPTERS, ids=lambda c: c.src_md)
def test_live_docs_parse(ch):
    """Every live chapter parses, yields a title, and produces code cells."""
    md_path = DOCS / ch.md_name
    if not md_path.exists():
        pytest.skip(f"{md_path.name} not generated yet")
    rendered = render_notebook(md_path.read_text(encoding="utf-8"))
    code, *_ = _counts(rendered.html)
    assert rendered.title, f"{ch.md_name} produced no H1 title"
    assert code > 0, f"{ch.md_name} produced no code cells"
