# Handoff: qcfinancial notebook → documentation site

> **Status: ported and live.** The production converter described in this handoff
> now lives in the `qcfdocs/` package at the repo root. `transform.reference.js`
> was ported 1:1 to `qcfdocs/convert.py`, and the productionized copies of
> `qcf-docs.css` + `page-shell.html` live in `qcfdocs/templates/`. Build with
> `uv run qcf-docs build`; the converter is pinned to the golden output here via
> `tests/test_counts.py`. The files in this folder are kept as the **design
> reference / source of truth for look and behavior**.

## Overview
Turn the project's executable Jupyter notebooks into a branded documentation
site. The source notebooks are serialized to markdown by the existing mkdocs
pipeline (`qcfinancial/qcfinancial-docs`, `docs/*.md`); a converter maps each
notebook construct to styled "doc cells" (In/Out code cells, text outputs,
pandas DataFrames, headings, tables, LaTeX) inside a three-column docs shell.

## About the design files
The files here are a **design reference**, not production code to ship as-is:
- `qcf-docs.css` + `page-shell.html` are the **visual contract** — the exact look (colors, type, spacing, cells) as a real CSS class system + static page skeleton.
- `transform.reference.js` is a **runnable reference implementation** of the notebook→HTML transform. It is the algorithm to port, not a dependency to bundle.
- `reference/QcFinancial Docs Render.dc.html` is the original interactive prototype (React-style); read it as the working source of truth for behavior.

Your task: build the **production converter** (recommended: a Python library/CLI
run in CI) that reads the notebooks and emits static HTML targeting
`qcf-docs.css`. Recreate the look using the CSS contract here — do not hand-port
inline styles.

## Fidelity
**High-fidelity.** Colors, typography, spacing, and the per-cell markup are
final and exact. Match `qcf-docs.css`/`page-shell.html` pixel-for-pixel.

