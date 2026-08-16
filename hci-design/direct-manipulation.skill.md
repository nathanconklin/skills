---
name: direct-manipulation
description: >
  Enforce Ben Shneiderman's direct-manipulation principles as component-level
  constraints for user-interface generation: keep objects of interest and
  their state visible, make actions rapid, incremental, reversible, and visibly
  consequential, and replace command syntax with manipulation of represented
  objects whenever an honest representation is possible. Use whenever
  generating, modifying, extending, regenerating, reviewing, or auditing an
  interactive UI, component library, dashboard, form, table, chart, canvas,
  editor, workflow, control panel, or dialogue-built interface; when designing
  drag, resize, reorder, filter, edit-in-place, selection, navigation, or
  configuration behavior; or when evaluating whether a command, chat, menu, or
  agent action should become an object-level interaction. Apply alongside
  accessibility-wcag for every UI and preserve non-pointer alternatives.
---

# Direct Manipulation as a Component Invariant

## Purpose

Turn direct manipulation from a general preference into an emission gate for
structured UI components. Make the user's task object, available operations,
current state, and the effect of each operation perceptually connected. Reduce
the need to translate a task goal into arbitrary system syntax.

Treat directness as a property of an object-action-feedback loop, not as a
visual style. A graphical interface, an icon, a drag gesture, or an animation is
not direct manipulation by itself. Reject a component when its representation
is unclear, its action is detached from the represented object, its feedback is
delayed or elsewhere, or its mutation cannot be reversed or safely staged.

## Research basis and interpretation

Ground this skill in:

> Ben Shneiderman. 1983. *Direct Manipulation: A Step Beyond Programming
> Languages*. Computer 16, 8, 57-69. DOI: 10.1109/MC.1983.1654471.

Preserve the paper's three central criteria:

1. Keep the object of interest continuously represented.
2. Support rapid, reversible, incremental operations whose effects are
   immediately visible on that representation.
3. Prefer physical selection and manipulation, including clearly labeled
   actions, over complex command-language syntax.

Also preserve the paper's supporting layered or spiral approach to learning:
let a novice operate a small useful layer and discover more power gradually.
Do not mislabel this supporting principle as one of the three central criteria.
Apply it with `cognitive-load-progressive-disclosure` when that skill is
available.

Retain the paper's cautions. Graphic representations do not automatically
improve performance. The wrong content, a cluttered presentation, an unknown
icon, a misleading metaphor, mixed metaphors, or excessive graphic space can
make the interface worse. Some complex or abstract operations have no honest
physical analogue. Prefer a compact labeled representation or an explicit
indirect interaction over a decorative or deceptive simulation of directness.

## Non-negotiable component rule

Evaluate every task-level component and every interactive child against the
three criteria. Use the following applicability rule:

- For an interactive component, require DM-1, DM-2, and DM-3.
- For a read-only component, require DM-1. Mark DM-2 and DM-3 `N/A: read-only`
  only when the component truly exposes no operation.
- For a purely decorative element, exclude it from the direct-manipulation
  inventory and ensure accessibility semantics also mark it decorative.
- For a consequential action that changes the external world and cannot be
  undone, require direct manipulation for preparation and preview, then classify
  the final commitment as a guarded indirect action. Never claim the final
  commitment is reversible.

Do not apply the rule mechanically to every DOM node. Apply it to meaningful
components in the task model: a watchlist row, chart, alert rule, editable
value, node, card, selected range, panel, or workflow step.

## Generation workflow

### 1. Build the interaction inventory

For each component, record this contract before choosing a widget:

```yaml
component_id: stable identifier
task_goal: dialogue-backed reason the component exists
object_of_interest: domain object the user sees or changes
representation: visible form of that object and its current state
operations: user-meaningful actions supported by the component
direct_action: selection, movement, edit, gesture, or labeled action
increment: smallest meaningful step and any live preview
feedback: visible effect attached to the object
inverse: natural inverse operation, if one exists
undo: undo, restore, cancel, or version-recovery mechanism
commit_boundary: local, persisted, or external-world effect
non_pointer_path: keyboard and non-drag equivalent
command_fallback: optional expert path; never the sole routine path
provenance: dialogue turn or task-model fact that justified the component
```

Reject a planned interactive component if any required field is absent. Do not
invent a visible object after choosing a control; derive the representation from
the user's domain object first.

