# Watchfloor Interface Specification: CAOS — Counter-Adversary Operations System

| Field | Value |
| --- | --- |
| Author | MIA |
| Attribution | This was supported for MIA by Kilo (kilo-auto/free). |
| Document type | Interface specification |
| Subject | The operator console of the Counter-Adversary Operations System: capabilities, information architecture, the approval surface, interlock semantics, the abort control, accessibility, security posture, and the audit surface |
| Scope | The Watchfloor and the interface-level requirements it imposes. The machinery beneath the interface is specified in `operational/platform-architecture-and-agent-containment.md` |
| Layer | L4 Platform Layer |
| Identifier range | `WF-01`–`WF-21` (capabilities); `WF-22`–`WF-30` (interface-level requirements spanning capabilities); `WFP-1`–`WFP-16` (design principles); `LIM-WF1`–`LIM-WF12` (limitations) |
| Version | 1.0 |
| Status | Authoritative for the interface. Component documents remain individually authoritative for their own requirements |
| Companion documents | See the companion table below |

**Companion documents**

| Path | Relationship to this document |
| --- | --- |
| `system-design-and-framework.md` | Master design. §10 states the capability summary this document expands; §10.1 states the eight interface design constraints that become `WFP-1`–`WFP-8`; §2, §4, §5, §6 and §8 supply the objectives, mandate, intelligence model, decision-support model and control model the interface renders |
| `README.md` | Set index. Controlled vocabulary, conventions, identifier registry, change control |
| `constitutional/engagement-authorisation-and-rules-of-engagement.md` | The engagement authorisation, ROE profiles R0–R5, collateral classes C0–C3, autonomy classes AC-0–AC-4, and the authorisation ladder the interface renders |
| `compliance/operator-conduct-and-human-in-loop-standard.md` | Operator duty, human-in-the-loop checkpoints, uncertainty and attribution-error handling, escalation ethics |
| `operational/mission-lifecycle-and-decision-loop.md` | The six phases, the eight gates, the Operation Card lifecycle, the decision record, the error handler, the deconfliction procedure |
| `operational/platform-architecture-and-agent-containment.md` | Sensor and collector layer, fusion, policy engine, control plane, containment model, resilience, data protection, the ledger |
| `operational/adversary-ai-taxonomy-and-threat-model.md` | The AAT taxonomy the classification console renders, and the proving ground the interface exercises |
| `operational/countermeasure-catalogue.md` | The countermeasure set, with class, collateral class, reversibility, autonomy class and attribution dependency |
| `operational/decision-support-and-scoring-model.md` | Threat score, attribution confidence, residual risk, the admissibility algebra, the selection algorithm |
| `reference/audit-and-conformance-procedures.md` | Conformance assessment, ledger verification, replay procedure, the mechanically-enforced requirement register |
| `templates/operation-card.md` | The card the card editor edits and the approval surface presents |
| `templates/rules-of-engagement-card.md` | The pocket reference the interface renders in compact form |
| `templates/decision-log.md` | The record the interface produces for each decision |
| `templates/escalation-request.md` | The instrument the escalation console raises |
| `templates/after-action-report.md` | The artefact the reporting view generates |
| `templates/tabletop-exercise-pack.md` | The artefact the exercise analytics and proving ground views support |
| `impl/` | The executable reference implementation of the Watchfloor, against which the requirements in this document are testable |

---

## 1. Purpose and Scope

### 1.1 Purpose

The Watchfloor is the operator's only sanctioned point of contact with the estate and with the decision-support model. Everything the framework produces — signals, clusters, classifications, attributions, scores, hypotheses, countermeasures, admissibility results, authorisations, dispatches — reaches the human operator through the Watchfloor, and every consequential act the human takes is taken through it. It is therefore the place where the framework's abstractions either become real decisions or remain paperwork.

Three properties follow, and they govern everything in this document.

First, the Watchfloor is a high-value target, and this specification treats it as one. It holds the most sensitive view of the operator's estate — what the adversary is doing, what the operator has decided, what has been authorised, and what has been dispatched — and it holds the authority to act on that view. An adversary that can influence what the operator sees, or what the operator believes the operator has seen, can steer a defensive operation into an offensive one without touching the estate at all. The interface is therefore specified as an adversary-facing surface throughout, and adversary-supplied content is treated as hostile by default rather than as a display convenience.

Second, the interface is the enforcement point for several of the framework's controls, and enforcement is where interfaces are usually weak. The policy engine enforces the rules of engagement; the control plane enforces dispatch-time admissibility; the ledger enforces the record. But the operator's decision itself — the selection among candidates, the reading of the risk, the judgement that the residual risk is acceptable — exists nowhere except at the interface. An approval that is made without comprehension is not a decision, it is a timestamp. The Watchfloor must therefore make the decision real, or the control above it is theatre.

Third, and stated plainly because it is the premise of this document: **a control implemented only in the interface is a control implemented badly.** A control that lives only in the console is enforced only where a user remembers to invoke it, vanishes the moment the interface is bypassed or wrapped, produces no evidence of its own operation, and cannot be audited by anyone who was not looking at the screen. Every control the Watchfloor enforces must be enforced at a layer beneath it — in the policy engine, in the control plane, or in the ledger — and the interface's three duties are to make that enforcement visible, to make it comprehensible to a human in time pressure, and to record it. Where the interface duplicates a decision that the engine also makes, the engine's answer is authoritative and the interface's is advisory.

### 1.2 Scope

| In scope | Out of scope |
| --- | --- |
| The capabilities the Watchfloor presents, WF-01 to WF-21 | The detection engineering that produces the signals those capabilities render (`operational/adversary-ai-taxonomy-and-threat-model.md`) |
| The interface-level requirements that span capabilities, WF-22 to WF-30 | The implementation of the sensor, fusion, policy, control-plane and ledger components beneath the interface (`operational/platform-architecture-and-agent-containment.md`) |
| The information architecture, navigation model, and the distances between operator actions | The mission process the interface supports (`operational/mission-lifecycle-and-decision-loop.md`) |
| The approval surface, and what must be on it | The rules-of-engagement profiles themselves (`constitutional/engagement-authorisation-and-rules-of-engagement.md`) |
| The ROE gate's behaviour as seen and exercised by the operator | The policy engine's internal evaluation algorithm, save where the interface's rendering of it is specified |
| The abort control's placement, behaviour and consequences | The abort conditions the operator writes onto a card, which are defined by the mission lifecycle |
| Accessibility, human factors, and the operator's attention budget | Physical workstation specification, environmental ergonomics and acoustic design |
| The security posture of the console as a privileged surface | The hardening of the rest of the estate, and the containment of adversary agents |
| The audit surface, the export, and the reconstructibility of a decision | The audit procedures performed by a reviewer (`reference/audit-and-conformance-procedures.md`) |
| Degraded and offline behaviour of the console | The resilience mechanisms of the platform, except where the interface must display their state |

### 1.3 Status of this specification

This document states design intent. Where it describes behaviour that has not been implemented and tested, that behaviour is an architectural assertion and is registered in Section 15. The verification status of the claims in this document is not implied by the existence of the reference implementation in `impl/`; the requirements that the implementation mechanically enforces are listed in `reference/audit-and-conformance-procedures.md` §3.

---

## 2. Interpretation of Normative Terms

The terms **must**, **must not**, **should**, **should not**, and **may** are to be interpreted as described in RFC 2119.

- **Must / must not** denote absolute requirements.
- **Should / should not** denote recommendations that may be departed from only where legitimate reasons exist; any departure should be made explicit.
- **May** denote optional behaviour that remains at the operator's discretion within the constraints of this document.

Three conventions apply additionally.

**Identifier namespaces.** The set uses several identifier prefixes, and this document introduces one of its own. The distinction matters because the canonical set already contains a near-homonym.

| Form | Scope | Origin |
| --- | --- | --- |
| `WFC-1` to `WFC-8` | The eight interface design constraints, formerly `WF-1` to `WF-8` in the master design. Renamed at set revision 1.0 to remove the ambiguity with the `WF-01` to `WF-30` capability range. | Master design §10.1. Restated normatively in this document as `WFP-1` to `WFP-8` |
| `WF-01` to `WF-21` | The twenty-one capabilities of the Watchfloor. | Master design §10. Expanded by this document |
| `WF-22` to `WF-30` | The nine interface-level requirements that span capabilities. | Introduced by this document |
| `WFP-1` to `WFP-16` | The design principles of the Watchfloor. `WFP-1` to `WFP-8` correspond one-to-one with master design `WFC-1` to `WFC-8`; `WFP-9` to `WFP-16` are introduced by this document. | Introduced by this document |
| `LIM-WF1` to `LIM-WF12` | The limitations of the Watchfloor. | Introduced by this document. Prefixed to avoid collision with the set-level `LIM-1` to `LIM-14` in master design §11 |

**Registry note.** The `WF-` prefix comprises `WF-01` to `WF-30` — the twenty-one capabilities and the nine interface-level requirements. The `WFP-` prefix comprises the sixteen design principles. The master design's eight interface design constraints, formerly numbered `WF-1` to `WF-8` and now `WFC-1` to `WFC-8`, were renamed at set revision 1.0 because the original numbering was a live hazard: `WF-1` and `WF-01` were one character apart and meant different things. The set index and the master design registry have been amended accordingly, and the ambiguity no longer exists.

**Architectural assertions.** Where this document records a claim about how the console will behave, that claim is an architectural assertion of the framework authors and not, absent explicit statement to the contrary, an independently verified property. Assertions are registered in Section 15.

**Labelling.** Claims rendered in the Watchfloor carry the claim labels and source reliability tiers defined in `compliance/operator-conduct-and-human-in-loop-standard.md` §3 and `reference/ai-attack-technique-library.md`. This document inherits those conventions and does not restate them.

---

## 3. Defined Terms

Defined terms are declared once here and referenced thereafter by the defined term rather than by repetition.

| Term | Definition |
| --- | --- |
| **the Watchfloor** | The operator console; the interface through which the human operator observes the estate, receives decision support, and acts on the framework's behalf |
| **the operator** | The named human who holds the console session and is accountable for the decisions recorded in it. The operator is not an account, a role, or a rota position; the identity is a person and the accountability is personal |
| **a view** | A distinct, addressable surface of the Watchfloor with its own purpose, its own refresh behaviour, and its own set of permitted interactions. Views are the unit of navigation |
| **a panel** | A bounded region of a view that presents one coherent subject. A panel is not independently addressable and does not carry its own navigation |
| **a widget** | The smallest presentational unit within a panel: a value, a badge, an indicator, a bar, a row of a table, or a sparkline. A widget carries no behaviour of its own beyond display |
| **the triage queue** | The ranked, filterable working list of unhandled signals and clusters through which raw observation enters the mission loop (`operational/mission-lifecycle-and-decision-loop.md`, Detect phase) |
| **a cluster** | A group of signals sharing indicators and a shared hypothesis, produced by the fusion layer, and the unit at which the triage queue is dispositioned |
| **a card** | An Operation Card: the atomic unit of authorised work, and the data structure the card editor manipulates and the approval surface presents |
| **the card editor** | The view in which a card is created and amended, in which mandatory fields are enforced, and in which revisions are compared |
| **the ROE gate** | The interlock that evaluates a proposed action against the rules-of-engagement profile in force, and the surface that displays the outcome of that evaluation |
| **the approval surface** | The single view on which a named human authorises a proposed action, carrying the evidence, the alternatives, the risks and the consequences that the authorisation rests upon |
| **the abort control** | The always-available control that terminates a running operation and revokes associated autonomy, capturing the reason for the termination |
| **the escalation console** | The view in which an escalation request is raised, routed through the approval chain, timed, and recorded |
| **the evidence ledger** | The view in which every claim supporting a decision is presented with its claim label, source reliability tier, confidence, provenance and derivation chain. The evidence ledger is a *view of claims*; it is distinct from **the Ledger** (§3.1) and must never be described by the same term |
| **the assumption panel** | The panel in which every assumption underlying a card is listed with the confidence of each claim that depends upon it |
| **the autonomy monitor** | The view in which autonomy budget consumption, the envelope, the expiry and the reversion trigger are displayed live |
| **the telemetry view** | The view of source liveness, degraded sources, ingest lag, and the cues that indicate silent failure |
| **the replay view** | The view in which an operation is reconstructed from the Ledger, with the world state at each step |
| **the proving ground** | The exercise harness in which an adversary is simulated in order to validate detection and rehearse operators |
| **the doctrine editor** | The view in which the policy set itself — thresholds, weights and the rules by which the policy engine judges — is authored, versioned and published |
| **the audit export** | The signed, independently verifiable bundle of the Ledger, the cards and their associated records, produced for an external reviewer |
| **interlock** | A mechanism that makes an action unavailable unless a stated condition holds. An interlock is not a warning, a prompt, a confirmation, or a suggestion; it is the condition being structurally enforced |
| **degradation** | The state in which a component or source is operating but not to specification: partially available, reduced in fidelity, or returning results of reduced confidence. Degradation is distinct from failure, in which the component is not operating, and distinct from an absence of activity, in which the source is operating correctly and reporting nothing |
| **source fidelity** | A graded statement of how completely and faithfully a source reported what was asked of it. Fidelity is a property of the reporting, not of the underlying activity |
| **the world model** | The card's stated model of the state of the world at the time of the decision: what was believed to be true, on what evidence, with what confidence. The world model is stated at a point in time and is expected to diverge from reality; the divergence is itself recorded |
| **the operator's estate** | The systems, accounts, networks, data, services and physical or virtual assets that the operator owns or is responsible for, and the assets whose compromise the operation exists to prevent |
| **the policy engine** | The component that evaluates a proposed action against the rules-of-engagement profile in force and returns an allow or a refusal, naming the specific rule and, where refused, the specific margin of exceedance |
| **the control plane** | The component that holds card state, arms and dispatches countermeasures, and re-checks admissibility at the moment of dispatch against the then-current world state |
| **the notification channel** | The path by which the system reaches the operator, or an escalation contact, with an event requiring attention. The notification channel is a path of last resort and an exception, not the ordinary delivery mechanism for information the operator has asked to see |
| **session** | An authenticated, time-bounded period of console use by one named identity. A session carries a role, a set of permissions, and a recorded start and end |
| **role** | A named set of permissions bound to an identity for the duration of a session. The roles used in this document are viewer, approver, executor and administrator, and are defined in Section 11.3 |
| **the audit record** | The Ledger entry created by an operator action or by an automatic system action. The audit record is the evidence that the action occurred, and it is written whether the action succeeded or failed |

### 3.1 The Ledger

**the Ledger** is the append-only, hash-chained record of decisions, authorisations, dispatches, and state changes, as defined in `README.md` §3 and specified in `operational/platform-architecture-and-agent-containment.md`. The Ledger is the substrate of auditability. It is not the evidence ledger (§3); the evidence ledger is an interface view over the claims that the Ledger's entries refer to.

---

## 4. Design Principles

### 4.1 How the principles are used

Each principle below is stated in three parts: the principle itself, which is normative; the interface consequence, which is what the Watchfloor must therefore do; and the failure mode it prevents, which is what happens if the principle is not honoured. The failure-mode column is not decorative. A principle whose failure mode cannot be described concretely is a slogan, and this document does not carry slogans.

The principles are stated at the level of interface obligation. They are not the design objectives (`DO-1` to `DO-14`, master design §2), which concern the system as a whole, and they are not the interface design constraints of master design §10.1, which they restate and extend.

### 4.2 The inherited principles

**WFP-1 — The console is an attack surface.** Adversary-controlled content reaches the operator's screen by design. The Watchfloor renders adversary-supplied content in a sanitised, non-executing representation, treats model output as untrusted input regardless of its origin, and is subject to the same hardening requirements as the rest of the operator's estate.

**WFP-2 — The operator can always stop.** The abort control is always visible, always reachable without navigating, and requires no confirmation. It is never buried under a menu, is never disabled, and is never gated behind a role or a state that the operator might be unable to satisfy.

**WFP-3 — No approval without comprehension.** An approval presents the evidence, the alternatives, the rejected candidates, the residual risk, the risk of inaction and the abort conditions on the same surface as the approval itself. An approver who must assemble that context from other screens has not been given a real choice.

**WFP-4 — Uncertainty is always visible.** Confidence, provenance, source fidelity and assumption dependencies are rendered inline. They are not placed behind a disclosure control, a hover, a tooltip, or a detail drawer.

**WFP-5 — The system states what it does not know.** The absence of a signal, an unreached source and an unexercised branch are shown as such, and are distinguished from a negative finding.

**WFP-6 — Degraded operation is a first-class state.** The console remains usable when a source is down and states which conclusions are affected by that absence. It never silently omits a missing source.

**WFP-7 — Automation is legible.** Where a classifier, a scorer or a recommender has acted, the operator sees that it acted, on what input, with what confidence, and can override it.

**WFP-8 — The record is not optional.** Every view in which a decision was made can be exported as the record of that decision.

### 4.3 The additional principles

**WFP-9 — The surface is small.** The Watchfloor presents the operator with the minimum information required to act, and nothing else. Every additional panel consumes attention that would otherwise be spent on the decision.

**WFP-10 — The unsafe option is never the easy one.** No interaction, layout, default, ordering or wording in the Watchfloor may make the unsafe action cheaper to take than the safe one.

**WFP-11 — Degradation reduces information, never safety.** Where the console loses a source, it loses the ability to say something, and it must not lose the ability to stop, to record, or to refuse.

**WFP-12 — Confirmations are reversible; the abort is not.** An operator may undo a confirmation, amend a selection, or reconsider a rejected candidate without penalty. The abort is the one action with no undo, and it is designed so that it needs none.

**WFP-13 — Attention is a finite resource and the interface manages it.** The Watchfloor controls how much it asks of the operator at once, suppresses what can be deferred, and surfaces what was suppressed rather than discarding it.

**WFP-14 — Observation, authority and execution are separate.** The role that watches the estate is not the role that authorises, and the role that authorises is not the role that executes. The interface enforces the separation it depends upon.

**WFP-15 — The console states its own fitness.** Every view carries the console's current fitness — its data freshness, its configuration version, and its operating mode — so that an operator can never mistake a stale console for a current one.

**WFP-16 — Interlocks are structural.** A check that lives in the client is a hint. Every interlock the Watchfloor presents is enforced by the policy engine or the control plane, and the console's rendering of it is an account of that enforcement rather than a substitute for it.

### 4.4 Principles, consequences, and the failures they prevent

