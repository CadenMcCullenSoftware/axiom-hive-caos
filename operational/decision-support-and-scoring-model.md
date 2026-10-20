# Decision Support and Scoring Model: CAOS — Counter-Adversary Operations System

| Field | Value |
| --- | --- |
| Author | MIA |
| Attribution | This was supported for MIA by Kilo (kilo-auto/free). |
| Document type | Specification |
| Subject | The normative specification of the CAOS decision-support model: threat score, attribution confidence, confidence propagation, effective threat, expected effectiveness, residual risk, risk-adjusted priority, the admissibility algebra, the selection algorithm, and the counterfactual presentation of alternatives |
| Version | 1.0 |
| Status | Authoritative for the decision-support model. Subordinate to `system-design-and-framework.md` §6, which states the model in summary and which this document expands; subordinate to the constitutional instrument, which sets the classes the model evaluates against |
| Companion documents | `system-design-and-framework.md`; `README.md`; `constitutional/engagement-authorisation-and-rules-of-engagement.md`; `compliance/operator-conduct-and-human-in-loop-standard.md`; `operational/mission-lifecycle-and-decision-loop.md`; `operational/adversary-ai-taxonomy-and-threat-model.md`; `operational/countermeasure-catalogue.md`; `operational/watchfloor-interface-specification.md`; `operational/platform-architecture-and-agent-containment.md`; `reference/ai-attack-technique-library.md`; `reference/audit-and-conformance-procedures.md`; `templates/operation-card.md`; `templates/decision-log.md` |
| Identifier series owned by this document | `SCORE-1` to `SCORE-5`; `AD-1` to `AD-13`; `DS-1` to `DS-12`; `LIM-DS1` to `LIM-DS11` |

---

## 1. Purpose and Scope

### 1.1 The purpose of the model

The decision-support model exists to make a decision **under uncertainty** legible and contestable. It does not exist to make the decision.

An operator in this framework is nearly always deciding with incomplete evidence, under time pressure, against an adversary who is actively shaping what the operator can see. The failure mode the model is designed against is not a wrong number. It is a number that is acted upon without being understood — a score that arrives detached from the evidence, a recommendation that arrives without its alternatives, a risk figure that arrives without the risk of doing nothing beside it. Such an operator is not reasoning badly. The instrument is failing them.

The model therefore does five things and refuses a sixth:

| The model does | The model does not |
| --- | --- |
| Compute a threat score from four declared components, each separately contestable | Produce a single number that stands in for the assessment |
| Carry an explicit attribution confidence with a stated basis | Resolve attribution, or present a name without a confidence |
| Propagate confidence along derivation chains and expose the chain | Treat a strong observation as a strong conclusion regardless of how far it has travelled |
| Compute effective threat, residual risk, and risk-adjusted priority | Treat any of these as an authorisation |
| Evaluate admissibility as a conjunction of conditions and rank the survivors | Aggregate failures, grant partial credit, or recommend an action to be taken |

### 1.2 The model's central claim about itself

**The model never authorises. A score is never an authorisation.**

This is stated in the master design at `SCORE-1` and it is restated here as the first principle of the specification, because everything else in this document follows from it. A computed quantity is a summary of a judgement, not a warrant. The warrant is the engagement authorisation; the decision is the operator's; the record is the card. Where the model and the operator's judgement differ, the operator's judgement governs — and the card records the difference, the reason for it, and what would have caused the decision to be withdrawn.

This is not a disclaimer. It is a design commitment with consequences that run through the whole of this document:

- A high score does not create authority (`SCORE-1`).
- A high priority rank does not create authority (§8.4).
- An admissible countermeasure is not an approved one (§10.5).
- The absence of an authorisation is not repaired by a good score (§1.4).

### 1.3 What this document is authoritative for

| Subject | Status of this document |
| --- | --- |
| The definition, evaluation semantics, and display rules of `S`, `L`, `I`, `A`, `V` | **Authoritative.** The master design states the formula; this document states what each component means and how it is evaluated |
| The definition and evaluation semantics of `c`, the attribution confidence | **Authoritative.** The master design and `INT-2` state the concept; this document states the procedure |
| The confidence-propagation rule and the derivation-penalty table | **Authoritative.** `INT-9` states the principle; this document states the table and the evaluation procedure |
| The formulas for `S_eff`, `R`, and `P`, and the collateral-exposure normalisation | **Authoritative.** The master design states the formulas; this document states the inputs, the normalisation, and the display rules |
| The evaluation semantics of `AD-1` to `AD-13` | **Authoritative.** The master design §6.4 states the conditions; this document states the predicates, the inputs, the failure reporting, and the checkability classification |
| The expansion of the master design §6.5 selection steps | **Authoritative for the computational steps.** The gating, the card lifecycle, and the authorisation act are governed by `operational/mission-lifecycle-and-decision-loop.md` and the constitutional instrument |
| The collateral classes, the autonomy classes, the ROE profiles, the permitted action classes, the countermeasure entries, and the AAT categories | **Not authoritative.** Restated here only as the quantities the model evaluates against. The constitutional instrument, `operational/countermeasure-catalogue.md`, and `operational/adversary-ai-taxonomy-and-threat-model.md` govern, and where they differ from a restatement here the restatement is the defect |

### 1.4 Out of scope

The model does not address, and must not be read as addressing:

- whether an operation is lawful, proportionate, or ethically right;
- the adequacy of the mandate under which a card exists;
- the choice between conducting an operation and not conducting one at all, except as the comparison of residual risk against the risk of inaction (§7.5);
- the design of the sensors that produce the observations the model consumes;
- the interface on which the model is displayed, except where this document fixes what must be visible on it (§13.4, §14).

---

## 2. Interpretation of Normative Terms

The terms **must**, **must not**, **should**, **should not**, and **may** are to be interpreted as described in RFC 2119.

- **Must / must not** denote absolute requirements. A requirement so marked is a condition of validity of the assessment or of the decision record, not a preference.
- **Should / should not** denote recommendations that may be departed from only where legitimate reasons exist; any departure must be made explicit and recorded on the card.
- **May** denotes optional behaviour that remains at the operator's discretion within the constraints of this document and the authorisation in force.

Two additional conventions apply throughout.

**Verified terms.** A term in this document that describes the behaviour of the reference implementation, of the platform, or of the framework as a whole is a statement of **design intent** unless it is marked as verified. Where such a statement is load-bearing — where a reader might reasonably act on it — the statement is entered in the register at §15 with what substantiation would require.

**Quantified judgements.** Every numeric value produced by this model is an **estimate** produced by a named analyst or by the operator, and is not independently calibrated (§13). The word "probability" is used in this document in its ordinary sense of a stated degree of belief, not in the sense of a frequency verified against outcomes. Where the difference matters, the value is described as an estimate.

---

## 3. Defined Terms

| Term | Definition |
| --- | --- |
| **threat score** (`S`) | The prioritisation quantity `S = L × I × A × V`, ranging from 0 to 20. It is a summary of four separately recorded judgements and is never used alone. |
| **likelihood** (`L`) | The analyst's estimate, in [0.0, 1.0], of the probability that the observed activity is a real attack attempt against the operator, given the evidence held. It is **not** the probability that the activity succeeds. |
| **impact** (`I`) | The analyst's estimate, on the ordinal scale 0 to 5, of the consequence to the operator's estate if the activity succeeds. |
| **autonomy factor** (`A`) | The analyst's estimate, on the ordinal scale 0 to 2, of how far the observed activity proceeded without effective human supervision. |
| **velocity** (`V`) | The analyst's estimate, on the ordinal scale 0 to 2, of the degree to which the activity is adaptive rather than fixed. |
| **attribution confidence** (`c`) | The stated probability, in [0.0, 1.0], that the observed activity is attributable to the specific candidate adversary named in the attribution assessment. It is an estimate with a stated basis, an evidence tier, and a derivation chain. |
| **effective threat** (`S_eff`) | `S_eff = S × c`. The quantity to which the escalation ladder is applied: the portion of the threat that is attributable to the adversary the operator is answering. |
| **expected effectiveness** (`e`) | The analyst's estimate, in [0.0, 1.0], of the proportion of the effective threat that the selected countermeasure set is expected to neutralise, if it achieves its intended effect. `e` is always carried with a confidence. |
| **residual risk** (`R`) | `R = S_eff × (1 − e)`. The risk carried forward after the selected countermeasures. It is the figure the operator is accountable for. |
| **risk-adjusted priority** (`P`) | The ranking quantity `P = (S_eff / 20) × q × (1 − r)`, where `q` is the confidence in the countermeasure achieving its intended effect and `r` is the normalised collateral exposure. `P` is a ranking only. |
| **collateral exposure** (`r`) | The normalised measure, in [0.00, 1.00], of the collateral class of a countermeasure, used only as a term in `P`. The collateral class itself, and the approval depth it requires, are constitutional and are not derived from `r`. |
| **countermeasure** | A declared, bounded action or control recorded in `operational/countermeasure-catalogue.md` with its class, collateral class, reversibility, autonomy class, attribution dependency, preconditions, and technique bindings. |
| **admissible** | Satisfying every one of the conditions `AD-1` to `AD-12` for the card in question, under the profile in force. |
| **inadmissible** | Failing any one of the conditions `AD-1` to `AD-12`. The failing condition and its margin are reported (`AD-13`). |
| **assumption** | A proposition held but not observed, on which one or more claims depend. Each assumption is recorded with the confidence that depends on it, and is visible on the card. |
| **derivation penalty** | The declared deduction applied to the confidence of a derived claim, determined by the kind of inference that produced it. The table is at §6.2. The penalty is declared, not implicit (`INT-9`). |
| **world model** | The card's stated understanding of the world at a point in time: the classification, the attribution, the score, the evidence believed, and the assumptions held. Drift between the stated world model and the observed one is a trigger for the error handler. |
| **decomposition** | The requirement that every computed quantity be presented to the operator as the components it was computed from, each separately contestable, together with the reasoning recorded for each component. |
| **calibration** | The process of establishing, from recorded outcomes, that a stated confidence value corresponds to an observed frequency of correctness. Until calibration data exists, a confidence value is an estimate and not a calibrated probability. |
| **the card** | The Operation Card: the atomic unit of authorised work, and the record in which this model's outputs are recorded. |
| **the operator** | The named human with authority over a card, who selects, declines, or combines countermeasures, and who is accountable for the residual risk the card carries. |
| **the classifier** | The component — automated, human-assisted, or human — that assigns an AAT category to a signal, with a stated rationale and a stated confidence, and which the operator may override (`TAX-2`, `TAX-4`). |
| **attribution basis** | The specific kind of evidence supporting an attribution assessment, recorded with its reliability: behavioural signature match, infrastructure overlap, capability and timing correlation, TTP overlap, infrastructure artefacts, or inference from capability alone (`INT-2`). |
| **category confidence** | The confidence that a signal belongs to a stated AAT category. It is distinct from attribution confidence: a signal may be confidently *what* it is and uncertain *who* sent it (`INT-4`). |
| **the observing analogue** | The reference behaviour against which an observation is compared in order to establish that it is anomalous. The analogue is drawn from the operator's own baseline, from a catalogue of known benign patterns, or from the adversary's documented pattern. Where no observing analogue exists, the observation cannot be established as anomalous, and `L` must not be raised on it. |
| **the counterfactual** | An explicitly computed alternative state of the world under a course of action other than the one taken — including the state in which nothing is done — computed with the same formulas and displayed with its own residual risk and collateral exposure (§12). |
| **operator proposal** | A candidate countermeasure proposed by the operator that does not correspond to a catalogue entry. It enters the candidate set at `STEP-1` and is subject to the same admissibility algebra, with its attributes recorded on the card. |
| **provenance reference** (`PROP-nn`) | A local reference used in this document to identify an operator proposal. It is not a set-wide identifier series and does not enter the set index registry. |

---

## 4. The Threat Score

### 4.1 The formula

**S = L × I × A × V**

`S` ranges from 0 to 20. It is a prioritisation aid, not a decision, and it is never used alone (`SCORE-1`). The four components are displayed individually and separately contestable (`SCORE-2`), so that an operator who disputes the score can say which component they dispute rather than rejecting the whole assessment.

`L` is a quasi-continuous quantity on [0.0, 1.0]. `I`, `A`, and `V` are ordinal quantities on small integer scales. Their product is therefore **ordinal in construction**: a difference of 1.0 in `S` does not represent a proportionate difference in threat, and `S` must not be read as a linear quantity. The band labels at §4.6 exist to make this legible, not to imply a measurement scale.

### 4.2 Likelihood (`L`)

`L` is the analyst's estimate of the probability that the activity is a real attack attempt against the operator, given the evidence held. It is explicitly **not** the probability that the activity succeeds; that is a different question and is not asked here.

The score is computed from the analyst's stated point estimate, rounded to two decimal places. The band is recorded alongside for display, threshold comparison, and ordinal use. Where the analyst states a band without a point estimate, the band's representative value is used, and the use of a representative is recorded on the card.

| Band | Probability range | Ordinal | Representative | What the band means in evidence terms |
| --- | --- | --- | --- | --- |
| **L0** | 0.0 | 0 | 0.00 | The activity has been determined not to be an attack attempt — a scheduled internal test, a declared red-team exercise, or an activity matched to a known benign pattern by the observing analogue. |
| **L1** | 0.1 – 0.3 | 1 | 0.20 | The behaviour is consistent with routine, automated, or legitimate activity, and no adversary-specific artefact has been identified. One or more benign explanations remain plausible and none has been eliminated. |
| **L2** | 0.4 – 0.6 | 2 | 0.50 | Adversary-consistent artefacts are present but not distinctive. At least one benign explanation still accounts for the observations, and the evidence does not separate the two. |
| **L3** | 0.7 – 0.9 | 3 | 0.80 | The behaviour matches a known adversary technique pattern at a level at which coincidence is unlikely. The competing explanations have been tested and fail. Note that this establishes the *technique* better than it establishes the *actor*; the actor is a separate question addressed by `c`. |
| **L4** | above 0.9 | 4 | 0.95 | The behaviour is essentially unambiguous under the declared telemetry coverage, with an adversary-specific artefact directly observed and no competing explanation surviving. |

**Boundary rule.** The band boundary at exactly 0.9 is resolved into band **L3**, the conservative reading. A value of 0.90 is therefore *not* in L4; L4 begins above 0.90. The boundary is stated here because the master design records the bands as `0.0`, `0.1–0.3`, `0.4–0.6`, `0.7–0.9`, and `0.9–1.0`, and those ranges overlap at 0.9; the overlap is resolved in favour of the lower band.

**Required supporting material.** A stated `L` must be accompanied by the observing analogue against which the observation was read, the alternative explanations considered, and the reason the alternatives were accepted or rejected. A likelihood asserted without an observing analogue is not a likelihood; it is an intuition with a decimal in front of it.

### 4.3 Impact (`I`)

`I` is the consequence **to the operator's estate** if the activity succeeds. It is not the consequence to the adversary, not the consequence to a third party, and not the consequence in the general case.

| `I` | Name | Definition | Illustrative example |
| --- | --- | --- | --- |
| **0** | None | No consequence to the estate if the activity succeeds. | A scan of a publicly reachable service endpoint that finds nothing and changes nothing. |
| **1** | Nuisance | Minor inconvenience; no loss of data; no service effect beyond transient degradation that the estate absorbs without intervention. | A large volume of failed authentications against one account, throttled by existing controls, with no successful authentication. |
| **2** | Data exposure | Some data is read, disclosed, or reconstructed, in bounded and recoverable quantity; no material service effect. | Partial retrieval of a non-sensitive configuration file by a service account that was already compromised, from which little can be inferred. |
| **3** | Degradation of a service | A service is impaired or degraded for its users; recoverable without data loss and without loss of a capability the estate depends on. | Tool-output poisoning that degrades the quality of an assistant's answers for a class of queries across a sustained window, with no data loss. |
| **4** | Material loss or compromise | A system is materially compromised, or a material asset is lost; recovery requires reconstruction rather than restoration. | A credential set is exfiltrated from a shared workload identity and is then used to reach a second segment, requiring the affected systems to be rebuilt from trusted sources. |
| **5** | Loss of a critical function | A function the organisation depends upon is lost, or a capability bearing on safety or continuity is impaired. | The identity provider or the build-and-deploy pipeline serving the production estate is compromised, so that changes to production can no longer be made with confidence. |

