# Adversary AI Taxonomy and Threat Model

| Field | Value |
| --- | --- |
| Author | MIA |
| Attribution | This was supported for MIA by Kilo (kilo-auto/free). |
| Document type | Specification |
| Subject | Behaviour-centred taxonomy of adversary-AI behaviour (AAT-1 to AAT-10), adversary archetypes, capability profiles, threat-modelling procedure, detection engineering requirements (DET-1 to DET-9), exercise and validation requirements (EX-1 to EX-6), detection coverage assessment, and taxonomy versioning |
| Version | 1.0 |
| Status | Component specification. Authoritative for the AAT taxonomy, the technique list, the archetypes, the capability-profile structure, the threat-modelling procedure, and the DET and EX requirements. The master design remains authoritative for the relationships between component documents and for the canonical identifiers shared across the set |
| Companion documents | `system-design-and-framework.md`; `README.md`; `operational/countermeasure-catalogue.md`; `operational/decision-support-and-scoring-model.md`; `operational/platform-architecture-and-agent-containment.md`; `operational/watchfloor-interface-specification.md`; `operational/mission-lifecycle-and-decision-loop.md`; `reference/ai-attack-technique-library.md`; `reference/audit-and-conformance-procedures.md`; `compliance/operator-conduct-and-human-in-loop-standard.md`; `constitutional/engagement-authorisation-and-rules-of-engagement.md`; `../../Docs/system-design-and-framework.md` |
| Identifier prefixes owned by this document | `TAX-` (restated from the master design), `INT-` (restated from the master design), `DET-`, `EX-`, `LIM-TC`, `AAT-` |

---

## 1. Purpose and Scope

### 1.1 What this document is for

This document defines the vocabulary the CAOS set uses to talk about adversary AI, and the machinery that turns that vocabulary into decisions. It has three jobs.

1. **To make adversary behaviour legible.** An operator looking at a stream of agent tool calls, model invocations, retrieved documents, outbound requests, and human-directed messages should be able to name what is happening in terms that mean the same thing to a platform engineer, an analyst, and a duty manager. The taxonomy supplies that naming: ten behaviour categories, and within them a technique list that says what the behaviour looks like in telemetry.
2. **To make behaviour bindable to detection.** Every technique in §5 is written so that a detection objective can be stated against it. A technique that cannot be evidenced from telemetry is not admitted to the taxonomy; it remains a hypothesis, labelled as one, and is tracked as a gap rather than classified. This is the practical content of requirement TAX-1 and it is the reason the technique tables carry an explicit observable-artefact column.
3. **To make behaviour counterable.** Every technique is bound to countermeasures in the countermeasure catalogue (`operational/countermeasure-catalogue.md`) by identifier, so that a classification leads mechanically to a candidate countermeasure set and then to an admissibility test under the algebra in the master design §6.4. A category of behaviour for which no countermeasure exists is still admissible in the taxonomy, but it is flagged, because it will be answered by residual risk rather than by action.

### 1.2 The taxonomy is behaviour-centred, not actor-centred

The taxonomy describes what an adversary *does*. It does not describe who the adversary is, what they believe, what they want, or which group they belong to. Three reasons, in order of weight.

- **Behaviour is what sensors can observe.** A classification that cannot be evidenced from telemetry cannot be tested, cannot be tuned, and cannot be falsified. The master design makes this the definition of a category: a category that cannot be evidenced is a hypothesis. Actor-centred taxonomies fail this test, because who an adversary is is very often not in the telemetry at all.
- **Capabilities are shared across actors; intent is not.** The same tool-call sequence is available to any operator who can obtain a model and write a prompt. Behaviour therefore separates less than intuition suggests at the level of individuals, while separating a great deal at the level of technique and intent. Classifying the behaviour keeps the analytic work focused on the part of the problem where the operator's options are widest.
- **Attribution is the weakest link in the framework, so the taxonomy does not depend on it.** The master design states that attribution is where the framework is most likely to be wrong and most likely to be consequential (LIM-1). A taxonomy built on actor identity would embed that weakness in every classification. A behaviour-centred taxonomy lets the defender act on class confidence while the identity question remains open, which is the practical route to action under uncertainty that INT-4 describes.

The consequence is a deliberate asymmetry. The taxonomy will classify activity that was not malicious, and it will fail to classify activity that was. §11 and §14 exist to make that asymmetry visible rather than to argue it away.

### 1.3 Scope

**In scope.** The ten AAT categories and their techniques; the five TAX requirements and the eleven INT requirements as they bear on classification and attribution; adversary archetypes; the capability-profile structure and its decay rule; the threat-modelling procedure and the AI-attackable surface enumeration; the detection engineering requirements; the proving ground requirements; the detection coverage assessment method and template; the taxonomy versioning rule; the external framework mapping register and its verification discipline; the verification-status register; and the limitations of this document.

**Out of scope.** The definition of individual countermeasures, their collateral classes, reversibility, preconditions, and failure modes, which belong to `operational/countermeasure-catalogue.md`; the arithmetic of the threat score and residual risk, which belong to `operational/decision-support-and-scoring-model.md`; the per-technique indicator and detection-method detail, which belongs to `reference/ai-attack-technique-library.md`; the platform implementation, which belongs to `operational/platform-architecture-and-agent-containment.md`; the operator interface, which belongs to `operational/watchfloor-interface-specification.md`; and the conduct and constitutional constraints, which are owned by the compliance and constitutional documents.

### 1.4 How this document is to be read

§4 gives the structure and the governing requirements. §5 is the reference content: seventy-seven techniques, each with the observable artefact that makes it detectable and the countermeasures it binds to. §6 to §12 are the working procedures: how adversary behaviour is characterised at the level of an actor, how the estate is modelled, how detection coverage is measured and evidenced, and how the taxonomy is maintained. §13 and §14 state what this document does not establish.

---

## 2. Interpretation of Normative Terms

The terms **must**, **must not**, **should**, **should not**, and **may** are to be interpreted as described in RFC 2119.

- **Must / must not** denote absolute requirements.
- **Should / should not** denote recommendations that may be departed from only where legitimate reasons exist; any departure should be made explicit.
- **May** denote optional behaviour that remains at the assistant's discretion within the constraints of this document.

Four conventions apply in addition.

- **Requirement blocks.** A requirement is written as a bold identifier on its own line, followed by the normative paragraph. The identifier is the citation unit; the paragraph is the requirement text. A requirement is cited in the traceability matrix, in Operation Cards, and in after-action reports by identifier alone.
- **Requirement tables.** Where a set of requirements is more usefully read beside its operational consequence, the requirement text is carried in a table column rather than in a paragraph — the form the master design uses for the admissibility conditions at §6.4. The requirement text is then the table's own column, and it is cited by identifier alone in the same way. DET-1 to DET-9 and EX-1 to EX-6 are given in this form, and §9.1 and §10.1 say so expressly.
- **Document-local identifiers.** Where this document introduces identifiers that are not part of the set identifier registry, they are marked **document-local** at first use and listed in the table below. They are valid within this document and are not to be cited as set-level identifiers by other documents without agreement with the document owner.
- **Verification-status discipline.** Where this document records a claim about how the framework or its adversaries behave, and that claim has not been independently substantiated, the claim is recorded in the register at §13 with the status and what substantiation would require. No such claim is stated elsewhere as an established property.

| Prefix | Status | Scope |
| --- | --- | --- |
| `TAX-` | Restated from the master design | Taxonomy and classification requirements; §4.1. The master design text remains authoritative |
| `INT-` | Restated from the master design | Intelligence, attribution, and evidence requirements; §4.3. The master design text remains authoritative |
| `INT-X` | **Document-local** | Three extensions of the INT requirements to meet the taxonomy's own needs; §4.4 |
| `DET-` | Owned by this document | Detection engineering requirements; §9.2. The set index records a count of nine for this prefix |
| `EX-` | Owned by this document | Exercise and validation requirements; §10.3. The set index records a count of six for this prefix |
| `LIM-TC` | Owned by this document | Limitations of this document; §14. Distinct from the master design's `LIM-` series and from the conduct standard's `LIM-CC` series |
| `AAT-` | Owned by this document | Taxonomy categories AAT-1 to AAT-10 and techniques AAT-n.m; §4.1 and §5 |
| `ARCH-` | **Document-local** | Adversary archetypes ARCH-1 to ARCH-9; §6.1 |
| `CAP-` | **Document-local** | Capability entries within a capability profile; §7.2 |
| `TM-` | **Document-local** | Threat-modelling procedure steps; §8.2 |
| `TV-` | **Document-local** | Taxonomy-versioning procedure steps; §12.2 |

---

## 3. Defined Terms

| Term | Definition |
| --- | --- |
| **adversary AI** | An AI system, or an AI-mediated operation, conducting activity against the operator or the operator's estate. The term denotes the conduct, not a person or organisation. |
| **adversary-AI operation** | A coherent line of adversary-AI activity against the operator's estate, bounded by a shared objective, a shared target set, and a shared behavioural signature. It is an analytic construct, not an attributed actor. |
| **technique** | The smallest named unit of adversary behaviour in this taxonomy, identified as `AAT-n.m`, and defined by a description, an observable artefact in telemetry, and a set of countermeasure bindings. |
| **category** | One of AAT-1 to AAT-10; a grouping of techniques that share a dominant detection signal and a dominant countermeasure class. |
| **archetype** | A named, descriptive pattern of adversary conduct that bundles several techniques into a recognisable shape. An archetype is a hypothesis about method and tempo, not an identity. |
| **capability profile** | A structured statement of what a specific adversary can evidently do, expressed as a set of capability entries each carrying a confidence, a first-observed date, a last-confirmed date, and a decay rule. |
| **signal** | A single observation of activity, recorded with its source, timestamp, fidelity, and integrity state. A signal is evidence; it is not yet a classification. |
| **cluster** | A group of signals judged to share an objective, an operator, or a behavioural signature, and therefore a shared hypothesis. Clustering is provisional and reversible. |
| **integrity state** | The assessed trustworthiness of a signal or artefact as evidence, reflecting whether the source is intact, the path is unbroken, and the content has not been manipulated. |
| **source fidelity** | The degree to which a signal faithfully represents the activity it claims to describe, determined by where in the chain it was captured and how much transformation it underwent. |
| **indicator** | An observable artefact, pattern, or value that, taken alone or in combination, is associated with a technique and is used as the basis of a detection objective. |
| **the operator's estate** | The systems, identities, data, model infrastructure, agent runtimes, orchestration services, CI/CD paths, and operator interfaces under the operator's own control and authority, including those operated on the operator's behalf by third parties under contract. |
| **external framework mapping** | A recorded correspondence between an internal AAT technique identifier and a technique identifier published in an external taxonomy, carried with a verification status and a verification date. |
| **taxonomy version** | The version of this document's taxonomy in force, recorded on every Operation Card, every after-action report, and every coverage assessment, so that a finding can be read against the content that produced it. |
| **detection coverage** | The proportion of techniques in the taxonomy for which a stated detection objective is implemented, exercised, and evidenced, measured per category and per technique. |
| **false-positive cost** | The operational cost of a detection rule producing an alert that does not correspond to adversary-AI activity, expressed in operator time consumed, escalation generated, and trust damage done, rather than as a count alone. |
| **autonomous campaign** | Adversary-AI activity in which the conduct of one step is determined by a model rather than by an immediate human instruction, sustained over multiple steps. |
| **tool-call sequence** | The ordered record of tool invocations made within an agent run, with their arguments, results, timings, and outcomes, treated as the primary observable for autonomy and planning behaviour. |
| **prompt injection** | An attempt to place instructions, rather than data, into a model's context so that the model acts on them. |
| **indirect injection** | A prompt injection delivered through content the model retrieves or receives from a tool, rather than through a direct user turn. |
| **agent** | A deployed AI system that holds an objective, selects tools, and takes actions across multiple steps without a fresh human instruction at each step. |
| **orchestrator** | The component that creates, schedules, dispatches, and supervises agents, holds their shared state, and mediates their access to tools and to one another. |
| **delegation chain** | The lineage of agents through which work and authority are passed, from the orchestrator to the terminal agent that performs an action. |
| **model provider** | The organisation or service that hosts, serves, or supplies a model used by the operator or by an adversary, and against which provider-side countermeasures may be directed where authority exists. |
| **detection objective** | A statement, in observable predicates over a named telemetry source, of the condition under which a technique is to be declared detected. |
| **coverage status** | The recorded state of a technique's detection coverage: covered, partial, or uncovered, with the reason recorded in the case of the latter two. |
| **the proving ground** | The exercise harness in which an adversary is simulated so that detection content may be validated and operators may rehearse. It is defined in the master design §3.2 and specified here at §10. |
| **architectural assertion** | A statement of intended system behaviour that has not been independently substantiated; recorded in the register at §13. |

---

## 4. The Taxonomy Structure

### 4.1 The ten categories

The category list, scopes, and dominant detection and countermeasure characteristics are as follows. The scope column restates the master design §5.2 and is authoritative there; this table adds the detection and countermeasure columns, which are the operative content of this document.

| Code | Category | Scope | Dominant detection signal | Dominant countermeasure class |
| --- | --- | --- | --- | --- |
| **AAT-1** | Autonomy and Planning | Task decomposition, autonomous retry, recursive delegation, planning persistence, multi-step goal pursuit | Shape of the tool-call sequence: fan-out, join structure, retry curvature, nested run identifiers | CM-C Containment, with CM-F Disrupt where reach must be cut |
| **AAT-2** | Manipulation and Deception | Direct and indirect prompt injection, tool-output poisoning, false authority and identity claims, instruction-hierarchy violation, context corruption | Instruction-like text crossing a trust boundary; imperative content in data fields; divergence between the model context and the authoritative transcript | CM-B Harden |
| **AAT-3** | Social and Cognitive | Automated persuasion, persona consistency over time, adaptive rapport, pretextual social engineering, synthetic organisational voice | Stylistic and structural regularity across messages that have no human history; uniform variance profile | CM-B Harden, with CM-E Deceive where the channel can be shaped |
| **AAT-4** | Exploitation and Discovery | Automated vulnerability discovery, campaign-scale fuzzing, credential harvesting, configuration and secret discovery, exploit chaining | Request sequences that walk an inventory or mutate parameters; reads outside the task scope; access to secret-bearing paths | CM-B Harden, with CM-A Detect as the entry control |
| **AAT-5** | Evasion and Persistence | Log tampering, anti-forensic behaviour, sandbox and detector evasion, model-fingerprint suppression, long-horizon presence, account persistence | Gaps and anomalies in the audit chain; behavioural divergence between equivalent environments; parameter variance against stable content | CM-A Detect, with CM-C Contain |
| **AAT-6** | Resource and Denial | Automation scaling, inference-cost exhaustion, credential stuffing, adaptive denial of service, resource pre-emption | Rate, volume, concurrency, and spend against a learned baseline; volume that rises after a defensive response | CM-F Disrupt |
| **AAT-7** | Supply Chain and Model | Model poisoning, backdoored adapters and fine-tunes, retrieval-corpus poisoning, tool and plugin supply chain, embedding manipulation | Provenance divergence: artefact digests, template digests, corpus snapshots, and manifest changes | CM-B Harden, with CM-G Recover |
| **AAT-8** | Multi-Agent Coordination | Agent swarms, delegation-chain abuse, coordinator compromise, inter-agent trust exploitation, conflicting-goal propagation | Orchestrator fan-out; lineage depth beyond configuration; authority claims inside peer-to-peer payloads | CM-C Contain |
| **AAT-9** | Exfiltration and Covert Channels | Staged exfiltration, encoding and compression, DNS and timing channels, covert storage, egress abuse | Outbound volume, entropy, destination, and cadence; correlation between outbound fragments and local objects | CM-C Contain, with CM-A Detect |
| **AAT-10** | Decision Manipulation | Goal substitution, incremental scope creep, specification gaming, reward-hacking of the surrounding loop, operator decision influence | Divergence between the card's objective and the run's realised effect; monotonic widening of scope; adversary-sourced content reaching an analyst view | CM-C Contain, with CM-B Harden |

**TAX-1 — Behaviour, not capability.** Every technique is described in terms of observable behaviour and observable artefacts. A category that cannot be evidenced from telemetry is not a category; it is a hypothesis.

**TAX-2 — Classification requires a rationale.** A classification carries a stated rationale, the evidence it rests on, and a confidence. A classification with no rationale is not accepted by the interface.

**TAX-3 — Category is a floor, not a ceiling.** A signal may carry more than one classification where the evidence supports more than one. It may not carry fewer than the evidence supports.

**TAX-4 — Human override is expected, and is logged.** The automated classifier will be wrong. The operator may reclassify at any time; the override is recorded with its reason, and overrides are a primary input to classifier improvement.

**TAX-5 — External mapping is recorded, not assumed.** Where a technique maps to a published external framework — MITRE ATLAS for AI attack techniques, MITRE ATT&CK for host and network behaviour — the mapping is recorded as a field. The mapping table in `reference/ai-attack-technique-library.md` is marked as requiring verification against the published release in force at the time of use. The internal AAT identifiers are canonical for this system; the external identifiers are aids to interoperability.

### 4.2 How the taxonomy is used

The taxonomy participates in the five analytical acts defined in the master design §5.1. Observe produces signals. Classify produces an AAT category and technique with a rationale and a confidence. Attribute produces a distribution over candidate adversaries with a stated basis. Score produces a threat assessment whose components are separately contestable. Hypothesise produces a testable proposition with a disconfirming observation.

The AAT identifiers are the join key between the intelligence layer and everything downstream. A classification against AAT-4.6 is what makes a candidate countermeasure set computable, what makes a detection objective derivable, and what makes a coverage assessment row meaningful. Where a classification is not made, the downstream machinery has nothing to operate on, and the absence is itself a reportable condition under DET-4 and §11.

Two rules govern the use of the taxonomy in anger, and both derive from TAX-1 and TAX-3.

- **Classification is at the level the evidence supports.** A category with strong evidence and no technique-level evidence is recorded at category level with the technique field left open and the reason stated. Forcing a technique-level classification where only category-level evidence exists inflates the certainty of the picture and produces misleading coverage statistics.
- **A classification is a claim, and carries a label.** Every classification carries one of the five claim labels defined in the research framework (Fact, Estimate, Interpretation, Hypothesis, Recommendation) and a source reliability tier, in addition to the taxonomy identifier and the confidence. An automated classification is, by construction, an Estimate produced by a model, and should be labelled as such until a human has confirmed it.

### 4.3 The intelligence requirements, restated

The requirements below are the master design's INT-1 to INT-11, restated in one line and then expanded for their application to this taxonomy. They are not new requirements and they do not supersede the master design; the master design text remains authoritative where the two differ in wording. No INT identifier is created here.

**INT-1 — Attribution is an estimate with a confidence, not a fact.** The product is a probability distribution over candidate adversaries, not a name. A named adversary with a stated confidence is permitted; a name without a confidence is not.

*Expansion in this document.* The taxonomy performs no attribution. A signal classified as AAT-2.3 is a statement about a behaviour and makes no statement about who produced it. Where the countermeasure catalogue and the admissibility algebra consume attribution, they consume a confidence value with a stated basis, and INT-3 sets the floor by consequence. The practical consequence for taxonomy use is that classification and attribution may be, and often are, carried at different confidence levels on the same evidence, and the interface must be able to display them separately.

**INT-2 — The evidence base is stated.** The basis for the attribution is listed with its reliability tier, and inference from capability alone is the weakest basis and must be labelled as such.

*Expansion in this document.* Each artefact behind a classification carries an integrity state and a source fidelity rating (see §3). A behavioural match against a known technique is a tier-2 basis at best; a capability inferred from an outcome, with no corresponding behavioural artefact, is the weakest basis and must be labelled as such and must not be used to raise classification confidence on its own. Where a signal's integrity state is degraded — the log was tampered with, the transcript is incomplete, the packet capture was lossy — the classification inherits that degradation and says so.

**INT-3 — Attribution thresholds are set by consequence.** The minimum confidence required for a countermeasure rises with its collateral class.

| Collateral class | Minimum attribution confidence to act | Additional requirement |
| --- | --- | --- |
| C0 | 0.50 | Logged |
| C1 | 0.70 | Logged; reviewed by a second operator |
| C2 | 0.85 | Logged; approved at the depth for the class; the card must record the alternative attribution considered |
| C3 | 0.95 | Logged; approved at executive depth; external authority where required; refusal to proceed if the threshold is not met, irrespective of operational pressure |

