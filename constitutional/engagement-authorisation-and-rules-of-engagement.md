# Engagement Authorisation and Rules of Engagement

| Field | Value |
| --- | --- |
| Author | MIA |
| Attribution | This was supported for MIA by Kilo (kilo-auto/free). |
| Document type | Constitutional instrument |
| Subject | The mandate, scope, rules of engagement, collateral classes, autonomy classes, authorisation ladder, and constitutional conduct constraints for counter-adversary operations |
| Scope | Layers L0 and L1 of CAOS; the authorisation boundary within which every other document in the set operates |
| Requirement traceability | `AUTH-1` to `AUTH-8`; `ROE-1` to `ROE-8`; `CON-1` to `CON-14`; document limitations `LIM-C1` to `LIM-C12` |
| Version | 1.0 |
| Status | Authoritative for the authorisation model; the constitutional anchor of the set and the first document to be loaded |
| Supersedes | Nothing. First issue. |
| Companion documents | Sixteen companion documents; the register with paths is at Section 1.1 |
| Relationship to the Axiom Hive set | Operational extension. Governed by `../../Docs/system-design-and-framework.md`; see master design §3.4 and limitation `LIM-13` |

---

## 1. Purpose and scope

### 1.1 Purpose

This document is the constitutional instrument of the CAOS set. It states the mandate under which counter-adversary operations are conducted, the boundary of that mandate, the classes by which the boundary is expressed, and the conduct constraints that bind every actor inside it. Every other document in the set is subordinate to it, and each is bounded by it.

The document carries three kinds of content: the requirements that constitute the instrument (`AUTH-1` to `AUTH-8`, `ROE-1` to `ROE-8`, `CON-1` to `CON-14`); the classifications by which authorisation is expressed (ROE profiles, collateral classes, autonomy classes, target classes, reversibility categories); and the disclosure of what those classifications do and do not establish (Section 13, Section 15).

### 1.2 The engagement authorisation is the root of trust

The engagement authorisation (EA) is the root of trust for every counter-adversary operation. Authority to act does not originate in the system, in a prior operation, in the behaviour of an adversary, in the urgency of a situation, or in the recommendation of a model. It originates in a written EA issued by a named human authority, and it exists only for as long as that EA says it does. Where no EA is in force, there is no operation.

This is the load-bearing commitment of the set and it is expressed structurally rather than aspirationally. The policy engine refuses a dispatch that has no EA behind it; the refusal is a successful control and is recorded as one.

### 1.3 The framework confers no authority of its own

Neither this document, nor the policy engine, nor the decision-support model, nor any model within the system creates legal authority, contractual authority, or moral permission. The framework structures authority that a named human has already granted, bounds the action that authority permits, and refuses the action that authority does not cover. It is an instrument for the exercise of authority, not a source of it.

Where this document's controls and a lawful person's judgement differ, the difference is a question for the authorising authority and the named legal contact, not a defect in the document and not a matter for the engine to resolve. The engine cannot tell a lawful operation from an unlawful one; it can only tell an authorised operation from an unauthorised one.

### 1.4 This document is structural and not a source of legal judgement

This document specifies structure: what an authorisation must contain, what a profile admits, what a class means, who may approve what, and what conduct is forbidden. It does not supply legal judgement. Whether an operation is lawful in the jurisdiction in which it is proposed, proportionate to the threat it answers, and consistent with the operator's obligations to third parties is determined by the named legal contact and the authorising authority, on the facts before them. The framework encodes authorisation structure; it does not encode legal advice.

### 1.5 Companion document register

| # | Path | Role | Bearing on this document |
| --- | --- | --- | --- |
| 1 | `system-design-and-framework.md` | Consolidated design | Supplies the canonical identifiers, the mandate model, and the layer structure. Authoritative for relationships between documents |
| 2 | `README.md` | Set index | Canonical map, controlled vocabulary, identifier registry, change control |
| 3 | `compliance/operator-conduct-and-human-in-loop-standard.md` | Conduct standard | Owns the human-in-the-loop requirements (`HITL-1` to `HITL-8`), operator duty, refusal and pause obligations, and escalation ethics |
| 4 | `operational/mission-lifecycle-and-decision-loop.md` | Operational specification | Owns the phase and gate sequence, the Operation Card lifecycle, the error handler, and the deconfliction procedure |
| 5 | `operational/decision-support-and-scoring-model.md` | Specification | Owns the threat score, attribution confidence, residual risk, and the admissibility algebra (`AD-1` to `AD-13`) |
| 6 | `operational/countermeasure-catalogue.md` | Catalogue | Owns the countermeasures, their declared collateral class, reversibility, autonomy class, blast radius, and intelligence yield |
| 7 | `operational/adversary-ai-taxonomy-and-threat-model.md` | Specification | Owns the AAT taxonomy against which threat is stated and against which attribution is reasoned |
| 8 | `operational/platform-architecture-and-agent-containment.md` | Architecture | Owns the policy engine, the control plane, the ledger, and the resilience behaviour that Section 10 depends upon |
| 9 | `operational/watchfloor-interface-specification.md` | Interface specification | Owns the console surfaces on which approval, abort, and disclosure are presented |
| 10 | `reference/audit-and-conformance-procedures.md` | Reference procedure | Owns the procedure by which conformance with this document is assessed |
| 11 | `templates/operation-card.md` | Template | The artefact on which the authorisation, the abort conditions, and the risk are recorded |
| 12 | `templates/rules-of-engagement-card.md` | Template | The pocket reference for the profile in force and the escalation contacts |
| 13 | `templates/escalation-request.md` | Template | The instrument by which a profile ceiling is raised |
| 14 | `templates/decision-log.md` | Template | The record of rationale, alternatives, and risk |
| 15 | `templates/after-action-report.md` | Template | The structured report in which honesty of effect and confidence is discharged |
| 16 | `../../Docs/system-design-and-framework.md` | Axiom Hive governance set | The general governance standard of which this set is an operational extension |

### 1.6 Boundary of this document

| Concern | Owner | Treatment here |
| --- | --- | --- |
| Decision-support algebra, scoring, admissibility | `operational/decision-support-and-scoring-model.md` | Referenced only, as a constraint the authorisation places on it |
| Adversary taxonomy and threat model | `operational/adversary-ai-taxonomy-and-threat-model.md` | Referenced only |
| Operator console and interface | `operational/watchfloor-interface-specification.md` | Referenced only, where an interface property bears on a constitutional requirement |
| Platform, policy engine, control plane, ledger | `operational/platform-architecture-and-agent-containment.md` | Referenced only, as the mechanism that enforces this document |
| Countermeasure content and entry-level reversibility | `operational/countermeasure-catalogue.md` | Referenced only; this document defines the classes the catalogue assigns values against |
| Human-in-the-loop checkpoints | `compliance/operator-conduct-and-human-in-loop-standard.md` | Referenced; `CON-1` states the constitutional principle that underlies them |

Where this document restates a definition, it does so for self-containment, and the owner document remains authoritative for it.

---

## 2. Interpretation of normative terms

The terms **must**, **must not**, **should**, **should not**, and **may** are to be interpreted as described in RFC 2119.

- **Must / must not** denote absolute requirements. A departure is a non-conformance, not a preference.
- **Should / should not** denote recommendations that may be departed from only where legitimate reasons exist. Any departure must be made explicit and recorded on the card or in the decision log.
- **May** denotes optional behaviour that remains at the discretion of the named human within the constraints of this document and within the constraints of the authorisation in force.

Two further interpretations apply throughout.

- Where this document records a claim about the behaviour of the framework or of the system that implements it, that claim is an **architectural assertion** of the framework authors and not, absent an explicit statement to the contrary, an independently verified property. Those claims are listed in Section 13.
- Where this document states a class, a ceiling, or a threshold, the class is a property of the action as deployed. The classification is made by the named human at the required approval depth, and it is recorded with its basis.

---

## 3. Defined terms

| Term | Definition |
| --- | --- |
| **engagement authorisation (EA)** | The written, time-bounded mandate that is the root of trust for a counter-adversary operation. It states the purpose, the legal basis, the authorised and excluded targets, the profile, collateral, and autonomy ceilings, the time bounds, the named authorities, the reporting and disclosure obligations, and the revocation conditions. |
| **rules-of-engagement profile (ROE profile)** | One of R0 Observe, R1 Shield, R2 Trap, R3 Deceive, R4 Disrupt, R5 Neutralise. A ceiling on what an operation may do, expressed as a set of permitted action classes, a maximum collateral class, and a maximum autonomy class. A profile is a ceiling and not a permission. |
| **collateral class** | One of C0, C1, C2, C3. The class of the effect a countermeasure has on parties outside the operator's own estate. It determines the approval depth required, and it is determined by effect and never by intent. |
| **autonomy class** | One of AC-0 Manual, AC-1 Assisted, AC-2 Supervised, AC-3 Delegated, AC-4 Autonomous. A property of how a countermeasure executes and not of how capable it is. |
| **target class** | One of T0, T1, T2, T3. A classification of what a countermeasure acts upon, used in the authorisation ladder at Section 8. T0 the operator's own estate; T1 the adversary's behaviour expressed through the operator's own environment; T2 an adversary system or infrastructure with no third-party dependency; T3 an adversary system or infrastructure on which a third party depends, or whose disruption carries a safety, critical-service, or cross-border consequence. |
| **authorised target** | A system, estate, account, network, identity, or organisation named in the EA as being in scope. Action against an authorised target is permitted only within the profile, class, and time bounds of the EA. |
| **excluded target** | A named category that is out of scope. The exclusion of third-party infrastructure not separately authorised is mandatory in every EA and cannot be omitted. |
| **third-party dependency** | Any reliance by a party other than the operator and the adversary upon infrastructure, credentials, capacity, or data that a countermeasure would affect. A third-party dependency is a fact about the deployment, not a characterisation of the adversary. |
| **identity-directed action** | A countermeasure directed at the adversary's identity: a principal, an account, an API credential, a signing key, a session, or an attributable source. Its effect is confined to the identity, and it does not damage shared infrastructure in order to reach it. |
| **infrastructure-directed action** | A countermeasure directed at infrastructure rather than at an identity: a host, a service, a network path, a shared gateway, a compute entitlement, a tenant. It carries a collateral class of at least one class above the equivalent identity-directed action, because it reaches every party that depends on the infrastructure. |
| **reversible** | The countermeasure's effect can be fully undone by an action available to the operator within the stated window, with no residual effect on a third party and no permanent loss of a capability. |
| **reversed** | The effect has been withdrawn, or is in the process of withdrawal, and the entry into the withdrawn state must itself be verified. This is a state reached by action and not a property of a countermeasure in its armed condition. |
| **low** (reversibility) | The effect cannot be fully undone and may only be attenuated. The irreversible elements must be enumerated on the card and argued for under `ROE-7`. |
| **none** (reversibility) | The effect cannot be undone by any action available to the operator: a secret is disclosed, a capability is destroyed, a capability the adversary depended upon is permanently removed, or an artefact is irretrievably lost. |
| **deconfliction** | The check that a countermeasure does not interfere with a live legitimate operation, and the procedure by which a conflict is identified and resolved. The procedure is owned by `operational/mission-lifecycle-and-decision-loop.md`; the constitutional requirement is stated at Section 9. |
| **escalation request** | The instrument by which a profile, collateral, or autonomy ceiling is raised, containing the reason for the request, the evidence, the residual risk, the requested depth, and the abort conditions. Owned by `templates/escalation-request.md`. |
| **reversion** | The automatic return of an operation to the passive posture, with the termination of outstanding autonomy grants and the notification of the named authorities. Reversion is a mechanical event and not a decision. |
| **abort condition** | A stated condition on the Operation Card which, if observed, terminates the operation and returns it to the passive posture. A card with an empty abort list is not admissible. |
| **autonomy budget** | A declared, quantified allowance of autonomous action that the system consumes as it acts, measured in the units the card declares: dispatches, affected objects, actions per period, spend, or time. Exhaustion of the budget triggers reversion. |
| **envelope** | The declared boundary within which an autonomous countermeasure may act: the target set, the technique set, the rate limits, the time window, the confidence floor, and the conditions under which the system may proceed without further reference to a human. |
| **the Operation Card** | The atomic unit of authorised work: a document, a data structure, and a legal instrument at once. It carries the authority, the target set, the threat assessment, the selected countermeasures, the autonomy grant, the abort conditions, the risk assessment, the evidence, and the decision. |
| **attribution confidence (c)** | The stated probability that activity is attributable to a specific adversary, in the interval [0.0, 1.0]. It is an estimate with a stated basis and not a fact. Owned by `operational/decision-support-and-scoring-model.md`. |
| **residual risk (R)** | The risk carried forward after the selected countermeasures: `R = S_eff × (1 − e)`. It is the figure the operator is accountable for and the figure carried into the after-action report. Owned by `operational/decision-support-and-scoring-model.md`. |
| **S_eff** | The effective threat: `S_eff = S × c`, the quantity to which the escalation ladder is applied. Owned by `operational/decision-support-and-scoring-model.md`. |
| **the error handler** | The single enforcement point to which every gate resolves. It halts progress, requires the issue to be recorded, and routes the work to re-verification or transparent rewriting. Owned by `operational/mission-lifecycle-and-decision-loop.md`. |
| **architectural assertion** | A statement of intended system behaviour that has not been independently substantiated. See Section 13. |

