---
name: affordances-norman
description: >
  Enforce Donald Norman's affordance and signifier principles as blocking
  constraints on generated user interfaces. Load this skill whenever
  generating, modifying, extending, regenerating, or auditing any interactive
  UI component, including buttons, links, editable fields, selectors, toggles,
  menus, tabs, draggable or resizable objects, direct-manipulation surfaces,
  charts with interaction, and agent-created controls. Use it when a user asks
  whether an action is discoverable, whether a control looks actionable,
  whether perceived form matches real behavior, or why a control has a
  particular visual or interaction treatment. Apply it inline at the component
  library and composition levels: reject any control whose signifiers do not
  reveal its real actions, whose appearance promises an unavailable action, or
  whose mapping, constraints, state, and feedback do not make the interaction
  understandable before the UI reaches the user.
---

# Norman's Affordances and Signifiers as Generator Invariants

## Authority and scope

Use this skill as a procedural interpretation of:

- Donald A. Norman. 2013. *The Design of Everyday Things*, revised and expanded
  edition. Basic Books, New York, NY, USA. ISBN 978-0-465-05065-9.
  Publisher record: https://www.hachettebookgroup.com/titles/don-norman/the-design-of-everyday-things/9780465050659/
- Don Norman, "Affordances and Design," https://jnd.org/affordances-and-design/,
  and "Signifiers, Not Affordances,"
  https://jnd.org/signifiers-not-affordances/.
- Nathan Conklin, Miranda Capra, and Chris North. 2026. "Automating the
  Application of HCI Principles: Skills for On-Demand UI Construction, the
  Human-AI Space to Think, and the Future of HCI."

Treat the paper's sentence "perceived form must signal real action" as the
operational thesis of this skill. Do not present that sentence as a verbatim
quotation from Norman. Ground its implementation in Norman's distinctions:
affordances concern possible action; signifiers communicate what to do and
where; mappings relate controls to effects; constraints limit alternatives;
feedback communicates results; and the system image supports a useful
conceptual model.

Compose this skill with:

- `heuristics-nielsen.skill.md` for consistency, recognition, status, error
  prevention, and recovery.
- `accessibility-wcag.skill.md` for keyboard equivalence, focus, name-role-value,
  target size, contrast, labels, alternatives to dragging, and perceivability.
- `direct-manipulation.skill.md` for visible objects, incremental action, and
  reversible manipulation.
- `cognitive-load-progressive-disclosure.skill.md` for minimum sufficient
  surface area.
- `mixed-initiative.skill.md` for confirmation, confidence, auditability, and
  reversibility of actions that affect the world.

Where rules overlap, satisfy all of them. Let the stricter constraint govern.

## Purpose

Convert Norman's design principles from post-hoc critique into generation-time
invariants. Because the generator emits structured component code rather than
raw pixels, require each interactive element to declare its action contract,
select a library component whose signifier contract matches it, and pass
automated and critic checks before instantiation.

Block both classes of signifier failure:

1. **False promise:** the surface looks actionable in a particular way, but the
   promised action is absent, disabled without explanation, or produces a
   different result.
2. **Hidden possibility:** an action exists in code, but the user cannot
   discover from perceivable cues what can be done, where to act, or how to act.

Do not repair either class with documentation alone. Prefer a self-signifying
component. Use concise labels or instruction only when the action cannot be
made sufficiently clear through form, placement, convention, and state.

## Norman-grounded operating model

Apply these distinctions precisely.

### Affordance

Treat an affordance as a relationship between the properties of the interface
and the capabilities of the acting person or agent. Do not describe a color,
shadow, underline, icon, or cursor as the affordance itself. Those are potential
signifiers. The affordance is the action the person can actually perform under
the current conditions.

For every planned interaction, declare:

- the actor capabilities assumed (pointer, touch, keyboard, voice, assistive
  technology, motor precision, vision, hearing, cognition);
- the action that is actually possible;
- the preconditions and current availability of that action;
- the state transition and external effect;
- an equivalent path when the primary action excludes a relevant capability.

### Anti-affordance

Treat an anti-affordance as prevention of an interaction. Make prevention
perceivable before the user attempts the action. Pair a blocked action with a
clear state and, when useful, a reason or path to enable it. Do not rely on a
failed click, silent no-op, or error after the attempt as the first signal.

### Signifier

Treat a signifier as a perceivable indicator that communicates appropriate
behavior. Permit deliberate signifiers such as labels and icons and structural
signifiers such as shape, position, grouping, boundary, motion, sound, cursor,
or visible state. Require the cue to be perceivable by the intended actor and
consistent with the actual action.

