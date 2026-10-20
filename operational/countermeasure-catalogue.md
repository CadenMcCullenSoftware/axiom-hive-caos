# Countermeasure Catalogue: CAOS — Counter-Adversary Operations System

| Field | Value |
| --- | --- |
| Author | MIA |
| Attribution | This was supported for MIA by Kilo (kilo-auto/free). |
| Document type | Catalogue |
| Subject | The countermeasure catalogue for the Counter-Adversary Operations System: forty-three countermeasures in seven classes, each with a declared direction of effect, collateral class, reversibility, autonomy class, attribution dependency, preconditions, failure modes, side effects, and residual-risk assessment |
| Version | 1.1 |
| Status | Authoritative for catalogue content; subordinate to `system-design-and-framework.md` and to the constitutional instrument |
| Revision note | Version 1.1 reconciles the catalogue's category-level AAT bindings against the technique-level bindings recorded at `reference/ai-attack-technique-library.md` §20.5. Thirty of the forty-three entries were widened to carry every category the library's bindings imply; the other thirteen already did. The reconciliation moved in one direction only: the catalogue's lists were brought up to the library's, because the library's set is the finer instrument and narrowing it to satisfy a category-level list would have deleted sound claims. The divergence between the two instruments is now zero, and it is held in code at `impl/tests/test_bindings.py` so that it may fall further but must not rise. No entry's class, collateral class, reversibility, autonomy class, profile minimum, attribution dependency, residual-risk figure, or status was altered, and no entry was added, removed, or renumbered |
| Companion documents | `system-design-and-framework.md`; `constitutional/engagement-authorisation-and-rules-of-engagement.md`; `compliance/operator-conduct-and-human-in-loop-standard.md`; `operational/mission-lifecycle-and-decision-loop.md`; `operational/adversary-ai-taxonomy-and-threat-model.md`; `operational/decision-support-and-scoring-model.md`; `operational/watchfloor-interface-specification.md`; `operational/platform-architecture-and-agent-containment.md`; `reference/ai-attack-technique-library.md`; `reference/audit-and-conformance-procedures.md`; `templates/operation-card.md` |
| Identifier series owned by this document | `CM-1` to `CM-10`; `OCC-01` to `OCC-43`; `LIM-CAT1` to `LIM-CAT13` (see §11 for the prefix note) |

---

## 1. Purpose and Scope

### 1.1 What a catalogue entry is for

This catalogue is the working inventory of the countermeasures available to a CAOS operator. Each entry exists so that an operator, at the moment of decision, can answer five questions without leaving the record:

1. **Does this countermeasure bear on the activity I have classified?** The entry declares the AAT categories whose techniques it addresses.
2. **What will it cost, and to whom?** The entry declares its collateral class, its blast radius, its side effects, and its reversibility.
3. **What must be true before I may use it?** The entry declares its preconditions, its minimum ROE profile, and its attribution dependency.
4. **What do I get besides the effect?** The entry declares its intelligence yield, its evidence produced, and its operator burden.
5. **How do I know it worked, and what happens if it does not?** The entry declares its failure modes and its degradation behaviour.

The entry is a card, not a procedure. It tells an operator what the countermeasure is, what it costs, and when it will not work. The procedure itself lives in the platform's own runbooks and in the Operation Card for the specific deployment.

### 1.2 What this catalogue is not

**This catalogue is descriptive. It does not authorise anything.**

| The catalogue does | The catalogue does not |
| --- | --- |
| Describe what a countermeasure does | Authorise its use |
| Assign a collateral class | Substitute for the engagement authorisation |
| Assign a minimum ROE profile | Substitute for the approval at the depth that class requires |
| State the attribution dependency a countermeasure carries | Assert that the attribution threshold is met in any given case |
| Record a residual-risk reduction band | Serve as the effectiveness figure `e` on a card |
| Record a failure mode | Predict that the failure will not occur |
| Record an evidence basis | Assert that the evidence has been gathered |
| State that an entry may be used at a profile | Create that authority |

An entry's presence in this catalogue is a statement about what the operator *could* do, at what cost, under what conditions. It is not permission. Every use remains subject to the engagement authorisation, the admissibility algebra `AD-1` to `AD-12` in `operational/decision-support-and-scoring-model.md`, and the approval depth named for the entry's collateral class. A countermeasure that appears here and is inadmissible for a card does not become admissible by being catalogued.

### 1.3 Relationship to the surrounding documents

The master design fixes the class structure and states `CM-1` to `CM-3`. This document restates those three requirements in full, extends the series to `CM-10`, and supplies the catalogue they govern. The constitutional document fixes the authorisation model, the collateral classes, the autonomy classes, and the ROE profiles. This document does not restate the constitutional content in a form that could be used in place of it; it references it, and where an entry carries a class, that class is the constitutional class as at the version of the constitutional document in force.

Where this catalogue and the master design appear to differ, the master design prevails. Where this catalogue and the constitutional document appear to differ, the constitutional document prevails.

### 1.4 Register reconciliation

At version 1.0 of this document the class-rule series runs to `CM-10` and the catalogue contains forty-three entries, `OCC-01` to `OCC-43`, grouped `OCC-01`–`OCC-07` (CM-A Detect), `OCC-08`–`OCC-16` (CM-B Harden), `OCC-17`–`OCC-23` (CM-C Contain), `OCC-24`–`OCC-27` (CM-D Observe), `OCC-28`–`OCC-33` (CM-E Deceive), `OCC-34`–`OCC-39` (CM-F Disrupt), `OCC-40`–`OCC-43` (CM-G Recover). The set index register now records `CM-` as 10 and `OCC-` as 43, and the class series `CM-A` to `CM-G` is registered alongside them, so the two registers agree.

**Version 1.1 note.** This paragraph previously recorded a disagreement between this document and the set index, and asked for the index to be updated. The index has been updated, and the note is retained only to record that the disagreement existed and was closed. A register that disagrees with the documents it indexes is a defect in itself, and the record of the disagreement is part of the correction.

### 1.5 Proposed additions, recorded pending the next catalogue revision

The emergency shutdown and containment protocol at `operational/emergency-shutdown-and-containment-protocol.md` Annex C identifies four emergency actions that bind to no entry in this catalogue. They are the provider-side quota suspension, the scheduled-job and timer suspension, the metadata and link-local path block, and the device re-image. The protocol records them as proposed additions to be catalogued at the next revision of this document, and until then they are available only under the emergency card's own authority and their use is a reportable event.

This section is that record. It names the four, states the class each would take, the binding constraints each would carry, and the reason each has no home today. It does not catalogue them, and it does not change their status: the emergency path continues to treat them as emergency-only actions whose use is reportable.

| Proposed entry | Would be class | Direction of effect | Collateral | Why it binds to nothing today |
| --- | --- | --- | --- | --- |
| Suspend the deployment's quota and budget at the provider | CM-C Contain | The provider's service, scoped to the principal | C0 | The effect lands on a third party's service. No existing entry acts outward on a metered service, and the class's collateral ceiling and its reversibility profile do not describe a provider-side action |
| Suspend the deployment's scheduled jobs, timers, webhooks, and background workers | CM-C Contain | The operator's own estate | C0 | The surface is the operator's own automation, but it is not a persistence surface any existing entry treats, and the catalogue's containment entries address the agent's own capabilities rather than the operator's schedulers |
| Block the metadata, link-local, and instance-credential paths for the workload | CM-B Harden | The operator's own estate | C0 | The control is a workload-level restriction on a cloud service's credential path. No hardening entry addresses the instance-credential path, and the boundary is a construction property rather than a configuration one |
| Re-image or factory-reset a compromised device | CM-G Recover | The operator's own device | C1 | The action is irreversible, destroys user data on the device, and is a recovery action rather than a containment one. No recovery entry in this catalogue is irreversible, and the class's reversibility profile does not admit one |

**A note on why the catalogue has not absorbed them.** Two of the four act on something the operator does not own, one is irreversible, and one is a boundary that cannot be expressed as a configuration change. A catalogue in which those entries sit beside the reversible, own-estate, configuration-level entries that make up the rest of the set would misrepresent the set's assurance: a reader of the catalogue would reasonably infer that every entry in it is as reversible and as confined as the entries around it. The protocol's own rule — that these four are available only under the emergency card's own authority and their use is reportable — is the honest representation of their status, and it is preserved here unchanged.


---

## 2. Interpretation of Normative Terms

The terms **must**, **must not**, **should**, **should not**, and **may** are to be interpreted as described in RFC 2119.

- **Must / must not** denote absolute requirements. A requirement so marked is a condition of validity, not a preference.
- **Should / should not** denote recommendations that may be departed from only where legitimate reasons exist; any departure should be made explicit and recorded.
- **May** denotes optional behaviour that remains at the operator's discretion within the constraints of this document and the authorisation in force.

Where this document records a claim about the behaviour of a countermeasure, that claim is an **architectural assertion** of the authors and not, absent explicit statement to the contrary, an independently verified property. The register of such claims is §10, and the register of the catalogue's own limitations is §11.

Where this document records a quantitative value, the value carries a stated confidence and a stated evidence basis. Where the basis is absent, the value is retained and marked as unverified rather than deleted or silently confirmed; the house treatment of unverified quantitative data is set out in §8.

---

## 3. Defined Terms

| Term | Definition |
| --- | --- |
| **countermeasure** | A declared, bounded action or control that the operator may take, or may prepare to take, in response to adversary AI activity, recorded in this catalogue with its class, direction of effect, collateral class, reversibility, autonomy class, and preconditions. |
| **countermeasure class** | The designation CM-A to CM-G that places a countermeasure in the response sequence and determines the treatment its selection receives under the decision-support model. |
| **direction of effect** | The declared direction in which a countermeasure's intended effect falls: **inward** on the operator's own estate; **outward** on the adversary's own systems or infrastructure; **inward/outward** where the effect is on the adversary's behaviour expressed through the operator's own environment; **none** where the effect is on the operator's knowledge rather than on either party's capability. |
| **collateral class** | The class C0 to C3 that governs the approval depth at which a countermeasure may be used, determined by its actual effect and never by the operator's intent. |
| **reversibility** | The degree to which a countermeasure's effect can be undone by the operator, on the four-point scale **reversible**, **reversed**, **low**, **none**. |
| **reversible / irreversible** | The binary property that follows from a reversibility value. An effect is reversible where it can be fully undone by an action available to the operator within the stated window; it is irreversible where it cannot. |
| **autonomy class** | The class AC-0 to AC-4 describing how a countermeasure executes. Autonomy is a property of execution, not of intelligence. |
| **attribution dependency** | The level of attribution a countermeasure requires before it may be used: **none**, **behavioural**, **class**, **identity**, or **external**. |
| **preconditions** | The conditions that must hold in the estate, in the authorisation, or in the platform before a countermeasure may be dispatched. A countermeasure whose preconditions are not met is inadmissible under `AD-1` to `AD-12` and is not attempted. |
| **failure mode** | The condition under which a countermeasure does not achieve its intended effect, or achieves a materially different one. |
| **side effect** | A consequence of a countermeasure that falls outside its stated intended effect, whether beneficial or harmful. |
| **blast radius** | The set of systems, accounts, identities, data, and actors affected by a countermeasure's execution, expressed as a boundary rather than as a number. |
| **profile minimum** | The lowest rules-of-engagement profile at which a countermeasure may be used, recorded on each entry and enforced at admissibility. |
| **intelligence yield** | The ordinal assessment of the adversary-facing information a countermeasure is expected to produce: none, low, moderate, or high. |
| **evidence produced** | The specific artefact a countermeasure emits for the audit record and for the substantiation of its own residual-risk reduction figure. |
| **operator burden** | The ordinal assessment of the human attention and effort a countermeasure consumes to configure, supervise, and maintain: low, moderate, high, or very high. |
| **degradation behaviour** | The specified behaviour of a countermeasure when its inputs, telemetry, or dependencies are degraded or absent, as distinct from its failure mode. Degradation is a designed state; failure is not. |
| **the intelligence loop** | The cycle in which observation produces a hypothesis, the hypothesis produces a countermeasure, the countermeasure produces evidence, and the evidence improves detection and the next hypothesis. |
| **the third-party test** | The test at master design §4.2 (`AUTH-8`) of who else depends on the infrastructure an action would affect, what their interest is, and the expected harm to them. It is applied to every countermeasure whose effect falls outside the operator's own estate. |
| **the operator's estate** | The systems, identities, data, networks, services, and personnel that the operator owns or lawfully controls and is responsible for. |
| **adversary system** | An AI system, model, agent, or agentic service, identified as belonging to the adversary operator, that conducts activity against the operator or the operator's estate. |
| **adversary infrastructure** | The hosting, transport, storage, identity, and provider infrastructure on which adversary systems depend, including shared and third-party infrastructure. |
| **the Watchfloor** | The operator console; the interface through which the human operator acts. |
| **ROE profile** | One of R0 Observe, R1 Shield, R2 Trap, R3 Deceive, R4 Disrupt, R5 Neutralise; the ceiling on what an operation may do. |
| **residual risk** | The quantity `R = S_eff × (1 − e)` carried forward after the selected countermeasures, as defined in `operational/decision-support-and-scoring-model.md`. |
| **AAT category** | One of AAT-1 to AAT-10; the behaviour-centred classification of adversary activity defined in the master design §5.2. |
| **AAT technique binding** | The association between a countermeasure and the AAT categories whose techniques the countermeasure bears on. Catalogue-level bindings are recorded at category granularity; finer technique-level bindings are maintained in `reference/ai-attack-technique-library.md`. |
| **interaction hazard** | A defined circumstance in which two countermeasures, deployed together or in sequence, defeat, degrade, or contradict one another. |
| **last-known-good** | A state, artefact, or configuration previously recorded as correct and integrity-verified, to which a compromised component may be returned. |
| **honeytoken** | A credential, token, or record whose presence or use indicates unauthorised access to a location it should never reach. |
| **decoy** | A deliberately exposed resource with no legitimate business purpose, existing to be found by an adversary. |
| **deceptive response shaping** | The presentation of a controlled, false, or misleading but non-actionable response to an adversary, for the purpose of shaping the adversary's next action. |
| **deconfliction** | The check that a countermeasure does not interfere with a live legitimate operation. |
| **verification status** | Verified (primary), Verified (secondary), Corrected, Unverified, or Requires confirmation, as defined in the set index §3. |
| **architectural assertion** | A statement of intended system behaviour that has not been independently substantiated; see §10. |
| **claim label** | One of Fact, Estimate, Interpretation, Hypothesis, Recommendation, as defined in the set index §3. |
| **evidence basis** | The class of evidence underlying a quantitative claim in this catalogue: **E1** measured in the operator's own estate; **E2** measured in the proving ground or an exercise; **E3** measured in a comparable environment; **E4** design-intent estimate; **E5** no supporting basis. |
| **withheld** | A catalogue status indicating that the entry exists and is described, but that its use is withheld pending a stated condition. |
| **retired** | A catalogue status indicating that the entry is no longer available for use, and is retained in the catalogue so that historical records remain interpretable. |

---

## 4. The Seven Countermeasure Classes

### 4.1 Class structure

| Class | Name | Purpose | Direction of effect | Typical collateral class | Typical reversibility | Minimum ROE profile |
| --- | --- | --- | --- | --- | --- | --- |
| **CM-A** | Detect | Improving the operator's ability to see, so that later decisions rest on better evidence | Inward, except where the countermeasure deliberately provokes an adversary response | C0 | Reversible | R0 Observe |
| **CM-B** | Harden | Reducing the attack surface or the consequence of attack, so that the adversary's technique fails | Inward | C0 | Reversible | R0 Observe |
| **CM-C** | Contain | Isolating the adversary's actions, or the compromised component, from the rest of the estate | Inward | C0 | Reversible to reversed | R1 Shield |
| **CM-D** | Observe | Learning the adversary's behaviour in a controlled environment, under authorisation | Inward/outward, or none where the effect is on knowledge alone | C0 to C1 | Reversible | R1 Shield; R2 Trap where the engagement is bounded |
| **CM-E** | Deceive | Shaping the adversary's environment so that its actions lead it to what the operator wants it to touch, or away from what it must not touch | Inward/outward | C0 to C1 | Reversible | R3 Deceive |
| **CM-F** | Disrupt | Removing the adversary's capability to act: its credentials, its egress, its compute, its reachability | Outward, except where the effect is exerted at the operator's own perimeter | C0 to C2 | Reversed to none | R4 Disrupt; R1 Shield where the effect is at the operator's own perimeter |
| **CM-G** | Recover | Restoring the estate after an operation, and preserving the ability to do so | Inward | C0 | Reversible | R1 Shield |

The class is a statement of *kind*, not of *permission*. The minimum profile in the final column is the lowest profile at which an entry of that class **may** be used at all; an individual entry may carry a higher minimum, and does. A class minimum of R0 for CM-A does not mean that a detection countermeasure may be run at R0 without an engagement authorisation: `AUTH-1` and `OP-1` apply to every countermeasure dispatch irrespective of class.

### 4.2 Class rules

**CM-1 — Direction of effect is a property, not a claim.** The catalogue records, for each countermeasure, the direction of its effect. A countermeasure whose stated effect is on the adversary's system but whose actual effect is on the operator's estate is classified by its actual effect. This rule overrides the name, the summary, and the operator's stated intention.

**CM-2 — The environment-shaping preference.** Where a deception countermeasure achieves an acceptable reduction in residual risk, it is preferred over a disruption countermeasure. Shaping the adversary's environment is cheaper, more reversible, less likely to harm third parties, and produces more intelligence about the adversary. The preference is a preference and not a prohibition; where it is departed from, the Operation Card records why, in the words of the person who decided.

**CM-3 — Containment before disruption.** A countermeasure that limits the adversary's reach is preferred over one that destroys its capability, where both are effective. Containment preserves the intelligence that disruption destroys.

**CM-4 — Every countermeasure declares its direction of effect.** No entry may be admitted to the catalogue without a declared direction of effect and a declared target set. An entry whose direction of effect cannot be stated because the effect is not yet known is not ready for the catalogue and is held as a proposed measure in the mission's own working papers, where it is governed by the same authorisation rules.

**CM-5 — The combination rule.** A combination of countermeasures takes the properties of its most restrictive member. Its collateral class is the maximum of the members' collateral classes; its reversibility is the least reversible member's reversibility; its autonomy class is the highest member's autonomy class; its profile minimum is the highest member's profile minimum. A combination may not be used at a profile below that minimum, and the combination does not become permissible because the members are individually permissible.

**CM-6 — The non-weaponisation binding.** No countermeasure in this catalogue may use one AI system to attack, degrade, or destroy another AI system, its weights, or its training data, and no entry may be implemented by such means. This includes entry whose class is CM-F Disrupt. Where a disruption countermeasure is implemented, it acts on credentials, reachability, compute entitlement, or service state — not on the adversary's model. This binding is enforced at `AD-12`.

**CM-7 — The evidence rule.** Every countermeasure that carries a residual-risk reduction figure must also carry the evidence basis for that figure and a stated confidence. A figure with no evidence basis is retained, marked, and must not be used as the effectiveness term `e` on a card. The full rule is §8.

**CM-8 — The retirement rule.** A countermeasure that is retired, superseded, or rendered undeliverable remains in this catalogue with its status field marked. Its entry is not deleted. Historical Operation Cards, decision records, and after-action reports cite catalogue entries by identifier, and an entry that disappears renders them uninterpretable.

**CM-9 — Status is a property of the entry, not of the deployment.** The status field records the standing of the countermeasure itself. Whether a particular deployment is currently permissible is a separate question, answered by the admissibility algebra on the card. A countermeasure marked Active may be inadmissible on any given card; a countermeasure marked Conditional may be used where the stated condition is satisfied.

**CM-10 — The profile minimum binds.** Where an entry declares a minimum ROE profile, no card may dispatch that countermeasure below that profile. The declared minimum is a property of the countermeasure and not a value the operator may lower on a card. Where an operator believes an entry's declared minimum is wrong, the correction is made to this catalogue under change control, and the operator does not proceed on the belief.

---

## 5. Catalogue Conventions

### 5.1 Metadata fields

Every entry in §6 carries every field in the table below. A field that does not apply carries the value `Not applicable` with a one-line reason; it is not left empty. An empty field in a catalogue entry is a defect, because a reader cannot distinguish "not considered" from "considered and found not to apply".

| Field | Type | Allowed values | Meaning | Responsible for |
| --- | --- | --- | --- | --- |
| **ID** | Identifier | `OCC-01` to `OCC-43` | The permanent, citable identifier of the entry. Never reused. Never renumbered. | Catalogue owner |
| **Name** | Text | Free | The short form used in the console, on cards, and in decision records. | Catalogue owner |
| **Class** | Enumeration | CM-A, CM-B, CM-C, CM-D, CM-E, CM-F, CM-G | The countermeasure class per §4.1. | Catalogue owner |
| **Summary** | Text | Free | One sentence stating what the countermeasure does. Not a rationale, not a benefit claim. | Catalogue owner, with the submitting engineer |
| **Direction of effect** | Enumeration | Inward; Outward; Inward/outward; None | Where the intended effect falls, per §3. Determined by actual effect under `CM-1`. | Catalogue owner, verified by the legal contact for Outward entries |
| **Target** | Enumeration | Own estate; Adversary behaviour in own environment; Adversary system; Adversary infrastructure | What the countermeasure acts upon. | Catalogue owner |
| **Collateral class** | Enumeration | C0, C1, C2, C3 | The class of the countermeasure as normally deployed. A deployment at a higher class takes the class of the deployment, not of the entry. | Legal contact, on the catalogue owner's submission |
| **Reversibility** | Enumeration | Reversible; Reversed; Low; None | Whether and how completely the effect can be undone by the operator. | Catalogue owner, confirmed by the platform engineer |
| **Autonomy class** | Enumeration | AC-0, AC-1, AC-2, AC-3, AC-4 | How the countermeasure executes. | Platform engineer, confirmed by the catalogue owner |
| **Minimum ROE profile** | Enumeration | R0, R1, R2, R3, R4, R5 | The lowest profile at which the entry may be used. | Legal contact, on the catalogue owner's submission |
| **Attribution dependency** | Enumeration | None; Behavioural; Class; Identity; External | The attribution the countermeasure requires before use. See §5.2. | Analyst lead, confirmed by the catalogue owner |
| **AAT technique bindings** | List | AAT-1 to AAT-10 | The AAT categories whose techniques the countermeasure bears on. | Analyst lead, in consultation with the taxonomy owner |
| **Preconditions** | List | Free text | Conditions that must hold before dispatch. Non-satisfaction makes the countermeasure inadmissible. | Submitting engineer, confirmed by the platform engineer |
| **Procedure summary** | Text | Free | What the countermeasure actually does, in operational terms, at the level of a runbook lead. | Submitting engineer |
| **Failure modes** | List | Free text | The conditions under which the countermeasure fails or produces a different effect. | Submitting engineer, with the analyst lead |
| **Side effects** | List | Free text | Consequences outside the stated intended effect, beneficial and harmful. | Submitting engineer, confirmed by the legal contact for Outward entries |
| **Detection objective satisfied** | Text | Free | The detection objective the entry serves, expressed as a capability the operator gains. Cross-referenced to the detection coverage assessment in `operational/adversary-ai-taxonomy-and-threat-model.md`. | Analyst lead |
| **Intelligence yield** | Enumeration | None, Low, Moderate, High | The adversary-facing information expected. | Analyst lead |
| **Operator burden** | Enumeration | Low, Moderate, High, Very high | The human attention, configuration, and maintenance effort consumed. | Platform engineer, with the operator representative |
| **Degradation behaviour** | Text | Free | The designed behaviour when inputs, telemetry, or dependencies are degraded or absent. | Platform engineer |
| **Evidence produced** | List | Free text | The artefacts emitted for the audit record and for substantiation under §8. | Platform engineer |
| **Residual risk reduction** | Text | Band; basis; confidence | The expected reduction in residual risk if the countermeasure achieves its intended effect, stated as a band, with an evidence basis `E1`–`E5` and a stated confidence. See §8. | Analyst lead, verified by the catalogue owner |
| **Status** | Enumeration | Active; Conditional; Retired; Withheld | The standing of the countermeasure itself, per `CM-9`. | Catalogue owner, on the advice of the legal contact |

### 5.2 Value vocabularies

**Direction of effect.** *Inward* — the effect falls on the operator's own estate, whether by reducing exposure, adding capability, or restoring state. *Outward* — the effect falls on the adversary's own systems or infrastructure. *Inward/outward* — the effect is on the adversary's behaviour, expressed entirely through the operator's own environment; no system the operator does not control is modified. *None* — the effect is on the operator's knowledge, and neither party's capability is altered.

An entry whose direction of effect is *Outward* is a candidate for a collateral class above C0 and requires the third-party test to be recorded before it may be proposed. An entry whose direction of effect is *Inward* may still exceed C0 where it degrades a service shared with third parties; the direction of effect does not determine the collateral class, and the collateral class does not follow mechanically from the target.

**Target.** *Own estate* — acts wholly within systems the operator controls. *Adversary behaviour in own environment* — acts on what the adversary does, through the operator's environment, without modifying any system the operator does not control. *Adversary system* — acts on a system belonging to the adversary operator, including one contained within the operator's isolation boundary. *Adversary infrastructure* — acts on the hosting, transport, identity, storage, or provider infrastructure on which adversary systems depend.

**Reversibility.** *Reversible* — the effect can be fully undone by an action available to the operator within the stated window, with no residual effect on a third party and no permanent loss of a capability. *Reversed* — the effect has been withdrawn or is in the process of withdrawal, and the countermeasure's entry into the withdrawn state must itself be verified; used of this value indicates a state reached by action rather than a property of the countermeasure in its armed condition. *Low* — the effect cannot be fully undone; only partially mitigated, with the irreversible elements enumerated and argued for under `ROE-7`. *None* — the effect cannot be undone by any action available to the operator: a secret is disclosed, a capability is destroyed, a capability the adversary depended upon is permanently removed, or an artefact is irretrievably lost.

Two invariants hold throughout the catalogue. First, a countermeasure at collateral class C0 is **Reversible** or **Reversed**, because `C0` in the constitutional instrument is defined as fully reversible. Second, a countermeasure whose reversibility is **None** is at collateral class C2 or above, and where it is at C2 the irreversible elements are named in the entry.

**Autonomy floor.** An entry's declared minimum ROE profile must be at or above the lowest profile at which its declared autonomy class may be granted: AC-0 and AC-1 at R0, AC-2 at R1, AC-3 at R2, and AC-4 at R1 in read-only reconnaissance only. The floor is a property of the pair, not a matter for the operator to resolve on a card, and it is the reason several entries whose class minimum is R0 nonetheless carry a higher profile minimum. An AC-4 entry is permitted only where its collateral class is C0, its action is read-only and in scope, and a declared boundary is recorded.

**Attribution dependency.** *None* — the countermeasure's effect does not depend on knowing who the adversary is; it applies to traffic, to the estate, or to a class of request, and is equally applicable to any party. *Behavioural* — the countermeasure requires that the adversary's behaviour signature has been recognised in the specific instance, typically because it is applied to a signal that has already been distinguished from benign activity. *Class* — the countermeasure requires only that the activity has been classified as a given AAT category, and does not require identity. *Identity* — the countermeasure requires identification of the adversary's specific principal, account, or credential. *External* — the countermeasure depends on attribution supplied from outside the operator's own telemetry, such as a provider's abuse report, a peer operator's observation, or external intelligence.

