---
name: ability-based-personalization
description: >
  Generate, modify, regenerate, or audit a user interface for one user's
  articulated abilities, preferences, devices, tasks, and context, extending
  accessibility beyond WCAG conformance in the tradition of SUPPLE. Use whenever
  a user profile exists; when a user asks for an interface that is easier,
  bigger, simpler, slower, calmer, less cluttered, or step-by-step; when the user
  mentions target size, text, contrast, reading, pace, fatigue, one-handed use,
  input device, motion, memory, attention, gestures, or amount visible at once;
  when regenerating for a changed user, task, device, or situation; or when
  another UI skill needs per-user parameters. Apply together with
  accessibility-wcag: WCAG Level A and AA are the universal floor.
  Personalization may strengthen or reshape the interface above that floor and
  may never waive it.
---

# Ability-Based Personalization for On-Demand UI Generation

## Purpose

Generate for the person who will use the interface, not for an assumed average
user. Treat difficulty as a mismatch among effective abilities, task, device,
environment, and interface - never as a defect in the person.

Make accommodations structural. Select different components, interaction
methods, layouts, labels, timing, and disclosure before instantiation; do not
apply a cosmetic accessibility theme to an otherwise generic interface.

Follow SUPPLE's central move: specify what the interface must enable separately
from how it is rendered, enumerate legal renderings, and choose the rendering
with the lowest expected cost for this user and task. Keep function stable while
changing presentation.

## Non-negotiable rules

1. **Keep WCAG as the floor.** Load `accessibility-wcag` for every generated UI.
   Never trade away semantics, keyboard access, alternatives, focus, contrast,
   error identification, or another A/AA requirement.
2. **Personalize from needs, not diagnoses.** Ask what helps or hinders
   interaction. Do not infer impairment from age, appearance, writing style,
   behavior, device, or demographics.
3. **Separate preference from performance.** Preserve stated preferences and
   observed or measured performance as distinct evidence. Never describe an
   articulated preference as a measured ability.
4. **Optimize effective use.** Reduce expected effort, time, error, visual
   search, memory demand, fatigue, and unnecessary navigation for this person.
5. **Preserve agency and function.** Make accommodations inspectable,
   adjustable, and reversible. Simplify presentation without silently deleting
   capability.
6. **Preserve stability.** Penalize unnecessary changes from the familiar
   rendering. Explain material changes and preserve work, focus, and history.
7. **Personalize the whole pipeline.** Modify components, manipulation,
   information architecture, language, timing, feedback, help, and other skill
   parameters - not only color and type.
8. **Minimize sensitive data.** Retain only consented, task-relevant profile
   facts with provenance, scope, and a removal path.

## Application workflow

1. Load the task model, device/context model, prior rendering, applicable HCI
   skills, and the WCAG gate.
2. Resolve the active profile. If no profile exists, use neutral WCAG-compliant
   parameters and treat the first articulated need as a profile update; never
   block generation waiting for a profile.
3. Translate the profile into parameters and hard constraints before selecting
   components. Generate several functionally equivalent candidates when choices
   materially differ.
4. Reject every candidate that violates WCAG, safety, device limits, essential
   functionality, or an explicit required accommodation.
5. Compare remaining candidates against expected task trails and the active
   profile. Choose the lowest-cost legal rendering, not automatically the most
   conventional or attractive.
6. Run the Screen Budget Tradeoff when dimensions compete.
7. Verify the full personalized surface, emit the personalization manifest, and
   preserve the profile as a plan against the task model.
8. Explain a personalization using its parameter and dialogue provenance in the
   user's terms, never clinical language.

## SUPPLE-derived generation model

Represent generation with:

- `F`: functional task specification - goals, data, actions, constraints, and
  semantic groupings describing what the UI must support;
- `D`: device/context model - viewport, components, modalities, environment,
  and platform limits;
- `P`: user profile - articulated requirements, preferences, ability-related
  parameters, expertise, and accommodation priorities;
- `T`: anticipated or consented task/usage trails, frequencies, transitions,
  criticality, and current task;
