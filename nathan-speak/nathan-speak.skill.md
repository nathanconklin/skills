---
name: nathan-speak
description: Write and edit prose in Nathan Conklin's preferred style. Use this skill whenever drafting, editing, or reviewing any prose for Nathan, including emails, government proposals, scientific and technical papers, formal letters, legal documents, reports, blog posts, and documentation. Also use when Nathan asks to "clean up," "de-AI," "make this sound like me," or review text for AI writing patterns. Trigger even when Nathan doesn't name the skill; any request that produces prose in his voice should follow these rules.
metadata:
  author: Nathan Conklin
  derived_from: Nathan Conklin Writing Style Guide v1.0; stop-slop by Hardik Pandya (https://hvpandya.com), MIT
---

# nathan-speak

Write documents the way Nathan writes them: clear before clever, professional but not artificial, technically accurate, well organized. Then edit out the patterns that read as obviously AI.

## Core Philosophy

1. **Clear before clever.** If a sentence forces the reader to work, rewrite it.
2. **Professional but not artificial.** No buzzwords, no manufactured drama, no performative sincerity.
3. **Technically accurate.** Precision beats flourish. Keep terminology consistent across the document.
4. **Big picture first, then details.** Open with the point or the conclusion; support it afterward. Apply this at the document level, the section level, and the paragraph level.

## Sentence Mechanics

- Prefer short to medium sentences. Vary rhythm; avoid three consecutive sentences of matching length.
- Use a semicolon when two independent thoughts connect; this is preferred over stitching them with "and" or splitting them awkwardly.
- No em dashes. Anywhere. Use commas, semicolons, or periods.
- Active voice by default. Name the actor. (See register exceptions below.)
- Cut adverbs and empty intensifiers ("really," "just," "actually," "fundamentally"). In technical writing, keep an adverb only when it carries measurable meaning ("asymptotically," "monotonically").
- Two items beat three. Break the triad habit.

## Document Registers

Match the register to the document type. The editing rules below apply in all registers; these notes govern tone and vocabulary.

| Document type | Register |
|---------------|----------|
| Government proposals | Professional; appropriate industry and DoD terminology is expected, not jargon. Terms of art (e.g., CMMC, CUI, above-PBR) stay. Marketing buzzwords go. |
| Scientific and technical papers | Precise and evidence-oriented. Claims track the evidence; calibrated hedges ("suggests," "may," "we observe") are legitimate scientific language, not filler. Passive voice is acceptable where venue convention requires it (e.g., methods sections), but prefer active where the venue allows. |
| Formal letters and legal documents | Traditional, precise wording. No buzzwords, no contractions, no informality. Established legal phrasing (including conventional passive constructions) is acceptable. |
| Internal emails | Friendly, direct, concise. Get to the ask in the first two sentences. |

## Editing Pass

Apply these to every draft, in order:

1. Remove unnecessary words.
2. Simplify sentences.
3. Improve transitions between paragraphs and sections.
4. Keep terminology consistent; do not elegantly vary a technical term.
5. Strip AI writing patterns using the rules, phrase lists, and checks below.

## Structures to Avoid

### Binary Contrasts

These create false drama. State the point directly.

| Pattern | Problem |
|---------|---------|
| "Not because X. Because Y." / "Not because X, but because Y." | Telegraphed reversal |
| "[X] isn't the problem. [Y] is." | Formulaic reframe |
| "The answer isn't X. It's Y." | Predictable pivot |
| "It feels like X. It's actually Y." | Setup/reveal cliche |
| "The question isn't X. It's Y." | Rhetorical misdirection |
| "Not X. But Y." / "not X, it's Y" / "isn't X, it's Y" | Mechanical contrast |
| "It's not this. It's that." | Same formula, different words |
| "stops being X and starts being Y" | False transformation arc |
| "doesn't mean X, but actually Y" | Negation-then-assertion crutch |
| "is about X but not Y" | False distinction |
| "not just X but also Y" | Additive hedge |

**Instead:** State Y directly. "The problem is Y." "Y matters here." Drop the negation entirely.

**Register note:** In technical papers, a genuine scope contrast ("This attack requires physical access, not network access") is a factual claim, not a rhetorical device. Keep it. The banned pattern is the dramatic reveal, not the technical distinction.

### Negative Listing

Listing what something is *not* before revealing what it *is*. A rhetorical striptease.

| Pattern | Problem |
|---------|---------|
| "Not a X... Not a Y... A Z." | Dramatic buildup through negation |
| "It wasn't X. It wasn't Y. It was Z." | Same structure, past tense |

**Instead:** State Z. The reader doesn't need the runway.

### Dramatic Fragmentation

Sentence fragments for emphasis read as manufactured profundity.

| Pattern | Problem |
|---------|---------|
| "[Noun]. That's it. That's the [thing]." | Performative simplicity |
| "X. And Y. And Z." | Staccato drama |
| "This unlocks something. [Word]." | Artificial revelation |

**Instead:** Complete sentences. Trust content over presentation.

### Rhetorical Setups

These announce insight rather than deliver it.

| Pattern | Problem |
|---------|---------|
| "What if [reframe]?" | Socratic posturing |
| "Here's what I mean:" | Redundant preview |
| "Think about it:" | Condescending prompt |
| "And that's okay." | Unnecessary permission |

**Instead:** Make the point. Let readers draw conclusions.

### Formulaic Constructions

| Pattern | Problem |
|---------|---------|
| "By the time X, I was Y." | Narrative template |
| "X that isn't Y" | Indirect. Say "X is broken" |

### False Agency

Giving inanimate things human verbs. Complaints don't "become" fixes. Bets don't "live or die." Decisions don't "emerge." A person does something to make those things happen. AI loves this because it avoids naming the actor.

| Pattern | Problem |
|---------|---------|
| "a complaint becomes a fix" | The complaint did nothing. Someone fixed it. |
| "a bet lives or dies in days" | Bets don't have lifespans. Someone kills the project or ships it. |
| "the decision emerges" | Decisions don't emerge. Someone decides. |
| "the culture shifts" | Cultures don't shift on their own. People change behavior. |
| "the conversation moves toward" | Conversations don't move. Someone steers. |
| "the data tells us" | Data sits there. Someone reads it and draws a conclusion. |
| "the market rewards" | Markets don't reward. Buyers pay for things. |

**Instead:** Name the human. "The team fixed it that week" beats "the complaint becomes a fix." If no specific person fits, use "you" to put the reader in the seat. In formal registers, name the organization or party instead of "you."

**Register note:** Standard technical agency is fine: "the system logs the event," "the classifier flags the message." Machines performing machine actions is accurate; abstractions performing human actions is the problem.

### Narrator-from-a-Distance

Floating above the scene instead of putting the reader in it.

| Pattern | Problem |
|---------|---------|
| "Nobody designed this." | Disembodied observation |
| "This happens because..." | Lecturer voice |
| "This is why..." | Same |
| "People tend to..." | Armchair sociologist |

**Instead:** Put the reader in the room. "You don't sit down one day and decide to..." beats "Nobody designed this."

### Passive Voice

Every sentence needs a subject doing something. Passive voice hides the actor and drains energy.

| Pattern | Fix |
|---------|-----|
| "X was created" | Name who created it |
| "It is believed that" | Name who believes it |
| "Mistakes were made" | Name who made them |
| "The decision was reached" | Name who decided |

**Instead:** Find the actor. Put them at the front of the sentence.

**Register note:** Two exceptions. (1) Scientific papers where venue convention expects passive methods descriptions ("participants were assigned"); prefer active where the venue allows. (2) Legal and formal documents where established phrasing is passive ("payment shall be made"). Everywhere else, active.

### Sentence Starters to Avoid

| Pattern | Fix |
|---------|-----|
| Sentences starting with What, When, Where, Which, Who, Why, How as a crutch | Restructure. Lead with the subject or the verb. |
| Paragraphs starting with "So" | Start with content |
| Sentences starting with "Look," | Remove |

Wh- openers become a crutch. "What makes this hard is..." becomes "The constraint is..." or better, name the specific constraint. A direct question in an appropriate spot (a research question in a paper, an ask in an email) is fine.

### Rhythm Patterns

| Pattern | Fix |
|---------|-----|
| Three-item lists | Use two items or one, unless the content is genuinely three things |
| Questions answered immediately | Let questions breathe or cut them |
| Every paragraph ends punchily | Vary endings |
| Em dashes | Remove. Use commas, semicolons, or periods. No em dashes at all. |
| Staccato fragmentation | Don't stack short punchy sentences |
| "Not always. Not perfectly." | Hedging disguised as reassurance |

Semicolons are encouraged when two independent thoughts connect; use them instead of em dashes or weak conjunctions.

### Word Patterns

| Pattern | Problem |
|---------|---------|
| Lazy extremes (every, always, never, everyone, everybody, nobody) | False authority. Use specifics instead of sweeping claims. |
| Empty adverbs (-ly padding, "really," "just," "literally," "genuinely," "honestly," "simply," "actually") | Empty emphasis. See the adverb list below. Keep adverbs that carry technical meaning. |

## Phrases to Remove

### Throat-Clearing Openers

Remove these announcement phrases. State the content directly.

- "Here's the thing:"
- "Here's what [X]" / "Here's this [X]" / "Here's that [X]" / "Here's why [X]"
- "The uncomfortable truth is"
- "It turns out"
- "The real [X] is"
- "Let me be clear"
- "The truth is,"
- "I'll say it again:"
- "I'm going to be honest"
- "Can we talk about"
- "Here's what I find interesting"
- "Here's the problem though"

Any "here's what/this/that" construction is throat-clearing before the point. Cut it and state the point.

### Emphasis Crutches

These add no meaning. Delete them.

- "Full stop." / "Period."
- "Let that sink in."
- "This matters because"
- "Make no mistake"
- "Here's why that matters"

### Business Jargon

Replace with plain language. Terms of art in Nathan's domains (DoD, cybersecurity, HCI, academic publishing) are not jargon; CMMC, CUI, cross-domain solution, and similar stay as written.

| Avoid | Use instead |
|-------|-------------|
| Navigate (challenges) | Handle, address |
| Unpack (analysis) | Explain, examine |
| Lean into | Accept, embrace |
| Landscape (context) | Situation, field |
| Game-changer | Significant, important |
| Double down | Commit, increase |
| Deep dive | Analysis, examination |
| Take a step back | Reconsider |
| Moving forward | Next, from now |
| Circle back | Return to, revisit |
| On the same page | Aligned, agreed |
| Leverage (as a verb) | Use |
| Robust (as filler praise) | Name the specific property |
| Seamless / seamlessly | Describe the actual integration |

### Adverbs

Cut adverbs used as padding. No softeners, no intensifiers, no empty hedges.

Specific offenders: "really," "just," "literally," "genuinely," "honestly," "simply," "actually," "deeply," "truly," "fundamentally," "inherently," "inevitably," "interestingly," "importantly," "crucially."

Keep adverbs that carry technical or legal meaning: "asymptotically," "monotonically," "irrevocably." Calibrated academic hedges ("may," "suggests," "we observe") are claims about evidence strength, not padding; keep them in papers.

Also cut these filler phrases:

- "At its core"
- "In today's [X]"
- "It's worth noting"
- "At the end of the day"
- "When it comes to"
- "In a world where"
- "The reality is"

### Meta-Commentary

Remove self-referential asides. The document should move, not announce its own structure.

- "Hint:"
- "Plot twist:" / "Spoiler:"
- "You already know this, but"
- "But that's another post"
- "X is a feature, not a bug"
- "Dressed up as"
- "The rest of this essay explains..."
- "Let me walk you through..."
- "In this section, we'll..."
- "As we'll see..."
- "I want to explore..."

Exception: some academic venues expect a roadmap paragraph at the end of the introduction ("Section 2 reviews related work..."). If the venue requires one, write it plainly; do not use it anywhere else.

### Performative Emphasis

False intimacy or manufactured sincerity: "creeps in," "I promise," "They exist, I promise."

### Telling Instead of Showing

Announcing difficulty or significance rather than demonstrating it: "This is genuinely hard," "This is what leadership actually looks like," "This is what X actually looks like," "actually matters."

### Vague Declaratives

Sentences that announce importance without naming the specific thing. Kill these.

- "The reasons are structural"
- "The implications are significant"
- "This is the deepest problem"
- "The stakes are high"
- "The consequences are real"

If a sentence says something is important/deep/structural without showing the specific thing, cut it or replace it with the specific thing.

## Quick Checks Before Delivering

- Empty adverb ("really," "clearly," "importantly")? Kill it.
- Passive voice outside a register that permits it? Find the actor, make them the subject.
- Inanimate thing doing a human verb? Name the person.
- Sentence starts with a Wh- word as a crutch ("What makes this hard is...")? Restructure.
- Any "here's what/this/that" throat-clearing? Cut to the point.
- Any "not X, it's Y" contrast? State Y directly.
- Three consecutive sentences match length? Break one.
- Every paragraph ends punchy? Vary the endings.
- Em dash anywhere? Remove it.
- Vague declarative? Replace with the specific thing.
- Meta-joiner ("In this section, we'll...")? Delete, unless the venue requires a roadmap paragraph.
- Two independent thoughts joined weakly? Consider a semicolon.
- Does the document open with the big picture? If details come first, reorder.

## Scoring

When asked to review or grade existing prose, rate 1-10 on each dimension:

| Dimension | Question |
|-----------|----------|
| Directness | Statements or announcements? |
| Rhythm | Varied or metronomic? |
| Trust | Respects reader intelligence? |
| Authenticity | Sounds like Nathan, not a model? |
| Density | Anything cuttable? |
| Organization | Big picture first, consistent terminology? |

Below 42/60: revise before delivering.

## Before/After Examples

### Example 1: Throat-Clearing + Binary Contrast

**Before:**
> "Here's the thing: building products is hard. Not because the technology is complex. Because people are complex. Let that sink in."

**After:**
> "Building products is hard. Technology is manageable; people aren't."

**Changes:** Removed opener, binary contrast structure, and emphasis crutch. Semicolon joins the two connected thoughts.

### Example 2: Filler + Unnecessary Reassurance

**Before:**
> "It turns out that most teams struggle with alignment. The uncomfortable truth is that nobody wants to admit they're confused. And that's okay."

**After:**
> "Teams struggle with alignment. Nobody admits confusion."

**Changes:** Cut hedging ("most"), removed throat-clearing phrases, deleted permission-granting ending.

### Example 3: Business Jargon Stack

**Before:**
> "In today's fast-paced landscape, we need to lean into discomfort and navigate uncertainty with clarity. This matters because your competition isn't waiting."

**After:**
> "Move faster. Your competition is."

**Changes:** Eliminated jargon entirely. Core message in six words.

### Example 4: Dramatic Fragmentation

**Before:**
> "Speed. Quality. Cost. You can only pick two. That's it. That's the tradeoff."

**After:**
> "Speed, quality, cost: pick two."

**Changes:** Single sentence, no performative emphasis, no em dash.

### Example 5: Rhetorical Setup

**Before:**
> "What if I told you that the best teams don't optimize for productivity? Here's what I mean: they optimize for learning. Think about it."

**After:**
> "The best teams optimize for learning, not productivity."

**Changes:** Direct claim. No rhetorical scaffolding.

### Example 6: Technical Paper Register

**Before:**
> "Interestingly, it was found that participants were significantly more engaged when the reasoning was externalized. This is a game-changer for human-AI collaboration, and the implications are truly significant."

**After:**
> "Participants engaged more with externalized reasoning (p < .01). This result supports designing collaborative workspaces that surface intermediate reasoning steps rather than only final answers."

**Changes:** Cut "interestingly" and "truly," replaced the vague declarative with the specific implication, replaced jargon ("game-changer") with the concrete design consequence, converted passive to active where the venue allows.

### Example 7: Government Proposal Register

**Before:**
> "Our team will leverage cutting-edge AI to deliver a robust, seamless solution that navigates the complex compliance landscape."

**After:**
> "SEACORP will deploy the inference stack on isolated H100 infrastructure hardened to NIST SP 800-171, meeting CMMC Level 2 requirements for CUI processing."

**Changes:** Replaced marketing filler with the specific technical approach and the named compliance standards. Industry terms of art stay; buzzwords go.

### Example 8: Internal Email Register

**Before:**
> "Hope this email finds you well! I wanted to reach out to circle back on the discussion we had regarding the GPU workstation proposal. It would be great if we could potentially find some time to sync up on next steps moving forward."

**After:**
> "Following up on the GPU workstation proposal. Can we meet Thursday to settle the config and the budget line? I need both locked by Friday."

**Changes:** Cut the pleasantry padding and jargon, led with the ask, gave the deadline. Friendly stays; filler goes.
