# After-Action Report Template

| Field | Value |
| --- | --- |
| Author | MIA |
| Attribution | This was supported for MIA by Kilo (kilo-auto/free). |
| Document type | Fillable template — operational artefact, layer L6 |
| Subject | Structured learning, detection-gap feedback, and metric capture for a completed operation |
| Scope | One report per operation, filed at G-7 Closeout |
| Normative source | `system-design-and-framework.md` §5, §6, §8, §11; `operational/mission-lifecycle-and-decision-loop.md`; `reference/audit-and-conformance-procedures.md`; `reference/ai-attack-technique-library.md` |
| Companion templates | `templates/operation-card.md`; `templates/decision-log.md`; `templates/tabletop-exercise-pack.md` |
| Version | 1.0 |
| Status | Template; copied and completed per use |
| Language | British English; RFC 2119 keyword usage |

---

## 1. Purpose

The after-action report is how the operation returns value to the framework. It is the instrument by which what actually happened is compared with what was predicted, what was decided is compared with what should have been decided given what was known at the time, and what was learned is fed back into the taxonomy, the detection content, the countermeasure catalogue, and the exercise programme.

Two things this report is **not**.

It is not a performance assessment of the people involved. The report examines decisions, not individuals.

It is not a victory lap. An operation that ended well may still have exposed serious gaps, and an operation that ended badly may have been soundly decided on the information available. The two questions are asked separately and reported separately, and neither is allowed to colour the other.

**The sufficiency criterion is external.** A reviewer who was not present must be able to reconstruct what was known, what was decided, and what followed, from this report and the material it references.

> **Guidance.** Write the report against the record, not against the memory of the shift. Where the record and the memory differ, the report says so and records both. Where the report cannot establish something, it says that it cannot, rather than filling the gap with a plausible account.

---

## 2. Report sections

Complete every section. A section with nothing to report records "none" and the reason it is empty, which is information.

### 2.1 Operation summary

| Field | Req. | Value |
| --- | --- | --- |
| Report ID | Mandatory | «AAR-nnnn» |
| Operation / card | Mandatory | «card id, and the operation name» |
| EA reference | Mandatory | «EA id and version, including any amendment» |
| Profile in force | Mandatory | «R0 – R5» |
| Dates of operation | Mandatory | «start and end, UTC» |
| Report filed (UTC) | Mandatory | «YYYY-MM-DDThh:mm:ssZ» |
| Report author | Mandatory | «name and role» |
| Decision log reference | Mandatory | «log id» |
| Objective | Mandatory | «the objective as it was stated on the card» |
| Outcome against objective | Mandatory | «achieved / partially achieved / not achieved, with the observation that establishes it» |
| Observation window | Mandatory | «the window over which the outcome was judged» |

> **Guidance.** "Outcome against objective" is judged against the objective as written on the card, not against a revised objective written afterwards. Where the objective was wrong, that is recorded in §2.9 as a defect, not silently corrected here.

### 2.2 Timeline of decisions and actions

| Time (UTC) | Decision or action | Type | Actor / system | Authority | Decision log entry | Card state | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| «timestamp» | «what happened» | «decision / action / abort / reversion / escalation / detection» | «who or what» | «EA ref, profile, approver» | «DL-nnn» | «card state» | «the short note a reader needs to follow the row» |

> **Guidance.** The timeline is the spine of the report. Every decision log entry and every ledger event that bears on the operation appears here. A reader who follows only this table should be able to see the shape of the operation: when it started, when it was authorised, when it was armed, what happened, when it was aborted or completed, and when it closed.

### 2.3 What happened

| Field | Req. | Value |
| --- | --- | --- |
| Narrative of events | Mandatory | «the account, in chronological order, drawing on the timeline» |
| What was not as predicted | Mandatory | «the table below — the discrepancies between prediction and observation» |
| Unexpected outcomes | Mandatory | «any outcome the card did not predict, and the handler it invoked» |
| Unplanned third-party effect | Mandatory | «any effect on a party outside the operation's scope» |
| Data quality problems | Mandatory | «degraded sources, missing telemetry, ingest gaps, and what they prevented» |

