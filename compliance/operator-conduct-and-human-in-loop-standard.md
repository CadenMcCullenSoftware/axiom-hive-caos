# Operator Conduct and Human-in-the-Loop Standard

| Field | Value |
| --- | --- |
| Author | MIA |
| Attribution | This was supported for MIA by Kilo (kilo-auto/free). |
| Document type | Conduct standard |
| Subject | The conduct of the human operator of the Counter-Adversary Operations System (CAOS) under conditions of uncertainty, time pressure, and incomplete information |
| Version | 1.0 |
| Status | Authoritative for operator conduct, the human-in-the-loop checkpoints, and operator evidence discipline. Subordinate to the constitutional instrument; where both apply, the stricter prevails |
| Identifier ownership | `HITL-1` – `HITL-8`; `EVD-1` – `EVD-8`; `LIM-CC1` – `LIM-CC12`. Cross-references to `CON-1` – `CON-12` are citations only and are not defined here |
| Deployment form | Deployment block. A console configured to enforce this standard must render its rules inline at the point of decision (§1.3) |
| Companion documents | `system-design-and-framework.md`; `constitutional/engagement-authorisation-and-rules-of-engagement.md`; `operational/mission-lifecycle-and-decision-loop.md`; `operational/watchfloor-interface-specification.md`; `operational/decision-support-and-scoring-model.md`; `operational/countermeasure-catalogue.md`; `operational/adversary-ai-taxonomy-and-threat-model.md`; `operational/platform-architecture-and-agent-containment.md`; `reference/audit-and-conformance-procedures.md`; the six `templates/` artefacts; `README.md`. Full table with roles at §1.5 |

---

## 1. Purpose and Scope

### 1.1 Purpose

This standard binds the human operator of CAOS. It states the duties the operator owes, the checkpoints at which human authority must be exercised and demonstrated, the handling of uncertainty and of attribution error, the ethics of escalation, the obligations of refusal and of pause, and the reporting the operator owes when any of these are tested.

It exists because the framework's central claim is not that the system is right but that the human remains the decision-maker. A claim of that kind is only true if the conditions under which the human decides are themselves governed. This standard governs those conditions.

The standard is written for the person at the console. Where it states a duty, it states what that duty looks like on the screen, what record satisfies it, and how it fails. A duty that cannot be observed cannot be enforced, and a duty that cannot fail cannot be audited.

### 1.2 Scope

| Applies to | Does not apply to |
| --- | --- |
| The named operator of a CAOS operation, in both the defensive and the counter-adversary posture | The content of the rules-of-engagement profiles, the adversary taxonomy, the countermeasure catalogue, or the scoring model |
| Anyone acting in the operator role, including a relieving operator, a trainee under supervision, and an operator operating outside normal hours | The technical implementation of the policy engine, the control plane, or the ledger, except where this standard states an interface obligation the implementation must meet |
| The approver of an operation card, to the extent that the approver's conduct is governed by the human-in-the-loop checkpoints in §5 | The legal analysis itself, the proportionality judgement of the authorising authority, and the drafting of the engagement authorisation |
| Any console, procedure, or organisational practice that is used to authorise, dispatch, monitor, or stop a countermeasure | The conduct of the adversary, the behaviour of models, or the design of the framework's own intelligence content |

**Precedence.** This standard is subordinate to the constitutional instrument, `constitutional/engagement-authorisation-and-rules-of-engagement.md`. Where a matter is governed by both, the stricter requirement prevails. This standard never confers authority, never widens an authorisation, and never permits an action the constitutional instrument forbids.

**Constitutional conduct constraints.** The constitutional conduct constraints, `CON-1` to `CON-12`, are defined in the constitutional instrument and are not restated or paraphrased here. Where a duty in this document depends on a constitutional constraint, the operator must read the constitutional instrument. This standard does not summarise it, because a summary is a second source that can drift from the first.

### 1.3 Deployment block

This standard is a **deployment block**. It is not a manual to be read once and kept on a shelf, and it is not a set of principles to be recalled under pressure. An operator console configured to enforce this standard must carry these rules **inline**, at the point at which the operator is asked to decide.

A rule that lives only in a document is enforced by memory, and memory is the first thing the pressures in §4.3 consume. A rule that lives at the point of decision is enforced by the interface, and an interface does not get tired, does not get promoted, and does not get told to hurry.

| Rule group | Inline surface at the console | What must be present at that surface |
| --- | --- | --- |
| Human-in-the-loop checkpoints (§5) | The approval surface at G-4 Authorisation and the dispatch surface at G-5 Dispatch | The five things the approver must read (HITL-7), stated next to the approval control and not on a screen behind it |
| Evidence and claim labelling (§7) | The evidence panel and every field that carries a claim | The label set, the source tier set, and the rule that unlabelled material is not presented as a claim |
| Uncertainty and attribution error (§6) | The decision-record composer | The prompt to name the residual uncertainty; the prohibitions on treating model confidence as probability and on suppressing an inconvenient hypothesis |
| Escalation ethics (§8) | The escalation-request composer | The requirement to state the residual risk of not escalating, and the statement that escalation is a new instrument and not a field edit |
| Refusal and pause (§9) | The abort and recall surface, and the pause control | The statement that a pause is not a fault, and the requirement that a pause be recorded with its reason and its cost |
| Reporting (§10) | The reporting surface | The recipient list and the timing for each reportable event, stated at the point the report is raised |

**The inline test.** For each rule group above, the console must be able to demonstrate, on request, that the rule text is present on the surface that enforces it, and that the surface cannot be completed without the rule having been surfaced. Where a surface enforces a rule by refusing to proceed, the refusal message must name the rule it is enforcing. A refusal the operator cannot trace to a rule is an unexplained failure, and unexplained failures are not trusted by the people who depend on them.

**Verification status.** The reference implementation is asserted to enforce the mechanically checkable parts of this standard. That assertion is recorded in `reference/audit-and-conformance-procedures.md` §3 and is not independently substantiated at the time of writing. Verification status: **Unverified**.

### 1.4 What this standard does not do

- It does not create authority. No clause in this document permits an action that the engagement authorisation does not permit.
- It does not make attribution reliable. It makes the consequences of unreliability visible at the point of decision and bounded by class.
- It does not substitute for judgement. Where this document says the operator must decide, it means the operator decides, and the record shows the decision.
- It does not guarantee outcomes. It guarantees only that the record of an outcome is reconstructible by someone who was not present.

### 1.5 Companion documents

Paths are relative to the set root, `/home/k/Desktop/AI C@ Op`.

| Document | Path | Relevance to this standard |
| --- | --- | --- |
| System Design and Framework | `system-design-and-framework.md` | The authoritative source of the shared identifiers, the control spine, and the error handler's role |
| Engagement Authorisation and Rules of Engagement | `constitutional/engagement-authorisation-and-rules-of-engagement.md` | The constitutional instrument; `CON-1` to `CON-12`; the authorisation ladder this standard operates under |
| Mission Lifecycle and Decision Loop | `operational/mission-lifecycle-and-decision-loop.md` | The gates at which the checkpoints in §5 are exercised, the decision record, the error handler |
| Watchfloor Interface Specification | `operational/watchfloor-interface-specification.md` | The console behaviours that §5 and §7 require of the interface |
| Decision Support and Scoring Model | `operational/decision-support-and-scoring-model.md` | Attribution confidence, residual risk, and the components an operator may contest |
| Countermeasure Catalogue | `operational/countermeasure-catalogue.md` | The class, reversibility, and failure mode of each countermeasure referenced in this standard |
| Adversary AI Taxonomy and Threat Model | `operational/adversary-ai-taxonomy-and-threat-model.md` | The classification vocabulary and the proving ground |
| Platform Architecture and Agent Containment | `operational/platform-architecture-and-agent-containment.md` | The control plane, the ledger, and the containment model that the error handler depends on |
| Audit and Conformance Procedures | `reference/audit-and-conformance-procedures.md` | The procedures by which conformance in §11 is assessed |
| Operation Card template | `templates/operation-card.md` | The instrument that carries the approvals, evidence, and abort conditions |
| Rules of Engagement Card template | `templates/rules-of-engagement-card.md` | The pocket reference for the profile in force |
| Decision Log template | `templates/decision-log.md` | The record that §4, §6, and §10 require |
| Escalation Request template | `templates/escalation-request.md` | The instrument by which a ceiling is raised |
| After-Action Report template | `templates/after-action-report.md` | The instrument by which learning in §4 and §10 is delivered |
| Set Index | `README.md` | The canonical map, the controlled vocabulary, and the identifier registry |

---

## 2. Interpretation of Normative Terms

The terms **must**, **must not**, **should**, **should not**, and **may** are to be interpreted as described in RFC 2119.

- **Must / must not** denote absolute requirements.
- **Should / should not** denote recommendations that may be departed from only where legitimate reasons exist; any departure should be made explicit.
- **May** denotes optional behaviour that remains at the operator's discretion within the constraints of this document.

Two further terms carry specific force in this document.

- **Must not** on the display of information means the console must not present the material in that form, whether or not the operator asks for it.
- **Recorded** means captured in the ledger or the decision log in a form that a reviewer who was not present can read and reconstruct. A record held in the operator's memory, in an unlogged note, or in an unexported screen state is not a record.

---

## 3. Defined Terms

