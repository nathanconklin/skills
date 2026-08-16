---
name: cognitive-load-progressive-disclosure
description: >
  Enforce a minimum sufficient surface policy for user interfaces generated,
  modified, extended, regenerated, or audited from dialogue. Use whenever
  building dashboards, forms, workspaces, panels, tables, charts, menus,
  configuration flows, agent controls, or other interactive artifacts whose
  visible capabilities should grow only as the user's articulated task entails
  them. Also use when simplifying a crowded interface, deciding whether a
  control belongs now or later, staging novice-to-advanced functionality,
  preventing irrelevant or error-producing paths, preserving cognitive
  capacity for the current task, or auditing component-to-dialogue provenance.
  Apply with accessibility-wcag as the universal floor and with
  ability-based-personalization whenever a user profile exists.
---

# Minimum Sufficient Surface

## Purpose

Construct the smallest interface surface that is sufficient for the user's
current articulated task. Treat progressive disclosure as a runtime property
of the dialogue and task model, not as a static split between "basic" and
"advanced" product editions.

Enforce this invariant:

> Expose only the affordances the dialogue has so far justified. Introduce a
> new capability at the first dialogue turn where the user's articulated need
> entails it.

Do not interpret "minimum" as the fewest pixels, controls, or DOM nodes.
Minimize the number of concepts, decisions, actions, and state transitions the
user must consider while preserving task completion, comprehension,
accessibility, safety, feedback, and recovery.

Apply the policy inline during generation. Reject unjustified affordances
before instantiation rather than shipping a crowded interface and hiding parts
afterward.

## Research Translation and Limits

Use the three research foundations for different purposes:

| Foundation | Operational contribution | Do not overclaim |
| --- | --- | --- |
| Sweller (1988) | Preserve limited cognitive-processing capacity by removing concurrent information, choices, search, and coordination work that do not contribute to the current task. Treat every additional choice point and item that must be held in working memory as a cost. | The paper studies learning during problem solving, especially means-ends analysis. It does not propose a user-interface disclosure rule or prove that fewer visible controls always improve performance. |
| Carroll and Carrithers (1984) | Begin with functional capability for real work; make known irrelevant and troublesome error paths unreachable; stage the presentation of function; keep the path into the fuller system coherent. | The evidence comes from a small study of novice users learning a historical word processor. Generalize the mechanism cautiously, not its exact interface or participant results. |
| Shneiderman (2003) | Organize capability into comprehensible layers; start with a limited functional layer; let users move to higher layers when their needs require them; preserve predictability and user control. | The paper is an architectural proposal that calls for further design and longitudinal testing. It does not justify opaque, usage-based adaptation or a universal number of layers. |

- Derive the cognitive-cost test from Sweller's account of simultaneously
  coordinating problem state, goal state, operators, and subgoals.
- Treat Carroll and Carrithers' 12-person experiment as evidence of mechanism:
  training-wheels users reached useful work 48% faster, spent less time on the
  blocked-error paths, and performed better on the comprehension post-test.
- Preserve Shneiderman's emphasis on user-controlled progression; do not copy
  the unpredictable adaptive-menu behavior his paper criticizes.

The minimum-sufficient-surface policy is an operational synthesis for
dialogue-generated interfaces. Its strongest classical empirical support is
the training-wheels result; its cognitive rationale comes from Sweller; its
layering model comes from Shneiderman. Preserve that distinction when
explaining or citing the policy.

## Operational Model

Maintain these structures for every generation:

### Dialogue-grounded task model

Record:

- the user's active goal and subgoals;
- facts, entities, constraints, preferences, and ability-related needs the user
  has articulated;
- the current task phase and valid state transitions;
- required information and actions for completing the active goal;
- unresolved ambiguity, risk, and missing prerequisites;
- prior surface state, current focus, user-entered data, and undo history;
- a provenance link from each requirement to the dialogue turn or standing
  user-authored preference that established it.

