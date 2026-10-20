# Decision Log Template

| Field | Value |
| --- | --- |
| Author | MIA |
| Attribution | This was supported for MIA by Kilo (kilo-auto/free). |
| Document type | Fillable template — operational artefact, layer L6 |
| Subject | The reconstructible record of reasoning, alternatives, and risk for each material decision |
| Scope | One log per operation, held open for the duration of the operation and closed at the after-action report |
| Normative source | `system-design-and-framework.md` §6.6, §8.3; `compliance/operator-conduct-and-human-in-loop-standard.md`; `operational/mission-lifecycle-and-decision-loop.md` |
| Companion templates | `templates/operation-card.md`; `templates/escalation-request.md`; `templates/after-action-report.md` |
| Version | 1.0 |
| Status | Template; copied and completed per use |
| Language | British English; RFC 2119 keyword usage |

---

## 1. Purpose and the sufficiency criterion

The decision log is the system's memory and the substrate of auditability. For each material decision it records the rationale, the alternatives considered and the grounds for rejecting each, the known risks, the confidence at the time, and the pre-registered contingency. It additionally captures changes to scope, to assumptions, to evidence quality, and to the card's world model (`system-design-and-framework.md` §8.3).

**The sufficiency criterion is external.** Another reviewer must be able to reconstruct the decision from the record alone. A log that satisfies only its author does not satisfy the design.

A material decision is any decision that:

- changed the objective, the target set, the hypothesis, or the authority relied upon;
- selected, rejected, or deferred a countermeasure;
- raised, withdrew, or answered an escalation request;
- changed an assumption, a confidence value, or an evidence weighting;
- invoked an abort, a reversion, or the error handler;
- accepted or declined a residual risk;
- authorised, suspended, resumed, or closed a card;
- was made under time pressure, under uncertainty, or against someone's stated preference.

A decision that changed nothing and foreclosed nothing is not material and need not be logged. The burden is on the person who made the decision to decide whether it was material, and the conservative reading of "material" is the correct one.

> **Guidance.** Write the log as you go, not at the end. A log reconstructed from memory at the end of a shift is a record of what the author now believes happened, which is a different and weaker thing.

---

## 2. Log entry structure

Each entry is one decision. Copy the block below for each material decision and complete every field.

| Field | Req. | Value |
| --- | --- | --- |
| Entry ID | Mandatory | «DL-nnn» |
| Timestamp (UTC) | Mandatory | «YYYY-MM-DDThh:mm:ssZ — when the decision was taken, not when it was written up» |
| Card | Mandatory | «card id» |
| Decision point | Mandatory | «the gate or moment at which the decision was taken, e.g. G-3 Admissibility, mid-operation review, escalation response» |
| What was known at the time | Mandatory | «the state of the world as understood at that moment, with claim ids» |
| Claims relied upon | Mandatory | «claim id, label, tier, confidence — table below» |
| Options considered | Mandatory | «table below» |
| The choice | Mandatory | «what was decided, in one sentence» |
| Authority relied upon | Mandatory | «EA reference, profile, approval depth, and the named person who authorised it» |
| Residual risk accepted | Mandatory | «the residual risk figure after the decision, and the risk of not taking the chosen option» |
| Confidence at the time | Mandatory | «0.0 to 1.0, and the basis for that figure» |
| Pre-registered contingency | Mandatory | «what the decision-maker will do if the specified condition obtains» |
| Dissent | Conditional | «the grounds of any recorded dissent — required where any dissent was recorded» |
| Outcome, if known | Optional | «what subsequently happened, recorded as at the time of the update» |
| What would have changed the decision | Mandatory | «the observation, figure, or event that would have produced a different choice» |
| Recorded by | Mandatory | «name and role» |

**Claims relied upon**