| Term | Definition |
| --- | --- |
| **CAOS** | The Counter-Adversary Operations System described by this set |
| **this standard** | The Operator Conduct and Human-in-the-Loop Standard, this document |
| **the framework** | CAOS as a whole: its mandate, its doctrine, its machinery, and its artefacts |
| **the constitutional instrument** | `constitutional/engagement-authorisation-and-rules-of-engagement.md`, and the engagement authorisation issued under it |
| **the operator** | The named human who holds the operation at the console and who is accountable for the decisions taken under it. Where a task is delegated, the operator remains accountable for the delegation and for the outcome |
| **authorising authority** | The named human who issues the engagement authorisation and who may amend or revoke it. The authority for the profile in force is set by the profile table in the master design |
| **duty manager** | The named human accountable for the conduct of operations during a period of duty; the default recipient of an escalation, an abort, and a report of collateral impact |
| **legal contact** | The named human competent to advise on the legal position of the engagement, its authorisation, and its effects on third parties. Required at profile R2 and above |
| **asset owner** | The named human accountable for a specific asset, system, or service that an operation may affect |
| **card approver** | The named human who authorises an operation card at the depth required by its collateral class and its profile |
| **the specialist** | A named human accountable for a specific capability of the framework — legal, telemetry, model security, data protection, or such other specialism as the engagement authorisation requires — who is consulted where that capability bears on the decision. A specialist is a person, not a service, and not a model |
| **the Watchfloor** | The operator console; the interface through which the human operator acts |
| **Operation Card** | The atomic unit of authorised work; the record that authorises a specific set of actions against a specified target set |
| **engagement authorisation (EA)** | The written, time-bounded mandate that is the root of trust for an operation |
| **ROE profile** | One of R0 Observe, R1 Shield, R2 Trap, R3 Deceive, R4 Disrupt, R5 Neutralise; a ceiling on what an operation may do |
| **collateral class** | One of C0, C1, C2, C3; the class of the effect a countermeasure has, which governs the approval depth required. "C1+" denotes C1, C2, or C3 |
| **autonomy class** | One of AC-0 Manual, AC-1 Assisted, AC-2 Supervised, AC-3 Delegated, AC-4 Autonomous; how a countermeasure executes. "AC-2+" denotes AC-2, AC-3, or AC-4 |
| **the error handler** | The single enforcement point to which every gate resolves; it halts progress, requires the issue to be recorded, and routes the work to re-verification or transparent rewriting |
| **decision log** | The record of rationale, alternatives, and risk for each material decision |
| **the ledger** | The append-only, hash-chained record of decisions, authorisations, dispatches, and state changes |
| **the record** | The combined evidentiary surface of an operation: the ledger entries, the decision log, the Operation Card and its revisions, the escalation requests, and the after-action report |
| **claim label** | One of Fact, Estimate, Interpretation, Hypothesis, Recommendation |
| **source reliability tier** | Rank 1 (highest) to 4 (lowest) |
| **verification status** | Verified (primary), Verified (secondary), Corrected, Unverified, Requires confirmation |
| **architectural assertion** | A statement of intended system behaviour that has not been independently substantiated |
| **attribution confidence (c)** | The stated probability that activity is attributable to a specific adversary, in [0.0, 1.0] |
| **residual risk (R)** | S_eff × (1 − e); the risk carried forward after the selected countermeasures, and the figure the operator is accountable for |
| **the proving ground** | The exercise harness in which an adversary is simulated to validate detection and rehearse operators |
| **deconfliction** | The check that a countermeasure does not interfere with a live legitimate operation |
| **approval** | A recorded act by a named person, taken against a specific revision of a specific card, that is capable of being withheld |
| **active operation** | An operation that is authorised, armed, or dispatched, and whose effects may still be occurring |
| **abort** | The termination of a running countermeasure and reversion to the passive posture. An abort is immediate, unconditional, and not subject to confirmation |
| **pause** | The suspension of an operation by the operator pending information, authority, or clarification. A paused operation is not a failed operation and is not a closed operation |
| **reversion** | The automatic return of the system to the passive posture on a declared trigger, without human action |
| **misattribution** | The discovery, after an action has been taken, that the attribution on which it rested was wrong in whole or in part |
| **wrong classification** | The discovery that a signal was classified under the wrong AAT category, or that an attribution assessment named the wrong adversary, where no action was taken on the classification |
| **residual uncertainty** | The uncertainty that remains after the available evidence has been gathered, weighted, and stated. It is the uncertainty the decision is actually made under |
| **inconvenient hypothesis** | A hypothesis that is supported by evidence, or that the evidence does not exclude, and whose retention would complicate the current course of action |
| **the inline test** | The test stated in §1.3: the console must be able to demonstrate that the rule text is present on the surface that enforces it |
| **single-approver rule** | The rule stated in HITL-8: the person who executes a consequential action may not be the sole approver of that action |

---

## 4. The Operator's Duty

### 4.1 The asymmetry

The operator is accountable for a decision taken under uncertainty, with incomplete information, on a subject the adversary controls, against a deadline that belongs to somebody else.

The framework does not remove that accountability. Nothing in CAOS makes the decision easier, the evidence better, the attribution more likely to be right, or the adversary less capable. What the framework does is make the accountability **legible**: it makes visible what was known, what was not, what was chosen instead of what, what was risked, what was assumed, and what would have caused the decision to be withdrawn.

That is the whole of the promise, and it is worth stating precisely because the temptation in operational settings is to describe the framework as a guarantee. It is not a guarantee. It is an instrument for making a judgement defensible to a reviewer who was not present, and a judgement that is legible can be examined, corrected, and learned from. A judgement that is hidden cannot.

**The duty is asymmetric in one direction only.** The consequence of acting wrongly — a third party harmed, an account terminated, a service denied, a reputation damaged, a person harmed — falls on parties who did not choose it and cannot undo it. The consequence of failing to act — an adversary's campaign continues — falls principally on the operator's own estate, and is frequently borne by the same organisation. Under-reaction is often cheaper than over-reaction, but it is not costless, and where the two are close the framework does not permit the operator to prefer the cheaper one merely because it is cheaper.

### 4.2 The seven duties

| # | Duty | The operator must | Evidence that satisfies it | Typical failure signature |
| --- | --- | --- | --- | --- |
| 1 | **Care** | Take the action that a reasonable and informed person, in the same position and knowing what the operator knows, would consider right; and take no action that would be considered wrong | A decision record whose stated reasoning could be followed by a reviewer without the operator present | A decision whose rationale cites urgency, availability, or the absence of a better option |
| 2 | **Record** | Leave behind a record sufficient for another reviewer to reconstruct the decision, including the alternatives, the residual uncertainty, and the assumptions | A decision log entry and the ledger entries that correspond to it | A record that states the outcome and the conclusion, and omits the alternatives and the doubt |
| 3 | **Escalate** | Raise the question with the authority able to answer it, at the depth the profile requires, rather than deciding it alone | An escalation request and its disposition in the record | A silence treated as consent, or a decision taken above the ceiling because the escalation had not been answered |
| 4 | **Disclose** | Make the consequences of the decision visible to those who bear them and to those who must record them, before the decision takes effect where that is possible | The card's risk field, the collateral exposure entry, and the reporting in §10 | A decision whose collateral effect was discovered afterwards by a third party |
| 5 | **Refuse** | Decline to act where acting would exceed authority, breach the constitutional instrument, or be wrong on the evidence | A recorded refusal naming the reason and the rule | A refusal that is silent, so that the next operator makes the same decision again |
| 6 | **Learn** | Contribute what was learned — including what was wrong — to the framework's content, so that the same failure is not repeated | An after-action report, a detection-gap entry, a classifier correction | An operation that closes with no entry in the gap list, even though something was learned |
| 7 | **Stay in authority** | Act only within the profile, the card, and the target set in force | The card, the admissibility results, and the reversion and expiry behaviour | A field edit to a live card, or a dispatch made under a superseded authorisation |

**The duty of care.** The operator must act on the best information available at the time, not the best information that later proves to have existed, and not the information the operator wishes had existed. The duty is discharged by the quality of the judgement and the honesty of its record, not by its outcome. An operator who reasons well, records accurately, and is wrong has discharged the duty; an operator who reasons badly, records well, and is right has not.

**The duty of record.** The operator must write down what was decided, on what basis, with what uncertainty, and what was rejected. A decision with no recorded alternatives is not a decision; it is a result. The record is written at the time, in the operator's own words, and is not reconstructed afterwards from memory or from the outcome.

**The duty to escalate.** The operator must escalate when the question is not theirs to answer, and must not treat an unanswered escalation as a permission. Escalation is not an admission of incapacity and must not be presented as one; it is the ordinary exercise of the authority the framework places in the operator.

**The duty to disclose.** The operator must make the collateral position of a decision visible before the decision is taken, not after the effect has occurred. Concealing the operation's existence from the authority that authorised it, or from the persons whose systems are affected in a way carrying legal or safety consequences, is outside the framework's boundary and is prohibited.

**The duty to refuse.** The operator must refuse actions that exceed authority, breach the constitutional instrument, or are wrong on the evidence as it stands. A refusal is a successful control and is never treated as a failure of the system or of the operator. Where the operator refuses and is later shown to have been right to do so, the record must still show the refusal as a refusal.

**The duty to keep learning.** The operator must treat every operation as a source of information about the framework as well as about the adversary. Where the framework failed, the operator must say so, in the same terms as a detection gap, because an unnamed framework failure is repeated until someone else pays for it.

**The duty to remain within authority.** The operator must not act outside the profile, the card, or the target set in force, and must not extend an authorisation by interpretation, precedent, or urgency. Authority is a property of a document, not of a situation.

### 4.3 The pressures that erode these duties

Every duty in §4.2 fails under the same five conditions. They are stated here so that the operator can recognise them in themselves, and so that a supervisor can recognise them in a review.

