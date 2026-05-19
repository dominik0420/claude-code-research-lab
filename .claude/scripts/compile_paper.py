#!/usr/bin/env python3
"""
compile_paper.py — Claude Code Research Lab
Assembles markdown section drafts into a LaTeX paper and optionally compiles to PDF.

Usage:
    python3 .claude/scripts/compile_paper.py \
        --outline papers/outline.md \
        --drafts-dir papers/drafts \
        --output papers/main.tex \
        --venue neurips \
        [--no-compile]
"""

import argparse
import os
import re
import subprocess
import sys
from pathlib import Path


# ── Venue templates ────────────────────────────────────────────────────────────

VENUE_PREAMBLES = {
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
    # Protect math spans first (don't touch $...$)
    math_spans = {}
    def protect_math(m):
        key = f"MATHSPAN{len(math_spans)}END"
        math_spans[key] = m.group(0)
        return key
    text = re.sub(r'\$[^$]+\$', protect_math, text)

    # Bold+italic
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'\\textbf{\\textit{\1}}', text)
    # Bold
    text = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', text)
    text = re.sub(r'__(.+?)__', r'\\textbf{\1}', text)
    # Italic
    text = re.sub(r'\*(.+?)\*', r'\\textit{\1}', text)
    text = re.sub(r'_(.+?)_', r'\\textit{\1}', text)
    # Inline code
    text = re.sub(r'`([^`]+)`', r'\\texttt{\1}', text)
    # Links: [text](url) → text\footnote{url}
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1\\footnote{\\url{\2}}', text)

    # Restore math
    for key, val in math_spans.items():
        text = text.replace(key, val)

    return text


def md_table_to_latex(lines: list[str]) -> str:
    """Convert a markdown table block to a LaTeX booktabs table."""
    rows = []
    for line in lines:
        # Strip leading/trailing pipes and whitespace
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)

    if len(rows) < 2:
        return "\n".join(lines)

    header = rows[0]
    # rows[1] is the separator line — skip
    data = rows[2:]

    ncols = len(header)
    col_spec = "l" * ncols  # all left-aligned; could infer from content

    out = []
    out.append(r"\begin{table}[h]")
    out.append(r"\centering")
    out.append(f"\\begin{{tabular}}{{{col_spec}}}")
    out.append(r"\toprule")
    out.append(" & ".join(md_inline_to_latex(h) for h in header) + r" \\")
    out.append(r"\midrule")
    for row in data:
        # Pad or trim to ncols
        while len(row) < ncols:
            row.append("")
        out.append(" & ".join(md_inline_to_latex(c) for c in row[:ncols]) + r" \\")
    out.append(r"\bottomrule")
    out.append(r"\end{tabular}")
    out.append(r"\caption{[Caption]}")
    out.append(r"\label{tab:unlabeled}")
    out.append(r"\end{table}")
    return "\n".join(out)


def md_to_latex(md_text: str, section_offset: int = 0) -> str:
    """
    Convert a markdown string to LaTeX body content.
    section_offset: 0 = \section, 1 = \subsection, 2 = \subsubsection
    """
    section_cmds = [r"\section", r"\subsection", r"\subsubsection"]

    lines = md_text.split("\n")
    output = []
    i = 0

    in_code_block = False
    code_lang = ""
    code_lines = []

    in_list = False
    list_type = None   # "ul" or "ol"

    table_lines = []
    in_table = False

    def flush_list():
        nonlocal in_list, list_type
        if not in_list:
            return
        env = "itemize" if list_type == "ul" else "enumerate"
        output.append(f"\\begin{{{env}}}")
        # items were already appended with \item prefix
        output.append(f"\\end{{{env}}}")
        in_list = False
        list_type = None

    def flush_table():
        nonlocal in_table, table_lines
        if table_lines:
            output.append(md_table_to_latex(table_lines))
        in_table = False
        table_lines = []

    while i < len(lines):
        line = lines[i]

        # ── Code blocks ──
        if line.strip().startswith("```"):
            if in_code_block:
                # End block
                output.append(r"\end{verbatim}")
                if code_lang in ("python", "bash", "sh", "yaml", "json"):
                    pass  # could use lstlisting but verbatim is safe
                in_code_block = False
            else:
                flush_list()
                flush_table()
                code_lang = line.strip().lstrip("`").strip().lower()
                output.append(r"\begin{verbatim}")
                in_code_block = True
            i += 1
            continue

        if in_code_block:
            output.append(line)
            i += 1
            continue

        # ── Table detection ──
        if re.match(r'^\s*\|', line):
            in_table = True
            table_lines.append(line)
            i += 1
            continue
        elif in_table:
            flush_table()

        # ── Headings ──
        heading_match = re.match(r'^(#{1,4})\s+(.*)', line)
        if heading_match:
            flush_list()
            hashes = heading_match.group(1)
            title = heading_match.group(2).strip()
            depth = min(len(hashes) - 1 + section_offset, len(section_cmds) - 1)
            cmd = section_cmds[depth]
            # Strip trailing # if present
            title = title.rstrip("#").strip()
            # Don't escape inside heading — md_inline handles it
            output.append(f"{cmd}{{{md_inline_to_latex(title)}}}")
            i += 1
            continue

        # ── Horizontal rules ──
        if re.match(r'^---+$', line.strip()) or re.match(r'^\*\*\*+$', line.strip()):
            flush_list()
            output.append(r"\medskip\noindent\rule{\linewidth}{0.4pt}\medskip")
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
    """Extract title, authors, abstract, and section order from the outline."""
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

    # Title: first # heading
    for line in lines:
        m = re.match(r'^#\s+(.*)', line)
        if m:
            result["title"] = m.group(1).strip()
            break

    # Authors: look for "Author" or "Authors" line
    for i, line in enumerate(lines):
        if re.search(r'\bauthor', line, re.IGNORECASE) and ":" in line:
            result["authors"] = line.split(":", 1)[1].strip()
            break

    # Abstract block
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

    # Section names: ## headings (after Abstract)
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
    """Find the draft file for a section by fuzzy name matching."""
    # Normalize: lowercase, remove punctuation, spaces → hyphens
    def normalize(s):
        s = s.lower()
        s = re.sub(r'[^a-z0-9 ]', '', s)
        s = s.strip().replace(' ', '-')
        return s

    target = normalize(section_name)
    candidates = list(drafts_dir.glob("*.md"))

    for f in candidates:
        if normalize(f.stem) == target:
            return f

    # Partial match
    for f in candidates:
        norm = normalize(f.stem)
        if target in norm or norm in target:
            return f

    return None


