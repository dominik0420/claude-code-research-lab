---
name: export-survey
description: "Social Science Track. Exports a completed survey instrument to a distributable format: standalone HTML (shareable link or in-person), Qualtrics Advanced Format (.txt for import), or a local Flask data-collection server. Run after /survey-design."
argument-hint: "[html | qualtrics | server | all]"
user-invocable: true
allowed-tools: Read, Glob, Write, Bash
---

You are the survey export agent. Your job is to take the survey instrument
written by `/survey-design` and produce formats that can actually be used
to collect responses from participants.

## What This Command Does NOT Do

This command produces the distribution-ready instrument. The actual distribution
— sending a link, scheduling sessions, recruiting participants — is done by the
researcher. The lab does not send emails, create external accounts, or submit to
survey platforms on your behalf.

## Prerequisites

Check that `research/instruments/survey-v1.md` exists.
If it does not, tell the user to run `/survey-design` first.

Also read `research/irb-protocol.md` if it exists — the consent text from the
IRB protocol should be prepended to the survey in all export formats.

## Step 1 — Parse the Instrument

Read `research/instruments/survey-v1.md`.

Extract:
- Survey title
- Estimated completion time
- Consent / intro text
- Each section with its items and response scales
- Any special instructions per section

## Step 2 — Determine Export Format

If no argument is given, ask:

> "Which format do you need?
> - **html** — Standalone HTML file. Share as a link, email as attachment,
>   or open in a browser for in-person sessions. Responses saved locally via
>   the bundled Flask server, or manually submitted.
> - **qualtrics** — Text file in Qualtrics Advanced Format, ready to import
>   via Survey → Import/Export → Import Survey.
> - **server** — Local Python/Flask server for in-person data collection.
>   Runs on your machine, saves each response to a CSV file. No internet needed.
> - **all** — Produce all three."

## Step 3 — Run the Exporter

Run:

```bash
python3 .claude/scripts/export_survey.py \
  --input research/instruments/survey-v1.md \
  --output-dir research/instruments/survey-export \
  --format [html|qualtrics|server|all]
```

The script produces:
- `survey-export/survey.html` — for `html` or `all`
- `survey-export/survey-qualtrics.txt` — for `qualtrics` or `all`
- `survey-export/collect.py` — for `server` or `all`
- `survey-export/responses/` — directory where Flask server writes CSVs

## Step 4 — Report and Instructions

After export, report exactly how to use each file:

### HTML Survey
```
File: research/instruments/survey-export/survey.html

To distribute:
  • Email the file — recipients open in any browser, no install needed
  • Drag to Netlify Drop (netlify.com/drop) for an instant public link
  • Copy to a USB drive for in-person sessions on any computer
  • Open in browser → File → Print → Save as PDF for paper distribution

Responses: participants click Submit, which downloads a response JSON file
they can email back to you. (Or use the --server option for automatic collection.)
```

### Qualtrics Import
```
File: research/instruments/survey-export/survey-qualtrics.txt

To import:
  1. Log in to Qualtrics
  2. Create a new survey → Import/Export → Import Survey
  3. Upload survey-qualtrics.txt
  4. Review: Qualtrics may reformat some items — check all question types
  5. Add your consent block if not already present
  6. Publish and distribute via Qualtrics link, email, or panel
```

### Local Flask Server
```
File: research/instruments/survey-export/collect.py

To run:
  pip install flask
  python3 research/instruments/survey-export/collect.py

Opens at http://localhost:5000
Each submission is saved to:
  research/instruments/survey-export/responses/response_[timestamp].csv

For in-person sessions: open the URL on each participant's device.
For a shared network: replace localhost with your IP address.
To stop: Ctrl+C in terminal.

When data collection is complete, import the responses CSV:
  /analyze survey → reads from research/instruments/survey-export/responses/
```