Do not infer a broad feature need merely from available data, product
convention, component-library defaults, analytics, or assumed expertise.

### Affordance inventory

Treat an affordance as one user-perceivable opportunity for action, not merely
as a component container. Inventory each distinct action, input, view,
expansion point, navigation choice, status region, and recovery path.

For every candidate affordance, record:

```yaml
affordance_id: stable-id
label: user-visible name
capability: what the user can perceive or do
justification_type: explicit | entailed | invariant | state-recovery
provenance: dialogue turn, articulated profile constraint, or governing skill
active_goal: goal or subgoal served
first_entailed_turn: earliest turn at which the need required this capability
prerequisites: states or data required before enablement
disclosure_state: omitted | visible | visible-disabled | expanded
removal_condition: condition under which the justification expires
state_at_risk: user work or system state that removal could affect
```

Assign provenance at affordance granularity. A justified "Settings" panel does
not automatically justify every control inside it.

### Justification classes

Accept only these classes:

1. **Explicit** - The user directly requested the capability, information, or
   degree of control. A standing preference counts only if the user articulated
   it and it applies to the present task.
2. **Entailed** - The capability is a necessary means, prerequisite, or decision
   input for completing an active user goal. Explain the entailment in one
   sentence without appealing to convention.
3. **Invariant** - Another governing requirement makes the affordance necessary,
   such as accessibility, safety, privacy, system-status visibility,
   confirmation, cancellation, or undo. Cite the governing requirement.
4. **State-recovery** - The affordance is necessary to preserve, inspect,
   correct, retry, reverse, or safely leave the current state.

Reject these as insufficient by themselves:

- "Users usually want this."
- "This is standard in dashboards."
- "The component library includes it."
- "The user might need it later."
- "Experts expect all options to be visible."
- "The data is available."
- "Usage history predicts interest."
- "It makes the interface look complete."

## Formal Policy

At dialogue turn `t`, let `C_t` be the set of candidate affordances. An
affordance is eligible only when it has an active accepted justification.

Construct `S_t`, the visible surface at turn `t`, as the smallest subset of
eligible affordances that satisfies all of these conditions:

1. The active task remains completable or can advance to the next honest point
   of clarification.
2. Required decision context is visible at the point of decision.
3. Current system state and the result of user actions remain perceivable.
4. Accessibility, safety, privacy, confirmation, cancellation, and recovery
   obligations remain satisfied.
5. Active user work, focus, spatial memory, and undo history are preserved.
6. No enabled action leads only to an invalid, irrelevant, or unrecoverable
   state.

For a new affordance `a`, define its appearance turn as:

```text
first_entailed_turn(a) = earliest t where an accepted justification for a is active
```

Emit `a` in the generation produced for that turn. Do not expose it earlier as
a teaser, and do not delay it until the user fails without it.

If several candidate sets satisfy the conditions, prefer the set that:

1. requires fewer simultaneous decisions;
2. requires less information to be remembered across views;
3. introduces fewer new concepts or interaction patterns;
4. preserves more of the already-learned surface;
5. provides the shortest safe path to the user's next meaningful outcome.

Do not use unsupported magic limits such as "seven items" or "five menu
choices." Compare cognitive demands in context.

## Generation Workflow

### 1. Resolve the current need

Translate the latest dialogue into an active goal, required outcome, current
phase, and known constraints. Distinguish:

- what the user asked to accomplish;
- what information the user needs now;
- what actions must be possible now;
- what may become relevant later;
- what is still ambiguous.

Ask a focused question instead of emitting several speculative branches when
the ambiguity would materially change the surface.

### 2. Enumerate candidate affordances

Start from task requirements, not from a complete application template.
Include the minimum components needed for content, action, status,
accessibility, safety, and recovery. Keep customary extras in the candidate
list but do not surface them without accepted justification.

### 3. Run the entailment test

For each candidate, answer:

1. Which active user goal does this affordance serve?
2. What exact dialogue turn, articulated profile constraint, or governing
   invariant justifies it?
