#!/usr/bin/env python3
"""
compile_paper.py — Claude Code Research Lab
Assembles markdown section drafts into a LaTeX paper and optionally compiles to PDF.

Usage:
    python3 .claude/scripts/compile_paper.py \
        --outline papers/outline.md \
        --drafts-dir papers/drafts \
        --output papers/main.tex \
        --venue ctex \
        [--no-compile]
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


# ── Venue templates ────────────────────────────────────────────────────────────

VENUE_PREAMBLES = {
    # Chinese document — uses ctexart, requires XeLaTeX
    "ctex": r"""\documentclass[12pt,a4paper]{ctexart}
\usepackage[margin=2.5cm]{geometry}
\usepackage{hyperref}
\usepackage{url}
\usepackage{booktabs}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{xcolor}
\usepackage{parskip}
\usepackage{longtable}
\hypersetup{colorlinks=true, linkcolor=blue, urlcolor=blue, citecolor=blue}
""",
    "neurips": r"""\documentclass{article}
\usepackage[preprint]{neurips_2024}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{hyperref}
\usepackage{url}
\usepackage{booktabs}
\usepackage{amsfonts}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{microtype}
\usepackage{xcolor}
""",
    "icml": r"""\documentclass{article}
\usepackage[accepted]{icml2024}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{hyperref}
\usepackage{url}
\usepackage{booktabs}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{microtype}
""",
    "iclr": r"""\documentclass{article}
\usepackage{iclr2025_conference,times}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{hyperref}
\usepackage{url}
\usepackage{booktabs}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{microtype}
""",
    "acl": r"""\documentclass[11pt]{article}
\usepackage[hyperref]{acl_natbib}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{times}
\usepackage{latexsym}
\usepackage{booktabs}
\usepackage{amsmath}
\usepackage{graphicx}
\usepackage{microtype}
""",
    "cvpr": r"""\documentclass[10pt,twocolumn,letterpaper]{article}
\usepackage{cvpr}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{graphicx}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{booktabs}
\usepackage{microtype}
""",
    "article": r"""\documentclass[11pt,a4paper]{article}
