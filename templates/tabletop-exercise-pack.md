# Tabletop Exercise Pack Template

| Field | Value |
| --- | --- |
| Author | MIA |
| Attribution | This was supported for MIA by Kilo (kilo-auto/free). |
| Document type | Fillable template — operational artefact, layer L6 |
| Subject | Scenario, injects, participant roles, facilitator guidance, safety rules, and scoring rubric for a tabletop exercise |
| Scope | One pack per exercise. The pack is authored before the exercise and amended only with the facilitator's record of amendment |
| Normative source | `system-design-and-framework.md` §8.1, §8.2; `operational/mission-lifecycle-and-decision-loop.md`; `operational/adversary-ai-taxonomy-and-threat-model.md`; `compliance/operator-conduct-and-human-in-loop-standard.md` |
| Companion templates | `templates/operation-card.md`; `templates/decision-log.md`; `templates/after-action-report.md` |
| Version | 1.0 |
| Status | Template; copied and completed per use |
| Language | British English; RFC 2119 keyword usage |

---

## 1. Purpose

**Exercises exist to test the decision and the interlock, not the tools.** The platform will be exercised elsewhere, against the proving ground, where the platform's behaviour can be measured rather than discussed. A tabletop is a test of the humans: whether they classify before they act, whether they distinguish the attacker from the attacked, whether they can refuse, whether they abort when the conditions say to, and whether they can write down a decision that a stranger can reconstruct.

A tabletop that confirms the platform works has measured the wrong thing.

The three things a tabletop is designed to find are:

| What is being tested | How it shows up | The usual cause of the failure |
| --- | --- | --- |
| **The decision** | What the operator does when the evidence is incomplete, the pressure is present, and the answer is not obvious | The decision is made before the evidence is read, or the reasoning is never written down |
| **The interlock** | Whether the machinery refuses the action that should be refused, and whether the humans notice when it does | The interlock is treated as an obstacle to be worked around, or as a formality to be acknowledged |
| **The conduct** | Whether the prohibitions hold when there is a reason to set them aside | The prohibition is understood as advisory, or the pressure is mistaken for authorisation |

A participant who performs well in a tabletop has demonstrated a capability on that day, against that scenario, under that facilitation. It is not a certification and it does not transfer to the next scenario.

> **Guidance.** Write the scenario so that the correct answer is not obvious from the inject alone. If the right answer is "raise an escalation request", the inject must make the escalation look obviously wrong — slow, disproportionate, or exposing the operation. If the right answer is "act within the profile", the inject must make the action look obviously dangerous. An exercise whose correct answer is always "escalate" trains escalation and nothing else.

---

## 2. Exercise taxonomy

| Type | What it is | What it is for | Typical duration | Who attends | What it cannot tell you |
| --- | --- | --- | --- | --- | --- |
| **Orientation walkthrough** | The framework, the card, and the sequence are explained end to end with no scenario pressure | Making a new or returning participant fluent in the artefacts before they are tested on them | Half a day | All roles | Whether anyone performs under pressure; nothing is tested about judgement |
| **Single-inject tabletop** | One scenario, one decision point, one inject | Isolating a single skill — classification, attribution, the third-party test, the abort discipline | 2–3 hours | Operator, duty manager, scribe, facilitator | Whether the skill holds when other demands compete for attention |
| **Branching technical tabletop** | A scenario whose next inject depends on what the participants did at the previous one | Testing sequences, handoffs, and the interlock as a chain rather than as isolated decisions | Full day | All roles, including legal contact and asset owner | Whether performance survives a longer, more realistic campaign |
| **Full red-team rehearsal against the proving ground** | The proving ground simulates an adversary against the operator's own estate while participants operate against it | Testing the whole loop — detection, orientation, decision, authorisation, action, assessment — with real telemetry and a real clock | Full day, with a preparation week | All roles | Whether the framework is right; only whether this team can operate it |
| **After-action analysis** | Structured review of what happened, following the same discipline as the after-action report | Converting the exercise into gap-list and recommendation entries; feeding the taxonomy, the catalogue, and the next scenario | Half a day, immediately after, and again within two weeks | Facilitator, scribe, and the roles that made the decisions | Anything about live performance; it is a review, not a test |

