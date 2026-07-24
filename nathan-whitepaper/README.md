# nathan-whitepaper

A self-contained [Claude Agent Skill](https://docs.claude.com/en/docs/agents-and-tools/agent-skills) (`nathan-whitepaper.skill.md`) that converts a Markdown document into a Word `.docx` whitepaper matching Nathan Conklin's standard academic/technical template.

## What it does

The entire skill — instructions, template, and converter — lives in this one file. Embedded inside it is a complete Python script (with a base64-encoded Virginia Tech logo image baked in) that Claude extracts and runs to perform the conversion; there are no other files to fetch or install.

The workflow:

1. Extract the embedded Python converter to disk verbatim.
2. Locate the source `.md` file and skim it for a title and author metadata.
3. Write a small `config.json` filling in anything the Markdown doesn't specify (title, subtitle, header title, author block).
4. Run the converter: `python3 nathan_whitepaper.py input.md output.docx --config config.json`.
5. Verify the result — render to PDF, check the "Page X of Y" footer sequencing, and visually spot-check the header/logo placement on page 1 vs. later pages.
6. Deliver the `.docx`.

The generated template produces: US Letter pages with the VT logo on page 1 only (logo + running title/author on subsequent pages), live auto-updating "Page X of Y" footers (via real Word `PAGE`/`NUMPAGES` fields, not a static count), Times New Roman body text, styled headings, syntax-highlighted code blocks (via Pygments, with a plain-text fallback), formatted tables, lists, and auto-numbered figure captions for images.

## Use cases

- Converting a Markdown draft, report, or paper into a submission-ready Word document without manually reapplying formatting each time.
- Regenerating an updated `.docx` after editing the Markdown source, keeping formatting, pagination, and headers consistent.
- Serving as the final formatting stage in the [`chat-to-whitepaper`](../chat-to-whitepaper/README.md) pipeline, which drafts and styles the Markdown before handing it to this skill for conversion.