### 2. Select the representation before the gesture

Choose a representation that exposes the task-relevant state and permissible
relationships. Use the user's vocabulary and a single coherent conceptual
model. Prefer compact text, tables, or labeled shapes when they communicate
more accurately than icons or spatial metaphors.

Test both halves of the representation:

- **Static fitness:** Does it show the object, state, identity, relationships,
  selection, constraints, and relevant context?
- **Dynamic fitness:** Does it support the intended selection, editing,
  movement, comparison, filtering, creation, or deletion without implying
  operations the system does not support?

Do not continue to gesture design until both are satisfactory.

### 3. Design the complete action loop

For each operation, define this loop:

```text
perceive object -> perceive available action -> act on object or labeled action
-> see attached incremental feedback -> accept, refine, reverse, or cancel
```

Keep object, action, and feedback in the same perceptual and semantic context.
A detached toast may confirm completion, but it cannot be the only feedback.

### 4. Stage persistence and consequences

Separate exploration from commitment:

- Apply tentative changes locally or in preview while the user manipulates.
- Persist at a clear boundary such as pointer release, Enter, Apply, or Save.
- Preserve the prior state until persistence succeeds.
- Show pending, success, conflict, or failure on the affected object.
- On failure, restore or retain the editable state and offer retry.
- For external or irreversible effects, show a concrete preview and require an
  explicit commit. Add cancellation, revocation, or compensating action when
  the domain supports one.

### 5. Verify before emission and after regeneration

Run the component gate and the whole-surface checks below. Block an interactive
component on any DM-1, DM-2, or DM-3 failure. Re-run the gate on the complete
surface after regeneration because moving or replacing one component can break
another component's visible context, feedback attachment, or learned location.

## DM-1 - Visible objects of interest

### Required behavior

- Continuously represent the domain object while the user considers or acts on
  it. Show its identity and task-relevant current state before action.
- Keep the target visible during manipulation. Do not replace it with an
  unrelated modal, command prompt, or blank loading surface.
- Show selection, focus, edit mode, drag source, valid destination, constraints,
  and disabled state on or adjacent to the represented object.
- Present enough surrounding context to judge the operation: neighboring rows
  for reorder, both sides of a comparison, axes and units for chart selection,
  parent location for a moved item, and current plus proposed value for a change.
- Make system state inspectable. Show stale, pending, conflicted, invalid, and
  saved states instead of concealing them behind generic messages.
- Keep labels visible when icons or gestures might be ambiguous. An icon may
  supplement a word but must not force the user to learn the designer's private
  metaphor.
- Use final-form or high-fidelity preview when representation fidelity affects
  the decision, as in document formatting, layout, chart encoding, or media
  editing.
- Preserve object identity across refresh, sorting, filtering, and
  regeneration. Avoid abrupt relocation or replacement that destroys spatial
  continuity while the user is acting.

### Reject before emitting

- The user must remember or type an identifier for an object that could be
  selected from a visible representation.
- The current value, state, selection, destination, or constraint is hidden.
- The object disappears during action or feedback appears only in a detached
  notification or log.
- An icon, metaphor, or visualization suggests capabilities or relationships
  the underlying object does not have.
- Decorative graphics displace a denser, clearer representation.
- The representation contains the wrong task information or enough clutter to
  obscure the object of interest.

## DM-2 - Rapid, incremental, reversible action with visible impact

Treat DM-2 as four inseparable subchecks.

### DM-2a - Rapid acknowledgment

- Acknowledge input in the same interaction cycle through local visual change,
  pressed state, movement, preview, highlight, or attached pending state.
- Separate immediate acknowledgment from slower completion. If a backend call
  takes time, update the object locally and mark it pending; do not leave the
  user wondering whether the action registered.
- Keep interaction available during unrelated asynchronous work. Avoid freezing
  the full surface for a component-local operation.
- Define and test a project-specific response budget. Do not invent a universal
  millisecond threshold and attribute it to the 1983 paper.

### DM-2b - Incremental operation

- Break continuous changes into observable steps. Update position, size, range,
  value, selection, or preview as the manipulation progresses.
- Let the user stop at an intermediate state and inspect it before continuing.
- Prefer bounded, small operations over a hidden batch that produces a large
  unexplained jump.
- Show propagated consequences when changing one object affects others, while
  preserving a clear causal link to the object being changed.