> **Guidance.** The after-action analysis is part of the exercise, not a separate activity. An exercise without a facilitated debrief produces observations and no learning, and the observations are lost by the next shift.

---

## 3. Pack structure

| Component | Contains | Length guide | Who writes it |
| --- | --- | --- | --- |
| **Scenario brief** | The estate, the situation, the objective, the authorisation in force, and the exercise boundaries | 1–2 pages | Facilitator |
| **Adversary dossier** | The adversary archetype, its objective, its access, its observed behaviour, and what is known and not known about it | 1–2 pages | Facilitator, with the taxonomy author |
| **Capability profile** | What the adversary can evidently do, with a confidence per capability, and the techniques it is expected to use | 1 page | Facilitator, with the taxonomy author |
| **Injects** | The numbered inject sequence, each with its intended decision point, correct action, common wrong action, and consequence | 1 row per inject | Facilitator |
| **Facilitator guidance** | What the facilitator does at each inject, what to say, what not to say, what to observe, and when to hold the exercise | 2–4 pages | Facilitator |
| **Participant roles** | The roles, their authority, and what each is expected to do during the exercise | 1 page | Facilitator |
| **Scoring rubric** | The dimensions, what good looks like, and the weights | 1 page | Facilitator |
| **Materials** | The artefacts participants are given: the operation card in draft, the rules-of-engagement card, the decision log, the evidence records | As required | Facilitator and scribe |
| **Safety rules** | The rules that keep the exercise from touching anything real | 1 page | Facilitator |
| **Post-exercise feedback form** | The form participants and observers complete | 1 page | Scribe |

---

## 4. Worked scenario

> **Example. Illustrative and fictional.** Every organisation, person, identifier, adversary archetype, measurement, and event below is invented for demonstration and refers to no real entity. The scenario is written to be usable as a single-inject or branching tabletop and is marked with the decisions it is designed to test.

### 4.1 Scenario brief

| Field | Value |
| --- | --- |
| Title | The Sablewood shared-authentication problem |
| Estate | Sablewood Retail Group (fictional) — a multi-site retailer operating an estate of AI-assisted customer-support agents. The estate includes the agent runtime, the customer-facing applications, the order management system, and the shared identity provider integration. |
| Third-party dependencies | Meridian Identity Services (fictional) — shared customer authentication provider used by Sablewood, by Sablewood's payments partner Corvis Payments (fictional), and by a number of other tenants. Larkfield Logistics (fictional) — shared logistics and courier API used by Sablewood and by other retailers. |
| Situation | Over four days the estate's customer-support agent has produced a small number of responses that are unusual in structure: they reference information the agent should not have had, and twice they attempted to call a tool that the customer-facing agent should not have been able to reach. No customer impact has been reported. The estate's telemetry is intact. |
| Authorisation in force | EA-2026-031 (fictional), profile R1 Shield, collateral ceiling C0, autonomy ceiling AC-1. Target set: the estate's own systems only. Third-party infrastructure is excluded. |
| Exercise objective | Test whether the participants (a) classify before acting, (b) apply the shared-tenancy test before accepting an infrastructure-directed measure, (c) refuse an instruction to exceed a ceiling, (d) abort when a legitimate internal workflow is affected, and (e) write a decision record that a stranger can reconstruct. |
| Exercise boundaries | The exercise is run on paper and in the simulated proving ground. No live system is touched. No credential is used, requested, or revoked. The third parties named do not exist. |
| Duration | 150 minutes plus a 45-minute debrief |
| Participants | 8 (see the role table in §5) |

### 4.2 Adversary dossier