3. Would removing it make the current task impossible, unsafe,
   inaccessible, opaque, or needlessly dependent on memory?
4. Is it needed now, or only under a future condition?
5. Does a lower-load representation provide the same necessary capability?

Omit the candidate if questions 1 or 2 lack a concrete answer. Defer it if it
is justified only by a future condition. Replace it if a lower-load equivalent
meets the same need.

### 4. Block irrelevant and error-producing paths

Use the training-wheels mechanism selectively:

- Do not instantiate actions that are irrelevant to the active task.
- Prevent entry into states known to be invalid or unrelated.
- Preserve a real path to useful work; never reduce the interface to a passive
  tutorial.
- Give immediate, task-specific guidance when the user attempts an unavailable
  action through dialogue or another route.
- Prefer constrained inputs, safe defaults, and valid next actions over error
  messages after the fact.
- Keep the component vocabulary and interaction patterns compatible with later
  layers so learning transfers as the surface grows.

Do not permanently remove capability from the system. Omission from the
current surface means "not yet justified here," not "forbidden forever."

### 5. Choose the disclosure state

Apply this order:

| Condition | State | Rule |
| --- | --- | --- |
| No active accepted justification | Omitted | Do not render, focus, announce, or reserve empty space for it. |
| Justified now and actionable | Visible | Place it at the point of need with an unambiguous label. |
| Justified now but temporarily unavailable | Visible-disabled only when explanatory value is necessary | State the unmet prerequisite and provide the valid next step. Otherwise omit until actionable. |
| Justified secondary detail within the current task | Signposted disclosure | Use a local expansion, details region, drill-down, or next step whose label predicts the content. |
| User explicitly requests the full in-scope set | Expanded | Reveal the requested layer while retaining grouping, hierarchy, and accessibility. Do not add unrelated domains. |

Never use disabled controls as advertisements for unrequested features.
Hidden or collapsed content must not remain keyboard-focusable or be announced
as currently available by assistive technology.

### 6. Select a disclosure pattern

Match the mechanism to the task:

- Use **summary then detail** when the user needs an overview before evidence.
- Use **details on demand** when several items share optional depth.
- Use **stepwise disclosure** when later inputs depend on earlier choices.
- Use **contextual expansion** for secondary configuration attached to one
  visible object.
- Use **mode or layer change** only when the user requests or needs a coherent
  cluster of capabilities.
- Use **dialogue-driven addition** when a newly articulated goal requires a new
  view or control.
- Use **safe state gating** when an action becomes valid only after a
  prerequisite state.

Avoid nested disclosure chains that force the user to remember where content
was hidden. Avoid surprise movement, automatic menu reorganization, and
machine-initiated layer changes based only on observed behavior.

### 7. Generate and announce change

When the dialogue first entails a capability:

- add it in the same response or regeneration;
- place it near the object or step it serves;
- preserve positions and labels of unrelated existing controls;
- preserve focus or move it intentionally to the newly relevant region;
- announce the addition concisely when it may not be visually obvious;
- attach a "Why this exists" provenance explanation when the host interface
  supports it.

Do not celebrate or narrate every tiny surface change. Announce only enough to
maintain orientation and predictability.

### 8. Reconcile the surface on every turn

Recompute justifications after each material dialogue update.

- Keep an affordance while any active justification remains.
- Remove or collapse an affordance when its last justification expires and no
  active task state depends on it.
- Ask before removal when it would discard user-entered data, configuration,
  results, annotations, or a learned workflow the user is actively using.
- Prefer archival collapse or reversible removal when provenance or prior work
  remains useful.
- Never accumulate controls merely because they appeared in an earlier
  generation.
- Never reshuffle unaffected regions during decluttering.

## Layer Architecture

Use semantic layers rather than fixed expertise levels:

1. **Current work layer** - objects, information, and actions necessary for the
   active goal now.
2. **Task-support layer** - secondary details, configuration, comparison, or
   explanation already justified by the active goal.