### DM-2c - Reversibility

- Provide a natural inverse where one exists: move left/right, expand/collapse,
  select/deselect, zoom/unzoom, enable/disable, increment/decrement.
- Provide undo for every local mutation and for persisted mutations the system
  can safely reverse. Group a continuous gesture as one meaningful undo unit.
- Support cancel during preview or in-progress manipulation. Escape and pointer
  cancellation must restore the pre-action state.
- Preserve user work and prior state through validation, network, concurrency,
  and persistence failures.
- Make undo discoverable and scoped: name the object and effect, such as
  `Undo move "Threat Model" to Archive`.
- For deletion, prefer recoverable removal or version history. Confirmation
  alone does not satisfy reversibility.
- For genuinely irreversible actions, stage, preview, and confirm the boundary;
  label the action as irreversible and offer a compensating action if possible.

### DM-2d - Visible impact on the object

- Render the consequence on the represented object immediately: the row moves,
  the value changes, the filter result updates, the shape resizes, or the state
  indicator changes.
- Show before/after or live preview when the effect is not otherwise apparent.
- Keep secondary status messages consistent with the object state; never show
  success while the object still displays the old state.
- Announce dynamic changes through accessible status mechanisms without making
  announcements the only form of feedback.

### Reject before emitting

- The action has no immediate visible acknowledgment.
- Feedback appears only after submit, refresh, or navigation when an incremental
  preview is feasible.
- A mutation has no inverse, undo, cancel, recovery, or honest irreversible
  boundary.
- A drag or continuous control updates only at the end without showing the path
  or proposed result.
- The feedback is detached from the object, ambiguous about what changed, or
  inconsistent with persisted state.

## DM-3 - Replace command syntax with object manipulation

### Required behavior

- Let users select a represented object instead of recalling and typing its
  name, path, coordinate, or identifier.
- Map routine operations to direct edit, drag, resize, selection, gesture,
  constrained control, or a clearly labeled button adjacent to the object.
- Phrase actions in the problem domain, not the implementation domain. Use
  `Move to Archive`, not `PATCH /records/{id}`; use a threshold control, not a
  serialized rule expression.
- Expose legal operands and destinations. Prevent syntax errors by making
  invalid targets unavailable or clearly marked before commitment.
- Keep command palettes, shortcuts, natural-language instructions, formulas,
  and query languages as optional accelerators when users need abstraction or
  scale. Preserve an object-level path for routine operations where feasible.
- When a complex Boolean, mathematical, programmatic, or bulk operation cannot
  be represented without distortion, use a structured builder, examples,
  autocomplete, validation, and live preview. If expert syntax remains the best
  tool, label it as advanced rather than faking direct manipulation.
- Treat chat as a complementary control surface. A user may ask the interface
  to change, but ordinary work on visible objects must not require repeatedly
  describing those objects in prose.

### Reject before emitting

- A routine task requires memorized commands, opaque abbreviations, delimiters,
  paths, IDs, coordinates, or serialized syntax when the object is visible.
- The user must issue a separate command to reveal the result of an action.
- A command field is the only way to perform an operation that maps cleanly to
  selection or manipulation.
- A gesture has no perceivable target, no label or signifier, or no equivalent
  accessible control.
- A visual metaphor is used merely to hide complex syntax while preserving the
  same recall burden.

## Component-specific application

Apply all relevant rows; a composed component may activate several.