| Pressure | How it appears at the console | What the framework offers against it | What the operator must do |
| --- | --- | --- | --- |
| **Time compression** | A deadline shown as a countdown; an expiry approaching on a card or an autonomy grant; a queue behind the card; the sense that the system will not wait | Expiry is a hard stop rather than a prompt to hurry (`AUTH-3`); reversion is automatic (`HITL-5`); the console may be configured to refuse a dispatch that cannot complete its own abort test | Treat the countdown as a fact about authority, not about the operator's competence. Where the timeline does not permit the checkpoint, the operation does not proceed; it is not run without the checkpoint |
| **Uncertainty** | A confidence below the threshold; a source marked degraded; an attribution distribution with a leading candidate that is not decisive; an empty field | Confidence is rendered inline (`WFC-4`); absence is shown as absence and not as a negative finding (`WFC-5`); identity-independent countermeasures remain available (`INT-4`) | Name the residual uncertainty in the record. Prefer the countermeasure that does not depend on the contested claim. Do not convert uncertainty into confidence by the passage of time |
| **Cost of delay** | The adversary's campaign continues while the card is drafted; the competitor's window closes; the budget for the operation expires | The risk of inaction is recorded on the card and displayed beside the risk of acting (`OP-4`); an escalation request may be raised without waiting for the operation to be ready | Weigh the two risks explicitly. A campaign that continues is a real cost, and it is not a licence to act beyond authority. Where the delay is the greater harm, say so in the escalation request |
| **The attractiveness of a decisive-looking recommendation** | A ranked list with a clear leader; a single countermeasure at the top; a recommendation with prose that reads as settled | The full ranked set including rejected candidates and reasons is displayed; components of every score are separately contestable (`SCORE-2`); a recommendation whose justification cannot be shown from the card's evidence is refused (`§7.3` of the master design) | Treat the recommendation as a proposal with a named alternative set. Select against the ranking if the judgement warrants, and record that it was a choice (`STEP-4`) |
| **A model sounding confident** | Fluent, categorical, well-formatted output that reads as settled fact; a high confidence figure attached to a thin evidence base | Every claim carries a label and a tier; confidence is separate from label (`EVD-4`); the console renders the derivation chain (`WF-11`) | Treat a model's confidence as an expression of the model, not as a measurement of the world. A model sounding confident is not evidence, and a confident recommendation is not a reason |

**On time compression specifically.** The most common failure in practice is not a failure of judgement under pressure. It is a failure of sequence under pressure: the operator, needing to meet a deadline, performs the steps in the order that gets to dispatch, rather than in the order the framework sets, and the checkpoint that was going to change the decision is the one that gets compressed. The defence is procedural rather than heroic. The operator must confirm, before dispatch, that each checkpoint in §5 has been exercised in the order the framework requires, and must treat a checkpoint that was skipped under time pressure as an abort condition, not as a technicality.

**On uncertainty specifically.** The pressure is not the uncertainty itself. It is the discomfort of acting under uncertainty in front of a system that renders it visibly. A console that renders uncertainty honestly will be under constant pressure to render it less honestly, because the discomfort is felt by the people using it and the tidiness is felt by nobody. The operator must not soften what the evidence shows in order to make the decision feel less difficult.

---

## 5. Human-in-the-Loop Checkpoints

These are the points at which human authority is either exercised or is not. They are the framework's load-bearing controls, and the console is the instrument that makes them real.

The checkpoints are cumulative. A card at collateral class C1 and autonomy class AC-2 has been through HITL-1, HITL-2, HITL-3, HITL-4, HITL-5, HITL-6, HITL-7, and HITL-8. An operator cannot discharge them collectively at one moment; each has its own trigger and its own evidence.

| ID | Control | Applies when | Exercised at | Evidence produced |
| --- | --- | --- | --- | --- |
| **HITL-1** | Named approver for consequential actions | C1+ or AC-2+ | G-4 Authorisation | An approval record naming the approver |
| **HITL-2** | Human authority is substantive, not procedural | Every checkpoint | G-4 | The approver's attested reading, and evidence that the decision was open to change |
| **HITL-3** | The abort channel is tested first | AC-2+ | G-5 Dispatch | An abort rehearsal record: who, when, what transition, how long |
| **HITL-4** | No approval-by-inference | Every approval | G-4, G-5 | An approval state showing an explicit act by a named person |
| **HITL-5** | Reversion is automatic and unconditional | Every autonomous grant | Continuous | A reversion entry with timestamp and cause |
| **HITL-6** | The approver is competent and able to refuse | Every approval | G-4 | A role and currency check; a refusal path that is symmetric with the approval path |
| **HITL-7** | The approver has read the five | Every approval | G-4 | An attestation bound to the card revision that was read |
| **HITL-8** | Single-approver rule; the model is excluded from the chain | C1+ or AC-2+ | G-4, G-5 | The executor and approver identities displayed together; the provenance of every text field in the chain |

### 5.1 HITL-1 — Consequential actions need a named approver