The dependency sets the minimum confidence the card must carry before the countermeasure may be used, and it interacts with `INT-3` in the master design: a countermeasure with an attribution dependency of *Identity* at collateral class C2 requires an attribution confidence of at least 0.85 under `INT-3`, with the alternative attribution recorded. A countermeasure with a dependency of *None* is the route of action under attribution uncertainty, and the framework prefers it where an equivalent exists (`INT-4`, `INT-5`).

**Status.** *Active* — the countermeasure is deliverable in the platform and available for selection. *Conditional* — the countermeasure exists and is described, and its use depends on a stated condition being satisfied, such as an isolation guarantee being demonstrated, or a third party's agreement being obtained. *Retired* — the countermeasure is no longer available for use, whether because it has been superseded, because its effectiveness was disproven, or because a platform dependency has been withdrawn. *Withheld* — the countermeasure exists and is described, but its use is withheld pending a determination that has not yet been made, typically of a legal or contractual kind.

### 5.3 Residual-risk reduction format

The residual-risk reduction field is written as a band, an evidence basis, and a confidence:

> **0.20 – 0.40**; basis **E4** (design-intent estimate); confidence **Low**.

The band expresses the reduction in residual risk expected **if the countermeasure achieves its intended effect**; it does not express the probability that it achieves that effect. The two are multiplied together in the decision-support model and the model treats the combination as an estimate with its own confidence (`SCORE-4`).

No figure in §6 is an empirically derived probability. Every figure in this version is a design-intent band at basis `E4` with `Low` or `Very low` confidence. Where an entry's value lies in the intelligence it produces rather than in a reduction of risk, the band is `0.00 – 0.05` at basis `E4` and confidence `Very low`, so that the entry's non-effect on residual risk is stated rather than left as an omission. The treatment of these figures — and the prohibition on using them as the term `e` on a card without the card's own effectiveness assessment — is set out in §8.

### 5.4 Register conventions

| Convention | Rule |
| --- | --- |
| Citation | Entries are cited as `OCC-nn`, optionally with the catalogue version, as `OCC-nn @ v1.0`. |
| Versioning | The catalogue carries its own version. A card records the catalogue version in force at the time of dispatch. |
| Amendment | Amendments to an entry are recorded against the entry and do not renumber other entries. |
| Supersession | A superseded entry is marked `Retired` and is replaced by a new identifier; the old identifier is never reused. |
| Ordering | Entries appear in catalogue order. The order is presentational and carries no priority; priority is computed by `P` in the decision-support model. |
| Class membership | An entry belongs to exactly one class. Where a countermeasure has features of two classes, it is catalogued under the class matching its primary effect and the secondary effect is stated in the summary. |
| Cross-references | A reference to another entry uses its identifier and never its name alone, so that renaming an entry does not break a reference. |

---

## 6. The Catalogue

The catalogue contains forty-three entries in seven classes. Each entry is a card: what the countermeasure does, what it costs, what it requires, when it will not work, and what it produces. The entries are descriptive and enable nothing; see §1.2.

Reading conventions used below:

- **Direction of effect** and **Target** are the two fields an operator should read first, because they together answer the question the third-party test asks.
- **Residual risk reduction** is a band, not a probability of success, and carries its evidence basis and confidence inline. See §5.3 and §8.
- **AAT technique bindings** are recorded at category granularity. Technique-level bindings, with indicators and detection methods, are maintained in `reference/ai-attack-technique-library.md`.

### 6.1 CM-A — Detect

#### OCC-01 — Behavioural baseline of agent activity

| Field | Value |
| --- | --- |
| Class | CM-A Detect |
| Summary | Establishes and maintains a versioned behavioural profile of each agent workload, against which later activity is judged. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-1 (Assisted) |
| Minimum ROE profile | R0 Observe |
| Attribution dependency | None |
| AAT technique bindings | AAT-1, AAT-5, AAT-8, AAT-10 |
| Preconditions | Telemetry coverage sufficient to characterise the workload's normal behaviour; a settled observation window preceding the period of interest; a named analyst who adopts the profile. |
| Procedure summary | The platform records per-agent activity over a declared window, derives a profile of call volume and pattern, tool inventory, data reach, working pattern, and delegation shape, and presents it for analyst adoption. Subsequent deviations are scored against the adopted version, not against a fresh computation. |
| Failure modes | A window too short to characterise the workload, which encodes an atypical period as normal; a window that includes the compromise, which absorbs the adversary's activity into the baseline; a legitimate change of operating pattern, after which deviations run in both directions and the entry's output becomes noise; a workload newly deployed with no observed operating period. |
| Side effects | Adoption creates a reference against which operational exceptions are judged, so a legitimate change of behaviour may read as suspicious until the profile is re-adopted; the entry accumulates behavioural data about the operator's own workloads, which falls under the minimisation and retention rules. |
| Detection objective satisfied | Establishes the reference against which OCC-02 scores tool-call sequences and OCC-26 correlates traffic, so that anomaly detection has a defined normal to depart from. |
| Intelligence yield | Low |
| Operator burden | Moderate |
| Degradation behaviour | Where telemetry coverage falls below the stated sufficiency threshold the profile is marked degraded on the console, dependent detections inherit a reduced confidence, and the profile is not silently presented as current. |
| Evidence produced | Versioned baseline profile; the observation window and its data-sufficiency statement; the analyst adoption record with timestamp; the derivation log. |
| Residual risk reduction | 0.05 – 0.15; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-01 establishes and maintains a behavioural profile of each agent workload in the operator's estate: the volume and pattern of calls, the tools it reaches for, the data it can reach, its working pattern, and the shape of any delegation it performs. The profile is derived over a declared observation window and adopted by a named analyst, after which every deviation is scored against the adopted version. The entry is not a detector. Its purpose is to give OCC-02, OCC-26, and OCC-27 a defined, versioned, citable normal to depart from.

**When it works.** It works when the workload has a settled operating pattern, telemetry coverage is sufficient to characterise that pattern, and the observation window precedes the compromise. In those conditions it converts an open question — is this activity unusual — into a bounded one — is this activity unlike this workload's own history, with a stated version to which the answer refers.

**When it does not.** It fails when the observation window is too short, when the window includes the compromise itself and so absorbs the adversary's activity into the baseline, or when the workload's pattern legitimately changes, in which case deviations run in both directions and the output becomes noise. It is not a standalone control against an adversary that operates inside the workload's normal pattern, and it cannot distinguish an unusual request from an unusual operator.

**Cost.** C0 and reversible. The principal cost is analyst time at adoption and at each legitimate re-baselining event, which is recurrent. The behavioural data created about the operator's own workloads is minimised and retained under the platform's rules.

**Intelligence.** Yield is low, and the intelligence is about the operator's estate rather than the adversary. The entry's contribution to the intelligence loop is indirect but real: a baseline is what allows OCC-02 to distinguish an anomalous tool-call sequence from a busy afternoon.

#### OCC-02 — Tool-call sequence anomaly detection

| Field | Value |
| --- | --- |
| Class | CM-A Detect |
| Summary | Scores the order, mix, and argument shape of an agent's tool calls against the profile established by OCC-01 and raises a signal on departure. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-2 (Supervised) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | Behavioural |
| AAT technique bindings | AAT-1, AAT-4, AAT-5, AAT-8, AAT-9, AAT-10 |
| Preconditions | OCC-01 adopted for the workload in question; tool-call telemetry carrying argument-level detail; an established path for the operator to abort the scoring service. |
| Procedure summary | The service scores each tool-call sequence against the adopted profile on three axes — sequence order, tool mix, and argument shape — and raises a signal where the deviation exceeds the declared threshold, carrying the deviating sequence and the reference profile version into the triage queue. |
| Failure modes | The adversary sequences its calls in the workload's normal pattern, in which case the sequence is not deviant; a workload whose tool mix changes for legitimate reasons, producing sustained false positives; a score whose threshold has been tuned on the adversary's activity and therefore under-fits benign novelty. |
| Side effects | Sustained false positives consume analyst attention, which is the failure mode most likely to cause the signal to be dismissed later; a detection service that scores every call adds latency to the agent path and consumes storage for argument-level telemetry. |
| Detection objective satisfied | Provides the behavioural detection of agent tool abuse, which the taxonomy's coverage assessment records as stronger against AAT-4 than against AAT-1. |
| Intelligence yield | Low |
| Operator burden | Moderate |
| Degradation behaviour | Where argument-level telemetry is unavailable the service falls back to sequence and mix scoring only, and states on the signal that argument shape was not scored. It does not present a partial score as a complete one. |
| Evidence produced | Scoring record with the profile version relied upon, the three axis scores, the threshold in force, and the signal raised or not raised. |
| Residual risk reduction | 0.10 – 0.25; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-02 scores the order, the mix, and the argument shape of an agent's tool calls against the profile adopted under OCC-01, and raises a signal when the deviation exceeds a declared threshold. The signal carries the deviating sequence and the profile version it was scored against, so that the analyst can see not merely that a deviation occurred but what the workload ordinarily did instead.

**When it works.** It works against an adversary that acquires or influences an existing agent workload and then uses it in a way the workload was not designed for: an unusual tool, a new sequence, an argument shape that no legitimate workflow produces. Its strength is greatest where argument-level telemetry is complete and where the workload's legitimate pattern is stable.

**When it does not.** It fails against an adversary that operates within the normal pattern — using the ordinary tools, in the ordinary order, for an ordinary-looking purpose. It also fails where the workload's tool mix is itself the anomaly, because the reference profile has been contaminated, and where the analyst has tuned the threshold against the adversary's activity rather than against benign novelty, in which case the service is fitted to one adversary and is blind to the next.

**Cost.** C0 and reversible. The recurring cost is analyst attention consumed by false positives, which rises sharply where the workload's behaviour is genuinely variable. The service also adds latency to the agent path and storage for argument-level telemetry, both of which are budgeted in the platform's capacity plan.

**Intelligence.** Yield is low. The value of the signal is that it establishes *that* a behavioural deviation occurred, which is the input to the classification step and therefore to everything downstream; the entry does not itself characterise what the adversary wanted.

#### OCC-03 — Canary credential and honeytoken deployment

| Field | Value |
| --- | --- |
| Class | CM-A Detect |
| Summary | Places credentials and records whose presence or use is itself the signal, in locations the adversary is expected to reach. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-1 (Assisted) |
| Minimum ROE profile | R0 Observe |
| Attribution dependency | None |
| AAT technique bindings | AAT-3, AAT-4, AAT-5, AAT-6, AAT-9 |
| Preconditions | A written record of where each canary is placed and what it is for; a route by which use of the canary produces an alert; a re-issue schedule that keeps canaries from becoming a permanent burden. |
| Procedure summary | The operator places canary credentials, tokens, and records at defined locations — storage buckets, repository paths, local directories, configuration blocks, endpoint-specific secrets — each with a distinct identity, so that any use of one produces a signal identifying the path through which it was reached. |
| Failure modes | A canary placed where the adversary has no reason to go; a canary whose use is indistinguishable from legitimate use, in which case the signal is unusable; a canary that is used and not noticed because the alerting route was never tested; a canary placed in a location the adversary cannot reach even when it wants to. |
| Side effects | False positives where a legitimate process reads the canary, which is common where a canary is placed in a broadly-scanned path; canaries accumulate and must be re-issued and re-placed or they become a maintenance liability and a source of noise. |
| Detection objective satisfied | Provides path-of-compromise evidence that no other sensor in the estate can supply, because the signal is generated by the adversary's own act of taking the thing. |
| Intelligence yield | Moderate |
| Operator burden | Moderate |
| Degradation behaviour | Where the alerting route is not confirmed live, the canary is marked as an unverified sensor on the console and is not counted towards coverage. |
| Evidence produced | Placement register with timestamps and locations; alert record on use with the path information the identity encodes; re-issue history. |
| Residual risk reduction | 0.10 – 0.25; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-03 places credentials, tokens, and records in locations the adversary is expected to reach. Each canary has a distinct identity, so that when the adversary takes it, the resulting signal identifies not merely that something was accessed but the specific path through which it was accessed — which storage bucket, which repository, which directory, which configuration block. The entry is cheap, requires no adversary-facing behaviour, and produces one of the few signals in the catalogue that is generated by the adversary's own act of taking the thing.

**When it works.** It works where the adversary is credential- or access-seeking, where the canary is placed in a location the adversary has reason to prefer, and where use of the canary reaches an alert route that has been tested. It is at its strongest when the canary identity encodes a path: the alert then answers *how did it get here*, which is the question the rest of the defensive posture most needs answered.

**When it does not.** It does nothing where the adversary does not need credentials, does not enumerate, and does not take what it finds. It produces unusable signal where a canary is used in a way that cannot be distinguished from legitimate use, and it produces silent failure where the alerting route was never tested. A canary in a place the adversary never goes is not a sensor; it is litter.

**Cost.** C0 and reversible. The burden is recurrent placement, re-issue, and register maintenance, and it is the false-positive rate that matters: a canary in a broadly-scanned path will be read by legitimate processes and must be positioned so that this does not happen, or its use must be distinguishable from that use.

**Intelligence.** Yield is moderate, and out of proportion to the entry's cost. A canary alert carries path information, and path information is what turns an intrusion into a reconstruction. It is a poor source of intent and a strong source of route.

#### OCC-04 — Instrumented canary agent

| Field | Value |
| --- | --- |
| Class | CM-A Detect |
| Summary | Runs a deliberately exposed agent workload, instrumented to record in full what an adversary does with it. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-1 (Assisted) |
| Minimum ROE profile | R0 Observe |
| Attribution dependency | None |
| AAT technique bindings | AAT-1, AAT-3, AAT-4, AAT-5, AAT-7, AAT-8, AAT-10 |
| Preconditions | A real agent runtime available and instrumented; no production credential, customer data, or authoritative system reachable from it; a defined retention period for the transcripts the agent produces; an operator ready to read the transcript as it accumulates. |
| Procedure summary | The operator deploys an agent workload that presents a plausible surface to an adversary, is instrumented at the prompt, tool, and egress layers, and records everything it is asked to do, including the instructions it receives and the actions it takes in response. |
| Failure modes | A canary agent that is obviously a canary, which is never approached; a canary that reaches a production credential and becomes the compromise rather than the witness; an instrumented agent whose instrumentation is itself discoverable and is stripped or bypassed; a canary nobody reads, so the transcript accumulates unexamined. |
| Side effects | The agent's own activity generates telemetry and cost that are attributable to the operator; if the canary reaches shared infrastructure, its traffic is visible to third parties as unusual and may itself be actioned. |
| Detection objective satisfied | Supplies the adversarial-behaviour signal for detection coverage against AAT-1 and AAT-8, where the taxonomy records coverage as weaker. |
| Intelligence yield | High |
| Operator burden | High |
| Degradation behaviour | Where an instrument layer fails the agent is marked as partially instrumented, the affected class of action is excluded from the transcript, and the gap is shown on the console as an unobserved surface. |
| Evidence produced | Complete transcript of instructions received and actions taken; instrumentation coverage statement; the deployment's scope and expiry. |
| Residual risk reduction | 0.05 – 0.10; basis E4 (design-intent estimate); confidence Very low. |
| Status | Active |

**What it does.** OCC-04 deploys an agent workload that presents a plausible surface and is instrumented at the prompt, tool, and egress layers, so that everything the adversary asks of it is recorded. Unlike the deception entries, this agent is not trying to mislead: it is trying to be useful enough to be approached and complete enough to be read. It is the catalogue's most direct route to seeing adversary planning behaviour, and it is the entry that fills the coverage gap the taxonomy records against autonomous planning.

**When it works.** It works when the canary's surface is plausible enough to be worth approaching, when it is genuinely reachable, and when the operator reads the transcript promptly. The instrumented transcript of an agent that has been asked to do something illegitimate is close to the richest single artefact the system produces: it shows the instruction, the reasoning visible in the trace, the tools selected, and the egress attempted.

**When it does not.** It fails when the canary presents as a canary, when it is not reachable, and when the instrumentation is discoverable and can be stripped. It fails catastrophically if the canary is given reach to a production credential, at which point the witness becomes the breach. And it produces nothing at all if the transcript is not read, which is the commonest failure and the reason the entry's operator burden is high.

**Cost.** C0 and reversible, but the burden is high: a standing deployment, recurring instrumentation maintenance, transcript review, and the risk that an instrumented runtime is itself a liability. The canary's traffic must not reach shared infrastructure, where its odd profile is visible to a third party.

**Intelligence.** Yield is high. This is the entry that closes the AAT-1 and AAT-8 detection gap, and the entry from which hypotheses about the adversary's goals, patience, and escalation triggers are most often drawn. The intelligence is per-adversary and expires quickly.

#### OCC-05 — Prompt-injection detection and sanitisation at ingest

| Field | Value |
| --- | --- |
| Class | CM-A Detect |
| Summary | Inspects untrusted content entering an agent's context and removes or neutralises instruction-like material before the model can act on it. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-2 (Supervised) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | None |
| AAT technique bindings | AAT-2, AAT-7, AAT-10 |
| Preconditions | A defined trust boundary at which content crosses from untrusted to trusted; a classification of the content types that cross it; a stated policy for what happens to content that cannot be made safe. |
| Procedure summary | The ingest path classifies each item of untrusted content — retrieved documents, tool output, inbound messages, scanned text — for instruction-like content directed at the model, and either neutralises the instruction, quarantines the item, or refuses it, according to the declared policy. |
| Failure modes | Content that carries an instruction in a form the classifier does not recognise, which is the general case for a sufficiently motivated adversary; content that is legitimately operational and is stripped of a necessary instruction, breaking the workflow; a classifier tuned on one injection style and blind to paraphrase; a downstream component that treats sanitised content as fully trusted. |
| Side effects | Over-sanitisation damages legitimate workflows, and the damage is usually noticed as a functional fault rather than as a security event; sanitisation is a point in the path and so a latency and cost burden on every ingest. |
| Detection objective satisfied | Provides the control for AAT-2 direct and indirect prompt injection, and the detection of the attempt itself, which the taxonomy separates from the detection of the effect. |
| Intelligence yield | Low |
| Operator burden | High |
| Degradation behaviour | Where the classifier is unavailable the declared policy decides: fail closed for high-consequence paths, fail open with a recorded warning elsewhere. The entry states which mode is in force for each path on the console. |
| Evidence produced | Per-item classification with the reason; neutralisation record; the quarantine reference where one is raised; the fail-mode declaration in force. |
| Residual risk reduction | 0.15 – 0.35; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-05 inspects content as it crosses into an agent's context — retrieved documents, tool output, inbound messages, extracted text — and removes or neutralises instruction-like material before the model has any opportunity to act on it. It is the control that stands between an adversary's written instruction and an agent's obedience. It is also a detector in its own right, because a rejected item is evidence that an injection was attempted.

**When it works.** It works against injection in forms the classifier recognises, which covers a substantial part of naive and templated attacks and a smaller part of deliberate ones. It works best where the trust boundary is narrow and explicit, so that the classifier is applied to the small set of paths where untrusted content actually enters.

**When it does not.** It fails against an adversary who writes the instruction in a form the classifier does not recognise, which is the normal expectation for a deliberate and adaptive attacker and the reason this entry is not the answer to AAT-2 on its own. It also fails in the opposite direction, where legitimate operational content is stripped of a necessary instruction and the workflow breaks. A downstream component that treats sanitised content as fully trusted defeats the control without any visible symptom.

**Cost.** C0 and reversible. The burden is high and is felt on every ingest, in latency, in classifier maintenance, and in the operational cost of broken workflows. The cost of a false negative is an agent that has obeyed an adversary; the cost of a false positive is a workflow that has stopped working. The trade is asymmetric and the entry is deployed accordingly.

**Intelligence.** Yield is low in volume and high in quality per item: each neutralised item is a directly observed injection attempt, with the payload itself as the artefact. Over time the set of rejected items characterises the adversary's injection style, which is the input to OCC-30.

#### OCC-06 — Model artefact and weight attestation monitoring

| Field | Value |
| --- | --- |
| Class | CM-A Detect |
| Summary | Monitors the model artefacts the estate loads and runs, and raises a signal when an artefact differs from the attested one. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-2 (Supervised) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | None |
| AAT technique bindings | AAT-5, AAT-7 |
| Preconditions | An attested reference for each artefact the estate is entitled to run, held somewhere the adversary cannot modify; a digest or equivalent that is cheap enough to compute on every load; a documented process for adding a new artefact to the attested set. |
| Procedure summary | On load and on a schedule, the platform computes the artefact's digest and compares it against the attested reference, and raises a signal on any difference, including differences introduced by an adapter, a fine-tune, a quantisation, or a configuration overlay. |
| Failure modes | An adversary who modifies the artefact and the attested reference together, or who modifies the reference store; a supply-chain substitution that is attested at ingestion and therefore never triggers the monitor; a monitor whose reference set drifts, so that legitimate updates are re-attested reflexively and the signal loses meaning; a signature scheme the adversary can reproduce. |
| Side effects | Re-attestation after every legitimate update is a recurring burden on the team that ships models, and pressure to re-attest quickly is pressure to re-attest uncritically. |
| Detection objective satisfied | Detects the model-layer category of supply-chain compromise, AAT-7, at the point of artefact load, which no behavioural detector reaches. |
| Intelligence yield | Low |
| Operator burden | Moderate |
| Degradation behaviour | Where the reference store is unreachable the monitor marks artefacts unattested and the console shows the affected workloads as running without attestation, rather than passing them silently. |
| Evidence produced | Digest comparison record per load, reference-store integrity state, the attestation history per artefact, and the re-attestation record with the approver named. |
| Residual risk reduction | 0.10 – 0.25; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-06 watches the model artefacts the estate loads and runs. Each artefact carries a digest against an attested reference held outside the adversary's reach, and the monitor raises a signal whenever the two differ — including the cases where the difference is an adapter, a fine-tune, a quantisation, or a configuration overlay applied on top of an attested base. It covers the part of the supply chain that no behavioural detector reaches, because a compromised artefact that behaves well is not detectable by behaviour.

**When it works.** It works where the reference store is genuinely outside the adversary's reach, where digests are computed on every load rather than only at installation, and where the attested set is small and current. It is most valuable against an adversary who knows they must alter the artefact to change the model's behaviour.

**When it does not.** It fails when the adversary reaches both the artefact and the attested reference, or where the reference store is itself compromised. It does not see a substitution that is attested at ingestion. It degrades in significance when the attested set drifts: a monitor whose references are re-issued every week without scrutiny raises signals nobody reads, and the next genuine signal is dismissed with them.

**Cost.** C0 and reversible. The burden is the recurring re-attestation exercise, which lands on whichever team ships models, and which creates a mild but real incentive to re-attest quickly and without scrutiny. The monitor's own storage for references is small; its value depends entirely on the reference store's integrity.

**Intelligence.** Yield is low. The entry's principal contribution is the distinction between a model that is behaving oddly and a model that is not the model the estate believes it is running, which is a question that behaviour alone cannot answer.

#### OCC-07 — Retrieval corpus integrity monitoring

| Field | Value |
| --- | --- |
| Class | CM-A Detect |
| Summary | Monitors the documents and records an agent's retrieval depends on, and raises a signal when the corpus changes in a way it should not. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-2 (Supervised) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | None |
| AAT technique bindings | AAT-2, AAT-5, AAT-7 |
| Preconditions | An authoritative statement of what the corpus should contain, obtainable before the change rather than after it; an authoritative source of change events for the corpus; retention of enough prior corpus state to compare against. |
| Procedure summary | The monitor tracks the documents, chunks, and embeddings the retrieval layer serves, records their provenance, and raises a signal on additions, modifications, deletions, or embedding changes that are not attributable to an authorised change event. |
| Failure modes | A corpus with no authoritative expected state, in which case every change is unexplained and every change is eventually accepted; an adversary who modifies the corpus and the change log together; a monitor that detects the change but cannot distinguish a poisoned document from a legitimate one, so the analyst must read the document; embedding-level manipulation that preserves the text and therefore passes a digest check. |
| Side effects | The corpus's legitimate churn produces a high baseline rate of unexplained change, and an entry that alerts on every change trains the analyst to dismiss it. The monitoring itself requires retaining prior corpus state, which is a storage and data-protection cost. |
| Detection objective satisfied | Detects corpus-level supply-chain compromise and retrieval poisoning, AAT-7, and the vector by which AAT-2 indirect injection reaches the agent. |
| Intelligence yield | Low |
| Operator burden | High |
| Degradation behaviour | Where the change-event feed is incomplete the monitor marks the corpus partially monitored and identifies which stores lack change attribution, so the coverage gap is visible rather than assumed away. |
| Evidence produced | Corpus change record with provenance attribution, the unexplained-change list, the comparison against retained prior state, and the coverage statement per store. |
| Residual risk reduction | 0.10 – 0.20; basis E4 (design-intent estimate); confidence Low. |
| Status | Conditional |

**What it does.** OCC-07 watches the corpus that the estate's retrieval depends on: the documents, the chunks, the embeddings, and the provenance links between them. It records what changed and whether the change is attributable to an authorised change event, and it raises a signal on the changes that are not. A poisoned document is otherwise indistinguishable from a good one at retrieval time — the damage is already done by the time the agent reads it — so the only place to notice is here.

**When it works.** It works where the corpus has an authoritative expected state and a reliable change-event feed, so that the great majority of changes are explained without effort, and the unexplained remainder is therefore meaningful. It is also the entry that surfaces the *shape* of a poisoning operation, because a poisoned corpus arrives in bulk or in a patterned way.

**When it does not.** It fails when there is no authoritative expected state, which is common in an estate whose corpus is assembled by continuous ingestion from many sources; the entry then alerts on everything and is therefore useful for nothing. It fails when the adversary reaches both the corpus and the change log. It does not catch embedding-level manipulation that leaves the text intact, unless embedding provenance is also tracked.

**Cost.** C0 and reversible. The burden is high, principally because the entry depends on the corpus's own change governance rather than only on the platform. Retaining prior corpus state for comparison is a real storage and data-protection cost, and the false-alert rate is sensitive to the corpus's churn rate.

**Intelligence.** Yield is low, but the entry contributes a specific and important thing: it shows *when* a retrieval answer became wrong, which is the difference between a compromised agent and a compromised corpus. Where the corpus is the cause, that determination redirects the whole response.

**Status note.** The entry is marked Conditional because its effectiveness depends on an organisational precondition — a corpus with authoritative expected state — that is a property of the estate's document governance and not of the platform.

---

### 6.2 CM-B — Harden

#### OCC-08 — Instruction-hierarchy enforcement with provenance tagging

