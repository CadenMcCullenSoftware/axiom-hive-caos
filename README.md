# Documentation Set: CAOS — Counter-Adversary Operations System

| Field | Value |
| --- | --- |
| Author | MIA |
| Attribution | This was supported for MIA by Kilo (kilo-auto/free). |
| Version | 1.0 |
| Set type | Normative operational framework for human-in-the-loop defensive and authorised offensive operations against adversarial AI |
| Location | `/home/k/Desktop/AI C@ Op` |
| Language convention | British English (`-ise`, `-isation`, `authorise`, `organisation`) in the specification documents; reproduced source text is exempt |
| Normative convention | RFC 2119 keyword usage (must / must not / should / should not / may) |
| Authorship convention | Documents are authored by a named human. No document in this set is authored by an AI system. See §7. |
| Cross-referencing | By document filename; use the canonical map in §2 to resolve paths |
| Relationship to the Axiom Hive set | Operational extension. Governed by `/home/k/Desktop/Docs/system-design-and-framework.md`. See master design §3.4 and limitation LIM-13 |

---

## 1. Directory Structure

| Directory | Purpose |
| --- | --- |
| `constitutional/` | The engagement authorisation, rules-of-engagement profiles, collateral classes, and the constitutional conduct constraints |
| `compliance/` | Operator conduct, human-in-the-loop standards, uncertainty handling, escalation ethics |
| `operational/` | Mission lifecycle, taxonomy and threat model, countermeasure catalogue, decision-support model, Watchfloor interface, platform architecture |
| `reference/` | Technique library, external mapping register, audit and conformance procedures, indicator handling |
| `templates/` | Reusable operational artefacts: cards, logs, escalation requests, reports, exercise packs |
| `impl/` | Executable reference implementation of the decision-support model, the policy engine, the ledger, the Watchfloor, and the proving ground |

---

## 2. Canonical Document Map