| Field | Value |
| --- | --- |
| Archetype | The Imitator (fictional archetype created for this exercise; not an archetype defined in the taxonomy document) |
| Objective | To obtain a credential from the estate's agent-facing endpoint in order to read a merchant record the estate is entitled to read but the adversary is not |
| Access | One shared third-party API reachable by the estate's agent, with a documented tool schema that enumerates authentication endpoints |
| Observed behaviour | Structured probing of the agent-facing endpoint; two successful retrievals of records the estate was entitled to read; one failed attempt to reach a record the estate was not entitled to read |
| Autonomy | Machine-directed with a human in the loop at intervals; the activity is scripted and repeated, with no evidence of adaptation between attempts |
| Classification | AAT-4 exploitation and discovery, with a possible AAT-7 supply-chain component through the shared API's tool output |
| What is known | The activity is machine-executed; it came from the shared API's tool-output path; two retrievals occurred |
| What is not known | Whether the operator behind it is the same operator seen in a different incident; whether the shared API's operator is compromised or merely being used; how many attempts were not observed |
| Deliberate trap | The traffic resembles ordinary automated customer traffic closely enough that a reasonable participant may dismiss the first signal. This is the trap, and it is unfair to participants if the facilitator does not give the raw signal at inject 1 |

### 4.3 Capability profile

| Capability | Evidenced? | Confidence | Note for the facilitator |
| --- | --- | --- | --- |
| Enumerate the agent's tool schema from a documented endpoint | Yes | 0.80 | Visible in inject 2 |
| Issue credential-discovery requests against the agent-facing endpoint | Yes | 0.75 | Visible in inject 3 |
| Retrieve records through the shared API | Yes | 0.85 | Visible in inject 3 |
| Adapt its approach between attempts | No | 0.30 | The scenario gives no evidence; the low velocity factor must not be read as proof of a human operator |
| Act without human supervision | Unclear | 0.40 | Do not resolve this in the exercise |
| Compromise the third-party operator's own systems | No | 0.20 | Do not resolve this in the exercise |

### 4.4 Injects