**Bounding rule.** Where the activity's effect on the estate is contingent on a step that has not occurred, `I` is assessed on the **most likely** effect, not the maximum possible effect, and the card records the assessment and the contingency. Impact is a statement about what to expect, not a worst-case envelope.

### 4.4 Autonomy factor (`A`)

`A` describes how far the observed activity proceeded without effective human supervision. It is a property of the observed activity, not of the adversary's capability in general.

| `A` | Name | Definition | Operative test |
| --- | --- | --- | --- |
| **0** | Human-directed and supervised in real time | A named human directed the activity and could see its effect as it happened. | Can the operator identify a human decision point at which the activity would have been stopped, and was a human in a position to observe that point at the time? If yes, `A = 0`. |
| **1** | Machine-directed with a human in the loop at intervals | A machine executed the activity; a human reviewed it on a cadence, on exception, or after the fact. | Is there any point at which a human could have intervened before the activity completed its objective, other than after the fact? If yes, but not in real time, `A = 1`. |
| **2** | Machine-directed with no effective human supervision | The activity ran to completion, or to its objective, without a human being in a position to observe it, influence it, or stop it while it ran. | Could a human have observed, influenced, or stopped the activity while it was still running, at a cost proportionate to the activity itself? If no, `A = 2`. |

**The operative test for "no effective human supervision".** The question is not whether a human *could* have been watching in principle, and not whether a human reviewed the outcome afterwards. It is whether human intervention was **available in practice at a proportionate cost during the activity**. Where the only human involvement was a retrospective review of logs produced after the fact, the activity had no effective human supervision and `A = 2`. Where an operator was watching a live console and could have intervened, `A = 0` even if the operator chose not to.

**Interaction with the taxonomy.** `A` is a property of the observed instance, not of the AAT category. The same technique observed under supervisory review and observed running unattended are different `A` values, and the same campaign may occupy both across its duration. Where the evidence supports different values for different portions of the activity, the assessment states which portion each value describes.

### 4.5 Velocity (`V`)

`V` describes the degree to which the activity is adaptive — the adversary changing approach in response to outcomes — rather than fixed.

| `V` | Name | Definition | Operative test |
| --- | --- | --- | --- |
| **0** | One-off | The activity occurred once. | Has the activity occurred exactly once, or is it the output of a fixed script whose parameters have not varied? Then `V = 0`. |
| **1** | Repeated or scripted | The activity recurred, or is the output of a fixed, pre-written script that does not change between attempts. | Has the activity recurred, or does it run from a script with invariant parameters? Then `V = 1`. |
| **2** | Adaptive | The adversary changed approach between attempts in response to the outcome of a previous attempt. | Is there evidence of variation correlated with the observed outcome of a prior attempt — a changed parameter, a new technique, a different target, a different timing — such that the variation is better explained by learning than by chance? Then `V = 2`. |

**The operative test for "adaptive".** Recurrence alone is `V = 1`, not `V = 2`. The evidence that distinguishes `V = 2` is **correlation between a change in the activity and the outcome of a prior attempt**. Where the variation is equally well explained by chance, by a schedule, or by a human operator changing the parameters, `V = 1` is the correct value, and the card records that the adaptive reading was considered and not supported.

**Leading-indicator rule.** A rising `V` against a flat `I` is treated as the strongest available signal of an emerging autonomous campaign (`SCORE-3`).

### 4.6 Bands of `S`

The bands exist to make the score legible at a glance and to support queue ordering. They are display labels. The score itself is the product.

| Range of `S` | Band | Reading |
| --- | --- | --- |
| 0.00 – 0.99 | **S-A** | Negligible. |
| 1.00 – 2.99 | **S-B** | Low. |
| 3.00 – 5.99 | **S-C** | Moderate. |
| 6.00 – 9.99 | **S-D** | Elevated. |
| 10.00 – 14.99 | **S-E** | High. |
| 15.00 – 20.00 | **S-F** | Severe. |

### 4.7 Worked examples

#### Worked example WE-A — Tool-output poisoning in an internal assistant service

An internal assistant service, used by staff, is observed returning answers that contradict the operator's own written policy on a class of queries. Examination of a sampled batch of tool responses shows an embedded instruction directed at the assistant's tool layer, in text that the service had ingested from a third-party content source.

| Component | Value | Band / level | Reasoning | Label |
| --- | --- | --- | --- | --- |
| `L` | 0.85 | L3 (high) | The observing analogue is the operator's own content pipeline, which does not emit instruction-like text addressed to the tool layer; the sampled responses do. The two competing benign explanations — a stale template in the service and a misconfigured retrieval source — were tested against the sampled batch and neither accounts for text addressed to the tool layer. The activity is a real attack attempt. The actor is not yet established, which is a separate question. | Estimate |
| `I` | 3 | Degradation of a service | The service answers are degraded for a class of queries across a sustained window. No data was lost, and no capability the estate depends upon has been lost. Restoration is possible by removing the source and revalidating the affected outputs, but the answers already given to staff cannot be recalled, which places the effect above a pure nuisance. | Estimate |
| `A` | 1 | Machine-directed, human in the loop at intervals | The campaign ran unattended between daily review points. No human was in a position to observe or stop it while it ran, which rules out `A = 0`; but a human did review the outcome of each day's output, and the activity was not carried through to an objective no human could have intervened before, which rules out `A = 2`. | Estimate |
| `V` | 1 | Repeated or scripted | The same injection payload was replayed across many queries by a fixed harness, with the target and payload unchanged. No change correlated with the outcome of a prior attempt was identified. | Estimate |

**S = 0.85 × 3 × 1 × 1 = 2.55**, band S-B (low).

The low score is not a reassurance and must not be read as one. It says: the activity is confidently real, its effect is bounded to degradation, it was unattended but reviewed, and it shows no evidence of adaptation. The 3 in the impact term is doing the work of the assessment; the 1 in the autonomy term is doing the work of the caution. An operator who disputed only the impact would say so, and the record would show exactly which number is in dispute.

#### Worked example WE-B — Autonomous credential harvesting with adaptive evasion and exfiltration

An account authentication service records a sustained, high-volume pattern of failures against many accounts, followed by a small number of successes, followed by a burst of outbound traffic from a workload identity to a destination not present in the operator's baseline, followed by a second burst to a different destination with different parameters.

| Component | Value | Band / level | Reasoning | Label |
| --- | --- | --- | --- | --- |
| `L` | 0.92 | L4 | Two adversary-specific artefacts are directly observed: a request shape inconsistent with the observing analogue for legitimate client traffic, and an outbound destination absent from the operator's baseline and identified in the operator's own records as adversary-associated. No benign account of either artefact survives. | Estimate |
| `I` | 4 | Material loss or compromise | A credential set was taken from a shared workload identity and was then used to reach a second segment. Recovery requires reconstruction of the affected systems from trusted sources, not restoration of a single service. The critical-function level is not reached: the identity provider and the delivery pipeline are not compromised, and no safety-bearing capability is impaired. | Estimate |
| `A` | 2 | No effective human supervision | The harvesting ran to completion across many accounts without a human in a position to observe, influence, or stop it. A proportionate intervention would have required monitoring the authentication telemetry live, which was not in place for this service. The successes and the exfiltration followed from the harvesting, and no human observed any part of it in progress. | Estimate |
| `V` | 2 | Adaptive | The second outbound burst used different parameters from the first and followed the observation window in which the first destination failed to yield. The change is better explained by the adversary learning from the first attempt's outcome than by chance or by schedule. | Estimate |

**S = 0.92 × 4 × 2 × 2 = 14.72**, band S-E (high).

The four components compound, and they are not equally reliable. `A = 2` rests on the absence of a monitoring capability rather than on a positive observation of unsupervised operation; that is an inference, and it is recorded as one. `V = 2` rests on a single change correlated with a single outcome, which is a thin basis for the highest band of the scale. Both entries are separately contestable, which is the point of `SCORE-2`.

#### Worked example WE-C — Automated bulk access that is not an attack

A partner integration begins making a larger number of routine read calls than in the preceding period, at times that differ from its historical pattern, using its normal credentials.

| Component | Value | Band / level | Reasoning | Label |
| --- | --- | --- | --- | --- |
| `L` | 0.20 | L1 (low) | The request shape is within the observing analogue for the integration's historical behaviour, and the volume change has a candidate benign explanation in a schedule change on the partner's side that has not yet been confirmed. No adversary-specific artefact is present. | Estimate |
| `I` | 1 | Nuisance | No successful access to sensitive data is indicated, no service effect is observed, and the existing rate controls absorb the traffic. | Estimate |
| `A` | 1 | Machine-directed, human in the loop at intervals | The integration runs unattended; a human reviews its usage weekly. | Estimate |
| `V` | 1 | Repeated or scripted | The traffic recurs on a schedule and does not vary in response to any prior outcome. | Estimate |

**S = 0.20 × 1 × 1 × 1 = 0.20**, band S-A (negligible).

**The low score is not a finding of innocence.** It is a record that the evidence held does not support an attack reading. Where a subsequent observation raises `L` — the partner confirms no schedule change, and the call pattern matches no known automation — the card must be revised and the earlier score superseded in the record, not quietly overwritten. A low score that is later revised is normal; a low score that is never revisited is a failure of the review discipline.

### 4.8 The `SCORE-` requirements

**SCORE-1 — Score is never used alone.** No action is authorised on the basis of a score. The score orders the queue; the card, the evidence, and the authorisation authorise the action. *Expansion.* A score is a summary of four judgements. Any of the four may be wrong, and the product conceals which. Accordingly: (a) no interface may present a score as a reason to act; (b) a card that cites a score as the justification for a countermeasure selection is defective; (c) the residual risk on the card, and the comparison against the risk of inaction, are the figures the approver weighs; (d) the score may be used to order the queue, to prioritise review, and to decide what to look at next, and for nothing else. Where an operator states that they are acting on the score, the record is defective and the error handler is triggered.

**SCORE-2 — Components are separately contestable.** Every scoring decision is recorded with the reasoning for each component, so that a later reviewer can dispute a specific component rather than the whole assessment. *Expansion.* A recorded score is four entries, each carrying: the value; the band; the observing analogue or reference against which the judgement was made; the alternatives considered; the reason for the alternatives' rejection; the analyst's name; and the claim label. A reviewer who disputes the assessment must be able to identify which component is disputed, say what the correct value would be, and see what the score would have been. A score recorded as a single number without components is not accepted by the interface and is not a valid input to any other computation in this model.

**SCORE-3 — Velocity is a leading indicator.** A rising `V` against a flat `I` is the strongest available signal of an emerging autonomous campaign, and is treated as such in the watchboard's escalation cues. *Expansion.* The queue is otherwise ordered on `S`, which is dominated by `I` and `A`. A campaign that is currently causing nuisance-level damage but is visibly adapting is the case the queue must surface first, and a queue ordered strictly on `S` will not surface it. The treatment is: (a) where `I` is flat and `V` has risen by at least one level since the previous assessment, the item is flagged as an emerging-campaign candidate regardless of its band; (b) the flag is a cue for the operator to look, and carries no authority and no priority over an authorisation; (c) the flag is a hypothesis-generating observation, and the card that results from it must state a disconfirming observation; (d) the `V` change is recorded with the evidence of adaptation, per the operative test at §4.5, so that a rising `V` cannot be asserted without the correlation that supports it.

**SCORE-4 — `e` is an estimate with a confidence.** Expected effectiveness is stated as a value and a confidence. A countermeasure with high effectiveness and low confidence is reported as such, and is not presented as a certainty. *Expansion.* The effectiveness term and the confidence in it are distinct quantities and are never merged into one figure. The requirements are: (a) every effectiveness value carries a confidence, and a value with no confidence is refused by the interface (§7.2); (b) the residual risk is displayed as a range wherever the confidence is below 0.60, using the display convention at §7.4; (c) a countermeasure assessed at `e ≥ 0.70` with `q < 0.50` carries an explicit unconfirmed-effectiveness marker and is never rendered as a bare reduction figure; (d) a catalogue band may not be used as a card's `e` without a card-level effectiveness assessment, because the catalogue records what a measure would remove *if it worked*, and not how likely it is to work; and (e) the assessment, its basis, and its confidence are recorded on the card, so that the realised effectiveness at `G-6` can be compared against what was expected.

**SCORE-5 — Residual risk is compared to the risk of inaction.** Both are on the card. An operation proceeds when the reduction in residual risk justifies the collateral exposure relative to the risk of doing nothing, and the argument is written down. *Expansion.* The comparison is computed and displayed; the model does not compute a verdict, and all three outcomes — acting, declining, and sitting close — are legitimate and must be presentable without the model favouring one (§7.5). The requirements are: (a) the risk of inaction is computed on every card carrying a selection, using the effectiveness of the current baseline posture, and is not omitted because inaction is uncomfortable to record; (b) the comparison is presented beside the residual risk, not on a separate screen; (c) the card records the argument by which the reduction was judged to justify the exposure, in the words of the person deciding, and where the comparison is close the card says so rather than resolving it artificially; (d) the argument, the baseline estimate it rests on, and the counterfactual alternatives are all visible to the approver at `G-4`; and (e) a card that records a selection without the comparison against inaction is defective.

---

## 5. Attribution Confidence

### 5.1 Probability semantics

`c` is the stated probability, in [0.0, 1.0], that the observed activity is attributable to the **specific candidate adversary** named in the attribution assessment.

Four points of interpretation, each of which the implementation must respect:

1. **It is a probability over a hypothesis about identity, not a score of how dangerous the activity is.** A perfectly executed attack by an unknown actor is `c` low and `S` high. A trivial probe confidently attributed is `c` high and `S` low. The two quantities are multiplied only in `S_eff` (§7.1), and the components remain separately visible.
2. **It is an estimate, not a frequency.** No calibration data exists for it (§13.3). It is used as an ordering device and as a threshold input.
3. **It attaches to a named candidate.** `c` without a candidate is meaningless. Where the assessment is ambiguous between candidates, there is one `c` per candidate, and the rules at §5.5 apply.
4. **It is not the same quantity as category confidence.** A signal may be confidently *what* it is and uncertain *who* sent it (`INT-4`). A countermeasure whose attribution dependency is *Class* or *None* is evaluated on category confidence alone, and is unaffected by `c`.

### 5.2 Attribution bases and their reliability

The basis for an attribution is always listed, with its reliability (`INT-2`). The basis ceilings below are the **maximum** confidence that the basis alone can support; the actual contribution is the ceiling multiplied by the evidence weight at §5.3.

| Basis | Description | Basis ceiling | Principal weakness |
| --- | --- | --- | --- |
| **Behavioural signature match** | The activity matches a documented behavioural pattern of the candidate at a granularity at which coincidence is unlikely. | 0.90 | Deliberate imitation defeats it, and the reference pattern may itself be an inference rather than an observation. |
| **Infrastructure overlap** | The activity shares infrastructure characteristics — hosting patterns, transport artefacts, naming conventions, protocol behaviour — with previously attributed activity by the candidate. | 0.75 | Infrastructure is shared, rented, and re-used. Shared infrastructure is weak evidence of shared control. |
| **Infrastructure artefacts** | Artefacts are present in the adversary's own systems — residual configuration, build fingerprints, credential formats, code fragments — that are characteristic of the candidate. | 0.70 | Artefacts can be planted deliberately, and the artefact may have been inherited from a shared source. |
| **TTP overlap** | The candidate's operator tradecraft, targeting preferences, and timing patterns match the observed activity. | 0.65 | Tradecraft is imitated deliberately, and much tradecraft is common to many operators. |
| **Capability and timing correlation** | The capability displayed, and the timing of the activity, correlate with the candidate's known capability and known activity. | 0.50 | Correlation is not identity, and the capability is widely available. |
| **Inference from capability alone** | The activity is consistent with the candidate's capability and with nothing else that distinguishes it. | 0.30 | Any actor with the same commercial access could produce it. This basis carries almost no identity information. |