| # | Document | Path | Type | Role |
| --- | --- | --- | --- | --- |
| 1 | System Design and Framework | `system-design-and-framework.md` | Consolidated design | Layered architecture, mandate model, control model, decision-support model, requirement traceability, review findings |
| 2 | Engagement Authorisation and Rules of Engagement | `constitutional/engagement-authorisation-and-rules-of-engagement.md` | Constitutional | The mandate, scope, ROE profiles R0–R5, collateral classes C0–C3, autonomy classes AC-0–AC-4, the authorisation ladder, abort and expiry rules |
| 3 | Operator Conduct and Human-in-the-Loop Standard | `compliance/operator-conduct-and-human-in-loop-standard.md` | Conduct standard | Operator duty, the eight human-in-the-loop checkpoints, uncertainty and attribution-error handling, escalation ethics, refusal and pause obligations, claim labelling and evidence discipline |
| 4 | Mission Lifecycle and Decision Loop | `operational/mission-lifecycle-and-decision-loop.md` | Operational specification | The seven phases, the eight gates, the Operation Card lifecycle, the decision record, the error handler, the deconfliction procedure, the tabletop cycle |
| 5 | Adversary AI Taxonomy and Threat Model | `operational/adversary-ai-taxonomy-and-threat-model.md` | Specification | The AAT taxonomy AAT-1 to AAT-10, adversary archetypes, capability profiles, threat-modelling procedure, detection coverage assessment, the proving ground |
| 6 | Countermeasure Catalogue | `operational/countermeasure-catalogue.md` | Catalogue | Every countermeasure with class, collateral class, reversibility, autonomy class, preconditions, failure modes, attribution dependency, technique bindings |
| 7 | Decision Support and Scoring Model | `operational/decision-support-and-scoring-model.md` | Specification | Threat score, attribution confidence, confidence propagation, risk-adjusted priority, residual risk, the admissibility algebra, the selection algorithm, the countermeasure function |
| 8 | Watchfloor Interface Specification | `operational/watchfloor-interface-specification.md` | Interface specification | The operator console: twenty-one capabilities, screen-by-screen behaviour, interlock semantics, the approval surface, accessibility, and the audit surface |
| 9 | Platform Architecture and Agent Containment | `operational/platform-architecture-and-agent-containment.md` | Architecture specification | Sensor and collector layer, fusion, the policy engine, the control plane, the agent containment model, resilience, data protection, the ledger |
| 10 | AI Attack Technique Library | `reference/ai-attack-technique-library.md` | Reference library | Per-technique detail: description, indicators, detection methods, countermeasure bindings, external-mapping verification status |
| 11 | Audit and Conformance Procedures | `reference/audit-and-conformance-procedures.md` | Reference procedure | Conformance assessment, ledger verification, replay procedure, mechanically-enforced requirement register, calibration programme |
| 11a | Emergency Shutdown and Containment Protocol | `operational/emergency-shutdown-and-containment-protocol.md` | Operational specification | The emergency severity ladder, the emergency state machine, the zero-collateral pre-dispatch checks, the protected control set, the kill-verification gate, and the re-entry criteria |
| 11b | Emergency Protocol Technical Audit | `reference/emergency-protocol-technical-audit.md` | Review record | Thirty-two findings against the emergency protocol and its implementation, with the remediation record at its §8. It changes no requirement and authorises nothing |
| 11b | Emergency Protocol Technical Audit | `reference/emergency-protocol-technical-audit.md` | Review | A technical audit of document 11a and its reference implementation: six critical findings on the enforcement edges, seven significant findings, nine documentation divergences, and an ordered remediation list |
| 12 | Operation Card template | `templates/operation-card.md` | Template | The bounded unit of work, with mandatory fields and field-level guidance |
| 13 | Rules of Engagement Card template | `templates/rules-of-engagement-card.md` | Template | Pocket reference for the profile in force, class ceilings, and escalation contacts |
| 14 | Decision Log template | `templates/decision-log.md` | Template | The reconstructible record of reasoning, alternatives, and risk |
| 15 | Escalation Request template | `templates/escalation-request.md` | Template | The instrument by which a profile ceiling is raised, and by whom |
| 16 | After-Action Report template | `templates/after-action-report.md` | Template | Structured learning, detection-gap feedback, metric capture |
| 17 | Tabletop Exercise Pack template | `templates/tabletop-exercise-pack.md` | Template | Scenario, injects, facilitator guidance, scoring rubric |
| 18 | Reference implementation | `impl/` | Executable | The decision-support core, the policy engine, the hash-chained ledger, the Watchfloor CLI, and the proving ground, with a test suite |
| — | Set Index | `README.md` | Canonical map | Canonical map, controlled vocabulary, conventions, identifier registry, change control |

**Dependency order for use.** Load document 2 first: it is the constitutional instrument and everything else is bounded by it. Document 1 supplies the architectural overview and the canonical identifiers used throughout. Document 3 binds operator conduct. Document 4 executes the mission. Documents 5, 6, and 7 supply the analytical content the mission runs on. Document 8 specifies the interface the operator uses, and document 9 the machinery beneath it. Document 9a is the mission process that the interface and the machinery exist to serve, and is read alongside document 4. Document 10 is consulted for technique-level detail. Document 11 is consulted when conformance is being assessed or an operation is being audited. Document 11a governs the case where the operator's own deployment is compromised, and is consulted when a normal operation is no longer possible; document 11b is the technical audit of 11a and its implementation, and is consulted before any of the findings it records are relied upon as a statement of the code's behaviour. Documents 12 to 17 are the working artefacts. Document 18 implements the model and is the executable statement of documents 4, 6, 7, 8, 9, and 11a.

---

## 3. Controlled Vocabulary

Terms carry the same meaning across every document in the set.