def read_status(papers_dir: Path) -> dict:
    """Read papers/STATUS.md and return {section_name: status}."""
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

def assemble(
    outline_path: Path,
    drafts_dir: Path,
    output_path: Path,
    venue: str,
    no_compile: bool,
) -> list[str]:
    """Assemble LaTeX file. Returns list of warning/info messages."""
    messages = []
    papers_dir = outline_path.parent

    # Parse outline
    meta = parse_outline(outline_path)
    statuses = read_status(papers_dir)

    # Venue preamble
    preamble = VENUE_PREAMBLES.get(venue, VENUE_PREAMBLES["article"])

    # Build document
    doc = []
    doc.append(preamble)
    doc.append("")

    # Title block
    doc.append(f"\\title{{{meta['title']}}}")
    doc.append("")

    if venue in ("neurips", "icml", "iclr"):
        doc.append(f"\\author{{{meta['authors']}}}")
    elif venue == "acl":
        doc.append(f"\\author{{{meta['authors']}}}")
    else:
        doc.append(f"\\author{{{meta['authors']}}}")

    doc.append("")
    doc.append(r"\begin{document}")
    doc.append(r"\maketitle")
    doc.append("")

    # Abstract
    if meta["abstract"]:
        doc.append(r"\begin{abstract}")
        doc.append(md_inline_to_latex(meta["abstract"]))
        doc.append(r"\end{abstract}")
    else:
        # Try to find abstract draft
        abs_draft = find_draft(drafts_dir, "abstract")
        if abs_draft:
            abs_text = abs_draft.read_text(encoding="utf-8", errors="ignore")
            # Strip any markdown heading from the top
            abs_text = re.sub(r'^#.*\n', '', abs_text, count=1)
            doc.append(r"\begin{abstract}")
            doc.append(md_inline_to_latex(abs_text.strip()))
            doc.append(r"\end{abstract}")
        else:
            doc.append(r"\begin{abstract}")
            doc.append(r"% TODO: Write abstract")
            doc.append(r"\end{abstract}")
            messages.append("WARNING: No abstract found — placeholder inserted.")

    doc.append("")

    # Sections
    section_order = meta["sections"] if meta["sections"] else []

    # If no sections in outline, fall back to all drafts alphabetically
    if not section_order:
        all_drafts = sorted(drafts_dir.glob("*.md"))
        section_order = [f.stem.replace("-", " ").title() for f in all_drafts
                         if f.stem.lower() not in ("abstract",)]
        messages.append("NOTE: No section order found in outline — using alphabetical draft order.")

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
            doc.append(f"% TODO: No draft found for this section. Run /write-section {section.lower()}")
            doc.append("")
            missing.append(section)
            messages.append(f"WARNING: No draft found for section '{section}'.")
            continue

        content = draft_file.read_text(encoding="utf-8", errors="ignore")

        # Strip leading YAML frontmatter if present
        content = re.sub(r'^---.*?---\s*', '', content, flags=re.DOTALL)

        # Strip the first heading (section heading is added by \section{})
        content = re.sub(r'^#{1,3}[^#\n][^\n]*\n', '', content, count=1)

        if sec_status != "APPROVED":
            doc.append(f"% TODO: Section '{section}' is {sec_status} — review before submission")

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
        doc.append(r"\bibliographystyle{plainnat}")
        doc.append(r"% \bibliography{references}  % Uncomment and point to your .bib file")
        doc.append(r"\begin{thebibliography}{99}")
        doc.append(r"% TODO: Add references or create literature/bibliography.bib")
        doc.append(r"\end{thebibliography}")
        messages.append("NOTE: No .bib file found — placeholder bibliography inserted.")

    doc.append("")
    doc.append(r"\end{document}")

    # Write output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(doc), encoding="utf-8")

    if included:
        messages.insert(0, f"OK: Included sections: {', '.join(included)}")
    if missing:
        messages.insert(1, f"MISSING sections: {', '.join(missing)}")

    return messages


