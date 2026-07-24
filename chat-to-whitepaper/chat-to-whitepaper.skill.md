---
name: chat-to-whitepaper
description: Transform a voice chat summary or conversation transcript into a formatted technical whitepaper (.docx) in Nathan's standard format. Use this skill whenever Nathan attaches a chat summary, voice conversation recap, brainstorm transcript, or discussion notes and wants them turned into a paper, whitepaper, technical document, or "written up" -- even if he doesn't say "whitepaper" explicitly. Phrases like "turn this chat into a paper," "write up our conversation," "make a whitepaper from this discussion," or "convert this voice chat" should all trigger it. This skill chains two other skills, nathan-speak (prose style) and nathan-whitepaper (docx formatting); read and apply both as part of the workflow below.
metadata:
  author: Nathan Conklin
  depends_on: nathan-speak, nathan-whitepaper
---

# chat-to-whitepaper

Turn a voice chat summary into a polished technical whitepaper through a
three-stage pipeline:

1. **Draft**: read the chat summary and write a technical paper in Markdown.
2. **Style**: apply the `nathan-speak` skill to the prose.
3. **Format**: apply the `nathan-whitepaper` skill to produce the .docx.

The dependent skills live in the user skills directory (normally
`/mnt/skills/user/nathan-speak/SKILL.md` and
`/mnt/skills/user/nathan-whitepaper/SKILL.md`). If either is missing, stop and
tell Nathan rather than improvising a substitute; the whole point of this
pipeline is his specific style and template.

## Stage 1: Draft the paper

**Locate the input.** The chat summary is usually an attachment in
`/mnt/user-data/uploads` (or pasted into the conversation). Read all of it
before writing anything.

**Understand the material.** A voice chat is ideation, not exposition. Expect
meandering, restated ideas, informal terminology, and positions that get
revised mid-conversation. Interpret accordingly:

- When the chat revises an idea, the later position supersedes the earlier one.
  Do not present abandoned versions as part of the argument (unless the
  evolution itself is the point, e.g., a design-rationale paper).
- Normalize terminology. If the chat calls the same concept three different
  things, pick the most precise term and use it consistently.
- Voice transcription garbles technical terms. If a term looks like a
  mis-transcription of something Nathan plausibly said (e.g., "sea out T" for
  "CoT"), silently correct it; if you cannot tell what was meant, flag it with
  a [TODO] marker rather than guessing.

**Identify the contribution.** Before outlining, state to yourself in one
sentence what this paper claims or contributes. Everything in the paper should
serve that sentence. If the chat contains two genuinely separate contributions,
tell Nathan and ask whether he wants one paper or two before proceeding.

**Infer the structure from the content.** Do not force a fixed template. Every
paper gets a title, an author block, and an opening section (usually an
Abstract, or an Introduction for shorter pieces) that states the contribution
up front; the rest of the structure should follow the shape of the material.
Typical shapes, for calibration rather than prescription:

- A proposed system or tool: motivation, design/architecture, usage scenario,
  discussion.
- A position or argument: the claim, supporting threads as sections,
  counterarguments, implications.
- A methodology or process: problem context, the method, a worked example,
  limitations.

**Elaborate freely, but honestly.** Nathan wants the paper fleshed out with
background knowledge, not a transcript. Add context, definitions, related
concepts, and connective reasoning that a reader needs; sharpen half-formed
arguments from the chat into complete ones. The chat's ideas stay central; the
elaboration serves them. Two hard limits:

- Never fabricate results, data, quotations, or citations. Cite only works you
  are confident exist and say what you claim; otherwise write
  `[TODO: cite support for X]`.
- Never elaborate the paper into claiming things the chat argued against.

**Flag gaps inline.** Where the chat leaves a hole -- missing evidence, an
unresolved design decision, a claim that needs a source, an unintelligible
passage -- insert a bold inline marker in the text where the fix belongs:

    **[TODO: quantify the alert-volume claim; chat gave no numbers]**

Markers must survive into the .docx so Nathan sees them while reviewing.

**Write the Markdown** to `/home/claude/<short-slug>.md` in the format
`nathan-whitepaper` expects: first line is the `# H1` title, followed by italic
metadata lines (author, affiliation). Default author is Nathan Conklin. Infer
the affiliation from the topic: academic work (visualization, HCI, research)
gets `nathan.conklin@vt.edu` / Department of Computer Science / Virginia Tech;
work documents (DoD, proposals, submarine systems) get SEACORP. Ask if the
topic straddles both.

## Stage 2: Apply nathan-speak

Read `/mnt/skills/user/nathan-speak/SKILL.md` and edit the draft against it,
using the **scientific and technical papers register**. Do the full editing
pass and the quick checks; then score the draft on the six dimensions and
revise until it clears 42/60. Edit the .md file in place so the styled text is
what gets converted.

Do not "fix" the [TODO] markers during this pass; they are for Nathan, not for
polishing away.

## Stage 3: Apply nathan-whitepaper

Read `/mnt/skills/user/nathan-whitepaper/SKILL.md` and follow its workflow
exactly: extract the embedded converter, write a `config.json` (craft a short
`header_title`; fill in author defaults), run the conversion, and perform its
verification steps (PDF render, footer numbering check, visual check of page 1
and a later page).

## Deliver

Copy **both** the .docx and the .md source to `/mnt/user-data/outputs` and
present them, .docx first. The .md matters because Nathan edits the source and
regenerates the .docx from it.

In the chat, give a short report: the paper's one-sentence contribution, the
inferred structure, and a list of every [TODO] marker with its location. Keep
the report brief; the document speaks for itself.