- `R_prev`: prior familiar rendering, if any;
- `R`: candidate assignment of components, layout, manipulation, size, language,
  timing, and disclosure to `F`.

Choose conceptually:

```text
R* = argmin R in Legal(F, D, hard_constraints(P))
     Cost(R | P, T, R_prev)
```

Use this as a design discipline when no formal solver exists: search, rank,
critique, and regenerate candidates. Never let a low weighted cost compensate
for a hard-constraint failure.

Include weighted terms for target acquisition, manipulation, navigation,
reading, visual search, memory, timing, error likelihood, fatigue, preference,
and dissimilarity from `R_prev`. Weight current, frequent, consequential, and
safety-critical tasks appropriately. Smooth sparse usage so unfamiliar but
necessary functions do not disappear.

## Build the user profile

### Evidence model

- **Articulated - primary:** Apply direct statements about what is easier,
  harder, preferred, or unavailable. Capture the requirement and the user's
  words.
- **Observed - proposal only:** Use repeated mis-hits, undo, abandonment,
  re-explanation, or difficult transitions only when collection is available and
  consented. Propose a change, identify the observation, and request confirmation
  before making it persistent.
- **Measured - objective when valid:** Use performance measurements only when a
  disclosed, appropriate instrument produced them. Record the method and scope.
  Do not label ordinary dialogue or trace inference as measurement.
- **Inferred - confirm first:** Infer only a task/device implication directly
  entailed by current context, such as touch lacking hover. Confirm any
  person-specific inference before storing or applying it beyond the moment.

Preference and performance may disagree. Measured performance can inform a
recommendation, but the user remains the authority on the interface.

### Profile entry contract

Record each entry with `dimension`, `need`, `parameter`, `value`, `strength`
(`required`, `preferred`, or `exploratory`), `scope`, `source`, `provenance`,
`confidence`, `volatility`, `consent`, and `review`. Scope entries to a control,
workflow, device/context, session, or persistent profile. Never silently promote
an exploratory or situational entry to a persistent requirement.

Use this canonical parameter vocabulary when applicable:

```yaml
profile:
  pointer:
    min_target_css_px: 24       # WCAG floor; raise from user need/preset
    target_spacing: default     # default | increased | isolated
    dragging: available         # available | avoid | unavailable
    multi_click: available      # available | avoid | unavailable
    hover: available            # available | unavailable
    precision: typical          # typical | reduced | low
  vision:
    type_scale: 1.0
    contrast_text: 4.5          # actual WCAG floor may vary by text size
    contrast_nontext: 3.0
    visual_cue_scale: 1.0
    color_channel: redundant    # never color-only
  input:
    primary: unspecified        # mouse | touch | keyboard | switch | eye | voice
    keyboard_only: false
    one_handed: false
  timing:
    dwell_ms: null              # require user value or adjustable preset
    interaction_pace: typical   # typical | extended | untimed
    motion: system              # system | reduced | none
  cognition_language:
    surface_budget: typical     # typical | reduced | minimal
    disclosure: contextual      # single_view | progressive | step_by_step
    language_register: domain   # domain | plain | plain_short
    instruction_chunk: typical  # typical | short | one_at_a_time
  context:
    volatility: stable          # stable | session | fluctuating
    situational: []
    never_adapt: []
```

Treat 44 px enlarged and 56 px extra-large targets, 7:1 enhanced text contrast,
and similar values as adjustable implementation presets, not as SUPPLE findings
or universally correct values. Prefer the user's value, preview, or measured
need. Re-check fluctuating entries with one low-cost question at the relevant
session or context boundary.

## Generate accommodations

### Targets and reach

**Generate:** Apply `min_target_css_px` to the complete hit region of every
pointer target, including list rows, tabs, handles, chart marks, row actions,
and close controls. Measure the smaller dimension. Increase spacing, reduce
frequent pointer travel, and place related actions near their objects while
preserving semantic and focus order. Under one-handed or reduced reach, avoid
simultaneous inputs and place primary actions in the articulated reachable
region.

