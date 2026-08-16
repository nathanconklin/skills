---
name: affordances-norman
description: >
  Enforce Donald Norman's affordance and signifier principles as generation-time
  constraints on interactive user interfaces. Load this skill whenever generating,
  modifying, extending, regenerating, selecting components for, or auditing any UI
  with user-operable controls, including buttons, links, fields, selectors, toggles,
  menus, tabs, sortable tables, draggable or resizable objects, charts, canvases,
  direct-manipulation surfaces, and agent-created actions. Also load when a user
  cannot discover an action, attempts an action the interface does not support,
  asks how a control works, or asks whether perceived form matches real behavior.
  Apply the rules at both component-library and composition levels: reject controls
  that falsely promise action, hide real action, map ambiguously to their targets,
  conceal constraints or state, or fail to communicate their results.
---

# Norman's Affordances and Signifiers as Generation Constraints

## Purpose and authority

Turn Norman's principles into an inline generation and verification policy. Because
an on-demand UI generator emits structured component code, require declared actions,
approved signifier contracts, and behavioral verification before a control reaches
the user. Make good interaction a property of generation rather than a post-hoc
design review.

Ground this skill in:

- Donald A. Norman. 2013. *The Design of Everyday Things*, revised and expanded
  edition. Basic Books, New York, NY, USA. ISBN 978-0-465-05065-9.
- Don Norman, "Affordances and Design," https://jnd.org/affordances-and-design/,
  and "Signifiers, Not Affordances," https://jnd.org/signifiers-not-affordances/.
- Nathan Conklin, Miranda Capra, and Chris North. 2026. "Automating the Application
  of HCI Principles: Skills for On-Demand UI Construction, the Human-AI Space to
  Think, and the Future of HCI."

Treat "perceived form must signal real action" as the paper's operational synthesis,
not a verbatim quotation from Norman. Interpret it through Norman's distinctions:
affordances make action possible; anti-affordances prevent action; signifiers
communicate what to do and where; mappings connect controls to effects; constraints
narrow alternatives; feedback communicates results; and the system image supports
a useful conceptual model.

Compose with `heuristics-nielsen.skill.md`, `accessibility-wcag.skill.md`,
`direct-manipulation.skill.md`, `cognitive-load-progressive-disclosure.skill.md`,
`mixed-initiative.skill.md`, and `ability-based-personalization.skill.md`. Satisfy all
applicable constraints; let the stricter testable requirement govern. Never weaken
WCAG conformance or a user's required accommodation to preserve a visual convention.

## Core operating model

Use these terms precisely.

- **Affordance:** Treat an affordance as a relationship between interface properties
  and an actor's capabilities that makes an action possible. Do not call a shadow,
  border, icon, label, cursor, or color an affordance; those may be signifiers.
- **Anti-affordance:** Treat an anti-affordance as prevention of interaction. Make
  prevention perceivable before the user attempts the blocked action.
- **Signifier:** Treat a signifier as any perceivable cue that communicates appropriate
  behavior. Include form, label, icon, position, grouping, boundary, motion, sound,
  cursor, and visible state. Account for intended and unintended signifiers created by
  composition.
- **False signifier:** Treat a cue that promises an unsupported, unavailable, or
  different action as a defect. Examples include a raised static card, a decorative
  chevron on a fixed row, or static text styled like an input.
- **Orphan affordance:** Treat a supported user-facing action with no discoverable
  access point as a defect. A gesture, shortcut, hidden handler, or clickable region
  does not become discoverable merely because it exists in code.
- **Mapping:** Make the relationship among control, action, affected object, direction,
  scope, and result clear through proximity, containment, spatial correspondence,
  labels, and temporal contiguity.
- **Constraint:** Use physical, logical, semantic, and cultural constraints to reduce
  invalid alternatives. Make the restriction understandable before failure.
- **Feedforward and feedback:** Use signifiers, mappings, constraints, and the
  conceptual model to communicate what can happen before action. Use feedback to
  communicate what happened after action.
- **System image and conceptual model:** Make the complete rendered surface, states,
  relationships, labels, feedback, help, and dialogue provenance support a coherent
  and non-misleading explanation of how the interface works.