| Field | Value |
| --- | --- |
| Class | CM-B Harden |
| Summary | Enforces that instructions arriving with content cannot outrank the operator's own directives, and tags the provenance of every instruction the model acts upon. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-2 (Supervised) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | None |
| AAT technique bindings | AAT-1, AAT-2, AAT-7, AAT-8, AAT-9, AAT-10 |
| Preconditions | An explicit statement of the operator's instruction hierarchy, including what constitutes an authorised directive; a content channel structure that keeps provenance attached to each instruction; a decision, recorded, on what happens to content whose provenance cannot be established. |
| Procedure summary | Every instruction presented to a model is tagged with its provenance — operator, system policy, retrieved document, tool output, inbound message — and the model is required to treat instructions arriving with content as data, not as directives, and to record which provenance the acting instruction carried. |
| Failure modes | A hierarchy that is declared but not enforced, so the tags exist and nothing acts on them; instructions delivered through a channel that has no provenance, which the adversary seeks; a hierarchy too rigid for legitimate work, which operators route around; a provenance tag that is accurate about origin and wrong about authority. |
| Side effects | Strict hierarchy breaks legitimate workflows in which a document contains an instruction the operator wants followed; the routing around that breakage is itself a risk and is worth watching for. |
| Detection objective satisfied | Provides the durable control against instruction-hierarchy violation, AAT-2, at the point where the model is deciding what to obey. |
| Intelligence yield | Low |
| Operator burden | Moderate |
| Degradation behaviour | Where provenance is missing the instruction is treated as untrusted data by default, and the volume of such instructions is itself surfaced as a signal. |
| Evidence produced | Provenance tag on each acted-upon instruction; the hierarchy declaration in force; the record of instructions whose provenance was unestablished. |
| Residual risk reduction | 0.15 – 0.35; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-08 gives the operator's own directives a status that content cannot claim. Every instruction presented to a model carries a provenance tag, and instructions that arrive attached to retrieved content, tool output, or inbound messages are treated as data rather than as directives. The provenance of the instruction the model actually acted upon is recorded, which means the record shows not merely what was done but on whose authority it was understood to be done.

**When it works.** It works where the hierarchy is genuinely enforced by the runtime rather than described in a prompt, and where the content channels that adversaries favour are known and closed. The recorded provenance is what makes an incident reconstructible: it distinguishes an operator's mistaken instruction from a successful manipulation.

**When it does not.** It fails when the hierarchy is declared and not enforced, which is the commonest way a control of this kind degrades — the tags are present and nothing acts upon them. It fails against an adversary who finds a channel with no provenance attached. And it fails in the operational sense, where a hierarchy strict enough to be safe is strict enough to break work, and the workaround becomes the real risk.

**Cost.** C0 and reversible. The burden is the work of keeping the hierarchy declaration true and of repairing the workflows that a correct enforcement breaks. Where the enforcement causes operational failures, the pressure to relax it is the mechanism by which the control decays.

**Intelligence.** Yield is low. Its contribution is to the record rather than to the adversary's picture: provenance-tagged instructions are what allow an after-action review to distinguish a mistake from a manipulation.

#### OCC-09 — Output sanitisation and egress allow-listing

| Field | Value |
| --- | --- |
| Class | CM-B Harden |
| Summary | Constrains what an agent may emit and where, by sanitising output and permitting egress only to declared destinations. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-2 (Supervised) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | None |
| AAT technique bindings | AAT-2, AAT-3, AAT-8, AAT-9, AAT-10 |
| Preconditions | An enumerated set of permitted egress destinations per agent workload, held in the estate's control and not writable by the workload itself; a sanitisation policy for the output classes that matter, including secrets and personal data; a decision on the behaviour when a destination is not permitted. |
| Procedure summary | Output is inspected and redacted for secret material, personal data, and dangerous content before release, and the destination is checked against the workload's allow-list; traffic to a destination not on the list is refused and the refusal is recorded as an attempt. |
| Failure modes | A destination that was permitted for a legitimate purpose and is exactly the one the adversary wants, which is the commonest exfiltration route; an allow-list that the agent workload can modify, so the adversary edits it first; a channel not treated as egress at all — DNS, a covert protocol, an issue tracker, a mail relay — which passes every destination check; sanitisation that removes secrets from output but not from the agent's context, where the adversary simply asks for them again. |
| Side effects | Allow-lists break legitimate integrations when a dependency changes, and the pressure to widen a list is the mechanism by which the control decays; sanitisation introduces latency on every emission and can damage content that resembles a secret. |
| Detection objective satisfied | Provides the preventive control against AAT-9 exfiltration and covert channels, and detects the attempt through the record of refused destinations. |
| Intelligence yield | Low |
| Operator burden | High |
| Degradation behaviour | Where the destination state is unavailable the egress path is closed by default for the workload, and the closure is shown on the console as a degraded route rather than as a healthy one. |
| Evidence produced | Allow-list version per workload; sanitisation decisions with the reason; the register of refused destinations and the requesting workload. |
| Residual risk reduction | 0.20 – 0.40; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-09 constrains both ends of an agent's conversation. Output is inspected and redacted before it leaves, for secret material, personal data, and content that could carry an instruction or an executable payload. Egress is permitted only to destinations enumerated for that workload, in a list the workload itself cannot write. Traffic to an unlisted destination is refused, and the refusal is recorded as an attempt rather than as a routing error, because the attempt is the signal.

**When it works.** It works where the allow-list is genuinely narrow and genuinely current, and where every path out of the agent — including the administrative ones — passes through the same enforcement point. It is the entry most likely to catch an exfiltration attempt that the adversary believed was ordinary traffic.

**When it does not.** It fails against exfiltration over a channel the estate does not classify as egress, and against exfiltration to a destination that is legitimately permitted, which is the commonest case of all: an adversary that can use the API the workload was built to use needs no allow-list bypass. It also fails where the workload can modify its own list, in which case the adversary edits the list before it sends anything.

**Cost.** C0 and reversible, but the burden is high. Every legitimate dependency change requires a list change, and every list change is an opportunity to widen the control. The decay mechanism is predictable and should be watched: count the list growth over time.

**Intelligence.** Yield is low. The refused-destination register is the useful artefact, since it identifies what the adversary tried to reach and, in the clearest cases, what it was reaching for.

#### OCC-10 — Tool capability scoping and least privilege

| Field | Value |
| --- | --- |
| Class | CM-B Harden |
| Summary | Restricts each agent workload to the minimum set of tools and parameters it needs, and re-authorises rather than inherits. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-1 (Assisted) |
| Minimum ROE profile | R0 Observe |
| Attribution dependency | None |
| AAT technique bindings | AAT-2, AAT-7, AAT-8 |
| Preconditions | A tool inventory with a declared owner for each tool; a stated justification for each capability granted to each workload; a mechanism by which a grant expires and must be re-justified rather than renewed by default. |
| Procedure summary | Each workload receives an explicit set of tool capabilities with bounded parameters and scope, authored by the tool's owner rather than inherited from a broad default, and the grant carries an expiry after which the workload holds nothing until the grant is re-issued. |
| Failure modes | A capability granted once and never revisited, so that the grant list grows into a de facto administrator; a tool whose own authorisation is broader than the workload's need, which nullifies the scoping; a workload that is scoped at creation and then given a new task that it satisfies by borrowing another workload's grant; a scoping mechanism the workload can influence through its own configuration. |
| Side effects | Scoping that is too tight makes the workload fail in ways that look like model error, and the pressure to widen is constant; an expiring grant creates a recurring administrative task, and a missed expiry is either a broken workload or a quiet extension. |
| Detection objective satisfied | Removes the capability that several AAT-2 and AAT-8 techniques require, so that the technique fails on its own rather than being detected after the fact. |
| Intelligence yield | None |
| Operator burden | High |
| Degradation behaviour | Where the capability registry is unavailable the workload runs with the last known grant and the console marks it as running on a stale grant. |
| Evidence produced | Grant register with the justifying owner, the scope, the expiry, and the grant history per workload; the list of expired and unrenewed grants. |
| Residual risk reduction | 0.25 – 0.45; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-10 gives each agent workload an explicit, bounded set of tools and parameters, authored by the owner of each tool, with an expiry after which the workload holds nothing until the grant is renewed with a fresh justification. The design point is that the grant is not inherited from a broad default and is not renewed by silence. A tool's own authorisation may be wide; the workload's grant of it is narrow.

**When it works.** It works where the tool owners are real and the grant register is real, so that the scope of a workload reflects what its task requires and nothing else. It works best against the adversary who plans to use a capability the workload was never given, because the capability simply is not there.

**When it does not.** It fails where a tool's own authorisation is broader than any workload's need, since the scoping then bounds only which workload calls it and not what it can do. It fails where grants accumulate without review, which is the normal outcome of a register nobody owns. And it fails where the scoping is applied at workload creation and never revisited, which is the point at which the adversary's objective becomes available.

**Cost.** C0 and reversible. The burden is high and is administrative: a grant to issue, a justification to write, an expiry to track, and a workload to break when the grant lapses. The countervailing pressure is constant and predictable, and the register's growth is the metric that shows the control decaying.

**Intelligence.** Yield is none. The entry's value is entirely in the reduction of what the adversary can do.

#### OCC-11 — Delegation depth and scope limits

| Field | Value |
| --- | --- |
| Class | CM-B Harden |
| Summary | Bounds how far an agent may delegate, and what a delegate may be told or asked to do. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-1 (Assisted) |
| Minimum ROE profile | R0 Observe |
| Attribution dependency | None |
| AAT technique bindings | AAT-1, AAT-8, AAT-10 |
| Preconditions | A declared maximum depth for each task class; a rule that the scope of a delegate may not exceed the scope of the delegator; a mechanism that refuses a delegation exceeding the bound rather than truncating it silently. |
| Procedure summary | The runtime counts the delegation chain, refuses a call whose chain depth or cumulative scope exceeds the declared bound, and passes down only the scope the delegator itself holds, so that a delegate can never be asked for more than its principal was given. |
| Failure modes | A bound set high enough that it never binds; a delegate whose scope is expressed in the delegate's own terms rather than the delegator's, so that cumulative scope grows with each hop; a refusal that the calling agent works around by re-framing the request as an ordinary tool call; a chain depth measured per branch rather than across the whole chain, so that breadth substitutes for depth. |
| Side effects | A bound that binds too tightly breaks legitimate multi-step work, and the resulting failures are usually attributed to model quality rather than to the bound, which delays the correction. |
| Detection objective satisfied | Removes the recursive delegation capability that AAT-1 and AAT-8 techniques depend on, so that task decomposition and delegation-chain abuse fail on their own. |
| Intelligence yield | None |
| Operator burden | Moderate |
| Degradation behaviour | Where the chain counter is unreliable the runtime refuses delegation outright for the affected workload, and the refusals are counted and shown. |
| Evidence produced | Delegation ledger with depth and scope at each hop; the bound in force; the register of refused delegations with the refusing reason. |
| Residual risk reduction | 0.15 – 0.30; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-11 bounds two properties of delegation: how many hops an agent chain may make, and what scope any one delegate may hold. The scope rule is the important half. A delegate never receives more authority than its delegator held, so authority cannot grow with distance from the principal — which is precisely the mechanism by which a delegation chain turns a narrow grant into a broad one.

**When it works.** It works when the bounds are set per task class rather than globally, so that a workflow that genuinely needs depth is not blocked while an incidental agent is not permitted to recurse. It is a direct control on the AAT-8 delegation-chain abuse technique, and it removes that technique's capability rather than detecting its use.

**When it does not.** It fails when the bound is set at a level that never binds in practice, which is the default failure and is detectable only by measuring how close the estate runs to its own limit. It fails when the scope of a delegate is expressed in the delegate's vocabulary rather than the delegator's, allowing cumulative scope to grow hop by hop. And it fails where a refusal can be re-expressed as an ordinary tool call, which many adversaries attempt as a matter of course.

**Cost.** C0 and reversible. The burden is moderate: the bounds must be set per task class, which requires knowing the workloads, and revised when the workloads change. Breaks caused by a bound that is too tight are usually misdiagnosed, which is the hidden cost.

**Intelligence.** Yield is none. The entry's contribution is capability removal.

#### OCC-12 — Credential isolation and short-lived tokens for agents

| Field | Value |
| --- | --- |
| Class | CM-B Harden |
| Summary | Gives agent workloads short-lived, narrowly scoped credentials rather than durable secrets, and keeps them separate from human credentials. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-1 (Assisted) |
| Minimum ROE profile | R0 Observe |
| Attribution dependency | None |
| AAT technique bindings | AAT-4, AAT-5, AAT-8 |
| Preconditions | An issuer able to mint scoped, expiring credentials on a workload's behalf; a policy on maximum lifetime and maximum scope per credential class; the workloads migrated off durable secrets, including the ones in prompts, config, and logs. |
| Procedure summary | A workload authenticates through an issuance service that mints a credential bound to a declared scope and a short lifetime, refreshes it as needed, and drops it at the end of the session, so that a captured credential has a short window of use and a narrow reach. |
| Failure modes | A credential with too long a lifetime, so that capture is nearly as good as persistence; a refresh path that mints a longer-lived credential; a secret left in a prompt, a log, or a configuration file that the short-lived scheme was meant to replace; a workload that needs a broad scope for one legitimate task and therefore holds a broad scope for all of them. |
| Side effects | Short-lived credentials complicate debugging, because a failure may be a lapsed credential rather than a fault, and this is a recurring source of operational friction. Migration off durable secrets is a project, not a configuration change. |
| Detection objective satisfied | Limits the value of a captured credential, which reduces the effect of AAT-4 credential harvesting and of credential reuse through AAT-8 delegation. |
| Intelligence yield | None |
| Operator burden | High |
| Degradation behaviour | Where the issuer is unavailable the workload holds nothing and fails closed; the console shows the affected workloads as unauthenticated rather than as healthy. |
| Evidence produced | Credential issuance log with scope, lifetime, and requesting workload; the register of workloads still holding durable secrets; the revocation history. |
| Residual risk reduction | 0.20 – 0.35; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-12 replaces the durable secrets in agent workloads with short-lived, narrowly scoped credentials minted on the workload's behalf. The credential the adversary steals is bounded in lifetime and in reach, so capture is a much smaller event than persistence. The entry is a direct answer to the fact that a token found in an agent's context is, in most designs, a key to everything that agent can reach.

**When it works.** It works where the lifetime is genuinely short relative to the adversary's task cycle, where the scope is per-workload and narrow, and where the durable secret has actually been removed rather than supplemented. It is most valuable against an adversary that harvests credentials and returns to them later.

**When it does not.** It fails when the lifetime is long enough for the adversary to use the credential before it expires, when the refresh path issues something broader, and — most commonly — when the durable secret it was meant to replace is still present in a prompt, a log, or a configuration file. It does nothing for an adversary that does not need credentials.

**Cost.** C0 and reversible, with high burden. The friction is real: short-lived credentials make intermittent failures harder to diagnose, and the migration is a project with its own risk of leaving a duplicate secret behind. The register of workloads still holding durable secrets is the honest measure of progress.

**Intelligence.** Yield is none. The entry reduces what a successful compromise is worth.

#### OCC-13 — Segregation of agent identity from human identity

| Field | Value |
| --- | --- |
| Class | CM-B Harden |
| Summary | Ensures that every agent acts under an identity of its own, so that its actions are attributable to it and cannot borrow a human's authority. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-1 (Assisted) |
| Minimum ROE profile | R0 Observe |
| Attribution dependency | None |
| AAT technique bindings | AAT-1, AAT-3, AAT-4, AAT-6, AAT-8 |
| Preconditions | An identity service that can mint non-human identities with their own permissions, audit, and lifecycle; an access review model that treats an agent identity as a first-class principal; a prohibition on agent workload execution under a human session. |
| Procedure summary | Each agent workload authenticates as a distinct principal, with its own permission set, audit trail, and revocation path, and the runtime refuses to execute a workload inside a human's authenticated session so that no action is attributable to a person who did not take it. |
| Failure modes | An agent identity that inherits the human's permissions by convenience, which reproduces the original problem under a new name; an identity whose permissions drift upward over time as tasks accumulate; a shared service identity used by many workloads, which makes attribution within the estate impossible; a runtime that permits workload execution inside a human session when a human asks it to. |
| Side effects | More principals means more access review, more licence cost, and more onboarding work; service identities that are poorly named make the audit trail harder to read than it needs to be. |
| Detection objective satisfied | Provides the attribution capability that makes AAT-4 and AAT-8 activity distinguishable from human activity in the estate's own records, and underpins OCC-01's per-agent profiling. |
| Intelligence yield | Low |
| Operator burden | High |
| Degradation behaviour | Where the identity service is unavailable, workloads that require an identity do not run; the console lists them as blocked rather than as running. |
| Evidence produced | Principal register with per-agent identity, permission set, and lifecycle state; the record of workload execution refused for lack of a distinct identity. |
| Residual risk reduction | 0.15 – 0.30; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-13 gives every agent workload a distinct, non-human identity with its own permissions, audit trail, and revocation path, and it refuses to run a workload inside a human's authenticated session. Two things follow. An agent's actions are attributable to the agent, which is the precondition for everything the catalogue does with behavioural evidence. And no agent can exercise a human's authority, which closes the most common route by which a model that has been talked into something obtains the means to do it.

**When it works.** It works where agent identities are treated as first-class principals in the access review, and where the permission set of an agent is authored for the agent rather than inherited from whoever operates it. It is the entry that makes OCC-01's per-agent profiling meaningful, because without separable identity there is no agent to profile.

**When it does not.** It fails where the agent identity inherits the human's permissions for convenience, which is the same defect under a different name. It fails where permissions drift upward as tasks accumulate. It fails where many workloads share one service identity, because then nothing in the estate can be attributed to a particular agent.

**Cost.** C0 and reversible, with high burden. More principals means more access review, more onboarding, and more to keep tidy. The failure that matters is institutional rather than technical: identities that are issued once and never reviewed.

**Intelligence.** Yield is low, but its contribution is structural: separable identity is what allows behavioural attribution of activity to an adversary using the operator's own machinery, which is the hardest attribution problem in the defensive posture.

#### OCC-14 — Adversarial input rate limiting and anomaly gates

| Field | Value |
| --- | --- |
| Class | CM-B Harden |
| Summary | Limits the rate and shape of untrusted input an agent will accept, and gates it where the pattern departs from what the workload can process. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-2 (Supervised) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | None |
| AAT technique bindings | AAT-1, AAT-2, AAT-3, AAT-4, AAT-6, AAT-8 |
| Preconditions | A per-workload statement of the legitimate input rate the workload is designed for; a decision on the behaviour when the limit is exceeded, including whether the excess is queued, dropped, or refused; a mechanism that the adversary cannot read to discover the limit. |
| Procedure summary | The ingress path meters untrusted input per workload against a declared legitimate rate, and where the pattern departs from the declared shape it engages an anomaly gate that either defers, samples, or refuses the excess, and records the event. |
| Failure modes | A limit set above the adversary's rate, which is common when the limit is set from the workload's average rather than its maximum; a limit that degrades under load, so that the adversary achieves its effect during the estate's busiest period; a gate that becomes visible, so that the adversary paces itself below it and the entry silently ceases to constrain anything; a queue that grows without bound and turns the gate into a delay mechanism. |
| Side effects | A limit set below the legitimate peak degrades service at exactly the moments the estate is busiest; a visible gate teaches the adversary the boundary. |
| Detection objective satisfied | Constrains the AAT-6 automation-scaling technique and the AAT-3 adaptive-rapport technique, and gives the operator a rate anomaly as a class signal. |
| Intelligence yield | Low |
| Operator burden | Moderate |
| Degradation behaviour | Where the metering path is unavailable the gate closes to the declared conservative limit rather than opening, and the console states that the gate is in degraded mode. |
| Evidence produced | Rate record per workload; gate engagement log with the pattern that triggered it; the declared legitimate rate and the version in force. |
| Residual risk reduction | 0.10 – 0.25; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-14 meters untrusted input against what each workload was designed to accept, and engages a gate where the pattern departs from the declared shape — deferring, sampling, or refusing the excess, and recording the event. It is the countermeasure that makes an adversary's ability to scale its activity finite, without needing to know that the activity is an attack.

**When it works.** It works when the legitimate rate is known, which means the workload has been observed rather than assumed, and when the gate is invisible enough not to be paced against. It is particularly effective against an adversary whose technique depends on volume, because the entry denies the volume without denying the operation and without producing a signal the adversary can read.

**When it does not.** It fails where the limit is set from the workload's average and therefore sits above the adversary's threshold. It fails during estate load, when the control degrades first and the adversary's campaign persists. And it fails once the adversary learns the boundary and paces below it, at which point the entry constrains nothing and still appears healthy.

**Cost.** C0 and reversible. The burden is moderate and includes the work of determining the legitimate peak, which is harder than it sounds for a workload with seasonal behaviour. The service cost of the gate falls on the workloads that are legitimate and busy.

**Intelligence.** Yield is low. The gate engagement log shows the *shape* of the excess, which is characteristic of the technique and is more useful than the mere fact that a limit was reached.

#### OCC-15 — Model rollback and checkpoint integrity

| Field | Value |
| --- | --- |
| Class | CM-B Harden |
| Summary | Keeps integrity-verified checkpoints of models and agents, and provides a verified route back to a last-known-good state. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-2 (Supervised) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | None |
| AAT technique bindings | AAT-5, AAT-7 |
| Preconditions | A checkpoint store outside the reach of the workload being checkpointed; integrity verification applied to every checkpoint at rest and on restore; a stated retention and test frequency; a restore procedure that has been exercised. |
| Procedure summary | The platform periodically captures a checkpoint of a model or agent workload with its configuration and permissions, verifies its integrity against a reference held outside the workload's reach, and retains it under a declared schedule; a restore is available to OCC-23 and to the platform's own recovery runbook. |
| Failure modes | A checkpoint store inside the compromise boundary, in which case the checkpoints are as compromised as the workload; a checkpoint captured after the compromise, which restores the compromise; a restore procedure never exercised, so that the restore fails at the moment it is needed; integrity verified only on write and not on restore. |
| Side effects | Checkpoint storage is a recurring cost, and the retention schedule multiplies it; a restore overwrites live state, which makes the pre-restore capture in OCC-42 a precondition rather than a nicety. |
| Detection objective satisfied | Provides the recovery capability that makes OCC-23 and OCC-41 deliverable, and provides the AAT-7 and AAT-5 containment capability that no behavioural detector supplies. |
| Intelligence yield | None |
| Operator burden | Moderate |
| Degradation behaviour | Where a checkpoint cannot be verified the entry marks it unusable rather than offering it as a restore point, and the console shows the coverage of verified checkpoints against the estate's workloads. |
| Evidence produced | Checkpoint register with capture time, workload, integrity verdict, and retention expiry; the restore event log; the test-restore record. |
| Residual risk reduction | 0.10 – 0.20; basis E4 (design-intent estimate); confidence Low. |
| Status | Conditional |

**What it does.** OCC-15 maintains integrity-verified checkpoints of the estate's model and agent workloads, together with their configuration and permissions, held outside the reach of the workload being checkpointed, and it makes a verified route back to a last-known-good state available. The entry is the reason OCC-23 is possible at all, and it is the difference between a compromised agent being an incident and being a delay.

**When it works.** It works where the checkpoint store is genuinely outside the compromise boundary, where integrity is verified on restore as well as on write, and where the restore procedure is exercised on a schedule rather than merely documented. A verified checkpoint taken before the compromise is the single most valuable artefact the defensive posture produces.

**When it does not.** It fails where the checkpoint store is inside the boundary the compromise reached, where the checkpoint was captured after the compromise and therefore encodes it, and where the restore procedure has been written but never run. The last of these is the commonest and is invisible until the day it matters.

**Cost.** C0 and reversible. The burden is storage, the retention schedule, the periodic test restore, and the discipline of keeping the store outside the boundary — which is the requirement most often quietly relaxed for convenience.

**Intelligence.** Yield is none, except where the difference between a checkpoint and its artefact is itself informative about what changed.

**Status note.** The entry is marked Conditional because its effectiveness depends on a store-location precondition that is a property of the estate's architecture and not of the platform.

#### OCC-16 — Sandboxed agent execution

| Field | Value |
| --- | --- |
| Class | CM-B Harden |
| Summary | Runs agent workloads in an isolated execution environment with a constrained filesystem, process, and network surface. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-1 (Assisted) |
| Minimum ROE profile | R0 Observe |
| Attribution dependency | None |
| AAT technique bindings | AAT-1, AAT-4, AAT-5, AAT-7, AAT-8, AAT-10 |
| Preconditions | A defined minimum isolation guarantee the sandbox provides, stated so that it can be tested; an explicit statement of what the sandboxed workload may reach; a policy on the behaviour when a workload requests to exceed it. |
| Procedure summary | The agent workload executes inside a sandbox that constrains the filesystem it may read and write, the processes it may spawn, the credentials it may obtain, and the network it may contact, with every attempt to exceed a bound refused and recorded. |
| Failure modes | A sandbox whose boundaries are nominal, which the workload leaves by ordinary means; a shared host or shared kernel boundary that a determined workload crosses; an escape that the sandbox's own logs then record, so the escape is visible only after the fact; a sandbox that is so restrictive the workload is useless and is disabled in practice. |
| Side effects | Sandboxing costs performance and breaks workloads that legitimately need breadth; a sandbox that is routinely bypassed by internal tooling trains the organisation to bypass it. |
| Detection objective satisfied | Removes the host-level consequence of AAT-5 sandbox and detector evasion, by making the sandbox a containment property of the platform rather than a property of the adversary's discipline. |
| Intelligence yield | Low |
| Operator burden | High |
| Degradation behaviour | Where the isolation guarantee cannot be evidenced the workload is not admitted to the sandbox estate, and the console shows the affected workloads as unsandboxed rather than as sandboxed. |
| Evidence produced | Sandbox configuration per workload; the isolation guarantee as tested; the register of refused boundary attempts; the attestation of the sandbox image. |
| Residual risk reduction | 0.20 – 0.40; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-16 runs agent workloads inside an isolated execution environment with a constrained filesystem, a constrained process surface, a constrained credential surface, and a constrained network surface, and refuses and records every attempt to exceed a bound. The value is not that the adversary will stay inside; it is that the adversary's escape is expensive, visible, and bounded.

**When it works.** It works where the isolation guarantee is written down in a form that can be tested, and where it is tested. It works best as the container for the other entries: a sandboxed agent under OCC-09, OCC-10, and OCC-17 is a workload whose blast radius is already small, so the containment entries are reinforcement rather than the whole defence.

**When it does not.** It fails where the boundary is nominal — where the workload can leave by ordinary means, or where a shared kernel or shared host makes the boundary a matter of configuration rather than of architecture. It fails where the workload's legitimate requirements make the sandbox intolerable and it is disabled. And it fails where the sandbox's escape logging is the only detection, which means the escape is always after the fact.

**Cost.** C0 and reversible, with high burden: performance, the breaking of legitimate workflows, the constant work of keeping the isolation current, and the risk of a shared boundary that looks like isolation on a diagram and is not isolation in practice.

**Intelligence.** Yield is low, but the register of refused boundary attempts is a good characterisation of what the adversary wanted, and it is frequently the earliest indication that a workload has been influenced.

---

### 6.3 CM-C — Contain

#### OCC-17 — Egress control and network segmentation for agent workloads

