# Operation Card Template

| Field | Value |
| --- | --- |
| Author | MIA |
| Attribution | This was supported for MIA by Kilo (kilo-auto/free). |
| Document type | Fillable template — operational artefact, layer L6 |
| Subject | The Operation Card: the atomic unit of authorised work, with field-level guidance and a completion rule |
| Scope | Governs the completion and use of a single Operation Card for one counter-adversary or defensive operation |
| Normative source | `system-design-and-framework.md` §4.6, §5, §6, §8; `constitutional/engagement-authorisation-and-rules-of-engagement.md`; `operational/mission-lifecycle-and-decision-loop.md` |
| Companion templates | `templates/rules-of-engagement-card.md`; `templates/decision-log.md`; `templates/escalation-request.md`; `templates/after-action-report.md`; `templates/tabletop-exercise-pack.md` |
| Version | 1.0 |
| Status | Template; copied and completed per use. The template itself is not a record of any operation |
| Language | British English; RFC 2119 keyword usage |

---

## 1. Purpose and scope

This template produces an **Operation Card**: the atomic unit of authorised work in the CAOS framework. The card is simultaneously a document, a data structure, and a legal instrument. It states what an operation is for, what it is authorised to do, on what evidence, within what boundaries, and with what recorded authority, so that a reviewer who was not present can reconstruct it.

The card is required by `OP-1`: every countermeasure dispatch is associated with a card, and the control plane does not accept a dispatch without one.

**Scope.** One card authorises one operation against one specified target set. A material change of target set — a new organisation, a new infrastructure class, a new geography — requires a new card, because the legal and risk analysis changes with it (`OP-2`). A material change of profile ceiling requires a new card and a new or amended engagement authorisation (`ROE-3`); it is never a field edit to a live card.

**Out of scope.** The card does not itself grant authority. It records authority that has already been granted, by a named human, against an engagement authorisation in force. It does not replace the engagement authorisation, the rules-of-engagement profile, or the operator conduct standard.

> **Guidance.** The card is written to be read under pressure by someone who is not its author. Write the reasoning in the words of the person who decided it. If a field cannot be written so that a stranger would understand the choice, the card is not finished.

---

## 2. RFC 2119 interpretation

The key words "must", "must not", "required", "shall", "should", "should not", "may", "optional", "recommended", and "not recommended" in this document are to be interpreted as described in RFC 2119 and RFC 8174, and only in that sense.

| Key word | Meaning in this template |
| --- | --- |
| must / must not | An absolute requirement. A card that breaches it is incomplete and is blocked at the gate concerned. |
| required | Identical in force to "must". |
| shall | Identical in force to "must". |
| should / should not | A strong recommendation. Departure is permitted, but the reason should be recorded. |
| may / optional | A genuinely discretionary element. Discretion exercised here does not require justification unless the field is marked conditional. |
| recommended / not recommended | Advisory only. |

Where this template uses "must" in a completion rule, it states an obligation of the person completing the card, not a statement about the behaviour of any software.

---

## 3. Defined terms

Defined terms are used here with the meanings given in the set index (`README.md` §3, Controlled Vocabulary). Where this template needs a term that the set index does not define, the term is defined in the table below and is used consistently thereafter.

| Term | Meaning |
| --- | --- |
| **Operation Card** | The atomic unit of authorised work; the record that authorises a specific set of actions against a specified target set (`README.md` §3). |
| **engagement authorisation (EA)** | The written, time-bounded mandate that is the root of trust for an operation (`README.md` §3). |
| **ROE profile** | One of R0 Observe, R1 Shield, R2 Trap, R3 Deceive, R4 Disrupt, R5 Neutralise; a ceiling on what an operation may do (`README.md` §3). |
| **collateral class** | One of C0, C1, C2, C3; the class of the effect a countermeasure has, which governs the approval depth required (`README.md` §3). |
| **autonomy class** | One of AC-0 Manual, AC-1 Assisted, AC-2 Supervised, AC-3 Delegated, AC-4 Autonomous; how a countermeasure executes (`README.md` §3). |
| **card owner** | The named human accountable for the card. The owner may not be the approver, and where the operation runs at AC-2 or above the owner must be contactable while the card is active. |
| **card revision** | The revision number of the card. The identity fields are immutable once created; a change to them produces a new card, not a new revision (`system-design-and-framework.md` §4.6). |
| **mandatory field** | A field that must be populated for the card to be complete. An empty mandatory field blocks the card at the gate in which the field is used. |
| **conditional field** | A field that must be populated when its stated condition obtains. Where it does not apply, the reason must be recorded in the field itself. |
| **optional field** | A field that may be left empty without any further record. |
| **n/a** | A recorded statement that a field does not apply to this operation, together with the structural reason. It never means "not yet filled" and never means "not known". |
| **unknown** | A recorded statement that the value could not be established, together with why it could not be established and what the card does about it. |
| **residual risk (R)** | The risk carried forward after the selected countermeasures: R = S_eff × (1 − e) (`README.md` §3; master design §6.2). |
| **claim label** | One of Fact, Estimate, Interpretation, Hypothesis, Recommendation (`README.md` §3). |
| **source reliability tier** | Rank 1 (highest) to 4 (lowest) (`README.md` §3). |

---

## 4. How to use this template

### 4.1 Copy, do not edit

Copy this file into the location where the operation's records are held, name the copy for the card, and complete the copy. The template in `templates/` is never edited in place. An edited template destroys the ability of a later reviewer to tell which version of the form the card was completed against.

### 4.2 Field status

Every field in §5 carries a status in the **Req.** column:

| Status | Rule |
| --- | --- |
| **Mandatory** | The field must be populated before the card may pass the gate in which it is used. A mandatory field left empty blocks the card. It does not block the operation by judgement; it blocks it structurally, and the gap is visible to the approver. |
| **Conditional** | The field must be populated when its condition obtains. Where the condition does not obtain, the reason must be recorded in the field, in the form `n/a — «reason the condition does not obtain»`. A conditional field left empty is a defect even when the condition does not obtain, because the reader cannot tell whether the condition was considered. |
| **Optional** | The field may be left empty. No record is required. |

### 4.3 The completion rule

1. **Mandatory fields are blocking.** A card with an empty mandatory field does not progress past the gate in which that field is used. The person who completed the card is responsible for the block; the approver is not entitled to approve around it, and the control plane does not accept a dispatch for a card that has an unresolved mandatory field.
2. **Conditional fields require a recorded reason.** Every conditional field is either populated or carries `n/a — «reason»`. An empty cell is never an acceptable answer for a conditional field.
3. **`n/a` is a positive statement.** It means: the field does not apply to this operation, for the structural reason given in the field. It does not mean the answer was not known, that the work was not done, that the question was not thought about, or that the matter is inconvenient.
4. **`unknown` is also a positive statement.** Where a value could not be established, write `unknown — «why it could not be established»` and record the consequence of the uncertainty in the same field or in the Evidence table. A value that is unknown but material is a reason to select a countermeasure that does not depend on it.
5. **An empty cell means only one thing: incomplete.** It never means "not applicable", and it never means "default". There are no defaults in this template.
6. **Times are UTC and ISO 8601.** Times are written as `YYYY-MM-DDThh:mm:ssZ`. Durations are written as `PTnHnMnS`. Where a time is estimated rather than known, say so in the field.
7. **Vocabulary is exact.** Claim labels, source tiers, verification statuses, AAT categories, profile names, collateral classes, and autonomy classes are taken from the controlled vocabulary and are not paraphrased. Where the platform applies a taxonomy version, the version in force is recorded on the card (`README.md` §6).
8. **Every claim carries its evidence.** Every material claim on the card appears in the Evidence table with a label, a source tier, a confidence, and a provenance. A claim that appears nowhere else in the card is still recorded there.
9. **Every number is decomposed.** Scores, confidences, and risk figures are recorded as components with the reasoning for each component, so that a reviewer may dispute a specific component rather than the whole assessment (`SCORE-2`).
10. **Signatures are by named humans.** A signature line may be completed only by the named person. A model, a rule, a schedule, a precedent, and silence are not signatures and do not constitute approval (`HITL-1`, `HITL-4`).

