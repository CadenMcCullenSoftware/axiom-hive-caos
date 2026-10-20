# Escalation Request Template

| Field | Value |
| --- | --- |
| Author | MIA |
| Attribution | This was supported for MIA by Kilo (kilo-auto/free). |
| Document type | Fillable template — operational artefact, layer L6 |
| Subject | The instrument by which a rules-of-engagement ceiling is raised, and by whom |
| Scope | One request per ceiling that is to be raised, for one operation |
| Normative source | `system-design-and-framework.md` §4.3, §4.4, §5.3; `constitutional/engagement-authorisation-and-rules-of-engagement.md`; `compliance/operator-conduct-and-human-in-loop-standard.md` |
| Companion templates | `templates/operation-card.md`; `templates/decision-log.md`; `templates/rules-of-engagement-card.md` |
| Version | 1.0 |
| Status | Template; copied and completed per use |
| Language | British English; RFC 2119 keyword usage |

---

## 1. Purpose

An escalation request is a **fresh instrument**. It is never a field edit to a live card.

Raising the ceiling requires an escalation request, an approval at the depth named for the target profile, a new or amended engagement authorisation, and a new Operation Card (`ROE-3`). The request is one of those four steps: it is the application, not the permission.

A request is raised when a specific, identified action cannot lawfully be taken under the profile in force because it exceeds a ceiling, because it affects a third party without per-target authorisation, because it depends on an attribution confidence that is not held, or because the autonomy class required exceeds the ceiling. The request states precisely what is wanted, precisely which rule is in the way, and what happens if the answer is no.

> **Guidance.** A refusal by the policy engine is a successful control, not a failure, and it is recorded as a refusal (`ROE-2`). The escalation request is the formal next step after a refusal, not a way of getting around one. Where the operator believes the refusal is wrong, the route is the request, not a workaround.

---

## 2. Request fields

Copy this section into the working request and complete every field.

| Field | Req. | Value |
| --- | --- | --- |
| Request ID | Mandatory | «ESC-nnnn» |
| Card | Mandatory | «card id — the card the escalation relates to» |
| Raised by | Mandatory | «name, role, organisation» |
| Raised at (UTC) | Mandatory | «YYYY-MM-DDThh:mm:ssZ» |
| Current profile | Mandatory | «R0 – R5» |
| Requested profile | Mandatory | «R0 – R5» |
| Specific rule or ceiling exceeded | Mandatory | «the precise rule, class, or threshold — quote it» |
| Specific action or capability requested | Mandatory | «what would actually happen, to which system, described so that a reader can picture it» |
| Threat being answered | Mandatory | «the activity and its classification» |
| Evidence for the threat | Mandatory | «claim table reference — ids, labels, tiers, confidences» |
| Attribution assessment | Mandatory | «candidate, basis, alternative explanations» |
| Attribution confidence | Mandatory | «0.0 – 1.0» |
| INT-3 threshold | Mandatory | «the threshold that applies at the requested collateral class, and whether it is met» |
| Proposed action's collateral class | Mandatory | «C0 – C3» |
| Proposed action's autonomy class | Mandatory | «AC-0 – AC-4» |
| Risk of the action | Mandatory | «residual risk created, collateral exposure, irreversibility» |
| Risk of not escalating | Mandatory | «the residual risk that remains if nothing changes, and the time horizon over which it accrues» |
| Alternatives considered | Mandatory | «table below — and why each is insufficient» |
| Scope of the request | Mandatory | «table below — targets, time, budget» |
| Expiry requested | Mandatory | «YYYY-MM-DDThh:mm:ssZ, with the reason for that duration» |
| Supporting authorities | Mandatory | «table below — EA amendment, legal opinion, asset owner, external authority» |
| Deconfliction result | Mandatory | «pass / conflict found / not applicable — with the reason» |
| Abort conditions | Mandatory | «the conditions under which the requested action would be stopped» |
| Time limit for response | Mandatory | «the period within which a response is required, and what happens if there is none» |

**Alternatives considered**

| Alternative | Why it is insufficient |
| --- | --- |
| «alternative course within the current profile» | «the specific reason it does not meet the requirement» |

**Scope of the request**

| Dimension | Requested scope | Boundary |
| --- | --- | --- |
| Targets | «systems, accounts, estates, and any named third party» | «what is expressly excluded, including every tenant other than those named» |
| Time | «start and end» | «the point at which the scope lapses without further approval» |
| Budget | «the declared limit, in the units of the operation» | «what happens when the budget is consumed» |
| Actions | «the specific actions authorised, exhaustively listed» | «any action not listed is excluded» |

