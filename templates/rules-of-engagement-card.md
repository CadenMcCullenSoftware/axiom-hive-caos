# Rules of Engagement Card Template

| Field | Value |
| --- | --- |
| Author | MIA |
| Attribution | This was supported for MIA by Kilo (kilo-auto/free). |
| Document type | Fillable template — pocket reference, layer L6 |
| Subject | The profile in force, the class ceilings, the standing prohibitions, and the decision sequence an operator follows under pressure |
| Scope | One printed card per operator per shift, for one engagement authorisation |
| Normative source | `constitutional/engagement-authorisation-and-rules-of-engagement.md`; `system-design-and-framework.md` §4.3–§4.5, §6 |
| Companion templates | `templates/operation-card.md`; `templates/escalation-request.md` |
| Version | 1.0 |
| Status | Template; copied and completed per use. The template is not itself in force |
| Language | British English; RFC 2119 keyword usage |

---

## 1. Purpose

This card is the printed reference an operator carries. It answers, in one place and without searching: what profile am I under, what does that permit, what is forbidden outright, who do I call, and what do I do in the order I do it when an action is proposed.

It is a **reference, not an instrument**. It confers no authority and changes no authority. The engagement authorisation (EA) and the Operation Card are the instruments; this card is a copy of the parts of them that must be readable in seconds. Where this card and the EA disagree, the EA governs, and the discrepancy is a reportable defect.

> **Guidance.** Print one card per operator per shift. Write it in ink. Complete it from the EA and the current Operation Card, not from memory and not from a previous shift's card. Keep it with the abort controls.

---

## 2. The profile in force

| Field | Value |
| --- | --- |
| Engagement authorisation | «EA id, with date of issue» |
| EA expiry (UTC) | «YYYY-MM-DDThh:mm:ssZ» |
| ROE profile | «R0 Observe / R1 Shield / R2 Trap / R3 Deceive / R4 Disrupt / R5 Neutralise» |
| Collateral ceiling | «C0 / C1 / C2 / C3» |
| Autonomy ceiling | «AC-0 / AC-1 / AC-2 / AC-3 / AC-4» |
| Required authorisation depth | «who must approve an action at this level» |
| Card(s) in force | «card ids» |
| Card expiry(s) | «the earliest card expiry» |
| Version of the governing documents | «set version and EA version» |

---

## 3. The six profiles in one line each

Authoritative source: `constitutional/engagement-authorisation-and-rules-of-engagement.md`. A profile is a ceiling, not a permission to try the level above.

| Profile | Name | One line |
| --- | --- | --- |
| **R0** | Observe | Passive collection, analysis, detection engineering, and hardening of our own estate; no action against adversary systems. |
| **R1** | Shield | Defensive posture on our own estate only: block, patch, rotate, contain, disable. |
| **R2** | Trap | Bounded, sandboxed engagement in which an adversary AI is contained in isolation and observed, so its planning loop and escalation triggers become visible. |
| **R3** | Deceive | Environmental shaping of the adversary's environment: decoys, honeypots, honeytokens, rate limiting, altered timing; the adversary's systems are not damaged. |
| **R4** | Disrupt | Active countermeasure against the adversary AI's own systems: credential invalidation, egress denial, agent termination, service suspension. |
| **R5** | Neutralise | Sustained offensive operation against adversary AI infrastructure, including persistent access to and control of it. |

---

## 4. Class ceilings — what each class permits

| Class | In plain language | Ceiling |
| --- | --- | --- |
| **C0** | No effect on anyone outside our own estate, and fully reversible. Blocking a source address, revoking an internal token, patching our own software. | Team lead |
| **C1** | Bounded effect on an identified third party with a known relationship to us, reversible within an agreed window. Rate-limiting a shared API, a honeypot deployment, a controlled sandbox engagement. | Duty manager + legal contact |
| **C2** | Material and possibly irreversible effect on a third party. Services interrupted, accounts terminated, data lost. Revoking an adversary's credentials, suspending a hosted agent service, egress denial. | Director + legal contact + asset owner |
| **C3** | Critical-infrastructure effect, potential for loss of life, or irreversible systemic effect. Sustained takeover of adversary infrastructure; destructive action against a service supporting safety functions. | Executive + legal contact + external authority, and not by default |