**Predictions against observations**

| # | What the card predicted | What was observed | Divergence | Cause | Consequence for the operation |
| --- | --- | --- | --- | --- | --- |
| 1 | «prediction, and the claim or figure it rested on» | «observation» | «the size and direction of the divergence» | «the cause, or "not established"» | «what it changed» |

> **Guidance.** "What was not as predicted" is not a list of complaints. It is the calibration data. Where the framework's own estimates were wrong, the estimate is the thing that is wrong, and the report names it. Where the observation was wrong, that is recorded too. The report does not resolve a discrepancy by asserting that the card was right.

### 2.4 Effectiveness assessment

| Field | Req. | Value |
| --- | --- | --- |
| Residual risk predicted (on the card) | Mandatory | «R_before, R_after, e, and the confidence in e» |
| Residual risk measured | Mandatory | «the recomputed figure, with the basis for the recomputation» |
| Difference | Mandatory | «measured minus predicted, with an explanation» |
| Countermeasures that achieved their intended effect | Mandatory | «ids and the evidence» |
| Countermeasures that did not | Mandatory | «ids and the evidence» |
| Effectiveness of the countermeasure set (observed) | Mandatory | «the observed e, with confidence and basis» |
| Whether the objective was met by the countermeasure set or by other means | Mandatory | «the attribution of the outcome» |

> **Guidance.** The comparison between predicted and measured residual risk is the single most useful figure in this report, and it is the one most often omitted. Where the recomputation cannot be performed because the data is not there, the report says so and records the effect as a measurement gap rather than estimating a figure.

### 2.5 Decision assessment

> **Guidance.** The question is: **was the decision sound given what was known at the time?** It is not: was the outcome lucky? A sound decision that ended badly is a sound decision, and this report must say so. An unsound decision that ended well is an unsound decision, and this report must say so. Where the two coincide, no inference is drawn from the outcome.

| Decision | Sound given what was known? | Basis for that judgement | Divergence a later reviewer would reach, and why | Carried forward |
| --- | --- | --- | --- | --- |
| «DL-nnn — the decision» | «yes / partly / no» | «what was known at the time, and the reasoning» | «the divergence, or "none identified"» | «the lesson, the recommendation, or "none"» |

> **Guidance.** Where a later reviewer would have decided differently on the same information, that divergence is recorded rather than smoothed over (`ERR-5`). It is a statement about the information available, not about the competence of the person who decided.

### 2.6 Detection assessment

| Field | Req. | Value |
| --- | --- | --- |
| Techniques present in the operation | Mandatory | «AAT categories and techniques observed» |
| Techniques detected | Mandatory | «the table below» |
| Techniques not detected | Mandatory | «the table below» |
| Detection gaps exposed | Mandatory | «the gaps, the telemetry that was absent, and the consequence» |
| Detection latency observed | Mandatory | «from first adversary activity to first detection, per technique where separable» |
| False positives encountered | Mandatory | «count, cost, and what was done with them» |
| Feed back to the taxonomy | Mandatory | «the changes proposed to the taxonomy, technique library, or detection content» |

**Detected**

| Technique | Detected by | Detection latency | Signal fidelity | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| «AAT-n / technique» | «the detection method or sensor» | «duration» | «high / medium / low» | «0.0 – 1.0» | «notes» |

**Not detected**

| Technique | Why not detected | Earliest point at which detection was possible | Dependency that would close the gap | Owner |
| --- | --- | --- | --- | --- |
| «AAT-n / technique» | «the absent signal, the absent sensor, or the analysis that did not run» | «the point at which a different signal would have been visible» | «what would need to change» | «name, role» |

> **Guidance.** The "not detected" table is the most valuable part of this section and the part most often left empty. An undetected technique that the framework claims coverage for is a coverage claim that has been falsified, and that is a finding about the framework. Every entry here becomes a detection-gap feedback entry (§2.14) with an owner.

### 2.7 Collateral assessment

