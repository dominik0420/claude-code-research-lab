#!/usr/bin/env python3
"""
compile_paper.py — Claude Code Research Lab
Assembles markdown section drafts into a LaTeX paper and optionally compiles to PDF.

Usage:
    python3 .claude/scripts/compile_paper.py \
        --outline papers/outline.md \
        --drafts-dir papers/drafts \
        --output papers/main.tex \
        --venue arxiv-cn \
        [--no-compile]

Venues:
    arxiv-cn  — Chinese academic paper, Arxiv-ready (XeLaTeX)
    ctex      — Generic Chinese document (XeLaTeX)
    neurips / icml / iclr / acl / cvpr / article
"""

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


# ── Venue templates ────────────────────────────────────────────────────────────

_CJK_BASE = r"""
\usepackage{fontspec}
% ctexart: body=宋体, headings=黑体 (standard Chinese academic convention)
% For fake-bold of same font, uncomment:
%   \setCJKmainfont{SimSun}[AutoFakeBold=1.5]
\usepackage[top=2.54cm,bottom=2.54cm,left=3.17cm,right=3.17cm]{geometry}
\usepackage{amsmath,amssymb,amsthm}
\usepackage{booktabs,longtable,tabularx}
\usepackage{adjustbox}
\usepackage{graphicx,float}
\usepackage{xcolor}
\usepackage[numbers,sort&compress]{natbib}
\linespread{1.3}
\setlength{\parskip}{0.2em}
\ctexset{
    section     = {format=\zihao{-3}\heiti, beforeskip=1.5em, afterskip=0.8em},
    subsection  = {format=\zihao{4}\heiti,  beforeskip=1.0em, afterskip=0.5em},
    subsubsection = {format=\zihao{-4}\heiti, beforeskip=0.8em, afterskip=0.3em},
}
\renewenvironment{abstract}{%
    \noindent{\zihao{-4}\heiti 摘\quad 要：}\small\ignorespaces
}{\par\vspace{0.5em}}
\newcommand{\keywords}[1]{\par\noindent{\zihao{-4}\heiti 关键词：}\small #1\par\vspace{1em}}
"""

VENUE_PREAMBLES = {
    "arxiv-cn": r"""\documentclass[12pt,a4paper]{ctexart}
""" + _CJK_BASE + r"""
\usepackage[colorlinks=true,linkcolor=blue,citecolor=blue,urlcolor=blue]{hyperref}
\hypersetup{pdfencoding=auto, CJKbookmarks=true}
""",
    "ctex": r"""\documentclass[12pt,a4paper]{ctexart}
""" + _CJK_BASE + r"""
\usepackage[colorlinks=true,linkcolor=black,citecolor=black,urlcolor=blue]{hyperref}
\hypersetup{pdfencoding=auto, CJKbookmarks=true}
""",
    "neurips": r"""\documentclass{article}
\usepackage[preprint]{neurips_2024}
\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}
\usepackage{hyperref,url,booktabs,amsfonts,amsmath,amssymb,graphicx,microtype,xcolor,adjustbox}
""",
    "icml": r"""\documentclass{article}
\usepackage[accepted]{icml2024}
\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}
\usepackage{hyperref,url,booktabs,amsmath,amssymb,graphicx,microtype,adjustbox}
""",
    "iclr": r"""\documentclass{article}
\usepackage{iclr2025_conference,times}
\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}
\usepackage{hyperref,url,booktabs,amsmath,amssymb,graphicx,microtype,adjustbox}
""",
    "acl": r"""\documentclass[11pt]{article}
\usepackage[hyperref]{acl_natbib}
\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}
\usepackage{times,latexsym,booktabs,amsmath,graphicx,microtype,adjustbox}
""",
    "cvpr": r"""\documentclass[10pt,twocolumn,letterpaper]{article}
\usepackage{cvpr}
\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}
\usepackage{graphicx,amsmath,amssymb,booktabs,microtype,adjustbox}
""",
    "article": r"""\documentclass[11pt,a4paper]{article}
\usepackage[margin=1in]{geometry}
\usepackage[utf8]{inputenc}\usepackage[T1]{fontenc}
\usepackage{hyperref,url,booktabs,amsmath,amssymb,graphicx,microtype,xcolor,adjustbox}
\setlength{\parskip}{0.4em}
""",
}

XELATEX_VENUES = {"ctex", "arxiv-cn"}