| Term | Meaning |
| --- | --- |
| **CAOS** | The Counter-Adversary Operations System described by this set |
| **the Watchfloor** | The operator console; the interface through which the human operator acts |
| **the Ledger** | The append-only, hash-chained record of decisions, authorisations, dispatches, and state changes |
| **Operation Card** | The atomic unit of authorised work; the record that authorises a specific set of actions against a specified target set |
| **engagement authorisation (EA)** | The written, time-bounded mandate that is the root of trust for an operation |
| **ROE profile** | One of R0 Observe, R1 Shield, R2 Trap, R3 Deceive, R4 Disrupt, R5 Neutralise; a ceiling on what an operation may do |
| **collateral class** | One of C0, C1, C2, C3; the class of the effect a countermeasure has, which governs the approval depth required |
| **autonomy class** | One of AC-0 Manual, AC-1 Assisted, AC-2 Supervised, AC-3 Delegated, AC-4 Autonomous; how a countermeasure executes |
| **adversary AI** | An AI system, or an AI-mediated operation, conducting activity against the operator or the operator's estate |
| **AAT category** | One of AAT-1 to AAT-10; the behaviour-centred classification of adversary activity |
| **claim label** | One of Fact, Estimate, Interpretation, Hypothesis, Recommendation |
| **source reliability tier** | Rank 1 (highest) to 4 (lowest) |
| **verification status** | Verified (primary), Verified (secondary), Corrected, Unverified, Requires confirmation |
| **attribution confidence (c)** | The stated probability that activity is attributable to a specific adversary, in [0.0, 1.0] |
| **threat score (S)** | The prioritisation quantity S = L × I × A × V, ranging 0 to 20 |
| **effective threat (S_eff)** | S × c; the quantity the escalation ladder is applied to |
| **residual risk (R)** | S_eff × (1 − e); the risk carried forward after the selected countermeasures |
| **admissibility** | The conjunction of conditions AD-1 to AD-12 that a countermeasure must satisfy to be eligible for a card |
| **reversible / reversed / low / none** | The four-point reversibility scale used across the set, ordered from most to least reversible. A C0 countermeasure is *reversible* or *reversed*; a countermeasure whose reversibility is *none* is at C2 or above |
| **deconfliction** | The check that a countermeasure does not interfere with a live legitimate operation |
| **the error handler** | The single enforcement point to which every gate resolves |
| **the decision log** | The record of rationale, alternatives, and risk for each material decision |
| **the proving ground** | The exercise harness in which an adversary is simulated to validate detection and rehearse operators |
| **architectural assertion** | A statement of intended system behaviour that has not been independently substantiated |
| **author** | The named human accountable for a document in this set |
| **attribution note** | The closing statement naming the author and the supporting model |
| **the emergency posture** | The target state the operator drives towards when the operator's own deployment is suspected compromised, as distinct from the ROE profile in force |
| **operating posture** | The master design's term for the pair of situations the system operates in: the defensive posture, where the system is the object of the adversary's attention, and the counter-adversary posture, where it is acting against an identified adversary |
| **posture (platform sense)** | The platform architecture specification's term for the ROE profile ceiling in force, together with the current mission phase. "Revert to Observe" in this sense means R0 behaviour: passive collection only. Where a document uses *posture* in this sense and the master design's sense could also apply, the context determines which is meant, and the disambiguation is recorded here because the two senses are not the same thing |
| **zero-collateral pre-dispatch check** | One of the K-series checks that must all pass before a containment action is dispatched against a suspected-compromised deployment |
| **protected control set** | The subset of the operator's control path that must remain outside any containment action's blast radius, so that containment does not lock the operator out of their own estate |
| **pre-flight gate** | The mandatory mechanical check every containment dispatch passes before execution, verifying that the target resolves to exactly one instance-scoped resource owned by the compromised deployment and that it does not intersect the protected control set |
| **command authority** | The operator's standing authority to command the system and to stop any running action. Held by a named human; never revoked, downgraded, or transferred by the system |
| **kill verification** | The two-pass confirmation that a containment action actually terminated the target rather than merely appearing to |
| **re-entry criteria** | The conditions that must be satisfied before the operator returns a contained component to service |
| **integrity state** | The state of a data source, not of the observation it carried: one of trustworthy, degraded, stale, missing, or tampered-suspect |
| **source fidelity** | The degree to which a source can be relied upon to represent the thing it claims to represent |
| **admission control** | The check applied before a model, tool, plugin, or artefact is loaded, covering integrity, entitlement, and provenance |
| **credential broker** | The service that issues scoped, short-lived credentials to agents, so that an agent never holds a durable secret |
| **egress proxy** | The policy point through which all outbound traffic is mediated, defaulting to deny |
| **envelope** | The declared boundary within which a delegated action may be taken: target set, permitted action set, limits, window, and confidence floor |

