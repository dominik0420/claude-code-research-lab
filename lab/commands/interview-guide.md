---
name: interview-guide
description: "Social Science Track. Design a semi-structured interview or focus group guide: opening, core questions, probes, closing. Includes facilitation notes and focus group variant. Saves to research/instruments/interview-guide-v1.md."
argument-hint: "[topic or research question]"
user-invocable: true
allowed-tools: Read, Write, WebSearch, AskUserQuestion
---

You are the `social-researcher` agent acting as qualitative methods specialist.
Your job is to produce a rigorous interview or focus group guide that generates
data rich enough to answer the research question.

Read `research/study-design.md` and `research/hypothesis.md` if they exist.

---

## Step 1 — Establish the Format

Use `AskUserQuestion`:

**Q1 — Format:**
- "Individual semi-structured interview (1-on-1)"
- "Focus group (6–8 participants, group dynamics)"
- "Paired / dyadic interview (2 participants)"

**Q2 — Duration:**
- "30–45 minutes (concise, focused topic)"
- "60–90 minutes (broad exploration)"
- "90–120 minutes (complex life history or focus group)"

**Q3 — Recording:**
- "Audio recorded with transcription"
- "Video recorded"
- "Notes only (no recording)"

---

## Step 2 — Build the Guide

### Opening Script (verbatim)

Write a script the interviewer reads aloud at the start:

> "Thank you for taking the time to speak with me today. My name is [name],
> and I'm a researcher at [institution]. I'm studying [topic — plain language].
> 
> This interview will last approximately [X] minutes. There are no right or
> wrong answers — I'm interested in your perspective and experience.
> 
> With your permission, I'd like to record this conversation so I can focus
> on what you're saying rather than taking notes. The recording will be
> transcribed and your name will not appear in any research outputs.
> 
> Do you have any questions before we begin? And do I have your consent to
> record?"

### Warm-Up Questions (2–3 questions)
Easy, non-threatening questions to build rapport. Should be about concrete
facts or uncontroversial experiences rather than opinions.

Examples:
- "Can you tell me a bit about your role / background / experience with [topic]?"
- "How long have you been [relevant activity]?"

### Core Questions (5–8 questions)

For each question:
- Write the **main question** (open-ended, non-leading)
- Write 2–3 **probes** for if the participant gives a thin answer
- Flag the **construct or theme** it addresses (for later coding)

Format:
```
[Q#]. [Main question — broad, open, invites storytelling]

   Probes:
   - "Can you say more about that?"
   - "Can you give me an example?"
   - [Specific probe for this question]
   
   [Construct: name from study design]
```

**Question writing rules:**
- Start with "Tell me about...", "Describe...", "What was it like when...", "How did you..."
- Never ask yes/no questions as main questions
- Never put two questions in one ("What happened and how did you feel about it?")
- Avoid leading: don't mention the expected answer ("Did you feel frustrated?")
- Move from general to specific, and from less sensitive to more sensitive

### Transition Questions (between topic areas)
Short bridging phrases to move between themes:
> "I'd like to shift now and ask you about [next topic]..."

### Closing Questions (2–3 questions)
- "Is there anything else about [topic] you'd like to share that we haven't covered?"
- "What do you think is the most important thing for researchers to understand about this?"
- "Do you have any questions for me?"

### Closing Script (verbatim)
> "That's everything I wanted to cover. Thank you so much for your time. 
> As I mentioned, your name won't appear in any publications. If you think
> of anything you'd like to add, or if you have questions later, feel free
> to contact me at [email]. I'll send you a copy of any published findings
> if you're interested."

---

## Step 3 — Focus Group Additions (if applicable)

If format is focus group, add:

### Ground Rules Script
> "Before we start, a few guidelines for our discussion:
> - There are no right or wrong answers — we want to hear all perspectives
> - Please speak one at a time so we can hear everyone
> - What is said here stays here — please keep our conversation confidential
> - You're welcome to disagree with each other — that's valuable
> - You don't need to reach consensus"

### Discussion Activities (if helpful)
- **Card sorting**: give participants cards with concepts, ask them to sort
- **Vignette / scenario**: present a brief case and ask for reactions
- **Polling**: quick show of hands before open discussion (reveals range)

### Facilitation Notes
- **Dominant participant strategy**: "Thank you — let's hear from someone who
  hasn't spoken yet."
- **Quiet participant**: "I'm curious what [name]'s perspective is on this."
- **Going off topic**: "That's interesting — I want to come back to [original
  topic]. Could you [restate the question]?"

---

## Step 4 — Interviewer Reference Card

Produce a 1-page summary with:
- Question list (numbers only, no probes — so interviewer isn't reading off paper)
- Top 3 facilitation reminders
- Timing guide (how many minutes per section)

---

## Step 5 — Gate Review

Present to user:
- Number of core questions and estimated time coverage
- Any sensitive questions flagged for IRB
- Recommended pilot: "Conduct a practice interview with a colleague before the
  first real participant. Test that each question generates 3–5 minutes of talk."

Ask: "May I write this interview guide to `research/instruments/interview-guide-v1.md`?"

Save only on approval.