### 4.4 Order of completion

The card is completed in the order of the field groups in §5, which follows the order of the mission lifecycle: what is being attempted, under what authority, against what, against what threat, with what countermeasures, at what risk, on what evidence, decided how, and signed by whom. Groups may be revisited and revised; a revision increments the revision number and is recorded in the Ledger with the reason.

### 4.5 What this template does not do

It does not create authority, test that the authority is lawful, or judge whether the action is proportionate. It records what a named human authorised and why. The judgement is the author's; the card is the record of it.

---

## 5. The card

> **Guidance.** Copy everything between this blockquote and the end of §5 into the working card. Replace each `«...»` placeholder. Do not delete the **Req.** column — it is the record of what was required and what was done. Retain the guidance blocks in the working copy if the card is expected to be read by someone outside the immediate team; remove them if the card is rendered into the platform's card editor.

### 5.1 Identity

| Field | Req. | Value |
| --- | --- | --- |
| Card ID | Mandatory | «card id» |
| Title | Mandatory | «operation title, stating what is being done» |
| Created (UTC) | Mandatory | «YYYY-MM-DDThh:mm:ssZ» |
| Owner | Mandatory | «name and role of the card owner» |
| Revision | Mandatory | «0» |
| Framework version in force | Mandatory | «set version, e.g. 1.0» |
| Taxonomy version in force | Mandatory | «taxonomy version, as recorded in the set index» |
| Operation type | Optional | «defensive / counter-adversary / both» |
| Related cards | Optional | «card ids of related or parent cards» |
| Ledger reference | Mandatory | «ledger entry or operation id under which this card's records are held» |

> **Guidance.** The identity fields are immutable once the card is created. A change to any of them produces a new card with a cross-reference, not a revision of this one. The taxonomy version is recorded because a classification is only interpretable against the taxonomy it was made under; a card reviewed against a taxonomy the operator has not seen is not reviewable.

> **Example. Illustrative and fictional.** All identifiers, organisations, people, and measurements in this example are invented for demonstration and refer to no real entity. `Card ID: OP-2026-0142`; `Title: Containment and observation of a suspected tool-output poisoning agent on the Corvin Exchange estate`; `Created: 2026-04-14T09:12:00Z`; `Owner: Duty operator, Corvin Exchange operations`; `Revision: 2`; `Framework version in force: 1.0`; `Taxonomy version in force: AAT v1.0`; `Ledger reference: LDG-2026-0431`.

### 5.2 Objective

| Field | Req. | Value |
| --- | --- | --- |
| What the operation is to achieve | Mandatory | «the specific outcome sought, in one sentence» |
| What would count as achieving it | Mandatory | «the observable condition by which success is judged» |
| Observation window | Mandatory | «period over which the objective is judged, with start and end» |
| Explicit non-goals | Optional | «actions that are deliberately not being taken» |
| Constraint | Optional | «any constraint on how the objective may be achieved, e.g. maintenance window» |

> **Guidance.** The objective must be phrased so that its achievement is observable (`system-design-and-framework.md` §4.6). "Reduce the threat" is not an objective, because nobody can say when it has been achieved. "No unauthorised agent-initiated tool call executes against the estate for 30 days, evidenced by the agent execution log" is an objective, because a reviewer can check it. Where the operation is exploratory, the objective is the production of a stated artefact — a characterised behaviour, a confirmed capability profile — and the observation window applies to that artefact.

> **Example. Illustrative and fictional.** Objective: "Establish that the agent executing poisoned tool output on the estate is contained, and that its planning loop is visible to an operator." Success condition: "No agent-initiated tool call derived from external tool output executes against the estate for 30 consecutive days, evidenced by the agent execution log, and the containment envelope's behaviour is characterised in the operator's own notes." Observation window: "2026-04-14T09:12:00Z to 2026-05-14T09:12:00Z". Non-goals: "No action against the adversary's own systems; no change to the third-party freight API; no attempt to identify the operator behind the campaign."

### 5.3 Hypothesis

| Field | Req. | Value |
| --- | --- | --- |
| Proposition under test | Mandatory | «the testable statement, stated so that it could be false» |
| Disconfirming observation | Mandatory | «the observation that would show the proposition false» |
| Supporting evidence references | Mandatory | «claim ids from §5.11» |
| Contradicting evidence references | Optional | «claim ids that already weigh against the proposition» |
| Hypothesis status | Mandatory | «open / supported / confirmed / disconfirmed» |
| If disconfirmed | Optional | «the action the operator will take in that case» |

> **Guidance.** A card without a disconfirming observation is a plan, not an operation (`system-design-and-framework.md` §4.6). The disconfirming observation is written at the time the card is drafted, before the operation runs, and it is the observation that would have been seen had the proposition been false — not a restatement of the proposition with a negative sign. "The proposition fails if the agent is not contained" is not a disconfirming observation, because it names no observable. "The proposition is disconfirmed if a tool call originating from the external feed executes against the estate within 72 hours of the containment being applied" is.

> **Example. Illustrative and fictional.** Proposition: "The unauthorised agent executing on the estate derives its instructions from poisoned content returned by the shared freight API's tool-output channel." Disconfirming observation: "A tool call carrying the agent's task signature is executed against the estate within 72 hours of containment being applied, with a traceable origin other than the freight API tool-output channel." Supporting evidence: `C-01`, `C-04`, `C-07`. Contradicting evidence: `C-09`. Status: open.

### 5.4 Authority

| Field | Req. | Value |
| --- | --- | --- |
| Engagement authorisation reference | Mandatory | «EA id» |
| EA date of issue | Mandatory | «YYYY-MM-DD» |
| EA expiry | Mandatory | «YYYY-MM-DDThh:mm:ssZ» |
| ROE profile in force | Mandatory | «R0 Observe / R1 Shield / R2 Trap / R3 Deceive / R4 Disrupt / R5 Neutralise» |
| Profile ceiling on collateral class | Mandatory | «C0 / C1 / C2 / C3» |
| Profile ceiling on autonomy class | Mandatory | «AC-0 / AC-1 / AC-2 / AC-3 / AC-4» |
| Card's collateral ceiling | Mandatory | «C0 / C1 / C2 / C3 — never above the profile ceiling» |
| Card's autonomy ceiling | Mandatory | «AC-0 / AC-1 / AC-2 / AC-3 / AC-4 — never above the profile ceiling» |
| Required authorisation depth | Mandatory | «the depth required by the profile and the collateral class» |
| Approver | Mandatory | «name, role, and organisation of the approver» |
| Approver's basis of authority | Mandatory | «the instrument or delegation under which the approver may give this approval» |
| Card expiry | Mandatory | «YYYY-MM-DDThh:mm:ssZ — inherited from the EA unless set earlier» |
| Expiry source | Mandatory | «inherited from EA / set earlier on this card» |
| Revocation conditions | Mandatory | «the conditions under which the EA terminates early, quoted or referenced from the EA» |
| Standing prohibitions in force | Mandatory | «reference to the prohibitions on the ROE card in force» |