# ── Markdown → LaTeX ───────────────────────────────────────────────────────────

def fix_quotes(text: str) -> str:
    """Convert straight double quotes to Unicode curly quotes (correct in XeLaTeX)."""
    result, open_q = [], True
    for ch in text:
        if ch == '"':
            result.append('“' if open_q else '”')
            open_q = not open_q
        else:
            result.append(ch)
    return ''.join(result)


def md_inline_to_latex(text: str) -> str:
    math_spans: dict[str, str] = {}
    def protect_math(m: re.Match) -> str:
        k = f"MATH{len(math_spans)}END"
        math_spans[k] = m.group(0)
        return k
    text = re.sub(r'\$[^$]+\$', protect_math, text)
    text = fix_quotes(text)
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\\textbf{\\textit{\1}}', text)
    text = re.sub(r'\*\*(.+?)\*\*',     r'\\textbf{\1}', text)
    text = re.sub(r'__(.+?)__',         r'\\textbf{\1}', text)
    text = re.sub(r'\*(.+?)\*',         r'\\textit{\1}', text)
    text = re.sub(r'_([^_]+)_',         r'\\textit{\1}', text)
    text = re.sub(r'`([^`]+)`',         r'\\texttt{\1}', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1\\footnote{\\url{\2}}', text)
    for k, v in math_spans.items():
        text = text.replace(k, v)
    return text


def md_table_to_latex(lines: list[str]) -> str:
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines]
    if len(rows) < 2:
        return ""
    header, body, ncols = rows[0], rows[2:], len(rows[0])
    out = [
        r"\begin{table}[htbp]", r"\centering", r"\small",
        r"\renewcommand{\arraystretch}{1.2}",
        r"\begin{adjustbox}{max width=\linewidth}",
        r"\begin{tabular}{" + "l" * ncols + "}",
        r"\toprule",
        " & ".join(md_inline_to_latex(h) for h in header) + r" \\",
        r"\midrule",
    ]
    for row in body:
        padded = row + [""] * (ncols - len(row))
        out.append(" & ".join(md_inline_to_latex(c) for c in padded[:ncols]) + r" \\")
    out += [r"\bottomrule", r"\end{tabular}", r"\end{adjustbox}", r"\end{table}"]
    return "\n".join(out)


def md_to_latex(content: str, section_offset: int = 0) -> str:
    CMDS = ["\\section", "\\subsection", "\\subsubsection", "\\paragraph"]
    lines = content.split("\n")
    output: list[str] = []
    in_list = False
    list_type = None
    table_buf: list[str] = []
    in_code = False
    code_buf: list[str] = []

    def flush_list():
        nonlocal in_list, list_type
        if in_list:
            output.append(r"\end{itemize}" if list_type == "ul" else r"\end{enumerate}")
            in_list = False; list_type = None

    def flush_table():
        nonlocal table_buf
        if table_buf:
            output.append(md_table_to_latex(table_buf)); table_buf = []

    for line in lines:
        if line.strip().startswith("```"):
            flush_list(); flush_table()
            if not in_code:
                in_code = True; code_buf = []
            else:
                in_code = False
                output += [r"\begin{verbatim}"] + code_buf + [r"\end{verbatim}"]
                code_buf = []
            continue
        if in_code:
            code_buf.append(line); continue
        if line.strip().startswith("|"):
            flush_list(); table_buf.append(line); continue
        elif table_buf:
            flush_table()
        hm = re.match(r'^(#{1,4})\s+(.*)', line)
        if hm:
            flush_list(); flush_table()
            lvl = min(len(hm.group(1)) - 1 + section_offset, len(CMDS) - 1)
            output.append(f"{CMDS[lvl]}{{{md_inline_to_latex(hm.group(2))}}}")
            continue
        if re.match(r'^-{3,}$', line.strip()) or re.match(r'^\*{3,}$', line.strip()):
            flush_list(); output.append(r"\noindent\rule{\linewidth}{0.4pt}"); continue
        ul = re.match(r'^\s*[-*+]\s+(.*)', line)
        if ul:
            if not in_list or list_type != "ul":
                flush_list(); output.append(r"\begin{itemize}"); in_list = True; list_type = "ul"
            output.append(f"  \\item {md_inline_to_latex(ul.group(1))}"); continue
        ol = re.match(r'^\s*\d+[.)]\s+(.*)', line)
        if ol:
            if not in_list or list_type != "ol":
                flush_list(); output.append(r"\begin{enumerate}"); in_list = True; list_type = "ol"
            output.append(f"  \\item {md_inline_to_latex(ol.group(1))}"); continue
        if in_list and not line.strip():
            flush_list(); output.append(""); continue
        bq = re.match(r'^>\s*(.*)', line)
        if bq:
            flush_list()
            output += [r"\begin{quote}", md_inline_to_latex(bq.group(1)), r"\end{quote}"]; continue
        if not line.strip():
            flush_list(); output.append(""); continue
        flush_list()
        output.append(md_inline_to_latex(line))

    flush_list(); flush_table()
    return "\n".join(output)