\usepackage[margin=1in]{geometry}
\usepackage[utf8]{inputenc}
\usepackage[T1]{fontenc}
\usepackage{hyperref}
\usepackage{url}
\usepackage{booktabs}
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{microtype}
\usepackage{xcolor}
\usepackage{parskip}
""",
}

# Venues that require XeLaTeX (CJK / Unicode fonts)
XELATEX_VENUES = {"ctex"}


# ── Markdown → LaTeX conversion ────────────────────────────────────────────────

def escape_latex(text: str) -> str:
    """Escape special LaTeX characters in plain text (not in already-converted spans)."""
    replacements = [
        ("\\", r"\textbackslash{}"),
        ("&",  r"\&"),
        ("%",  r"\%"),
        ("$",  r"\$"),
        ("#",  r"\#"),
        ("_",  r"\_"),
        ("{",  r"\{"),
        ("}",  r"\}"),
        ("~",  r"\textasciitilde{}"),
        ("^",  r"\textasciicircum{}"),
    ]
    for ch, rep in replacements:
        text = text.replace(ch, rep)
    return text


def md_inline_to_latex(text: str) -> str:
    """Convert inline markdown (bold, italic, code, links) to LaTeX."""
    math_spans = {}
    def protect_math(m):
        key = f"MATHSPAN{len(math_spans)}END"
        math_spans[key] = m.group(0)
        return key
    text = re.sub(r'\$[^$]+\$', protect_math, text)

    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\\textbf{\\textit{\1}}', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    text = re.sub(r'__(.+?)__', r'\\textbf{\1}', text)
    text = re.sub(r'\*(.+?)\*', r'\\textit{\1}', text)
    text = re.sub(r'_(.+?)_', r'\\textit{\1}', text)
    text = re.sub(r'`([^`]+)`', r'\\texttt{\1}', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1\\footnote{\\url{\2}}', text)

    for key, val in math_spans.items():
        text = text.replace(key, val)

    return text


def md_table_to_latex(lines: list[str]) -> str:
    """Convert a markdown table block to a LaTeX booktabs table."""
    rows = []
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)

    if len(rows) < 2:
        return ""

    header = rows[0]
    # rows[1] is the separator line — skip it
    body = rows[2:]

    ncols = len(header)
    col_spec = "l" * ncols

    out = []
    out.append(r"\begin{table}[htbp]")
    out.append(r"\centering")
    out.append(r"\begin{tabular}{" + col_spec + "}")
    out.append(r"\toprule")
    out.append(" & ".join(md_inline_to_latex(h) for h in header) + r" \\")
    out.append(r"\midrule")
    for row in body:
        padded = row + [""] * (ncols - len(row))
        out.append(" & ".join(md_inline_to_latex(c) for c in padded[:ncols]) + r" \\")
    out.append(r"\bottomrule")
    out.append(r"\end{tabular}")
    out.append(r"\end{table}")
    return "\n".join(out)


def md_to_latex(content: str, section_offset: int = 0) -> str:
    """Convert a markdown section draft to LaTeX body content."""
    lines = content.split("\n")
    output = []
    i = 0
    in_list = False
    list_type = None
    table_buffer = []
    in_code = False
    code_buffer = []

    SECTION_CMDS = ["\\section", "\\subsection", "\\subsubsection", "\\paragraph"]

    def flush_list():
        nonlocal in_list, list_type
        if in_list:
            output.append(r"\end{itemize}" if list_type == "ul" else r"\end{enumerate}")
            in_list = False
            list_type = None

    def flush_table():
        nonlocal table_buffer
        if table_buffer:
            output.append(md_table_to_latex(table_buffer))
            table_buffer = []

    while i < len(lines):
        line = lines[i]

        # ── Code blocks ──
        if line.strip().startswith("```"):
            flush_list()
            flush_table()
            if not in_code:
                in_code = True
                code_buffer = []
                i += 1
                continue
            else:
                in_code = False
                output.append(r"\begin{verbatim}")
                output.extend(code_buffer)
                output.append(r"\end{verbatim}")
                code_buffer = []
                i += 1
                continue

        if in_code:
            code_buffer.append(line)
            i += 1
            continue

        # ── Table rows ──
        if line.strip().startswith("|"):
            flush_list()
            table_buffer.append(line)
            i += 1
            continue
        elif table_buffer:
            flush_table()

        # ── Headings ──
        heading_match = re.match(r'^(#{1,4})\s+(.*)', line)
        if heading_match:
            flush_list()
            flush_table()
            level = len(heading_match.group(1)) - 1 + section_offset
            level = min(level, len(SECTION_CMDS) - 1)
            cmd = SECTION_CMDS[level]
            title = md_inline_to_latex(heading_match.group(2))
            output.append(f"{cmd}{{{title}}}")
            i += 1
            continue

        # ── Horizontal rules ──
        if re.match(r'^---+$', line.strip()) or re.match(r'^\*\*\*+$', line.strip()):
            flush_list()
            output.append(r"\noindent\rule{\linewidth}{0.4pt}")
            i += 1
            continue

        # ── Unordered lists ──
        ul_match = re.match(r'^(\s*)[-*+]\s+(.*)', line)
        if ul_match:
            if not in_list or list_type != "ul":
                flush_list()
                output.append(r"\begin{itemize}")
                in_list = True
                list_type = "ul"
            output.append(f"  \\item {md_inline_to_latex(ul_match.group(2))}")
            i += 1
            continue

        # ── Ordered lists ──
        ol_match = re.match(r'^(\s*)\d+[.)]\s+(.*)', line)
        if ol_match:
            if not in_list or list_type != "ol":
                flush_list()
                output.append(r"\begin{enumerate}")
                in_list = True
                list_type = "ol"
            output.append(f"  \\item {md_inline_to_latex(ol_match.group(2))}")
            i += 1
            continue

        # ── End of list ──
        if in_list and line.strip() == "":
            flush_list()
            output.append("")
            i += 1
            continue

        # ── Blockquotes ──
        bq_match = re.match(r'^>\s*(.*)', line)
        if bq_match:
            flush_list()
            output.append(r"\begin{quote}")
            output.append(md_inline_to_latex(bq_match.group(1)))
            output.append(r"\end{quote}")
            i += 1
            continue

        # ── Blank lines ──
        if line.strip() == "":
            flush_list()
            output.append("")
            i += 1
            continue

        # ── Regular paragraph text ──
        flush_list()
        output.append(md_inline_to_latex(line))
        i += 1

    flush_list()
    flush_table()

    return "\n".join(output)


# ── Outline parsing ────────────────────────────────────────────────────────────

def parse_outline(outline_path: Path) -> dict:
    result = {
        "title": "Research Paper",
        "authors": "Author Names",
        "affiliation": "",
        "abstract": "",
        "sections": [],
        "venue": "article",
    }

    if not outline_path.exists():
        return result

    text = outline_path.read_text(encoding="utf-8", errors="ignore")
    lines = text.split("\n")

    for line in lines:
        m = re.match(r'^#\s+(.*)', line)
        if m:
            result["title"] = m.group(1).strip()
            break

    for line in lines:
        if re.search(r'\bauthor', line, re.IGNORECASE) and ":" in line:
            result["authors"] = line.split(":", 1)[1].strip()
            break

    abs_start = None
    for i, line in enumerate(lines):
        if re.match(r'^#{1,3}\s+Abstract', line, re.IGNORECASE):
            abs_start = i + 1
            break
    if abs_start is not None:
        abs_lines = []
        for line in lines[abs_start:]:
            if re.match(r'^#{1,3}\s+', line):
                break
            abs_lines.append(line)
        result["abstract"] = " ".join(l.strip() for l in abs_lines if l.strip())

    in_sections = False
    for line in lines:
        if re.match(r'^#{1,3}\s+Abstract', line, re.IGNORECASE):
            in_sections = True
            continue
        if in_sections:
            m = re.match(r'^#{1,3}\s+(.*)', line)
            if m:
                sec = m.group(1).strip()
                if sec.lower() not in ("abstract", "references", "bibliography"):
                    result["sections"].append(sec)

    return result


def find_draft(drafts_dir: Path, section_name: str) -> Path | None:
    def normalize(s):
        s = s.lower()
        s = re.sub(r'[^a-z0-9一-鿿 ]', '', s)
        s = s.strip().replace(' ', '-')
        return s

    target = normalize(section_name)
    candidates = list(drafts_dir.glob("*.md"))

    for f in candidates:
        if normalize(f.stem) == target:
            return f
    for f in candidates:
        norm = normalize(f.stem)
        if target in norm or norm in target:
            return f
    return None


def read_status(papers_dir: Path) -> dict:
    status_path = papers_dir / "STATUS.md"
    statuses = {}
    if not status_path.exists():
        return statuses
    text = status_path.read_text(encoding="utf-8", errors="ignore")
    for line in text.split("\n"):
        m = re.match(r'.*\|\s*([^|]+?)\s*\|\s*(DRAFT|REVIEWED|APPROVED)\s*\|', line)
        if m:
            statuses[m.group(1).strip().lower()] = m.group(2).strip()
    return statuses


# ── Main assembler ─────────────────────────────────────────────────────────────

def assemble(outline_path, drafts_dir, output_path, venue, no_compile):
    messages = []
    papers_dir = outline_path.parent

    meta = parse_outline(outline_path)
    statuses = read_status(papers_dir)

    preamble = VENUE_PREAMBLES.get(venue, VENUE_PREAMBLES["article"])

    doc = []
    doc.append(preamble)
    doc.append("")
    doc.append(f"\\title{{{meta['title']}}}")
    doc.append("")
    doc.append(f"\\author{{{meta['authors']}}}")
    doc.append("")
    doc.append(r"\begin{document}")
    doc.append(r"\maketitle")
    doc.append("")

    if meta["abstract"]:
        doc.append(r"\begin{abstract}")
        doc.append(md_inline_to_latex(meta["abstract"]))
        doc.append(r"\end{abstract}")
    else:
        abs_draft = find_draft(drafts_dir, "abstract")
        if abs_draft:
            abs_text = abs_draft.read_text(encoding="utf-8", errors="ignore")
            abs_text = re.sub(r'^---.*?---\s*', '', abs_text, flags=re.DOTALL)
            abs_text = re.sub(r'^#{1,3}[^#\n][^\n]*\n', '', abs_text, count=1)
            doc.append(r"\begin{abstract}")
            doc.append(md_inline_to_latex(abs_text.strip()))
            doc.append(r"\end{abstract}")
        else:
            doc.append(r"\begin{abstract}")
            doc.append(r"% TODO: Write abstract")
            doc.append(r"\end{abstract}")
            messages.append("WARNING: No abstract found — placeholder inserted.")

    doc.append("")

    section_order = meta["sections"]
    if not section_order:
        all_drafts = sorted(drafts_dir.glob("*.md"))
        section_order = [f.stem.replace("-", " ").title() for f in all_drafts
                         if f.stem.lower() not in ("abstract",)]
        messages.append("NOTE: No section order in outline — using alphabetical draft order.")

    included = []
    missing = []

    for section in section_order:
        if section.lower() in ("abstract",):
            continue

        draft_file = find_draft(drafts_dir, section)
        sec_status = statuses.get(section.lower(), "DRAFT")

        if draft_file is None:
            doc.append(f"% ── MISSING SECTION: {section} ──")
            doc.append(f"\\section{{{section}}}")
            doc.append(f"% TODO: No draft found — run /write-section {section.lower()}")
            doc.append("")
            missing.append(section)
            messages.append(f"WARNING: No draft for '{section}'.")
            continue

        content = draft_file.read_text(encoding="utf-8", errors="ignore")
        content = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)
        content = re.sub(r'^#{1,3}[^#\n][^\n]*\n', '', content, count=1)

        if sec_status != "APPROVED":
            doc.append(f"% TODO: '{section}' is {sec_status}")

        doc.append(f"\\section{{{md_inline_to_latex(section)}}}")
        doc.append(md_to_latex(content.strip()))
        doc.append("")
        included.append(section)

    # References
    bib_path = papers_dir.parent / "literature" / "bibliography.bib"
    alt_bib_path = papers_dir / "references.bib"

    doc.append(r"\newpage")
    if bib_path.exists():
        doc.append(r"\bibliographystyle{plainnat}")
        doc.append(f"\\bibliography{{{str(bib_path.with_suffix(''))}}}")
    elif alt_bib_path.exists():
        doc.append(r"\bibliographystyle{plainnat}")
        doc.append(f"\\bibliography{{{str(alt_bib_path.with_suffix(''))}}}")
    else:
        doc.append(r"\begin{thebibliography}{99}")
        doc.append(r"% TODO: Add references")
        doc.append(r"\end{thebibliography}")

    doc.append("")
    doc.append(r"\end{document}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(doc), encoding="utf-8")

    if included:
        messages.insert(0, f"OK: Included: {', '.join(included)}")
    if missing:
        messages.insert(1, f"MISSING: {', '.join(missing)}")

    return messages


# ── PDF compilation ────────────────────────────────────────────────────────────

def try_engine(engine: str, tex_path: Path, extra_args: list[str] = []) -> tuple[bool, str]:
    """Try one LaTeX engine. Returns (success, message)."""
    if not shutil.which(engine):
        return False, f"{engine} not found"

    out_dir = tex_path.parent
    cmd = [engine] + extra_args + [
        "-interaction=nonstopmode",
        f"-output-directory={out_dir}",
        str(tex_path),
    ]

    for _pass in range(2):  # two passes for cross-references
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        except subprocess.TimeoutExpired:
            return False, f"{engine} timed out"
        except Exception as e:
            return False, f"{engine} error: {e}"

    pdf_path = tex_path.with_suffix(".pdf")
    if pdf_path.exists():
        return True, f"PDF written to {pdf_path}"

    # Extract errors from log
    log_lines = (result.stdout + result.stderr).split("\n")
    errors = [l for l in log_lines if l.startswith("!") or "Error" in l][:8]
    return False, f"{engine} failed:\n" + "\n".join(errors)


def compile_pdf(tex_path: Path, venue: str) -> tuple[bool, str]:
    """
    Try multiple LaTeX engines in order of preference.
    CJK venues (ctex) require xelatex — try it first.
    Falls back through lualatex → tectonic → pdflatex.
    """
    needs_xelatex = venue in XELATEX_VENUES

    if needs_xelatex:
        engine_order = ["xelatex", "lualatex", "tectonic", "pdflatex"]
    else:
        engine_order = ["pdflatex", "xelatex", "lualatex", "tectonic"]

    attempts = []
    for engine in engine_order:
        extra = []
        # tectonic uses different flags
        if engine == "tectonic":
            if not shutil.which("tectonic"):
                attempts.append("tectonic not found")
                continue
            cmd = ["tectonic", str(tex_path)]
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
                pdf_path = tex_path.with_suffix(".pdf")
                if pdf_path.exists():
                    return True, f"PDF written to {pdf_path}"
                attempts.append(f"tectonic failed: {result.stderr[:200]}")
            except Exception as e:
                attempts.append(f"tectonic error: {e}")
            continue

        ok, msg = try_engine(engine, tex_path, extra)
        if ok:
            return True, msg
        attempts.append(msg)

    # All engines failed — give install advice
    if needs_xelatex:
        install_hint = (
            "This document uses CJK/Chinese (ctexart) and requires XeLaTeX.\n"
            "  Install options:\n"
            "    Windows:  winget install MiKTeX.MiKTeX  (then: xelatex --version)\n"
            "    Mac:      brew install --cask mactex\n"
            "    Linux:    apt install texlive-xetex texlive-lang-chinese\n"
            "    Any OS:   install tectonic → https://tectonic-typesetting.github.io\n"
            "  Or upload main.tex to Overleaf and select XeLaTeX as the compiler."
        )
    else:
        install_hint = (
            "  Install options:\n"
            "    Windows:  winget install MiKTeX.MiKTeX\n"
            "    Mac:      brew install --cask mactex\n"
            "    Linux:    apt install texlive-full\n"
            "  Or upload main.tex to Overleaf."
        )

    return False, "No LaTeX engine found.\n" + install_hint + "\n\nAttempts:\n" + "\n".join(f"  - {a}" for a in attempts)


# ── CLI entry point ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Assemble and compile a LaTeX research paper.")
    parser.add_argument("--outline",    default="papers/outline.md")
    parser.add_argument("--drafts-dir", default="papers/drafts")
    parser.add_argument("--output",     default="papers/main.tex")
    parser.add_argument("--venue",      default="article",
                        choices=list(VENUE_PREAMBLES.keys()),
                        help="ctex = Chinese document (requires XeLaTeX)")
    parser.add_argument("--no-compile", action="store_true")
    args = parser.parse_args()

    outline_path = Path(args.outline)
    drafts_dir   = Path(args.drafts_dir)
    output_path  = Path(args.output)
    venue        = args.venue

    if not outline_path.exists():
        print(f"ERROR: Outline not found at {outline_path}", file=sys.stderr)
        sys.exit(1)

    if not drafts_dir.exists() or not any(drafts_dir.glob("*.md")):
        print(f"ERROR: No drafts found in {drafts_dir}", file=sys.stderr)
        sys.exit(1)

    print(f"Assembling {drafts_dir}/ → {output_path}  (venue: {venue})")
    messages = assemble(outline_path, drafts_dir, output_path, venue, args.no_compile)

    print("\n── Assembly ─────────────────────────────────────────")
    for msg in messages:
        print(f"  {msg}")
    print(f"\n  LaTeX: {output_path}")

    if args.no_compile:
        print("\n  [--no-compile] Skipping PDF compilation.")
        sys.exit(0)

    print("\n── Compiling PDF ────────────────────────────────────")
    success, log = compile_pdf(output_path, venue)

    if success:
        print(f"  ✅ {log}")
    else:
        print(f"  ❌ {log}")
        sys.exit(2)


if __name__ == "__main__":
    main()