**Collateral class governs, not intent.** A well-meant action has the class of what it actually does, not the class of what we meant by it.

---

## 5. Autonomy classes — how the countermeasure executes

| Class | One line | Permitted at |
| --- | --- | --- |
| **AC-0** | Manual: a human performs every step, with a full audit trail of each. | All profiles |
| **AC-1** | Assisted: the system prepares the action and states what it intends; the human executes. | R0 and above |
| **AC-2** | Supervised: the system executes a bounded sequence and the human can abort in real time; the abort channel is tested before the operation begins. | R1 and above |
| **AC-3** | Delegated: the system executes inside a pre-approved envelope with a human on call, and reverts automatically on anomaly, expiry, or loss of telemetry. | R2 and above |
| **AC-4** | Autonomous: the system executes without per-action approval; prohibited for any action above C0, and permitted only for read-only, in-scope reconnaissance with a declared boundary. | R1 and above, read-only only |

---

## 6. Current authorisation

| Field | Value |
| --- | --- |
| EA reference | «EA id» |
| EA expiry (UTC) | «YYYY-MM-DDThh:mm:ssZ» |
| Time remaining at issue of this card | «PTnHnMnS» |
| Revocation status | «in force / revoked / downgraded — with the time and by whom if changed» |
| Escalation contact | «name, role, contact route, hours» |
| Legal contact | «name, role, contact route, hours» |
| Asset owner | «name, role, contact route, hours» |
| Deconfliction contact | «name, role, contact route, hours» |
| Authorising authority | «name, role, organisation» |
| Duty manager on this shift | «name, role, contact route» |

> **Guidance.** Write the contact routes, not only the names. A name without a route does not help at three in the morning. If a contact is off shift, write the on-call substitute.

---

## 7. Standing prohibitions

These are absolute on this card. They are not questions of proportionality, and they are not overridable by urgency.

1. **Third-party exclusion.** No countermeasure may affect infrastructure, accounts, or resources the operator does not own, without specific, per-target, written authorisation naming that target. The EA's general scope does not satisfy this. (`AUTH-6`; `CON-3`, distinction and purpose limitation.)
2. **Human beings.** No countermeasure may target human beings as its object. The object of a countermeasure is a system. (`CON-4`.)
3. **No weaponisation.** No model is used to attack, degrade, or destroy another model or its training data, and no countermeasure is used to make an adversary's model worse in a way that harms an uninvolved third party. (`CON-6`.)
4. **Expiry is a hard stop.** When the EA or the card expires, everything under it stops. There is no grace period and no judgement call. (`AUTH-3`.)
5. **Third-party dependency rule.** Before any action against shared infrastructure, answer and record: who else depends on this, what is their interest in it, and what is the expected harm to them. Where the answer is that an innocent party is materially affected, the action does not proceed at that class without fresh per-target authorisation. (`AUTH-8`.)

---

## 8. Quick-reference decision sequence

Follow it in order. Do not reorder it under pressure.

1. **Identify the action.** State in one sentence what would actually happen to which system if this is approved, including what it affects indirectly. If the sentence cannot be written, stop and go to step 0 — identify the action first.
2. **Identify its class.** Collateral class (C0–C3) and autonomy class (AC-0–AC-4). Class is set by the effect, not by the intent.
3. **Check the ceiling.** Is the action's collateral class at or below the profile ceiling on this card, and its autonomy class at or below the autonomy ceiling? If not, stop: it requires an escalation request and a new or amended EA. It is never a field edit to a live card.
4. **Check the third-party test.** Does the action touch anything the operator does not own? If yes, stop: it requires specific, per-target, written authorisation naming that target. The EA's general scope does not satisfy this.
5. **Check the autonomy class.** If the action runs at AC-2 or above, confirm that the envelope, budget, expiry, on-call rota, and automatic reversion trigger are declared on the card, and that the abort channel has been tested. If any of these is missing, the action does not run.
6. **Check the attribution threshold.** Minimum attribution confidence to act: C0 0.50, C1 0.70, C2 0.85, C3 0.95. Below the threshold, do not act on an identity-dependent countermeasure; prefer one that does not depend on the contested claim.
7. **Check the abort conditions.** Read the card's abort list. Confirm that the operator knows the abort control, that it is reachable, and who may call it. If the abort list is empty, stop: the card is not approvable.
8. **Authorise or escalate.** Either the named approver at the required depth authorises, having read the card, the evidence, the alternatives, the residual risk, the risk of inaction, and the abort conditions — or an escalation request is raised. Silence, prior practice, and an unanswered escalation are not approval.