# ── Outline parsing ────────────────────────────────────────────────────────────

_WORD_COUNT_RE  = re.compile(r'[（(][^）)]*[字词words][^）)]*[）)]')
_CN_ORDINAL_RE  = re.compile(r'^[一二三四五六七八九十百]+[、．.]')
_ABSTRACT_NAMES = {"abstract", "执行摘要", "摘要", "executive summary"}
_SKIP_PATTERNS  = [r'^受众导航', r'^图表映射', r'^写作前', r'^open.?question', r'^figure.?map']


def clean_section_name(raw: str) -> str:
    return _WORD_COUNT_RE.sub('', raw).strip(' ：:')


def should_skip(name: str) -> bool:
    if name.lower() in _ABSTRACT_NAMES:
        return True
    return any(re.search(p, name, re.IGNORECASE) for p in _SKIP_PATTERNS)


def parse_outline(path: Path) -> dict:
    result = dict(title="Research Paper", authors="", affiliation="",
                  date=r"\today", abstract="", keywords="", sections=[])
    if not path.exists():
        return result
    text  = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.split("\n")

    for line in lines:
        m = re.match(r'^#\s+(.*)', line)
        if m:
            t = re.sub(r'^(论文大纲\s*[：:]\s*|Paper\s+Outline\s*[:\s]+)', '', m.group(1))
            t = re.sub(r'\s*[暨—–]\s.*$', '', t)
            result["title"] = t.strip(); break

    for line in lines:
        if re.search(r'\b(author|作者)\b', line, re.IGNORECASE) and re.search(r'[：:]', line):
            val = re.split(r'[：:]', line, 1)[1].strip().strip('*')
            if val: result["authors"] = val; break

    for line in lines:
        if re.search(r'关键词[：:]|keywords?\s*[：:]', line, re.IGNORECASE):
            val = re.split(r'[：:]', line, 1)[-1].strip()
            if val: result["keywords"] = val; break

    abs_re = re.compile(r'^#{1,3}\s+(' + '|'.join(_ABSTRACT_NAMES) + r')', re.IGNORECASE)
    abs_start = next((i+1 for i, l in enumerate(lines) if abs_re.match(l)), None)
    if abs_start:
        abs_lines = []
        for line in lines[abs_start:]:
            if re.match(r'^#{1,3}\s+', line): break
            if not re.match(r'^\s*[-*]', line) and line.strip():
                abs_lines.append(line.strip())
        result["abstract"] = " ".join(abs_lines)

    seen_abs = False
    for line in lines:
        if abs_re.match(line): seen_abs = True; continue
        if not seen_abs: continue
        m = re.match(r'^#{2,3}\s+(.*)', line)
        if m:
            sec = clean_section_name(m.group(1))
            if sec and not should_skip(sec):
                result["sections"].append(sec)
    return result


def find_draft(drafts_dir: Path, section: str) -> Path | None:
    def norm(s: str) -> str:
        s = _WORD_COUNT_RE.sub('', s).lower()
        return re.sub(r'[^a-z0-9一-鿿]', '', s)
    tgt     = norm(section)
    tgt_no  = norm(_CN_ORDINAL_RE.sub('', section))
    for f in drafts_dir.glob("*.md"):
        fn = norm(f.stem)
        if fn in (tgt, tgt_no): return f
    for f in drafts_dir.glob("*.md"):
        fn = norm(f.stem)
        if tgt in fn or fn in tgt or (tgt_no and (tgt_no in fn or fn in tgt_no)):
            return f
    return None