Bridge the Gulf of Execution by answering what actions are possible, which control
performs them, where to act, and how. Bridge the Gulf of Evaluation by answering
whether the system received the action, what changed, whether the result met the
goal, and how to recover or continue.

## Severity model

Classify findings before deciding whether to instantiate:

- **Blocking:** Reject false signifiers, orphan primary affordances, broken or
  contradictory behavior, ambiguous consequential actions, inaccessible-only paths,
  misleading state, and mappings that can affect the wrong object.
- **Repair before release:** Repair weak secondary signifiers, unclear scope, poor
  feedback, confusable adjacent controls, or inconsistent conventions. Block only the
  affected component or flow until repaired; do not discard an unrelated valid UI.
- **Test required:** When a novel, cultural, domain-specific, or context-dependent
  signifier is plausible but uncertain, run a first-exposure probe. Do not convert
  critic uncertainty into either automatic acceptance or an endless rejection loop.

## Generation workflow

1. **Read the task model.** Identify goals, domain objects, planned actions, state
   transitions, risks, input modalities, user capabilities, and dialogue provenance.
2. **Inventory actions.** Include visible controls, gestures, shortcuts, implicit row
   or chart interactions, hover/focus behaviors, disabled states, progressive
   disclosures, and agent-initiated actions.
3. **Bind each action to a component contract.** Reuse an approved component-library
   variant. Do not attach interaction handlers to passive containers when a semantic
   component exists.
4. **Declare instance-specific bindings.** Record the action, target, preconditions,
   result, scope, reversal path, and provenance. Do not repeat variant-level semantics,
   signifier tokens, and state behavior on every instance.
5. **Compose without erasing cues.** Prevent theme, density, responsive layout,
   minimalism, personalization, or local styling from removing required signifiers.
6. **Run structural, rendered-state, behavioral, and critic checks.** Check the whole
   surface on every regeneration because adjacency and styling can create unintended
   cues in unchanged components.
7. **Repair and recheck.** Correct the action or component before adding explanatory
   text. Do not ship a simple control that needs a paragraph to explain basic use.
8. **Learn from user difficulty.** Treat "How do I use this?", an unsupported click,
   or repeated misoperation as evidence about the design. Record and repair the
   responsible component rather than blaming the user.

## Two-level interaction contract

Declare stable rules once at the library-variant level and bind only contextual facts
at the instance level.

```yaml
component_variant_contract:
  library_id: string
  semantic_primitive: string
  supported_actions: [activate, edit, select, toggle, drag, resize, navigate, reveal]
  input_methods: [pointer, touch, keyboard, voice]
  mandatory_signifiers: [string]
  supported_states: [default, focus, active, selected, disabled, busy, invalid]
  feedback_contract: string
  accessibility_contract: string
  allowed_customizations: [string]
  forbidden_overrides: [string]

component_instance_binding:
  id: string
  library_id: string
  user_goal: string
  action: string
  controlled_object: string
  scope: string
  preconditions: [string]
  result: string
  reversible_by: string | null
  provenance: dialogue-turn-or-task-model-id
```

Reject missing bindings, variant/instance contradictions, unsupported actions, and
rendered states that disagree with either contract.

## Universal invariants

### N1 - Bidirectional action truth

Ensure every real user-facing action has a perceivable point of access and every
control-like cue corresponds to a real action. Reserve interaction vocabulary for
interaction. Allow passive surfaces to use borders, grouping, or elevation only when
their complete treatment does not imply operation in context.

### N2 - Resting discoverability

Give each primary action a persistent cue visible without hover, motion, cursor
change, tooltip, trial, or error. Use hover, focus, animation, cursor, and tooltips as
reinforcement. Permit shortcuts and gestures as accelerators only alongside a
discoverable path.

### N3 - Conventional but context-sensitive form

Prefer established component-library and platform conventions. Do not mandate one
appearance across every design system. Require a button to be recognizable as a
button, not necessarily filled or raised; require a draggable object to signal
movement, not necessarily through one universal grip. Validate novel forms rather
than assuming novelty is self-explanatory.