| Claim ID | Claim (short form) | Label | Source tier | Confidence | Provenance |
| --- | --- | --- | --- | --- | --- |
| «C-nn» | «the claim as understood at the time» | «Fact / Estimate / Interpretation / Hypothesis / Recommendation» | «1 – 4» | «0.0 to 1.0» | «where it came from» |

**Options considered**

| Option | Grounds for rejection |
| --- | --- |
| «option» | «why it was not chosen, or why it was chosen over the others» |

> **Guidance.** The options table records the real courses that were on the table. An option that was never seriously entertained is not listed, and a list of obviously worse options added for appearance is worse than no list, because it misleads the reviewer about how the decision was reached.

> **Guidance.** "What was known at the time" is not a summary of the evidence that exists now. It is the evidence that existed then, including what was misread, what had not yet been collected, and what was available but not looked at. Where a source was degraded at the time, say so.

---

## 3. Rules for writing an entry

1. **Record the decision as taken, not as it would appear in retrospect.** Where a later reviewer would reach a different decision with the same information, that divergence is recorded as a known limitation of the assessment rather than smoothed over (`ERR-5`).
2. **Record the alternatives.** Every option seriously considered is listed with its grounds for rejection. An entry with a single option is either a false record or a signal that the alternatives were not generated.
3. **Record what would have changed the decision.** This is the field that converts a log into a learning instrument. It forces the decision-maker to state the condition the decision was contingent on, which is the same discipline as the pre-registered contingency.
4. **Do not smooth over divergence.** Where the record now looks less sound than it looked then, that is written down. The record is not a reputation.
5. **Write the confidence as it was held, not as it would be rated now.** A confidence value revised after the outcome is a new entry, not an edit to the old one.
6. **Preserve the timestamp of the decision.** A late-written entry carries the time the decision was taken; if that time cannot be established, write `unknown` and state the basis on which it was approximated.
7. **Name the authority, not the role alone.** "Duty manager" is not an authority that a reviewer can check; "A. Person, duty manager, under EA-2026-007 clause 4" is.
8. **Record refusals and deferrals.** A refusal to act, a request to wait, and a decision not to escalate are decisions, and they are logged as such.
9. **Keep the language of the moment.** Where the entry records what was understood at the time, use the terms in use at the time and do not translate them into the framework's later vocabulary.
10. **One decision per entry.** Where a decision bundle is recorded as one entry, the entry must list each constituent decision and each constituent risk.

---

## 4. Claim-label and source-tier vocabulary used inline

The five claim labels and the four source reliability tiers are the controlled vocabulary of the set (`README.md` §3). They are reproduced here so that an operator writing an entry under pressure does not have to reach for another document.

**Claim labels**

| Label | Use it when | Do not use it when |
| --- | --- | --- |
| **Fact** | The statement is directly supported by an identified asset or verifiable source, and is verifiable independently of the author's assertion. | The source is the person making the assertion and no other. |
| **Estimate** | The statement is a quantified approximation whose precision, basis, and limits can be stated. | The figure is copied from a source without an assessment of its precision. |
| **Interpretation** | The statement is a reasoned reading of evidence that extends beyond what any source states explicitly. | The source states it directly. That is a Fact. |
| **Hypothesis** | The statement is a testable proposition not yet supported by sufficient evidence. | The statement cannot be tested, in which case it is a narrative, not a hypothesis. |
| **Recommendation** | The statement is a proposed course of action with its basis stated and distinguishable from the findings that motivate it. | The statement is a finding. |

**Source reliability tiers**

| Tier | Description | Consequence of reliance |
| --- | --- | --- |
| **1** | Primary data, peer-reviewed research, authoritative standards or regulatory instruments | May support a decision directly |
| **2** | Reputable secondary analysis and institutional grey literature with attributable authorship | May support a decision, and must be attributed |
| **3** | Single-expert assertion, pre-publication material, or commercial sources with verifiable provenance | May support a decision only with the tier recorded and the reliance noted |
| **4** | Unverified material, anonymous assertion, AI-generated suggestions or leads | Presented as a lead requiring verification; never as an established finding, and never as the sole basis for an action at C1 or above |