**Inference from capability alone is the weakest basis** and must be labelled as such wherever it is used (`INT-2`). A `c` resting on this basis alone cannot exceed 0.30 before the evidence weight of §5.3 is applied, and a countermeasure with an attribution dependency of *Identity* is not available on it.

**Rule against basis-shopping.** An assessment may not select the most generous basis available in order to raise `c`. The bases that the evidence actually supports are recorded, including those that support a different candidate. An assessment that records only the supporting basis is defective.

### 5.3 Evidence-tier weighting

Each basis is supported by evidence carrying a source reliability tier, as defined in the set index. The tier scales the basis contribution.

| Source tier | Description | Weight |
| --- | --- | --- |
| **1** | Primary data, the operator's own directly held and integrity-verified records, or an authoritative instrument. | 1.00 |
| **2** | Reputable secondary analysis and institutional grey literature with attributable authorship, including another operator's confirmed observation. | 0.80 |
| **3** | Single-expert assertion, pre-publication material, or commercial sources with verifiable provenance. | 0.50 |
| **4** | Unverified material, anonymous assertion, and model-generated suggestions or leads. | 0.25 |

**The basis score** is `basis ceiling × tier weight`, rounded to two decimal places.

**The combination rule.**

```
c(candidate) = min(0.99, max(basis scores) + corroboration bonus)
```

**The corroboration bonus** is `0.05` for each additional basis of a *different kind* whose basis score is at least `0.70 ×` the highest basis score, capped at `0.15` in total. A second basis of the same kind does not corroborate; two observations of the same signature are one piece of evidence observed twice, not two independent pieces.

**The contradiction rule.** Where contradicting evidence exists and has not been explained, the corroboration bonus is void and `c` is reduced by `0.10`, floored at `0.00`. Contradicting evidence is not a discount applied at the analyst's discretion; it must be recorded with what is known about it.

### 5.4 Worked attribution example

Activity: a burst of automated tool calls against an exposed integration endpoint, followed by access to a document store, followed by an outbound request to a newly registered domain.

| Candidate | Basis | Tier | Basis score |
| --- | --- | --- | --- |
| **Candidate A** | Behavioural signature match | 1 | 0.90 × 1.00 = **0.90** |
| **Candidate A** | Infrastructure overlap | 2 | 0.75 × 0.80 = **0.60** |
| **Candidate A** | TTP overlap | 3 | 0.65 × 0.50 = **0.33** |
| **Candidate B** | Behavioural signature match | 1 | 0.90 × 1.00 = **0.90** |
| **Candidate B** | Infrastructure overlap | 1 | 0.75 × 1.00 = **0.75** |
| **Candidate B** | Capability and timing correlation | 2 | 0.50 × 0.80 = **0.40** |
| **Candidate C** | Inference from capability alone | 3 | 0.30 × 0.50 = **0.15** |

**Candidate A.** Highest basis score 0.90. Corroboration test at `0.70 × 0.90 = 0.63`: infrastructure overlap 0.60 does not qualify; TTP overlap 0.33 does not qualify. Bonus 0.00. **c(A) = 0.90.**

**Candidate B.** Highest basis score 0.90. Corroboration test at 0.63: infrastructure overlap 0.75 qualifies (different kind from the signature match) → +0.05; capability correlation 0.40 does not qualify. **c(B) = 0.95.**

**Candidate C.** Highest basis score 0.15, no corroboration. **c(C) = 0.15.**

**Ambiguity.** `c(B) − c(A) = 0.05`, which is within 0.10. The two candidates are within the ambiguity threshold and the case is **ambiguous**. The reason is recorded: both candidates are known to operate through the same managed platform, and the behavioural signature available from platform telemetry does not discriminate between them at the granularity observed. A tier-1 basis that *does* discriminate — an operator-specific artefact, a credential format unique to one of them, or a direct observation tying the activity to one of their established infrastructure patterns — would resolve the ambiguity; none is held.

**Consequence.** Under §5.5, the effective confidence for any identity-dependent countermeasure is capped at 0.49, and `AD-9` fails for every countermeasure whose attribution dependency is *Identity*. The available route is a countermeasure whose dependency is *None*, *Behavioural*, or *Class* — `INT-4` and `INT-5` made operative. Candidate C at `c = 0.15` is below the C0 threshold of 0.50 and is not a viable identity either.

### 5.5 Multi-actor ambiguity

Attribution is frequently ambiguous, and the framework does not require ambiguity to be resolved before it can proceed. It requires ambiguity to be **handled** rather than collapsed.

| Rule | Statement |
| --- | --- |
| **AMB-1** | The assessment carries a distribution over candidates, each with its own `c`, its own bases, and its own contradicting evidence. A single name with no alternatives is not an attribution assessment (`INT-1`). |
| **AMB-2** | Where two or more candidates lie within **0.10** of the highest, the assessment is marked **ambiguous** and the marking is displayed on the card. |
| **AMB-3** | While an assessment is ambiguous, the effective confidence for any countermeasure whose attribution dependency is *Identity* is capped at **0.49**, which is below the C0 threshold of 0.50. `AD-9` therefore fails for such countermeasures, and the only admissible candidates are those whose dependency does not require identity. |
| **AMB-4** | The ambiguity is resolved when a basis that **discriminates between the named candidates** is available at tier 1. The resolving basis is recorded by name. Where a discriminating basis exists at tier 2 or below, the assessment remains ambiguous and the cap at AMB-3 applies. |
| **AMB-5** | The operator may not resolve an ambiguity by assertion. A candidate may be nominated as the working attribution for the purpose of planning only, marked as such, and the countermeasure set is then constrained as under AMB-3. |
| **AMB-6** | Where an assessment is ambiguous and the operator proceeds with an identity-independent countermeasure set, the card records that the action was taken under acknowledged attribution ambiguity, and the residual risk is computed at the **lower** of the competing candidates' `c` values. |
| **AMB-7** | "AI-driven" is not a candidate. A finding that the traffic is machine-generated is a classification and not an attribution, and supports no countermeasure against a third party (`INT-6`). |

### 5.6 The INT-3 thresholds

The minimum attribution confidence required to act rises with the collateral class of the countermeasure. This table is the master design's `INT-3` and is restated here because `AD-9` evaluates against it.

| Collateral class | Minimum attribution confidence to act | Additional requirement |
| --- | --- | --- |
| **C0** | 0.50 | Logged. |
| **C1** | 0.70 | Logged; reviewed by a second operator. |
| **C2** | 0.85 | Logged; approved at the depth for the class; the card must record the alternative attribution considered. |
| **C3** | 0.95 | Logged; approved at executive depth; external authority where required; refusal to proceed if the threshold is not met, irrespective of operational pressure. |

**Interaction with attribution dependency.** The threshold that applies is the one for the **countermeasure's collateral class**, and it applies only where the countermeasure's attribution dependency requires identity or external attribution. A countermeasure with a dependency of *None*, *Behavioural*, or *Class* is evaluated on class confidence rather than on identity confidence, and the `INT-3` table — which scales with the collateral class and governs identity attribution — does not apply to it. A separate floor does: `CLASS_CONFIDENCE_FLOOR`, at 0.50, which does not scale, because such a countermeasure acts on the estate rather than on a party.

---

## 6. Confidence Propagation

### 6.1 The rule

A derived claim is never more confident than its least confident input, less a declared penalty for the assumptions in the derivation (`INT-9`).

```
c_derived = max(0.00, min over leaf inputs of (c_input) − p)
```

where `p` is the **derivation penalty** declared for the chain. The penalty is not implicit and is not computed by the engine: the analyst declares which kind of inference was made, and the engine verifies the declaration against the chain structure, and refuses a derived claim whose declared penalty is lighter than the chain supports.

**The penalty for a chain is the highest penalty encountered on it, not the sum.** A chain of two single-step inferences carries the single-step penalty of 0.05, not 0.10. The multi-step penalty of 0.10 exists for a derivation that is not adequately described as a single step. The rule is stated here because the alternative — summing penalties — produces values that collapse to zero on long chains and would make long derivations unusable rather than merely cautious.

**Chain length** is the number of inferential steps from the nearest leaf observation to the claim. It is recorded and displayed on every derived claim, because chain length and the confidence it produces are the same fact seen from two directions.

### 6.2 The derivation-penalty table

| Derivation type | Penalty | Applies where |
| --- | --- | --- |
| **Direct observation** | **0.00** | The claim is the observation. Nothing is inferred between the world and the claim. |
| **Single-step inference** | **0.05** | One inferential step from an observed input, with no intermediate unlabelled claim and no coverage gap. |
| **Multi-step inference** | **0.10** | Two or more inferential steps, each individually labelled, where the result is not adequately characterised as a single step. |
| **Inference across a gap in telemetry** | **0.15** | The derivation crosses a period, a source, or a coverage boundary where the evidence is known to be incomplete, including a source that went dark. |
| **Inference from an unclassified input** | **0.20** | The derivation depends on a signal whose AAT category has not been established, or whose classification is itself in dispute. |

**Interaction.** Where a chain exhibits more than one derivation type, the highest applicable penalty governs (`p = max`). A derivation that crosses a telemetry gap **and** rests on an unclassified input carries 0.20, not 0.35.

**No penalty is applied to the observation itself.** A claim labelled Fact that is a direct observation carries the observer's confidence with no deduction. The penalty attaches to the step from the observation to the claim about the world.

**The subtraction is a deduction, not a multiplication.** The rule is `c_derived = c_weakest − p`, as `INT-9` states it, and not `c_weakest × (1 − p)`. The two forms agree at small penalties and diverge visibly at the larger ones: a leaf at 0.95 with a multi-step penalty of 0.10 gives 0.85 under the subtractive form and 0.855 under the multiplicative form, and the difference crosses the 0.85 threshold that `INT-3` sets for a C2 countermeasure. The subtractive form is normative. The reference implementation applies the subtractive form, and the divergence is closed; the closure is recorded at §14.4.

### 6.3 Worked examples

#### Chain 1 — A well-supported attribution

| Step | Claim | Label | Tier | Confidence | Derivation | Penalty | Chain length |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A sampled batch of tool responses contained text addressed to the assistant's tool layer. | Fact | 1 | 0.95 | Direct observation | 0.00 | 0 |
| 2 | That text was placed in the tool output by a party other than the operator's own content pipeline. | Interpretation | 1 | 0.90 | Single-step inference from step 1 | 0.05 | 1 |
| 3 | The placing party is candidate A. | Estimate | 1 | 0.85 | Multi-step inference from steps 1–2 | 0.10 | 2 |

**Resulting attribution confidence: c = 0.85.** The chain carries 0.85, 0.90, and 0.85.

#### Chain 2 — The same observation, across a gap in telemetry

The same leaf observation, but the origin channel of the tool-output path was degraded for a forty-minute window during the campaign, and the degradation was detected only afterwards.

| Step | Claim | Label | Tier | Confidence | Derivation | Penalty | Chain length |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | A sampled batch of tool responses contained text addressed to the assistant's tool layer. | Fact | 1 | 0.95 | Direct observation | 0.00 | 0 |
| 2 | The text was placed in the tool output by a party other than the operator's own content pipeline. | Interpretation | 1 | 0.80 | Inference across a gap in telemetry | 0.15 | 1 |
| 3 | The placing party is candidate A. | Estimate | 1 | 0.80 | Inference across a gap in telemetry | 0.15 | 2 |

**Resulting attribution confidence: c = 0.80.** The observation is identical and just as reliable. The confidence in the conclusion has fallen by 0.05, and the reason is not the observation but the **gap in the chain**.

**Consequence for the decision.** At `c = 0.80` the case meets the C1 threshold of 0.70 and fails the C2 threshold of 0.85. A C1 countermeasure is available; a C2 countermeasure is not, and the margin is 0.05.

#### Chain 3 — An unclassified input

A telemetry anomaly is reported by a single analyst, with no established category and no confirmed provenance.

| Step | Claim | Label | Tier | Confidence | Derivation | Penalty | Chain length |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | An unexplained anomaly was observed in the session telemetry. | Fact | 3 | 0.55 | Direct observation | 0.00 | 0 |
| 2 | The anomaly corresponds to AAT-4 exploitation technique activity. | Interpretation | 3 | 0.35 | Inference from an unclassified input | 0.20 | 1 |
| 3 | The activity is attributable to candidate A. | Estimate | 3 | 0.25 | Multi-step inference from steps 1–2 | 0.10 | 2 |

**Resulting attribution confidence: c = 0.25.** This fails even the C0 threshold of 0.50, and no identity-dependent countermeasure is available. The route to action is a countermeasure with a dependency of *None* or *Class*, applied to the class of activity rather than to the actor (`INT-4`).

### 6.4 The consequence the rule exists to produce

**A strong observation can carry a weak decision if the chain to the decision is long.** This is the entire purpose of the rule, and it is worth stating plainly because it runs against the intuition that more evidence means more confidence.

In Chain 1 and Chain 2 the leaf observation is identical: a direct observation at confidence 0.95, tier 1, in the operator's own hands. The two chains differ only in the length and character of the path from that observation to the decision. The decisions they support differ: one reaches 0.85 and supports a C2 countermeasure; the other reaches 0.80 and does not. The model exposes the chain length so that an operator, and a reviewer, can see *why* the two decisions differ rather than being told only that they do.

Three practical consequences follow, and each is a requirement of the implementation:

1. **The chain is displayed with the claim.** A derived claim is shown with its leaf observations, the number of steps between, the penalty at each step, and the resulting confidence. A claim shown without its chain is a claim whose confidence cannot be checked.
2. **The chain is counted, not just its endpoint.** A confidence of 0.62 may rest on a single well-evidenced step or on six weak ones, and the two are different assessments. Chain length is recorded separately from the confidence value and is displayed separately.
3. **Long chains are a finding, not a detail.** Where a decision rests on a chain of three or more steps, the card records that fact, because the most common way a well-evidenced observation produces a wrong decision is through a chain that nobody examined.

**Propagation is also the rule that governs the combination of countermeasures.** A countermeasure set's confidence is the weakest member's confidence, for the same reason and by the same mechanism (§8.4, §10.4).

---

## 7. Effective Threat, Expected Effectiveness, and Residual Risk

### 7.1 Effective threat

**S_eff = S × c**

`S` is what the activity is worth. `S_eff` is what is attributable to the adversary actually being answered. It is the quantity the escalation ladder is applied to, and it is the quantity that is reduced by a countermeasure.

The multiplication is a modelling convenience, not a claim that threat and attribution are independent in a statistical sense. They are not: evidence that raises `L` typically also bears on `c`. The formula is used because it is legible under pressure and because its behaviour is easy to reason about, and the record states the components separately so that a reviewer can see what the multiplication produced. The independence assumption is registered as a limitation at §16 (`LIM-DS2`).

### 7.2 Expected effectiveness and its confidence

**e** is the expected proportion of the effective threat that the selected countermeasure set neutralises, **if it achieves its intended effect**, in [0.0, 1.0].

Three things must be kept apart, because conflating them is the most common way an over-confident number is produced:

| Quantity | Question it answers | Typical source |
| --- | --- | --- |
| **e** | *If it works, how much of the threat does it remove?* | The countermeasure's residual-risk reduction band in the catalogue, adjusted on the card for the specific instance |
| **q** | *How confident are we that it works at all?* | The evidence basis for the countermeasure's effectiveness, in the operator's own estate or otherwise |
| **The realised reduction** | *What actually happened?* | The effectiveness assessment at `G-6`, not the estimate |