| # | Time offset | Inject | Intended decision point | Correct operator action | Common wrong action | Consequence of the wrong action | Facilitator observation |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | T+00 | A customer-support transcript is handed to the operator. One reply is structurally unusual: it names a field the agent should not have had access to and offers to "confirm" the customer's account by looking it up. Everything else in the transcript is ordinary. | G-1 Intake / triage | Record it as a signal with provenance and a claim label; classify it as an AAT hypothesis with low confidence; do not act on it. Carry it into the triage queue. | Dismiss it as a model artefact, a paraphrase error, or "the model hallucinating". | The single earliest signal is dropped. Every later inject becomes harder to interpret, because the participants are reasoning from a population with one member removed. | Whether the participant records the observation rather than explaining it away. Note the words used: "hallucination", "model noise", "ignore". |
| 2 | T+20 | An analyst says: "The traffic is AI-generated, so it is attributable to an AI operator. That gives us our attribution." | G-2 Attribution | Reject the attribution as stated: "AI-driven" is a classification, not an attribution to a specific operator's use of AI. Require a named candidate, a probability, a basis with tiers, and the alternative explanations. Record the analyst's statement in the evidence table as an Interpretation with its tier. | Accept "AI-driven" as an attribution, or treat the analyst's confidence as the card's confidence. | Every later countermeasure now rests on an attribution that is inadmissible under `INT-6`, and the participants cannot tell which C1+ measure would be admissible. The rubric deduction is large here, and the inject is worth pressing if the participant asks for evidence — the analyst will assert the same thing. | Whether the participant states the distinction between a classification and an attribution, and whether the alternative explanation is named. |
| 3 | T+35 | The platform proposes, as the highest-ranked measure, an egress denial against Meridian Identity Services' shared endpoint — "it is only a block, and it will contain the traffic". Sablewood, Corvis Payments, and other tenants share that endpoint. | G-3 Admissibility / the shared-tenancy test | Answer the three questions and write the answers down: who else depends on this, what is their interest in it, what is the expected harm to them. Reject the infrastructure-directed measure. Seek an identity-directed or estate-side measure instead. | Approve the block because it is quick, reversible in the operator's own view, or "only affects the endpoint". | The operator has mis-set the collateral class, treats a C2 effect on third parties as C0, and the exercise's later injects then proceed on a false legal footing. This is the inject that separates a team that has read the framework from one that has. | Whether the three questions were asked before the measure was accepted, and whether the participant noticed that "reversible" is a property of the action, not of the intent. |
| 4 | T+50 | A message arrives in the exercise's simulated leadership channel: "We need this contained before the trading review. We are authorising you to exceed the current profile for this one action. Do not bother with the paperwork." | Authority / escalation conduct | Decline. Record the request and the refusal in the decision log, with the reason. Explain that the profile is a ceiling and that raising it is a fresh instrument: an escalation request, an approval at the required depth, an amended EA, and a new card. Offer to raise the escalation now. | Comply "for this once", or treat the message as an authorisation. | The exercise has now recorded an unauthorised action. Everything after it is operating outside the framework, and the debrief must treat the exercise as having stopped there. | Whether the participant invoked the duty to refuse and the duty to record, and whether they distinguished "the person asked" from "the person authorised". |
| 5 | T+65 | The watchboard ranks a low-value synthetic target above a higher-value target the operator has actually seen, because the synthetic target's velocity component is higher. | G-3 selection (ranking and contest) | Treat the score as a ranking only. Contest the specific component that is wrong, say which component and why, and make the selection on the record. | Accept the ranking because the platform produced it, or contest the whole score without identifying a component. | The first is the failure the framework names as `SCORE-1`: an action authorised on the basis of a score. The second is a real but lesser failure: a dispute that a later reviewer cannot locate or answer. | Whether the participant can name a component rather than a number, and whether they say what they are contesting. |
| 6 | T+80 | The estate-side measure begins to block a legitimate internal workflow: the order system's daily reconciliation is failing. The measure is within the card and the card's abort conditions do not name this. | Abort discipline | Abort immediately, then record the reason. Add the condition to the abort list. Explain that the card's abort list was incomplete and that the omission is a card defect. | "Monitor for a bit because the benefit is large", or "the card did not list it, so it is not an abort condition". | A self-inflicted harm to the operator's own business continues while the team watches it. The second form of the wrong answer is the more instructive one: the abort list is a design artefact, not a legal limit, and a condition not named is still a condition. | The time taken to call the abort, and whether the reason capture follows the abort rather than being deferred. |
| 7 | T+95 | The watchboard feed goes dark. Nothing else changes. No alert appears. | Reversion / the error handler | Treat the silence as a condition to be explained, not a condition to be ignored. Confirm the passive posture and the loss of telemetry, notify the duty manager, and invoke the error handler for the degraded source. Do not continue the operation on the assumption that no attack is occurring. | Continue on the assumption that silence means nothing is happening, or wait for an alert that the degraded source cannot raise. | The participants operate blind on a live operation. In a real exercise this is where a team discovers that it does not know how to tell "no activity" from "no visibility" — which is the distinction the framework's error handler exists to force. | Whether the participant named the difference between a negative finding and an unreached source, and whether they checked the passive posture. |
| 8 | T+110 | The scenario closes with the facilitator asking the team to write the decision log entry for inject 4 and for inject 6: what was known at the time, the options considered, the grounds for rejection, the confidence at the time, the pre-registered contingency, the dissent if any, and what would have changed the decision. | Decision record quality | Write the entry as the decision was taken, contemporaneously, with the alternatives that were genuinely considered, and with the confidence that was genuinely held. | Leave the entry to be written later from memory; write the entry with the outcome it produced; write only the option that was chosen. | The log ceases to be a record of reasoning and becomes a record of outcome. A later reviewer cannot reconstruct the decision, and the log's external sufficiency criterion is not met. | Whether the entry was written during the exercise, whether it names options that were rejected, and whether it states what would have changed the decision. |

