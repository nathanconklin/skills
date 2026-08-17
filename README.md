# skills

Nathan Conklin's collection of [Claude Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills) — reusable instruction sets that shape how Claude drafts documents, formats them, and (in one case) generates accessible/usable UI. Each subfolder is a single skill; see its own README for details.

| Folder | Summary |
|---|---|
| [`chat-to-whitepaper/`](chat-to-whitepaper/README.md) | Turns a voice-chat summary or transcript into a polished technical whitepaper `.docx`, by chaining the `nathan-speak` and `nathan-whitepaper` skills below into a draft → style → format pipeline. |
| [`hci-design/`](hci-design/README.md) | Six skills that encode HCI design principles — Nielsen's usability heuristics, WCAG 2.2 accessibility, Norman's affordances, per-user personalization, progressive disclosure, and direct manipulation — as hard constraints for AI-generated user interfaces, so generated dashboards/forms/charts are usable and accessible by construction. |
| [`nathan-speak/`](nathan-speak/README.md) | A prose style guide that makes Claude write like Nathan Conklin — clear, precise, register-appropriate, and free of common "AI writing" tells (throat-clearing, false binary contrasts, empty adverbs, etc.), with a scoring rubric to check drafts against. |
| [`nathan-whitepaper/`](nathan-whitepaper/README.md) | A self-contained skill (instructions + embedded Python script + VT logo) that converts a Markdown file into a Word `.docx` matching Nathan's standard Virginia Tech whitepaper template. |

## Use cases

These skills support a user interface design, user interface evaluation, and docuemnt-production workflows: the skills can be used to draft technical content from raw notes or conversation, style it consistently in a personal voice, and format it into a submission-ready Word document — plus the hci-design skills can be used for enforcing usability and accessibility standards or evaluating a user interface for HCI Design Principal conformance.