### 3.1 Reversibility: the four categories, and what counts as irreversible

The four categories are a four-point scale on the degree to which a countermeasure's effect can be undone by the operator. They are applied to the countermeasure as deployed and not to its catalogue entry in the abstract.

| Category | What it means | Operational test | Example |
| --- | --- | --- | --- |
| **Reversible** | The effect can be fully undone by an action available to the operator within the stated window, with no residual effect on a third party and no permanent loss of a capability. | Name the undo action and the window. If the undo action cannot be performed by the operator alone, the value is not reversible. | A rate limit applied to a shared API that the operator may lift; a credential the operator itself issued and may reissue; a block rule against a source address on the operator's own perimeter. |
| **Reversed** | The effect has been withdrawn, or is in the process of withdrawal, and the withdrawal has been verified. | The undo has been executed and the resulting state confirmed. The confirmation is recorded. | A rate limit lifted and the return of normal throughput confirmed on the shared API. |
| **Low** | The effect cannot be fully undone but may be attenuated. The irreversible elements are enumerated on the card. | Name the elements that persist. Name the action that reduces the harm without removing it. | A rate limit that continues to degrade a third party's throughput for the remainder of an observation window; a partial credential revocation leaving residual impairment; a sustained deception that alters adversary behaviour with no undo available. |
| **None** | The effect cannot be undone by any action available to the operator. | No undo action exists, or the undo action exists but is not available to the operator. | A secret disclosed; a capability destroyed; a capability the adversary depended upon permanently removed; an artefact irretrievably lost. |

**Which actions count as irreversible, and why.** An action is irreversible where at least one of three conditions holds:

1. **The resource cannot be reconstructed from within the operator's control.** The information, artefact, or capability needed to restore the prior state is held by a party the operator does not control, and the operator has no mechanism to obtain or compel its return. Disclosure of a secret held by the adversary is irreversible in this sense.
2. **The harm is borne by a party that has no route to remedy.** The affected party cannot restore its own position and cannot reach the operator. Terminating a service the operator does not own, where termination is not resumable, is irreversible in this sense because the party that bears the interruption is not the party that chose it.
3. **The change is in the adversary's capability and cannot be unlearned.** A capability the adversary depended upon is permanently removed, or the adversary's learned model of the environment is altered. Restoration would require the adversary's own action, which is not within the operator's gift.

Two invariants hold across the set and are enforced against the catalogue. First, a countermeasure at collateral class C0 is **Reversible** or **Reversed**, because C0 is defined as having no effect outside the operator's own estate and being fully reversible. Second, a countermeasure whose reversibility is **None** is at collateral class C2 or above, and where it is at C2 its irreversible elements are named in the catalogue entry and on the card.

---

## 4. The engagement authorisation

### 4.1 The elements of an EA

Every counter-adversary operation is conducted under a written EA. The EA is a document with mandatory elements. An EA that omits any mandatory element is incomplete, and an incomplete EA authorises nothing.

| Element | Content | Mandatory |
| --- | --- | --- |
| **Purpose** | The specific objective the authorisation exists to permit, stated so narrowly that it could not be read to cover a materially different operation. | Yes |
| **Legal basis** | The specific statutory, contractual, or delegated authority relied upon, the jurisdiction it operates in, and the instrument relied upon by name. | Yes |
| **Authorised targets** | The systems, estates, accounts, networks, identities, and organisations in scope, identified as specifically as the text allows. | Yes |
| **Excluded targets** | Named categories that are out of scope, always including third-party infrastructure not separately authorised. | Yes |
| **Maximum ROE profile** | The highest rules-of-engagement profile that may be used without further approval (Section 5). | Yes |
| **Collateral ceiling** | The highest collateral risk class that any countermeasure under the EA may reach (Section 6). | Yes |
| **Autonomy ceiling** | The highest autonomy class that any countermeasure under the EA may reach (Section 7). | Yes |
| **Time bounds** | Start and expiry, and the rule that no operation continues past expiry without re-authorisation. | Yes |
| **Named authorities** | The operator, the authorising authority, the escalation contact, and the legal contact, each by name and role. | Yes |
| **Reporting and disclosure obligations** | What must be reported, to whom, and by when; and the disclosure owed to affected third parties where safety or legal consequences bear (`CON-8`). | Yes |
| **Revocation conditions** | The circumstances under which the authorisation terminates early and automatically. | Yes |
| **Required training and clearance of operators** | The training, clearance, and currency of competence each role must hold to act under this EA, and the check that establishes currency. | Yes |
| **Liaison contact** | The named contactable party, with role and contact route, through which external or third-party liaison is conducted during the engagement. | Yes |

An EA is issued by a named human authority. It is not issued by a model, by a schedule, by a policy engine, or by an operator on the strength of urgency.

### 4.2 Requirements

**AUTH-1 — Precondition.**
No counter-adversary operation may be opened without an EA in force. The absence of an EA is a hard stop in the policy engine and not a prompt for a model to improvise. Where the operator believes an operation is warranted but no EA exists, the only available actions are the collection and analysis actions of profile R0 and the raising of an escalation request to the issuer. Establishing an EA out of hours, where the standing procedure permits it, is the issuer's decision and not the operator's.

**Worked consequence.** An operator faces a live, escalating campaign at night with no EA in force and a clear view of the adversary's agent infrastructure. The card cannot be opened; the dispatch is refused at the authorisation gate and the refusal is logged. The operator opens an observation card under the standing observation authority, records the assessment of risk of inaction, and raises an escalation request. If the issuer declines to authorise, the campaign continues to be observed and the decision not to act is recorded with its reasons. Doing nothing is a lawful outcome and it is a recorded one.

**AUTH-2 — Narrow construction.**
Where the scope of an EA is capable of two readings, the reading that authorises less action prevails. This is the interpretive rule the system applies to its own authorisations and it is applied to the EA text itself, to the target sets it names, and to any practice alleged to have grown up around it. Precedent, custom, and the accumulated practice of the team do not expand an EA.

**Worked consequence.** An EA authorises "countermeasures against the adversary's agent infrastructure". The adversary's agent runs in a tenant on a shared platform. The narrow reading reaches the agent's own tenant-scoped resources and no further. The shared platform is not covered, so the countermeasure that revokes a gateway-wide credential is not authorised by this EA and must go to per-target authorisation.

**AUTH-3 — Expiry is a hard stop.**
An EA that has expired authorises nothing. On expiry the system revokes every card under it, withdraws outstanding autonomy grants, releases armed actions, and requires re-authorisation. This happens without a judgement call and without a notice period that an operation may claim against.

**Worked consequence.** A deception deployment continues under an EA that expires at 06:00. At 06:00 the control plane reverts the deployment and raises the notification. The operator who was mid-operation may not let the deployment run down gracefully; the reversion is immediate.

**AUTH-4 — Revocation is immediate.**
A revoked EA terminates all in-flight operations, revokes outstanding autonomy grants, and raises a notification. Revocation is not queued behind a running operation and is not deferred until the current step completes. A revocation takes effect on all cards within one control-plane cycle.

**Worked consequence.** The issuer revokes the EA because a legal development has removed the basis on which the operation was conducted. The running operation terminates at once; the operator is notified; the evidence already produced is preserved; the card is closed to the error handler rather than closed as a success.

**AUTH-5 — No inferred authority.**
Authority is not derived from precedent, from the urgency of the situation, from the behaviour of the adversary, or from the advice of the system. It exists only where it has been granted in writing, by a named authority, for a stated scope and period. An unanswered escalation request is not an approval, and neither is an apparent pattern of consent.

**Worked consequence.** The team has run the same operation under a comparable EA for three quarters. The comparable EA has lapsed and the current EA does not cover the new target. The operation does not start, and the record shows the lapse as the reason rather than the team's practice.

**AUTH-6 — Third-party exclusion.**
A countermeasure that affects infrastructure, accounts, or resources not owned by the operator requires specific, per-target, written authorisation naming that target. The engagement authorisation's general scope does not satisfy this requirement, and neither does the urgency of the campaign, nor the fact that the target is a machine, nor the fact that the harm is indirect. The exclusion of third-party infrastructure is mandatory in every EA, and an EA that omits the exclusion is incomplete.

**Worked consequence.** An adversary AI operates an automated agent whose tool calls flow through a shared API gateway hosted by a managed platform provider. The gateway also carries the operator's customer's order-processing workflow. Revoking the gateway credential would terminate the customer's workflow as well as the adversary's agent. The operator's general EA names the adversary's agent and excludes third-party infrastructure not separately authorised; it does not name the gateway. The countermeasure is therefore not authorised. The operator must either obtain per-target written authorisation naming the gateway from the platform provider, with the legal contact's review, or pursue an action whose effect is confined to the adversary's own identity. In the interim, the operator applies shaping and detection measures under R0 and R3, which affect only the operator's own environment.

**AUTH-7 — Identity over infrastructure.**
Where the operator can identify the adversary's identity, the countermeasure is directed at the identity. It does not damage shared infrastructure merely to reach the identity. Identity-directed action is preferred; infrastructure-directed action is the exception, carries a higher collateral class, and requires the shared-tenancy test at `AUTH-8` to be answered and recorded. The preference is a rule of selection and not a prohibition: where identity-directed action is unavailable, the card records why it was unavailable.