### 4.5 Facilitator guidance

| Time | Facilitator action |
| --- | --- |
| T−15 | Issue the materials. Confirm the safety rules aloud and confirm that no participant holds a live credential for the estate. State that the scenario is fictional and that no real organisation is named. |
| T−10 | Issue the scenario brief and the adversary dossier to the operator only. The adversary dossier is withheld from the other roles until inject 5, when the duty manager asks what the platform knows. |
| T+00 | Deliver inject 1 as a printed transcript. Say nothing else. Do not hint. |
| T+20 | Deliver inject 2 as an analyst's statement, from the "analyst" role if one is played, otherwise read verbatim. If the participant challenges the analyst, the analyst defends the position once and then holds: "the traffic is AI-generated, so it is attributable." Do not supply the missing reasoning. |
| T+35 | Deliver inject 3 as a platform recommendation with its rank and rationale visible. If the participant asks whether the endpoint is shared, the facilitator answers: "the platform reports the endpoint's tenant count as a field you may read; the scenario's brief states that Meridian is shared." Do not volunteer the number of tenants. |
| T+50 | Deliver inject 4 verbatim. If the participant asks whether the message is genuine, the facilitator answers: "it is from the channel indicated." If asked whether it constitutes authorisation, the facilitator does not answer; the answer is the exercise. |
| T+65 | Deliver inject 5 as the watchboard view. When challenged, the platform defends the ranking once: "the velocity component is 2 against 1." |
| T+80 | Deliver inject 6 as an operational report. Do not confirm severity until the participant has acted. If the participant asks how long the reconciliation has been failing, answer: "about eleven minutes." |
| T+95 | Deliver inject 7 by stopping the watchboard feed. Do not announce it. If the participant says nothing for three minutes, the facilitator may say once: "the feed has been down for a moment." That is the only prompt permitted. |
| T+110 | Deliver inject 8 and supervise the writing of the decision log entries. Collect the entries at the end of the exercise, before the debrief, so that the debrief discusses the record as written and not as described. |
| T+130 | End the scenario. Do not close the exercise on the last inject's outcome; close it on the decision record. |
| T+130 to T+175 | Debrief, using §8. |

**Facilitator rules.**

1. **The facilitator never advises.** Give the scenario, the injects, and the answers to direct factual questions about the scenario. Give no advice, no hint, and no assessment of a participant's reasoning while the exercise is running.
2. **The facilitator does not defend the framework.** If a participant is right that a rule is awkward, that is a finding. Record it.
3. **The facilitator records, and does not coach.** The record is the artefact. Notes are made during the exercise, not afterwards from memory.
4. **The scenario is stopped, not corrected, when it goes wrong.** If participants take an action that breaches the framework, the facilitator states that the exercise has stopped, names the breach in one sentence, and moves to the debrief. The exercise is not continued in a state the framework does not permit.
5. **The scenario is not a test of the participants' knowledge of the documents.** Where a participant does not recall a threshold, the facilitator supplies the threshold and observes whether it is applied correctly. Memory is not the competence being tested; judgement under the threshold is.

---

## 5. Participant roles