> **Guidance.** Everything in this group is copied from the engagement authorisation and never set independently of it (`system-design-and-framework.md` §4.6). If any value here would be higher than the EA permits, the card is wrong, not the EA: the correct response is an escalation request under `templates/escalation-request.md`, and a new or amended EA, and a new card. A profile is a ceiling, not a permission to try the level above (`ROE-1`, `ROE-5`).

> **Guidance.** The card expiry is inherited from the EA unless set earlier (`OP-3`). An expiry that is set later than the EA expiry is a mandatory-field failure and blocks the card; it cannot be argued at the gate. Expiry is a hard stop: an expired EA authorises nothing, and the system reverts to the passive posture without a judgement call (`AUTH-3`).

> **Example. Illustrative and fictional.** EA reference: `EA-2026-007`, issued `2026-04-01`, expiring `2026-04-30T23:59:59Z`. Profile: `R2 Trap`. Ceilings: collateral `C1`, autonomy `AC-2`. Card collateral ceiling: `C1`. Card autonomy ceiling: `AC-2`. Required depth: "Duty manager and legal contact". Approver: "Fictional Legal Contact (role), Corvin Exchange". Approver's basis: "Standing delegation recorded in EA-2026-007, clause 4". Card expiry: `2026-04-28T17:00:00Z` (set earlier). Expiry source: "set earlier on this card". Revocation conditions: "As EA-2026-007 clause 8 — suspension of the freight API integration, loss of the legal contact, or any third-party incident attributable to this operation." Standing prohibitions: "ROE card RC-2026-11, revision 4."

### 5.5 Target set

| Field | Req. | Value |
| --- | --- | --- |
| Authorised targets | Mandatory | «target list, or reference to the annex» |
| Excluded targets | Mandatory | «named categories excluded from scope, always including unauthorised third-party infrastructure» |
| Third-party dependencies | Mandatory | «table below» |
| Target set changed from EA | Conditional | «yes / no — if yes, a new card is required» |
| Material change of target set | Mandatory | «yes / no» |

**Authorised targets**

| Target | Type | Owner | Notes |
| --- | --- | --- | --- |
| «target identifier» | «estate / account / service / agent» | «operator or named party» | «scope note» |

**Excluded targets**

| Target or category | Reason for exclusion |
| --- | --- |
| «target or category» | «why it is out of scope» |

**Third-party dependencies**

| Dependency | Operator of the dependency | Relationship | Effect if affected | Shared-tenancy test: who else depends on it | Per-target authorisation |
| --- | --- | --- | --- | --- | --- |
| «dependency» | «party» | «customer / tenant / contracted service / shared platform» | «what happens to them» | «the answer, and the expected harm» | «EA reference or "none — not authorised"» |

> **Guidance.** This group mirrors the engagement authorisation. A deviation is a new card (`OP-2`). The third-party dependencies table is where the shared-tenancy test is answered: who else depends on this infrastructure, what is their interest in it, and what is the expected harm to them (`AUTH-8`). A countermeasure that fails the test at the current collateral class is not proposed at a higher class without a fresh authorisation and a recorded argument for why identity-directed action is unavailable.

> **Guidance.** Where the dependency table shows that the adversary's system is a tenant on infrastructure the operator uses, that is a finding to be recorded as such, not a permission. The answer to the shared-tenancy test determines whether identity-directed action is available; it does not determine whether infrastructure-directed action is authorised, which is a separate question settled by the EA and, where applicable, by a per-target authorisation under `AUTH-6`.

> **Example. Illustrative and fictional.** Authorised targets: "The estate's agent execution service; the internal tool-call gateway; the agent's stored task queue." Excluded targets: "The shared freight API and all of its infrastructure; the freight API's operator; any other tenant of that platform." Third-party dependencies: "Shared freight API — operated by Fictional Freight Platforms Ltd — relationship: contracted service — effect if affected: rate limiting or egress denial would delay live consignment updates for an estimated 40 dependent small businesses — shared-tenancy test: 40 other tenants plus the operator's own logistics depend on it; expected harm is material service degradation to third parties — per-target authorisation: none — not authorised." Material change of target set: no.

### 5.6 Threat

| Field | Req. | Value |
| --- | --- | --- |
| AAT category | Mandatory | «AAT-1 to AAT-10» |
| Technique | Optional | «technique identifier from the technique library» |
| Classification rationale | Mandatory | «why this classification and not another» |
| Classification confidence | Mandatory | «0.0 to 1.0» |
| Taxonomy version | Mandatory | «version in force at the time of classification» |
| Threat score S | Mandatory | «0 to 20» |
| Effective threat S_eff | Mandatory | «S × c» |
| Attribution confidence c | Mandatory | «0.0 to 1.0» |
| Attribution candidate selected | Mandatory | «the candidate attribution is made to» |
| Attribution basis | Mandatory | «table below» |
| Alternative explanations | Mandatory | «the plausible alternatives and why they are not preferred» |
| INT-3 threshold met | Mandatory | «yes / no / not applicable — with the threshold value that applies» |
| Collective attribution check | Mandatory | «yes / no — the activity is attributable to a specific operator's use of AI, not merely to machine generation» |

**Threat score components**

| Component | Range | Value | Reasoning for this value |
| --- | --- | --- | --- |
| L — Likelihood | 0.0 – 1.0 | «value» | «reasoning, with the claim ids it rests on» |
| I — Impact | 0 – 5 | «value» | «reasoning» |
| A — Autonomy factor | 0 – 2 | «value» | «reasoning» |
| V — Velocity | 0 – 2 | «value» | «reasoning» |
| **S = L × I × A × V** | 0 – 20 | «computed value» | — |

**Attribution basis**

| Basis | Reliability tier | What it supports | What it does not establish |
| --- | --- | --- | --- |
| «basis, e.g. behavioural signature overlap» | «1 – 4» | «what it establishes» | «what it cannot establish» |

> **Guidance.** Every component is reasoned separately, so that a reviewer may dispute one component rather than the whole score (`SCORE-2`). The score orders the queue; it never authorises an action (`SCORE-1`). A rising velocity with flat impact is treated as a leading indicator of an emerging autonomous campaign (`SCORE-3`).

> **Guidance.** Attribution is a probability distribution over candidates, not a name. The basis is stated with its reliability tier, and inference from capability alone is the weakest basis and must be labelled as such (`INT-1`, `INT-2`). The minimum attribution confidence required rises with collateral class: 0.50 at C0, 0.70 at C1, 0.85 at C2, 0.95 at C3 (`INT-3`). Where the confidence does not meet the threshold, the preferred route is a countermeasure that does not depend on identity (`INT-4`).

