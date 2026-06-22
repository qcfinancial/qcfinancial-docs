# Transform spec: notebook markdown → documentation HTML

This is the exact mapping the production converter must implement. The reference
implementation (`transform.reference.js`) realizes every rule below and is
verified to reproduce the approved prototype. Port it to Python; keep the rules
and the **order of checks** identical.

## Input

The source is NOT raw `.ipynb`. The existing mkdocs pipeline
(`qcfinancial/qcfinancial-docs`, `docs/*.md`) already serializes each executed
notebook to **nbconvert-style markdown**:

- Code cells → fenced ` ```python … ``` ` blocks.
- Text/stream/`repr` outputs → **4-space-indented** blocks immediately after the cell.
- `DataFrame` / pandas `Styler` outputs → **raw HTML** (`<style>…</style><table id="T_…">…</table>`) immediately after the cell.
- Prose → ordinary markdown (headings, paragraphs, pipe tables, inline `code`/`**bold**`/links).
- Math → `$…$` (inline) and `$$…$$` (display), MathJax/arithmatex syntax.

> If the pipeline ever switches to converting `.ipynb` directly, the cleanest
> production path is an **nbconvert custom template/exporter** whose blocks emit
> the markup below. Either way the output contract (the `.nb-*` classes) is the same.

In chapters 01–04 there are **no** images, mermaid diagrams, or admonitions —
but the shell + CSS support admonitions (`.nb-admonition`) for later chapters.

## Block grammar (walk top-to-bottom; first match wins)

| # | Detect (on the current line) | Emit | Notes |
|---|------------------------------|------|-------|
| 1 | ` ``` ` fence | `codeCell()` → `.nb-cell--code` + `In[n]`, then scan its output | `n` = running code-cell counter (`exec`), starts at 1 |
| 1a | …followed (past blanks) by a line matching `^\s*<(style\|table\|div)`  | `dfCell()` → `.nb-df` with the raw HTML **injected verbatim** | collect until a blank line *after* the block closes (`</table>`/`</div>`) |
| 1b | …followed (past blanks) by a 4-space-indented line | `outCell()` → `.nb-out` mono `<pre>`, text **escaped** | strip 4 leading spaces; a blank line stays in the block only if more indented lines follow |
| 2 | `^#{1,6}\s` heading | `heading()` | first `#` (H1) = page title (NOT emitted in body); H2/H3 also pushed to TOC |
| 3 | `^\$\$` | `mathBlock()` → `.nb-math`, raw `$$…$$` | single- or multi-line; MathJax typesets client-side |
| 4 | `^\s*\|` | `mdTable()` → `.nb-table` | row 0 = header, row 1 = `---` separator (skipped), rest = body |
| 5 | anything else | paragraph `.nb-p` | greedily consume until blank line or the start of blocks 1–4 |

Output text and code are **HTML-escaped**; pandas DataFrame HTML and math are
passed through **unescaped** (they are trusted generator output). Inline markdown
(`` `code` ``, `**bold**`, `[t](url)`, `*em*`) is rendered inside paragraphs and
table cells; `$…$` is left untouched for MathJax.

## Output → markup (1:1 with `qcf-docs.css`)

| Construct | Markup |
|-----------|--------|
| Code cell | `.nb-cell.nb-cell--code` > `.nb-prompt--in` (`In[n]:`) + `.nb-in` (bar with chevron/lang/copy + `pre.nb-in__code`) |
| Text output | `.nb-cell.nb-cell--out` > `.nb-prompt--out` (`Out[n]:`) + `.nb-out` > `pre.nb-out__pre` |
| DataFrame | `.nb-cell.nb-cell--out` > `.nb-prompt--out` + `.nb-df` (raw Styler HTML inside; styled by descendant CSS) |
| H2 / H3 / H4 | `h2.nb-h2` / `h3.nb-h3` / `h4.nb-h4` with `id=slug(text)` |
| Paragraph | `p.nb-p` |
| Pipe table | `.nb-table > table` |
| Display math | `.nb-math` (raw `$$…$$`) |
| Admonition | `.nb-admonition` (icon + title + body) |

## Python syntax highlighter

`highlightPython(code)` emits `<span class="tok-*">`. Classification:

- `#…` → `tok-comment` (to EOL)
- `"…"` `'…'` `f"…"` triple-quoted → `tok-string` (handles `\` escapes)
- numeric literal not inside an identifier (`123`, `1_000_000`, `0x..`, `1e-3`) → `tok-number`
- Python keyword → `tok-keyword` (see `PY_KEYWORDS` set)
- name immediately followed by `(` → `tok-call`
- name immediately preceded by `.` → `tok-attr`
- everything else → plain (escaped)

Token colors live in `qcf-docs.css` `:root` (`--tok-*`). This is a pragmatic
documentation highlighter, **not** a full lexer — if you prefer, swap in Pygments
on the Python side and map its token classes onto `--tok-*`.

## Interactions the static page owns

1. **Collapsible code cells** — toggle `.is-collapsed` on `.nb-in` (hides `.nb-in__code`, rotates `.nb-in__chevron`, shows `.nb-in__hidden` "···"). The chevron/bar is the control; the whole bar is clickable.
2. **MathJax** — config in `<head>` (`inlineMath $…$`, `displayMath $$…$$`, skip `pre/code`); call `typesetPromise()` after content mounts.
3. **TOC scroll-spy** (optional) — mark the in-view H2 `.is-active`. Never use `scrollIntoView`; anchor `href="#id"` jumps suffice.

## Validation (parser must reproduce these counts)

Run `transform.reference.js` over the four `docs/*.md`; totals across 01–04:

| Chapter | code | text out | DataFrame | H2 | H3 |
|--------|-----:|---------:|----------:|---:|---:|
| 01 Objetos Fundamentales | 77 | 58 | 0 | 11 | 32 |
| 02 Cashflows | 165 | 107 | 12 | 11 | 59 |
| 03 Construcción de Operaciones | 71 | 5 | 20 | 12 | 3 |
| 04 Valorización y Sensibilidad | 117 | 53 | 13 | 3 | 12 |
| **Total** | **430** | **223** | **45** | — | — |

Plus 1 markdown table and 2 display-math blocks (both in ch01). The walk
terminates cleanly on every file (no stalls).

## Gotcha that shaped the architecture

In the prototype's sandbox, `fetch()` of project files is blocked (401
"preview token required"), so the notebook sources are bundled into a JS data
module (`nbsources.js` → `window.QCF_NB`) loaded via `<script src>` rather than
fetched at runtime. **This is a sandbox quirk, not a production constraint** — a
real build reads the `.md`/`.ipynb` straight from disk in the build step and
writes static HTML. Mentioned so the prototype's data-loading path isn't mistaken
for a requirement.
