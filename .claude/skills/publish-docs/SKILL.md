---
name: publish-docs
description: Run the full documentation publishing pipeline for qcfinancial-docs — regenerate docs/*.md from the notebooks, build the site, run tests, then commit and push so CI deploys to GitHub Pages. Use after finishing a change to a chapter notebook or adding a new chapter notebook.
---

# Publish the docs

Runs the end-to-end publish pipeline for this repo. The user invokes this after
they have **finished editing a chapter notebook (and saved it with fresh
outputs)** or **added a new chapter notebook**. Architecture/background is in
`CLAUDE.md`; the human-facing version of this flow is in `CONTRIBUTING.md`.

Work from the repo root. Stop and report if any step fails — do not push a
broken build.

## 1. Preflight

```bash
git rev-parse --abbrev-ref HEAD          # note the branch
git fetch -q origin
git status -s
git rev-list --left-right --count HEAD...@{u} 2>/dev/null || true
```

- If the working tree has **unrelated** uncommitted changes (things the user did
  not just work on — e.g. stray stashable edits), point them out and ask before
  continuing; this skill should only publish notebook + generated-doc changes.
- If the branch is **behind** its upstream, tell the user to `git pull --rebase`
  first and stop (don't auto-merge shared history).
- Ensure the toolchain is present: `uv sync` (installs the dev tools only;
  building the site needs neither qcfinancial nor the notebooks extra).

## 2. New-notebook check

If the user added a **new chapter**, its notebook must be in the manifest first,
or the build will ignore it.

```bash
uv run python -c "from qcfdocs.chapters import CHAPTERS; print([c.notebook for c in CHAPTERS if c.notebook])"
ls [0-9]*_*.ipynb
```

If a new chapter notebook is not listed in `CHAPTERS`, edit
`qcfdocs/chapters.py` to add a `Chapter(...)` entry (give it the next `number`,
a lowercase `slug`, a short nav `title`, and the notebook/`src_md` stems — see
the existing entries). A hand-written page with no notebook uses `notebook=None`.
Then continue. If the user only edited an existing chapter, skip this step.

## 3. Regenerate, build, test

```bash
uv run qcf-docs notebooks    # nbconvert each chapter .ipynb -> docs/*.md (as-is)
uv run qcf-docs build        # render the static site into site/ (local check)
uv run pytest -q             # converter must stay pinned to the reference output
```

If `pytest` fails, stop and report — the converter changed unexpectedly.
`qcf-docs notebooks` does **not** re-run the notebooks; it serializes whatever
outputs are saved in the `.ipynb`, so the user must have run the notebook first.

## 4. Review what changed

```bash
git status -s
git diff --stat -- docs/ qcfdocs/chapters.py
```

Sanity-check that the `docs/*.md` churn matches the notebook(s) the user touched
(and nothing unrelated). `site/` is gitignored and never committed.

## 5. Commit and push

Stage **only** the relevant files: the notebook(s) that changed, their
regenerated `docs/*.md`, and `qcfdocs/chapters.py` if a chapter was added.

```bash
git add <changed_notebook>.ipynb docs/<changed_chapter>.md   # repeat per chapter
# git add qcfdocs/chapters.py                                 # only if a chapter was added
git commit -m "<concise summary of the doc change>

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
git push
```

Write a commit message describing the actual documentation change (e.g.
"Update Cashflows: add overnight-index example"), not "run publish pipeline".

## 6. Report

Confirm the push and remind the user that CI (`.github/workflows/ci.yml`) builds
with `qcf-docs build` and deploys to GitHub Pages
(https://qcfinancial.github.io/qcfinancial-docs/) automatically — usually live
within a minute or two. No manual deploy step is needed.