3. **Extended task layer** - additional in-scope capabilities first justified
   by a newly articulated subgoal or explicit request for broader control.
4. **System repertoire** - capabilities the system could provide but that have
   no current surface entitlement.

Keep layers non-destructive and user-controlled. A user may remain indefinitely
with a small surface, jump directly to a higher in-scope layer, or ask to return
to a simpler surface. Do not equate layer with intelligence, competence,
seniority, age, or disability.

## Non-Negotiable Visibility

Do not hide or defer information merely to make the surface look sparse. Keep
these visible when applicable:

- the primary content or action required for the current goal;
- information needed to make the current decision;
- current mode, selection, scope, filters affecting the visible result, and
  data freshness;
- errors, warnings, uncertainty, constraints, and material consequences;
- progress for active operations;
- cancel, back, undo, retry, or recovery when the current state requires them;
- accessible names, instructions, alternatives, focus, and status semantics;
- user-authored data that would otherwise be lost or become misleading.

Progressive disclosure must not become progressive concealment. Never bury a
primary action, a safety-critical warning, or information required to interpret
the current result behind "More."

## Composition with Other Skills

Apply these precedence rules:

1. Treat `accessibility-wcag` Level A/AA constraints as a universal floor.
   Accessibility-required alternatives and controls have invariant
   justification; do not remove them as clutter.
2. Apply `ability-based-personalization` above that floor. A user's articulated
   profile may strengthen staging, reduce simultaneous content, simplify
   gestures, or slow transitions. Never infer disability or ability from
   interaction behavior alone.
3. Apply `heuristics-nielsen` jointly. Its minimalist-design rule aligns with
   this skill. When a generic heuristic suggests common dashboard features
   such as filter, sort, or alternate views, expose them only when the active
   task or an explicit request justifies them.
4. Apply `affordances-norman` to every visible control. This skill decides
   whether a control belongs on the current surface; the affordance skill
   decides whether its perceived form truthfully signals its action.
5. Apply `mixed-initiative` without silent surface growth. Offer speculative
   capabilities conversationally or as reversible proposals; instantiate them
   only after an accepted justification exists.
6. Apply `direct-manipulation` only to justified objects and actions. Any
   accessibility-required non-drag alternative inherits invariant
   justification.

Where two requirements truly conflict, preserve accessibility, safety,
correctness, user data, and recovery before minimizing the surface. Record the
reason for the additional affordance.

## Examples

### Business performance interface

Dialogue: "Show me how the business is performing."

Generate a concise performance overview with the measures necessary to answer
that question, visible scope/time period, freshness, and an accessible path to
supporting detail. Do not add alert builders, exports, forecasting controls,
scenario modeling, or administrative settings.

Later dialogue: "Alert me if operating margin falls below 12%."

Add the alert condition, delivery choice if required, review/confirmation, and
undo only now. Link each new affordance to this turn.

### Data table

Dialogue: "List the open findings assigned to my team."

Show the open findings, assignment context, and status needed to interpret the
list. Add search or sorting only if required by the result size or articulated
task; add bulk reassignment only after the user asks to change ownership.

### Cyber investigation workspace

Dialogue: "Help me investigate alert 174."

Show alert context, evidence, provenance, uncertainty, and investigation
actions. Do not expose containment or destructive response controls unless the
user asks to act or a governing safety process requires a visible escalation
path. If containment becomes justified, add confirmation, consequence preview,
audit trail, and recovery at the same time.

### Audit finding

An "Export PDF" button exists because the library's dashboard template always
includes it, but no dialogue turn or invariant requires export. Mark it
`prematurely_exposed` and remove it. Do not relabel it as justified by
convention.

## Verification Gate

Run both stages over the complete surface before instantiation and after every
material regeneration. A failed blocking check requires revision.

### Stage 1: Structural checks

- [ ] Every visible affordance has exactly one or more active accepted
      justifications and resolvable provenance.