The catalogue records the first of these as a band with an evidence basis and a confidence, and expressly does not supply the second for any particular case; the card's own effectiveness assessment supplies it. A figure taken from the catalogue without a card-level assessment is not an `e` for the purposes of this model (catalogue `CM-7`).

### 7.3 Residual risk

**R = S_eff × (1 − e)**

Residual risk is the number the operator is accountable for. It is displayed on the card at every stage, and it is the figure carried into the after-action report.

`R` is expressed in the same units as `S` and `S_eff`, which are themselves ordinal (§4.1). The quantity is comparable across cards and is not a probability.

### 7.4 The display rule for effectiveness and its confidence

**A high-effectiveness, low-confidence measure must not be shown as a certainty.**

*Expansion.* Where a countermeasure is assessed at a high `e` and a low `q`, the operator is being asked to accept a large reduction in risk that may not occur. Presenting that reduction as a bare figure is a misrepresentation even when every input is correctly stated, because the reader of a bare figure has no way to know it is contingent.

**The uncertainty band.** Where a countermeasure's effectiveness is carried with a confidence, the residual risk is displayed as a **range** rather than a point. The band is derived by the declared display convention:

```
e_low  = max(0.00, e − (1 − q) / 2)
e_high = min(1.00, e + (1 − q) / 2)
R_high = S_eff × (1 − e_low)
R_low  = S_eff × (1 − e_high)
```

**This band is a display convention for communicating uncertainty. It is not a statistical confidence interval and must not be reported as one.** Its purpose is to prevent a point estimate from reading as a certainty. Where a deployment is reviewed by an auditor, the underlying `e` and `q` and their bases are what is examined.

**Mandatory presentation rule.** Where `e ≥ 0.70` and `q < 0.50`, the countermeasure is displayed with an explicit **unconfirmed effectiveness** marker, and the residual risk is displayed as a range. Where `q < 0.30`, the countermeasure is not presented as a risk-reduction measure at all, but as a measure whose effect is unestablished, and the card records the decision to use it in those terms.

**Consequence for authorisation.** A high-`e`, low-`q` countermeasure may be selected; the framework does not forbid acting on an uncertain measure. What it forbids is the presentation of the measure's benefit as though it were established. The approver at `G-4` sees the band, the `q`, and the `e` basis, and the approval is made in the knowledge that the reduction may not materialise.

### 7.5 Residual risk against the risk of inaction

**R_inaction = S_eff × (1 − e₀)**, where `e₀` is the expected effectiveness of the **current baseline posture** — the defences already in place, before any countermeasure under consideration. Where the baseline is treated as ineffective, `e₀ = 0` and `R_inaction = S_eff`.

Both figures are on the card (`OP-4`). A card that carries only the risk of acting is an incomplete assessment, and the master design names it as the most common way a legitimate operation goes wrong in practice: the countermeasure is judged against a straw man of inaction.

**The comparison is informational.** The model computes both figures and displays both. It does **not** compute a verdict of "proceed" or "do not proceed", and the interface must not present the comparison as a recommendation. The judgement is the operator's, and the approver's at `G-4`; the model's contribution is to make sure that the comparison is complete.

Three outcomes are legitimate, and the model must be able to present all three without favouring one.

#### Case 1 — Doing nothing is worse

`S_eff = 12.0`. Baseline posture `e₀ = 0.20`. Selected countermeasure set at `e = 0.70`, `q = 0.75`, collateral class C1 (`r = 0.25`).

| | Value |
| --- | --- |
| `R_inaction` | 12.0 × (1 − 0.20) = **9.60** |
| `R_action` | 12.0 × (1 − 0.70) = **3.60** |
| Reduction | **6.00** |
| Collateral exposure | 0.25 |
| Effectiveness confidence | 0.75 |

The action removes six units of effective threat for a C1 exposure, against a baseline posture that is already holding the line. The argument for acting is available and the operator records it.

#### Case 2 — Doing nothing is better

`S_eff = 4.0`. The baseline posture is already strong: `e₀ = 0.75`. The proposed countermeasure is effective but carries a material collateral exposure: `e = 0.85`, `q = 0.60`, collateral class C2 (`r = 0.60`).

| | Value |
| --- | --- |
| `R_inaction` | 4.0 × (1 − 0.75) = **1.00** |
| `R_action` | 4.0 × (1 − 0.85) = **0.60** |
| Reduction | **0.40** |
| Collateral exposure | 0.60 |
| Effectiveness confidence | 0.60 |

The action achieves a real reduction of 0.40 — and pays a C2 collateral exposure for it, against a baseline that is already holding residual risk at 1.00. The reduction is not obviously worth the exposure, and the operator may reasonably decline, record the decline, and pursue a C0 alternative or no action. The model presents both figures; it does not conclude.

#### Case 3 — The two are close

`S_eff = 8.0`. Baseline `e₀ = 0.60`. Proposed countermeasure `e = 0.72`, `q = 0.65`, collateral class C1 (`r = 0.25`).

| | Value |
| --- | --- |
| `R_inaction` | 8.0 × (1 − 0.60) = **3.20** |
| `R_action` | 8.0 × (1 − 0.72) = **2.24** |
| Reduction | **0.96** |
| Collateral exposure | 0.25 |
| Effectiveness confidence | 0.65 |

The reduction is 0.96 against a residual of 3.20 — a difference of the same order as the residual itself. In this state the deciding considerations are not in the numbers at all: they are the reversibility of the countermeasure, the confidence in the baseline estimate, the operational cost of the alternative, and the judgement of the people involved. The model records the closeness rather than resolving it, and the card's decision entry is expected to say so.

---

## 8. Risk-Adjusted Priority

### 8.1 The formula

For ranking candidate countermeasures within a card:

**P = (S_eff / 20) × q × (1 − r)**

| Term | Definition | Range | Source |
| --- | --- | --- | --- |
| `S_eff / 20` | The effective threat, normalised by the maximum possible score. | [0.00, 1.00] | §7.1, computed |
| `q` | The confidence that the countermeasure achieves its intended effect. | [0.00, 1.00] | The card's effectiveness assessment, §7.2 |
| `r` | The collateral exposure of the countermeasure, normalised across the collateral classes. | [0.00, 1.00] | §8.2, from the catalogue entry |
| `P` | The ranking quantity. | [0.00, 1.00] | Computed |

### 8.2 The collateral exposure normalisation

**The normalisation used by this model is stated exactly, as follows:**

| Collateral class | `r` |
| --- | --- |
| **C0** | **0.00** |
| **C1** | **0.25** |
| **C2** | **0.60** |
| **C3** | **1.00** |

These four values are a **chosen normalisation**, adopted by this document as the definition of `r` for the purposes of `P`. They are not measured, not derived from any observation, and not a claim about the relative harm of the four classes. They are a stated convention so that the implementation can compute `P` identically wherever it is run, and they are subject to organisational review (§13.1). The choice is registered as a limitation at §16 (`LIM-DS5`).

**The consequence of this normalisation, stated plainly.** A C3 countermeasure has `r = 1.00` and therefore `(1 − r) = 0`, and therefore **`P = 0` for every C3 countermeasure, by construction.** This is deliberate. The normalisation makes the ranking collapse on the most exposed class rather than under-weight it, and it means that a C3 countermeasure can only ever be selected by the recorded human judgement of `STEP-4`, never by its rank. An operator who reaches a C3 countermeasure has argued for it, and the card must show the argument.

**The collateral class is not derived from `r`.** The class is constitutional; it determines the approval depth. `r` is a derived quantity used only in `P`. A change to `r` changes a ranking and changes nothing about what authority is required.

### 8.3 Worked example — ranking six candidates

A card at profile R4 with a C2 collateral ceiling and an effective threat of 12.0, so `S_eff / 20 = 0.60`. Six candidates, all admissible on that card. The `e` values sit inside the residual-risk reduction bands declared by the catalogue entries, and the `q` values are the card's own effectiveness assessments.

| Rank | Candidate | Class | Collateral | Reversibility | `q` | `e` | `e` confidence | `r` | `R` | `P` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `OCC-09` — output sanitisation and egress allow-listing | CM-B | C0 | Reversible | 0.85 | 0.30 | 0.70 | 0.00 | 8.40 | **0.510** |
| 2 | `OCC-10` — tool capability scoping and least privilege | CM-B | C0 | Reversible | 0.75 | 0.35 | 0.60 | 0.00 | 7.80 | **0.450** |
| 3 | `OCC-17` — egress control and network segmentation for agent workloads | CM-C | C0 | Reversible | 0.65 | 0.40 | 0.65 | 0.00 | 7.20 | **0.390** |
| 4 | `OCC-28` — decoy target deployment | CM-E | C1 | Reversible | 0.60 | 0.20 | 0.45 | 0.25 | 9.60 | **0.270** |
| 5 | `OCC-35` — egress denial and service suspension for adversary agent endpoints | CM-F | C2 | Low | 0.80 | 0.45 | 0.55 | 0.60 | 6.60 | **0.192** |
| 6 | `OCC-36` — agent termination and compute revocation | CM-F | C2 | None | 0.65 | 0.55 | 0.35 | 0.60 | 5.40 | **0.156** |

**Three things this table shows, and they are worth reading together.**

First, **`P` and `R` answer different questions and they disagree sharply.** Ranked by residual risk, the order is `OCC-36` (5.40), `OCC-35` (6.60), `OCC-17` (7.20), `OCC-10` (7.80), `OCC-09` (8.40), `OCC-28` (9.60). Ranked by priority, `OCC-09` is first and `OCC-36` is last. The countermeasure that leaves the least risk standing is the one the ranking puts at the bottom, because it is irreversible, it is the most exposed, and its effectiveness is the least well founded. This is not a defect in either quantity. `R` asks *how much risk would remain*; `P` asks *how should this queue be ordered, given what we believe about each measure and what it costs us to try*. An operator reading the ranking and an approver reading the residual risk are reading different questions, and the card shows both.

Second, **the deception entry ranks fourth on priority and last on residual risk**, and both of those positions are earned rather than arbitrary. Its effectiveness confidence is 0.45 — the lowest in the set — which reflects what the catalogue says about deception: the effect is per-adversary, expires as the adversary adapts, and is not a property of the countermeasure. Its collateral class is C1, which puts a 0.25 exposure against it and drops it a rank. Its own residual risk is the highest in the set because its expected effect is the lowest. An operator who prefers it on grounds the model cannot see — the intelligence yield, the fact that it produces no visible effect on the adversary's infrastructure — is entitled to select it and record why (`STEP-4`).

Third, **`P` does not order the set by risk reduction, and the operator is the one who decides.** The two most aggressive entries have the lowest priority and the lowest residual risk. Neither fact decides anything on its own, and the model emits no recommendation.

**On the C3 collapse.** No entry in the countermeasure catalogue at version 1.0 is classified C3; the maximum class in the catalogue is C2. The collapse described at §8.2 therefore cannot be exercised with a current entry, and it is stated as a property of the normalisation rather than as a ranking result:

| Notional candidate | Collateral class | `r` | `q` | `P` |
| --- | --- | --- | --- | --- |
| Any countermeasure deployed at C3 | C3 | 1.00 | any | **0.000** |

A deployment takes the class of its actual effect rather than the class of its catalogue entry, so a C3 deployment can arise from a C2 entry used in a way that produces a C3 effect. Where that happens, the entry disappears from the ranking entirely and can be reached only by recorded human judgement.

**On status.** A countermeasure whose catalogue status is *Withheld* is not selectable on any card and is refused by the engine; it does not appear in the ranking at all. Status governs availability, not priority. `OCC-38` is the current example: it is catalogued, classified, and described, and its use is withheld pending a determination that has not been made.

### 8.4 `P` is a ranking only

**`P` is never an authorisation, and a low `P` never prevents a high-`P` alternative from being chosen when the operator judges the trade-off differently and records why.**

*Expansion.* `P` is an ordering. It is used to present the candidate set, to sequence the discussion, and to make the decision legible to an approver who was not present. It is not used:

- to determine whether a countermeasure may be selected — that is the admissibility algebra (§9), and `P` is computed only for admissible candidates;
- to determine whether a countermeasure may be approved — that is the authorisation at `G-4` and the depth the collateral class requires;
- to determine whether a countermeasure may be dispatched — that is the control plane, against the current world state;
- to close a discussion — a lower-ranked countermeasure may be selected, and the interface does not prevent it.

**Combination.** Where a set of countermeasures is selected, the set's `q` is the **weakest member's** `q` (the confidence-propagation rule of §6.1 applied to a set rather than a chain) and the set's `r` is the **most exposed member's** `r`. This is consistent with the catalogue's `CM-5` rule, which makes a combination take the properties of its most restrictive member; that rule governs admissibility, and the rule here governs the ranking and the residual-risk estimate. The set's `e` is computed by the combination rule at §10.4.

---

## 9. The Admissibility Algebra

### 9.1 The general statement

A countermeasure **C** is admissible for card **K** under profile **P** if and only if **all** of `AD-1` to `AD-12` hold. Any single failure makes `C` inadmissible. There is no aggregation, no averaging, no weighting, and no judgement call inside the engine (`ROE-2`).

`AD-13` is a thirteenth condition, but it is a condition on the **reporting** of inadmissibility rather than a predicate on the countermeasure. It is stated after the conjunction semantics at §9.5.

### 9.2 Checkability classification

Every condition is classified as one of:

| Class | Meaning |
| --- | --- |
| **MACHINE** | Fully determined by declared card state. The engine evaluates it without human input. |
| **HYBRID** | Partially determined by declared state; the remainder requires an operator attestation recorded on the card. |
| **HUMAN** | Requires a human judgement that cannot be encoded. The machine can establish that the judgement has been made and recorded; it cannot make it. |

### 9.3 The conditions

#### AD-1 — Class and profile minimum

| | |
| --- | --- |
| **Predicate** | `C.class ∈ P.permittedActionClasses` **and** `P ≥ C.minimumProfile`. |
| **Inputs read** | `C.class` and `C.minimumProfile` (catalogue entry); `P.permittedActionClasses` and the profile's ordinal (constitutional instrument and catalogue). |
| **Checkability** | **MACHINE** |
| **Failure message** | `AD-1 — class CM-E is not among the action classes permitted at profile R2, which permits CM-D Observe within an isolation boundary and CM-C Contain. Margin: 1 profile level (CM-E is permitted at R3). The countermeasure's declared minimum profile is R3 and the card is at R2. To admit: escalate to a profile that permits the class, obtain a new or amended engagement authorisation, and raise a new card. The permitted class set and the declared minimum profile are properties of the profile and of the countermeasure and are not alterable on a card.` |

**The permitted action classes.** These are the constitutional instrument's, and the constitutional instrument governs:

| Profile | Permitted action classes | Maximum collateral class | Maximum autonomy class |
| --- | --- | --- | --- |
| **R0** Observe | CM-A Detect; CM-B Harden | C0 | AC-1 |
| **R1** Shield | CM-A Detect; CM-B Harden; CM-C Contain; CM-D Observe; CM-G Recover; CM-F Disrupt where the effect is exerted at the operator's own perimeter | C0 | AC-2, and AC-4 read-only on the operator's own estate and on sources already lawfully observed |
| **R2** Trap | CM-A Detect; CM-B Harden; CM-C Contain; CM-D Observe within an isolation boundary; CM-G Recover | C1 | AC-3 |
| **R3** Deceive | CM-A Detect; CM-B Harden; CM-C Contain; CM-D Observe; CM-E Deceive; CM-G Recover | C1 | AC-3 |
| **R4** Disrupt | CM-A Detect; CM-B Harden; CM-C Contain; CM-D Observe; CM-E Deceive; CM-F Disrupt; CM-G Recover | C2 | AC-3 |
| **R5** Neutralise | CM-A Detect; CM-B Harden; CM-C Contain; CM-D Observe; CM-E Deceive; CM-F Disrupt at C3; sustained containment; CM-G Recover | C3 | AC-3 |