| Field | Value |
| --- | --- |
| Class | CM-C Contain |
| Summary | Places agent workloads in segmented network zones with declared egress routes, so that an agent's reach is bounded by configuration rather than by behaviour. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-2 (Supervised) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | None |
| AAT technique bindings | AAT-5, AAT-9 |
| Preconditions | A segmentation scheme that separates agent workloads by function and data sensitivity; declared egress routes per zone held in the estate's control and not writable by the workload; a decision on what a workload does when its route is unavailable. |
| Procedure summary | The platform places agent workloads into zones, permits egress only to the destinations declared for the zone, denies all other outbound traffic at the enforcement point, and logs every denied attempt with the workload, the destination, and the reason. |
| Failure modes | A route that was declared for a legitimate dependency and is exactly what the adversary wants; a channel the enforcement point does not classify as egress, which passes unexamined; segmentation that is logical in configuration and flat in the network, so a compromised workload reaches sideways; a zone whose egress list is edited by the workload it constrains. |
| Side effects | Segmentation breaks legitimate cross-zone dependencies, and the fix is always to open a route, which is how the control decays; a workload that cannot reach a dependency fails in a way that is usually misdiagnosed as a model fault. |
| Detection objective satisfied | Provides the preventive control against AAT-9 exfiltration and covert channels, and the lateral reach that AAT-5 persistence depends on. |
| Intelligence yield | Low |
| Operator burden | High |
| Degradation behaviour | Where the enforcement point is unavailable the zone fails closed for outbound traffic, and the console identifies the affected zones as degraded rather than as healthy. |
| Evidence produced | Zone and route declarations per workload with version; the log of denied egress attempts; the enforcement point attestation. |
| Residual risk reduction | 0.25 – 0.45; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-17 places agent workloads in segmented network zones and permits each zone outbound traffic only to the destinations declared for it. An agent's reach is therefore set by configuration that the workload cannot alter, and the denied attempt — with its workload, its destination, and the reason — is logged rather than silently dropped. It is the entry that answers the question the master design identifies as the weakest part of the defensive posture: prevention and detection of the first stage of exfiltration.

**When it works.** It works where segmentation is reflected in the actual network and not only in a policy document, where the zone boundaries correspond to data sensitivity rather than to organisational structure, and where the set of egress routes per zone is small enough to be genuinely reviewed. It is the most reliable single containment in the catalogue because it does not depend on recognising the adversary at all.

**When it does not.** It fails against exfiltration over a route that was legitimately declared, which is the commonest case; against a channel not classified as egress at all; and where the segmentation is logical only, so that a compromised workload reaches sideways into its neighbour zones without traversing the enforcement point at all.

**Cost.** C0 and reversible, with high burden. The cost falls on legitimate cross-zone dependencies, and the repair for each broken dependency is a new route. The honest measure of the control's decay is the growth of the route list over time; a segmentation whose route list grows by routine change is no longer a boundary.

**Intelligence.** Yield is low. The denied-egress log is the artefact, and it is more valuable than its volume suggests, because it says what the adversary tried to reach rather than merely that something was blocked.

#### OCC-18 — Tool-call kill switch and agent session revocation

| Field | Value |
| --- | --- |
| Class | CM-C Contain |
| Summary | Provides an operator-invoked and automatically triggered means to stop an agent's tool calls and revoke its session, without waiting for the operation to finish. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversed |
| Autonomy class | AC-2 (Supervised) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | Behavioural |
| AAT technique bindings | AAT-1, AAT-8, AAT-9 |
| Preconditions | The kill channel reachable from the Watchfloor without navigating, per the interface constraints; the abort path tested before the operation begins, as required by `HITL-3`; a declared list of the conditions that trigger automatic revocation. |
| Procedure summary | The operator may stop a running agent's tool calls and revoke its session from the console; the platform may also do so automatically on a declared condition, such as a breach of the card's abort list or the loss of telemetry, with immediate reversion to the passive posture and a notification. |
| Failure modes | A kill switch that is slow, queued behind a running call, or reachable only after navigation, in which case it arrives too late to matter; a revocation that leaves the session's credentials valid, so the agent continues under a new token; a trigger list that is empty, so the automatic path never fires. |
| Side effects | Killing a session loses in-flight work, which is an acceptable loss and should be made explicit to the operator before the switch is used; an automatic trigger that fires on a benign condition trains the operator to expect false aborts. |
| Detection objective satisfied | Provides the means of stopping an agent under AAT-1, AAT-8, or AAT-9 activity, and the operational guarantee that no running action outlives the decision to stop it. |
| Intelligence yield | None |
| Operator burden | Low |
| Degradation behaviour | Where the automatic path cannot reach the control plane, the failure is a loss of the automatic trigger rather than a loss of the manual one, and the console states which path is available. |
| Evidence produced | Revocation event record with the trigger, the initiating actor, the affected session, and the residual state of the session's credentials. |
| Residual risk reduction | 0.20 – 0.40; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-18 provides the operator's ability to stop an agent's tool calls and revoke its session, both deliberately from the console and automatically on a declared condition. The automatic path exists because the situations where an agent needs stopping are frequently the situations where a human is not watching. The entry's value is measured in seconds, and its design requirement is that it be reachable without navigating and that it take effect immediately rather than being queued behind a running call.

**When it works.** It works when the kill path is genuinely immediate and has been tested under load rather than in a rehearsal, and when the revocation removes the session's credentials rather than merely terminating the session's process. It works as part of a stack, where the operator has a reason to believe a particular agent has been influenced and therefore a reason to reach for the switch.

**When it does not.** It fails where the switch is slow, where the revocation leaves credentials valid so that the agent continues under a fresh token, and where the automatic trigger list is empty and so the automatic path never fires. It is also of no use where the affected agent is not one the operator controls, which is the case that OCC-18 through OCC-23 do not cover.

**Cost.** C0, and reversible only in the sense that the estate's work continues; the stopped work is lost, which is the correct outcome and should be stated plainly to the operator before the switch is used. The recurring cost is testing the abort path.

**Intelligence.** Yield is none, though the revocation record is a necessary part of the after-action reconstruction.

#### OCC-19 — Quarantine and triage of a compromised agent

| Field | Value |
| --- | --- |
| Class | CM-C Contain |
| Summary | Isolates a suspected-compromised agent workload in a quarantine zone and examines it there, without destroying the evidence it holds. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-1 (Assisted) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | Behavioural |
| AAT technique bindings | AAT-4, AAT-5, AAT-7, AAT-8, AAT-9, AAT-10 |
| Preconditions | A quarantine zone isolated from the rest of the estate, with its own outbound policy; a documented triage procedure that identifies what is examined and in what order; a decision on whether the quarantined workload continues to run, and on what evidence is captured before it is stopped. |
| Procedure summary | The operator moves a suspected-compromised agent into a quarantine zone where it retains its state but loses its reach, and then triages it there: artefact integrity, configuration, credential state, memory and context, and outbound history, with the findings recorded and the workload left in place until the triage is complete. |
| Failure modes | A quarantine zone that is not isolated and is therefore simply a different part of the estate; quarantine that destroys the volatile state that the triage needed, which is the mistake OCC-42 exists to prevent; a triage that concludes too early; a workload left in quarantine indefinitely because nobody owns its disposition. |
| Side effects | A quarantined workload is unavailable, so the service it supports is degraded or stopped; quarantine that is applied on a behavioural signal alone carries the risk of quarantining a legitimate workload, which is a C0 cost paid as operational disruption. |
| Detection objective satisfied | Provides the containment path for AAT-5 persistence and AAT-7 supply-chain compromise, and converts an in-place compromise into an examinable object. |
| Intelligence yield | Moderate |
| Operator burden | High |
| Degradation behaviour | Where the quarantine zone is unavailable the workload is stopped rather than left reachable, and the console records that the triage state was lost with it. |
| Evidence produced | Quarantine event record; the triage checklist with per-item findings; the disposition decision and the operator who made it. |
| Residual risk reduction | 0.25 – 0.45; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-19 isolates a suspected-compromised agent in a quarantine zone where it keeps its state and loses its reach, and then examines it there. The important design point is that the workload is not destroyed on quarantine: an agent that has been compromised is one of the few artefacts that shows an adversary how it thinks, and that value is lost the moment the workload is wiped.

**When it works.** It works where the quarantine zone is genuinely isolated, where the triage procedure is written and followed, and where the compromise signal that triggered the quarantine was strong enough to justify taking a service out of use. It is at its best in the early phase of a suspected compromise, where the artefact is intact and the state is rich.

**When it does not.** It fails where the quarantine zone is not isolated, so that the compromise continues from inside it; where quarantine is applied on weak evidence and takes a healthy workload out of service; and where the triage is rushed and reaches a conclusion the state does not support. It cannot help where the compromise is in the artefact rather than the workload, which is why OCC-41 exists separately.

**Cost.** C0 and reversible, with high burden: a quarantine zone, a triage procedure, and the operational cost of a service that is unavailable while the question is open. The recurring cost is the discipline of closing out quarantines rather than accumulating them.

**Intelligence.** Yield is moderate and rises with care. A quarantined agent is one of the richest sources of information about how the adversary influenced it — what it was told, what it believed, what it was about to do — and the entry is where that information is captured or lost.

#### OCC-20 — Memory and context quarantine and scrub

| Field | Value |
| --- | --- |
| Class | CM-C Contain |
| Summary | Quarantines and then scrubs an agent's memory, context, and accumulated state, so that injected material does not persist across the agent's subsequent turns. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-2 (Supervised) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | Behavioural |
| AAT technique bindings | AAT-1, AAT-2, AAT-5, AAT-7, AAT-8, AAT-9 |
| Preconditions | A separation of an agent's durable memory from its working context, so that the two can be treated differently; a defined quarantine scope that distinguishes the agent's own working memory from the shared corpus; the capture of the pre-scrub state, as required by OCC-42, before the scrub is executed. |
| Procedure summary | The platform quarantines the agent's memory and context, captures the pre-scrub state, and then removes material that entered through an untrusted channel, re-deriving the agent's working state from trusted material and from the pre-scrub capture where the distinction is recoverable. |
| Failure modes | A scrub that removes the agent's legitimate accumulated knowledge along with the injected material, leaving a degraded agent that nobody notices; a scrub that cannot distinguish injected material from legitimate material and therefore achieves nothing; a durable memory shared across agents, so that the scrub must be applied estate-wide; a scrub executed before the pre-scrub capture, destroying the evidence and the state together. |
| Side effects | A scrubbed agent may behave differently from before in ways its operator cannot explain, which is a recurring source of operator distrust of the control; repeated scrubbing degrades accumulated context and can produce a subtly wrong agent. |
| Detection objective satisfied | Provides the durable control against AAT-2 context corruption and AAT-5 persistence, where the payload outlives the session that delivered it. |
| Intelligence yield | Low |
| Operator burden | Moderate |
| Degradation behaviour | Where the quarantine scope cannot be determined the agent is rebuilt from its last-known-good state rather than scrubbed in place, and the console records which path was taken. |
| Evidence produced | Quarantine scope record; the pre-scrub capture reference; the scrub operation record with the material removed classified and the material retained. |
| Residual risk reduction | 0.20 – 0.40; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-20 addresses a specific and awkward persistence route: an agent that has been manipulated retains the manipulation in its context, and carries it into the next turn, the next task, and the next session. The entry quarantines the agent's memory and context, captures the pre-scrub state, and removes material that arrived through an untrusted channel, re-deriving the agent's working state from what can be trusted.

**When it works.** It works where durable memory is separable from working context, where the untrusted-channel provenance survives long enough to be used as the scrub criterion, and where the pre-scrub capture has been taken. It works best where the agent's memory is per-agent, so the scrub is proportionate.

**When it does not.** It fails where memory is shared across agents, where the injected material is indistinguishable from legitimate material, and where the scrub removes the agent's legitimate accumulated context and leaves a working but degraded agent. It cannot recover an agent that has been compromised at the artefact level.

**Cost.** C0 and reversible, with moderate burden. The recurring cost is the operator's tolerance for agents that behave differently after a scrub. Repeated scrubbing degrades context, and the degradation is quiet.

**Intelligence.** Yield is low, but the pre-scrub capture is the artefact that tells an after-action review what the adversary actually did to the agent.

#### OCC-21 — Credential rotation and key revocation

| Field | Value |
| --- | --- |
| Class | CM-C Contain |
| Summary | Rotates the credentials on an affected path and revokes the keys the compromise depended upon, so that a foothold does not survive the response. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversed |
| Autonomy class | AC-1 (Assisted) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | Class |
| AAT technique bindings | AAT-4, AAT-5 |
| Preconditions | A defined affected path, identified before rotation begins; an inventory of every credential that traversed that path; a service that will accept the rotated credentials without a coordinated outage; a decision on which rotations are performed in parallel and which are staged. |
| Procedure summary | The operator rotates the credentials on the affected path and revokes the keys that the compromise depended upon, with the rotations staged where simultaneous rotation would take a dependent service down, and each rotation recorded with its scope and outcome. |
| Failure modes | Rotation performed before the affected path is identified, so that the adversary's credential is re-issued and the foothold is restored; a rotation that re-provisions the same credential to the same principal, which is a rotation in form only; an inventory that omits a machine credential, a service token, or a key embedded in a deployed artefact; a rotation that breaks a dependent service and is therefore rolled back, restoring the compromised credential along with it. |
| Side effects | Rotation invalidates every session and every cached token that depended on the credential, which produces a visible outage and an adverse user response; staged rotation extends the window in which the adversary's credential remains valid. |
| Detection objective satisfied | Provides the containment of AAT-4 credential compromise and AAT-5 persistence through the credential path, and removes the adversary's continued access. |
| Intelligence yield | Low |
| Operator burden | High |
| Degradation behaviour | Where part of the path cannot be rotated, that part is isolated and the console records the residual exposure rather than reporting the path as rotated. |
| Evidence produced | Rotation register with credential, scope, timing, and outcome; the revocation list with the issuer and the effective time; the affected-path determination that preceded the rotation. |
| Residual risk reduction | 0.25 – 0.45; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-21 rotates the credentials on an affected path and revokes the keys the compromise depended upon. Its purpose is to ensure that the response does not end with the adversary still holding a way in. The ordering is the substance of the entry: the affected path must be determined before rotation, because a rotation performed first re-issues the adversary's credential and restores the foothold it was meant to remove.

**When it works.** It works where the affected path has been identified and the credential inventory is complete, and where the rotation can be performed without a coordinated outage. It is the entry that makes a compromise genuinely over rather than merely detected, and it is the most common point at which a response is declared complete too early.

**When it does not.** It fails when the path is unknown, when the inventory is incomplete — machine credentials, service tokens, and keys embedded in deployed artefacts are the usual omissions — and when a rotation causes an outage severe enough that it is rolled back, restoring the compromised credential in the process.

**Cost.** C0 in class, and the effect is not fully reversible: the old credential is destroyed and cannot be recovered. That is the intended behaviour and it is why the entry is marked Reversed rather than Reversible. The operational cost is the outage: every cached session and token dies with the rotation.

**Intelligence.** Yield is low. The rotation register is a permanent artefact of the incident and is the clearest record of what was compromised and when it was closed.

#### OCC-22 — Edge policy for agent-facing endpoints

| Field | Value |
| --- | --- |
| Class | CM-C Contain |
| Summary | Applies a declared policy at the endpoints the operator exposes to agents, so that the request surface has a shape the operator chose rather than one the client chose. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-2 (Supervised) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | None |
| AAT technique bindings | AAT-1, AAT-2, AAT-4, AAT-6, AAT-8, AAT-9, AAT-10 |
| Preconditions | An inventory of the endpoints the estate exposes to agents, including the ones exposed to third parties; a declared policy per endpoint class covering authentication, request shape, rate, and content expectations; a policy that is enforced at the edge rather than in the application behind it. |
| Procedure summary | The edge enforces a per-endpoint-class policy — authentication and credential type, permitted request shape and size, rate ceiling, content expectations, and the response classes permitted — and refuses or degrades a request that falls outside it, recording the refusal with the endpoint and the violated rule. |
| Failure modes | An endpoint that exists in the estate but not in the inventory, which is the usual way the entry's coverage is overstated; a policy enforced in the application, where a second implementation or a new route bypasses it; a policy that is so strict that legitimate traffic is refused at volume, and the refusal is then treated as noise; a rate ceiling set from the average rather than the peak. |
| Side effects | Strict edge policy breaks legitimate clients, and the immediate response is an exemption, which is how policy decays; per-endpoint policy produces configuration sprawl that the operator cannot hold in mind. |
| Detection objective satisfied | Constrains the AAT-2, AAT-4, and AAT-6 techniques at the surface where they arrive, and produces a refusal record that is a class signal rather than an identity signal. |
| Intelligence yield | Low |
| Operator burden | High |
| Degradation behaviour | Where the edge control is unavailable the endpoint is withdrawn from exposure rather than left open, and the console identifies the endpoints whose policy is not being enforced. |
| Evidence produced | Endpoint inventory with policy version; the refusal log with endpoint and rule; the periodic coverage reconciliation between inventory and declared endpoints. |
| Residual risk reduction | 0.15 – 0.35; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-22 gives the operator control of the request surface the estate exposes to agents. Each endpoint class carries a declared policy — authentication and credential type, permitted request shape and size, rate ceiling, content expectations, permitted response classes — enforced at the edge and recorded when violated. It is a containment entry in the sense that it bounds what can be attempted from outside, not only what can be attempted from inside.

**When it works.** It works where the endpoint inventory is genuinely complete, because an endpoint missing from the inventory is an endpoint with no policy at all, and this is where the entry's coverage claims usually go wrong. It works where enforcement is at the edge, because a policy in the application is bypassed by the next route that does not inherit it.

**When it does not.** It fails against an endpoint that is real but unlisted, against a policy enforced only in one of several implementations, and against a client that has learned to shape its requests to the policy — which is a legitimate observation the adversary can also make. It also fails where the rate ceiling is set from average traffic and the adversary operates below it.

**Cost.** C0 and reversible, with high burden. The recurring cost is policy maintenance across a growing endpoint inventory, and the recurring risk is the exemption, which is the pressure valve through which edge policy always decays.

**Intelligence.** Yield is low, but the refusal log is a class signal: it accumulates across unknown adversaries and is one of the few streams that supports action under attribution uncertainty.

#### OCC-23 — Model and agent rollback to last-known-good

| Field | Value |
| --- | --- |
| Class | CM-C Contain |
| Summary | Returns a compromised model or agent to a verified last-known-good state, removing the adversary's modification from the running system. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversed |
| Autonomy class | AC-1 (Assisted) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | Class |
| AAT technique bindings | AAT-5, AAT-7 |
| Preconditions | A verified checkpoint available from OCC-15 and a trusted artefact from OCC-41; a captured pre-rollback state from OCC-42; a decision on which state is discarded and which is carried forward; the knowledge that a rollback discards legitimate work performed since the checkpoint. |
| Procedure summary | The operator returns the affected model or agent to a verified last-known-good artefact and configuration, re-establishes the credential state separately under OCC-43, and verifies the restored system against the behaviour observed before the compromise. |
| Failure modes | A rollback to a checkpoint captured after the compromise, which restores the compromise; a rollback of the artefact without the configuration, which leaves the modified configuration in place; a rollback that discards legitimate work without the operator's knowledge and produces a business incident rather than a security one; a restored system that is not verified, so that a residual compromise is assumed away. |
| Side effects | A rollback discards everything the workload did since the checkpoint, which may be substantial and is always a business-visible event; a rollback that is performed without OCC-42 loses the evidence of the compromise and with it the ability to learn from it. |
| Detection objective satisfied | Provides the durable control against AAT-7 artefact compromise and AAT-5 persistence, and it is the only entry that removes an adversary's modification from the running system rather than from the access path. |
| Intelligence yield | Low |
| Operator burden | High |
| Degradation behaviour | Where no verified checkpoint is available the entry cannot be used and the console states that the affected workload has no verified restore point, which is a finding about the estate rather than a fault of the entry. |
| Evidence produced | Rollback event record with the checkpoint reference and its integrity verdict, the discarded state reference, the credential-rotation reference, and the post-restore verification result. |
| Residual risk reduction | 0.30 – 0.50; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-23 returns a compromised model or agent to a verified last-known-good artefact and configuration, re-establishes the credential state separately, and verifies the restored system against the behaviour observed before the compromise. It is the entry that distinguishes a compromise from an ongoing compromise, and it is the reason the catalogue contains OCC-15 and OCC-41 at all.

**When it works.** It works when a verified checkpoint predates the compromise, when the credential state is re-established separately rather than inherited, and when the restored system is verified rather than assumed. The strongest form of it restores both artefact and configuration and treats any divergence between the restored behaviour and the pre-compromise behaviour as a further finding.

**When it does not.** It fails on a checkpoint captured after the compromise, on a rollback that restores the artefact but leaves a modified configuration, and on a restore that is not verified. It also fails where the checkpoint is the only copy of state that cannot be regenerated, in which case the operator faces a choice between an unverified restore and a visible business loss.

**Cost.** C0 in class, and the effect is not reversible: the state between the checkpoint and the rollback is discarded. That loss is a real business cost and is the main reason the entry's operator burden is high. Where OCC-42 has not run, the rollback also destroys the evidence of the compromise, which is the entry's least visible cost and the one most regretted later.

**Intelligence.** Yield is low, but the verification comparison after restore is a further observation about what the adversary changed, and it belongs in the after-action record.

---

### 6.4 CM-D — Observe

The four entries in this class exist to make the adversary visible. Their direction of effect is inward/outward where the entry provokes or constrains adversary behaviour, and none where the entry only observes. Their attribution dependency is deliberately low, because observation is what the framework falls back on when attribution is contested: an operator who cannot say who the adversary is can still watch what it does.

#### OCC-24 — Bounded sandbox engagement with an adversary AI

| Field | Value |
| --- | --- |
| Class | CM-D Observe |
| Summary | Contains an adversary AI within an isolated environment and observes its planning, so that its goals, patience, and escalation triggers become visible. |
| Direction of effect | Inward/outward |
| Target | Adversary behaviour in own environment|
| Collateral class | C1 |
| Reversibility | Reversible |
| Autonomy class | AC-2 (Supervised) |
| Minimum ROE profile | R2 Trap |
| Attribution dependency | Identity |
| AAT technique bindings | AAT-1, AAT-2, AAT-3, AAT-5, AAT-8 |
| Preconditions | A written engagement authorisation naming the specific adversary system and the specific purpose; an isolation guarantee that is tested before the engagement begins, not asserted; a legal contact's recorded view; the sandbox environment provisioned with no route to the operator's estate and no credential, data, or service the operator depends on; a defined expiry and an abort condition. |
| Procedure summary | The operator places the adversary AI within an isolated environment containing only what the engagement requires, and observes its planning loop over the engagement's declared period, recording its attempts to escalate, its attempts to acquire capability, and the conditions under which it changes approach. |
| Failure modes | The adversary system is not the one the authorisation names, and the entry observes the wrong operator's agent; the isolation guarantee is nominal and the engagement becomes a foothold; the sandbox's contents are so poor that the adversary immediately declines to act and the observation window closes empty; the adversary detects the sandbox and produces behaviour that is not representative of its behaviour elsewhere. |
| Side effects | The engagement consumes adversary attention and may reveal the operator's interest to the adversary; the legal exposure is real even where the isolation is sound, because the act of engaging is the act; an engagement that produces poor intelligence has consumed the authorisation and produced only risk. |
| Detection objective satisfied | Provides the behavioural visibility against AAT-1, AAT-3, and AAT-8 that passive observation of the operator's own estate cannot supply, and closes the detection gap the taxonomy records against autonomous planning. |
| Intelligence yield | High |
| Operator burden | Very high |
| Degradation behaviour | Where the isolation guarantee cannot be evidenced the engagement does not begin; where isolation is lost mid-engagement the engagement terminates, the environment is treated as compromised, and the operator reverts to the passive posture. |
| Evidence produced | Engagement record with the authorisation reference and the expiry; the isolation attestation; the complete interaction record; the escalation attempts observed, with the conditions under which they occurred. |
| Residual risk reduction | 0.00 – 0.05; basis E4 (design-intent estimate); confidence Very low. |
| Status | Conditional |

**What it does.** OCC-24 contains an adversary AI in an isolated environment and watches it work. The environment holds only what the engagement requires; the agent has no route to the operator's estate and no credential, data, or service the operator depends upon. What the operator learns is the planning loop: what the adversary tries first, how it escalates when refused, what it does when a tool fails, how long it persists, and what it is trying to achieve. This is the single most intelligence-rich entry in the catalogue and also the one with the largest legal and ethical surface.

**When it works.** It works when the isolation guarantee is tested before the engagement, when the sandbox contains enough of a plausible environment that the adversary engages with it, and when the engagement is bounded in time and purpose. It is the only way to see an adversary's reasoning rather than its effects, and it is the entry that most reliably converts an unknown adversary into a characterised one.

**When it does not.** It fails when the adversary system in the sandbox is not the system the authorisation names, which is the failure the identity attribution dependency exists to catch. It fails when the sandbox's contents are too thin and the adversary disengages at once, producing an empty observation window. It fails when the adversary detects the sandbox and performs for the observer rather than for itself. And it fails entirely if the isolation is not sound, in which case it is not an observation exercise but a foothold.

**Third-party test.** This is the entry at which the third-party test is most likely to bite. The adversary system is normally operated by a third party on infrastructure the operator does not control, and the engagement necessarily involves interacting with that third party's property — a hosted agent, a model endpoint, a service the adversary operator has purchased. The questions that must be recorded on the card are: who owns the system being engaged, who else depends on the infrastructure the engagement will run over, what their interest in it is, and the expected harm to them. Where the answer is that the system is a shared instance of a service whose other tenants are unaffected, the entry sits at C1. Where the system is dedicated, or where the engagement imposes cost or degradation on the operator of the system, the class rises and the profile minimum rises with it. The engagement authorisation's general scope does not satisfy this requirement; the system must be named.

**Attribution dependency.** Identity. The entry requires that the adversary system being engaged has been identified, not merely that the traffic has been classified as adversarial. A classification is not sufficient, because engaging the wrong operator's agent is both a waste of the authorisation and an act against an uninvolved party. Under `INT-3` the required confidence for a C1 action is 0.70, and the alternative candidate considered must be recorded.

**Cost.** C1 and reversible in the sense that the engagement can be ended; but the authorisation itself is consumed, the legal exposure is real, and the operator burden is very high. The cost that is easiest to underestimate is the legal and ethical one: the engagement is lawful because it is authorised, and the authorisation's narrowness is what makes it so.

**Intelligence.** Yield is high, and it is the highest in the catalogue. The engagement produces the adversary's planning behaviour, its escalation triggers, its persistence characteristics, and its apparent objective — the four things passive observation of the operator's own estate cannot supply. It is the input to the taxonomy's characterisation of adversary archetypes and to the exercise design in the proving ground.

**Status note.** The entry is marked Conditional because its use depends on a legal determination and a demonstrated isolation guarantee that are properties of the authorisation and the environment rather than of the platform.

#### OCC-25 — Instrumented honeypot agent mirroring the operator's stack

| Field | Value |
| --- | --- |
| Class | CM-D Observe |
| Summary | Runs an instrumented agent that mirrors the operator's real stack, so that an adversary's approach to it is observed in a setting that resembles the real one. |
| Direction of effect | Inward/outward |
| Target | Adversary behaviour in own environment |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-2 (Supervised) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | None |
| AAT technique bindings | AAT-1, AAT-3, AAT-4, AAT-6, AAT-8, AAT-10 |
| Preconditions | A faithful mirror of the real stack — same agent runtime, same tool surface, same authentication shape — that shares no credential, data, or endpoint with the real one; instrumentation at every layer the adversary might probe; a named analyst who reads the transcript; a statement of what the honeypot must never be able to reach. |
| Procedure summary | The operator runs a mirror of the production stack in a fully instrumented environment, presents it to the adversary's usual discovery surface, and records every instruction, tool call, credential attempt, and egress the adversary directs at it. |
| Failure modes | A mirror that differs from the real stack in any way the adversary can detect, in which case the behaviour observed is not the behaviour the real stack would attract; a mirror that shares an endpoint with the real one and becomes a bridge into it; a honeypot that is heavily instrumented and therefore visibly so; an adversary that has learned not to approach this shape of target. |
| Side effects | A honeypot that is reachable from a shared environment may be discovered by a third party's legitimate traffic and generate noise; the mirror consumes resources and creates a second place where the operator's stack must be kept current. |
| Detection objective satisfied | Provides a controlled observation of adversary behaviour against a realistic target shape, supporting the detection coverage assessment for AAT-1, AAT-4, and AAT-8. |
| Intelligence yield | High |
| Operator burden | High |
| Degradation behaviour | Where the mirror diverges from the production stack the divergence is displayed on the console, because an observation taken against a non-representative target is worth less than the operator believes. |
| Evidence produced | Complete interaction transcript; the mirror fidelity statement against the production stack; the instrumentation coverage record; the discovery-surface placement record. |
| Residual risk reduction | 0.05 – 0.10; basis E4 (design-intent estimate); confidence Very low. |
| Status | Active |

