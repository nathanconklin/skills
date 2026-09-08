---
name: graduate-seminar-writeup
description: >
  Prepare Nathan Conklin's Graduate Seminar documentation from a seminar,
  research presentation, guest lecture, colloquium, or similar academic talk.
  Use this skill when Nathan provides an attached transcript, pasted transcript,
  presentation notes, or sufficient current chat context and asks to prepare
  his Graduate Seminar writeup. The skill produces two documents from the same
  source material: (1) a full whitepaper using the existing chat-to-whitepaper
  skill and (2) a shorter Graduate Seminar writeup containing a presentation
  summary, positive critique, negative critique, and discussion of how the
  research could advance Nathan's own research. The shorter document must use
  nathan-speak for prose and nathan-whitepaper for document formatting.
metadata:
  author: Nathan Conklin
  depends_on: chat-to-whitepaper, nathan-speak, nathan-whitepaper
---

# Graduate Seminar Writeup

Turn a Graduate Seminar presentation, lecture, or research talk into two
separate polished documents.

The two outputs serve different purposes:

1. **Full Whitepaper** — a complete technical whitepaper created using the
   existing `chat-to-whitepaper` skill exactly as that skill normally operates.
2. **Graduate Seminar Writeup** — a much tighter academic response containing
   four required sections:
   - Section 1: Presentation Summary
   - Section 2a: Positive Evaluation and Critique
   - Section 2b: Critical Evaluation and Critique
   - Section 2c: Relevance to Nathan's Research

Do not merge these documents. Produce both.

## Dependencies

This skill depends on three existing Nathan Conklin skills:

- `chat-to-whitepaper`
- `nathan-speak`
- `nathan-whitepaper`

Locate and read the installed versions of these skills before beginning.

Do not reproduce or approximate their behavior when the installed skills are
available. Delegate work to them so changes to those skills automatically carry
forward into this workflow.

If one of the required skills cannot be found, identify which dependency is
missing rather than silently replacing Nathan's established writing or document
format.

---

# Stage 1: Identify and Read the Source Material

The source material may be provided in several ways:

- an attached transcript;
- an attached Markdown or text document;
- pasted transcript text;
- presentation notes;
- a conversation in the current chat containing a transcript or detailed
  discussion of the presentation.

Use the richest available source.

If a transcript is attached, read the entire transcript before drafting either
document.

If the current conversation contains the presentation discussion or transcript
and no attachment is supplied, use the relevant conversation context as the
source.

Do not require Nathan to export a transcript merely because the presentation
was discussed in the current conversation.

## Normalize the Transcript

Presentation transcripts frequently contain:

- transcription errors;
- repeated statements;
- verbal fillers;
- unfinished sentences;
- audience questions;
- corrections made later in the presentation;
- incorrectly transcribed technical terminology.

Interpret the transcript as a record of the presentation rather than polished
prose.

Silently correct obvious transcription errors when the intended meaning is
clear.

If an important technical term, claim, speaker identity, research result, or
other detail cannot be determined reliably, do not invent it. Use an inline
marker such as:

**[TODO: verify name of algorithm from transcript]**

Later statements from the presenter supersede earlier statements when the
presenter clearly corrects or revises a point.

## Extract Presentation Metadata

When possible, identify:

- presentation title;
- presenter or presenters;
- presenter affiliation;
- presentation date;
- central research problem;
- primary contribution;
- research methodology;
- important findings or results;
- limitations discussed by the presenter;
- future-work directions.

Do not invent missing metadata.

The document title should normally be derived from the actual presentation
title. If appropriate, the shorter document may use a title such as:

`Graduate Seminar Response: <Presentation Title>`

---

# Stage 2: Produce the Full Whitepaper

Invoke and follow the existing `chat-to-whitepaper` skill using the seminar
source material.

Treat this stage exactly like Nathan's normal chat-to-whitepaper workflow.

The purpose of this document is to preserve the presentation in a more complete
technical form. It may therefore include background, explanation, technical
details, methodology, findings, implications, and other material warranted by
the source.

Do not shorten the normal whitepaper merely because a second, shorter document
will also be produced.

Allow `chat-to-whitepaper` to perform its normal sequence:

1. draft the technical paper;
2. apply `nathan-speak`;
3. apply `nathan-whitepaper`;
4. verify the generated document;
5. preserve the Markdown source;
6. produce the formatted Word document.

The first document should therefore look and behave exactly like any other
whitepaper produced by Nathan's normal whitepaper workflow.

Suggested filenames:

`<presentation-slug>-whitepaper.md`

`<presentation-slug>-whitepaper.docx`

---

# Stage 3: Draft the Graduate Seminar Writeup

After completing the full whitepaper, create a separate Markdown source for the
shorter Graduate Seminar response.

The seminar response should be substantially tighter than the whitepaper.

It should demonstrate that Nathan:

- understood the research;
- considered its strengths;
- critically examined its weaknesses;
- connected the presentation to his own research.

The shorter document is analytical rather than merely descriptive.

The transcript remains the authoritative primary source. The completed
whitepaper may be used as a normalized representation of the presentation, but
do not allow elaboration introduced for the whitepaper to become an unsupported
claim in the seminar writeup.

## Document Header

Use the metadata structure expected by `nathan-whitepaper`.

Begin with an H1 document title followed by Nathan's standard academic contact
information.

Default academic author information:

Nathan Conklin  
nathan.conklin@vt.edu  
Department of Computer Science  
Virginia Tech

Retain Nathan's normal title, author, email, department, institution, header,
footer, and paragraph formatting.

**Do not include an Abstract.**

**Do not include a separate Introduction.**

After the title and author/contact information, immediately begin Section 1.

---

# Required Content

The document contains exactly four substantive sections.

## 1. Presentation Summary

Write one tight paragraph of approximately **300–350 words**.

This section should summarize the presentation as a coherent piece of research,
not as a chronological transcript.

The paragraph should identify, when supported by the source:

- the problem being investigated;
- why the problem matters;
- the research question or objective;
- the proposed method, system, experiment, or theoretical approach;
- the important findings;
- the contribution of the work;
- the broader implication of the research.

Prioritize the central research contribution over presentation logistics.

Do not write:

"The speaker first discussed..."

"Next, the presenter talked about..."

"Finally, the presentation covered..."

Instead, synthesize the presentation into a concise technical summary.

The paragraph should stand on its own for a reader who did not attend the talk.

Target length: **300–350 words.**

Use one paragraph unless paragraph separation is required for readability.

---

## 2a. Positive Evaluation and Critique

Evaluate the research from a predominantly **positive perspective**.

This is still a critique, not praise for its own sake.

Identify aspects of the research that were particularly effective, convincing,
useful, rigorous, novel, or important.

Potential considerations include:

- significance of the research problem;
- novelty of the research question;
- appropriateness of the methodology;
- experimental design;
- technical contribution;
- quality of the evidence;
- applicability of the results;
- clarity of the research argument;
- implications for the field.

Focus on the strongest one or two points rather than producing a generic list
of compliments.

Explain **why** those elements strengthen the research.

Where appropriate, acknowledge a limitation while explaining why the overall
research decision remains defensible.

Keep the tone professional, evidence-oriented, and constructive.

This section should normally be about **175–250 words**.

---

## 2b. Critical Evaluation and Critique

Provide an alternative evaluation from a predominantly **negative or skeptical
perspective**.

Do not manufacture flaws merely to make the section negative.

Identify the strongest legitimate concern supported by the presentation,
methodology, evidence, assumptions, or scope of the research.

Potential concerns include:

- limited sample size;
- questionable assumptions;
- evaluation methodology;
- missing comparison conditions;
- external validity;
- generalizability;
- insufficient evidence for a claim;
- unclear causal reasoning;
- scalability;
- usability;
- reproducibility;
- applicability outside the tested environment;
- unaddressed confounding variables;
- unanswered questions raised by the results.

The critique should distinguish between:

1. a limitation actually acknowledged by the researchers;
2. a limitation Nathan infers from the presented work.

Do not state an inferred limitation as though the presenter admitted it.

Explain why the concern matters and, when useful, what additional evidence,
experiment, analysis, or design change could address it.

The goal is thoughtful academic skepticism, not hostility.

This section should normally be about **175–250 words**.

---

## 2c. Relevance to My Research

Explain how the presented research could help advance Nathan's own research.

This section should move beyond statements such as:

"This is relevant to my research."

Identify a concrete intellectual, methodological, experimental, architectural,
or design connection.

Use the most current information available in the conversation about Nathan's
research.

Relevant connections may include, when appropriate:

- human-computer interaction;
- information visualization;
- human-AI collaboration;
- interactive AI systems;
- visualization of AI reasoning;
- reasoning and decision structures;
- human intervention in AI reasoning;
- uncertainty and confidence visualization;
- collaborative sensemaking;
- evaluation of agentic AI systems;
- experimental methodology for studying interactions between humans and AI.

These are starting points, not mandatory topics. Prefer the most direct
connection supported by Nathan's current research context.

Discuss specifically how an idea from the presentation might influence:

- a research question;
- prototype design;
- visualization technique;
- evaluation methodology;
- experiment;
- metric;
- system architecture;
- theoretical framing;
- future paper.

Whenever possible, propose at least one **actionable research implication**.

Examples include adapting an experimental method, adding a comparison
condition, borrowing an evaluation metric, testing a visualization technique,
or using the presented findings to motivate a new research hypothesis.

Do not imply that Nathan has already performed an experiment, implemented a
feature, or reached a result unless that information is actually available.