| Component | Visible object | Direct action | Incremental feedback | Reverse or recovery |
| --- | --- | --- | --- | --- |
| Button or row action | Named target and current state remain visible | Labeled action beside or within target | Pressed/pending state, then target changes | Undo, inverse action, cancel, or guarded commit |
| Text or numeric field | Current value, label, units, constraints | Edit value in place or through a constrained control | Validate and preview while editing | Esc/cancel, restore prior value, undo |
| Toggle or checkbox | Setting and explicit current state | Select the represented setting | State changes immediately on the control and affected view | Operate the same control to invert; undo failed persistence |
| Slider, stepper, or range | Value, scale, bounds, and affected object | Drag, arrow, click, or step on the control | Value and consequence update continuously | Move back, Reset, undo; retain exact-entry alternative |
| List, table, card set | Items, selection, order, and destination | Select, edit in place, reorder, move, or resize | Source, insertion point, destination, and result stay visible | Move back, undo reorder/edit; provide non-drag controls |
| Chart or visualization | Marks, labels, units, selection, filters | Select, brush, zoom, pan, or manipulate a mutable encoding | Highlight and derived values update during action | Clear/reset/undo; do not imply immutable data is draggable |
| Map, canvas, graph, or timeline | Objects, coordinates/relations, viewport, selection | Pan, zoom, connect, move, resize, or annotate | Ghost, snap, constraint, and affected relationships update live | Cancel gesture, undo, zoom reset, keyboard path |
| Tree, hierarchy, or navigation | Current item, ancestors, siblings, destination | Expand, collapse, select, move, zoom in/out | Current location and newly exposed level remain visible | Collapse/back/unzoom; preserve prior selection |
| Menu, toolbar, or palette | Target and current state remain in context | Choose a labeled operation | Selected state and target effect appear immediately | Undo/inverse; menu selection alone is not sufficient feedback |
| Form or configuration flow | Object being configured plus current draft/preview | Manipulate structured fields and represented choices | Draft and consequences update per field or step | Back/cancel with state preservation, field undo, version restore |
| File or media editor | File/media, selection, playhead, crop, or layer | Drop on a valid target, trim, crop, move, annotate | Preview the exact affected region and output | Undo stack, revert version, cancel export or upload when possible |
| Agent proposal or automation | Proposed object-level changes and affected targets | Accept, reject, edit, or apply selected changes | Show preview, progress, and per-object result | Revoke/undo/compensate plus audit trail; never hide delegation |
| Command, query, or formula editor | Structured operands, examples, results, and errors | Select/insert operands; optional typing for expert expression | Parse, validate, and preview continuously | Edit/cancel, version history, restore last valid expression |

### Dragging is never sufficient by itself

Use drag only when source, destination, motion, and consequence are meaningful.
Always provide:

- visible drag handles or another clear signifier;
- source and valid/invalid destination states;
- a live insertion, resize, range, or movement preview;
- pointer cancellation and undo;
- keyboard operation; and
- a non-drag single-pointer alternative such as Move up/down, a destination
  menu, steppers, or exact-value input.

Do not make a component draggable simply to appear direct.

## Representation-suitability gate

Before approving a visual or physical metaphor, answer all questions:

1. Does the representation contain the information needed for this task?
2. Is it more compact or comprehensible than the available textual or tabular
   form?
3. Will users understand the objects and operations without learning a private
   icon language?
4. Does it accurately bound what can and cannot be done?
5. Does it avoid mixing incompatible metaphors?
6. Does it remain legible at the available screen size and under personalized
   text, zoom, contrast, and target-size settings?
7. Can the object-action-feedback loop be operated by keyboard, pointer, touch,
   voice, and assistive technology as applicable?

If any answer is no, repair the representation, choose a simpler model, or use
an honest labeled indirect interaction. Record the decision in the component
contract.

## Whole-surface constraints

- Preserve cross-generation continuity: stable object identity, location,
  terminology, interaction pattern, selection, focus, undo history, and draft
  state unless the user requested a change.
- Keep the smallest useful capability layer visible. Reveal advanced direct
  operations when the task entails them without removing the basic layer.
- Allow novices to learn by observation and successful action. Keep expert
  accelerators additive rather than substitutive.
- Support exploration by lowering the cost of a wrong turn: small steps,
  previews, inverse actions, undo, and minimal lost work.
- Preserve user control. Do not let agentic behavior silently manipulate
  objects on the user's behalf; preview and instrument such changes.
- Avoid gamelike randomness in task interfaces. Keep system behavior
  predictable even when motion or animation makes feedback vivid.

## Composition with other UI skills

- **accessibility-wcag:** Treat WCAG Level A and AA as the universal floor.
  Direct manipulation never authorizes drag-only, pointer-only, unlabeled,
  low-contrast, or inaccessible custom widgets. In particular, satisfy WCAG
  2.2 SC 2.5.7 with a non-dragging single-pointer alternative and SC 2.1.1 with
  keyboard access.
- **affordances-norman:** Make the available direct action perceptible. A true
  action with no signifier still fails; a signifier for an unavailable action
  makes the representation misleading and fails DM-1.
- **heuristics-nielsen:** Pair visible impact with system-status feedback, pair
  reversibility with user control and freedom, and preserve consistency across
  regeneration.