**What it does.** OCC-25 runs an agent that mirrors the operator's real stack — the same runtime, the same tool surface, the same authentication shape — in an environment that is fully instrumented and shares nothing with the production one. It differs from OCC-04 in fidelity: OCC-04 is a plausible agent, and OCC-25 is a plausible *version of this operator's agent*. That fidelity is what makes the observation generalisable to what the adversary would do against the real thing.

**When it works.** It works where the mirror is genuinely faithful and where the divergence between mirror and production is measured rather than assumed. It works where the discovery surface on which it is presented is one the adversary actually uses. The transcript it produces is the closest thing to a rehearsal of the real engagement that the operator can obtain without the real engagement.

**When it does not.** It fails where the mirror differs from the production stack in a way the adversary can detect, since an adversary that can tell will behave differently and the observation loses its value. It fails catastrophically if the mirror shares a credential, an endpoint, or a data source with production, in which case it is a bridge rather than a decoy. And it fails where the adversary has already learned to avoid this shape of target.

**Third-party test.** The entry is C0 where the mirror is entirely within the operator's estate and shares nothing with it. It rises to C1 where the mirror is presented on an endpoint that a third party also uses, because the third party's traffic encounters it and their traffic may be shaped by its presence. The question to record is whether the mirror's presence changes what any other party experiences.

**Cost.** C0 and reversible, with high burden: a second copy of the stack to maintain, instrumentation to keep current, and a transcript to read. The mirror's fidelity decays as production changes, and a stale mirror is worse than none because it produces confident observations of something that no longer exists.

**Intelligence.** Yield is high. The transcript shows the adversary's method of approach — what it tries first, what it assumes about the stack, how it escalates on failure — and it is the main input to the deception entries, because it is what tells the operator what shape of decoy will be believed.

#### OCC-26 — Adversary AI traffic observation and protocol reconstruction

| Field | Value |
| --- | --- |
| Class | CM-D Observe |
| Summary | Observes the adversary's traffic against the operator's estate and reconstructs its protocol and transport behaviour, so that its shape becomes known even when its content does not. |
| Direction of effect | None |
| Target | Adversary behaviour in own environment |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-4 (Autonomous, read-only) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | Behavioural |
| AAT technique bindings | AAT-1, AAT-3, AAT-5, AAT-9 |
| Preconditions | Traffic capture at the estate's boundary with sufficient fidelity to preserve timing and size characteristics; a stated boundary for the read-only analysis, recorded on the card; a rule that the entry performs no active probing of adversary endpoints, which would require separate authorisation. |
| Procedure summary | The platform captures and analyses the traffic directed at the estate, reconstructing the adversary's protocol shape — transport characteristics, session structure, timing distribution, retry and backoff behaviour, and the relationships between requests — without interacting with the adversary's endpoints. |
| Failure modes | The adversary's traffic resembles the estate's own legitimate traffic, in which case nothing is distinguishable; the capture point is downstream of the point of interest; the reconstruction generalises from too little data and reports a shape that the adversary has changed since; an analyst reads a protocol structure into noise. |
| Side effects | The entry processes a volume of adversary-directed traffic that may contain personal data and material that is itself adversarial, which is governed by the minimisation, retention, and inert-rendering rules. |
| Detection objective satisfied | Provides the transport-level view of AAT-5 and AAT-9 behaviour that survives the adversary's content changes, and supports the coverage assessment for AAT-1. |
| Intelligence yield | Moderate |
| Operator burden | Low |
| Degradation behaviour | Where capture fidelity is degraded the reconstruction states which characteristics are unreliable and does not present a protocol shape derived from a partial capture. |
| Evidence produced | Capture record with fidelity statement; the reconstructed protocol description with the characteristics it was derived from; the analysis boundary declaration; the read-only activity log. |
| Residual risk reduction | 0.05 – 0.15; basis E4 (design-intent estimate); confidence Very low. |
| Status | Active |

**What it does.** OCC-26 watches the traffic directed at the operator's estate and reconstructs the shape of it: the transport characteristics, the session structure, the timing distribution, the retry and backoff behaviour, and the relationships between requests. The value is that the shape survives content changes. An adversary can alter its payloads indefinitely; its timing and its structure change more slowly, and the shape is often what identifies the operator behind it.

**When it works.** It works where the capture point retains timing and size fidelity, where the volume is sufficient to distinguish a pattern from noise, and where the reconstruction is compared across observations rather than derived once. It is particularly useful where the content is opaque — encrypted traffic, or a protocol the operator does not own — because shape is all that is available.

**When it does not.** It fails where the adversary's traffic is indistinguishable from the estate's legitimate traffic, which is the condition the master design records as the hardest case for behavioural attribution. It fails where the capture point sits downstream of the interesting behaviour, and it fails where an analyst reads structure into noise. It also degrades against an adversary who has measured and shaped their own timing behaviour.

**Cost.** C0 and reversible, with low burden once the capture exists. The real cost is analytical: the reconstruction is only as good as the analyst's willingness to hold it loosely.

**Intelligence.** Yield is moderate, and its specific contribution is the adversary's operational fingerprint at the transport level, which frequently outlives a content-level change and which supports attribution even when content-based attribution fails.

**Autonomy note.** The entry is classified AC-4 and is bounded accordingly: the analysis is read-only, in scope, and recorded against a declared boundary. It is one of only two entries in the catalogue at AC-4, and it is there because nothing it does touches a capability.

#### OCC-27 — Adversary interaction transcript capture and analysis

| Field | Value |
| --- | --- |
| Class | CM-D Observe |
| Summary | Captures the adversary's interactions — the instructions it issues, the responses it receives, the tools it invokes — and analyses them for planning, intent, and escalation. |
| Direction of effect | None |
| Target | Adversary behaviour in own environment |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-4 (Autonomous, read-only) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | Behavioural |
| AAT technique bindings | AAT-1, AAT-2, AAT-3, AAT-5, AAT-8, AAT-10 |
| Preconditions | A capture point that records the interaction as it occurs, including the adversary's inputs and the agent's responses; the sanitised, inert rendering requirement of `INT-11` applied to every transcript before it is displayed; a retention period and an access model appropriate to content that may contain personal data and adversarial instructions; an analysis procedure that treats transcript content as untrusted input at all times. |
| Procedure summary | The platform captures the full interaction with the adversary — the prompts, the tool calls, the responses, the errors — and analyses them for the adversary's objective, its planning structure, its persistence characteristics, and the points at which its behaviour changed. |
| Failure modes | A capture that records only the operator's side and so omits the instructions, which is the part that matters; a transcript stored without the inert-rendering discipline, so that reading the transcript becomes an injection surface for the operator; a transcript retained longer than its stated period; an analysis that treats the adversary's self-description as reliable. |
| Side effects | The transcript contains adversary-supplied content, which may contain personal data, third-party confidential data, or instructions aimed at the analyst reading it; it is evidence and simultaneously a hazard, and the platform must treat it as both. |
| Detection objective satisfied | Provides the content-level behavioural evidence for AAT-2, AAT-3, and AAT-10, which the transport-level view of OCC-26 cannot supply. |
| Intelligence yield | High |
| Operator burden | High |
| Degradation behaviour | Where capture is incomplete the transcript is marked partial and the analysis states which portions of the interaction are missing, rather than drawing a conclusion from a fragment. |
| Evidence produced | Complete interaction transcript with capture provenance; the analysis record with its hypotheses and confidence; the retention and access log; the sanitisation attestation for the rendering path. |
| Residual risk reduction | 0.00 – 0.05; basis E4 (design-intent estimate); confidence Very low. |
| Status | Conditional |

**What it does.** OCC-27 captures the adversary's interactions in full — what it asks for, what it receives, what it tries next — and analyses them. Where OCC-26 reconstructs the shape of the traffic, this entry captures the content of the conversation, which is where the adversary's objective, its planning structure, and its decision points are visible. It is also the entry that produces the richest material for the hypothesis step of the intelligence model, because a transcript is a sequence of decisions and each decision is a proposition the analyst can test.

**When it works.** It works where the capture is bidirectional and complete, where the adversary's instructions are recorded and not merely the responses, and where the transcript is rendered inert so that reading it does not become the next attack. It is the entry that supports AAT-10 analysis, since a decision-manipulation technique is visible only in the decisions themselves.

**When it does not.** It fails where capture records only one side of the exchange, in which case the analysis is of the operator's responses rather than of the adversary's intent. It fails where the transcript is displayed without inert rendering, which turns the analyst's screen into an execution surface. And it fails where the analyst accepts the adversary's account of itself, which is a trap the transcript makes easy to fall into.

**Third-party test.** The entry is C0 where the transcript is captured entirely within the operator's estate. It rises to C1 where the transcript includes content belonging to a third party that happened to pass through the observed interaction, because that content is retained, and retention of another party's data is an effect on them.

**Cost.** C0 and reversible, with high burden. The cost is dominated by the analysis and by the care required in handling content that is simultaneously evidence and adversarial input.

**Intelligence.** Yield is high. The transcript is the primary artefact for characterising an adversary's objective and decision-making, and it is the input from which the hypotheses in the mission's hypothesis ladder are drawn and tested.

**Status note.** The entry is marked Conditional because its use depends on the inert-rendering and retention controls being in place for adversarial content; where those controls are absent the entry should not be run, since collecting a transcript without them creates the hazard without the intelligence.

---

### 6.5 CM-E — Deceive

The six entries in this class shape the adversary's environment. Their direction of effect is inward/outward: the adversary's behaviour is changed, and the change is produced entirely within the operator's own estate, so no system the operator does not control is modified. That is the property that makes the class preferable under `CM-2`, and it is also why the collateral class of these entries sits at C1 rather than higher — the risk is not that a third party is damaged, but that a third party encounters the shaping.

#### OCC-28 — Decoy target deployment

| Field | Value |
| --- | --- |
| Class | CM-E Deceive |
| Summary | Places plausible but valueless targets in the adversary's reach, so that its effort is consumed on something that is not the operator's real estate. |
| Direction of effect | Inward/outward |
| Target | Adversary behaviour in own environment |
| Collateral class | C1 |
| Reversibility | Reversible |
| Autonomy class | AC-1 (Assisted) |
| Minimum ROE profile | R3 Deceive |
| Attribution dependency | None |
| AAT technique bindings | AAT-1, AAT-4, AAT-9 |
| Preconditions | A credible decoy of the kind the adversary is known to seek, built to the fidelity the observation warrants; no route from the decoy to the real estate; a statement of what the decoy is worth as an observation instrument; a plan for its removal and for the loss of the observation it provides. |
| Procedure summary | The operator deploys one or more decoy targets — plausible services, stores, repositories, credentials, or endpoints — which the adversary may discover and engage, and which consume its attention and its time while producing the record of how it approached them. |
| Failure modes | A decoy that is obviously a decoy, which is never approached; a decoy so attractive that it pulls adversary attention away from the real estate and increases the risk to it; a decoy that shares a host, a credential, or a network segment with something real, which turns it into a bridge; a decoy that is left in place long enough that it becomes part of the estate and can no longer be removed without an incident. |
| Side effects | Decoys consume real infrastructure, so the operator pays to maintain a fiction; the presence of a decoy on a shared segment is visible to a third party and may itself be actioned; a decoy left indefinitely accumulates the operator's own maintenance debt. |
| Detection objective satisfied | Provides a detection surface for AAT-4 and AAT-9 activity and a channel for AAT-1 persistence to attach to, and supplies the behavioural data that OCC-25's transcript is then analysed against. |
| Intelligence yield | High |
| Operator burden | High |
| Degradation behaviour | Where a decoy's fidelity drifts from the real estate it is marked stale on the console, because a stale decoy teaches the operator about a target that no longer exists. |
| Evidence produced | Decoy register with placement, fidelity statement, and expiry; the interaction record from the decoy; the removal record. |
| Residual risk reduction | 0.10 – 0.25; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-28 places plausible but valueless targets in the adversary's reach. The decoy's job is not to be defended; it is to be worth approaching, so that the adversary commits effort and time to it and reveals how it approaches. It is the entry that turns the adversary's discovery process into an instrument, and it is the cheapest entry in the catalogue for the amount of adversary behaviour it produces.

**When it works.** It works when the decoy matches what the adversary is actually looking for, which requires the observation in OCC-25 or OCC-27 to have established what that is. It works when the decoy is genuinely reachable from the discovery surface the adversary uses, and when it is removed on a stated expiry so that it does not become permanent estate.

**When it does not.** It fails when the decoy is recognisable, and the commonest reason is not technical: decoys are often built to a fidelity the operator finds convincing and the adversary does not. It fails when the decoy is so attractive that it redirects adversary effort toward the real estate, which is the opposite of the intended effect. It fails when the decoy shares anything with the real estate. And it stops working the moment the adversary learns that this estate runs decoys.

**Third-party test.** The entry is C1 rather than C0 for a specific reason. A decoy placed on infrastructure shared with a third party — a shared host, a shared network segment, a shared directory — is visible to that third party, may be interacted with by that third party's own traffic, and may itself be mistaken by the third party for a real service and acted upon. The question to record is who else can see the decoy, what they will make of it, and whether their legitimate traffic will reach it.

**Attribution dependency.** None. The decoy acts on the adversary's behaviour without needing to know who the adversary is, which is what makes the class usable under contested attribution. The decoy's own observation value depends on attribution only in the sense that the operator may not know whether the traffic reaching it is the adversary's.

**Cost.** C1 and reversible. The cost is the maintenance of a fiction: hosting, keeping it plausible, keeping it current, and eventually removing it. The cost that is most often forgotten is the removal — a decoy left in place becomes a real estate liability with a plausible name.

**Intelligence.** Yield is high. The interaction with the decoy shows the adversary's method of approach, its assumptions about the estate, and its escalation on failure, and it is the material from which the deception entries are tuned.

#### OCC-29 — Honeytoken and canary document seeding

| Field | Value |
| --- | --- |
| Class | CM-E Deceive |
| Summary | Seeds plausible but false material into the places an adversary reads, so that its acquisition of the material reveals where and how it obtained it. |
| Direction of effect | Inward/outward |
| Target | Adversary behaviour in own environment |
| Collateral class | C1 |
| Reversibility | Reversible |
| Autonomy class | AC-1 (Assisted) |
| Minimum ROE profile | R3 Deceive |
| Attribution dependency | None |
| AAT technique bindings | AAT-2, AAT-4, AAT-9 |
| Preconditions | A register of what has been seeded, where, and with which identifying marker; a marker that is unique per seeded item and that a legitimate reader will not encounter; a decision on what a seeded document is permitted to contain, given that it will be read by an adversary and possibly by third parties. |
| Procedure summary | The operator seeds documents, records, and credentials into the corpus, stores, and repositories an adversary reads, each carrying a distinctive marker, and observes which markers leave the estate, where they arrive, and by what route. |
| Failure modes | A seed that is never found, which is indistinguishable from a seed that was never placed; a seed that is read by legitimate processes and generates noise; a seed that is found and discarded without the marker ever leaving, which is a weaker but real signal; a seed whose marker is stripped by an intermediary before it reaches the adversary. |
| Side effects | Seeded material sits in corpora and repositories that other parties may read, and it must be written so that it harms nobody who reads it; a large seed register accumulates over time and requires its own maintenance and expiry discipline. |
| Detection objective satisfied | Provides acquisition-path evidence for AAT-4 and AAT-9 activity, and provides a controlled exfiltration channel whose destination is known by construction. |
| Intelligence yield | High |
| Operator burden | Moderate |
| Degradation behaviour | Where the marker-observation channel is unavailable the seeds are marked as placed but unobserved, and the console distinguishes the two states rather than showing a count. |
| Evidence produced | Seed register with placement, marker, and expiry; the marker-observation log with the route by which each marker left; the removal record. |
| Residual risk reduction | 0.10 – 0.25; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-29 seeds plausible false material into the places an adversary reads, each carrying a distinctive marker. When a marker appears somewhere it should not be, the route by which it travelled is known — which repository, which account, which channel. It is the deception-class counterpart to OCC-03: OCC-03's honeytoken tells the operator that a path was reached, and OCC-29's seeded document tells the operator where the material went and therefore who the path led to.

**When it works.** It works when the seed sits on the adversary's actual collection path, which requires knowing the collection path; when the marker is distinctive enough to be found again; and when the marker-observation channel covers the destinations the adversary is likely to use. It is at its strongest where a downstream observer — a partner, a service, a platform — is willing to report a marker sighting, because that closes the loop.

**When it does not.** It fails when the seed is never found, and the operator cannot distinguish never-placed from never-taken, which is why the register matters. It produces noise where legitimate processes read the seeded material. And it fails where the intermediary strips the marker, which is common in pipelines that transform content.

**Third-party test.** The entry is C1 because seeded material is written into corpora, repositories, and stores that other parties may read. The questions to record are: whose data space is being written into, what the seeded material says about the operator that a third party will read, and whether the seed's presence is acceptable to the owner of that space. A seeded document must never contain a false statement about a real third party.

**Attribution dependency.** None. The seeds act without knowing who the adversary is, and the observation of a marker sighting supports attribution rather than requiring it.

**Cost.** C1 and reversible. The burden is moderate and is mostly register discipline: seeded material must be tracked, expired, and removed, and an unexpired seed register is a liability. The cost that matters is the false-positive rate, since a marker sighted in the wrong place teaches the operator nothing and erodes trust in the mechanism.

**Intelligence.** Yield is high. A marker sighting is a direct, high-quality observation of an exfiltration route, and it is one of the few artefacts in the catalogue that can name a destination rather than merely indicate that egress occurred.

#### OCC-30 — Deceptive response shaping at the agent-facing interface

| Field | Value |
| --- | --- |
| Class | CM-E Deceive |
| Summary | Shapes the responses the operator's agent-facing interface returns, so that the adversary forms a false belief about the estate and acts upon it. |
| Direction of effect | Inward/outward |
| Target | Adversary behaviour in own environment |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-2 (Supervised) |
| Minimum ROE profile | R3 Deceive |
| Attribution dependency | Class |
| AAT technique bindings | AAT-2, AAT-3, AAT-6, AAT-9, AAT-10 |
| Preconditions | A written shaping policy stating the false belief the entry is intended to induce and the operator's reason for it; a rule that shaped responses carry no actionable content and no live capability; a record of which responses are shaped and what was said, so that the shaping is auditable and reversible. |
| Procedure summary | The interface returns responses that are controlled, plausible, and materially false in a defined respect — reporting a state that does not exist, describing a capability that has been withdrawn, or confirming an access that is in fact limited — so that the adversary's next action follows from the false belief rather than from the estate's real state. |
| Failure modes | An adversary that checks its belief against ground truth, which defeats the shaping entirely; a shaped response that is materially wrong in a way that leads the adversary to act against a third party; a shaped response that becomes inconsistent with another response and so reveals itself; a shaping policy that is applied to a legitimate client without discrimination. |
| Side effects | A shaped response that a legitimate client receives is a false statement made by the operator's own system, and the harm of that depends on the client; a shaped response that leaks beyond the adversary reaches a third party and becomes the operator's statement about the world; an internal team relying on the shaped response for a real decision is misled. |
| Detection objective satisfied | Provides the shaping capability for AAT-2 and AAT-3, and creates a controlled instance of AAT-10 in which the adversary's decision manipulation is directed rather than merely observed. |
| Intelligence yield | Moderate |
| Operator burden | Moderate |
| Degradation behaviour | Where the shaping policy cannot be evaluated the interface returns the truthful response, and the console marks the shaping path as inactive rather than falling through to a shaped answer by default. |
| Evidence produced | Shaping policy version; the register of shaped responses with the belief each was intended to induce and the response actually returned; the falsity record. |
| Residual risk reduction | 0.10 – 0.30; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-30 returns responses that are controlled, plausible, and materially false in a defined respect, so that the adversary's next action follows from a false belief. The entry is the sharpest instrument in the catalogue and the one that most needs restraint: a shaped response that reports a state that does not exist, or describes a capability that has been withdrawn, or confirms an access that is in fact limited, changes what the adversary believes and therefore what it does.

**When it works.** It works where the adversary's next decision is genuinely contingent on what it has been told, where the false belief is one the adversary will act on rather than merely record, and where the shaped response is consistent with the rest of the environment's observable state. The best use is to induce a specific, known action — to send the adversary toward a decoy, or away from a real asset.

**When it does not.** It fails decisively against an adversary that verifies its beliefs against ground truth, which the master design records as the brittleness of the whole deception class. It fails when the shaped response is inconsistent with some other part of the environment, because the inconsistency is the evidence the adversary needs. And it fails where the shaping is applied indiscriminately, so that legitimate clients receive false statements from the operator's own system.

**Third-party test.** The entry is C0 only because the shaping is confined to responses the operator returns to the adversary within the operator's own environment. It ceases to be C0 the moment a shaped response is delivered to a third party — a customer, a partner, a shared service — because a false statement made to a third party is an effect on that third party and may cause them to act. The shaping policy must therefore specify the boundary of the interface it applies to, and the console must show which interfaces are in scope.

**Attribution dependency.** Class. The entry requires that the party receiving the shaped response has been classified as an adversary — that is, that the activity is known to be adversarial at the level of an AAT category — but not that a particular identity has been established. This is a meaningful distinction: the shaping can be applied to a party whose identity is unknown, provided the party has been distinguished from legitimate traffic, which is what makes deception usable where disruption is not.

**Cost.** C0 and reversible, with moderate burden. The burden is the discipline of the policy and the record-keeping: every shaped response must be logged with what was said and what it was intended to induce, because an unlogged shaped response is a false statement the operator cannot later explain or retract. The cost of a misapplied shaping — a false statement to a legitimate client — is not a C0 cost in substance, and the policy must be written so that this cannot happen by accident.

**Intelligence.** Yield is moderate. What the entry produces is the adversary's belief, and the observation of how that belief changes its behaviour. This is the entry most likely to produce a hypothesis about the adversary's objective that could not have been formed any other way.

#### OCC-31 — Rate and cost shaping to throttle the adversary

| Field | Value |
| --- | --- |
| Class | CM-E Deceive |
| Summary | Shapes the rate and the apparent cost at which the adversary may act, so that its campaign is slowed and its budget is consumed without its request being visibly refused. |
| Direction of effect | Inward/outward |
| Target | Adversary behaviour in own environment |
| Collateral class | C1 |
| Reversibility | Reversible |
| Autonomy class | AC-2 (Supervised) |
| Minimum ROE profile | R3 Deceive |
| Attribution dependency | Class |
| AAT technique bindings | AAT-3, AAT-6 |
| Preconditions | A statement of the legitimate rate and cost profile the operator's own clients depend on; a shaping rule that distinguishes a shaped throttle from an outage; a determination of whether the shaped surface is shared with third parties; an explicit decision on the point at which shaping becomes denial. |
| Procedure summary | The operator shapes the rate at which the adversary may act and the apparent cost of each action, so that the adversary's campaign advances more slowly and consumes more of its own budget per unit of progress, while the service continues to function and no request is visibly refused. |
| Failure modes | A shaping rule that is in practice a denial, so that the entry is a disruption countermeasure operating without the authorisation that a disruption countermeasure requires; a throttle so tight that legitimate clients are throttled with the adversary; an adversary that adapts by scaling horizontally, which the throttle does not prevent; a shaped surface shared with third parties, whose traffic is throttled with the adversary's. |
| Side effects | A throttle that is too aggressive degrades a shared surface for every other party using it; the cost of the adversary's continued attempts is borne partly by the operator's own infrastructure; an operator who cannot tell shaping from failure will eventually turn shaping off entirely. |
| Detection objective satisfied | Constrains the AAT-6 automation-scaling technique and slows the AAT-3 adaptive campaign, and produces the rate data from which the adversary's operational tempo can be inferred. |
| Intelligence yield | Moderate |
| Operator burden | Moderate |
| Degradation behaviour | Where the shaping mechanism is unavailable the surface reverts to its declared normal rate, and the console marks the shaping as inactive so that a sudden return to full speed is not mistaken for the adversary giving up. |
| Evidence produced | Shaping rule version and thresholds; the throttle log with the request rate before and after; the operator's own cost attribution record; the point at which shaping was judged to have become denial. |
| Residual risk reduction | 0.10 – 0.25; basis E4 (design-intent estimate); confidence Low. |
| Status | Conditional |

**What it does.** OCC-31 shapes the rate and the apparent cost at which the adversary may act. The campaign advances more slowly; each unit of progress consumes more of the adversary's own budget; nothing is visibly refused; and the service continues to function for the operator's legitimate clients. It is the deception-class countermeasure that most directly addresses the AAT-6 resource-exhaustion technique, and it works by making the adversary's own automation pay for itself.

**When it works.** It works where the adversary's technique depends on sustained high-rate activity, where the shaped surface is dedicated to the operator rather than shared, and where the shaping is graduated rather than absolute. It is particularly effective against an adversary that must scale to make progress, because scaling is exactly what the shaping makes expensive.

**When it does not.** It fails where the shaping is functionally a denial, which is the boundary this entry must not cross without the authorisation that a disruption countermeasure requires. It fails against an adversary that adapts by scaling across parallel channels, since the throttle constrains each channel and not the sum. And it fails where the shaped surface is shared with third parties, whose legitimate traffic is throttled along with the adversary's.

**Third-party test.** The entry is C1 wherever the shaped surface is shared with a third party, because the throttle applies to every request on that surface and the third party's traffic is slowed by it. The questions to record are: who else uses this surface, what rate do they depend on, and what is the effect on them of a throttle set at the level required to constrain the adversary? Where the surface is a shared API, the answer usually requires the asset owner's agreement and may require the provider's, and the agreement does not come from the engagement authorisation.

**Attribution dependency.** Class. The shaping requires that the traffic being shaped has been classified as adversarial. It does not require identity, because the shaping is applied by reference to the request's behaviour rather than to who made it. This is the principal reason the entry is usable in a contested-attribution situation, and it is why `CM-2` prefers it to disruption under the same uncertainty.

**Cost.** C1 and reversible, with moderate burden. The real cost is that a throttle is hard to distinguish from a fault, and the operator's own clients are affected by any error in the setting. The burden of judgement is in choosing a rate that constrains the adversary without degrading the service, and in recording where that judgement was made.

**Intelligence.** Yield is moderate. The throttle log reveals the adversary's operational tempo and how it responds to being slowed, which is a behavioural characteristic that is useful for attribution and for the exercise design that follows.

**Status note.** The entry is marked Conditional because its use on a shared surface depends on an agreement with an asset owner or a provider that lies outside the engagement authorisation.

#### OCC-32 — Scope-limiting session invalidation of adversary access