**HITL-1 — Consequential actions need a named approver.** Any action at collateral class C1 or above, and any action at autonomy class AC-2 or above, requires authorisation by a named human who has read the card, the risk assessment, and the abort conditions. A model, a rule, a schedule, or a previous precedent cannot supply that authorisation. *(Restated from `system-design-and-framework.md` §4.5; this standard is the authoritative source for the checkpoint's operational meaning.)*

**What it means at the console.** The approval control on a card at C1+ or AC-2+ must be bound to a single identified person, resolved from the authorisation ladder for the profile in force and confirmed at the moment of approval rather than at the moment the card was drafted. Where the person on the ladder is unavailable, the console must show that the request is unassigned and must not offer a default, a fallback, a group alias, or a role inbox. Where the operator executing the action is also the person the ladder resolves to, the control must remain available — the constraint against that arrangement is HITL-8, not HITL-1 — and the identity must be displayed. The approval record must name the person, the time, and the card revision approved. The identity must survive into the dispatch record and into the ledger, so that a reviewer can reconstruct who authorised what, not merely that something was authorised.

**Failure mode.** The approval is real but anonymous: an approval recorded against a role, a shift, a rota, or a group identity, so that the ledger shows an authorisation but cannot name a person who could be asked what they read. The second failure mode is institutional rather than technical: a ladder that resolves, in practice, to whoever is free, so that the named approver has not been brought into the operation at all and is discovering its existence in the ledger. Both failures are invisible in the approval field and visible only in the audit.

### 5.2 HITL-2 — Human authority is substantive, not procedural

**HITL-2 — Human authority is substantive, not procedural.** The approver must be able to change the decision. Where the interface makes approval a formality — a single button, no supporting information, no visible consequences — the checkpoint has failed its purpose and must be redesigned. *(Restated from `system-design-and-framework.md` §4.5.)*

**What it means at the console.** The approval control must be accompanied, on the same surface, by the material a person needs in order to reach a different decision: the ranked countermeasure set including the rejected candidates and the reason each was rejected; the residual risk before and after; the risk of inaction; the abort conditions; the collateral exposure; the attribution assessment and its confidence. The console must not offer an approval path that reaches the control without passing that material, and the material must not be collapsed by default. It is not sufficient that the material exists elsewhere in the console; an approver who must assemble it from other screens has been given a choice of a different kind, and usually a worse one, because the context they assemble will be the context they remember.

**Failure mode.** The approval is real but hollow. The approver is technically competent and busy, and the surface in front of them carries a summary that omits the rejected candidates, shows only the effective score and not the components, and puts the abort conditions on a separate screen. The decision is approved, the ledger records a named human, and the audit reveals that the human had no opportunity to exercise the judgement the framework claimed to have preserved.

### 5.3 HITL-3 — The abort channel is tested first

**HITL-3 — The abort channel is tested first.** Where a countermeasure is to run at AC-2 or above, the ability to abort must be demonstrated before the operation begins, not assumed. The demonstration must exercise the mechanism on a live control path, must record the identity of the person who exercised it and the time at which the passive posture was observed, and must be repeated after any change to the control plane, the console, or the network path between them. *(Restated from `system-design-and-framework.md` §4.5 and extended by this standard.)*

**What it means at the console.** The dispatch surface at G-5 must not offer to arm a countermeasure at AC-2+ unless a current abort rehearsal is recorded against the deployment it will run on. The rehearsal record must state the initiator, the mechanism used, the time the abort was issued, the time the passive posture was observed, the measured interval between them, and the state of the operation at the point of the abort. The rehearsal must exercise the path the operator would actually use under pressure — which is the path the operator has been trained on and which is the path that remains usable when something else is on fire. The abort control must be reachable without navigation and must require no confirmation, consistent with the interface constraint that the operator can always stop.

Two properties are required of the abort itself, and both are properties of the design rather than of the rehearsal. First, the abort must not depend on the same subsystem whose failure would make the abort necessary; where the control plane is degraded, the abort must still reach the countermeasure. Second, the abort must return the system to the passive posture, not merely stop the dispatch of new actions, leaving in-flight ones running.

**Failure mode.** The abort test is performed once, at deployment, and never repeated; the platform is then changed, and the abort path silently depends on the component that was changed. A second failure is the test that proves nothing: the abort is exercised with nothing running, so the interface returns success because the request was well formed, and nobody has observed a countermeasure actually stop. A third is the abort that stops dispatch but not effect, so the card shows an aborted operation while the countermeasure continues to run against the target. A fourth is the abort that exists but is not usable by the person who needs it, because it sits behind a menu, is disabled during a specific alert state, or requires a confirmation step that a saturated operator will not complete.

### 5.4 HITL-4 — No approval-by-inference

**HITL-4 — No approval-by-inference.** An approval is a recorded act by a named person. Silence, prior practice, an apparent pattern of consent, or an escalation that has not been answered does not constitute approval. *(Restated from `system-design-and-framework.md` §4.5.)*

**What it means at the console.** The approval state on a card must be an explicit enumeration with no default that can be mistaken for consent: pending, approved by a named person at a stated time against a stated revision, declined by a named person, withdrawn by the requester, or expired unanswered. The console must never render an unanswered request in a state that can be read as approved — including as an approved state inherited from a previous card, a previous revision, or a previous operator's session. Where an escalation request reaches the end of its window without a decision, the console must move the request to an explicit expired state and must treat the affected card as unauthorised for the action that required the escalation.

Bulk and batch approval is prohibited for actions at C1 or above. Each card is approved by a named person individually, because a bulk action cannot carry a per-card reading of the evidence, the alternatives, and the abort conditions. Where a supervisor wishes to approve many cards, the approval must still be taken per card; what may be expedited is the preparation, not the act.

**Failure mode.** The consent that was never given. The escalation was raised at 02:14 during a live campaign, nobody answered, the operator proceeded at 02:31 because the situation was deteriorating, and the ledger now carries an operation authorised by no one. The variant is quieter: the request timed out, the console's default on timeout is the absence of a decision, and the operator read the card as live because the card was live. The variant in the other direction is the standing pattern — the same request, the same duty manager, the same approval each time — which feels like consent and is nothing of the kind. Prior practice is not authority (`AUTH-5`).

### 5.5 HITL-5 — Reversion is automatic and unconditional

**HITL-5 — Reversion is automatic and unconditional.** Loss of telemetry, loss of the control plane, expiry of the autonomy grant, or detection of a condition on the card's abort list causes immediate reversion to the passive posture and notification. Reversion does not wait for a human to notice. *(Restated from `system-design-and-framework.md` §4.5 and extended by this standard to cover the trigger set, the state transition, and the console obligation.)*

**What it means at the console.** The triggers that must cause reversion are fixed and are not configurable by the operator: loss of telemetry from any source the card declares as required; loss of control-plane connectivity; expiry of the autonomy grant or of the card; breach of the autonomy envelope or exhaustion of the autonomy budget; detection of any condition on the card's abort list; and expiry or revocation of the engagement authorisation. Each reversion must be recorded as a state transition with a timestamp and a cause, and must be distinguishable in the ledger from a voluntary abort, because the two carry different lessons and different accountability.

The reversion must be effective without acknowledgement, without confirmation, and without any human action, and it must take precedence over any queued dispatch. The console must show the reversion as it happens, on the operation's own surface, not only in a notification that can be missed. Where reversion has occurred, the operator must not resume the operation on the basis of the belief that it is still running; the console must state the time of the last transition and the operation's actual state on every refresh.

**Failure mode.** The reversion implemented as a prompt. The console raises a banner asking the operator to acknowledge that a source has gone dark, the banner is dismissed, and the countermeasure continues to run against a state the operator can no longer see. That is not reversion; it is a notice. A second failure is the partial reversion: new dispatches are blocked, in-flight actions continue, and the card's status shows an operation that has been stopped. A third is the counter reset: the counters and the clock are reset on reversion such that the operator concludes that nothing much happened, when in fact the operation ran unsupervised for the interval concerned. A fourth is the human-gated reversion: a trigger exists, but the console waits for the operator to confirm before reverting, which means that the system depends on the attention of the person it was designed to be independent of.

### 5.6 HITL-6 — The approver is competent, current, and able to refuse

**HITL-6 — The approver is competent, current, and able to refuse.** An approval may be given only by a person who holds the role required at the approval depth for the card's collateral class, whose own authority is current and has not been revoked or expired, and who is able to withhold that approval as easily as they are able to give it. Where the approver cannot refuse — because the interface offers no refusal affordance, or because refusal carries a cost that the organisation makes the approver pay alone — the checkpoint has failed. *(Defined by this standard; not previously stated as a numbered requirement.)*

**What it means at the console.** The console must verify, at the moment of approval, that the approving identity holds the role required for the card's collateral class, that the person's own delegated authority is in date, and that no disqualifying condition applies. Where a role check fails, the control must be unavailable and the reason must be named. The refusal affordance must be given the same prominence, the same accessibility, and the same ease of use as the approval affordance: a refusal that requires a different number of clicks, a different screen, or an explanatory justification that approval does not require is a refusal the interface discourages, and an interface that discourages refusal has produced a checkpoint in name only.

Refusal must also be safe. Where refusing an operation exposes the approver to a consequence that approving it does not, the checkpoint is defeated by the organisation rather than by the framework. The operator's duty to refuse depends on refusal being a recognised, ordinary act within the organisation, and the console's duty here is to make refusal routine rather than to model it.

A person may not approve at a depth they do not hold. Where a card requires the duty manager and the duty manager is absent, the console must refuse the approval and show the required depth. It must not offer the option of approving anyway.

**Failure mode.** The approver by rota. The role check is absent, the ladder resolves to whoever is on shift, and the approver's competence is whatever the shift provides. The second failure mode is the asymmetry of the interface: a large green approve control and a small, distant, two-step decline control. The third is the unapprovable card, where the required depth is unavailable at the moment it is needed, so the operator either waits — losing the operational window — or obtains an approval from someone whose competence in the specific decision has never been established. The fourth is the approver who is current in role but stale in knowledge of the operation, having been added to the chain for availability rather than for judgement.

### 5.7 HITL-7 — The approver must have read the five; an approval without them is void

**HITL-7 — The approver must have read the five.** No approval is valid unless, at the time of approval, the approver has read: (a) the evidence on which the action rests, with its labels, tiers, and derivation; (b) the alternatives considered and the grounds for rejecting each; (c) the residual risk the action leaves behind; (d) the risk of not acting; and (e) the abort conditions under which the action will be withdrawn. An approval given without these is void, and the void approval must be recorded as void rather than silently honoured. *(Defined by this standard; not previously stated as a numbered requirement.)*

**What it means at the console.** All five must be present on the same surface as the approval control. The console must not enable the approval control until each of the five has actually been surfaced to the approver: the evidence panel must be expanded through its full derivation chain, the rejected set must be fully listed with its reasons, the residual risk must be shown both before and after the action, the risk of inaction must be shown on the same surface rather than in a separate field that can be collapsed, and the abort conditions must be displayed in full.

The approval must be bound to the revision of the card that was read. Where the card is revised after the approval — because new evidence arrived, a countermeasure was added, an assumption changed, or the residual risk was recomputed — the approval is void against the new revision and the console must require a fresh approval. This is the mechanism that makes the reading a fact about a moment rather than an intention about a document.

The console must record the approver's attestation to the five, and the attestation must identify the revision. The attestation is not a substitute for the surfacing; it is the record that the surfacing happened.

**Failure mode.** The approval captured against a summary. The approver approves a one-screen summary that carries the operation's name, a score, and an approve control; the evidence, the alternatives, and the abort conditions are three clicks away and were never opened. The second failure mode is the checkbox, which produces a compliance artefact and no comprehension: a control that satisfies the letter of HITL-7 by recording that a person clicked a box, without the material ever having been surfaced. The third is the stale approval, where the evidence changed materially after the reading — a new signal, a corrected attribution, a revised effectiveness estimate — and the approval was never retaken, so the authority on the record is authority over a decision nobody made. The fourth is the collapsed risk, where the residual risk and the risk of inaction are rendered as a single number with the counterfactual hidden, so that the approver approves the action without ever having seen what declining would have cost.

### 5.8 HITL-8 — Single-approver rule, and the exclusion of the model from the chain

**HITL-8 — Single-approver rule; the model is excluded from the chain.** A person who executes a consequential action may not be the sole approver of that action, where the action is at collateral class C1 or above or at autonomy class AC-2 or above. Separately, and without exception, a model may not occupy any role in the approval chain: not as approver, not as a second approver, not as a tie-breaker, not as a quorum participant, not as a source of the confidence on which a human's approval is said to rest, and not as the author of the text a human is approving. *(Defined by this standard; not previously stated as a numbered requirement.)*

**What it means at the console.** The console must display the executor's identity and the approver's identity together on the approval surface, and must make the approval control unavailable to the executor where the card is at C1+ or AC-2+ and no second approver is present. Where the card requires an approval depth of two or more, the console must enforce the quorum and must not permit the same individual to occupy two seats in it.

On the exclusion of the model, the console must make the provenance of every element of the approval chain visible. Text generated by a model must be visibly distinguished from text written by a person; the model's output is advisory material presented for a human to judge, and it may not be presented as a field of the approval chain. Concretely: there may be no auto-approval, no confidence-triggered approval, no approval pre-set by a model, no approval populated from a model's characterisation of the situation, and no field in the chain whose content was written by a model without being visibly a model output. Where the approver's decision was materially shaped by a recommendation, the recommendation is part of the evidence and is labelled as such under EVD-1 — it is not a participant in the chain.

**Failure mode.** The single-approver case, which is common precisely where the pressure is highest: the operator who is also the most qualified person available prepares the card, dispatches the action, and approves it, and the ledger shows a compliant-looking approval. The second failure mode is the model as second approver, in the form of an advisory field the operator reads and treats as a second opinion, or a model-written summary of the risk that the approver accepts in place of forming their own. The third is the automated pre-set: a card drafted by a model with a recommendation already positioned, such that approving the recommended option requires one click and declining requires the full path through the alternatives. The fourth is the named but ceremonial second approver, present in the quorum and unable to refuse for any of the reasons in HITL-6, which satisfies the count and none of the purpose.

---

## 6. Uncertainty, Attribution Error, and the Error Handler

### 6.1 Naming the residual uncertainty

**The operator must name the residual uncertainty in the decision record.** Not the uncertainty as it stood before the evidence was gathered, and not a general acknowledgement that the situation is complex. The decision record must state what remained uncertain at the moment of the decision, in the terms that bear on the choice, and the record must show what was done about it.

| Uncertainty | How it appears at the console | What the decision record must contain |
| --- | --- | --- |
| **Evidential** | A required source is degraded, late, or silent; the evidence on the card is thin | Which source is degraded, which conclusions depend on it, and what was done in its absence |
| **Attributional** | The attribution distribution has a leading candidate that is not decisive, or the leading candidate changed between assessments | The candidate set, the confidence, the basis, and the alternative explanation that was not excluded |
| **Classificational** | The signal sits between two AAT categories, or the category is stable but the technique is not | The categories carried, the evidence for each, and which classification the countermeasure depends on |
| **Consequential** | The collateral effect cannot be bounded to the class named on the card | The known effects, the unbounded portion, and the decision to proceed regardless, with its reason |
| **Predictive** | The countermeasure's effectiveness is estimated, and the estimate carries a wide interval | The effectiveness estimate, its confidence, and the effect of the low end of the interval on the residual risk |
| **Temporal** | The situation is developing faster than the evidence can be gathered | The evidence available at the decision, the evidence expected later, and the contingency if the later evidence contradicts the earlier one |

**The operator must not close a gap in the record with confidence.** Where a field of the decision record cannot be completed because the evidence is unavailable, the field is left open with the reason stated. An open field is a legible state; a plausible entry in a closed field is not.

### 6.2 A wrong classification is a normal event, not a failure

The framework will be wrong. The classifier will miscategorise, the attribution assessment will name the wrong adversary, the effectiveness estimate will be too high, the hypothesis will turn out to be unfalsifiable. This is the expected condition of the work, not an exception to it.

What distinguishes a healthy error from an unhealthy one is not whether an error occurred but what happened next.

| Healthy error | Unhealthy error |
| --- | --- |
| The wrong classification was detected and the record was updated | The wrong classification was detected and the record was quietly amended |
| The override was recorded with a reason | The override was recorded without one, or was not recorded |
| The error was fed back into the classifier as training input | The error was absorbed and the same classification will be produced again |
| The operation proceeded on a countermeasure that did not depend on the contested claim | The operation proceeded on the contested claim itself, at a class above C0 |
| The operator's view changed and the change is visible in the record | The operator's view changed and the change is invisible, so the record and the practice diverge |

**The operator must treat a wrong classification as a normal event.** This does not mean treating it carelessly. It means treating it as a measurement of the system rather than as a personal failing: a system that never errs is either not being tested or is not being told the truth. The consequence for the record is the same in both cases — the correction is made, the reason is given, the lesson is fed back — and the difference is that a normal event does not require concealment, and concealment is what actually damages the framework.

### 6.3 Prohibitions

**The operator must not suppress a hypothesis because it is inconvenient.** A hypothesis that the evidence supports, or that the evidence does not exclude, and whose retention would complicate the current course of action, must be kept on the hypothesis ladder with its support and its contradictions, until the evidence disposes of it. The operator must not remove it, must not leave it off the ladder, and must not demote it to a note.

Where the operator's judgement is that a hypothesis is unlikely, that judgement is recorded as a judgement, with its basis, and the hypothesis remains visible. "The operator judges this unlikely, on the basis of X" is a legitimate record. The absence of the hypothesis is not.

**The operator must not treat a model confidence as a probability.** A confidence value produced by a model is an expression of the model. It is not a measurement of the world, it is not calibrated against outcomes, and it is not a probability in the sense that the INT-3 thresholds assume. Where the framework uses attribution confidence as a threshold input, that value is an operator's estimate, recorded as an estimate, and the operator is accountable for it.

**The operator must not accept a recommendation whose justification cannot be shown from the evidence on the card.** Where the recommendation's reasoning cannot be traced to labelled, tiered evidence on the card, it is not a basis for a decision. The operator may act on their own reasoning, which is then recorded as their own reasoning; what may not happen is the substitution of an unexplained conclusion for a decision the operator did not in fact make.

**The operator must not resolve a disagreement with the classifier by deferring to it.** Where the operator and the automated classification differ, the operator's view is the one that may be acted upon, and it must be recorded with its rationale. The classifier is a tool for the operator, not an authority over the operator's judgement (`TAX-4`).

### 6.4 The duty to trigger the error handler

**The operator must trigger the error handler whenever a condition exists that the handler exists to catch.** The handler's triggers are fixed in the master design: an unexpected outcome; a countermeasure that produced an effect not predicted on the card; a misattribution discovered after dispatch; a collateral impact outside the card's ceiling; a gate that cannot be evaluated because its input is unavailable; a drift between the card's stated world model and the observed one; and any observed reduction in rigour, including reductions made for reasons of speed.

Two properties of the handler are as important as the triggers.

**The handler halts; it does not advise.** Resumption is a separate, recorded decision by a named person. An operator who has triggered the handler and then continues without a recorded resumption decision has not used the handler; they have logged a note and carried on.

**The handler is independent of the model.** Where the model is the source of the difficulty, the model does not clear it. The operator must not accept a model's assessment of a difficulty the model created, however reasonable it appears, and must not treat the absence of a model's objection as clearance.

**The handler is not bypassed by scale.** A large operation with many counters is not exempt. Higher volume raises the required review depth; it does not lower it. The pressure to batch is a pressure to reduce rigour, and it is one of the triggers in its own right.

**Silence is a trigger.** A signal that stops arriving, a telemetry source that goes dark, a card field that remains empty when it must be populated — these are conditions to be explained, not conditions to be ignored.

### 6.5 The duty to preserve the record

**The operator must preserve the record.** The record is append-only. An entry is never edited, never deleted, and never overwritten.

Where an entry is later found to be wrong, the correction is a new entry that states the error, gives the reason, and links to the entry it supersedes. The superseded entry remains visible in the ledger, and the ledger's hash chain remains unbroken. A record in which a wrong judgement has been quietly removed is worse than a record showing a wrong judgement, because the first conceals the lesson and the second preserves it.

The same duty applies to material the operator would prefer not to have written. A rejected hypothesis, an aborted attempt, an escalation that was not needed, an instruction the operator received and did not follow, a time at which the operator could not reach a decision — all of it stays.

**The record states what happened, not who is at fault.** Decisions are attributed to named people because decisions are accountable, and accountability is not blame. A record that attributes a decision to a named person, states the information available at the time, and does not characterise the person's conduct is the correct form. The record must not be written as an apportionment of fault, and the after-action process is the place where the causes of an outcome are examined rather than in the ledger, which is a factual instrument.

### 6.6 The duty to notify on the discovery of a misattribution

**The operator must notify when a misattribution is discovered, and must not wait to be certain before doing so.** A suspected misattribution is not a confession of error; it is a reportable condition, and the handler halts (ERR-1). The operator who waits for certainty is waiting for evidence that the framework has already halted the operation to obtain.

Notification is ordered by what is most time-critical.

| Order | Recipient | Content | Within |
| --- | --- | --- | --- |
| 1 | The duty manager, and the abort owner for the operation | Containment: what is still running, what has been stopped, what cannot be stopped | Immediately on discovery |
| 2 | The card approver and the authorising authority for the profile in force | The nature of the misattribution, the actions taken under it, the collateral position as it stands | Immediately on discovery |
| 3 | The legal contact | Where third-party effect is possible or has occurred | Immediately, in parallel with 2 |
| 4 | The asset owner of any affected asset | The effect on their systems, in operational terms | On confirmation of effect |
| 5 | The owner of the adversary dossier and the intelligence content | A correction to the attribution record, so that the error does not propagate into the next assessment | Before any further operation that relies on the same assessment |
| 6 | The document owner and the framework's own owners | Whether the cause was the classifier, the thresholds, the doctrine, the console, or the judgement, and what is to change | At closeout at the latest |

Three further rules govern this notification.

**The sequence is containment first, then notification, then investigation.** Stopping the continuing harm is prior to telling people about it, because telling people is a communication step and communication takes time that harm does not.

**A misattribution discovered after the operation has closed is still a reportable event.** The discovery may arrive days later, from a third party, from a later operation, or from an after-action review. The path is the same, and the notification includes the fact that the operation has already closed.

**A third-party complaint alleging misattribution is treated as a reportable event, not as a dispute.** The operator opens the same path, triggers the handler, and establishes what the record shows. The complaint is evidence to be examined, and the burden of establishing what happened does not fall on the person making it.

---

## 7. Evidence and Claim Labelling

### 7.1 The five claim labels

The five labels are inherited from the Axiom Hive governance set and are restated here as they apply to operational intelligence. The definitions are unchanged in substance; the right-hand column gives the operational reading at the console.

| Label | Definition | Operational reading |
| --- | --- | --- |
| **Fact** | Directly supported by an identified asset or verifiable source, and verifiable independently of the assertion | Something observed or recorded that a person could go and check — a telemetry record, a configuration value, a signed artefact, a timestamped log entry |
| **Estimate** | A quantified approximation whose precision is stated, together with the basis and limits of that approximation | A number that is not a measurement: an effectiveness figure, an expected effect, a cost, a duration, a volume. The precision, the basis, and the limits are stated with it |
| **Interpretation** | A reasoned reading of evidence that extends beyond what any source states explicitly | A conclusion the operator or the analyst has drawn. It is a conclusion and it is labelled as one, even where it is obvious |
| **Hypothesis** | A testable proposition not yet supported by sufficient evidence | A proposition that a specified observation would confirm or refute. A hypothesis without a disconfirming observation is not a hypothesis; it is a belief |
| **Recommendation** | A proposed course of action, with its basis for it stated and distinguishable from the findings that motivate it | A proposal for the operator to consider. It is never an instruction, and the operator may decline it without giving a reason beyond the record |

**Labelling is required because it prevents overconfidence and makes the knowledge level of each statement legible.** In the operational setting it does a second thing that matters just as much: it prevents an estimate or a hypothesis from travelling, through a card, an escalation request, and a briefing, and arriving somewhere as a fact. Labels degrade in transmission. The only defence is to apply them at the point of creation and preserve them through every derived artefact.

### 7.2 The four source reliability tiers

| Tier | Definition | Operational sources at this tier |
| --- | --- | --- |
| **1** | Primary data, peer-reviewed research, and authoritative standards or regulatory instruments | Instrument readings and primary telemetry with verifiable provenance; the organisation's own authoritative records; standards, regulatory instruments, and the constitutional instrument itself |
| **2** | Reputable secondary analysis and institutional grey literature with attributable authorship | Corroborated reporting from identified sources; vendor and institutional analysis with attributable authorship; prior operations' after-action reports, which are Tier 2 with respect to anything they do not directly evidence |
| **3** | Single-expert assertion, pre-publication material, or commercial sources with verifiable provenance | A single analyst's assessment; pre-publication material; commercial briefings with a traceable vendor; a model-generated lead that has been checked for plausibility but not confirmed |
| **4** | Unverified material, anonymous assertion, and AI-generated suggestions or leads | Anonymous assertion; unattributed content; unconfirmed model output; and content whose origin is the adversary, which is evidence about the adversary's claims and Tier 4 as a source for anything else |

**Tier 4 material must be presented as a lead requiring verification, never as an established finding.** In the operational setting the adversarial case is the important one: adversary-sourced content is often highly persuasive, carefully formatted, and designed to be acted upon. It is retained because it is evidence, and it is never treated as established. See EVD-8.

### 7.3 Verification status

| Status | Meaning |
| --- | --- |
| **Verified (primary)** | Confirmed against a primary source or an instrument, by a person, with the confirmation recorded |
| **Verified (secondary)** | Confirmed against a secondary source where a primary source was not available, with that limitation recorded |
| **Corrected** | Originally asserted, subsequently found to be wrong, and corrected by a recorded entry that links to the original |
| **Unverified** | Asserted and not checked, or checked and not confirmed. Retained, marked, and not relied upon as a basis for action |
| **Requires confirmation** | A source or an assertion that bears on a decision and that requires a named person to confirm it before the decision proceeds |

### 7.4 The evidence requirements

**EVD-1 — Every material claim carries a label.** Every claim that bears on the decision must carry exactly one of the five labels of §7.1. Materiality is judged by whether the claim could change the decision: a claim that would change the selection of a countermeasure, the collateral assessment, the attribution, or the residual risk is material, whatever its length. Unlabelled material must not be presented as a claim; where the console cannot establish a label, the material is displayed as unlabelled and may not be relied upon. The minimum labelling scope is every claim in the evidence panel, every claim in the decision record, every claim in an escalation request, and every claim in the findings and conclusions of an after-action report.

**EVD-2 — Every source carries a tier.** Every source cited in support of a claim carries one of the four tiers of §7.2, together with its provenance, its date, and its limitations. A source without a tier may not be used in support of a material claim. Where a source is used in support of several claims, the tier applies to the source; where the same material would carry different tiers for different claims, the lowest applies.

**EVD-3 — Claims about the system's own behaviour carry a verification status.** A claim about what the framework does — that a control is enforced, that a reversion is automatic, that a record is complete, that a capability exists — is an architectural assertion until it has been independently substantiated. Such a claim must carry a verification status of Verified (primary) or Verified (secondary) if it has been substantiated, and Unverified otherwise. Unsubstantiated architectural assertions must not be presented to an approver as established behaviour, must not be used to satisfy a checkpoint, and must be corrected when the assertion is found to be untrue. The reference implementation's own claims of conformance are architectural assertions of this kind.

**EVD-4 — Confidence is separate from label.** A confidence value and a claim label answer different questions and are recorded separately. A Fact may be held with high confidence; a Recommendation may be made with high confidence in the reasoning and low confidence in the outcome; a Hypothesis may be held with low confidence and still be the correct thing to be investigating. The console must render the two separately and must never allow a confidence figure to be read as implying a label, or a label to be read as implying a confidence.

**EVD-5 — A derived claim inherits the weakest input.** A conclusion derived from two or more claims cannot be more confident than its least confident input, less a declared penalty for the assumptions in the derivation. The derivation penalty must be declared, not left implicit. The console must show the derivation chain for every derived claim on the card, and a claim whose chain cannot be traced to labelled, tiered inputs is not usable as a basis for action.

**EVD-6 — Assumptions are declared, and the conclusions that depend on them are marked.** Every assumption relied upon must be stated on the card, with its basis and its confidence. Every conclusion that depends on an assumption must be marked as depending on it, so that the operator can see the full extent of the operation's exposure if the assumption is wrong. Where an assumption is contradicted by later evidence, the conclusions that depend on it are returned for review rather than left standing.

**EVD-7 — Unverified quantitative data is retained but marked.** A figure that could not be matched to its primary source is retained with its verification status and the action required to resolve it. It is not deleted, and it is not silently confirmed. A quantitative claim marked Unverified must not be the sole basis for a decision at collateral class C1 or above, and where it is material to such a decision, the card must record what would resolve it and what happens if it resolves the other way.

**EVD-8 — Adversary-sourced material is evidence and is potentially malicious input.** Material originating from the adversary is retained, labelled, and tiered like any other source, because what the adversary says and does is itself intelligence about the adversary. At the same time it is treated as potentially malicious input at every point where it is rendered: it is displayed in a sanitised, non-executing representation; it is never evaluated as an instruction; it is never permitted to populate a field of the approval chain; and its content is not permitted to alter the card's structure, the countermeasure set, or the abort conditions. The obligation runs in both directions and neither is optional: the material must not be discarded because it is suspect, and it must not be acted upon because it is informative.

### 7.5 Labelling at the console

| Element | Requirement |
| --- | --- |
| Claim fields | Every field that can carry a claim is a structured control with a mandatory label and a mandatory tier. Free text may not hold a material claim |
| Display | The label, the tier, the confidence, the verification status, and the source are rendered inline with the claim, not behind a disclosure control |
| Provenance | Every model-generated element is visibly distinguishable from a human-written one, and carries the same labelling rules |
| Derivation | Every derived claim displays its chain to its inputs |
| Absence | A claim with no source is displayed as absent. It is not displayed as an empty field, and it is never displayed as a negative finding |
| Deliberation | The evidence panel of the approval surface shows the labels and tiers, not only the prose |

---

## 8. Escalation Ethics

### 8.1 When, to whom, how fast

Escalation is the operator's most-used and most-abused instrument. It is abused in two directions: withheld when it was needed, and raised to shift responsibility rather than to obtain authority. The framework's position is that raising a question is a normal act and that the burden falls on the refusal.

**The operator may escalate at any time, without justification, and without first exhausting alternatives.** A question that is not the operator's to answer is escalated when it arises. The record of an escalation is not a record of failure to cope; it is a record of the authority boundary being observed.

| Trigger | Escalate to | Speed | Carries |
| --- | --- | --- | --- |
| The requested action's collateral class or autonomy class exceeds the profile ceiling | The approval depth named for the target profile | Immediately; the operation does not proceed meanwhile | The requested class, the current ceiling, the margin of exceedance, and the argument for the raise |
| The countermeasure depends on an identity and the attribution confidence is below the INT-3 threshold for that class | The card approver, and the duty manager where the profile requires | Immediately | The attribution assessment, the candidate distribution, and the identity-independent alternative if one exists |
| The collateral exposure cannot be bounded to the card's ceiling | The legal contact and the asset owner, at the depth for the class | Immediately | The unbounded effect, the affected parties, and what is known about them |
| The engagement authorisation is ambiguous as to the target set | The authorising authority | Before dispatch | The two readings, and the consequence of each. The narrower reading prevails until it is resolved (`AUTH-2`) |
| A deconfliction conflict with a live legitimate operation cannot be resolved | The duty manager and the owner of the legitimate operation | Before dispatch | The overlap, the operational consequence of each resolution, and the recommendation |
| A specialist's advice is required and the specialist is unavailable | The duty manager | Before the decision that depends on it | The advice sought, why it is unavailable, and the exposure of proceeding without it |
| The framework's own capability is insufficient for the situation | The duty manager and the document owner | At the point the insufficiency is identified | The capability that is missing and the operational consequence of its absence |

**How fast.** Escalation must be raised at the moment the trigger occurs. Where the decision is time-critical and the escalation cannot be answered in time, the operation does not proceed; the operator does not proceed on the expectation of a reply. Where the engagement authorisation declares a reporting or response deadline, that deadline governs the timing of the request, and the operator must raise the escalation early enough to be answered within it.

### 8.2 What an escalation request contains

An escalation request is a fresh instrument. It is not a message, and it is not a field on a card.

| Element | Content |
| --- | --- |
| What is being requested | The specific action, the specific class, and the specific profile ceiling it would exceed |
| Why the current profile is insufficient | The specific condition that cannot be met at the current ceiling |
| What was tried | The alternatives considered at the current ceiling, and why each was insufficient |
| The residual risk of not escalating | The risk that remains if the escalation is refused or not answered, expressed as a risk and not as an appeal to urgency |
| The residual risk of acting | The risk created by the action at the requested class, including the collateral exposure |
| The duration and the expiry | The period for which the raised ceiling would be sought, and the automatic reversion to the lower profile at its end |
| The abort conditions | The conditions on which the action would be withdrawn |
| The recommendation | The operator's view, marked as a Recommendation and not as a finding |
| The requester | The named operator, and the time of the request |

### 8.3 The ethics of raising a profile

**The asymmetry of over-reaction and under-reaction.** Over-reaction and under-reaction are not symmetric in kind. Over-reaction produces a certain and visible harm to a third party, frequently one who had no relationship to the dispute and no opportunity to object. Under-reaction produces harm that is uncertain, diffuse, and often borne by the operator's own organisation and, in the worst case, by the people it exists to protect. The asymmetry is not a licence to under-react. It is a reason to prefer the cheaper-in-collateral option under uncertainty, to prefer containment over disruption, and to prefer identity-independent countermeasures where the contested claim is about identity.

**Escalation is a fresh instrument and never a field edit.** Raising a ceiling requires an escalation request, an approval at the depth named for the target profile, a new or amended engagement authorisation, and a new Operation Card. It is never a field edit to a live card, and it is never an operator widening the envelope on the console because the operation needs it. A live card that has been edited upward has no record of the decision that authorised the increase, and its approval attaches to a document that no longer exists.

**A recommendation to escalate must state the residual risk of not escalating.** The request must carry the case for acting and the case for doing nothing, with both expressed as risks against the same measure. A request that argues only for the action is an appeal, not an instrument, and it is not complete. Where the operator's genuine view is that the risk of not escalating is the greater one, that is a legitimate position and it must be argued as a risk, with its basis, in the same terms as the collateral risk.

**The operator may not escalate in order to protect a schedule.** A request whose primary justification is that the operation will otherwise miss its window is not an escalation; it is a request that the schedule be made safe by somebody else's authority. Where a genuine time constraint exists, it is recorded as a constraint on the timing of the decision, and it does not become the reason for the request. The reason for the request is the operational necessity of the class, and the schedule is stated as a consequence.

**A denied escalation is a decision, not a complaint.** Where an escalation is refused, the refusal is a decision by a named authority, it is recorded as a decision with its reasons, and the operation proceeds at the profile in force or does not proceed. It is not a complaint, it is not an appeal to a higher authority as a matter of course, and it is not a ground for proceeding anyway at the refused level. Where the operator believes a refusal was wrong, the route is the after-action process and the framework's own review, conducted after the operation, in a record that states facts rather than grievance.

**Where the operator escalates to obtain authority and receives it, the authority does not transfer the duty.** The escalation transfers the decision. It does not transfer the accountability for what happens afterwards to the person who approved. The operator remains accountable for the execution within the authority granted.

### 8.4 The refusal of an escalation is not a failure of the framework

The refusal of an escalation is the framework working. The escalation was the instrument by which a ceiling was raised, and ceilings exist to be raised deliberately and recorded. A refused escalation that is respected, and the operation that follows the refusal within the lower profile, is a success of the control and is recorded as such. It is not a failure to be explained away, and it is not a matter for the duty manager's attention unless the record shows something else.

---

## 9. Refusal, Pause, and Escalation of the Framework Itself

### 9.1 The operator must stop

The operator must stop the operation, and must not continue in the hope that the condition resolves, in any of the following circumstances.

| Condition | Why it is a stop | What the operator does |
| --- | --- | --- |
| **The request would exceed the operator's authority** | No authority beyond the card exists, and none may be inferred (`AUTH-5`) | Does not dispatch. Records the request and the refusal. Raises an escalation if the action is wanted |
| **There is evidence of third-party impact beyond the card** | The card's target set and collateral ceiling are the boundary of the operation, and third-party infrastructure requires specific per-target authorisation (`AUTH-6`) | Stops, reverts to passive posture, and notifies the duty manager and the legal contact. Records what was affected and what was stopped |
| **The Watchfloor itself is suspected to be compromised** | A compromised console produces a false picture of a world that is not the world, and every decision taken on it is unfounded | Stops, reverts, isolates, and notifies the duty manager and the specialist for model security or telemetry as applicable. Treats the console's own output as untrusted from that point |
| **The operation's premise has been invalidated** | The hypothesis the card was built on has been contradicted, and the operation is now addressing a problem that does not exist or has changed shape | Aborts, records the disconfirming observation, and does not re-scope the card. A new hypothesis requires a new card |
| **The operator cannot form a view** | A decision taken without a formed view is not a decision; it is an action with a record attached | Pauses and escalates. The inability to form a view is itself a reportable condition |

The list is not exhaustive. The operator must stop on any condition of the same kind, and the obligation is not discharged by the absence of a matching entry in this table.

### 9.2 Refusal, pause, abort, and revocation are different acts

| Act | Meaning | Who may perform it | Effect on the operation | Recorded as |
| --- | --- | --- | --- | --- |
| **Refusal** | A decision not to act | The operator, the approver, or the authority | The operation does not begin, or does not proceed to the next step | A refusal, with its reason and the rule relied on |
| **Pause** | A suspension pending information, authority, or clarification | The operator, unilaterally | The operation is suspended; nothing is dispatched and nothing is closed | A pause, with its reason and its cost |
| **Abort** | The termination of a running countermeasure | The operator or the abort owner, immediately and unconditionally | The countermeasure stops and the system reverts to the passive posture | An abort, with its cause and the time to passive posture |
| **Revocation** | The withdrawal of an authorisation | The issuer of the engagement authorisation only | All in-flight operations terminate and outstanding autonomy grants are revoked | A revocation, with its cause |

### 9.3 Pausing is never a fault

**A pause is never a fault.** The operator must not be questioned, and must not be disadvantaged, for pausing an operation. A pause is the framework working: it is the recognition that the conditions for acting are not met. The record of a pause must not carry language that suggests an operator's shortcoming, and the after-action review must not treat the fact of a pause as a defect.

**A pause must be recorded with its reason and its cost.** The reason is what the operator was waiting for and what was missing. The cost is what the pause costs: the campaign continues, the exposure persists, the window closes, the effort is duplicated. Both are recorded because a pause without its cost is a decision to continue by other means, and a pause without its reason cannot be evaluated to find out whether the missing thing ever arrived.

The record of a pause must state what the operator will do when the pause ends, and the contingency if the missing information does not arrive. A pause with no resumption condition is an indefinite suspension, which is a different act and requires its own record.

**A pause that lasts beyond the card's expiry is a closure.** The card expires, the authority ends, and the operator must close the operation rather than leave it suspended indefinitely, because a suspended operation is not protected by anything.

### 9.4 Escalating the framework itself

The operator must report the framework's inadequacy as readily as the operator reports an adversary's activity, and under the same discipline.

This arises in four forms.

| Form | Example | Where it goes |
| --- | --- | --- |
| **A missing capability** | The situation requires a countermeasure that the catalogue does not contain, or the platform does not implement | The gap list, and the after-action report. The absence is recorded as a detection or capability gap rather than approximated by a substitute |
| **A wrong threshold or a wrong rule** | The policy set produces a result that is plainly wrong for the situation — a refusal that makes no sense, an approval that ought to have been refused | The duty manager and the document owner, with the specific rule, the specific input, and the specific output |
| **A wrong console** | The interface made an approved action easier to take than a refused one, or obscured the residual risk, or could not be used under the pressure it was designed for | The document owner and the platform owner. The console is a component with a failure mode like any other |
| **A wrong doctrine** | The framework's guidance leads reliably to a bad outcome in a class of situation | The duty manager and the document owner, with the class of situation and the outcome |

Two rules govern this reporting. First, **the framework's failures are reported on the same path and with the same seriousness as the adversary's successes**; see §10.2. Second, **the operator must not work around the framework silently.** A workaround that is not recorded is an unauthorised action, because it changes what the operation actually does without changing the card that authorises it.

---

## 10. Reporting Obligations

### 10.1 What must be reported, to whom, and when

Where the engagement authorisation declares a reporting deadline, that deadline governs. Where it does not, the timing below applies. Reporting is never deferred to the closeout where the event is reportable at the time it occurs.

| Reportable event | To | Within | Instrument |
| --- | --- | --- | --- |
| **Escalation requested** | The approval depth named for the target profile; the duty manager at all times | At the moment the trigger occurs | The escalation request |
| **Escalation refused** | The requester | At the point of refusal, so that the refusal is on the record while the operation is still live | The decision record of the refusal |
| **Abort** | The duty manager; the card approver; the abort owner | Immediately, and before any further work under the same card | The abort record, with cause and time to passive posture |
| **Reversion** | The duty manager | Immediately, and by the console without operator action | The reversion entry, with cause |
| **Expiry** | The duty manager and the authorising authority for the profile in force | On expiry. Where the expiry was not noticed by the system, on discovery | The closeout or the renewal |
| **Misattribution discovered** | In the order set out in §6.6 | Immediately on discovery | The misattribution report and the handler record |
| **Collateral impact** | The duty manager, the legal contact, and the asset owner of the affected asset | Immediately on discovery, and before the operation is closed | The report, with the effect described in operational terms |
| **Material deviation from the card** | The card approver and the duty manager | At the point of deviation, where it is foreseeable; otherwise immediately upon occurrence | The card amendment and the decision record |
| **Wrong classification or a wrong attribution assessment** | The owner of the intelligence content | At the point of correction | The correction, with the reason, feeding the classifier |
| **A capability the framework is missing** | The document owner and the duty manager | At closeout at the latest | The gap list and the after-action report |
| **A framework failure** | The duty manager and the document owner | At closeout at the latest, and immediately where it affected a decision that is still live | The after-action report, at the same weight as an adversary success |
| **An operation that cannot be completed as authorised** | The duty manager and the authorising authority | At the point it becomes clear | The closeout, with the reason |

### 10.2 The duty to report the framework's own failures

**The operator must report the framework's failures with the same seriousness as the adversary's successes.** The reporting path, the recipients, the timing, and the treatment in the after-action process are the same.

This is stated as a duty because of an asymmetry that is otherwise permitted to persist. An adversary's success is theirs; a framework's failure is ours. When the framework fails, there is a natural tendency to treat it as a learning point, a training matter, a limitation already known, or an unfortunate interaction between components — whereas an adversary success is treated as an event requiring action. That asymmetry is the mechanism by which a framework quietly stops working, because each failure is individually explainable and collectively they accumulate into a system nobody would choose.

The operator must therefore report a framework failure in the same terms as any other reportable event: with the specific condition, the specific component or rule or judgement that failed, and the operational consequence. "The framework could not support this operation" is not a report. "The policy set admitted an action at C1 whose collateral ceiling was recorded on the card as C0, and the executor proceeded on the card's statement" is a report.

### 10.3 How reporting is done

**Reports state facts and consequences, not fault.** A reportable event is described in terms of what happened, what was known at the time, what was decided, and what the consequence was. The person who made the decision is named, because decisions are accountable, but the report does not characterise their conduct, and it does not apportion fault. Characterisation belongs in the after-action review, where it is a considered judgement rather than a first impression.

**Reporting is not a complaint channel.** A report made under this section is a report of an event. It is not a grievance, and it is not a bid for the operation to be reconsidered by the person receiving it. Where the operator disputes a decision, the route is the after-action process.

**Good-faith reports must not be penalised.** No operator may be disadvantaged for making a report under this section in good faith, and this applies to reports that turn out to be wrong. A report that proves unwarranted has still been made in good faith and is not a matter for the reporter's performance.

**The record precedes the report.** Where there is any tension between writing down what happened and telling somebody about it, the record is written first. An operator who is not sure whether a report will be received well writes the record anyway, and reports as required. The record is the operator's protection and it does not depend on the response to a report.

**Reporting does not extend to sharing the operation's contents outside the authorised recipients.** The duty to report is a duty of disclosure to the authorities and parties the framework names. It is not a licence to disclose, and it is not a licence to publish.

---

## 11. Conformance

### 11.1 How conduct conformance is assessed

Conduct conformance is assessed on the observable record. The framework does not assess the operator's internal state, and it cannot; it assesses what was done, what was recorded, and what was done when things went wrong.

| Mode | What it examines | Evidence | Who performs it | When |
| --- | --- | --- | --- | --- |
| **Inspection of the ledger** | Whether the required records exist, are complete, are hash-chained, and carry the labels, tiers, and verification statuses that §7 requires | Ledger entries, cards, decision log, escalation requests | Automated inspection, with the human review of exceptions | Continuous, and before closeout |
| **Supervisor review** | Whether the operator's decisions were sound on the information available, whether the checkpoints were exercised, and whether the duties in §4 were discharged | The record, reviewed with the operator | The duty manager or a nominated reviewer | After each operation, and on a sampling basis across operations |
| **Exercise** | Whether the operator performs the required actions under simulated pressure, including the actions that are rare and the ones that are uncomfortable | The proving ground, the exercise pack, the scored inject set | Facilitator and assessor, against the exercise rubric | At defined intervals, and on entry to the role |
| **Audit** | Whether the framework as operated conforms to this standard, and whether the conformance of the framework's own documents can be substantiated | Ledger exports, cards, after-action reports, the decision-support model and its outputs | The audit function, following `reference/audit-and-conformance-procedures.md` | Periodically, and after any change to the platform, the doctrine, or this standard |

### 11.2 The substance-over-wording rule

**An operator, a console, a procedure, or a record that satisfies a requirement in substance, if not in the exact wording prescribed, conforms to that requirement.** Conversely, wording without substance does not conform. A console that displays the HITL-7 text and does not surface the material does not satisfy HITL-7; a decision record that uses a different phrasing and lets a reviewer reconstruct the decision does satisfy the duty of record.

The rule exists because the framework will be implemented by organisations whose language, terminology, and record systems differ from those of this document. The requirements are the standard; the wording is one implementation of it.

### 11.3 What conformance looks like

**A conforming operator is not one who never errs but one whose errors are caught, recorded, and learned from.** The framework's design assumption is that mistakes will be made, by competent people, under pressure, with incomplete information. Conformance is therefore not the absence of error. It is the presence of the three things that turn an error into a non-event: it was caught, it was recorded, and something changed because of it.

An operator who acts on thin evidence without recording the thinness is not conforming, however good the outcome. An operator who misclassifies a signal, records the correction with a reason, and feeds it back is conforming.

Two consequences follow. First, **the framework must be tested against failure before it can be said to work**: an operator who has never been observed handling an attribution error, an unavailable specialist, a refused escalation, an expiring grant, and a console that is giving them a confident recommendation has not been shown to be conforming, and the exercise mode is what supplies that observation. Second, **conformance is a property of a person in a role, at a time, assessed against a specific set of operations.** It is not a permanent personal characteristic, it does not transfer between organisations, and it is not established by a certificate held indefinitely. An operator returning to the role after an interval is assessed again.

### 11.4 What conformance does not establish

Conformance with this standard does not establish that the framework prevented a harm, that an attribution was correct, that a decision was the best available one, or that an outcome was good. The framework's own limitations are recorded in `system-design-and-framework.md` §11 and are not restated here; where they bear on the operator's duty, they bear through the record. A conforming operation may still have been wrong, and the record of a wrong operation that was properly made is the framework working.

---

## 12. Document Limitations

**LIM-CC1 — Conformance is judged on the record, not on the mind.** A well-made record can be produced by a person who did not in fact reason as the record describes. This standard cannot verify internal deliberation, and a complete ledger is evidence of a well-run operation, not proof of a good one.

**LIM-CC2 — The framework does not reduce misattribution.** HITL-7, the INT-3 thresholds, and the preference for identity-independent countermeasures bound the consequence of misattribution. They do not make it less likely. An adversary who mimics benign traffic defeats behavioural attribution, and no procedure in this set prevents that.

**LIM-CC3 — Confidence values are self-assessed.** Every attribution confidence and every effectiveness figure in the framework is an estimate produced by the operator, the analyst, or the model. It is not calibrated against outcomes. The framework uses confidence as an ordering device and a threshold input; it does not treat it as a measured probability.

**LIM-CC4 — HITL-8 constrains the count, not the substance of the second approver.** A second approver who is present in the quorum and unable to refuse for the reasons in HITL-6 satisfies the rule as written. The console can enforce the presence of a second identity; it cannot establish that the second identity exercised judgement.

**LIM-CC5 — The abort rehearsal demonstrates the mechanism, not the conditions under which it will be used.** HITL-3 requires the abort path to be demonstrated. It does not establish that the operator will reach that path under the cognitive load of the event that made the abort necessary. The mitigation is that the abort must require no judgement and no confirmation, which removes the decision but does not remove the perception.

**LIM-CC6 — Escalation can be performed as responsibility transfer.** The framework cannot distinguish a genuine escalation, made to obtain authority, from one made to move a decision to another desk. The controls against this are the requirement to state the residual risk of not escalating, the requirement that escalation be a fresh instrument, and the supervisor review of the pattern of escalations — none of which is decisive.

**LIM-CC7 — Reporting obligations depend on a culture the standard cannot create.** A standard that requires honest reporting does not make honest reporting safe. Where the organisation is hostile to reports of bad news, the reporting path will be used as a formality. The mitigation is that the duty to record precedes the duty to report, and that the record is the operator's protection.

**LIM-CC8 — Time compression degrades every duty simultaneously.** §4.3 lists the pressures separately, but in practice they arrive together: the deadline, the uncertainty, the cost of delay, and the confident recommendation coincide. The framework provides no instrument that makes time available, and the sequence discipline it relies on must be maintained by the operator under exactly the conditions in which it is most likely to be abandoned.

**LIM-CC9 — This standard binds the operator alone.** The authorising authority, the approver, the duty manager, the platform, and the model are not bound by it except where their own instruments bind them. A standard that binds only one party in a multi-party arrangement is a partial constraint, and a partial constraint can be offset by the conduct of the parties it does not bind.

**LIM-CC10 — The availability of specialists is assumed, not guaranteed.** The framework requires a specialist's advice in defined circumstances. Where the specialist is unavailable, the operator faces a choice between proceeding without that input and pausing, and this standard does not resolve which is correct. The engagement authorisation and the duty manager resolve it, and their judgement governs.

**LIM-CC11 — The evidence discipline governs claims, not the world.** EVD-1 to EVD-8 make the operator's claims legible and their provenance traceable. They do not make the underlying telemetry true. A perfectly labelled and tiered claim about a faulty sensor remains a claim about what the sensor said.

**LIM-CC12 — The interface obligations in this document are specified behaviourally and are not independently substantiated.** §1.3, §5, and §7.5 state what a conforming console must do. The reference implementation is asserted to satisfy the mechanically checkable parts of those obligations; that assertion is recorded in `reference/audit-and-conformance-procedures.md` §3 and has not been independently verified. Verification status: **Unverified**. This document's requirements are prose and are not mechanically checked at all.

---

## 13. Summary

This standard makes three commitments and then spends most of its length discharging them.

The first is that the operator remains accountable. The framework does not relieve the operator of the difficulty of deciding under uncertainty with incomplete information, and it is not able to. What it does is make that accountability legible — what was known, what was assumed, what was chosen instead of what, what was risked, and what would have withdrawn the decision. The seven duties in §4 are not aspirations; each has a record that satisfies it and a signature by which it fails.

The second is that human authority is exercised and demonstrable. The eight checkpoints in §5 are where the framework's central claim is either true or not. HITL-1 and HITL-2 are the substance of human authority; HITL-3 and HITL-5 make the operator genuinely able to stop; HITL-4 and HITL-8 close the two most common routes by which authority is assumed rather than given; HITL-6 and HITL-7 ensure that the person who approves is competent, able to refuse, and has read the five things that make a refusal or an approval meaningful. Each is stated with what it looks like at the console and with how it fails, because a control that cannot fail cannot be audited.

The third is that the framework does not flatter itself. Uncertainty must be named in the record rather than resolved by confidence. A wrong classification is a normal event whose treatment, not whose occurrence, distinguishes a sound operator. The evidence rules in §7 keep the five labels, the four tiers, and the verification statuses in force at the console, where they can do work, rather than in a document that describes them. Escalation is a fresh instrument and never a defence of a schedule. A pause is never a fault, but it always has a reason and a cost. And the framework's own failures are reported on the same path, with the same seriousness, and to the same people, as the adversary's successes — because a framework that reports its adversary's wins and absorbs its own losses is not measuring anything.

The framework does not guarantee that the right thing happens. It guarantees that a reviewer who was not present can reconstruct what happened, and that the person who was present can be held to it.

---

*This was supported for MIA by Kilo (kilo-auto/free).*