def read_status(papers_dir: Path) -> dict:
    sp = papers_dir / "STATUS.md"
    if not sp.exists(): return {}
    statuses = {}
    for line in sp.read_text(encoding="utf-8", errors="ignore").split("\n"):
        m = re.match(r'.*\|\s*([^|]+?)\s*\|\s*(DRAFT|REVIEWED|APPROVED)\s*\|', line)
        if m: statuses[m.group(1).strip().lower()] = m.group(2).strip()
    return statuses


# ── Assembler ──────────────────────────────────────────────────────────────────

def assemble(outline_path: Path, drafts_dir: Path, output_path: Path,
             venue: str, no_compile: bool) -> list[str]:
    messages: list[str] = []
    meta     = parse_outline(outline_path)
    statuses = read_status(outline_path.parent)
    preamble = VENUE_PREAMBLES.get(venue, VENUE_PREAMBLES["article"])

    doc: list[str] = [preamble, ""]
    title   = meta["title"]   or "Research Paper"
    authors = meta["authors"] or "Author"
    doc.append(f"\\title{{{md_inline_to_latex(title)}}}")
    doc.append("")
    if meta["affiliation"]:
        doc.append(f"\\author{{{md_inline_to_latex(authors)} \\\\ "
                   f"\\small {md_inline_to_latex(meta['affiliation'])}}}")
    else:
        doc.append(f"\\author{{{md_inline_to_latex(authors)}}}")
    doc += ["", f"\\date{{{meta['date']}}}", "", r"\begin{document}", r"\maketitle", ""]

    # Abstract
    abs_text = meta["abstract"]
    if not abs_text:
        ab = find_draft(drafts_dir, "abstract") or find_draft(drafts_dir, "执行摘要")
        if ab:
            raw = ab.read_text(encoding="utf-8", errors="ignore")
            raw = re.sub(r'^---.*?---\s*', '', raw, flags=re.DOTALL)
            raw = re.sub(r'^#{1,3}[^\n]*\n', '', raw, count=1)
            abs_text = raw.strip()

    doc.append(r"\begin{abstract}")
    doc.append(md_inline_to_latex(abs_text) if abs_text else r"% TODO: 执行摘要")
    doc.append(r"\end{abstract}")
    if not abs_text:
        messages.append("WARNING: No abstract — placeholder inserted.")
    if meta["keywords"]:
        doc.append(f"\\keywords{{{md_inline_to_latex(meta['keywords'])}}}")
    doc.append("")

    # Body sections
    section_order = meta["sections"] or [
        f.stem.replace("-", " ").title()
        for f in sorted(drafts_dir.glob("*.md"))
        if f.stem.lower() not in _ABSTRACT_NAMES
    ]
    if not meta["sections"]:
        messages.append("NOTE: No section order in outline — using alphabetical draft order.")

    included, missing = [], []
    for sec in section_order:
        if sec.lower() in _ABSTRACT_NAMES: continue
        draft = find_draft(drafts_dir, sec)
        status = statuses.get(sec.lower(), "DRAFT")
        if draft is None:
            doc += [f"% MISSING: {sec}", f"\\section{{{md_inline_to_latex(sec)}}}",
                    f"% TODO: /write-section {sec}", ""]
            missing.append(sec); messages.append(f"WARNING: No draft for '{sec}'."); continue
        content = draft.read_text(encoding="utf-8", errors="ignore")
        content = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)
        content = re.sub(r'^#{1,3}[^\n]*\n', '', content, count=1)
        if status != "APPROVED":
            doc.append(f"% [{status}] {sec}")
        doc += [f"\\section{{{md_inline_to_latex(sec)}}}", md_to_latex(content.strip()), ""]
        included.append(sec)

    # References
    bib = outline_path.parent.parent / "literature" / "bibliography.bib"
    alt = outline_path.parent / "references.bib"
    doc.append(r"\newpage")
    if bib.exists():
        doc += [r"\bibliographystyle{plainnat}", f"\\bibliography{{{str(bib.with_suffix(''))}}}"]
    elif alt.exists():
        doc += [r"\bibliographystyle{plainnat}", f"\\bibliography{{{str(alt.with_suffix(''))}}}"]
    else:
        doc += [r"\begin{thebibliography}{99}", r"% TODO: references", r"\end{thebibliography}"]
    doc += ["", r"\end{document}"]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(doc), encoding="utf-8")

    if included: messages.insert(0, f"OK: {', '.join(included)}")
    if missing:  messages.insert(1, f"MISSING: {', '.join(missing)}")
    return messages