Do not assume that conventional appearance is universal. Validate conventions
against platform, locale, domain, input modality, and user capability. Preserve
well-established conventions unless the task supplies a compelling reason to
depart from them and testing demonstrates equal or better discoverability.

### Mapping

Make the relationship among control, action, controlled object, direction, and
result obvious. Prefer direct, spatial, semantic, and temporally contiguous
mappings. Place a control on or near the object it affects when practical. If a
control affects several objects or an object has several controls, represent
the relationship explicitly and unambiguously.

### Constraints

Use physical, logical, semantic, and cultural constraints to reduce the set of
possible actions and prevent error:

- **Physical:** make invalid operations impossible in the component behavior.
- **Logical:** expose only actions consistent with the current state and task.
- **Semantic:** allow actions that make sense for the meaning of the object.
- **Cultural:** follow learned platform and domain conventions.

Make constraints visible enough to guide action before failure. Do not disable
an action without communicating why when the reason is not obvious.

### Feedback and feedforward

Use signifiers, constraints, mappings, and the conceptual model as
feedforward: communicate what can happen before action. Use feedback to
communicate what happened after action. Provide both. Make feedback immediate,
informative, proportionate, attributable to the triggering action, and visible
in the location where the user expects the result.

Avoid feedback noise. Prioritize critical changes; render routine confirmation
unobtrusively; never use an undifferentiated beep, flash, or spinner as the only
explanation of state.

### Conceptual model and system image

Make the rendered UI, labels, states, relationships, help, and feedback form a
coherent system image from which the user can infer a useful conceptual model.
Do not expose a control organization that implies a false causal model. Keep
the model simple enough to support prediction, but never simplify it into a
misleading relationship.

### Gulfs of execution and evaluation

Bridge the Gulf of Execution by making it easy to determine:

- what actions are possible;
- which control performs the intended action;
- where and how to operate the control;
- what preconditions or constraints apply.

Bridge the Gulf of Evaluation by making it easy to determine:

- whether the system received the action;
- what changed and what remains unchanged;
- whether the result matches the user's goal;
- how to recover or continue.

## Required generation workflow

1. **Read the task model.** Identify each user goal, domain object, planned
   action, state transition, affected object, risk, input modality, and dialogue
   provenance link.
2. **Create an action inventory.** Include visible actions, gestures, keyboard
   commands, hover/focus behaviors, implicit row or chart interactions, agentic
   actions, disabled states, and actions revealed progressively.
3. **Declare an interaction contract.** For every action, record actual
   capability, signifiers, mapping, constraints, feedback, failure state,
   reversal path, and accessibility equivalent.
4. **Select a conforming library component.** Reuse an approved component whose
   tested signifier contract matches the action. Do not hand-roll a one-off
   interactive surface when an approved semantic component exists.
5. **Compose without erasing signifiers.** Prevent layout, theme, density,
   responsive behavior, or visual customization from removing required
   boundaries, labels, handles, focus, state, or feedback.
6. **Run the conformance gate.** Execute structural checks, rendered-state
   checks, interaction checks, and an AI critic pass over the complete surface.
7. **Repair before instantiation.** Replace or redesign every failing component,
   then rerun the entire gate. Do not ship with a warning.
8. **Revalidate on regeneration.** Check the complete UI, not only the diff.
   New adjacency, density, state, or visual tokens can create a false or hidden
   signifier in an unchanged component.

## Interaction contract

Require every interactive component instance to expose an equivalent of this
manifest in structured code or generator metadata:

```yaml
interaction_contract:
  id: string
  component_library_id: string
  controlled_object: string
  user_goal: string
  actual_actions:
    - action: activate | edit | select | toggle | drag | resize | navigate | reveal
      input_methods: [pointer, touch, keyboard]
      preconditions: [string]
      result: string
      reversible_by: string | null
  signifiers:
    - channel: form | label | icon | position | cursor | motion | sound | state
      cue: string
      communicates: string
  mapping:
    control_to_object: string
    action_to_result: string
  constraints:
    allowed: [string]
    blocked: [string]
    blocked_reason: string | null
  feedback:
    acknowledgement: string
    changed_state: string
    completion_or_error: string
  accessibility_equivalents: [string]
  provenance: dialogue-turn-or-task-model-id
```

Reject a component whose manifest is missing, contradicts its rendered states,
or declares an action the implementation does not support.

## Universal blocking constraints

### N1 - Action truth

Make every signaled action real and every real user-facing action signaled.
Ensure activation method, availability, target, direction, scope, and outcome
match the cue. Reject decorative elements that impersonate controls and
controls styled to resemble passive content.