**Supporting authorities**

| Authority | Held | Reference |
| --- | --- | --- |
| EA amendment (draft) | «yes / no / in preparation» | «reference or "not yet drafted"» |
| Legal opinion | «yes / no» | «reference and the question put» |
| Asset owner agreement | «yes / no / not applicable» | «reference or the reason it is not applicable» |
| External authority | «yes / no / not applicable» | «reference, and the depth required» |
| Per-target authorisation for third-party effect | «yes / no / not applicable» | «reference naming the specific target» |

**Approver block**

| Role | Name | Organisation | Authority under which they may approve | Decision | Timestamp (UTC) |
| --- | --- | --- | --- | --- | --- |
| «role, e.g. director» | «name» | «organisation» | «the instrument or delegation» | «approve / approve with amendment / refuse» | «timestamp» |
| «role, e.g. legal contact» | «name» | «organisation» | «the instrument or delegation» | «approve / approve with amendment / refuse» | «timestamp» |
| «role, e.g. asset owner» | «name» | «organisation» | «the instrument or delegation» | «approve / approve with amendment / refuse» | «timestamp» |
| «role, e.g. executive» | «name» | «organisation» | «the instrument or delegation» | «approve / approve with amendment / refuse» | «timestamp» |
| «role, e.g. external authority» | «name» | «organisation» | «the instrument or delegation» | «approve / approve with amendment / refuse» | «timestamp» |

**Decision block**

| Field | Value |
| --- | --- |
| Decision | «approved / approved with amendment / refused / no answer within the time limit» |
| Effective profile granted | «R0 – R5, or the existing profile if refused» |
| Conditions attached | «any conditions, limitations, or amended scope» |
| Reasons | «the reasons given, in the approver's words» |
| Amended EA reference | «the EA id, if approved» |
| New card required | «yes — the card id once created» |
| Decision recorded by | «name and role» |
| Decision recorded at (UTC) | «YYYY-MM-DDThh:mm:ssZ» |

> **Guidance.** Where the decision is a refusal, the reasons are recorded with the same care as an approval. A refusal is a decision, it is entered in the Ledger, it is carried into the after-action report, and it is not a subject for renegotiation with the approver. Where the decision is an approval with amendment, the amendment is written into the effective scope, not left to be understood at execution time.

> **Guidance.** An approved escalation does not authorise action on the existing card. It requires an amended or new EA and a new Operation Card, because the risk analysis, the target set, and the evidence have all changed (`ROE-3`, `OP-2`).

---

## 3. Processing rules

### 3.1 Who may approve what

| Escalation to | Required depth |
| --- | --- |
| A profile ceiling not raised, but a per-target authorisation for a named third party | The named target's owner, with the legal contact notified |
| **R1 Shield** (C0) | Team lead |
| **R2 Trap** (C1) | Duty manager + legal contact |
| **R3 Deceive** (C1) | Duty manager + asset owner |
| **R4 Disrupt** (C2) | Director + legal contact + asset owner |
| **R5 Neutralise** (C3) | Executive + legal contact + external authority, and not by default |
| A collateral class above the profile ceiling | The depth named for that class, regardless of the technical simplicity of the action (`ROE-8`) |

Authoritative source: `constitutional/engagement-authorisation-and-rules-of-engagement.md`.

### 3.2 Time limit

| Rule | Statement |
| --- | --- |
| Response required within | «PTnHnMnS, stated on the request» |
| Consequence of no answer | The request is refused. No answer is a no. |
| Who may extend | The approver, in writing, once, with the reason recorded. |
| Effect while pending | The existing profile remains in force. The pending request authorises nothing. |
| Effect of a partial answer | Only what is expressly granted is authorised. Silence on a condition is not a grant. |

### 3.3 The rules of use

1. **A refusal is recorded, not contested.** A refused escalation is entered in the Ledger and carried into the after-action report. It is not renegotiated with the approver, and it is not re-submitted on the same facts without new evidence.
2. **Escalation may not be used to protect a schedule.** An operator may not raise a request in order to hold a timetable, to avoid a delay, or to avoid reporting an overrun. Where the schedule is the reason, the schedule yields.
3. **Escalation is not an approval.** An approved request authorises nothing until the amended or new EA exists and a new card is issued against it.
4. **The operator may escalate the rule, not the person.** A request challenges a ceiling, not an approver. Where the objection is to a named individual's judgement of a different matter, that is a matter for the conduct standard and the after-action report, not for this instrument.
5. **The request is complete or it is not an application.** A request missing a mandatory field is returned, not processed. The time limit does not begin until the request is complete.
6. **The request does not suspend the operation.** The operation continues under the existing profile, or stops, on its own terms. A pending request is not a reason to continue an action that the current profile does not permit, and not a reason to abandon an action the current profile does permit.

