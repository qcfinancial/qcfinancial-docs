"""Assemble the branded static site from the generated ``docs/*.md``.

For each chapter: read ``docs/<src_md>.md`` -> :func:`qcfdocs.convert.render_notebook`
-> fill the ``page.html`` slots (nav / title / content / toc / pager) -> write
``site/<slug>.html``. Copies the CSS contract and writes an ``index.html`` that
points at the first chapter. The look is owned entirely by ``qcf-docs.css``.
"""

from __future__ import annotations

import shutil
from importlib import resources
from pathlib import Path

from . import convert
from .chapters import CHAPTERS, Chapter

# Repo root = two levels up from this file (qcfdocs/build.py -> repo/).
REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"
SITE_DIR = REPO_ROOT / "site"
GITHUB_NB_BASE = "https://github.com/qcfinancial/qcfinancial-docs/blob/master"


def _template(name: str) -> str:
    return resources.files("qcfdocs.templates").joinpath(name).read_text(encoding="utf-8")


def _nav_html(current: Chapter) -> str:
    items = []
    for ch in CHAPTERS:
        active = " is-active" if ch.number == current.number else ""
        items.append(
            f'          <a class="qcf-nav__item{active}" href="{ch.html_name}">'
            f'<span class="qcf-nav__num">{ch.num2}</span>{ch.title}</a>'
        )
    return "\n".join(items)


def _toc_html(toc: list[dict]) -> str:
    if not toc:
        return '          <span class="qcf-toc__empty">—</span>'
    items = []
    for idx, h in enumerate(toc):
        cls = "qcf-toc__item"
        if h["level"] == 3:
            cls += " lvl-3"
        if idx == 0:
            cls += " is-active"
        items.append(f'          <a class="{cls}" href="#{h["id"]}">{h["text"]}</a>')
    return "\n".join(items)


def _pager_html(current: Chapter) -> str:
    by_num = {c.number: c for c in CHAPTERS}
    prev_ch = by_num.get(current.number - 1)
    next_ch = by_num.get(current.number + 1)

    if prev_ch:
        left = (
            f'          <a class="qcf-pager__link" href="{prev_ch.html_name}">\n'
            f'            <div class="qcf-pager__eyebrow">&larr; Anterior</div>\n'
            f'            <div class="qcf-pager__title">{prev_ch.title}</div>\n'
            f'          </a>'
        )
    else:
        left = '          <span class="qcf-pager__spacer"></span>'

    if next_ch:
        right = (
            f'          <a class="qcf-pager__link qcf-pager__link--next" href="{next_ch.html_name}">\n'
            f'            <div class="qcf-pager__eyebrow">Siguiente &rarr;</div>\n'
            f'            <div class="qcf-pager__title">{next_ch.title}</div>\n'
            f'          </a>'
        )
    else:
        right = '          <span class="qcf-pager__spacer"></span>'

    return f'        <nav class="qcf-pager">\n{left}\n{right}\n        </nav>'


def _callout_html(ch: Chapter) -> str:
    """Sidebar callout linking to the source notebook (omitted for hand-written pages)."""
    if not ch.notebook:
        return ""
    return (
        '        <div class="qcf-callout">\n'
        '          <div class="qcf-callout__title">Generado desde notebooks</div>\n'
        '          <p class="qcf-callout__body">Esta página se renderiza directamente '
        'desde el .ipynb ejecutable. Córrelo tú mismo.</p>\n'
        f'          <a class="qcf-callout__link" href="{GITHUB_NB_BASE}/{ch.ipynb_name}" '
        'target="_blank" rel="noopener">.ipynb &darr;</a>\n'
        '        </div>'
    )


def _plain_title(text: str) -> str:
    """Strip markdown code/emphasis markers for use in text contexts (title, h1)."""
    return text.replace("`", "")


def _fill(template: str, mapping: dict[str, str]) -> str:
    out = template
    for key, value in mapping.items():
        out = out.replace("{{" + key + "}}", value)
    return out


def build(docs_dir: Path = DOCS_DIR, site_dir: Path = SITE_DIR) -> list[Path]:
    """Build every chapter into ``site_dir``. Returns the written HTML paths."""
    site_dir.mkdir(parents=True, exist_ok=True)
    template = _template("page.html")
    css = _template("qcf-docs.css")
    (site_dir / "qcf-docs.css").write_text(css, encoding="utf-8")

    written: list[Path] = []
    for ch in CHAPTERS:
        md_path = docs_dir / ch.md_name
        if not md_path.exists():
            raise FileNotFoundError(
                f"Missing {md_path}. Run `qcf-docs notebooks` to generate it first."
            )
        rendered = convert.render_notebook(md_path.read_text(encoding="utf-8"))
        page = _fill(template, {
            "CHTITLE": _plain_title(rendered.title or ch.title),
            "CSS": "qcf-docs.css",
            "CALLOUT": _callout_html(ch),
            "NAV": _nav_html(ch),
            "CONTENT": rendered.html,
            "TOC": _toc_html(rendered.toc),
            "PAGER": _pager_html(ch),
        })
        out_path = site_dir / ch.html_name
        out_path.write_text(page, encoding="utf-8")
        written.append(out_path)

    return written


if __name__ == "__main__":
    paths = build()
    print(f"Built {len(paths)} chapter pages into {SITE_DIR}/")