### N2 - Perceivable signifiers

Provide at least one persistent primary signifier for every primary action.
Do not depend on hover, animation, tooltip, cursor change, color, sound, or
gesture knowledge as the sole cue. Ensure signifiers survive common themes,
responsive sizes, zoom, forced colors, touch input, and keyboard focus.

### N3 - Conventional form

Use the approved component library's conventional visual grammar. Render
buttons as buttons, links as links, editable values as editable controls, drag
handles as handles, and selection controls with visible state. Preserve semantic
HTML and platform behavior. Do not repurpose a familiar form for a conflicting
action.

### N4 - Honest availability and state

Differentiate enabled, hovered, focused, pressed, selected, checked, expanded,
busy, invalid, read-only, and disabled states wherever applicable. Ensure each
state is perceivable and programmatically exposed. Never make an unavailable
action look enabled. Never make an enabled action visually disappear merely
because it is secondary.

### N5 - Clear mapping

Associate controls with their targets through proximity, containment, alignment,
labeling, and spatial correspondence. Ensure movement direction predicts result
direction. For repeated row or card actions, bind each action visibly and
programmatically to the correct item. Reject remote, ambiguous, or cross-wired
mappings.

### N6 - Guiding constraints

Prevent impossible actions in code and signal the restriction before attempt.
Prefer constrained controls over free text when the domain defines allowable
values. Use progressive disclosure to hide inapplicable actions, but use a
disabled state with explanation when users need to learn that an action exists
but is temporarily unavailable.

### N7 - Immediate and informative feedback

Acknowledge input immediately. Communicate the resulting state, not merely that
"something happened." Keep feedback near the acted-on control or changed
object, preserve it long enough to perceive, and expose it to assistive
technology. For latency, distinguish received, in progress, completed, failed,
and canceled.

### N8 - Coherent conceptual model

Use consistent objects, action verbs, causal relationships, and state models
across the surface and across regenerations. Ensure labels and control grouping
help the user predict outcomes. Reject controls that imply independence when
their effects are coupled or imply a direct effect when the action only creates
a proposal, preview, queue entry, or request.

### N9 - Discoverability without trial and error

Require first-exposure discoverability for core actions. A user should not need
to click arbitrary regions, memorize undocumented gestures, inspect source code,
or cause an error to learn what is possible. Permit learned shortcuts only as
accelerators alongside a discoverable path.

### N10 - Capability-relative affordance

Evaluate possible action relative to the intended user, device, and modality.
Do not call an interaction available when it requires precision, perception, or
input capability the user may not have and no equivalent is provided. Defer the
testable accessibility floor to `accessibility-wcag.skill.md`; treat this rule as
the conceptual requirement that affordance is relational, not an object-only
property.

## Component-class contracts

### Buttons

Generate a semantic button with a visible boundary or other library-approved
button form, an action verb or unambiguous label, sufficient target area, and
distinct enabled, focus, pressed, busy, and disabled states as applicable.
Make its label predict the result: "Save alert," not "OK." On activation,
acknowledge immediately and show the result.

Reject text or an icon styled as a button without button semantics; a button
styled as passive body text; a raised or bordered surface that looks pressable
but has no action; or a label that names an object without clarifying the action.

### Links and navigation

Render navigation as a semantic link with conventional link treatment and text
that identifies the destination or result. Distinguish navigation from command
execution. Do not style a destructive command as a link or a link as a primary
submit button unless the component semantics and user expectation remain clear.

### Editable text and numeric fields

Use a persistent visible label, a recognizable input boundary or editable
surface, an insertion caret on focus, current value, format or unit where
needed, and visible read-only/disabled/invalid state. Keep placeholder text as
an example or hint, never as the sole signifier of editability or the sole label.

For inline editing, provide a persistent cue such as an edit action or
established editable treatment. Do not make static-looking text secretly
editable only on double-click.

### Checkbox, radio, and switch controls

Use checkbox for independent binary selection, radio buttons for one choice in
a visible set, and switch for an immediate on/off setting. Expose the current
state persistently in form, text, and programmatic state. Keep the label's click
target mapped to the control. Do not use a switch for an action that requires a
separate commit without making that two-step model explicit.

### Select, combobox, menu, and disclosure

Signal that more options exist with a conventional indicator and visible focus
state. Distinguish value selection from command menus and content disclosure.
Maintain expected keyboard behavior. Show the chosen value or expanded state
after action. Reject unlabeled chevrons whose target, direction, or effect is
ambiguous.

### Tabs and segmented controls

