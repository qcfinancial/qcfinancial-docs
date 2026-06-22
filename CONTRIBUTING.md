# Contributing

This repo publishes the `qcfinancial` documentation site. The notebooks are the
content; a small generator (`qcfdocs/`) turns them into the branded static site.

## How publishing works

The **source of truth for the site is the committed `docs/*.md`**, not the
notebooks. On every push to `master`/`main`, CI (`.github/workflows/ci.yml`)
runs `uv run --no-dev qcf-docs build` and deploys `site/` to GitHub Pages.

So publishing a change = getting it into `docs/*.md` on `master`.

> **Editing a notebook alone changes nothing.** The site only updates when
> `docs/*.md` is regenerated from the notebook and committed.

## One-time setup

```bash
uv sync                       # docs build toolchain (nbconvert, jupyterlab, pytest)
```

To *run* the notebooks you also need the execution stack:

```bash
uv sync --extra notebooks     # qcfinancial, pandas, numpy, holidays, openpyxl, pydantic
```

On macOS **Intel** this install fails — `qcfinancial` has no Intel wheel
(only macOS arm64 / Linux x86_64). Use the vendored `qcfinancial.cpython-*.so`
instead (gitignored). The publish path below never imports qcfinancial, so it
works anywhere, including CI.

## Workflow: you edited a notebook

**The easy path — let the skill do it.** In Claude Code, after you've run the
notebook and saved it, run `/publish-docs`. It regenerates `docs/*.md`, builds,
tests, then commits and pushes (CI deploys). See
`.claude/skills/publish-docs/SKILL.md`. The manual steps below are what it does.

```bash
# 1. Run the notebook so its saved outputs are fresh
uv run jupyter lab            # run cells, save the .ipynb

# 2. Regenerate the markdown the site is built from
uv run qcf-docs notebooks

# 3. (optional) preview locally
uv run qcf-docs build
open site/1_objetos_fundamentales.html

# 4. Commit BOTH the notebook and its regenerated markdown
git add 2_Cashflows.ipynb docs/2_Cashflows.md
git commit -m "..."
git push                      # CI builds + deploys to Pages
```

Step 2 is the one people forget. `qcf-docs notebooks` replaces the old
`publish.sh`: same nbconvert step, but driven by the chapter manifest and
hardened against stale global Jupyter config.

## Workflow: you changed the look or the generator

If you touch `qcfdocs/` (converter, templates, `qcf-docs.css`) or
`qcfdocs/chapters.py`, no notebook step is needed:

```bash
uv run pytest                 # keeps the converter pinned to the reference output
uv run qcf-docs build         # eyeball site/ locally
git add qcfdocs/ ...
git commit -m "..."
git push
```

The visual contract lives entirely in `qcfdocs/templates/qcf-docs.css` — add
CSS classes there rather than inline styles in the generator.

## Scope

The site builds chapter **0** (the hand-written home, `docs/0_index.md`) plus
notebook chapters **1–6** (`qcfdocs/chapters.py`). To publish a new chapter, add
an entry to the `CHAPTERS` manifest (use `notebook=None` for a hand-written
page), then run the notebook workflow above.

See `CLAUDE.md` for the architecture and module-level details.