---

## 4. Conventions Applied Across the Set

- **Requirement identifiers.** Objectives use `DO-`; engagement authorisation `AUTH-`; rules of engagement `ROE-`; constitutional conduct `CON-`; human-in-the-loop `HITL-`; evidence and claim labelling `EVD-`; operational workflow `OP-`; gates `GATE-`; error handler `ERR-`; mission lifecycle `ML-`; intelligence `INT-`; taxonomy `TAX-`; scoring `SCORE-`; admissibility `AD-`; decision support `DS-`; countermeasure rules `CM-`; detection `DET-`; containment `CTG-`; platform `INFRA-`; interface `WF-`, `WFP-`, `WFC-`; emergency protocol `ESC-`, `ZC-`, `PACE-`; measurement `MET-`; exercise `EX-`; limitations `LIM-` and the document-scoped limitation series.
- **Tables over prose** for enumerated taxonomies, class definitions, admissibility conditions, and checklists, so that each can be read independently of the surrounding narrative.
- **Defined terms are declared once per document** and referenced thereafter by the defined term rather than by repetition.
- **Verification status is disclosed.** Claims about system behaviour that have not been substantiated are labelled and carry a statement of what substantiation would require. This applies to the reference implementation as much as to the prose: the implementation is asserted to be conformant with the model, and the specific requirements it mechanically enforces are listed in `reference/audit-and-conformance-procedures.md` §3.
- **External mappings are recorded as unverified until checked.** Where a technique maps to a published external framework, the mapping carries a verification status and a date.
- **Unverified quantitative data is retained but marked.** Where a figure could not be matched to its primary source, the figure is retained with its status and the action required to resolve it, rather than deleted or silently confirmed.
- **No claim of the framework's own efficacy is stated in absolute terms.** Section 11 of the master design and `reference/audit-and-conformance-procedures.md` §8 record what the framework does not establish; §6 of that document holds the calibration programme, and §5 the replay procedure.
- **Authorship is declared.** See §7.

---

## 5. Identifier Registry