| Principle | Interface consequence | Failure mode prevented |
| --- | --- | --- |
| **WFP-1** | Adversary content is rendered inert: plain text, escaped, in a marked container, with no active markup, no embedded instructions, no auto-loading artefacts. Model output is labelled as model output and is subject to the same containment. The console is in the operator's own red-team scope. | Prompt injection and content-borne manipulation steering an operator's decision without the operator ever seeing the injection |
| **WFP-2** | The abort control is in the persistent chrome of every view, requires one action and no confirmation, and is never disabled, hidden, or conditional. | An operation that cannot be stopped because the operator could not find the control, or was asked to confirm first |
| **WFP-3** | The approval surface is rendered as a single complete surface from a server-assembled bundle. Evidence, candidates, rejections, risk before and after, risk of inaction, collateral exposure and abort conditions are all present at the moment the control is presented. | Approval as a formality; a human in the loop who is technically in the loop and substantively absent |
| **WFP-4** | Confidence values, source tiers, provenance and assumption dependencies are inline fields in the element where they qualify. No confidence is conveyed by colour, position, or omission. | Certainty manufactured by layout, and an operator who cannot tell a 0.4 from a 0.9 without opening something |
| **WFP-5** | Each source and each analysis carries an explicit state: observed, absent, unreached, stale, degraded. An unreached source is rendered with the same weight as an observed one, marked as unreached. | Silence read as absence, and an unknown treated as a negative finding |
| **WFP-6** | A degraded source is rendered as a degraded source, in place, with the affected conclusions named. The console continues to operate on what it has, and says what it does not have. | Silent omission of a source, and a confident conclusion drawn from a partial picture |
| **WFP-7** | Every automated act is attributed to the automation that performed it, carries its inputs and its confidence, and is overridable in one action from the same surface. | Unattributable machine judgement, and a classification the operator believes they made |
| **WFP-8** | Every view writes a view-state snapshot to the Ledger when an operator action is taken on it, and every decision record references the snapshot that was on screen. | A record that records the outcome but not the context, and a decision that cannot be reconstructed |
| **WFP-9** | Each view declares a single primary object and defers everything else. Secondary content is reachable but not resident. | Decision fatigue; an operator who reviews everything and therefore understands nothing |
| **WFP-10** | Destructive and high-collateral actions are not the default, are not adjacent to the safe action in the layout, and never carry a shorter interaction path than the reversible alternative. | A mis-click becoming an incident, and a pattern of consumption of the unsafe option |
| **WFP-11** | Where any source is lost, the console's own protective functions — interlock, abort, recording, refusal — continue to operate at full strength. | A degraded console becoming a permissive console |
| **WFP-12** | Selections are amendable in place. Amendments are recorded as amendments, not as silent replacement. The abort is the sole irreversible control and is the only control with no undo affordance. | Operators choosing the first plausible option because changing it is inconvenient |
| **WFP-13** | Alerts are ranked, aggregated and capped. Deferred alerts are counted, summarised and re-surfaced rather than discarded. | Alarm fatigue; the significant alert lost in a stream of the insignificant |
| **WFP-14** | The console's permissions are bound to the session's role. Viewer, approver and executor are distinct, and the approval surface records the approving identity separately from the operating identity. | One compromised session authorising and executing its own actions; undetectable self-approval |
| **WFP-15** | A persistent status element shows the console's data freshness, configuration version and mode. Every view inherits it, and it changes when any source changes state. | An operator acting on a picture that stopped updating an hour ago |
| **WFP-16** | The ROE gate's display is generated from the policy engine's answer, with the engine's rule reference and margin of exceedance. A local re-implementation of the rules is never the basis of a display. | A console that permits what the engine would refuse, because the two disagree and the console is trusted |

### 4.5 Principle-to-capability mapping

| Principle | Capabilities that carry it |
| --- | --- |
| **WFP-1** | WF-02, WF-04, WF-08, WF-11, WF-16, WF-19 |
| **WFP-2** | WF-15 (primary), WF-13, WF-01, WF-10 |
| **WFP-3** | WF-06, WF-07, WF-08, WF-10, WF-12 (primary carrier: the approval surface, §7) |
| **WFP-4** | WF-01, WF-04, WF-08, WF-11, WF-12, WF-13 |
| **WFP-5** | WF-02, WF-14, WF-05, WF-17 |
| **WFP-6** | WF-02, WF-03, WF-09, WF-13, WF-14, WF-17, WF-18 |
| **WFP-7** | WF-04, WF-05, WF-08, WF-13, WF-17, WF-18, WF-19 |
| **WFP-8** | WF-06, WF-11, WF-16, WF-20, WF-21 (primary carrier: §13) |
| **WFP-9** | WF-01, WF-03, WF-06, WF-10 |
| **WFP-10** | WF-06, WF-08, WF-10, WF-15 |
| **WFP-11** | WF-07, WF-13, WF-14, WF-15 |
| **WFP-12** | WF-04, WF-06, WF-08, WF-10, WF-15 |
| **WFP-13** | WF-01, WF-03, WF-14, WF-17 |
| **WFP-14** | WF-06, WF-08, WF-10, WF-15, WF-21 |
| **WFP-15** | All views, through the persistent chrome (§5.4) |
| **WFP-16** | WF-07 (primary), WF-08, WF-13, WF-19 |

---

## 5. Information Architecture

### 5.1 The top-level view set

The Watchfloor presents twenty-one capabilities. They are organised into five groups, and the grouping is a navigation aid rather than a hierarchy of authority: no group may be entered without the same authentication and session policy as any other, and no group's content may be reached only through another group.

| Group | Views | Purpose of the group |
| --- | --- | --- |
| **A — Situation** | WF-01 Watchboard, WF-02 Signal Ingest, WF-03 Triage Queue, WF-14 Telemetry and Health | What is happening now, and how much of it can be believed |
| **B — Understanding** | WF-04 Classification Console, WF-05 Hypothesis Ladder, WF-11 Evidence Ledger, WF-12 Assumption Panel | What it means, and how certain anyone is about it |
| **C — Decision** | WF-06 Card Editor, WF-07 ROE Gate, WF-08 Countermeasure Console, WF-09 Deconfliction Map, WF-10 Escalation Console | What to do, whether it is permitted, and how to obtain the authority to do it |
| **D — Execution** | WF-13 Autonomy Monitor, WF-15 Abort and Recall | What is running, and how to stop it |
| **E — Assurance** | WF-16 Replay and Timeline, WF-17 Exercise Analytics, WF-18 Proving Ground, WF-19 Doctrine Editor, WF-20 Reporting, WF-21 Audit Export | What happened, whether it would work again, and whether anyone can check |

### 5.2 View specification

| View | Purpose | Primary user | Refresh behaviour | What it must always show | What it must never show |
| --- | --- | --- | --- | --- | --- |
| **WF-01 Watchboard** | Live situation: active campaigns, open cards, confidence decay, autonomy utilisation, approaching expiries | Operator on watch | Continuous push; re-render on any state change | Current posture; open cards with their risk state; autonomy consumption; expiries in time order; console fitness | Deduplicated raw signal; unlabelled conclusions; the adversary's payload text rendered executably |
| **WF-02 Signal Ingest** | Event stream with integrity state, source fidelity and provenance | Operator on watch; analyst | Continuous push, append-only | Each event with integrity state, source, timestamp, fidelity, provenance; gaps in the stream | Events presented without a fidelity grade; events whose provenance is unstated |
| **WF-03 Triage Queue** | Ranked, filterable queue with clustering, deduplication and bulk disposition | Operator on watch; analyst | Re-ranked on change; manual refresh permitted | Rank and rank basis; cluster composition; the disposition state of every item | Unlabelled ranking; items silently removed from the queue; bulk actions without a preview of their effect |
| **WF-04 Classification Console** | Assisted classification against the AAT taxonomy, with rationale, confidence and operator override | Analyst; operator | On load and on demand | The signal set; the proposed categories with rationale and confidence; the operator's override state; taxonomy version | A classification without a rationale; an override that is not recorded; taxonomy identifiers without their version |
| **WF-05 Hypothesis Ladder** | The operator's working hypotheses, their support, contradictions and disconfirming observations | Operator; analyst | On change; manual refresh | Each hypothesis with its status, its supporting and contradicting evidence, and its disconfirming observation | A hypothesis presented without a disconfirming observation; a supported hypothesis presented as established |
| **WF-06 Card Editor** | Create and amend Operation Cards; mandatory-field enforcement; diff of revisions | Operator; approver | On load; re-validated on every edit | Every mandatory field with its completion state; the current revision; the diff against the previous revision; the live ROE gate state | An incomplete card that can be saved as if complete; an amendment that erases the prior revision |
| **WF-07 ROE Gate** | The hard interlock: the current profile, the ceiling, the requested action and the margin of exceedance | Operator; approver; authorising authority | On every evaluation; the engine's answer is authoritative | The profile in force; the ceiling; the requested action; the engine's verdict with rule reference; the margin of exceedance where refused | A local approximation of the rules; a verdict without its rule reference; a silent failure |
| **WF-08 Countermeasure Console** | Candidate generation, admissibility results, ranking, selection, and the rejected set with reasons | Operator | On demand; re-evaluated on any change to the card or the world state | The full candidate set; the admissibility result per candidate with the failed condition and the value that would have made it admissible; the ranking; the selection | A candidate list without its rejected members; a rejected candidate without its reason; a ranking presented as a recommendation without the operator's preference |
| **WF-09 Deconfliction Map** | Live legitimate operations overlaid on intended effect, with automatic conflict detection | Operator | Continuous; re-evaluated on dispatch-intent change | Live operations; the intended effect envelope; conflicts and near-conflicts; the deconfliction verdict | A deconfliction result without the live-operation set it was computed against |
| **WF-10 Escalation Console** | Approval chain, quorum, timers and the pending request queue | Approver; authorising authority; operator | Continuous for timers; on change for chain state | Each pending request with its stage, its timer, its required quorum and who holds it; the decision taken and by whom | A request whose expiry is not visible; a quorum shown without the outstanding names; a chain shown as complete when it is not |
| **WF-11 Evidence Ledger** | Every claim with label, tier, confidence, provenance and derivation chain | Operator; approver; auditor | On demand; snapshot on demand | Every claim with its label, tier, confidence, provenance and derivation; superseded claims retained and marked | A claim without a label or tier; a derivation shown without its weakest input; a superseded claim shown as current |
| **WF-12 Assumption Panel** | Every assumption behind a current card, with the confidence that depends on it | Operator; approver | On change to the card | Each assumption; each dependent claim; the confidence of each dependent claim; the effect of the assumption being false | An assumption without its dependents; a dependent claim whose confidence is not shown as dependent |
| **WF-13 Autonomy Monitor** | Budget consumption, envelope, expiry and reversion trigger, live | Operator | Continuous, live | Consumption against budget; the envelope's boundaries; the expiry countdown; the reversion trigger and its current state | A budget shown without its envelope; an expiry hidden while an operation runs inside it; a reversion trigger not shown until it fires |
| **WF-14 Telemetry and Health** | Source liveness, degraded sources, ingest lag, and the silent-failure cues | Operator; platform engineer | Continuous | Per-source liveness; ingest lag; degraded and unreached sources; the silence window; the last successful contact time | A source shown as healthy because it has not been checked; an unreached source shown as idle |
| **WF-15 Abort and Recall** | Single, prominent, always-available termination of any running operation, plus the reason capture | Operator | Always resident; state updates on change | The abort control; the list of running operations; the reason-capture dialog; the abort channel's own health | A disabled abort control; a confirmation step before abort; the abort control hidden behind navigation |
| **WF-16 Replay and Timeline** | Reconstruction of any operation from the Ledger, with the world state at each step | Auditor; operator; reviewer | On demand | The ordered sequence of records; the world state at each step; the decisions and their reasoning; the view snapshots referenced | A reconstructed sequence without the source record references; an edited or smoothed presentation of the sequence |
| **WF-17 Exercise Analytics** | Detection coverage against the taxonomy, false-positive cost, MTTD and MTTR, gap list | Operator; platform engineer; exercise facilitator | On demand; recomputed on exercise completion | Coverage by taxonomy category; the cost of false positives; the detection and response intervals as measured; the gap list | Coverage expressed without its denominator; intervals presented without the exercise that produced them |
| **WF-18 Proving Ground** | Adversary simulation for detection validation and operator rehearsal | Operator; exercise facilitator; analyst | Continuous during an exercise | The exercise state; the adversary behaviour as it is simulated; the detection and response events as they occur; the scoring rubric | A simulation outcome presented as a field result; adversary behaviour rendered executably |
| **WF-19 Doctrine Editor** | The policy set itself: thresholds, weights, and the rules by which the engine judges | Administrator; platform engineer | On load; staged changes applied on publish | The current doctrine version in force; the staged version; the diff; the affected rules and their dependent cards; the publication state | An unpublished change shown as in force; a change applied without its version recorded |
| **WF-20 Reporting** | After-action report generation from the Ledger, with the metrics and the gap list | Operator; authorising authority | On demand | The source records the report is built from; the metrics with their derivation; the gap list; the report's own verification status | A metric without its derivation; a report that omits the records it was built from |
| **WF-21 Audit Export** | Signed, verifiable export of the Ledger and the cards for an external reviewer | Auditor; authorising authority | On demand, with a visible progress and integrity state | The manifest of every artefact included with its hash; the chain state; the signature state; the verification instructions | An export without its manifest; a partial export presented as complete |

### 5.3 The navigation model

Navigation in the Watchfloor is by view, and views are flat with respect to authority. There are three navigation gestures and no others: **switching view**, **opening an object** (a card, a cluster, a claim, a request), and **going back**. There is no drill-down hierarchy in which a panel becomes a view, no modal dialog that contains a view, and no context in which the abort control is not present.

| Gesture | Semantics | Effect on the audit record |
| --- | --- | --- |
| Switching view | Changes what is displayed; changes nothing else | A view-state snapshot is written on entry and on exit |
| Opening an object | Binds the current view to a specific object — a card, a cluster, a claim, an escalation request | The binding is recorded, so the snapshot identifies what was in focus |
| Going back | Returns to the previous binding or the previous view | Recorded as a view transition, not as a decision |

Opening an object from the watchboard and opening the same object from the triage queue produce the same object view. The Watchfloor has one representation of an object and many ways to reach it. This matters for the audit surface: the record must be able to say that the operator was looking at card K-114 when they decided, regardless of how they arrived.

**The one-click rule.** Any action whose omission would change the safety of the operation must be reachable in one action from the current view, without navigation and without a menu. Two things in this document are permanent members of that class:

1. **The abort control.** Present in the persistent chrome of every view, addressed by a single fixed key binding and by a fixed position.
2. **The current card's risk state.** The residual risk, the risk of inaction, and the autonomy utilisation of the card currently in focus are shown in the persistent chrome at all times, not only on the card or the approval surface.

The two-click rule applies to everything else that is not ambient. A two-click path may pass through one intermediate view, and the intermediate view may not itself require a decision to be taken in order to continue. A control whose failure mode would be an unmitigated risk must not be two clicks away.

