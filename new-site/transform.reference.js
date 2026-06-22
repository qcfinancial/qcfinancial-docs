/* ============================================================================
 * transform.reference.js
 * ----------------------------------------------------------------------------
 * Reference implementation of the notebook(.md) -> documentation HTML transform.
 *
 * This is the SAME algorithm as the approved prototype
 * (QcFinancial Docs Render.dc.html), rewritten to emit plain HTML strings with
 * the `qcf-docs.css` classes instead of React elements. It is dependency-free
 * and is meant to be (a) run as-is to produce reference output, and (b) ported
 * to Python for the production converter.
 *
 * INPUT  : the markdown produced by the existing mkdocs pipeline
 *          (qcfinancial/qcfinancial-docs  docs/*.md) — i.e. nbconvert-style
 *          markdown where code cells are ```python fences and outputs are
 *          either 4-space-indented text OR a raw pandas Styler <table id="T_…">.
 * OUTPUT : an HTML fragment for the {{ content }} slot of page-shell.html,
 *          plus a list of {id, text, level} headings for the {{ toc }} slot.
 *
 * Run (Node):
 *     const { renderNotebook } = require('./transform.reference.js');
 *     const fs = require('fs');
 *     const md = fs.readFileSync('sample_notebook.md', 'utf8');
 *     const { html, toc, title } = renderNotebook(md);
 *     fs.writeFileSync('out.fragment.html', html);
 *
 * PORTING TO PYTHON: each function below maps 1:1 to a method. The block walk in
 * parse() is the contract; keep the ORDER of checks identical (fence -> heading
 * -> display-math -> pipe-table -> paragraph) — it disambiguates the grammar.
 * ========================================================================== */

'use strict';

/* ---- helpers -------------------------------------------------------------- */

function escapeHtml(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function slug(s) {
  return s.toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')   // strip accents
    .replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
}

/* ---- Python syntax highlighter -------------------------------------------
 * Emits <span class="tok-*">…</span>. Classification rules:
 *   #…            -> tok-comment (to end of line)
 *   "…" '…' f"…"  -> tok-string  (single + triple quotes, backslash escapes)
 *   123 1_000 0x..-> tok-number
 *   keyword       -> tok-keyword
 *   name(         -> tok-call    (name immediately followed by "(")
 *   .name         -> tok-attr    (name immediately preceded by ".")
 *   anything else -> plain text (no span)
 * Good enough for documentation; NOT a full Python lexer.
 * ------------------------------------------------------------------------- */

var PY_KEYWORDS = new Set(['import','from','as','def','class','return','for','in',
  'if','else','elif','while','try','except','finally','with','lambda','None',
  'True','False','and','or','not','is','pass','break','continue','global',
  'nonlocal','yield','raise','assert','del','async','await']);

function highlightPython(code) {
  var out = '';
  var i = 0; var n = code.length;
  var span = function (cls, txt) { return '<span class="' + cls + '">' + escapeHtml(txt) + '</span>'; };

  while (i < n) {
    var c = code[i];

    // comment
    if (c === '#') { var j = i; while (j < n && code[j] !== '\n') j++; out += span('tok-comment', code.slice(i, j)); i = j; continue; }

    // string (single or triple quoted)
    if (c === '"' || c === "'") {
      var q = c; var k = i + 1; var triple = false;
      if (code[i + 1] === q && code[i + 2] === q) { triple = true; k = i + 3; }
      if (triple) { while (k < n && !(code[k] === q && code[k + 1] === q && code[k + 2] === q)) k++; k = Math.min(n, k + 3); }
      else { while (k < n && code[k] !== q && code[k] !== '\n') { if (code[k] === '\\') k++; k++; } k = Math.min(n, k + 1); }
      out += span('tok-string', code.slice(i, k)); i = k; continue;
    }

    // number (not part of an identifier)
    var prev = code[i - 1] || '';
    if (c >= '0' && c <= '9' && !/[A-Za-z_]/.test(prev)) {
      var p = i; while (p < n && /[0-9_.eExXa-fA-F]/.test(code[p])) p++; out += span('tok-number', code.slice(i, p)); i = p; continue;
    }

    // identifier
    if (/[A-Za-z_]/.test(c)) {
      var q2 = i; while (q2 < n && /[A-Za-z0-9_]/.test(code[q2])) q2++;
      var word = code.slice(i, q2);
      var after = q2; while (after < n && code[after] === ' ') after++;
      var isCall = code[after] === '(';
      var b = i - 1; while (b >= 0 && code[b] === ' ') b--;
      var prevNS = code[b];
      if (PY_KEYWORDS.has(word)) out += span('tok-keyword', word);
      else if (isCall) out += span('tok-call', word);
      else if (prevNS === '.') out += span('tok-attr', word);
      else out += escapeHtml(word);
      i = q2; continue;
    }

    // operator / punctuation / whitespace
    out += escapeHtml(c); i++;
  }
  return out;
}

/* ---- inline markdown ------------------------------------------------------
 * `code`  **bold**  [text](url)  *italic*  — leaves $…$ math untouched for MathJax.
 * ------------------------------------------------------------------------- */
function renderInline(text) {
  var re = /(`[^`]+`)|(\*\*[^*]+\*\*)|(\[[^\]]+\]\([^)]+\))|(\*[^*\s][^*]*\*)/g;
  var out = ''; var last = 0; var m;
  while ((m = re.exec(text))) {
    if (m.index > last) out += escapeHtml(text.slice(last, m.index));
    var tok = m[0];
    if (tok[0] === '`') out += '<code class="nb-inline-code">' + escapeHtml(tok.slice(1, -1)) + '</code>';
    else if (tok.slice(0, 2) === '**') out += '<strong>' + escapeHtml(tok.slice(2, -2)) + '</strong>';
    else if (tok[0] === '[') { var mm = tok.match(/\[([^\]]+)\]\(([^)]+)\)/); out += '<a class="nb-link" href="' + mm[2] + '" target="_blank" rel="noopener">' + escapeHtml(mm[1]) + '</a>'; }
    else out += '<em>' + escapeHtml(tok.slice(1, -1)) + '</em>';
    last = re.lastIndex;
  }
  if (last < text.length) out += escapeHtml(text.slice(last));
  return out;
}