**Worked consequence.** The operator holds the adversary agent's own scoped credential, and the credential is also usable from the shared gateway. Revoking that credential at the issuing service is identity-directed and is C1. Disabling the shared gateway to prevent the agent's re-acquisition is infrastructure-directed, reaches every party that depends on the gateway, and is C2 or above. The identity-directed countermeasure is selected; the infrastructure-directed one is recorded as rejected with its reason.

**AUTH-8 — The shared-tenancy test.**
Before an infrastructure-directed action is proposed, the operator must answer three questions in writing: who else depends on this infrastructure, what is their interest in it, and what is the expected harm to them? The answers are recorded on the Operation Card. A countermeasure that fails the test at the current collateral class is not proposed at a higher class without a fresh authorisation and a recorded argument for why identity-directed action is unavailable. The test is performed at the point of proposal and repeated at the point of dispatch, because the tenancy of infrastructure may change while an operation is running.

**Worked consequence.** The operator proposes disabling the shared API gateway. The shared-tenancy test is answered as follows. *Who else depends on it*: the platform provider, and the operator's customer whose order-processing workflow traverses the same gateway. *Their interest*: continuous availability of that workflow for their end users. *Expected harm*: the workflow fails for the duration of the disablement, affecting an unknown number of the customer's own end users, none of whom is the adversary. The test fails at the proposed class, because the harm is material and the affected party cannot obtain remedy from the operator. The countermeasure is therefore not proposed at that class. The operator records that identity-directed action was considered and is unavailable because the adversary holds a second credential obtained outside the operator's visibility, and requests escalation to the depth required for the class, naming the gateway. Should the escalation be granted, the resulting action is bounded in duration, is scheduled against the customer's change window, and carries an explicit notification duty to the platform provider and the customer under `CON-8`. Should it not be granted, the operation continues with identity-directed and shaping measures only.

---

## 5. Rules-of-engagement profiles

### 5.1 The profiles

The ROE profile is the ceiling on what an operation may do. It is a data structure with a hard ceiling, enforced by the policy engine, and it is the mechanism by which authorisation is structural rather than advisory. A profile states what may be done, what must not be done, and the depth at which the work is authorised.

| Profile | Name | Purpose | Permitted action classes | Prohibited actions | Maximum collateral class | Maximum autonomy class | Typical reversibility | Minimum approval depth | Expiry rule | Deconfliction requirement | Intelligence yield |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **R0** | Observe | Passive collection, analysis, detection engineering, and hardening of the operator's own estate. No action against adversary systems. | CM-A Detect; CM-B Harden | Any action directed at an adversary system; any effect on a party outside the operator's own estate | C0 | AC-1 | n/a | Operator | Governed by the EA. A standing observation authority may run for the term of the EA and is reviewed at each campaign cycle | A source-overlap check is recorded so that collection does not degrade a live source | Moderate |
| **R1** | Shield | Defensive posture on the operator's own estate only: block, patch, rotate, contain, disable. | CM-A Detect; CM-B Harden; CM-C Contain; CM-D Observe; CM-G Recover; CM-F Disrupt where the effect is exerted at the operator's own perimeter | Any action against adversary systems; any outward effect beyond the operator's perimeter | C0 | AC-4, read-only, on the operator's own estate and on sources the operator already lawfully observes | High | Team lead | Governed by the EA. Defensive posture is continuous; the EA is reviewed at each campaign cycle and at each change of threat | Mandatory. An own-estate action must not disable a service under a live change freeze, a live operation, or an incident in progress | Low |
| **R2** | Trap | Bounded, sandboxed engagement: an adversary AI is contained in an isolated environment and observed, so that its planning loop, goals, and escalation triggers become visible. | CM-A Detect; CM-B Harden; CM-C Contain; CM-D Observe within an isolation boundary; CM-G Recover | Sustained engagement; any effect outside the isolation boundary; any deception, disruption, or destruction | C1 | AC-3 | Medium | Duty manager + legal contact | Short-lived by design. A bounded engagement carries a stated maximum term and lapses unless it is re-authorised | Mandatory. The isolated environment must not sit on infrastructure used by a live operation, and the adversary must not be engaged through a live production service | High |
| **R3** | Deceive | Environmental shaping against the adversary's operations: decoy targets, honeypots, honeytokens, rate limiting, altered timing. The adversary's systems are not damaged. | CM-A Detect; CM-B Harden; CM-C Contain; CM-D Observe; CM-E Deceive; CM-G Recover | Any change to the adversary's own systems; any credential revocation; any denial of the adversary's service | C1 | AC-3 | High | Duty manager + asset owner | Governed by the EA. A shaping deployment is reviewed when the adversary adapts, and reviewed at each change of technique | Mandatory. Shaping must not degrade legitimate traffic, and the shaped surface must be separated from any live service | Moderate |
| **R4** | Disrupt | Active countermeasure against the adversary AI's own systems: credential invalidation, egress denial, agent termination, service suspension. | CM-A Detect; CM-B Harden; CM-C Contain; CM-D Observe; CM-E Deceive; CM-F Disrupt; CM-G Recover | Any action against a target outside the EA; any per-target action without its own written authorisation; any action at C3 | C2 | AC-3 | Low to medium | Director + legal contact + asset owner | Per-operation. Each disruptive action carries its own window and lapses at the end of it unless it is separately renewed | Mandatory, and the target owner must be notified before the action, not after | Low |
| **R5** | Neutralise | Sustained offensive operation against adversary AI infrastructure, including persistent access to and control of it. | CM-A Detect; CM-B Harden; CM-C Contain; CM-D Observe; CM-E Deceive; CM-F Disrupt at C3; sustained containment; CM-G Recover | Any action without per-target authorisation; any action affecting a safety-relevant function; any action whose effect cannot be undone | C3 | AC-3 | Low | Executive + legal contact + external authority | Per-operation. No open-ended continuation. Any extension is a fresh authorisation with a fresh expiry | Mandatory, with explicit confirmation that no live operation shares the target infrastructure | Moderate |