**Reject:** undersized hit regions; enlarged icons with small hit boxes;
crowded adjacent targets; nested targets whose activation areas conflict.

### Gestures and manipulation

**Generate:** When dragging, multiple clicking, hover, precision movement, or
simultaneous input is unavailable or difficult, choose a lower-cost equivalent:
move-up/down or position selector; numeric range inputs; preset sizes; select
then place; larger lists or radio groups; steppers; keyboard, voice, or switch
operation. Retain another method when the chosen technique may fail.

**Reject:** any capability reachable only through an excluded gesture;
drag-only reordering; hover-only information; timing-sensitive operation for a
profile that excludes it. Remove a false signifier for an unavailable action,
but retain an optional drag path when the user can use it and an equivalent
alternative exists.

### Dwell, timing, and motion

**Generate:** Use dwell only when requested or required by the input modality.
Use the user's duration or offer adjustable presets with visible progress,
departure-to-cancel, repeat suppression, pause/lock, and undo. Remove
nonessential time limits and auto-advance. For essential external, security,
safety, or real-time limits, preserve correctness while offering pause,
extension, warning, recovery, or an untimed alternative where possible. Keep
recovery paths persistent and preserve input. Respect reduced motion.

**Reject:** countdown-bound destructive action; disappearing-only undo;
automatic advancement contrary to the profile; indiscriminate multiplication
of a deadline whose semantics cannot change.

### Contrast, visual cues, and type

**Generate:** Start with actual WCAG-compliant tokens. Raise text and non-text
contrast separately to profile values; use 7:1 normal text and 4.5:1 large text
as enhanced presets only when appropriate. Scale the complete type ramp and
important visual cues, including labels, tables, axes, legends, badges, helper
text, errors, icons, focus, and chart marks. Pair color with text, shape,
pattern, or position. Reflow after personalization, not only before it.

**Reject:** unscaled chrome around scaled body text; clipped fixed-height text;
color-only information; charts or controls unreadable at the active scale;
one contrast number incorrectly applied to every content category.

### Simplified layout and reduced surface

**Generate:** Preserve `F`, then show the minimum sufficient surface for the
current sub-goal. Prioritize current, frequent, and consequential actions;
flatten grouping depth; reduce distinct interaction patterns; use one dominant
task path and stable locations. Put secondary capability behind one clearly
labeled expansion point. Duplicate frequently used but hard-to-reach functions
into a stable "Common actions" area without deleting their familiar path.

**Reject:** capability silently dropped; a simple view with no discoverable
full path; hidden safety state, undo, status, help, or required errors;
decorative chrome surviving a minimal surface budget.

### Plain language and recognition

**Generate:** Use the user's vocabulary and expertise. Prefer concrete
verb-object labels, expand uncommon abbreviations, pair uncertain icons with
text, keep one idea per sentence, and place examples and instructions at the
point of action. Apply the register to labels, errors, confirmations, help, and
provenance. Preserve precise domain terms the user uses.

**Reject:** generator jargon; ambiguous icon-only actions; reading-level edits
that change consequential meaning; simplification that erases the user's domain
language; visible-label/accessibility-name mismatch.

### Progressive and step-by-step disclosure

**Generate:** Under `step_by_step`, present one coherent decision or small group
per step with progress, prior choices, next-step expectation, Back, Cancel,
Save-and-resume, and Review. Carry known values forward. Under `progressive`,
keep one view and reveal secondary surfaces on demand. Under `single_view`, do
not fragment a task the user can efficiently complete at once.

**Reject:** wizard without progress or Back; repeated data entry; discarded
state; step-by-step imposed on a one-decision task; hidden current-subgoal
controls.

## Screen Budget Tradeoff

When larger targets, larger type, visual cues, and a reduced surface compete for
available space, resolve in this order:

1. Preserve safety, correctness, and every WCAG A/AA requirement.
2. Preserve explicit required accommodations and essential capability.
3. Remove decorative and unjustified surface.
4. Disclose secondary, infrequent functions while keeping them discoverable.
5. Flatten, stack, paginate, or add a step before shrinking targets or text.
6. Compact only rare elements and never below their active profile floor.
7. Minimize deviation from familiar terminology, position, grouping, and
   manipulation.