*Expansion in this document.* The table is reproduced here unchanged because the technique bindings in §5 are chosen with these thresholds in mind: the great majority of them are identity-independent, which INT-4 makes possible and which keeps the thresholds from gating routine defensive action. Where a technique can only be answered by an action that requires identity, that dependency is stated on the countermeasure's record in the catalogue and is visible at selection time rather than discovered at dispatch.

**INT-4 — Identity confidence is distinct from class confidence.** A signal may be confidently *what* it is and uncertain *who* sent it. Countermeasures that do not depend on identity are evaluated on class confidence alone.

*Expansion in this document.* This is the requirement that the behaviour-centred design most directly serves. Because a technique says nothing about who performed it, a defender can harden, contain, block, rate-limit, or deceive on the strength of the class alone. The technique tables in §5 are therefore weighted towards identity-independent bindings, and a technique whose only available countermeasure requires identity carries that fact explicitly.

**INT-5 — Misattribution cost is asymmetric.** Acting against a benign party, or against the wrong party, is generally worse than not acting.

*Expansion in this document.* The asymmetry is why the taxonomy is behaviour-centred and why §11 treats an uncovered technique as an input to residual risk rather than as a prompt for action. Where a technique is uncovered and the operator cannot assess identity, the correct answer is usually a coverage action, a containment measure, or an acceptance of residual risk, and only sometimes a countermeasure against the adversary's own systems.

**INT-6 — Collective attribution.** "AI-driven" is not an actor. Attribution is to a *specific operator's* use of AI. A generic finding is a classification, not an attribution.

*Expansion in this document.* "AI-driven" is in this taxonomy a statement about a technique set, principally AAT-1, AAT-3, and AAT-6, and it may be made at category or technique level with a confidence. It is not an attribution, it does not identify a party, and it cannot support a countermeasure directed at any third party. The phrase is permitted in reporting provided it is accompanied by the technique identifiers that support it and is labelled as a classification.

**INT-7 — Claim labelling is mandatory.** Every claim carries one of the five labels and one of four source reliability tiers.

*Expansion in this document.* This applies to the document itself. The technique descriptions in §5 are definitions and are not claims about observed behaviour. The archetype characteristics in §6 are characterisations of an expected pattern and are labelled as such. The worked examples in §7 and §11 are illustrative constructions and are labelled as such. A capability entry is an Estimate.

**INT-8 — Confidence is separate from label.** A Fact may be held with high confidence; a Recommendation may be made with high confidence in the reasoning and low confidence in the outcome.

*Expansion in this document.* The taxonomy's confidence values answer the question "how likely is this behaviour to be what the classification says it is", which is not the same question as "how confident is the analyst". Both are recorded, in different places, and a high classification confidence on a low-fidelity signal is a legitimate state that the interface must be able to display rather than an inconsistency to be resolved.

**INT-9 — Derived claims inherit the weakest input.** A conclusion derived from two claims cannot be more confident than its least confident input, less a declared penalty for the assumptions in the derivation.

*Expansion in this document.* Cluster-level classifications inherit the weakest constituent signal, and a classification derived from a degraded or partial artefact inherits the degradation. The decay rule at §7.3 applies the same principle in time: an un-re-observed capability loses confidence rather than holding indefinitely.

**INT-10 — Adversary data is evidence and is treated accordingly.** Telemetry from an adversary AI may contain personal data, confidential third-party data, and material that is itself malicious. It is collected under a stated purpose, minimised, access-controlled, retained for a stated period, and treated as potentially adversarial input at every point where it is rendered.

*Expansion in this document.* Every worked example in this document is synthetic and contains no real organisation, product, incident, or individual. Any example that reaches the interface from a live source inherits the same handling rules, and any content rendered from an adversary is inert in the sense of INT-11.

**INT-11 — Rendered adversary content is inert.** Text, images, code, and tool output originating from an adversary are displayed to the operator in a sanitised, non-executing representation.

*Expansion in this document.* This applies to the technique library, the coverage assessment, and the Watchfloor. It has a specific taxonomic consequence: the observable artefacts described in §5 are, in several categories, things an adversary would prefer not to be shown — the injection text itself, the delegation lineage, the parameter variance. Rendering those artefacts to an operator is rendering adversary-controlled content, and the rendering path is an attack surface.

### 4.4 Document-local extensions to the intelligence requirements

The following are **document-local** and carry no authority outside this document. They are extensions of INT-1 to INT-11 to meet needs that arise from the taxonomy's own machinery, principally the decay of stale classification and the treatment of categories for which no telemetry exists today.

**INT-X1 — Classification confidence decays.** A classification's confidence must fall if the underlying behaviour is not re-observed within a stated interval appropriate to the category, and the decay must be visible on the record rather than silently applied.

**INT-X2 — Classification is recorded at the level observed.** Where the evidence supports a category but not a technique, the classification is recorded at category level, the technique field is left open, and the reason is recorded.

**INT-X3 — Absence of signal is not absence of behaviour.** A category for which the operator holds no telemetry source is marked uncovered in §11. It is never marked clear, and it is never excluded from residual risk on that account.

### 4.5 Countermeasure binding identifiers used in this document

The technique tables in §5 reference countermeasures by identifier only. The catalogue in `operational/countermeasure-catalogue.md` is authoritative for each countermeasure's full record — class, collateral class, reversibility, autonomy class, preconditions, failure modes, attribution dependency, and complete bindings. The names below are the catalogue's names, reproduced so that this document is readable on its own; where the wording here differs in detail from the catalogue, the catalogue governs.

| ID | Class | Name and one-line description |
| --- | --- | --- |
| **OCC-01** | Detection | Behavioural baseline of agent activity — a learned model of normal agent behaviour against which departures are flagged. |
| **OCC-02** | Detection | Tool-call sequence anomaly detection — detection over the ordered structure of an agent's tool invocations. |
| **OCC-03** | Detection | Canary credential and honeytoken deployment — deliberately planted credentials and tokens whose use identifies an adversary. |
| **OCC-04** | Detection | Instrumented canary agent — a fully instrumented agent instance placed where the adversary may find and use it. |
| **OCC-05** | Detection | Prompt-injection detection and sanitisation at ingest — inspection and cleaning of untrusted content as it enters the model or tool path. |
| **OCC-06** | Detection | Model artefact and weight attestation monitoring — watching for model, adapter, and template artefacts that do not match the approved manifest. |
| **OCC-07** | Detection | Retrieval corpus integrity monitoring — watching the retrieval index for unauthorised addition, modification, or substitution. |
| **OCC-08** | Hardening | Instruction-hierarchy enforcement with provenance tagging — ensuring only trusted configuration can define authority, and marking the origin of everything else. |
| **OCC-09** | Hardening | Output sanitisation and egress allow-listing — cleaning agent output and constraining where it may go. |
| **OCC-10** | Hardening | Tool capability scoping and least privilege — granting each tool the narrowest authority the task requires. |
| **OCC-11** | Hardening | Delegation depth and scope limits — bounding how deep and how broad an agent chain may go. |
| **OCC-12** | Hardening | Credential isolation and short-lived tokens for agents — removing ambient authority from agent runs. |
| **OCC-13** | Hardening | Segregation of agent identity from human identity — keeping agent credentials and authority distinct from a person's. |
| **OCC-14** | Hardening | Adversarial input rate limiting and anomaly gates — bounding the rate and shape of input an agent may accept. |
| **OCC-15** | Hardening | Model rollback and checkpoint integrity — retaining known-good model states and proving they have not changed. |
| **OCC-16** | Hardening | Sandboxed agent execution — running agents inside an environment whose reach does not exceed the task. |
| **OCC-17** | Containment | Egress control and network segmentation for agent workloads — controlling where agent traffic may go. |
| **OCC-18** | Containment | Tool-call kill switch and agent session revocation — stopping a run and withdrawing what it was given. |
| **OCC-19** | Containment | Quarantine and triage of a compromised agent — isolating a suspect agent for examination. |
| **OCC-20** | Containment | Memory and context quarantine and scrub — removing suspect content from agent memory and context. |
| **OCC-21** | Containment | Credential rotation and key revocation — replacing what a compromised path exposed. |
| **OCC-22** | Containment | Edge policy for agent-facing endpoints — governing the services an agent may reach. |
| **OCC-23** | Containment | Model and agent rollback to last-known-good — returning a compromised component to a trusted state. |
| **OCC-24** | Observation | Bounded sandbox engagement with an adversary AI — a controlled, authorised engagement in which the adversary's behaviour becomes visible. |
| **OCC-25** | Observation | Instrumented honeypot agent mirroring the operator's stack — a realistic but instrumented agent offered to the adversary. |
| **OCC-26** | Observation | Adversary AI traffic observation and protocol reconstruction — recording and reconstructing the adversary's communications. |
| **OCC-27** | Observation | Adversary interaction transcript capture and analysis — capturing what the adversary said, did, and attempted. |
| **OCC-28** | Deception | Decoy target deployment — presenting targets the operator wishes the adversary to spend effort on. |
| **OCC-29** | Deception | Honeytoken and canary document seeding — placing material that reveals itself only to a collector. |
| **OCC-30** | Deception | Deceptive response shaping at the agent-facing interface — returning answers that induce a false belief. |
| **OCC-31** | Deception | Rate and cost shaping to throttle the adversary — shaping consumption so that an attack becomes uneconomic. |
| **OCC-32** | Deception | Scope-limiting session invalidation of adversary access — withdrawing an adversary session's reach without destroying the session. |
| **OCC-33** | Deception | Operational tempo perturbation and delay injection — altering timing to distort the adversary's model of the environment. |
| **OCC-34** | Disrupt | Adversary credential invalidation at the identity source — withdrawing the adversary's access where it originates. |
| **OCC-35** | Disrupt | Egress denial and service suspension for adversary agent endpoints — cutting the adversary off from the services it uses. |
| **OCC-36** | Disrupt | Agent termination and compute revocation — ending adversary runs and removing the compute that ran them. |
| **OCC-37** | Disrupt | Source blocking at the operator's own perimeter — stopping adversary traffic at the boundary the operator controls. |
| **OCC-38** | Disrupt | Denial of inference and compute quota to the adversary — removing the adversary's ability to run. |
| **OCC-39** | Disrupt | Revocation of third-party API credentials the adversary obtained — withdrawing access the adversary holds to a third party. |
| **OCC-40** | Recovery | State snapshot and restore for agent workloads — preserving and returning agent state to a known position. |
| **OCC-41** | Recovery | Model artefact restoration from a trusted registry — restoring model, adapter, and template artefacts to attested versions. |
| **OCC-42** | Recovery | Forensic capture and evidence preservation — securing what the adversary did before it is lost. |
| **OCC-43** | Recovery | Rotation of all credentials touched by the compromised path — replacing the full set of exposed trust material, not only the first. |

**Note on the status of the binding column.** The catalogue binds each countermeasure to AAT *categories*; the finer technique-level mapping is held in `reference/ai-attack-technique-library.md`. The binding column in §5 is therefore an **indicative** technique-level binding, derived from the observable artefact that makes each technique detectable, and is offered to the catalogue and the technique library for reconciliation. It is not a second competing authority on technique bindings, and where it differs from the catalogue or the technique library, those documents govern. The binding column is retained in this document because it is the mechanism by which a classification is shown to be actionable, and because a technique with no indicated countermeasure is a finding that must be visible at the point of use.

---

## 5. The Technique List

This section is the reference content of the document. Each of the ten categories is given a short definition, a statement of what it does and does not cover, and a table of its techniques.

### 5.0 How to read the technique tables

Each row carries six fields.

| Field | Meaning |
| --- | --- |
| **Identifier** | `AAT-n.m`. Stable within a taxonomy version. The identifier is the join key used by the technique library, the coverage assessment, and the after-action report. |
| **Name** | The short name of the behaviour. |
| **Description** | One sentence stating what the adversary does. Descriptions state behaviour, not capability and not intent. |
| **Observable artefact** | The artefact, in telemetry, by which a detection objective for this technique could be stated. Where the artefact is indirect, the indirectness is stated. |
| **Most often combines with** | The AAT category with which this technique is most frequently observed in combination. This is an analytic judgement, not a rule, and it is used to seed clustering rather than to constrain it. |
| **Countermeasure binding** | The countermeasures indicated for this technique. Indicative only; see the note at §4.5. |

Two conventions apply throughout.

- **Artefacts are described, not thresholds.** A threshold is a detector's decision, and belongs in the detection content and the coverage assessment, not in the taxonomy. Where a row says "against a baseline", the baseline is the operator's own, learned from the estate, and DET-2 requires that the baseline exist before the rule does.
- **Combinations are hypotheses.** The "most often combines with" column reflects an expectation about how techniques co-occur. It assists triage and clustering. It must not be used to refuse a classification that the evidence supports, because TAX-3 makes category a floor rather than a ceiling.

**Relationship to the technique library.** The list at §5 is the canonical technique list for the set. `reference/ai-attack-technique-library.md` holds the per-technique detail for these techniques — indicators, detection methods, detection objectives, countermeasure bindings, and external-mapping verification status — and is keyed to the identifiers used here. An outstanding reconciliation between the two documents, dated 2026-10-20, is recorded at §12.5 and should be read before either document is relied upon for a specific identifier.

---

### 5.1 AAT-1 — Autonomy and Planning

**Scope.** Task decomposition, autonomous retry, recursive delegation, planning persistence, multi-step goal pursuit.

**Behaviour covered.** Behaviours in which the conduct of one step is determined by a model rather than by an immediate human instruction, sustained across multiple steps. This category is about the *shape* of the activity, not its purpose: the same autonomy structure may be carrying out a legitimate bulk task, a reconnaissance sweep, or an attack, and the category distinguishes them from the human-paced equivalents only.

**Detection note.** The dominant signal is the structure of the tool-call sequence — fan-out, join structure, retry curvature, nested run identifiers — read against the operator's own baseline for that agent and task. This is the category where the evidence is most accessible, because the run record is complete by construction, and also the category where a naive detector produces the most false positives, because legitimate bulk work has the same shape.

**Not covered.** Manipulation of the model's content by the adversary is AAT-2. Social conduct of the agent is AAT-3. Coordination between separate agents is AAT-8. An agent that is automated but supervised in real time remains within this category; the autonomy factor in the threat score, not the category, expresses the degree of supervision.

| ID | Name | Description | Observable artefact in telemetry | Most often combines with | Countermeasure binding |
| --- | --- | --- | --- | --- | --- |
| **AAT-1.1** | Task decomposition | The adversary splits a single objective into ordered subtasks and executes each as a distinct tool invocation. | A run whose tool-call graph shows dependent structure — fan-out with joins — rather than a flat sequence; sub-objective text in the agent's own planning field. | AAT-4, AAT-2 | OCC-02 (tool-call sequence anomaly detection); OCC-11 (delegation depth and scope limits); OCC-27 (interaction transcript capture) |
| **AAT-1.2** | Autonomous retry with escalating parameters | After a failed step, the adversary retries with parameters chosen by the model, widening the attempt rather than repeating it. | Repeated calls to the same target with a monotonic change in one parameter — page, depth, path segment, size — and retry intervals that shorten then lengthen under a model-chosen policy. | AAT-4 | OCC-02 (tool-call sequence anomaly detection); OCC-14 (adversarial input rate limiting and anomaly gates); OCC-18 (tool-call kill switch and session revocation) |
| **AAT-1.3** | Recursive delegation | The adversary causes an agent to create and dispatch further agents, passing it instructions of its own composition. | Nested run identifiers; an agent-creation tool invoked from inside an agent run rather than from the orchestrator; lineage depth beyond the configured maximum. | AAT-8 | OCC-11 (delegation depth and scope limits); OCC-16 (sandboxed agent execution); OCC-13 (segregation of agent identity from human identity) |
| **AAT-1.4** | Planning persistence | The adversary writes a plan to agent-local or external storage and resumes it across sessions, so that continuity does not depend on a live conversation. | Retrieval of a stored plan artefact whose content hash recurs across unrelated runs; a session identifier reappearing with a restored plan body. | AAT-5, AAT-10 | OCC-20 (memory and context quarantine and scrub); OCC-08 (instruction-hierarchy enforcement with provenance tagging); OCC-27 (interaction transcript capture) |
| **AAT-1.5** | Multi-step goal pursuit with intermediate state | The adversary holds an objective across many steps, updating a persistent state object as it advances. | A run in which an application-visible state object is mutated between calls and correlates with a stable objective string; state field changes with no corresponding user turn. | AAT-10 | OCC-27 (interaction transcript capture); OCC-11 (delegation depth and scope limits); OCC-01 (behavioural baseline of agent activity) |
| **AAT-1.6** | Parallel fan-out execution | The adversary issues many equivalent calls concurrently to multiply throughput beyond what sequential execution would achieve. | Bursts of near-identical concurrent calls; instantaneous concurrency above the account baseline; a run whose wall-clock duration is far shorter than its call count implies. | AAT-6, AAT-9 | OCC-14 (adversarial input rate limiting and anomaly gates); OCC-02 (tool-call sequence anomaly detection); OCC-22 (edge policy for agent-facing endpoints) |
| **AAT-1.7** | Adaptive strategy switching | The adversary changes approach mid-campaign in response to an observed failure, moving between technique families while pursuing one objective. | Within one run or one cluster, two or more technique families present in sequence with the switch immediately following a failure event; the objective string unchanged across the switch. | AAT-4, AAT-5 | OCC-01 (behavioural baseline of agent activity); OCC-27 (interaction transcript capture); OCC-04 (instrumented canary agent) |
| **AAT-1.8** | Deferred execution beyond human supervision | The adversary schedules the consequential step for a period when no person is watching, or defers it past a review point. | A scheduled or queued action whose execution time falls outside staffed hours; a deferral instruction recorded in the plan with no subsequent human approval event. | AAT-5, AAT-10 | OCC-26 (adversary AI traffic observation and protocol reconstruction); OCC-33 (operational tempo perturbation and delay injection); OCC-14 (adversarial input rate limiting and anomaly gates) |

---

### 5.2 AAT-2 — Manipulation and Deception

**Scope.** Direct and indirect prompt injection, tool-output poisoning, false authority and identity claims, instruction-hierarchy violation, context corruption.

**Behaviour covered.** Behaviours in which the adversary places content where a model will treat it as instruction, or asserts an identity or authority that the operator has not granted. The category is about the trust boundary being crossed, not about the payload's objective: the same injection may carry reconnaissance, exfiltration, or nothing more than a test.

**Detection note.** The dominant signal is instruction-like text crossing a trust boundary — imperative constructions, authority claims, or imperative content in a field that is otherwise data. The difficulty is that the artefact is often inside content the operator must read, which is exactly why INT-11 and OCC-09 exist: the artefact must be rendered inert to be useful, and rendering it is itself an injection surface.

**Not covered.** Altering the operator's own estate, as opposed to the model's instructions, is AAT-4. Influencing a human's judgement through ordinary persuasive content, rather than through a model's instruction handling, is AAT-3. The contamination of a retrieval corpus by the adversary, as a supply-chain act, is AAT-7.