### N4 - Honest availability and state

Differentiate applicable enabled, focus, active, pressed, selected, checked,
expanded, busy, invalid, read-only, and disabled states visually and
programmatically. Never make unavailable action look enabled. Explain temporary
unavailability when the reason or path forward is not obvious. Do not require an
explanation for an already self-evident restriction.

### N5 - Clear mapping and scope

Associate each control with its target through position, containment, alignment,
labels, and spatial or semantic correspondence. Make global, multi-object, and
cross-view scope visible before activation. Ensure directional controls produce the
signaled direction and repeated row/card actions affect only their bound object.

### N6 - Guiding constraints

Make invalid operations impossible where practical and signify the restriction
before attempt. Prefer typed, bounded, and constrained controls over free text when
the domain defines valid values. Hide irrelevant actions; show disabled actions when
their existence or unmet precondition helps the user understand the path forward.

### N7 - Immediate, informative, proportionate feedback

Acknowledge input immediately and communicate the resulting state, not merely that
something happened. Keep feedback attributable to the initiating action and near the
expected locus. Distinguish received, in progress, completed, failed, and canceled.
Prioritize consequential feedback and keep routine confirmation unobtrusive.

### N8 - Capability-relative action

Evaluate action relative to the intended user, device, context, and modality. Do not
call an interaction available when it requires precision, perception, memory, or an
input method the user lacks and no equivalent exists. Apply WCAG as the universal
floor and ability-based personalization above that floor.

### N9 - Coherent conceptual model

Use consistent objects, verbs, causal relationships, and state models across the
surface and across regenerations. Do not imply independent effects when controls are
coupled or immediate effects when an action only previews, proposes, queues, or
requests a result.

### N10 - Error-aware design

Distinguish slips from mistakes. Prevent slips through distinct controls, visible
state, mappings, constraints, and undo. Prevent mistakes through clear consequences,
sensibility checks, and a coherent model. Make unavoidable modes continuously visible
in the region they affect. Treat repeated user error as a design signal.

## Corrected component archetype matrix

Treat this matrix as a minimum behavior and signification contract, not a universal
visual style. Let the approved design system determine exact tokens.

| Archetype | Real action | Required signification and behavior | Reject |
|---|---|---|---|
| Button | Activate command | Semantic button; visible action label or unambiguous contextual label; recognizable library-approved button treatment; focus, active, busy, and disabled states as applicable; result feedback | Passive-looking command; passive surface styled as a button; vague consequential label such as "OK" |
| Link | Navigate or open destination | Semantic link; destination discernible from text/context; distinguishable from surrounding content without color alone | "Click here"; link semantics used for a non-navigation command without clear convention |
| Editable field | Enter or edit value | Persistent label; recognizable editable surface or established inline-edit cue; current value, units/format, caret on focus, and clear invalid/read-only states | Placeholder-only label; static-looking secret edit; read-only state that still promises editing |
| Checkbox/radio/switch | Select or change state | Correct semantic pattern; visible persistent state; label mapped to control; state not conveyed by hue alone | Binary control with hidden or ambiguous current state; switch that secretly requires an unexplained second commit |
| Select/combobox/menu/disclosure | Choose, command, or reveal | Conventional indication that options/content exist; visible current selection or expansion; expected keyboard behavior; clear distinction among selection, commands, and disclosure | Unlabeled chevron or text that opens unknown content; one pattern reused for conflicting actions |
| Tabs/segmented control | Switch peer view or choice | Visible peer set; selected state; one-to-one panel/choice mapping; spatial association | Tab styling for unrelated navigation or independent commands |
| Slider/stepper/range | Adjust value | Dimension, current value, range, direction, and units; natural directional mapping; precise and keyboard alternative when needed | Unlabeled track or knob; direction/result mismatch; slider-only path when exact entry is required |
| Sortable header | Sort collection | Header is operable and announces sortability; current direction visible; resting cue chosen to remain discoverable without forcing identical glyphs in every design | Sorting discoverable only through unexplained clicking; state visible only after leaving the table |
| Draggable/reorderable object | Move or reorder | Persistent movement cue appropriate to context; legal targets and insertion position during action; visible confirmation; non-drag alternative; dedicated handle when embedded controls or whole-object dragging would be ambiguous | Drag-only path; invisible hit region; handle that does not drag; ambiguous card/row behavior |
| Resizer/splitter | Resize regions | Visible divider or grip; permitted axis; adequate hit area; direct mapping; live/preview feedback; keyboard adjustment and reset | Decorative divider that appears resizable; invisible functional edge; wrong-axis movement |
| Expandable region | Reveal/collapse content | Scope and expanded state visible; semantic expanded state; control remains associated with revealed content | Decorative expansion glyph; clickable row with no disclosure cue |
| Row/card action | Act on bound item | Persistent or otherwise conventionally discoverable action; target binding; embedded actions use their own semantic archetypes | Whole-card click with no cue; hover-only primary action; action mapped to wrong item |
| Icon-only control | Contextual command | Established icon in context; accessible name; tooltip on hover/focus; visible control boundary when context requires one | Novel or consequential icon with no text; same icon used for conflicting actions |
| Chart/canvas/map interaction | Select, brush, zoom, drill, manipulate | Cues at the object of interest; visible modes; labeled controls or first-use hint for non-obvious interaction; structured/equivalent path; local feedback | Silently interactive pixels; gesture-only capability; state or selection visible only through color |
| Static content | None | May use visual grouping, borders, or elevation only when the complete contextual treatment remains non-interactive | Cursor, pressed response, disclosure cue, caret, focusability, or other action signal without action |