8. If no legal rendering remains, name the competing parameters, show concrete
   alternatives and tradeoffs, let the user choose, and record the decision.

Never quietly lower a value the user articulated. Extra navigation may be the
better cost than inaccurate manipulation, but simulate the user's frequent task
trail before choosing it.

## Modify other HCI skills

| Skill | Personalized application |
| --- | --- |
| `accessibility-wcag` | Keep A/AA invariant; raise targets, contrast, type, timing, motion, and alternatives above the floor. |
| `heuristics-nielsen` | Strengthen recognition and minimalism; adapt accelerators to expertise/input; preserve cross-generation consistency. |
| `affordances-norman` | Amplify signifiers in perceivable channels; remove false promises for unavailable actions. |
| `cognitive-load-progressive-disclosure` | Set simultaneous choices, chunk size, help density, surface budget, and sequence from the profile. |
| `direct-manipulation` | Preserve visible objects and reversibility; supply lower-effort discrete alternatives to precision gestures. |
| `mixed-initiative` | Adjust pacing and confirmation; surface uncertainty; prefer suggestion when predictability or time is needed. |

Resolve remaining cross-skill conflicts by: (1) safety, law, correctness; (2)
WCAG/platform invariants; (3) explicit required accommodations; (4) device and
environment; (5) function and recoverability; (6) expected performance and
error reduction; (7) stability; (8) aesthetic preference. Ask only when the
choice materially changes the outcome.

## Persistence, adaptation, and dignity

- Persist the profile and customization plan against `F`, not pixels or emitted
  markup. Re-evaluate device-specific sizes instead of copying pixel values.
- Preserve form values, selection, focus, scroll context, undo, and history on
  regeneration. A profile change authorizes only changes it requires.
- Balance optimization against familiarity using a dissimilarity penalty to
  `R_prev`. Explain necessary relocation and offer a stable alternative.
- Do not covertly rearrange the main interface from behavior. Preview a
  system-suggested change or copy promoted functionality into an explainable,
  pinnable, removable "Common actions" region. Do not move the original based
  on a single observation.
- Keep every customization reversible, including out of order when dependencies
  permit. Identify dependent changes before removing a prerequisite.
- Do not infer, unnecessarily retain, or expose a condition or diagnosis when an
  interaction requirement is sufficient. Use condition-related language only
  when the user explicitly chooses it and it is relevant.
- Do not stigmatize the surface as a lesser or special interface. Label modes or
  regions only when the distinction helps the user, using neutral task language.
- Let the user inspect, correct, scope, export where appropriate, or delete the
  profile. Honor `never_adapt`; a rejected proposal stays rejected.

## Verification gate

Run both stages over the complete interface before instantiation and after every
regeneration. Block emission on any hard-constraint failure.

### Stage 1 - structural and machine-checkable

- [ ] Pass the complete `accessibility-wcag` A/AA gate at personalized values.
- [ ] Trace every accommodation to an entry/default with provenance, consent,
      scope, strength, and reversal path.
- [ ] Confirm every essential capability remains reachable and discoverable.
- [ ] Measure targets on their smaller dimension and verify spacing at all
      states and responsive breakpoints.
- [ ] Verify visual cues, type ramp, text/non-text contrast, reflow, zoom, and
      spacing after profile scaling; confirm no clipping or overlap.
- [ ] Verify zero excluded-gesture-only, hover-only, repeated-click-only,
      simultaneous-input-only, or time-pressure-only task paths.
- [ ] Verify dwell, timeouts, warnings, auto-advance, notification persistence,
      recovery, and motion against the profile and task semantics.
- [ ] Verify progressive steps preserve state and provide Back, Cancel, Review,
      and resume where applicable.
- [ ] Verify reduced surface drops no capability and hides no current or
      safety-critical information.
- [ ] Compare with `R_prev`; flag unrequested terminology, position, grouping,
      visibility, or manipulation changes.