This section should normally be about **175–250 words**.

---

# Stage 4: Apply Nathan's Writing Style

Read and apply the installed `nathan-speak` skill to the entire Graduate Seminar
writeup.

Use the **scientific and technical papers** register.

The prose should sound like Nathan rather than generic AI-generated academic
writing.

In particular:

- lead with the point;
- favor clear, direct sentences;
- maintain technical precision;
- use active voice where appropriate;
- keep terminology consistent;
- remove unnecessary intensifiers;
- avoid manufactured drama;
- avoid empty praise;
- avoid formulaic AI transitions;
- avoid em dashes;
- use calibrated scientific language when evidence is incomplete.

Apply the complete editing and quality-check process required by
`nathan-speak`.

Do not remove `[TODO: ...]` markers merely to make the document appear
finished.

---

# Stage 5: Format the Graduate Seminar Writeup

Use the installed `nathan-whitepaper` skill to convert the Graduate Seminar
Markdown into Word format.

Do not manually approximate its layout.

The seminar writeup must therefore inherit Nathan's normal document formatting,
including:

- Virginia Tech logo header;
- title and contact block;
- running title and author information;
- standard margins;
- standard heading styles;
- Times New Roman body typography;
- standard paragraph spacing;
- live `Page X of Y` footer;
- all other formatting controlled by `nathan-whitepaper`.

Although the visual formatting comes from `nathan-whitepaper`, the content
structure intentionally differs from an ordinary whitepaper.

### Important exception

**There is no Abstract.**

The first body heading after Nathan's title/contact information must be:

`1. Presentation Summary`

Follow it with:

`2a. Positive Evaluation and Critique`

`2b. Critical Evaluation and Critique`

`2c. Relevance to My Research`

Do not insert an Abstract or Introduction between the contact block and
Section 1.

Use a short running header title derived from the presentation title when
necessary.

Follow all verification requirements in `nathan-whitepaper`, including header,
footer, pagination, and visual inspection.

Suggested filenames:

`<presentation-slug>-graduate-seminar.md`

`<presentation-slug>-graduate-seminar.docx`

---

# Stage 6: Quality Review

Before delivering the seminar response, verify the following.

## Source fidelity

- The summary accurately reflects the presentation.
- No research results were invented.
- No speaker quotations were invented.
- Technical terminology is consistent.
- Uncertain facts are marked rather than guessed.

## Section 1

- Contains approximately 300–350 words.
- Functions as a synthesis rather than a chronological recap.
- Clearly communicates the research problem and contribution.
- Is approximately one paragraph.

## Section 2a

- Provides a genuinely positive evaluation.
- Explains why the identified strengths matter.
- Does more than praise the presentation.

## Section 2b

- Provides a genuinely skeptical alternative evaluation.
- Criticism is grounded in the research rather than manufactured.
- Distinguishes presented limitations from Nathan's inferred criticisms.
- Suggests an improvement or additional evidence where appropriate.

## Section 2c

- Makes a substantive connection to Nathan's own research.
- Identifies at least one concrete way the presented research could influence
  his work.
- Does not fabricate progress or results in Nathan's research.

## Style

- `nathan-speak` has been applied.
- The writing is concise and technically precise.
- No generic AI filler remains.
- No em dashes remain.

## Formatting

- `nathan-whitepaper` has been used.
- Nathan's academic contact information appears correctly.
- There is no Abstract.
- There is no unnecessary Introduction.
- Section 1 begins immediately after the title/contact material.
- Headers render correctly.
- Footers display `Page X of Y` correctly.
- Page 1 and at least one later page have been visually inspected.

---

# Stage 7: Deliver All Artifacts

Deliver both document sets.

### Full Whitepaper

1. `<presentation-slug>-whitepaper.docx`
2. `<presentation-slug>-whitepaper.md`

### Graduate Seminar Writeup

3. `<presentation-slug>-graduate-seminar.docx`
4. `<presentation-slug>-graduate-seminar.md`

Present the two Word documents prominently, with the full whitepaper first and
the Graduate Seminar writeup second.

Also provide the Markdown sources because Nathan may want to edit and
regenerate either document.

In the chat response, provide only a short completion summary containing:

- presentation title;
- presenter, if known;
- full whitepaper word count;
- Graduate Seminar writeup word count;
- Section 1 word count;
- any `[TODO: ...]` items that require Nathan's attention.

Do not reproduce the documents themselves in the chat unless Nathan explicitly
asks for their text.

---

# Operating Principle

The two outputs should complement each other.

The **whitepaper** captures and expands the intellectual content of the seminar
in Nathan's normal technical-paper format.

The **Graduate Seminar writeup** demonstrates concise comprehension, critical
evaluation from two perspectives, and thoughtful integration of the seminar
with Nathan's own research.

Both documents originate from the same presentation, but they should not read
like different-length versions of the same paper.