- [ ] Provenance coverage is 100%; orphaned visible affordances equal zero.
- [ ] Prematurely exposed affordances equal zero.
- [ ] Missing affordances whose need is already entailed equal zero.
- [ ] Every nested action inside a justified container has its own
      justification.
- [ ] Every enabled action has at least one valid next state.
- [ ] Every invalid or irrelevant state transition is unreachable from the
      current surface.
- [ ] Every visible-disabled control is already justified, names its unmet
      prerequisite, and exposes the valid next step.
- [ ] Omitted or collapsed content is absent from focus order and the active
      accessibility tree.
- [ ] Current task, decision context, system status, accessibility, safety,
      confirmation, cancellation, and recovery requirements remain reachable.
- [ ] Every newly added affordance appears no earlier and no later than its
      `first_entailed_turn`.
- [ ] Regeneration preserves unrelated positions, labels, focus, input, and
      undo state.
- [ ] Expired affordances with user data or consequential state are not removed
      without preservation or confirmation.

### Stage 2: Cognitive and interaction critic

- [ ] A first-time user can identify the primary current task and next action
      without scanning unrelated capability.
- [ ] Each visible item competes for attention only because it contributes to
      the active task, comprehension, safety, accessibility, or recovery.
- [ ] Required information is colocated with the decision that uses it; the
      interface does not create avoidable cross-view memory demands.
- [ ] Disclosure labels accurately predict what will appear.
- [ ] The interface remains functional rather than becoming a passive tutorial
      or an artificially crippled demonstration.
- [ ] The layering is predictable and user-controlled; no behavior-only
      adaptation silently changes menus or modes.
- [ ] The surface is minimal in semantic demand, not merely visually sparse.
- [ ] The removal of any further item would make the active experience less
      complete, safe, accessible, comprehensible, or recoverable.

## Audit Output

When auditing an existing interface, report each finding with:

| Field | Required content |
| --- | --- |
| Component or affordance | Stable identifier and visible label |
| Classification | justified, prematurely exposed, missing, stale, improperly disabled, or over-disclosed |
| Provenance | Dialogue turn, articulated profile constraint, governing invariant, or none |
| Cognitive cost | Extra concept, choice, memory dependency, search, mode, or error path introduced |
| User impact | Effect on task completion, learning, safety, accessibility, or orientation |
| Regeneration action | Keep, add now, omit, collapse, gate, relocate, preserve, or ask |
| Confidence | High, medium, or low, with ambiguity stated |

Do not claim a direct measurement of human cognitive load from component count
alone. Describe observable proxies and recommend user testing when the decision
depends on actual cognitive performance.

## Failure Handling

If the surface cannot be made both sufficient and minimal:

1. Preserve accessibility, safety, correctness, transparency, user data, and
   recovery.
2. Identify the exact conflicting requirements.
3. Ask the user to resolve a material ambiguity or preference when necessary.
4. Offer the smallest safe alternatives and explain their surface tradeoffs.
5. Record the chosen exception and its provenance.
6. Re-run the full verification gate.

Do not silently remove a necessary capability. Do not silently add speculative
capability to avoid asking a question.

## Sources

- Sweller, J. (1988). Cognitive Load During Problem Solving: Effects on
  Learning. *Cognitive Science, 12*(2), 257-285.
  https://doi.org/10.1207/s15516709cog1202_4
- Carroll, J. M., & Carrithers, C. (1984). Training Wheels in a User
  Interface. *Communications of the ACM, 27*(8), 800-806.
  https://doi.org/10.1145/358198.358218
- Shneiderman, B. (2003). Promoting Universal Usability with Multi-Layer
  Interface Design. *Proceedings of the 2003 Conference on Universal
  Usability*, 1-8. https://doi.org/10.1145/957205.957206
- Conklin, N., Capra, M., & North, C. (2026). Automating the Application of HCI
  Principles: Skills for On-Demand UI Construction, the Human-AI Space to
  Think, and the Future of HCI. *FutureHCI '26*.
