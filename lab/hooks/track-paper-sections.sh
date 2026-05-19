#!/bin/bash
# track-paper-sections.sh — PostToolUse: Write
# After writing to papers/drafts/, reads the status comment from the first
# line of each section file and updates papers/STATUS.md with a dashboard.
# Status format in draft files: <!-- Status: DRAFT / REVIEWED / APPROVED -->

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib.sh"

INPUT=$(cat)

FILE_PATH=$(echo "$INPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    tool_input = data.get('tool_input', {})
    print(tool_input.get('file_path', '') or tool_input.get('path', ''))
except:
    print('')
" 2>/dev/null)

if ! echo "$FILE_PATH" | grep -q "papers/drafts/"; then
    exit 0
fi

# Export project dir for Python
export PDIR=$(get_project_dir)

# Rebuild the full status dashboard
python3 - <<'PYEOF'
import os, re, datetime, sys

pdir = os.environ.get("PDIR", "")
def ppath(rel):
    return os.path.join(pdir, rel) if pdir else rel

DRAFTS_DIR = ppath("papers/drafts")
STATUS_FILE = ppath("papers/STATUS.md")

SECTION_ORDER = [
    "abstract", "introduction", "related-work", "method",
    "experiments", "results", "discussion", "conclusion", "appendix"
]

STATUS_EMOJI = {
    "APPROVED": "✅",
    "REVIEWED": "🔍",
    "DRAFT": "📝",
    "MISSING": "⬜"
}

rows = []
if os.path.isdir(DRAFTS_DIR):
    for section in SECTION_ORDER:
        filepath = os.path.join(DRAFTS_DIR, f"{section}.md")
        if os.path.exists(filepath):
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                first_line = f.readline().strip()
            match = re.search(r"Status:\s*(DRAFT|REVIEWED|APPROVED)", first_line, re.IGNORECASE)
            status = match.group(1).upper() if match else "DRAFT"
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
            rows.append((section, status, mtime.strftime("%Y-%m-%d")))
        else:
            rows.append((section, "MISSING", "—"))

    # Also check for any extra files not in the ordered list
    for f in sorted(os.listdir(DRAFTS_DIR)):
        name = f.replace(".md", "")
        if name not in SECTION_ORDER and f.endswith(".md"):
            filepath = os.path.join(DRAFTS_DIR, f)
            with open(filepath, "r", encoding="utf-8", errors="ignore") as fh:
                first_line = fh.readline().strip()
            match = re.search(r"Status:\s*(DRAFT|REVIEWED|APPROVED)", first_line, re.IGNORECASE)
            status = match.group(1).upper() if match else "DRAFT"
            mtime = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
            rows.append((name, status, mtime.strftime("%Y-%m-%d")))

lines = [
    f"# Paper Section Status",
    f"",
    f"*Updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}*",
    f"",
    f"| Section | Status | Last Modified |",
    f"|---------|--------|--------------|",
]

for section, status, mtime in rows:
    emoji = STATUS_EMOJI.get(status, "❓")
    lines.append(f"| {section} | {emoji} {status} | {mtime} |")

approved = sum(1 for _, s, _ in rows if s == "APPROVED")
reviewed = sum(1 for _, s, _ in rows if s == "REVIEWED")
drafted = sum(1 for _, s, _ in rows if s == "DRAFT")
total = len([r for r in rows if r[1] != "MISSING"])

lines += [
    "",
    f"**Progress:** {approved} approved / {reviewed} reviewed / {drafted} draft / {total} total sections",
    "",
    "To change a section's status, update the first line of the file:",
    "```",
    "<!-- Status: DRAFT -->",
    "<!-- Status: REVIEWED -->",
    "<!-- Status: APPROVED -->",
    "```",
]

os.makedirs(os.path.dirname(STATUS_FILE), exist_ok=True)
with open(STATUS_FILE, "w") as f:
    f.write("\n".join(lines) + "\n")

print(f"📄 Paper status updated: {approved}/{total} sections approved", file=sys.stderr)
PYEOF

exit 0