| Field | Req. | Value |
| --- | --- | --- |
| Third-party effect observed | Mandatory | «what happened to whom, and when» |
| Within the card | Mandatory | «yes / no — with the clause or field that does or does not cover it» |
| Within the EA | Mandatory | «yes / no» |
| Within the authorisation | Mandatory | «yes / no» |
| Consequence | Mandatory | «the effect on the third party, and any action taken in response» |
| Disclosure made | Mandatory | «who was told, when, and by whom» |
| Collateral class of the observed effect | Mandatory | «C0 – C3, as it would be classified» |
| Whether the effect was foreseeable | Mandatory | «yes / no / partly, with the basis» |
| Changes made to the card or the shared-tenancy test | Mandatory | «the change, or "none — with the reason"» |

> **Guidance.** A third-party effect outside the card is not automatically a failure of the operation; it may be a failure of the shared-tenancy test, of the countermeasure's classification, or of the deconfliction check. The report distinguishes these, because they have different remedies. An effect that was within the card but that the operator did not foresee is still an effect on a third party and is still reported.

### 2.8 Attribution assessment

| Field | Req. | Value |
| --- | --- | --- |
| Attribution made at the time | Mandatory | «the candidate, the confidence, and the basis» |
| Attribution that holds up | Mandatory | «the candidate after the operation, and the evidence for the change» |
| Attribution held up | Mandatory | «yes / no / partly» |
| Basis for the change | Mandatory | «what was learned that changed or did not change the view» |
| Calibration of the confidence stated at the time | Mandatory | «the table below» |
| Consequences of the attribution, if it was wrong | Mandatory | «what would have happened, and what did happen» |

**Confidence calibration**

| Decision point | Confidence stated at the time | Basis given at the time | Basis as it appears now | Assessment |
| --- | --- | --- | --- | --- |
| «DL-nnn» | «0.0 – 1.0» | «the basis stated» | «the basis as it now appears» | «well calibrated / over-stated / under-stated / cannot be assessed» |

> **Guidance.** Confidence is a self-assessment (master design `LIM-2`). A single operation cannot calibrate anything, and the report must not claim that it has. What an operation can do is record whether the confidence stated at the time was well founded on the information available, and whether the basis held up afterwards. That is a case, not a calibration programme.

### 2.9 What worked

| Field | Req. | Value |
| --- | --- | --- |
| What worked | Mandatory | «the table below» |
| Why it worked | Mandatory | «the mechanism, not the outcome» |
| Whether it would work again | Mandatory | «the conditions under which it would, and those under which it would not» |

| Element | What happened | Why it worked | Would it work again, and under what conditions |
| --- | --- | --- | --- |
| «element — a control, a process step, a piece of judgement, a piece of the platform» | «the observation» | «the mechanism» | «conditions» |

> **Guidance.** Credit is given to mechanisms, not to luck. "The operator noticed the pattern" is not a mechanism; "the watchboard's velocity cue surfaced the repetition on the second day, before the impact threshold was reached" is.

### 2.10 What did not

| Field | Req. | Value |
| --- | --- | --- |
| What did not work | Mandatory | «the table below» |
| Why it did not work | Mandatory | «the mechanism that was missing, wrong, or absent» |
| Whether it could have been made to work | Mandatory | «yes / no, and what it would have taken» |
| Whether it was known at the time | Mandatory | «yes / no — the judgement of the people present» |

| Element | What happened | Why it did not work | Could it have been made to work | Was it known at the time |
| --- | --- | --- | --- | --- |
| «element» | «the observation» | «the mechanism» | «and what it would have taken» | «yes / no» |

> **Guidance.** The "known at the time" column matters. A gap that was visible and was not seen is a judgement finding; a gap that was invisible is a design or coverage finding. They have different owners and different remedies, and conflating them produces an unfair report and a useless one.

### 2.11 Countermeasure catalogue entries exercised