## Recommended architecture
```
notebooks/*.ipynb ──(mkdocs/nbconvert serialize)──▶ docs/*.md
        │
        ▼  converter (Python lib/CLI, in CI — THIS is what you build)
   static docs HTML  ──targets──▶ qcf-docs.css  (the theme contract)
                                  page-shell.html (the shell)
```
- Notebooks are the source of truth for **content**; `qcf-docs.css` is the source of truth for **look**. Regenerate pages on every notebook change — never hand-edit generated HTML.
- Two viable converter implementations: (a) **nbconvert custom template/exporter** whose blocks emit the `.nb-*` markup (reuses Jupyter's execution + markdown); (b) a **standalone parser** over the serialized `.md` exactly like `transform.reference.js`. Start with whichever fits the existing build; the output contract is identical.

## Screens / views
One screen: **a documentation page** (repeated per chapter). Layout:
- **Top bar** (sticky, 59px): logo lockup (navy badge `ℚℂ` + italic "financial" + `docs` tag) · search field (280px) · EN/ES segmented toggle · GitHub icon.
- **Grid** `268px / minmax(0,1fr) / 232px`, max-width 1480px, centered.
  - **Left sidebar** (sticky, own scroll): "Guía" eyebrow + chapter nav (number + title; current `.is-active` = navy fill) + "Generado desde notebooks" callout.
  - **Main**: breadcrumb · H1 (38px/600/-1.1px) + "Abrir en la demo" button · hairline · **notebook body** (the converted cells) · prev/next pager.
  - **Right TOC** (sticky): "En esta página" + H2/H3 anchors (active = navy left-border).

The notebook body and its cell markup are specified exactly in **`TRANSFORM_SPEC.md`**;
`page-shell.html` shows one worked example of every block type.

## Interactions & behavior
- **Collapsible code cells**: clicking a cell's header bar toggles `.is-collapsed` on `.nb-in` — hides the code, rotates the chevron, shows a `···` marker. Each cell is independent.
- **EN/ES toggle**: see "Making the EN/ES toggle work for notebooks" below.
- **MathJax**: `$…$` inline, `$$…$$` display; configured to skip `pre/code`; `typesetPromise()` after content mounts.
- **TOC** (optional scroll-spy): mark in-view H2 active. Use anchor `href="#id"`; never `scrollIntoView`.
- Hover states for nav items, pager links, code-cell header, df rows — all in `qcf-docs.css`.

## Making the EN/ES toggle work for notebooks
The toggle has **two layers**, and only the first is built in the prototype:

1. **UI chrome + chapter titles (done).** A small string dictionary keyed by
   language (`{ es: {...}, en: {...} }`) drives search placeholder, nav group,
   breadcrumb, callout, TOC heading, pager, demo button, and the four chapter
   titles. Switching `lang` re-renders these. In the prototype this is the `STR`
   and `titles` maps in the logic class; in production it's a tiny i18n table.

2. **Notebook body content (not built — here's how).** The prototype renders one
   language because there is only a Spanish notebook set. To make the body
   bilingual, give the converter **parallel source notebooks per language** and
   emit **one HTML page per (chapter × language)**:

   ```
   notebooks/es/1_Objetos_Fundamentales.ipynb     notebooks/en/1_Fundamental_Objects.ipynb
   notebooks/es/2_Cashflows.ipynb                 notebooks/en/2_Cashflows.ipynb
        │                                                │
        ▼ converter (same transform, per language)      ▼
   docs/es/1_objetos_fundamentales.html           docs/en/1_fundamental_objects.html
   ```

   The transform itself is **language-agnostic** — it never inspects prose — so
   you run the exact same `transform.reference.js`/Python converter over each
   language's notebooks. The toggle then becomes **navigation**: ES/EN swap the
   URL between the matching pages (e.g. `/es/…` ⇄ `/en/…`, preserving the chapter
   slug and `#hash`), rather than re-rendering in place.

   Practical notes:
   - **Pair pages by a stable key** (chapter number), not by filename, since
     titles/slugs differ across languages. Keep a small manifest
     `{ "1": { es: "…", en: "…" }, … }` mapping chapter № → per-language slug so
     the toggle and the prev/next pager can resolve the sibling URL.
   - **Code cells are identical across languages** — only markdown prose (and
     sometimes `print`/comment strings) differ. Translating notebooks means
     translating the markdown cells; the code and outputs carry over.
   - **Fallback**: if a chapter has no `en` notebook yet, point EN at the `es`
     page (or hide EN for that chapter) so the toggle never 404s.
   - **Single-page-app variant** (matches the prototype's in-place feel): instead
     of separate URLs, the converter can emit both languages' bodies into one
     page and the toggle shows/hides the active one — heavier payload, but no
     navigation. The per-language-page approach above is recommended for a static
     site (smaller pages, better SEO, real per-language URLs).
All tokens live in `qcf-docs.css` `:root`. Key values:
- **Ink/brand**: ink `#0b1b34`, navy `#0c2a66`, logo-navy `#0b1d42`, teal `#11a89f`, teal-deep `#0e8f8a`, orange (Out) `#b85c00`.
- **Text ramp**: body `#3c4a64`, muted `#516183`, faint `#8593aa`/`#93a0b6`/`#aab4c6`.
- **Surfaces**: bg `#fff`, soft `#f7f9fc`, code `#fbfcfe`, input `#f4f6fb`; borders `#e7ecf4`/`#eef1f7`/`#f0f3f8`; cream (glyph) `#f5f1e6`; teal panel `#e9f7f5`/`#c9ece8`; inline-code bg `#eef2f8`.
- **Syntax**: comment `#8a93a3`, keyword `#8250df`, string `#0e7c77`, number `#b35900`, call `#0c5fd6`, attr `#0b1b34`.
- **Type**: IBM Plex Sans (UI/headings), IBM Plex Mono (code/labels/data), STIX Two Math + STIX Two Text italic (logo only). Scale: H1 38/600/-1.1px · H2 23/600/-0.4px · H3 18/600 · H4 15/600 · body 16/1.7 · code 13 mono/1.7 · output 13 mono/1.6 · df 12.5 mono.
- **Geometry**: cell radius 10px, panel/pager 12px; code cell 3px navy left rail; In/Out prompt gutter 58px; prose max-width 760px.

## Assets
- Fonts via Google Fonts (IBM Plex) + jsDelivr `@fontsource/stix-two-math@5`, `@fontsource/stix-two-text@5/500-italic`.
- MathJax 3 (`tex-mml-chtml`) via unpkg.
- Icons are inline SVG (search, github, play, info, chevron) — already in `page-shell.html`. No raster assets.
- Logo: the mark is blackboard-bold `ℚℂ` (STIX Two Math) + "financial" in STIX Two Text italic. (Clean SVG/PNG/favicon export is still a TODO in the main project.)

## Files in this bundle
- `README.md` — this file.
- `qcf-docs.css` — the theme contract (all styling; classes documented inline).
- `page-shell.html` — static page skeleton with `{{ nav }}/{{ chTitle }}/{{ content }}/{{ toc }}/{{ pager }}` slots and one worked example per block type.
- `TRANSFORM_SPEC.md` — the precise notebook-markdown → markup mapping, highlighter rules, interactions, and validation counts.
- `transform.reference.js` — runnable, dependency-free reference parser (`renderNotebook(md) → {html, toc, title}`). Node: see header comment.
- `reference/QcFinancial Docs Render.dc.html` — original interactive prototype (behavioral source of truth).
- `reference/sample_notebook.md` — a real source chapter (Objetos Fundamentales) to test against.
- `reference/sample_output_ch1.html` — the fragment `transform.reference.js` produces from it.
- `reference/sample_page_ch1.html` — that fragment wrapped in the shell (open in a browser to see the target result).

## Quick start
```bash
node -e "const{renderNotebook}=require('./transform.reference.js');\
const fs=require('fs');const md=fs.readFileSync('reference/sample_notebook.md','utf8');\
fs.writeFileSync('out.html',renderNotebook(md).html);"
# then wrap out.html in page-shell.html's {{ content }} slot (with qcf-docs.css linked)
```
Open `reference/sample_page_ch1.html` to see exactly what "done" looks like.