An archetype's behavioral contract is a floor. Do not weaken mandatory semantics,
states, or cues through local styling. When no approved archetype fits, redesign with
existing components or block the affected capability pending a library addition.

## Constraints, forcing functions, and error defenses

Use Norman's four constraint classes deliberately:

- **Physical:** Prevent impossible operations in behavior and data types.
- **Logical:** Expose actions consistent with current state and arrangement.
- **Semantic:** Offer actions meaningful for the object and task.
- **Cultural:** Follow learned platform, locale, and domain conventions.

For consequential actions, choose the weakest effective forcing function:

- Use an **interlock** to require a safe sequence.
- Use a **lock-in** only when leaving before completion would cause harm; provide an
  explicit safe exit.
- Use a **lockout** to place a deliberate barrier before dangerous or irreversible
  action.

Do not burden routine actions with excessive confirmations. Use undo, previews,
sensibility checks, constrained input, and visible consequences before escalating to
a stronger forcing function. Distinguish adjacent destructive and routine controls by
more than position or label length.

## Workspace signifier registry and regeneration

Maintain a workspace-scoped registry of established forms, meanings, and contexts.
Enforce these corrected rules:

- Do not let one established form acquire conflicting meanings in the same context.
- Permit the same action to use multiple conventional forms when context, density, or
  modality requires it, but keep labels, semantics, and consequences consistent.
- Preserve learned controls, terminology, spatial position, and state models across
  regeneration unless the user's request requires change.
- Recheck the whole composed surface for accidental signifiers created by new
  adjacency, elevation, borders, alignment, or motion.
- Signal that the on-demand interface itself is malleable through an established
  conversational or editing affordance.
- Resolve minimalism conflicts by removing unjustified capability, grouping secondary
  actions behind a discoverable disclosure, or selecting a quieter conforming
  archetype. Never keep a hidden primary capability by stripping its signifier.

## Verification gate

### Stage 1 - Structural and contract checks

- [ ] **N-AFF-01 Coverage:** Every user-facing action maps to a component instance
      binding and approved variant.
- [ ] **N-AFF-02 Reality:** Every declared action works in every state presented as
      available.
- [ ] **N-SIG-01 Forward truth:** No primary action lacks a resting signifier.
- [ ] **N-SIG-02 Reverse truth:** No passive node presents a misleading action cue.
- [ ] **N-LIB-01 Conformance:** No passive container substitutes for an available
      semantic component; no forbidden variant override is present.
- [ ] **N-STA-01 State agreement:** Visual and programmatic state agree.
- [ ] **N-MAP-01 Target binding:** Every control identifies its affected object and
      scope; repeated controls bind to the correct instance.