- **cognitive-load-progressive-disclosure:** Keep the initial action set small
  and task-justified while retaining the visible object and a discoverable path
  to more power.
- **ability-based-personalization:** Adapt gesture complexity, target size,
  density, feedback duration, and input method to the user without weakening
  the object-action-feedback loop.
- **mixed-initiative:** Treat autonomous action as delegation, not direct
  manipulation. Require proposal visibility, confidence, preview, approval as
  appropriate, auditability, and reversal or compensation.

When constraints conflict, keep the stricter safety or accessibility rule and
choose a different direct-manipulation pattern.

## Verification gate

Run both stages over every interactive component and the complete surface. A
single unresolved mandatory failure blocks emission.

### Stage 1 - Structural and interaction checks

- [ ] Every interactive component has a complete interaction contract.
- [ ] Every component resolves to a visible domain object and task-model goal.
- [ ] Current state, selection, constraints, and destination are represented.
- [ ] Every operation declares an immediate attached acknowledgment.
- [ ] Every continuous operation declares live incremental feedback.
- [ ] Every mutation declares a natural inverse, undo, restore, cancel, or an
      explicit guarded irreversible boundary.
- [ ] Every persistence operation preserves prior state until success.
- [ ] No routine operation requires command syntax when object manipulation is
      feasible.
- [ ] Every drag has keyboard and non-drag pointer alternatives.
- [ ] Every object and action exposes accessible name, role, value, and state.
- [ ] Regeneration preserves identity, focus, selection, drafts, and undo
      history unless change is justified.
- [ ] Static components mark DM-2/DM-3 N/A explicitly; decorative elements are
      excluded rather than falsely passed.

### Stage 2 - Simulation and critic checks

- [ ] **First-use test:** Can a person identify the object and a useful action
      without recalling syntax or reading a manual?
- [ ] **Wrong-turn test:** Can the person try a small action, see its effect,
      and return to the exact prior state without lost work?
- [ ] **Latency test:** Does input receive immediate local acknowledgment while
      slower work remains visibly attached to the object?
- [ ] **Increment test:** During a continuous action, can the person inspect and
      stop at intermediate states?
- [ ] **Causality test:** When related values propagate, is it clear which
      manipulated object caused the change?
- [ ] **Metaphor test:** Does the representation communicate only real objects,
      relationships, and permissible operations?
- [ ] **Density test:** Would text or a table show more relevant objects or
      relationships with less clutter?
- [ ] **Accessibility test:** Can the same task be completed without dragging,
      precise pointing, vision, or a memorized gesture?
- [ ] **Command-substitution test:** Is any remaining syntax genuinely required
      by abstraction or scale, optional where possible, validated, and paired
      with a visible result?
- [ ] **Regeneration test:** Can an existing user continue acting without
      relearning positions, representations, or controls?

## Audit mode

When reviewing an existing interface, produce one finding per failing
component in this form:

```text
Component: <stable name or selector>
Criterion: DM-1 | DM-2a | DM-2b | DM-2c | DM-2d | DM-3
Evidence: <observable failure>
User cost: <recall, delay, uncertainty, error risk, anxiety, or lost work>
Severity: blocker | major | minor
Repair: <specific representation, action, feedback, or reversal change>
Related constraints: <WCAG, affordance, heuristic, personalization, if any>
```

Classify a missing visible object, absent feedback, unrecoverable ordinary
mutation, drag-only action, or command-only routine operation as a blocker.
Classify a misleading representation or falsely reversible external action as a
blocker even if the interface is visually polished.

## Failure handling

If a criterion cannot be satisfied:

1. Do not silently emit the component and do not label it direct manipulation.
2. Identify the failing criterion and the domain constraint.
3. Offer the nearest honest alternative: a clearer representation, labeled
   action, structured builder, preview, staged commit, version recovery, or
   optional expert syntax.
4. Preserve accessibility and safety even if that makes the interaction less
   physically direct.
5. Ask the user only when the unresolved choice materially changes the task,
   risk, or representation; otherwise choose the simplest compliant repair.

## Success condition

Approve the interface only when every interactive component keeps a faithful
object of interest in view, lets the user act in small observable steps with
immediate object-level feedback, provides a way back or an honest guarded
commit boundary, and avoids making routine work depend on arbitrary command
syntax. The result should let the interface recede while the user's task remains
visible, predictable, and under the user's control.
