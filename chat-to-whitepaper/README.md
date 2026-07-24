# chat-to-whitepaper

A [Claude Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills) that turns a voice-chat summary or conversation transcript into a polished technical whitepaper (`.docx`), formatted in Nathan Conklin's standard template.

## What it does

This is not a standalone application; it is an instruction set (`chat-to-whitepaper.skill.md`) that Claude follows when invoked. It chains two other skills in this repo into a three-stage pipeline:

1. **Draft** — Reads the raw chat summary/transcript and writes a technical paper in Markdown. Voice chats are messy: ideas get revised mid-conversation, terminology drifts, and transcription garbles technical terms. The skill's instructions tell Claude how to normalize terminology, resolve revisions in favor of the latest position, infer a sensible document structure (motivation/design/usage for a proposed system, claim/support/counterarguments for a position paper, etc.), and flag unresolved gaps inline with `[TODO]` markers rather than guessing or fabricating content.
2. **Style** — Applies the [`nathan-speak`](../nathan-speak/README.md) skill to edit the prose into Nathan's voice, scoring the draft against a rubric before proceeding.
3. **Format** — Applies the [`nathan-whitepaper`](../nathan-whitepaper/README.md) skill to convert the styled Markdown into a `.docx` using Nathan's Virginia Tech whitepaper template, including verification steps (PDF render check, page-numbering check, visual spot-check).

The skill delivers both the final `.docx` and the Markdown source (so the paper can be edited and regenerated later), along with a short report listing the paper's one-sentence contribution and any outstanding `[TODO]` markers.

## Use cases

- Converting a recorded brainstorming or ideation session into a shareable technical document.
- Turning informal research discussion notes into a first-draft whitepaper or position paper.
- Producing consistently formatted, submission-ready documents (VT academic format or SEACORP/DoD format) from unstructured conversational input, without manually re-typing or reformatting.