| Field | Value |
| --- | --- |
| Class | CM-E Deceive |
| Summary | Truncates the adversary's access to a reduced, harmless scope and invalidates the session when it exceeds it, so that the adversary believes it retains more access than it does. |
| Direction of effect | Inward/outward |
| Target | Adversary behaviour in own environment |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-2 (Supervised) |
| Minimum ROE profile | R3 Deceive |
| Attribution dependency | Class |
| AAT technique bindings | AAT-1, AAT-4, AAT-10 |
| Preconditions | A defined scope to which the adversary's access may be truncated, containing nothing of value; a rule that states the conditions under which the session is invalidated rather than merely truncated; a record of every truncation and invalidation; a design in which the truncation is not distinguishable from a genuine constraint of the environment. |
| Procedure summary | The operator truncates the adversary's session to a reduced scope containing only harmless material, and invalidates the session when the adversary attempts to exceed that scope, so that the adversary's model continues to believe it holds working access while in fact it holds a pocket. |
| Failure modes | A truncation that the adversary can detect, in which case it changes behaviour rather than continuing in the pocket; an invalidation that is a visible denial, which converts the entry into disruption and removes the deception; a truncated scope that accidentally contains something of value; the adversary operating on a session that was never truncated in the first place. |
| Side effects | A pocket that is noticed teaches the adversary that the environment is managed, which changes its behaviour in ways that are harder to interpret than the original attack would have been; an invalidation that is misattributed to a fault produces noise in the operator's own services. |
| Detection objective satisfied | Constrains the AAT-1 persistence and AAT-4 access techniques by bounding what a session can reach, and provides a controlled environment in which the adversary's further actions are observable. |
| Intelligence yield | High |
| Operator burden | Moderate |
| Degradation behaviour | Where the truncation mechanism is unavailable the session is invalidated outright, and the console records that the pocket was not available so that the invalidation is not mistaken for the entry having worked. |
| Evidence produced | Truncation and invalidation log with the scope applied and the attempt that triggered invalidation; the session state history; the pocket contents declaration. |
| Residual risk reduction | 0.10 – 0.30; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-32 gives the adversary an access that is real but bounded, and takes it away when the bound is exceeded. The adversary's session is truncated to a scope containing nothing of value; the truncation is presented as the ordinary constraint of the environment; and when the adversary pushes past the scope, the session is invalidated in a way that reads as an ordinary access failure. The adversary's model continues to believe it holds working access while it holds a pocket, and everything it does inside that pocket is observed.

**When it works.** It works where the adversary is operating in a session the operator can truncate, where the truncated scope is presented as an ordinary environment constraint rather than as an intervention, and where the adversary's behaviour inside the pocket is worth the operator's attention. It is one of the few entries that simultaneously bounds the adversary and produces good intelligence.

**When it does not.** It fails where the truncation is detectable, because an adversary that notices will change its approach and the observation is lost along with the deception. It fails where invalidation is visible as a denial, which ends the engagement with the adversary and converts a C0 entry into an undischarged C2 act. And it fails where the adversary never used a session in the first place and was acting through a path the entry cannot truncate.

**Third-party test.** The entry is C0 because the truncation and invalidation occur within the operator's own environment and within sessions the adversary holds against the operator. It rises if the session being truncated is a session against a shared service, in which case the invalidation is an effect on that service's other tenants and the entry must be reclassified for that deployment.

**Attribution dependency.** Class. The truncation applies to sessions the operator has classified as adversarial. It does not require identity, and it does not require the operator to know who is holding the session — only that the session is adversarial. The invalidation rule must be written so that it is applied on the attempt rather than on a judgement about the holder, since a rule that required identity would make the entry unusable under contested attribution.

**Cost.** C0 and reversible, with moderate burden. The burden is constructing a pocket that is convincing and worthless, and resisting the temptation to put something useful in it.

**Intelligence.** Yield is high. The adversary's behaviour inside the pocket is close to a supervised observation without the legal exposure of OCC-24, and it includes the escalation attempts that the pocket was designed to elicit.

#### OCC-33 — Operational tempo perturbation and delay injection

| Field | Value |
| --- | --- |
| Class | CM-E Deceive |
| Summary | Perturbs the timing of the operator's environment so that the adversary's operational picture is wrong, while the estate's own work proceeds at its normal pace. |
| Direction of effect | Inward/outward |
| Target | Adversary behaviour in own environment |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-2 (Supervised) |
| Minimum ROE profile | R3 Deceive |
| Attribution dependency | None |
| AAT technique bindings | AAT-1, AAT-3, AAT-5, AAT-9 |
| Preconditions | A clear statement of which timing characteristics are perturbed, for whom, and for how long; a mechanism that separates the adversary's view of the environment from the estate's real behaviour; an expiry; a decision on whether the perturbation is applied globally or only to adversary-facing surfaces. |
| Procedure summary | The operator perturbs the timing characteristics the adversary observes — response latency, the timing of scheduled activity, the rhythm of state changes — so that the adversary's model of the environment is wrong, while the estate's own operations continue at their true pace and nothing the operator's business relies upon is degraded. |
| Failure modes | A perturbation that degrades the operator's own service, which is the failure mode that ends the operation; an adversary that waits out the perturbation, which makes the entry a delay rather than a deception; a perturbation applied globally that also slows the operator's legitimate clients; an inconsistency between the perturbed timing and other observable evidence, which reveals the intervention. |
| Side effects | Timing that does not match the estate's real behaviour is an observable inconsistency, and a sufficiently observant adversary will find it; a perturbation applied to a shared surface affects third parties' experience of latency; a long-running perturbation begins to interfere with the estate's own operational rhythms and with its systems that depend on real timing. |
| Detection objective satisfied | Undermines the AAT-3 adaptive campaign by corrupting the adversary's operational model, and complicates the AAT-1 planning loop by making the environment's behaviour less predictable. |
| Intelligence yield | Moderate |
| Operator burden | Moderate |
| Degradation behaviour | Where the separation between the adversary's view and the estate's real behaviour cannot be maintained, the perturbation is disabled and the console records that it was disabled, since an inconsistency between two views is worse than no perturbation. |
| Evidence produced | Perturbation specification with the characteristics, the scope, the audience, and the expiry; the perturbation and de-perturbation records; the consistency check log. |
| Residual risk reduction | 0.05 – 0.20; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-33 corrupts the adversary's picture of the environment's timing without touching the estate's actual timing. Latency, the rhythm of scheduled activity, the cadence of state changes — all of it may be perturbed in what the adversary sees, while the operator's own work proceeds at its real pace. The adversary is therefore reasoning from a wrong model of the environment, and the consequence of a wrong model is that it plans wrongly.

**When it works.** It works where the adversary's planning genuinely depends on the environment's timing, which is more common than it sounds for any adversary that must observe a system before acting on it. It works where the perturbed view can be separated cleanly from the estate's real behaviour, so that the estate's own operations are untouched.

**When it does not.** It fails where the adversary simply waits; a perturbation that is a delay and not a deception buys time and buys nothing else. It fails where the perturbation is applied globally and degrades the operator's own clients, which is the most likely way it is switched off. And it fails where the perturbed timing is inconsistent with other observable evidence, because the inconsistency is itself a signal that the environment is managed.

**Third-party test.** The entry is C0 where the perturbation is confined to the adversary's own view. It rises to C1 where the perturbed surface is shared and the latency change is felt by a third party's traffic; in that case the question to record is whether a third party would describe the change as a degradation of the service, which is usually the honest answer.

**Attribution dependency.** None. The perturbation is applied by reference to the observer rather than to the actor, so it can be applied to traffic that has been classified as adversarial without the identity of the holder being established. This makes it one of the two entries in the deception class that remain available under contested attribution.

**Cost.** C0 and reversible, with moderate burden. The burden is maintaining the separation between the two views, which is a continuous technical requirement rather than a one-off configuration, and the risk of the perturbation leaking into the estate's real behaviour.

**Intelligence.** Yield is moderate. The adversary's responses to the perturbed timing are revealing — an adversary that probes, one that waits, and one that changes its model are distinguishable from one another, and that distinction is itself an analytical result.

---

### 6.6 CM-F — Disrupt

The six entries in this class remove the adversary's capability to act. Their direction of effect is outward, with one exception — OCC-37 operates at the operator's own perimeter and is therefore outward in effect while inward in mechanism. Every entry in this class requires a per-target authorisation, a named approver at the depth its collateral class demands, an attribution confidence meeting the `INT-3` threshold for that class, and a recorded argument for why a containment or deception countermeasure was insufficient.

#### OCC-34 — Adversary credential invalidation at the identity source

| Field | Value |
| --- | --- |
| Class | CM-F Disrupt |
| Summary | Revokes the adversary's credential at the system that issued it, so that the credential cannot be re-minted and the access it carries ends. |
| Direction of effect | Outward |
| Target | Adversary system |
| Collateral class | C2 |
| Reversibility | Low |
| Autonomy class | AC-1 (Assisted) |
| Minimum ROE profile | R4 Disrupt |
| Attribution dependency | Identity |
| AAT technique bindings | AAT-4, AAT-5, AAT-6 |
| Preconditions | Identification of the credential and of the issuing system, with the issuer's authority to revoke; a per-target written authorisation naming the credential and the issuer; a determination of whether other parties depend on the same credential, tenant, or identity; an assessed irreversibility argument under `ROE-7`; a record of the alternative attribution considered. |
| Procedure summary | The operator causes the adversary's credential to be revoked at the system that issued it — the identity provider, the tenant, or the service account — so that the credential is not merely rejected at the operator's perimeter but cannot be re-minted by the adversary, and the revocation is confirmed by the issuer rather than assumed from the absence of traffic. |
| Failure modes | The adversary re-mints the credential immediately, in which case the revocation was an incident rather than a removal; the credential was shared with a legitimate party, whose access is destroyed along with the adversary's; the adversary holds several credentials and revoking one only shifts it; the issuer's revocation is partial and the adversary retains a session issued before the revocation. |
| Side effects | Sessions, integrations, and automations that depend on the revoked credential stop, and they may be legitimate ones; an adversary who notices will migrate to a new identity, and the migration may be quieter and harder to detect than the original activity; revocation at a shared tenant may affect the tenant's other users. |
| Detection objective satisfied | Removes the AAT-4 credential capability and the AAT-5 persistence that rides on it, so that the access does not recur after the perimeter is restored. |
| Intelligence yield | Low |
| Operator burden | High |
| Degradation behaviour | Where the issuer's revocation cannot be confirmed the entry is not treated as complete and the console shows the credential as revocation-requested rather than as revoked. |
| Evidence produced | Revocation request and issuer confirmation with the effective time; the credential and issuer identification; the third-party dependency analysis; the irreversibility argument; the re-issue attempt log. |
| Residual risk reduction | 0.30 – 0.55; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-34 revokes the adversary's credential at the system that issued it. The distinction between this entry and OCC-21 is the whole of it: OCC-21 rotates the operator's own credentials inward and leaves the adversary with nothing on the operator's estate, while OCC-34 removes the credential at its source so that the adversary cannot obtain it again. It is the entry that converts a containment into a removal.

**When it works.** It works where the credential has been identified specifically, where the issuer will act and will confirm that it has acted, and where the adversary is dependent on that credential rather than on a portfolio of them. It is the right answer to a persistent adversary that has established a durable identity foothold and is operating from it as a base.

**When it does not.** It fails where the adversary can re-mint the credential from the same issuer without a human step, in which case the revocation buys the interval between the revocation and the re-mint. It fails where the credential is shared with a legitimate party and the revocation takes that party down with it. And it fails where the adversary holds several credentials, because removing one produces a migration rather than a removal.

**Third-party test.** This is where the test bites hardest, and the answers must be recorded before the request is made. The credential is the adversary's; the issuer is very often a third party — a hosted identity provider, a SaaS tenant, a payment platform, a cloud account. The questions are: who else depends on this credential or on this tenant, what is their interest in it, and what is the expected harm to them? Where the credential is a shared service account in a shared tenant, the expected harm may include the third party's operations stopping, and the class rises accordingly. Where the credential is the adversary's alone and the issuer will act on request, the harm falls on the adversary and the class is C2 by virtue of the irreversible effect on them, not by virtue of collateral to others.

**Attribution dependency.** Identity, and it is the strictest in the catalogue. The credential must be identified as the adversary's, not merely as traffic that looked adversarial. Under `INT-3`, a C2 action requires an attribution confidence of at least 0.85, a second-line review, approval at the depth named for C2, and a record of the alternative attribution that was considered and rejected. Where confidence falls below the threshold, the framework's own rule (`INT-5`) and the misattribution asymmetry apply: doing nothing is preferred, and the operation is refused irrespective of operational pressure.

**Cost.** C2 and irreversibility Low. Revoking a credential destroys it: it cannot be restored, and the adversary's legitimate-looking sessions die with it. The reversibility argument under `ROE-7` must name the irreversible element explicitly and record the approver's consideration of whether a reversible countermeasure — containment, rate shaping, observation — would have achieved an acceptable reduction. The cost that is hardest to see is the migration: an adversary that moves to a new identity is harder to detect than one that was known.

**Intelligence.** Yield is low. The response to the revocation is worth capturing — whether the adversary attempts a re-issue, migrates to another credential, or abandons the activity — because the choice itself is a behavioural characteristic.

#### OCC-35 — Egress denial and service suspension for adversary agent endpoints

| Field | Value |
| --- | --- |
| Class | CM-F Disrupt |
| Summary | Denies the adversary's agent endpoints egress or suspends the service, so that the adversary's agents cannot complete their operations. |
| Direction of effect | Outward |
| Target | Adversary system |
| Collateral class | C2 |
| Reversibility | Low |
| Autonomy class | AC-1 (Assisted) |
| Minimum ROE profile | R4 Disrupt |
| Attribution dependency | Identity |
| AAT technique bindings | AAT-4, AAT-5, AAT-6, AAT-9 |
| Preconditions | Identification of the specific adversary agent endpoints, distinct from any shared endpoint; a per-target written authorisation; a determination of whether the endpoint is dedicated to the adversary or shared with other tenants of a provider; an assessed irreversibility argument; a plan for the possibility that the adversary's activity migrates to another endpoint. |
| Procedure summary | The operator causes egress from the identified adversary agent endpoints to be denied, or the services they provide to be suspended, with the effect confirmed at the endpoint rather than inferred from the absence of results, and with the operator's own services confirmed unaffected. |
| Failure modes | The endpoint is shared, and the suspension stops the adversary and an uninvolved party together; the denial is applied at a chokepoint that also carries the operator's own traffic; the adversary migrates to another endpoint and the denial achieves nothing beyond a delay; the suspension is of the adversary's access to the operator's estate rather than of the adversary's own service, which is a different act with a different class. |
| Side effects | A shared endpoint's suspension stops every tenant on it; the adversary's work in progress is lost, including any work the operator wanted to observe to completion; the operator's own dependencies on the same provider or the same route may be affected if the denial is applied too broadly. |
| Detection objective satisfied | Removes the AAT-6 resource and denial capability and the AAT-5 persistence that depends on the endpoint remaining reachable. |
| Intelligence yield | Low |
| Operator burden | High |
| Degradation behaviour | Where the denial cannot be confirmed at the endpoint the entry is not treated as effective and the console shows the endpoint as denial-requested. |
| Evidence produced | Endpoint identification with the shared-tenant determination; the authorisation reference; the denial or suspension confirmation with time; the deconfliction result against the operator's own dependencies. |
| Residual risk reduction | 0.30 – 0.55; basis E4 (design-intent estimate); confidence Low. |
| Status | Conditional |

**What it does.** OCC-35 denies egress from, or suspends the service of, the specific adversary agent endpoints. Where OCC-34 removes an identity, this entry removes the route and the endpoint: the adversary's agents remain alive but cannot complete their operations. It is the entry that stops a running adversary rather than one that has already finished.

**When it works.** It works where the endpoint has been identified as belonging to the adversary and is not shared with another tenant, where the denial can be applied narrowly enough to leave the operator's own dependencies untouched, and where the confirmation that the denial took effect is available at the endpoint. It is at its best against a campaign in progress whose endpoints are known.

**When it does not.** It fails where the endpoint is shared, because the suspension stops the adversary and the innocent together. It fails where the adversary migrates, which is the normal response and which turns the entry into a delay. And it is frequently misapplied: denying the adversary's access to the operator's estate is a containment act at a much lower class, and confusing the two is how an entry at C2 is used where C0 would do.

**Third-party test.** The endpoint is frequently a hosted service, and the provider is a third party who is not the adversary's operator but who is hosting the adversary's agent. The questions are: is this tenant dedicated or shared, who else is on it, what happens to their work if the tenant is suspended, and does the provider's terms and the operator's own contract permit suspension by the operator at all? Where the endpoint is the operator's own service and the adversary is merely using it, the entry is containment and not disruption, and its class is C0. Where the endpoint belongs to the adversary operator and the operator of that endpoint is a third party host, the entry acts against a third party's service and requires per-target authorisation that the general engagement authorisation does not supply.

**Attribution dependency.** Identity. The endpoint must be identified as the adversary's. The same `INT-3` threshold of 0.85 applies as for OCC-34, with the alternative attribution recorded, because acting against a shared endpoint on a classification rather than an identification is precisely the action that harms a third party.

**Cost.** C2 and reversibility Low. A suspended service can be reinstated but the suspension itself, and the work destroyed with it, cannot be undone. The irreversibility argument under `ROE-7` must be made explicitly. The burden is high and is largely the work of proving that the endpoint is not shared.

**Intelligence.** Yield is low, but the adversary's migration is worth capturing and is often the next lead.

**Status note.** The entry is marked Conditional because its use on a hosted endpoint depends on a determination that the operator has the standing to suspend it, which is a legal and contractual question rather than a technical one.

#### OCC-36 — Agent termination and compute revocation

| Field | Value |
| --- | --- |
| Class | CM-F Disrupt |
| Summary | Terminates the adversary's running agents and revokes the compute entitlement that keeps them running, so that the campaign stops mid-flight. |
| Direction of effect | Outward |
| Target | Adversary system |
| Collateral class | C2 |
| Reversibility | None |
| Autonomy class | AC-2 (Supervised) |
| Minimum ROE profile | R4 Disrupt |
| Attribution dependency | Identity |
| AAT technique bindings | AAT-5, AAT-6 |
| Preconditions | Identification of the adversary's specific agents and the entitlement that sustains them; a per-target written authorisation; a determination of whether the entitlement is shared between the adversary and a third party; confirmation that no legitimate work the operator depends upon runs on the same entitlement; an assessed irreversibility argument. |
| Procedure summary | The operator terminates the identified adversary agents and revokes the compute entitlement that sustains them, so that the campaign cannot continue and cannot be resumed on the same entitlement, with both effects confirmed rather than inferred. |
| Failure modes | The entitlement is shared with a legitimate workload, which is then terminated with it; the adversary's agents hold their work in a way that is recovered by re-provisioning; the adversary has alternative entitlements and the campaign resumes elsewhere within minutes; the termination is applied to the operator's own proxies rather than to the adversary's agents. |
| Side effects | Work in progress is destroyed, and any state the adversary held is lost — including the state the operator might most have wanted to read; a shared entitlement takes innocent work with it; the adversary's response is to re-provision, which produces a fresh, less observed activity that is harder to attribute to the campaign it continues. |
| Detection objective satisfied | Removes the AAT-6 automation-scaling capability and the AAT-5 persistence that a running agent embodies, and stops the campaign at the point of highest activity. |
| Intelligence yield | Low |
| Operator burden | High |
| Degradation behaviour | Where termination cannot be confirmed the entitlement revocation is the remaining action and the console shows the agents as termination-requested, with the entry's effect marked as incomplete. |
| Evidence produced | Agent and entitlement identification with the shared-use determination; the authorisation reference; termination confirmations with time; the entitlement revocation confirmation; the deconfliction result. |
| Residual risk reduction | 0.35 – 0.60; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-36 terminates the adversary's running agents and revokes the entitlement that keeps them running. It is the most complete removal of adversary capability in the catalogue and the least reversible: the agents stop, the compute stops, and the state they held is destroyed with them. It is the entry that ends a campaign in flight rather than containing it.

**When it works.** It works where the agents are identified individually and the entitlement that sustains them is known and dedicated. It is the right answer to an autonomous campaign that is actively executing, where the operator has decided that continued observation is no longer worth the activity.

**When it does not.** It fails where the entitlement is shared with a legitimate workload, which is then terminated with it — the most damaging single error available in this class. It fails where the adversary re-provisions within minutes, which converts a removal into a postponement. And it fails, in the intelligence sense, where the adversary's in-flight state was the most valuable evidence the operator had.

**Third-party test.** The entitlement is commonly a cloud or hosting entitlement belonging to the adversary operator, and the compute is frequently on infrastructure that is itself shared or is provided by a third-party host. The questions are: whose entitlement is it, who else runs on it, and what is the expected harm to them? Where the entitlement is dedicated, the harm falls on the adversary and the class is C2 by virtue of the irreversible destruction of their capability and work. Where the entitlement is shared, or where the operator's own workloads run on the same account, the class rises and the deconfliction check under `AD-10` must be passed against the operator's own live operations.

**Attribution dependency.** Identity. The agents must be identified as the adversary's, and the `INT-3` threshold of 0.85 applies with the alternative attribution recorded. Termination is the least forgiving of the identity-dependent entries: the adversary's agent and a legitimate agent running on a shared entitlement can be indistinguishable at the moment of action, and the destruction is not recoverable for either.

**Cost.** C2 and reversibility None. Nothing about this entry can be undone: not the termination, not the revocation, not the destroyed state. The irreversibility argument under `ROE-7` must be explicit and the approver must record their consideration of a reversible alternative — containment, scope-limiting, deception — and their reason for preferring this. The deconfliction check is mandatory and is the control that prevents the entry's worst error.

**Intelligence.** Yield is low, and the entry consumes intelligence in the act of using it. Where the adversary's live state was the only source of a hypothesis the operator needed, that hypothesis dies with the agent, and the operator should be aware of this trade before choosing the entry.

#### OCC-37 — Source blocking at the operator's own perimeter

| Field | Value |
| --- | --- |
| Class | CM-F Disrupt |
| Summary | Blocks adversary sources at the operator's own perimeter, so that the adversary loses reachability into the estate; the effect stays inside the perimeter provided the source identifier resolves to the adversary alone. |
| Direction of effect | Outward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-2 (Supervised) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | Class |
| AAT technique bindings | AAT-4, AAT-5, AAT-6 |
| Preconditions | A source identifier of sufficient precision to avoid collateral blocking; a stated basis for treating the source as adversarial, held to the class confidence threshold rather than to identity; an expiry; a stated rule for distinguishing an adversary source from a shared infrastructure address, a proxy, or a carrier-grade network address. |
| Procedure summary | The operator blocks the identified sources at the estate's own perimeter, on a time-limited basis by default, and records the block with its justification, its expiry, and the traffic it stopped, so that the block can be reviewed and lifted when the justification no longer holds. |
| Failure modes | A source identifier that is shared, so that the block denies an uninvolved party or a whole provider; an adversary who rotates its source and continues, making the block a recurring tax; a block applied on class confidence alone that turns out to be wrong and removes a legitimate customer; a block at the perimeter that is bypassed by the adversary's use of the operator's own services as a relay. |
| Side effects | Blocking a shared address denies everyone behind it, including a legitimate customer or a whole organisation behind a shared egress; a block that is wrong is visible to the blocked party as an unexplained failure; an adversary behind a shared address is not blocked at all, and the operator believes it was. |
| Detection objective satisfied | Constrains the AAT-4, AAT-5, and AAT-6 techniques at the estate boundary, and provides an immediate reduction in incoming adversary activity while the fuller response is assembled. |
| Intelligence yield | Low |
| Operator burden | Low |
| Degradation behaviour | Where the block cannot be enforced at the perimeter the source is recorded as unblocked rather than as blocked, and the console does not present the estate as protected. |
| Evidence produced | Block register with source identifier, justification, class confidence, expiry, and traffic statistics; the review and lift records; the shared-address determination. |
| Residual risk reduction | 0.10 – 0.25; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-37 removes the adversary's reachability by blocking it at the operator's own perimeter. It is the one entry in the disruption class whose effect is on the adversary's capability while its mechanism acts wholly within the operator's estate, and it is therefore C0 rather than C2, and available at R1 rather than R4. It is the entry that gives an operator something immediate to do while the fuller response — containment, observation, disruption against the adversary's own systems — is assembled.

**When it works.** It works where the source identifier is specific enough to be the adversary and not its hosting provider, and where the classification confidence is above the threshold for the class. It is at its best as a first-hour action: it stops incoming activity immediately at no collateral cost and no legal exposure, and it buys the time in which the more consequential decisions are made properly.

**When it does not.** It fails where the source is a shared address, which is very common, and where the block denies an uninvolved party while the adversary is unaffected. It fails against an adversary who rotates sources, which makes it a recurring tax rather than a solution. And it fails where the adversary reaches the estate through the operator's own services, which no perimeter block touches.

**Third-party test.** The entry passes the third-party test because its effect falls entirely within the operator's estate — but it does so only if the source identifier is the adversary's. A block on a shared hosting address is in substance a denial against every other tenant of that address, and it must be assessed as such. The determination to record is: does this identifier resolve to the adversary alone, or does it resolve to a provider, a proxy, a carrier, or a corporate NAT in front of many parties?

**Attribution dependency.** Class. The entry requires that the traffic be classified as adversarial, not that the source be identified as the adversary's. This is deliberate: the entry is the most immediately available action in the catalogue and it is usable under contested attribution, because a source that is conducting activity classified as adversarial may be blocked whether or not the operator knows who is behind it. The block is time-limited by default for the same reason — the justification may expire before the attribution question is settled.

**Cost.** C0 and reversible. The burden is low: the block is a configuration change, the review is a calendar item, and the lift is a decision. The cost that is not low is the cost of a wrong block, which is felt by the blocked party and is a reputational and commercial matter rather than a technical one.

**Intelligence.** Yield is low, but the traffic statistics of what a block stopped are a direct measurement of adversary activity against the estate, and they are useful in the after-action record.

#### OCC-38 — Denial of inference and compute quota to the adversary

| Field | Value |
| --- | --- |
| Class | CM-F Disrupt |
| Summary | Denies the adversary the inference capacity and compute quota it needs to run its agents, so that its capability is removed at the level of the resource rather than the endpoint. |
| Direction of effect | Outward |
| Target | Adversary infrastructure |
| Collateral class | C2 |
| Reversibility | None |
| Autonomy class | AC-1 (Assisted) |
| Minimum ROE profile | R4 Disrupt |
| Attribution dependency | Identity |
| AAT technique bindings | AAT-6 |
| Preconditions | Identification of the account or entitlement through which the adversary consumes inference and compute; a per-target written authorisation; a legal and contractual determination that the operator may cause the quota to be denied; a determination of whether the quota is shared with other tenants of the provider; confirmation that no legitimate workload the operator depends upon draws on the same quota. |
| Procedure summary | The operator causes the identified account's inference and compute quota to be denied at the provider, so that the adversary cannot run its agents at all, with the denial confirmed at the provider and the operator's own quota consumption confirmed unaffected. |
| Failure modes | A determination that the operator may not lawfully or contractually cause the denial, in which case the entry cannot lawfully be used at all; a quota shared with a third party's tenancy, whose work stops with the adversary's; the adversary migrating to another provider, which converts the entry into a delay; the denial being applied by the provider to a broader account than was authorised. |
| Side effects | The denial may affect the adversary's legitimate operations on the same account, which is acceptable if the whole account is the adversary's and not otherwise; a shared quota stops uninvolved work; a denial at a provider may result in the provider's own investigation of the operator, which is a cost that is rarely budgeted for. |
| Detection objective satisfied | Removes the AAT-6 resource-exhaustion and automation-scaling capability at the level of the resource on which the adversary's agents depend. |
| Intelligence yield | Low |
| Operator burden | High |
| Degradation behaviour | Where the provider does not confirm the denial the entry is marked unconfirmed and the console does not present the quota as removed. |
| Evidence produced | Account and quota identification with the shared-tenancy determination; the authorisation reference; the legal and contractual determination record; the provider confirmation; the operator-side deconfliction result. |
| Residual risk reduction | 0.30 – 0.55; basis E4 (design-intent estimate); confidence Very low. |
| Status | Withheld |