**Verification status**, where recorded: Verified (primary), Verified (secondary), Corrected, Unverified, Requires confirmation.

**Rule.** Every material claim in an entry carries a label and a tier. A claim with neither is not a claim, and a decision resting on such material has no recorded basis.

---

## 5. A worked example entry

> **Example. Illustrative and fictional.** Every organisation, person, identifier, measurement, and adversary archetype below is invented for demonstration and refers to no real entity. The figures are illustrative arithmetic, not measurements.

| Field | Value |
| --- | --- |
| Entry ID | DL-0031 |
| Timestamp (UTC) | 2026-04-14T10:05:00Z |
| Card | OP-2026-0142 |
| Decision point | G-4 Authorisation — selection of the countermeasure set |
| What was known at the time | Three days of structured tool-output poisoning attempts against the estate; the shared freight API was confirmed to be a shared dependency with approximately 40 other tenants; no per-target authorisation for the freight API existed; behavioural overlap with a previously seen operator pattern was noted but not confirmed. The agent execution log had been degraded for 41 minutes earlier in the day and had recovered. |
| Claims relied upon | C-01 (Fact, Tier 1, 0.95); C-04 (Fact, Tier 1, 0.90); C-07 (Interpretation, Tier 3, 0.70); C-09 (Fact, Tier 2, 0.60); C-12 (Fact, Tier 1, 0.85 — the freight API is shared) |
| Options considered | (a) Contain execution of tool-derived instructions only — rejected: reduces recurrence but leaves the agent's goal and escalation triggers unknown, which the objective requires. (b) Contain and observe in an instrumented decoy workspace — chosen. (c) Credential invalidation at the freight API — rejected: exceeds the profile ceiling, requires per-target authorisation that does not exist, and depends on an attribution confidence not held. (d) Defer the decision pending further attribution — rejected: the estate remained exposed during the deferral and the hypothesis was not going to be resolved by waiting. |
| The choice | Contain execution of tool-derived instructions and place the agent in an instrumented decoy workspace for a 30-day observation window. |
| Authority relied upon | EA-2026-007; profile R2 Trap; card collateral ceiling C1; approved by Fictional Legal Contact (legal contact, Corvin Exchange) and the duty manager under EA-2026-007 clause 4. |
| Residual risk accepted | Residual risk after: 0.432, at expected effectiveness 0.75 with confidence 0.60. Risk of not acting: 1.555. The difference was accepted on the basis that the containment is reversible and confined to our own estate, and the confidence in effectiveness is recorded as low. |
| Confidence at the time | 0.65 in the decision as a whole. Basis: classification confidence 0.85 and attribution confidence 0.72 were both held with high confidence in the underlying observations, but the effectiveness estimate of 0.75 was held at confidence 0.60, and that estimate carries the decision. |
| Pre-registered contingency | If the agent begins to influence a human decision channel rather than acting only through tools, the operation is aborted, the card is escalated for a profile review, and no countermeasure beyond containment is applied. |
| Dissent | The duty manager recorded that containment alone was probably sufficient and that the decoy workspace added effort without a defined detection benefit. The decoy was retained because it alone produces the capability profile the objective requires. The dissent is recorded and was not resolved by the approver; it is carried into the after-action report. |
| Outcome, if known | Containment applied 2026-04-14T10:22:00Z. Abort channel test passed 2026-04-14T08:41:00Z. No tool call derived from external tool output executed against the estate during the observation window; one tool call was blocked by containment on 2026-04-19. Recorded 2026-05-14T16:30:00Z. |
| What would have changed the decision | Attribution confidence at or above 0.85, or the presence of a per-target authorisation for the freight API, or a disconfirming observation showing the instruction did not originate in the tool-output channel. Any of the three would have produced an escalation request rather than an R2 operation. |
| Recorded by | Duty operator, Corvin Exchange operations |

