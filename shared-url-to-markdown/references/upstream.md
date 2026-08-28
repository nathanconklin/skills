# Upstream reference

This skill was informed by `DHRVIR/LLM_Chat_Exporter` at commit
`b5d5b1cd9fa7ab6dac27fd8c0900edea76f5c5de` (2026-07-27):

<https://github.com/DHRVIR/LLM_Chat_Exporter>

The upstream README labels the project MIT, but the inspected commit does not
contain a standalone license file or copyright notice. This package therefore
uses a fresh implementation and retains this attribution rather than copying
the upstream Python files.

The upstream project established the useful idea of collecting mounted message
nodes while moving through ChatGPT's virtualized scroll container. This skill
changes the design substantially:

- ChatGPT and Claude provider adapters share one normalized model.
- Structured snapshot data is preferred over DOM scraping.
- Browser fallback traverses from top to bottom so discovery order remains
  chronological.
- URL validation uses exact hosts and share paths.
- Public, ephemeral browser contexts replace persistent or authenticated ones.
- Completeness state and warnings are part of the Markdown output.
- Tests cover normalization, ordering, deduplication, rendering, and safety.