**The two limbs.** The class limb asks whether the countermeasure is of a kind the profile permits at all. The minimum-profile limb asks whether this particular countermeasure carries a floor above the profile in force; the catalogue's per-entry minimum is never lower than the class minimum, and it is the tighter constraint where it applies. The engine evaluates both and reports whichever fails. Where the two limbs disagree with each other — a catalogue entry whose declared minimum profile is lower than the profile in whose permitted action classes its class appears — the entry fails on the class limb, and the disagreement is a defect to be raised against the catalogue rather than something for the card to resolve.

**A recorded divergence.** The reference implementation's `_ROE_PERMITTED_CLASSES` in `impl/caos/vocab.py` sets materially wider class sets than the constitutional instrument at R0, R1, R2, R3, and R4. The implementation's sets were widened relative to the constitutional instrument's permitted action classes at R2 and R3, where CM-F Disrupt was available; that divergence is closed, and the implementation now carries the constitutional instrument's classes exactly. The constitutional instrument governs, and the implementation must be corrected to it. The divergence is recorded at §14.4 and in the register at §15.

#### AD-2 — Collateral class against the card ceiling

| | |
| --- | --- |
| **Predicate** | `ordinal(C.collateralClass) ≤ effectiveCeiling`, where `effectiveCeiling = min(K.collateralCeiling, P.maxCollateral)` and C0 < C1 < C2 < C3. The class of the deployment governs, not the class of the catalogue entry, because the class is a property of the effect as actually deployed. |
| **Inputs read** | `C.collateralClass` (the class of the deployment as configured); `K.collateralCeiling`; `P.maxCollateral`. |
| **Checkability** | **MACHINE** |
| **Failure message** | `AD-2 — collateral class C2 exceeds the effective ceiling C1 (card ceiling C1, profile ceiling C1). Margin: 1 class. To admit: raise the card's collateral ceiling to C2 by amending the engagement authorisation and raise a new card at the depth C2 requires; the class follows the actual effect and cannot be lowered by assertion.` |

#### AD-3 — Reversibility against the card requirement

| | |
| --- | --- |
| **Predicate** | `C.reversibility ≥ K.requiredReversibility` on the four-point scale **Reversible → Reversed → Low → None**, in which a **higher** value is **more** reversible. The canonical encoding is `REVERSIBLE = 3`, `REVERSED = 2`, `LOW = 1`, `NONE = 0`, and the comparison is `value(C) ≥ value(K)`. Where `C.reversibility` is *Low* or *None* and the card does not carry the irreversibility argument required by `ROE-7`, the condition additionally fails. |
| **Inputs read** | `C.reversibility` (catalogue entry); `K.requiredReversibility`; the presence of a `ROE-7` argument on the card. |
| **Checkability** | **HYBRID** — the comparison is machine-performed; the `ROE-7` argument is a human attestation, and the determination of whether a stated reversibility is accurate in the specific deployment is a human judgement. |
| **Failure message** | `AD-3 — reversibility Low does not meet the required reversibility Reversed. Margin: 1 step on the reversibility scale. To admit: the card must record the ROE-7 argument that no reversible countermeasure achieves an acceptable reduction in residual risk, and the approver must confirm the argument explicitly. The reversibility of the countermeasure cannot be altered on the card.` |

**Note on the comparison direction.** The scale is ordered from most reversible to least, and the encoding used by the constitutional instrument and the reference implementation assigns the **higher** value to the **more** reversible state. "At least as reversible as required" is therefore the greater-or-equal comparison. The two ways of getting this wrong are to compare in the opposite direction, and to encode the scale so that the most reversible state holds the lowest ordinal while still comparing with `≥`. The test suite at §14 must cover both.

#### AD-4 — Target set containment

| | |
| --- | --- |
| **Predicate** | `C.targetSet ⊆ K.authorisedTargetSet`. |
| **Inputs read** | `C.targetSet` (catalogue entry, resolved for the deployment); `K.authorisedTargetSet`. |
| **Checkability** | **MACHINE** |
| **Failure message** | `AD-4 — target "adversary-hosting-provider:eu-west" is not in the card's authorised target set. Margin: 1 target of 3 in the countermeasure's target set. To admit: remove the target from the deployment's scope, or raise a new card for the extended target set under OP-2; a material change of target set is a new card, not a field edit.` |

#### AD-5 — Third-party exclusion, authority not held, and the shared-tenancy test

| | |
| --- | --- |
| **Predicate** | `C.thirdPartyDependencies` is empty, **or** every named third party carries a specific per-target written authorisation on the card, **and** the shared-tenancy assessment required by `AUTH-8` is recorded on the card: who else depends on the affected infrastructure, what their interest in it is, and the expected harm to them. The condition additionally fails where `C.status` is **Withheld**, because the determination withheld — typically a legal or contractual one — has not been made and cannot be made by the card. |
| **Inputs read** | `C.thirdPartyDependencies` (catalogue entry, resolved for the deployment); `C.status`; `K.perTargetAuthorisations`; `K.sharedTenancyAssessment` (attestation). |
| **Checkability** | **HUMAN** |
| **Failure message** | `AD-5 — the countermeasure affects third-party infrastructure ("hosting-provider:eu-west") with no per-target authorisation on the card, and no shared-tenancy assessment is recorded. Margin: 1 third party. To admit: either select an identity-directed alternative, or obtain specific per-target written authorisation and record the shared-tenancy assessment; the engagement authorisation's general scope does not satisfy this condition.` |

**Why this condition is human.** The machine can establish that a dependency is named and that a per-target authorisation is present or absent. It cannot establish that the expected harm to an identified third party is acceptable, that their interest in the infrastructure has been correctly characterised, or that the countermeasure's effect falls where the dependency says it does. `AUTH-8` requires the operator to answer these questions, and the answers are recorded on the card. The condition is classified HUMAN because the substantive determination cannot be encoded; the machine check is limited to establishing that the determination has been made and recorded, and that no withheld entry has been proposed.

#### AD-6 — No targeting of human beings

| | |
| --- | --- |
| **Predicate** | `C.objectClass ∉ {human}`, and where the countermeasure's effect is indirect — where human beings are affected without being the object — the operator has attested the determination. |
| **Inputs read** | `C.objectClass` (catalogue entry); the presence of the operator's attestation where the effect is indirect. |
| **Checkability** | **HYBRID** — the declared object class is machine-checked; the determination of indirect effects is a human judgement. |
| **Failure message** | `AD-6 — the countermeasure's declared object class is "human". Margin: none — this condition is not satisfiable by adjustment, and there is no value of any other field that would make it admissible. To admit: the countermeasure must be withdrawn. (Constitutional conduct constraint CON-4.)` |

#### AD-7 — Autonomy class

| | |
| --- | --- |
| **Predicate** | `ordinal(C.autonomyClass) ≤ ordinal(K.autonomyClass)`, where AC-0 < AC-1 < AC-2 < AC-3 < AC-4, **and** `ordinal(C.autonomyClass) ≤ ordinal(P.maxAutonomy)`, **and** the card carries a live autonomy grant at that class. |
| **Inputs read** | `C.autonomyClass` (catalogue entry); `K.autonomyClass`; `P.maxAutonomy`; the presence of a grant with envelope, budget, expiry, automatic reversion, and on-call rota. |
| **Checkability** | **MACHINE** |
| **Failure message** | `AD-7 — autonomy class AC-3 exceeds the card's AC-2. Margin: 1 class. To admit: raise the card's autonomy class, which requires the AC-3 grant fields to be populated and the abort channel to have been demonstrated before the operation begins (HITL-3); a grant may not be created by the dispatch request. Note that AC-4 above collateral class C0 is not approvable at any profile.` |

#### AD-8 — Effectiveness confidence

