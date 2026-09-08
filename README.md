# skills

Nathan Conklin's collection of [Claude Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills) supports document writing and formatting, public conversation exports, and accessible user interface design. Each folder contains a skill or related set of skills; follow the links below for its README or skill instructions.

| Folder | Summary |
|---|---|
| [`chat-to-whitepaper/`](chat-to-whitepaper/README.md) | Turns a voice-chat summary or transcript into a polished technical whitepaper `.docx`, by chaining the `nathan-speak` and `nathan-whitepaper` skills below into a draft → style → format pipeline. |
| [`graduate-seminar-writeup/`](graduate-seminar-writeup/SKILL.md) | Produces a full technical whitepaper and a shorter Graduate Seminar response from a presentation transcript or notes. The response includes a presentation summary, positive and critical evaluations, and relevance to Nathan's research; both documents use his writing style and Word formatting skills. |
| [`hci-design/`](hci-design/README.md) | Six skills that encode HCI design principles — Nielsen's usability heuristics, WCAG 2.2 accessibility, Norman's affordances, per-user personalization, progressive disclosure, and direct manipulation — as hard constraints for AI-generated user interfaces, so generated dashboards/forms/charts are usable and accessible by construction. |
| [`nathan-speak/`](nathan-speak/README.md) | A prose style guide that makes Claude write like Nathan Conklin — clear, precise, register-appropriate, and free of common "AI writing" tells (throat-clearing, false binary contrasts, empty adverbs, etc.), with a scoring rubric to check drafts against. |
| [`nathan-whitepaper/`](nathan-whitepaper/README.md) | A self-contained skill (instructions + embedded Python script + VT logo) that converts a Markdown file into a Word `.docx` matching Nathan's standard Virginia Tech whitepaper template. |
| [`shared-url-to-markdown/`](shared-url-to-markdown/SKILL.md) | Exports a public ChatGPT or Claude shared conversation to one Markdown file, preserving visible turns, formatting, and exposed artifact text, with a reported completeness status. |

## Use cases

Use these skills to preserve public shared conversations as Markdown, draft technical papers from notes or transcripts, and prepare Graduate Seminar summaries and critiques. The writing and formatting skills apply Nathan's prose style and standard Word template. The HCI design skills support interface creation and evaluation against usability and accessibility principles.