> **Guidance.** Keep the request factual and short. The approver is reading it to decide, not to be persuaded by narrative. State the ceiling, the action, the evidence, the risk on both sides, and the scope precisely.

---

## 4. A worked example

> **Example. Illustrative and fictional.** Every organisation, person, identifier, measurement, and adversary archetype below is invented for demonstration and refers to no real entity. The figures are illustrative arithmetic, not measurements. Catalogue identifiers are taken from `operational/countermeasure-catalogue.md`.

### 4.1 Request

| Field | Value |
| --- | --- |
| Request ID | ESC-2026-0044 |
| Card | OP-2026-0142 |
| Raised by | Duty operator, Corvin Exchange operations |
| Raised at (UTC) | 2026-04-16T11:20:00Z |
| Current profile | R2 Trap (collateral ceiling C1, autonomy ceiling AC-2) |
| Requested profile | R4 Disrupt (collateral ceiling C2) |
| Specific rule or ceiling exceeded | `ROE-1` and `ROE-8`: the profile is a ceiling, and a countermeasure whose collateral class exceeds the profile's ceiling requires escalation to the depth named for that class. The requested action is at C2. The profile ceiling is C1. |
| Specific action requested | Revocation of the third-party API credential set that the adversary obtained and used against the shared freight API (`OCC-39`), limited to that credential set, together with the estate's own gateway rule denying egress for the agent's service account (`OCC-17`, which acts only on the operator's estate). No other tenant's traffic is affected by the credential revocation; the egress denial is scoped to one service account on the estate's own gateway. |
| Threat being answered | AAT-7 tool-output poisoning, active on the estate for at least three days, with the agent's task signature appearing in the estate's execution log. Classification confidence 0.85. |
| Evidence | C-01 (Fact, Tier 1, 0.95), C-04 (Fact, Tier 1, 0.90), C-07 (Interpretation, Tier 3, 0.70), C-12 (Fact, Tier 1, 0.85), C-15 (Fact, Tier 2, 0.80 — the credentials are still valid and the agent continued to attempt execution after containment) |
| Attribution assessment | Candidate: the Lamplighter operator (fictional archetype). Basis: behavioural signature overlap, Tier 2. Alternative considered: an unaffiliated actor reusing a publicly described technique, disfavoured on timing correlation but not excluded. |
| Attribution confidence | 0.78 |
| INT-3 threshold | C2 requires 0.85. Not met at 0.78. |
| Proposed collateral class | C2 |
| Proposed autonomy class | AC-1 (assisted; credential revocation and egress rule applied by a named human) |
| Risk of the action | The agent loses its access and cannot be observed further through that channel; the credential is the adversary's session credential, so revocation may terminate the adversary's access to its own tooling; the freight API operator is notified and may treat the revocation as a service incident affecting an unknown third party. |
| Risk of not escalating | The agent retains a valid credential and a live channel to a third-party service; the containment remains partial and depends on the agent's continued use of the observed pattern; residual risk of recurrence is estimated at 0.9 of the pre-containment figure, assessed over a 14-day horizon. |
| Alternatives considered | (a) Continue with containment alone — insufficient: the credential remains valid, the channel remains open, and the agent demonstrated post-containment attempt on 2026-04-15. (b) Credential invalidation at the identity source (`OCC-34`) with per-target authorisation from the freight API operator — insufficient: not obtainable inside the time horizon, and it would not bind the estate's own egress, which is where the observed pattern re-enters. (c) Rate limiting on the estate gateway for the agent's account only — insufficient: does not remove the credential, and prior containment showed the agent adapting its timing. (d) Escalate for an attribution-confidence increase only — insufficient: a higher confidence does not change the credential's validity or the open channel. |
| Scope of the request | Targets: the third-party API credential set identified as C-15 (revocation, `OCC-39`), and the estate gateway rule for the agent's service account only (egress control, `OCC-17`). Excluded: every other tenant of the freight API, the freight API's operator's own infrastructure beyond the credential set named, and all other services in the estate. Time: 2026-04-16T12:00:00Z to 2026-04-23T12:00:00Z. Budget: one credential revocation and one egress rule; no automated repetition. Actions: revocation of the named credential set, and the estate-side egress rule as described. No other action is authorised. |
| Expiry requested | 2026-04-23T12:00:00Z — the length of time the agent would need to obtain replacement credentials and re-establish a channel, plus margin. |
| Supporting authorities | EA amendment: in preparation, drafted as EA-2026-007-A1. Legal opinion: held, Fictional Legal Contact opinion LEG-2026-011, advising that revocation of an adversary's own third-party API credential at the API operator, with the operator notified, is a C2 action requiring the operator's notification rather than its consent. Asset owner agreement: the owner of the estate's agent estate, from which the credential was obtained, has agreed to the request. External authority: not applicable at C2. Per-target authorisation for third-party effect: the API operator's notification is a condition of the action; no separate per-target authorisation is held, and the legal opinion is the stated basis for proceeding without one at this scope. |
| Deconfliction result | Pass — checked against the deconfliction map 2026-04-16T11:05:00Z; no live legitimate operation intersects the credential set or the egress rule. |
| Abort conditions | Any effect observed on another tenant of the freight API; the freight API's operator reports a service impact attributable to this action; the credential revocation is found to have affected an account other than the one named; the estate's own logistics workflow loses access to the freight API for longer than 30 minutes; the legal contact becomes unreachable. |
| Time limit for response | PT4H, because the observed pattern repeated after containment on 2026-04-15 and the authorising depth is within reach during the shift. |

### 4.2 Decision

| Field | Value |
| --- | --- |
| Decision | Approved with amendment |
| Effective profile granted | R3 Deceive for the estate-side measures, with a per-target C2 action authorised for the named credential set only. The requested R4 profile was not granted in full. |
| Conditions attached | The egress rule is limited to the agent's service account and must be removed within the expiry; the freight API's operator is notified within 60 minutes of the action; the action is performed manually at AC-1; no further credential is revoked without a new request. |
| Reasons | "Approved on the narrow scope only. The attribute gap is the attribution confidence of 0.78 against the 0.85 the class requires, which the operator has acknowledged and which the narrow, single-credential scope mitigates. The collateral effect on other tenants of the shared platform is real and is not accepted at this volume; the amended scope does not affect them." |
| Amended EA reference | EA-2026-007-A1 |
| New card required | Yes — OP-2026-0158, opened 2026-04-16T16:05:00Z |
| Decision recorded by | Fictional Director, Corvin Exchange; Fictional Legal Contact, Corvin Exchange; Fictional Asset Owner (agent estate), Corvin Exchange |
| Decision recorded at (UTC) | 2026-04-16T15:40:00Z |

> **Guidance.** The example shows the ordinary shape of an escalation: a narrowly scoped request, an explicit acknowledgement that a threshold is not met, an approval that is narrower than the request, and a new card rather than an edit to the old one.

---

## 5. Approval ladder

| Target profile or class | Collateral ceiling | Approval depth | Additional requirement |
| --- | --- | --- | --- |
| **R0 Observe** | C0 | Operator | — |
| **R1 Shield** | C0 | Team lead | — |
| **R2 Trap** | C1 | Duty manager + legal contact | The legal contact's judgement is a necessary input, not a formality |
| **R3 Deceive** | C1 | Duty manager + asset owner | Reversibility argument where any element is irreversible |
| **R4 Disrupt** | C2 | Director + legal contact + asset owner | Attribution confidence at or above 0.85; the alternative attribution considered is recorded |
| **R5 Neutralise** | C3 | Executive + legal contact + external authority | Not by default; attribution confidence at or above 0.95; refusal to proceed if the threshold is not met, irrespective of operational pressure |
| Any class above the profile ceiling | — | The depth named for that class (`ROE-8`) | Recorded on the request, with the specific rule quoted |

Authoritative source: `constitutional/engagement-authorisation-and-rules-of-engagement.md`. Where this table and that document differ, that document governs.

---

## 6. Document limitations

1. **The request creates no authority.** Approval of a request is one of four steps; the amended or new EA and the new card are the others.
2. **Approval is not a legality opinion.** The approving authority's judgement is theirs. The framework encodes authorisation structure, not legal judgement (master design `LIM-10`).
3. **The time limit is a control against drift, not a guarantee of a decision.** An unanswered request is a refusal by rule, and the operation proceeds or stops on its own terms.
4. **The worked example is illustrative only.** The entities, figures, and timings in §4 are invented and describe no real operation, approval, or incident.
5. **The template does not assess proportionality.** It requires the comparison to be written down; it does not judge it.

---

*This was supported for MIA by Kilo (kilo-auto/free).*
