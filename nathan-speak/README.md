# nathan-speak

A [Claude Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills) (`nathan-speak.skill.md`) that makes Claude write and edit prose in Nathan Conklin's personal style — clear, professional, technically precise, and stripped of patterns that read as obviously AI-generated.

## What it does

The skill is a detailed style guide encoded as instructions rather than code. It defines:

- **Core philosophy**: clear before clever, professional but not artificial, technically accurate, big-picture-first organization.
- **Sentence mechanics**: short/medium sentences, semicolons over "and", no em dashes, active voice by default, cutting empty adverbs.
- **Document registers**: different tone/vocabulary rules for government proposals, scientific/technical papers, formal letters/legal documents, and internal emails (e.g., DoD terms of art like CMMC/CUI are fine in proposals; hedges like "suggests"/"may" are legitimate in papers, not filler).
- **An extensive catalog of "AI writing tells" to strip out**: binary-contrast reveals ("Not because X. Because Y."), negative listing, dramatic fragmentation, rhetorical setups ("What if..."), false agency (inanimate things doing human verbs), passive voice outside its narrow exceptions, throat-clearing openers, business jargon, empty adverbs, meta-commentary, and vague declaratives — each with a table of the pattern, why it's a problem, and the fix.
- **A scoring rubric** (six dimensions, out of 60) for grading a draft and a threshold (42/60) below which it should be revised before delivery.
- **Before/after examples** across registers (technical paper, government proposal, internal email, etc.) showing the edits applied.

## Use cases

- Drafting or editing emails, proposals, papers, letters, or blog posts so they consistently sound like Nathan rather than a generic AI assistant.
- Running a "de-AI" pass on text Nathan didn't write himself, on request ("clean this up," "make this sound like me").
- Acting as the styling stage inside other pipelines in this repo, notably [`chat-to-whitepaper`](../chat-to-whitepaper/README.md), which applies this skill to a drafted paper before formatting it as a `.docx`.
