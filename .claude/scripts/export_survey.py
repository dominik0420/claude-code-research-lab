#!/usr/bin/env python3
"""
export_survey.py — Claude Code Research Lab
Converts a markdown survey instrument into distributable formats.

Outputs (selected by --format):
  html       → standalone HTML survey with CSS/JS, submit downloads JSON
  qualtrics  → Qualtrics Advanced Format (.txt) for Survey Import
  server     → Flask data-collection server + HTML form

Usage:
    python3 .claude/scripts/export_survey.py \
        --input research/instruments/survey-v1.md \
        --output-dir research/instruments/survey-export \
        --format all
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from dataclasses import dataclass, field


# ── Survey data model ──────────────────────────────────────────────────────────

@dataclass
class Item:
    number: int
    text: str
    response_type: str   # likert5 | likert7 | text | multiple_choice | yesno
    options: list[str] = field(default_factory=list)
    reverse_scored: bool = False
    required: bool = True


@dataclass
class Section:
    title: str
    instruction: str
    items: list[Item] = field(default_factory=list)
    response_type: str = "likert5"   # section default
    scale_labels: list[str] = field(default_factory=list)


@dataclass
class Survey:
    title: str = "Survey"
    estimated_time: str = ""
    consent_text: str = ""
    intro_text: str = ""
    sections: list[Section] = field(default_factory=list)


# ── Markdown parser ────────────────────────────────────────────────────────────

def detect_response_type(text: str) -> tuple[str, list[str]]:
    """Infer response type from scale descriptions in text."""
    text_lower = text.lower()
    if re.search(r'1.{0,5}7|7.point|strongly disagree.{0,30}strongly agree', text_lower):
        labels = ["Strongly Disagree", "Disagree", "Somewhat Disagree",
                  "Neutral", "Somewhat Agree", "Agree", "Strongly Agree"]
        return "likert7", labels
    if re.search(r'1.{0,5}5|5.point|strongly disagree.{0,30}agree', text_lower):
        labels = ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]
        return "likert5", labels
    if re.search(r'yes.{0,10}no|true.{0,10}false', text_lower):
        return "yesno", ["Yes", "No"]
    if re.search(r'open.ended|free.text|short answer|paragraph', text_lower):
        return "text", []
    # Multiple choice: look for a) b) c) or bullet options
    if re.search(r'^\s*[a-d][).]\s', text, re.MULTILINE):
        options = re.findall(r'^\s*[a-d][).]\s+(.*)', text, re.MULTILINE)
        return "multiple_choice", options
    return "likert5", ["Strongly Disagree", "Disagree", "Neutral", "Agree", "Strongly Agree"]


def parse_survey_md(path: Path) -> Survey:
    """Parse a survey instrument markdown file into a Survey object."""
    text = path.read_text(encoding="utf-8", errors="ignore")

    # Strip YAML frontmatter
    text = re.sub(r'^---.*?---\s*', '', text, flags=re.DOTALL)

    survey = Survey()
    lines = text.split('\n')
    i = 0
    item_counter = 1
    current_section: Section | None = None

    def flush_section():
        if current_section and current_section.items:
            survey.sections.append(current_section)

    while i < len(lines):
        line = lines[i]

        # Title
        if re.match(r'^#\s+', line) and not survey.title:
            survey.title = line.lstrip('#').strip()
            i += 1
            continue

        # Estimated time
        tm = re.search(r'[Ee]stimated\s+time[:\s]+([^\n]+)', line)
        if tm:
            survey.estimated_time = tm.group(1).strip()
            i += 1
            continue

        # Section heading
        sec_match = re.match(r'^#{2,3}\s+(.*)', line)
        if sec_match:
            flush_section()
            sec_title = sec_match.group(1).strip()
            # Collect instruction lines until next heading or item
            instruction_lines = []
            j = i + 1
            while j < len(lines) and not re.match(r'^#{1,3}\s+', lines[j]) \
                    and not re.match(r'^\s*\d+[.)]\s+', lines[j]):
                if lines[j].strip():
                    instruction_lines.append(lines[j].strip())
                j += 1

            instruction = ' '.join(instruction_lines)
            rtype, labels = detect_response_type(instruction)
            current_section = Section(
                title=sec_title,
                instruction=instruction,
                response_type=rtype,
                scale_labels=labels,
            )
            i = j
            continue

        # Numbered item: "1. Item text" or "1) Item text"
        item_match = re.match(r'^\s*(\d+)[.)]\s+(.*)', line)
        if item_match and current_section is not None:
            item_text = item_match.group(2).strip()
            reverse = item_text.endswith('(R)') or item_text.endswith('(r)')
            item_text = re.sub(r'\s*\([Rr]\)\s*$', '', item_text)

            # Collect any continuation lines (for multi-line items)
            j = i + 1
            while j < len(lines) and lines[j].strip() \
                    and not re.match(r'^\s*\d+[.)]\s+', lines[j]) \
                    and not re.match(r'^#{1,3}\s+', lines[j]):
                item_text += ' ' + lines[j].strip()
                j += 1

            item = Item(
                number=item_counter,
                text=item_text,
                response_type=current_section.response_type,
                options=list(current_section.scale_labels),
                reverse_scored=reverse,
            )
            current_section.items.append(item)
            item_counter += 1
            i = j
            continue

        # Consent / intro block heuristic
        if re.search(r'[Cc]onsent|[Ii]nformed|[Pp]urpose of this study', line):
            consent_lines = [line.strip()]
            j = i + 1
            while j < len(lines) and lines[j].strip() \
                    and not re.match(r'^#{1,3}\s+', lines[j]):
                consent_lines.append(lines[j].strip())
                j += 1
            if not survey.consent_text:
                survey.consent_text = ' '.join(consent_lines)
            i = j
            continue

        i += 1

    flush_section()

    # Fallback title
    if not survey.title:
        survey.title = path.stem.replace('-', ' ').replace('_', ' ').title()

    return survey


# ── HTML export ────────────────────────────────────────────────────────────────

HTML_CSS = """
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        background: #f5f5f5;
        color: #222;
        line-height: 1.6;
    }
    .survey-wrapper {
        max-width: 760px;
        margin: 40px auto;
        background: #fff;
        border-radius: 8px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.10);
        padding: 48px 56px;
    }
    h1 { font-size: 1.8rem; margin-bottom: 8px; color: #111; }
    .meta { color: #666; font-size: 0.9rem; margin-bottom: 32px; }
    .consent {
        background: #f0f4ff;
        border-left: 4px solid #4a6fa5;
        padding: 16px 20px;
        border-radius: 4px;
        margin-bottom: 32px;
        font-size: 0.92rem;
    }
    .section { margin-bottom: 40px; }
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 8px;
        margin-bottom: 12px;
    }
    .section-instruction {
        color: #555;
        font-size: 0.9rem;
        margin-bottom: 20px;
        font-style: italic;
    }
    .item { margin-bottom: 28px; }
    .item-text {
        font-weight: 500;
        margin-bottom: 10px;
        font-size: 0.97rem;
    }
    .item-number {
        color: #888;
        font-size: 0.85rem;
        margin-right: 6px;
    }
    /* Likert scale */
    .likert-scale {
        display: flex;
        gap: 0;
        border: 1px solid #ddd;
        border-radius: 6px;
        overflow: hidden;
    }
    .likert-scale label {
        flex: 1;
        text-align: center;
        padding: 10px 4px 8px;
        cursor: pointer;
        font-size: 0.78rem;
        color: #444;
        border-right: 1px solid #ddd;
        transition: background 0.15s;
    }
    .likert-scale label:last-child { border-right: none; }
    .likert-scale input[type=radio] { display: none; }
    .likert-scale input[type=radio]:checked + span { font-weight: 700; }
    .likert-scale label:has(input:checked) {
        background: #4a6fa5;
        color: #fff;
    }
    .likert-scale label:hover:not(:has(input:checked)) { background: #f0f4ff; }
    /* Text input */
    textarea.response {
        width: 100%;
        min-height: 80px;
        border: 1px solid #ddd;
        border-radius: 6px;
        padding: 10px;
        font-size: 0.95rem;
        font-family: inherit;
        resize: vertical;
    }
    textarea.response:focus { outline: 2px solid #4a6fa5; border-color: transparent; }
    /* Yes/No */
    .yesno-group { display: flex; gap: 16px; }
    .yesno-group label {
        display: flex;
        align-items: center;
        gap: 8px;
        cursor: pointer;
        font-size: 0.95rem;
        padding: 8px 20px;
        border: 1px solid #ddd;
        border-radius: 6px;
    }
    .yesno-group label:has(input:checked) {
        background: #4a6fa5;
        color: #fff;
        border-color: #4a6fa5;
    }
    .yesno-group input[type=radio] { display: none; }
    /* Submit */
    .submit-section { margin-top: 40px; border-top: 2px solid #eee; padding-top: 24px; }
    button.submit-btn {
        background: #4a6fa5;
        color: #fff;
        border: none;
        padding: 14px 40px;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 6px;
        cursor: pointer;
        transition: background 0.2s;
    }
    button.submit-btn:hover { background: #3a5a8f; }
    .validation-msg {
        color: #c0392b;
        font-size: 0.87rem;
        margin-top: 8px;
        display: none;
    }
    .item.error .item-text { color: #c0392b; }
    .item.error .likert-scale { border-color: #c0392b; }
    #confirmation {
        display: none;
        background: #eafaf1;
        border: 1px solid #27ae60;
        border-radius: 6px;
        padding: 20px 24px;
        margin-top: 24px;
        color: #1e8449;
        font-weight: 500;
    }
"""

HTML_JS = """
    function collectResponses() {
        const data = {
            survey_title: document.title,
            submitted_at: new Date().toISOString(),
            responses: {}
        };
        document.querySelectorAll('.item').forEach(item => {
            const id = item.dataset.itemId;
            const radio = item.querySelector('input[type=radio]:checked');
            const textarea = item.querySelector('textarea');
            if (radio) data.responses[id] = radio.value;
            else if (textarea) data.responses[id] = textarea.value;
        });
        return data;
    }

    function validateRequired() {
        let valid = true;
        document.querySelectorAll('.item[data-required="true"]').forEach(item => {
            const id = item.dataset.itemId;
            const radio = item.querySelector('input[type=radio]:checked');
            const textarea = item.querySelector('textarea');
            const answered = radio || (textarea && textarea.value.trim());
            if (!answered) {
                item.classList.add('error');
                valid = false;
            } else {
                item.classList.remove('error');
            }
        });
        return valid;
    }

    function downloadJSON(data) {
        const blob = new Blob([JSON.stringify(data, null, 2)], {type: 'application/json'});
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'survey-response-' + new Date().toISOString().slice(0,19).replace(/:/g,'-') + '.json';
        a.click();
        URL.revokeObjectURL(url);
    }

    function submitSurvey() {
        if (!validateRequired()) {
            document.getElementById('val-msg').style.display = 'block';
            return;
        }
        document.getElementById('val-msg').style.display = 'none';
        const data = collectResponses();

        // Try to POST to local Flask server first; fall back to download
        fetch('/submit', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(data)
        }).then(r => {
            if (r.ok) {
                document.getElementById('confirmation').style.display = 'block';
                document.getElementById('confirmation').textContent =
                    'Response submitted successfully. Thank you for your participation.';
            } else { downloadJSON(data); }
        }).catch(() => {
            downloadJSON(data);
            document.getElementById('confirmation').style.display = 'block';
            document.getElementById('confirmation').textContent =
                'Your response has been downloaded as a JSON file. Please send it to the researcher. Thank you.';
        });
    }
"""


def render_item_html(item: Item) -> str:
    parts = []
    parts.append(f'<div class="item" data-item-id="q{item.number}" data-required="{str(item.required).lower()}">')
    parts.append(f'  <div class="item-text"><span class="item-number">{item.number}.</span> {item.text}</div>')

    if item.response_type in ("likert5", "likert7"):
        parts.append('  <div class="likert-scale">')
        for idx, label in enumerate(item.options, 1):
            parts.append(
                f'    <label>'
                f'<input type="radio" name="q{item.number}" value="{idx}">'
                f'<span>{label}</span></label>'
            )
        parts.append('  </div>')

    elif item.response_type == "text":
        parts.append(f'  <textarea class="response" name="q{item.number}" rows="4" placeholder="Your answer..."></textarea>')

    elif item.response_type == "yesno":
        parts.append('  <div class="yesno-group">')
        for opt in (item.options or ["Yes", "No"]):
            parts.append(
                f'    <label><input type="radio" name="q{item.number}" value="{opt}"> {opt}</label>'
            )
        parts.append('  </div>')

    elif item.response_type == "multiple_choice":
        for idx, opt in enumerate(item.options):
            parts.append(
                f'  <label style="display:block;margin:6px 0;cursor:pointer;">'
                f'<input type="radio" name="q{item.number}" value="{opt}" style="margin-right:8px;"> {opt}</label>'
            )

    parts.append('</div>')
    return '\n'.join(parts)


def export_html(survey: Survey, output_dir: Path) -> Path:
    sections_html = []
    for section in survey.sections:
        items_html = '\n'.join(render_item_html(item) for item in section.items)
        sections_html.append(f"""
<div class="section">
  <div class="section-title">{section.title}</div>
  {'<div class="section-instruction">' + section.instruction + '</div>' if section.instruction else ''}
  {items_html}
</div>""")

    consent_block = ""
    if survey.consent_text:
        consent_block = f'<div class="consent">{survey.consent_text}</div>'

    meta_block = ""
    if survey.estimated_time:
        meta_block = f'<div class="meta">Estimated time: {survey.estimated_time}</div>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{survey.title}</title>
  <style>{HTML_CSS}</style>
</head>
<body>
<div class="survey-wrapper">
  <h1>{survey.title}</h1>
  {meta_block}
  {consent_block}

  {''.join(sections_html)}

  <div class="submit-section">
    <button class="submit-btn" onclick="submitSurvey()">Submit Response</button>
    <div class="validation-msg" id="val-msg">
      Please answer all required questions before submitting.
    </div>
    <div id="confirmation"></div>
  </div>
</div>
<script>{HTML_JS}</script>
</body>
</html>"""

    out_path = output_dir / "survey.html"
    out_path.write_text(html, encoding="utf-8")
    return out_path


# ── Qualtrics Advanced Format export ──────────────────────────────────────────

def export_qualtrics(survey: Survey, output_dir: Path) -> Path:
    """
    Generate Qualtrics Survey File Advanced Format (.txt).
    Reference: https://www.qualtrics.com/support/survey-platform/survey-module/survey-tools/import-and-export-surveys/
    """
    lines = []
    lines.append("[[AdvancedFormat]]")
    lines.append("")
    lines.append(f"[[ED:SurveyTitle]]")
    lines.append(survey.title)
    lines.append("")

    if survey.consent_text:
        lines.append("[[Block:Consent]]")
        lines.append("")
        lines.append("[[Question:Text]]")
        lines.append("[[ID:consent]]")
        lines.append(survey.consent_text)
        lines.append("")
        lines.append("[[Choices]]")
        lines.append("I agree to participate in this study")
        lines.append("")

    for section in survey.sections:
        lines.append(f"[[Block:{section.title}]]")
        lines.append("")

        if section.instruction:
            lines.append("[[Question:DB]]")
            lines.append(f"[[ID:instr_{section.title[:20].replace(' ','_')}]]")
            lines.append(section.instruction)
            lines.append("")

        for item in section.items:
            if item.response_type in ("likert5", "likert7"):
                lines.append("[[Question:Matrix]]")
                lines.append(f"[[ID:q{item.number}]]")
                lines.append(item.text)
                lines.append("[[Choices]]")
                lines.append(item.text)
                lines.append("[[Answers]]")
                for label in item.options:
                    lines.append(label)

            elif item.response_type == "text":
                lines.append("[[Question:TE:Essay]]")
                lines.append(f"[[ID:q{item.number}]]")
                lines.append(item.text)

            elif item.response_type == "yesno":
                lines.append("[[Question:MC:SingleAnswer]]")
                lines.append(f"[[ID:q{item.number}]]")
                lines.append(item.text)
                lines.append("[[Choices]]")
                for opt in (item.options or ["Yes", "No"]):
                    lines.append(opt)

            elif item.response_type == "multiple_choice":
                lines.append("[[Question:MC:SingleAnswer]]")
                lines.append(f"[[ID:q{item.number}]]")
                lines.append(item.text)
                lines.append("[[Choices]]")
                for opt in item.options:
                    lines.append(opt)

            lines.append("")

    out_path = output_dir / "survey-qualtrics.txt"
    out_path.write_text('\n'.join(lines), encoding="utf-8")
    return out_path


# ── Flask data-collection server ───────────────────────────────────────────────

def export_flask_server(survey: Survey, output_dir: Path) -> Path:
    """Generate a self-contained Flask server for in-person data collection."""

    # Embed the survey HTML (same as the standalone version)
    html_path = output_dir / "survey.html"
    if not html_path.exists():
        export_html(survey, output_dir)

    responses_dir = output_dir / "responses"
    responses_dir.mkdir(exist_ok=True)

    # Build the field list for CSV header
    all_items = [item for section in survey.sections for item in section.items]
    field_names = [f"q{item.number}" for item in all_items]
    field_names_repr = repr(["submitted_at", "participant_id"] + field_names)

    server_code = f'''#!/usr/bin/env python3
"""
collect.py — Local survey data collection server
Generated by Claude Code Research Lab / export_survey.py

Run:
    pip install flask
    python3 collect.py

Opens at http://localhost:5000
Responses saved to: responses/response_<timestamp>.csv
Press Ctrl+C to stop.
"""

import csv
import json
import os
import uuid
from datetime import datetime
from pathlib import Path

try:
    from flask import Flask, request, jsonify, send_file
except ImportError:
    print("Flask not installed. Run: pip install flask")
    raise

app = Flask(__name__)
RESPONSES_DIR = Path(__file__).parent / "responses"
RESPONSES_DIR.mkdir(exist_ok=True)
SURVEY_HTML = Path(__file__).parent / "survey.html"

FIELD_NAMES = {field_names_repr}

participant_counter = [0]


@app.route("/")
def index():
    if SURVEY_HTML.exists():
        return send_file(SURVEY_HTML)
    return "<h1>Survey HTML not found. Re-run export_survey.py --format html</h1>", 404


@app.route("/submit", methods=["POST"])
def submit():
    data = request.get_json(force=True)
    participant_counter[0] += 1
    pid = f"P{{participant_counter[0]:04d}}"

    # Flatten responses
    responses = data.get("responses", {{}})
    row = {{
        "submitted_at": datetime.now().isoformat(),
        "participant_id": pid,
    }}
    for field in FIELD_NAMES[2:]:  # skip submitted_at and participant_id
        row[field] = responses.get(field, "")

    # Write to individual CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    csv_path = RESPONSES_DIR / f"response_{{timestamp}}.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
        writer.writeheader()
        writer.writerow(row)

    # Append to master CSV
    master_path = RESPONSES_DIR / "all_responses.csv"
    write_header = not master_path.exists()
    with open(master_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELD_NAMES)
        if write_header:
            writer.writeheader()
        writer.writerow(row)

    print(f"  [{{datetime.now().strftime('%H:%M:%S')}}] Response saved — Participant {{pid}}")
    return jsonify({{"status": "ok", "participant_id": pid}})


@app.route("/count")
def count():
    """Quick status endpoint — how many responses so far."""
    n = len(list(RESPONSES_DIR.glob("response_*.csv")))
    return jsonify({{"responses_collected": n}})


if __name__ == "__main__":
    import socket
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Survey: {survey.title}
  Local:   http://localhost:5000
  Network: http://{{local_ip}}:5000
  Responses saved to: responses/all_responses.csv
  Press Ctrl+C to stop.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
    app.run(host="0.0.0.0", port=5000, debug=False)
'''

    out_path = output_dir / "collect.py"
    out_path.write_text(server_code, encoding="utf-8")
    return out_path


# ── CLI ────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Export a survey instrument to distributable formats.")
    parser.add_argument("--input",      default="research/instruments/survey-v1.md")
    parser.add_argument("--output-dir", default="research/instruments/survey-export")
    parser.add_argument("--format",     default="all",
                        choices=["html", "qualtrics", "server", "all"])
    args = parser.parse_args()

    input_path = Path(args.input)
    output_dir = Path(args.output_dir)

    if not input_path.exists():
        print(f"ERROR: Survey instrument not found at {input_path}", file=sys.stderr)
        print("Run /survey-design first to create the instrument.", file=sys.stderr)
        sys.exit(1)

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "responses").mkdir(exist_ok=True)

    print(f"Parsing survey from {input_path}...")
    survey = parse_survey_md(input_path)

    total_items = sum(len(s.items) for s in survey.sections)
    print(f"  Title: {survey.title}")
    print(f"  Sections: {len(survey.sections)}")
    print(f"  Items: {total_items}")
    print()

    fmt = args.format
    produced = []

    if fmt in ("html", "all"):
        p = export_html(survey, output_dir)
        produced.append(("HTML survey", p))
        print(f"  ✅ HTML → {p}")

    if fmt in ("qualtrics", "all"):
        p = export_qualtrics(survey, output_dir)
        produced.append(("Qualtrics import", p))
        print(f"  ✅ Qualtrics → {p}")

    if fmt in ("server", "all"):
        if fmt == "server" and not (output_dir / "survey.html").exists():
            export_html(survey, output_dir)
        p = export_flask_server(survey, output_dir)
        produced.append(("Flask server", p))
        print(f"  ✅ Flask server → {p}")

    print(f"""
── Distribution instructions ─────────────────────────
  HTML:       Open survey.html in any browser, or drag to netlify.com/drop
  Qualtrics:  Survey → Import/Export → Import Survey → upload .txt file
  Flask:      pip install flask && python3 collect.py
              → http://localhost:5000
              → Responses saved to: {output_dir}/responses/all_responses.csv
""")


if __name__ == "__main__":
    main()