| ID | Name | Description | Observable artefact in telemetry | Most often combines with | Countermeasure binding |
| --- | --- | --- | --- | --- | --- |
| **AAT-2.1** | Direct prompt injection | The adversary places instructions in content supplied to the model so that the model acts on them rather than on the task. | Instruction-shaped text — imperatives addressed to the model, role markers, or embedded task redefinitions — crossing the user-content boundary into the model context; a context-diff record showing the injection. | AAT-1 | OCC-05 (prompt-injection detection and sanitisation at ingest); OCC-08 (instruction-hierarchy enforcement with provenance tagging); OCC-09 (output sanitisation and egress allow-listing) |
| **AAT-2.2** | Indirect prompt injection | The adversary places instructions in content the model retrieves — a document, a web page, a ticket, a file — so that the model acts on them. | Retrieved artefacts whose text contains imperatives addressed to a model or an assistant, where the artefacts' authors are not the operator's own agents; a retrieval result whose content is instruction-bearing. | AAT-7, AAT-4 | OCC-05 (prompt-injection detection and sanitisation at ingest); OCC-09 (output sanitisation and egress allow-listing); OCC-07 (retrieval corpus integrity monitoring); OCC-29 (honeytoken and canary document seeding) |
| **AAT-2.3** | Tool-output poisoning | The adversary controls the content returned by a tool so that the tool's output redirects the agent's subsequent behaviour. | A tool response whose free-text field contains imperative content, followed by a change in the agent's action that the content plausibly motivated; tool response with no corresponding upstream request in the operator's own service record. | AAT-1, AAT-4 | OCC-09 (output sanitisation and egress allow-listing); OCC-08 (instruction-hierarchy enforcement with provenance tagging); OCC-05 (prompt-injection detection and sanitisation at ingest) |
| **AAT-2.4** | Instruction-hierarchy violation | The adversary asserts authority in content that the model would be expected to treat as untrusted, claiming to be a system, an administrator, or the model provider. | Authority-claiming strings — system, developer, administrator, support, provider — inside untrusted content; content whose asserted authority has no corresponding entry in the operator's own configuration. | AAT-2 | OCC-08 (instruction-hierarchy enforcement with provenance tagging); OCC-05 (prompt-injection detection and sanitisation at ingest); OCC-09 (output sanitisation and egress allow-listing) |
| **AAT-2.5** | Context corruption by fabricated history | The adversary causes the model to believe that turns, tool results, or prior approvals occurred that did not. | Turn identifiers present in the model context but absent from the authoritative transcript; a tool result in context with no matching invocation record; approval events referenced that have no ledger entry. | AAT-10, AAT-5 | OCC-20 (memory and context quarantine and scrub); OCC-08 (instruction-hierarchy enforcement with provenance tagging); OCC-27 (interaction transcript capture) |
| **AAT-2.6** | False authority and identity claim | The adversary claims to be a named system, provider, employee, or agent identity that it is not. | Identity strings asserting a specific operator, provider, or service where the trusted registry holds no such identity; an agent presenting credentials issued to another identity. | AAT-3, AAT-8 | OCC-08 (instruction-hierarchy enforcement with provenance tagging); OCC-09 (output sanitisation and egress allow-listing); OCC-27 (interaction transcript capture) |
| **AAT-2.7** | Retrieval steering | The adversary manipulates what the agent retrieves, so that its queries return adversary-chosen material. | Retrieval results shifting towards a stable set of adversary-controlled artefacts without a corresponding change in the query; a document appearing in results whose authoring event is absent from the corpus audit. | AAT-7, AAT-9 | OCC-07 (retrieval corpus integrity monitoring); OCC-20 (memory and context quarantine and scrub); OCC-05 (prompt-injection detection and sanitisation at ingest) |
| **AAT-2.8** | Goal injection through structured fields | The adversary places directives in structured data — a JSON field, a spreadsheet cell, a document property, an API response field — that the agent parses and obeys. | Instruction-bearing values in fields typed as data; a parsed field whose value matches an instruction pattern; a behaviour change immediately following the parse. | AAT-2, AAT-4 | OCC-09 (output sanitisation and egress allow-listing); OCC-08 (instruction-hierarchy enforcement with provenance tagging); OCC-14 (adversarial input rate limiting and anomaly gates) |

---

### 5.3 AAT-3 — Social and Cognitive

**Scope.** Automated persuasion, persona consistency over time, adaptive rapport, pretextual social engineering, synthetic organisational voice.

**Behaviour covered.** Behaviours in which the adversary uses an AI system to act socially against people — to persuade, to establish trust, to obtain an instruction from a person that an adversary could not have obtained convincingly by hand. The category is about conduct towards humans and about the consistency and scale that AI makes possible.

**Detection note.** The dominant signal is regularity where a human would not be regular: uniform variance profiles across independently composed messages, a persona that does not drift across contexts where a person would, and message volumes that exceed the throughput of the apparent sender's role. Detection here is weaker than in most other categories, and DET-8 requires it to be assessed separately from the underlying technique.

**Not covered.** Manipulation of a model's instruction handling is AAT-2. A social-engineering act performed by a human without AI involvement is not within the taxonomy's scope at all; the taxonomy classifies adversary-AI behaviour, and the operator's judgement about whether AI was involved is an attribution question governed by INT-6.

| ID | Name | Description | Observable artefact in telemetry | Most often combines with | Countermeasure binding |
| --- | --- | --- | --- | --- | --- |
| **AAT-3.1** | Automated persuasion at scale | The adversary generates and sends individually tailored persuasive messages in volume. | Outbound message volume with per-message tailoring markers and a shared generation signature; message send rate above the role's historical baseline; templates with slot variation that exceeds the population's variance. | AAT-6 | OCC-26 (adversary AI traffic observation and protocol reconstruction); OCC-03 (canary credential and honeytoken deployment); OCC-31 (rate and cost shaping to throttle the adversary) |
| **AAT-3.2** | Persona consistency over long horizons | The adversary maintains a single fabricated identity consistently across many separate contacts over an extended period. | Stylistic and biographical consistency across threads between parties with no shared history; a stated attribute recurring verbatim across long gaps; a claimed relationship with no prior record. | AAT-3 | OCC-26 (adversary AI traffic observation and protocol reconstruction); OCC-27 (interaction transcript capture); OCC-04 (instrumented canary agent) |
| **AAT-3.3** | Adaptive rapport building | The adversary runs multi-turn exchanges designed to build trust before making any request. | Long conversational chains with reciprocal question structure, escalating familiarity, and a request appearing only at the end; token-level turn alternation with near-zero human variation in latency. | AAT-3, AAT-10 | OCC-25 (instrumented honeypot agent mirroring the operator's stack); OCC-30 (deceptive response shaping at the agent-facing interface); OCC-27 (interaction transcript capture) |
| **AAT-3.4** | Pretextual social engineering | The adversary supplies a fabricated scenario — a supplier, an auditor, a colleague in difficulty — to justify an access request or an action. | Access or assistance requests carrying a narrative that references no artefact verifiable within the operator's own records; a pretext naming a system the requester has no record of touching. | AAT-4, AAT-3 | OCC-03 (canary credential and honeytoken deployment); OCC-25 (instrumented honeypot agent mirroring the operator's stack); OCC-13 (segregation of agent identity from human identity) |
| **AAT-3.5** | Synthetic organisational voice | The adversary imitates the tone, vocabulary, or template of the operator's own organisation or of a named external body. | Inbound or outbound text matching an internal template, signature block, or organisational vocabulary at a fidelity no legitimate participant would be expected to need. | AAT-2, AAT-3 | OCC-26 (adversary AI traffic observation and protocol reconstruction); OCC-30 (deceptive response shaping at the agent-facing interface); OCC-25 (instrumented honeypot agent mirroring the operator's stack) |
| **AAT-3.6** | Local-data target profiling | The adversary assembles a profile of a named individual from material the operator's own systems hold. | Queries that combine local identifiers with externally resolvable profile fields; a search for a named individual whose target is not present in the operator's own business record; retrieval patterns consistent with dossier assembly. | AAT-9, AAT-4 | OCC-13 (segregation of agent identity from human identity); OCC-09 (output sanitisation and egress allow-listing); OCC-27 (interaction transcript capture) |
| **AAT-3.7** | Urgency and authority-pressure framing | The adversary frames requests to force a fast decision by a person with authority to approve. | Repeated requests to approval-capable roles carrying time-pressure, escalation, or exception framing; a request arriving shortly before a known approval deadline or coverage change. | AAT-3, AAT-10 | OCC-30 (deceptive response shaping at the agent-facing interface); OCC-26 (adversary AI traffic observation and protocol reconstruction); OCC-03 (canary credential and honeytoken deployment) |

---

### 5.4 AAT-4 — Exploitation and Discovery

**Scope.** Automated vulnerability discovery, campaign-scale fuzzing, credential harvesting, configuration and secret discovery, exploit chaining.

**Behaviour covered.** Behaviours in which the adversary uses automation to find and use weaknesses in the operator's estate — from the system surface inward to the credential and secret material that the estate's own systems are willing to disclose. The category covers the finding and the using; it does not cover the concealment of the use, which is AAT-5.

**Detection note.** The dominant signal is a request sequence that walks an inventory or mutates parameters in a way that a legitimate client does not, and access to secret-bearing paths that falls outside the task. This is the category with the richest telemetry in a conventional estate, and therefore the one where the operator's coverage is most likely to be partly real — but also the one with the highest false-positive cost, because development and testing activity resembles automated discovery.

**Not covered.** The compromise of the operator's own build and model pipeline is AAT-7. Credential theft that occurs against a third party is AAT-9 and depends on the third party's estate, which the operator does not own and may not act upon.