| Catalogue ref | Class | Intended effect | Collateral class | Autonomy class | Residual risk as stated | Residual risk as observed | Effect | Catalogue update proposed |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| «OCC-nn» | «CM-x» | «what it was meant to achieve» | «C0 – C3» | «AC-0 – AC-4» | «the figure on the card» | «the figure observed» | «achieved / partially achieved / not achieved» | «the change proposed, or "none"» |

> **Guidance.** The as-stated and as-observed columns are the point of this section. A countermeasure whose observed effect differs materially from its stated effectiveness, or whose stated effectiveness had no stated confidence, produces a catalogue update: a change to the expected effectiveness figure, to the confidence that accompanies it, to the preconditions, or to the failure modes. A catalogue entry that has never been exercised carries a stated effectiveness estimate that is an engineering judgement; an entry that has been exercised carries one that has been observed at least once, and the report says which it is.

### 2.12 Metrics

> **Guidance.** The metric **names** only are listed here. The definitions, the measurement windows, and the collection procedure live in `reference/audit-and-conformance-procedures.md`, which is the authoritative source for the MET- series. Do not restate a definition here, and do not report a metric whose definition you have not read: a figure produced from a remembered definition is not a measurement.

| Metric name | Value this operation | Basis and window | Notes |
| --- | --- | --- | --- |
| Detection coverage | «value or "not measured"» | «as defined in `reference/audit-and-conformance-procedures.md`» | «notes» |
| Autonomous-action interception rate | «value or "not measured"» | «as defined in `reference/audit-and-conformance-procedures.md`» | «notes» |
| False-positive cost | «value or "not measured"» | «as defined in `reference/audit-and-conformance-procedures.md`» | «notes» |
| Residual risk | «value» | «as defined in `reference/audit-and-conformance-procedures.md`» | «notes» |
| Mean time to detect | «value or "not measured"» | «as defined in `reference/audit-and-conformance-procedures.md`» | «notes» |
| Mean time to respond | «value or "not measured"» | «as defined in `reference/audit-and-conformance-procedures.md`» | «notes» |
| Mean time to recover | «value or "not measured"» | «as defined in `reference/audit-and-conformance-procedures.md`» | «notes» |
| «further metric names, if the audit procedures document defines more that bear on this operation» | «value» | «as defined in `reference/audit-and-conformance-procedures.md`» | «notes» |

> **Guidance.** "Not measured" is an acceptable entry. An invented figure is not, and a figure whose definition was not consulted is not. Where a metric could not be computed because the underlying data was degraded or absent, the report says so and names the data gap, because that data gap is itself a finding.

### 2.13 Gap list

| Gap ID | Description | Category | Severity | Effect on future operations | Owner | Target date | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| «GAP-nnn» | «the specific gap, stated so that closing it is testable» | «detection / containment / process / authority / platform / doctrine / content» | «high / medium / low» | «the concrete future consequence» | «name, role» | «YYYY-MM-DD» | «open / in progress / closed» |

> **Guidance.** A gap is a specific absence with a testable close condition. "Improve detection" is not a gap; "no sensor observes the tool-output channel on the gateway, so a technique executed on that path is invisible until it reaches an agent" is a gap, and its close condition is a named sensor or a named log change in production.

### 2.14 Detection-gap feedback entry

> **Guidance.** One entry is created for each gap that is a detection or coverage gap. The feedback entry is the mechanism by which the lesson returns to the taxonomy, the technique library, and the exercise programme. The worked example is in §2.18.

| Field | Req. | Value |
| --- | --- | --- |
| Feedback entry ID | Mandatory | «DFB-nnnn» |
| Raised from | Mandatory | «AAR id» |
| Technique | Mandatory | «AAT-n and technique» |
| Gap description | Mandatory | «what is not observed, and what the consequence is» |
| First observed | Mandatory | «YYYY-MM-DD» |
| Evidence | Mandatory | «claim ids, labels, tiers» |
| Coverage claim affected | Mandatory | «the claim of coverage that this falsifies or qualifies» |
| Proposed content change | Mandatory | «the indicator, detection method, or technique detail to be added or amended» |
| Proposed taxonomy change | Mandatory | «yes / no — and the change, or "none"» |
| Proposed exercise change | Mandatory | «the scenario or inject to be added to the programme» |
| Verification required | Mandatory | «how the change will be shown to work, and in what proving-ground run» |
| Owner | Mandatory | «name, role» |
| Status | Mandatory | «open / in progress / closed» |