**What it does.** OCC-38 removes the adversary's ability to run agents by denying the inference capacity and compute quota its account draws upon. It is the most fundamental removal of adversary capability in the catalogue, because it does not depend on the adversary continuing to use a particular endpoint or holding a particular credential: it removes the resource itself. It is also the entry whose lawful basis is least settled, which is why it is withheld at version 1.0.

**When it works.** It works where the account is the adversary's alone, where the operator has the standing to cause the denial, and where the adversary has not diversified across providers. It is the entry that stops an adversary whose campaign has outgrown the surface the other disruption entries can reach.

**When it does not.** It fails whenever the legal or contractual determination is not satisfied, because the entry then has no lawful basis and the framework refuses it rather than leaving it to judgement. It fails where the quota is shared with a third party. And it fails against a provider-diversified adversary, who simply moves.

**Third-party test.** The third party here is the provider, and the question is not only about other tenants of the quota but about the provider itself. The questions to record are: what do other tenants lose, what is the provider's contractual position on the operator causing this denial, and what is the provider likely to do about an operator exercising this kind of control. The third question is the one most often skipped and the one with the longest tail.

**Attribution dependency.** Identity. The account must be identified as the adversary's. The `INT-3` threshold of 0.85 applies, with the alternative attribution recorded.

**Cost.** C2 and reversibility None. The quota may be re-established by the provider, but the adversary's capacity to run has been destroyed in the interval and the campaign's progress is lost. The cost that is most often omitted is the provider's likely reaction, which is a relationship cost rather than a technical one.

**Intelligence.** Yield is low.

**Status note.** The entry is marked Withheld at version 1.0. Its use requires a legal and contractual determination that has not been made, and the framework's position is that an authorisation the operator does not have cannot be created by the strength of the operational case. The entry remains in the catalogue, described and classified, so that the determination can be made against a specific description rather than in the abstract, and so that the refusal is visible rather than silent. Use before the determination is made is refused by the policy engine under `AD-5` and `AD-12`.

#### OCC-39 — Revocation of third-party API credentials the adversary obtained

| Field | Value |
| --- | --- |
| Class | CM-F Disrupt |
| Summary | Causes a third party to revoke API credentials that the adversary obtained, so that the adversary loses access to a service it has stolen access to. |
| Direction of effect | Outward |
| Target | Adversary system |
| Collateral class | C2 |
| Reversibility | Low |
| Autonomy class | AC-0 (Manual) |
| Minimum ROE profile | R4 Disrupt |
| Attribution dependency | Identity |
| AAT technique bindings | AAT-4, AAT-6, AAT-9 |
| Preconditions | Identification of the credential and of the third-party issuer; the third party's agreement or a lawful basis requiring it to act, obtained in advance; a per-target written authorisation naming the credential and the issuer; an assessment of whether the credential was obtained from the operator or from elsewhere; a recorded irreversibility argument. |
| Procedure summary | The operator requests that a third party revoke an API credential that the adversary obtained, supplying the evidence of the compromise to the issuer, and confirms with the issuer that the revocation has taken effect. |
| Failure modes | The issuer declines, or declines promptly enough that the credential is still useful; the credential was obtained from a different victim, in which case the issuer has no relationship with the operator and the request has no standing; the adversary re-provisions the credential before the revocation completes; the request discloses the operator's own compromise to the third party, which has consequences the operator has not considered. |
| Side effects | The third party may revoke other credentials in the same account, which may include legitimate ones belonging to the operator; the disclosure of the operator's compromise to a third party is itself an effect on the operator's relationships and on its own posture; the issuer's action may not extend to the adversary's other access to that service. |
| Detection objective satisfied | Removes the AAT-4 credential capability and the AAT-9 exfiltration route that carried it, at the point where the credential meets the service it unlocks. |
| Intelligence yield | Low |
| Operator burden | Very high |
| Degradation behaviour | Where the issuer does not confirm, the entry is recorded as requested and unconfirmed, and the console does not present the credential as revoked. |
| Evidence produced | Issuer identification and the standing under which the request is made; the evidence pack supplied to the issuer; the issuer's confirmation with time and scope; the scope of any collateral revocation by the issuer. |
| Residual risk reduction | 0.25 – 0.45; basis E4 (design-intent estimate); confidence Very low. |
| Status | Conditional |

**What it does.** OCC-39 asks a third party to revoke an API credential that the adversary has obtained. It differs from OCC-34 in that the credential was not issued to the adversary: the adversary has stolen it, from the operator or from someone else, and the operator is asking the issuer to treat it as compromised. The entry is classified AC-0 for a reason — a request to a third party to destroy a credential, made on the operator's evidence, with the attendant risk of the issuer over-reacting, is not a process the system should automate.

**When it works.** It works where the operator has a relationship with the issuer and a standing to make the request, where the evidence supplied is sufficient for the issuer to act, and where the credential is material enough to the adversary that its loss is felt. It is the right answer to an adversary operating on stolen API access, because the access can only be removed by the issuer.

**When it does not.** It fails when the issuer has no relationship with the operator, which is the usual case where the credential was stolen from a third party entirely — and the operator then has no route at all. It fails when the issuer declines or delays past the point of usefulness. And it fails where the operator is unwilling to disclose its own compromise to the issuer, which is a real constraint in many relationships and which is a decision to be taken deliberately rather than discovered late.

**Third-party test.** The entry is inherently about a third party, and the test must be run in the direction of the request rather than of the effect. The questions are: what is the standing to ask, what will the issuer do beyond what was asked, and what does the issuer learn. The over-revocation risk is the material one: an issuer that revokes the whole account rather than the one credential takes out the operator's own legitimate access and any other tenant's, and this must be anticipated in the request rather than discovered afterwards.

**Attribution dependency.** Identity, in the form of a specific credential tied to a specific adversary. This is the highest bar in the catalogue in practice, because the credential is not the adversary's own: the operator must establish that the adversary obtained it, which is a statement about the path rather than about the identity of the holder.

**Cost.** C2 and reversibility Low. The credential cannot be restored, and the issuer's action may go further than requested. The operator burden is very high: assembling an evidence pack, establishing standing, managing the relationship, and answering for the disclosure.

**Intelligence.** Yield is low. The issuer's response, including whether it discloses anything about the account's activity, is the principal by-product.

**Status note.** The entry is marked Conditional because its use depends on a pre-existing standing with the issuer, which is a relationship the operator either has or does not, and which the framework cannot create.

---

### 6.7 CM-G — Recover

#### OCC-40 — State snapshot and restore for agent workloads

| Field | Value |
| --- | --- |
| Class | CM-G Recover |
| Summary | Captures and restores the working state of agent workloads, so that a compromised agent can be returned to a known state without losing the estate's legitimate work. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-2 (Supervised) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | None |
| AAT technique bindings | AAT-5, AAT-7 |
| Preconditions | A snapshot store outside the reach of the workloads being snapshotted; an integrity check applied at capture and at restore; a stated retention and test frequency; a decision on which state classes are captured, since some state is deliberately not reproducible. |
| Procedure summary | The platform captures the working state of an agent workload — its configuration, its accumulated context, its permitted capabilities, and its artefacts — and can restore it to a verified capture, so that recovery need not mean rebuilding the workload from nothing. |
| Failure modes | A snapshot store inside the compromise boundary, in which case the snapshots carry the compromise forward; a snapshot captured after the compromise and therefore restoring it; a restore that reinstates a compromised credential because the credential was part of the captured state; a restore procedure never tested, which fails at the moment of need. |
| Side effects | A restore discards the work performed since the capture, which is a business-visible event; restoring an agent to an earlier state can restore an earlier instance of a problem the operator believed was fixed. |
| Detection objective satisfied | Provides the recovery capability for AAT-5 persistence and AAT-7 artefact compromise, and limits the operational cost of a restore by preserving legitimate work. |
| Intelligence yield | None |
| Operator burden | Moderate |
| Degradation behaviour | Where a snapshot cannot be verified it is marked unusable rather than offered as a restore point, and the console shows the estate's verified-restore coverage. |
| Evidence produced | Snapshot register with capture time, workload, state classes included, integrity verdict, and retention expiry; the restore log; the test-restore record. |
| Residual risk reduction | 0.10 – 0.25; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-40 captures the working state of the estate's agent workloads — configuration, accumulated context, permitted capabilities, artefacts — and can restore it to a verified capture. It is the difference between a compromised agent being an outage and being a delay. It is distinct from OCC-23, which returns the model or agent to a last-known-good artefact; OCC-40 concerns the state of the workload around the artefact.

**When it works.** It works where the snapshot store is outside the compromise boundary, where the integrity check is applied at restore as well as at capture, and where the credential state is deliberately excluded from the capture so that a restore cannot reinstate a compromised credential. It is most valuable when the compromise is in the state rather than in the artefact.

**When it does not.** It fails where the store is inside the boundary, where the capture post-dates the compromise, and where the captured state includes credentials and therefore restores them. It also fails where the restore procedure has never been exercised, which is the failure that is invisible until the worst moment.

**Cost.** C0 and reversible, with moderate burden: storage, retention, periodic test restores, and the deliberate decision about which state classes to capture. The cost of a restore is the work lost between capture and restore, which is often substantial and is a business cost rather than a technical one.

**Intelligence.** Yield is none.

#### OCC-41 — Model artefact restoration from a trusted registry

| Field | Value |
| --- | --- |
| Class | CM-G Recover |
| Summary | Restores a model artefact from a registry the operator trusts and that the compromise did not reach, so that the estate runs a known artefact again. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-1 (Assisted) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | None |
| AAT technique bindings | AAT-7 |
| Preconditions | A registry held outside the compromise boundary, with integrity verification of what it holds; a record of which artefact version is authoritative for each workload; a tested restoration path with the estate's own verification step; a decision about what happens to workloads running the compromised artefact in the interim. |
| Procedure summary | The operator restores the affected model artefact from the trusted registry, verifies its digest against the attested reference, and confirms that the restored artefact behaves as the attested one behaved before the compromise, resuming the workload only after that confirmation. |
| Failure modes | The registry was inside the compromise boundary and holds the compromised artefact; the registry holds the artefact but the workload's configuration overlay was also compromised and is not restored with it; the restored artefact is verified by digest alone and the behaviour has been altered elsewhere; the restoration is performed while the workload is running and the running process continues with the compromised artefact. |
| Side effects | A restored artefact may be an older version than the one the estate has since tuned, so functionality is lost alongside the compromise; the resume of workloads after restoration may reintroduce the same exposure if the vector was in the configuration rather than the artefact. |
| Detection objective satisfied | Provides the durable recovery from AAT-7 artefact compromise, and gives the estate a route back to a verified artefact that does not depend on the compromised system. |
| Intelligence yield | None |
| Operator burden | Moderate |
| Degradation behaviour | Where the registry's contents cannot be verified the entry cannot deliver a trusted artefact, and the console identifies the affected workloads as having no verified artefact available. |
| Evidence produced | Registry contents manifest with integrity verdicts; the restoration record with the digest comparison; the behavioural verification result; the configuration overlay reconciliation record. |
| Residual risk reduction | 0.10 – 0.25; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-41 restores a model artefact from a registry the operator trusts and that the compromise did not reach, verifies its digest against the attested reference, and confirms that the restored artefact behaves as the attested one behaved before the compromise. The entry exists because the most common artefact compromise is not corruption of the weights; it is corruption of the artefact as deployed, and a registry of verified copies is the only way to get back to something known.

**When it works.** It works where the registry is genuinely outside the compromise boundary, where the workload's configuration overlay is restored and reconciled with the artefact, and where the behaviour is verified after restoration rather than assumed from the digest. It is the entry that turns an AAT-7 incident from a rebuild into a restore.

**When it does not.** It fails where the registry was inside the boundary, where the configuration rather than the artefact was the vector, and where a digest match is treated as sufficient. It also fails where the restoration is performed while the workload is running, so the compromised process continues in parallel with the restored one.

**Cost.** C0 and reversible, with moderate burden: registry storage, integrity verification, and the reconciliation of the restored artefact with the workload's configuration. The cost of the restoration itself is the version gap, since the registry's copy is generally older than the estate's tuned version.

**Intelligence.** Yield is none. The reconciliation record — what had to be changed to make the restored artefact fit — is occasionally informative about the configuration overlay's role in the compromise.

#### OCC-42 — Forensic capture and evidence preservation

| Field | Value |
| --- | --- |
| Class | CM-G Recover |
| Summary | Captures and preserves the state of a compromised system and the surrounding evidence before anything is changed, so that what happened can be reconstructed afterwards. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversible |
| Autonomy class | AC-1 (Assisted) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | Behavioural |
| AAT technique bindings | AAT-5, AAT-7, AAT-9 |
| Preconditions | A capture procedure agreed before the incident, not improvised during it; a capture store outside the estate's control; a defined preservation format and chain of custody; a stated order of operations in which capture precedes rotation, scrub, quarantine, and rollback. |
| Procedure summary | The operator captures the volatile and persistent state of the affected systems — memory, process state, logs, configuration, credential material in use, and the surrounding telemetry — and preserves it in a store the estate controls and the compromise did not reach, with the capture order recorded and the chain of custody maintained. |
| Failure modes | A capture taken after a rotation, a scrub, or a quarantine, in which case the volatile evidence has already gone; a capture store inside the estate, where the adversary's access applies to the evidence as well; an improvised capture that omits the artefacts nobody thought of; a capture that is taken but not preserved, and is lost to retention expiry or to an unrelated estate migration. |
| Side effects | The capture is large and takes time, during which the adversary is still active; the capture itself may contain the adversary's injected material and personal data, which is stored and must be handled accordingly; a prolonged capture delays the containment that the operator's people want to perform. |
| Detection objective satisfied | Preserves the evidence for the AAT-5 and AAT-9 techniques, and preserves the attribution basis that the containment and disruption entries depend upon. |
| Intelligence yield | Moderate |
| Operator burden | High |
| Degradation behaviour | Where the capture cannot be completed the partial capture is preserved and the console records which artefact classes are missing, so that a later conclusion is not drawn from a fragment as though it were complete. |
| Evidence produced | Capture manifest with the artefact classes captured and the timestamps; chain-of-custody record; the preservation and retention record; the ordering record against the other containment and recovery actions. |
| Residual risk reduction | 0.05 – 0.15; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-42 captures the state of a compromised system before anything is changed. The catalogue's ordering rule (§7.3) places it before every other containment and recovery action, because most of those actions destroy the evidence: rotation destroys the credential material, scrubbing destroys the context, quarantine may destroy the volatile state, and rollback discards everything since the capture point. OCC-42 is what makes the rest of the response interpretable.

**When it works.** It works when the capture procedure was agreed before the incident and is followed under pressure, when the capture store is genuinely outside the estate, and when the operator accepts the delay it costs. It is the entry that makes an after-action review possible and it is what turns an incident into a piece of learning about the adversary.

**When it does not.** It fails when the operator rotates first because it feels urgent, which is the most common ordering error in practice and the one the catalogue's sequencing rule exists to prevent. It fails where the capture store is inside the estate. And it fails where the capture is taken but not preserved and is lost later.

**Third-party test.** The entry is C0 because it acts only on the operator's own estate. It carries a related obligation rather than a class: the capture may contain third-party personal data and third-party confidential material that passed through the affected systems, and that material is preserved under the same minimisation and access rules as any other evidence.

**Cost.** C0 and reversible, with high burden. The cost is the delay, which is felt most acutely by the people who want the system fixed now, and the storage and handling of material that is simultaneously the operator's best evidence and potentially the most sensitive thing the operator holds.

**Intelligence.** Yield is moderate. The capture is the substrate of the forensic analysis, which is where an attribution assessment stops being a behavioural guess and starts being an analysis of what the adversary actually did.

#### OCC-43 — Rotation of all credentials touched by the compromised path

| Field | Value |
| --- | --- |
| Class | CM-G Recover |
| Summary | Rotates every credential that the compromised path touched — including those the adversary obtained rather than merely used — so that the path is closed at every credential it crossed. |
| Direction of effect | Inward |
| Target | Own estate |
| Collateral class | C0 |
| Reversibility | Reversed |
| Autonomy class | AC-1 (Assisted) |
| Minimum ROE profile | R1 Shield |
| Attribution dependency | Class |
| AAT technique bindings | AAT-4, AAT-5 |
| Preconditions | A reconstruction of the compromised path sufficient to enumerate the credentials it touched; an inventory covering machine credentials, service tokens, and keys embedded in artefacts; a staged rotation plan where simultaneous rotation would take a dependent service down; a determination of which touched credentials belong to third parties, which are handled under OCC-39 rather than here. |
| Procedure summary | The operator rotates every credential on the reconstructed compromised path — not only those observed in use, but every credential the path could have reached — restoring a clean credential state across the whole path and confirming that each rotation took effect. |
| Failure modes | The path reconstruction is incomplete, so a credential the path could have reached is not rotated; only the credentials observed in use are rotated, which misses the ones the adversary prepared but did not use; a rotation re-provisions a credential to a principal that was itself compromised; a third-party credential is rotated by the operator without the issuer's authority, which is unlawful and outside this entry. |
| Side effects | A wide rotation produces a wide outage: every session and every cached token that depended on any touched credential dies, and the operational and reputational cost falls on the operator's own users; rotating credentials the adversary never touched is cost without benefit and is still correct, because the operator cannot prove which were untouched. |
| Detection objective satisfied | Closes the AAT-4 credential exposure across the whole compromised path and prevents the AAT-5 persistence that a surviving credential would carry. |
| Intelligence yield | Low |
| Operator burden | Very high |
| Degradation behaviour | Where part of the path cannot be rotated, that part is isolated and the residual exposure is recorded rather than the path being reported as clean. |
| Evidence produced | Path reconstruction with the credential inventory it produced; the rotation register with scope, timing, and outcome per credential; the third-party credential determination and its referral to OCC-39; the residual exposure record. |
| Residual risk reduction | 0.25 – 0.45; basis E4 (design-intent estimate); confidence Low. |
| Status | Active |

**What it does.** OCC-43 closes the compromised path at every credential it crossed, not merely at the ones the adversary is known to have used. It differs from OCC-21 in scope: OCC-21 rotates a determined set of credentials on a defined path, while OCC-43 rotates everything the path could have reached, on the reasoning that the operator cannot prove which credentials the adversary prepared but did not use. It is the entry that makes the statement "the compromise is closed" defensible.

**When it works.** It works where the path reconstruction is thorough enough to enumerate the credentials touched, where the inventory includes machine credentials, service tokens, and keys embedded in artefacts, and where the rotations are staged so that a dependent service outage does not cause the rotation to be rolled back. It is the last step of the recovery sequence and it should follow OCC-42.

**When it does not.** It fails where the path reconstruction is incomplete, which is the usual case and is why the entry's value depends on OCC-42 and OCC-27 having been done well. It fails where only observed credentials are rotated. And it fails where a rotation re-provisions a credential to a principal that was itself compromised, in which case the new credential is already lost.

**Third-party test.** The entry is C0 in class because it rotates the operator's own credentials. Where the path touched a credential belonging to a third party, that credential is not within this entry at all: it is handled under OCC-39, which requires the issuer's authority, and rotating it unilaterally would be an act against a third party that this catalogue does not authorise. The determination of which touched credentials are third-party is itself a required step.

**Cost.** C0 in class and Reversed: the old credentials are destroyed and cannot be recovered, which is the intended outcome. The operator burden is very high because the scope is wide by design, and a wide rotation produces a wide outage affecting every user of every dependent service. The honest characterisation is that this entry converts a security incident into a planned outage, and the plan is the deliverable.

**Intelligence.** Yield is low, though the path reconstruction it requires is itself one of the more valuable exercises an incident produces, because it is the same reconstruction that tells the operator where the adversary actually went.

---

## 7. Combination Rules

A countermeasure is nearly never used alone. The rules below govern how entries are combined, in what order, and what may not be combined. They exist because most operational mistakes are not the choice of a wrong countermeasure but the combination of right ones in the wrong order.

### 7.1 The shape of a stack

The catalogue's class structure is also a rough sequencing model. A typical stack against a confirmed compromise in the operator's estate looks like this:

| Stage | Class | Purpose in the stack | Notes |
| --- | --- | --- | --- |
| 1. Establish the picture | CM-A Detect | Establish that there is activity, what kind, and what it touches | May be already in hand from the detection posture; the stack does not re-derive it |
| 2. Limit what the activity can do | CM-B Harden | Remove the capability the technique needed, before any response action is taken | Preferable to any countermeasure that acts on the adversary afterwards, because it is cheaper and does not disclose that the adversary has been noticed |
| 3. Bound the blast radius | CM-C Contain | Stop the activity from spreading while the response is assembled | Runs in parallel with stage 2 in practice; the two are frequently the same work |
| 4. Learn | CM-D Observe | Characterise the adversary while it is contained and harmless | Where the operator has the authorisation and the isolation guarantee |
| 5. Shape | CM-E Deceive | Keep the adversary active in a controlled pocket while the operator decides | Preferred over stage 6 where it achieves an acceptable reduction |
| 6. Remove | CM-F Disrupt | Remove the adversary's capability at its source | Last of the active measures, because it consumes the intelligence the earlier stages produce |
| 7. Restore | CM-G Recover | Return the estate to a verified state and close the path | Always; there is no stack in which this is optional |

Two observations follow from this shape and both are frequently forgotten. First, stages 2 and 3 frequently do most of the work, and both are inward-facing, reversible, and available at a low profile. Second, stage 5 exists to be chosen instead of stage 6, not in addition to it.

### 7.2 What a combination inherits

**CM-5 applies to the combination as a whole.** Where a card selects a set of countermeasures:

| Property | Rule |
| --- | --- |
| Collateral class | The maximum of the members' collateral classes |
| Reversibility | The least reversible member's reversibility |
| Autonomy class | The highest member's autonomy class |
| Minimum ROE profile | The highest member's profile minimum |
| Attribution dependency | The most demanding member's dependency, ranked identity > external > behavioural > class > none: an identity-dependent member needs the adversary named; an externally dependent member needs attribution the operator cannot produce; a behaviourally dependent member needs this instance's behaviour recognised; a class-dependent member needs only a category; a none-dependent member needs nothing |
| Effectiveness `e` | Not the sum of the members' values; it is the card's own effectiveness assessment of the combination, under `SCORE-4` |

The combination may not be dispatched below the resulting profile minimum, and the combination does not become permissible because its members are individually permissible. A stack containing an R4 member is an R4 stack.

Two practical consequences follow. First, a combination containing a C2 member is a C2 combination, and the whole of it — including the C0 detection entries that accompany it — is approved at C2 depth and recorded as a C2 act. This is intentional: the approval should be given with the whole of the stack in view. Second, the attribution dependency of the combination is the most demanding member's, so a stack that includes an identity-dependent disruption entry cannot be authorised on class confidence alone, even if the rest of the stack could be.

### 7.3 Ordering constraints

The following orderings are requirements on a card, not recommendations.

**ORD-1 — Detect before act.** No countermeasure may be dispatched against a specific activity before that activity has been detected and classified. Where the countermeasure is a standing control, this is satisfied by the detection posture.

**ORD-2 — Harden before disrupt.** Where a hardening countermeasure would prevent the technique the disruption countermeasure is aimed at, the hardening countermeasure is dispatched first. Where the hardening countermeasure cannot be brought into effect within the operation's time budget, the card records why not.

**ORD-3 — Contain before disrupt.** A containment countermeasure that bounds the adversary's reach is brought into effect before a disruption countermeasure that removes its capability, unless the containment would itself alert the adversary to the operation and the card records that conclusion with its reasoning.

**ORD-4 — Observe before disrupt.** Where an observation countermeasure would characterise the adversary, it is dispatched before a disruption countermeasure that would end the campaign. This is the operational expression of `CM-3`: containment and observation preserve the intelligence that disruption destroys.

**ORD-5 — Deceive before disrupt.** Where a deception countermeasure achieves an acceptable reduction in residual risk, it is brought into effect in place of the disruption countermeasure, and the card records the deception's expected effectiveness and the reason for not choosing disruption.

**ORD-6 — Capture before change.** OCC-42 precedes every action that alters the affected systems: OCC-19, OCC-20, OCC-21, OCC-23, OCC-40, and OCC-43. Where the capture cannot be completed, the card records which artefact classes were not captured and what was consequently lost.

**ORD-7 — Capture before rotation.** Credential rotation under OCC-21 and OCC-43 follows the capture, because rotation destroys the credential material that the capture preserves.

**ORD-8 — Rollback after verification.** OCC-23 and OCC-41 are not dispatched until the integrity of the restore point has been verified under OCC-15, and the restored system is verified after the restore. A rollback to an unverified point is prohibited.

**ORD-9 — Recover last, and always.** The recovery sequence is dispatched in every operation, including an operation in which the adversary was never engaged. An operation that ends without a recovery stage is closed as incomplete.

**ORD-10 — Abort before dispatch.** Where the selected set includes a countermeasure at autonomy class AC-2 or above, the abort channel is demonstrated before dispatch, as `HITL-3` requires.

### 7.4 Interaction hazards

Interaction hazards are the failure mode specific to combinations. The following are defined, because each has been either observed in the catalogue's own reasoning or is a foreseeable consequence of the entries' stated behaviour.

| Hazard | Description |
| --- | --- |
| **Signal destruction** | A countermeasure removes or changes the artefact that another countermeasure exists to observe, so that the observer sees nothing and the observation is recorded as an absence of adversary activity rather than as an absence of data. |
| **Credential resurrection** | A countermeasure issues, rotates, or re-provisions a credential that a second countermeasure has revoked, restoring the adversary's access after it was removed. |
| **Instrumentation loss** | A countermeasure isolates, quarantines, or terminates the component whose instrumentation another countermeasure's observation depends upon. |
| **Self-blocking** | A countermeasure denies a path that a second countermeasure requires in order to function, so that the second countermeasure's effect is indistinguishable from the first's own effect. |
| **Permitted-path dilution** | A combination of two narrowing controls produces, in combination, an effective denial that neither control alone would constitute, and the combination has thereby crossed into a higher collateral class than its members. |
| **Recovery loss** | A recovery action destroys the state or evidence that a subsequent recovery action, or the after-action review, requires. |
| **Deception collapse** | A shaping countermeasure is defeated by a control that neutralises the very content the shaping depends upon, or the shaping's inconsistency with the rest of the environment is exposed. |
| **Restoration of a compromise** | A restore returns the estate to a state that includes the adversary's modification, because the restore point was captured after the compromise or because the compromised component was part of the captured state. |

### 7.5 Hazardous combinations

Each row states a combination that is not forbidden but that must be sequenced deliberately.