> **Guidance.** Note the dissent and the low confidence in the effectiveness estimate carried forward into the after-action report. That is the point of the log: a decision that was sound on its information is not the same as a decision that was lucky, and the record has to hold both facts.

---

## 6. Blank multi-entry log

Copy the row structure into the working log and add one row per entry. Where the working log is kept in the Ledger, the Ledger carries the same fields; this table is the copy for the operation file and for any reviewer without Ledger access.

| Entry ID | Timestamp (UTC) | Card | Decision point | Choice | Authority relied upon | Residual risk accepted | Confidence at the time | Alternatives recorded | Dissent | Pre-registered contingency | Outcome, if known | Recorded by |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DL-0001 | «YYYY-MM-DDThh:mm:ssZ» | «card id» | «gate or moment» | «the decision, one sentence» | «EA ref, profile, depth, named approver» | «R after; risk of not acting» | «0.0 – 1.0, with basis» | «yes — see entry» | «none recorded / grounds» | «the condition and the response» | «as at update» | «name, role» |
| DL-0002 | «YYYY-MM-DDThh:mm:ssZ» | «card id» | «gate or moment» | «the decision, one sentence» | «EA ref, profile, depth, named approver» | «R after; risk of not acting» | «0.0 – 1.0, with basis» | «yes — see entry» | «none recorded / grounds» | «the condition and the response» | «as at update» | «name, role» |
| DL-0003 | «YYYY-MM-DDThh:mm:ssZ» | «card id» | «gate or moment» | «the decision, one sentence» | «EA ref, profile, depth, named approver» | «R after; risk of not acting» | «0.0 – 1.0, with basis» | «yes — see entry» | «none recorded / grounds» | «the condition and the response» | «as at update» | «name, role» |
| DL-0004 | «YYYY-MM-DDThh:mm:ssZ» | «card id» | «gate or moment» | «the decision, one sentence» | «EA ref, profile, depth, named approver» | «R after; risk of not acting» | «0.0 – 1.0, with basis» | «yes — see entry» | «none recorded / grounds» | «the condition and the response» | «as at update» | «name, role» |
| DL-0005 | «YYYY-MM-DDThh:mm:ssZ» | «card id» | «gate or moment» | «the decision, one sentence» | «EA ref, profile, depth, named approver» | «R after; risk of not acting» | «0.0 – 1.0, with basis» | «yes — see entry» | «none recorded / grounds» | «the condition and the response» | «as at update» | «name, role» |

### 6.1 Log header

| Field | Value |
| --- | --- |
| Log ID | «DL-nnn — log id» |
| Operation | «operation or card ids covered» |
| Opened (UTC) | «YYYY-MM-DDThh:mm:ssZ» |
| Closed (UTC) | «YYYY-MM-DDThh:mm:ssZ» |
| Maintained by | «name and role» |
| Filed with | «the after-action report reference» |

---

## 7. Document limitations

1. **The log records reasoning; it does not verify it.** A complete, honest entry can still rest on a mistaken reading of the evidence. The log makes the reasoning inspectable; it does not make it correct.
2. **Reconstruction is a qualitative test.** The sufficiency criterion is satisfied when a reviewer can reconstruct the decision from the record alone. The framework does not specify a quantitative test for that, and two reviewers may reconstruct differently.
3. **The log inherits the reliability of its evidence.** A decision log built on Tier 4 material inherits its weakness, however carefully the reasoning is recorded.
4. **Confidence values in the log are self-assessments** and are not independently calibrated (master design `LIM-2`).
5. **Materiality is judged by the person logging.** A decision wrongly judged immaterial is absent from the record, and nothing in the framework detects that absence except a reviewer's scepticism.
6. **The worked example is illustrative only.** The entities, figures, and timings in §5 are invented and describe no real operation.

---

*This was supported for MIA by Kilo (kilo-auto/free).*