### 2.15 Recommendations

| Rec ID | Recommendation | Basis | Owner | Priority | Target date | Status |
| --- | --- | --- | --- | --- | --- | --- |
| «REC-nn» | «the specific change, in imperative form» | «the finding, gap, or measurement it follows from — not "best practice"» | «name, role» | «high / medium / low» | «YYYY-MM-DD» | «open / in progress / closed» |

> **Guidance.** Every recommendation states its basis. A recommendation whose basis is "this is good practice" is not a recommendation; it is a preference, and it does not enter the register. A recommendation that follows from a gap carries the gap id; one that follows from a measurement carries the metric name and the figure.

### 2.16 Lessons-learned register

| Lesson ID | Lesson | Type | Derived from | Carried into |
| --- | --- | --- | --- | --- |
| «LL-nn» | «the lesson, stated as a proposition that will be true next time» | «control / process / technology / doctrine / judgement» | «AAR id, gap id, or recommendation id» | «the document, catalogue entry, exercise, or training item that will change» |

> **Guidance.** A lesson is written as a proposition that will be true next time, not as a narrative of what happened. "The signal was buried in a log nobody was reading" is a narrative; "a signal that arrives only in a log without a watchboard cue does not produce detection" is a lesson, and it can be tested.

### 2.17 Sign-off

| Role | Name | Organisation | Signature | Timestamp (UTC) | Basis for signing |
| --- | --- | --- | --- | --- | --- |
| Report author | «name» | «organisation» | «signature» | «timestamp» | «the report is accurate to the best of the author's knowledge» |
| Duty manager | «name» | «organisation» | «signature» | «timestamp» | «the gaps and recommendations are accepted» |
| Legal contact | «name» | «organisation» | «signature» | «timestamp» | «the collateral and disclosure assessment is accepted» |
| Framework owner | «name» | «organisation» | «signature» | «timestamp» | «the feedback entries are accepted into the taxonomy, catalogue, and exercise programme» |

### 2.18 Completeness checklist before filing

Every line is answered before the report is filed. "n/a" is written with a reason.

| # | Check | Answer |
| --- | --- | --- |
| 1 | The timeline reconciles with the decision log and the Ledger; every material decision appears in both | «yes / no — and the reconciliation record» |
| 2 | Every decision log entry has been assessed for soundness given what was known at the time | «yes / no» |
| 3 | Predicted and measured residual risk are both recorded, or the absence of the measurement is recorded as a gap | «yes / no» |
| 4 | Every undetected technique has a detection-gap feedback entry with an owner | «yes / no» |
| 5 | Every third-party effect is recorded, whether or not it was within the card, with disclosure recorded | «yes / no» |
| 6 | The attribution assessment states whether the attribution held up, and the calibration table is complete | «yes / no» |
| 7 | Every countermeasure exercised has an as-stated and an as-observed residual-risk figure | «yes / no» |
| 8 | Every metric reported has had its definition read from the audit procedures document; "not measured" is used where it could not be measured | «yes / no» |
| 9 | Every gap has a testable close condition, an owner, and a target date | «yes / no» |
| 10 | Every recommendation states a basis drawn from this operation's findings | «yes / no» |
| 11 | Every lesson is written as a proposition and is carried into a named artefact | «yes / no» |
| 12 | No assessment of the competence of named individuals appears in the report | «yes / no» |
| 13 | No absolute claim of system efficacy appears; unverified figures are marked as such | «yes / no» |
| 14 | The report is filed at G-7 Closeout, and the Ledger hash chain verifies for the operation | «yes / no» |

> **Guidance.** A report that fails any check is not filed in a state of completeness; it is filed with the failure recorded, and the failure becomes a gap. Filing an incomplete report with the incompleteness declared is acceptable. Filing it as though it were complete is not.