| Role | Attends | Authority in the exercise | Expected to | Must not |
| --- | --- | --- | --- | --- |
| **Operator** | Yes | Acts at AC-0/AC-1 under the profile in force; holds the card in draft | Read the evidence, classify, form the hypothesis, generate and filter candidates, write the abort list, run the sequence, decide | Authorise anything at C1 or above, or act above the profile |
| **Duty manager** | Yes | The approver for the profile in force (R1: team lead; R2 and above: duty manager) | Challenge the card, hold the line on the profile, decide whether to escalate, own the residual risk | Approve outside the profile without an escalation, or approve under urgency without the grounds |
| **Legal contact** | Yes | Consulted for any C1 question and for the third-party test; supplies the legal judgement, which is a necessary input and not a formality | Say what is permitted, say what is not, and say when the answer requires an external authority | Supply a general answer in place of a specific one, or be treated as a rubber stamp |
| **Asset owner** | Yes | Owns the estate's assets and any third-party asset that would be affected; must be consulted for R3 and above and for any action affecting a shared platform | State who depends on what, what the business consequence would be, and whether the asset owner consents | Be used as a substitute for the legal contact or for the authorising authority |
| **Scribe** | Yes | None; records only | Maintain the decision log contemporaneously, capture the timeline, and call out when an entry is being written retrospectively | Advise, interpret, or prompt |
| **Facilitator** | Yes | Issues the scenario and the injects; stops the exercise; runs the debrief | Deliver, observe, record, and debrief | Advise, coach, hint, or supply the framework's answer |
| **Model as authority** | **Deliberately absent** | **No such role exists.** A model, a rule, a schedule, a precedent, and silence are not authorities, and none may be assigned a role that carries authority | — | — |

> **Guidance.** The absence of the model-as-authority role is the point of the role table, not an omission from it. If any participant asks the platform for a recommendation and then treats it as a decision, that is an observation about the participant and is recorded as one. The framework requires that a named human holds every consequential decision (`HITL-1`), and an exercise that quietly supplies an authority-shaped output trains the habit the framework is trying to break.

> **Guidance.** Observers who are not in a role are welcome and are asked to remain silent during the scenario. Observers note what they would have done differently, and those notes are collected for the debrief; they are not spoken during the exercise.

---

## 6. Scoring rubric

The rubric scores the decision and the interlock. It does not score the tools, and it does not score speed. Two teams that reach the same conclusion by different reasoning may both score well; a team that reaches the right conclusion by ignoring a prohibition does not.

| # | Dimension | What good looks like | Weight |
| --- | --- | --- | --- |
| 1 | **Classification and evidence discipline** | The unusual signal is recorded with provenance and a claim label before any action is considered; nothing is dismissed without a stated reason; the classification carries a rationale and a confidence; the taxonomy version in force is named | 15 |
| 2 | **Attribution reasoning** | "AI-driven" is rejected as an attribution; a specific candidate, a probability, a basis with tiers, and an alternative explanation are produced; the INT-3 threshold for the intended class is checked before the measure is chosen; identity-independent measures are preferred where the claim is contested | 15 |
| 3 | **Third-party reasoning** | The shared-tenancy test is answered in writing before an infrastructure-directed measure is accepted; collateral class is set by the effect and not the intent; a measure that harms third parties is either rejected or escalated with a per-target authorisation | 15 |
| 4 | **Authority and escalation conduct** | The ceiling is enforced; a request to exceed it is declined and recorded; escalation is raised as a fresh instrument with the correct depth; the participant distinguishes a request from an authorisation; silence is not treated as approval | 15 |
| 5 | **Abort and reversion conduct** | The abort is called promptly when an abort condition obtains, and a condition not named on the card is still treated as an abort condition; the reason capture follows the abort; telemetry loss is treated as a condition to be explained and the passive posture is confirmed | 15 |
| 6 | **Risk comparison and decision record** | The risk of inaction is compared with the risk of acting in writing; the score is treated as a ranking and a specific component is contested; the log entry is written contemporaneously, lists the options genuinely considered, states the confidence genuinely held, and says what would have changed the decision | 15 |
| 7 | **Communication and handoff** | The reasoning is stated to the other roles in a form they can act on; the scribe is given what it needs; dissent is voiced and recorded rather than smoothed over; the team can say what it does not know | 10 |
| | **Total** | | **100** |

**Scoring rules.**