- [ ] **N-CON-01 Constraint declaration:** Invalid operations are prevented or
      intentionally handled; non-obvious blocked states expose a reason/path.
- [ ] **N-FBK-01 Feedback:** Every action declares acknowledgement, result, and
      completion/error behavior.
- [ ] **N-EQV-01 Equivalence:** Capability-restricted interactions expose applicable
      alternative input paths.
- [ ] **N-REG-01 Registry stability:** No established form changes meaning in its
      context without an explicit, justified migration.

Any contradiction, false signifier, broken primary path, accessibility failure, or
wrong-target mapping blocks the affected component or flow.

### Stage 2 - Rendered-state and behavioral checks

- [ ] Render every applicable default, hover, focus, active, selected, disabled,
      read-only, busy, invalid, success, and error state in supported themes and
      responsive sizes.
- [ ] Confirm required labels, boundaries, handles, carets, focus, and state indicators
      remain perceivable in context.
- [ ] Activate each control through declared input methods and compare the actual
      transition with its contract.
- [ ] Confirm feedback appears promptly, at the expected locus, and names the result.
- [ ] Confirm directional, slider, drag, resize, and reorder actions produce the
      signaled direction, axis, range, target, and insertion point.
- [ ] Confirm disabled/read-only components reject prohibited action without
      masquerading as enabled/editable.
- [ ] Confirm responsive composition keeps control, label, target, result, and
      feedback associated.

Behavioral mismatches block. Weak secondary presentation enters repair-before-release.

### Stage 3 - First-exposure AI critic

Without reading implementation metadata, inspect the rendered surface and infer for
each primary control:

- What action is possible, where and how should it be performed, and what object will
  it affect?
- What result and scope should be expected?
- What is the current state and is action available?
- After activation, what happened and did it satisfy the apparent goal?
- Does any form promise an unsupported action or hide a real primary action?
- Does the complete surface support a coherent and non-misleading model?

Compare inference against the contracts. Block material mismatches for primary or
consequential action. Repair secondary mismatches. Mark plausible context-dependent
forms as test-required rather than guessing.

### Stage 4 - First-exposure task probe

For new, changed, novel, primary, or consequential patterns, give a fresh critic or
representative user only the rendered interface and a realistic goal. Measure whether
they select the correct control, predict the result, recognize state, and interpret
feedback without coaching. Treat repeated exploratory clicking or misidentification
as evidence of failure. Do not require this expensive probe for every unchanged,
previously validated conventional component.

## Repair order

1. Correct or remove the false, hidden, or broken action.
2. Replace the component with an approved semantic archetype.
3. Restore or strengthen the conventional primary signifier.
4. Correct control-to-object, direction, scope, and action-to-result mapping.
5. Clarify constraints, availability, and state.
6. Add immediate and informative feedback.
7. Clarify the conceptual model through grouping, labeling, or disclosure.
8. Re-run applicable stages against the complete affected surface.

Do not use documentation as the first repair for a simple component. If a button,
handle, field, or disclosure requires a paragraph to explain basic operation, replace
the component or mapping.

## Failure handling and audit output

If no conforming component can represent a required action, do not silently ship a
custom control or drop the capability. Record the blocked action and failed rule,
surface the conflict in dialogue, and offer the nearest conforming alternative. Treat
uncertainty as a reason to test or ask, not permission to ship.

When auditing, report each violation with rule ID, component and state, inferred
action, implemented action, affected user goal/capability, severity, proposed
component-library or regeneration fix, and evidence needed to verify repair. End with
counts for contracts examined, blocking failures, repair findings, test-required
findings, library changes, and first-exposure probes.

## Final invariant

Instantiate no interactive component unless its perceivable form truthfully signals a
real and available action, its mapping and constraints guide the intended operation,
its state and feedback make the result understandable, and the complete surface
supports a coherent conceptual model. A button must look pressable and be pressable.
A draggable object must signal movement and move the signaled object in the signaled
way. An editable field must signal editability and accept the signaled editing method.
Reject or repair everything else before it reaches the user.
