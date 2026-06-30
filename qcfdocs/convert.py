"""Notebook-markdown -> documentation HTML transform.

A 1:1 Python port of ``new-site/transform.reference.js``. The block-walk order
(fence -> heading -> display-math -> pipe-table -> paragraph) and every renderer
mirror the reference implementation, so the output is byte-comparable with the
approved prototype and reproduces the ``TRANSFORM_SPEC.md`` validation counts.

Input  : the markdown emitted by ``jupyter nbconvert --to markdown`` -- code
         cells as ```python fences, text outputs 4-space-indented, pandas Styler
         outputs as raw ``<table id="T_...">`` HTML.
Output : :class:`Rendered` with ``html`` (the ``{{ content }}`` fragment),
         ``toc`` (H2/H3 anchors) and ``title`` (the page's first H1).

Code and text outputs are HTML-escaped; DataFrame Styler HTML and ``$...$`` /
``$$...$$`` math pass through verbatim (trusted generator output).
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field


@dataclass
class Rendered:
    html: str
    toc: list[dict] = field(default_factory=list)
    title: str | None = None


# ---- helpers ---------------------------------------------------------------

def escape_html(s: str) -> str:
    # Matches the reference: only & < > (NOT quotes).
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def slug(s: str) -> str:
    s = s.lower()
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))  # strip accents
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"(^-|-$)", "", s)
    return s


# ---- Python syntax highlighter --------------------------------------------
# Pragmatic documentation highlighter, NOT a full lexer. Emits <span class="tok-*">.

PY_KEYWORDS = {
    "import", "from", "as", "def", "class", "return", "for", "in",
    "if", "else", "elif", "while", "try", "except", "finally", "with",
    "lambda", "None", "True", "False", "and", "or", "not", "is", "pass",
    "break", "continue", "global", "nonlocal", "yield", "raise", "assert",
    "del", "async", "await",
}

_IDENT_START = re.compile(r"[A-Za-z_]")
_IDENT_CHAR = re.compile(r"[A-Za-z0-9_]")
_NUM_CHAR = re.compile(r"[0-9_.eExXa-fA-F]")


def highlight_python(code: str) -> str:
    out: list[str] = []
    i = 0
    n = len(code)

    def at(idx: int) -> str:
        return code[idx] if 0 <= idx < n else ""

    def span(cls: str, txt: str) -> str:
        return f'<span class="{cls}">{escape_html(txt)}</span>'

    while i < n:
        c = code[i]

        # comment
        if c == "#":
            j = i
            while j < n and code[j] != "\n":
                j += 1
            out.append(span("tok-comment", code[i:j]))
            i = j
            continue

        # string (single or triple quoted)
        if c == '"' or c == "'":
            q = c
            k = i + 1
            triple = False
            if at(i + 1) == q and at(i + 2) == q:
                triple = True
                k = i + 3
            if triple:
                while k < n and not (at(k) == q and at(k + 1) == q and at(k + 2) == q):
                    k += 1
                k = min(n, k + 3)
            else:
                while k < n and code[k] != q and code[k] != "\n":
                    if code[k] == "\\":
                        k += 1
                    k += 1
                k = min(n, k + 1)
            out.append(span("tok-string", code[i:k]))
            i = k
            continue

        # number (not part of an identifier)
        prev = at(i - 1)
        if "0" <= c <= "9" and not _IDENT_START.match(prev):
            p = i
            while p < n and _NUM_CHAR.match(code[p]):
                p += 1
            out.append(span("tok-number", code[i:p]))
            i = p
            continue

        # identifier
        if _IDENT_START.match(c):
            q2 = i
            while q2 < n and _IDENT_CHAR.match(code[q2]):
                q2 += 1
            word = code[i:q2]
            after = q2
            while after < n and code[after] == " ":
                after += 1
            is_call = at(after) == "("
            b = i - 1
            while b >= 0 and code[b] == " ":
                b -= 1
            prev_ns = at(b)
            if word in PY_KEYWORDS:
                out.append(span("tok-keyword", word))
            elif is_call:
                out.append(span("tok-call", word))
            elif prev_ns == ".":
                out.append(span("tok-attr", word))
            else:
                out.append(escape_html(word))
            i = q2
            continue

        # operator / punctuation / whitespace
        out.append(escape_html(c))
        i += 1
    return "".join(out)


# ---- inline markdown -------------------------------------------------------
# `code`  **bold**  [text](url)  *italic*  -- leaves $...$ math untouched for MathJax.

_INLINE_RE = re.compile(
    r"(`[^`]+`)|(\*\*[^*]+\*\*)|(\[[^\]]+\]\([^)]+\))|(\*[^*\s][^*]*\*)"
)
_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def render_inline(text: str) -> str:
    out: list[str] = []
    last = 0
    for m in _INLINE_RE.finditer(text):
        if m.start() > last:
            out.append(escape_html(text[last:m.start()]))
        tok = m.group(0)
        if tok[0] == "`":
            out.append('<code class="nb-inline-code">' + escape_html(tok[1:-1]) + "</code>")
        elif tok[:2] == "**":
            out.append("<strong>" + escape_html(tok[2:-2]) + "</strong>")
        elif tok[0] == "[":
            mm = _LINK_RE.match(tok)
            out.append(
                '<a class="nb-link" href="' + mm.group(2)
                + '" target="_blank" rel="noopener">' + escape_html(mm.group(1)) + "</a>"
            )
        else:
            out.append("<em>" + escape_html(tok[1:-1]) + "</em>")
        last = m.end()
    if last < len(text):
        out.append(escape_html(text[last:]))
    return "".join(out)


# ---- block renderers (1:1 with qcf-docs.css) ------------------------------

def _code_cell(exec_n: int, lang: str, code: str) -> str:
    return (
        '<div class="nb-cell nb-cell--code">'
        f'<div class="nb-prompt nb-prompt--in">In&nbsp;[{exec_n}]:</div>'
        '<div class="nb-in">'
        '<div class="nb-in__bar" role="button" tabindex="0">'
        '<span class="nb-in__barleft">'
        '<svg class="nb-in__chevron" width="11" height="11" viewBox="0 0 24 24" fill="none" '
        'stroke="#8593aa" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M6 9l6 6 6-6"></path></svg>'
        f'<span class="nb-in__lang">{escape_html(lang)}</span>'
        '</span>'
        '<span class="nb-in__copy">copy</span>'
        '</div>'
        f'<pre class="nb-in__code"><code>{highlight_python(code)}</code></pre>'
        '</div>'
        '</div>'
    )


def _out_cell(exec_n: int, text: str) -> str:
    return (
        '<div class="nb-cell nb-cell--out">'
        f'<div class="nb-prompt nb-prompt--out">Out[{exec_n}]:</div>'
        f'<div class="nb-out"><pre class="nb-out__pre"><code>{escape_html(text)}</code></pre></div>'
        '</div>'
    )


def _df_cell(exec_n: int, html: str) -> str:
    # `html` is the raw pandas Styler block, injected verbatim; .nb-df CSS styles descendants.
    return (
        '<div class="nb-cell nb-cell--out">'
        f'<div class="nb-prompt nb-prompt--out">Out[{exec_n}]:</div>'
        f'<div class="nb-df">{html}</div>'
        '</div>'
    )


def _heading(level: int, text: str, hid: str) -> str:
    if level == 2:
        return f'<h2 class="nb-h2" id="{hid}">{render_inline(text)}</h2>'
    if level == 3:
        return f'<h3 class="nb-h3" id="{hid}">{render_inline(text)}</h3>'
    return f'<h4 class="nb-h4" id="{hid}">{render_inline(text)}</h4>'


def _md_table(rows: list[str]) -> str:
    def cells(r: str) -> list[str]:
        r = r.strip()
        r = re.sub(r"^\|", "", r)
        r = re.sub(r"\|$", "", r)
        return [s.strip() for s in r.split("|")]

    header = cells(rows[0])
    body = [cells(r) for r in rows[2:]]  # rows[1] is the |---|---| separator
    h = "<thead><tr>" + "".join(f"<th>{render_inline(c)}</th>" for c in header) + "</tr></thead>"
    b = "<tbody>" + "".join(
        "<tr>" + "".join(f"<td>{render_inline(c)}</td>" for c in r) + "</tr>" for r in body
    ) + "</tbody>"
    return f'<div class="nb-table"><table>{h}{b}</table></div>'


def _math_block(tex: str) -> str:
    return f'<div class="nb-math">{tex}</div>'  # raw -- MathJax typesets on the client


def _list_block(items: list[str], ordered: bool) -> str:
    tag = "ol" if ordered else "ul"
    cls = "nb-ol" if ordered else "nb-ul"
    lis = "".join(f"<li>{render_inline(t)}</li>" for t in items)
    return f'<{tag} class="{cls}">{lis}</{tag}>'


# ---- the transform ---------------------------------------------------------

_FENCE = re.compile(r"^```")
_HEADING = re.compile(r"^(#{1,6})\s+(.*)$")
_HEADING_START = re.compile(r"^#{1,6}\s")
_PIPE = re.compile(r"^\s*\|")
_LIST = re.compile(r"^\s*([-*+]|\d+\.)\s+")        # unordered (- * +) or ordered (1.)
_OLIST = re.compile(r"^\s*\d+\.\s+")
_HTML_OUT = re.compile(r"^\s*<(style|table|div)\b")
_CLOSE_TAG = re.compile(r"</(table|div)>")


def parse(md: str) -> Rendered:
    lines = md.replace("\r\n", "\n").split("\n")
    html: list[str] = []
    toc: list[dict] = []
    title: str | None = None
    i = 0
    n = len(lines)
    exec_n = 0

    def is_blank(l: str) -> bool:
        return l.strip() == ""

    def is_indent(l: str) -> bool:
        return l.startswith("    ") or l.startswith("\t")

    def is_html(l: str) -> bool:
        return bool(_HTML_OUT.match(l))

    while i < n:
        line = lines[i]
        if is_blank(line):
            i += 1
            continue

        # (1) code fence + its output
        if _FENCE.match(line):
            lang = re.sub(r"^```", "", line).strip() or "text"
            code: list[str] = []
            i += 1
            while i < n and not _FENCE.match(lines[i]):
                code.append(lines[i])
                i += 1
            i += 1  # closing fence
            exec_n += 1
            html.append(_code_cell(exec_n, lang, "\n".join(code)))

            # look past blank lines for an output block
            j = i
            while j < n and is_blank(lines[j]):
                j += 1
            if j < n and (is_indent(lines[j]) or is_html(lines[j])):
                if is_html(lines[j]):
                    # raw pandas Styler HTML -- contiguous until a blank line AFTER it closes
                    buf: list[str] = []
                    k = j
                    closed = False
                    while k < n:
                        if is_blank(lines[k]) and closed:
                            break
                        buf.append(lines[k])
                        if _CLOSE_TAG.search(lines[k]):
                            closed = True
                        k += 1
                    html.append(_df_cell(exec_n, "\n".join(buf)))
                    i = k
                else:
                    # 4-space-indented text output (may contain blank lines mid-block)
                    out_lines: list[str] = []
                    k2 = j
                    while k2 < n:
                        if is_indent(lines[k2]):
                            out_lines.append(re.sub(r"^ {4}", "", lines[k2]))
                            k2 += 1
                        elif is_blank(lines[k2]):
                            p = k2
                            while p < n and is_blank(lines[p]):
                                p += 1
                            if p < n and is_indent(lines[p]):
                                out_lines.append("")
                                k2 += 1
                            else:
                                break
                        else:
                            break
                    text = re.sub(r"\n+$", "", "\n".join(out_lines))
                    html.append(_out_cell(exec_n, text))
                    i = k2
            continue

        # (2) heading
        hm = _HEADING.match(line)
        if hm:
            level = len(hm.group(1))
            text = re.sub(r"\s*#+\s*$", "", hm.group(2)).strip()
            if level == 1 and title is None:
                title = text  # first H1 = page title (not emitted in body)
                i += 1
                continue
            hid = slug(text) + "-" + str(i)
            if level in (2, 3):
                toc.append({"id": hid, "text": text, "level": level})
            html.append(_heading(level, text, hid))
            i += 1
            continue

        # (3) display math
        if re.match(r"^\$\$", line.strip()):
            mbuf = [line]
            t = line.strip()
            if t == "$$" or not re.search(r"\$\$[\s\S]*\$\$", t):
                i += 1
                while i < n and not re.search(r"\$\$\s*$", lines[i]):
                    mbuf.append(lines[i])
                    i += 1
                if i < n:
                    mbuf.append(lines[i])
            i += 1
            html.append(_math_block("\n".join(mbuf)))
            continue

        # (4) pipe table
        if _PIPE.match(line):
            tbl: list[str] = []
            while i < n and _PIPE.match(lines[i]):
                tbl.append(lines[i])
                i += 1
            if len(tbl) >= 2:
                html.append(_md_table(tbl))
            continue

        # (5) list (unordered / ordered) -- flat; first item sets the kind
        if _LIST.match(line):
            ordered = bool(_OLIST.match(line))
            items: list[str] = []
            while i < n and _LIST.match(lines[i]):
                items.append(_LIST.sub("", lines[i], count=1))
                i += 1
            html.append(_list_block(items, ordered))
            continue

        # (6) paragraph
        para = [line]
        i += 1
        while (
            i < n
            and not is_blank(lines[i])
            and not _FENCE.match(lines[i])
            and not _HEADING_START.match(lines[i])
            and not _PIPE.match(lines[i])
            and not _LIST.match(lines[i])
            and not re.match(r"^\$\$", lines[i].strip())
        ):
            para.append(lines[i])
            i += 1
        html.append('<p class="nb-p">' + render_inline(" ".join(para)) + "</p>")

    return Rendered(html="".join(html), toc=toc, title=title)


def render_notebook(md: str) -> Rendered:
    return parse(md)