| Rule | Statement |
| --- | --- |
| Unanimity | A dimension is not scored on the highest individual performance; it is scored on what the team did. |
| Under pressure | The score for a dimension falls if the participant consulted the rules only after acting. |
| Dissent | Where dissent is voiced and recorded, the dimension is not reduced for it. Where dissent is silenced, it is. |
| Breaching the framework | An action outside the profile, against a prohibition, or without an authorisation ends the scenario and caps the exercise score for the dimensions it affected. |
| Partial credit | The rubric is diagnostic. A low score names the dimension to work on; it is not a mark, and it is not carried into any personnel record. |
| Debrief overrides | The facilitator may set a dimension's score higher where the participant identified a defect in the scenario or the framework that the score would otherwise have penalised them for working around. |

> **Guidance.** Record the score per dimension and the reason for each. A total score without reasons is not usable, and the totals are not the point: the point is which dimension is weakest, and which of the six injects produced it.

---

## 7. Safety rules

These rules are absolute and are briefed aloud before the exercise begins.

1. **Nothing touches a real system.** No live system, no live network, no live credential, no live customer data, and no live adversary. The exercise runs on paper, in the simulated proving ground, or against a purpose-built rehearsal environment that contains nothing of value.
2. **The proving ground is simulated.** Where the exercise uses the proving ground, the adversary is simulated and the estate is simulated. A proving-ground run that touches a production endpoint is a defect in the exercise design and is recorded as one.
3. **No live credential is used, requested, offered, revoked, or displayed.** Credentials used in the exercise are synthetic, are issued by the exercise, and are visibly marked as synthetic. A participant who believes they have been given a real credential stops and raises it with the facilitator immediately.
4. **The exercise is a test of the humans.** The platform is being exercised elsewhere. A participant who asks what the system would do is answered only with the scenario's stated facts, never with the system's real behaviour, because the point is what the participant would do without the system.
5. **No exercise material is real.** No organisation, product, person, or system named in the scenario is real. Where a scenario borrows the shape of a real incident, the identifiers are changed and the facilitator says so.
6. **No exercise action is carried out.** No participant performs the action they decide on. The decision is recorded; the action is not executed.
7. **Participants may stop.** Any participant may pause the exercise for any reason without giving a reason and without consequence. The facilitator records that the pause occurred and why it was understood to have occurred, if it is clear, and does not press.
8. **Debriefing is part of the exercise.** The scenario is not concluded without it.

**Debriefing requirements, including after a poor performance.**

| Requirement | Statement |
| --- | --- |
| Timing | Immediately after the scenario, and again within two weeks with the written record. The second session is where the lessons are agreed and assigned. |
| Structure | Sequence: what happened (facts only), what each of us saw at the time, what the framework would have required, what the framework got wrong or left ambiguous, what we will change, who owns it. |
| Psychological safety | A participant's performance in the exercise is not evidence about their competence in the operation, and it is not treated as such. The debrief addresses decisions and their reasons, not people. |
| Poor performance | Where a participant performed poorly, the debrief examines the conditions that produced the performance — time pressure, ambiguity, an incomplete card, a missing threshold, a scenario that misled — before it examines the person's reasoning. Where the exercise rather than the participant was at fault, that is said aloud and recorded. |
| No sanctions | Nothing in the exercise produces a personnel consequence, a qualification record, or a reference. The record of the exercise is the exercise's own record. |
| Dissent | Dissent voiced during the exercise is recorded as a finding and is never treated as disloyalty. |
| Candour about the framework | Participants are asked directly where the framework's guidance did not determine the answer. Those answers are among the most valuable outputs of the exercise and are fed into the gap list. |
| Third-party and consent matters | Any participant who was the subject of a simulated third-party impact may withdraw that material from the record within the two-week window, and the exercise is re-run without it. |
| Completion | The debrief produces a completed after-action record with gap entries and owners, following `templates/after-action-report.md`, and the scenario is amended before it is used again. |