/* ---- block renderers (1:1 with qcf-docs.css) ------------------------------ */

function codeCell(exec, lang, code) {
  return ''
    + '<div class="nb-cell nb-cell--code">'
    +   '<div class="nb-prompt nb-prompt--in">In&nbsp;[' + exec + ']:</div>'
    +   '<div class="nb-in">'
    +     '<div class="nb-in__bar" role="button" tabindex="0">'
    +       '<span class="nb-in__barleft">'
    +         '<svg class="nb-in__chevron" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="#8593aa" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"></path></svg>'
    +         '<span class="nb-in__lang">' + escapeHtml(lang) + '</span>'
    +       '</span>'
    +       '<span class="nb-in__copy">copy</span>'
    +     '</div>'
    +     '<pre class="nb-in__code"><code>' + highlightPython(code) + '</code></pre>'
    +   '</div>'
    + '</div>';
}

function outCell(exec, text) {
  return ''
    + '<div class="nb-cell nb-cell--out">'
    +   '<div class="nb-prompt nb-prompt--out">Out[' + exec + ']:</div>'
    +   '<div class="nb-out"><pre class="nb-out__pre"><code>' + escapeHtml(text) + '</code></pre></div>'
    + '</div>';
}

// `html` is the raw pandas Styler block (<style>…</style><table id="T_…">…</table>)
// injected verbatim. .nb-df CSS styles the descendant table/th/td.
function dfCell(exec, html) {
  return ''
    + '<div class="nb-cell nb-cell--out">'
    +   '<div class="nb-prompt nb-prompt--out">Out[' + exec + ']:</div>'
    +   '<div class="nb-df">' + html + '</div>'
    + '</div>';
}

function heading(level, text, id) {
  if (level === 2) return '<h2 class="nb-h2" id="' + id + '">' + escapeHtml(text) + '</h2>';
  if (level === 3) return '<h3 class="nb-h3" id="' + id + '">' + escapeHtml(text) + '</h3>';
  return '<h4 class="nb-h4" id="' + id + '">' + escapeHtml(text) + '</h4>';
}

function mdTable(rows) {
  var cells = function (r) { return r.trim().replace(/^\|/, '').replace(/\|$/, '').split('|').map(function (s) { return s.trim(); }); };
  var header = cells(rows[0]);
  var body = rows.slice(2).map(cells); // rows[1] is the |---|---| separator
  var h = '<thead><tr>' + header.map(function (c) { return '<th>' + renderInline(c) + '</th>'; }).join('') + '</tr></thead>';
  var b = '<tbody>' + body.map(function (r) { return '<tr>' + r.map(function (c) { return '<td>' + renderInline(c) + '</td>'; }).join('') + '</tr>'; }).join('') + '</tbody>';
  return '<div class="nb-table"><table>' + h + b + '</table></div>';
}