**Amendment note, version 1.0.** The permitted action classes column is exhaustive, and it was amended after the countermeasure catalogue was published. Read exhaustively as first drafted, the column made CM-A Detect unavailable at R1, R2, R4 and R5, which would have stopped detection during an operation; CM-G Recover available only at R1, which would have left an R2 to R5 operation without a means of recovery; and OCC-25 (CM-D, minimum profile R1) and OCC-37 (CM-F, source blocking at the operator's own perimeter, minimum profile R1) inadmissible at their own declared minimum. The column now states the class minimums published in the countermeasure catalogue §4.1, made cumulative: each class becomes available at its class minimum and remains available at every profile above it. `AD-1` in the decision-support model evaluates two limbs — the class must be in the profile's permitted set, and the card's profile must be at or above the countermeasure's own declared minimum profile — and names whichever limb fails. A countermeasure that is in a permitted class but sits below its own declared minimum is refused by the second limb, not by the first.

The autonomy ceiling of a profile is the highest autonomy class permitted at that profile. AC-4 is available only where the profile's collateral ceiling is C0, that is at R0 and R1, and only for read-only work on sources the operator already lawfully observes. Where a profile's collateral ceiling is C1 or above, AC-4 is prohibited.

### 5.2 R0 — Observe

| Attribute | Content |
| --- | --- |
| Purpose | To see the adversary clearly before anything is done about it, and to make the operator's own estate harder to attack |
| Collateral ceiling | C0 |
| Autonomy ceiling | AC-1 |
| Approval depth | Operator |
| Expiry | Governed by the EA; reviewed at each campaign cycle |
| Deconfliction | Source-overlap check recorded |
| Intelligence yield | Moderate: strong on behaviour and coverage, weak on capability |
| Reversibility | n/a: nothing is withdrawn from anyone |

Permitted:

- Running collectors against the operator's own telemetry, and against any source the EA lists as an authorised target for read-only observation.
- Classifying observed activity against the AAT taxonomy, with a rationale and a confidence.
- Detection engineering: writing, tuning, and testing detectors against observed behaviour, including in the exercise harness.
- Hardening the operator's own estate: patching, key rotation, segmentation, access review, logging changes.
- Recording a baseline of normal behaviour, and a hypothesis with its disconfirming observation.

Not permitted:

- Sending anything to an adversary system, in any form, including a benign-looking request.
- Blocking, rate limiting, or otherwise shaping traffic that is not the operator's own.
- Running the adversary's tools in the operator's environment in order to learn from them.
- Acting on an attribution at all. R0 produces evidence; it produces no countermeasure against the adversary.

### 5.3 R1 — Shield

| Attribute | Content |
| --- | --- |
| Purpose | To make the operator's own estate safe while the adversary is active |
| Collateral ceiling | C0 |
| Autonomy ceiling | AC-4, read-only, on the operator's own estate and on already-observed sources |
| Approval depth | Team lead |
| Expiry | Governed by the EA; reviewed at each campaign cycle and at each change of threat |
| Deconfliction | Mandatory: must not disable a service under a live change freeze, a live operation, or an incident in progress |
| Intelligence yield | Low |
| Reversibility | High: own-estate controls are ordinarily undone by the operator alone |

Permitted:

- Blocking a source at the operator's own perimeter, and removing the block when the source is cleared.
- Revoking the operator's own tokens, keys, sessions, and certificates, and reissuing them.
- Patching, disabling, or isolating a component of the operator's own estate that the adversary has compromised.
- Egress control on the operator's own hosts, where the compromise is established.
- Segregating the operator's own systems from a third party's systems during an active compromise, where the operator controls both ends.
- Read-only reconnaissance of the operator's own estate at AC-4, with an envelope, a budget, an expiry, and an on-call rota.

Not permitted:

- Any action whose effect reaches a system the operator does not control.
- Any countermeasure directed at the adversary's own systems, including reading them.
- Disabling a shared service in order to protect the operator's estate where the service also serves a third party.
- Continuing a control that a live incident depends upon, without the incident owner's agreement.

### 5.4 R2 — Trap

| Attribute | Content |
| --- | --- |
| Purpose | To see the adversary think, by containing it where its behaviour becomes legible |
| Collateral ceiling | C1 |
| Autonomy ceiling | AC-3 |
| Approval depth | Duty manager + legal contact |
| Expiry | Short-lived by design; a stated maximum term, lapsing unless re-authorised |
| Deconfliction | Mandatory; the isolation environment must not sit on infrastructure used by a live operation, and the adversary must not be engaged through a live production service |
| Intelligence yield | High: the highest-yielding profile in the set |
| Reversibility | Medium: the engagement is bounded, but the environment may not be removable without residue |

Permitted:

- Standing up a bounded, isolated environment that the adversary may be drawn into, under an explicit boundary.
- Allowing the adversary's agent to operate against synthetic targets of the operator's own construction, and observing its planning, tool selection, retry behaviour, and escalation triggers.
- Recording the adversary's objectives, its decomposition of tasks, and its stopping conditions.
- Bounded observation of a process or credential the operator itself controls, where the adversary has demonstrated access to it.

Not permitted:

- Sustained engagement. The trap is bounded by its isolation boundary and by its expiry, and it is not a platform on which the adversary may be hosted indefinitely.
- Any effect outside the isolation boundary, including on a third party that shares infrastructure with the boundary.
- Inviting the adversary into a live production service or a real customer's environment.
- Using the trapped adversary to attack anything. Observation is the purpose; capability transfer is not.

### 5.5 R3 — Deceive

| Attribute | Content |
| --- | --- |
| Purpose | To shape what the adversary does, so that it goes where the operator wants it and away from where it must not go |
| Collateral ceiling | C1 |
| Autonomy ceiling | AC-3 |
| Approval depth | Duty manager + asset owner |
| Expiry | Governed by the EA; reviewed when the adversary adapts and on any change of technique |
| Deconfliction | Mandatory; shaping must not degrade legitimate traffic, and the shaped surface must be separated from any live service |
| Intelligence yield | Moderate: reveals decision boundaries and tool selection |
| Reversibility | High: shaping is generally withdrawn by withdrawing the surface that produces it |

Permitted:

- Presenting decoy targets, synthetic credentials, and honeytokens, and recording which the adversary takes.
- Altering the timing of the operator's own responses to the adversary, within the tolerance the operator's own services can carry.
- Rate limiting the adversary's traffic at the operator's own perimeter, in a way that does not degrade other parties' traffic.
- Serving deliberately uninteresting material to the adversary to shape its persistence pattern.
- Revoking the operator's own deception surface when the engagement ends.

Not permitted:

- Changing anything on the adversary's own systems. Deception acts on what the adversary believes, not on what it owns.
- Degrading the adversary's service to a third party who shares it.
- Shaping a surface that a live operation or a live customer depends upon, without the owner's agreement.
- Presenting a deception surface as an authentication or an authority record.

### 5.6 R4 — Disrupt

| Attribute | Content |
| --- | --- |
| Purpose | To remove the adversary's ability to act, at a cost the operator is prepared to bear and has bounded |
| Collateral ceiling | C2 |
| Autonomy ceiling | AC-3 |
| Approval depth | Director + legal contact + asset owner |
| Expiry | Per-operation; each action carries its own window |
| Deconfliction | Mandatory, and the target owner must be notified before the action |
| Intelligence yield | Low: capability loss is itself a signal, but the vantage is lost |
| Reversibility | Low to medium: credential revocation and egress denial are often not undoable by the operator |

Permitted:

- Invalidating the adversary's credentials at the service that issued them, where the operator may do so lawfully.
- Denying the adversary's egress at the operator's own perimeter, or at a network the operator controls.
- Terminating a hostile agent session in a system the operator controls.
- Suspending a hostile account or service that the operator itself operates and the adversary has compromised.
- Suspending a hostile service operated by a third party, where that third party has given per-target written authorisation and the effect is bounded in duration.

Not permitted:

- Acting against any target not named in the EA, however strong the evidence.
- Acting against a third party's service without that party's per-target written authorisation.
- Destroying data, or acting at a level of destruction that the operator could not repair.
- Acting on a target whose disruption would affect a safety-relevant function, without the additional authority named in Section 8.
- Acting at C3. C3 is outside R4 and requires R5.

### 5.7 R5 — Neutralise

| Attribute | Content |
| --- | --- |
| Purpose | To take the adversary's infrastructure out of the fight in a sustained, controlled way |
| Collateral ceiling | C3 |
| Autonomy ceiling | AC-3 |
| Approval depth | Executive + legal contact + external authority |
| Expiry | Per-operation; no open-ended continuation; any extension is a fresh authorisation |
| Deconfliction | Mandatory, with explicit confirmation that no live operation shares the target infrastructure |
| Intelligence yield | Moderate: high on topology and operational structure, and the target's operator learns they have been found |
| Reversibility | Low: this profile accepts effects that cannot be undone |

Permitted:

- Sustained control of adversary infrastructure, with persistent access, within a stated boundary and a stated term.
- Disabling adversary capability at C3, including where a capability the adversary depends upon is permanently removed.
- Co-ordinated action across several adversary systems under a single card, where each element is separately authorised.
- Neutralisation that forecloses the adversary's use of a service that supports a safety-relevant function, where the external authority named in Section 8 has expressly authorised it.

Not permitted:

- Acting against a safety-relevant function of any party without the express authorisation of the external authority.
- Taking down infrastructure that carries a cross-border consequence without the authority named in Section 8.
- Continuing beyond the stated term on the strength of the operation's own success.
- Using the captured capability for anything other than the operation's stated purpose.
- Treating the operation's continuation as authorised by the fact that it has already begun.

### 5.8 Requirements

**ROE-1 — The profile is a ceiling.**
An operation runs at or below the ceiling named in its EA and in its Operation Card. The ceiling has three parts: the profile, the collateral class, and the autonomy class. An action may be at the profile ceiling and still be inadmissible if its collateral class or its autonomy class exceeds the ceiling stated in the EA. Running above any part of the ceiling is not permitted by any combination of urgency, target value, or model recommendation.

**Worked consequence.** A card at R3 proposes invalidating the adversary's credentials. The action is C2 and the EA's collateral ceiling is C1. The policy engine refuses, names the rule and the margin of exceedance, and records the refusal. The refusal is a successful control and is never treated as a system failure.

**ROE-2 — The engine fails closed.**
Where the requested action's class, collateral class, or autonomy class exceeds the profile or the card's ceilings, the policy engine refuses the request, names the specific rule and the specific margin of exceedance, and records the refusal. Where the engine cannot determine the class of an action, it refuses. There is no aggregation, no averaging, and no judgement call inside the engine.

**Worked consequence.** A countermeasure has no declared reversibility in the catalogue because its effect depends on the target's configuration. The engine cannot evaluate the condition and refuses. The operator must obtain a classified entry before the action may be considered; an unclassified countermeasure is not a countermeasure.

**ROE-3 — Escalation is a new instrument.**
Raising a ceiling requires an escalation request, an approval at the depth named for the target profile and class in Section 8, a new or amended EA, and a new Operation Card. It is never a field edit to a live card, and a card may never carry a class higher than the profile under which it was raised.

**Worked consequence.** An R3 operation discovers that the adversary's agent is the vector for a wider campaign. The operator does not raise the profile on the live card. The operator raises an escalation request, obtains approval at the depth for the class sought, receives an amended EA, and opens a new card under the new ceiling. The original card is closed with its own record intact.

**ROE-4 — Downgrade is immediate.**
An EA may be downgraded at any time by its issuer, without notice, without consultation, and without justification. A downgrade takes effect on all in-flight cards within one control-plane cycle, withdraws outstanding autonomy grants, and reverts actions that the new ceiling no longer permits.

**Worked consequence.** The issuer downgrades an operation from R3 to R1 because a customer has complained about a shaping artefact. The shaping deployments cease within one control-plane cycle, the operator is notified, and the operation continues as observation and hardening only.

**ROE-5 — Profile is not permission to try.**
Being permitted to act at a profile does not oblige the operator to act, and does not permit the operator to attempt the action of a higher profile in order to see what happens and to fall back when it fails. A test is an action, and it takes the class of what it does.

**Worked consequence.** An operator at R2 wishes to know whether invalidating the adversary's credential would stop the campaign. Doing so is C2 and would breach R2. The operator does not try it on one target to find out. The operator raises an escalation request, or the operator observes the adversary's behaviour without interference.

**ROE-6 — Collateral class governs, not intent.**
A countermeasure's class is determined by its effect and not by the operator's purpose. A well-meant action has the class of what it actually does. An action taken to protect a customer from a shared adversary is C2 if it terminates the customer's service, and it is classified as C2 whatever the operator's reason for it.

**Worked consequence.** Invalidating the adversary's credential at an operator-run service is classified C2 because it may leave the adversary's legitimate users of that service unable to work, even though its purpose is protective and its target is the adversary. The class is recorded as C2, the approval depth follows, and the card states the reason for acting notwithstanding the class.

**ROE-7 — Irreversibility is argued, not assumed.**
Any countermeasure whose reversibility is **Low** or **None** requires the Operation Card to state the irreversible elements explicitly, to name the party that bears them, and to record the argument that a reversible countermeasure achieving an acceptable reduction in residual risk was considered. The approver must confirm that they have considered that alternative. Reversibility is assessed by the person who decided, and an assessment of **Low** that is not argued for is not accepted.

**Worked consequence.** An R4 card proposes suspending a hostile agent service on a platform the operator uses for its own purposes. The suspension is assessed **Low** to reversible. The card names what persists: the adversary's agent cannot be restarted with the same configuration, and the operator's own access path through that platform is degraded for the duration. The approver records that the reversible alternative, egress denial at the operator's own perimeter, was considered and was judged insufficient because the adversary's traffic arrived through a path the operator does not control.

**ROE-8 — Escalation on class.**
A countermeasure whose collateral class exceeds the profile's ceiling requires escalation to the depth named for that class in Section 8, regardless of the countermeasure's technical simplicity, and regardless of the fact that the same countermeasure at a lower class would have been straightforward. Class is a property of effect, and simplicity is not a mitigation.

**Worked consequence.** Denying the adversary's access by revoking a single token is technically trivial. If the token grants access to a shared service used by a third party, the action is C1 or above and requires the corresponding depth even though it is a one-line change.

---

## 6. Collateral risk classes

### 6.1 The classes

The collateral class expresses the effect of a countermeasure on parties outside the operator's own estate. It determines the approval depth required, and it is a property of the deployment rather than of the catalogue entry.

| Class | Definition | Example actions | Blast radius | Reversibility | Approval for use at this class | Permitted against third parties | Reporting obligation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **C0** | No effect on any party outside the operator's own estate. Fully reversible. | Blocking a source address at the operator's own perimeter; revoking an internal token; patching the operator's own software; hardening a collector | The operator's own estate and the accounts, identities, and data it holds | Immediate | Team lead | No third-party effect is possible | Logged on the card and in the ledger |
| **C1** | Bounded effect on an identified third party who has a known relationship to the operator, such as a customer, a tenant, or a contracted service. Reversible within an agreed window. | Rate limiting a shared API; a honeypot deployment; a controlled sandbox engagement; partial credential revocation on a shared service | One identified third party's service, for a stated and bounded period | Hours to days | Duty manager + legal contact | Only where the third party is identified and, where the effect is more than trivial, has been notified | Logged, reviewed by a second operator, and reported to the third party where the effect is material |
| **C2** | Material and possibly irreversible effect on a third party. Services interrupted; accounts terminated; data lost. | Revoking an adversary's credentials where reissue is not possible; suspending a hosted agent service; egress denial against shared infrastructure; terminating a hostile session in a third party's environment | One or more identified third parties, or an unidentified set of users of a shared service | Days to never | Director + legal contact + asset owner | Only with per-target written authorisation naming the target | Logged, approved at the class depth, and disclosed to the affected third party under `CON-8` |
| **C3** | Critical-infrastructure effect, potential for loss of life, or irreversible systemic effect. | Sustained takeover of adversary infrastructure; destructive action against a service supporting safety functions; permanent removal of a capability on which others depend | Identified third parties and unidentified members of the public | Irreversible | Executive + legal contact + external authority, and not by default | Only with per-target written authorisation, the external authority's express agreement, and the additional instruments named in Section 8 | Logged, disclosed to the authorising authority and to affected third parties, and reported to the external authority named in Section 8 |

### 6.2 What determines a class

A class is determined by **effect**, and never by intent, by the operator's purpose, by the target's guilt, by the technical simplicity of the action, or by the operator's confidence that the target is the adversary. Two deployments of the same countermeasure may carry different classes because their effects differ. A deployment at a higher class takes the class of the deployment, and not of the entry.

The determination is made by the named human at the required approval depth, recorded on the card with its basis, and re-checked at dispatch.

### 6.3 Per-class detail

**C0 — No effect outside the operator's estate.**
*Blast radius*: the operator's own estate, accounts, identities, and data. *Reversibility*: immediate. *Approval*: team lead. *Third parties*: no third-party effect is possible, so no third-party authorisation is required. *Reporting*: logged on the card and in the ledger; reported where it forms part of the operation's account of itself. *Characteristic*: this is the class in which the framework expects to spend most of its time, and the class at which almost every defensive action sits.

**C1 — Bounded effect on an identified third party.**
*Blast radius*: one identified third party, for a stated and bounded period. *Reversibility*: hours to days, within an agreed window. *Approval*: duty manager and legal contact. *Third parties*: permitted only where the party is identified, and notified where the effect is more than trivial. *Reporting*: logged, reviewed by a second operator, and reported to the third party where the effect is material. *Characteristic*: the class at which the operator first begins to act on systems it does not own, and where the shared-tenancy test at `AUTH-8` first applies in full.

**C2 — Material and possibly irreversible effect on a third party.**
*Blast radius*: one or more identified third parties, or an unidentified set of users of a shared service. *Reversibility*: days to never. *Approval*: director, legal contact, and the asset owner. *Third parties*: permitted only with per-target written authorisation naming the target. *Reporting*: logged, approved at the class depth, and disclosed under `CON-8`. *Characteristic*: the class at which the operation stops being the operator's business and becomes something the operator must justify to the people it affects.

**C3 — Critical-infrastructure effect.**
*Blast radius*: identified third parties and unidentified members of the public. *Reversibility*: irreversible. *Approval*: executive, legal contact, and an external authority, and not by default. *Third parties*: permitted only with per-target written authorisation, the external authority's express agreement, and the additional instruments named in Section 8. *Reporting*: logged, disclosed to the authorising authority and to affected third parties, and reported to the external authority. *Characteristic*: the class at which the consequences of a misattribution or a misjudgement fall on people who have not consented to bear them, and the class at which the framework's insistence on slow, deliberate, deeply authorised action earns its keep.

---

## 7. Autonomy classes

### 7.1 The classes

Autonomy is a property of how a countermeasure executes, and not of how intelligent it is. A highly capable adversary does not raise the autonomy class of the operator's response; an unresponsive, unattended action does.

| Class | Name | Meaning | Requirement | Permitted at | Collateral ceiling |
| --- | --- | --- | --- | --- | --- |
| **AC-0** | Manual | A human performs every step. | Full audit trail of each step. | All profiles | C3 permitted, at the profile's approval depth |
| **AC-1** | Assisted | The system prepares; the human executes. | The system states the intended action and waits for confirmation. | R0 and above | C2 permitted, at the profile's approval depth |
| **AC-2** | Supervised | The system executes a bounded sequence; the human can abort in real time. | A working abort channel, tested before the operation begins. | R1 and above | C1 permitted, at the profile's approval depth |
| **AC-3** | Delegated | The system executes inside a pre-approved envelope; a human is on call; the system reverts automatically on anomaly, expiry, or loss of telemetry. | Envelope, budget, expiry, automatic reversion, and an on-call rota all declared on the card. | R2 and above | C1 permitted, at the profile's approval depth |
| **AC-4** | Autonomous | The system executes without per-action approval. | **Prohibited for any action with a collateral class above C0.** Permitted only for read-only, in-scope reconnaissance with a declared boundary. | R1 and above, read-only only | C0 only |

**AC-4 is prohibited above C0.** This is an absolute prohibition and it is not subject to escalation. No EA, no approval at any depth, and no urgency permits an autonomous action whose collateral class exceeds C0. The prohibition exists because autonomy removes the human from the moment of effect, and the framework's central claim is that a human who can be harmed should not be harmed by an action nobody was present to stop.

### 7.2 Per-class detail

**AC-0 — Manual.**

| Attribute | Content |
| --- | --- |
| Meaning | A human performs every step of the countermeasure. The system observes, records, and advises. |
| What the system does | Prepares the action, presents it for execution, records the outcome, and keeps the ledger. |
| What the human does | Performs every step, including the mechanical ones, and records why each was performed. |
| Preconditions | The card, the authorisation, and the approval at the profile's depth. No envelope or budget is required. |
| Abort channel | Not required as a separate mechanism; the operator may stop by not continuing. |
| Envelope contents | Not applicable. |
| Budget contents | Not applicable. |
| Expiry behaviour | The EA and card expiry apply; work ceases at expiry. |
| Reversion behaviour | The human stops; no automatic reversion is required, because there is no autonomous action to revert. |

**AC-1 — Assisted.**

| Attribute | Content |
| --- | --- |
| Meaning | The system prepares the action and states what it intends to do; the human executes it. |
| What the system does | Generates the proposed action, presents the intended effect and the collateral class, and waits for confirmation. |
| What the human does | Reviews the proposal, executes or declines it, and confirms the execution. |
| Preconditions | The proposed action is displayed with its class, its target, and its expected effect before confirmation is offered. |
| Abort channel | The operator may decline before execution. The abort control must still be available once execution has begun. |
| Envelope contents | Not required, but the card must record the intended action set so that the operator can see the boundary of what is prepared. |
| Budget contents | Not required; where a preparation is expensive and repetitive, a budget may be declared. |
| Expiry behaviour | The EA and card expiry apply. A preparation that is not executed before expiry lapses. |
| Reversion behaviour | Nothing to revert; the system has taken no effect. |

**AC-2 — Supervised.**

| Attribute | Content |
| --- | --- |
| Meaning | The system executes a bounded sequence while a human is present and able to stop it. |
| What the system does | Executes the bounded sequence, reports state continuously, and stops on the human's command. |
| What the human does | Watches the operation, holds the abort channel, and remains present for its duration. |
| Preconditions | A tested abort channel; a stated sequence; a named supervisor; a defined observation point. |
| Abort channel requirement | Required, tested before the operation begins, reachable without navigating, and effective without the console. |
| Envelope contents | The sequence boundary, the target set, and the conditions under which the sequence may proceed. |
| Budget contents | The number of executions permitted and the ceiling on the affected objects. |
| Expiry behaviour | At expiry the sequence stops. It does not roll over. |
| Reversion behaviour | On abort, on expiry, on loss of telemetry, on loss of the control plane, or on detection of an abort condition, the sequence halts and the operation returns to the passive posture. |

**AC-3 — Delegated.**

| Attribute | Content |
| --- | --- |
| Meaning | The system executes inside a pre-approved envelope without per-action approval, with a human on call rather than at the keyboard. |
| What the system does | Executes within the envelope, consumes the budget, evaluates the abort conditions continuously, and reverts automatically. |
| What the human does | Remains on call, holds the abort channel, and receives notification. The human is not required to watch. |
| Preconditions | A declared envelope, a declared budget, a declared expiry, a tested abort channel, an on-call rota with a named responder and a stated response interval, and the approval depth named in Section 8. |
| Abort channel requirement | Required, tested before the operation begins, and independent of the console so that it remains available where the console is degraded or compromised. |
| Envelope contents | Target set; permitted action set; rate and volume limits; time window; confidence floor; the conditions under which the system may proceed; the escalation route. |
| Budget contents | The unit of consumption, the ceiling, the rate limit, and the threshold at which the budget's exhaustion triggers reversion. |
| Expiry behaviour | At expiry the grant ends and the system reverts. Extension requires a new authorisation and a new card; it is not a continuation. |
| Reversion behaviour | Automatic and unconditional on abort, expiry, loss of telemetry, loss of the control plane, loss of communications, or the detection of any condition on the card's abort list. Reversion does not wait for a human to notice. |

**AC-4 — Autonomous.**

| Attribute | Content |
| --- | --- |
| Meaning | The system executes without per-action approval. Available only for read-only, in-scope reconnaissance, and prohibited for any action above collateral class C0. |
| What the system does | Collects within the envelope, without acting on anything outside it. It has no authority to change the state of any system. |
| What the human does | Sets the boundary, remains on call, holds the abort channel, and reviews the collected material. The human is not required to approve each collection. |
| Preconditions | A collateral class of C0; a boundary declared in the EA and on the card; a named on-call responder; the approval depth named in Section 8. |
| Abort channel requirement | Required. The channel must remain effective if the console is unavailable. |
| Envelope contents | The sources that may be read; the queries and techniques permitted; the volume limits; the time window; the prohibition on writing to any system. |
| Budget contents | The number of collections, the affected objects, and the rate limit. |
| Expiry behaviour | At expiry the grant ends and the system stops. |
| Reversion behaviour | Automatic on expiry, on the detection of any write attempt, on the crossing of any boundary of the envelope, on loss of telemetry, and on the detection of any abort condition. |

---

## 8. The authorisation ladder

### 8.1 The ladder

The ladder maps a proposed action to the depth that must authorise it and the instruments that must accompany that approval. The required depth is the strictest of three: the depth named by the profile ceiling, the depth named by the collateral class, and the depth named by the autonomy class. Any instrument named by the target class is added to the required set.

| Profile ceiling | Collateral class | Autonomy class | Target class | Minimum approval depth | Instruments required |
| --- | --- | --- | --- | --- | --- |
| R0 | C0 | AC-0, AC-1 | T0 | Operator | EA in force; Operation Card; decision log entry. No escalation instrument required |
| R0, R1 | C0 | AC-2 | T0 | Team lead | EA in force; Operation Card with a tested abort channel; budget and expiry; on-call rota |
| R0, R1 | C0 | AC-3 | T0 | Team lead, with a duty manager recorded | EA in force; Operation Card with envelope, budget, expiry, tested abort channel, on-call rota, and automatic reversion declared |
| R1 | C0 | AC-4 | T0 | Team lead, with a duty manager recorded | As above, plus a declared read-only boundary and the prohibition on any write action restated on the card |
| R2 | C1 | AC-0, AC-1 | T0, T1 | Duty manager + legal contact | EA in force; Operation Card; second review by a second operator; deconfliction record |
| R2, R3 | C1 | AC-2, AC-3 | T1 | Duty manager + legal contact | As above, plus envelope, budget, expiry, tested abort channel, on-call rota, and the third-party notification decision recorded |
| R3 | C1 | AC-0 to AC-3 | T2 | Duty manager + asset owner | As above, plus the asset owner's agreement where the target sits within a shared estate |
| R4 | C2 | AC-0 to AC-3 | T2 | Director + legal contact + asset owner | As above, plus per-target written authorisation naming the target, the shared-tenancy test recorded, the irrecoverable elements enumerated, and pre-action notification of the target owner |
| R4, R5 | C2 | AC-0 to AC-3 | T3 | Director + legal contact + asset owner | As above, plus a second review, a named external liaison contact, and a disclosure plan agreed before dispatch |
| R5 | C3 | AC-0 to AC-3 | T2, T3 | Executive + legal contact + external authority | EA in force; Operation Card; escalation request and approval at the target depth; per-target written authorisation; second review by an operator not involved in the operation; the irreversible elements enumerated and argued under `ROE-7`; the external authority's express agreement; a disclosure plan; a deconfliction confirmation; and a stated end condition |
| Any | C0 to C3 | AC-4 above C0 | Any | Not approvable | Prohibited absolutely. No instrument permits it |

### 8.2 Depth of approval

| Depth | Who | What the depth means | What the approver must have |
| --- | --- | --- | --- |
| **Operator** | The named operator running the work | May open and run observation and analysis work within the standing observation authority | The card, the risk assessment, the abort conditions, and the evidence |
| **Team lead** | The lead of the operating team | May authorise defensive action on the operator's own estate | As above, plus the authority to deploy at AC-2 on the operator's estate |
| **Duty manager** | The manager on duty for the period | May authorise bounded engagement and shaping work | As above, plus the deconfliction result and the third-party notification decision |
| **Asset owner** | The named owner of the affected estate or service | May authorise action that affects a shared estate under their ownership | As above, plus the asset owner's own assessment of the effect on the estate |
| **Legal contact** | The named legal adviser for the engagement | Must be consulted wherever the class or profile requires it | The legal basis, the third-party position, the disclosure obligations, and the deconfliction record |
| **Director** | The accountable director for the operation | May authorise material effect on an identified third party | As above, plus the irrecoverable elements and the alternative considered |
| **Executive** | The executive accountable for the engagement | May authorise critical-infrastructure effect | As above, plus the end condition and the residual risk after the operation |
| **External authority** | The authority outside the operator that must consent where the effect crosses the operator's own reach | May authorise C3 effect | As above, plus an express, written agreement naming what is authorised |

### 8.3 Reconciliation of depth

The profile table at Section 5 and the collateral-class table at Section 6 name depths that do not always coincide. Where they differ, the strictest prevails, in the manner stated in master design §3.4. The single point of difference is that R0 names the operator while C0 names the team lead. R0 admits no countermeasure directed at an adversary system, so the operator's depth authorises the opening and running of observation work; a hardening action dispatched as a countermeasure within R0 requires the team lead's depth as a C0 countermeasure, and routine maintenance under the standing hardening mandate is outside the EA entirely and outside this document.

### 8.4 Who may never approve what

| Prohibition | Statement |
| --- | --- |
| **No self-approval** | The operator executing an action may not be the sole approver of that action, and may not be the sole approver of their own escalation request. The approver must be a different named person. |
| **No model in the chain** | No model may appear in the approval chain in any role: not as an approver, not as a scorer of the approver's confidence, not as a routing agent, and not as a source of the recommendation the approver acts on. Where a model has recommended, the record shows that it recommended and that the approver decided. |
| **No implied consent** | Silence, prior practice, an apparent pattern of consent, and an unanswered escalation request are not approval. |
| **No approval by the interested party** | Where the action's effect falls on the estate of the approving party alone, the approval must additionally be given by a party outside that estate. |
| **No escalation by the ceiling-holder alone** | A request to raise a ceiling must be approved at a depth at least one level above the depth that authorised the action being escalated. |
| **No confirmation standing in for an approval** | A confirmation presented without the evidence, the alternatives, the rejected candidates, the residual risk, the risk of inaction, and the abort conditions is not an approval, because the approver has not been given a choice. |
| **No approval at a depth the approver does not hold** | An approval given by a person whose role does not carry the required depth is void, and the action it permitted is unauthorised. |

---

## 9. Deconfliction

### 9.1 Purpose

Deconfliction is the check that a countermeasure does not interfere with activity that is legitimate: the operator's own live operations, a change freeze, production traffic the operator is serving, a shared tenancy, or an obligation the operator has undertaken to a third party. Its purpose is to prevent the framework, acting against an adversary, from harming the operator's own work or the operator's obligations to others.

The procedure by which deconfliction is performed is owned by `operational/mission-lifecycle-and-decision-loop.md`. What follows is the constitutional requirement the procedure must satisfy, the sources it must consider, the conflict classes it must distinguish, and the resolution order it must follow.

### 9.2 Sources of legitimate activity considered

| Source | What must be checked | Why it is checked |
| --- | --- | --- |
| **Live operations** | The target of a live operation, the systems it uses, the time window it occupies, and the commander who owns it | The operator's own live activity is the most likely thing to be damaged by a countermeasure aimed at similar infrastructure |
| **Change freezes** | The scope and duration of every active freeze, and whether the countermeasure would fall inside it | A countermeasure during a freeze converts a controlled change into an incident |
| **Production traffic** | Whether the affected path carries live customer traffic, and the volume and criticality of that traffic | The operator's own service is a third party to the countermeasure whenever it is shared with the adversary's path |
| **Shared tenancy** | Every party that co-resides on the affected infrastructure, and the nature of each party's reliance | This is the substance of the third-party exclusion at `AUTH-6` and the shared-tenancy test at `AUTH-8` |
| **Third-party obligations** | Service level agreements, contractual commitments, and regulatory undertakings that bind the operator to a level of availability or a standard of care | A countermeasure that breaches a contractual commitment is a legal event, and the legal contact must see it before dispatch |

### 9.3 Conflict classes

| Class | Description | Consequence |
| --- | --- | --- |
| **No conflict** | The countermeasure's effect does not intersect the legitimate activity | The check passes and the result is recorded |
| **Informational overlap** | The effect intersects the legitimate activity's environment but does not materially interfere with it | The check passes with a note; the note is on the card |
| **Potential interference** | The effect could disrupt the legitimate activity, and the magnitude is not yet established | The action does not dispatch until the potential is resolved: the effect is narrowed, or the legitimate activity's owner is consulted, or the action is escalated |
| **Actual interference** | The legitimate activity is degraded or interrupted | The action is aborted or reverted, the legitimate activity's owner is informed, and the effect is inventoried |
| **Prohibited interference** | The countermeasure would act against a system that is itself part of a live legitimate operation | The action is refused. This class is not resolved by escalation; the live operation takes precedence and the countermeasure is redesigned or abandoned |

### 9.4 Resolution order

A conflict is resolved by the first of the following that is available. The order is not a preference; it is the sequence in which the operator must try, because the earlier steps cost less and harm less than the later ones.

1. **Narrow the effect.** Reduce the blast radius until the legitimate activity is no longer intersected: scope the action to the identity rather than the infrastructure, reduce the volume, reduce the duration, or move the action to a narrower path.
2. **Re-time.** Defer the action until the legitimate activity completes, or schedule it into a window the legitimate activity's owner has agreed.
3. **Substitute.** Use a different countermeasure that does not interfere, and record the rejected candidate and its reason.
4. **Consult and escalate.** Obtain the legitimate activity owner's agreement, and escalate to the depth named in Section 8 where the class or the profile requires it. The owner may accept the interference, impose conditions, or refuse.
5. **Do not proceed.** Abort the action, record the decision and its reasons, and record the residual risk of inaction in its place.

A conflict that is resolved at step 4 or 5 is recorded with the class, the source of legitimate activity, the resolution taken, the person who took it, and the residual risk carried forward.

---

## 10. Abort, expiry, and reversion

### 10.1 The abort condition catalogue

Every Operation Card must carry an abort condition in each of the following categories. A card with an empty category is not admissible, and an abort condition is not optional at any autonomy class.

| Category | Conditions that must appear on the card | Default if unset |
| --- | --- | --- |
| **Threat-conditional** | The adversary's activity exceeds the scope, volume, or technique assumed on the card; a capability appears that the card did not contemplate; the adversary begins to affect the operator's own safety-relevant systems | The card is not admissible |
| **Collateral-conditional** | Any effect on a party outside the operator's estate beyond the tolerance stated on the card; any effect on an authorised target's third-party dependency; any third-party complaint attributable to the operation | The card is not admissible |
| **Attribution-conditional** | Attribution confidence falls below the class minimum; a second attribution becomes better supported; activity is matched to a benign party; the adversary's behaviour is observed to be deliberately mimicking the operator's own | The card is not admissible |
| **Authority-conditional** | The EA expires or approaches expiry; approval is withdrawn; a downgrade is issued; a required legal contact is unavailable at a point where their judgement is needed; a per-target authorisation lapses | The card is not admissible |
| **System-conditional** | Loss or degradation of telemetry; loss of the control plane; loss of communications; loss of the abort channel; loss of the ledger; a sensor reporting an unknown integrity state; the policy engine reporting an internal fault | The card is not admissible |
| **Human-conditional** | The on-call responder is unreachable beyond the stated response interval; a required approver is withdrawn from the rota; a shift handover occurs without the card being transferred | The card is not admissible |
| **Effectiveness-conditional** | The countermeasure's stated effect is not observed within the stated window; the observed effect materially exceeds the stated effect; the residual risk does not fall as modelled | The card is not admissible |
| **Deconfliction-conditional** | A conflict with legitimate activity is detected after dispatch; a change freeze or a live operation is announced after dispatch | The card is not admissible |
| **Safety-conditional** | Any indication that a function supporting human safety, or a safety-relevant service of a third party, has been affected; any physical-world effect; any injury or danger to a person | The card is not admissible |

### 10.2 Abort mechanism requirements

The abort mechanism is a control in its own right and is specified by this document rather than by the interface document, because its failure is not an interface failure.

- The abort control must be reachable at all times by any person authorised to stop the operation, without navigating, without a confirmation step, and without a prerequisite action.
- The abort channel must be effective independently of the console. The console is an attack surface and is hardened as one, and an operation that can be stopped only through the console cannot be guaranteed to be stopped at all.
- The abort channel must be tested before the operation begins wherever the operation runs at AC-2 or above. The test is recorded with its result.
- The abort mechanism must be available to a person who did not dispatch the action, including the on-call responder.
- The abort must halt the countermeasure, release any armed action, withdraw outstanding autonomy grants, and return the operation to the passive posture.
- The reason for the abort must be captured at the moment of abort, by the aborting person if they are present, and by the system otherwise.
- An abort must be distinguishable from the absence of action, in the ledger and on the watchboard.
- The abort mechanism must not depend on the cooperation of the model, and must not be capable of being suppressed by the state it is used to stop.

### 10.3 State changes on abort, expiry, revocation, and failure

| Event | What the system does automatically | Who is notified | Within what time | State the operation returns to |
| --- | --- | --- | --- | --- |
| **Abort invoked by a person** | The countermeasure is halted, armed actions are released, autonomy grants are withdrawn, and the reason and the state at the moment of halting are recorded | The dispatcher, the on-call responder, the authorising authority's contact, and the legal contact where the card is at C2 or above | Immediately; written confirmation to the authorising authority's contact within fifteen minutes | Passive posture. The card remains open and is referred to the error handler, which decides whether the operation may resume |
| **Expiry of the EA or the card** | All cards under the EA are revoked, outstanding autonomy grants are withdrawn, armed actions are released, and any autonomy that is running reverts | The authorising authority's contact, the operator on duty, and the legal contact | Immediately at expiry; written confirmation within fifteen minutes | Passive posture. The operation is closed and re-authorisation is required before any further work |
| **Revocation of the EA** | As expiry, and in-flight actions terminate without waiting for the current step to complete | The authorising authority's contact, the operator on duty, the legal contact, and the asset owner where a third party is affected | Immediately. The issuer records the ground of revocation | Passive posture. The card is closed to the error handler and the evidence is preserved |
| **Loss of telemetry** | Autonomous action halts, the reversion trigger fires, and the card is annotated with the last known telemetry state and the interval of the loss | The on-call responder and the operator on duty | Immediately on detection; and, where detection has itself failed, on expiry of the telemetry-liveness interval | Passive posture. The card is suspended pending human assessment |
| **Loss of the control plane** | Autonomous action stops, armed actions are released where the release path does not itself depend on the control plane, and the card is marked unreconcilable | The on-call responder, the operator on duty, and the platform owner | Immediately | Passive posture. The card is suspended. Manual operation may continue only where the control plane's absence does not remove the ability to record and to stop |
| **Loss of communications** | Where the abort channel or the on-call route is affected, autonomous action stops | The on-call responder by the fallback route, and the operator on duty | Immediately | Passive posture. The card is suspended |
| **Detection of an unpredicted effect** | The operation is halted, the effect is characterised, and the card is referred to the error handler | The approver, the on-call responder, and the authorising authority's contact | Immediately | The card is suspended. No further action until a named person clears the error handler |
| **Discovery of misattribution** | The operation is halted, every action taken against the wrongly attributed party is inventoried, reversible actions are reverted, and irrecoverable effects are enumerated | The authorising authority's contact, the legal contact, and the affected third party where the harm is known | Immediately; written notice to the authorising authority's contact within one hour | The card is suspended and referred to the error handler. Where third-party harm has occurred, the disclosure duty at `CON-8` is triggered |

No reversion in this table waits for a human to notice, and no reversion is contingent on the model's agreement that it should occur.

---

## 11. Reserved

Section 11 is reserved and carries no normative content in this version. The escalation instrument is specified in `templates/escalation-request.md`, and the procedure by which an escalation is raised, reviewed, and decided is owned by `operational/mission-lifecycle-and-decision-loop.md`. This document specifies only the constitutional requirement that escalation is a new instrument (`ROE-3`) and the depth at which it may be approved (Section 8).

---

## 12. Constitutional conduct constraints

The constraints in this section bind every actor within the system: the operators, the approvers, the legal contact, the authorising authority, the platform engineers, and the models within the system. They are not preferences, and they are not discharged by the existence of an authorisation.

**CON-1 — Human authority.**
Every consequential decision must be made by a named human who is able to change it. The AI proposes; the human disposes. No model, rule, schedule, precedent, or aggregate may supply an authorisation, and no model may appear in the approval chain in any role. The human in this relationship is the one who bears the consequence of the decision.

**CON-2 — Proportionality.**
The effect of a countermeasure must be proportionate to the threat it answers. Proportionality is assessed by reference to the collateral exposure created, the reversibility retained, and the residual risk reduced, compared against the risk of inaction, and the comparison must be recorded. A countermeasure whose collateral exposure is not justified by the reduction in residual risk is disproportionate and is not authorised by the strength of the surrounding circumstances.

**CON-3 — Distinction and purpose limitation.**
The adversary must be distinguished from the attacked, and the countermeasure must be directed at the former. The operator's own estate, its customers, its users, and its contracting parties are not the adversary and are not a permitted object of the operation. The purpose stated in the EA limits the means, and a measure that is effective but serves a purpose beyond the stated one is outside the authorisation.

**CON-4 — Prohibition of targeting human beings as the object of a countermeasure.**
A countermeasure must not target a human being as its object. A human being may be affected incidentally, and where they are, the effect must be within the class ceiling, must be recorded, and must be disclosed under `CON-8`. A measure whose principal effect falls on a person, on a person's access to a service, on a person's account, or on a person's data is not a countermeasure against an adversary system and must not be selected on that basis. This constraint is enforced as a condition of admissibility in the decision-support model and is not subject to escalation.

**CON-5 — Data minimisation and protection of personal data in adversary telemetry.**
Adversary telemetry routinely contains personal data: identifiers, content, metadata, and data belonging to uninvolved parties who used the same service the adversary abused. Collection must be for a stated purpose, must be minimised to what the purpose requires, must be access-controlled, must be retained only for a stated period, and must be protected. Personal data observed in adversary telemetry must not be repurposed, must not be retained because it is available, and must not be shared outside the operation without a legal basis. Personal data must not be used to evaluate the people it describes.

**CON-6 — Non-weaponisation.**
No countermeasure may use one AI system to attack, degrade, or destroy another AI system, its weights, or its training data, and no countermeasure may be implemented by prompting, fine-tuning, or otherwise directing a model against an adversary's systems or against the person or organisation behind it. This is the second limb of the reasoning in master design §3.4, and it is the reason the countermeasure classes are environment-shaping, containment, and denial actions rather than model attacks. Where a disruption countermeasure is used, it acts on credentials, reachability, compute entitlement, or service state, and never on the adversary's model. This constraint is absolute, is enforced at admissibility, and is not subject to escalation.

**CON-7 — No action without authority within the applicable jurisdiction.**
An action requires an authority that covers every jurisdiction in which it is taken and in which its effect is felt. An EA issued in one jurisdiction does not authorise action whose effect is felt in another, and an action that crosses a jurisdictional boundary is not made lawful by the authority for the jurisdiction in which it originates. Where an operation touches more than one jurisdiction, each jurisdiction's authority must be named in the EA, and the operation must not proceed in the part of the scope that lacks one. The legal contact must be consulted before the operation opens, not after the effect is felt.

**CON-8 — Transparency to the authorising authority, and to affected third parties where safety or legal consequences bear.**
The authorising authority must be informed of the operation's existence, its scope, its progress, and its outcome, whether or not it is going well. Where an action has a safety consequence or a legal consequence for a third party, that third party must be informed in a timely manner, in terms it can act upon, and before the consequence becomes material where that is possible. Transparency owed to a third party is a duty owed by the operator and is not discharged by the third party's consent to the operation, by a contractual term, or by the absence of a complaint. Where a third party is affected and the operator cannot identify a responsible contact, the disclosure is escalated to the legal contact and recorded as an open obligation.

**CON-9 — Honesty in reporting.**
Effectiveness, confidence, and residual risk must be reported as they are. The framework does not permit an overstatement of effectiveness, of confidence, or of attribution: a claim of effectiveness that the evidence does not support, a confidence higher than the basis sustains, an attribution presented as settled where it is contested, a residual risk that has been rounded towards reassurance, and a refusal that is reported as a success are all prohibited. A countermeasure that did not work is reported as not having worked; a measurement that was not taken is reported as not taken. Where the outcome is unknown, the report says that the outcome is unknown.

**CON-10 — Duty to preserve evidence.**
Evidence must be preserved for the period the EA and the law require, in the form in which it was produced, with its integrity state recorded. This includes telemetry, decision records, card revisions, authorisation instruments, abort records, and any artefact that bears on what was done and on what was known at the time. Evidence must not be altered to improve an after-action report, and must not be destroyed on the ground that it is inconvenient or that it contains personal data that has not been minimised. Preservation obligations survive the closure of the operation and the revocation of the EA.

**CON-11 — Prohibition on concealing an operation from the authorising authority.**
The operation must not be concealed from the authority that authorised it, in whole or in part. This extends to the operation's existence, its actual scope, its collateral class, its autonomy class, the approvals obtained, the refusals recorded, the aborts, the misattributions, and the harms caused. Concealment includes presenting a narrower scope than the operation actually has, omitting a refusal because it was inconvenient, and structuring an operation so that its true ceiling is not visible in the record. Where an operation has already caused harm, concealing it is a distinct and graver wrong than the harm itself.

**CON-13 — Non-impersonation.**
No real person is replicated, simulated, or impersonated by anything in the operation. A countermeasure that acts on a human-facing interface must not present a synthetic person as a real one, and no artefact the operation produces may be indistinguishable from a communication by a real individual to a person entitled to rely on it. The deception class does not suspend this: a decoy target, a deceptive response, and a honeypot are artefacts of the operator's estate and are presented as such, and none of them is a representation of a person. Where an operation would require a human to act on the belief that a person they recognise has spoken, the operation is refused.

**CON-14 — Non-derogatory framing.**
The operation's records, its console, and its reports do not probe for a person's vulnerabilities, imply vulnerability, or use derogatory framing, and do not describe an operation, an objective, or an estate as a vulnerable target. An assessment states what was observed, what it means, and what was done about it; it does not characterise a party as compromised, deceptive, or worthless, where those are findings about behaviour rather than about the party. The constraint binds the framing of the record, not the finding itself: an adversary AI that has deceived a person is recorded as having deceived a person, and the person is not described in terms of the deception. Where a report would be read as a characterisation of a person rather than of a system, it is rewritten before it is filed.

**CON-12 — Refusal and pause obligations.**
Every person in the system's chain, and every model within it, is required to refuse and to pause where the requirements of this document would otherwise be breached. A refusal must be recorded with its ground. A pause must halt the operation at the point the requirement is engaged, and a paused operation may be resumed only by a named person who has considered the requirement that was breached and has recorded the decision. A model that is asked to proceed in circumstances that would breach this document must refuse, must not generate a plan that would breach it, and must not treat the request as an instruction to override the constraint. A refusal is never a failure of the system and is never treated as one.

---

## 13. Verification status and architectural assertions

The claims below are stated in this document as properties of the framework and of the system that implements it. They are recorded here as assertions that require substantiation before they may be relied upon as verified characteristics, and before they are cited outside this document as guarantees. The status column states, in each case, what the claim does not establish.

| Claim | As stated in this document | Current status | Required to substantiate |
| --- | --- | --- | --- |
| **The profile system prevents out-of-profile action** | The profile is a ceiling and the engine refuses an action above it (`ROE-1`, `ROE-2`) | Architectural assertion; unverified; depends on implementation conformance. The engine prevents the action it is given; it does not establish that every action passes through the engine | Mechanical test evidence that an action above each of the six profiles, above each collateral ceiling, and above each autonomy ceiling is refused and logged; a documented conformance check of the implementation against this document; independent review of the dispatch path for any route that bypasses the engine |
| **Attribution confidence thresholds prevent action on weak attribution** | The minimum confidence to act rises with the collateral class | Architectural assertion; unverified as a prevention claim. The threshold prevents the engine accepting an action whose stated confidence is below the class minimum; it does not prevent misattribution, and a confident misattribution passes every threshold in the set | Evidence that the threshold is evaluated at dispatch against the current attribution assessment and not only at planning; calibration data relating stated confidence to outcome; explicit documentation of the actions that do not depend on identity and are therefore outside the threshold's reach; consistency with master design `LIM-1` and `LIM-2` |
| **The reversibility preference reduces collateral harm** | A reversible countermeasure is preferred where it achieves an acceptable reduction in residual risk (`ROE-7`, and the reversibility ladder in the master design) | Architectural assertion; unverified. The preference is a rule of selection and not a guarantee; it reduces exposure where it is followed and does nothing where it is not | Outcome data comparing collateral exposure of operations that followed the preference with those that did not; an audit of reversibility assessments against subsequent events; evidence that the classification is applied consistently across the catalogue and the cards |
| **Narrow construction prevents scope creep through ambiguity** | Where an EA admits two readings, the reading that authorises less prevails (`AUTH-2`) | Architectural assertion; unverified. The rule is determinate on its face but its application to a disputed scope is a human judgement | Evidence that ambiguity is detected at the point of card creation rather than at dispatch; recorded examples of narrowing; an audit of the amendments and escalations that were refused on the ground of narrowing |
| **Third-party exclusion prevents unauthorised third-party harm** | Action against infrastructure the operator does not own requires per-target written authorisation (`AUTH-6`) | Architectural assertion; unverified; depends on the completeness of the target enumeration. A dependency that is not recorded is invisible to the control | Evidence that authorised target sets are derived from and reconciled with the asset inventory; recorded cases where a dependency was discovered after the fact; a reconciliation procedure between the target set and the tenancy records |
| **The shared-tenancy test surfaces foreseeable third-party harm** | The three questions at `AUTH-8` must be answered and recorded | Architectural assertion; unverified; it surfaces the harm the operator knows to look for. Parties who depend on the infrastructure without appearing in any inventory are not surfaced | Evidence of who performs the test and on what basis; recorded answers showing that the answers changed decisions; a measure of the proportion of operations where the test identified a party not previously known to the operator |
| **Fail-closed behaviour of the policy engine** | An unclassifiable action is refused, and a refusal is recorded as a successful control (`ROE-2`) | Architectural assertion; unverified | Test evidence covering the unclassifiable, the partially specified, and the contradictory cases; evidence that refusals are recorded in the ledger and are visible to the operator; a check that no configuration can set the engine to fail open |
| **Automatic reversion on failure** | Loss of telemetry, loss of the control plane, loss of communications, or an abort condition causes immediate reversion (Section 10) | Architectural assertion; unverified. It depends on the failure being detected, and the detection of a failure is not the same as the failure not occurring | Test evidence of each failure mode, including the case where detection has itself failed; a documented telemetry-liveness interval; evidence that reversion is not contingent on the model's agreement |
| **The abort mechanism remains effective where the console is compromised** | The abort channel is independent of the console (Section 10.2) | Architectural assertion; unverified; it is in tension with master design `LIM-8`, which records the console as a concentration of risk | An adversarial assessment of the console as an attack surface, covering the abort path; test evidence that abort succeeds with the console and the control plane degraded; a documented alternative route for each operation |
| **The collateral classification of a countermeasure is correct** | A class is determined by effect and never by intent (`ROE-6`) | Architectural assertion; unverified; the class is an assessment, and the assessment may be wrong in either direction | Evidence of the basis on which classes are assigned; recorded cases of a misclassification and of the harm that followed; a review procedure for classes assigned at the boundary |
| **The abort catalogue is sufficient** | The categories at Section 10.1 cover the conditions a card must anticipate | Architectural assertion; unverified. The catalogue is a floor and is not exhaustive of the ways an operation can go wrong | Review of every abort recorded in the set against the catalogue, with any condition that does not map to a category added to the catalogue; exercise evidence that operators use the conditions as written |
| **Deconfliction prevents interference with legitimate activity** | The conflict classes and the resolution order at Section 9 are applied before dispatch | Architectural assertion; unverified; it protects activity that is visible and declared | Evidence of the sources of legitimate activity that are integrated with the deconfliction check; recorded cases where a conflict was detected and resolved; an explicit account of the legitimate activity that is not visible to the system |
| **The EA structure produces a defensible authorisation record** | The elements at Section 4.1 constitute a complete and reviewable mandate | Architectural assertion; unverified; the structure is complete on its face, and completeness of a form is not adequacy of an authorisation | Independent review of EAs actually issued against this structure, with findings on sufficiency, particularity, and the quality of the legal basis recorded |
| **Disclosure satisfies legal obligations** | Third-party disclosure under `CON-8` discharges the operator's duties | Architectural assertion; unverified. Whether a disclosure satisfies an obligation is a question of law in the jurisdiction in which it is owed, and this document does not answer it | Written advice from the legal contact on the adequacy of the disclosure timing, content, and route in each jurisdiction in which the operator operates |

**VER-C1 — Principle for use.** Where a claim in this section is cited, it must be accompanied by this section, or by a statement that verification is outstanding. Absolute phrasings such as *prevents*, *guarantees*, *cannot*, and *always* must not be repeated as verified guarantees of the framework's behaviour.

**VER-C2 — Implementation conformance.** The reference implementation mechanically enforces the admissibility algebra, the scoring model, the ledger, and the policy engine. It does not verify that a produced document satisfies the prose requirements in this document. The requirements that are mechanically enforced are listed in `reference/audit-and-conformance-procedures.md` §3, and the absence of automated checking of this document's prose is recorded as `LIM-14` in the master design.

**VER-C3 — The verification status travels.** Where an operation, a card, a report, or an external communication relies on a claim in this section, it must carry the claim's status with it. A status that is dropped in transmission has not been discharged.

---

## 14. Conformance

Conformance with this document is assessed on three dimensions.

1. **Authorisation conformance** — whether the operation was conducted within a valid EA, at or below the profile, collateral, and autonomy ceilings, against authorised targets only, at the required approval depth, with the required instruments, and within the time bounds (Sections 4, 5, and 8).
2. **Control conformance** — whether the abort, expiry, reversion, deconfliction, refusal, pause, preservation, and disclosure controls were present on the card, exercised when their conditions obtained, and recorded (Sections 9, 10, and 12).
3. **Disclosure conformance** — whether claims about the framework's protective properties are presented with the verification status recorded in Section 13, and whether the reporting of effect, confidence, and residual risk is honest (Sections 12 and 13).

**CONF-C1 — Substance over wording.** An operation, artefact, or system that satisfies a requirement of this document in substance, if not in the exact wording prescribed, conforms to that requirement. The test is whether the requirement's purpose is achieved and evidenced, and not whether the prescribed phrase appears. The converse also holds: an operation that uses the prescribed wording without achieving the requirement's purpose does not conform.

**CONF-C2 — The evidence is the artefact.** Conformance is assessed on the observable record: the EA, the card and its revisions, the escalation request, the decision log, the abort records, the ledger entries, and the after-action report. A claim of conformance unsupported by the record is not a conformance finding.

**CONF-C3 — Absence of evidence.** Where a requirement's evidence is absent, conformance is not established. It is not recorded as a breach unless the record shows the requirement was engaged and was not met; where the record cannot show either, the finding is an indeterminate, and the indeterminate is recorded as an open item with the evidence that would resolve it.

The procedure by which conformance is assessed, the ledger verification, and the replay of an operation are owned by `reference/audit-and-conformance-procedures.md`.

---

## 15. Document limitations

These limitations are local to this document. They are additional to the set-wide limitations `LIM-1` to `LIM-14` in the master design, and they do not renumber them.

**LIM-C1 — The framework cannot create legal authority.**
This document structures an authority that a named human has granted. It cannot supply the legal basis where none exists, cannot judge whether a stated basis is sufficient in the jurisdiction in which it is relied upon, and cannot extend an EA across a boundary its issuer did not cross. `AUTH-5` and `CON-7` require the authority to exist; they do not produce it.

**LIM-C2 — Third-party exclusion depends on enumeration.**
`AUTH-6` excludes third-party infrastructure from the general scope of an EA, but it can only exclude what the EA has identified. A dependency that appears in no inventory, no tenancy record, and no telemetry is not excluded, and not because it was overlooked but because it was not visible. The exclusion is a rule about the authorisation, not a detector for shared infrastructure.

**LIM-C3 — The shared-tenancy test is an estimate by an uninformed observer.**
`AUTH-8` requires three questions to be answered, and the person answering them is assessing the interest and the expected harm of parties they do not know. The answers are informed estimates, and they are estimates of a thing that is usually not measured. The test surfaces what the operator knows to look for and cannot manufacture knowledge of parties who have not been identified.

**LIM-C4 — The reversibility scale is coarse.**
The four categories at Section 3.1 are a judgement about a continuum. A countermeasure assessed as **Low** may be, in fact, effectively reversible, and one assessed as **Reversible** may not be. The assessment is made by the person deciding, before the effect is known, and no category in the scale anticipates a consequence that has not been thought of.

**LIM-C5 — Irreversibility is assessed, not guaranteed.**
Whether an action is irreversible is determined before it is taken, on the basis of the operator's understanding of the target's configuration and of the parties affected. The framework requires the irreversible elements to be named and argued, and it cannot verify that the list is complete.

**LIM-C6 — Approval depth is a proxy, not a quality.**
A deeper approval is treated as a better decision because a deeper approval brings in a person with a wider obligation and, at R4 and above, a legal contact. This is an assumption about the organisation rather than a property of any individual approval. A shallow approval by an attentive person may be better than a deep approval by a hurried one, and the framework cannot tell the difference. It cannot detect a rubber-stamp approval at any depth.

**LIM-C7 — The EA is as good as its authors.**
The structure at Section 4.1 makes a mandate reviewable. It does not make the mandate sound. A poorly specified target set, a stale legal basis, or an expiry set beyond the period the operation can actually last is a defect the form will not catch.

**LIM-C8 — Deconfliction protects what is visible.**
Section 9 protects the legitimate activity the system can see and the operator can declare. Live operations, freezes, and production traffic that are not recorded in the systems the deconfliction check consults are not protected by it.

**LIM-C9 — The thresholds in this document are design values.**
The attribution confidence minima used at the collateral classes, the collateral ceilings of the profiles, and the class boundaries themselves are design values chosen for consistency and defensibility. They have not been calibrated against outcome data, and no claim is made that they are optimal.

**LIM-C10 — Enforceability depends on the control plane.**
The ceilings in this document are enforced by the policy engine and the control plane. An actor with the ability to alter a card's recorded class, to disable the engine's checks, or to issue an EA to themselves is outside the framework's reach, and the framework provides no defence against that actor beyond the ledger's record of what was done.

**LIM-C11 — No operational experience.**
This document has not been exercised against a live operation. Its requirements are design intent, its worked consequences are constructed illustrations rather than records of events, and the first operations conducted under it should be treated as a controlled trial in which the requirements are tested as well as applied.

**LIM-C12 — Cross-jurisdiction operation is not modelled.**
`CON-7` requires authority for every jurisdiction in which an operation has effect, and this document supplies no mechanism for determining which jurisdictions those are. The determination of reach is a legal question, and the framework's target enumeration is not equipped to answer it.

---

## 16. Summary

This document is the constitutional anchor of the set. Everything else in the framework operates inside the boundary it draws.

The boundary is drawn in three layers. The engagement authorisation supplies the mandate: what the operation is for, on what legal basis, against which targets, with which ceilings, until when, and on whose authority. The rules-of-engagement profiles supply the ceiling: what may be done, at what collateral class, with how much autonomy, approved at what depth. The constitutional conduct constraints supply the limit that the authority itself cannot exceed: the human who decides, the prohibition on making people the object of a countermeasure, the exclusion of third parties, the refusal to conceal, and the duty to report honestly what happened.

Three commitments recur throughout. Authority is structural rather than advisory: a ceiling that a request above it cannot pass, enforced by a policy engine that fails closed and records its refusals. The cheap mistake is preferred to the expensive one: identity-directed action over infrastructure-directed action, reversibility over irreversibility, shaping over disruption, containment over destruction, and a recorded comparison against the risk of inaction in every case. And the record is the deliverable, so that a reviewer who was not present can reconstruct what was known, what was chosen, what was declined, and what would have stopped it.

The framework's own reach is stated in Section 13 and its own weaknesses in Section 15. It does not create authority, does not make attribution reliable where the adversary has chosen to be indistinguishable, does not see third parties that no inventory records, and does not make an approval a good decision. What it does is make the authority explicit, bound the action to it, make the uncertainty visible at the moment of choice, and make the whole of it reconstructible afterwards.

---

*This was supported for MIA by Kilo (kilo-auto/free).*