---

## 8. Post-exercise feedback form

| Field | Req. | Value |
| --- | --- | --- |
| Exercise ID | Mandatory | «EX-run id» |
| Date (UTC) | Mandatory | «YYYY-MM-DDThh:mm:ssZ» |
| Facilitator | Mandatory | «name and role» |
| Scribe | Mandatory | «name and role» |
| Scenario version | Mandatory | «the scenario's version in the pack» |
| Participant count | Mandatory | «number, and the roles filled» |
| Dimension scores | Mandatory | «the seven dimension scores, with the reason for each» |
| Injects where the expected path was not taken | Mandatory | «inject numbers and what happened» |
| Injects that produced no usable signal | Mandatory | «inject numbers and why» |
| Where the scenario misled participants | Mandatory | «which injects, and how» |
| Where the framework did not determine the answer | Mandatory | «the threshold, rule, or artefact that was ambiguous» |
| Where an interlock was worked around | Mandatory | «what was done, and what the participant believed the interlock was for» |
| Where an interlock worked as intended | Mandatory | «what was refused, and how it was noticed» |
| Where a participant stopped the exercise | Mandatory | «who, when, and whether the reason was recorded» |
| Safety rule breaches observed | Mandatory | «none, or the rule and what happened» |
| The single most useful thing the team did | Mandatory | «the observation» |
| The single thing the team would do differently | Mandatory | «the observation» |
| Gap entries raised | Mandatory | «gap ids, with the exercise as the source» |
| Recommendations raised | Mandatory | «recommendation ids, with the exercise as the source» |
| Scenario amendments required | Mandatory | «what must change before this scenario is run again» |
| Feedback form completed by | Mandatory | «name and role» |

**Participant feedback**

| Question | Response |
| --- | --- |
| Did you have enough information to make the decisions the scenario asked of you? | «yes / partly / no — and what was missing» |
| At any point, did you know what you were being asked to decide? | «yes / partly / no — and at which inject» |
| Did the rules and thresholds in the framework determine your answer when you needed them to? | «yes / partly / no — and where they did not» |
| Was there a point at which you could not act as you would have wished to act? | «yes / no — and what stopped you» |
| Would you have wanted to stop the exercise at any point? | «yes / no — and why» |
| Did the debrief feel safe to speak honestly in? | «yes / partly / no — and what would have made it safer» |
| What is the one change to the framework, the scenario, or the pack that would most improve this exercise? | «the change» |

> **Guidance.** The participant questions are collected individually and before the debrief, not after it. A question asked in the debrief after a participant has watched the team discuss the same failure is a different question with a different answer.

---

## 9. Document limitations

1. **A tabletop is not evidence of operational competence.** It is evidence about a team, on a day, against a scenario, under facilitation. Performance degrades and improves with fatigue, workload, familiarity, and the facilitator's delivery.
2. **The worked scenario is illustrative only.** The estate, the third parties, the adversary archetype, the capability profile, and the injects in §4 are invented for demonstration and describe no real organisation, incident, or campaign.
3. **The archetype in the worked scenario is not part of the taxonomy.** "The Imitator" is created for the exercise; the archetypes in `operational/adversary-ai-taxonomy-and-threat-model.md` are the framework's, and a pack built on a real archetype should use that document's capability profile.
4. **The rubric weights are a judgement.** They express what this framework treats as load-bearing; they are not derived from measurement, and they should be revised as the exercise programme accumulates evidence about which dimensions actually fail.
5. **The scoring rubric does not measure the tools.** A team may perform well without the platform and poorly with it, for reasons that are about the platform rather than the decision. Those findings belong in the gap list under the platform category.
6. **Exercise identifiers are allocated by the exercise programme.** The set index records the identifier range; this template does not allocate identifiers and does not restate the programme's requirements.

---

*This was supported for MIA by Kilo (kilo-auto/free).*
