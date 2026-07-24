---
name: accessibility-wcag
description: >
  Encodes Web Content Accessibility Guidelines (WCAG) 2.2 success criteria as
  hard constraints on on-demand user interface generation. Load this skill
  whenever generating, modifying, extending, or regenerating ANY user interface
  artifact within the Space to Think — every dashboard, form, table, chart,
  alert builder, configuration panel, or interactive component, without
  exception. Unlike advisory skills, this skill's constraints are invariants:
  a component that fails a Level A or AA check is rejected before it reaches
  the user, not shipped with a warning. Also load when the user asks about the
  accessibility of a generated interface, when auditing an existing generated
  UI for conformance, when another skill (heuristics-nielsen,
  ability-based-personalization) requests an accessibility pass, or when
  emitting any component that renders color, text, images, focusable controls,
  forms, motion, media, or dynamic status updates — which is to say, always.
metadata:
  version: 0.1.0
  conformance-target: WCAG 2.2 Level AA (hard invariant); AAA criteria advisory
  source: >
    World Wide Web Consortium. Web Content Accessibility Guidelines (WCAG) 2.2.
    W3C Recommendation, 12 December 2024. https://www.w3.org/TR/WCAG22/
    Supporting documents: Understanding WCAG 2.2
    (https://www.w3.org/WAI/WCAG22/Understanding/) and Techniques for WCAG 2.2
    (https://www.w3.org/WAI/WCAG22/Techniques/).
  framework: >
    Nathan Conklin, Miranda Capra, and Chris North. 2026. Automating the
    Application of HCI Principles: Skills for On-Demand UI Construction, the
    Human-AI Space to Think, and the Future of HCI. In Proceedings of The
    Future of HCI Workshop (FutureHCI ’26). ACM, New York, NY, USA, 6 pages.
  relationship-to-other-skills: >
    Composes with heuristics-nielsen.skill.md (usability constraints; its H9
    error recovery pairs with SC 3.3.1/3.3.3 here, its H4 consistency pairs
    with SC 3.2.3/3.2.4), affordances-norman.skill.md (signifiers; SC 1.4.11
    non-text contrast makes signifiers perceivable), direct-manipulation
    .skill.md (SC 2.5.7 requires single-pointer alternatives to its dragging
    interactions), and mixed-initiative.skill.md (SC 4.1.3 governs how agentic
    status is announced). ability-based-personalization.skill.md builds ON TOP
    of this skill: AA conformance is the universal floor this skill enforces
    for every user; personalization raises individual dimensions above the
    floor (never below it). Where constraints conflict, the stricter wins.
---

# WCAG 2.2 Success Criteria as Generator Invariants

## Purpose

Accessibility has historically been a release-time audit: an expert reviews a
finished product, files violations, and remediation competes with the roadmap.
This skill inverts that. Because every interface here is generated as
structured component code rather than hand-assembled pixels, WCAG success
criteria can be enforced at the point of emission. A component that cannot pass
is redesigned before the user ever sees it. Conformance becomes a property of
the generation process — every user receives an accessible interface by
default, across arbitrary domains, at zero marginal design cost.

The on-demand paradigm also creates obligations a static site never had: the
interface regenerates, so conformance must be re-verified on every generation;
content updates live, so status changes must be programmatically announced; and
each interface is generated for one user, so the AA floor established here is
the base that ability-based personalization raises, never lowers.

WCAG 2.2 is organized under four principles — Perceivable, Operable,
Understandable, Robust (POUR) — with testable success criteria at Levels A
(minimum), AA (target), and AAA (enhanced). This skill enforces all applicable
Level A and AA criteria as hard constraints and applies AAA criteria as
advisory defaults where they cost nothing. Note: SC 4.1.1 Parsing was removed
in WCAG 2.2 and is not checked.

## How to apply this skill

1. **Before generating**: identify which criteria the planned components
   activate. Text → contrast, spacing, resize. Controls → keyboard, focus,
   name/role/value, target size. Forms → labels, errors, redundant entry.
   Charts/images → text alternatives, use of color. Live data → status
   messages, pause/stop/hide. Media → captions/descriptions.
2. **During generation**: emit only from the accessible component library
   (semantic HTML first; ARIA only where semantics are insufficient). Satisfy
   every applicable constraint below in the emitted code itself — accessible
   names, roles, states, and relationships are part of the component, not a
   post-processing layer.
3. **After generating**: run the two-stage verification (bottom of this file):
   automated checks for the machine-decidable criteria, then an AI critic pass
   for the judgment criteria (alt-text quality, label meaningfulness, reading
   order sense). Any Level A/AA failure blocks instantiation.
4. **On regeneration**: re-verify the full surface, not just the diff — layout
   changes can silently break focus order, contrast against new adjacencies,
   and reflow.
5. **On user query**: when asked why a component is built a certain way, cite
   the specific success criterion (e.g., "SC 2.5.8 Target Size (Minimum)")
   and, per heuristics-nielsen H10, the dialogue turn that justified the
   component itself.

---

## Principle 1 — Perceivable

Information and UI components must be presentable to users in ways they can
perceive.

### 1.1 Text alternatives (SC 1.1.1, Level A)

**Generate:**
- Every non-text element carries a text alternative serving an equivalent
  purpose: informative images and icons get descriptive alt text; icon-only
  controls get an accessible name describing the action ("Edit alert", not
  "pencil"); charts and visualizations get both a concise alt summary and a
  structured equivalent (data table or accessible description) conveying the
  same information — for a generated chart, derive both from the same task
  model data that produced the chart.
- Purely decorative graphics are marked so assistive technology ignores them
  (empty alt, `aria-hidden="true"` — never a filename or "image").

**Reject before emitting:** any `<img>` without an alt attribute; any icon-only
control without an accessible name; any chart whose information exists only in
pixels.

### 1.3 Adaptable structure (SC 1.3.1, 1.3.2, 1.3.3 A; 1.3.4, 1.3.5 AA)

**Generate:**
- Structure and relationships are programmatically determinable (1.3.1): real
  `<table>` with `<th scope>` for data tables (the ETF watchlist is a table,
  not styled divs); `<label for>` or equivalent for every input; heading
  elements in a logical hierarchy that mirrors the task model's goal
  structure; lists as list markup; grouped controls in `<fieldset>`/`<legend>`
  or `role="group"` with an accessible name.
- DOM order matches meaningful reading order (1.3.2) — the visual layout the
  generator plans and the source order it emits tell the same story.
- Instructions never rely solely on shape, color, size, or position (1.3.3):
  "Select Edit Alert", not "click the button on the right" or "the red one".
- No orientation lock (1.3.4) unless essential.
- Inputs collecting user data declare their purpose via `autocomplete` tokens
  (1.3.5) so user agents can assist.

**Reject before emitting:** div-soup tables; visually implied but
programmatically absent relationships; positional or color-only instructions.

### 1.4 Distinguishable (SC 1.4.1, 1.4.2 A; 1.4.3–1.4.5, 1.4.10–1.4.13 AA)

**Generate:**
- Color is never the only channel (1.4.1): gains/losses pair color with sign
  and/or icon (▲ +2.31% / ▼ −1.28%); chart series differ by more than hue
  (markers, dash patterns, direct labels); required fields and errors are
  marked by text/icon, not red alone; links in prose are distinguishable
  without color alone.
- Text contrast ≥ 4.5:1; large-scale text (≥ 18 pt, or ≥ 14 pt bold) ≥ 3:1
  (1.4.3). Compute contrast from the component library's actual token values
  against the actual rendered background, including states (hover, disabled
  conveys-no-information exception noted, placeholder text is NOT exempt).
- Non-text contrast ≥ 3:1 (1.4.11) for UI component boundaries, states (focus,
  selected, toggle on/off), and meaningful graphics (chart lines, axes,
  slider tracks) against adjacent colors.
- Text resizes to 200% without loss (1.4.4); no images of text where real text
  can achieve the presentation (1.4.5) — generated charts render labels as
  text/SVG text, not rasterized.
- Reflow (1.4.10): content remains usable at 320 CSS px width without
  two-dimensional scrolling; generated dashboards linearize their panels;
  exceptions only for genuinely two-dimensional content (data tables, charts,
  maps) — and those scroll within their own region.
- Text spacing tolerance (1.4.12): no content or functionality lost when the
  user overrides line height to 1.5×, paragraph spacing to 2×, letter spacing
  to 0.12×, word spacing to 0.16× font size — no fixed-height text containers
  that clip.
- Content on hover/focus (1.4.13): generated tooltips are dismissible
  (Esc), hoverable (pointer can move onto them), and persistent until
  dismissed or invalid.
- Autoplaying audio beyond 3 seconds has pause/stop or independent volume
  (1.4.2); prefer never autoplaying.

**Reject before emitting:** any token pair failing its contrast ratio; any
information encoded in hue alone; fixed layouts that break at 320 px or clip
under spacing overrides; hover content that vanishes when approached.

### 1.2 Time-based media (SC 1.2.1–1.2.3 A; 1.2.4–1.2.5 AA)

Generated interfaces rarely emit media, but when the task model includes it:
prerecorded audio gets transcripts, prerecorded video gets captions and audio
description, live audio gets captions (AA). If conformant media cannot be
produced, surface the gap to the user rather than embedding inaccessible media
silently.

---

## Principle 2 — Operable

UI components and navigation must be operable.

### 2.1 Keyboard accessible (SC 2.1.1, 2.1.2, 2.1.4, Level A)

**Generate:**
- Every function is operable through a keyboard interface (2.1.1): all
  controls focusable and activatable (Enter/Space); composite widgets (menus,
  tab lists, grids, comboboxes) implement the ARIA Authoring Practices
  keyboard patterns; custom interactions (chart brushing, reordering) have
  keyboard equivalents.
- No keyboard traps (2.1.2): modals hold focus while open but always release
  on Esc/close; focus returns to the triggering control on dismissal.
- Single-character shortcuts, if generated, can be turned off, remapped, or
  are active only on focus (2.1.4).

**Reject before emitting:** click-only handlers on non-interactive elements;
positive `tabindex`; any widget without its expected keyboard pattern; modals
without a keyboard exit.

### 2.4 Navigable (SC 2.4.1–2.4.4 A; 2.4.5–2.4.7, 2.4.11 AA)

**Generate:**
- Bypass mechanism for repeated blocks (2.4.1): skip link and/or landmark
  regions (`main`, `nav`, complementary) so assistive tech users jump straight
  to the generated workspace content.
- The page/workspace has a title describing its purpose (2.4.2) — derive it
  from the task model ("ETF Watchlist & Alerts"), and update it on
  regeneration.
- Focus order preserves meaning and operability (2.4.3): tab sequence follows
  the task's logical flow; newly generated components enter the sequence where
  they belong, not appended arbitrarily; when the UI regenerates while the
  user is working, focus is preserved or moved intentionally — never dropped
  to body.
- Link purpose clear from text or programmatic context (2.4.4): "View in
  conversation" links carry accessible names identifying what will be viewed;
  no bare "click here".
- Headings and labels describe topic or purpose (2.4.6), in the user's own
  vocabulary (composes with heuristics-nielsen H2).
- Focus visible (2.4.7): every focusable component shows a visible indicator;
  never remove outlines without an equal-or-better replacement meeting 1.4.11
  contrast.
- Focus not obscured (2.4.11, new in 2.2): sticky headers, toolbars, banners,
  and non-modal panels the generator emits must not entirely hide the focused
  element — verify against the planned layout's sticky regions.
- Multiple ways to locate views (2.4.5) where the workspace has several: the
  dialogue itself is one way; provide at least a navigation/overview affordance
  as the second.

**Reject before emitting:** focus order contradicting visual/logical order;
suppressed focus indicators; layouts where sticky chrome can fully cover a
focused control; undescriptive titles, headings, or link text.

### 2.5 Input modalities (SC 2.5.1–2.5.4 A; 2.5.7, 2.5.8 AA)

**Generate:**
- Path-based or multipoint gestures have single-pointer alternatives (2.5.1).
- Dragging movements have a non-dragging single-pointer alternative (2.5.7,
  new in 2.2): anything direct-manipulation.skill.md makes draggable
  (reordering watchlist rows, resizing panels, adjusting a range on a chart)
  also works via click-based controls (move up/down buttons, +/- steppers,
  numeric input).
- Actions complete on the up-event or are abortable/undoable (2.5.2).
- The accessible name of a control contains its visible label text (2.5.3) so
  voice-input users can speak what they see — when generating `aria-label`,
  start it with the visible text.
- No motion-only actuation without UI alternative and a disable option (2.5.4).
- Target size ≥ 24×24 CSS px (2.5.8, new in 2.2) for all pointer targets,
  including icon buttons, table row actions, toggles, and chart interaction
  handles; smaller targets only with 24 px spacing offsets, inline-text
  exception, or equivalent larger control. Prefer 44×44 (2.5.5 AAA) for
  primary actions.

**Reject before emitting:** drag-only interactions; targets under 24×24 without
a qualifying exception; visible-label/accessible-name mismatches.

### 2.2 Enough time & 2.3 Seizures (SC 2.2.1, 2.2.2, 2.3.1, Level A)

**Generate:**
- No generated time limits; if the task model demands one (auction, session),
  make it adjustable/extendable per 2.2.1.
- Auto-updating content (live prices, streaming status) provides pause, stop,
  hide, or frequency control (2.2.2) — the watchlist's refresh gets a visible
  pause; pair with the freshness indicator from heuristics-nielsen H1.
- Nothing flashes more than three times per second (2.3.1): no flashing alert
  animations — use a persistent, announced state change instead. Respect
  `prefers-reduced-motion` for all generated animation (2.3.3 AAA, adopted as
  a default because it costs nothing).

---

## Principle 3 — Understandable

Information and operation of the UI must be understandable.

### 3.1 Readable (SC 3.1.1 A, 3.1.2 AA)

**Generate:** the workspace declares its human language (`lang` attribute);
passages in another language are marked with their own `lang` (3.1.2). The
generator knows the dialogue's language — set it, and update it if the user
switches.

### 3.2 Predictable (SC 3.2.1, 3.2.2 A; 3.2.3, 3.2.4, 3.2.6 AA/A)

**Generate:**
- Receiving focus changes no context (3.2.1); changing an input's value does
  not auto-submit, auto-navigate, or re-layout without prior notice (3.2.2) —
  filters apply on explicit action or with clearly announced live filtering.
- Navigation mechanisms repeat in the same relative order across views (3.2.3)
  and identical functions are identified identically (3.2.4) — this is the
  accessibility half of heuristics-nielsen H4's cross-generation consistency:
  regeneration must not reshuffle navigation or rename repeated actions.
- Help mechanisms appear in a consistent location across views (3.2.6, new in
  2.2): the "Why this exists" provenance affordance and any contextual help
  occupy the same relative position on every generated component.

**Reject before emitting:** on-focus or on-input context changes; regeneration
diffs that reorder navigation or relabel identical actions without a user
request.

### 3.3 Input assistance (SC 3.3.1, 3.3.2, 3.3.7 A; 3.3.3, 3.3.4, 3.3.8 AA)

**Generate:**
- Every input has a visible, persistent label or instruction (3.3.2) —
  placeholders are not labels; required formats and units stated up front
  ("Drop threshold (%)").
- Errors are identified in text, naming the field and the problem (3.3.1), and
  suggest a correction where known (3.3.3): "Threshold must be between 0.1%
  and 50% — you entered 300." Announce errors to assistive technology (pair
  with 4.1.3) and move focus or link to the first error. Composes with
  heuristics-nielsen H9's plain-language recovery.
- For actions with legal, financial, or data consequences (deleting
  configurations, committing transactions the task model deems consequential):
  reversible, or checked and correctable, or confirmed via review step (3.3.4)
  — this is the accessibility mandate behind H5's confirmation constraint.
- Redundant entry (3.3.7, new in 2.2): never ask the user to re-enter
  information already provided in the same process — the generator holds the
  shared task model, so auto-populate or offer selection instead; the dialogue
  already captured it.
- If generating authentication, no cognitive function test (memorization,
  transcription, puzzles) without an alternative or assistance — support paste
  and password managers (3.3.8, new in 2.2).

**Reject before emitting:** placeholder-only labeling; error states that only
change color; consequential actions with no reverse/review path; forms that
re-ask what the task model already knows.

---

## Principle 4 — Robust

Content must be robust enough to be interpreted reliably by a wide variety of
user agents, including assistive technologies.

### 4.1 Compatible (SC 4.1.2 A, 4.1.3 AA)

**Generate:**
- Name, role, value (4.1.2): every UI component exposes an accessible name, a
  correct role, and its states/properties programmatically, with changes
  notified to user agents. Semantic HTML first (`<button>`, `<select>`,
  `<input type>`, `<table>`, `<dialog>`); ARIA only to fill genuine gaps, and
  then completely — a `role="switch"` carries `aria-checked` and updates it;
  an expandable section carries `aria-expanded`; a custom combobox implements
  the full pattern or is replaced with a native control. No ARIA is better
  than wrong ARIA.
- Status messages (4.1.3): dynamic changes that do not take focus are exposed
  via live regions so assistive technology announces them — data refreshes
  ("Prices updated 9:31 AM"), alert triggers ("SPY down 3.1% — alert fired"),
  filter result counts ("12 rows shown"), async completion, and agent-initiated
  changes from mixed-initiative actions. Choose politeness appropriately
  (`polite` for updates, `assertive` only for urgent alerts); throttle
  high-frequency streams to meaningful announcements.

**Reject before emitting:** clickable divs where a button belongs; ARIA roles
missing their required states/properties; silent dynamic updates; live regions
that would fire on every price tick.

---

## Verification: the conformance gate

Run both stages over the complete generated surface before instantiation, and
again on every regeneration. Any Level A or AA failure blocks instantiation;
fix and re-verify. AAA items are advisory and reported, not blocking.

### Stage 1 — Automated checks (machine-decidable)

- [ ] **Alt text present**: every image/icon/graphic has alt or is marked
      decorative; every icon-only control has an accessible name. (1.1.1)
- [ ] **Structure**: tables use table semantics with header associations;
      every input programmatically labeled; heading levels do not skip;
      lists are list markup. (1.3.1)
- [ ] **DOM vs. planned reading order**: source order matches the layout
      plan's declared reading sequence. (1.3.2)
- [ ] **Input purpose**: personal-data fields carry autocomplete tokens. (1.3.5)
- [ ] **Contrast**: computed ratios for every text token/background pair
      ≥ 4.5:1 (≥ 3:1 large); every component boundary, state indicator, and
      meaningful graphic ≥ 3:1 against adjacencies. (1.4.3, 1.4.11)
- [ ] **Reflow & spacing**: layout renders at 320 px without 2-D scroll (data
      tables/charts scroll in-region); no clipping under 1.5/2/0.12/0.16
      spacing overrides. (1.4.10, 1.4.12)
- [ ] **Keyboard**: every interactive element focusable and activatable; no
      positive tabindex; modals trap-and-release with Esc; shortcuts
      conformant. (2.1.1, 2.1.2, 2.1.4)
- [ ] **Focus**: visible indicator on every focusable element; focus order
      list matches logical order; no sticky region fully overlaps any
      focusable element's position. (2.4.3, 2.4.7, 2.4.11)
- [ ] **Targets**: all pointer targets ≥ 24×24 CSS px or qualify for an
      exception; drag interactions declare a non-drag alternative. (2.5.8,
      2.5.7)
- [ ] **Label in name**: accessible name contains visible label text. (2.5.3)
- [ ] **Language**: lang set on the workspace; foreign-language parts marked.
      (3.1.1, 3.1.2)
- [ ] **No context change on focus/input** declared by any component. (3.2.1,
      3.2.2)
- [ ] **Forms**: visible persistent labels; error states include text + 
      programmatic association; consequential actions declare
      reverse/review/confirm; no field re-collects task-model-known data.
      (3.3.1, 3.3.2, 3.3.4, 3.3.7)
- [ ] **Name/role/value**: every component resolves to a complete accessible
      role with required states; every dynamic non-focus update maps to a live
      region; live regions throttled. (4.1.2, 4.1.3)
- [ ] **Motion/flash**: no >3 flashes/sec; auto-updating regions expose
      pause/stop/hide; animations gated on prefers-reduced-motion. (2.3.1,
      2.2.2)

### Stage 2 — AI critic checks (judgment required)

- [ ] Alt text and chart summaries convey the *equivalent purpose*, in the
      user's domain vocabulary — not "chart of data". (1.1.1)
- [ ] Headings, labels, titles, and link texts genuinely describe topic or
      purpose to a first-time assistive-technology user. (2.4.2, 2.4.4, 2.4.6)
- [ ] Reading order narrative makes sense when linearized (read the DOM order
      aloud: does the task flow survive?). (1.3.2)
- [ ] Instructions reference nothing by sensory characteristics alone. (1.3.3)
- [ ] Error messages diagnose and suggest in plain domain language. (3.3.1,
      3.3.3)
- [ ] Live-region announcements are meaningful and appropriately urgent, not
      noise. (4.1.3)
- [ ] Consistency across the regenerated surface: navigation order, repeated
      identifications, and help placement unchanged without user request.
      (3.2.3, 3.2.4, 3.2.6)

## Failure handling

If a Level A/AA constraint genuinely cannot be met — an upstream component
library lacks a conformant widget, a data source provides charts only as
opaque images, media arrives without captions — do not silently ship the
violation and do not silently drop the capability. Surface the conflict in the
dialogue, record it in the task model as a known conformance gap with the
affected success criterion, offer the nearest conformant alternative (data
table for the opaque chart; transcript request for the media), and let the
user decide with full information. Uncertainty about whether an exception
applies (is this orientation "essential"? is this drag "essential"?) is a
signal to ask, not to assume the exception.

## Scope notes

- Conformance applies to the full generated page/workspace and to complete
  processes: if any step in a generated multi-step flow fails, the flow fails
  (WCAG conformance requirements 5.2.2–5.2.3). Non-interference criteria
  (1.4.2, 2.1.2, 2.2.2, 2.3.1) apply to everything on the surface, even
  content not otherwise relied upon.
- This skill encodes WCAG 2.2's testable floor. It does not exhaust
  accessibility: cognitive and learning accessibility needs exceed what these
  criteria capture (per the W3C's own guidance), which is precisely the gap
  ability-based-personalization.skill.md and
  cognitive-load-progressive-disclosure.skill.md address above this floor.
- Audit mode: run both verification stages against an existing generated
  interface and report each violation with the success criterion, level,
  failing component, and a proposed regeneration fix.
- The skill tracks the W3C Recommendation; when WCAG updates, update this file
  — conformance guidance ships at the speed of the standard, not the speed of
  model pretraining.