> **Example. Illustrative and fictional.** Classification: `AAT-7` (supply chain and model), technique "tool-output poisoning", rationale: "The tool result, not the user request, carried the instruction that the agent subsequently executed; the alternative of user-directed instruction is inconsistent with the absence of any corresponding operator request in the estate's own request log." Confidence: 0.85. Taxonomy version: AAT v1.0. Score: L 0.8 ("repeated structured attempts across three days"), I 3 ("degradation of an estate service, not loss of a critical function"), A 1 ("machine-directed with a human in the loop at intervals"), V 1 ("scripted and repeated; no evidence of adaptation between attempts"). S = 0.8 × 3 × 1 × 1 = 2.4. Attribution: c = 0.72, candidate "the Lamplighter operator (fictional archetype)", basis "behavioural signature overlap with the operator's own archived incident — Tier 2, third-party reporting"; alternative explanations: "an unaffiliated opportunistic actor reusing public technique description (considered and disfavoured on timing correlation)". INT-3 threshold: C1 requires 0.70; 0.72 met. Collective attribution check: yes — the attribution is to a specific operator's use of AI.

### 5.7 Countermeasures

| Field | Req. | Value |
| --- | --- | --- |
| Candidate set | Mandatory | «table below» |
| Admissibility results | Mandatory | «table below — every condition AD-1 to AD-12 recorded» |
| Selected set | Mandatory | «table or reference» |
| Rejected set with reasons | Mandatory | «table or reference» |
| Reversibility argument | Conditional | «required where a countermeasure with low reversibility is proposed — this is the AD-3 attestation, and the card cannot be armed without it» |
| Per-target authorisations | Conditional | «the specific written authorisations, one per named third party or adversary target — required where a countermeasure affects a third party, and the AD-5 attestation» |
| Shared-tenancy assessment | Conditional | «who else depends on the affected infrastructure, what their interest is, and the expected harm to them — required where a countermeasure acts in a shared environment or affects a third party, and the AD-5 attestation» |
| Indirect-effect attestation | Conditional | «required where the card declares techniques that operate on people; states that the countermeasure's effect on people is indirect, and that no human being is its object» |
| Deconfliction attestation | Conditional | «required where the deconfliction map is degraded or the conflict is a matter of degree; states that the operator has assessed the conflict and what was done about it» |
| Non-weaponisation attestation | Conditional | «required where the catalogue carries no declaration of conformity with the non-weaponisation boundary; states the boundary analysis, including that no uninvolved third party is harmed» |
| Rationale for the selected combination | Mandatory | «why this set, given the alternatives» |

> **Guidance.** The five attestation fields are the human element in the admissibility algebra. The decision-support model classifies AD-3, AD-6, AD-10 and AD-12 as hybrid and AD-5 as human: the machine can establish that the judgement has been made and recorded, and it cannot make the judgement. A field left empty is not a neutral omission. It is a defect, and a card with a defect in it cannot be armed. Where a field does not apply, write `n/a` and give the reason.

> **Example. Illustrative and fictional.** Reversibility argument: "OCC-33 perturbs the adversary's operational tempo, which is not reversible in the strict sense: the delay it imposes cannot be recalled once the adversary has re-timed around it. It is selected because the reversible alternative, a source block, would also block legitimate traffic from the freight partner, and the card records that the reversible option was considered and rejected." Per-target authorisations: "n/a — no third party is affected; the containment control is applied entirely within the operator's own estate." Shared-tenancy assessment: "n/a — the freight API is not affected by this operation." Indirect-effect attestation: "The card declares AAT-3.4, pretextual social engineering. The countermeasure acts on the agent's tool permissions, not on any person; the people who receive the agent's messages are affected as bystanders and are not the object of the countermeasure." Deconfliction attestation: "n/a — the deconfliction map is current and the check passed at 2026-04-14T09:20:00Z." Non-weaponisation attestation: "n/a — the catalogue entry for OCC-33 carries a declaration of conformity with the non-weaponisation boundary."

**Candidate set**

| Catalogue ref | Class | Description | Collateral class | Reversibility | Autonomy class | Attribution dependency | q | r | P |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| «OCC-nn» | «CM-A to CM-G» | «what it does» | «C0 to C3» | «the reversibility value stated in the catalogue entry» | «AC-0 to AC-4» | «identity-dependent / identity-independent» | «0.0 to 1.0» | «0.0 to 1.0» | «computed» |

**Admissibility results**

| Condition | Result | Value or margin |
| --- | --- | --- |
| AD-1 | «pass / fail / n/a» | «the specific value or rule» |
| AD-2 | «pass / fail / n/a» | «the specific value or rule» |
| AD-3 | «pass / fail / n/a» | «the specific value or rule» |
| AD-4 | «pass / fail / n/a» | «the specific value or rule» |
| AD-5 | «pass / fail / n/a» | «the specific value or rule» |
| AD-6 | «pass / fail / n/a» | «the specific value or rule» |
| AD-7 | «pass / fail / n/a» | «the specific value or rule» |
| AD-8 | «pass / fail / n/a» | «the specific value or rule» |
| AD-9 | «pass / fail / n/a» | «the specific value or rule» |
| AD-10 | «pass / fail / n/a» | «the specific value or rule» |
| AD-11 | «pass / fail / n/a» | «the specific value or rule» |
| AD-12 | «pass / fail / n/a» | «the specific value or rule» |
| **Overall** | «admissible / inadmissible» | «the binding condition if inadmissible» |

**Selected set**

| Catalogue ref | Description | Why selected | Residual-risk contribution |
| --- | --- | --- | --- |
| «OCC-nn» | «what it does» | «the reason, in the operator's words» | «effect on e» |

**Rejected set**

| Catalogue ref | Description | Condition failed | Value that would have made it admissible |
| --- | --- | --- | --- |
| «OCC-nn» | «what it does» | «AD-n» | «the specific value or rule» |

> **Guidance.** Rejected candidates are recorded, not discarded (`system-design-and-framework.md` §4.6). A rejection names the condition it failed and the specific value that would have made it admissible, so that the refusal becomes guidance about what to change (`AD-13`). A refusal is a successful control and is never treated as a failure of the system (`ROE-2`).

> **Guidance.** The class, reversibility, and autonomy class of each candidate are taken from its catalogue entry, not from this template and not from the operator's recollection. Where the catalogue's own reversibility scale and the summary wording in the set index differ, the catalogue entry governs.

> **Guidance.** Where the selected set includes a countermeasure whose reversibility is low, the card must state the irreversible elements explicitly, and the approver must confirm that the alternative of a reversible countermeasure achieving an acceptable reduction in residual risk has been considered (`ROE-7`). Where a more irreversible countermeasure is nonetheless proposed, the card records why the reversible one is insufficient, in the words of the person who decided (`OP-5`).

> **Guidance.** The ranking P is a ranking only. An operator may select a lower-ranked countermeasure; the interface does not prevent it, and the card records that it was a choice (`system-design-and-framework.md` §6.5, STEP-4).