- [ ] Verify semantics and accessible names survive visual substitution.
- [ ] Verify usage/profile collection is consented, minimal, and free of hidden
      diagnoses or demographic inference.

### Stage 2 - critic and user-centered

- [ ] Simulate common and consequential task trails; compare candidates for
      manipulation, navigation, reading, memory, timing, fatigue, and error cost.
- [ ] Confirm each accommodation addresses the articulated difficulty instead
      of merely looking accessible.
- [ ] Confirm lower-effort substitutes are functionally equivalent and not
      disproportionately burdensome.
- [ ] Confirm language is concrete, consistent, accurate, and aligned with the
      user's vocabulary and expertise.
- [ ] Confirm enlargement and stronger cues did not produce a denser or more
      confusing surface.
- [ ] Confirm progressive disclosure hides the right functions and preserves
      the frequent path.
- [ ] Confirm adaptation is predictable, explainable, reversible, and free of
      stigmatizing labels.
- [ ] Preview or ask when evidence is uncertain or legal candidates have
      materially different tradeoffs.

### Personalization manifest

Attach an inspectable manifest to the artifact or task model:

```yaml
profile_basis:
  - need: "Small controls are difficult to hit"
    source: articulated
    scope: this_device
    provenance: dialogue_turn
accommodations:
  - parameter: pointer.min_target_css_px
    value: 56
    affects: [buttons, list_rows, handles, row_actions]
    reversible: true
preserved: [wcag_2_2_aa, essential_functionality, undo]
tradeoffs: ["More vertical scrolling for larger targets"]
verification: passed
```

Keep it user-readable and omit diagnoses, hidden inferences, and irrelevant
sensitive data.

## Audit and failure handling

For an audit, load the profile and task model, run WCAG first, map task-critical
components to exercised profile dimensions, and report each mismatch with task,
evidence, component, proposed alternative, benefit, tradeoff, and priority. Do
not edit on an audit-only request. Describe a mismatch in interface terms, not
as a user's inability.

If no legal rendering satisfies the profile and hard constraints, do not relax
WCAG, silently lower a parameter, or drop function. Identify the exact conflict,
retain the safest accessible version, and offer concrete alternatives. If an
upstream library cannot express the accommodation, reject that component,
choose a conforming alternative, and record the gap.

If profile evidence conflicts, believe neither automatically: disclose the
evidence, propose the change, and let the user decide. Uncertainty about whether
a dimension applies is a reason to ask; uncertainty about a diagnosis is not.

## Evidence boundaries

Ground the functional-specification/rendering separation, device and usage
models, constrained optimization, target and visual-cue parameters, alternative
widget selection, consistency penalty, customization plan, adaptive-area
pattern, and measured motor-performance findings in:

Krzysztof Z. Gajos, Daniel S. Weld, and Jacob O. Wobbrock. 2010.
"Automatically generating personalized user interfaces with Supple."
*Artificial Intelligence* 174, 12-13, 910-950.
https://doi.org/10.1016/j.artint.2010.05.005

Represent the evidence accurately. SUPPLE evaluated 11 motor-impaired and 6
able-bodied participants. Its factored preference cost produced results in
under a second in most tested cases; its expected-speed ability cost required
3.6 seconds to 20.6 minutes. Related CHI 2008 reporting found motor-impaired
participants averaged 26.4% faster and 73% fewer errors with ability-based
interfaces than baselines. Do not generalize motor findings as validation of
every cognitive, language, visual, or timing rule.

Treat plain language, reduced surface, broader timing, amplified contrast,
step-by-step disclosure, and other extensions as applications of SUPPLE's
person-specific optimization tradition to the on-demand paradigm in Nathan
Conklin, Miranda Capra, and Chris North, "Automating the Application of HCI
Principles: Skills for On-Demand UI Construction, the Human-AI Space to Think,
and the Future of HCI" (2026). Cite SUPPLE for the optimization and ability
model lineage; cite the on-demand framework and articulated profile for the
broader accommodation set.