| | |
| --- | --- |
| **Predicate** | `C.q ≥ K.minimumQ`. |
| **Inputs read** | `C.q` (the confidence attached to the card's effectiveness assessment for this countermeasure); `K.minimumQ`. |
| **Checkability** | **MACHINE** |
| **Failure message** | `AD-8 — confidence in the stated effectiveness 0.45 is below the card's minimum 0.60. Margin: 0.15. To admit: raise the confidence, which requires evidence and not argument; or lower the card's minimum, which the approver must justify and record. The effectiveness figure itself may not be raised to satisfy this condition.` |

#### AD-9 — Attribution dependency

| | |
| --- | --- |
| **Predicate** | Where `C.attributionDependency ∈ {Identity, External}`: `c(card) ≥ INT-3 threshold for C.collateralClass` **and** the assessment is not ambiguous under §5.5. Where `C.attributionDependency ∈ {None, Behavioural, Class}`: the condition is satisfied by category confidence and the INT-3 threshold does not apply. |
| **Inputs read** | `C.attributionDependency`; `C.collateralClass`; the card's attribution confidence `c`; the ambiguity flag on the attribution assessment; the candidate distribution. |
| **Checkability** | **MACHINE** |
| **Failure message** | `AD-9 — the countermeasure depends on identity and the card's attribution confidence is 0.62, below the C1 threshold of 0.70. Margin: 0.08. To admit: raise the attribution confidence, which requires new evidence at a higher tier or a resolving basis for the ambiguity, or select a countermeasure whose attribution dependency does not require identity. This condition is not satisfiable by argument.` |

#### AD-10 — Deconfliction

| | |
| --- | --- |
| **Predicate** | `deconflictionMap.intersections(C) = ∅`: no live legitimate operation is materially affected by the countermeasure's intended effect. |
| **Inputs read** | The live operations map; the countermeasure's intended effect and blast radius. |
| **Checkability** | **HYBRID** — the map comparison is machine-performed where the map is complete and current; where the map is degraded, where the effect is indirect, or where the conflict is a matter of degree, the determination is a human judgement recorded on the card. |
| **Failure message** | `AD-10 — the countermeasure's intended effect intersects live operation OP-LIVE-2 (scheduled 18:00–23:00 local). Margin: 1 conflict of 3 live operations. To admit: reschedule the live operation, narrow the countermeasure's scope to exclude the conflict, or record the live operation owner's agreement on the card.` |

#### AD-11 — Autonomy budget and envelope

| | |
| --- | --- |
| **Predicate** | `C.autonomyCost ≤ K.remainingAutonomyBudget` **and** `C.autonomyEnvelope ⊆ K.autonomyEnvelope` **and** `C.expectedRuntime ≤ K.grantRemainingTime`. |
| **Inputs read** | The countermeasure's declared autonomy cost, envelope, and expected runtime; the card's remaining budget, envelope, and grant expiry. |
| **Checkability** | **MACHINE** |
| **Failure message** | `AD-11 — the countermeasure requires 4 autonomy units against 2 remaining on the card. Margin: 2 units. To admit: release other autonomy consumption, or raise a new grant for the enlarged envelope under a fresh authorisation. Budget may not be exceeded by a dispatch.` |

#### AD-12 — The non-weaponisation boundary

| | |
| --- | --- |
| **Predicate** | `C` falls within the boundary stated at master design §3.4 and §7.3: it does not use one AI system to attack, degrade, or destroy another AI system, its weights, or its training data; it does not target human beings; it does not act on infrastructure the operator does not own without per-target authorisation; its primary effect is not to make the adversary's model worse in a way that harms an uninvolved third party; and it does not conceal the operation from the authority that authorised it or from persons affected in a way carrying legal or safety consequences. |
| **Inputs read** | The countermeasure's declared direction of effect, procedure summary, and target; the catalogue's declaration of conformity; the operator's attestation where the declaration is absent. |
| **Checkability** | **HYBRID** — the catalogue declaration is machine-checked; the boundary question, where the effect is indirect or the declaration is absent, is a human judgement. |
| **Failure message** | `AD-12 — the countermeasure's declared effect is to degrade the adversary's model, and the catalogue carries no declaration of conformity with the non-weaponisation boundary. Margin: not applicable — the condition is binary. To admit: the operator must attest the boundary analysis, including that no uninvolved third party is harmed, or the countermeasure must be withdrawn.` |

### 9.4 Summary of the conditions

| Condition | Short title | Predicate in one line | Checkability | Where the human element lies |
| --- | --- | --- | --- | --- |
| **AD-1** | Class and profile minimum | The countermeasure's class is permitted at the profile in force, and its declared minimum profile is at or below it | **MACHINE** | — |
| **AD-2** | Collateral class ceiling | The class of the deployment as configured is at or below the effective ceiling | **MACHINE** | — |
| **AD-3** | Reversibility floor | The countermeasure is at least as reversible as the card requires, and the irreversibility argument is recorded where the countermeasure is `Low` or `None` | **HYBRID** | The `ROE-7` argument, and the accuracy of the stated reversibility for the deployment |
| **AD-4** | Target containment | The countermeasure's target set is within the card's authorised target set | **MACHINE** | — |
| **AD-5** | Third-party exclusion and authority held | No third party is affected without per-target authorisation, the shared-tenancy assessment is recorded, and no withheld entry is proposed | **HUMAN** | The shared-tenancy assessment and the acceptability of the expected harm |
| **AD-6** | Human beings not the object | The countermeasure's object class is not human, and indirect effects have been attested | **HYBRID** | The determination of indirect effect on persons |
| **AD-7** | Autonomy class ceiling | The countermeasure's autonomy class is at or below the card's and the profile's, and a live grant exists | **MACHINE** | — |
| **AD-8** | Effectiveness confidence floor | The confidence in the stated effectiveness is at or above the card's minimum | **MACHINE** | — |
| **AD-9** | Attribution dependency satisfied | Where the countermeasure depends on identity or external attribution, the attribution confidence meets the `INT-3` threshold for the class and the assessment is not ambiguous | **MACHINE** | — |
| **AD-10** | Deconfliction passed | No live legitimate operation is materially affected | **HYBRID** | The determination of indirect or partial conflict, and where the map is degraded |
| **AD-11** | Autonomy budget available | The countermeasure's autonomy cost, envelope, and runtime fit the card's grant | **MACHINE** | — |
| **AD-12** | Non-weaponisation boundary | The countermeasure falls within the boundary at master design §3.4 and §7.3 | **HYBRID** | The boundary analysis where the effect is indirect or the catalogue's declaration is absent |
| **AD-13** | Inadmissibility is informative | Every refusal names the condition, the observed value, the required value, the margin, and the route to admission | **MACHINE** | — |

**Seven conditions are wholly mechanical, four carry a human element, and one is a reporting rule rather than a predicate.** The distribution is worth stating plainly, because it is the honest answer to the question "how much of this is automated?": the boundary checks are almost entirely mechanical, and the judgements that remain are judgements about effect and about harm — not about arithmetic.

### 9.5 The conjunction semantics

**All conditions must hold.** The admissibility predicate is the conjunction `AD-1 ∧ AD-2 ∧ … ∧ AD-12`. There is no aggregation, no averaging, no weighting, no trade-off between conditions, and no partial credit. A countermeasure that satisfies eleven conditions and fails one is inadmissible.

**No partial credit.** No countermeasure may be admitted on the strength of how well it does on the others. This is the property that makes the algebra an enforcement surface rather than a scoring function, and it is the reason the conditions are stated as predicates rather than as questions.

**All failures are recorded, not the first.** Every condition is evaluated for every candidate, and every failure is reported, not only the first encountered. An operator who is going to re-scope a countermeasure needs the whole set of what to change, and an approver needs to see that the failures are not a single marginal issue.

**A failure is reported with the specific condition and the specific margin.** Each failure record carries:

| Field | Content |
| --- | --- |
| The condition | The identifier of the condition that failed |
| The predicate, restated | The condition as it applied to this candidate |
| The observed value | The value the engine read |
| The required value | The value that would have satisfied the condition |
| The margin | The difference between the two, in the unit of the condition |
| The route to admission | What must change, and under whose authority |

**The margin is a fact about the card, not a recommendation.** A margin of 2 profile levels and a margin of 0.08 of attribution confidence are not comparable, and the interface must not present them as though they were. The margin tells the operator what the distance is; the route to admission tells the operator who can close it.

**Refusal is a successful control.** A refusal is not a failure of the system and is never treated as one (`ROE-2`). It is recorded, it is displayed, and it is the mechanism by which the operator learns what to change.

### 9.6 AD-13 — Inadmissibility is informative

**AD-13 — Inadmissibility is informative.** A rejected countermeasure is reported with the specific condition it failed and the specific value that would have made it admissible. This turns the refusal into guidance, and it is how an operator learns what to change rather than what to give up on.

*Expansion.* The engine's refusal message is part of the interface, not a log entry. It is presented in the countermeasure console alongside the surviving candidates, in the same surface, and it must contain, for each failed condition: the condition identifier, the observed value, the required value, the margin, and the route to admission. A refusal that says only "inadmissible" is a defect.

**Worked example of an informative refusal.** Candidate `OCC-35` (egress denial and service suspension for adversary agent endpoints) on the card `OC-EXAMPLE-014` of §10.7, which is at profile R2 with a C1 collateral ceiling, an AC-2 autonomy class, a *Reversed* reversibility requirement, and an attribution confidence of 0.62:

| Condition | Observed | Required | Margin | Route to admission |
| --- | --- | --- | --- | --- |
| **AD-1** | Class CM-F; declared minimum profile R4 | R2 permits CM-D Observe within an isolation boundary, and CM-C Contain | 2 profile levels | Escalate to R4, obtain a new or amended engagement authorisation, raise a new card. |
| **AD-2** | Collateral class C2 | Effective ceiling C1 | 1 class | Raise the card's collateral ceiling to C2 — director, legal contact, and asset owner — on a new card. |
| **AD-3** | Reversibility Low | Reversed | 1 step on the scale | Record the `ROE-7` argument, or lower the card's reversibility requirement by decision of the approver. |
| **AD-9** | Attribution confidence 0.62; dependency Identity | 0.85, the C2 threshold | 0.23 | New evidence at a higher tier, or a resolving basis for the ambiguity; otherwise select a countermeasure with a class or none dependency. |

**What the operator now knows.** Not "you cannot do this" but: this countermeasure is out of profile by two levels, out of ceiling by one class, one step less reversible than the card permits, and short of the attribution threshold by 0.23. Those are four different problems with four different owners, and two of them are closable by work rather than by argument. The third may not be closable at all, in which case the operator has a clear, recorded reason to choose a different route — and the card will show the rejected set with these reasons alongside the selected one.

**This is the mechanism by which the framework supports learning rather than abandonment.** A countermeasure that fails on `AD-9` by 0.23 today may be available tomorrow if the attribution assessment improves; the record shows the distance, not a wall.

---

## 10. The Selection Algorithm

The six steps below expand master design §6.5. The steps are sequential in the sense that each consumes the previous one's output; the gate that authorises the result of `STEP-4` is `G-4` in the mission lifecycle, and this document does not restate the gate.

### 10.1 STEP-1 — Generate candidates

**Candidates come from two sources, and both are recorded.**

**Source A — the catalogue, by technique binding.** Every countermeasure in `operational/countermeasure-catalogue.md` whose AAT technique bindings intersect the card's classification, is a candidate. The intersection is computed on the card's AAT categories, not on the technique library's finer granularity, because the catalogue binds at category level. A countermeasure whose entry carries the binding but whose preconditions are plainly not met in this estate is still a candidate; the precondition failure is reported as a rejection with a margin, because a candidate that was silently dropped leaves the operator unable to see that it was considered.

**Source B — operator proposals.** Any countermeasure the operator proposes explicitly enters the candidate set, whether or not it appears in the catalogue. A proposal carries the same attributes a catalogue entry carries — class, collateral class, reversibility, autonomy class, attribution dependency, target set, effectiveness assessment, and preconditions — and is subject to the same admissibility algebra. A proposal is not privileged by having been proposed, and it is not disadvantaged by not being in the catalogue; the attributes decide.

**Both sources are recorded separately on the card**, so that a later reviewer can see which candidates the model surfaced and which the operator brought.

### 10.2 STEP-2 — Filter on admissibility

Apply `AD-1` to `AD-12` to every candidate. Record every rejection with its reason, in the form required by §9.5 and `AD-13`. All failures for a candidate are recorded, not only the first.

The rejected set is **retained on the card**, not discarded. It is presented alongside the survivors, and the approver at `G-4` sees it. A card that presents only the admissible set has concealed the decision from the person authorising it.

### 10.3 STEP-3 — Rank the survivors

Rank the admissible candidates by `P` (§8), with the operator's stated preference as the tie-break. Present the **full ranked set including the rejected candidates and their reasons** (§9.6).

Two rules govern what may be presented here:

- The ranking is an ordering, and it is labelled as an ordering. It is not a recommendation, and it is not a filtered list of the admissible set by some other criterion.
- A candidate is not removed from the presentation because it ranks low. All admissible candidates are shown, in rank order, with their `P`, their `q`, their `r`, their `e`, and their `R`.

### 10.4 STEP-4 — Human selection

The operator selects, declines, or selects a combination. The selection, the reasoning, the alternatives considered, and any dissent are written to the card.

**The rule that a lower-ranked choice is permitted and must be recorded as a choice.** An operator may select a lower-ranked countermeasure. The interface does not prevent it, and the card records that it was a choice. A selection record for a candidate that is not rank 1 must carry the reason, in the words of the person who selected it, and must record the rank of the selected candidate. A card that records a selection without recording the rank is incomplete, because a reviewer cannot tell whether the top-ranked candidate was considered.

**Combination.** A combination of candidates is selected in the same way and is subject to the same recording requirement. For a combination:

| Property of the combination | Rule |
| --- | --- |
| Collateral class | The maximum of the members' collateral classes (catalogue `CM-5`) |
| Reversibility | The least reversible member's reversibility (catalogue `CM-5`) |
| Autonomy class | The highest member's autonomy class (catalogue `CM-5`) |
| Profile minimum | The highest member's profile minimum (catalogue `CM-5`) |
| Effectiveness `e` | `e_combined = 1 − Π(1 − e_i)` over the members, on the declared assumption that the members' effects are independent |
| Confidence `q` | The weakest member's `q` (§6.1, weakest-link rule) |
| Collateral exposure `r` | The most exposed member's `r` (§8.4) |

**The independence assumption.** The combination rule for `e` assumes that the members' effects are independent. Where they are not — where one member's effect depends on another's, or where they contend for the same resource — the rule overstates the combined reduction, and the card must state the dependence and, where the dependence is material, state the combined effectiveness as assessed rather than as computed. The independence assumption is an architectural assertion, registered at §15.

**Declining.** An operator may decline to select anything. The card records the decline, the reason, and the residual risk that is accepted, and the risk of inaction remains on the card. A card that records no selection and no decline is incomplete.

### 10.5 STEP-5 — Authorise

The selection and the risk assessment go to the approval depth required by the profile and the collateral class of the selected set. The approver sees, in one surface:

- the evidence and the attribution assessment, with its confidence and its chain;
- the threat score, decomposed, with each component's reasoning;
- the effective threat, the residual risk before and after, and the risk of inaction;
- the full ranked set of admissible candidates;
- the rejected candidates, with the condition and the margin for each rejection;
- the alternatives considered, including the counterfactuals at §12;
- the abort conditions and the pre-registered contingency;
- the card's own residual risk after the selection.

**Approval is at the depth the class requires, and depth is not a formality.** The required approval depth is set by the authorisation ladder in the constitutional instrument, which takes the **strictest of three** floors: the depth named by the profile ceiling, the depth named by the collateral class of the deployment, and the depth named by the autonomy class. Where two floors differ, the approval must satisfy both, and the instruments named by the target class are added to the required set. A C0 selection at team-lead depth is a different act from a C2 selection at director depth with a legal contact, and the record must show which depth was required and which was obtained.

**A lower-ranked or higher-exposure selection is not a reason to refuse approval.** The approver's task is to decide whether the recorded argument is sound, not to re-rank the candidates. Where the approver disagrees with the operator's choice, the disagreement is recorded as dissent, and the dissent does not by itself withhold the authorisation.

### 10.6 STEP-6 — Arm and dispatch

The card is armed with its autonomy envelope, budget, expiry, and abort conditions. The control plane **re-checks admissibility at dispatch time**, because card state and world state both change.

The dispatch re-check is a full evaluation of `AD-1` to `AD-12` against the current state, not a subset. Between `STEP-2` and `STEP-6` the world may have changed in ways that invalidate an earlier admissibility result: the profile may have been downgraded, the engagement authorisation may have expired or been revoked, the autonomy budget may have been consumed by another card, the deconfliction map may have changed, the attribution confidence may have decayed, a third-party authorisation may have lapsed, or an abort condition on another live card may have been triggered.

**A failed dispatch re-check is not an error.** It is the control working. The card returns to `STEP-4` with the failure recorded, and the operator re-selects, or raises an escalation request, or lets the card lapse. The re-check result and its outcome are written to the ledger.

### 10.7 Worked example

**The card.** `OC-EXAMPLE-014`, illustrative and fictional throughout. A card against a compromised internal agent workload.

| Field | Value |
| --- | --- |
| Card | `OC-EXAMPLE-014` |
| Profile in force | R2 (Trap) |
| Permitted action classes at R2 | CM-D Observe within an isolation boundary; CM-C Contain |
| Collateral ceiling | C1 |
| Autonomy class | AC-2 |
| Required reversibility | Reversed |
| Minimum `q` | 0.55 |
| Classification | AAT-4 (Exploitation and Discovery) and AAT-9 (Exfiltration and Covert Channels) |
| Attribution confidence `c` | 0.62, single candidate, not ambiguous |
| `S_eff` | 12.0 |
| Authorised target set | The operator's own estate, and the adversary's agent identity source at the operator's own identity service |
| Autonomy budget remaining | 4 units |
| Live operations | 3, from the deconfliction map |

**STEP-1 — Candidates.** Seven from the catalogue by AAT technique binding (AAT-4, AAT-9) and one operator proposal. The attributes are the catalogue entries' declared metadata.

| # | Candidate | Source | Class | Collateral | Reversibility | Autonomy | Dependency | Min. profile |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `OCC-21` — credential rotation and key revocation | Catalogue | CM-C | C0 | Reversed | AC-1 | Class | R1 |
| 2 | `OCC-18` — tool-call kill switch and agent session revocation | Catalogue | CM-C | C0 | Reversed | AC-2 | Behavioural | R1 |
| 3 | `OCC-17` — egress control and network segmentation for agent workloads | Catalogue | CM-C | C0 | Reversible | AC-2 | None | R1 |
| 4 | `OCC-03` — canary credential and honeytoken deployment | Catalogue | CM-A | C0 | Reversible | AC-1 | None | R0 |
| 5 | `OCC-28` — decoy target deployment | Catalogue | CM-E | C1 | Reversible | AC-1 | None | R3 |
| 6 | `OCC-34` — adversary credential invalidation at the identity source | Catalogue | CM-F | C2 | Low | AC-1 | Identity | R4 |
| 7 | `OCC-39` — revocation of third-party API credentials the adversary obtained | Catalogue | CM-F | C2 | Low | AC-0 | Identity | R4 |
| 8 | `PROP-01` — operator proposal: staged isolation of the compromised workload's outbound path, narrower in blast radius than a full segmentation change | Operator | CM-C | C0 | Reversible | AC-1 | None | R1 |

**STEP-2 — Admissibility filter.**

| Candidate | Result | Conditions failed | Detail |
| --- | --- | --- | --- |
| `OCC-21` | **Admissible** | — | All twelve conditions hold. |
| `OCC-18` | **Admissible** | — | All twelve hold; autonomy cost 4 units against 4 remaining. |
| `OCC-17` | **Admissible** | — | All twelve hold. |
| `PROP-01` | **Admissible** | — | All twelve hold. The proposal's attributes are recorded on the card alongside the catalogue's. |
| `OCC-03` | Rejected | **AD-1** | Class CM-A is not among the action classes permitted at R2, which permits CM-D Observe within an isolation boundary and CM-C Contain. Margin: 1 profile level — CM-A is permitted at R3. |
| `OCC-28` | Rejected | **AD-1** | Class CM-E is not among the action classes permitted at R2; the entry's declared minimum profile is R3. Margin: 1 profile level. |
| `OCC-34` | Rejected | **AD-1**, **AD-2**, **AD-3**, **AD-9** | CM-F at minimum profile R4 against R2 — margin 2 levels. Collateral class C2 against effective ceiling C1 — margin 1 class. Reversibility Low against required Reversed — margin 1 step. Identity dependency with `c = 0.62` against the C2 threshold of 0.85 — margin 0.23. |
| `OCC-39` | Rejected | **AD-1**, **AD-2**, **AD-3**, **AD-4**, **AD-5**, **AD-9** | As `OCC-34`, and in addition: the third-party API provider is outside the card's authorised target set — margin 1 target — and carries no per-target written authorisation, with no shared-tenancy assessment recorded — margin 1 third party. |

**The rejections are informative, and they are not equivalent.** `OCC-28` is one profile level away and is closable by escalation, and the operator may well want it. `OCC-34` is two profile levels, one class, one reversibility step, and a substantial attribution gap away. `OCC-39` adds a third party whose authorisation the operator does not hold and may not obtain. The card shows the difference, and the operator's decision is informed by it rather than by a uniform "no".

**STEP-3 — Rank the survivors.** `S_eff / 20 = 0.60`.

| Rank | Candidate | `q` | `r` | `P` | `e` | `e` confidence | `R` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `OCC-21` — credential rotation and key revocation | 0.80 | 0.00 | **0.480** | 0.35 | 0.70 | 7.80 |
| 2 | `PROP-01` — staged isolation of the outbound path | 0.75 | 0.00 | **0.450** | 0.45 | 0.65 | 6.60 |
| 3 | `OCC-18` — tool-call kill switch and agent session revocation | 0.70 | 0.00 | **0.420** | 0.45 | 0.70 | 6.60 |
| 4 | `OCC-17` — egress control and network segmentation | 0.65 | 0.00 | **0.390** | 0.40 | 0.65 | 7.20 |

**STEP-4 — Human selection.** The operator selects **`OCC-18` (rank 3)**, combined with `OCC-21` (rank 1). The record states, in the operator's words, that rotation alone leaves the compromised session live and therefore leaves the exfiltration path open, whereas the session kill switch stops the active session immediately while the rotation removes the credential beneath it; and that both are at C0 with no collateral exposure and no irreversibility, so the combination costs nothing that the individual entries do not.

**This is a lower-ranked choice and the card records it as one**, with the selected rank (3) stated, and with the rank-1 candidate recorded as considered. The interface did not prevent the choice and did not prompt for it in a way that implied the choice was wrong.

**Combined properties of the selected set**, by the combination rules at §10.4:

| Property | Value | Derivation |
| --- | --- | --- |
| Collateral class | C0 | Maximum of C0 and C0 (catalogue `CM-5`) |
| Reversibility | Reversed | Least reversible member's reversibility |
| Autonomy class | AC-2 | Highest member's autonomy class |
| Profile minimum | R1 | Highest member's profile minimum |
| `e` | **0.64** | `1 − (1 − 0.35)(1 − 0.45) = 1 − 0.3575` |
| `q` | 0.70 | Weakest member's `q` |
| `r` | 0.00 | Most exposed member's `r` |
| `R` | **4.29** | `12.0 × (1 − 0.6425) = 12.0 × 0.3575` |
| `P` | 0.420 | `0.60 × 0.70 × 1.00` |

**The independence assumption is recorded.** The two members are treated as independent in the combination rule. The operator records that `OCC-21`'s effect on the adversary's access and `OCC-18`'s effect on the live session are distinct and neither depends on the other, and that both are within the operator's own estate, so no interaction hazard applies.

**STEP-5 — Authorise.** The required depth is the strictest of three floors:

| Floor | Depth required |
| --- | --- |
| Profile ceiling R2 | Duty manager + legal contact |
| Collateral class C0 | Team lead |
| Autonomy class AC-2 | Team lead, with the authority to deploy at AC-2 on the operator's own estate |

**The strictest is duty manager + legal contact.** The approver sees the decomposition, the ranking, the rejected set with margins, the residual risks, the risk of inaction, and the abort conditions. The approval is recorded with the operator's selection, including the recorded reason for the lower-ranked choice.

**STEP-6 — Arm and dispatch, and the re-check.** The card is armed with its envelope, budget, expiry, and abort conditions. The control plane re-evaluates `AD-1` to `AD-12` against the current world state and finds that the autonomy budget has been reduced by another card's dispatch since `STEP-2`: `OCC-18`'s autonomy cost of 4 units now exceeds the 3 units remaining.

**The dispatch is refused.** `AD-11 — the countermeasure requires 4 autonomy units against 3 remaining on the card. Margin: 1 unit.` The card returns to `STEP-4`. The operator re-selects `OCC-21` alone, recording that the session kill switch could not be re-authorised within the remaining budget, and the card records that the residual risk is consequently higher than intended: `R = 12.0 × (1 − 0.35) = 7.80` rather than 4.29. The operator raises an escalation request for a fresh autonomy grant under `ROE-3`, and the after-action report records the budget contention as a finding.

**What the re-check was for.** Between `STEP-2` and `STEP-6`, the assessment that produced the admissibility result became stale. The re-check caught it, refused the dispatch, and forced a re-selection with a recomputed residual risk — before anything was armed. Had the re-check been omitted, the card would have dispatched a countermeasure beyond the budget it was granted.

---

## 11. What the Model Deliberately Does Not Do

Each entry states a limit and the reason for it. These are design commitments, not caveats to be traded against operational convenience.

| # | The model does not | Reason |
| --- | --- | --- |
| 1 | **Authorise anything.** | Authority exists only where a named human has granted it in writing (`AUTH-5`). A computed quantity cannot create a permission the operator does not hold, and a model that could would make the authorisation structure decorative. |
| 2 | **Predict adversary behaviour.** | Behaviour prediction requires the adversary's model, its state, its objective, and its access — none of which the operator holds, and some of which the adversary is actively concealing. The model scores observed activity; it does not forecast what comes next. Where a forward-looking judgement is required, it belongs to the hypothesis ladder, as a testable proposition with a disconfirming observation (`TAX-1`). |
| 3 | **Estimate intent.** | Intent is not observable from telemetry. The framework records what the adversary did and how the operator characterises it, and it demands a disconfirming observation for every hypothesis, so that a narrative which cannot be disproved cannot be entered and therefore cannot run. |
| 4 | **Resolve attribution.** | The model aggregates evidence into a stated confidence and a candidate distribution. It does not decide which candidate is correct, because that decision is the analyst's and the cost of getting it wrong is asymmetric (`INT-5`, `LIM-1`). |
| 5 | **Substitute for the operator's judgement.** | The model orders and bounds; `STEP-4` is a human act. A tool that made the decision would remove the human from the loop at exactly the point where the framework is weakest (`DO-1`, `HITL-2`). |
| 6 | **Produce a single number for an operator to accept.** | No single figure authorises anything (`SCORE-1`). Every quantity is decomposed, and every decomposition is separately contestable, so that a disagreement can be located in a component rather than being absorbed into a verdict on the whole assessment. |
| 7 | **Hide its inputs.** | Every number in the model is traceable to its components, its evidence, its tier, and its derivation chain. A model whose workings cannot be inspected cannot be contested, and a model that cannot be contested cannot be reviewed. |
| 8 | **Claim that its own outputs are calibrated.** | No component is a calibrated probability until calibration data exists (§13.3). The model's confidence values are estimates, used as ordering devices and threshold inputs, and are labelled as such wherever they are displayed. |
| 9 | **Conceal a rejected candidate.** | The rejected set, with the condition and the margin for each rejection, is on the card and in front of the approver. A decision recorded without the set of things not chosen is not a decision, it is an assertion. |
| 10 | **Act on its own output.** | The model computes. The operator selects. The authorisation approves. The control plane dispatches. The separation is structural, and the model is not given a path around it. |

---

## 12. Counterfactual Analysis

### 12.1 The requirement

The model must present **"if you do nothing"** and **"if you take the second-ranked option"** as explicit, computed alternatives, each with its own effective threat, residual risk, and collateral exposure, so that the operator sees the shape of the decision space rather than a single recommendation.

The requirement is not cosmetic. The most common failure in a decision-support system is that it produces one answer, that the answer is the product of a model the operator cannot inspect, and that the alternatives are never computed and therefore never compared. The operator's only basis for a real choice is what the model has not shown them.

### 12.2 What is computed for each alternative

| Quantity | For the inaction option | For each countermeasure option |
| --- | --- | --- |
| `S_eff` | Unchanged — the threat does not vary with the option | Unchanged — the threat does not vary with the option |
| `e` | `e₀`, the effectiveness of the current baseline posture | The countermeasure's assessed effectiveness, or `1 − Π(1 − e_i)` for a combination |
| `q` | The confidence in the baseline effectiveness assessment | The weakest member's `q` |
| `r` | 0.00 — no collateral exposure is created by inaction | The most exposed member's `r` |
| `R` | `S_eff × (1 − e₀)` | `S_eff × (1 − e)` |
| `P` | **Not applicable.** The inaction option is not a countermeasure and is not ranked. It is displayed in its own row, not in the ranking. | As computed |

**The inaction option is not in the ranking.** It is displayed beside it. Mixing "do nothing" into a priority ranking would put a non-countermeasure into a comparison of countermeasures, which is a category error, and it would lend the inaction option a rank that suggests a considered preference among the alternatives.

**The alternatives are computed with the same formulas as the selected option.** Not approximated, not summarised. An alternative whose `e` is unknown is displayed with the uncertainty band of §7.4 and with the "unestablished" marker where the band is too wide to be useful — not omitted, and not displayed as a better or worse option than one that has been assessed.

### 12.3 Worked table — three options on the card `OC-EXAMPLE-014`

`S_eff = 12.0` throughout. The figures are the card's own; the two countermeasure options are the top two admissible candidates by `P`, and the rejected candidates are addressed in §12.4.

| Option | `e` | `q` | `r` | `R` | `P` | What it buys | What it costs |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **Do nothing** (baseline posture only) | 0.20 | 0.55 | 0.00 | **9.60** | n/a | No collateral exposure, no operational commitment, no irreversibility. The card's live session is not disturbed. | The exfiltration path remains open. 9.60 of effective risk stands. Detection coverage does not improve, and the credential set remains valid. |
| **Option A** — `OCC-21` credential rotation and key revocation (rank 1) | 0.35 | 0.80 | 0.00 | **7.80** | 0.480 | The highest priority rank of the admissible set, the highest confidence in effectiveness, no collateral exposure, reversible. | The live session is not terminated. The credential is invalidated but the compromised process continues to hold whatever access it already holds. Residual risk remains at 7.80. |
| **Option B** — `OCC-18` tool-call kill switch and agent session revocation (rank 3) | 0.45 | 0.70 | 0.00 | **6.60** | 0.420 | The lowest residual risk of the three, and it stops the session rather than the credential. | A weaker confidence in effectiveness. The lowest priority rank of the three, and a residual risk still above half of the effective threat. |

**What the operator sees.** The three rows are close enough that no row is obviously correct, and the differences are of different kinds. Option A is the most *confident* and the cheapest and the most reversible, and the least effective. Option B is the most *effective* of the two and the least confident. Inaction is free and leaves 9.60 standing. An operator reading only `P` sees Option A at the top; an operator reading only `R` sees Option B at the top. The model shows both, and the choice is made on grounds the model does not contain — the analyst's judgement about the session, the operational cost of intervening, and what the evidence suggests is still running.

**The selected combination.** The set actually under consideration in §10.4 is `OCC-21` + `OCC-18`, with `e = 0.64`, `q = 0.70`, `r = 0.00`, and `R = 4.29`. It appears in the counterfactual table as its own row, because it is the option being decided on, and the operator must be able to see it against the alternatives without reconstructing it.

### 12.4 Rejected candidates in the counterfactual view

The alternatives that were **not** admissible are not part of the counterfactual comparison, because a counterfactual requires a course of action the operator could actually take. They are shown in the rejected set, with their conditions and margins, and the operator can see from the margins how far away they are — which is what makes a rejection actionable rather than final.

A candidate whose rejection is closable by a change the operator can make — a profile escalation, an attribution improvement, a third-party authorisation — appears in the counterfactual view **marked as conditionally available**, with the condition and the margin stated. It is not in the comparison, and it is not hidden.

### 12.5 The rule against a single recommendation

The model must not present a single recommended action. A ranked list with a counterfactual table is not a recommendation, and the interface must not render it as one. Concretely:

- The top-ranked candidate is not marked as recommended, highlighted as the expected choice, or presented as the default in a way that makes declining it the path of least resistance.
- The counterfactual table is presented beside the ranking, not behind a disclosure control.
- The word "recommend" is not used by the model. Where the framework expresses a preference — the environment-shaping preference (`CM-2`), containment before disruption (`CM-3`) — it is expressed as a doctrine rule with a recorded exception, not as a model output.

---

## 13. Calibration and the Limits of the Numbers

### 13.1 Thresholds are organisational settings, and they are reviewed

Every threshold in this model is a setting of the organisation, not a property of the model. The list below is not exhaustive of the settings the organisation will make, but it is the list this document governs.

| Setting | Where it is set | Review |
| --- | --- | --- |
| `L` band boundaries | This document, §4.2 | On revision of the taxonomy or of the observing-analogue baseline |
| The `INT-3` attribution thresholds (0.50 / 0.70 / 0.85 / 0.95) | Master design §5.3, restated at §5.6 | Annually, and on any change to the collateral classes |
| The derivation-penalty table | This document, §6.2 | Annually, and on any acquisition of calibration data |
| The `r` normalisation (0.00 / 0.25 / 0.60 / 1.00) | This document, §8.2 | Annually, and on any change to the collateral classes |
| The ambiguity threshold (0.10) | This document, §5.5 | Annually |
| The corroboration bonus and the contradiction deduction | This document, §5.3 | Annually, and on any acquisition of calibration data |
| The card's `minimumQ` and `requiredReversibility` | The card, set by the approving authority | Per card |

**Reviews are recorded.** A review produces a dated record of what was reviewed, what changed, and on what basis — and, where nothing changed, a record that the review occurred and found no reason to change. The set index §6 change-control table applies: a change to the admissibility algebra requires the document owner and the legal contact, and a versioning of the implementation.

### 13.2 What a confidence value actually is

Every confidence value in this model is a **stated estimate**, produced by a named analyst or by the operator, and is not independently calibrated. The card records, for each confidence value:

| Field | Content |
| --- | --- |
| The value | As used in the computation |
| The claim label | Fact, Estimate, Interpretation, Hypothesis, or Recommendation |
| The source reliability tier | 1 to 4 |
| The basis | The attribution basis, the observing analogue, the evidence reference, or the measurement, as applicable |
| The derivation | The chain, the step count, and the penalty applied at each step |
| The author and the date | The named person who stated it, and when |
| The review status | Whether it has been reviewed by a second operator, and by whom |

A confidence value presented without these fields is not accepted by the interface. This is the discipline of `INT-7` and `INT-8` applied to the numbers the model produces rather than only to the claims it displays.

### 13.3 No component is a calibrated probability until calibration data exists

This is stated plainly because the model's arithmetic invites the opposite conclusion.

| Component | Is it a calibrated probability? | What it actually is |
| --- | --- | --- |
| `L` | **No** | An analyst's estimate of a probability-like quantity, banded for legibility. The bands are ordinal. |
| `c` | **No** | A stated probability computed by a declared rule from evidence of a declared tier. The rule is transparent; the outputs are not verified against outcomes. |
| `e` | **No** | A design-intent band from the catalogue, or a card-level assessment, carried with a stated confidence. The catalogue's own figures are at evidence basis E4 with low confidence. |
| `q` | **No** | A stated confidence in a countermeasure's effectiveness, of the same character as `c`. |
| The derived-penalty table | **No** | A declared convention expressing caution about inference. It is not derived from measurement. |
| `r` | **Not applicable** | A stated normalisation of the collateral class. It is a convention, not an estimate of harm. |
| `P` | **Not applicable** | A ranking index. It is not a probability and is not a risk. |

**What follows from this.** The model is a *structuring* device: it makes the reasoning legible, locates the disagreement, and records the distance between the operator's position and the thresholds. It is not a *predictive* device, and no part of its output should be quoted as a frequency of anything. The framework's own limitation register states this as `LIM-2` in the master design, and this document does not soften it.

**What would change it.** Calibration requires recorded outcomes against recorded confidences, over a period long enough to be informative, with the population of decisions well enough defined to be meaningful. Until that exists, the thresholds at §13.1 are conventions, and the model's role is to make the conventions visible.

### 13.4 The requirements that govern this

The requirements at §14 that bear on calibration are `DS-4` (propagation and chain exposure), `DS-6` (effectiveness confidence and the uncertainty band), `DS-8` (full admissibility evaluation), and `DS-12` (no calibrated-probability presentation without calibration data). `DS-12` in particular is the requirement that keeps the model honest about itself: the interface must not present any of these values as a verified probability, and must not permit a derived figure to be quoted without its basis.

---

## 14. Decision-Support Requirements (DS-1 to DS-12)

### 14.1 What these requirements are for

The `DS-` series is owned by this document. It states what the decision-support model **must compute**, what it **must expose**, and what it **must refuse to do**. It is deliberately narrow in scope: it governs the decision-support model and its outputs, and it does not restate the `SCORE-`, `AD-`, `INT-`, `AUTH-`, `ROE-`, or `OP-` requirements of the wider set.

The `DS-` series is the machine-checkable face of this document. Where a requirement is marked MACHINE, an implementation can be tested against it directly. Where it is marked HYBRID, the machine can establish that the human element has been performed and recorded, but cannot perform it.

### 14.2 The requirements

| # | Requirement | Type | Where it is implemented |
| --- | --- | --- | --- |
| **DS-1** | The model must compute the threat score as `S = L × I × A × V` from four declared components, and must expose each component separately with its band, its reasoning, its observing analogue, and the alternatives considered. | MACHINE | `impl/caos/scoring.py` — `threat_score`, `score_breakdown`, `band_for_likelihood`, `band_for_impact` |
| **DS-2** | The model must refuse to compute or display a score in which any component is unstated, out of range, or unsupported by the required reasoning. A partial score must not be presented as a score, and must not be used as an input to any other computation in the model. | MACHINE | `impl/caos/scoring.py` — `score_breakdown`; `impl/caos/models.py` — `ThreatAssessment` validation |
| **DS-3** | The model must carry every attribution confidence with its candidate, its bases, its evidence tiers, its contradicting evidence, and its derivation chain, and must refuse to emit a countermeasure's effective threat where a countermeasure with an identity or external attribution dependency is evaluated against a card that does not carry one. | MACHINE | `impl/caos/vocab.py` — the source reliability tier vocabulary; `impl/caos/models.py` — the attribution basis, which is free text on `ThreatAssessment`; `impl/caos/models.py` — `Claim`, `ThreatAssessment` |
| **DS-4** | The model must apply confidence propagation to every derived claim, must take the derivation penalty from the declared table and apply it subtractively, and must expose the chain, the step count, and the penalty at each step. The engine must refuse a derived claim that declares no derivation penalty at all, because an undeclared penalty is an undischarged derivation. | MACHINE | `impl/caos/scoring.py` — `propagate_confidence`, `derivation_penalty`, `DERIVATION_PENALTIES` |
| **DS-5** | The model must compute effective threat as `S_eff = S × c` and residual risk as `R = S_eff × (1 − e)`, and must display the risk of inaction alongside the residual risk on every card that carries a selection. | MACHINE | `impl/caos/scoring.py` — `effective_threat`, `residual_risk`, `residual_risk_after`; `impl/caos/decision.py` — `counterfactuals` |
| **DS-6** | The model must attach a confidence to every effectiveness value, must refuse to accept an effectiveness figure that has no confidence, and must display the residual risk as a range using the declared band convention wherever the confidence is below 0.60. A countermeasure with `e ≥ 0.70` and `q < 0.50` must carry the unconfirmed-effectiveness marker. Both are implemented in `impl/caos/scoring.py` as `residual_band` and `is_effectiveness_unconfirmed`, and are rendered by the Watchfloor's decision-space view. | MACHINE | `impl/caos/scoring.py` — `residual_risk`, `Option`; `impl/caos/watchfloor.py` — residual-risk rendering |
| **DS-7** | The model must compute risk-adjusted priority as `P = (S_eff / 20) × q × (1 − r)` with the `r` normalisation stated at §8.2, and must not present `P` as a recommendation, an authorisation, a threshold verdict, or a reason for selection. A low `P` must not prevent a candidate from being selected. | MACHINE | `impl/caos/scoring.py` — `risk_adjusted_priority`; `impl/caos/vocab.py` — `CollateralClass.exposure` |
| **DS-8** | The model must evaluate all twelve admissibility conditions `AD-1` to `AD-12` for every candidate, must record every failure with the condition identifier, the observed value, the required value, the margin, and the route to admission, and must admit no candidate that fails any condition. The dispatch re-check must be a full evaluation against the current world state. | MACHINE | `impl/caos/roe.py` — `evaluate`, `AdmissibilityResult`, `AdmissibilityFailure`; `impl/caos/decision.py` — `filter_admissible`; `impl/caos/roe.py` — `card_is_armable` |
| **DS-9** | The model must not aggregate admissibility failures, must not assign partial credit, and must not permit a candidate that fails one condition to be admitted on the strength of satisfying the others. All failures for a candidate must be reported, not only the first. | MACHINE | `impl/caos/roe.py` — `evaluate` (conjunction, no early exit) |
| **DS-10** | The model must present the computed alternatives — the inaction option, each admissible candidate, each selected combination, and each rejected candidate with its distance from admissibility — with their own `e`, `q`, `r`, `R`, and `P`, and must not present a single recommended action. The inaction option must be displayed beside the ranking and not within it. | MACHINE | `impl/caos/decision.py` — `counterfactuals`, `select`; `impl/caos/scoring.py` — `compare_options` |
| **DS-11** | The model must not conceal from the operator view any input, assumption, derivation penalty, chain, evidence basis, rejection, margin, dissent, or override. The complete record of a card's decision inputs must be exportable in the form in which it was presented to the operator. | MACHINE | `impl/caos/decision.py` — `select` (decision record); `impl/caos/ledger.py`; `impl/caos/watchfloor.py` — countermeasure console rendering |
| **DS-12** | The model must treat every confidence value as an uncalibrated estimate, must record the basis, tier, derivation, author, and review status of each, and must not present any value as a calibrated probability, nor permit a derived figure to be quoted without its basis. The calibration status of the organisation is recorded, and the model presents it. | HYBRID | `impl/caos/models.py` — `Claim` metadata; `impl/caos/scoring.py` — the confidence metadata, the derivation-penalty table, and the residual-risk band; `impl/caos/ledger.py` — the hash-chained record |

### 14.3 Reading the implementation references

The third column states **where each requirement is implemented in the reference implementation under `impl/`**. The mapping was made against the source as it stood at the time of writing, and it is an **assertion** rather than a verified fact. The conformance of the implementation to this document is assessed by `reference/audit-and-conformance-procedures.md` §3, which maintains the mechanically-enforced register. The register and this table must agree; where they do not, the register is the record of what is actually enforced, and the difference is a defect to be raised.

The implementation is a reference implementation, not the system.

### 14.4 Divergences recorded at the time of writing

Three divergences between this document and the reference implementation were identified when this document was written. They are recorded here rather than left silent, because a register that disagrees with the code it describes is a defect in itself. Each must be resolved before the implementation is described as conformant, and each must be re-derived against the source, since the implementation may have changed.

| # | Divergence | This document | Reference implementation as at writing | Required resolution |
| --- | --- | --- | --- | --- |
| **DIV-1** | Confidence propagation | `c_derived = c_weakest − p`, a subtraction, as `INT-9` states it | `impl/caos/scoring.py` — `propagate_confidence`, now corrected to the subtractive form | **Resolved 2026-10-20.** The implementation was corrected to the subtractive form. The two agree at small penalties and diverge visibly at the larger ones: a leaf at 0.95 with a 0.10 penalty gives 0.85 here and 0.855 there, and that difference crosses the `INT-3` threshold for a C2 countermeasure. |
| **DIV-2** | Permitted action classes | The constitutional instrument's permitted action classes, at §9.3, as amended at version 1.0 | `impl/caos/vocab.py` — `_ROE_PERMITTED_CLASSES`, now corrected to the amended column | **Resolved 2026-10-20.** The constitutional instrument's column was amended rather than the implementation, because the column as first drafted made CM-A Detect unavailable at R1, R2, R4 and R5, CM-G Recover available only at R1, and OCC-25 and OCC-37 inadmissible at their own declared minimum. The column now states the countermeasure catalogue §4.1 class minimums made cumulative. The implementation now carries the amended column exactly — CM-F is available at R1, where the effect is exerted at the operator's own perimeter, and at no profile below it — and AD-1 evaluates both limbs as specified here. |
| **DIV-3** | Checkability classification | `AD-3`, `AD-6`, `AD-10`, and `AD-12` are HYBRID and `AD-5` is HUMAN, at §9.2 and §9.3 | `impl/caos/roe.py` — `CONDITION_NATURE`, now corrected to this document's classification | **Resolved 2026-10-20.** The implementation's table was corrected and the attestation fields the human and hybrid conditions require were added to the Operation Card model: `irreversibility_argument`, `indirect_effect_attestation`, `deconfliction_attestation`, `deconfliction_map_current`, `non_weaponisation_attestation`, and `per_target_authorisations`. AD-5 now also refuses any countermeasure whose status is Withheld. |

**DIV-3 is the one that changes how the framework reads.** A table that records every condition as machine-checkable tells an operator that the whole algebra is automatic, and it is not. `AD-5` requires a human judgement that cannot be encoded, and the classification is the framework's statement that this is so.

---

## 15. Verification Status and Architectural Assertions

### 15.1 The principle

Where this document states a claim about the behaviour of the model, the implementation, or the framework, that claim is an **architectural assertion** of the author and not, absent explicit statement to the contrary, an independently verified property. A statement of this kind must carry a statement of what substantiation would require.

The claims below are the load-bearing ones. They are recorded here rather than left implicit because a reader may reasonably act on them.

### 15.2 The register

| Claim | As stated | Current status | Required to substantiate |
| --- | --- | --- | --- |
| The admissibility algebra prevents out-of-profile action | The conjunction of `AD-1` to `AD-12` ensures that no countermeasure outside the ROE profile, outside the card's ceiling, or otherwise out of bounds can be selected for dispatch. | Architectural assertion; unverified. | End-to-end test evidence across every profile, collateral class, and autonomy class, showing each out-of-bounds request refused with the correct condition and margin; an independent review of the condition set for completeness against the constitutional instrument and the authorisation model; a documented review of the `AD-3` comparison direction, which is the condition most likely to be implemented inversely. |
| The scoring model orders the queue usefully | The ordering produced by `P` corresponds to the order in which an experienced operator would prioritise candidates, and the `S` bands correspond to the order in which an operator would work a queue. | Architectural assertion; unverified. | A structured comparison against operator judgement over a representative set of cases, with agreement statistics and the disagreement cases recorded and their causes identified. |
| The confidence-propagation rule reflects reality | Subtracting a declared derivation penalty from the weakest input's confidence produces a value that is no better warranted than the truth supports, and long chains do produce less reliable conclusions than short ones. | Architectural assertion; unverified. | Calibration data against recorded outcomes for derived claims; peer review of the derivation-penalty table; a demonstration that the propagated values discriminate between reliable and unreliable derivations in practice. |
| The model does not crowd out human judgement | Operators make their decisions on the model's output without deferring to it mechanically, and the recorded lower-ranked selections are genuine choices rather than formalities. | Architectural assertion; unverified. | Observation of operator behaviour in exercises and live operations; measurement of selection frequency against rank; the record of overridden recommendations and whether the overrides were vindicated. |
| The countermeasure combination rule does not materially overstate combined effect | `e_combined = 1 − Π(1 − e_i)` is a reasonable estimate of the combined effect for the combinations the framework anticipates. | Architectural assertion; unverified. | Measurement of combined effect for at least a defined subset of countermeasure pairs; a stated dependence assessment per pair; identification of the pairs where the rule is unreliable. |
| The collateral exposure normalisation reflects operational reality | The mapping of C0–C3 to `r = 0.00 / 0.25 / 0.60 / 1.00` induces an ordering of candidates that an experienced operator would endorse. | Architectural assertion; unverified. | Comparison of the induced ordering against operator judgement over a representative set; sensitivity analysis over the four values, including the effect of the C3 collapse; organisational review under §13.1. |
| The model exposes what the operator needs in order to contest it | The decomposition of every computed quantity, and the exposure of the derivation chain, are sufficient for a reviewer to locate a disagreement and say what the assessment would be under a different component. | Architectural assertion; unverified. | Usability testing with operators and with reviewers who were not present; the record of disagreements that could not be located in a component; an independent audit of a sample of cards for reconstruction sufficiency. |
| The reference implementation conforms to this document | The implementation under `impl/` implements the model as specified here. | Architectural assertion; unverified in full, and the three divergences recorded at §14.4 are now closed. | The mechanically-enforced register in `reference/audit-and-conformance-procedures.md` §3 re-derived against the source and test files, with function and test names cited; the three divergences at §14.4 closed and the closing evidenced; a test suite covering each `DS-` requirement in §14, including the negative cases and the `AD-3` comparison direction; a statement of the requirements that are not mechanically enforced. |

### 15.3 The principle for use

Where any claim in this register is cited, it must be accompanied by this section or by a statement that verification is outstanding. The framing "the model prevents", "the model ensures", "the model guarantees", and "the model calibrates" must not be used of the system as a whole.

**VR-DS-1 — The obligation is unconditional.** The requirements at §14 apply irrespective of the verification status of the claims above. The implementation must enforce the admissibility algebra, must expose the decomposition and the chain, and must refuse the presentations the model refuses, whether or not anyone has yet demonstrated that these controls achieve the outcomes asserted for them. This is the same principle the wider set applies to the defensive claims: the procedure is required now; the claims about the procedure's outcome await evidence.

---

## 16. Document Limitations

**LIM-DS1 — Confidence values are uncalibrated.** Every confidence value in the model is a self-assessment. The model treats confidence as an ordering device and a threshold input; it does not treat it as a probability validated against outcomes. The thresholds in §13.1 are conventions until calibration data exists.

**LIM-DS2 — The scores are ordinal in construction, and the multiplication assumes independence.** `L` is quasi-continuous while `I`, `A`, and `V` are ordinal, so a difference of 1.0 in `S` does not represent a proportionate difference in threat. The multiplication `S_eff = S × c` further assumes that threat and attribution are independent, which they are not: evidence that raises `L` typically also bears on `c`. The formula is used because it is legible under pressure, and the components are recorded separately so that a reviewer can see what it produced.

**LIM-DS3 — The admissibility algebra cannot detect a false declaration.** The algebra is sound over declared state. A countermeasure whose collateral class, reversibility, autonomy class, or target set is mis-declared passes the check. The model verifies consistency between the declaration and the catalogue, not the truth of the declaration.

**LIM-DS4 — The combination rule for countermeasure sets assumes independence.** `e_combined = 1 − Π(1 − e_i)` overstates the combined effect where the members' effects are dependent. The card must state the dependence; nothing in the model detects it.

**LIM-DS5 — The collateral exposure normalisation is a chosen convention.** The values 0.00, 0.25, 0.60, and 1.00 are adopted so that implementations agree, not because they measure the relative harm of the four classes. The C3 collapse to `P = 0` is a structural consequence of the choice, not a finding about C3 countermeasures.

**LIM-DS6 — Attribution remains the weakest link.** The framework bounds the consequence of misattribution through confidence thresholds, class asymmetry, and the preference for identity-independent countermeasures. It does not make misattribution less likely. An adversary who deliberately mimics benign traffic defeats behavioural attribution, and no procedure in this set prevents that.

**LIM-DS7 — The model does not learn and its parameters drift.** The scoring bands, the penalty table, the thresholds, and the normalisation are organisational settings with a review cadence, not a self-updating apparatus. An operator who believes a threshold is wrong is right to say so, but the correction is a governed change, and the model will continue to apply the setting until that change is made and versioned.

**LIM-DS8 — The model cannot create authority, and the error handler is the most exposed element.** The engine enforces the authorisation it is given. It cannot determine whether a countermeasure is lawful, proportionate, or ethically right, and does not attempt to. The human judgement at `G-4` remains the load-bearing element and the element most exposed to pressure.

**LIM-DS9 — Verification of the reference implementation is outstanding, though the three recorded divergences are closed.** The mapping between the `DS-` requirements and the implementation under `impl/` is stated as an assertion at §14.3 and is not verified here. The register in `reference/audit-and-conformance-procedures.md` §3 is the record of what is mechanically enforced, and it requires re-derivation against the source before it is relied upon. Three specific divergences were recorded at §14.4 and each is now closed: the confidence propagation is subtractive, the implementation's permitted action classes match the constitutional instrument's, and the checkability table records the hybrid and human conditions as such before the implementation is described as conformant.

**LIM-DS10 — The model's value depends on how it is used under pressure.** A decomposed score, an explicit chain, and a full rejected set are of no use to an operator who is not given the time to read them, and the interface's ability to present them at the moment of decision is a separate matter from this document's specification of their content. Nothing in this document guarantees that they are read.

**LIM-DS11 — The counterfactual set is bounded by the candidates that exist.** The alternatives computed at §12 are alternatives among the candidates that survived `STEP-1`. A better course of action that is not in the catalogue and is not proposed by the operator does not appear, and the model cannot generate one.

---

## 17. Summary

This document specifies the CAOS decision-support model in full: the threat score and the evidence discipline of its four components; the attribution confidence and the declared rule by which it is computed; the confidence-propagation rule and the derivation-penalty table, with the consequence that a strong observation can carry a weak decision when the chain to it is long; the effective threat, the expected effectiveness with its confidence, and the residual risk; the risk-adjusted priority, with its stated collateral-exposure normalisation and its rule that it ranks and does not authorise; the admissibility algebra, condition by condition, with the predicate, the inputs, the failure message, and the checkability of each; the selection algorithm in six expanded steps with a worked example showing four rejections and their margins; the counterfactual presentation of the alternatives, including inaction; the model's declared limits; and the register of claims that are design intent rather than verified fact.

Two commitments run through the whole of it, and they are the reason the model is shaped as it is rather than as a calculator.

The first is that **the model never authorises and a score is never an authorisation**. Authority is structural: it comes from a written instrument, it is enforced by a profile with a hard ceiling, and it is granted by a named human. Everything the model computes is a summary of judgements made by people, offered to other people in a form they can disagree with. The number is never the action; the card, the evidence, and the authorisation are the action.

The second is that **a decision is only reconstructible if its alternatives were computed**. The model does not produce a recommended action. It produces a set of computed options, each with its own residual risk, its own collateral exposure, its own confidence, and its own margin from admissibility — including the option of doing nothing and the option of choosing the second-ranked countermeasure. An operator who disagrees with the ranking can see what the alternatives look like, and an approver who was not present can see the shape of the space in which the decision was made.

The numbers in the model are estimates, the thresholds are organisational conventions, and the calibration data does not yet exist. The document says so on every page where it might otherwise be assumed otherwise, because a model whose uncertainty is hidden is more dangerous than a model that has none.

---

*This was supported for MIA by Kilo (kilo-auto/free).*