| Prefix | Count | Scope |
| --- | --- | --- |
| `DO-` | 14 | Design objectives — master design §2 |
| `AUTH-` | 8 | Engagement authorisation, scope, third-party exclusion |
| `ROE-` | 8 | ROE profiles, collateral classes, autonomy classes, reversibility — constitutional instrument |
| `CON-` | 14 | Constitutional conduct constraints — constitutional instrument |
| `HITL-` | 8 | Human-in-the-loop controls — conduct standard |
| `EVD-` | 8 | Operator evidence and claim labelling — conduct standard |
| `OP-` | 10 | Mission workflow and the Operation Card — master design; expanded by the mission lifecycle |
| `GATE-` | 8 | The gate requirements GATE-1 to GATE-8, for the gates G-1 Intake to G-8 Continuity — master design §8.1; expanded by the mission lifecycle |
| `ERR-` | 5 | Error handler — master design; expanded by the mission lifecycle |
| `ML-` | 12 | Mission lifecycle requirements — mission lifecycle document |
| `INT-` | 11 | Intelligence collection, classification, attribution, evidence |
| `TAX-` | 7 | Taxonomy and classification |
| `SCORE-` | 5 | Scoring and confidence model |
| `AD-` | 13 | Admissibility algebra — decision-support model |
| `DS-` | 12 | Decision-support requirements — decision-support model |
| `CM-` | 10 | Countermeasure class rules — countermeasure catalogue |
| `OCC-` | 43 | Individual countermeasures — countermeasure catalogue |
| `DET-` | 9 | Detection engineering — taxonomy document |
| `EX-` | 6 | Exercise and validation — taxonomy document |
| `CTG-` | 9 | Containment and agent isolation — platform architecture |
| `INFRA-` | 12 | Platform, control plane, resilience, data protection — platform architecture |
| `WF-` | 30 | Watchfloor interface capabilities and interface-level requirements — Watchfloor specification |
| `WFP-` | 16 | Watchfloor design principles — Watchfloor specification |
| `WFC-` | 8 | Watchfloor interface design constraints — master design §10.1 |
| `ESC-` | 89 | Emergency protocol requirements — emergency shutdown and containment protocol |
| `F-` | 32 | Technical audit findings — emergency protocol technical audit |
| `ZC-` | 14 | Zero-collateral isolation invariants — emergency protocol |
| `PACE-` | 7 | Pre-authorised containment envelope — emergency protocol |
| `ESL-` | — | Emergency severity ladder — emergency protocol |
| `MET-` | 14 | Measurement and evaluation — definitions in the audit procedures at its §7 |
| `AUD-` | 6 | Conformance assessment procedures — audit and conformance procedures |
| `AUT-` | 4 | Automation and self-reporting assessments — audit and conformance procedures |
| `TP-` | — | Technique profile records — AI attack technique library |
| `MAP-` | — | External mapping records — AI attack technique library |
| `LIB-` | — | Library conventions — AI attack technique library |
| `ORD-` | 10 | Countermeasure ordering rules — countermeasure catalogue |
| `HZ-` | 15 | Hazardous combination rules — countermeasure catalogue |
| `STK-` | 6 | Stack and combination rules — countermeasure catalogue |
| `RET-` | 12 | Retirement and withdrawal rules — countermeasure catalogue |
| `EVD-CC-` | 8 | Catalogue evidence rule — countermeasure catalogue |
| `AA-CC-` | 14 | Architectural assertions — countermeasure catalogue |
| `PL-` | — | Platform requirement families — platform architecture |
| `TZ-` | — | Trust zones — platform architecture |
| `TB-` | — | Trust boundaries — platform architecture |
| `SHA-` | — | Hash-chain and record integrity — platform architecture |
| `DIV-` | 3 | Recorded implementation divergences — decision-support model, now resolved |
| `LIM-` | 15 | Known limitations — master design §11 |
| `AAT-` | 10 categories, 77 techniques | Adversary AI taxonomy |
| `R0`–`R5` | 6 | Rules-of-engagement profiles |
| `C0`–`C3` | 4 | Collateral risk classes |
| `AC-0`–`AC-4` | 5 | Autonomy classes |
| `T0`–`T3` | 4 | Target classes — constitutional instrument §5.1 |
| `AT-0`–`AT-5` | 6 | Action tiers — emergency shutdown and containment protocol, Annex C |
| `CM-A`–`CM-G` | 7 | The seven countermeasure classes — countermeasure catalogue §4 |
| `ST-` | 4 | Source reliability tiers — the code's `SourceTier.ST1` to `SourceTier.ST4`; the documents describe them as ranks 1 to 4 |
| `ESL-1`–`ESL-4` | 4 | Emergency severity levels — emergency shutdown and containment protocol |
| `PF-1`–`PF-3` | 3 | The pre-flight gate's checks — emergency shutdown and containment protocol §6.1 |
| `K-1`–`K-16` | 16 | The collateral checklist — emergency shutdown and containment protocol §14.1 |
| `AMB-1`–`AMB-7` | 7 | Decision-support ambiguity families — decision-support and scoring model |
| `ARCH-1`–`ARCH-9` | 9 | Architectural assertions — adversary-AI taxonomy and threat model |
| `CAP-1`–`CAP-6` | 6 | Capability-profile entries — adversary-AI taxonomy and threat model |
| `TM-1`–`TM-9` | 9 | Threat-modelling procedure steps — adversary-AI taxonomy and threat model |
| `TV-1`–`TV-8` | 8 | Verification records — AI attack technique library |
| `LIVE-1`–`LIVE-2` | 2 | Deployed-context distinctions — decision-support and scoring model |
| `PROP-1` | 1 | Proposition families — decision-support and scoring model |
| `STEP-1`–`STEP-6` | 6 | The mission's phase steps — master design §8.1 |
| `F-1`–`F-32` | 32 | Technical-audit findings — the emergency protocol technical audit |
| `GC-1`–`GC-8` | 8 | **Referenced, not owned.** The Axiom Hive governance set's governing constraints — `../Docs/system-design-and-framework.md` |
| `CP-1`–`CP-2` | 2 | **Referenced, not owned.** The Axiom Hive governance set's core principles — `Docs/operational/axiom-hive-defensive-architecture.md` |