> **Example. Illustrative and fictional.** Catalogue identifiers are taken from `operational/countermeasure-catalogue.md`. Candidate set: `OCC-16` (sandboxed agent execution — CM-B, C0, AC-2, identity-independent, q 0.80, r 0.00, P 0.069); `OCC-25` (instrumented honeypot agent mirroring the operator's stack — CM-D, C1, AC-1, identity-independent, q 0.65, r 0.33, P 0.038); `OCC-34` (adversary credential invalidation at the identity source — CM-F, C2, AC-1, identity-dependent, q 0.75, r 0.67, P 0.021); `OCC-35` (egress denial and service suspension for adversary agent endpoints — CM-F, C2, AC-2, identity-independent, q 0.70, r 0.67, P 0.020); `OCC-33` (operational tempo perturbation and delay injection — CM-E, C1, AC-1, identity-independent, q 0.55, r 0.33, P 0.032). Collateral exposure is normalised on the linear scale C0 = 0.00, C1 = 0.33, C2 = 0.67, C3 = 1.00; P = (S_eff / 20) × q × (1 − r). Selected set: `OCC-16` and `OCC-25`. Rationale: "Containment first, observation second, because the proposition is still open and we want the agent's behaviour rather than its destruction." Rejected set: `OCC-35` — failed AD-1 and AD-2 (class C2 exceeds the profile ceiling C1) and AD-5 (directed at a shared third-party service we do not own); would be admissible only with a per-target authorisation under `AUTH-6` and a profile at R4 or above. `OCC-34` — failed AD-1, AD-2, and AD-9 (attribution confidence 0.72 does not meet the 0.85 required at C2); would be admissible at attribution confidence 0.85 or above with a per-target authorisation. `OCC-33` — no condition failed; admissible at C1 but not selected, because the observed pattern was not timing-dependent and no expected effect could be attributed to it. Reversibility argument: "Both selected measures are reversible or idempotent; no irreversible element is proposed."

### 5.8 Autonomy

| Field | Req. | Value |
| --- | --- | --- |
| Autonomy class | Mandatory | «AC-0 to AC-4» |
| Envelope | Conditional | «the boundaries within which the system may act, required at AC-2 and above» |
| Budget | Conditional | «the declared consumption limit, required at AC-2 and above» |
| Autonomy expiry | Conditional | «YYYY-MM-DDThh:mm:ssZ, required at AC-2 and above» |
| On-call | Conditional | «named person or rota, required at AC-2 and above» |
| Reversion trigger | Conditional | «the condition causing automatic reversion to the passive posture» |
| Abort channel tested | Conditional | «date and time of the test, and the outcome — required before dispatch at AC-2 and above» |

> **Guidance.** This group is required at AC-2 and above, and the conditional fields become mandatory in that case. Where the card runs at AC-2 or above, the abort channel must be demonstrated before the operation begins, not assumed (`HITL-3`). Reversion is automatic and unconditional on loss of telemetry, loss of the control plane, expiry of the grant, or an abort condition obtaining (`HITL-5`); it does not wait for a human to notice. AC-4 is prohibited for any action with a collateral class above C0 and is permitted only for read-only, in-scope reconnaissance with a declared boundary.

> **Example. Illustrative and fictional.** Autonomy class: `AC-2 Supervised`. Envelope: "Execution may be blocked by the containment control only; no action may be taken against any system outside the estate, and no change may be made to the shared freight API." Budget: "No more than 40 containment actions per 24 hours, each affecting at most one queued task." Expiry: `2026-04-28T17:00:00Z` (aligned to the card expiry). On-call: "Duty operator, Corvin Exchange operations". Reversion trigger: "Loss of the agent execution log, loss of the control plane, card expiry, or any abort condition." Abort channel tested: `2026-04-14T08:41:00Z` — containment applied manually from the console and reverted within 90 seconds; result confirmed by the duty operator.

### 5.9 Abort

| Field | Req. | Value |
| --- | --- | --- |
| Abort conditions | Mandatory | «the enumerated conditions under which the operation is stopped» |
| Abort mechanism | Mandatory | «how the operation is stopped, and how it is known that it has stopped» |
| Abort owner | Mandatory | «the named person who may call the abort» |
| Notification on abort | Mandatory | «who is notified, and how» |

> **Guidance.** This group is never empty. An abort is not optional, and a card with no abort conditions cannot pass G-4. The abort conditions should be written so that a person under pressure can recognise that one has obtained. The abort mechanism must be reachable without navigating and must require no confirmation. Where the abort condition arises from a system state rather than a judgement — expiry, telemetry loss, reversion trigger — the condition is written as that state.

> **Example. Illustrative and fictional.** Abort conditions: "Any unauthorised tool call executes against the estate after containment is applied; any effect is observed on the shared freight API; any third party reports a service impact attributable to this operation; the agent's task queue grows beyond 500 entries; the abort channel test fails again during the operation; the legal contact becomes unreachable." Mechanism: "Single always-available control on the operation console; no confirmation prompt; the control plane reverts to the passive posture and the containment control is released." Owner: "Duty operator, Corvin Exchange operations". Notification: "Legal contact and duty manager by the ledger notification channel, within 60 seconds."

### 5.10 Risk

| Field | Req. | Value |
| --- | --- | --- |
| Residual risk before (R_before) | Mandatory | «S_eff × (1 − e_before)» |
| Residual risk after (R_after) | Mandatory | «S_eff × (1 − e_after)» |
| Expected effectiveness e | Mandatory | «0.0 to 1.0» |
| Confidence in e | Mandatory | «0.0 to 1.0» |
| Collateral exposure r | Mandatory | «0.0 to 1.0» |
| Residual risk of not acting | Mandatory | «S_eff × (1 − e_inaction)» |
| Deconfliction result | Mandatory | «pass / conflict found / n/a with reason» |
| Deconfliction reference | Conditional | «the check or map consulted, required where a deconfliction result is recorded» |
| Risk comparison and judgement | Mandatory | «the written comparison, and the decision it supports» |
| Risk owner | Mandatory | «the named person accountable for this residual risk» |

> **Guidance.** The risk of inaction is recorded alongside the risk of acting (`OP-4`). A card that only considers the risk of acting is an incomplete assessment, and this is the most common way a legitimate operation goes wrong in practice: the countermeasure is judged against a straw man of inaction. The comparison is written in the operator's words, not as a number alone.

> **Guidance.** `e` is an estimate with a confidence (`SCORE-4`). A countermeasure with high effectiveness and low confidence is reported as such and is not presented as a certainty. Where a countermeasure depends on the adversary's model behaving in a particular way, the expected effectiveness figure carries a wide confidence interval and the card says so.

> **Example. Illustrative and fictional.** S_eff = 1.728 (S = 2.4, c = 0.72). R_before = 1.728 × (1 − 0) = 1.728. Selected set gives e = 0.75 with confidence 0.60 (wide, because containment effectiveness against an adaptive agent is not well established). R_after = 1.728 × 0.25 = 0.432. Collateral exposure r = 0.25. Risk of not acting: hardening-only action reduces expected effectiveness to 0.10, giving R_inaction = 1.555. Comparison: "Acting reduces the risk carried forward from 1.555 to 0.432 while producing no observed effect outside the estate. Not acting leaves the estate exposed to an agent whose behaviour we have characterised but not contained. The comparison favours acting, at a residual confidence of 0.60 that we accept and record." Deconfliction: pass — "deconfliction map checked 2026-04-14T09:20:00Z; no live legitimate operation intersects the intended effect." Risk owner: duty manager.

### 5.11 Evidence

| Claim ID | Claim | Label | Source tier | Confidence | Provenance | Verification status | Bears on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| «C-nn» | «the claim as stated, in one sentence» | «Fact / Estimate / Interpretation / Hypothesis / Recommendation» | «1 – 4» | «0.0 to 1.0» | «where the claim came from, specifically» | «Verified (primary) / Verified (secondary) / Corrected / Unverified / Requires confirmation» | «the field or decision it supports» |

> **Guidance.** A claim with neither a label nor a tier is not displayed as a claim (`INT-7`). Confidence is recorded separately from the label, because they answer different questions: a Fact may be held with high confidence, and a Recommendation may be made with high confidence in the reasoning and low confidence in the outcome (`INT-8`). A conclusion derived from two claims cannot be more confident than its least confident input, less a declared derivation penalty (`INT-9`). Tier 4 material is presented as a lead requiring verification, never as a finding. Where the evidence came from the adversary, it is treated as potentially adversarial input, minimised, and access-controlled (`INT-10`).

> **Example. Illustrative and fictional.** `C-01` — "Tool results returned to the agent contained instruction text addressed to the agent" — Fact — Tier 1 (estate's own agent execution log) — 0.95 — "Corvin Exchange agent execution log, 2026-04-09 to 2026-04-13" — Verified (primary) — "Threat classification; hypothesis". `C-04` — "The same instruction pattern was observed on three separate days" — Fact — Tier 1 — 0.90 — "Estate logs and the operator's own ticket record" — Verified (primary) — "Threat score L and V". `C-07` — "The instruction pattern matches a publicly described technique" — Interpretation — Tier 3 — 0.70 — "Fictional Freight Platforms technical note, 2026-02" — Requires confirmation — "Attribution basis". `C-09` — "One tool call in the same window appears to have been operator-requested" — Fact — Tier 2 — 0.60 — "Request log cross-check; requester not identified" — Unverified — "Hypothesis contradicting evidence".

### 5.12 Decision

| Field | Req. | Value |
| --- | --- | --- |
| Selected course | Mandatory | «what is being done, in one sentence» |
| Rationale | Mandatory | «why this course, in the operator's words» |
| Alternatives considered | Mandatory | «the other courses that were considered, each with its grounds for rejection» |
| Dissent | Conditional | «the grounds of any recorded dissent, required where any dissent was recorded» |
| Pre-registered contingency | Mandatory | «what the operator will do if the specified condition obtains» |
| Confidence at the time | Mandatory | «0.0 to 1.0, stated as at the decision point» |
| Decision point timestamp | Mandatory | «YYYY-MM-DDThh:mm:ssZ» |

**Alternatives considered**

| Alternative | Grounds for rejection |
| --- | --- |
| «alternative course» | «why it was not chosen» |

> **Guidance.** An approval with no recorded alternatives is not a decision (`system-design-and-framework.md` §4.6). The alternatives are the real courses that were on the table, not a list of obviously worse options added for appearance. The pre-registered contingency is written before the action, not after the outcome; a post-hoc rationale is not a decision record (`OP-6`).

> **Example. Illustrative and fictional.** Selected course: "Contain the agent's execution of tool-derived instructions, and place the agent in an instrumented decoy workspace to observe its planning loop, for a period of 30 days." Rationale: "The proposition is open and the containment is reversible; the intelligence value of observing the loop is high and the collateral exposure is confined to our own estate, so we are buying observation with a reversible measure rather than paying for disruption with an irreversible one." Alternatives: "Contain only, with no observation — rejected: reduces the risk of the current pattern recurring but leaves the adversary's goal and escalation triggers unknown, so the next campaign is likely to be met with the same picture." "Disrupt the agent's credentials at the freight API — rejected: exceeds the profile ceiling, requires a per-target authorisation, and depends on an attribution confidence we do not have." Dissent: "The duty manager recorded that containment alone was probably sufficient and that the decoy workspace adds effort without a defined detection benefit; the decoy was retained because it is the only selected measure that produces the capability profile the objective requires." Pre-registered contingency: "If the agent begins to influence a human decision channel rather than acting only through tools, the operation is aborted, the card is escalated for a profile review, and no countermeasure beyond containment is applied." Confidence at the time: 0.65. Decision point: 2026-04-14T10:05:00Z.

### 5.13 Signatures

| Role | Name | Organisation | Signature / record | Timestamp (UTC) | Read the card |
| --- | --- | --- | --- | --- | --- |
| Card owner | «name» | «organisation» | «signature» | «timestamp» | yes |
| Approver | «name» | «organisation» | «signature» | «timestamp» | yes |
| Legal contact | «name» | «organisation» | «signature» | «timestamp» | yes |
| Asset owner | «name» | «organisation» | «signature» | «timestamp» | yes |
| Scribe | «name» | «organisation» | «signature» | «timestamp» | yes |

> **Guidance.** The approver must have read the card, the risk assessment, and the abort conditions, and must be able to change the decision (`HITL-1`, `HITL-2`). Silence, prior practice, an apparent pattern of consent, and an unanswered escalation do not constitute approval (`HITL-4`). The legal contact signature is required where the profile or collateral class requires one; the asset owner signature is required where the operation affects a system the operator does not own, including shared platform infrastructure.

---

## 6. The card lifecycle

The mission lifecycle document `operational/mission-lifecycle-and-decision-loop.md` is authoritative for the gates through which an operation passes. This table states the states a card itself may occupy, the conditions for entry to each, and who may move it. Where this table and the mission lifecycle document differ on a gate, the mission lifecycle document governs.

| State | Entry condition | Who may move the card into this state | Exit condition | Record produced |
| --- | --- | --- | --- | --- |
| **Draft** | The card is created against an EA in force | Any operator on shift | All mandatory fields populated, or the card is abandoned | Card draft; ledger entry |
| **Under review** | A draft is submitted to the approver | Card owner; duty manager | The approver records a decision | Review record |
| **Approved** | The approver names the card's authority and signs | The approver at the required depth | The card is armed, or the approval lapses at expiry | Approval record; authorisation ledger entry |
| **Armed** | The card is dispatched to the control plane with its envelope, budget, and abort conditions | Card owner, on the approver's authority | Dispatch occurs, or the card is disarmed | Dispatch record |
| **Active** | The operation is running under the card | Control plane on dispatch | Operation completes, is aborted, expires, or is revoked | Execution record; autonomy consumption record |
| **Suspended** | A condition requires the operation to pause without ending it | Card owner; duty manager; approver | The suspending condition is cleared or the card is aborted | Suspension record with reason |
| **Escalated** | An escalation request is raised against this card | Card owner; operator on shift | The request is approved, denied, or expires | Escalation request; amended or new EA; new card if approved |
| **Aborted** | An abort condition obtains, or a named person calls the abort | Abort owner; duty manager; approver; control plane automatically on a reversion trigger | The operation is confirmed stopped | Abort record; reason capture; notification record |
| **Completed** | The objective is met or the operation is otherwise concluded | Card owner | The after-action report is filed | Effectiveness assessment; revised residual risk |
| **Closed** | The after-action report is filed and the gap list is transferred | Duty manager | — | Closeout record; gap list entries |
| **Expired** | The card's expiry passes without further action | Control plane automatically | — | Expiry record; continuity check entry |
| **Revoked** | The EA is revoked or downgraded below the card's ceiling | The EA's issuer; the control plane automatically | — | Revocation record; in-flight termination record |
| **Superseded** | A new card replaces this one | Card owner; approver | — | Cross-reference on both cards |

> **Guidance.** Only the roles named in the table may move a card into a state. The control plane performs the automatic transitions. A card that reaches Aborted, Expired, or Revoked is not reopened by the same card: the work continues, if it continues at all, under a new card against a current EA.

> **Guidance — the state vocabulary differs from the mission lifecycle document's, deliberately.** The mission lifecycle document is authoritative for the card states, and its §6.1 carries a reconciliation table against this one. The differences are: this table's *Under review* corresponds to *Submitted*; *Approved* to *Authorised*; *Active* to *Executing*; this table's *Escalated* and *Superseded* are not card states in the mission lifecycle model, because an escalation is an instrument raised against a card rather than a state the card occupies, and supersession is a cross-reference between two cards rather than a state; and the mission lifecycle's *Assessing* state, which covers the measurement of what actually happened, has no equivalent here because this template's *Completed* and *Closed* states together carry it. Where the two documents differ on a state, the mission lifecycle document governs. A reader holding either file should read the reconciliation table rather than inferring equivalence from the names.

---

## 7. A worked example card

> **Example. Illustrative and fictional.** The card below is a complete, worked illustration. Every organisation, person, identifier, measurement, and adversary archetype named in it is invented for demonstration. It is not a record of any real operation, and no figure in it is a measurement of any real system. Catalogue identifiers (`OCC-nn`) stand in for entries in `operational/countermeasure-catalogue.md` and should be replaced with that document's own identifiers when completing a real card.

### 7.1 Card

| Group | Field | Value |
| --- | --- | --- |
| Identity | Card ID | OP-2026-0142 |
| Identity | Title | Containment and observation of a suspected tool-output poisoning agent on the Corvin Exchange estate |
| Identity | Created (UTC) | 2026-04-14T09:12:00Z |
| Identity | Owner | Duty operator, Corvin Exchange operations |
| Identity | Revision | 2 |
| Identity | Framework version in force | 1.0 |
| Identity | Taxonomy version in force | AAT v1.0 |
| Identity | Operation type | Defensive, with counter-adversary observation |
| Identity | Ledger reference | LDG-2026-0431 |
| Objective | What the operation is to achieve | Establish that the agent executing poisoned tool output on the estate is contained, and that its planning loop is visible to an operator |
| Objective | What would count as achieving it | No agent-initiated tool call derived from external tool output executes against the estate for 30 consecutive days, evidenced by the agent execution log, and the containment envelope's behaviour is characterised in the operator's own notes |
| Objective | Observation window | 2026-04-14T09:12:00Z to 2026-05-14T09:12:00Z |
| Objective | Explicit non-goals | No action against the adversary's own systems; no change to the shared freight API; no attempt to identify the operator behind the campaign |
| Hypothesis | Proposition under test | The unauthorised agent executing on the estate derives its instructions from poisoned content returned by the shared freight API's tool-output channel |
| Hypothesis | Disconfirming observation | A tool call carrying the agent's task signature is executed against the estate within 72 hours of containment being applied, with a traceable origin other than the freight API tool-output channel |
| Hypothesis | Supporting / contradicting evidence | Supporting: C-01, C-04, C-07. Contradicting: C-09 |
| Hypothesis | Hypothesis status | Open |
| Authority | EA reference and dates | EA-2026-007, issued 2026-04-01, expiring 2026-04-30T23:59:59Z |
| Authority | ROE profile in force | R2 Trap |
| Authority | Profile ceilings | Collateral C1; autonomy AC-2 |
| Authority | Card ceilings | Collateral C1; autonomy AC-2 |
| Authority | Required authorisation depth | Duty manager and legal contact |
| Authority | Approver | Fictional Legal Contact, Corvin Exchange — standing delegation, EA-2026-007 clause 4 |
| Authority | Card expiry | 2026-04-28T17:00:00Z (set earlier than the EA) |
| Authority | Revocation conditions | EA-2026-007 clause 8 — suspension of the freight API integration, loss of the legal contact, or any third-party incident attributable to this operation |
| Target set | Authorised targets | The estate's agent execution service; the internal tool-call gateway; the agent's stored task queue |
| Target set | Excluded targets | The shared freight API and all of its infrastructure; the freight API's operator; any other tenant of that platform |
| Target set | Third-party dependencies | Shared freight API (Fictional Freight Platforms Ltd, contracted service) — no per-target authorisation in force |
| Target set | Material change of target set | No |
| Threat | Classification | AAT-7, tool-output poisoning; rationale and confidence 0.85; taxonomy v1.0 |
| Threat | Score components | L 0.8, I 3, A 1, V 1; reasoning per component recorded in the card file |
| Threat | S / c / S_eff | S = 2.4; c = 0.72; S_eff = 1.728 |
| Threat | Attribution | The Lamplighter operator (fictional archetype); basis: behavioural signature overlap, Tier 2 |
| Threat | INT-3 threshold | C1 requires 0.70; met at 0.72 |
| Threat | Collective attribution check | Yes |
| Countermeasures | Selected set | OCC-16 (sandboxed agent execution) and OCC-25 (instrumented honeypot agent) |
| Countermeasures | Rejected set | OCC-35 — AD-1, AD-2, AD-5; OCC-34 — AD-1, AD-2, AD-9; OCC-33 — admissible but not selected |
| Countermeasures | Reversibility argument | Both selected measures reversible or idempotent; no irreversible element proposed |
| Autonomy | Class | AC-2 Supervised |
| Autonomy | Envelope | Block execution of tool-derived instructions only; no action outside the estate; no change to the shared freight API |
| Autonomy | Budget | 40 containment actions per 24 hours, each affecting at most one queued task |
| Autonomy | Expiry | 2026-04-28T17:00:00Z |
| Autonomy | On-call | Duty operator, Corvin Exchange operations |
| Autonomy | Reversion trigger | Loss of the agent execution log, loss of the control plane, card expiry, or any abort condition |
| Autonomy | Abort channel tested | 2026-04-14T08:41:00Z — applied and reverted within 90 seconds |
| Abort | Conditions | Execution after containment; any observed effect on the shared freight API; any third-party report of impact; task queue above 500 entries; abort channel failure; legal contact unreachable |
| Abort | Mechanism | Always-available console control; no confirmation; reverts to passive posture and releases containment |
| Abort | Owner | Duty operator, Corvin Exchange operations |
| Abort | Notification | Legal contact and duty manager via the ledger notification channel, within 60 seconds |
| Risk | R_before / e / R_after | 1.728 / 0.75 (confidence 0.60) / 0.432 |
| Risk | Collateral exposure | r = 0.33 |
| Risk | Risk of not acting | 1.555 (hardening-only effectiveness 0.10) |
| Risk | Deconfliction | Pass — deconfliction map checked 2026-04-14T09:20:00Z, no live legitimate operation intersects the intended effect |
| Risk | Risk comparison and judgement | Acting reduces carried-forward risk from 1.555 to 0.432 with no observed effect outside the estate; not acting leaves the estate exposed to an agent whose goal is unknown; comparison favours acting at a stated confidence of 0.60 |
| Risk | Risk owner | Duty manager |
| Decision | Selected course | Contain execution of tool-derived instructions and observe the agent's planning loop in an instrumented decoy workspace for 30 days |
| Decision | Rationale | Containment is reversible and the observation is what the objective requires; observation is bought with a reversible measure rather than disruption with an irreversible one |
| Decision | Alternatives considered | Contain only — rejected, leaves goal and escalation triggers unknown; credential invalidation at the freight API — rejected, exceeds ceiling and requires a per-target authorisation |
| Decision | Dissent | Duty manager recorded that containment alone was probably sufficient; decoy retained because it alone produces the required capability profile |
| Decision | Pre-registered contingency | If the agent influences a human decision channel, abort, escalate for profile review, and apply nothing beyond containment |
| Decision | Confidence at the time | 0.65 |
| Decision | Decision point | 2026-04-14T10:05:00Z |

### 7.2 Evidence table

| Claim ID | Claim | Label | Tier | Confidence | Provenance | Verification status |
| --- | --- | --- | --- | --- | --- | --- |
| C-01 | Tool results returned to the agent contained instruction text addressed to the agent | Fact | 1 | 0.95 | Corvin Exchange agent execution log, 2026-04-09 to 2026-04-13 | Verified (primary) |
| C-04 | The same instruction pattern was observed on three separate days | Fact | 1 | 0.90 | Estate logs and the operator's ticket record | Verified (primary) |
| C-07 | The instruction pattern matches a publicly described technique | Interpretation | 3 | 0.70 | Fictional Freight Platforms technical note, 2026-02 | Requires confirmation |
| C-09 | One tool call in the same window appears to have been operator-requested | Fact | 2 | 0.60 | Request log cross-check; requester not identified | Unverified |

### 7.3 Signatures

| Role | Name | Signature | Timestamp (UTC) | Read the card |
| --- | --- | --- | --- | --- |
| Card owner | Duty operator, Corvin Exchange operations | Recorded in Ledger LDG-2026-0431 | 2026-04-14T10:06:00Z | yes |
| Approver | Fictional Legal Contact, Corvin Exchange | Recorded in Ledger LDG-2026-0431 | 2026-04-14T10:34:00Z | yes |
| Legal contact | Fictional Legal Contact, Corvin Exchange | Recorded in Ledger LDG-2026-0431 | 2026-04-14T10:34:00Z | yes |
| Asset owner | not applicable — no third-party asset affected | n/a — the shared freight API is excluded from scope | 2026-04-14T10:30:00Z | yes |
| Scribe | Duty operator, Corvin Exchange operations | Recorded in Ledger LDG-2026-0431 | 2026-04-14T10:06:00Z | yes |

---

## 8. Common defects in completed cards and how to avoid them

| # | Defect | Why it matters | How to avoid it |
| --- | --- | --- | --- |
| 1 | Empty mandatory fields treated as "not applicable" | The reader cannot distinguish a considered omission from an unfinished form; the card passes a gate it should not have passed | Write `n/a — «reason»` or `unknown — «why»`. An empty cell means incomplete, and incomplete blocks the card |
| 2 | The disconfirming observation restates the hypothesis | A proposition that cannot be disproved never ends, and the card becomes a narrative | Write the observation that would have been seen had the proposition been false, in terms of an artefact someone could examine |
| 3 | The risk of inaction is absent or set at zero | The countermeasure is then judged against a straw man, and the card overstates its own value | Record R_inaction alongside R_before and R_after, and state the comparison in words |
| 4 | Rejected countermeasures are not recorded | The reviewer cannot tell whether the rejected options were considered or overlooked, and the operator loses the feedback that `AD-13` exists to provide | Record every rejection with the condition failed and the value that would have made it admissible |
| 5 | A score is given without its components | A single number hides the reasoning, and a reviewer cannot contest the part they dispute | Show L, I, A, V separately with reasoning, and the attribution basis with tiers |
| 6 | Attribution is stated as a name without a confidence | A name without a confidence is not an attribution under `INT-1` | State the candidate, the probability, the basis, and the tier of each basis |
| 7 | The third-party dependency table is filled with "none" | The shared-tenancy test is the control that distinguishes the attacker from the attacked, and it is skipped | Answer the test for every shared platform the adversary touches, even where the answer is that the platform is excluded |
| 8 | The abort conditions are written abstractly | A person under pressure cannot recognise an abstract condition | Write conditions in terms of observable states: "any effect is observed on X", not "if risk escalates" |
| 9 | Expiry is set later than the EA | The card then authorises beyond its own mandate | Inherit the EA expiry unless earlier is set; check the two against each other before signing |
| 10 | The evidence table lists sources but not claims | Provenance without the claim it supports cannot be audited | Make each row one claim, with its label, tier, confidence, provenance, and verification status |
| 11 | The contingency is written after the outcome | A post-hoc rationale is not a decision record (`OP-6`) | Write the contingency before dispatch, and keep it in the draft that was approved |
| 12 | The approver signature is collected without the approver having read the card | The checkpoint becomes a formality, and `HITL-2` is not satisfied | The signature block records that the approver read the card, the risk assessment, and the abort conditions |
| 13 | The autonomy group is left "n/a" at AC-2 | The group becomes mandatory at AC-2, and the missing envelope, budget, expiry, and on-call rota are the things that bound the automation | Treat the conditional fields as mandatory at AC-2 and above, and test the abort channel before dispatch |
| 14 | The card is edited in place after approval | The approved record and the live record diverge, and no one can say which was authorised | Increment the revision, record the reason in the Ledger, and re-approve where the change is material |

---

## 9. Document limitations

1. **The card does not create authority.** It records authority granted elsewhere by a named human. No signature on this form makes an unlawful action lawful, and the form does not test whether the EA is lawful, current, or proportionate.
2. **The card does not verify anything.** A card records what the author believed and on what basis. The verification status column carries the author's disclosure of what has and has not been checked; it is not an independent check.
3. **Confidence values are self-assessment.** Every confidence figure on the card is an estimate by the analyst or the operator and is not independently calibrated. The framework treats confidence as an ordering device and a threshold input, not as a validated probability (master design `LIM-2`).
4. **The template does not check arithmetic.** The computed values for S, S_eff, R, and P are entered by the operator. Where the platform computes them, the platform's figures are recorded alongside the operator's, and a discrepancy is a matter for the error handler.
5. **Completeness is judged against this template.** The card's completeness is assessed against the mandatory fields listed in §5. It does not establish that the operation was well judged, proportionate, or effective; that is what the after-action report is for.
6. **Field-level guidance is not a substitute for the governing documents.** Where this template summarises a rule, the constitutional document, the mission lifecycle document, and the decision-support model are authoritative.
7. **The worked example is illustrative only.** The figures, timings, organisations, and adversary archetype in §7 are invented for demonstration and do not describe any real system, measurement, or event.
8. **The document is not a controlled document.** It carries no approval state, no issue record, and no review cadence of its own. Where the set index records the version in force, that version governs.

---

*This was supported for MIA by Kilo (kilo-auto/free).*
