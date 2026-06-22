# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

This is the **documentation** repo for `qcfinancial` — a C++/Python library (imported as `import qcfinancial as qcf`) for pricing interest-rate and FX derivatives. This repo contains **no library source code**; it is a set of executable Jupyter notebooks that teach the library by example, plus a custom static-site generator (`qcfdocs/`) that publishes them. Content and most prose are in **Spanish** — match that language when editing notebooks or docs.

`qcfinancial` is a compiled extension. It publishes wheels **only for macOS arm64 and Linux x86_64** — there is **no macOS Intel (x86_64) wheel**. On an Intel Mac it is provided out-of-band as a vendored `qcfinancial.cpython-*.so` (gitignored). You cannot read its source here; learn its API from the notebooks and from `qcf_wrappers.py`.

## Environment (uv)

The project is managed with **uv** (`pyproject.toml`, `uv.lock`, Python pinned to 3.12 via `.python-version`).

- `uv sync` — create `.venv` and install the **docs build toolchain** (`[tool.uv] dev-dependencies`: nbconvert, jupyterlab, ipykernel, pytest). This is all you need to build the site.
- `uv sync --extra notebooks` — additionally install the **notebook execution surface** (`[project.optional-dependencies] notebooks`: qcfinancial, pandas, numpy, holidays, openpyxl, pydantic). Needed only to *re-run* the notebooks. On macOS Intel this install fails (no qcfinancial wheel) — use the vendored `.so` instead.
- `uv run jupyter lab` — run the notebooks.

The project itself (`qcfinancial-docs`) has **no install-time runtime deps**: the site converter is pure standard library.

## Build pipeline

Two stages, both exposed via the `qcf-docs` CLI (`qcfdocs/cli.py`):

1. **Notebooks → `docs/*.md`**: `uv run qcf-docs notebooks` runs `jupyter nbconvert --to markdown` over the chapter notebooks **as-is** (no re-execution; outputs come from whatever is saved in the `.ipynb`). It overrides `Exporter.preprocessors=[]` to neutralize stale `jupyter_contrib_nbextensions` entries in the user/system Jupyter config. Implemented in `qcfdocs/notebooks.py`.
2. **`docs/*.md` → static site**: `uv run qcf-docs build` reads the committed `docs/*.md`, converts each to branded HTML, and writes `site/` (gitignored). Implemented in `qcfdocs/build.py`.

So: **editing a notebook does not change the site until you run `qcf-docs notebooks` (regenerating `docs/*.md`) and commit.** The committed `docs/*.md` are the source of truth the site is built from.

**Scope:** only chapters **1–4** are wired into the site (see `qcfdocs/chapters.py`). Notebooks 5–7, `90_*`, `98_*`, `99_*`, `Ejemplos_*` are extra/test/WIP and not built — add chapters 5–6 by extending the manifest.

**Publish:** CI (`.github/workflows/ci.yml`) runs `uv run --no-dev qcf-docs build` on push to `master`/`main` and deploys `site/` to GitHub Pages via `actions/deploy-pages`. This **requires** Pages source set to "GitHub Actions" in repo Settings. The site converter needs neither the dev toolchain nor qcfinancial at deploy time.

## The site generator (`qcfdocs/`)

A pure-stdlib package (no runtime deps). Key modules:

- `convert.py` — **a 1:1 port of `new-site/transform.reference.js`**. `render_notebook(md) -> Rendered(html, toc, title)` walks the nbconvert markdown (block order: code-fence → heading → display-math → pipe-table → paragraph) and emits `.nb-*` HTML. DataFrame Styler HTML and `$…$`/`$$…$$` math pass through unescaped; code/text are escaped. **Keep this byte-for-byte equal to the reference** — `tests/test_counts.py` asserts parity against `new-site/reference/sample_output_ch1.html`. If you change it, re-verify with that test (and optionally `node` over `transform.reference.js`).
- `chapters.py` — the `CHAPTERS` manifest (number, slug, title, notebook, src_md). Single source of truth for nbconvert targets, sidebar nav, pager, and output filenames.
- `build.py` — fills `templates/page.html` slots (`{{NAV}}`, `{{CHTITLE}}`, `{{CONTENT}}`, `{{TOC}}`, `{{PAGER}}`, `{{CSS}}`, `{{IPYNB}}`) per chapter; writes `site/<slug>.html` + `index.html` + `qcf-docs.css`.
- `templates/` — `page.html` (the shell, with placeholder slots) and `qcf-docs.css` (**the visual contract — never hand-port inline styles; add classes to the CSS instead**). These are the productionized copies of `new-site/page-shell.html` and `new-site/qcf-docs.css`.

`new-site/` remains the **design reference** (README, `TRANSFORM_SPEC.md`, `transform.reference.js`, `reference/` golden samples). Its `TRANSFORM_SPEC.md` block counts were measured against `reference/sample_notebook.md`, an older ch01 snapshot — the live `docs/*.md` have since drifted, so don't expect those exact counts from current chapters. The test pins to the sample, not the live docs.

## Tests

`uv run pytest` — validates the converter: golden byte-parity + spec counts on the bundled sample, and a parse sanity check on the live `docs/*.md`.

## Repo layout

- `N_*.ipynb` (root) — chapter notebooks (`N` = order). `90_*`/`98_*` are test/validation, `99_*`/`Ejemplos_*` are extra examples, `7_Templates_unfinished` is WIP.
- `docs/` — committed nbconvert markdown; the input to the site build.
- `input/` — CSV/XLSX market data the notebooks read; keep paths stable.
- `aux_functions.py` — notebook helpers: `leg_as_dataframe(leg)` wraps a `qcf.Leg` into a `pd.DataFrame`, `get_business_calendar(...)` builds a `qcf.BusinessCalendar` from the `holidays` package, `format_dict` maps column names → display formats.
- `qcf_wrappers.py` — Pydantic enums/dataclasses wrapping raw `qcf` objects with `.as_qcf()` converters (`Currency`, `BusAdjRules`, `StubPeriods`, …). The readable Python-side vocabulary for the C++ API.
- `deprecated/`, `other/` — old notebooks; not current.

## Conventions when editing notebooks

- Always import as `import qcfinancial as qcf`.
- Display legs/cashflows via `aux_functions.leg_as_dataframe(...)` and style with `format_dict`, rather than printing raw objects.
- Notebooks read market data from `input/` by relative path; run from the repo root so those paths resolve.
- After changing a chapter notebook, run `uv run qcf-docs notebooks` and commit the regenerated `docs/*.md` so the site reflects it.