---

## 3. Worked example — detection-gap feedback entry

> **Example. Illustrative and fictional.** Every organisation, person, identifier, measurement, and adversary archetype below is invented for demonstration and refers to no real entity. The figures are illustrative arithmetic, not measurements.

| Field | Value |
| --- | --- |
| Feedback entry ID | DFB-2026-0009 |
| Raised from | AAR-2026-0021 (operation OP-2026-0142, fictional) |
| Technique | AAT-7, tool-output poisoning by direct instruction embedded in tool results |
| Gap description | The estate observes the tool-call gateway's egress and the agent execution log, but does not observe or retain the *content* of tool results returned to agents. A poisoned tool result that the agent did not act upon — because the instruction was malformed, or because the agent chose not to comply — leaves no artefact at all. Two such tool results were observed during the operation only because a subsequent execution was blocked and the blocked payload was retained; the other four attempts in the same window left no trace. The consequence is that the campaign's true volume is unknown, and the velocity component of the threat score is estimated from an incomplete set. |
| First observed | 2026-04-14 |
| Evidence | C-01 (Fact, Tier 1, 0.95 — retained blocked payload); C-18 (Fact, Tier 1, 0.90 — four attempts with no corresponding artefact); C-20 (Estimate, Tier 2, 0.65 — reconstructed campaign volume from the freight API's own published incident notice) |
| Coverage claim affected | The framework's coverage of AAT-7 rests on observing execution, not the preparation of the instruction. The coverage claim is therefore qualified: it is a detection coverage of execution, not of instruction delivery. That distinction was not stated in the technique library entry. |
| Proposed content change | Extend the AAT-7 technique entry to state explicitly that coverage is of execution, not of instruction delivery, and record the detection latency as applying to the execution stage. Add an indicator for the absence of an artefact following a tool-result delivery. |
| Proposed taxonomy change | No. The category is correct and the behaviour is correctly classified. The deficiency is in coverage and in the statement of coverage, not in the classification. |
| Proposed exercise change | Add an inject to the tabletop programme in which a poisoned tool result is delivered and not executed, and the operator is required to establish that the absence of an execution is not evidence of the absence of the attempt. The inject is written into `templates/tabletop-exercise-pack.md` as part of the scenario's inject sequence. |
| Verification required | A proving-ground run in which the simulator delivers poisoned tool results with a configurable execution rate. Coverage is demonstrated when the count of delivered-but-not-executed results is recoverable from the estate's own telemetry, with the delivery and execution counts reconciling. The run is recorded against the technique entry, with its date and its verification status. |
| Owner | Detection engineering lead (role), with the platform owner for the retention change |
| Status | Open |

> **Guidance.** The worked example shows the three parts of a useful feedback entry: the gap stated precisely enough to be testable, the coverage claim it qualifies, and the verification that would close it. It also shows the discipline of declining to amend the taxonomy when the taxonomy is not what is wrong.

---

## 4. Document limitations

1. **The report is a learning instrument, not an assurance statement.** A filed report does not establish that the framework works; it establishes what happened in one operation and what was learned from it.
2. **Confidence calibration cannot be established from one operation.** The report records cases. The calibration programme in `reference/audit-and-conformance-procedures.md` is where calibration is assessed, and this report does not claim to discharge it.
3. **Observed effectiveness is per-operation.** A countermeasure observed to work once against one adversary has not thereby been shown to work against another, and the report must not generalise beyond the case observed.
4. **The metric table lists names only.** The definitions live in `reference/audit-and-conformance-procedures.md`. Where the audit procedures document is unavailable, the metric values are not reported rather than reconstructed from memory.
5. **Attribution assessment after the fact is subject to the same weakness as attribution before it.** The operation gives better evidence; it does not give certainty, and the report must not present hindsight as calibration.
6. **The worked example is illustrative only.** The entities, figures, and timings in §3 are invented and describe no real operation, detection, or campaign.

---

*This was supported for MIA by Kilo (kilo-auto/free).*