Render a visible set of peer choices, distinguish the selected item, map each
control to one panel or view, and keep the selected panel spatially associated.
Do not use tab styling for independent buttons or links to unrelated pages.

### Sliders, steppers, and range controls

Show the adjustable dimension, current value, allowed range, direction, and
units. Make direction map naturally to increase/decrease. Provide keyboard and
precise-entry alternatives when a slider alone cannot support exact values.
Reject an unlabeled track or knob whose value and consequence are unknowable.

### Dragging and reordering

Make draggable objects visually distinct from static objects. Provide a visible
handle or another persistent library-approved drag signifier; use an appropriate
cursor only as a supplementary cue. Signal the movable axis, legal drop targets,
and insertion position during the operation. Announce and visibly confirm the
result. Provide a non-drag alternative such as Move Up/Down or a position menu.

Reject drag-only behavior, invisible hit regions, handles that do not drag, the
entire card being draggable when embedded controls create ambiguity, or drop
targets revealed only after an unsuccessful attempt.

### Resizing and splitters

Render a visible grip or divider with sufficient hit area, indicate the permitted
axis, bind movement directly to the affected region, and show live or preview
feedback. Provide keyboard adjustment and reset. Do not use a decorative divider
that resembles a splitter or a functional splitter that resembles decoration.

### Icon-only controls

Use only established icons whose meaning is clear in context. Provide an
accessible name and a hover/focus tooltip, preserve a visible control boundary
when needed, and avoid using the same icon for different actions. Prefer visible
text when interpretation depends on domain knowledge or consequence.

### Charts, canvases, maps, and direct-manipulation surfaces

Render interaction cues at the object of interest: handles, selection outlines,
crosshairs, zoom controls, or labeled modes. Make possible actions discoverable
without requiring exploratory clicking. Provide semantic or structured
alternatives and equivalent controls outside the canvas. Keep feedback attached
to the selected or transformed object.

### Disabled, read-only, hidden, and busy states

Use each state according to its meaning:

- Use **disabled** when an action exists but cannot currently be performed;
  communicate the reason when not obvious.
- Use **read-only** when content can be inspected or selected but not edited;
  preserve its field identity without signaling editability.
- Use **hidden** when the action is irrelevant and its absence will not confuse
  the user about the system model.
- Use **busy** while an accepted action is processing; preserve the action's
  acknowledgement and prevent accidental duplicates without erasing context.

## Component-library enforcement

Maintain an approved component registry. Require each variant to declare:

- semantic primitive and ARIA pattern, if any;
- supported actions and input methods;
- required signifier tokens and minimum visible parts;
- supported states and state-specific tokens;
- mapping and placement rules;
- feedback contract;
- accessibility requirements and equivalents;
- allowed customizations;
- forbidden overrides;
- automated tests and critic exemplars;
- version and conformance status.

Permit the generator to instantiate only approved variants. Reject raw event
handlers on passive elements, unregistered interactive CSS classes, invisible
hit areas, and local overrides that remove required signifiers. If no approved
component matches the action, redesign with existing components or block
generation and request a library addition. Do not bypass the gate with custom
pixels.

Treat theme tokens as constrained inputs. Verify that border, elevation,
underline, caret, handle, focus, selection, and disabled-state tokens remain
perceivable in every supported theme and state. Verify components in context,
because adjacent surfaces can erase an otherwise valid signifier.

## Verification: the Norman conformance gate

Run all stages against the complete rendered interface. Treat every failure as
blocking.

### Stage 1 - Structural and manifest checks

- [ ] **N-AFF-01 Action inventory:** every event handler, gesture, shortcut,
      focus behavior, and agentic action maps to an interaction contract.
- [ ] **N-AFF-02 Reality:** every declared action is implemented in every state
      in which it is presented as available.
- [ ] **N-SIG-01 Coverage:** every user-facing action has a perceivable primary
      signifier; no undocumented gesture-only or hit-region-only action.
- [ ] **N-SIG-02 Honesty:** no passive element uses an approved actionable style
      and no active element uses a prohibited passive style.
- [ ] **N-LIB-01 Provenance:** every interactive instance resolves to an approved
      component-library variant and version; no ad-hoc interactive component.
- [ ] **N-STA-01 States:** required state model is complete and exposed in code;
      visual state and programmatic state agree.
- [ ] **N-MAP-01 Target binding:** every control identifies exactly which object
      or scope it affects.
- [ ] **N-CON-01 Constraints:** invalid operations are prevented; blocked states
      declare a perceivable reason when needed.
- [ ] **N-FBK-01 Feedback:** every action declares acknowledgement, resulting
      state, and completion/error behavior.