### Document-scoped limitation series

The `LIM-` row covers the master design's fourteen set-level limitations only. Each component document carries its own, so that a limitation is recorded where it arises and is not diluted by a single global list.

| Prefix | Count | Owner |
| --- | --- | --- |
| `LIM-C-` | 12 | Constitutional instrument |
| `LIM-CC-` | 12 | Operator conduct standard |
| `LIM-CAT-` | 13 | Countermeasure catalogue |
| `LIM-TC-` | 14 | Adversary AI taxonomy and threat model |
| `LIM-DS-` | 11 | Decision support and scoring model |
| `LIM-WF-` | 12 | Watchfloor interface specification |
| `LIM-PL-` | 11 | Platform architecture and agent containment |
| `LIM-ML-` | 12 | Mission lifecycle and decision loop |
| `LIM-AU-` | 14 | Audit and conformance procedures |
| `LIM-ESC-` | 13 | Emergency shutdown and containment protocol |

---

## 6. Change Control

| Change | Requires | Rationale |
| --- | --- | --- |
| A new or amended ROE profile | Executive + legal contact; amendment to the EA | A profile is a constitutional instrument |
| A change to a collateral class or autonomy class definition | Executive + legal contact | These determine the approval depth for every operation |
| A change to the admissibility algebra (AD-1 to AD-12) | Document owner + legal contact; versioning of the implementation | Admissibility is the enforcement surface of the authorisation model |
| A new countermeasure class | Document owner; legal review if it acts on the adversary's systems | Class determines the ceiling it may operate under |
| A change to the taxonomy categories | Document owner; taxonomy version recorded on every card | Cards depend on the taxonomy version in force |
| A change to the claim labels or source tiers | Synchronisation across every document that restates them | Inherited from the Axiom Hive set; see LIM-13 in the master design |

**Identifier hygiene.** Every identifier within this set is unique: one token, one meaning, one owner. The prefixes in §5 are registered in both this index and the master design's §9.1, and the two registries carry an identical prefix set. Uniqueness does **not** extend across the four document sets on the desktop — the governance set, the command-centre research set, and the counter-engagement research set each use tokens such as `AC-`, `CM-`, `C-`, `CP-`, `S-`, `R-`, `L-`, `D-`, `NG-` and `C0`–`C3` for their own purposes. A namespace scheme across all four sets is a precondition for any merger between them, and is not established. Where a new document needed a prefix that a peer had already taken, the new document took a longer, distinct prefix rather than a shared one, and the substitution is recorded in the document's own control table. The `WF-1` to `WF-8` series of the master design was renamed `WFC-1` to `WFC-8` at set revision 1.0, because `WF-1` and `WF-01` were one character apart and meant different things.

**Version rule.** Each document carries its own version. The set index records the set version. Where a card cites the framework version in force, it cites the set version and the specific document versions of the documents it relied upon.

---

## 7. Authorship and Attribution

No document in this set is authored by an AI system. Every document is the work of a named human author, prepared with the assistance of an AI system that is identified as such.

**Requirements**

1. Every document declares its author in its control table.
2. Every document closes with an attribution note.
3. The attribution note states the author, the supporting model, and the fact of support.
4. The same note closes every interaction in which the set is worked on.
5. Where a document carries text reproduced verbatim from supplied source material, that text is exempt from attribution editing and is not otherwise altered.
6. The reference implementation is likewise the work of the named human author, assisted as above. It is not claimed to have been written by an AI system acting independently.

**Note format**

> This was supported for MIA by Kilo (kilo-auto/free).

**Scope note.** The note records support, not authorship. It does not attribute the analytical judgements, the verification verdicts, or the normative requirements to the supporting model; those are the author's. Where a document makes a claim that has not been independently substantiated, the document says so, and the attribution note does not imply otherwise.

---

*This was supported for MIA by Kilo (kilo-auto/free).*