**What may not be collapsed.** The following must remain separately addressable, and a redesign that merges them does not conform to this document: the evidence ledger and the assumption panel (a claim is not an assumption, and the operator must be able to see the difference); the countermeasure console and the deconfliction map (a candidate's admissibility and its conflict with live operations are different questions); the escalation console and the approval surface (an escalation request and a direct authorisation are different instruments with different depths); and the audit export and the reporting view (a reviewer-facing verifiable bundle and an internal narrative are different products).

### 5.4 The persistent chrome

Every view carries the same persistent chrome. It is the part of the interface that the operator does not have to navigate to in order to know where they are and what the system thinks is happening.

| Element | Behaviour | Failure mode it prevents |
| --- | --- | --- |
| **Abort control** | Always present, always enabled, always one action (§9) | An operation that cannot be stopped |
| **Current card risk state** | Residual risk, risk of inaction, autonomy utilisation, and card expiry for the card in focus; dimmed with an explicit label when no card is in focus | Operating on a card whose risk has moved without noticing |
| **Console fitness strip** | Data freshness (age of the freshest source), doctrine version in force, operating mode (normal, degraded, offline-read), and the identity and role of the session | Acting on a stale picture; an operator unaware of which role they are acting in |
| **Notification inbox indicator** | Count of deferred notifications, with the oldest age; never a modal interruption | Unattended escalation, and a console that interrupts work to deliver trivia |
| **Degradation banner** | Appears when any source or component is degraded, failed or unreached; names the affected capability and the affected conclusions (§12) | Silent partial operation |
| **Command line** | Direct addressing of a card, cluster, claim or request, returning to the current view state afterwards | Navigation as the bottleneck on a time-critical lookup |

---

## 6. The Twenty-One Capabilities

Each capability below is specified under its own identifier. The identifier is the capability; the specification is its full normative detail. Master design §10 states each capability's purpose in one line; that line is expanded here into elements, interactions, failure behaviour, record behaviour, and the operator burden the capability is permitted to impose.

Throughout this section:

- **Refresh behaviour** describes when the element's displayed state is recomputed, not how quickly the underlying data changes.
- **Data drawn on** names the authoritative source of the element's content. Where a view displays a value that originates in another component, that component is named, and the console does not recompute it.
- **Operator burden** states the attention the capability is permitted to cost. A capability that exceeds its stated burden does not conform to this document, and the remedy is to reduce the surface, not to train the operator harder.

### 6.1 WF-01 — Watchboard

**WF-01 — Watchboard.** The Watchboard is the operator's ambient view of the operation. It shows the active campaigns, the open cards, the decay of confidence in the picture, the consumption of autonomy, and the expiries that are approaching, in a form that can be read in a single glance and acted upon in a single action. It is the view the operator returns to between decisions and the view they see when something has changed while they were elsewhere.

**Purpose.** The Watchboard exists to answer the question the operator has when they look up from the work: *is anything different, and does it need me?* It is a situational awareness surface, not a queue and not a control panel. It is designed to be read in under five seconds, because it is read far more often than it is acted upon, and because a surface that takes longer to read than the next alert takes to arrive will be abandoned.

**Elements.**

| Element | Type | Refresh behaviour | Data drawn on |
| --- | --- | --- | --- |
| Posture banner | Panel | On change | Control plane's current posture; engagement authorisation state; expiring authorisations |
| Active campaign list | Table | On change; re-ordering on state change | Fusion layer's campaign state; cluster store |
| Open card summary | Table | On change | Control plane card state; card repository; residual risk computed by the scoring model |
| Confidence decay strip | Sparkline per card | Periodic, on the scoring refresh cycle | Attribution confidence over time from the fusion layer; scoring model history |
| Autonomy utilisation | Gauge per active operation | Continuous | Control plane autonomy counters; the card's declared budget |
| Expiry ladder | List | On change | Card expiry; engagement authorisation expiry; escalation request timers; autonomy grant expiry |
| Live alert stack | Stack of alert rows | Continuous | Notification channel; the alert ranking described in §10.8 |
| Console fitness strip | Persistent strip | Continuous | Source liveness from the telemetry view; doctrine version; session identity and role |

**Interactions.** The operator can open a campaign and thereby open the cluster and the card it belongs to; open a card directly; acknowledge and defer an alert with a stated reason; change the display order of the card summary; and collapse the alert stack to a count. The operator cannot approve, dispatch, abort, or edit from the Watchboard; it is a navigation and awareness surface, and every one of those actions belongs to a surface that is built for it.

**Failure and degradation.**

| Source state | Behaviour |
| --- | --- |
| A telemetry source down | The affected card or campaign is shown with its source marked unreached, the conclusions that depend on it named, and its confidence decay strip shown as interrupted rather than flat |
| Fusion layer stale | The banner states the age of the picture; the card summary is marked as of that time; the operator can request a fresh evaluation but is not told that one is unnecessary |
| Control plane unreachable | The posture banner is replaced by an explicit statement that the current posture is unknown; the watchboard does not display the last known posture as if current |
| Ledger unwritable | A banner states that actions taken from this view will not be recorded, and the operator is warned before acting |

**Audit and record.** Every entry to and exit from the Watchboard writes a view-state snapshot. Every alert acknowledgement writes a record naming the alert, the operator, the time, and the reason for the deferral. Opening an object writes the binding. The Watchboard writes no decision records of its own, because it takes no decisions.

**Operator burden.** The Watchboard is the highest-frequency view in the system and must therefore be the lowest-burden. Its budget is a single glance and at most three distinct judgements: whether the posture has changed, whether anything on the expiry ladder requires action now, and whether the live alert stack contains something that cannot be deferred. Where the number of open cards or active campaigns exceeds what can be ranked in one glance, the watchboard ranks and truncates explicitly, states that it has truncated, and makes the full set one click away. It must never display an unranked wall.

### 6.2 WF-02 — Signal Ingest

**WF-02 — Signal Ingest.** The Signal Ingest view presents the event stream as it arrives, with the integrity state, source fidelity and provenance of every event, and with the gaps in the stream made as visible as the events themselves. It exists so that the operator can see what the sensors are actually reporting, rather than a cleaned-up version of it.

**Purpose.** Signal Ingest is the bottom of the evidence stack. It is where source fidelity and integrity state become visible to a human, and where the framework's rule that absence is a condition to be explained is given its practical expression. A stream that omits its gaps is a stream that makes silence indistinguishable from health.

**Elements.**

| Element | Type | Refresh behaviour | Data drawn on |
| --- | --- | --- | --- |
| Event stream | Table, virtualised | Continuous append; prepend only where the source's own sequence requires it | Sensor and collector layer's normalised event feed |
| Integrity state column | Badge per event | With the event | The ingest service's integrity determination |
| Fidelity grade column | Badge per event | With the event | The source's reported fidelity; the ingest service's assessment where it differs |
| Provenance column | Key-value per event | With the event | Collector metadata: collector identity, collection time, transformation history |
| Source selector | Selector | On change | The registered source inventory |
| Stream gap markers | Marker row within the stream | On detection | The ingest service's gap and silence-window detections |
| Silence window readout | Panel | Periodic | The per-source silence window; the last successful contact time |

**Interactions.** The operator can filter by source, integrity state, fidelity grade and time range; open an event's full provenance; open the source's health entry in the telemetry view; and mark an event as reviewed, which records the marking but does not disposition the underlying cluster. The operator cannot classify, score, or disposition from the stream; those belong to the triage queue and the classification console.

**Failure and degradation.**

| Source state | Behaviour |
| --- | --- |
| A collector down | The stream continues with a gap marker at the point of loss, the source's last successful contact time shown, and the events after the gap marked as unverified continuity |
| Ingest lag building | The stream shows the lag explicitly, with the age of the newest event, and marks the point after which events are late |
| A source reporting at reduced fidelity | Events are badged with the reduced fidelity grade, and any conclusion drawn from them is marked as resting on reduced-fidelity evidence |
| Provenance incomplete for some events | Those events are marked as provenance-incomplete and are excluded from the set of events eligible to support a labelled claim |

**Audit and record.** View-state snapshots on entry and exit. A marking of an event as reviewed writes a record. The stream itself is not copied into the Ledger event by event; the Ledger records the stream's state hash at each snapshot, so that the stream at the moment of a decision is provable without storing the stream twice.

**Operator burden.** The Signal Ingest view is a monitoring surface, not an analysis surface. Its budget is one judgement per inspection: whether the stream is healthy. An operator who must read the stream to understand the estate is using the wrong view. It must never be the default landing view, and it must never auto-expand on entry.

### 6.3 WF-03 — Triage Queue

**WF-03 — Triage Queue.** The triage queue is the ranked, filterable working list of unhandled signals and clusters, in which clustering, deduplication and bulk disposition are performed, and from which work enters the mission loop.

**Purpose.** The triage queue is the interface's throughput bottleneck and the point at which most false positives die. Its ranking is an allocation of human attention under scarcity, and its design obligation is therefore to make the ranking inspectable: the operator must be able to see why an item is where it is, and to disagree.

**Elements.**

| Element | Type | Refresh behaviour | Data drawn on |
| --- | --- | --- | --- |
| Queue table | Table | Re-ranked on change; manual refresh permitted | Fusion layer's cluster store; the scoring model's risk-adjusted priority |
| Rank and rank basis column | Key-value per row | With the row | The score components that produced the priority, per SCORE-2 |
| Cluster composition | Expandable panel per row | On demand | The cluster's member signals and their source fidelity |
| Deduplication marker | Badge per row | With the row | The ingest service's duplicate grouping |
| Filter bar | Control group | On change | The cluster store's indexed attributes |
| Bulk disposition control | Action group | On demand | The current selection and its aggregate composition |
| Disposition history | Panel | On change | The triage dispositions already recorded |

**Interactions.** The operator can filter, re-rank within a filter by any score component, expand a cluster, open it for classification, assign a disposition — promote to a card, hold for a later signal, or mark as not actionable with a stated reason — and perform bulk disposition over a selected set with a preview of the aggregate effect before commitment. A bulk disposition over more than a stated threshold of items requires a reason and is recorded as a distinct decision record.

**Failure and degradation.**

| Source state | Behaviour |
| --- | --- |
| Scoring model unavailable | Items are ranked by the last computed priority, with the age of that computation shown; new items are appended at the end marked unranked, and are not silently given a nominal rank |
| Cluster store stale | The banner states the age of the queue; the operator is told that new signals are not being reflected |
| A source degraded | Items depending on it are badged, and the ranking carries a degraded flag on those items |
| Deduplication unavailable | The queue displays items individually and states that dedup is not being applied, so that the operator does not read the count as an activity count |

**Audit and record.** Every disposition writes a decision record naming the items, the disposition, the reason where one is required, and the operator. Every re-rank writes the ranking basis used. A bulk disposition writes a single record covering the batch, with the individual item identifiers enumerated, and with the preview state recorded alongside.

**Operator burden.** The queue's budget is that the operator can rank by the criterion they actually care about without leaving the view, and can disposition the common cases in one action. The view must not require the operator to open an item to decide whether to keep it; the expanded composition is available but not required for disposition. Where the queue length exceeds the operator's working capacity — see §10.7 — the console must not present an unbounded list and rely on scrolling; it must rank, cap, and state that it has capped.

### 6.4 WF-04 — Classification Console

**WF-04 — Classification Console.** The Classification Console presents the assisted classification of a signal set against the AAT taxonomy, with the proposed categories, their rationale, their confidence, and the operator's ability to override, and it records the override as a first-class output.

**Purpose.** Automated classification will be wrong, and the framework's position is that the operator's correction is not a failure of the automation but the mechanism by which the automation improves. The console exists to make the automation's reasoning inspectable and the correction cheap.

**Elements.**

| Element | Type | Refresh behaviour | Data drawn on |
| --- | --- | --- | --- |
| Signal set panel | Panel | On load; on change to the selection | The triage queue's cluster composition |
| Proposed category list | Table | On completion of the classifier | The classifier's output; the AAT taxonomy version in force |
| Rationale panel | Panel per proposed category | With the category | The classifier's stated rationale; the evidence it cites |
| Confidence control | Value with stated range and basis | With the category | The classifier's confidence estimate and its declared basis |
| Override control | Action, with mandatory reason | On demand | The operator's alternative classification and reasoning |
| Taxonomy browser | Reference panel | On demand | The AAT taxonomy, at the version in force |
| Classifier provenance | Key-value | With the proposal | The model and configuration version that produced the classification |

**Interactions.** The operator can accept a proposed category, amend its confidence, override the category to a different one or to several, add a category the automation did not propose, withdraw a proposed category, and record a rationale in their own words. The operator cannot delete the automation's original proposal from the record: the override is layered on top of it, and both are visible.

**Failure and degradation.**

| Source state | Behaviour |
| --- | --- |
| Classifier unavailable | The console shows the signal set with the classification fields empty and explicitly marked as not assessed. It does not fall back to a rule-based guess presented as a classification |
| Classifier partially complete | Completed categories are shown with their own confidence; incomplete fields are marked as pending and the record notes that the proposal was partial |
| Taxonomy version mismatch | The console shows the taxonomy version the classifier used and the version the console holds, and marks the classification as made against a different version |
| Operator override with no rationale | The override cannot be submitted; the rationale field is mandatory, per TAX-4 |

**Audit and record.** Every classification, every confidence amendment and every override writes a record carrying the automation's original proposal, the operator's version, the reason, the taxonomy version, and the classifier's configuration version. The override record is a primary input to classifier improvement and must therefore be retrievable as such.

**Operator burden.** The console's budget is one classification decision per inspection, on a signal set that has already been dispositioned as worth classifying. It must never open automatically on triage, and it must never present more than one classification question at a time, even where the model has proposed several categories at once.

### 6.5 WF-05 — Hypothesis Ladder

**WF-05 — Hypothesis Ladder.** The Hypothesis Ladder presents the operator's working hypotheses, their support, their contradictions, and the disconfirming observation that would settle each one.

**Purpose.** A hypothesis without a disconfirming observation never ends. The Ladder exists to force every proposition the operator is working on to carry the observation that would kill it, and to show, at any moment, how many hypotheses the operator is currently carrying and how well each is supported.

**Elements.**

| Element | Type | Refresh behaviour | Data drawn on |
| --- | --- | --- | --- |
| Ladder of hypotheses | Ordered list, ranked by standing | On change | The hypothesis store; the card's hypothesis field where one exists |
| Support panel | Panel per hypothesis | With the hypothesis | The evidence ledger's claims that support the hypothesis, each with label and tier |
| Contradiction panel | Panel per hypothesis | With the hypothesis | The claims that contradict it; the card's recorded contradiction entries |
| Disconfirming observation field | Text control per hypothesis | With the hypothesis | The hypothesis's declared disconfirming observation |
| Standing indicator | Badge per hypothesis | On change | The hypothesis's status: proposed, supported, contradicted, suspended, retired |
| Confidence dependency | Key-value per hypothesis | With the hypothesis | The assumption panel's dependencies for the claims bearing on the hypothesis |

**Interactions.** The operator can raise a hypothesis, attach and detach evidence, record a contradiction, amend the disconfirming observation, promote a hypothesis onto a card, suspend one, and retire one with a reason. A hypothesis whose disconfirming observation is empty may be raised and carried, but it must be marked as lacking that observation, and any card that adopts it must record the fact.

**Failure and degradation.**

| Source state | Behaviour |
| --- | --- |
| Evidence ledger unavailable | Support and contradiction panels show their contents as unavailable, and each hypothesis is marked as not currently re-evaluated; the Ladder does not display a stale count as a current count |
| Card repository unavailable | Promotion is unavailable and the reason is stated; hypotheses remain editable |
| Conflicting standing data | Where the store and a card disagree about a hypothesis's standing, both are shown and the disagreement is flagged for the error handler |
| Long-lived hypotheses | A hypothesis carried beyond the card's expiry is marked as overdue and is surfaced on the watchboard, since an unbounded hypothesis is a standing assumption in disguise |

**Audit and record.** Every raise, amendment, contradiction, suspension and retirement writes a record. The set of hypotheses in force at the moment of a decision is written into the view-state snapshot, so that a reviewer can reconstruct not only what the operator decided but what the operator believed they were trying to do.

**Operator burden.** The Ladder's burden is proportional to the number of live hypotheses, and the console must therefore make that number visible and must resist the accumulation of propositions. It must offer consolidation, and must not present a long list of equally-weighted hypotheses as though they were a coherent working set.

### 6.6 WF-06 — Card Editor

**WF-06 — Card Editor.** The Card Editor creates and amends Operation Cards, enforces the mandatory fields of the card structure, and shows the diff between revisions so that an amendment is visible as an amendment.

**Purpose.** The card is the instrument of authorisation, and the editor is where the operator's understanding becomes an authorisable artefact. Its obligations are completeness, immutability of what has been approved, and visibility of what has changed since the approval.

**Elements.**

| Element | Type | Refresh behaviour | Data drawn on |
| --- | --- | --- | --- |
| Mandatory field set | Form | On load; re-validated on every edit | The Operation Card template's mandatory fields |
| Field completion state | Indicator per field | On edit | The card's validation state |
| Live ROE gate state | Panel | On every change to an authority or countermeasure field | The policy engine's evaluation of the card as it currently stands |
| Assumption set | Panel | On change | The card's assumption field and the assumption panel's bindings |
| Revision history | List | On change | The card repository's revision chain |
| Diff view | Side-by-side comparison | On demand | Two card revisions and the audit records between them |
| Countermeasure selection summary | Panel | On change | The countermeasure console's selection; the admissibility results |
| Attachments | List of records | On change | Evidence ledger claims referenced by the card |

**Interactions.** The operator can create a card, complete and amend every field, attach and detach evidence claims, record assumptions and their dependencies, submit the card to the approval surface, withdraw it from approval, and view the diff against any prior revision. The operator cannot mark a mandatory field complete without supplying its value, and cannot delete a field that has been populated on an approved revision; they supersede it.

**Failure and degradation.**

| Source state | Behaviour |
| --- | --- |
| Policy engine unreachable | The live ROE gate state is replaced by an explicit statement that admissibility cannot be evaluated at present, the card may still be edited, and the card cannot be submitted for approval |
| Card repository unreachable | Editing is disabled and the card state is marked unavailable; the operator is not permitted to edit against a stale copy, because the edit would be against an unknown base |
| Evidence ledger unreachable | Claims cannot be attached; existing attachments remain visible with their stored labels; the card may not be submitted, because evidence completeness cannot be confirmed |
| Concurrent revision by another operator | The editor shows that the card has been revised elsewhere, presents the diff, and requires an explicit base reconciliation before the edit is applied |

**Audit and record.** Every field change writes a revision with the field, the prior value, the new value, the operator and the time. The diff is derivable from the revision chain without a separate artefact. Submission to the approval surface writes a record naming the exact revision submitted, so that the approval cannot later be read as applying to a different card.

**Operator burden.** The card editor is the heaviest view in the system and is used during preparation, not during crisis. Its burden is therefore a function of preparation time, not of the emergency. The console must support section-by-section completion, must preserve an operator's work between sessions, and must not require the whole card to be visible at once. It must also keep the operator out of fields that are not theirs: the authority fields are populated from the engagement authorisation, and an edit to them is an escalation, not an edit.

### 6.7 WF-07 — ROE Gate

**WF-07 — ROE Gate.** The ROE gate is the hard interlock of the Watchfloor. It displays the rules-of-engagement profile in force, the ceiling that profile imposes, the action requested, the policy engine's verdict on that action, and the margin of exceedance where the action is refused. It blocks what is out of profile, and it says so.

**Purpose.** The gate exists so that the boundary of an operation is visible to the person who would otherwise cross it, and so that crossing it is impossible rather than discouraged. Its behaviour in full is specified in Section 8; this subsection specifies the surface.

**Elements.**

| Element | Type | Refresh behaviour | Data drawn on |
| --- | --- | --- | --- |
| Profile in force | Panel | On load; on change | The engagement authorisation; the card's authority fields |
| Ceiling statement | Key-value | With the profile | The policy engine's profile object: permitted classes, permitted collateral class, permitted autonomy class |
| Requested action | Key-value set | On change to the card | The card's selected countermeasures, their classes, their targets |
| Verdict | Badge, with rule reference | On every evaluation | The policy engine's evaluation result |
| Margin of exceedance | Key-value | On refusal | The policy engine's refusal detail: the rule, the ceiling, the requested value |
| Escalation affordance | Action | On refusal where escalation is available | The escalation console's request template for the required depth |
| Deconfliction verdict | Badge | On evaluation | The deconfliction map's result, per AD-10 |

**Interactions.** The operator can request an evaluation, inspect the rule and margin on refusal, and raise an escalation request from the gate. The operator cannot override the gate, cannot dismiss a refusal, and cannot mark a blocked action as "proceeded anyway" — there is no affordance for it, and the absence of the affordance is itself a control.

**Failure and degradation.**

| Source state | Behaviour |
| --- | --- |
| Policy engine unreachable | The gate displays "cannot evaluate" as a distinct state, blocks the action, and logs the attempt. It does not fall back to a permissive local evaluation (§8.6) |
| Policy engine slow | The action remains blocked while the evaluation is outstanding. The gate shows that an evaluation is in flight and does not display an interim verdict |
| Profile object missing | The gate blocks everything and states that the profile in force cannot be read. There is no implicit default profile |
| Engine returns an unrecognised verdict | The action is blocked and the unrecognised verdict is routed to the error handler. An unknown verdict is not treated as a pass |

**Audit and record.** Every evaluation writes a record: the request, the profile version, the verdict, the rule reference, and the margin where applicable. Every block writes a record that names the rule and the operator's action that was prevented. A record of a block is not an error: it is evidence that the control operated.

**Operator burden.** The gate's burden is a single yes or no that the operator can act on. It must never require the operator to read the ceiling, the margin and the rule in order to know that they are blocked. The verdict must be legible from the badge alone, and the detail must be available for the case where the operator intends to escalate.

### 6.8 WF-08 — Countermeasure Console

**WF-08 — Countermeasure Console.** The Countermeasure Console generates the candidate set, applies the admissibility algebra, ranks the survivors, supports the operator's selection, and presents the rejected set with the specific condition each rejection failed and the value that would have made the countermeasure admissible.

**Purpose.** This is the view where the framework's most consequential analytical act becomes a human choice, and where the requirement that a rejected countermeasure is recorded rather than discarded is discharged. It also exists to make the choice reversible: an operator who selects wrongly should be able to change the selection without penalty.

**Elements.**

| Element | Type | Refresh behaviour | Data drawn on |
| --- | --- | --- | --- |
| Candidate set | Table | On demand; re-evaluated on card change | The countermeasure catalogue, filtered by the card's AAT technique bindings, plus operator proposals |
| Admissibility result column | Key-value per candidate, per AD-1 to AD-12 | With the candidate | The admissibility algebra's evaluation |
| Rejection reason column | Key-value per rejected candidate, per AD-13 | With the candidate | The failed condition and the value that would have made it admissible |
| Ranking column | Value with its components | With the candidate | The risk-adjusted priority P and its three terms |
| Selection control | Action per candidate | On demand | The card's selection field |
| Operator preference field | Text and weight control | On demand | The operator's stated preference, used as the ranking tie-break |
| Effectiveness estimate | Value with confidence, per SCORE-4 | With the candidate | The countermeasure catalogue's effectiveness figure and its confidence |
| Collateral exposure | Key-value | With the candidate | The countermeasure's collateral class and its third-party dependencies |

**Interactions.** The operator can request a candidate set, inspect any candidate's admissibility result condition by condition, accept the system's ranking, override the ranking, select one or more candidates, deselect, change the selection after approval — which writes an amendment and re-runs the gate — and record a reason for a selection that departs from the ranking. The operator cannot select a rejected candidate; the console explains what would have to change and offers to raise an escalation where the change is one the framework permits.

**Failure and degradation.**

| Source state | Behaviour |
| --- | --- |
| Catalogue unavailable | The candidate set is shown as unavailable; the console does not present a truncated catalogue as complete. An operator-proposed countermeasure may still be added by identifier, and is evaluated by the engine |
| Admissibility engine unavailable | No candidate is presented as admissible or inadmissible. The console shows the evaluation as outstanding and blocks selection |
| Scoring model unavailable | The ranking column is marked unavailable and candidates are presented unranked, grouped by class. The operator is told that the ordering is absent rather than arbitrary |
| A countermeasure's metadata is incomplete | The candidate is presented with the missing fields marked, and is flagged as not eligible for selection at a class requiring those fields |

**Audit and record.** The evaluation writes a record containing the full candidate set with each admissibility result, the ranking, the operator's preference, the selection, the reason for any departure from the ranking, and the operator's identity. The record is sufficient to reconstruct the selection without reference to the catalogue's state at the time, which must therefore be captured alongside it.

**Operator burden.** The console's burden is the highest legitimate burden in the system, and it is paid during preparation. Its budget is one selection decision plus, where the operator departs from the ranking, one written sentence explaining why. The console must make the rejected set available without making the operator read it — the rejected set must be present and inspectable, but it must not compete with the surviving candidates for attention.

### 6.9 WF-09 — Deconfliction Map

**WF-09 — Deconfliction Map.** The Deconfliction Map overlays live legitimate operations on the intended effect envelope of a proposed countermeasure, and detects conflicts automatically.

**Purpose.** The deconfliction check is the requirement that a countermeasure not interfere with legitimate activity, and it is the requirement most likely to be satisfied by assertion rather than by computation. The Map exists to make the interference visible geometrically and temporally, and to record the live-operation set the verdict was computed against.

**Elements.**

| Element | Type | Refresh behaviour | Data drawn on |
| --- | --- | --- | --- |
| Live operation layer | Panel | Continuous | The control plane's registry of live legitimate operations |
| Intended effect envelope | Panel | On change to the selection | The selected countermeasure's stated target set and effect |
| Conflict markers | Marker set | On evaluation | The deconfliction service's conflict and near-conflict detection |
| Deconfliction verdict | Badge | On evaluation | The deconfliction result required by AD-10 |
| Operation registry table | Table | Continuous | The control plane's live operation list with owners |
| Time-overlap strip | Timeline | Continuous | The temporal overlap between the intended effect window and live operations |

**Interactions.** The operator can inspect each live operation's owner and purpose, inspect each conflict's nature, request a re-evaluation, and record a justification for proceeding where the verdict is a conflict but the framework permits the operator to proceed with a recorded argument. The operator cannot suppress a conflict; the map shows conflicts whether or not the operator wants to see them.

**Failure and degradation.**

| Source state | Behaviour |
| --- | --- |
| Live operation registry unavailable | The deconfliction verdict is "cannot evaluate" and the check is not satisfied. AD-10 is not met, and the card cannot be dispatched |
| Registry stale | The verdict is computed against the stated registry snapshot and the snapshot's age is shown. A stale registry cannot satisfy AD-10 at dispatch time |
| A conflict is detected | The conflict is marked as a hard conflict or a near-conflict, and the distinction is defined in the console rather than left to the reader |
| The intended effect envelope is undefined for a countermeasure | The countermeasure is not eligible for deconfliction and therefore not eligible for selection |

**Audit and record.** Every evaluation writes the live-operation registry snapshot identifier, the intended effect envelope, the conflicts found, and the verdict. A recorded justification to proceed against a conflict writes the justification as its own decision record, and the justification is written in the operator's words.

**Operator burden.** The Map's burden is one question — does this interfere with anything legitimate — and the answer must be available without the operator having to construct the comparison themselves. The map must therefore show the overlay by default rather than requiring a toggle, and the operator must never be required to reason spatially to determine the verdict.

### 6.10 WF-10 — Escalation Console

**WF-10 — Escalation Console.** The Escalation Console presents the approval chain, the quorum required, the timers running against each pending request, and the queue of requests awaiting a decision.

**Purpose.** Escalation is a deliberate, recorded exception, and the framework treats it as a distinct instrument from ordinary authorisation rather than as a larger version of it. The Console exists to make that distinctness visible: a request that is out of profile is visibly out of profile, is visibly with someone else, and is visibly time-limited.

**Elements.**

| Element | Type | Refresh behaviour | Data drawn on |
| --- | --- | --- | --- |
| Pending request queue | Table | Continuous | The escalation console's request store |
| Chain state diagram | Diagram per request | On change | The approval chain defined for the target profile and collateral class |
| Quorum readout | Key-value per stage | On change | The required and actual approvals at each stage |
| Timer | Countdown per request | Continuous | The request's expiry timer |
| Outstanding names | List per stage | On change | The identities from whom a response is outstanding |
| Decision history | Table | On change | The recorded decisions on prior requests |
| Withdraw control | Action | On demand | The request's lifecycle state |

**Interactions.** The operator can raise a request, attach the card and the reason for escalation, respond where the operator holds a stage, withdraw a request, and read the history of prior requests against the same rule. A response is a recorded act: silence is not a response, and an unanswered timer is displayed as an unanswered timer.

**Failure and degradation.**

| Source state | Behaviour |
| --- | --- |
| Escalation service unavailable | Requests cannot be raised; the console states that escalation is unavailable and does not present an alternative route. There is no informal channel promoted by the interface |
| A request expired | The request is shown as expired, with its expiry time, and the card reverts to the state it held before the request was raised |
| A stage's approver unreachable | The outstanding name is marked as unreachable, with the time since last contact, and the request's timer continues to run |
| Conflicting decisions at the same stage | Both are recorded; the request is routed to the error handler; the console does not silently select one |

**Audit and record.** Every request, every response, every expiry and every withdrawal writes a record. The record names the rule that was exceeded, the depth required, each person who responded and what they said, and the time the request reached its terminal state. The record must show whether the chain completed in order.

**Operator burden.** The console's burden is the cost of waiting, which the framework accepts, and the cost of understanding where a request has stalled. It must therefore make the stall visible and name the person whose action is outstanding. It must not, however, permit the operator to chase the approver through the console, because that pressure is exactly what converts an authorisation into a formality.

### 6.11 WF-11 — Evidence Ledger

**WF-11 — Evidence Ledger.** The Evidence Ledger presents every claim that bears on a decision with its claim label, its source reliability tier, its confidence, its provenance, and its derivation chain, and retains superseded claims rather than overwriting them.

**Purpose.** The evidence ledger is where the framework's claim-labelling discipline becomes an operator's working surface. It exists so that a decision can be checked claim by claim — not so that the operator can adjudicate the labelling in the moment, but so that the labelling is there when the question is asked, including by someone who was not present.

**Elements.**

| Element | Type | Refresh behaviour | Data drawn on |
| --- | --- | --- | --- |
| Claim list | Table | On demand | The evidence store for the card's scope |
| Label column | Badge per claim | With the claim | The claim's label: Fact, Estimate, Interpretation, Hypothesis, Recommendation |
| Tier column | Badge per claim | With the claim | The claim's source reliability tier, 1 to 4 |
| Confidence column | Value with basis | With the claim | The claim's stated confidence and the basis for it |
| Provenance panel | Panel per claim | With the claim | The source, collection time, and transformation history of the claim |
| Derivation chain | Expandable tree per claim | With the claim | The derivation relationships; the weakest input per INT-9 |
| Superseded marker | Badge per claim | With the claim | The claim's supersession state and the claim that replaced it |
| Filter and grouping | Control group | On change | The evidence store's attributes |

**Interactions.** The operator can filter by label, tier, confidence and provenance; inspect a derivation chain; supersede a claim with a reason; and attach a claim to a card. The operator cannot relabel a claim without a reason, and the reason is recorded as a new claim rather than an edit of the old one.

**Failure and degradation.**

| Source state | Behaviour |
| --- | --- |
| Evidence store unavailable | The view shows the claims it holds from the card's frozen bundle with the unavailability stated; it does not display an empty ledger as though the evidence were absent |
| A claim's provenance unavailable | The claim is marked provenance-incomplete and is shown as ineligible to support a decision, per the platform's evidence rules |
| Derivation chain broken | The chain is rendered with the break marked, and the affected claim's confidence is marked as not computable rather than carried forward |
| Confidence withdrawn | The claim's prior confidence is shown struck through and the withdrawal is dated; the claim is retained |

**Audit and record.** Attaching a claim to a card writes a record with the claim's identifier and its label and tier at the time of attachment, so that a later reclassification does not retrospectively alter what the approver saw. Supersession writes a record linking the superseded claim to its replacement. The evidence ledger view-state is captured in the snapshot for every decision taken against it.

**Operator burden.** The ledger's burden is deferred by design: the operator should not need to work in it during an incident. Its obligation is to be complete and inspectable in ten minutes, so that an approval under time pressure is informed by claims whose labels and tiers are visible without opening anything.

### 6.12 WF-12 — Assumption Panel

**WF-12 — Assumption Panel.** The Assumption Panel lists every assumption behind a current card together with the confidence of each claim that depends upon it, so that the cost of an assumption being wrong is visible rather than latent.

**Purpose.** Assumptions are the most consequential and least visible part of any assessment: the decision is correct given the assumptions, and the assumptions are rarely examined. The Panel makes the dependency structure of a card explicit, and it makes the failure of an assumption a thing the console can anticipate rather than discover afterwards.

**Elements.**

| Element | Type | Refresh behaviour | Data drawn on |
| --- | --- | --- | --- |
| Assumption list | Table | On change to the card | The card's assumption field |
| Dependent claims column | List per assumption | On change | The evidence ledger's claims that rest on the assumption |
| Dependent confidence column | Value per dependent claim | On change | The confidence of each dependent claim, per INT-9 |
| Derivation penalty | Key-value per dependent claim | On change | The declared penalty for the derivation, per INT-9 |
| Assumption status | Badge per assumption | On change | Stated, contested, withdrawn, confirmed |
| Impact statement | Text per assumption | With the assumption | What the card concludes if the assumption is false |

**Interactions.** The operator can add an assumption, state its basis, link it to dependent claims, amend its status, and record the effect of its being false. The operator cannot delete an assumption that a dependent claim rests upon; they withdraw it, which is recorded, and the dependent claims' confidences are recomputed.

**Failure and degradation.**

| Source state | Behaviour |
| --- | --- |
| Evidence ledger unavailable | Dependent claims cannot be listed; the assumption is shown with its dependency set marked unavailable, and the panel states that the dependency structure is not currently verifiable |
| A confidence recomputation fails | The panel shows the last computed value with the failure stated, and marks it as not current. It does not retain the value silently |
| An assumption has no dependent claims | It is shown, and it is marked as not currently load-bearing, which is itself information worth displaying |
| Many assumptions carry one claim | The card's fragility is concentrated in a single proposition; the panel must show the count of dependent claims per assumption so that concentration is visible |

**Audit and record.** Every assumption, amendment, withdrawal and status change writes a record, together with the confidence values recomputed as a consequence. The set of assumptions in force, and the dependent confidence values at that moment, are captured in the card's view-state snapshot for each decision.

**Operator burden.** The panel is an inspection surface for a prepared card and a mandatory element of the approval surface. Its burden is a count and a list, not an analysis: the operator must be able to see how many assumptions the card rests on and which claims are most exposed, without performing any calculation.

### 6.13 WF-13 — Autonomy Monitor

**WF-13 — Autonomy Monitor.** The Autonomy Monitor displays autonomy budget consumption, the envelope within which it may be spent, the expiry, and the reversion trigger, live and continuously, while an operation runs.

**Purpose.** Bounded autonomy is the framework's answer to the question of how much the system may do without a human in the loop, and the answer is only meaningful if the human can see the bound being approached. The Monitor exists to make the consumption of an authority visible to the person who granted it, at the moment the consumption happens rather than afterwards.

**Elements.**

| Element | Type | Refresh behaviour | Data drawn on |
| --- | --- | --- | --- |
| Budget gauge | Gauge, with consumption and remaining | Continuous | The control plane's autonomy counters |
| Envelope boundary list | Key-value set | On change | The card's declared envelope |
| Expiry countdown | Countdown | Continuous | The autonomy grant's expiry |
| Reversion trigger state | Badge with the trigger's condition | Continuous | The card's abort list and the platform's evaluation of it |
| Action log | Table | Continuous | The actions taken under the grant, in order |
| Budget forecast | Sparkline | Periodic | The consumption rate against the remaining budget |

**Interactions.** The operator can inspect what has been spent and on what, extend the budget where the framework permits it, narrow the envelope, and trigger reversion manually. The operator cannot increase the budget beyond the card's declared ceiling, and cannot extend the expiry past the engagement authorisation's expiry.

**Failure and degradation.**

| Source state | Behaviour |
| --- | --- |
| Control plane unreachable | The Monitor cannot display consumption. It states that the operation's state is unknown and that the reversion condition cannot currently be evaluated, and it treats this as a reversion condition in its own right, per HITL-5 |
| A budget action is rejected by the envelope | The action is refused by the control plane and the refusal is displayed with the boundary that was reached, because a refusal at the envelope is information about a mis-specified envelope |
| The consumption rate exceeds the forecast | The monitor raises a warning before the budget is exhausted, rather than at exhaustion |
| Reversion has already occurred | The monitor shows the reversion, its cause, its time, and the notification that accompanied it, and the interface does not present the operation as still running |

**Audit and record.** Every action taken under the grant writes a record in the control plane's action log, referenced from the monitor's view-state. Every budget extension, envelope narrowing and manual reversion writes a decision record naming the operator and the reason. The reversion event, whether automatic or manual, writes a record naming the condition that caused it.

**Operator burden.** The monitor's burden during a live operation is deliberately close to zero: it is read, not worked. It must therefore be legible at a glance and must not require interaction. Its budget is a glance, in which the operator takes in the remaining budget, the expiry, and whether the reversion trigger has fired.

### 6.14 WF-14 — Telemetry and Health

**WF-14 — Telemetry and Health.** The Telemetry view presents the liveness of every source, the degraded and unreached sources, the ingest lag, and the cues that distinguish a source that is healthy and reporting nothing from a source that has stopped reporting.

**Purpose.** Detection coverage is a function of telemetry, and telemetry fails quietly. This view exists so that the operator can distinguish silence from absence, and so that a gap in the picture is noticed before a decision is taken on the picture. It is a health surface for the evidence, not a health surface for the software.

**Elements.**

| Element | Type | Refresh behaviour | Data drawn on |
| --- | --- | --- | --- |
| Source liveness table | Table | Continuous | The sensor and collector layer's heartbeats |
| Integrity state column | Badge per source | Continuous | The ingest service's integrity determination |
| Fidelity column | Badge per source | Continuous | Each source's reported fidelity |
| Ingest lag | Value per source, with age | Continuous | The ingest service's lag measurement |
| Silence window readout | Key-value per source | Continuous | The configured silence window; the last successful contact |
| Silent-failure cues | Panel | Continuous | The ingest service's gap, stall and sequence-break detections |
| Degraded-source impact list | Table | On change | The dependency map from source to derived claims |

**Interactions.** The operator can inspect any source's health history, jump to the signals that source produced, see which derived claims depend on it, and mark a source's silence as known or as a fault to be chased. The operator cannot suppress a health alert from this view; health alerts are deferred by the alerting mechanism in §10.8, not removed here.

**Failure and degradation.**

| Source state | Behaviour |
| --- | --- |
| The telemetry view's own data source down | The view states that it cannot currently report source health and displays the last known state with its age. It must never present a stale liveness table as current |
| A source silent beyond its window | The source is marked silent, with the elapsed time, and a silent-failure cue is raised. Silence is presented as an event, not as an empty row |
| A source's heartbeats arrive but its content does not | The source is marked degraded rather than healthy, because liveness without content is a distinct failure |
| A source reports at reduced fidelity | The source's fidelity column shows the reduction, and the dependent claims table lists what is affected |

**Audit and record.** View-state snapshots on entry and exit. The marking of a silence as known or as a fault writes a record with the source, the operator and the reason. The view's state hash is written with each snapshot, so that the health picture at the moment of a decision is provable.

**Operator burden.** The telemetry view is consulted when something looks wrong, and it must be legible as a single question: is the picture complete? Its budget is a scan for the count of unhealthy sources. It must therefore lead with counts rather than with a long table, and it must never be the landing view.

### 6.15 WF-15 — Abort and Recall

**WF-15 — Abort and Recall.** The Abort and Recall capability provides a single, prominent, always-available termination of any running operation, together with the capture of the reason for the termination.

**Purpose.** The framework requires that a human can stop an operation in real time and that the ability to do so be demonstrated before the operation begins. This capability is that demonstration. It is the only control in the Watchfloor that is always visible, that is never disabled, and that has no confirmation step.

**Elements.**

| Element | Type | Refresh behaviour | Data drawn on |
| --- | --- | --- | --- |
| Abort control | Action, persistent | Always resident; state updates on change | The control plane's running-operation registry |
| Running operations list | Table | Continuous | The control plane's live operation state |
| Reason capture | Dialog, invoked by the abort action | On demand | The operator's stated reason, with a required minimum substance |
| Recall control | Action per recently terminated operation | On change | The control plane's recall capability and its preconditions |
| Abort channel health | Badge | Continuous | The abort channel's own health, per HITL-3 |
| Post-abort state summary | Panel | After an abort | The resulting posture, autonomy state and notification record |

**Interactions.** The operator can abort a specific running operation, or abort everything in the affected card. The abort is a single action with no confirmation. The reason capture is invoked by the abort and does not delay it: the operation is halted first and the reason is captured immediately afterwards, and the abort completes even if the operator closes the reason dialog without writing one — the absence of a reason is itself recorded as "no reason given". The operator can invoke a recall where the framework permits it, and can read the state of the operation after the abort.

**Failure and degradation.**

| Source state | Behaviour |
| --- | --- |
| Control plane unreachable | The abort control remains enabled and visible. The console shows that the abort could not be confirmed and raises the notification channel. It must never disable the control because the state is unknown; an operator must never be left unable to try to stop something |
| Abort channel degraded | The abort control is marked as operating in degraded mode, with what that means for the abort's effect, and remains enabled |
| The reason dialog fails to open | The abort proceeds; the reason is captured afterwards from the notification channel |
| Multiple operations running under one card | The abort dialog's selector is not used: the abort affects the card's operations, and the operator may refine the scope afterwards through recall |

**Audit and record.** The abort writes a record immediately: the operation, the operator, the time, the reason or its absence, the resulting posture and the resulting autonomy state. The record is written even where the abort could not be confirmed, in which case the record states the failure and the notification that followed. An abort is never silent.

**Operator burden.** Zero by design. The abort costs one action and no reading, and it must remain that way under every state of the console. Any design change that adds a step, a confirmation, or a precondition to the abort fails this capability.

### 6.16 WF-16 — Replay and Timeline

**WF-16 — Replay and Timeline.** The Replay view reconstructs any operation from the Ledger, with the world state at each step, so that a reviewer who was not present can follow what was known, what was decided, and in what order.

**Purpose.** The framework's central claim is that every consequential decision is reconstructible. This view is where that claim is either honoured or found to be false, and it is therefore a view that must be built to serve an adversary of the decision as well as its defender — a reviewer looking for the moment where the assessment went wrong, not a reader looking for a narrative.

**Elements.**

| Element | Type | Refresh behaviour | Data drawn on |
| --- | --- | --- | --- |
| Operation timeline | Timeline | On demand | The Ledger's entries for the operation |
| Step detail panel | Panel per step | On selection | The Ledger entry, the referenced card revision, and the referenced view snapshot |
| World state panel | Panel per step | On selection | The world model as recorded at that step |
| Decision record panel | Panel per decision | On selection | The decision record: options, choice, reason, authority, confidence, contingency |
| Evidence panel | Panel per decision | On selection | The claims in force at that moment, with labels and tiers |
| Chain verification readout | Badge | On load | The Ledger's hash-chain verification state |
| Gap marker | Marker within the timeline | On load | Any break, retraction, or missing record detected in the chain |

**Interactions.** The reviewer can step through the sequence, filter it to decisions, compare the world model at two steps, and export the reconstruction. The reviewer can switch between the reconstructed state and the contemporaneous records, and the view must not smooth over a discrepancy: where the reconstruction differs from what was recorded at the time, both are shown.

**Failure and degradation.**

| Source state | Behaviour |
| --- | --- |
| Ledger unavailable | The view states that the reconstruction cannot be produced and does not present a partial reconstruction as complete |
| Chain verification fails | The failure is displayed prominently at the top of the view, the break is marked in the timeline, and the affected steps are marked as not independently verifiable |
| A referenced snapshot is missing | The step is shown with the missing state named, and the step's verifiability is reduced accordingly. The step is not omitted |
| A card revision is missing | The step shows the record without the card, with the discrepancy stated |

**Audit and record.** The view writes a record of every replay session: the operation replayed, the reviewer, the filters applied, and the export produced. Replaying is an inspection of the record and must not itself alter it.

**Operator burden.** The view is used after the fact, by a reviewer with time. Its burden is therefore comprehension, not time. It may be dense. It must, however, remain usable by someone who has never seen the operation, which means it must supply the sequence and the state rather than assume the reader knows what the steps were.

### 6.17 WF-17 — Exercise Analytics

**WF-17 — Exercise Analytics.** The Exercise Analytics view reports detection coverage against the taxonomy, the cost of false positives, the measured detection and response intervals, and the gap list.

**Purpose.** The framework requires that the system's performance be measured and reported rather than asserted, and that coverage be assessed against the taxonomy rather than described in prose. This view is the instrument of that requirement, and its honesty is the point: a coverage figure without its denominator, or an interval without the exercise that produced it, is worse than no figure, because it invites reliance.

**Elements.**

| Element | Type | Refresh behaviour | Data drawn on |
| --- | --- | --- | --- |
| Coverage matrix | Table by AAT category | On demand | Detection coverage results from completed exercises |
| Coverage denominator panel | Panel | With the matrix | The exercise set and its scope that the coverage is computed over |
| False-positive cost table | Table | On demand | The recorded cost of false positives per exercise |
| Interval measurements | Table with the exercise reference | On demand | Measured detection and response intervals, each with its source exercise |
| Gap list | Table | On demand | The detection-gap feedback accumulated from after-action reports |
| Exercise selector | Selector | On change | The exercise inventory |

**Interactions.** The operator can select an exercise or an exercise set, inspect the coverage computation, drill into a category to see which techniques were exercised and which were not, and export the gap list into the after-action process. The operator cannot edit a measurement from this view.

**Failure and degradation.**

| Source state | Behaviour |
| --- | --- |
| No exercises completed | The view states that no measurement exists, and shows the taxonomy as entirely uncovered by measurement rather than as covered by default |
| Exercise results partially available | The coverage is computed over the exercises available and the denominator panel states which exercises are missing from the computation |
| Measurement collection failed during an exercise | The affected exercise is excluded from the computation and named in the denominator panel; it is not silently counted as a non-detection |
| Coverage figures from an old taxonomy version | The view shows the taxonomy version the measurement was made against and marks the coverage as not comparable with the version in force |

**Audit and record.** The view writes a record of each export and each drill-through performed. The measurement data itself is not editable from the console, and its integrity is verified through the Ledger.

**Operator burden.** The view is used at review cadence, not during an incident. Its burden is that the gaps must be read and acted upon, and the console must therefore make the gap list actionable rather than merely visible: a gap that cannot be opened into the detection engineering process is a report, not a control.

### 6.18 WF-18 — Proving Ground

**WF-18 — Proving Ground.** The Proving Ground simulates an adversary so that detection can be validated and operators can be rehearsed, within an exercise harness that is explicitly separated from field telemetry.

**Purpose.** The Proving Ground is where the framework tests itself without exposing the operator's estate. It serves two purposes that the console must keep visibly distinct: validating that a detection works, and rehearsing an operator. A view that conflates the two produces rehearsal that mistakes a scripted success for a capability.

**Elements.**

| Element | Type | Refresh behaviour | Data drawn on |
| --- | --- | --- | --- |
| Exercise selector and state | Panel | On load | The exercise inventory; the harness's session state |
| Scenario panel | Panel | On load | The scenario definition, its injects, and its success criteria |
| Adversary behaviour view | Panel | Continuous during the exercise | The simulated adversary's actions as the harness generates them |
| Detection event stream | Table | Continuous | The detectors' responses during the exercise |
| Operator task panel | List | On load | The rehearsal tasks and the operator's performance against them |
| Scoring rubric | Panel | On demand | The rubric from the exercise pack |
| Separation indicator | Badge | Continuous | The harness's isolation state, confirming no field telemetry is affected |

**Interactions.** The operator can select and start an exercise, observe it, respond to the rehearsal tasks, end the exercise, and review the scoring. The operator cannot import field telemetry into the harness, and cannot export harness artefacts into the field pipeline.

**Failure and degradation.**

| Source state | Behaviour |
| --- | --- |
| Harness unavailable | The view states that the proving ground is unavailable; exercises cannot be started |
| Exercise running with a missing detector | The exercise continues and the missing detector is marked as absent, so that a non-detection in that area is not read as a failure of the detector |
| Operator abandons the exercise | The partial performance data is retained and marked incomplete, and the rubric is not scored as though the exercise were completed |
| Isolation cannot be confirmed | The exercise does not start. The separation indicator is not a report; it is a precondition |

**Audit and record.** The exercise session, its injects, the operator's responses and its scoring are recorded. The separation state at start and at end is recorded. Exercise results feed the after-action process and the gap list.

**Operator burden.** The burden is the exercise's own. The console's obligation is to make the distinction between rehearsal performance and field capability unmistakable in the record, so that a rehearsal score is never quoted later as a detection rate.

### 6.19 WF-19 — Doctrine Editor

**WF-19 — Doctrine Editor.** The Doctrine Editor authors, versions and publishes the policy set itself: the thresholds, weights and rules by which the policy engine judges.

**Purpose.** The rules that bind the system are themselves a policy, and a policy that can be changed silently by an operator is not a policy. The Editor exists so that doctrine is changed deliberately, versioned, published with an effect, and reviewed against the operations it would have decided differently.

**Elements.**

| Element | Type | Refresh behaviour | Data drawn on |
| --- | --- | --- | --- |
| Doctrine version list | Table | On change | The doctrine repository |
| Rule editor | Form | On load | The doctrine repository's rule set |
| Staged-versus-in-force diff | Comparison panel | On change | The staged version and the version in force |
| Affected rules panel | Table | On change | The rules whose evaluation would change under the staged version |
| Affected cards list | Table | On change | The open cards whose admissibility would change under the staged version |
| Publication control | Action | On demand | The doctrine repository's publication interface |
| Change history | Table | On change | The doctrine change log with its authors |

**Interactions.** The administrator can edit a rule, stage the change, see the diff against the version in force, see which rules and which open cards would be affected, publish the change with a recorded rationale, and roll back to a prior version with a recorded reason. The administrator cannot publish without a rationale, and cannot publish a change that would affect an open card without the affected card being named in the confirmation.

**Failure and degradation.**

| Source state | Behaviour |
| --- | --- |
| Doctrine repository unreachable | Editing is disabled and the version in force is displayed with its identifier and age |
| Policy engine running a different version | The mismatch is displayed prominently, and the editor must not present a staged change as though it were being applied to the engine in force |
| A rule has never been exercised | The rule is marked as unexercised, with the note that its behaviour is untested in practice |
| Publication partially fails | The publication does not take effect; the staged version remains staged and the failure is recorded |

**Audit and record.** Every edit, stage, publication and rollback writes a record with the author, the rationale, the affected rules and the affected cards. The published doctrine version identifier is written into every card and every decision record created while it is in force, so that a decision can be evaluated against the rules that were actually applied.

**Operator burden.** The editor is used rarely and by a small number of people. Its burden is that a doctrine change is consequential and slow, and the console should make it feel consequential rather than convenient. The affected-cards list is the principal mechanism for that.

### 6.20 WF-20 — Reporting

**WF-20 — Reporting.** The Reporting view generates the after-action report from the Ledger, with the metrics and the gap list, and states the verification status of everything it reports.

**Purpose.** Reporting is the framework's discharge of accountability upwards, and it is where the framework's honesty is most easily lost: a report that is easier to write than the record it draws from will eventually be written from memory. This view exists to make the report a derivative of the Ledger rather than a narrative written afterwards.

**Elements.**

| Element | Type | Refresh behaviour | Data drawn on |
| --- | --- | --- | --- |
| Report builder | Form | On load | The after-action report template's required sections |
| Source record list | Table | On demand | The Ledger entries the report will draw on, with their identifiers |
| Metric panel | Table | On recompute | The measurement values, each with its derivation and its exercise or record reference |
| Gap list panel | Table | On demand | The accumulated detection-gap feedback |
| Verification status panel | Panel | On recompute | The verification status of each reported claim |
| Export and file control | Action group | On demand | The report output controls |

**Interactions.** The operator selects the operation, the reporting period and the required sections; the console assembles the report from the records; the operator may add narrative commentary, which is recorded as commentary distinct from the derived content; and the operator may generate the report, export it and file it. The operator cannot edit a derived figure: a corrected figure is corrected at source, in the record, and the report recomputes.

**Failure and degradation.**

| Source state | Behaviour |
| --- | --- |
| Ledger unavailable | The report cannot be generated. The view states that the report is unavailable rather than producing a report from cached content |
| Ledger incomplete | The report is generated with an explicit completeness statement, the missing records named, and the affected sections marked as incomplete |
| A metric's derivation unavailable | The metric is reported as not computable, with the reason, and is excluded from any summary aggregate |
| Export destination unavailable | The report is retained in the console with a statement that it has not been filed, and the operator is not told that filing succeeded |

**Audit and record.** The report generation writes a record identifying the source records, the reporting period, the version of the template used and the operator. The report itself carries its own verification status and the identifier of the records it was built from.

**Operator burden.** The burden is the operator's honest narrative. The console must make the derived material free — automatically assembled, never retyped — so that the only thing the operator writes is the part that requires judgement.

### 6.21 WF-21 — Audit Export

**WF-21 — Audit Export.** The Audit Export produces a signed, independently verifiable bundle of the Ledger, the cards and their associated records, for a reviewer who was not present and who may not have access to the platform.

**Purpose.** The framework's claim of reconstructibility is a claim about the outside world: that a reviewer can check it. That claim is only testable through an export that leaves the platform's trust boundary, is self-contained, and can be verified without the platform's cooperation.

**Elements.**

| Element | Type | Refresh behaviour | Data drawn on |
| --- | --- | --- | --- |
| Export scope selector | Control group | On load | The Ledger segments, cards and records available for export |
| Manifest panel | Table | On generation | The artefacts included, each with its hash |
| Chain verification readout | Badge | On generation | The hash-chain verification result for the exported segment |
| Signature panel | Panel | On generation | The signing status and the verification instructions |
| Completeness statement | Panel | On generation | What the export does and does not contain |
| Export progress and integrity panel | Panel | During generation | The progress and the integrity state of the export in flight |
| Verification instructions | Document panel | On generation | The procedure for an independent party to verify the bundle |

**Interactions.** The operator selects the scope, generates the export, and observes the manifest and verification state. The export is written to a location the operator specifies and is accompanied by the verification instructions. Where the export is to be released outside the organisation, the console must record the release and the recipient.

**Failure and degradation.**

| Source state | Behaviour |
| --- | --- |
| Ledger partially unavailable | The export proceeds for the available segment with an explicit completeness statement, and the manifest marks the missing range. A partial export is permitted; an unmarked partial export is not |
| Chain verification fails | The export is still produced, with the verification failure displayed at the top of the bundle and marked in the manifest. The failure must not be withheld |
| Signing service unavailable | The export is produced unsigned and is clearly marked as such, with the reason. An unsigned export must not be presented as satisfying the signature requirement |
| Export destination unwritable | The export is not produced; the console states the failure and leaves the ledger untouched |

**Audit and record.** The export event writes a record: the scope, the manifest hash, the chain verification state, the signature state, the destination, the operator and the time. Any external release writes a further record naming the recipient.

**Operator burden.** The burden is one selection and one confirmation of the destination. The console must make the completeness statement legible in that moment, because a reviewer who receives an incomplete bundle without knowing it is incomplete will draw the wrong conclusion.

---

## 7. The Approval Surface

### 7.1 The rule

The approval surface is the most important screen in the Watchfloor, and it is the screen on which the framework's central control — human authority over consequential decisions — either exists or does not. Master design `HITL-2` requires that human authority be substantive rather than procedural: the approver must be able to change the decision. `WFC-3` requires the same of the interface: an approver who has to assemble context from other screens has not been given a real choice.

The rule that follows is therefore absolute and admits of no exception:

**No information necessary to the decision may be behind a disclosure control, on another screen, or retrievable only by navigating away from the approval surface.**

This includes information that is "obviously known", information that is "in the evidence ledger", information that "the countermeasure console shows", and information that "was on the previous screen". If the approver needs it, it is on the surface. If they need to leave the surface to obtain it, the surface has failed.

### 7.2 What must be on the surface

The following must be present on the approval surface at the moment the approval control is presented. Each is assembled server-side into a single bundle before the surface is rendered, so that the approver never sees a partially populated decision.

| # | Element | Content | Source |
| --- | --- | --- | --- |
| 1 | The evidence | The claims the action rests upon, each with its claim label, source reliability tier, confidence and provenance | Evidence ledger, per WF-11 |
| 2 | The classification | The AAT categories and techniques the evidence supports, with rationale, confidence, and the taxonomy version | Classification console, per WF-04 |
| 3 | The attribution assessment | The candidate distribution, the stated confidence, and the alternatives considered | The card's attribution assessment |
| 4 | The attribution basis | The specific basis for the attribution — behavioural signature, infrastructure overlap, capability and timing correlation, operator TTP overlap, infrastructure artefact — with the reliability tier of each basis | Per `INT-2` |
| 5 | The threat score, components exposed | L, I, A and V individually, each with its own reasoning, and the resulting S and S_eff | Scoring model, per SCORE-2 |
| 6 | The full candidate set | Every candidate, including the rejected set, each with the specific admissibility condition it failed and the value that would have made it admissible | Countermeasure console, per WF-08 and AD-13 |
| 7 | The selected countermeasure's metadata | Class, collateral class, reversibility, autonomy class, preconditions, failure modes, attribution dependency, effectiveness estimate and its confidence, third-party dependencies | Countermeasure catalogue |
| 8 | Residual risk before | R computed on the current card with no countermeasure applied | Scoring model |
| 9 | Residual risk after | R recomputed for the selected set, with the expected effectiveness used and its confidence | Scoring model, per SCORE-4 |
| 10 | The risk of inaction | The assessed risk of not acting, stated with its own basis, alongside the risk of acting | Per `OP-4` |
| 11 | Collateral exposure | The countermeasure's collateral class, the identified third-party dependencies, and the shared-tenancy assessment | Per `AUTH-8` and `ROE-6` |
| 12 | The abort conditions | The specific conditions under which the operation will be terminated, the mechanism, and the owner | The card's abort field; never empty |
| 13 | The expiry | The card's expiry, the engagement authorisation's expiry, the autonomy grant's expiry, and the earliest of them | Per `OP-3` and `AUTH-3` |
| 14 | The autonomy envelope | The boundaries within which the system may act without further approval, the budget, and the reversion trigger | Per `DO-9` and `HITL-5` |
| 15 | The deconfliction result | The verdict, the live-operation set it was computed against, and any conflict with its justification | Per `AD-10` and WF-09 |
| 16 | The authority relied upon | The engagement authorisation reference, the ROE profile in force, the ceiling, the required approval depth, and the identity of the named authorities | Constitutional documents |
| 17 | The gate's verdict | The policy engine's assessment of the selected action, with its rule reference and, where refused, the margin of exceedance | Per WF-07 and §8 |
| 18 | The consequences | What will happen, to the estate, to third parties, and to the adversary, if the decision is taken | §7.4 |

**The surface may also contain** the card's objective, hypothesis, disconfirming observation, assumptions and their dependent confidences, the operator's recorded reasoning and departure from the ranking, the existing dissent, and the notification channel's assessment of urgency.

### 7.3 The required reading confirmation

The approval control is not enabled by the approver's presence alone. The approver must make an explicit act of confirmation, and that act is recorded.

| Element | Requirement |
| --- | --- |
| Confirmation form | A statement, in plain language, of what is being authorised, naming the selected countermeasure, the collateral class, and the expiry |
| Evidence acknowledgement | A confirmation that the evidence set was displayed. The console must not ask the approver to certify that they read or understood it; that is not a thing an interface can verify, and asking for it invites a false attestation |
| Consequence acknowledgement | A confirmation that the stated consequences, the residual risk and the risk of inaction were displayed |
| Scope confirmation | A confirmation that the authorisation is bounded by the named envelope and the stated expiry, and that it does not extend beyond them |
| Reversibility acknowledgement | Where the selected countermeasure is not fully reversible, a confirmation that the irreversible elements were considered and that the reversible alternative was assessed, per `ROE-7` |
| Identity binding | The approving identity, the session role, and the time, captured on the act of confirmation |

**WF-A1 — The confirmation is an act, not a state.** The approval control is enabled only when the confirmation form has been completed in full. A control that is merely clickable is not a control under this document.

### 7.4 The consequences of the decision

The consequences block states what the decision does, in the operator's and the approver's terms. It is not a summary of the card; it is a statement of effects.

| Consequence class | Content |
| --- | --- |
| Effect on the operator's estate | What will change on the estate, and what will remain exposed |
| Effect on third parties | Named third parties who may be affected, and the nature and expected duration of the effect |
| Effect on the adversary | What the adversary will observe and what it may infer, where that is known |
| Loss of the status quo | What the operator gives up by acting, including continued exposure |
| Loss of the opportunity | What the operator gives up by not acting, including the loss of the ability to act later without further authorisation |
| Reversibility | Whether the action can be undone, by whom, and within what period |
| Detection of the action itself | Whether the operation's existence is observable, to whom, and what the framework requires to be disclosed |
| Expiry consequence | What happens at expiry, and what happens if the card is not renewed |

### 7.5 Amending and rejecting

**WF-A2 — Amendment, not acceptance-only.** The approver must be able to amend the proposed action rather than accept or reject it as a whole. The minimum amendable set is the selection among candidates, the proposed rationale, the envelope, the budget and the expiry. An amendment re-runs the policy gate before it can be confirmed, and the resulting surface is re-rendered with the amendment applied.

**WF-A3 — Rejection carries a required reason.** The approver may reject the proposal. A reason is required, and the reason is recorded with the rejection. The console must offer reason categories for speed and must accept free text; it must not require the approver to compose an essay before the rejection can be submitted.

**WF-A4 — Deferral is distinct from rejection.** The approver may defer a request, indicating that they will respond before expiry. A deferral is recorded as a deferral, with the time, and it does not authorise anything.

**WF-A5 — A failed confirmation is recorded.** Where an approver attempts to confirm with an incomplete form, the attempt is recorded with the fields that were incomplete. This is evidence about the interface's behaviour under pressure, and it is more useful than a silent rejection.

### 7.6 The audit record produced

The approval produces a decision record containing, at minimum:

| Field | Content |
| --- | --- |
| Identity and role | The approving identity, the session identifier, and the role held |
| Time | The instant of confirmation, and the elapsed time the approval surface was open |
| The subject | The card identifier and the exact revision approved |
| The evidence set | The identifiers of every claim displayed, with their labels and tiers as displayed |
| The classification and attribution | As displayed, including the confidence and the basis |
| The score components | L, I, A, V, S and S_eff as displayed |
| The candidate set | Every candidate displayed, with its admissibility result, and the selection as amended |
| The risk | Residual risk before and after, the risk of inaction, and the collateral exposure, as displayed |
| The gate verdict | The engine's verdict and rule reference |
| The deconfliction result | As displayed, including the registry snapshot |
| The authority | The engagement authorisation, the profile, the ceiling, and the approval depth |
| The envelope and expiry | As displayed |
| The abort conditions | As displayed |
| The confirmation | The completed confirmation form in full, including the free text of each acknowledgement |
| The reason | The approver's stated reason, in their words, whether they accepted, amended or rejected |
| The dissent | Any dissent recorded during preparation |
| The view snapshot | The identifier of the rendered approval-surface snapshot, so that the exact surface displayed is reconstructible |

**WF-A6 — The snapshot is part of the approval.** The approval record must reference a snapshot of the surface as rendered. An approval that cannot be shown what was on screen is an approval that cannot be audited, and the framework's reconstructibility claim does not extend to decisions that lack it.

### 7.7 What the approver sees, does not see, and is not asked to retrieve

| The approver sees | The approver does not see | The approver must not be asked to retrieve from elsewhere |
| --- | --- | --- |
| The evidence with labels, tiers, confidence and provenance | The raw adversary payloads, rendered executably, behind the evidence | Any claim's label, tier or confidence |
| The classification with rationale and taxonomy version | The classifier's internal prompt or configuration | The rationale for a classification |
| The attribution assessment, its confidence and its basis | The analyst's private working notes | The attribution basis |
| The threat score with L, I, A and V exposed | A single unexposed score | Any score component or its reasoning |
| The full candidate set with per-candidate admissibility results | The countermeasure catalogue's full text | Any rejected candidate or its reason |
| The selected countermeasure's metadata and its effectiveness confidence | Prejudgements about which candidate the system prefers | The selected countermeasure's properties |
| Residual risk before and after | A single risk figure | Either residual risk figure |
| The risk of inaction | A risk of acting stated without the alternative | The risk of inaction |
| The collateral exposure and the shared-tenancy assessment | A reassurance that there is no collateral risk | The collateral exposure |
| The abort conditions, mechanism and owner | An empty abort field | The abort conditions |
| The expiry, the earliest of the three expiries | A single undifferentiated expiry date | Any expiry |
| The autonomy envelope, budget and reversion trigger | The budget without the envelope | The envelope or the reversion trigger |
| The deconfliction result and the registry it was computed against | A bare "no conflict" assertion | The deconfliction result |
| The authority, the profile, the ceiling and the depth | A statement that the action is authorised | The authority relied upon |
| The gate's verdict, rule reference and margin | A bare pass or fail | The rule and the margin |
| The consequences, in the form of §7.4 | A reassurance that the consequences are acceptable | The consequences |
| The assumptions and the confidence of their dependents | An assumption that is load-bearing but unstated | The assumptions |
| The operator's reasoning and any dissent | The operator's private notes | The reasoning or the dissent |
| The time elapsed since the surface opened | — | — |

**WF-A7 — Nothing necessary to the decision is withheld.** Where an item in the second column would change the decision, it belongs in the first column. The second column lists what may be withheld because it does not bear on the decision; it does not licence withholding anything that does.

### 7.8 Constraints on the surface

| Constraint | Requirement |
| --- | --- |
| Assembly | The surface is assembled from a server-side bundle. The approver never sees a partially populated decision, and the approval control is not enabled until the bundle is complete and the gate has evaluated |
| No disclosure control | No element of §7.2 may be collapsed, hidden, truncated without expansion, or placed behind a hover or a drawer |
| No navigation away | The surface does not require navigation to another view for any required element. Where an element is available elsewhere in the console, the copy on the surface is authoritative for that decision |
| Scroll is permitted, navigation is not | A long surface may be scrolled. The approver must not be able to lose the approval control, the gate verdict, the expiry, or the abort conditions by scrolling |
| No auto-approval | Nothing on the surface acts on the approver's behalf. There is no timeout, no unattended confirmation, and no automation of the confirming act (`WF-30`) |
| Independence of the approver | Where the framework requires a second reviewer, the console must make it visible that a second approval is outstanding and must not let the first approver's confirmation stand in for it |
| Fidelity of the record | The snapshot written to the Ledger must be of the same content that was rendered, in the same order, with the same labels |

---

## 8. Interlock Semantics

### 8.1 What the gate reads

The ROE gate evaluates a proposed action against the profile in force. It reads, as a minimum:

| Input | Source | Use |
| --- | --- | --- |
| The ROE profile in force | The engagement authorisation, as carried on the card | The ceiling: permitted classes, permitted collateral class, permitted autonomy class, permitted target scope |
| The proposed action | The card's selected countermeasures, their class, collateral class, reversibility, autonomy class and target set | The object of the evaluation |
| The card's bounds | The card's target set, collateral ceiling, required reversibility, minimum effectiveness confidence, autonomy class and budget | The card-local bounds in `AD-2` to `AD-11` |
| The attribution confidence | The card's attribution assessment | Whether the countermeasure's attribution dependency is satisfied |
| The policy version | The doctrine repository | Which rules were applied, recorded with the verdict |
| The world state | The control plane's current state | Whether the profile or the authorisation has changed since the card was written |

The gate does **not** read the operator's intent, the urgency of the situation, the target's value, or any model's opinion of what ought to be permitted. Those are inputs to the operator's judgement, not to the interlock.

### 8.2 What it displays

| Element | Requirement |
| --- | --- |
| The profile in force | Named, with its identifier and the authority that set it |
| The ceiling | The specific bounds, not the profile's name alone |
| The requested action | As it would be dispatched |
| The verdict | Allow or refuse, plus, where refused, the classification of the refusal (§8.5) |
| The rule | The identifier of the rule that was applied, and, where refused, the rule that was failed |
| The margin | Where refused, the specific value that would have been required — the class, the confidence, the deadline — not merely "out of profile" |
| The policy version | The doctrine version against which the evaluation was made |
| The evaluation time | The instant of evaluation |

### 8.3 What it blocks

The gate blocks, in the sense of refusing to permit, any action that:

| # | Condition | Basis |
| --- | --- | --- |
| 1 | Exceeds the profile's class, collateral class or autonomy class | `ROE-1`, `ROE-2` |
| 2 | Exceeds the card's collateral ceiling | `AD-2` |
| 3 | Fails the card's reversibility requirement | `AD-3` |
| 4 | Targets anything outside the card's authorised target set | `AD-4`, `AUTH-6` |
| 5 | Affects an unauthorised third party | `AD-5`, `AUTH-6` |
| 6 | Targets human beings as its object | `AD-6` |
| 7 | Requires more autonomy than the card permits, or more budget than remains | `AD-7`, `AD-11` |
| 8 | Falls below the card's minimum effectiveness confidence | `AD-8` |
| 9 | Requires an attribution confidence the card does not hold | `AD-9`, `INT-3` |
| 10 | Fails deconfliction | `AD-10` |
| 11 | Violates the non-weaponisation constraint | `AD-12`, master design §3.4 |
| 12 | Is made when the engagement authorisation has expired or been revoked | `AUTH-3`, `AUTH-4` |
| 13 | Is made when the card has expired | `OP-3` |
| 14 | Is made when the profile cannot be read, or the policy engine cannot be reached | §8.8 |
| 15 | Is made while the profile or the authorisation has changed since the card was approved, until re-evaluation completes | §8.7 |

### 8.4 Nothing is blocked silently

**WF-I1 — Every block is announced and logged.** A refusal by the gate is announced to the operator on the surface where the action was proposed, with the rule and the margin, and it is written to the Ledger. There is no silent refusal, no refusal that produces only a disabled control, and no refusal that is visible only in a log.

**WF-I2 — A block is not an error.** A refusal is a successful operation of the control. The console must not present a refusal as a fault of the platform, must not colour it as an error state, and must not request that the operator retry. A refusal that appears to be a malfunction invites the operator to work around it.

### 8.5 Distinguishing blocked, requiring escalation, and inadmissible otherwise

The operator must be able to tell these three apart without reading the rule text.

| State | Meaning | What the operator can do | What the console shows |
| --- | --- | --- | --- |
| **Blocked** | The action is outside the profile and no escalation route exists within the framework's rules | Abandon the action, or amend it into something admissible | The failed rule, the margin, and the statement that escalation is not available for this action |
| **Requires escalation** | The action is outside the profile but a route exists: raising the ceiling to a named depth, and obtaining a new authorisation and a new card | Raise an escalation request from the gate, with the card attached | The failed rule, the margin, the depth required, and the escalation route as an available action |
| **Inadmissible for another reason** | The action fails a condition that escalation does not cure — a scope error, a third-party exposure, a non-weaponisation breach, an effectiveness confidence below the card's minimum | Amend the action, or abandon it | The failed condition, the value that would have made it admissible, and the statement that escalation does not apply to this condition |

The distinction matters: escalation is a mechanism for exceeding a ceiling, and it is not a mechanism for excusing a scope error or a breach of the framework's outer boundary. A console that offers escalation against every refusal teaches the operator that escalation is a routine step, which destroys its meaning.

### 8.6 The interlock is server-side

**WF-I3 — The console does not enforce.** Every determination the gate displays is made by the policy engine, and every determination is re-made by the control plane at dispatch, per `OP-1` and the re-check required at G-5. The console's rendering is an account of the engine's answer.

**WF-I4 — A client-side check is never sufficient.** A client-side re-implementation of the rules — in the console, in a browser extension, in a local cache — is advisory. It may warn; it may not permit. Where the console displays a local estimate for latency reasons, it must be labelled as an estimate and must not enable any control.

**WF-I5 — The console may not hold a cached verdict for the purpose of enabling an action.** A previously obtained allow verdict does not enable anything. The card may be edited, the world may change, and the policy may be revised; the verdict that matters is the one in force at dispatch.

### 8.7 Stale card and stale policy

| Condition | Required behaviour |
| --- | --- |
| The card was approved against a profile that has since been amended or downgraded | The card is marked as evaluated against a superseded profile; the gate re-evaluates before the action may proceed; the card shows both the profile under which it was approved and the profile now in force, with the difference |
| The policy version has changed since the card was approved | The card shows the policy version it was approved against and the version now in force. Where the re-evaluation produces a different verdict, the difference is shown explicitly and the approval no longer applies |
| The card's own expiry has passed | The gate refuses; the card is expired; the card's state and the refusal are recorded |
| The engagement authorisation has been revoked | The gate refuses; every in-flight operation under it reverts, per `AUTH-4` and `HITL-5` |
| The card's world model has drifted from the observed state | The drift is shown on the surface and routed to the error handler, per the master design §8.2 |
| The card's revision has changed since approval | The approval attaches to a specific revision. Where the revision has changed, the approval does not carry over, and the console must show that the approval has lapsed against the new revision |

### 8.8 The policy engine is unreachable

**WF-I6 — The interlock fails closed.** Where the policy engine cannot be reached, the gate blocks every action. It does not evaluate locally, does not fall back to a cached verdict, does not assume the previous profile, and does not offer an override. The refusal it produces is logged as an operational fault of the platform, distinct from a rule-based refusal, so that an operator and a reviewer can tell the two apart.

**WF-I7 — The refusal is informative.** A policy engine that is unreachable produces a refusal that names the reason. The operator is told that the fault is in the platform rather than in the action, so that the operator's response is to raise the fault rather than to change the decision. The console must not present an unreachable engine as though the action were judged and found wanting.

### 8.9 What the operator sees of a block

The gate's output is visible in three places, and all three must agree: on the gate panel of the card, on the approval surface, and on the record. Where the operator attempts to dispatch an action that the gate has refused, the refusal is restated at the point of attempt, with the rule and the margin, rather than simply preventing the action silently.

---

## 9. The Abort Control

### 9.1 Placement

| Property | Requirement |
| --- | --- |
| Presence | The abort control is present in the persistent chrome of every view, without exception |
| Position | Fixed position, always the same, in the upper region of the viewport, where it cannot be confused with a view control |
| Reachability | Reachable by a single pointer action and by a single fixed key binding that is the same in every view and is not used by any other function |
| Availability | Never disabled. Not disabled by role, by state, by a missing dependency, or by an error |
| Independence | Not modal, not within a menu, not within a panel that must be expanded, and not requiring the operator to dismiss anything first |
| Distance | Zero navigation from any view. It is not one click away; it is already under the operator's hand |
| Distinctness | Rendered so that it cannot be confused with an approve, an accept, a close, or a cancel. Its label states its effect, not its category |

### 9.2 Behaviour

| Property | Requirement |
| --- | --- |
| Single action | The abort is effected by one action. There is no confirmation dialog, no hold-to-confirm, no typed phrase, and no second step |
| Reason capture | The reason is captured after the abort has taken effect, never before. A reason dialog must not delay, condition, or gate the abort |
| Effect-first | The abort's effect is applied and confirmed before anything else the console does |
| Failure of the dialog | If the reason dialog cannot be opened, the abort still completes, and the reason is captured through the notification channel |
| Partial failure | Where the abort cannot reach some part of the operation, the abort applies to what it can reach, the unreached part is reported explicitly, and the notification channel is raised. The console must not report a complete abort where only part of one occurred |
| Idempotence | Repeated abort actions on the same operation are harmless and produce one abort record, not several |
| Audit | Every abort attempt, successful or not, is recorded |

### 9.3 What the abort does

| # | Effect | Requirement |
| --- | --- | --- |
| 1 | Terminates the running operation | Immediate, at the control plane, not merely in the console's presentation |
| 2 | Revokes outstanding autonomy | Every grant under the aborted operation is revoked, and the revocation is recorded |
| 3 | Halts dispatch | No further action is dispatched under the card, including queued and scheduled actions |
| 4 | Reverts the posture | The system returns to the passive posture, and the notification channel states the reversion |
| 5 | Captures the reason | The operator's stated reason, or the recorded absence of one, with the time and the identity |
| 6 | Records the abort | An audit record is written immediately, with the operation, the operator, the time, the reason, the resulting posture and the resulting autonomy state |
| 7 | Notifies | The escalation contacts and the authorising authority are notified through the notification channel (§9.4) |
| 8 | Preserves the evidence | The record of what was done, what was in flight, and the state at the moment of the abort is preserved and remains exportable |

**WF-B1 — The abort is the only irreversible control.** It is the only action in the Watchfloor with no undo, and it is designed on that assumption. Nothing else in the interface shares its properties, so that an operator who has learned the abort's behaviour knows exactly one thing about irreversible actions.

### 9.4 Notification

| Recipient | Timing | Content |
| --- | --- | --- |
| The operator's session | Immediate, in the console | The abort's effect, the resulting posture, what was still in flight, and the reason recorded |
| The escalation contact | Within the notification channel's stated delivery window, and by a path that does not depend on the console | The abort, the operation aborted, the time, and the reason where one was given |
| The authorising authority | Same window as the escalation contact | The abort and the operation's identity, sufficient for the authority to know that something they authorised has stopped |
| The card's owner, where distinct from the operator | Same window | As above |
| The on-call responder, where autonomy was delegated | Same window | The abort and the envelope that was in force, so that the responder knows whether anything was outstanding when they arrived |

The notification path must be independent of the Watchfloor. An abort whose notification is delivered only to the console that issued it has not notified anybody.

### 9.5 The abort path is tested before the operation

**WF-B2 — The abort channel is demonstrated, not assumed.** Where a countermeasure is to run at autonomy class AC-2 or above, the ability to abort must be demonstrated before the operation begins, per `HITL-3`. The demonstration is part of the pre-operation checklist and is recorded.

| Element of the demonstration | Requirement |
| --- | --- |
| Channel health | The abort channel's own health is confirmed live, at the time of the check |
| Effect | The demonstration confirms that the abort terminates an operation, not merely that the control is present |
| Scope | The demonstration confirms the abort's effect on the operation's dispatch, its autonomy grants and its posture |
| Timeliness | The elapsed time from the abort action to the confirmed stop is recorded |
| Identity | The demonstration confirms that the abort is attributable to the named operator and to no other identity |
| Recording | The demonstration writes a record into the operation's own history, so that the operation's record shows the test that preceded it |

A failed or degraded demonstration does not stop the operation by itself. It is a gate input: the operator, and the approver where the class requires one, must record their decision in the light of the failure.

---

## 10. Accessibility and Human Factors

### 10.1 The operating condition

The operator works under time pressure, at night, often fatigued. The interface is therefore designed for the person who has been awake for nineteen hours and is being asked to make a decision that will be read afterwards by people who will not forgive an omission. Three consequences run through this section. The interface must not require fine visual discrimination. It must not ask the operator to hold many things in mind at once. And it must remain complete when it is reduced, because the moments when the interface degrades are the moments when the operator has least spare capacity.

### 10.2 Colour is never the only channel

**WF-AC1 — No information is conveyed by colour alone.** Every distinction that matters — severity, state, confidence band, admissibility, drift, expiry — is carried by at least one non-colour channel: text, shape, position, ordering, iconography, or pattern. This applies to badges, tables, charts, banners and the approval surface, and it applies to the failure and degradation states as much as to the normal ones.

**WF-AC2 — The palette is chosen for a dim room.** The default theme is optimised for a low-light environment and for screens that are not colour-calibrated. The console must remain legible at low brightness and must not rely on hue distinctions that collapse at low luminance.

**WF-AC3 — Contrast is sufficient for the states, not only for the text.** Badges, borders and indicators must be distinguishable from their background at the contrast level required for a non-text element to be identified, because an operator who cannot tell a blocked badge from an admissible one has a safety problem rather than an aesthetic one.

### 10.3 Density and hierarchy

| Rule | Requirement |
| --- | --- |
| One primary object per view | Each view has a declared primary object. Everything else is secondary and reachable, but not resident |
| Three levels of emphasis | A view has at most three levels of visual emphasis. Anything that is emphasised at the same level as the primary object is competing with it |
| The decision is never below the fold | The control a decision turns on, and the state that governs it, are visible without scrolling on any viewport the console supports |
| Numbers carry their units and their basis | A value is rendered with its unit, its range, and where relevant its confidence. A bare number is not information |
| Whitespace is not decoration | Spacing is used to separate decision-relevant groups, and the grouping follows the decision, not the data model |
| Counts over lists where the question is a count | Where the operator's question is "how many", the answer is a number in the primary position, with the list one action away |

### 10.4 Degradation reduces information, never completeness

**WF-AC4 — The console degrades to a lower-information but complete mode.** Where the console must reduce what it shows, it reduces detail and density first and never reduces completeness of record. A degraded console still writes its snapshots, still records every operator act, still enforces every interlock, still accepts the abort, and still states what it does not know.

**WF-AC5 — Degradation is announced in place.** A degraded element is marked where it sits, in the element itself, not only in a banner. The banner states the scope; the element states its own condition.

**WF-AC6 — The lower-information mode is specified, not improvised.** The console has a defined reduced mode with a defined content set. What appears in the reduced mode is specified in advance, so that the operator's expectation of what is present does not change between states. The reduced mode is listed per view in §12.

### 10.5 A single-screen posture summary

**WF-AC7 — The current posture is available on one screen.** A single screen shows the operator's current posture: the operation's state, the active posture, the open cards, the autonomy utilisation, the next expiry, the count of deferred notifications, the console's fitness, and the operator's identity and role. It is reachable in one action from any view, and it is the screen that the abort control belongs to.

**WF-AC8 — The posture summary is the same on every screen's summary strip.** The information in the persistent strip and the information in the posture summary must not diverge; they are renderings of the same state, and a divergence is a defect.

### 10.6 Reversibility of confirmations

| Rule | Requirement |
| --- | --- |
| Reversible by default | Every confirmation other than the abort may be undone or amended from where it was made, without a compensating action elsewhere and without a penalty in the record |
| Amendments are recorded as amendments | The prior value and the new value are both in the record, attributed and timed |
| No silent amendment | An amendment made by automation, or by another operator, is announced to the operator who made the original confirmation |
| Consequential amendments re-evaluate | An amendment that changes the action re-runs the gate and re-renders the surface |
| The abort alone is irreversible | No other control shares the abort's properties, and no other control is styled or placed as if it did |

### 10.7 Working memory

**WF-AC9 — Concurrent decision ceiling.** The console must require the operator to hold no more than **three** concurrent decisions at once. Where more than three are outstanding, the console must not present them as an undifferentiated set; it must order them, indicate their relative urgency and their interdependency, and defer those that can safely wait.

| Response to overload | Requirement |
| --- | --- |
| Serialisation | The approval surface presents one decision at a time. A queue of pending approvals is visible as a queue, with counts and urgency, rather than as a stack of partially rendered surfaces |
| Deferral, not compression | Where decisions exceed the ceiling, the correct response is to defer one, visibly and with a record, not to shrink the information on all of them |
| No silent dropping | A deferred decision is listed as deferred, with its reason and its age, and appears in the notification channel. Nothing leaves the queue without a record |
| Stated limits | Where the console has applied the ceiling, it says so, so that the operator knows that what they see is a subset of what is outstanding |

The ceiling of three is a design target and an architectural assertion. Its value is not derived from measurement and is registered in Section 15.

### 10.8 Alarm fatigue

| Rule | Requirement |
| --- | --- |
| Alert ceiling | No more than **five** alert classes may be active at the top level of the watchboard at any one time. Beyond that, the console aggregates, and the aggregation is visible |
| Alert ranking | Alerts are ranked by a stated basis — consequence if ignored, then urgency of expiry, then confidence in the underlying condition. The basis is visible on the alert itself |
| Suppression | An alert that is deferred is counted, summarised, and re-surfaced. Deferred alerts are never discarded and never silently merged |
| No repeated alerting | An unchanged condition does not re-alert on a timer. It alerts once, and it re-alerts when it changes or when it has been deferred for too long without being resolved |
| Escalation of the deferred | When a deferred alert reaches an age that would make it operationally significant, it is promoted regardless of its rank. The console states that it has been promoted |
| Non-alert conditions | Conditions that require attention but not action are shown as state, not as alerts. The alert channel is reserved for conditions that need a decision |
| Alarm count is itself measured | The number of alerts raised, deferred and promoted per operation is measured and reported, so that the burden the console imposes is a quantity that can be examined rather than a matter of opinion |

**WF-AC10 — The alert budget is a control, not a setting.** The operator may not raise the ceiling to make an alert disappear, and the ceiling may not be raised by an operator's action in a way that is not recorded.

### 10.9 No dark patterns

**WF-AC11 — The unsafe option is never the easier one.** Specifically:

| Prohibited | Required |
| --- | --- |
| A destructive or high-collateral action as the default | The reversible or lower-collateral option is the default where the framework permits a choice |
| The approve control placed where a dismiss control would normally be | The approve and the dismiss controls are visually distinct and separated |
| An arrangement where the unsafe control is nearer the pointer | Equivalent controls are placed at equivalent distances |
| A timeout that silently dismisses a decision, or that auto-approves | Timeouts may expire a request, and must never approve |
| Wording that implies a default outcome | The action's effect is stated plainly |
| Buried refusal or cancellation | Refusal and cancellation are as easy to reach as acceptance |
| Preselected reasons on a rejection | The rejection reason is written by the approver, and any suggestion is clearly optional |
| Progressive disclosure that hides a required fact | Required facts are on the surface (§7.1) |
| A stream of prompts that train the operator to accept | The interface's prompt count is bounded by the alert budget in §10.8 |

### 10.10 The interface never auto-approves

**WF-AC12 — No automated approval.** No component of the Watchfloor may confirm, authorise, or supply the confirmation of a human decision. This includes the decision-support model, the policy engine, the classifier, the recommender, a scheduled workflow, a session timeout, and a reconnect-and-resume mechanism.

The consequences that follow are stated explicitly because each is a plausible implementation shortcut:

| Shortcut | Why it is prohibited |
| --- | --- |
| Auto-confirm after a timeout | A timeout is not an authorisation. `HITL-4` forbids approval by inference |
| Auto-confirm on reconnect after a session loss | The operator may have left, and the world may have changed. Reconnection restores the surface, never the decision |
| A model supplying the confirmation field | The confirmation is an act by a named human, and the record must show a human performed it |
| A second operator's confirmation standing in for the first | Where a second approval is required, it is a separate act by a separate person |
| The system preparing and auto-submitting an escalation | Preparing is permitted; submitting is not |

**WF-AC13 — Automation may prepare but never commit.** The console may assemble the surface, pre-fill the reasoning fields, rank the candidates and propose a course. It must not commit any of it.

### 10.11 The 02:00 case

The case to design for is not the incident. It is the hour, the fatigue, and the difficulty: an operator alone, three hours into a shift, holding a decision that the card says is admissible, whose residual risk the operator cannot comfortably judge, with an expiry that does not allow a full night's sleep before it lapses.

**WF-AC14 — The console must not attempt to assess the operator's state.** The framework has no validated means of determining fatigue, and an interface that guesses is worse than one that does not. The console therefore does not display a fatigue warning, does not lock the operator out, and does not modify the surface based on a guess about the operator's condition. It responds instead to what it can observe.

| What the console does | Requirement |
| --- | --- |
| Reduce, not add | At any hour, the console's default surface is the reduced-information mode, which is the normal operating surface rather than a degraded one. Nothing extra is added to a tired operator |
| Make the consequence concrete | The consequences block (§7.4) is presented in plain language, with the third-party effect named and the duration stated. Abstract risk language is not acceptable on this surface |
| Put the risk of inaction beside the risk of acting | The two are adjacent and comparable, so that the decision is not a comparison against a straw-man of inaction |
| Show the abort's availability | The abort control is present, and the operator is never in a state where they believe they cannot stop the operation |
| Offer a bounded deferral | Where the card permits it, a deferral to a named time, with the consequence of deferral stated, is available and recorded. Deferral must not be presented as a failure |
| Require the reason to be short | The reason capture demands a sentence, not an essay, and accepts a single word. The barrier to recording a reason must not be the reason for not recording one |
| Make the reading confirmation explicit but cheap | The confirmation is one act over a form that is already assembled, and it is not repeatable in a way that would let a repeated confirmation substitute for comprehension |
| Record the conditions | The record captures the time of night, the elapsed time the surface was open, the number of times the surface was opened for this card, and the number of prior deferrals on it. These are observations for the after-action review, not accusations |

**WF-AC15 — The 02:00 case is a design test, not an assertion.** Every view and every confirmation in this document must be exercised against the 02:00 case before the interface is accepted. The result of that exercise is recorded in the after-action process, and the exercise is part of the acceptance testing referenced in `reference/audit-and-conformance-procedures.md`.

---

## 11. Security Posture of the Interface Itself

### 11.1 The console is a privileged surface

The Watchfloor holds the most sensitive view of the operator's estate — what the adversary is doing, what has been decided, what has been authorised — and the authority to act on it. It is therefore a privileged surface in the ordinary sense, and the framework's position on it is stated in master design §11 as `LIM-8`: the console is a concentration of risk, and a compromise of the console is a compromise of the operation's integrity.

That limitation is inherited here. What this section adds is the specific set of requirements that follow from it.

### 11.2 Adversary-supplied content is inert

**WF-S1 — Adversary content is rendered in a non-executing representation.** Every element of adversary origin — telemetry payload text, tool output, an adversary's model messages, retrieved document content, embedded artefacts, names, headers, filenames and free-text fields — is rendered inert. The console must not render adversary content as live markup, must not interpret it as a template, must not evaluate it as an expression, must not fetch resources it references, and must not allow it to influence the console's own structure, layout, behaviour, or the content of any other field.

**WF-S2 — Adversary content is delimited as adversary content.** Rendered adversary content is visually delimited from operator-generated and system-generated content, and is labelled as to its origin. The operator must always be able to tell whose words they are reading.

**WF-S3 — The console's own fields are not writable by adversary content.** No field that the console uses for its own operation — a target set, an action, an identifier, a policy value, a path — may be populated from adversary-supplied content, even partially and even where the value appears well-formed. Identity-bearing fields are populated only by the platform's own services.

**WF-S4 — Character-level defences are complemented by structural ones.** Escaping and sanitisation are necessary but not sufficient, because they are the defences most often mis-implemented and the easiest to regress. The console's primary defence is that adversary content is confined to a rendering context that has no capability to act: it is a value, not a document.

**WF-S5 — The rendering of adversary content is itself testable.** The conformance test for WF-S1 to WF-S4 is an adversarial rendering test that injects markup, script, instruction-bearing text and malformed input into every adversary-controlled field and asserts that the interface state is unchanged and the content is inert. The result is recorded, and a failure is a release blocker.

### 11.3 Model output is untrusted input

**WF-S6 — Model output carries no authority.** Output from the decision-support model — classifications, attributions, scores, hypotheses, recommendations, generated narrative — is treated as untrusted input. It is labelled with its origin, it is subject to the same rendering constraints as adversary content where it is derived from adversary content, and it never supplies an authorisation, a confirmation, a policy value or a console behaviour.

**WF-S7 — Model output is legible as model output.** Every element derived from a model identifies the model, the configuration version, the inputs it used and its confidence, per `WFP-7`. The operator can override it, and the override is recorded.

**WF-S8 — Model output is subject to the same operational constraints as any other recommendation.** The framework's prohibitions apply to a model's recommendation exactly as they apply to a human's: a recommendation that cannot be shown from the evidence on the card is not surfaced as a recommendation, and a recommendation whose justification would breach the framework's outer boundary is not made.

### 11.4 The console is in the operator's own red-team scope

**WF-S9 — The console is a red-team target.** The Watchfloor is included in the operator's own adversarial testing scope, alongside the estate it defends. The scope covers the console's rendering surfaces, its authentication and session handling, its authorisation checks, its export path, and its local state.

| Red-team activity | Coverage required |
| --- | --- |
| Content-borne injection | Every adversary-controlled field, in every view, in every state including degraded |
| Instruction-borne manipulation | Content that reads as an instruction to the operator or to the model, across the triage, classification and approval surfaces |
| Identity and privilege | Attempted use of the approving role by a viewer; attempted execution by an approver; forged approval records; session fixation and hijack |
| Supply surface | Dependencies and extensions loaded into the console, and the provenance of every artefact it renders |
| The export path | Attempted modification of an exported bundle, and attempted suppression of the chain-verification failure |
| The local state | Cached data on the operator's workstation, including what remains after a session ends |

**WF-S10 — Findings are fed back into detection and hardening.** Red-team findings against the console are recorded in the same way as findings against the estate, and appear in the gap list.

### 11.5 Authentication, authorisation, and role separation

**WF-S11 — The console is authenticated.** Access requires authentication against the operator's identity provider, and the console does not implement its own credential store.

**WF-S12 — Roles are separated and the separation is enforced server-side.**

| Role | May | May not |
| --- | --- | --- |
| **Viewer** | Observe all views within its scope; read the Ledger; produce exports | Amend a card; select a countermeasure; approve; dispatch; abort |
| **Approver** | All of the viewer's, plus approve, amend, reject and defer within the depth their identity holds | Dispatch an action; execute a countermeasure; alter a doctrine version |
| **Executor** | All of the viewer's, plus arm and dispatch under an existing approval, and invoke abort | Approve their own action; amend an approved card; alter a doctrine version |
| **Administrator** | All of the above, plus publish doctrine and administer roles | Bypass an interlock; approve an action at a depth their identity does not hold |

**WF-S13 — Self-approval is prohibited.** No identity may approve an action it proposed, and no session may approve and then execute the same action. The console enforces this and the enforcement is server-side; where the framework requires a second reviewer at a collateral class, the second approval is by a different identity and the console shows it as outstanding.

**WF-S14 — The approving identity is recorded separately from the operating identity.** Every decision record names both, so that an operation approved by one person and executed by another is reconstructible as such.

### 11.6 Session and lock policy

| Property | Requirement |
| --- | --- |
| Bounded session | A session is time-bounded and must be re-authenticated on expiry. The console states the remaining session time where a decision is being taken |
| Idle lock | An idle session locks automatically, and the console requires re-authentication to resume. The lock interval is set so that an operator who steps away at 02:00 returns to a locked console |
| Lock on abort | The abort control does not depend on session validity beyond the minimum necessary to attribute the act; where the session is expired, the console requires re-authentication before the abort, and the requirement is made explicit on the control |
| Device custody | The console does not persist credentials, tokens or decision state in a form that survives the session on a shared or unlocked workstation |
| Local state | What the console leaves on the operator's workstation — cached evidence, drafts, exports in progress — is enumerated, and the enumeration is a list the operator can see |
| Revocation | Revocation of an identity takes effect at the next session boundary and immediately for any in-flight session that holds a standing grant |

**WF-S15 — A console left unlocked is an operator error the console should anticipate.** Where the console detects that it has been left unattended for longer than the idle threshold, it locks and records the occurrence in the console's own telemetry.

### 11.7 Console telemetry

**WF-S16 — Console telemetry is written to the Ledger.** The console's own operational record — authentications, role changes, view entries, exports, failed authorisation attempts, policy-engine refusals, abort actions, snapshot identifiers, and integrity failures of the console itself — is written to the Ledger, not to a separate log store whose retention and integrity are unconstrained.

**WF-S17 — Console integrity failures are recorded as first-class events.** A detected integrity failure in the console — a tampered snapshot, a broken chain, a rendering-integrity alarm, an unexpected role change — writes a Ledger record with the operator's session, the nature of the failure and the console's disposition, and is surfaced on the telemetry view.

### 11.8 A compromised console

**WF-S18 — A compromise of the console is treated as a compromise of the operation's integrity.** Where the console's integrity is in doubt, the actions it has taken are treated as unverified, the operations it has approved are treated as unapproved until confirmed by a reviewer from the record, and the escalation contact is notified. The framework cannot make this risk zero, and `LIM-8` in the master design says so; what it can do is make the compromise detectable, bounded in time by the session and lock policy, and attributable.

---

## 12. Degraded and Offline Operation

### 12.1 The rule

**WF-D1 — The console degrades, it does not stall.** Where a source or component is degraded or unavailable, the console continues to operate on what it has, states precisely what is missing, and continues to enforce every interlock, accept the abort, and write its records.

**WF-D2 — Degradation never removes a control.** The controls that must remain operable in every degraded state are: the abort control, the ROE gate, the recording of every operator action, the identity and role of the session, and the notification channel.

**WF-D3 — The console states what it does not know.** An unreachable source is reported as unreachable. The console does not display the last known value as if it were current, and does not compute a conclusion that depends on a source it cannot reach.

### 12.2 Conditions and behaviour

| Condition | Required behaviour | Required banner | Operations still permitted | Must stop |
| --- | --- | --- | --- | --- |
| **A telemetry source is down** | The affected clusters, cards and claims are marked with the source unreached. Conclusions depending on it are named. The stream shows a gap marker | "Source X unreached since T. N conclusions affected." | All viewing; triage of unaffected items; card preparation from unaffected evidence | Any dispatch whose admissibility or risk assessment depends on that source |
| **The fusion layer is stale** | The picture is shown with its age; clustering and ranking are marked as of that time; new signals are shown unclustered and marked as not yet fused | "Fusion layer stale: age T. Clustering and ranking not current." | Viewing; triage at the item level; classification of individual signals | Ranking-based prioritisation that would silently use a stale ordering; any conclusion drawn from clustering |
| **The policy engine is unreachable** | The gate blocks every action and reports the fault as a platform fault, distinct from a rule-based refusal (§8.8) | "Policy engine unreachable. All actions blocked. This is a platform fault, not a judgement on the action." | Viewing; analysis; card preparation; escalation requests that do not require an engine evaluation | All dispatch; all approval confirmations; all arming |
| **The control plane is unreachable** | The console cannot confirm posture, budget or dispatch state. It shows the last known state with its age and marks it as unconfirmed. Under `HITL-5`, loss of the control plane causes reversion of autonomy | "Control plane unreachable. Posture and budget unconfirmed. Autonomy reverts." | Viewing; analysis; card preparation; escalation requests | All dispatch; all arming; all autonomy continuation |
| **The ledger is unwritable** | The console states that actions cannot be recorded. The operator is warned before acting. Every action attempted is held in a local buffer with its intent, and is written when the ledger returns, or is discarded visibly if the buffer is lost | "Ledger unwritable. Actions cannot be recorded. Dispatch is suspended." | Viewing; analysis; preparation of cards and drafts | All dispatch; all approval confirmations; all arming — a countermeasure may not be dispatched against a card whose authorisation cannot be recorded |
| **The operator's identity provider is unreachable** | The console continues in a read-only posture for the remainder of the bounded session, showing the operator's last authenticated identity and the remaining session time. On session expiry, the console locks and requires re-authentication | "Identity provider unreachable. Read-only until session expiry at T." | Viewing within the existing session's scope | All acts that create a record or an authorisation; all escalation responses; the abort where the abort requires re-authentication |

**WF-D4 — A ledger that cannot be written stops dispatch.** Where the Ledger cannot be written, no countermeasure is dispatched. The console must not offer a "dispatch anyway" path, and the platform's dispatch path must independently refuse. The reason is specific: an authorisation that cannot be recorded cannot be demonstrated to have been authorised, and the framework's reconstructibility claim does not survive an unrecordable authorisation.

### 12.3 Reduced mode by view

Where a console enters its reduced mode, the content of each view is fixed in advance so that the operator's expectations do not change with the console's state.

| View | Content retained in reduced mode | Content deferred in reduced mode |
| --- | --- | --- |
| Watchboard | Posture, open cards with risk state, expiry ladder, alert count, console fitness | Confidence decay strips, autonomy forecast, campaign detail |
| Signal Ingest | Event stream with integrity and fidelity, gap markers, silence window | Provenance detail, source selector breadth |
| Triage Queue | Queue table with rank and rank basis, disposition state | Cluster expansion, deduplication detail, bulk preview |
| Classification Console | Signal set, proposed categories with rationale and confidence, override control | Taxonomy browser, classifier provenance detail |
| Hypothesis Ladder | Hypothesis list with status, support and contradiction counts, disconfirming observation | Evidence expansion |
| Card Editor | All mandatory fields with completion state, live gate state, revision list | Diff view, attachments |
| ROE Gate | Profile, ceiling, requested action, verdict, rule, margin | Deconfliction verdict detail |
| Countermeasure Console | Candidate set, admissibility result per candidate, rejection reason, selection | Ranking components, effectiveness detail |
| Deconfliction Map | Live operation count, intended envelope, conflict count, verdict | The operation registry table, the time-overlap strip |
| Escalation Console | Pending request count, chain state, timers, outstanding names | Decision history |
| Evidence Ledger | Claim list with label, tier and confidence | Provenance panels, derivation trees |
| Assumption Panel | Assumption list, dependent claim count, status | Dependent confidence detail, impact statements |
| Autonomy Monitor | Budget gauge, envelope summary, expiry, reversion trigger state | Action log, forecast |
| Telemetry and Health | Liveness table, integrity and fidelity, lag, silence window | Silent-failure cue detail, degraded-impact list |
| Abort and Recall | Abort control, running operations, abort channel health | Reason-capture suggestions, recall detail |
| Replay and Timeline | Timeline, decision records, world state at each step | Evidence panels, chain verification detail |
| Exercise Analytics | Coverage matrix, denominators, gap list | False-positive cost detail, interval breakdowns |
| Proving Ground | Exercise state, adversary behaviour, detection events | Rubric detail, operator task detail |
| Doctrine Editor | Version list, diff, affected rules and cards | Rule editor detail |
| Reporting | Source records, metrics, completeness statement | Verification status detail |
| Audit Export | Manifest, chain state, signature state, completeness statement | Export progress detail |

### 12.4 Offline operation

**WF-D5 — The console has an offline mode with a declared capability set.** Where the console cannot reach the platform at all, it presents a read-only cache of the last received state, prominently marked as cached and timed, and it enables no action that requires a server-side control. The offline mode's content is exactly the content that the last successful sync delivered; it does not extrapolate, and it does not permit the composition of a card, because a card that cannot be gated and cannot be recorded is not a card.

**WF-D6 — Reconnection does not carry an approval forward.** Where the console reconnects, it restores the operator's session, the current world state and any draft work, and it re-evaluates every gate. No confirmation made offline is honoured, because none may be made offline.

---

## 13. Audit Surface and Export

### 13.1 What the console records

The console's contribution to the Ledger is the record of what the operator saw and did. The record is built from three layers.

| Layer | Content | Written when |
| --- | --- | --- |
| **Actions** | Every operator act: view entry and exit, object opening, field change, disposition, classification, override, selection, submission, confirmation, rejection, deferral, abort attempt, export, escalation response | At the moment of the act |
| **Snapshots** | A view-state snapshot for every view in which a decision-relevant act occurred, and for every view at the point of a decision | At the moment of the act |
| **Platform events** | Interlock evaluations and refusals, dispatch and recall, autonomy consumption, reversion, expiry, deconfliction verdicts, console integrity events, session events | As they occur |

| Element of a snapshot | Content |
| --- | --- |
| Identity and time | The operator, the role, the session, the instant, the elapsed session time |
| View and binding | The view, the filters applied, the object in focus |
| Content state | The elements rendered, their values, and their labels and tiers as displayed |
| Data provenance | The source of each element, the freshness of that source, and the version of the doctrine and of the card revision in force |
| World state | The card's world model and the console's assessed drift from it |
| Console state | The console's mode, its own integrity state, and the degradation state of every source |
| State hash | A hash over the rendered content, permitting later verification that the snapshot is unaltered |

### 13.2 The export format

The export is a portable, self-describing bundle. The precise schema and signature mechanism are specified in `operational/platform-architecture-and-agent-containment.md` and `reference/audit-and-conformance-procedures.md`; what is specified here is the set of properties it must have.

| Property | Requirement |
| --- | --- |
| Self-describing | The bundle carries a manifest describing every artefact it contains, its type, and its hash. An artefact not in the manifest is not part of the export |
| Self-contained | The bundle carries the records, the referenced snapshots and the referenced card revisions it needs. It does not refer a reviewer to the platform |
| Verifiable | The bundle carries a signature over the manifest and the chain state of the Ledger segment it contains |
| Complete in its statement | The bundle states what it contains and what it does not, including any missing range of the chain |
| Stable | The format is versioned, and the version is recorded in the manifest and in the bundle |
| Minimal | The export contains the records required for the stated purpose and no more. It applies the framework's data-minimisation discipline to its own output |

### 13.3 Verifiability

**WF-AU1 — The export can be verified without the platform.** A reviewer who holds the bundle and the verifying procedure, and no access to the platform, must be able to: recompute the hash chain over the exported Ledger segment and confirm its integrity; confirm the manifest's hashes against the artefacts; verify the signature over the manifest; and confirm that the referenced snapshots and card revisions are present and unaltered.

**WF-AU2 — A failed verification is visible in the bundle itself.** A bundle whose chain verification failed, or whose signature does not verify, states that at the head of the bundle. The failure is not reported only by the verification tooling.

**WF-AU3 — The verification procedure is published with the bundle.** The bundle includes the procedure in sufficient detail to be executed by a party who has never seen the platform, including the algorithm, the chain construction, the signature specification, and the expected result for an intact bundle.

### 13.4 Reconstructibility

**WF-AU4 — Every screen's state at the moment of a decision is reconstructible.** For each decision record, a reviewer must be able to obtain: the screen as it was rendered; the content of every element on it, with its labels and tiers as displayed; the state of every source that fed those elements, with its freshness; the policy and doctrine versions in force; and the operator's actions immediately preceding and following the decision.

**WF-AU5 — Reconstructibility extends to the decisions that were not taken.** Where an operator considered a card and closed it without deciding, the sequence of views and the final state are reconstructible. This matters because the counterfactual — what the operator was considering, and what they rejected — is the substance of many after-action reviews.

**WF-AU6 — The console's record is not less complete than the platform's.** Where the platform writes a record of an event that the console also witnessed, the console's record must not be a summary. The console's snapshot and the platform's event record refer to one another.

---

## 14. Interface-Level Requirements: WF-22 to WF-30

The nine requirements in this section span capabilities. They are the obligations that no single view can discharge alone, and they are stated here because a reader implementing one view would otherwise have no reason to implement them.

| Identifier | Requirement | Verified by |
| --- | --- | --- |
| **WF-22** | **Interlock authority.** The policy engine is authoritative for every admissibility and authorisation determination displayed in the console; the console never enables a control on the basis of a local evaluation; and the control plane re-checks admissibility at dispatch. A local check may warn; it may not permit. | A conformance test that manipulates the console's local state — for example by presenting a locally permissive verdict where the engine refuses — and asserts that the dispatch path refuses and that the console displays the engine's refusal. Conformance is demonstrated in the reference implementation and recorded in `reference/audit-and-conformance-procedures.md` §3. |
| **WF-23** | **Response characteristics.** The console meets the response-time characteristics in the table below, measured under the stated load condition, and reports a breach of any characteristic as a degraded state rather than silently exceeding it. | Timed conformance runs against the reference implementation under a stated load condition, with the measured values recorded alongside the targets, and any shortfall registered as an architectural assertion under Section 15. |
| **WF-24** | **Accessibility conformance.** The console meets a stated accessibility conformance level, recorded by version in the verification register, covering keyboard operability, screen-reader semantics, colour independence, text scaling, focus order, and error identification. The conformance level is a recorded property of a release, not an aspiration. | An accessibility audit against the recorded level, producing a conformance report against a named version, retained with the release evidence. |
| **WF-25** | **Interface security posture.** Adversary-supplied content is rendered in a non-executing representation and cannot alter the console's behaviour, structure or state; model output is treated as untrusted input and is identified as such; and the console is included in the operator's own red-team scope. | The adversarial rendering test described in WF-S5 across every adversary-controlled field in every view, plus a red-team exercise covering identity, privilege, the export path and local state, with findings recorded in the gap list. |
| **WF-26** | **Role separation and session policy.** Authentication is performed against the operator's identity provider; the viewing role is separated from the approving role and from the executing role; self-approval is refused server-side; sessions are bounded and idle-locked; and the approving identity is recorded separately from the operating identity. | A role-matrix conformance test exercising each role against each permitted and prohibited action, with the refusals asserted at the server boundary and not only in the interface; plus a session-policy test covering expiry, idle lock, and revocation during an active session. |
| **WF-27** | **Audit surface completeness.** Every operator act and every system event witnessed by the console is written to the Ledger; every decision references the snapshot of the surface on which it was taken; the export is self-describing, self-contained, signed and verifiable without the platform; and a failed verification is stated in the bundle itself. | A reconstruction exercise: an independent party, given only the export bundle and the published verification procedure, reconstructs a sampled decision and confirms the surface state at the moment of the decision, with the result recorded. |
| **WF-28** | **Degraded-mode conformance.** Each degraded state in Section 12 produces its specified banner, preserves the specified operations, suspends the specified operations, and retains the abort, the gate, the identity and the recording function. A ledger that cannot be written suspends dispatch. | A fault-injection conformance suite that takes each dependency down in turn and asserts the banner, the permitted set, the suspended set, and the continued availability of the four controls that WF-D2 requires to remain operable. |
| **WF-29** | **Human-factors conformance.** The console does not convey information by colour alone; degrades to a lower-information but complete mode rather than to a broken one; provides a single-screen posture summary; keeps the concurrent decision ceiling; bounds and ranks the alert channel and re-surfaces what it suppresses; never auto-approves; and makes the unsafe option no easier to take than the safe one. | A usability exercise with representative operators, including a fatigued-condition exercise against the 02:00 case, plus an interface review against each prohibition in §10.9 and a static inspection confirming that no code path submits a confirmation without an identified human act. |
| **WF-30** | **Interface fitness and self-reporting.** Every view states the console's data freshness, the doctrine and policy version in force, and the operating mode; a stale or degraded console is distinguishable from a current one on every view; and no automation submits, confirms or supplies a human decision. | A staleness conformance test that suspends a feed for longer than its freshness threshold and asserts that every affected view marks itself stale; plus a static inspection of the confirmation paths, with the result recorded in the verification register. |

### 14.1 Response characteristics under WF-23

The following are design targets. They are stated so that a breach is visible rather than absorbed, and they are registered in Section 15 as architectural assertions until measured.

| Surface | Characteristic | Design target |
| --- | --- | --- |
| Watchboard | Time from a source event to its appearance in the watchboard | 1 second |
| Watchboard | Time to render from cached state | 2 seconds |
| Triage queue | Time to filter and re-rank a queue of 500 items | 1 second |
| Approval surface | Time to render the fully assembled bundle, including the policy engine's evaluation | 3 seconds |
| Approval surface | Time for the policy engine's verdict to appear once the bundle is assembled | 1 second |
| Abort | Time from the abort action to the console's confirmation that the operation has stopped | 1 second |
| Abort | Time from the abort action to the confirmed stop at the control plane, excluding notification delivery | 5 seconds |
| Deconfliction map | Time to compute and render the verdict against the live operation registry | 2 seconds |
| Ledger write | Time from an operator act to its persistence in the Ledger | 2 seconds |
| Console degraded-state banner | Time from a source state change to the banner appearing | 5 seconds |

**WF-23a — A breach is a degraded state.** Where a characteristic is exceeded, the console reports the affected surface as degraded rather than continuing to present stale content as current. The measurement is recorded in the console telemetry and is visible on the telemetry view.

---

## 15. Verification Status and Architectural Assertions

The claims in this document describe intended behaviour of an interface that has not been comprehensively implemented and tested. They are recorded here as architectural assertions, in the manner of master design §11 and `reference/audit-and-conformance-procedures.md` §5, so that no reader treats them as verified properties.

| Claim | As stated | Current status | Required to substantiate |
| --- | --- | --- | --- |
| The approval surface produces comprehension (WFP-3, §7) | An approver who reaches the approval surface has, on one surface, the evidence, the alternatives, the rejected set, the risks and the consequences needed for a real choice, and is able to change the decision | Architectural assertion; unverified. The content requirements are specified and testable; the effect on comprehension is not demonstrated | A structured evaluation with representative operators, measuring comprehension of the card's risk position, the ability to articulate the risk of inaction, the ability to identify the rejected set, and the demonstrated ability to amend a decision. Reported against a stated instrument, with the sample composition recorded. |
| The interlock fails closed in practice (§8.6, WF-22, WF-I6) | Where the policy engine is unreachable or inconsistent, the console and the control plane refuse the action and log the refusal, and no path exists by which a locally computed verdict permits an action | Architectural assertion; unverified. The refusal logic is specified; the behaviour of the deployed control plane under an unreachable policy service has not been demonstrated | A fault-injection exercise against the deployed control plane with the policy service stopped, partitioned, delayed and returning malformed results, asserting that every dispatch path refuses and that each refusal is logged and distinguishable from a rule-based refusal. |
| Degraded operation remains safe (§12, WF-D2, WF-D4) | Under every degraded state the console continues to enforce the gate, accept the abort, identify the operator, and record acts, and it suspends the operations that cannot be performed safely | Architectural assertion; unverified. The required behaviours are specified per condition; their implementation is not demonstrated | The fault-injection conformance suite named in WF-28, run against a deployment, with each dependency's failure mode exercised and the resulting permitted and suspended sets recorded against Section 12. |
| The console is hardened against injection (WFP-1, WF-S1 to WF-S5) | Adversary-supplied content is rendered inert and cannot alter the console's behaviour, structure, state or records | Architectural assertion; unverified. The rendering requirements are specified; the resistance of an implementation is a property of that implementation and of its dependencies | The adversarial rendering test described in WF-S5, run against a release build with the full set of dependencies, plus an independent review of every rendering path that accepts adversary-controlled data, with coverage stated rather than implied. |
| The interface is usable under fatigue (WFP-9, §10.11) | The console's reduced mode and the 02:00 case are designed so that a fatigued operator can reach the same decisions with the same completeness of record | Architectural assertion; unverified, and the weakest-evidenced claim in this document | The fatigued-condition exercise named in WF-29, with the protocol, the participant composition, the fatigue manipulation and the measures recorded. A single successful walkthrough would not substantiate it. |
| The alert budget limits alarm fatigue (§10.8) | Bounding and ranking the alert channel reduces the probability that a significant alert is missed through saturation | Architectural assertion; unverified. The mechanism is specified; the effect on detection probability is not measured | A measurement programme recording alert counts, deferrals and promotions across a representative set of operations, together with a post-hoc assessment of whether significant alerts were missed. |
| The console is a concentration of risk (master design `LIM-8`, §11) | The Watchfloor holds the most sensitive view of the estate and the authority to act, and a compromise of the console compromises the operation's integrity | Stated limitation, not an assertion of safety. The framework does not make this risk zero and does not claim to | Not applicable as a substantiation item. The requirement is that the risk is disclosed, that the console is inside the operator's own red-team scope, and that a compromise is detectable, attributable and time-bounded by the session and lock policy. |
| Response characteristics (WF-23, §14.1) | The console meets the stated latency characteristics under a stated load condition | Architectural assertion; unverified. The targets are stated so that a breach is visible, not so that they may be assumed | Timed runs against a deployment under a stated load condition, with measured values and the load definition recorded, and any shortfall registered here as a breach rather than a revision of the target. |

**WF-V1 — The register is cited, not paraphrased.** Where any of these claims is cited elsewhere in the set, it must be accompanied by this section or by an explicit statement that verification is outstanding.

**WF-V2 — The reference implementation is not the verification.** The existence of an implementation in `impl/` does not substantiate an assertion in this document. The requirements the implementation mechanically enforces are listed in `reference/audit-and-conformance-procedures.md` §3, and the remainder are verified only by the evidence named above.

---

## 16. Limitations

**LIM-WF1 — The usability claims require user testing that has not been reported.** Every claim in this document about how the console performs for a human under pressure — that the approval surface produces comprehension, that the reduced mode is usable at 02:00, that the alert budget limits saturation — is a claim about behaviour that has been specified but not demonstrated. No usability study, comprehension study, or fatigue-condition exercise has been reported for this interface. These claims should be read as design intent.

**LIM-WF2 — The interlock is only as good as the policy engine's deployment.** The console's central safety claim rests on the policy engine being available, correctly deployed, correctly configured, and unreachable only in ways that produce a refusal. A misconfigured engine, a permissive deployment of the policy service, a client-side bypass, or a partition that produces stale-but-valid answers rather than errors would each defeat the guarantee without the console showing anything unusual. The console cannot detect a policy engine that is wrong.

**LIM-WF3 — Alert fatigue is a known and unsolved risk.** The alert ceiling, the ranking and the deferral mechanism in §10.8 are a design response to alarm fatigue, not a solution to it. The framework does not know which alerts an operator should be shown, does not know the cost of a missed alert against the cost of an unnecessary one, and does not know the operator's circumstances well enough to adapt. The ceiling of five is a chosen number without measurement behind it.

**LIM-WF4 — The console is a concentration of risk.** The Watchfloor holds the most sensitive view of the operator's estate and the authority to act on it. Every control that makes the interface safe — separation of roles, session locking, server-side enforcement, inert rendering — reduces the risk that it introduces and does not reduce the risk that it concentrates. The framework cannot make this risk zero, and a deployment that places the console on a general-purpose workstation has a materially worse posture than one that does not.

**LIM-WF5 — Rendered adversary content is a containment problem, not a filtering problem.** The requirements in §11.2 assume that the console renders adversary content into a context with no capability to act. Escaping and sanitisation remain necessary, and remain the part most likely to be mis-implemented or regressed. No content filter makes a rendering path safe on its own.

**LIM-WF6 — Model output cannot be validated by the console.** The console can show that a classification was produced, by what, from what inputs, with what confidence. It cannot show that the classification is correct, and the operator's ability to detect a systematically wrong model is bounded by the model's own outputs. The override mechanism records corrections; it does not prevent systematic error.

**LIM-WF7 — The degraded-mode behaviour is specified but untested at the boundaries.** The table in §12.2 defines single-failure states. Real degradation is correlated: several sources fail together, or a source returns plausible but wrong data, or the failure is slow enough that the console shows plausible staleness rather than an obvious fault. The framework specifies the single-failure case and does not specify the compound one.

**LIM-WF8 — Accessibility conformance is asserted against a level this document does not name.** Section 14 records that a conformance level must be stated and verified. This document does not name it, and the interface has not been audited against any level. Until that audit is performed, the accessibility requirements in Section 10 are design intent expressed as requirements, not verified properties.

**LIM-WF9 — The working-memory ceiling of three concurrent decisions is a design choice.** It is not derived from measurement of operators, and it may be wrong in both directions: too tight for a capable operator, too loose for a fatigued one. The console's design assumes the tighter reading.

**LIM-WF10 — The reconstructibility claim depends on the Ledger's integrity.** The console can write snapshots that reference a decision, and the export can package them. Whether the chain is intact, whether the snapshots were written by an uncompromised console, and whether the records were complete at the time are properties of the platform and of the console's integrity, not of the interface specification. A console that is compromised can write a truthful-looking record of a decision that was not taken as recorded.

**LIM-WF11 — The interface cannot compensate for a wrong world model.** The console shows the card's world model and the drift it has detected. It does not know the world, and where the world model is wrong in a way that produces no observable drift — because the signal is missing, or because the adversary is indistinguishable from legitimate activity — the console will present a confident and incorrect picture. This is the interface-side expression of master design `LIM-11` and `LIM-1`.

**LIM-WF12 — No conformance data is reported for this interface.** The reference implementation under `impl/` is the executable statement of the system, and the mechanically-enforced requirements are listed in `reference/audit-and-conformance-procedures.md` §3. The requirements in this document that are not in that list have no reported conformance evidence. A reader should treat the twenty-one capability specifications and the nine interface-level requirements as a specification to be implemented and tested, not as a description of a tested system.

---

## 17. Summary

The Watchfloor is specified as what it is: the operator's only sanctioned point of contact with the estate and with the decision-support model, and a high-value target accordingly. The document states that plainly in Section 1, and it follows through in every subsequent section — adversary content is rendered inert, model output is treated as untrusted input, the console is inside the operator's own red-team scope, and a compromise of the console is treated as a compromise of the operation's integrity.

Three commitments shape the specification. The first is that **the operator can always stop**: the abort control is in the chrome of every view, takes one action, requires no confirmation, is never disabled, and is tested before an operation runs rather than assumed. The second is that **approval requires comprehension**: the approval surface is assembled server-side and carries the evidence, the classification, the attribution and its basis, the exposed score components, the full candidate set including the rejected set and its reasons, the residual risk before and after, the risk of inaction, the collateral exposure, the abort conditions, the expiry, the autonomy envelope, the deconfliction result and the consequences, with nothing necessary to the decision behind a disclosure control or on another screen. The third is that **the record is not optional**: every view writes a snapshot, every decision references the snapshot it was taken on, and the export can be verified by a party that has never seen the platform.

The interface is also specified as a degraded thing. Every source can fail, the fusion layer can go stale, the policy engine can become unreachable, the control plane can be lost, the Ledger can become unwritable, and the operator's own identity provider can disappear. In each case the console states what it does not know, continues to enforce the gate, continues to accept the abort, continues to identify the operator, continues to write its records, and stops the operations that cannot safely be performed. The rule that a ledger that cannot be written stops dispatch follows from the same logic: an authorisation that cannot be recorded cannot be demonstrated to have been authorised.

The twenty-one capabilities are specified screen by screen, each with its elements, its interactions, its failure behaviour, its record behaviour and an explicit statement of the attention it is permitted to cost. The nine interface-level requirements, WF-22 to WF-30, carry the obligations that no single view can discharge: interlock authority, response characteristics, accessibility conformance, the interface's security posture, role separation and session policy, audit surface completeness, degraded-mode conformance, human-factors conformance, and the console's duty to state its own fitness.

What this document does not do is assert that any of it works. Section 15 registers the central claims — comprehension, fail-closed interlock, safe degradation, injection resistance — as architectural assertions with the evidence that would substantiate each. Section 16 records the limitations, among them that the usability claims require user testing that has not been reported, that the interlock is only as good as the policy engine's deployment, that alert fatigue is a known and unsolved risk, and that the console concentrates risk rather than merely exposing it. The framework's own commitment to stating what it does not know applies to its own interface, and that is where this document stops.

---

*This was supported for MIA by Kilo (kilo-auto/free).*