- [ ] **N-EQV-01 Equivalence:** every capability-restricted interaction declares
      applicable alternative input paths.

### Stage 2 - Rendered-state and interaction checks

- [ ] Render default, hover, focus, active/pressed, selected/checked, disabled,
      read-only, busy, invalid, success, and error states that apply.
- [ ] Confirm required labels, boundaries, handles, carets, state indicators,
      and focus indicators remain visible in every theme and responsive size.
- [ ] Activate each control through every declared input method and compare the
      actual state transition with the interaction contract.
- [ ] Confirm feedback appears immediately, near the expected locus, persists
      long enough to perceive, and identifies the resulting state.
- [ ] Confirm repeated controls affect only their bound row, card, series,
      object, region, or selection.
- [ ] Confirm drag, resize, slider, and directional controls move in the
      signaled direction and respect the signaled range or axis.
- [ ] Confirm disabled and read-only components do not accept prohibited action
      and do not masquerade as enabled or editable.
- [ ] Confirm no decorative element gains an actionable cursor, focus treatment,
      hover response, or pressed appearance without a real action.
- [ ] Confirm responsive layout and composition do not separate a control from
      its label, target, result, or feedback.

### Stage 3 - AI critic checks

Evaluate the interface from first exposure without reading implementation
metadata. Answer each question for every interactive component:

- [ ] What action appears possible?
- [ ] Where should the action occur?
- [ ] How should the component be operated?
- [ ] What object will be affected?
- [ ] What result should be expected?
- [ ] What is the current state and is action available now?
- [ ] What happened after action and did it satisfy the apparent goal?
- [ ] Does any visual form promise an action the component does not perform?
- [ ] Does any real action remain undiscoverable without trial and error?
- [ ] Does the complete system image support a coherent, non-misleading model?

Fail the component if the critic's inferred action, target, method, or outcome
differs materially from the interaction contract. Do not accept a rationale
that depends on documentation, source inspection, or designer intent.

### Stage 4 - First-exposure task probe

For primary or high-consequence flows, run a short task-based probe with a fresh
critic or user test. Provide only the rendered interface and a realistic goal.
Measure whether the tester selects the correct control, predicts the result,
recognizes state, and interprets feedback without coaching. Treat repeated
misidentification or exploratory clicking as evidence of signifier failure even
when structural checks pass.

## Repair order

Repair failures in this order:

1. Correct or remove the false action.
2. Replace the component with an approved semantic variant.
3. Restore the conventional primary signifier.
4. Correct control-to-object and action-to-result mapping.
5. Add or clarify constraints and state.
6. Add immediate, informative feedback.
7. Clarify the conceptual model through grouping, labels, or progressive
   disclosure.
8. Re-run all stages against the complete surface.

Do not use extra help text as the first repair for a simple control. If a
button, handle, or field needs a paragraph explaining basic operation, replace
the component or its mapping.

## Failure handling

If a required action cannot be represented by a conforming approved component,
do not emit a custom control and do not silently remove the capability. Record
the blocked action and failed rule, surface the conflict in dialogue, and offer
the nearest conforming alternative. Examples include replacing drag-only
reordering with Move Up/Down controls, replacing an ambiguous gesture with
visible commands, or keeping a field read-only until an editable component is
available.

If stakeholder styling requests conflict with a signifier invariant, preserve
the invariant and explain the specific action that would become deceptive or
undiscoverable. If two conventions conflict across platform or culture, use the
target platform's established convention and validate it with a first-exposure
probe.

Treat uncertainty as a signal to test or ask, not as permission to ship. A
component passes only when perceived form, actual action, mapping, constraints,
state, and feedback agree.

## Audit output

When auditing an existing interface, report each violation with:

- rule and gate identifier;
- component and rendered state;
- perceived action inferred from its signifiers;
- actual implemented action;
- affected user goal or capability;
- severity (all false-promise and hidden-action failures are blocking);
- component-library replacement or concrete regeneration fix;
- evidence needed to verify the repair.

End the audit with counts for action contracts examined, blocking failures,
components requiring library changes, and flows requiring first-exposure tests.

## Final invariant

Instantiate no interactive component unless its perceivable signifiers truthfully
communicate a real, available action; its mapping and constraints guide the user
toward the intended operation; its feedback makes the result understandable;
and the complete surface supports a coherent conceptual model. A button must
look pressable and be pressable. A draggable handle must look draggable and
drag the signaled object in the signaled way. An editable field must signal
editability and accept the signaled form of editing. Reject everything else
before it reaches the user.