# ── PDF compilation ────────────────────────────────────────────────────────────

def compile_pdf(tex_path: Path) -> tuple[bool, str]:
    """Run pdflatex twice on the tex file. Returns (success, log_excerpt)."""
    out_dir = tex_path.parent
    cmd = [
        "pdflatex",
        "-interaction=nonstopmode",
        f"-output-directory={out_dir}",
        str(tex_path),
    ]

    errors = []
    success = False

    for pass_num in range(1, 3):
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120,
            )
            if result.returncode == 0:
                success = True
            else:
                # Extract error lines from log
                log_lines = (result.stdout + result.stderr).split("\n")
                errors = [l for l in log_lines if l.startswith("!") or "Error" in l][:10]
        except FileNotFoundError:
            return False, "pdflatex not found — install TeX Live or MiKTeX, or upload main.tex to Overleaf."
        except subprocess.TimeoutExpired:
            return False, "pdflatex timed out after 120s."
        except Exception as e:
            return False, f"pdflatex error: {e}"

    if success:
        pdf_path = tex_path.with_suffix(".pdf")
        if pdf_path.exists():
            return True, f"PDF written to {pdf_path}"
        else:
            return False, "pdflatex exited 0 but no PDF found."
    else:
        return False, "Compilation errors:\n" + "\n".join(errors)


# ── CLI entry point ────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Assemble and compile a LaTeX research paper.")
    parser.add_argument("--outline",    default="papers/outline.md",  help="Path to outline.md")
    parser.add_argument("--drafts-dir", default="papers/drafts",      help="Directory of section drafts")
    parser.add_argument("--output",     default="papers/main.tex",    help="Output .tex file path")
    parser.add_argument("--venue",      default="article",
                        choices=["neurips", "icml", "iclr", "acl", "cvpr", "article"],
                        help="Target venue (determines LaTeX class)")
    parser.add_argument("--no-compile", action="store_true",
                        help="Write .tex only, do not run pdflatex")
    args = parser.parse_args()

    outline_path = Path(args.outline)
    drafts_dir   = Path(args.drafts_dir)
    output_path  = Path(args.output)
    venue        = args.venue

    # ── Validate inputs ──
    if not outline_path.exists():
        print(f"ERROR: Outline not found at {outline_path}", file=sys.stderr)
        print("Run /outline-paper first to create the paper outline.", file=sys.stderr)
        sys.exit(1)

    if not drafts_dir.exists() or not any(drafts_dir.glob("*.md")):
        print(f"ERROR: No draft files found in {drafts_dir}", file=sys.stderr)
        print("Run /team-writing first to produce section drafts.", file=sys.stderr)
        sys.exit(1)

    # ── Assemble ──
    print(f"Assembling paper from {drafts_dir}/ → {output_path} (venue: {venue})")
    messages = assemble(outline_path, drafts_dir, output_path, venue, args.no_compile)

    print("\n── Assembly report ──────────────────────────────────")
    for msg in messages:
        print(f"  {msg}")
    print(f"\n  LaTeX written to: {output_path}")

    if args.no_compile:
        print("\n  [--no-compile] Skipping PDF compilation.")
        print("  Upload main.tex to Overleaf or run: pdflatex papers/main.tex")
        sys.exit(0)

    # ── Compile ──
    print("\n── Compiling PDF (2 passes) ─────────────────────────")
    success, log = compile_pdf(output_path)

    if success:
        pdf_path = output_path.with_suffix(".pdf")
        print(f"  ✅ PDF compiled successfully: {pdf_path}")
    else:
        print(f"  ❌ PDF compilation failed:")
        for line in log.split("\n"):
            print(f"     {line}")
        print("\n  The .tex file is still usable — upload to Overleaf if pdflatex is unavailable.")
        sys.exit(2)


if __name__ == "__main__":
    main()