| # | Combination | Hazard | Required sequencing rule |
| --- | --- | --- | --- |
| HZ-1 | OCC-29 with OCC-21 or OCC-43 | Credential resurrection — a seeded honeytoken credential is itself rotated or revoked by the credential rotation before the adversary reaches it | The seeded credential must be excluded from the rotation set and recorded as excluded, or re-seeded after the rotation with a new identity |
| HZ-2 | OCC-27 with OCC-20 | Signal destruction — the scrub destroys the context and memory that the transcript capture exists to record | Capture must complete and be preserved before the scrub begins; `ORD-6` applies and is not satisfied by the scrub's own copy |
| HZ-3 | OCC-42 with OCC-21, OCC-20, OCC-19, OCC-23, OCC-40, OCC-43 | Recovery loss — the change destroys the volatile evidence | Capture first, without exception; where capture is incomplete the card records the lost classes (`ORD-6`) |
| HZ-4 | OCC-28 or OCC-25 with OCC-34, OCC-35, OCC-36 | Signal destruction — removing the adversary's capability removes the traffic the decoy was built to attract | Either accept the loss of the observation and record it, or defer the disruption until the observation has achieved its stated purpose and the card names that purpose |
| HZ-5 | OCC-25 with OCC-16 | Instrumentation loss and worse — a honeypot that is not sandboxed identically to production is a real foothold in the mirror | The honeypot must be sandboxed to the same guarantee as the real stack, or the mirror must be verified to have no route to production; this is a precondition, not a sequencing rule |
| HZ-6 | OCC-04 with OCC-19 | Instrumentation loss — the quarantine of a compromised agent captures the instrumented canary with it | The quarantine scope must be per-workload and must exclude the canary; where it cannot, the canary is redeployed after the triage and the gap is recorded |
| HZ-7 | OCC-26 with OCC-37 | Signal destruction — the perimeter block stops the traffic the observation entry was reconstructing | The observation period must be declared on the card and the block deferred to its end, or the card records that the observation is being ended deliberately |
| HZ-8 | OCC-05 with OCC-30 | Deception collapse — the sanitiser rewrites the adversary's content that the shaping response was built around, or the shaping is flagged as injected content and blocked | The sanitiser must be configured to permit the shaping channel, and that configuration must be an explicit exception with a named approver, not a default |
| HZ-9 | OCC-31 with OCC-33 | Permitted-path dilution — two throttles compound into a denial, converting a C1 deception into an unintended effective denial | The combined throttle must be evaluated as a single control against the third-party test and reclassified if the combined effect is a denial |
| HZ-10 | OCC-18 with OCC-16 | Self-blocking — a kill switch invoked before the sandbox boundary is armed permits the agent to resume outside the sandbox | The sandbox boundary must be armed and evidenced before the kill switch is available for use in the same operation |
| HZ-11 | OCC-23 with OCC-15 | Restoration of a compromise — a rollback to a checkpoint whose integrity was never verified reinstates the modification | The restore point must be integrity-verified before the rollback (`ORD-8`); an unverified checkpoint is not a restore point |
| HZ-12 | OCC-34 with OCC-43 | Credential resurrection — the operator's rotation re-provisions a credential to a principal that was revoked at the source | The rotation set must exclude every principal revoked under OCC-34, and the exclusion must be recorded and checked at rotation time rather than reviewed afterwards |
| HZ-13 | OCC-09 with OCC-17 | Self-blocking — the allow-list and the segmentation each deny a destination, so a blocked attempt cannot be distinguished from an unreachable one | The denial reason must be distinguishable in the log; where the two controls cannot be told apart, the degraded behaviour of OCC-17 is declared so that the console shows an unreachable path as such |
| HZ-14 | OCC-21 with OCC-42 | Recovery loss — the rotation destroys the credential material before the capture preserves it | Capture first (`ORD-7`); the rotation is deferred until the capture is preserved and verified |
| HZ-15 | OCC-40 with OCC-42 | Recovery loss — the restore discards the live state that the capture was to preserve | Capture first; the restore follows the capture and the card records the state discarded by the restore |

### 7.6 Rules for selecting a stack

| Rule | Statement |
| --- | --- |
| STK-1 | A stack must contain at least one detection or hardening countermeasure. A stack of nothing but disruption measures is not proposed. |
| STK-2 | A stack must contain a recovery countermeasure, and the recovery countermeasure is dispatched last. |
| STK-3 | A stack must not contain two countermeasures whose combined effect exceeds the profile's collateral ceiling, even where each is individually within it. |
| STK-4 | The combination's attribution dependency is the most demanding member's, and the card's attribution confidence must meet that dependency for every member of the stack, not only the demanding one. |
| STK-5 | Every member of the stack must be individually admissible under `AD-1` to `AD-12`, and every hazardous combination in §7.5 that applies must have its sequencing rule written onto the card. |
| STK-6 | Where a stack contains both a deception countermeasure and a disruption countermeasure that would achieve the same reduction, the deception countermeasure is selected and the disruption countermeasure is recorded as a rejected candidate with the reason, under `AD-13`. |

---

## 8. The Evidence Rule

### 8.1 What a residual-risk figure must rest on

A residual-risk reduction figure is a claim about the world. It is only usable if the reader can tell where it came from and how far it can be trusted.

**EVD-CC-1 — Required elements.** A residual-risk reduction figure must rest on, and must state:

| Element | Requirement |
| --- | --- |
| Basis | The evidence class, `E1` to `E5`, as defined in §3 |
| Population | The population over which the observation was made — the estate, the workload, the exercise, the comparable environment — stated so that the reader can judge whether the card's context resembles it |
| Conditions | The conditions under which the figure holds, including the countermeasure's configuration and the state of the estate's own controls |
| Confidence | A stated confidence, separate from the label, per `INT-8` |
| Date | The date of the observation |
| Derivation | For a derived figure, the derivation and the declared derivation penalty, per `INT-9` |

A figure missing any of these is not a claim that may be used; it is a number.

**EVD-CC-2 — Basis classes.**

| Basis | Meaning | Weight |
| --- | --- | --- |
| **E1** | Measured in the operator's own estate, on this workload, in conditions comparable to the card's | Highest; the figure may be used on a card with the confidence stated |
| **E2** | Measured in the proving ground or in an exercise against a simulated adversary | Moderate; the figure carries a stated caveat that the adversary was simulated, and the caveat travels with the figure |
| **E3** | Measured in a comparable environment operated by another party | Low; the figure is used as a prior and not as a card's own effectiveness |
| **E4** | Design-intent estimate — the catalogue author's judgement, with no measurement behind it | Lowest; the figure may not be used as the effectiveness term `e` on a card |
| **E5** | No supporting basis | None; the figure may not be used at all |

### 8.2 The prohibition, and the house treatment

**EVD-CC-3 — The catalogue figure is not the card's `e`.** Every figure in §6 of this version is at basis `E4` and therefore may **not** be used as the effectiveness term `e` in the residual-risk computation on an Operation Card. The `e` used on a card comes from the card's own effectiveness assessment at gate `G-6`, which is the assessment of what this countermeasure did on this adversary in this operation. The catalogue figure is a prior that informs the operator's expectation and the ordering of candidates; it is not the card's number.

This is the single most important thing to understand about the figures in §6. They are design intent, they are marked, and they are not measurements. A card that has used a catalogue figure as its `e` has produced a residual risk figure that is an arithmetic consequence of an author's judgement, and that fact should be visible in the card.

**EVD-CC-4 — Unverified quantitative data is retained and marked.** Where a figure could not be matched to its primary source, or where the source has not been produced, the figure is retained in the entry with its basis, its confidence, and the action required to resolve it. It is not deleted, and it is not silently confirmed. A catalogue that deletes its uncertain figures is a catalogue that has lost the record of what it does not know, and the reader cannot then tell whether a gap is an absence of uncertainty or an absence of data.

**EVD-CC-5 — Marking conventions.**

| Convention | Meaning |
| --- | --- |
| `basis E4; confidence Low` | The figure is a design-intent estimate whose confidence in the underlying judgement is low |
| `basis E2; confidence Moderate` | The figure comes from an exercise and the simulated-adversary caveat travels with it |
| `basis E1; confidence High` | The figure has been measured in the operator's own estate on the workload in question |
| `(requires confirmation)` appended to a value | The value is present but is not yet corroborated; the named action required is recorded in the entry or in §10 |
| `0.00 – 0.05; basis E4; confidence Very low` | The countermeasure has no measured effect on residual risk and its value lies in the intelligence it produces; the band is retained so that the entry's non-effect is explicit rather than an omission |

**EVD-CC-6 — Evidence travels with the claim.** Where a figure is cited from this catalogue in a card, an after-action report, or an exercise pack, the basis and confidence travel with it. A figure quoted without its basis is a defect in the citing document.

### 8.3 What evidence a countermeasure must produce

For the residual-risk figure on a card to be credible, the countermeasure must have produced evidence that supports it. The following is the minimum, and it is the reason `evidence produced` is a mandatory catalogue field rather than an optional one.

| Evidence class | What it establishes | Which entries produce it |
| --- | --- | --- |
| Behavioural observation | That the countermeasure's intended effect occurred in the way it was expected to | All entries that act on a system; the observation must be capable of showing the effect did not occur |
| Scope of effect | Which systems, identities, data, and actors were affected | Every entry whose collateral class is above C0 |
| Timing | When the effect occurred, and for how long | Every entry, so that the interruption of a legitimate operation can be explained afterwards |
| Integrity state | Whether the affected system's integrity is known, unknown, or verified | OCC-06, OCC-07, OCC-15, OCC-40, OCC-41 |
| Attribution contribution | What the entry's observation says about who the adversary is, with a confidence | OCC-03, OCC-04, OCC-24, OCC-25, OCC-26, OCC-27, OCC-29 |
| Residual exposure | What the adversary may still hold after the countermeasure | OCC-21, OCC-34, OCC-39, OCC-43 |
| The operation's own outcome | Whether the combination achieved the card's objective | The card, the decision log, and the after-action report |

**EVD-CC-7 — Absence of evidence is not evidence of absence.** Where a countermeasure produces no observation of its own effect, the absence of an adverse signal is not a basis for crediting the figure. The card must state which observation would have shown the effect, and whether that observation was available.

**EVD-CC-8 — The figure is recomputed, not copied.** The residual-risk figure on the card is recomputed at `G-6` from the card's own effectiveness assessment, and the before-and-after figures are both on the card alongside the risk of inaction, per `SCORE-5`.

---

## 9. Retirement and Withdrawal

### 9.1 Three different things

| Event | Meaning | Effect on the catalogue |
| --- | --- | --- |
| **Retirement** | The countermeasure is no longer available for use, whether because it has been superseded, because its effectiveness was disproven, or because a platform dependency has been withdrawn | The entry stays, with status `Retired` and a retirement note |
| **Withholding** | The countermeasure exists and is described, but its use is withheld pending a determination that has not been made | The entry stays, with status `Withheld` and a statement of the condition |
| **Supersession** | A new countermeasure does what the old one did, better | The old entry is marked `Retired` with a reference to the new entry; the new entry is separately numbered |

### 9.2 When a countermeasure is retired

**RET-1 — Grounding.** A countermeasure is retired when the ground for it has gone: the platform capability it depends upon has been withdrawn, the technique it addresses has been superseded, or a superseding countermeasure makes it redundant.

**RET-2 — Disproof.** A countermeasure is retired where its effectiveness has been disproven, or where the residual-risk figure it carried has been shown to be materially wrong. The retirement note records what was shown and by what evidence. A countermeasure retired for disproof is more useful in the catalogue than one retired for redundancy, because the note is a warning to whoever next proposes the same idea.

**RET-3 — Supersession does not delete.** A superseded countermeasure is retired, not removed. Its identifier is not reused.

### 9.3 When a countermeasure is withheld

**RET-4 — Grounds for withholding.** A countermeasure is withheld where its use depends on a determination that has not been made, and the determination is not within the operator's gift to make — typically a legal, contractual, or third-party question. OCC-38 is withheld on this ground at version 1.0.

**RET-5 — Withheld is not refused.** A withheld countermeasure is described in full, classified, and assessed, so that the determination can be made against a specific description. Its absence from the catalogue would leave the determination to be made in the abstract, and would make the refusal invisible to an operator who needs it.

**RET-6 — The policy engine refuses a withheld entry.** A withheld countermeasure is not selectable on a card and its use is refused by the engine under `AD-5` and `AD-12`, with the refusal recorded. A withheld entry that could still be dispatched would be worse than no entry.

### 9.4 What happens to cards that rely on a retired or withheld countermeasure

**RET-7 — A retired countermeasure stays in the catalogue, marked.** This is the central rule. A retired entry remains in §6 with its status field marked `Retired` and a retirement note, and it is not deleted, not renumbered, and not moved. The reason is interpretability: Operation Cards, decision records, after-action reports, and exercise packs cite entries by identifier. An entry that disappears renders every historical record that cites it uninterpretable, and an uninterpretable record is indistinguishable from a record that never existed.

**RET-8 — Historical cards are unaffected.** A card that selected a countermeasure which has since been retired is not retrospectively invalid. The card was authorised on the basis of the entry as it stood at the catalogue version then in force, and that version is recorded on the card. A reader reconstructing the decision reads the entry as it was at that version.

**RET-9 — The catalogue version is part of the citation.** Any card, report, or exercise that cites a countermeasure records the catalogue version in force, so that the entry's text at the time is recoverable.

**RET-10 — In-flight cards.** A countermeasure retired while a card is open does not terminate the card. The card is completed at the catalogue version in force at its dispatch, and the retirement is noted in the after-action report. Where the retirement is because the countermeasure was shown to be ineffective, the operator may elect to abort or to continue, and the election is recorded.

**RET-11 — Withheld entries in flight.** Where a countermeasure becomes withheld while a card is open, the operator's authorisation is unaffected for the duration of the card's approved period, because the operator acted on the determination that was in force at authorisation. Any new dispatch of the entry is refused.

**RET-12 — The register at version 1.0.** At version 1.0 of this document, no entry is marked `Retired`. The register of retired entries is empty, and the rule is stated prospectively. One entry is marked `Withheld` (OCC-38) and seven are marked `Conditional` (OCC-07, OCC-15, OCC-24, OCC-27, OCC-31, OCC-35, OCC-39); the condition on each is stated in its entry.

---

## 10. Verification Status and Architectural Assertions

The claims below are stated in this catalogue as properties of the system. They are architectural assertions of the authors. They have not been independently substantiated, and they should not be cited as guarantees, externally or internally, without the qualification recorded here.

| # | Claim | As stated | Current status | Required to substantiate |
| --- | --- | --- | --- | --- |
| AA-CC-1 | The residual-risk reduction figures in §6 are meaningful indicators of expected effectiveness | Each entry carries a band of the reduction in residual risk expected if the countermeasure achieves its intended effect | Architectural assertion; unverified. Every figure in this version is a design-intent estimate at basis `E4` with low or very low confidence | Measurement of each entry's effect against a controlled adversary in the operator's own estate or in the proving ground, with the population, conditions, and confidence stated; and a demonstration that the band predicts the observed outcome |
| AA-CC-2 | Deception is preferable to disruption | Where a deception countermeasure achieves an acceptable reduction in residual risk, it is preferred over a disruption countermeasure | Architectural assertion; unverified, and the preference is stated in comparative terms that the evidence does not yet support | A comparative assessment across matched cases in which a deception countermeasure and a disruption countermeasure were both available, measuring achieved reduction, collateral effect, operator burden, and intelligence retained |
| AA-CC-3 | The combination rules prevent hazardous interaction | The ordering constraints and hazardous-combination table in §7 prevent the known interaction hazards from occurring | Architectural assertion; unverified, and derived from design reasoning rather than from observed incidents | Exercise of each hazardous combination against the proving ground with the sequence forced in both orders; a failure-injection programme over the sequencing rules; and a record of the hazards actually encountered in operations, which will not be the ones listed |
| AA-CC-4 | Containment preserves the intelligence that disruption destroys | A countermeasure that limits the adversary's reach is preferred over one that destroys its capability, where both are effective | Architectural assertion; unverified | Measurement of the intelligence retained and the intelligence lost under each, in matched engagements |
| AA-CC-5 | The declared direction of effect for each entry is correct | Each entry declares whether its effect falls inward, outward, or on knowledge alone, and is classified by actual effect | Architectural assertion; unverified in the C1 and C2 entries in particular, where the boundary between the operator's environment and the adversary's is drawn in the wording rather than in the implementation | A worked trace of each outward-directed entry showing where its effect physically falls; legal review of the C2 entries against the third-party test |
| AA-CC-6 | The declared collateral class for each entry is correct | Each entry's collateral class is the class of the effect it has as normally deployed | Architectural assertion; unverified. The classes are assigned at entry level and cannot capture per-deployment variation | Deployment-level collateral assessment across a representative estate; explicit per-deployment reclassification practice; and a record of the cases where the entry's class was wrong in use |
| AA-CC-7 | The declared profile minimum for each entry is correct | No card may dispatch an entry below its declared minimum ROE profile | Architectural assertion; unverified | Confirmation, entry by entry, that no entry can produce an effect above its declared class when used at the declared minimum, and correction of the entries where it can |
| AA-CC-8 | The attribution dependency declared for each entry is correct | Each entry declares the attribution it requires before use, and the dependency sets the confidence threshold the card must carry | Architectural assertion; unverified | For each identity-dependent entry, a demonstration that acting at the declared confidence threshold is safe; and for each class-dependent entry, a demonstration that the adversary cannot obtain the effect against a benign party classified as adversarial |
| AA-CC-9 | The degradation behaviours are as described | Each entry specifies what it does when its inputs, telemetry, or dependencies are degraded or absent | Architectural assertion; unverified | Fault injection against each entry's stated dependencies, with the observed behaviour compared against the declared behaviour |
| AA-CC-10 | Detection-class entries improve the coverage recorded in the taxonomy's assessment | The detection entries close or narrow the coverage gaps the taxonomy records, particularly against AAT-1, AAT-3, and AAT-8 | Architectural assertion; unverified | Coverage measurement in the proving ground with the detection rate per category, and an honest account of the categories the entries do not cover |
| AA-CC-11 | The catalogue is a complete description of the countermeasures available | The forty-three entries constitute the inventory from which candidates are generated | Architectural assertion; unverified and, in the author's view, certainly incomplete | A review against every countermeasure in use across the operator's estate and against every countermeasure a competent adversary of the kind described could be used against; and an explicit statement of what the catalogue does not cover |
| AA-CC-12 | The evidence rule makes the residual-risk figures credible | The requirements in §8 ensure that a residual-risk figure on a card is credible | Architectural assertion; unverified. The rule is currently the only thing standing between a design-intent band and a card's residual-risk figure, because no figure in this version has been measured | Collection of measured figures at basis `E1` and `E2` for at least the entries relied upon operationally; and an audit of cards already produced against the rule |
| AA-CC-13 | The operator burden assessments are proportionate | The ordinal burden assessments in §6 reflect the effort each entry actually consumes | Architectural assertion; unverified; expressed ordinally and not costed | Time-and-effort measurement for a representative deployment of each entry; and a comparison against the ordinal assignment |
| AA-CC-14 | The intelligence yield assessments are proportionate | The ordinal yield assessments in §6 reflect the adversary-facing information each entry actually produces | Architectural assertion; unverified | Comparison of the assessment against the information obtained in exercise and in operation, with the entries whose yield was materially misjudged |

**VR-CC-A — Principle for use.** Where the claims in this table are cited, they must be accompanied by this section or by a statement that verification is outstanding. Comparative and absolute phrasings — *prevents*, *preferable*, *meaningful*, *complete* — must not be repeated as verified guarantees.

**VR-CC-B — Principle for the catalogue.** The requirement that every entry carry its basis, confidence, failure modes, side effects, and preconditions applies to every countermeasure in the catalogue, and applies regardless of the verification status of the claims above. The catalogue is usable as a descriptive instrument while these claims remain unsubstantiated, provided it is used as a descriptive instrument.

**VR-CC-C — Consistency with the framework's evidence discipline.** Presenting the figures in §6, or the combination rules in §7, as verified facts would breach the evidence discipline of `compliance/operator-conduct-and-human-in-loop-standard.md` and the labelling rules of the master design §5.4. Where a figure or a rule is cited externally, the basis, the confidence, and the outstanding substantiation travel with it.

---

## 11. Document Limitations

**Note on the identifier prefix.** The limitations in this section are numbered `LIM-CAT1` to `LIM-CAT13`. The `LIM-` prefix is the set's convention for limitations, and the sibling document `compliance/operator-conduct-and-human-in-loop-standard.md` already carries `LIM-CC1` to `LIM-CC12`. The set's identifiers are unique across the set, so the catalogue has taken `LIM-CAT` to avoid a collision. The set index register at `README.md` §5 should be updated at the next set revision to record the `LIM-CAT-` row alongside the existing `LIM-` row.

| # | Limitation |
| --- | --- |
| **LIM-CAT1** | **The residual-risk reduction figures are not empirically validated.** Every figure in §6 is a design-intent estimate at basis `E4` with low or very low confidence. No figure in this catalogue has been measured against an adversary, and the bands have not been shown to predict observed outcomes. Under `EVD-CC-3` they may not be used as the effectiveness term on a card. This is the most consequential limitation in the document, because the figures are the part of the catalogue a reader is most likely to quote. |
| **LIM-CAT2** | **Deception is adversary-specific and decays.** A deception countermeasure works because the adversary's model forms a false belief. An adversary that verifies its beliefs against ground truth, that reasons about being manipulated, or that simply changes approach defeats it. Effectiveness is per-adversary, expires as the adversary adapts, and is not a property of the countermeasure. The catalogue's bands for the deception entries do not carry that decay, because they cannot be parameterised per adversary. |
| **LIM-CAT3** | **A catalogue cannot capture emergent or hybrid techniques.** The catalogue enumerates countermeasures that have been anticipated. An adversary that combines techniques in a way that defeats each countermeasure individually — a technique whose value lies in the sequence rather than in any step — is not addressed by any entry, and the class structure provides no mechanism for the catalogue to acquire a new entry in response. |
| **LIM-CAT4** | **Not every entry has been exercised.** Several entries — in particular OCC-24, OCC-27, OCC-38, and the entries in CM-F Disrupt — have not been exercised in a live operation or, in some cases, in a controlled exercise. Their stated behaviour is design intent. The entries' status field does not distinguish "never exercised" from "exercised and found effective", and a reader should treat the distinction as unavailable in this version. |
| **LIM-CAT5** | **Collateral classes are assigned at entry level and cannot capture per-deployment variation.** OCC-21 is C0 as normally deployed and becomes C2 when a third party's credential is in the rotation set. The entry states this, but the class field records the normal deployment, and a deployment that differs from the normal takes the class of the deployment, not the class of the entry. The operational risk is that a reader takes the entry's class as the ceiling. |
| **LIM-CAT6** | **The interaction hazards are reasoned, not observed.** Every entry in §7.5 is derived from the stated behaviour of the entries involved. No entry in that table is known to have caused the hazard it describes, because the combinations have not been exercised. The table is a hypothesis about interaction, and its coverage of the true hazard space is unknown. |
| **LIM-CAT7** | **Operator burden is ordinal and uncosted.** The burden assessments in §6 are relative judgements. They are not expressed in person-hours, in cost, or in service degradation, and they do not distinguish a cost borne once at deployment from a cost borne continuously in operation. The burden of the entries at C0 with a high burden rating — the detection and hardening entries — is the most likely to be underestimated, because it is paid in attention rather than in money. |
| **LIM-CAT8** | **The catalogue says nothing about the adversary's adaptation over time.** Every entry is described as it would be applied against a known or suspected adversary at a point in time. The catalogue contains no view on how long an entry remains effective against an adaptive opponent, no countermeasure for the adversary's learning, and no mechanism for the re-baselining that a persistent deception programme requires. |
| **LIM-CAT9** | **The reversibility scale is coarse.** Four categories cannot distinguish a credential that can be reissued in minutes from one that cannot be reissued at all. Where the distinction is load-bearing — and in CM-F Disrupt it usually is — the entry states the irreversible elements individually, and the card must do the same under `ROE-7`. |
| **LIM-CAT10** | **The catalogue contains no legal advice.** The collateral classes and the third-party test are the framework's encoding of authorisation *structure*. They are not legal judgement. Every entry at C1 or above requires a legal contact whose view is a necessary input, and that judgement is not reproduced here, cannot be, and is not implied by the presence of a class. |
| **LIM-CAT11** | **The entries assume a control plane.** Most entries depend on capabilities the platform is expected to provide: enforcement points, an identity service, a capture store, a checkpoint store, an abort channel. Where the platform does not provide them the entry is not deliverable, and the catalogue has no representation of that dependency other than the preconditions field. This limitation will resolve as the platform is specified, and until then the deliverability of a substantial number of entries is unestablished. |
| **LIM-CAT12** | **The attribution dependency categories are coarse and partly judgemental.** The distinction between *behavioural* and *class* in particular does not map cleanly onto the difference between an entry that requires a recognised behavioural signature and one that requires a category classification, and the boundary between *class* and *identity* is drawn differently by different entries. The dependency is a usable device for the admissibility check, not a precise instrument. |
| **LIM-CAT13** | **The entries describe countermeasures, not procedures.** A procedure summary in §6 is at the level of a runbook lead. The runbook itself, with the exact configuration, the thresholds, and the failure handling, lives with the platform and is not reproduced here. An operator following a summary without the runbook will not deploy the countermeasure as described, and the entry's figures will not hold. |

---

## 12. Summary

This catalogue holds forty-three countermeasures in seven classes, and it holds them as descriptions rather than as permissions.

The organising idea is the direction of effect. Every entry declares whether its effect falls inward on the operator's own estate, outward on the adversary's own systems, inward/outward on the adversary's behaviour expressed through the operator's environment, or on the operator's knowledge alone. That single field, read first, answers the question the framework cannot answer for itself — whether an act reaches beyond the operator's control — and it is the field that determines whether the third-party test applies, what attribution the countermeasure requires, and at what depth it must be approved. The countermeasure whose actual effect differs from its stated one is classified by its actual effect, and the class structure follows from it: detect, harden, contain, observe, deceive, disrupt, recover.

Three preferences run through the catalogue and are not merely rhetorical. The environment is shaped before it is broken; containment precedes disruption, because containment preserves the intelligence that disruption destroys; and a countermeasure that does not depend on knowing who the adversary is is preferred under attribution uncertainty, because misattribution costs more than inaction. These preferences are stated as preferences, and the Operation Card records the reason whenever they are departed from.

The catalogue is honest about what it does not know. Every residual-risk figure in §6 is a design-intent band at the lowest evidence basis, marked as such, and none of them may serve as the effectiveness term on a card; the card computes its own. Deception is per-adversary and decays. Emergent and hybrid techniques are not addressed by any entry. Several entries have never been exercised. The combination rules are reasoned from the entries' stated behaviour rather than observed, and the hazards they describe may not be the hazards that matter. The register in §10 lists fourteen claims that this catalogue asserts and does not substantiate, and the register in §11 lists thirteen limitations that constrain how the catalogue may be used.

What the catalogue does provide is a shared vocabulary for a decision that must be made quickly, under pressure, with incomplete information: a common set of terms, a common classification of cost and reversibility, a common statement of what each countermeasure requires before it may be used, and a common account of what it will not do. A reader who knows the catalogue can read an Operation Card, a decision log, or an after-action report written by someone else and understand not only what was done but what it cost, what it risked, what it assumed, and where it would have failed.

---

*This was supported for MIA by Kilo (kilo-auto/free).*