# ── PDF compilation ────────────────────────────────────────────────────────────

def try_engine(engine: str, tex_path: Path) -> tuple[bool, str]:
    if not shutil.which(engine):
        return False, f"{engine}: not in PATH"
    out_dir = tex_path.parent
    cmd = [engine, "-interaction=nonstopmode", f"-output-directory={out_dir}", str(tex_path)]
    for _ in range(2):
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            return False, f"{engine}: timeout"
        except Exception as e:
            return False, f"{engine}: {e}"
    if tex_path.with_suffix(".pdf").exists():
        return True, f"PDF -> {tex_path.with_suffix('.pdf')}"
    errors = [l for l in (r.stdout + r.stderr).split("\n") if l.startswith("!") or "Error" in l][:6]
    return False, f"{engine} failed:\n" + "\n".join(errors)


def try_tectonic(tex_path: Path) -> tuple[bool, str]:
    if not shutil.which("tectonic"):
        return False, "tectonic: not in PATH"
    try:
        r = subprocess.run(["tectonic", str(tex_path)], capture_output=True, text=True, timeout=300)
        if tex_path.with_suffix(".pdf").exists():
            return True, f"PDF -> {tex_path.with_suffix('.pdf')}"
        return False, f"tectonic failed: {r.stderr[:200]}"
    except Exception as e:
        return False, f"tectonic: {e}"


def compile_pdf(tex_path: Path, venue: str) -> tuple[bool, str]:
    engines = ["xelatex", "lualatex"] if venue in XELATEX_VENUES else ["pdflatex", "xelatex", "lualatex"]
    attempts = []
    for eng in engines:
        ok, msg = try_engine(eng, tex_path)
        if ok: return True, msg
        attempts.append(msg)
    ok, msg = try_tectonic(tex_path)
    if ok: return True, msg
    attempts.append(msg)

    hint = (
        "CJK document requires XeLaTeX:\n"
        "  Windows: winget install MiKTeX.MiKTeX\n"
        "  macOS:   brew install --cask mactex\n"
        "  Linux:   sudo apt install texlive-xetex texlive-lang-chinese\n"
        "  Any OS:  https://tectonic-typesetting.github.io\n"
        "  Online:  https://overleaf.com (set compiler to XeLaTeX)"
    ) if venue in XELATEX_VENUES else (
        "  Windows: winget install MiKTeX.MiKTeX\n"
        "  macOS:   brew install --cask mactex\n"
        "  Linux:   sudo apt install texlive-full"
    )
    return False, "No LaTeX engine found.\n" + hint + "\n\nAttempts:\n" + "\n".join(f"  {a}" for a in attempts)


# ── CLI ────────────────────────────────────────────────────────────────────────

def main() -> None:
    p = argparse.ArgumentParser(description="Assemble markdown drafts → LaTeX → PDF")
    p.add_argument("--outline",    default="papers/outline.md")
    p.add_argument("--drafts-dir", default="papers/drafts")
    p.add_argument("--output",     default="papers/main.tex")
    p.add_argument("--venue",      default="arxiv-cn", choices=sorted(VENUE_PREAMBLES))
    p.add_argument("--no-compile", action="store_true")
    args = p.parse_args()

    outline   = Path(args.outline)
    drafts    = Path(args.drafts_dir)
    output    = Path(args.output)

    if not outline.exists():
        print(f"ERROR: outline not found: {outline}", file=sys.stderr); sys.exit(1)
    if not drafts.exists() or not any(drafts.glob("*.md")):
        print(f"ERROR: no draft .md files in {drafts}", file=sys.stderr); sys.exit(1)

    print(f"Assembling  {drafts}/ -> {output}  [venue: {args.venue}]")
    msgs = assemble(outline, drafts, output, args.venue, args.no_compile)
    print("\n-- Assembly " + "-" * 40)
    for m in msgs: print(f"  {m}")
    print(f"\n  LaTeX: {output}")

    if args.no_compile:
        print("\n  [--no-compile] done."); sys.exit(0)

    print("\n-- Compiling PDF " + "-" * 36)
    ok, log = compile_pdf(output, args.venue)
    print(f"  {'OK' if ok else 'FAILED'}  {log}")
    sys.exit(0 if ok else 2)


if __name__ == "__main__":
    main()