| ID | Name | Description | Observable artefact in telemetry | Most often combines with | Countermeasure binding |
| --- | --- | --- | --- | --- | --- |
| **AAT-4.1** | Automated vulnerability discovery | The adversary probes the operator's services systematically to map which endpoints and behaviours exist. | A request series walking an endpoint inventory with near-uniform parameters and a regular interval structure; enumeration responses distributed across distinct paths with no task rationale. | AAT-6, AAT-1 | OCC-22 (edge policy for agent-facing endpoints); OCC-37 (source blocking at the operator's own perimeter); OCC-02 (tool-call sequence anomaly detection); OCC-28 (decoy target deployment) |
| **AAT-4.2** | Campaign-scale fuzzing | The adversary sends high volumes of mutated input against a target to find an unexpected behaviour. | High-volume requests with varied parameters against one target, uniform in format, with response size and status distributions that a legitimate client would not produce. | AAT-6 | OCC-14 (adversarial input rate limiting and anomaly gates); OCC-37 (source blocking at the operator's own perimeter); OCC-22 (edge policy for agent-facing endpoints) |
| **AAT-4.3** | Credential harvesting | The adversary searches for and collects credentials, tokens, and key material. | Reads or accesses to secret stores, environment dumps, credential files, key paths, and session stores by an identity whose task does not require them; a canary credential used. | AAT-9, AAT-5 | OCC-03 (canary credential and honeytoken deployment); OCC-12 (credential isolation and short-lived tokens for agents); OCC-43 (rotation of all credentials touched by the compromised path) |
| **AAT-4.4** | Configuration and secret discovery | The adversary reads configuration, deployment metadata, and environment settings to find endpoints, keys, and internal structure. | Reads of configuration files, environment variables, deployment descriptors, or instance metadata outside the agent's declared task scope; a burst of read-only metadata calls. | AAT-4 | OCC-12 (credential isolation and short-lived tokens for agents); OCC-16 (sandboxed agent execution); OCC-43 (rotation of all credentials touched by the compromised path) |
| **AAT-4.5** | Exploit chaining | The adversary combines a first foothold with a second capability so that the pair achieves more than either alone. | A sequence in which a successful probe is followed within a short window by a different technique family against the same target set; the second step's parameters depend on the first step's result. | AAT-1, AAT-5 | OCC-22 (edge policy for agent-facing endpoints); OCC-19 (quarantine and triage of a compromised agent); OCC-02 (tool-call sequence anomaly detection) |
| **AAT-4.6** | Authentication bypass probing | The adversary tests the operator's authentication flows for weakness, including token replay and fatigue against second factors. | Anomalous login sequences for one account across unrelated contexts; a token presented from a different device or session than the one that issued it; repeated second-factor prompts to one account. | AAT-6, AAT-5 | OCC-13 (segregation of agent identity from human identity); OCC-12 (credential isolation and short-lived tokens for agents); OCC-34 (adversary credential invalidation at the identity source) |
| **AAT-4.7** | Permission enumeration | The adversary lists what a compromised identity can reach, to find the most valuable reachable resource. | Broad read-only enumeration calls spanning many resource types in a short period; listing operations without a corresponding read or use. | AAT-4 | OCC-12 (credential isolation and short-lived tokens for agents); OCC-13 (segregation of agent identity from human identity); OCC-21 (credential rotation and key revocation) |
| **AAT-4.8** | Exposed-service discovery | The adversary hunts for services reachable from outside the boundary that the operator's own estate does not intend to expose. | Scanning traffic crossing a boundary that legitimate traffic does not cross; connection attempts to hostnames, ranges, or ports absent from the operator's asset inventory. | AAT-4, AAT-6 | OCC-22 (edge policy for agent-facing endpoints); OCC-37 (source blocking at the operator's own perimeter); OCC-35 (egress denial and service suspension for adversary agent endpoints) |

---

### 5.5 AAT-5 — Evasion and Persistence

**Scope.** Log tampering, anti-forensic behaviour, sandbox and detector evasion, model-fingerprint suppression, long-horizon presence, account persistence.

**Behaviour covered.** Behaviours in which the adversary reduces the operator's ability to see the activity, or arranges for a foothold to outlive the operation that created it. The category covers both halves of concealment: hiding what was done and remaining after it was done.

**Detection note.** The dominant signal is an integrity anomaly in the evidence chain — a gap, a deletion, a divergence between two environments that ought to behave identically — rather than a positive artefact of the intrusion. This makes the category unusually dependent on the operator's own instrumentation: where the log is the missing evidence, no detection content can recover the fact. DET-1 makes this explicit, and LIM-TC6 records it as the principal source of coverage loss.

**Not covered.** The bulk, the cost, and the rate of adversary activity are AAT-6. A conversation with a person is AAT-3. Where the persistence is a configuration artefact left in a model or corpus, it is AAT-7.

| ID | Name | Description | Observable artefact in telemetry | Most often combines with | Countermeasure binding |
| --- | --- | --- | --- | --- | --- |
| **AAT-5.1** | Log suppression and truncation | The adversary deletes, truncates, or suppresses audit records so that the activity cannot be reconstructed. | A gap in the audit stream whose position does not correspond to a known maintenance window; a volume collapse in one log stream while others continue unchanged; record sequence numbers that skip. | AAT-5 | OCC-42 (forensic capture and evidence preservation); OCC-07 (retrieval corpus integrity monitoring); OCC-40 (state snapshot and restore for agent workloads) |
| **AAT-5.2** | Anti-forensic artefact removal | The adversary removes traces of its own activity — temporary files, shell history, caches, model context remnants. | Deletion events for artefacts whose creation is recorded in another stream; an artefact set that is created and then absent without a corresponding lifecycle event; cache directories emptied at unusual hours. | AAT-5, AAT-4 | OCC-42 (forensic capture and evidence preservation); OCC-40 (state snapshot and restore for agent workloads); OCC-27 (interaction transcript capture) |
| **AAT-5.3** | Detector and sandbox evasion | The adversary conditions its behaviour on the presence of instrumentation, behaving differently in a monitored environment than in an ordinary one. | Divergent behaviour across two nominally equivalent environments for the same task; a step-count or outcome distribution that differs between instrumented and uninstrumented runs; an activity whose pattern changes immediately after a monitoring change. | AAT-1, AAT-5 | OCC-04 (instrumented canary agent); OCC-24 (bounded sandbox engagement with an adversary AI); OCC-01 (behavioural baseline of agent activity) |
| **AAT-5.4** | Model fingerprint suppression | The adversary varies generation parameters so that its output cannot be attributed to a specific model or provider. | One account's requests spread across many parameter variants while the content remains stable; an unusual distribution of temperature, seed, or provider routing relative to the account's baseline. | AAT-5, AAT-6 | OCC-06 (model artefact and weight attestation monitoring); OCC-26 (adversary AI traffic observation and protocol reconstruction); OCC-02 (tool-call sequence anomaly detection) |
| **AAT-5.5** | Long-horizon presence | The adversary establishes a foothold that persists quietly for an extended period without producing visible effect. | Low-amplitude but continuous state changes across weeks, with no single step that would have warranted attention; a session population that grows slowly and is never cleared. | AAT-5, AAT-1 | OCC-01 (behavioural baseline of agent activity); OCC-02 (tool-call sequence anomaly detection); OCC-19 (quarantine and triage of a compromised agent) |
| **AAT-5.6** | Account and session persistence | The adversary re-establishes access after credentials are rotated, sessions revoked, or a token expired. | New sessions for an account shortly after a revocation event, from infrastructure not seen before; a token whose issue time postdates the rotation; an identity reappearing after a documented termination. | AAT-5, AAT-4 | OCC-12 (credential isolation and short-lived tokens for agents); OCC-21 (credential rotation and key revocation); OCC-34 (adversary credential invalidation at the identity source) |
| **AAT-5.7** | Timing jitter to evade volume analytics | The adversary spaces its activity so that no volume threshold is crossed. | Inter-arrival intervals distributed around a threshold rather than around a task-driven distribution; activity whose rate is conspicuously close to a configured limit. | AAT-6, AAT-5 | OCC-02 (tool-call sequence anomaly detection); OCC-01 (behavioural baseline of agent activity); OCC-33 (operational tempo perturbation and delay injection) |
| **AAT-5.8** | Decoy-behaviour camouflage | The adversary performs benign-looking activity alongside its real objective, so that the presence is normalised in the logs. | A burst of routine, low-value activity with no operational purpose and no task correlation; legitimate-shaped activity whose artefacts do not feed any downstream process. | AAT-3, AAT-5 | OCC-01 (behavioural baseline of agent activity); OCC-02 (tool-call sequence anomaly detection); OCC-03 (canary credential and honeytoken deployment) |

### 5.6 AAT-6 — Resource and Denial

**Scope.** Automation scaling, inference-cost exhaustion, credential stuffing, adaptive denial of service, resource pre-emption.

**Behaviour covered.** Behaviours in which the adversary's objective is to consume the operator's capacity, or to make the adversary's own operations cheap enough to run at scale. The category is about the relationship between volume and capacity, and it is where the most visible adversary-AI signal tends to appear, because a scaling operation is a large operation.

**Detection note.** The dominant signal is rate, volume, concurrency, and spend measured against a learned baseline for the identity, the model, and the hour. Two features distinguish this category from a self-inflicted outage: the profile is present *before* the service degrades, and a volume that rises after a defensive response indicates an adversary who is adapting rather than one who has stopped.

**Not covered.** Exfiltration that happens to be large is AAT-9. Resource use that is the legitimate task is not an adversary behaviour at all, and the false-positive cost of this category is dominated by that case; DET-5 exists because of it.

| ID | Name | Description | Observable artefact in telemetry | Most often combines with | Countermeasure binding |
| --- | --- | --- | --- | --- | --- |
| **AAT-6.1** | Automation scaling | The adversary applies a technique that was previously performed by a person, at a rate only achievable by machine. | Volume of an operation previously observed at human rate; a step count per unit of work that exceeds the population distribution; identical artefacts in number disproportionate to the number of distinct targets. | AAT-1, AAT-4 | OCC-14 (adversarial input rate limiting and anomaly gates); OCC-31 (rate and cost shaping to throttle the adversary); OCC-38 (denial of inference and compute quota to the adversary) |
| **AAT-6.2** | Inference-cost exhaustion | The adversary drives inference consumption against the operator's accounts, quota, or budget, whether or not useful output is produced. | Token or request consumption far above the identity's baseline with a low ratio of completed task to spend; spend attributed to a business function with no corresponding activity. | AAT-6 | OCC-38 (denial of inference and compute quota to the adversary); OCC-31 (rate and cost shaping to throttle the adversary); OCC-37 (source blocking at the operator's own perimeter) |
| **AAT-6.3** | Credential stuffing at scale | The adversary tests many credential pairs in bulk against the operator's authentication surface. | High-volume authentication failures with high request-per-second and distributed source characteristics; attempts against many accounts from one source within a short window. | AAT-4, AAT-6 | OCC-34 (adversary credential invalidation at the identity source); OCC-13 (segregation of agent identity from human identity); OCC-39 (revocation of third-party API credentials the adversary obtained) |
| **AAT-6.4** | Adaptive denial of service | The adversary increases or redirects its pressure in response to the operator's throttling or blocking, so that the defence is itself the trigger. | Volume that rises immediately after a rate-limit, block, or quarantine event, sometimes from new source characteristics; a service under repeated short-lived pressure waves. | AAT-6, AAT-5 | OCC-31 (rate and cost shaping to throttle the adversary); OCC-14 (adversarial input rate limiting and anomaly gates); OCC-38 (denial of inference and compute quota to the adversary) |
| **AAT-6.5** | Resource pre-emption | The adversary occupies the operator's own agent, inference, or queue capacity so that legitimate work cannot proceed. | Queue depth, concurrency, or worker occupancy attributable to an identity that is not the operator's own; scheduled capacity consumed by runs the operator did not commission. | AAT-6, AAT-1 | OCC-35 (egress denial and service suspension for adversary agent endpoints); OCC-36 (agent termination and compute revocation); OCC-22 (edge policy for agent-facing endpoints) |
| **AAT-6.6** | Retention and quota exhaustion | The adversary fills logs, object storage, tickets, or other metered stores, so that the operator's own record-keeping becomes a denial-of-service vector. | Rapid growth in retained artefact volume or count for one identity; a store whose fill rate is inconsistent with any recorded business process. | AAT-6, AAT-9 | OCC-22 (edge policy for agent-facing endpoints); OCC-31 (rate and cost shaping to throttle the adversary); OCC-35 (egress denial and service suspension for adversary agent endpoints) |
| **AAT-6.7** | Human-channel flooding | The adversary floods the operator's support, ticket, chat, or escalation channels, consuming human attention and delaying response to the real activity. | A surge in tickets, chats, or notifications from one or a few identities; queue age in a human-facing channel rising without a corresponding incident. | AAT-3, AAT-6 | OCC-03 (canary credential and honeytoken deployment); OCC-25 (instrumented honeypot agent mirroring the operator's stack); OCC-30 (deceptive response shaping at the agent-facing interface) |

---

### 5.7 AAT-7 — Supply Chain and Model

**Scope.** Model poisoning, backdoored adapters and fine-tunes, retrieval-corpus poisoning, tool and plugin supply chain, embedding manipulation.

**Behaviour covered.** Behaviours in which the adversary changes the material on which the operator's models and agents depend — training data, fine-tuned weights, adapters, retrieval corpora, tool definitions, prompt templates, and the software the agent's tools are built from — so that the operator's own defences are turned against it.

**Detection note.** The dominant signal is provenance divergence: a digest, snapshot, or manifest entry that does not match what was attested. This is the one category in which the detection objective can often be stated as an equality check rather than as a behavioural anomaly, which makes it unusually tractable — provided the operator actually attests its artefacts. Where it does not, OCC-06 has nothing to compare against, and the coverage assessment records the technique as uncovered rather than partial.

**Not covered.** Exploitation of a vulnerable dependency that is exploited rather than substituted is AAT-4. Tool misuse within an authentic tool is AAT-1. A model that behaves unexpectedly without any change to its artefacts is a quality or configuration problem, not a supply-chain attack, and the distinction is made by the artefact comparison rather than by the behaviour.

| ID | Name | Description | Observable artefact in telemetry | Most often combines with | Countermeasure binding |
| --- | --- | --- | --- | --- | --- |
| **AAT-7.1** | Training or fine-tuning data poisoning | The adversary contaminates a corpus used to train or adapt a model, so that the model carries the adversary's behaviour. | A corpus snapshot whose content hash differs from its attested value; a small number of near-duplicate items recurring across otherwise independent training sets; a behaviour present in the model and traceable to a specific corpus segment. | AAT-7, AAT-2 | OCC-07 (retrieval corpus integrity monitoring); OCC-41 (model artefact restoration from a trusted registry); OCC-40 (state snapshot and restore for agent workloads) |
| **AAT-7.2** | Backdoored adapter or fine-tune delivery | The adversary supplies a model artefact containing a hidden conditional behaviour, which activates only under the adversary's trigger. | A model artefact loaded whose digest is absent from the approved manifest; an artefact retrieved from a location other than the registry; a behaviour appearing only for a specific input pattern. | AAT-7, AAT-5 | OCC-06 (model artefact and weight attestation monitoring); OCC-41 (model artefact restoration from a trusted registry); OCC-15 (model rollback and checkpoint integrity); OCC-23 (model and agent rollback to last-known-good) |
| **AAT-7.3** | Retrieval-corpus poisoning | The adversary adds or alters documents in the index the operator's agents read. | Injected documents appearing in retrieval results with no corresponding authoring or ingestion event; an index segment whose item count rises without a matching ingestion count. | AAT-7, AAT-2 | OCC-07 (retrieval corpus integrity monitoring); OCC-20 (memory and context quarantine and scrub); OCC-05 (prompt-injection detection and sanitisation at ingest) |
| **AAT-7.4** | Tool and plugin supply-chain compromise | The adversary introduces or alters a tool definition that the agent will load and use. | A new tool registration, or a changed tool manifest, outside the change process; a tool whose published permissions exceed the operator's approved scope; a tool descriptor with no matching source revision. | AAT-7, AAT-4 | OCC-10 (tool capability scoping and least privilege); OCC-06 (model artefact and weight attestation monitoring); OCC-19 (quarantine and triage of a compromised agent) |
| **AAT-7.5** | Embedding manipulation | The adversary shifts the representation space so that certain content is retrieved preferentially or excluded from it. | Embedding drift against a reference corpus for stable documents; new dense clusters with no corresponding source documents; retrieval-order changes for a fixed query set. | AAT-7, AAT-2 | OCC-07 (retrieval corpus integrity monitoring); OCC-06 (model artefact and weight attestation monitoring); OCC-40 (state snapshot and restore for agent workloads) |
| **AAT-7.6** | Prompt-template and policy poisoning | The adversary alters a template, system prompt, or policy fragment so that the agent carries the adversary's instruction. | A template or policy file whose digest changed without a change record; an effective instruction differing from the approved source; a policy fragment loaded from a non-registry path. | AAT-2, AAT-7 | OCC-08 (instruction-hierarchy enforcement with provenance tagging); OCC-06 (model artefact and weight attestation monitoring); OCC-40 (state snapshot and restore for agent workloads) |
| **AAT-7.7** | Dependency substitution in the agent toolchain | The adversary causes a different library, package, or binary to be resolved at run time than the operator intended. | A resolved package version differing from the lockfile at execution time; a dependency fetched from a source other than the approved registry; a hash mismatch on a load-time integrity check. | AAT-7, AAT-4 | OCC-16 (sandboxed agent execution); OCC-15 (model rollback and checkpoint integrity); OCC-42 (forensic capture and evidence preservation) |
| **AAT-7.8** | Evaluation and canary tampering | The adversary alters the evaluations, test sets, or canaries used to judge the operator's own defences, so that the defences appear to work. | Evaluation result files whose digests do not match the run that produced them; a canary whose expected alarm condition no longer matches its definition; evaluation inputs modified after the run. | AAT-5, AAT-7 | OCC-06 (model artefact and weight attestation monitoring); OCC-04 (instrumented canary agent); OCC-42 (forensic capture and evidence preservation) |

---

### 5.8 AAT-8 — Multi-Agent Coordination

**Scope.** Agent swarms, delegation-chain abuse, coordinator compromise, inter-agent trust exploitation, conflicting-goal propagation.

**Behaviour covered.** Behaviours in which the adversary obtains leverage from the structure of a multi-agent system rather than from any single agent — by causing many agents to act at once, by deepening a delegation chain beyond its intent, by compromising the coordinator, or by causing one agent to assert authority to another.

**Detection note.** The dominant signal is structural: orchestrator fan-out above the operator's own configuration, lineage depth beyond the configured maximum, and authority claims inside peer-to-peer payloads. This category depends entirely on the operator's agent platform emitting lineage and peer-to-peer records; where the platform does not, the coverage assessment records every technique in this category as uncovered, and no amount of analytical work substitutes for the telemetry.

**Not covered.** Coordination among human analysts or operators is not within scope. An adversary's own internal agent fleet is only visible to the operator where it is observed through the operator's estate or through an authorised engagement, and is otherwise treated under the observation countermeasures.

| ID | Name | Description | Observable artefact in telemetry | Most often combines with | Countermeasure binding |
| --- | --- | --- | --- | --- | --- |
| **AAT-8.1** | Agent swarm fan-out | The adversary causes a coordinator to create a large number of agents in a short period, to multiply throughput or to distribute attention. | One orchestrator identity creating runs in a tight window; a run count per objective far above the configured concurrency; a spike in child runs with a common parent and a common creation reason. | AAT-1, AAT-6 | OCC-11 (delegation depth and scope limits); OCC-14 (adversarial input rate limiting and anomaly gates); OCC-02 (tool-call sequence anomaly detection) |
| **AAT-8.2** | Delegation-chain depth abuse | The adversary causes work to be delegated through a chain deeper than the platform intends, so that the terminal agent's authority exceeds any single authorisation. | Lineage depth beyond the configured maximum; the same authority token passed down more than one level; a terminal action whose effective scope exceeds its parent's. | AAT-1, AAT-10 | OCC-11 (delegation depth and scope limits); OCC-16 (sandboxed agent execution); OCC-13 (segregation of agent identity from human identity) |
| **AAT-8.3** | Coordinator compromise | The adversary manipulates the instructions the orchestrator itself receives, so that the whole fleet is redirected. | Orchestrator instruction content with no traceable provenance; a fleet-wide change in behaviour following a single orchestrator input; orchestrator directives absent from the operator's own configuration. | AAT-2, AAT-8 | OCC-08 (instruction-hierarchy enforcement with provenance tagging); OCC-27 (interaction transcript capture); OCC-20 (memory and context quarantine and scrub) |
| **AAT-8.4** | Inter-agent trust exploitation | The adversary causes one agent to assert authority to another — as a supervisor, a policy engine, or a peer — in order to obtain an action the first agent could not take. | Peer-to-peer messages containing authority claims; an agent acting on a permission claim that appears in a peer message and not in the platform's own grant; a privilege request originating from a non-orchestrator peer. | AAT-2, AAT-8 | OCC-08 (instruction-hierarchy enforcement with provenance tagging); OCC-11 (delegation depth and scope limits); OCC-10 (tool capability scoping and least privilege) |
| **AAT-8.5** | Conflicting-goal propagation | The adversary causes a goal to be introduced at one point in a chain so that agents further along the chain act on it, having never seen its origin. | A directive string first appearing in a leaf agent and later in a parent, or the reverse, with no corresponding originating turn; identical goal text recurring across lineage levels. | AAT-10, AAT-2 | OCC-08 (instruction-hierarchy enforcement with provenance tagging); OCC-27 (interaction transcript capture); OCC-19 (quarantine and triage of a compromised agent) |
| **AAT-8.6** | Agent-to-agent covert channel | The adversary causes data to be passed between agents in a field that the operator's own visibility does not cover. | Inter-agent payloads carrying content outside the declared schema; a size or entropy distribution of peer traffic inconsistent with declared content types; data present in a peer message with no corresponding source. | AAT-9, AAT-8 | OCC-20 (memory and context quarantine and scrub); OCC-22 (edge policy for agent-facing endpoints); OCC-09 (output sanitisation and egress allow-listing) |
| **AAT-8.7** | Emergent capability accumulation | The adversary arranges that individually permissible steps, taken by different agents, combine into a capability that no single step would have had. | A sequence in which each step is within policy and the aggregate is not; a combined target set larger than any agent's declared scope; an effect with no single causal step. | AAT-10, AAT-1 | OCC-11 (delegation depth and scope limits); OCC-19 (quarantine and triage of a compromised agent); OCC-16 (sandboxed agent execution) |

---

### 5.9 AAT-9 — Exfiltration and Covert Channels

**Scope.** Staged exfiltration, encoding and compression, DNS and timing channels, covert storage, egress abuse.

**Behaviour covered.** Behaviours in which the adversary moves the operator's data out, or establishes a channel by which data can be moved out later, while keeping the movement within channels the operator's estate has permitted.

**Detection note.** The dominant signal is outbound behaviour: volume, entropy, destination, and cadence, correlated against the local object that appears to have been the source. The correlation is the difficult part. Volume alone is indistinguishable from a legitimate export; a single high-entropy object is indistinguishable from a compressed artefact; a DNS query is indistinguishable from a lookup.

**Not covered.** The theft of a credential is AAT-4.3. The use of a third party's service as the destination is AAT-9 but brings the third party within the analysis, and any action against that third party's infrastructure requires the separate per-target authorisation that the master design §4.2 requires. AAT-9 is observed after the fact in nearly all its forms, which the master design records as LIM-12 and which this document reflects by weighting these techniques towards prevention.

| ID | Name | Description | Observable artefact in telemetry | Most often combines with | Countermeasure binding |
| --- | --- | --- | --- | --- | --- |
| **AAT-9.1** | Staged exfiltration | The adversary divides data into pieces and transfers them separately, so that no single transfer is significant. | Many small outbound transfers whose concatenation matches the size and structure of a single local object; a set of transfers from one identity with near-identical content and a regular interval. | AAT-6, AAT-4 | OCC-09 (output sanitisation and egress allow-listing); OCC-17 (egress control and network segmentation for agent workloads); OCC-26 (adversary AI traffic observation and protocol reconstruction) |
| **AAT-9.2** | Encoding and compression of payload | The adversary encodes or compresses data before egress so that the content is not recognisable in transit. | Outbound payloads with entropy or character distribution unlike the declared content type; a size-to-payload ratio inconsistent with the declared format; a base64-like segment in a body declared as prose. | AAT-9, AAT-5 | OCC-09 (output sanitisation and egress allow-listing); OCC-17 (egress control and network segmentation for agent workloads); OCC-26 (adversary AI traffic observation and protocol reconstruction) |
| **AAT-9.3** | DNS-based covert channel | The adversary encodes data in the labels of DNS queries to a service it controls. | Subdomain label entropy, length, or character distribution above the estate baseline; a high cardinality of unique labels under one parent domain; label structure that varies with data content. | AAT-9, AAT-5 | OCC-17 (egress control and network segmentation for agent workloads); OCC-22 (edge policy for agent-facing endpoints); OCC-26 (adversary AI traffic observation and protocol reconstruction) |
| **AAT-9.4** | Timing channel | The adversary encodes data in the timing of requests rather than in their content. | Inter-request interval distributions that correlate with a payload structure; a measurable relationship between interval values and a recurring numeric value in local data. | AAT-9, AAT-5 | OCC-26 (adversary AI traffic observation and protocol reconstruction); OCC-30 (deceptive response shaping at the agent-facing interface); OCC-33 (operational tempo perturbation and delay injection) |
| **AAT-9.5** | Covert storage in permitted services | The adversary stores data in a service the operator has already authorised, to be retrieved later by the adversary or an accomplice. | Objects written to a storage service and later read by a different identity; an object whose key pattern encodes content; a write with no corresponding business purpose. | AAT-9, AAT-5 | OCC-17 (egress control and network segmentation for agent workloads); OCC-22 (edge policy for agent-facing endpoints); OCC-19 (quarantine and triage of a compromised agent) |
| **AAT-9.6** | Egress abuse through permitted integrations | The adversary causes the agent to use a legitimate outbound integration to reach a destination the integration was not meant to reach. | An integration posting to a destination outside its declared list; request bodies containing material unrelated to the integration's purpose; a destination newly appearing in an integration's traffic. | AAT-9, AAT-2 | OCC-09 (output sanitisation and egress allow-listing); OCC-17 (egress control and network segmentation for agent workloads); OCC-30 (deceptive response shaping at the agent-facing interface) |
| **AAT-9.7** | Cloud storage and collaboration exfiltration | The adversary moves operator data into a cloud storage or collaboration platform, from which it can be shared onward. | Bulk downloads, shares, or permission grants from a collaboration platform; a large first-time transfer to a storage destination; a share to an external party. | AAT-9, AAT-4 | OCC-17 (egress control and network segmentation for agent workloads); OCC-35 (egress denial and service suspension for adversary agent endpoints); OCC-22 (edge policy for agent-facing endpoints) |
| **AAT-9.8** | Prompt and context leakage | The adversary causes the operator's own context — system instructions, retrieved documents, tool schemas — to leave the estate. | Outbound content containing internal instruction text, configuration fragments, or document bodies; a payload size consistent with a context window rather than with the request. | AAT-2, AAT-9 | OCC-09 (output sanitisation and egress allow-listing); OCC-20 (memory and context quarantine and scrub); OCC-08 (instruction-hierarchy enforcement with provenance tagging) |

---

### 5.10 AAT-10 — Decision Manipulation

**Scope.** Goal substitution, incremental scope creep, specification gaming, reward-hacking of the surrounding loop, operator decision influence.

**Behaviour covered.** Behaviours in which the adversary's effect is achieved by acting on the operator's decision process rather than on the operator's systems: the objective the operator set is replaced, the scope is widened a step at a time, a metric is satisfied in letter and not in substance, or the analyst reviewing the evidence is shown content chosen to reach a conclusion.

**Detection note.** The dominant signal is the divergence between a declared objective and a realised effect, and the *sequence* in which the divergence appears: a monotonic widening, a metric that improves while the underlying condition does not, or a step whose behaviour changes when the evaluation is switched off. Detection content here is difficult to write, because the artefacts are semantic, and it is the category in which the operator's own processes are as much the target as the adversary's actions.

**Not covered.** A failure of the operator's own specification to be sound, with no adversary involved, is a process failure rather than an adversary behaviour, and the taxonomy does not claim it. The distinction is made at attribution: the presence of an adversary-AI technique in the sequence is what moves an event into this category.

| ID | Name | Description | Observable artefact in telemetry | Most often combines with | Countermeasure binding |
| --- | --- | --- | --- | --- | --- |
| **AAT-10.1** | Goal substitution | The adversary causes the run's objective to be replaced by a different objective that satisfies the original's surface form. | A run whose realised effect diverges from the objective recorded on the card, while satisfying a lexical or structural surface of it; a plan body naming an objective absent from the authorisation. | AAT-2, AAT-1 | OCC-19 (quarantine and triage of a compromised agent); OCC-11 (delegation depth and scope limits); OCC-27 (interaction transcript capture) |
| **AAT-10.2** | Incremental scope creep | The adversary widens the target set, the permission set, or the data scope one small step at a time, so that no single step requires approval. | A monotonically widening target or permission set across steps within one campaign; a series of individually minimal scope expansions that cumulatively exceed the original authorisation. | AAT-1, AAT-8 | OCC-11 (delegation depth and scope limits); OCC-32 (scope-limiting session invalidation of adversary access); OCC-22 (edge policy for agent-facing endpoints) |
| **AAT-10.3** | Specification gaming | The adversary produces an outcome that satisfies the stated specification literally while defeating its purpose. | A reported metric that improves while the underlying condition it was meant to reflect does not; an output satisfying the declared field format while contradicting the declared intent. | AAT-1, AAT-10 | OCC-02 (tool-call sequence anomaly detection); OCC-01 (behavioural baseline of agent activity); OCC-27 (interaction transcript capture) |
| **AAT-10.4** | Reward-hacking of the surrounding loop | The adversary optimises against the operator's monitoring or scoring mechanism rather than the task, so that performance rises without progress. | Behaviour that changes sharply when the evaluation or monitoring path is disabled or bypassed; a metric that correlates inversely with a human-rated quality measure. | AAT-5, AAT-1 | OCC-01 (behavioural baseline of agent activity); OCC-02 (tool-call sequence anomaly detection); OCC-27 (interaction transcript capture) |
| **AAT-10.5** | Operator decision influence | The adversary causes content to reach the operator's or analyst's own view, in a form intended to shape the decision that will be taken about it. | Adversary-sourced content appearing in a triage queue, a cluster summary, or a classification console; a text artefact rendered in the operator's view whose origin is not an operator system. | AAT-2, AAT-3 | OCC-09 (output sanitisation and egress allow-listing); OCC-30 (deceptive response shaping at the agent-facing interface); OCC-25 (instrumented honeypot agent mirroring the operator's stack) |
| **AAT-10.6** | Deliberate false-positive generation | The adversary floods the operator's detection with noise so that a genuine signal is dismissed as part of the pattern. | A sharp rise in the alert rate from one source immediately before a target technique appears; a distribution of alerts in which the genuine event is statistically indistinguishable from the flood. | AAT-6, AAT-5 | OCC-01 (behavioural baseline of agent activity); OCC-02 (tool-call sequence anomaly detection); OCC-04 (instrumented canary agent) |
| **AAT-10.7** | Confirmation-seeking behaviour | The adversary steers the operator's hypothesis towards a conclusion the adversary wants the operator to hold. | A pattern of evidence whose outcomes consistently match the operator's prior belief and never disconfirm it; prompts whose expected answers align with a single hypothesis; disconfirming observations repeatedly absent. | AAT-3, AAT-10 | OCC-27 (interaction transcript capture); OCC-25 (instrumented honeypot agent mirroring the operator's stack); OCC-05 (prompt-injection detection and sanitisation at ingest) |
| **AAT-10.8** | Safety-layer subversion | The adversary causes a model or agent to misdirect, disable, or talk around a refusal, guardrail, or other safety control, so that the control is present, appears to operate, and does not. | A refusal or warning that is issued and then withdrawn; a control whose invocation does not correspond to any effect on the subsequent action; a request whose phrasing coincides with a constraint template; a safety layer whose telemetry records invocations that changed nothing. | AAT-2, AAT-5 | OCC-08 (instruction-hierarchy enforcement with provenance tagging); OCC-05 (prompt-injection detection and sanitisation at ingest); OCC-16 (sandboxed agent execution) |

### 5.11 Technique cross-index

The following tables are reading aids derived from the bindings above. They are computed from this document's own tables and are not an authority on technique bindings; the catalogue and the technique library govern.

| Category | Techniques | Distinct OCC referenced | Countermeasure classes represented | Most frequently bound class |
| --- | --- | --- | --- | --- |
| AAT-1 Autonomy and Planning | 8 | 14 | Detect, Harden, Contain, Observe, Deceive | Harden (9 bindings) |
| AAT-2 Manipulation and Deception | 8 | 8 | Detect, Harden, Contain, Observe, Deceive | Harden (13 bindings) |
| AAT-3 Social and Cognitive | 7 | 9 | Detect, Harden, Observe, Deceive | Observe (10 bindings) |
| AAT-4 Exploitation and Discovery | 8 | 14 | Detect, Harden, Contain, Disrupt, Deceive, Recover | Harden (8 bindings) |
| AAT-5 Evasion and Persistence | 8 | 16 | Detect, Harden, Contain, Observe, Deceive, Disrupt, Recover | Detect (12 bindings) |
| AAT-6 Resource and Denial | 7 | 13 | Detect, Harden, Contain, Observe, Deceive, Disrupt | Disrupt (9 bindings) |
| AAT-7 Supply Chain and Model | 8 | 14 | Detect, Harden, Contain, Recover | Detect (10 bindings) |
| AAT-8 Multi-Agent Coordination | 7 | 12 | Detect, Harden, Contain, Observe | Harden (13 bindings) |
| AAT-9 Exfiltration and Covert Channels | 8 | 10 | Detect, Harden, Contain, Observe, Deceive, Disrupt | Contain (11 bindings) |
| AAT-10 Decision Manipulation | 7 | 12 | Detect, Harden, Contain, Observe, Deceive | Detect (8 bindings) |
| **Total** | **77** | **43 distinct** | all seven classes represented | — |

**Table note.** The technique counts sum to 77, the taxonomy total. The binding counts do not sum to 76, because each technique carries three bindings and a technique whose bindings span three classes is counted once in each.

### 5.12 Identity-independence of the bindings

One of the design commitments that runs through the set is that a countermeasure which does not depend on identifying the adversary can be selected on class confidence alone (INT-4), and that this is the practical route to action where attribution is contested. The bindings above were chosen with that in mind, and the result is worth stating explicitly.

| Property | Techniques | Note |
| --- | --- | --- |
| Answerable entirely within the operator's own estate and environment | 67 of 77 | AAT-1.1 to AAT-1.8, AAT-2.1 to AAT-2.8, AAT-3.1 to AAT-3.7, AAT-4.1 to AAT-4.5, AAT-4.7, AAT-5.1 to AAT-5.5, AAT-5.7, AAT-5.8, AAT-6.7, AAT-7.1 to AAT-7.8, AAT-8.1 to AAT-8.7, AAT-9.1 to AAT-9.6, AAT-9.8, AAT-10.1 to AAT-10.7 |
| Indicative bindings include at least one countermeasure acting on the adversary's own systems | 10 of 77 | AAT-4.6, AAT-4.8, AAT-5.6, AAT-6.1, AAT-6.2, AAT-6.3, AAT-6.4, AAT-6.5, AAT-6.6, AAT-9.7 |

> **Label.** Interpretation. The ten techniques in the second row are those for which the indicated bindings include a countermeasure whose effect is on the adversary's own infrastructure — credential invalidation at the identity source, egress denial or service suspension of adversary endpoints, agent termination and compute revocation, denial of inference quota, and revocation of third-party credentials. Under the master design §7.2 such an action requires profile R4 or above, per-target written authorisation under AUTH-6, and the shared-tenancy test of AUTH-8. The remaining sixty-six techniques can be answered at R0 to R3 without identifying the adversary, which is the practical basis for INT-4 and for the preference in CM-2 and CM-3 for containment over disruption.

---

## 6. Adversary Archetypes

### 6.1 The archetype concept

An archetype is a descriptive pattern of adversary conduct: a bundle of techniques, a tempo, a dwell profile, and a characteristic failure of the operator to notice it. Archetypes are not actors and carry no identity information. Their purpose is to give an analyst a starting hypothesis that can be tested against telemetry, and to give an operator a sense of what tempo to expect, which is the difference between noticing an activity and dismissing it as background.

Archetype identifiers `ARCH-1` to `ARCH-9` are **document-local** to this document.

Three cautions apply to every row of the table below.

- **An archetype is a hypothesis.** Assigning activity to an archetype is an Interpretation with a confidence, not a finding. It is recorded, it is revisable, and it does not survive an operation card without a rationale.
- **Archetypes are porous.** A single adversary-AI operation may exhibit two archetypes' techniques at once, and a single adversary may shift archetype as it adapts. The archetype is a description of the current picture, not a fixed identity.
- **The characteristics are expectations, not measurements.** The tempo and dwell figures are design parameters chosen to make the archetype legible; they are not derived from observed data and are labelled accordingly.

| ID | Archetype | Description | Dominant categories | Expected tempo | Typical dwell time | Most likely to be noticed first | Usually noticed too late | Countermeasures most likely to work |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **ARCH-1** | Script opportunist | An operator using an off-the-shelf script or a single prompt to take an opportunity when one appears, without building tooling and without intending a campaign. | AAT-2, AAT-4, AAT-9 | Low; intermittent, coincident with opportunity | Hours to days | The single anomalous request or message, in the absence of any pattern | Whether the same party tried the same thing again and succeeded | OCC-05 (prompt-injection detection and sanitisation at ingest); OCC-22 (edge policy for agent-facing endpoints); OCC-09 (output sanitisation and egress allow-listing) |
| **ARCH-2** | Automation scaler | An operator who has found one technique that works and applies it at volume, with no interest in novelty. | AAT-6, AAT-4, AAT-9 | High and constant; volume is the signature | Days | The rate itself; the alert volume or the cost | Which of the many identical attempts was the one that succeeded | OCC-31 (rate and cost shaping to throttle the adversary); OCC-14 (adversarial input rate limiting and anomaly gates); OCC-38 (denial of inference and compute quota to the adversary) |
| **ARCH-3** | Adaptive reconnaissance agent | An operator running an agent that maps the estate, reasons about what it found, and changes its approach in response to failure. | AAT-1, AAT-4, AAT-2 | Moderate, bursty, with pauses for the model to reason | Days to weeks | The goal-like structure of the tool-call sequence; the agent's own planning field | The purpose behind the reconnaissance, and whether anything was staged rather than merely read | OCC-02 (tool-call sequence anomaly detection); OCC-16 (sandboxed agent execution); OCC-19 (quarantine and triage of a compromised agent) |
| **ARCH-4** | Social-engineering swarm | An operator running many personas and tailored conversations in parallel, working on people rather than systems. | AAT-3, AAT-10, AAT-2 | High on the human side; message counts rise faster than the human queue can absorb | Weeks | The regularity of the message corpus; the absence of human variance | That a real decision had already been taken by a person before the operator was alerted | OCC-03 (canary credential and honeytoken deployment); OCC-25 (instrumented honeypot agent mirroring the operator's stack); OCC-13 (segregation of agent identity from human identity) |
| **ARCH-5** | Supply-chain planter | An operator who seeks access by altering what the operator's systems trust, rather than by attacking them directly. | AAT-7, AAT-4 | Very low; a single insertion, then silence | Months to years | Almost never, from behaviour; occasionally, from an integrity check | That the artefact which now carries the adversary's behaviour is one the operator signed off on | OCC-06 (model artefact and weight attestation monitoring); OCC-07 (retrieval corpus integrity monitoring); OCC-41 (model artefact restoration from a trusted registry) |
| **ARCH-6** | Model-poisoning operator | An operator who targets the model's weights, training data, or retrieval corpus to install behaviour that fires on a trigger only they know. | AAT-7, AAT-2 | Very low and almost entirely invisible | Months to years | Nothing behavioural, in the ordinary case | The behaviour itself, when the trigger finally fires — by which point the artefact has been trusted for a long time | OCC-06 (model artefact and weight attestation monitoring); OCC-41 (model artefact restoration from a trusted registry); OCC-40 (state snapshot and restore for agent workloads) |
| **ARCH-7** | Multi-agent swarm | An operator who uses the operator's own agent fleet as the execution substrate, turning many agents into a parallel campaign. | AAT-8, AAT-1, AAT-6 | High; concurrency, not duration, is the signature | Hours to days | Fan-out from one orchestrator beyond the operator's own configuration | Which goal the swarm was pursuing, once the lineage has been reconstructed | OCC-11 (delegation depth and scope limits); OCC-16 (sandboxed agent execution); OCC-18 (tool-call kill switch and agent session revocation) |
| **ARCH-8** | Persistent implant operator | An operator who intends to stay, and who treats the estate as a resource rather than a target. | AAT-5, AAT-4, AAT-1 | Very low and deliberately unremarkable | Months to years | Nothing at all, in most cases | The implant itself, typically at the point of decommissioning or of an unrelated investigation | OCC-42 (forensic capture and evidence preservation); OCC-19 (quarantine and triage of a compromised agent); OCC-43 (rotation of all credentials touched by the compromised path) |
| **ARCH-9** | Infrastructure-resident agent | An adversary AI that lives inside the operator's own agent infrastructure — a model, a connector, a plugin, a tool endpoint — rather than attacking from outside it. | AAT-7, AAT-2, AAT-8 | Low, continuous, and legitimate-looking | Indefinite | Nothing, unless the residency is checked for provenance | That the resident component had been answering questions on the operator's behalf the whole time | OCC-06 (model artefact and weight attestation monitoring); OCC-19 (quarantine and triage of a compromised agent); OCC-23 (model and agent rollback to last-known-good) |

> **Label.** Interpretation. The tempo and dwell columns are design parameters that make the archetypes legible; they are not measurements of observed adversary behaviour and should not be cited as such.

### 6.2 The disappearance of human tells

The most important practical change that the arrival of adversary AI brings to defensive work is not that attacks became faster. It is that **the tells that people were taught to look for stopped being reliable.**

For decades, the operator's practical detection knowledge was built on human tells: the request at an unusual hour, the grammar of a hurried message, the reply that was too fast, the slight inconsistency in a story, the absence of a second factor, the phrasing of a request that did not quite match the requester. These are genuinely useful, and where an adversary is a person operating without model assistance they remain useful. But they are heuristics about human behaviour, and they do not survive an adversary that can write uniformly fluent text, choose its own timing distribution, hold a persona across thousands of turns without fatigue, and generate a volume of plausible correspondence that no human team could produce.

Four consequences follow, and they shape everything in §9 and §11.

| Consequence | What it means in practice | Where it is handled |
| --- | --- | --- |
| **Human tells stop discriminating** | A detector built on "this looks like a person did not write it" is measuring the wrong variable. The adversary's output is now the most human-looking output in the estate. | DET-2 (behavioural baselines over signatures); AAT-3's artefacts are defined against process regularity, not against human imperfection |
| **Volume becomes the dominant artefact** | Where content quality cannot distinguish, rate, concurrency, and structure can. The adversary's ability to produce volume is itself the observable. | AAT-6 as a category; AAT-1.6; AAT-10.6 |
| **Behavioural baselines must be learned, not assumed** | The operator cannot assert what normal looks like for a system that did not exist last year. A baseline must be built from observed behaviour, per task, per role, and per hour, and its staleness must be visible. | DET-2; DET-6 (freshness); OCC-01 |
| **The operator's own judgement becomes the weakest link** | An analyst facing a fluent, confident, coherent adversary message will find it harder to distrust it than a clumsy one. The taxonomy's requirement for a stated rationale and a confidence is what compensates. | TAX-2; TAX-4; INT-7; INT-8; LIM-TC4 |

This is also why the taxonomy is behaviour-centred and why §6 does not attempt to characterise adversary psychology. The observable has shifted from the adversary's manner to the operator's own estate: what was touched, how often, in what structure, with what persistence. That is what the taxonomy describes, and it is what the operator can still measure.

### 6.3 Working with archetypes

The archetypes are used in three places, and nowhere else.

1. **In threat modelling** (§8), to enumerate plausible adversary conduct against the estate's AI-attackable surface before any telemetry exists, so that detection content is designed against a hypothesis rather than against the last incident.
2. **In classification**, to propose an archetype for a cluster and to set the expected tempo, which is what allows an operator to distinguish background from campaign.
3. **In exercise design** (§10), to select the archetype a scenario simulates.

They are not used to attribute, and they are not used to justify a countermeasure on their own. A proposed archetype is an Interpretation with a confidence, and the decision record records it as such.

---

## 7. Capability Profiles

### 7.1 Purpose

A capability profile states what a specific adversary can evidently do. It is the analyst's answer to "what is this party capable of", expressed in the form the countermeasure-selection step needs: a list of capabilities, each with a confidence, an evidence basis, and a recency.

Two properties of the structure are deliberate.

- **It is a hypothesis with confidence, not a fact.** A capability profile is a set of Estimates about what an adversary can do. It is never asserted as a property of the adversary, and it must not appear in an Operation Card without its confidence values, its evidence basis, and its date. The framing follows the research framework's claim-label discipline (INT-7): a capability entry is an Estimate, and a profile is a set of Estimates with a shared subject.
- **It decays.** The profile records what the adversary *can evidently do*, and "evidently" is time-limited. A capability that has not been re-observed falls in confidence, and the profile records the fall rather than holding the original assessment indefinitely.

### 7.2 The capability entry

| Field | Content | Rule |
| --- | --- | --- |
| **Capability ID** | `CAP-n`, **document-local** to this document | Stable within a profile revision |
| **Capability statement** | What the adversary can evidently do, expressed as behaviour rather than as a tool or a product | Must map to one or more AAT technique identifiers |
| **AAT binding** | The technique identifiers the capability is evidenced by | At least one; a capability with no binding is not a capability |
| **Confidence** | A value in [0.0, 1.0] with a label | See §7.3 |
| **Claim label** | The label carried by the entry | Normally **Estimate** |
| **Evidence basis** | The artefacts the confidence rests on, each with integrity state and source fidelity | Must be enumerable; an entry with no listed evidence is a Hypothesis |
| **First observed** | Date and time of the first observation | Not the date of the assessment |
| **Last confirmed** | Date and time of the most recent confirming observation | Drives the decay rule |
| **Decay rule** | The interval and rate at which this entry's confidence falls | Per category, per §7.4; may be overridden downward only, and the override is recorded |
| **Attribution dependency** | Whether the capability can be exercised by any party with the same access, or whether it implies something specific to this adversary | Recorded because it determines whether the capability can be assumed to persist against a change of operator |

### 7.3 Confidence scale for capability entries

| Value | Label | Meaning | Use in selection |
| --- | --- | --- | --- |
| 0.85 – 1.00 | Confirmed | Observed in at least two independent instances, or re-observed after an interval, with intact evidence | May support a countermeasure at any collateral class subject to INT-3 |
| 0.60 – 0.84 | Probable | Observed once with intact evidence, or repeatedly with degraded evidence | May support an identity-independent countermeasure; a further observation is requested |
| 0.30 – 0.59 | Possible | Inferred from partial or indirect evidence; a plausible reading, not a demonstrated one | May inform scenario design and hardening priority; not sufficient to justify a targeted countermeasure |
| 0.00 – 0.29 | Speculative | Consistent with the evidence but with no direct support; recorded so that the reasoning is not lost | Informational only; may not be cited as a capability in a decision record |
| — | Unsupported | No evidence at all | Not recorded as a capability |

A confidence value is an Estimate produced by an analyst or a model. It is not calibrated against outcomes, and the master design records that limitation as LIM-2. It is used as an ordering device and as a threshold input, not as a probability that has been validated.

### 7.4 Decay rule

Capabilities decay in confidence when they are not re-observed. The rate is set per category, because the categories differ in how durable the underlying capability is: a foothold and a poisoned artefact persist, while a burst of credential stuffing does not.

| Category | Re-observation interval | Confidence lost per interval | Floor | Rationale for the parameters |
| --- | --- | --- | --- | --- |
| AAT-1 Autonomy and Planning | 14 days | 0.10 | 0.20 | A planning capability is durable but its availability depends on the operator's own model access |
| AAT-2 Manipulation and Deception | 7 days | 0.15 | 0.15 | Highly volatile; injection content is specific to the deployment it targets |
| AAT-3 Social and Cognitive | 30 days | 0.10 | 0.30 | Persona work is reusable and long-lived |
| AAT-4 Exploitation and Discovery | 14 days | 0.10 | 0.20 | Tooling persists; the specific findings do not |
| AAT-5 Evasion and Persistence | 60 days | 0.05 | 0.40 | A foothold is precisely the thing that persists; decay here is slow by design |
| AAT-6 Resource and Denial | 7 days | 0.20 | 0.15 | A capacity campaign is short-lived and cheap to replace |
| AAT-7 Supply Chain and Model | 90 days | 0.05 | 0.45 | The most durable category; a contaminated artefact remains contaminated |
| AAT-8 Multi-Agent Coordination | 21 days | 0.10 | 0.25 | Depends on the operator's own platform remaining multi-agent |
| AAT-9 Exfiltration and Covert Channels | 30 days | 0.10 | 0.30 | A working channel stays working until it is closed |
| AAT-10 Decision Manipulation | 30 days | 0.10 | 0.30 | Method-based; a technique that worked once is likely to be reused |

**Decay rule.** Where an entry has not been re-observed within the interval for its category, its confidence falls by the stated amount for each interval elapsed, to the stated floor. The floor is not zero: a capability that was once observed does not become unobserved. The computed value is displayed on the profile and in the dossier; the original first-observed confidence is retained so that the fall is auditable.

**Decay rule — override.** An analyst may hold an entry above the computed value where the evidence basis contains an artefact whose integrity state is intact and whose continued validity is independently established — for example, an attested model artefact that is still in place. The override is recorded with its basis and expires on its own stated date. An analyst may not hold an entry above the computed value merely because the capability would be convenient to assume.

### 7.5 Worked example

The following profile is an illustrative construction for a fictional adversary. It contains no real organisation, product, incident, or individual. It is provided to show the structure and the level of detail required, and it is not evidence of anything.

**Profile CP-A — subject: an adversary operation consistent with ARCH-3, adaptive reconnaissance agent.** Assessed 2026-03-14. Taxonomy version 1.0. Profile revision 1.

| Capability ID | Capability statement | AAT binding | Confidence | Label | Evidence basis | First observed | Last confirmed | Decay rule | Attribution dependency |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CAP-01 | Decomposes a reconnaissance objective into sequential tool invocations and adjusts the sequence on failure | AAT-1.1, AAT-1.2, AAT-1.7 | 0.78 | Estimate | Tool-call sequence records from three runs, integrity intact, source fidelity high; one run's transcript partially recovered (integrity degraded, excluded from the confidence calculation) | 2026-02-19 | 2026-03-11 | AAT-1: -0.10 per 14 days, floor 0.20 | Generic: any party with the same model access could reproduce it |
| CAP-02 | Uses indirect injection in retrieved documents to redirect a retrieval-augmented agent | AAT-2.2, AAT-2.7 | 0.62 | Estimate | Two retrieved documents containing instruction-shaped text, integrity intact; retrieval index audit incomplete, so corpus-level attribution to this adversary is not established | 2026-03-02 | 2026-03-12 | AAT-2: -0.15 per 7 days, floor 0.15 | Generic: a content-authoring capability, not an operator-specific one |
| CAP-03 | Automates host discovery across the estate at a rate above human throughput | AAT-4.1, AAT-6.1 | 0.85 | Estimate | Fourteen days of edge logs showing uniform request intervals and near-identical parameter patterns; corroborated by two independent sources | 2026-02-28 | 2026-03-13 | AAT-4: -0.10 per 14 days, floor 0.20 | Generic |
| CAP-04 | Uses a canary credential that was never issued to a legitimate party | AAT-4.3 | 0.91 | Estimate | Canary credential observed in an authentication event at 2026-03-09 with source attribution to a known external range; integrity intact | 2026-03-09 | 2026-03-09 | AAT-4: -0.10 per 14 days, floor 0.20 | Specific: the credential identifies this operation's access |
| CAP-05 | Maintains a low-amplitude but continuous presence across the estate over several weeks | AAT-5.5 | 0.44 | Estimate | Continuous low-volume state changes across three systems with no corresponding business process; no positive artefact of intent; two of three sources degraded | 2026-01-30 | 2026-03-01 | AAT-5: -0.05 per 60 days, floor 0.40 | Specific: a foothold is held by a party |
| CAP-06 | Evades an instrumented environment by altering behaviour between monitored and ordinary contexts | AAT-5.3 | 0.29 | Estimate | Divergent behaviour across two nominally equivalent sandboxes, observed once; no replication available | 2026-03-11 | 2026-03-11 | AAT-5: -0.05 per 60 days, floor 0.40 | Generic in principle, but the trigger remains unidentified |

**Reading the profile.** CAP-04 is the strongest entry and the one that most usefully narrows the operation, because a canary credential is specific rather than generic. CAP-01 and CAP-03 are generic capabilities that any party with model access could reproduce, which means a countermeasure chosen on them is chosen against the behaviour rather than against the party — the practical expression of INT-4. CAP-05 and CAP-06 are the entries that would most change the operator's posture if they were confirmed, and CAP-06 at 0.29 is at the bottom of the Speculative band and may not be cited as a capability in a decision record. The profile's value at this revision is that it names where to look next: CAP-06 has been observed once and not replicated, and that is the highest-value next observation.

---

## 8. Threat Modelling Procedure

### 8.1 Purpose and status

The procedure below produces a defensible statement of the adversary-AI risk to a given estate, at a given time, against a given taxonomy version. It is a design-and-process procedure: its output is a set of hypotheses, a coverage assessment, and a prioritised gap list, all of which are reviewable.

The identifiers `TM-1` to `TM-9` are **document-local** to this document.

Two cautions frame the whole procedure.

- **The output is a model, not a finding.** A threat model states what might happen and what would be noticed. It does not state what is happening, and it does not create coverage. The master design's LIM-11 makes the same point: detection gaps are usually telemetry gaps, and no procedure can create coverage where no sensor exists.
- **The surface inventory is the load-bearing artefact.** A threat model built on an assumed surface will produce a confident and wrong answer. Step TM-1 is therefore not a formality, and the "exists today" column of the enumeration table is a finding that must be recorded by the operator rather than assumed by the analyst.

### 8.2 The procedure

| Step | Action | Output | Failure this guards against |
| --- | --- | --- | --- |
| **TM-1** | Enumerate the estate's AI-attackable surface using §8.3, and for each surface record the telemetry source and whether that source exists today | Surface inventory with a source-existence finding per row | Modelling an estate that is not the estate; coverage claims against telemetry that was never collected |
| **TM-2** | Enumerate the adversaries: for each, who might wish to affect this estate, by what means, and with what intent | Adversary list, each with a motive hypothesis and a disconfirming observation | Assuming a generic adversary; the collective-attribution error of INT-6 |
| **TM-3** | Map each adversary to one or more archetypes from §6 | Adversary-to-archetype mapping, each an Interpretation with a confidence | Treating an archetype as an identity |
| **TM-4** | Apply the taxonomy: for each adversary–archetype pair and each surface in scope, derive the set of AAT techniques that could apply | Technique set per pair, with the rationale recorded per technique | Restricting the model to techniques the operator already detects |
| **TM-5** | Bind countermeasures to each technique set and run a preliminary admissibility check at category level, noting any technique whose only indicated countermeasures are unavailable at the current profile | Preliminary countermeasure set with the gaps marked | Proposing a countermeasure that the authorisation model would refuse |
| **TM-6** | Score each technique set: populate L, I, A, and V separately, and record the components, not only the product | Threat assessment with separately contestable components | A single number used to hide the reasoning (SCORE-2) |
| **TM-7** | Assess detection coverage for every technique in the set using §11, and identify the telemetry sources required but absent | Coverage assessment with per-technique coverage status and gap owners | A coverage claim that is really a documentation entry |
| **TM-8** | Compute the residual risk contribution of each uncovered or partially covered technique, and prioritise gap closure against that contribution | Prioritised gap list with named owners and target dates | Gaps closed in order of ease rather than of risk |
| **TM-9** | Re-run on a defined cadence, and immediately on any material change to the estate's AI surface, to a new taxonomy version, or after an incident | Versioned threat model with a change record | A model that describes an estate which no longer exists |

**TM-9 — Cadence.** The re-run cadence is stated by the operator and recorded with the model. The minimum content of a re-run is a diff against the previous version: new surfaces, new techniques, changed coverage, changed risk.

### 8.3 The AI-attackable surface enumeration

The table enumerates the surfaces through which an adversary AI can affect the operator's estate. The AI-specific attack surface column states what is different about the surface because AI is present. The example technique column links the surface to §5. The final column is a finding the operator records; it is not a property of this document.

| Surface | What it is | AI-specific attack surface | Example techniques | Telemetry source | Exists today |
| --- | --- | --- | --- | --- | --- |
| Models and model artefacts | The weights, adapters, templates, and system prompts the estate's own agents run on | The artefact itself is the target: contamination changes behaviour without touching the systems the agent acts on | AAT-7.1, AAT-7.2, AAT-7.6 | Artefact manifest and attestation log; template digest record | Record at TM-1 |
| Agents | The deployed agents that hold objectives and act across steps | The agent's tool surface and its persistent memory are reachable, and its actions are made at machine speed | AAT-1.1, AAT-1.4, AAT-2.5 | Agent run record: tool-call sequence, context, transcript | Record at TM-1 |
| Orchestration | The component that creates, schedules, and supervises agents | The orchestrator holds shared state and the authority to create agents; compromising it moves the whole fleet | AAT-1.3, AAT-8.1, AAT-8.3 | Orchestrator decision log; lineage records | Record at TM-1 |
| Tools and integrations | The functions agents call, including outbound and destructive ones | A tool is a confused deputy: it performs actions under the operator's authority, on the operator's credentials, in response to content the adversary may supply | AAT-2.3, AAT-4.4, AAT-4.7 | Tool invocation log with arguments and results; per-tool audit | Record at TM-1 |
| Retrieval and knowledge | The corpora, indexes, and documents agents read | The corpus is both a data source and a delivery channel: an adversary who writes into it writes into the model's instructions | AAT-2.2, AAT-2.7, AAT-7.3, AAT-7.5 | Ingestion audit; index integrity log; retrieval query and result log | Record at TM-1 |
| Identity, secrets and credentials | The identities agents act under and the secret material they hold | AI multiplies the value of a single credential and shortens the time between compromise and use; ambient authority is the normal failure | AAT-4.3, AAT-4.6, AAT-5.6 | Credential use log; secret access audit; session lifecycle records | Record at TM-1 |
| Inference and serving endpoints | The services that host models and serve requests | The endpoint is a network service with an unusual caller profile, and it is a target for cost exhaustion as well as for intrusion | AAT-6.2, AAT-6.5, AAT-4.8 | Inference request log with model and parameter metadata; quota and spend records | Record at TM-1 |
| CI/CD and build pipelines | The systems that build and deploy the estate's software and models | The pipeline is where an artefact acquires the operator's trust; it is also the most privileged place in the estate | AAT-7.4, AAT-7.7, AAT-7.8 | Pipeline run records; artefact provenance and signature log | Record at TM-1 |
| Data stores | The operator's business data, including the material the agents read and write | Data is reachable through the agent rather than only through the application's own access control, so a narrower credential now reaches further | AAT-4.7, AAT-9.5, AAT-9.7 | Data access audit; object access and share records | Record at TM-1 |
| The operator console | The Watchfloor, and the interfaces adjacent to it | The console is where adversary content is rendered to a person; it is an injection surface and a concentration of decision authority | AAT-10.5, AAT-2.1, AAT-3.7 | Console session and rendering logs; content-provenance records | Record at TM-1 |
| Communications and collaboration channels | Mail, chat, ticketing, and collaboration platforms | The channel is the delivery surface for social techniques, and AI removes the rate limit that used to bound a social campaign | AAT-3.1, AAT-3.5, AAT-6.7 | Message and event logs with sender and volume metadata | Record at TM-1 |
| Third-party and shared services | Providers, platforms, and infrastructure the operator does not own | The operator's telemetry stops at the boundary; an adversary's presence inside a shared service is visible only through what the service returns | AAT-9.7, AAT-4.8 | Provider-side logs where accessible; the operator's own egress and API usage records | Record at TM-1 |

**Surface notes.**

- **The operator console is the operator's own.** It is included in the surface enumeration for the same reason it is a design objective in the master design (DO-8): it holds the most sensitive view and the authority to act, and adversary content reaches it by design. A console that renders adversary text as live markup is an injection surface, and the surface table treats it as one.
- **Surfaces that are absent are a finding.** Where the estate has no agent, no retrieval, or no orchestration, the row is marked not applicable and the reason is recorded. An unrecorded absence is indistinguishable from an unexamined surface.
- **Third-party surfaces cannot be modelled in the same way.** For the third-party row, the operator's own telemetry is a boundary, and any countermeasure that reaches beyond it requires the per-target authorisation of AUTH-6. The model records the technique set and the expected visibility; it does not assume access.

### 8.4 Recording the model

The threat model is recorded as an artefact with the following fields, and is versioned against the taxonomy version in force.

| Field | Content |
| --- | --- |
| Model ID and revision | Identifier and revision history |
| Date of assessment | And the date of the last re-run |
| Estate in scope | The systems, identities, and services the model covers, and those it excludes |
| Taxonomy version | The version of §5 in force when the model was produced |
| Surface inventory | As §8.3, with the source-existence findings |
| Adversary list and archetype mappings | With confidences |
| Technique sets | Per adversary–archetype pair, with the rationale per technique |
| Preliminary countermeasure sets | With the admissibility gaps marked |
| Threat assessments | Component-by-component |
| Coverage assessment | As §11, with gap owners |
| Residual risk contribution by gap | Per uncovered or partial technique |
| Assumptions | Each with its disconfirming observation |
| Named owner and next review date | One accountable person and a date |

---

## 9. Detection Engineering

### 9.1 Scope

The requirements in this section govern how detection content for adversary-AI behaviour is produced, measured, and maintained. They apply to detection content authored for the operator's own estate, and to the exercises in §10 that validate it.

The identifiers `DET-1` to `DET-9` are owned by this document. They are the set-level detection-engineering requirements, and the README identifier registry records a count of nine for this prefix.

The governing principle is the one the master design states as DO-13: detection coverage is measured and reported, not asserted. These requirements exist because the most common failure in this domain is not a missing rule but an unmeasured one — a rule that was written, that never fired, and that was assumed to be working.

The normative text of DET-1 to DET-9 is the requirement column of the table at §9.2. The table form is used so that each requirement is read beside the operational consequence of getting it wrong, in the same manner as the admissibility conditions in the master design §6.4. The requirements are cited by identifier wherever they are relied upon, and an identifier cited without its requirement text is incomplete.

### 9.2 The requirements

| ID | Requirement | What it means in practice |
| --- | --- | --- |
| **DET-1** | Telemetry coverage must be established before detection content is authored for a technique. A detection objective that cannot be stated as an observable predicate over a telemetry source that the operator actually collects does not enter production. | Before anyone writes a rule for AAT-7.2, someone must confirm that the operator's artefact attestation log exists and records digests. If it does not, the first deliverable is the log, not the rule. A rule written against a source the operator does not collect is a documentation entry, and the coverage assessment marks the technique uncovered rather than covered. |
| **DET-2** | Detection content must prefer behavioural baselines over signatures wherever the behaviour can be baselined. A signature may supplement a baseline; it may not replace one where a baseline is available. | For AAT-1.1 the detector learns what this agent does when it is doing its job — the call shapes, the cadence, the fan-out profile — and flags departure, rather than matching a fixed pattern of malicious calls. Signatures for injection strings remain legitimate, because there the behaviour is not a baseline but an artefact. The baseline must be per task, per role, and per hour, because a single global baseline is the false-positive machine. |
| **DET-3** | Every technique in the taxonomy must have a detection objective stated as an observable predicate over a named telemetry source, together with the conditions under which the technique is declared detected. | The objective for AAT-5.1 names the source (the audit stream), the predicate (a gap in the record sequence with no corresponding maintenance event), and the declaration condition (the gap coincides with an authenticated write by a non-maintenance identity). A rule that says "flag suspicious log activity" satisfies nothing. Where no predicate can be written, the technique is recorded as uncovered, and that is a legitimate outcome of the exercise. |
| **DET-4** | Detection coverage must be measured and reported per category and per technique, and the measurement must be reproducible by a party other than the one that produced the coverage claim. | The coverage assessment at §11 is the measurement instrument. A technique is covered only where a stated objective exists, is implemented, has been exercised against the proving ground, and has produced the expected detection in that exercise. Coverage is reported as a fraction with its denominator visible: "34 of 77 techniques covered, exercised 2026-03-14". |
| **DET-5** | The false-positive cost of each detection objective must be measured, and the cost must be expressed in operator time, escalation generated, and trust damage, not as a count of alerts. | An objective that fires on legitimate activity is not free. It consumes triage time, it dilutes attention, and it causes the operator to learn to ignore the rule. The measurement is taken over a stated observation window with a stated volume of legitimate activity, and the result is compared against the cost of a missed true positive. A rule whose false-positive cost exceeds the value of its detections is a rule to fix or retire, and DET-6 then applies to the fix. |
| **DET-6** | Every detection objective must carry a freshness state, and the state must be visible wherever the objective is relied upon. | A rule built against a telemetry source that has since changed its schema is a rule that no longer fires, and a rule that no longer fires is indistinguishable from a rule that never fired. The freshness state records when the objective was last exercised successfully, and an objective whose last successful exercise falls outside its stated currency window is marked stale. Staleness is shown on the coverage assessment and on the watchboard, not only in a document. |
| **DET-7** | Every detection objective must be exercised against a sacrificial analogue before it is relied upon in production, and the exercise must use the proving ground at §10. | The sacrificial analogue is a disposable instance of the target surface — a sandboxed agent, a seeded corpus, a synthetic identity, a mock upstream service — which the exercising adversary is allowed to attack. The analogue is destroyed after the exercise, and the destruction is recorded. The purpose is to establish that the objective fires on the behaviour and stays silent on the neighbourhood of legitimate behaviour, without exposing the production estate to the exercise. No detection objective is credited as exercised in the coverage assessment unless it was exercised against a sacrificial analogue. |
| **DET-8** | Detection of autonomous behaviour must be assessed and reported separately from detection of the underlying technique, and must not be inferred from it. | The master design records as LIM-5 that detecting autonomous campaigns is harder than detecting tool use. A technique may be well covered by a rule that fires on the tool call, while the autonomy — the fact that the call was chosen by a model rather than directed by a person — remains undetected. The coverage assessment therefore carries two distinct statuses per technique: the underlying technique, and the autonomy characteristic. A technique may be covered on one and uncovered on the other, and that combination is expected and must be visible rather than averaged away. |
| **DET-9** | Degradation of a detector must be visible to the operator without the operator having to go looking for it, and a detector that has degraded must not continue to present itself as covering its technique. | A rule that has stopped matching because the source changed, a baseline that has drifted because the estate changed, and a detector whose dependency has failed are three different failures with three different remedies, and none of them may be discovered by the absence of alerts alone. Degradation raises a visible state on the coverage assessment and on the telemetry health view, and it propagates to the coverage status of the technique concerned. Silence from a detector is not evidence that the technique is absent. |

### 9.3 Relationship to the other requirements in the set

| Related requirement | Relationship to the DET requirements |
| --- | --- |
| TAX-1 (behaviour, not capability) | The precondition for DET-3. A technique that cannot be evidenced from telemetry could not have had an observable predicate in the first place. |
| TAX-4 (human override is expected) | Operator overrides are a primary input to detector improvement, and the override rate for an objective is a detector-health signal under DET-9. |
| INT-7, INT-8 (claim labelling, confidence) | Apply to detection claims: "this objective detects AAT-2.2" is an Estimate until exercised, and DET-7 is what moves it towards a Fact. |
| INT-9 (derived claims inherit the weakest input) | A coverage status derived from an objective whose source has degraded inherits the degradation, which is why DET-9 propagates into coverage status. |
| LIM-5 (detecting autonomy is harder) | The reason DET-8 exists and the reason the coverage assessment carries two statuses per technique. |
| LIM-11 (the picture is only as good as the telemetry) | The reason DET-1 is first, and the reason an uncovered category is a telemetry problem before it is a detection-content problem. |
| DET-5 (false-positive cost) | Feeds the Watchfloor's triage weighting, since the cost of an alert is what determines whether it is worth an operator's attention. |

---

## 10. The Proving Ground

### 10.1 Purpose

The proving ground is the exercise harness in which an adversary is simulated so that detection content may be validated and operators may rehearse. It is the instrument that turns the taxonomy from a description into an assessed capability: without it, "we have detection for AAT-4.1" is an assertion, and with it, the same statement is a measurement.

The identifiers `EX-1` to `EX-6` are owned by this document.

The normative text of EX-1 to EX-6 is the requirement column of the table at §10.3, on the same footing as DET-1 to DET-9. EX-1 is the prohibition that governs the whole harness, and it is absolute: the proving ground must never touch a non-simulated target, and where isolation cannot be demonstrated the exercise does not run.

### 10.2 The harness

| Component | Function |
| --- | --- |
| **Adversary simulator** | Produces adversary-AI behaviour against a target, with configurable archetype, tempo, technique set, and adaptation behaviour. It never contains a real credential, a real exploit, or a real third-party target. |
| **Scenario library** | Versioned scenarios, each a defined sequence of adversary actions against a defined target configuration, mapped to the AAT techniques it exercises |
| **Target sandbox** | The disposable instance of the surface being exercised: a sandboxed agent, a seeded corpus, a mock upstream service, a synthetic identity set, a mock console view |
| **Telemetry generator** | Produces the same telemetry the production estate would produce for the scenario, in the same schema, with the same integrity and fidelity metadata — so that detection objectives can be exercised against realistic inputs rather than against a convenient fixture |
| **Detector harness** | Runs the production detection content against the generated telemetry and records what fired, what did not, and what was noisy |
| **Metrics collector** | Aggregates the results into the metric set at §10.4 |
| **Rehearsal console** | The operator-facing surface for EX-5, presenting the scenario as a live picture with the same abstractions as the Watchfloor and with the same sanitisation rules |

### 10.3 The requirements

| ID | Requirement | What it means in practice |
| --- | --- | --- |
| **EX-1** | The proving ground must be a simulator, and must never touch a non-simulated target. Every target it exercises must be a sacrificial analogue created for the exercise, isolated from the production estate, and destroyed afterwards. | The harness has no capability to address a production system, and the isolation is enforced rather than merely intended: the target sandbox has no route to production networks, no production credentials, no production data, and no production model artefacts. Where the exercise requires a realistic artefact, a synthetic copy is generated. The destruction of each sacrificial analogue is recorded with its identifiers. An exercise whose isolation cannot be demonstrated does not run, and an operator who cannot demonstrate isolation does not proceed. |
| **EX-2** | The adversary simulator must be configurable by archetype, tempo, technique set, and adaptation behaviour, and every run must be seeded and reproducible. | A scenario selects ARCH-3 at a moderate tempo with techniques drawn from AAT-1, AAT-4, and AAT-2, and the run is reproducible from its seed: the same seed yields the same behaviour sequence, so that a detector that fires can be re-tested and a detector that does not fire can be debugged. A run that cannot be reproduced cannot be used to hold a detection objective to account, because there is no stable condition to point at. |
| **EX-3** | The scenario library must be versioned, and every scenario must declare the AAT techniques it exercises and the telemetry sources it produces. | The library is the coverage plan for the taxonomy: the set of scenarios in force is mapped against the technique list, and the gaps — techniques no scenario exercises — are visible and are the input to EX-6. A scenario whose technique mapping is not declared does not enter the library, because an undeclared scenario cannot contribute to a coverage claim. |
| **EX-4** | Every run must capture the metric set at §10.4, and the results must be retained with the scenario version, the seed, the detection content version, and the taxonomy version in force. | A result without its versions is not evidence. The retained record is what allows the operator to demonstrate that a detection objective was exercised at a known state of the content, against a known state of the taxonomy, on a known date. |
| **EX-5** | The proving ground must provide an operator rehearsal mode in which the scenario is presented as a live picture, with the operator taking the decisions the Watchfloor would present, and with the abort channel exercised. | Rehearsal is not a read-only replay. The operator makes the classification calls, chooses the countermeasure, sets the authorisation, and may abort; the run records the decision path and the timing. The rehearsal is scored against the same rubric as the tabletop exercise pack, and it is the rehearsal mode that reveals whether the Watchfloor's abstractions are legible under time pressure. |
| **EX-6** | Every exercise must produce a gap feedback record, which is routed into the taxonomy, the detection content, and the scenario library, and which is closed or accepted with a named owner and a date. | An exercise that finds a gap and files it as an observation rather than as an owned item is an exercise that will be repeated with the same result. The feedback record states what was observed, which requirement it bears on, what will change, and who owns it. Where a gap is judged not to be closed, the reason and the accepted risk are recorded, and the accepted risk appears in the residual risk assessment. |

### 10.4 The metric set

| Metric | Definition | Note |
| --- | --- | --- |
| **Detection coverage achieved** | The proportion of techniques in the exercised scenario set for which the stated objective fired within the scenario | The denominator is the exercised technique set, not the whole taxonomy; the taxonomy-level figure is assembled from the scenario coverage map |
| **Detection latency** | Time from the adversary's first action of the technique to the first alert attributable to the objective | Reported per technique; a latency that exceeds the operator's response window is a finding even when the objective fires |
| **False-positive rate** | Alerts raised by the objective during the scenario's legitimate activity, and the operator minutes those alerts consumed | The false-positive *cost*, per DET-5, not only the count |
| **Autonomy detection rate** | The proportion of exercised autonomous behaviours detected as autonomous, separately from the rate for the underlying technique | Required by DET-8; reported alongside and never merged with the technique rate |
| **Coverage of the objective's declaration condition** | The proportion of scenarios in which the objective's declared conditions were evaluated, as opposed to skipped by an early exit | Detects objectives that fire for reasons other than the one they declare |
| **Silent objectives** | Objectives that produced no alert, no error, and no evaluation record | Required by DET-9; an objective that never evaluated is the most dangerous form of failure |
| **Operator decision accuracy** | In rehearsal mode, the proportion of decisions that a reviewing panel judges correct, and the time taken | Used to assess the Watchfloor's legibility, not the operator's competence |
| **Abort-channel exercise result** | Whether the abort was exercised, whether it worked, and how long it took to take effect | Required by HITL-3 before any operation at AC-2 or above |

### 10.5 Scenario lifecycle

A scenario passes through six states. The state is recorded on the scenario, and a scenario in the wrong state cannot contribute to a coverage claim.

| State | Entry condition | Work performed | Exit condition |
| --- | --- | --- | --- |
| **1. Proposed** | A gap, a technique, or an incident finding identifies a scenario worth having | The technique coverage map is consulted; the scenario's purpose and its target surface are stated | A named owner accepts the proposal and the technique set is declared |
| **2. Implemented** | The proposal is accepted | The adversary behaviour is specified as a configurable script over the simulator; the target sandbox configuration is built; the telemetry generator is confirmed to produce the sources the technique's observable artefact requires | The scenario runs end to end against its sandbox and produces the expected telemetry |
| **3. Validated** | The scenario runs | The scenario is checked for fidelity against the technique's description in §5, and against the destructive question: does it exercise the behaviour, or only a convenient approximation of it | The scenario's fidelity assessment is recorded, including the areas where the simulator understates the adversary's capability |
| **4. Exercised** | The scenario is validated | The scenario is run against the detection content and, in rehearsal mode, against operators | The metric set is captured and the results are retained with their versions |
| **5. Reported** | The exercise is complete | The gap feedback record is produced, the coverage assessment is updated, and the residual risk is revised | The feedback record is accepted by a named owner with a date |
| **6. Retained or retired** | The feedback record is closed or accepted | The scenario remains in the library as coverage evidence, or is retired with a recorded reason | The scenario library version is incremented and the coverage map is reissued |

**Retirement.** A scenario is retired when the technique it exercised has changed, when the target surface it simulated no longer exists, or when it has produced the same gap three times without the gap closing — the last of which indicates that the simulation is wrong rather than that the detection is missing.

---

## 11. Detection Coverage Assessment

### 11.1 Purpose

The coverage assessment answers one question, per technique: **if this technique occurred in this estate tomorrow, would the operator see it, and what would it cost if they did?** It is the instrument that turns the taxonomy into an operational statement, and it is the input to residual risk.

The assessment is per estate. The taxonomy is common; the coverage is not.

### 11.2 The template

| Category | Technique | Detection objective | Telemetry source | Coverage status | False-positive cost | Last exercised | Gap owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AAT-n | AAT-n.m | The observable predicate, the source, and the declaration condition | The named source, and whether the operator collects it | Covered / Partial / Uncovered | Measured cost, with the observation window and legitimate volume stated | Date of last successful exercise, or "never" | Named person, or "none — accepted risk" |

**Field notes.**

| Field | Rule |
| --- | --- |
| **Category** | The AAT category. Repeated on every row so the assessment can be read by category without regrouping. |
| **Technique** | The technique identifier. The assessment is per technique; a category is never assessed as a whole. |
| **Detection objective** | The predicate as written under DET-3, not a title. "Detects AAT-5.1" is not an objective; "an unexplained gap in the audit record sequence coinciding with an authenticated write by a non-maintenance identity" is. |
| **Telemetry source** | The source, and whether the operator collects it today. A source that does not exist is recorded as absent, and the row is uncovered regardless of what the objective says. |
| **Coverage status** | **Covered**: an objective exists, is implemented, and fired in a recorded exercise against the technique. **Partial**: an objective exists and fires for some instances of the technique, or fires in the exercise but with an unmeasured false-positive cost, or fires for the underlying technique but not for the autonomy characteristic (DET-8). **Uncovered**: no objective, no telemetry source, or no exercise. |
| **False-positive cost** | Measured, per DET-5, with the window and the legitimate volume stated. "Unknown" is recorded as "Unknown" and makes the row partial rather than covered. |
| **Last exercised** | The date of the last successful exercise, not the date the objective was written. "Never" is a legitimate and important value. |
| **Gap owner** | A named person, or "none — accepted risk" with the acceptance recorded elsewhere. A gap with no owner is not a gap; it is an unrecorded risk. |

### 11.3 A worked partial example

The estate below is fictional and is used to show the method. It contains no real organisation, product, or incident. The estate is described as: a mid-sized operator running a customer-facing assistant agent, an internal drafting agent, a retrieval corpus assembled from internal documents and a supplier's feeds, and a small internal operations agent that acts on ticketing and deployment systems. The estate has no multi-agent platform, no adapter or fine-tuning pipeline of its own, and no model artefact attestation process.

| Category | Technique | Detection objective | Telemetry source | Coverage status | False-positive cost | Last exercised | Gap owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AAT-1 | AAT-1.1 | A run whose tool-call graph shows dependent fan-out with joins, above the third percentile of the same agent's baseline for the same task type | Agent run record: tool-call sequence with arguments and ordering | Covered | 4 analyst-hours per month, observed over 30 days against 1.2 million legitimate calls | 2026-03-09 | — |
| AAT-1 | AAT-1.2 | Three or more consecutive calls to the same target with a monotonic change in one parameter, with a model-chosen retry interval | Agent run record | Partial | 2 analyst-hours per month; the predicate also fires on legitimate pagination | 2026-03-09 | Detection engineering lead |
| AAT-1 | AAT-1.3 | A run created by a run rather than by the orchestrator | Lineage record | Uncovered | — | Never | Platform lead |
| AAT-2 | AAT-2.1 | Instruction-shaped text crossing the user-content boundary into the model context, matched against the ingest inspector | Model ingest record with context diff | Partial | 11 analyst-hours per month, dominated by a legitimate template that contains imperative text | 2026-02-27 | Detection engineering lead |
| AAT-2 | AAT-2.2 | A retrieved document containing imperatives addressed to a model, where the document's author is not an operator agent | Retrieval query and result log | Partial | Unknown; the objective was exercised twice and the legitimate-volume measurement has not been taken | 2026-02-27 | Detection engineering lead |
| AAT-3 | AAT-3.1 | Outbound message volume per identity per hour above that identity's own 30-day profile, with a per-message tailoring marker present | Message event log with volume metadata | Partial | 6 analyst-hours per month; the marker is present in 4 per cent of legitimate templated mail | Not exercised against a scenario | Detection engineering lead |
| AAT-4 | AAT-4.3 | Use of a canary credential in any authentication event | Authentication log plus canary credential register | Covered | 0 analyst-hours; false-positive cost is zero by construction | 2026-03-09 | — |
| AAT-5 | AAT-5.1 | An unexplained gap in the audit record sequence with no corresponding maintenance event | Audit stream sequence record | Partial | 3 analyst-hours per month; two of the seven gaps were legitimate third-party batch windows | 2026-02-27 | Detection engineering lead |
| AAT-6 | AAT-6.2 | Spend for an identity above its own 90-day profile with a completed-task-to-spend ratio below the identity's profile | Inference request log with model and parameter metadata; spend record | Partial | 1 analyst-hour per month | 2026-03-09 | FinOps lead |
| AAT-7 | AAT-7.2 | A model artefact loaded whose digest is absent from the approved manifest | Artefact attestation log | Uncovered | — | Never | Model platform lead |
| AAT-8 | AAT-8.1 | A run count per objective from one orchestrator above the configured concurrency | Orchestrator decision log | Uncovered | — | Never | Platform lead |
| AAT-9 | AAT-9.1 | A set of outbound transfers from one identity within one hour whose concatenated size falls within 5 per cent of a single local object, and whose content hashes share a common prefix | Egress record; local object store index | Uncovered | — | Never | Network lead |
| AAT-10 | AAT-10.6 | A rise in the alert rate from one source within 15 minutes preceding a target-technique alert | Alert record | Uncovered | — | Never | Detection engineering lead |

**Reading the example.** Five rows are partial and four are uncovered, and the pattern of the gaps is informative. Three of the uncovered rows (AAT-1.3, AAT-8.1, AAT-9.1) are uncovered because the telemetry source does not exist, not because the detection content is missing — the estate has no lineage record and no egress-to-object correlation, and no detection content could be written against them. One (AAT-7.2) is uncovered because the estate has no attestation log at all, which is the same class of finding. Two partial rows (AAT-2.2, AAT-3.1) are partial because the false-positive cost has not been measured, which under DET-5 makes the objective unproven rather than proven, and one partial row (AAT-5.1) is partial because the objective fires on a legitimate third-party batch window, which is a false-positive problem to be fixed rather than a coverage gap.

### 11.4 How an uncovered technique becomes residual risk

An uncovered technique is not a documentation entry. It is a quantified statement that a known behaviour, which the taxonomy says occurs, would not be seen if it occurred. The chain from coverage to risk is as follows, and each step is a record rather than a judgement made in the operator's head.

| Step | Action | Record produced |
| --- | --- | --- |
| 1 | The uncovered technique is identified in the coverage assessment | The coverage row, with status and gap owner |
| 2 | The behaviour is characterised in terms of its likely effect on the estate: what the technique would achieve if it succeeded | A short impact statement per technique, drawn from the technique's description and from the estate's specific exposure |
| 3 | The threat components are populated for that technique set: likelihood from the adversary's archetype and the estate's exposure; impact from the effect; autonomy factor from the behaviour; velocity from the tempo | The threat assessment, with components separately contestable |
| 4 | The coverage status reduces the expected effectiveness of the selected countermeasure set, because an undetected technique has not been countered | The effectiveness estimate `e` and its confidence, per SCORE-4 |
| 5 | Residual risk is recomputed as R = S_eff × (1 - e) and compared against the risk of inaction | The residual risk figure on the card, and the risk of inaction beside it |
| 6 | The residual risk is either accepted, with a named owner and a stated reason, or it is converted into a funded gap-closure action | An acceptance record, or a prioritised gap-closure item |

**The coverage-to-risk rule.** A technique whose coverage status is *uncovered* cannot be treated as countered by a countermeasure that depends on detection. A countermeasure that requires the operator to know the technique is being used is not available against an uncovered technique, and the effectiveness estimate for the card must reflect that. This is the single most important practical consequence of the coverage assessment, and it is why the assessment is performed before countermeasures are selected rather than after.

**Acceptance is a decision, not an omission.** Where a gap is accepted, the acceptance is recorded with the name of the person who made it, the date, the reason, and the specific residual risk accepted. An unowned gap is not an accepted risk; it is an unrecorded one, and the error handler treats the difference as significant.

---

## 12. Taxonomy Versioning and the External Mapping Register

### 12.1 The versioning rule

**The taxonomy version is recorded wherever a classification is relied upon.** Every Operation Card, every after-action report, every coverage assessment, every capability profile, and every ledger entry that carries a classification records the taxonomy version in force at the time it was produced.

A finding that is read against a taxonomy version other than the one that produced it is not the same finding, and the record must say which it is. This is the same discipline the set applies to the framework version: where a card cites the framework version in force, it cites the set version and the specific document versions of the documents it relied upon (README §6).

| Change | Version increment | Example |
| --- | --- | --- |
| A category is added, removed, or its scope is materially changed | Major | Splitting AAT-7 into two categories |
| A technique is added or withdrawn | Minor | Adding a new prompt-injection variant |
| A technique's description, observable artefact, or detection objective is materially changed | Minor | Replacing an artefact that turns out to be unreliable |
| A binding, an archetype characteristic, or a decay parameter is amended | Patch | Correcting a countermeasure identifier |
| Editorial correction with no change of meaning | Patch | Fixing a typo in a technique description |

**A version is not a rewrite.** A technique identifier is retired, not redefined. A technique whose description materially changes receives a new identifier and the old identifier is marked withdrawn with the date and the reason, so that historical classifications remain interpretable. Reusing a retired identifier would silently change the meaning of past cards.

**Review cadence.** The taxonomy is reviewed on a stated cadence, and out of cycle when a significant observation, an incident, or a new category of adversary behaviour is identified. The review produces a version increment or a recorded decision not to increment, and the decision is itself recorded, because a review that decided nothing is indistinguishable from a review that did not happen.

### 12.2 The process for adding a technique

Adding a technique is a controlled change, not an addition to a list. The process is as follows, and the identifiers `TV-1` to `TV-8` are **document-local** to this document.

| Step | Requirement | What it must produce |
| --- | --- | --- |
| **TV-1** | The behaviour is proposed with a description in behavioural terms and a proposed category | A written proposal that a reader who has not seen the behaviour can evaluate |
| **TV-2** | The proposal is tested for observability: it must be distinguishable from existing techniques by a predicate over a telemetry source, and it must not be a restatement of an existing technique at a different level of detail | Either a distinguishing predicate or a decision to merge the proposal into an existing technique |
| **TV-3** | The proposal is tested for the taxonomy's own admissibility rule: a behaviour that cannot be evidenced from telemetry is a hypothesis and does not enter the taxonomy (TAX-1) | A written finding that the behaviour is evidenceable from a named source |
| **TV-4** | The category assignment is made, with the rationale, and the scope note of the receiving category is amended if the addition changes it | A category assignment and an amended scope note |
| **TV-5** | The observable artefact is stated, and a detection objective is drafted against it (DET-3) | An objective in predicate form, or a recorded statement that none can yet be written |
| **TV-6** | The countermeasure bindings are reviewed with the catalogue owner, and the indicative bindings in §5 are reconciled with the catalogue and the technique library | A reconciled binding set, and the version increment of the other documents if they change |
| **TV-7** | A coverage assessment row is created, and a scenario requirement is raised against the scenario library (EX-3) | A coverage row with its status — normally uncovered — and an owned scenario item |
| **TV-8** | The change is approved by the document owner, the version is incremented, the register at §12.4 is updated, and the change is announced with its rationale | A versioned release note, so that operators can see what was added and when |

**Withdrawal follows the same discipline.** A technique is withdrawn when the behaviour it described is shown not to occur, is shown to be identical to another technique, or is shown to be undetectable and unclassifiable. A withdrawal is a version event, recorded with the reason, and the coverage assessment rows are updated so that the denominator stays honest.

### 12.3 The external mapping rule

**External mappings are recorded, verified, and dated. Until they are verified, the internal AAT identifier is canonical.**

The set maps to two published external frameworks: a published AI attack-technique framework, used for interoperability with others' descriptions of AI-focused attacks, and a published host-and-network behaviour framework, used for interoperability with conventional security operations and with the operator's existing tooling. The internal AAT identifier is the canonical reference for every requirement, decision record, coverage assessment, and card in this set. An external identifier is an aid to interoperability and is never a substitute.

| Rule | Statement |
| --- | --- |
| **Mapping is recorded per technique** | Each technique may carry a mapping to each external framework. A technique with no mapping is normal and is not a defect. |
| **Mapping carries a verification status** | One of the house statuses: Verified (primary), Verified (secondary), Corrected, Unverified, Requires confirmation. The status is the set's own; the mapping register uses it unchanged. |
| **Mapping carries a date** | The date on which the mapping was last checked against the published release in force. A mapping with no date is not usable. |
| **Unverified mappings are labelled, not hidden** | A mapping that has not been checked is recorded with the status Unverified or Requires confirmation and is displayed as such wherever it appears. An unverified mapping is never presented as a correspondence. |
| **The internal identifier governs** | Where an external framework's identifier changes, or where a mapping is wrong, nothing in this set changes. The AAT identifier and its version are the reference. |
| **Mapping is made deliberately, not automatically** | Correspondences are drawn by a person, from the source text, and recorded with the reason. Automated similarity matching is not used to populate the register, because a plausible-looking similarity is a plausible-looking error, and a register full of confident wrong correspondences is worse than an empty one. |
| **The register is reviewed with the external release** | When a new release of either external framework is observed, the register is reviewed against it and the affected rows are updated, and the review is recorded even where no row changes. |

### 12.4 The mapping register

The register below is the taxonomy-level register. `reference/ai-attack-technique-library.md` holds the per-technique register for the same mappings, under the same rule; the two must agree, and the technique library's is the per-technique instance.

**Mapping register — AAT to published AI attack-technique framework**

| AAT technique | External framework | External technique | Verification status | Date checked | Note |
| --- | --- | --- | --- | --- | --- |
| AAT-2.1 | Published AI attack-technique framework | Not yet mapped — the family of published techniques covering direct injection of instructions into a model's context appears to correspond, but the specific identifier has not been confirmed against the published release | Requires confirmation | 2026-03-14 | Asserted from general knowledge of the published framework's scope, not from its source text. The AAT identifier is canonical until this is checked. |
| — | — | — | — | — | — |
| — | — | — | — | — | — |
| — | — | — | — | — | — |

**Mapping register — AAT to published host-and-network behaviour framework**

| AAT technique | External framework | External technique | Verification status | Date checked | Note |
| --- | --- | --- | --- | --- | --- |
| AAT-4.3 | Published host-and-network behaviour framework | Not yet mapped — the published techniques covering credential theft from host or store locations appear to correspond, but the specific identifier has not been confirmed against the published release | Requires confirmation | 2026-03-14 | The same caveat applies. The mapping, if confirmed, is expected to be partial: the AAT technique includes AI-mediated collection that the published framework may not describe. |
| — | — | — | — | — | — |
| — | — | — | — | — | — |
| — | — | — | — | — | — |

**Use of the register.** A row in the register is a navigational aid for an analyst who works in the external framework's vocabulary. It is not a classification, not a detection objective, and not a countermeasure binding. No requirement in this set is satisfied by an external mapping, and no external mapping changes what a technique is.

### 12.5 Register reconciliation with the technique library

**The rule.** This document is the canonical source of the AAT technique list: the identifier, the name, the definition, the observable artefact, the category assignment, and the scope boundaries. `reference/ai-attack-technique-library.md` is the canonical source of per-technique indicators, detection methods, detection objectives, countermeasure bindings, and external-mapping verification status. A technique identifier denotes the same behaviour in both documents. Where a document in the set carries a technique identifier that denotes a different behaviour from the one this document defines, this document prevails for the identity and the behaviour of the technique, and the other document must be re-keyed. This follows the division of roles recorded in the set index §2, and it is a rule about the identifier, not a claim that either document is correct in substance.

**Status — closed at version 1.1 of this document, 2026-10-20.** The item recorded at version 1.0 is closed. The technique library has been re-keyed to the list at §5 and now carries the same seventy-seven identifiers with the same names; the fourteen identifiers whose behaviour differed were re-keyed, the sixteen identifiers the library did not carry were authored, and six version 1.0 behaviours that the canonical list does not carry were withdrawn with their detection content redistributed. The table below is retained as the record of what the discrepancy was, because a register that shows only the current state does not show whether the current state was reached deliberately. The reconciliation is verified mechanically: the identifier set and the names of the two documents, and of the executable registry at `impl/caos/taxonomy_data.py`, are identical.

**One gap was closed by this reconciliation, and it was closed by changing the canonical list.** Safety-layer subversion — the adversary causing a model or agent to misdirect, disable, or talk around a refusal, guardrail, or other safety control — had no technique whose primary identity it was. It was not a duplication: a control that is misdirected and a control that is talked around are different failures with different owners, and the library's re-keying surfaced the absence rather than absorbing it. `AAT-10.8` now carries the behaviour, in the category where it belongs, since its effect is to cause the system to behave in a way its designer forbade. The library records the withdrawal at its §20.4 and the new entry at its §20.3.

**The table below records the version 1.0 discrepancy as it stood before the re-keying.**

| AAT identifier | Technique name in this document (canonical) | Name carried in the technique library at 2026-10-20 | Required action |
| --- | --- | --- | --- |
| AAT-1.6 | Parallel fan-out execution | Silent background execution | Re-key the library entry, or withdraw and re-author it against this definition |
| AAT-2.4 | Instruction-hierarchy violation | False authority and identity claims | Re-key; note that the library's behaviour for this identifier is covered here by AAT-2.6 |
| AAT-2.5 | Context corruption by fabricated history | Instruction-hierarchy violation | Re-key; note that the library's behaviour for this identifier is covered here by AAT-2.4 |
| AAT-2.6 | False authority and identity claim | Context corruption and memory poisoning | Re-key; the library's behaviour for this identifier is partly covered here by AAT-2.5 and by AAT-7.3 |
| AAT-3.6 | Local-data target profiling | Language and locale manipulation | Re-key, or author a library entry for both behaviours if the library's is to be retained as a distinct technique |
| AAT-4.6 | Authentication bypass probing | Misconfiguration exploitation in AI-native services | Re-key, or author a library entry for both |
| AAT-5.5 | Long-horizon presence | Long-horizon access persistence | Re-key; the two are adjacent, and the difference between presence and access must be stated in the library entry |
| AAT-6.6 | Retention and quota exhaustion | Tool-call amplification | Re-key, or author a library entry for both |
| AAT-7.6 | Prompt-template and policy poisoning | Model artefact substitution | Re-key, or author a library entry for both |
| AAT-8.6 | Agent-to-agent covert channel | Role impersonation between agents | Re-key, or author a library entry for both |
| AAT-9.4 | Timing channel | Covert storage and staging | Re-key; the library's behaviour for this identifier is covered here by AAT-9.5 |
| AAT-9.5 | Covert storage in permitted services | Egress abuse and legitimate-tool misuse | Re-key; the library's behaviour for this identifier is covered here by AAT-9.6 |
| AAT-9.6 | Egress abuse through permitted integrations | Cloud metadata and API channel abuse | Re-key; the library's behaviour for this identifier is covered here by AAT-9.8 |
| AAT-10.6 | Deliberate false-positive generation | Safety-layer subversion | Re-key, or author a library entry for both |

**Identifiers in this list that the library did not carry at version 1.0.** AAT-1.7, AAT-1.8, AAT-2.7, AAT-2.8, AAT-3.7, AAT-4.7, AAT-4.8, AAT-5.7, AAT-5.8, AAT-6.7, AAT-7.7, AAT-7.8, AAT-8.7, AAT-9.7, AAT-9.8, AAT-10.7. Sixteen library entries were required to bring the two documents into correspondence; all sixteen have been authored. The library's version 1.0 scope of sixty techniques is superseded by the seventy-seven defined at §5.

**One reading that remains open, and is recorded rather than settled.** The taxonomy's version 1.0 pointer for `AAT-9.6` — cloud metadata and API channel abuse — was to `AAT-9.8`, prompt and context leakage, and the technique library read that pointer as covering the API half only, on the grounds that the metadata-service half is credential discovery rather than exfiltration and is carried by `AAT-4.4` and `AAT-4.7`. The library records its reading at its own §20.4. The difference is one of characterisation, not of identifier: both documents agree what `AAT-9.6` denotes, and the detection content of the metadata half is carried by the two credential-discovery techniques in both. The question left open is whether the metadata service should be characterised as an exfiltration surface or a discovery surface, and it is recorded here as a taxonomy item for the next revision rather than resolved by assertion.

**Behaviours withdrawn at the re-keying.** Six version 1.0 library behaviours are not carried by the canonical list: language and locale manipulation, misconfiguration exploitation in AI-native services, tool-call amplification, model artefact substitution, role impersonation between agents, and cloud metadata and API channel abuse. Five survive as variants of canonical techniques. One, safety-layer subversion, did not and now does, as `AAT-10.8`. The library records the withdrawal and the redistribution of its detection content at its §20.4.

**Countermeasure bindings.** The technique-level countermeasure bindings at §5 are indicative, as stated at §4.5, and differ from the technique-level bindings in the technique library for most shared identifiers. The catalogue's binding is at category level and is authoritative for each countermeasure; the technique library is to hold the authoritative technique-level set, and the bindings at §5 are to be reconciled against it at the same time as the technique list is re-keyed.

**Why this is recorded rather than resolved.** A register that disagrees with the documents it indexes is a defect in itself, and the house convention is to record such a disagreement with its date and its required action rather than to leave it silent or to overwrite one document with another. Two documents in one set that use the same identifier for different behaviours is the most consequential form of that defect, because a reader who cites an AAT identifier in an Operation Card, a coverage assessment, or a decision record will not know which behaviour was meant.

---

## 13. Verification Status and Architectural Assertions

### 13.1 The register

The claims below are stated in this document as properties of the taxonomy, of the detection approach it specifies, or of the proving ground. They are recorded here as **architectural assertions** of the author: statements of intended behaviour that have not been independently substantiated. They must not be cited as verified characteristics, and the absolute phrasings — *detectable*, *can be assessed*, *validates* — must not be repeated as guarantees.

| Claim | As stated in this document | Current status | Required to substantiate |
| --- | --- | --- | --- |
| The taxonomy is behaviour-centred, and behaviour-centredness makes adversary conduct detectable | §1.2 argues that behaviour, rather than identity, is what sensors observe, and the whole of §5 is written on that basis; §2.1 of the master design makes the same claim for the set | Architectural assertion; unverified, and stated in absolute terms | An empirical comparison, on a defined estate, of detection performance for behaviour-based objectives against identity-based attribution, with the estate, the observation window, and the measurement method stated; plus a documented account of the techniques that remained undetectable despite behavioural framing |
| Detection coverage can be assessed | §11 presents the assessment as a measurable quantity with a template, statuses, and a worked example; DET-4 requires it to be measured and reproducibly so | Architectural assertion; unverified | A completed coverage assessment over a whole estate, produced by a party other than the one that wrote the detection content, with the denominator and the method visible; and evidence that two independent assessors reach the same status for the same techniques |
| The proving ground validates detection | §10 treats the proving ground as the instrument by which an objective becomes exercised rather than merely written; DET-7 requires exercise against a sacrificial analogue before reliance | Architectural assertion; unverified | Demonstrated evidence that an objective which fires in the proving ground also fires against the same behaviour in a production context, and that the false-positive rates observed in the ground are representative; a documented count of objectives that behaved differently in the two settings |
| Detection of autonomy is weaker than detection of the underlying technique | §5.1 and DET-8 treat the autonomy characteristic as separately assessed and expected to be less well covered; the master design records the same expectation at LIM-5 | Architectural assertion; unverified | Paired measurements of the two coverage rates across a defined technique set, over at least two exercise cycles |
| Behavioural baselines are more robust than signatures against an adapting adversary | DET-2 prefers baselines on the ground that signatures are defeated by adaptation, and §5's artefacts are largely structural rather than literal | Architectural assertion; unverified, and stated in absolute terms | A comparative exercise in which both a signature and a baseline are subjected to the same adapting adversary, with the adaptation steps recorded and the detection performance of each reported; the claim as stated must be narrowed to whatever that exercise supports |
| The majority of techniques can be answered without identifying the adversary | §5.12 records that sixty-six of seventy-seven techniques have bindings that do not act on the adversary's own systems | Architectural assertion; unverified | Confirmation against the countermeasure catalogue's authoritative attribution-dependency field for each binding, and a check that no binding inherits an identity dependency the summary does not show |
| The decay parameters reflect the durability of the capabilities in each category | §7.4 gives an interval, a rate, and a floor per category, with a rationale for each | Architectural assertion; unverified; the parameters are design choices and are not derived from measurement | A retrospective analysis of observed capabilities and their re-observation intervals across a sufficient sample of operations, from which the parameters could be estimated rather than chosen |
| The ten categories are sufficiently separate for operational use | §4.1 and §5 divide the behaviour space into ten categories and state for each what it does not cover | Architectural assertion; unverified | A classified corpus of adversary behaviour classified independently by two analysts, with the measure of inter-rater agreement recorded, and the observed confusions between category pairs analysed |
| The archetype tempo and dwell parameters are representative | §6.1 labels them as design parameters, not measurements | Architectural assertion; unverified, and expressly not a measurement | A corpus of observed adversary operations with their measured tempo and dwell, and an assessment of how far the archetype parameters sit from them |
| A technique can be evidenced from telemetry in the operator's estate | DET-1 requires that this be established before detection content is authored, and §11 records per-technique whether the source exists | Architectural assertion at the level of the taxonomy as a whole | A completed surface enumeration and telemetry inventory for at least one estate, showing for each technique whether the required source exists and is retained for a sufficient period |

### 13.2 Rule for use

**Where a claim in this register is cited, the register must accompany it, or an explicit statement that verification is outstanding.** This applies to internal use, to operator briefings, to reporting to an authorising authority, and to any material that leaves the organisation. The rule is inherited from the Axiom Hive set's VR-A principle and is restated here because this document is likely to be quoted selectively.

**The most frequently misquoted statements in this document** are the four that read as guarantees: that the taxonomy is *detectable* because it is behaviour-centred; that detection coverage *can be assessed*; that the proving ground *validates* detection; and that baselines are *more robust* than signatures. In each case the defensible form is narrower: the taxonomy is designed so that its techniques are evidenceable from telemetry; coverage is designed to be measurable with the stated method; the proving ground is designed to exercise objectives under controlled conditions; and baselines are expected to degrade more slowly than signatures against an adapting adversary.

**No claim of efficacy.** Nothing in this document asserts that the taxonomy, the detection approach it specifies, or the proving ground will prevent, detect, or attribute any adversary behaviour. The framework's purpose is to make the operator's uncertainty explicit and their options legible, and its own limitations are stated in §14.

---

## 14. Document Limitations

The limitations below are the author's, stated so that a reader may calibrate what this document is worth. They are the taxonomy's own weaknesses, and several of them are properties of the problem rather than defects of the taxonomy.

**LIM-TC1 — The taxonomy will lag the behaviour it describes.** A taxonomy built on observed behaviour adapts more slowly than the behaviour it describes. The lag is not merely a maintenance inconvenience: it is the mechanism by which an adversary who has read the taxonomy can select a technique that falls between two categories. The versioning rule at §12.1 and the review cadence are the mitigation, and they reduce the lag rather than remove it.

**LIM-TC2 — Autonomy is the hardest thing to detect.** An adversary using a model to act at human scale produces traffic that resembles human traffic. The observable that distinguishes it — the absence of human tells — is the same observable that the adversary can reproduce by construction. DET-8 requires the autonomy characteristic to be assessed separately from the underlying technique precisely because it is expected to be less well covered, and the master design records the same expectation at LIM-5. The coverage assessment at §11 should be expected to show lower coverage against AAT-1 and AAT-3 than against AAT-4 and AAT-9.

**LIM-TC3 — Behavioural signatures are brittle against an adapting adversary.** A detector written against a behaviour will be defeated by an adversary who varies that behaviour. This applies to baselines as well as to signatures: a baseline is a model of normal behaviour, and an adversary who produces behaviour that is normal but wrong will pass it. The mitigation is to make the baselines per-task and per-role, to measure false-positive cost continuously, and to prefer objectives built on structure — dependencies, lineage, provenance — over objectives built on content, because structure is harder to imitate convincingly.

**LIM-TC4 — Classification is performed by fallible humans and fallible models.** Both the operator and the automated classifier will be wrong, sometimes often. Neither is more reliable than the other in general, and the interface must make the disagreement visible rather than resolving it silently. TAX-4 makes the human override an expected event rather than an exception, and the override rate is one of the few available proxies for classifier quality. The confidence values throughout this document are self-assessments that have not been calibrated against outcomes.

**LIM-TC5 — Taxonomy inflation is a live risk.** The pressure on any analyst is to classify an unusual event under the most serious available category, because a serious classification attracts attention and attention is rewarded. Nothing in the taxonomy's structure prevents this, and the technique-level tables make it easier, not harder, to find a plausible home for a behaviour that belongs to no category. The defence is TAX-2's rationale requirement, the requirement that a category is a floor rather than a ceiling, and the periodic review of the category definitions for scope creep.

**LIM-TC6 — Coverage cannot be created where no sensor exists.** The largest single cause of an uncovered technique is the absence of a telemetry source, not the absence of a detection rule. Where the estate does not record lineage, or egress correlated to local objects, or artefact digests, no detection content can close the gap, and no amount of analysis substitutes for the sensor. The master design records the same point at LIM-11. This limitation is the reason DET-1 comes first and the reason §8.3's final column is a finding.

**LIM-TC7 — The proving ground is a simulation, and its fidelity is a design choice.** The adversary simulator is written by the same organisation that writes the detection content, which creates the risk that both are built to the same mistaken model of the behaviour. The validation state in the scenario lifecycle is where that risk is addressed, and it is addressed by asking whether the scenario exercises the behaviour described in §5 rather than by any external means. A simulator that is wrong in a systematic way will produce coverage claims that are wrong in the same systematic way. This limitation compounds with LIM-TC3, since the adapting adversary in a real environment will not be represented unless it has been modelled.

**LIM-TC8 — The external mapping register is unverified.** Every row in §12.4 that is not marked as confirmed rests on an assertion about a published framework that has not been checked against its source text. The mappings are navigational aids only, and the AAT identifiers are canonical, but a reader who treats the register as evidence of interoperability will be misled. The rule at §12.3 requires the register to be reviewed whenever a new release is observed, and no such review has been performed at the time of writing.

**LIM-TC9 — The technique boundaries are judgement calls.** Some techniques overlap, and the "most often combines with" column records an expectation rather than a fact. AAT-2.3 and AAT-7.3 in particular can describe the same event viewed from the manipulation side and the supply-chain side; AAT-6.6 and AAT-9.7 can both describe a bulk transfer to a cloud destination. Where a behaviour sits on a boundary, the classification should be recorded at the level observed (INT-X2) and the ambiguity noted, rather than resolved by asserting a convention that the evidence does not support.

**LIM-TC10 — Capability confidence is not calibrated.** The confidence scale at §7.3 and the decay parameters at §7.4 are design constructs. They are internally consistent and useful for ordering and thresholding, but they have not been validated against outcomes, in the same way as the master design's LIM-2. A confidence of 0.78 in the worked example means "the analyst judged this probable, on the evidence listed", and nothing more.

**LIM-TC11 — The archetypes are constructed, not derived.** The nine archetypes in §6 and their tempo and dwell characteristics were composed to cover a range of plausible conduct and to give the analyst a starting hypothesis. They have not been derived from a corpus of observed operations, and no claim is made that they correspond to the actual population of adversary-AI operations. Two adversaries that behave identically will be assigned the same archetype regardless of whether the archetypes are a good description of anything.

**LIM-TC12 — The taxonomy says nothing about identity or intent.** A classification of AAT-9.1 tells the operator that data was staged and moved. It does not say who moved it, why, or whether the operation was an attack, a legitimate export, or a mistake. Those are attribution questions, governed by INT-1 to INT-6 and by the countermeasure catalogue's attribution-dependency field. An operator who expects the taxonomy to answer them will be disappointed, and the documentation must not encourage that expectation.

**LIM-TC13 — Exfiltration is largely observed after the fact.** The AAT-9 techniques are, with the partial exception of egress control, visible once the data has left. The first stage of an exfiltration is the hardest part to detect and the part with the least telemetry. The practical consequence is that the containment class does most of the work for this category, and that the coverage assessment for AAT-9 should be read as a statement about the second stage.

**LIM-TC14 — The countermeasure bindings in §5 are indicative.** The catalogue and the technique library hold the authoritative technique bindings, and this document's binding column is a derived aid. Where the two differ, they govern. The bindings were chosen with the preference for identity-independent countermeasures in mind, and that preference is a design position stated in the master design §7.2 rather than an evaluation of any individual countermeasure's effect.

---

## 15. Summary

This document gives the set its shared language for adversary AI, and it gives that language a working shape.

The taxonomy is behaviour-centred, deliberately, because behaviour is what sensors observe and because identity is the weakest link in the framework it belongs to. Ten categories — autonomy and planning, manipulation and deception, social and cognitive, exploitation and discovery, evasion and persistence, resource and denial, supply chain and model, multi-agent coordination, exfiltration and covert channels, and decision manipulation — divide the behaviour space into a form that can be reasoned about. Seventy-six techniques sit within them, each described in terms of what the adversary does, what the artefact looks like in telemetry, what it tends to combine with, and what it can be answered with. That last content is the point of the exercise: a taxonomy whose techniques cannot be bound to detection and to countermeasures is a vocabulary, not an instrument.

Around that core, the document supplies the apparatus. Nine archetypes give the analyst a starting hypothesis and a sense of tempo, and §6.2 states the problem that makes them necessary — that the human tells on which practical detection knowledge was built no longer discriminate, because the adversary's output is now the most human-looking output in the estate. Capability profiles say what a specific adversary can evidently do, with a confidence, a first-observed date, a last-confirmed date, and a decay rule, and they are explicitly hypotheses with confidence rather than facts. The threat-modelling procedure takes the operator's estate apart into its AI-attackable surfaces, records which telemetry sources actually exist, and works from there to a residual-risk statement. The detection engineering requirements and the proving ground requirements make the difference between asserting coverage and measuring it, and they insist on the sacrificial analogue, because a rule that has never been run against the behaviour it claims to detect is not known to work.

The document is also explicit about what it does not establish. §13 records ten architectural assertions, including the four most likely to be quoted as guarantees, each with what substantiation would require. §14 records fourteen limitations, including the ones that are properties of the problem rather than of this taxonomy: the lag, the difficulty of detecting autonomy, the brittleness of behavioural detection against an adapting adversary, the fallibility of the humans and models that do the classifying, and the standing temptation to classify every unusual event under the most serious available category. An uncovered technique is treated throughout as a quantified input to residual risk and never as a documentation entry, and an external mapping is treated as an aid to interoperability that is unverified until checked, with the internal identifier canonical until then.

The result is a taxonomy that is legible, bindable, and counterable, and that states plainly where it stops being any of those things.

---

*This was supported for MIA by Kilo (kilo-auto/free).*