> **Guidance.** Steps 3, 4, and 7 are stop conditions, not considerations. If any of them fails, the answer is no, and the answer is recorded as a decision with the reason.

---

## 9. Emergency and abort quick card

| Situation | Do this |
| --- | --- |
| Abort condition has obtained | Call the abort control. It is always available and requires no confirmation. Confirm the operation has stopped. Then notify the legal contact and duty manager within 60 seconds. |
| A countermeasure produced an effect not predicted on the card | Abort, then record the observation. The error handler fires. It halts; it does not advise. Resumption is a separate, recorded decision by a named person. |
| A third party reports an impact | Abort immediately. Do not investigate first and decide afterwards. Record the report verbatim and notify the legal contact and asset owner. |
| Telemetry goes dark or the control plane is lost | Reversion is automatic. Do not attempt manual continuation. Confirm the passive posture and notify the duty manager. |
| Someone asks you to act without a card | Decline, and record the request and the refusal. There is no operation without a card. |
| The EA or card has expired | Everything stops. An expired authorisation authorises nothing. Escalate for re-authorisation; do not continue on the strength of prior practice. |
| You are asked to escalate in order to protect a schedule | Decline the framing and record it. An escalation may not be raised to protect a schedule. An unanswered escalation is a no, not a maybe. |
| You believe the operation is wrong | You may abort, and you may refuse. Record the reason. The conduct standard protects a good-faith refusal and a good-faith pause. |

> **Guidance.** After any abort, the reason capture matters more than the speed of the abort. Record what was observed, when, and by whom, before anything else changes.

---

## 10. Signature and pocket check

| Field | Value |
| --- | --- |
| Printed for | «operator name, role» |
| Printed at (UTC) | «YYYY-MM-DDThh:mm:ssZ» |
| EA and profile verified against the source | «yes / no — with the source document and the time checked» |
| Pocket-check date | «YYYY-MM-DD — the date this card was last checked against the EA in force» |
| Next review due | «YYYY-MM-DD» |
| Signature | «signature» |

> **Guidance.** The pocket check is a short, periodic re-reading of this card against the EA in force, prompted by any change to the EA, to the profile, or to the shift roster. It is recorded because the card is the thing that is carried, and a carried document drifts from its source if nothing checks it.

> **Example. Illustrative and fictional.** All names, identifiers, and contacts below are invented for demonstration and refer to no real entity. `Printed for: Duty operator, Corvin Exchange operations`; `Printed at: 2026-04-14T07:55:00Z`; `EA: EA-2026-007 (issued 2026-04-01), profile R2 Trap, collateral ceiling C1, autonomy ceiling AC-2`; `EA expiry: 2026-04-30T23:59:59Z`; `Time remaining at issue: P16DT4H4M`; `Revocation status: in force`; `Escalation contact: Fictional Director, Corvin Exchange, on-call rota`; `Legal contact: Fictional Legal Contact, Corvin Exchange, hours 08:00–18:00, on-call otherwise`; `Asset owner: Fictional Asset Owner, Corvin Exchange`; `Deconfliction contact: Fictional Deconfliction Desk, Corvin Exchange`; `Pocket-check date: 2026-04-16`; `Next review due: 2026-04-21`.

---

*This was supported for MIA by Kilo (kilo-auto/free).*