function mathBlock(tex) {
  return '<div class="nb-math">' + tex + '</div>'; // raw — MathJax typesets on the client
}

/* ---- the transform -------------------------------------------------------- */

function parse(md) {
  var lines = md.replace(/\r\n/g, '\n').split('\n');
  var html = ''; var toc = []; var title = null;
  var i = 0; var n = lines.length; var exec = 0;

  var isBlank  = function (l) { return l.trim() === ''; };
  var isIndent = function (l) { return /^ {4}/.test(l) || /^\t/.test(l); };
  var isHtml   = function (l) { return /^\s*<(style|table|div)\b/.test(l); };

  while (i < n) {
    var line = lines[i];
    if (isBlank(line)) { i++; continue; }

    /* (1) code fence + its output ---------------------------------------- */
    if (/^```/.test(line)) {
      var lang = line.replace(/^```/, '').trim() || 'text';
      var code = []; i++;
      while (i < n && !/^```/.test(lines[i])) { code.push(lines[i]); i++; }
      i++; // closing fence
      exec++;
      html += codeCell(exec, lang, code.join('\n'));

      // look past blank lines for an output block
      var j = i; while (j < n && isBlank(lines[j])) j++;
      if (j < n && (isIndent(lines[j]) || isHtml(lines[j]))) {
        if (isHtml(lines[j])) {
          // raw pandas Styler HTML — contiguous until a blank line AFTER it closes
          var buf = []; var k = j; var closed = false;
          while (k < n) { if (isBlank(lines[k]) && closed) break; buf.push(lines[k]); if (/<\/(table|div)>/.test(lines[k])) closed = true; k++; }
          html += dfCell(exec, buf.join('\n')); i = k;
        } else {
          // 4-space-indented text output (may contain blank lines mid-block)
          var out = []; var k2 = j;
          while (k2 < n) {
            if (isIndent(lines[k2])) { out.push(lines[k2].replace(/^ {4}/, '')); k2++; }
            else if (isBlank(lines[k2])) {
              var p = k2; while (p < n && isBlank(lines[p])) p++;
              if (p < n && isIndent(lines[p])) { out.push(''); k2++; } else break;
            } else break;
          }
          html += outCell(exec, out.join('\n').replace(/\n+$/, '')); i = k2;
        }
      }
      continue;
    }

    /* (2) heading -------------------------------------------------------- */
    var hm = line.match(/^(#{1,6})\s+(.*)$/);
    if (hm) {
      var level = hm[1].length;
      var text = hm[2].replace(/\s*#+\s*$/, '').trim();
      if (level === 1 && title === null) { title = text; i++; continue; } // first H1 = page title
      var id = slug(text) + '-' + i;
      if (level === 2 || level === 3) toc.push({ id: id, text: text, level: level });
      html += heading(level, text, id); i++; continue;
    }

    /* (3) display math --------------------------------------------------- */
    if (/^\$\$/.test(line.trim())) {
      var mbuf = [line];
      var t = line.trim();
      if (t === '$$' || !/\$\$[\s\S]*\$\$/.test(t)) {
        i++; while (i < n && !/\$\$\s*$/.test(lines[i])) { mbuf.push(lines[i]); i++; } if (i < n) mbuf.push(lines[i]);
      }
      i++; html += mathBlock(mbuf.join('\n')); continue;
    }

    /* (4) pipe table ----------------------------------------------------- */
    if (/^\s*\|/.test(line)) {
      var tbl = []; while (i < n && /^\s*\|/.test(lines[i])) { tbl.push(lines[i]); i++; }
      if (tbl.length >= 2) html += mdTable(tbl);
      continue;
    }

    /* (5) paragraph ------------------------------------------------------ */
    var para = [line]; i++;
    while (i < n && !isBlank(lines[i]) && !/^```/.test(lines[i]) && !/^#{1,6}\s/.test(lines[i]) && !/^\s*\|/.test(lines[i]) && !/^\$\$/.test(lines[i].trim())) { para.push(lines[i]); i++; }
    html += '<p class="nb-p">' + renderInline(para.join(' ')) + '</p>';
  }

  return { html: html, toc: toc, title: title };
}

function renderNotebook(md) { return parse(md); }

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { renderNotebook: renderNotebook, parse: parse, highlightPython: highlightPython, renderInline: renderInline, slug: slug };
}
