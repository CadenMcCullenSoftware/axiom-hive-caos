# Audit and Conformance Procedures

| Field | Value |
| --- | --- |
| Author | MIA |
| Attribution | This was supported for MIA by Kilo (kilo-auto/free). |
| Document type | Reference procedure |
| Subject | How conformance with the CAOS set is assessed, how the ledger is verified, how an operation is replayed, and what an auditor may and may not conclude from the record |
| Scope | The reference implementation under `impl/`, the append-only ledger, the replay procedure, the calibration programme, and the stated limits of the audit model |
| Companion documents | `system-design-and-framework.md`; `README.md`; `operational/decision-support-and-scoring-model.md`; `operational/mission-lifecycle-and-decision-loop.md`; `operational/countermeasure-catalogue.md`; `operational/platform-architecture-and-agent-containment.md`; `operational/emergency-shutdown-and-containment-protocol.md`; `reference/ai-attack-technique-library.md` |
| Verification pass | 2026-10 |
| Version | 1.1 |
| Status | Reference procedure. Not a certification scheme, and the set holds no accreditation or regulatory status |
| Revision note | Version 1.3 records the code review's findings and their closure: the suite stands at 359 tests with no failures. The material changes are listed at §3.15 — the countermeasure's status became an availability precondition, the third-party flag was tied to the direction of effect, the emergency prohibitions were given one live mechanism, the protected control set is matched by scope, the authority check covers the verification and transition paths, the autonomy grant is validated on the card, the export is validated on load and compared against its anchor, both synchronisers refuse a degraded document, the canonical JSON form is defined once, and the approval requirement is the union of the profile's and the collateral class's role sets. Version 1.2 re-derived the §3 register against the settled implementation: divergences D-1 to D-8 are all closed, each by a named instrument and each recorded with its test in §3.11. Version 1.1 recorded the register's first derivation. The divergence table is retained throughout: a closed divergence recorded as closed is the point of a register. |

---

## 1. Purpose and Scope

### 1.1 Purpose

This document is the auditor's charter for the CAOS set. It answers four questions:

| Question | Section |
| --- | --- |
| What does conformance with this set mean, and what can the record establish? | §1, §7, §8 |
| Which requirements are mechanically enforced, and by what? | §3 |
| How is the ledger verified, and what does tamper evidence establish? | §4 |
| How is an operation replayed, and what must replay be able to answer? | §5 |

It also records two things the set does not yet have: a calibration programme for confidence values (§6), and an explicit statement of what the audit model cannot do (§8, §9).

### 1.2 The scope of the evidence

The set's central proposition — that a reviewer who was not present can reconstruct an operation — is a claim about the *record*, not about the world. The distinction is load-bearing for every conclusion in this document, and it is stated here so that no reader has to infer it.

| The record can establish | The record cannot establish |
| --- | --- |
| That a decision was recorded, with the alternatives considered and the reason stated | That the reason was the operator's actual reason |
| That a countermeasure was admissible against the profile and card in force | That the profile in force was the correct profile for the situation |
| That an authorisation was given by a named person at the recorded depth | That the person had the authority the card asserted, or that the mandate existed |
| That the ledger's internal chain is intact at the point of audit | That the entries are complete, that none was omitted, or that the earliest entry is the true beginning |
| That an abort condition was written before the action | That the condition would have been met, or that its absence was noticed |
| That a claim was labelled and given a source tier | That the claim is true, or that the confidence is calibrated |
| That a countermeasure was selected from the ranked admissible set | That the selection was the best available, or that a lower-ranked option was wrongly rejected |
| That a residual risk figure was computed by the specified formula | That the inputs to the formula were correct, or that the figure is low in any absolute sense |

### 1.3 What this document does not do

- **It does not certify anything.** The set holds no certification, accreditation, or regulatory status, and no statement in this document may be read as conferring one.
- **It does not assess the framework's efficacy.** It assesses the framework's bookkeeping. Whether detection coverage improved, whether residual risk fell, and whether the operator's posture is stronger are measurement questions addressed by the set's measurement requirements, not by this procedure.
- **It does not create authority.** An auditor's finding that an operation was properly authorised is a statement about the record. It is not an authorisation for anything.
- **It does not replace the constitutional instrument.** The engagement authorisation and the rules-of-engagement profiles remain the only sources of authority for an action.
- **It does not assess human judgement.** Whether a given countermeasure was the right one, given the information available, is a question the record can frame and cannot answer.

### 1.4 Relationship to the master design and the set index

| Cross-reference | Where it points | Status |
| --- | --- | --- |
| Master design §11 LIM-14 | The mechanically-enforced requirements are listed in this document §3 | Consistent. §3 discharges it, and §3.11 records the divergences between the requirement texts and the implementation, with the resolution and the test for each |
| Master design §11 LIM-2 | Calibration data is tracked in this document §5 | **Divergent.** In this version the calibration programme is §6 and the replay procedure is §5. The master design's pointer should be amended to §6. Recorded as outstanding action 5 in §11.2 |
| Master design §11 LIM-1 | Attribution is the weakest link, and confidence thresholds bound the consequence of misattribution | Consistent. §8 states the corresponding conclusion limits |
| Master design §6.4 | A countermeasure is admissible if and only if all of AD-1 to AD-12 hold, with no aggregation and no judgement call inside the engine | Consistent as to the engine's structure. Divergences D-1 to D-3 in §3.11 record where the conditions' content differed from the requirement text, and each is now closed by a named instrument |
| Set index §4 | The implementation is asserted conformant with the model, and the requirements it mechanically enforces are listed in this document §3 | Consistent in substance, subject to §3.0, §3.12, and §8.2. The register states what the code does and where the evidence is; the judgement that the code is conformant is a human one and is not made in this document |
| Set index §4 | The master design §11 and this document §5 record what the framework does not establish | **Divergent.** In this version §8 records what may not be concluded. Recorded as outstanding action 6 in §11.2 |
| Master design §5.2 (TAX-5) | External mappings are recorded with a verification status and a date | Consistent. The register is in `reference/ai-attack-technique-library.md` §18 |
| Platform document §11 | The ledger's record structure, canonicalisation, digest computation, verification procedure, and export format | Consistent. The implementation follows the specification exactly, and the specification's own worked example is a test vector in the suite |
| Emergency protocol §22.1 | The emergency protocol's own mechanically-enforced surface is registered in that document | Consistent. This document's register covers the operational core; the emergency path is assessed against that document. See §3.11, D-8 |

---

## 2. RFC 2119 Interpretation

The key words **MUST**, **MUST NOT**, **REQUIRED**, **SHALL**, **SHALL NOT**, **SHOULD**, **SHOULD NOT**, **RECOMMENDED**, **MAY**, and **OPTIONAL** in this document are to be interpreted as described in RFC 2119, and only when they appear in capitals.

| Convention | Application in this document |
| --- | --- |
| **MUST** / **MUST NOT** | Binding on the auditor and on the operator. Used principally for the verification steps in §4 and §5, which are not optional if an audit is to be performed at all |
| **SHOULD** / **SHOULD NOT** | A strong recommendation, whose departure requires a recorded reason in the audit report |
| **MAY** | Optional, with no obligation either way |
| The registers in §3 | Normative as to *what is enforced* and *what is not*. Where a requirement is marked **Procedural only**, it is not enforced by the implementation and the assurance of its satisfaction rests on the operator's record and on human review |

The distinction between a mechanically-enforced requirement and a procedurally-satisfied one is the central distinction of this document. A requirement in the first category is tested by running code. A requirement in the second is tested by reading a document and talking to a person. Both are legitimate forms of assurance, and they are not comparable in strength.

---

## 3. The Mechanically-Enforced Requirement Register

### 3.0 Basis, snapshot, and what a conformance finding means

**What "mechanically enforced" means here.** A requirement is mechanically enforced where the reference implementation under `impl/` contains code that evaluates the requirement and returns a determination, such that a counterexample either cannot be constructed or causes the evaluation to fail. The determination is made by the code, not by a model, a rule written in prose, or a person's judgement.

**Snapshot.** This register was derived by inspection of the implementation source and the test suite at the following snapshot:

| Attribute | Value |
| --- | --- |
| Snapshot taken | 2026-10-20, 09:15 local |
| Implementation location | `impl/`, stdlib-only Python, package `caos` |
| Modules inspected | `vocab.py`, `models.py`, `taxonomy.py`, `countermeasures.py`, `scoring.py`, `roe.py`, `decision.py`, `ledger.py`, `watchfloor.py`, `emergency.py`, `emergency_console.py`, `proving_ground.py`, `cli.py`, `demo.py`, `version.py`, and the generated `taxonomy_data.py` and `catalogue_data.py` |
| Tests inspected | `impl/tests/`: `test_vocab.py`, `test_catalogue.py`, `test_roe.py`, `test_scoring.py`, `test_decision.py`, `test_ledger.py`, `test_watchfloor.py`, `test_emergency.py`, `test_bindings.py` |
| Tools inspected | `impl/tools/sync_taxonomy.py`, `impl/tools/sync_catalogue.py` |
| Suite | 364 tests collected, no failures |
| Drift check | `python3 tools/sync_taxonomy.py --check` and `python3 tools/sync_catalogue.py --check` both report the implementation in agreement with the canonical documents |

**The implementation is settled for this revision.** The register below is a point-in-time statement about a codebase that is no longer moving. The previous revision of this document was written against a moving target, and the difference is worth recording: where the implementation changed under the auditor's hand, the register had to be re-derived, and the divergences that were open are now closed by a named instrument each.

**This register is not a certification.** It is a statement about what the code does and where the evidence for that statement is. Every row names the function that implements the requirement and the test that demonstrates it, so that a reader can check the claim rather than accept it. **The judgement that the implementation is conformant with the framework remains a human one**, and is not made here. The register supports that judgement; it does not make it. Master design LIM-14 continues to hold: the implementation does not verify that a produced document satisfies the prose requirements of the conduct standard, the rules-of-engagement document, or the master design, and nothing in this register changes that.

**How to read the test column.** The test column names the test function in the suite that demonstrates the row's behaviour, and the test class where the class name carries information. An auditor working against a different snapshot must re-identify the corresponding test.

**Three statuses are used.**

| Status | Meaning |
| --- | --- |
| **Mechanically enforced** | The implementation evaluates the requirement and returns a determination that a counterexample would contradict, and a test demonstrates the behaviour |
| **Requires confirmation** | The check is stated in the code, but the behaviour is not demonstrated by a test at this snapshot, or the correspondence between the code and the requirement text is a matter of interpretation. An auditor must confirm before relying on it |
| **Procedural only** | Not evaluated by the implementation. Assurance rests on the operator's record, the human-in-the-loop controls, and review |

**The narrowness of the register is itself a finding.** Master design LIM-14 records that the implementation does not verify that a produced document satisfies the prose requirements of the conduct standard, the rules-of-engagement document, or the master design. This register quantifies that limitation rather than restating it. The framework contains a large body of normative requirements that the reference implementation does not touch, and a conformance assessment that reported only the mechanically-enforced rows would materially misrepresent the framework's enforcement surface.

### 3.1 The admissibility algebra — AD-1 to AD-13

The admissibility algebra is the enforcement surface of the authorisation model. Master design §6.4 states that a countermeasure is admissible if and only if all of AD-1 to AD-12 hold, that any single failure makes it inadmissible, and that there is no aggregation and no judgement call inside the engine.

`caos/roe.py` exposes `evaluate(card, cm, context) -> AdmissibilityResult` and `evaluate_all(...)`. Each condition is a `_check_adN` function returning a `CheckResult` carrying the condition identifier, a title, a nature, a pass flag, a detail string, a margin string, and a remedy string. `AdmissibilityResult.admissible` is the conjunction of all the pass flags, and `AdmissibilityResult.failures` converts the failed checks into `AdmissibilityFailure` records. `CONDITION_TITLES` gives every condition a title and `CONDITION_NATURE` classifies it as machine, hybrid, or human.

| Requirement | What the implementation checks | Module or function | Test | Status |
| --- | --- | --- | --- | --- |
| **AD-1** — C's class is in P's permitted class set | Two things in conjunction: the countermeasure's class is a member of the profile's permitted class set, **and** the card's profile is at or above the countermeasure's declared minimum profile. Either failure refuses, and the refusal names which of the two failed | `caos/roe.py` — `_check_ad1`; `caos/vocab.py` — `ROEProfile.permitted_classes` | `AD1ProfileClassTests.test_class_outside_the_profile_is_refused`, `.test_class_inside_the_profile_passes`, `.test_countermeasure_floor_above_the_card_profile_is_refused` | Mechanically enforced |
| **AD-2** — C's collateral class ≤ K's collateral ceiling | The countermeasure's collateral class is compared against the effective ceiling, which is the lower of the card's ceiling and the profile's ceiling. The refusal states the margin in classes | `caos/roe.py` — `_check_ad2` | `AD2CollateralTests.test_collateral_above_the_ceiling_is_refused`, `.test_collateral_above_the_profile_ceiling_is_refused`, `.test_collateral_within_the_ceiling_passes` | Mechanically enforced |
| **AD-3** — C's reversibility ≥ K's required reversibility | The reversibility ordinal is compared against the card's floor. Where the countermeasure's reversibility is Low or None, the condition additionally requires a recorded irreversibility argument on the card, so the ROE-7 argument is enforced rather than assumed | `caos/roe.py` — `_check_ad3`; `caos/vocab.py` — `Reversibility`; card field `OperationCard.irreversibility_argument` | `AD3ReversibilityTests.test_reversibility_below_the_floor_is_refused`, `.test_reversibility_at_or_above_the_floor_passes`; `AD3IrreversibilityArgumentTests` in `tests/test_attestations.py` demonstrates the argument limb in both its failing and its passing state | Mechanically enforced, including the argument limb |
| **AD-4** — C's target set ⊆ K's authorised target set | **Two limbs.** Where the catalogue entry names specific targets, the test is set containment: every named target must be on the card's authorised target set, and the refusal names the targets outside it. Where the entry names none, the test falls back to scope-prefix coverage against the countermeasure's direction of effect, and the refusal names the missing prefix | `caos/roe.py` — `_check_ad4`, `_SCOPE_PREFIX`, `_targets_with_prefix`; `caos/models.py` — `Countermeasure.targets` | `AD4SetContainmentTests.test_a_named_target_outside_the_card_is_refused`, `.test_a_named_target_on_the_card_passes`, `.test_an_entry_without_named_targets_falls_back_to_the_scope_test`; `AD4TargetContainmentTests.test_missing_scope_is_refused`, `.test_adversary_direction_needs_an_adversary_target` | Mechanically enforced |
| **AD-5** — C does not affect an unauthorised third party | A countermeasure that neither touches a third party nor acts in a shared environment passes. One acting in the operator's own shared environment must carry the shared-tenancy assessment. One at collateral class C0 passes, because C0 is defined as having no effect outside the operator's own estate. Otherwise the check requires the third-party authorisation flag, a recorded shared-tenancy assessment, a named third-party or adversary target, a matching per-target written authorisation, and a countermeasure whose status is not Withheld | `caos/roe.py` — `_check_ad5`; card fields `third_party_authorised`, `third_party_assessment`, `per_target_authorisations` | `AD5ThirdPartyTests.test_third_party_effect_without_authorisation_is_refused`, `.test_missing_tenancy_assessment_is_refused`, `.test_own_estate_countermeasure_passes`, `.test_a_c0_outward_countermeasure_needs_no_third_party_authorisation` | Mechanically enforced |
| **AD-6** — C does not target human beings as its object | The countermeasure's `targets_humans` flag must be false; the catalogue constructor refuses to construct such a countermeasure at all. Where the card declares a technique in a category that operates on people, the operator's indirect-effect attestation is required | `caos/roe.py` — `_check_ad6`, `HUMAN_FACING_CATEGORIES`; `caos/models.py` — `Countermeasure.__post_init__`; card field `OperationCard.indirect_effect_attestation` | `AD6HumanBeingsTests.test_a_countermeasure_targeting_people_cannot_be_constructed`, `.test_condition_passes_for_a_catalogued_countermeasure`; `AD6IndirectEffectTests` in `tests/test_attestations.py` demonstrates the indirect-effect attestation in both its failing and its passing state | Mechanically enforced, including the attestation limb |
| **AD-7** — C's autonomy class ≤ K's autonomy class | For AC-4 the check is a special case: read-only, collateral class C0, a profile that permits read-only autonomy, and a card autonomy ceiling at or above AC-4. Otherwise the countermeasure's autonomy must be at or below both the card's ceiling and the profile's ceiling | `caos/roe.py` — `_check_ad7`; `caos/models.py` — `Countermeasure.__post_init__` | `AD7AutonomyTests.test_autonomy_above_the_card_ceiling_is_refused`, `.test_autonomy_above_the_profile_ceiling_is_refused`, `.test_autonomous_execution_is_refused_at_a_raised_ceiling`, `.test_autonomous_execution_needs_a_raised_ceiling`, `.test_non_read_only_autonomous_execution_cannot_be_constructed` | Mechanically enforced |
| **AD-8** — C's effectiveness confidence q ≥ K's minimum q | The countermeasure's declared effectiveness confidence is compared against the card's floor, and the refusal states the shortfall to two decimal places | `caos/roe.py` — `_check_ad8` | `AD8ConfidenceTests.test_confidence_below_the_floor_is_refused`, `.test_confidence_at_or_above_the_floor_passes`, `.test_very_low_confidence_entries_fail_a_higher_floor` | Mechanically enforced |
| **AD-9** — C's attribution dependency is satisfied by the card's attribution confidence | The countermeasure's attribution dependency selects the confidence that is tested. No dependency passes outright. An external dependency requires the external determination to be on file. An identity dependency is tested against the card's recorded attribution confidence. A class or behavioural dependency is tested against the class confidence supplied in the evaluation context. The threshold is the collateral class's entry in the attribution threshold table | `caos/roe.py` — `_check_ad9`; `caos/vocab.py` — `AttributionDependency`, `attribution_threshold`, `ATTRIBUTION_THRESHOLDS` | `AD9AttributionTests.test_identity_dependent_action_below_the_threshold_is_refused`, `.test_identity_dependent_action_above_the_threshold_passes`, `.test_identity_independent_action_passes_at_low_confidence`, `.test_external_dependency_requires_the_external_determination` | Mechanically enforced |
| **AD-10** — C passes the deconfliction check against live operations | The deconfliction must be recorded as passed, **and** the deconfliction map must be recorded as current or the operator must have attested that the conflict has been assessed. A degraded map with no attestation is refused | `caos/roe.py` — `_check_ad10`; card fields `deconfliction_passed`, `deconfliction_map_current`, `deconfliction_attestation` | `AD10DeconflictionTests.test_failed_deconfliction_is_refused`, `.test_passed_deconfliction_passes`; `AD10DeconflictionAttestationTests` in `tests/test_attestations.py` demonstrates the map-currency and attestation limbs in both their failing and their passing state | Mechanically enforced, including the attestation limb |
| **AD-11** — C's autonomy needs fit within the card's remaining autonomy budget | A countermeasure at AC-0 or AC-1 draws no budget, because a human performs or approves every step. At AC-2 and above the countermeasure's autonomy units are compared against the card's remaining budget, and the refusal states the shortfall in units | `caos/roe.py` — `_check_ad11`; `caos/models.py` — `OperationCard.remaining_budget` | `AD11BudgetTests.test_insufficient_budget_is_refused`, `.test_sufficient_budget_passes` | Mechanically enforced |
| **AD-12** — C does not violate the non-weaponisation constraint | A countermeasure whose declared effect is to degrade the adversary's model is refused outright as a binary condition. Otherwise the condition passes where the catalogue declares conformity with the boundary or the operator has attested the boundary analysis | `caos/roe.py` — `_check_ad12`; `caos/models.py` — `Countermeasure.__post_init__`; card field `OperationCard.non_weaponisation_attestation` | `AD12NonWeaponisationTests.test_a_weaponising_countermeasure_cannot_be_constructed`, `.test_condition_passes_for_a_catalogued_countermeasure`; `AD12NonWeaponisationTests` in `tests/test_attestations.py` demonstrates the declaration-or-attestation limb in both its failing and its passing state | Mechanically enforced, including the attestation limb |
| **AD-13** — Inadmissibility is informative | Implemented as a property of the result rather than as a further condition: `AdmissibilityResult.failures` yields an `AdmissibilityFailure` for each failed check, carrying the condition, its title, the detail, the margin of exceedance, and a remedy. `AdmissibilityResult.blocking_summary` renders the refusal as one line naming each failed condition and its margin | `caos/roe.py` — `AdmissibilityResult.failures`, `.blocking_summary`; `caos/models.py` — `AdmissibilityFailure`, `.as_dict` | `InformativeFailureTests.test_rejection_states_the_condition_and_the_margin`, `.test_every_condition_is_titled_and_classified` | Mechanically enforced |

**Note on the engine's failure mode.** `evaluate()` returns a determination; it does not raise on a counterexample. `FailClosedTests.test_engine_never_raises_on_a_permitted_countermeasure` asserts that the engine does not raise where the countermeasure is permitted. An exception raised in place of a refusal would be a failure of the control, not a success.

### 3.2 The card-armability preconditions — G-3

A card-level precondition evaluated inside the same function as the algebra. `roe.card_is_armable(card, now)` returns the reasons a card cannot carry a dispatch, and `evaluate()` appends the failing check when that list is non-empty.

| Requirement | What the implementation checks | Module or function | Test | Status |
| --- | --- | --- | --- | --- |
| **G-3 — the card is armable** | A card that has expired, that carries a blocking completion defect, or that lacks a required approval fails the check, and the whole evaluation is inadmissible. The card's mandatory fields, the requirement that excluded targets be stated affirmatively, the requirement that the risk of inaction be recorded, and the requirement that alternatives be recorded are all enforced here | `caos/roe.py` — `card_is_armable`, `evaluate`; `caos/models.py` — `OperationCard.completion_defects`, `.expired`, `.approval_gap`, `.MANDATORY_FIELDS` | `CardArmabilityTests.test_expired_card_is_not_armable`, `.test_incomplete_card_is_not_armable`, `.test_missing_risk_of_inaction_is_a_defect`, `.test_missing_alternatives_is_a_defect`, `.test_missing_excluded_targets_is_a_defect`, `.test_missing_approvals_blocks_arming`, `.test_incomplete_card_refuses_every_countermeasure`, `.test_complete_card_is_armable` | Mechanically enforced |
| **A card's technique references resolve against the registry** | `OperationCard.unknown_techniques()` returns the card's technique references that the registry does not carry, and `completion_defects()` treats any such reference as a blocking defect, so a card citing an unknown identifier cannot be armed | `caos/models.py` — `OperationCard.unknown_techniques`, `.completion_defects`; `caos/taxonomy.py` — `TECHNIQUE_INDEX` | `CardArmabilityTests.test_an_unregistered_technique_reference_is_a_defect`, `.test_a_registered_technique_reference_is_not_a_defect` | Mechanically enforced |
| **The pre-registered contingency is timestamped** | A card that carries contingency text with no `contingency_recorded_at` is a blocking defect, so a contingency written after the action cannot satisfy the field. `DecisionRecord` carries the timestamp, so the record shows when the contingency was written relative to the action | `caos/models.py` — `OperationCard.contingency_recorded_at`, `.completion_defects`; `caos/decision.py` — `select` | `CardArmabilityTests.test_a_contingency_without_a_timestamp_is_a_defect`, `.test_a_timestamped_contingency_is_not_a_defect` | Mechanically enforced |

### 3.3 The scoring model

| Requirement | What the implementation checks | Module or function | Test | Status |
| --- | --- | --- | --- | --- |
| **S = L × I × A × V** | The score is the product of the four components, computed as a property of the threat assessment. The constructor refuses a likelihood outside [0.0, 1.0], an impact outside 0 to 5, an autonomy factor outside 0 to 2, a velocity outside 0 to 2, an attribution confidence outside [0.0, 1.0], and an empty attribution basis | `caos/models.py` — `ThreatAssessment.__post_init__`, `.score`; `caos/scoring.py` — `threat_score` | `ThreatScoreTests.test_score_is_the_product_of_its_components`, `.test_score_range_is_zero_to_twenty`, `.test_out_of_range_components_are_rejected` | Mechanically enforced |
| **S_eff = S × c** | The effective threat is the score multiplied by the attribution confidence, computed both as an assessment property and as a standalone function | `caos/models.py` — `ThreatAssessment.effective_threat`; `caos/scoring.py` — `effective_threat` | `ThreatScoreTests.test_effective_threat_applies_attribution_confidence`, `.test_zero_attribution_gives_zero_effective_threat` | Mechanically enforced |
| **R = S_eff × (1 − e)** | The residual risk is the effective threat multiplied by the complement of the expected effectiveness. An effectiveness outside [0.0, 1.0] raises rather than producing a figure | `caos/scoring.py` — `residual_risk`, `residual_risk_after` | `ResidualRiskTests.test_residual_risk_reduces_with_effectiveness`, `.test_effectiveness_out_of_range_is_rejected` | Mechanically enforced |
| **P = (S_eff / 20) × q × (1 − r)** | The priority is the normalised effective threat multiplied by the effectiveness confidence and by the complement of the collateral exposure, where the exposure is the normalised value fixed for the countermeasure's collateral class. A confidence outside [0.0, 1.0] raises | `caos/scoring.py` — `risk_adjusted_priority`; `caos/vocab.py` — `CollateralClass.exposure`, `_COLLATERAL_EXPOSURE` | `PriorityTests.test_priority_discounts_collateral_exposure`, `.test_priority_is_zero_at_full_collateral`, `.test_priority_scales_with_effective_threat` | Mechanically enforced |
| **P is a ranking only** | The priority value does not gate selection. `filter_admissible` returns admissible and rejected sets on admissibility alone, and `rank_candidates` orders the survivors by descending priority with the identifier as a tie-break. The operator may select any admissible candidate | `caos/decision.py` — `filter_admissible`, `rank_candidates`, `select` | `RankingTests.test_candidates_are_ranked_by_descending_priority`, `.test_ranking_breaks_ties_on_the_identifier`; `SelectionTests.test_selection_produces_a_reconstructible_record` | Mechanically enforced |
| **SCORE-2 — components are separately contestable** | `score_breakdown` returns each component with its value, its documented range, and the reasoning recorded against it. The four reasoning fields are separate fields on the threat assessment, so a reviewer can dispute one component without disputing the assessment | `caos/scoring.py` — `score_breakdown`; `caos/models.py` — `ThreatAssessment` | `ThreatScoreTests.test_velocity_is_visible_as_a_separate_component`; `SelectionTests.test_the_record_states_the_threat_components` | Mechanically enforced as to exposure; the adequacy of the recorded reasoning is procedural |
| **INT-9 — derived claims inherit the weakest input, less a declared penalty** | The derived confidence is the least confident input minus the declared derivation penalty, floored at zero. The operation is **subtractive**: `c_derived = c_weakest − p`. The penalty must be declared — `derivation_penalty` raises for a derivation kind absent from the declared table, and the table itself is not empty | `caos/scoring.py` — `propagate_confidence`, `derivation_penalty`, `DERIVATION_PENALTIES`; `caos/models.py` — `Claim.propagated_confidence` | `ConfidencePropagationTests.test_derived_confidence_is_the_weakest_input`, `.test_penalty_reduces_the_propagated_value`, `.test_propagation_never_returns_a_negative_confidence`, `.test_propagation_is_the_most_conservative_of_the_two_forms`, `.test_derivation_penalties_are_declared`, `.test_penalty_table_is_not_empty` | Mechanically enforced |
| **SCORE-5 — residual risk against the risk of inaction** | The do-nothing option is computed as an explicit alternative carrying the card's recorded risk of inaction, the options are ordered by residual risk, and an inadmissible option is marked in its note | `caos/decision.py` — `counterfactuals`; `caos/scoring.py` — `compare_options` | `CounterfactualTests.test_the_do_nothing_option_is_included`, `.test_options_are_ordered_by_residual_risk`, `.test_inadmissible_options_are_marked_in_the_note` | Mechanically enforced as to the option being present; the adequacy of the recorded risk of inaction is procedural |

### 3.4 The ceilings, the profile, expiry, and approval depth

| Requirement | What the implementation checks | Module or function | Test | Status |
| --- | --- | --- | --- | --- |
| **ROE-1 — the profile is the ceiling** | The card's profile is the only source of the ceiling. AD-1 refuses a countermeasure whose class is outside the profile's permitted set or whose minimum profile is above the card's, and AD-2 refuses a countermeasure above the profile's collateral ceiling. No input to the evaluation raises the profile | `caos/roe.py` — `_check_ad1`, `_check_ad2`; `caos/vocab.py` — `ROEProfile` | `AD1ProfileClassTests.test_class_outside_the_profile_is_refused`, `.test_countermeasure_floor_above_the_card_profile_is_refused`; `AD2CollateralTests.test_collateral_above_the_profile_ceiling_is_refused` | Mechanically enforced |
| **ROE-2 — the engine fails closed** | The evaluation always returns a determination, admissible or not, and the refusal carries the condition, the margin, and a remedy. The refusal is a successful control and is retained with its reasons rather than discarded | `caos/roe.py` — `evaluate`; `caos/decision.py` — `filter_admissible` | `FilteringTests.test_rejections_are_retained_with_reasons`, `.test_no_candidate_is_lost_between_generation_and_filtering` | Mechanically enforced |
| **ROE-3 — escalation is a new instrument** | The profile is a field on the card and the engine reads it. The countermeasure's own minimum-profile floor is checked against it, so a countermeasure requiring a higher profile is refused with the margin naming both profiles | `caos/roe.py` — `_check_ad1`; `caos/models.py` — `OperationCard.profile` | `AD1ProfileClassTests.test_countermeasure_floor_above_the_card_profile_is_refused` | Mechanically enforced as to the refusal; the procedural requirement that escalation also produce a new authorisation and a new card is not evaluated |
| **ROE-6 — collateral class governs, not intent** | The class tested is the countermeasure's declared `collateral` field, which is the class of the effect as recorded in the catalogue, and not any statement of purpose | `caos/models.py` — `Countermeasure.collateral`; `caos/vocab.py` — `DirectionOfEffect`; `caos/roe.py` — `_check_ad2` | `CatalogueIntegrityTests.test_catalogue_holds_forty_three_entries`, `.test_every_entry_declares_its_direction`, `.test_disruptive_entries_never_exceed_class_c2` | Mechanically enforced as to the class being read from the effect metadata; the substantive correspondence between the catalogue's declared effect and the class is a catalogue-quality matter |
| **ROE-8 — escalation on class** | The approval depth required is the more demanding of the profile's depth and the collateral class's depth; the two are not unioned, because a profile ceiling already governs the collateral class it permits | `caos/vocab.py` — `required_approvals`, `approval_depth_rank`, `APPROVAL_DEPTHS`, `COLLATERAL_APPROVALS` | `ApprovalDepthTests.test_more_demanding_of_profile_and_collateral_prevails`, `.test_higher_profile_demands_more_than_low_collateral`, `.test_every_profile_has_a_depth` | Mechanically enforced |
| **AC-4 prohibition above C0** | A countermeasure at AC-4 is admissible only where it is read-only, at collateral class C0, at a profile that permits read-only autonomy, and against a card autonomy ceiling at or above AC-4. The catalogue constructor additionally refuses to construct an AC-4 countermeasure that is not read-only at C0 | `caos/roe.py` — `_check_ad7`; `caos/models.py` — `Countermeasure.__post_init__` | `AD7AutonomyTests.test_autonomous_execution_is_refused_at_a_raised_ceiling`, `.test_autonomous_execution_needs_a_raised_ceiling`, `.test_non_read_only_autonomous_execution_cannot_be_constructed`; `CatalogueIntegrityTests.test_autonomous_entries_are_read_only_and_c0` | Mechanically enforced |
| **AUTH-3 — expiry is a hard stop** | A card whose expiry has passed is not armable, and the armability check is part of the admissibility evaluation. The refusal states the expiry time and that an expired card authorises nothing | `caos/roe.py` — `card_is_armable`; `caos/models.py` — `OperationCard.expired` | `CardArmabilityTests.test_expired_card_is_not_armable` | Mechanically enforced |
| **HITL-1 — a named approver at the required depth** | The card's approval gap is the required approval roles minus the roles actually recorded, and a card with a gap is not armable. The roles are role identifiers, not named individuals, and the card records the roles rather than the persons | `caos/models.py` — `OperationCard.approval_gap`, `.required_approvals`; `caos/roe.py` — `card_is_armable` | `CardArmabilityTests.test_missing_approvals_blocks_arming`; `RoeGateTests.test_gate_lists_the_approvals_required` | Mechanically enforced as to the approval depth; the identity of the approver and their substantive reading of the card are procedural |
| **OP-1 — no operation without a card** | The card's mandatory fields are checked before arming: objective, hypothesis, disconfirming observation, engagement authorisation reference, authorised targets, abort conditions, abort owner, abort mechanism, rationale, and contingency, together with the threat assessment, the excluded targets, the risk of inaction, and the alternatives considered | `caos/models.py` — `OperationCard.MANDATORY_FIELDS`, `.completion_defects`; `caos/roe.py` — `card_is_armable` | `CardArmabilityTests.test_incomplete_card_is_not_armable`, `.test_incomplete_card_refuses_every_countermeasure`; `FilteringTests.test_a_card_that_cannot_be_armed_admits_nothing` | Mechanically enforced as to the presence of the fields; their adequacy is procedural |
| **HITL-5 — reversion on abort** | The Watchfloor's abort command reverts the posture to Observe, consumes the remaining autonomy budget, and writes to the ledger. The command is human-initiated; there is no signal-driven reversion in the implementation | `caos/watchfloor.py` — `Watchfloor.abort` | `AbortTests.test_abort_records_the_reason_and_reverts_posture`, `.test_abort_writes_to_the_ledger`, `.test_abort_consumes_the_autonomy_budget` | The manual abort is mechanically implemented; the **automatic** reversion required by HITL-5 is **procedural only** |

### 3.5 The third-party exclusion

| Requirement | What the implementation checks | Module or function | Test | Status |
| --- | --- | --- | --- | --- |
| **AD-5 — the exclusion** | As set out in §3.1. The check is affirmative: the card must carry the third-party authorisation flag, a recorded shared-tenancy assessment, a named third-party or adversary target, and a per-target written authorisation covering that target, and the countermeasure must not be in Withheld status | `caos/roe.py` — `_check_ad5`, and the `PRE` availability check; `caos/models.py` — `OperationCard.third_party_authorised`, `.third_party_assessment`, `.per_target_authorisations`, `Countermeasure.status` and its guard tying `touches_third_party` to `direction` | `AD5ThirdPartyTests.test_third_party_effect_without_authorisation_is_refused`, `.test_missing_tenancy_assessment_is_refused`, `.test_own_estate_countermeasure_passes`, `.test_a_c0_outward_countermeasure_needs_no_third_party_authorisation` | Mechanically enforced |
| **AUTH-6 — per-target written authorisation** | The per-target authorisation set on the card is consulted, and a target without a matching entry refuses the countermeasure. The general third-party flag does not substitute for the per-target entry | `caos/roe.py` — `_check_ad5`; `caos/models.py` — `OperationCard.per_target_authorisations` | `AD5ThirdPartyTests.test_third_party_effect_without_authorisation_is_refused`; `AD5PerTargetAuthorisationTests` in `tests/test_attestations.py` demonstrates the per-target authorisation, the shared-tenancy assessment, and the Withheld-status refusal | Mechanically enforced |
| **AUTH-7 — identity over infrastructure** | The catalogue records each countermeasure's direction of effect, its collateral class, and its attribution dependency, and the catalogue's integrity tests assert that entries directed at the adversary's own systems above C0 require identity attribution, and that identity-free entries exist. The preference for identity-directed action is a property of the catalogue's construction rather than a rule the engine applies at evaluation time | `caos/countermeasures.py` — `CATALOGUE`; `caos/catalogue_data.py`; `caos/roe.py` — `_check_ad9` | `CatalogueIntegrityTests.test_outward_entries_above_c0_require_identity_attribution`, `.test_an_outward_c0_entry_may_depend_on_class_attribution`, `.test_identity_free_entries_exist_in_the_catalogue` | Mechanically enforced as a catalogue invariant; the comparative preference between two admissible countermeasures is an operator judgement and is procedural |
| **AUTH-8 — the shared-tenancy test** | The **presence** of the shared-tenancy assessment on the card is enforced, and its absence refuses any countermeasure that acts in a shared environment or affects a third party. The **content** of the assessment is not evaluated: the check tests that the field is non-empty, not that the answers are adequate | `caos/roe.py` — `_check_ad5`; `caos/models.py` — `OperationCard.third_party_assessment` | `AD5ThirdPartyTests.test_missing_tenancy_assessment_is_refused` | Mechanically enforced as to presence; the adequacy of the answers is procedural |
| **CON-3 — purpose limitation** | The card's objective, hypothesis, and disconfirming observation are mandatory fields, so a card without them cannot be armed | `caos/models.py` — `OperationCard.MANDATORY_FIELDS` | `CardArmabilityTests.test_incomplete_card_is_not_armable` | Partly enforced — presence only; the purpose limitation itself is procedural |

**Note on the exclusion's reach.** AD-5 and AUTH-6 are among the most consequential checks in the set, because they are the ones that stop a countermeasure reaching beyond the operator's estate. They are also the checks most dependent on correct card data: the exclusion is enforced against the authorised-target, third-party, and per-target authorisation sets as recorded, and a card that records a third party as authorised is the failure mode the check cannot detect. This is recorded as limitation LIM-AU7.

### 3.6 The attribution thresholds — INT-3

| Requirement | What the implementation checks | Module or function | Test | Status |
| --- | --- | --- | --- | --- |
| **INT-3 — thresholds by consequence** | The minimum attribution confidence is a function of the countermeasure's collateral class: 0.50 at C0, 0.70 at C1, 0.85 at C2, 0.95 at C3. The table is consulted by the AD-9 evaluation | `caos/vocab.py` — `ATTRIBUTION_THRESHOLDS`, `attribution_threshold`; `caos/roe.py` — `_check_ad9` | `AttributionThresholdTests.test_thresholds_rise_with_consequence`, `.test_threshold_table_matches_documentation`; `AD9AttributionTests.test_identity_dependent_action_below_the_threshold_is_refused`, `.test_identity_dependent_action_above_the_threshold_passes` | Mechanically enforced |
| **INT-3 — refusal at C3** | A countermeasure at C3 whose identity dependency is not met by the recorded confidence is refused, and the refusal names the shortfall. No input to the evaluation lowers the threshold | `caos/roe.py` — `_check_ad9` | `AD9AttributionTests.test_identity_dependent_action_below_the_threshold_is_refused` | Mechanically enforced |
| **INT-3 — recording, second review, and approval depth** | The approval-depth element is enforced through the card's approval gap, in the same way as for any other class. The recording and second-review elements are properties of the workflow and are not evaluated | `caos/models.py` — `OperationCard.approval_gap`; `caos/vocab.py` — `required_approvals` | `CardArmabilityTests.test_missing_approvals_blocks_arming` | The approval-depth element is mechanically enforced; the second-review element is **procedural only** |
| **INT-4 — identity confidence is distinct from class confidence** | The attribution dependency is a typed field on the countermeasure, with `none`, `behavioural`, `class`, `identity`, and `external` as distinct values. A countermeasure with no attribution dependency passes outright at any confidence. One depending on class or behavioural recognition is tested against the class confidence, so a low identity confidence does not block it | `caos/vocab.py` — `AttributionDependency`; `caos/roe.py` — `_check_ad9` | `AD9AttributionTests.test_identity_independent_action_passes_at_low_confidence` | Mechanically enforced |
| **INT-6 — collective attribution** | The dependency typing is the structural expression of the distinction, in that a class-level dependency is a first-class alternative to an identity dependency. The stronger form of INT-6, that a class-level finding cannot support a countermeasure against a third party, is not separately evaluated: the engine tests a single scalar attribution confidence against the threshold | `caos/vocab.py` — `AttributionDependency`; `caos/roe.py` — `_check_ad9` | `AD9AttributionTests.test_identity_independent_action_passes_at_low_confidence` | Partly enforced — the typing is enforced; the third-party consequence of a class-level finding is procedural |

### 3.7 The autonomy budget, the grant, and the dispatch path

| Requirement | What the implementation checks | Module or function | Test | Status |
| --- | --- | --- | --- | --- |
| **AD-11 — budget fit** | As set out in §3.1. The budget is the card's declared total less the consumed units, and the remaining value is what a countermeasure is tested against | `caos/roe.py` — `_check_ad11`; `caos/models.py` — `OperationCard.remaining_budget` | `AD11BudgetTests.test_insufficient_budget_is_refused`, `.test_sufficient_budget_passes` | Mechanically enforced |
| **AUT-4 — declared envelope, budget, expiry, and reversion trigger** | The `AutonomyGrant` record requires an expiry after the grant, a non-negative budget, a named on-call operator, and a non-empty reversion trigger, and refuses construction otherwise | `caos/models.py` — `AutonomyGrant.__post_init__`, `.expired`, `.remaining`; `OperationCard.autonomy_grant`, `.autonomy_budget`, `.autonomy_consumed`, `.autonomy_on_call`, `.autonomy_reversion_trigger` | `CountermeasureConsoleTests.test_autonomy_monitor_renders`; `CardArmabilityTests` for the completeness requirement | The declaration is mechanically enforced; the envelope's scope is not evaluated |
| **The budget is debited on dispatch** | `dispatch` re-evaluates the admissibility algebra at dispatch time, because both the card's state and the world may have changed since the selection. On a successful dispatch it debits `card.autonomy_consumed` by the countermeasure's autonomy units and writes a `dispatch.issued` record to the ledger carrying the units spent, the remaining budget, the collateral class, and the reversibility. On a refusal it spends nothing, returns the failing conditions, and writes a `dispatch.refused` record | `caos/decision.py` — `dispatch`, `DispatchResult`; `caos/ledger.py` — `Ledger.append`, `.of_kind` | `DispatchTests.test_a_dispatch_debits_the_autonomy_budget`, `.test_a_refused_dispatch_spends_nothing`, `.test_a_refusal_is_recorded_in_the_ledger`, `.test_a_dispatch_is_recorded_in_the_ledger` | Mechanically enforced |
| **The dispatch path is exposed to the operator** | The dispatch is reachable from the console and from the command line, and the console states the units spent and the remaining budget on a success, or that nothing was executed and no budget was spent on a refusal | `caos/watchfloor.py` — `Watchfloor.dispatch`; `caos/cli.py` — the `dispatch` subcommand | `DispatchTests` demonstrates the function; the console and command-line surfaces are not separately under test | **Requires confirmation** for the surfaces; the function beneath them is mechanically enforced |
| **HITL-3 — the abort channel is tested first** | The abort channel exists as a console command that reverts the posture, consumes the budget, and writes to the ledger. Whether it was demonstrated before the operation began is a record on the card and in the exercise, and is not enforced | `caos/watchfloor.py` — `Watchfloor.abort` | `AbortTests.test_abort_records_the_reason_and_reverts_posture`, `.test_abort_writes_to_the_ledger` | The mechanism is mechanically implemented; the demonstration before the operation is **procedural only** |

### 3.8 The ledger chain, the export, the anchor, and replay

`caos/ledger.py` implements the chain. Each record is a frozen `LedgerRecord` carrying `seq`, `prev`, `body`, and `digest`. The digest is a SHA-256 hash over the canonical UTF-8 bytes of the body, prefixed by the ASCII bytes of the preceding record's digest as 64 lower-case hexadecimal characters with no separator. The canonical body is the JSON object serialised with keys ordered by Unicode code point, no whitespace between tokens, minimal string escaping, and all other characters emitted literally as UTF-8. The first record's `prev` is the fixed genesis value of 64 zero characters.

| Requirement | What the implementation checks | Module or function | Test | Status |
| --- | --- | --- | --- | --- |
| **The chain conforms to the platform specification** | The digest, the sequence, the body fields, and the genesis value are exactly as `operational/platform-architecture-and-agent-containment.md` §11 specifies, and the specification's own worked example — two records with stated digests and a tampered record — reproduces byte for byte in the implementation | `caos/ledger.py` — `LedgerRecord.compute_digest`, `canonical_bytes`, `canonical_json`, `GENESIS_DIGEST`, `RECORD_SCHEMA` | `WorkedExampleTests.test_the_genesis_digest_reproduces`, `.test_the_second_digest_reproduces`, `.test_the_canonical_form_matches_the_specification_byte_for_byte`, `.test_the_tampered_digest_reproduces`, `.test_the_example_chain_verifies` | Mechanically enforced |
| **Canonicalisation** | Keys are ordered recursively, no whitespace is emitted, nulls are present rather than omitted, non-ASCII characters are emitted literally, and a value that cannot be serialised is rejected rather than coerced | `caos/ledger.py` — `canonical_json`, `_reject_non_serialisable` | `CanonicalisationTests.test_keys_are_ordered_recursively`, `.test_no_whitespace_is_emitted`, `.test_nulls_are_present_not_omitted`, `.test_non_ascii_is_emitted_literally`, `.test_a_non_serialisable_value_is_rejected` | Mechanically enforced |
| **Chain integrity** | `Ledger.verify()` walks the chain from the genesis value and reports three distinct classes of problem: an index discontinuity, a chain link mismatch where a record's recorded predecessor does not equal the previous record's stored digest, and a digest mismatch where the recomputed digest does not equal the stored one. The report states the number of records, the head, the problems found, and what the check does and does not establish | `caos/ledger.py` — `Ledger.verify`, `LedgerRecord.compute_digest`, `.is_intact` | `LedgerChainTests.test_chain_verifies`, `.test_tampering_with_a_payload_is_detected`, `.test_tampering_with_a_digest_is_detected`, `.test_reordering_records_is_detected`, `.test_a_truncated_chain_closes_only_against_a_different_head` | Mechanically enforced |
| **Sequence and body structure** | The sequence numbers start at 1 and are contiguous, the records are chained, and the body carries the specified fields — `schema`, `ts`, `kind`, `subject`, `actor`, `card_ref`, `integrity`, `payload`, and `seq` | `caos/ledger.py` — `Ledger.append`, `LedgerRecord`; `caos/version.py` — `PLATFORM_BUILD` | `LedgerChainTests.test_a_new_ledger_is_empty_with_a_genesis_head`, `.test_sequence_numbers_start_at_one`, `.test_records_are_chained`, `.test_the_body_carries_the_specified_fields` | Mechanically enforced |
| **Append-only** | The ledger exposes append, read, and query operations only. Records are frozen dataclasses, and the internal list is not exposed for mutation. There is no operation that rewrites a committed record | `caos/ledger.py` — `Ledger.append`, `.records`, `.for_card`, `.of_kind` | `LedgerChainTests.test_records_are_chained`; `QueryTests.test_for_card_filters_by_card`, `.test_of_kind_filters_by_kind` | Mechanically enforced |
| **Verification states its own limits** | The verification report carries an `establishes` field and a `does_not_establish` field. The `does_not_establish` text states that the chain cannot show that the recorded decisions were correct, that the authorisation was lawful, or that the chain could not have been rewritten in full by an attacker with write access to the chain and to the anchor, and names external anchoring and periodic independent export as the stated mitigation | `caos/ledger.py` — `Ledger.verify` | `LedgerChainTests.test_verification_states_what_it_does_not_establish` | Mechanically enforced |
| **External anchoring** | `Ledger.anchor()` returns an anchorable summary — the chain head, the record count, and a digest over the sequence of record digests — intended to be exported independently of the chain. The Watchfloor's audit view reports the chain, its limits, and the anchor for independent export | `caos/ledger.py` — `Ledger.anchor`; `caos/watchfloor.py` — `Watchfloor.audit` | `ExportTests.test_anchor_reports_the_chain_digest`; `ReplayAndAuditTests.test_audit_reports_the_chain_and_its_limits` | The **artefact** is mechanically implemented; the **periodic independent publication** of it is not. See §4.5 |
| **Export** | The export is a JSON document carrying a manifest and the records in sequence, and is readable by a party with no access to the platform. The manifest states the scope, the range, the genesis and head digests, the anchors consulted, the export time, the platform build, that the export is complete, and that it is **unsigned**: the `signature` field is present and `null`, with a note saying so. `Ledger.from_export` rebuilds a ledger from that export, so a party outside the operating boundary can verify the chain from the export alone | `caos/ledger.py` — `Ledger.export`, `.from_export`, `.anchor`, `.verify`, `EXPORT_FORMAT_VERSION` | `ExportTests.test_the_export_carries_a_manifest_and_the_records`, `.test_the_export_states_that_it_is_unsigned`, `.test_export_and_reimport_preserves_the_chain` | Mechanically enforced |
| **Replay at the ledger level** | `Ledger.replay(card_id)` returns the recorded sequence for a card as a timeline, and the Watchfloor's replay view renders the recorded entries and reports honestly when a card is unknown | `caos/ledger.py` — `Ledger.replay`, `.for_card`; `caos/watchfloor.py` — `Watchfloor.replay` | `QueryTests.test_replay_returns_a_timeline`; `ReplayAndAuditTests.test_replay_renders_recorded_entries`, `.test_replay_of_an_unknown_card_is_honest` | Mechanically enforced |
| **DO-12 / OP-6 — the record of reasoning** | The `DecisionRecord` carries the seven fields the model requires — what was known at the time, the options considered, the grounds for rejection, the choice, the authority relied upon, the confidence at the time, and the pre-registered contingency — together with the residual risk, the risk of inaction, the contingency's timestamp, the dissent, the outcome, and the actor. The record is constructed by `decision.select` and serialised by `as_payload` for the ledger | `caos/models.py` — `DecisionRecord`, `.as_payload`; `caos/decision.py` — `select` | `SelectionTests.test_selection_produces_a_reconstructible_record`, `.test_the_record_is_json_serialisable` | The fields are present and serialised; the **completeness of the field set is not enforced at construction**, so a record with an empty `known_at_the_time` or `pre_registered_contingency` is constructible. **Requires confirmation** that such a record should be refused |

### 3.9 The catalogue, the technique registry, the generated data modules, and the drift check

| Check | What the implementation checks | Module or function | Test | Status |
| --- | --- | --- | --- | --- |
| **The catalogue holds OCC-01 to OCC-43** | The catalogue is exactly forty-three entries, with unique contiguous identifiers, grouped contiguously by class, and every entry deliverable or expressly marked | `caos/countermeasures.py` — `CATALOGUE`, `CATALOGUE_INDEX`, `get`, `by_class`, `for_techniques`, `autonomy_units_for`; `caos/catalogue_data.py` | `CatalogueIntegrityTests.test_catalogue_holds_forty_three_entries`, `.test_identifiers_are_unique_and_contiguous`, `.test_class_grouping_is_contiguous`, `.test_every_entry_is_deliverable_or_marked`, `.test_a_withheld_entry_remains_in_the_catalogue`, `.test_get_returns_none_for_an_unknown_identifier`, `.test_for_techniques_accepts_categories_and_techniques` | Mechanically enforced |
| **No countermeasure may target a human being** | The catalogue constructor raises if `targets_humans` is set, so such an entry cannot exist | `caos/models.py` — `Countermeasure.__post_init__` | `CatalogueIntegrityTests.test_no_entry_targets_human_beings` | Mechanically enforced |
| **No countermeasure may weaponise a model** | The catalogue constructor raises if `weaponises_model` is set | `caos/models.py` — `Countermeasure.__post_init__` | `CatalogueIntegrityTests.test_no_entry_uses_a_model_as_a_weapon` | Mechanically enforced |
| **Every entry declares its metadata** | Each entry declares a minimum profile, a direction of effect, a reversibility, and an attribution dependency, and its residual reduction and effectiveness confidence are bounded | `caos/countermeasures.py`; `caos/models.py` — `Countermeasure.__post_init__` | `CatalogueIntegrityTests.test_every_entry_declares_a_minimum_profile`, `.test_every_entry_declares_its_direction`, `.test_every_entry_declares_a_reversibility`, `.test_every_entry_declares_an_attribution_dependency`, `.test_residual_reduction_is_bounded_and_carries_confidence` | Mechanically enforced |
| **The countermeasure identifier format** | A countermeasure identifier that does not begin `OCC-` is refused at construction | `caos/models.py` — `Countermeasure.__post_init__` | `CatalogueIntegrityTests.test_catalogue_holds_forty_three_entries` | Mechanically enforced |
| **The taxonomy registry is consistent** | Ten categories are defined, each technique belongs to a defined category, the identifiers are unique, the category prefix derives from the identifier, each category carries at least six techniques, the technique bindings resolve to the catalogue, each technique states its attribution note, and the technique index is consistent with the technique list | `caos/taxonomy.py` — `CATEGORIES`, `TECHNIQUES`, `TECHNIQUE_INDEX`, `category_of`, `techniques_for_category`, `technique`, `identity_dependent_techniques`, `categories_for_countermeasure_class`, `coverage_report` | `TaxonomyIntegrityTests.test_ten_categories_are_defined`, `.test_every_technique_belongs_to_a_defined_category`, `.test_technique_identifiers_are_unique`, `.test_every_category_carries_at_least_six_techniques`, `.test_technique_bindings_resolve_to_the_catalogue`, `.test_every_technique_states_its_attribution_note`, `.test_category_of_derives_the_prefix`, `.test_unknown_technique_returns_none`, `.test_coverage_report_distinguishes_covered_from_untested`, `.test_technique_index_is_consistent` | Mechanically enforced |
| **The registry is generated from the canonical document** | The executable registry is generated from `operational/adversary-ai-taxonomy-and-threat-model.md` §5 by `tools/sync_taxonomy.py` into `caos/taxonomy_data.py`, so that the written taxonomy and the executable registry cannot drift apart without the drift being visible. The registry carries seventy-seven techniques | `impl/tools/sync_taxonomy.py`; `caos/taxonomy_data.py`; `caos/taxonomy.py` — `TECHNIQUES` | The drift check is `python3 tools/sync_taxonomy.py --check`, which reports the implementation in agreement with the canonical document. The synchroniser itself is not under the unit-test suite | **Requires confirmation** for the synchroniser; the registry's own consistency is mechanically enforced by the taxonomy tests above |
| **The catalogue is generated from the canonical document** | The executable catalogue is generated from `operational/countermeasure-catalogue.md` by `tools/sync_catalogue.py` into `caos/catalogue_data.py`, on the same basis and with the same discipline | `impl/tools/sync_catalogue.py`; `caos/catalogue_data.py`; `caos/countermeasures.py` — `_build` | The drift check is `python3 tools/sync_catalogue.py --check`, which reports the implementation in agreement with the canonical document. The synchroniser itself is not under the unit-test suite | **Requires confirmation** for the synchroniser; the catalogue's own integrity is mechanically enforced by the catalogue tests above |
| **The detection objectives come from the technique library** | The synchroniser reads the per-technique detection objectives from `reference/ai-attack-technique-library.md`, which is canonical for them, and **fails** where the library carries no objective for a technique the taxonomy document defines. The library and the registry are therefore locked together: a technique cannot be added to the taxonomy without a detection objective in the library | `impl/tools/sync_taxonomy.py` — `extract_library_objectives`; `caos/taxonomy_data.py` | The drift check reports agreement. The failure path is exercised by the synchroniser's own error, not by a unit test | **Requires confirmation** for the synchroniser |
| **The controlled vocabulary is typed** | The claim labels, source tiers, verification statuses, collateral classes, autonomy classes, countermeasure classes, rules-of-engagement profiles, reversibility categories, attribution dependencies, directions of effect, countermeasure statuses, and integrity states are enumerated types, and the value tables for thresholds, approval depths, class permissions, ceilings, and exposure normalisation are fixed and tested | `caos/vocab.py` — the enums and value tables | `CollateralClassTests.test_exposure_normalisation_is_fixed`, `.test_exposure_is_monotonic`; `AttributionThresholdTests.test_thresholds_rise_with_consequence`, `.test_threshold_table_matches_documentation`; `ApprovalDepthTests.test_more_demanding_of_profile_and_collateral_prevails`, `.test_higher_profile_demands_more_than_low_collateral`, `.test_every_profile_has_a_depth`; `ProfileTests.test_collateral_ceilings_are_ordered`, `.test_disrupt_permits_the_disrupt_class`, `.test_observe_permits_detection_and_hardening_only`, `.test_deception_is_not_available_below_r3`, `.test_observation_is_available_from_r1`, `.test_read_only_autonomy_is_not_permitted_at_observe`; `ReversibilityTests.test_ordering_puts_reversible_above_none` | Mechanically enforced |
| **A claim requires a label, a tier, a confidence, and a provenance** | The `Claim` constructor refuses an empty text, a confidence outside [0.0, 1.0], and a derivation penalty outside [0.0, 1.0]. The label, tier, and verification status are typed fields | `caos/models.py` — `Claim.__post_init__`; `caos/vocab.py` — `ClaimLabel`, `SourceTier`, `VerificationStatus` | `CardViewTests.test_card_view_shows_the_evidence_with_labels` | Mechanically enforced as to the typed fields; the **tier's meaning and the confidence's calibration** are procedural |
| **The console refuses an out-of-profile countermeasure and states the margin** | The ROE gate view refuses a countermeasure outside the profile and renders the margin of exceedance and the approvals required; an unknown countermeasure is reported rather than ignored | `caos/watchfloor.py` — `Watchfloor.roe_gate` | `RoeGateTests.test_gate_refuses_an_out_of_profile_countermeasure`, `.test_gate_states_the_margin_of_exceedance`, `.test_gate_lists_the_approvals_required`, `.test_gate_reports_an_unknown_countermeasure` | Mechanically enforced |
| **The console shows the candidates and the rejections** | The countermeasure console renders the candidate set, the rejections with their reasons, the options including the do-nothing option, and the autonomy monitor | `caos/watchfloor.py` — `Watchfloor.countermeasure_console`, `.options`, `.autonomy_monitor` | `CountermeasureConsoleTests.test_console_shows_candidates_and_rejections`, `.test_options_include_doing_nothing`, `.test_autonomy_monitor_renders` | Mechanically enforced |
| **The two binding instruments agree** | The technique library records technique-level bindings — this countermeasure is a candidate response to this specific technique — and the countermeasure catalogue records category-level bindings — this countermeasure addresses this category. A test reads the library's bindings and measures their agreement with the catalogue's, and holds the recorded measurement: the divergence may fall, and it must not rise, because a rise would mean the two documents are drifting apart. The same test holds the binding count and the catalogue's pair counts, so neither can change silently | `impl/tests/test_bindings.py` — `BindingConsistencyTests`; `caos/countermeasures.py` — `CATALOGUE`; `caos/taxonomy.py` — `TECHNIQUES` | `BindingConsistencyTests.test_the_library_carries_an_entry_for_every_technique`, `.test_every_binding_resolves_to_a_catalogue_entry`, `.test_every_technique_carries_at_least_one_binding`, `.test_the_binding_count_has_not_changed_without_the_record_being_updated`, `.test_the_divergence_has_not_grown`, `.test_the_catalogue_pair_counts_have_not_changed_silently` | Mechanically enforced |
| **The proving ground is reproducible and reports misses** | Scenarios are seeded, a scenario produces a reproducible signal set, every archetype maps to known techniques, the detection evaluation distinguishes covered from untested and names personal data, and the scoring produces a breakdown that caps a dimension at its weight and states that it measures the exercise rather than the estate | `caos/proving_ground.py` — `Archetype`, `Scenario`, `SimulatedAdversary`, `run_scenario`, `ExerciseReport`, `evaluate_detection`, `score_exercise`; `caos/taxonomy.py` — `coverage_report` | `ProvingGroundTests.test_scenarios_are_reproducible`, `.test_a_scenario_produces_the_requested_number_of_signals`, `.test_every_archetype_maps_to_known_techniques`, `.test_detection_evaluation_reports_misses`, `.test_detection_evaluation_reports_full_coverage_when_covered`, `.test_the_report_names_personal_data`, `.test_scoring_produces_a_breakdown`, `.test_scoring_caps_a_dimension_at_its_weight`, `.test_scoring_states_that_it_measures_the_exercise` | Mechanically enforced |

### 3.10 The integrity states and the unusable-source rule

| Check | What the implementation checks | Module or function | Test | Status |
| --- | --- | --- | --- | --- |
| **The source-integrity vocabulary is the platform's five states** | `IntegrityState` carries trustworthy, degraded, stale, missing, and tampered-suspect, and the vocabulary is the one the platform architecture specification §6.1 fixes | `caos/vocab.py` — `IntegrityState` | `IntegrityStateTests.test_the_five_state_vocabulary_is_used` | Mechanically enforced |
| **A missing or tampered-suspect source produces no finding** | `IntegrityState.usable` is true only for trustworthy, degraded, and stale. A source in any other state is not usable, and the absence of a signal from it is never reported as a negative finding: the absence of a signal is not evidence of the absence of the thing the signal would have carried | `caos/vocab.py` — `IntegrityState.usable`; `caos/watchfloor.py` — `Watchfloor.watchboard`, `.triage`; `caos/models.py` — `Signal.usable` | `IntegrityStateTests.test_a_missing_source_is_not_usable`, `.test_a_stale_source_is_usable_but_impaired`, `.test_an_uninterpretable_state_is_treated_as_tampered`; `WatchboardTests.test_unusable_sources_are_reported_as_not_a_negative_finding`; `TriageTests.test_degraded_sources_are_marked`, `.test_unusable_sources_are_marked_distinctly` | Mechanically enforced |

### 3.11 The divergence register, D-1 to D-8

Each divergence recorded at the previous revision carries its resolution, the instrument that carried it, and the test that demonstrates it. A divergence that is closed stays in the table: a reader arriving later must be able to see that a disagreement existed, what it was, and how it was settled.

| # | What was divergent | Resolution | How it was carried | Test |
| --- | --- | --- | --- | --- |
| **D-1** | AD-4 was a scope-prefix coverage test, where the master design's AD-4 row states set containment | **Closed by a change to the implementation.** The implementation now performs both: set containment where the catalogue entry names specific targets, and the scope-prefix coverage test where it does not | `caos/countermeasures.py` — `Countermeasure.targets`; `caos/roe.py` — `_check_ad4`. The master design's AD-4 row has been amended to state both limbs | `AD4SetContainmentTests.test_a_named_target_outside_the_card_is_refused`, `.test_a_named_target_on_the_card_passes`, `.test_an_entry_without_named_targets_falls_back_to_the_scope_test`; `AD4TargetContainmentTests.test_missing_scope_is_refused`, `.test_adversary_direction_needs_an_adversary_target` |
| **D-2** | AD-12 was a declaration-or-attestation split, where the master design's AD-12 row stated only the prohibition | **Closed by reconciling the requirement text with the implementation.** The master design's AD-12 row now states that the countermeasure must not violate the non-weaponisation constraint *and* that either the catalogue declares conformity or the operator has attested the boundary analysis. The implementation already behaved this way and was not changed | `caos/roe.py` — `_check_ad12`; `caos/models.py` — `Countermeasure.non_weaponisation_declared`, `OperationCard.non_weaponisation_attestation` | `AD12NonWeaponisationTests.test_a_weaponising_countermeasure_cannot_be_constructed`, `.test_condition_passes_for_a_catalogued_countermeasure` |
| **D-3** | AD-10 recorded the deconfliction result rather than computing the conflict against the live operation set | **Closed by reconciling the requirement text with the implementation.** The master design's AD-10 row now states that the check must be recorded as passed and current, or attested, and records explicitly that the conflict computation belongs to the platform, which holds the live operation set. The implementation already behaved this way and was not changed | `caos/roe.py` — `_check_ad10`; card fields `OperationCard.deconfliction_passed`, `.deconfliction_map_current`, `.deconfliction_attestation` | `AD10DeconflictionTests.test_failed_deconfliction_is_refused`, `.test_passed_deconfliction_passes` |
| **D-4** | The derivation penalty was applied multiplicatively, where the decision-support model and INT-9 state a subtractive form | **Closed by a change to the implementation, in favour of the requirement text.** `propagate_confidence` now computes `c_derived = c_weakest − p`, floored at zero. The decision-support model's §6 and INT-9 agree with it | `caos/scoring.py` — `propagate_confidence`; `caos/models.py` — `Claim.propagated_confidence` | `ConfidencePropagationTests.test_derived_confidence_is_the_weakest_input`, `.test_penalty_reduces_the_propagated_value`, `.test_propagation_never_returns_a_negative_confidence`, `.test_propagation_is_the_most_conservative_of_the_two_forms` |
| **D-5** | The autonomy budget was consulted at admissibility and consumed on abort, but was not debited on dispatch, so the budget did not bound the act it was intended to bound | **Closed by a change to the implementation.** `dispatch` re-evaluates admissibility at dispatch time, debits the budget on a successful dispatch, spends nothing on a refusal, and writes a `dispatch.issued` or `dispatch.refused` record to the ledger | `caos/decision.py` — `dispatch`; `caos/watchfloor.py` — `Watchfloor.dispatch`; `caos/cli.py` — the `dispatch` subcommand | `DispatchTests.test_a_dispatch_debits_the_autonomy_budget`, `.test_a_refused_dispatch_spends_nothing`, `.test_a_refusal_is_recorded_in_the_ledger`, `.test_a_dispatch_is_recorded_in_the_ledger` |
| **D-6** | A card's technique references were an untyped tuple of strings, so a card could name a technique the registry did not hold, and the candidate generator would then return an empty set for it | **Closed by a change to the implementation.** `OperationCard.unknown_techniques` resolves the references against the registry, and `completion_defects` treats any unresolved reference as a blocking defect, so such a card cannot be armed | `caos/models.py` — `OperationCard.unknown_techniques`, `.completion_defects`; `caos/taxonomy.py` — `TECHNIQUE_INDEX` | `CardArmabilityTests.test_an_unregistered_technique_reference_is_a_defect`, `.test_a_registered_technique_reference_is_not_a_defect` |
| **D-7** | The pre-registered contingency was not timestamped, so the record asserted rather than established that the contingency preceded the action | **Closed by a change to the implementation.** The card carries `contingency_recorded_at`; contingency text with no timestamp is a blocking completion defect; and the decision record carries the timestamp, so the record shows when the contingency was written relative to the action | `caos/models.py` — `OperationCard.contingency_recorded_at`, `.completion_defects`, `DecisionRecord.contingency_recorded_at`; `caos/decision.py` — `select` | `CardArmabilityTests.test_a_contingency_without_a_timestamp_is_a_defect`, `.test_a_timestamped_contingency_is_not_a_defect` |
| **D-8** | The emergency protocol's enforcement surface sat outside this register, so the register understated the implementation's controls | **Closed by scoping, not by removal.** This register is a register for the operational core. The emergency shutdown and containment protocol's requirements — `ESC-`, `ZC-`, `PACE-` — are owned by `operational/emergency-shutdown-and-containment-protocol.md`, whose §22.1 registers that protocol's own mechanically-enforced surface with the module, function, and test for each requirement it evaluates. An auditor assessing the emergency path assesses it against that document and against `tests/test_emergency.py`, and the two registers together are the implementation's whole enforcement surface | `caos/emergency.py`; `caos/emergency_console.py` — `Drill`, `build_drill`, `show_catalogue`, `run_drill`; `operational/emergency-shutdown-and-containment-protocol.md` §22.1 | `tests/test_emergency.py` — the severity ladder, state machine, pre-flight gate, protected control set, no-AI-obtains-control, zero-collateral, containment envelope, staged rotation, posture ceiling, kill action, and prohibition test classes; the synthetic containment drill is exposed as `caos emergency drill` and the emergency catalogue as `caos emergency catalogue`, and neither console surface is separately under test |

**A note on what closing D-8 by scoping means.** The register in §3.1 to §3.10 covers the operational core and is now larger than it was. It is still not the whole of the implementation. The emergency path has its own register, in its own document, with its own snapshot, and a reader assessing the whole platform should read both.

### 3.12 The state of the test suite, and what a conformance finding now means

| Attribute | Position at the 2026-10-20, 09:15 snapshot |
| --- | --- |
| Tests collected | 364 |
| Result | No failures |
| Drift against the canonical documents | `tools/sync_taxonomy.py --check` and `tools/sync_catalogue.py --check` both report the implementation in agreement with `operational/adversary-ai-taxonomy-and-threat-model.md` and `operational/countermeasure-catalogue.md` |
| Movement | The implementation is settled for this revision. The previous revision of this document was written against a codebase that was moving, and the register had to be re-derived; that is no longer the case |

**What a conformance finding means now.** A finding that a requirement is mechanically enforced means that the code evaluates it, that a counterexample would contradict the determination, and that a named test demonstrates the behaviour. It does **not** mean that the code has been found conformant with the framework; that judgement is a human one, and it is not made in this document. It does not mean that the requirement's substance is satisfied in any deployment, which is a question about the deployment and the operator, not about the reference implementation. And it does not mean that the requirement is enforced anywhere else: the reference implementation is a reference, and master design LIM-14 holds.

**What would still be needed for a finding to rest on a recorded test result against a fixed snapshot.** Three things, none of which the reference implementation can supply for itself:

| # | Requirement | Why it is still needed |
| --- | --- | --- |
| 1 | A fixed, identified snapshot of the implementation, recorded with the finding | The synchronisers' `--check` mode gives a reproducible statement that the implementation agrees with the canonical *documents*. It does not identify the code, and a finding that cites a test result without identifying what was tested is not reproducible |
| 2 | A recorded run of the suite against that snapshot, with its result attached to the finding | The suite is the evidence. A finding that says the code does X, and that a test demonstrates it, is complete for the reader who can run the test; it is not complete for the reader who cannot, and an audit report is read by people who cannot |
| 3 | An independent re-run by a party other than the author of the code | A test that passes is evidence that the code behaves as the test says. It is not evidence that the test says what the requirement means, and only a reader who re-derives the correspondence can establish that |

**The attestation-field gap — closed at version 1.1.** Six card fields are consulted by the engine: `irreversibility_argument`, `indirect_effect_attestation`, `non_weaponisation_attestation`, `deconfliction_attestation`, `deconfliction_map_current`, and `per_target_authorisations`. The first four are the attestation limbs of the hybrid and human conditions, and the last two are the limbs of AD-5 and AD-10. At version 1.0 of this document those limbs were enforced in code and exercised by the engine but were not demonstrated by a dedicated test, and a finding resting on them was marked **Requires confirmation**. `tests/test_attestations.py` now demonstrates each of the six in both its failing and its passing state, and the corresponding register rows in §3.1 have been moved from **Requires confirmation** to mechanically enforced. The remaining **Requires confirmation** elements in the register are the two synchronisers, which are executable and are demonstrated by their own strictness rather than by the unit-test suite, and the console and command-line surfaces, which are not separately under test beneath the functions they call.

**The synchronisers.** The two drift checks are executable and are recorded as requiring confirmation for one reason: neither synchroniser is itself under the unit-test suite, so the failure path — what happens when the canonical document and the generated module disagree — is not demonstrated by a test. It is demonstrated by the strictness of the parser, which treats an unrecognised value as an error rather than a default, and by the fact that the synchroniser refuses to generate a registry for a technique the technique library carries no detection objective for. That is a reasonable basis for a **Requires confirmation** status and not a sufficient one for an unqualified one.

### 3.13 Procedural-only requirements

Everything in this section is satisfied by the operator's record and by human review, and is not evaluated by the implementation. An assessment against these requirements is an assessment of documents and of people, and the audit trail for it is the decision record and the after-action report.

| Requirement family | Count | Why it is procedural | Where the assurance sits |
| --- | --- | --- | --- |
| `AUTH-` (remainder) | 8 | AUTH-3, AUTH-6, AUTH-7, and AUTH-8 have enforced elements, recorded above. AUTH-1, AUTH-2, AUTH-4, AUTH-5, and AUTH-8's substantive answers are not evaluated | The authorisation document; the card's authority fields; the approver's record |
| `ROE-` (remainder) | 8 | ROE-1, ROE-2, ROE-3, ROE-6, and ROE-8 have enforced elements. ROE-4, ROE-5, and ROE-7 are workflow properties | The escalation instrument; the downgrade notice; the reversibility argument on the card |
| `CON-` | 14 | Constitutional conduct constraints bind conduct, not code. CON-4 and CON-6 have enforced counterparts in AD-6 and AD-12; the remainder are not evaluated | The operator's conduct standard; the approver's judgement; the after-action report |
| `HITL-` (remainder) | 8 | HITL-1 and HITL-3 have enforced or partly enforced elements. HITL-2, HITL-4, HITL-5's automatic case, HITL-6, HITL-7, and HITL-8 are about the quality and substance of a human's decision, which no engine can evaluate | The approval surface; the abort demonstration; the record of the approver's reading |
| `OP-` (remainder) | 10 | OP-1, OP-4, and OP-6 have enforced elements in the card's completion rules and the decision record. The remainder are process properties | The card; the mission record; the error handler's log |
| `GATE-` | 8 | The gates are points in a process at which a human or a workflow step confirms the state. Only G-3 is represented in the engine, as the card-armability check | The gate record in the ledger |
| `ERR-` | 5 | The error handler is a workflow, and its independence from the model is a governance property | The handler's log; the named resumption decision |
| `INT-` (remainder) | 11 | INT-3, INT-4, INT-6, and INT-9 have enforced elements. INT-1, INT-2, INT-5, INT-7, INT-8, INT-10, and INT-11 are evidence-handling disciplines | The claim with its label, tier, confidence, and provenance; the attribution assessment |
| `TAX-` | 5 | TAX-1 to TAX-5 are evidence-handling disciplines. The registry's internal consistency is tested, the registry is generated from the canonical document under a drift check, and a card's references to it are validated; the rationale requirement itself is not enforced | The classification with its rationale; the mapping register's status |
| `SCORE-` (remainder) | 5 | SCORE-1, SCORE-2, SCORE-3, SCORE-4, and SCORE-5 are recording and reasoning properties. The arithmetic, the exposure of the components, and the presence of the do-nothing option are enforced | The decision record; the card's risk assessment |
| `AD-` (remainder) | 13 | AD-1 to AD-13 are all implemented. The remainder of the requirement set is not | — |
| `CM-` | 3 + catalogue | The countermeasure class rules are the frame of the catalogue; each countermeasure's properties are catalogue data, and the catalogue's integrity is tested and its agreement with the canonical document is drift-checked | The catalogue; the binding on the card |
| `DET-` | 9 | Detection engineering is a programme of work, and a detector's coverage is a measured property. The proving ground reports coverage against a simulated estate and states that it measures the exercise | The coverage assessment; the exercise results |
| `CTG-` | 7 | Containment is a platform capability. The countermeasure bindings in the catalogue are the design | The platform configuration; the containment record |
| `INFRA-` | 8 | Platform architecture is an implementation concern of the deploying organisation | The platform's own configuration and evidence |
| `WF-` | 21 | Interface capabilities are properties of a deployment. The Watchfloor module in the reference implementation is a console view, not the specified console | The deployed interface; the audit export |
| `MET-` | 14 | Measurement is a reporting discipline | The after-action report; the exercise pack |
| `EX-` | 6 | Exercises are a programme | The exercise record |
| `LIM-` | 14 | Limitations are statements, and are not enforceable | This document §9; the master design §11 |

### 3.14 Summary of the register

| Measure | Value |
| --- | --- |
| Rows recorded as mechanically enforced | **76**, distributed as: the admissibility algebra AD-1 to AD-13 (13); the card-armability preconditions (3); the scoring model and the confidence propagation (8); the ceilings, expiry, approval depth, and card completeness (10); the third-party exclusion (5); the attribution thresholds (5); the autonomy budget, the grant, and the dispatch path (5); the ledger chain, canonicalisation, export, anchor, and replay (10); the catalogue, registry, generated modules, vocabulary, console, binding consistency, and proving ground (15); and the integrity states (2). Every row names the function that implements it and the test that demonstrates it, except where the test column says that no test exists |
| Rows carrying a *Requires confirmation* element | **9**: the attestation limb of AD-3; the attestation limb of AD-6; the attestation limb of AD-10; the attestation limb of AD-12; the dispatch console and command-line surfaces; the decision record's field completeness; the two synchronisers; and the library-supplied detection objectives |
| Rows recorded as procedural only | 19 requirement families, listed in §3.13 |
| Divergences recorded | 8, listed in §3.11. **All eight are closed** — five by a change to the implementation (D-1, D-4, D-5, D-6, and D-7), two by reconciling the requirement text with the implementation (D-2, D-3), and one by scoping (D-8) |
| Requirement families recorded as procedural only | 19, listed in §3.13 |
| Test-suite result at the snapshot | 364 tests collected, no failures, and both drift checks report agreement with the canonical documents |
| Principal negative finding | The mechanically-enforced surface covers the operational core — the admissibility algebra, the card's armability, the scoring arithmetic, the ceilings, the exclusion, the thresholds, the budget and the dispatch path, the ledger, the catalogue and registry's integrity, and the integrity states — and does not cover the framework's conduct, workflow, measurement, and deployment requirements. A report that presented only the enforced rows would overstate the framework's assurance by a wide margin |
| Principal caveat | This register is a statement about what the code does and where the evidence is. **The judgement that the implementation is conformant remains a human one, and is not made here** |

---

### 3.15 Version 1.2 — the register against a reworked implementation

The implementation was reworked after a code review, and the register is
re-derived here against the reworked source. The changes that bear on the
register are these.

| Change | Effect on the register |
| --- | --- |
| The countermeasure's `status` became an availability precondition of its own, checked as `PRE` rather than inside AD-5's third-party branch | A `Withheld` or `Retired` countermeasure is now inadmissible on every path, not only on the outward one. The AD-5 row and the new `PRE` row record it |
| `Countermeasure.touches_third_party` is now tied to the direction of effect, and the model refuses a countermeasure whose flag and direction disagree | The denormalised flag was a bypass: an outward action with the flag cleared escaped the third-party exclusion. The flag is no longer free |
| The emergency prohibitions are now read from one mapping, `PROHIBITION_FLAGS` and `prohibition_for`, and the dispatch consults that mapping | The prohibition list was documentation with no live mechanism, and the mapping contradicted the dispatch on four dispatchable actions. The mapping now names only the absolute prohibitions, and the conditional ones remain governed by `K-3`, `K-6` and `K-9` |
| The protected control set is matched by scope, not by exact string | A target that reached inside a protected session passed the gate. The protocol's own wording required the scope test |
| The authority check covers the verification, transition, and level paths, not only the dispatch and rotation paths | An actor holding no authority could fabricate the verification passes that unlock the irreversible recovery actions |
| `OperationCard.autonomy_grant()` validates the declared envelope, expiry, on-call operator, and reversion trigger | AUT-4's row previously named a validation that nothing on the dispatch path consulted. It is now consulted |
| `Ledger.from_export` refuses a document that is not an export, and the anchor's head is stored and compared | A foreign or tampered export raised a raw exception, and the anchor could not detect a rewritten chain because its value was never stored |
| Both synchronisers now refuse a duplicate identifier, an unreadable technique row, a missing technique library, and a technique in an undefined category | Each of those previously produced a silently degraded generated module |
| The two canonical JSON implementations were unified into `caos/canonical.py`, and `Claim.propagated_confidence` now performs the subtractive operation the model states | Two canonical forms made a digest computed in one place incomparable with one computed in another |
| `required_approvals` returns the union of the profile's and the collateral class's role sets | The more demanding set alone dropped a requirement, and an R0 card could arm with no operator's approval |
| The implementation's permitted action classes now match the constitutional instrument's column exactly, and CM-F is available at R1 only | The implementation had been wider than the constitutional instrument at R2 and R3, where CM-F Disrupt was admitted. The constitutional column governs |
| A countermeasure evaluated on class confidence is held to `CLASS_CONFIDENCE_FLOOR` rather than to the `INT-3` table | `INT-4` states that the `INT-3` table does not apply to a class-confidence countermeasure, and a floor that does not scale is what it needs instead |
| The residual risk is reported as a band where the confidence in the effectiveness is below 0.60, and a countermeasure with `e ≥ 0.70` and `q < 0.50` carries an unconfirmed-effectiveness marker | `DS-6` required both, and neither existed. They are now in `caos/scoring.py` as `residual_band` and `is_effectiveness_unconfirmed`, and are rendered by the Watchfloor |

The suite stands at 364 tests. The register's **Requires confirmation** rows
are unchanged in number: the two synchronisers remain marked as such, because
they are demonstrated by their own strictness rather than by the unit-test
suite, and the console and command-line surfaces remain marked as such,
because they are not separately under test beneath the functions they call.

---


## 4. The Verification Procedure for the Ledger

### 4.1 Purpose

The ledger is the set's memory. Verification establishes whether the ledger as presented is internally consistent with the append procedure that produced it. It is the one procedure in this document that can be performed by a party with no knowledge of the operation, against a material alone, without access to the operating systems.

### 4.2 What an auditor recomputes

The export format is fixed by `operational/platform-architecture-and-agent-containment.md` §11, and the reference implementation follows it exactly. The auditor recomputes, from the export alone:

| # | Step | What is checked | What a failure means |
| --- | --- | --- | --- |
| V-1 | Sequence | The records' `seq` values run consecutively from 1 and are unbroken across the exported range | Records are missing, or the export is incomplete |
| V-2 | Predecessor reference | Each record's recorded `prev` equals the stored digest of the record immediately before it | The chain has been broken, reordered, or a record replaced |
| V-3 | Digest | Each record's stored digest equals `SHA-256(ASCII(prev) ‖ canonical_bytes(body))`, recomputed from that record's own body and its recorded predecessor | The record's content has been altered since it was committed, or the record was forged |
| V-4 | Genesis value | The first record's `prev` is the fixed genesis value of sixty-four zero characters | The export does not begin at the beginning of this ledger |
| V-5 | Body structure and canonical form | Each body carries the specified fields — `schema`, `ts`, `kind`, `subject`, `actor`, `card_ref`, `integrity`, `payload`, `seq` — and the canonical serialisation is byte for byte as the specification fixes it: keys ordered by code point, no whitespace, minimal escaping, non-ASCII emitted literally as UTF-8 | The export was not produced by the specified procedure, or a record is malformed |
| V-6 | Manifest | The manifest states the scope, the range, the genesis and head digests, the anchors consulted, the export time, the platform build, that the export is complete, and that it is **unsigned** | The export cannot be read as a complete statement of the chain, or it has been presented as something it is not |
| V-7 | Head and anchor | The head digest in the manifest equals the digest recomputed from the exported records, and equals the head in the last exported record | The manifest and the records disagree, and the export is not the export it says it is |
| V-8 | Completeness against the record | The number of records is consistent with the number of material events the operation card records as having occurred | Records are missing, or the card does not reflect what was recorded |

V-1 through V-7 are properties of the export itself and require only the export. V-8 requires the card and is therefore a cross-check between two artefacts rather than a property of the export.

**On the signature field.** The export carries a `signature` field, and it is `null`. The manifest says so in terms, in a `signature_note`. This is deliberate: an unsigned export that is labelled as unsigned is more useful to a verifier than one that appears signed and is not, and the standard library offers no signing primitive that would be appropriate here without a cryptographic dependency. An auditor must record the export as unsigned, and must not treat the manifest as an attestation of anything.

**The auditor does not recompute** the hashes of the countermeasure catalogue, the model artefacts, the model weights, or the source telemetry. Those are attested elsewhere, and an audit of the ledger is not an audit of the estate.

### 4.3 The chain algorithm in plain terms

The algorithm is a chain of fingerprints over a fixed record envelope. In plain terms:

1. **Every record has a body and a fingerprint.** The body is a JSON object carrying exactly nine fields — the schema identifier, the timestamp, the kind, the subject, the actor, the card reference, the integrity state, the payload, and the sequence number. The fingerprint is a SHA-256 digest over that body.
2. **The fingerprint also covers the fingerprint of the record before it.** The digest is computed as `SHA-256(ASCII(prev) ‖ canonical_bytes(body))`, where `prev` is the preceding record's digest as sixty-four lower-case hexadecimal characters, encoded as ASCII with no separator, and `canonical_bytes` is the body's canonical UTF-8 serialisation.
3. **The canonical form is exact, not approximate.** Keys are ordered by Unicode code point and applied recursively; there is no whitespace between tokens; string escaping is minimal; every other character is emitted literally as UTF-8; nulls are present rather than omitted; and a value that cannot be serialised is refused rather than coerced. Two parties that both follow the rule produce the same bytes, which is the whole point of fixing it.
4. **So each fingerprint depends on everything before it.** To alter record 4, an editor would have to recompute record 4's digest and then the digests of records 5, 6, 7, and every record after — because each of them carries the one before it.
5. **The sequence starts at 1 and is contiguous.** The first record's predecessor is the genesis value, sixty-four zero characters. There is no record zero, and no gap in the sequence is permitted.
6. **Verification walks the chain forward.** The auditor recomputes record 1's digest and checks it against the value stored in record 1; then checks that record 2 carries record 1's stored digest and that record 2's own digest recomputes correctly; and so on to the end. The manifest's head digest is checked against the last record's, and against a digest recomputed over the whole sequence.
7. **The first divergence is where the chain was broken.** The first record where a recomputed digest disagrees with a stored one, where a predecessor reference does not match the preceding record's digest, or where the sequence number is out of place, is the point at which the exported ledger stopped being the ledger that was written.
8. **Records after the divergence are not continuations.** They are still individually well-formed, and they may well be genuine, but they cannot be shown to be a continuation of what came before, because the chain that bound them is broken.

### 4.4 What tamper evidence does and does not establish

| Tamper evidence establishes | Tamper evidence does not establish |
| --- | --- |
| That the exported ledger is not the product of the documented append procedure | Who altered it, or whether an alteration occurred at all as opposed to a defect in export or in storage |
| The location of the first divergence, which bounds the scope of the discrepancy | That the entries before the divergence are correct in their content |
| That the entries after the divergence cannot be relied upon as a continuation | That the entries after the divergence are false; they may be genuine records whose binding was severed |
| That a discrepancy exists which requires an explanation before the operation may be closed | That the discrepancy is material to any conclusion the operation rested on |
| — | That an entry's content was true when it was written |
| — | That no entry was omitted before the divergence point |
| — | That the first exported entry is the true beginning of the ledger |

**The specific case an auditor must understand.** A hash chain without an external anchor detects *naive* alteration and detects *accidental* corruption. It does not, by itself, detect a complete rebuild: an editor with write access to the whole ledger can alter an early entry and recompute every subsequent fingerprint, producing a chain that verifies cleanly and that is internally consistent from its new beginning. The verification procedure therefore establishes internal consistency, not authenticity of origin.

**This is why the chain cannot support a conclusion about intent.** The conclusion available is "the ledger is internally consistent with the append procedure as at the point of audit" — a statement about structure. Whether the structure was produced by the operator's control plane, by a reconstruction after a failure, or by a party with write access is not established by the chain. Establishing that requires the external anchoring discussed in §4.5.

### 4.5 The external-anchoring caveat

| Aspect | Position |
| --- | --- |
| The problem | The chain's first entry is trusted by fiat. Every later entry's trust derives from it. Nothing inside the ledger anchors it to anything outside itself |
| Consequence | Internal consistency is achievable by a party with write access to the whole ledger. The chain cannot distinguish an unaltered ledger from a wholly rebuilt one |
| The consequence for an audit | An audit that verifies the chain and stops there has verified structure, not authenticity. The audit report must say so in those terms |
| What external anchoring would mean | A digest or checkpoint of the ledger's head, published or countersigned outside the boundary of the system's write access, at intervals |
| Status in this set | The **artefact** exists in the reference implementation: `caos/ledger.py` provides `Ledger.anchor()`, which returns the chain head, the record count, and a digest over the sequence of record digests, for export independently of the chain, and `Watchfloor.audit` renders it for independent export. The **periodic independent publication** of that artefact is not implemented, and it is the publication that makes the anchor useful. Recorded as limitation LIM-AU3 and as outstanding action 8 |
| Consequence for the confidence an auditor may express | Where no external anchor exists, the auditor's finding on ledger integrity is expressed as a statement about internal consistency, and no stronger |

### 4.6 Verification outcomes and their disposition

| Outcome | What the auditor reports | Disposition |
| --- | --- | --- |
| **Chain intact** | Every entry's recomputed fingerprint matched, every predecessor reference matched, and the sequence was unbroken | The ledger's internal consistency is established. The finding is stated with the limits of §4.4 and §4.5 |
| **Chain broken** | The first divergent entry, with its sequence number and the nature of the disagreement | The operation may not be closed on the strength of its ledger. The discrepancy requires an explanation, and where none is available the audit records the scope of the uncertainty |
| **Chain incomplete** | The sequence numbers present and the gaps between them | The export or the storage is incomplete. The audit is conducted on the material available, and the absence is recorded against the replay in §5 |
| **Chain unverifiable** | The reason: no verifier available, malformed export, or a digest algorithm the auditor does not implement | The ledger's integrity is **not assessable**. The audit proceeds on the other artefacts, and the ledger's contribution to the audit is reduced accordingly |
| **Card and ledger disagree** | The material events the card records against the entries the ledger holds | Both artefacts are retained. The disagreement is itself a finding, and it is assessed under the evidence-conformance dimension in §7 |
| **Export does not match its manifest** | The head digest, the range, and the records as exported, and where they disagree | The export is not the export it says it is. The ledger's integrity is not assessable from this material, and the discrepancy is itself a finding |
| **Export presented as signed** | That the manifest carries a `signature` field and it is not `null` | The export has been represented as something it is not. The finding is recorded, and the export is not relied upon |
| **No ledger produced** | That the operation produced no exportable ledger | The operation is not auditable under this procedure. This is the most serious outcome available, and it is reported as such |

**AUD-1 — A broken chain is a finding, not a conclusion.** The auditor reports the divergence and its location. The auditor does not characterise the cause, and does not treat the divergence as evidence of misconduct unless an independent artefact establishes it.

**AUD-2 — A refusal to act on a broken chain is the correct behaviour.** Where the chain is broken, the auditor does not silently proceed on the entries that remain. The reduction in evidential weight is recorded, and the conclusions that would have relied on the broken section are qualified accordingly.

**AUD-3 — The verification is repeatable.** An auditor's verification must be reproducible by a second party from the same export. Where a verification cannot be reproduced, the finding is recorded as a disagreement between auditors rather than as a result.

---

## 5. The Replay Procedure

### 5.1 Purpose and limits of replay

Replay reconstructs an operation from the record. Its purpose is to allow a reviewer who was not present to answer the four questions in §5.4 from the artefacts rather than from memory.

**What replay establishes.** What the record says was known, what was considered, what was chosen, what was authorised, and what would have caused the operation to be withdrawn.

**What replay does not establish.** That the record is accurate, that the reasoning was sound, or that the decision was correct. Master design ERR-5 records the relevant discipline: the log records the decision as taken, not the decision as it would appear in retrospect, and a divergence between the two is recorded as a known limitation of the assessment rather than smoothed over.

### 5.2 Required fields

Replay cannot be performed without these fields. Where a field is absent, the replay for the operation is **not assessable** in that respect, and the absence is itself recorded.

| # | Field | Source artefact | Requirement | Consequence of absence |
| --- | --- | --- | --- | --- |
| 1 | Card identifier and revision | Operation Card | Must be present on every entry that concerns a card | Entries cannot be attributed to a card, and the operation cannot be bounded |
| 2 | Engagement authorisation reference | Card authority fields | Must be present | The authority for the action cannot be identified |
| 3 | Rules-of-engagement profile in force | Card authority fields | Must be present and must match the profile recorded on the authorisation | The ceiling cannot be established |
| 4 | Collateral ceiling and autonomy class | Card authority fields | Must be present | AD-2, AD-7, and AD-11 cannot be evaluated |
| 5 | Approver identity, recorded time, and approval depth | Decision record | Must be present | The question "who authorised it" cannot be answered |
| 6 | Classification: AAT category and technique, with rationale and confidence | Signal and classification records | Must be present | The basis for candidate generation is not reconstructible |
| 7 | Attribution assessment: candidate distribution, basis, confidence | Attribution assessment | Must be present | The INT-3 threshold check cannot be reconstructed |
| 8 | Evidence: every claim with label, source tier, confidence, and provenance | Evidence ledger | Must be present for every claim relied upon | "What was known at the time" cannot be answered |
| 9 | Threat score with its components and the reasoning for each | Threat assessment | Must be present | The priority ordering cannot be reconstructed |
| 10 | Candidate set, admissibility results, and the rejected set with reasons | Countermeasure console record | Must be present, including the rejections | "What was chosen instead of what" cannot be answered |
| 11 | Residual risk before and after, and the risk of inaction | Card risk assessment | Both must be present | The proportionality argument cannot be reconstructed |
| 12 | Abort conditions, abort mechanism, and abort owner | Card abort fields | Must be present and must not be empty | "What would have caused withdrawal" cannot be answered |
| 13 | Pre-registered contingency, and the time it was written | Decision record and card | Must be present, and the recorded time must precede the action | A post-hoc rationale is not a decision record (OP-6). The implementation refuses to arm a card whose contingency text carries no timestamp, so the absence is a defect rather than a gap to be reconstructed around |
| 14 | Autonomy envelope, budget, expiry, and reversion trigger | Card autonomy fields | Required at AC-2 and above | The bound on machine-directed action cannot be reconstructed |
| 15 | Deconfliction result, and whether the deconfliction map was current at the time or attested | Card and deconfliction map | Must be present | The possibility of interference with a legitimate operation is not excluded |
| 16 | Dispatch records: the `dispatch.issued` and `dispatch.refused` entries for the operation | Ledger export | Must be present for every action attempted, including the refused ones | Whether each action was executed, what it cost in autonomy budget, and what was refused cannot be reconstructed |
| 17 | Source integrity states for every signal relied upon | Signal records | Must be present, and the state must be one of the platform's five | A finding drawn on a source that was missing or tampered-suspect is not a finding. The implementation treats such a source as producing no finding rather than a negative one, and a replay must do the same |
| 18 | Ledger records for the operation, in order, with the chain intact and the export's manifest | Ledger export | Must be present | The sequence of events and the timing of each are not reconstructible |

### 5.3 The replay steps

| # | Step | Action | Output |
| --- | --- | --- | --- |
| R-1 | Establish the material | Obtain the card, its revisions, the engagement authorisation, the ledger export for the operation, the decision records, and the evidence set. Record the version of each artefact | An audit file listing the material and its versions |
| R-2 | Verify the chain | Perform §4.2 on the ledger export. The reference implementation provides the verifier: `Ledger.from_export` rebuilds a chain from a portable export, and `Ledger.verify` reports the sequence, link, and digest problems found, together with what the check does and does not establish | The chain verification outcome, per §4.6 |
| R-3 | Reconstruct the world state | For each material decision, assemble the evidence set, the classification, the attribution assessment, and the threat score **as they were recorded at that time**, not as they stand now | A per-decision world-state record |
| R-4 | Re-run the admissibility | Evaluate the selected countermeasure, and every rejected candidate, against the card and profile **in force at the time of the decision**, using the register in §3.1 | An admissibility reconstruction per candidate |
| R-5 | Compare | Compare the reconstruction with what was recorded: the selected set, the rejected set and reasons, the residual risk, the approval, and the dispatch records | A list of divergences, each with its cause |
| R-6 | Answer the four questions | Answer the questions in §5.4 from the reconstruction | The replay answer set |
| R-7 | Record the divergence | For each case in which a reviewer with the same information would reach a different decision, record it as a known limitation of the assessment, per ERR-5 | A divergence record, not a criticism |
| R-8 | State the limits | Record which of the required fields were unavailable, and what could consequently not be answered | The limits statement for the replay |

### 5.3.1 What the reference implementation supports

Replay is partly implemented, and the parts it covers are the parts that can be mechanised. An auditor should use the implementation where it exists and conduct the rest by hand.

| Part of replay | Support in the reference implementation | What remains the auditor's work |
| --- | --- | --- |
| Rebuilding the chain from a portable export | `caos/ledger.py` — `Ledger.from_export` | Confirming that the export is complete and is the export of the operation in question |
| Verifying the chain | `caos/ledger.py` — `Ledger.verify` | Interpreting the report under the limits in §4.4 and §4.5 |
| Extracting an operation's timeline | `caos/ledger.py` — `Ledger.replay(card_id)`, `.for_card` | Confirming that the records returned are the complete record for the card |
| Filtering the chain by kind | `caos/ledger.py` — `Ledger.of_kind` | Separating the operation's own records from the ledger's other traffic |
| Rendering the timeline for review | `caos/watchfloor.py` — `Watchfloor.replay` | Deciding what the timeline shows about the operation |
| Re-running the admissibility against the card and profile in force | `caos/roe.py` — `evaluate`, `evaluate_all` | Supplying the card as it stood at the time, including the authority, the ceiling, and the recorded state; and comparing the result with what was recorded |
| Reconstructing the decision record's fields | `caos/decision.py` — `select` produces the record from the card | Establishing that the card held the same values at the time, and that the record was made then |
| Establishing what was dispatched and what it cost | `caos/decision.py` — `dispatch` and the `dispatch.issued` and `dispatch.refused` records it writes | Confirming that the dispatch record matches the action actually taken in the estate, which the ledger alone does not establish |
| Checking that the card could carry the action at all | `caos/roe.py` — `card_is_armable`; `caos/models.py` — `OperationCard.completion_defects` | Judging whether a card that was armable was one that should have been |
| The audit export and the anchor | `caos/watchfloor.py` — `Watchfloor.audit`; `caos/ledger.py` — `Ledger.anchor` | The findings that follow from them, and the independent publication of the anchor, which the implementation does not perform |

### 5.4 The questions replay must be able to answer

These four questions are the specification of a successful replay. A replay that answers three of them is not a replay of the operation; it is a reading of it.

#### Q1 — What was known at the time?

| Aspect | Requirement |
| --- | --- |
| The question | What evidence did the decision-maker hold, and what did that evidence say? |
| Supporting artefacts | The evidence set as recorded at the time; each claim with its label, source tier, confidence, and provenance; the classification with its rationale; the attribution assessment with its candidate distribution and stated basis; and the integrity state of every source relied upon |
| The test | A reviewer must be able to state the decision-maker's position **in the terms they held it**, without reference to anything learned later |
| The common failure | Reconstructing the position from today's evidence. The record must be read as it stood, and a claim that was later superseded is read in its superseded form |
| The integrity-state rule | A signal drawn from a source whose integrity state is missing or tampered-suspect is **no finding at all**, and never a negative one. The absence of a signal is not evidence of the absence of the thing the signal would have carried, and a replay that reads a missing source as a negative finding has inverted the rule the framework sets |
| What a failure to answer indicates | That the evidence set was not recorded, or was recorded without labels, tiers, or provenance. Either way, the decision cannot be reconstructed as taken |

#### Q2 — What was chosen instead of what?

| Aspect | Requirement |
| --- | --- |
| The question | Which alternatives were available and admissible, and why was the chosen one preferred? |
| Supporting artefacts | The candidate set; the admissibility result for each candidate including the rejections and their reasons under AD-13; the ranking by risk-adjusted priority; the operator's recorded reason; the recorded dissent, where any |
| The test | A reviewer must be able to see the full admissible set, not only the selected countermeasure, and to identify the rejected candidates and the condition each failed |
| The common failure | The candidate set is reconstructed after the fact from the catalogue, which will not reproduce the set as it stood. The candidate set must be the one recorded at the time |
| What a failure to answer indicates | That the rejections were not recorded, which loses AD-13's whole purpose, or that the selection was made without a ranked set |

#### Q3 — What would have caused withdrawal?

| Aspect | Requirement |
| --- | --- |
| The question | Under what stated conditions was the action to be stopped, and were they met? |
| Supporting artefacts | The abort conditions as written before the action; the abort mechanism and owner; the pre-registered contingency together with the time it was written; the dispatch records; the abort record, if an abort occurred; the reversion record, if an automatic reversion occurred |
| The test | A reviewer must be able to state the withdrawal conditions in the operator's words and assess whether the recorded events met them |
| The common failure | Reading the abort conditions from the current card rather than the revision in force at the time of the action. Cards are revised, and the revision in force is the one that binds |
| The ordering rule | The pre-registered contingency's recorded time must precede the action. The implementation enforces this at the card, refusing to arm a card whose contingency text carries no timestamp, and carries the timestamp into the decision record, so the ordering is established by the record rather than asserted by it. A replay must check the ordering, not assume it |
| What a failure to answer indicates | That the abort conditions were not written before the action, in which case the record is a narrative of what happened rather than a decision record (OP-6) |

#### Q4 — Who authorised it?

| Aspect | Requirement |
| --- | --- |
| The question | Which named person authorised this, on what authority, at what depth, and when? |
| Supporting artefacts | The approver identity; the recorded time of approval; the approval depth required by the profile and collateral class; the engagement authorisation reference; the recorded statement that the approver read the card, the risk assessment, and the abort conditions |
| The test | A reviewer must be able to identify the person and check the approval against the depth the collateral class required |
| The common failure | Accepting the existence of an approval without its depth. An approval at the wrong depth is not an approval, and the check is mechanical |
| What a failure to answer indicates | That the authorisation was not recorded, or was recorded without the depth. In the latter case, the approval's sufficiency cannot be assessed at all |

#### Supporting questions

The four questions above are mandatory. The following are recorded where the material supports them, and their absence is a finding rather than a defect.

| # | Question | Supporting artefacts |
| --- | --- | --- |
| Q5 | What was the risk of not acting, and how did it compare with the risk of acting? | The card's risk assessment, recording both figures (OP-4) |
| Q6 | What did the reviewer believe at the time, and is the belief recorded with its basis? | The decision record's confidence at the time, and the evidence's source tiers |
| Q7 | What would have caused the operation to be escalated rather than continued? | The escalation request record, where one was raised; the card's escalation conditions |
| Q8 | What was the operator's own state of knowledge about their coverage? | The coverage assertions and the recorded detection gaps in force at the time |

### 5.5 The replay output

| Component | Content |
| --- | --- |
| Audit file | The material, its versions, and the chain verification outcome |
| World-state reconstruction | Per decision, the position as understood at the time |
| Admissibility reconstruction | Per candidate, the evaluation against the profile and card in force, compared with what was recorded |
| Answer set | The four questions, answered from the reconstruction, with the artefacts cited for each answer |
| Divergence record | Each case in which a reviewer with the same information would reach a different decision, recorded as a known limitation of the assessment, per ERR-5 |
| Limits statement | Which required fields were unavailable, and what could consequently not be answered |
| Verification status | Each answer carries a status from the set's vocabulary: **Verified (primary)** where the answer is supported directly by the record; **Verified (secondary)** where it is supported by a corroborating artefact; **Requires confirmation** where the record is ambiguous and a named person must settle it; **Unverified** where the record does not support it |

**AUD-4 — A replay reports divergence; it does not resolve it.** Where the reconstruction disagrees with what was recorded, the divergence is recorded with its cause. The replay does not adjudicate whether the operator was right.

### 5.6 Where replay cannot succeed

| Failure | Why it cannot be succeeded | What the auditor reports |
| --- | --- | --- |
| The ledger is broken at a point inside the operation | The sequence of events cannot be established across the break | The replay is performed to the break, and the conclusion is bounded accordingly |
| The ledger is absent | Nothing binds the decisions to a sequence | The operation is not auditable under this procedure |
| The evidence set was not recorded with labels, tiers, and provenance | Q1 cannot be answered | Q1 is recorded as not answerable, with the specific absence |
| The rejected candidate set was not recorded | Q2 cannot be answered | Q2 is recorded as not answerable |
| The abort conditions were written after the action | Q3 cannot be answered as the decision was taken | Q3 is recorded as not answerable, and the record is characterised as a narrative rather than a decision record |
| The approval depth was not recorded | Q4 cannot be answered | Q4 is recorded as not answerable, and the sufficiency of the authorisation cannot be assessed |
| Source telemetry has passed its retention period | Artefacts supporting the reconstruction are no longer available | The reconstruction is bounded by the retained material, and the bounds are recorded |

---

## 6. The Calibration Programme

### 6.1 What is being calibrated

Every confidence value in the set — attribution confidence, effectiveness confidence, the confidence of a claim, and the derivation penalty — is an estimate produced by an analyst or a model. Calibration is the process of establishing how well those estimates correspond to outcomes.

| Quantity | What calibration would mean for it |
| --- | --- |
| Attribution confidence (c) | Of all claims made at a stated confidence level, the proportion that were correct. A value of 0.70 should be right about seven times in ten, across the population of attributions made |
| Effectiveness confidence (q) | Of all countermeasure effectiveness estimates at a stated value, the proportion of operations in which the countermeasure achieved its intended effect |
| Claim confidence | The correspondence between the stated confidence on a claim and the claim's eventual disposition — confirmed, contradicted, or unresolved |
| Derivation penalty (INT-9) | The size of the deduction actually warranted between a derived claim and its inputs, rather than the size currently assumed |
| Threat score components (L, I, A, V) | The correspondence between each component's assigned value and the outcome that followed |

### 6.2 Current status

| Attribute | Position |
| --- | --- |
| Calibration status | **Not calibrated** |
| Basis for the statement | Master design limitation LIM-2 records that every confidence value in the system is an estimate produced by the analyst or the model, that it is not independently calibrated, and that the framework treats confidence as an ordering device and a threshold input rather than as a validated probability |
| Consequence for the framework's operation | The framework functions with uncalibrated confidence. The thresholds in INT-3 are therefore conservative rules of thumb rather than measured boundaries, and they act as floors on what may be done rather than as estimates of where the truth lies |
| Consequence for the audit | An auditor may report that a threshold was met. The auditor may not report that the threshold was the right one, or that meeting it carried any particular probability of the operation being correct |
| What is not claimed | Nothing in this set asserts that the INT-3 thresholds have been validated against outcomes, and no operation's outcome should be read back as though it had validated them |

### 6.3 What calibration would require

| # | Requirement | Detail |
| --- | --- | --- |
| C-1 | An outcome definition for each quantity | A stated, recorded definition of what "correct" means for an attribution, an effectiveness claim, and a claim confidence. Without it, there is nothing to compare against |
| C-2 | A labelled outcome record | For each assessed item, the outcome and its resolution date, recorded independently of the original estimate |
| C-3 | A population large enough to be meaningful | The population must be recorded, with its size, its composition, and the period it covers. A calibration computed on a handful of operations is an anecdote with arithmetic |
| C-4 | Independence of the outcome record from the original assessment | The person or process resolving the outcome must not be the person or process that made the estimate, or the result reflects agreement rather than accuracy |
| C-5 | A defined comparison method | The method by which the stated confidence is compared with the realised outcome, agreed before the outcomes are examined |
| C-6 | A reporting format that does not overstate | A calibration report states the population, the method, the result, and the uncertainty. It does not state that a threshold is correct; it states how often claims made at that threshold were correct |
| C-7 | A review cadence | Calibration is periodic. The thresholds and penalties are versioned, and the version in force is recorded on the card, as master design LIM-4 requires of the taxonomy |

### 6.4 The calibration data set

| Source | What it would contribute | Principal limitation |
| --- | --- | --- |
| After-action reports | Outcome and effectiveness assessments against the confidence stated at the time | Subjective in both halves; the same team produced both, which conflicts with C-4 |
| Exercise records | Outcomes against stated confidences, in a controlled setting | Exercises are not operations, and the setting changes the behaviour being measured |
| Adversary dossiers | Attribution outcomes accumulated across operations | Attribution outcomes are themselves estimates, which compounds the uncertainty rather than reducing it |
| Externally corroborated incidents | Outcomes established independently of the operator | Sparse, and selected for availability of corroboration rather than for representativeness |
| The ledger | The population of confidence values and decisions | The ledger records what was asserted, not what was true, which is the gap calibration is intended to close |

### 6.5 The interim rule

Until a calibration exists, the following applies and is recorded on the card:

| Rule | Statement |
| --- | --- |
| CAL-I-1 | Confidence values are used as ordering devices and threshold inputs. They are not reported as probabilities |
| CAL-I-2 | A confidence value below the INT-3 threshold is treated as insufficient even where the analyst believes it is likely to be correct, and the reason for proceeding is recorded |
| CAL-I-3 | Where a countermeasure does not depend on identity, INT-4 applies and the countermeasure is evaluated on class confidence. This is the principal practical route to action under uncalibrated confidence |
| CAL-I-4 | The uncalibrated status of confidence values is recorded on the card, so that a later reviewer can see that the value was not calibrated at the time and does not treat it as though it were |
| CAL-I-5 | No after-action report may present a confidence value as validated, and no case study may present a single successful operation as evidence of calibration |

### 6.6 Cross-reference to the master design

Master design §11 LIM-2 states that calibration data is a stated gap, tracked in `reference/audit-and-conformance-procedures.md` §5. In this version of the document, the calibration programme is §6 and §5 is the replay procedure. The set index §4 similarly refers to this document's §5 as recording what the framework does not establish, which in this version is §8.

| Item | Status | Action required |
| --- | --- | --- |
| Master design §11 LIM-2 pointer to this document's §5 | Divergent | Amend to §6 |
| Set index §4 pointer to this document's §5 | Divergent | Amend to §8 |
| Master design §11 LIM-14 pointer to this document's §3 | Consistent | None |
| Set index §4 pointer to this document's §3 | Consistent | None |
| Master design §6.4's AD-4, AD-10, and AD-12 rows against the implementation | Consistent after reconciliation | None; the closures are recorded at §3.11 |

Both divergences are recorded as outstanding actions in §11.2. Neither affects the substance of the master design or the set index; both affect a reader's ability to find the right section.

---

## 7. The Measurement Definitions (MET-1 to MET-14)

The master design's traceability table cites `MET-1` to `MET-12`, and the after-action report template names its metric columns by the definitions held here. This section is where they are held. Until it existed, the set registered a requirement family that no document defined, and pointed a template at definitions that were not there; that is a gap this section closes.

Every metric below is stated as a definition, a source, and a window. None of them is asserted to have been measured. The metrics are the ones the framework's own objectives require the operator to be able to state, and the ones the master design's limitation LIM-2 makes impossible to state as anything more than an estimate until the calibration programme at §6 has produced data.

| # | Metric | Definition | Source | Window and unit |
| --- | --- | --- | --- | --- |
| **MET-1** | Detection coverage | The proportion of the taxonomy's techniques for which a detection objective is satisfied **and exercised**, over the techniques exercised in the window. A technique not exercised is *untested*, not *uncovered*, and the two are not conflated | The taxonomy's coverage assessment; the proving ground's exercise record | Per exercise or per period; percentage of techniques exercised, with the untested count reported separately |
| **MET-2** | Autonomous-action interception rate | Of the actions a system took that the operator did not authorise, the proportion the framework intercepted before the action completed | The Ledger's dispatch and abort records | Per operation; count and proportion |
| **MET-3** | False-positive cost | The operator time consumed by detections that were not adversary activity, expressed as a count and as the operator's stated estimate of the time consumed | The triage queue's dispositions; the operator's own account | Per period; count of false positives and the operator's time estimate |
| **MET-4** | Residual risk | The risk carried forward after the selected countermeasures, computed as `R = S_eff × (1 − e)` under `SCORE-2` and `SCORE-4`, with the card's own effectiveness term `e` and not the catalogue's band | The Operation Card; the after-action report | Per operation; the card's figure and the recomputed figure |
| **MET-5** | Mean time to detect | The elapsed time from the adversary's first observable act to the operator's first detection of it | The signal's `observed_at` and the triage disposition | Per period; mean and median, with the window stated |
| **MET-6** | Mean time to respond | The elapsed time from detection to the first countermeasure dispatch under a card | The Ledger's signal and dispatch records | Per period; mean and median |
| **MET-7** | Mean time to recover | The elapsed time from the first countermeasure to the completion of the recovery stage | The Ledger's dispatch records; the card's closure | Per operation; mean and median |
| **MET-8** | Escalation latency | The elapsed time from an escalation request to the granting or refusal of the higher profile | The escalation console's record; the Ledger | Per escalation; mean and median, and the number exceeding the service level |
| **MET-9** | Human-in-the-loop override rate | The proportion of automated classifications, candidate rankings, and advisory outputs that a human overrode | The classification console's override records | Per period; proportion and count, by output kind |
| **MET-10** | Authorisation-refusal rate | The proportion of dispatches the policy engine refused, and the proportion of requests that were escalated rather than dispatched | The Ledger's `dispatch.refused` records; the escalation console | Per period; proportion and count, with the reasons |
| **MET-11** | Collateral incidents | The number of occasions on which a countermeasure had an effect on a party outside the operator's estate, whether or not the effect was authorised, with the severity class of each | The card's third-party assessment; the after-action report | Per operation and per period; count and class distribution |
| **MET-12** | Detection-gap closure rate | The proportion of recorded detection gaps that are closed, and the median time to closure | The gap register | Per period; proportion, count, and median time to closure |

**MET-13 — What a metric may be used for.** A metric value may be cited in an after-action report, an exercise report, or an audit finding. It may not be cited as evidence that the framework is effective, because a metric measures the operator's activity and not the framework's contribution to it. The distinction is the one the master design's LIM-2 and LIM-13 make: an uncalibrated number is an ordering device, and a series of ordering devices is not a demonstration.

**MET-14 — The metrics are not a scorecard.** No aggregate, index, or composite is to be computed across these metrics, and no weighting is to be applied. The metrics answer different questions, their units differ, and a composite would conceal exactly the differences a reader needs to see: a rising interception rate achieved by intercepting more benign traffic is not an improvement, and a falling residual risk achieved by choosing a lower collateral class is not a control.

---

## 8. Conformance Assessment Dimensions

### 7.1 The dimensions and the verdicts

| Dimension | Question asked | Artefact consulted | Verdict options |
| --- | --- | --- | --- |
| **Authorisation conformance** | Was every consequential act within a valid engagement authorisation, within the rules-of-engagement profile in force, and approved by a named person at the required depth? | Engagement authorisation; Operation Card authority fields; approval record; ledger entries for approvals | Conforms · Conforms with qualification · Non-conformance · Not assessable |
| **Control conformance** | Were the admissibility conditions, the class ceilings, the attribution thresholds, and the autonomy budget applied as specified, and were the refusals recorded as refusals? | The countermeasure record with admissibility results and rejections; the reconstructed evaluation under §3.1; the ledger's refusal entries | Conforms · Conforms with qualification · Non-conformance · Not assessable |
| **Disclosure conformance** | Were claims labelled, were confidence and provenance recorded, and was the authorising authority and any affected third party told what the disclosure obligations required? | Evidence ledger entries with label, tier, confidence, and provenance; the after-action report; disclosure and notification records | Conforms · Conforms with qualification · Non-conformance · Not assessable |
| **Evidence conformance** | Is the record complete enough to answer the four replay questions, and is the ledger internally consistent? | The card, the decision records, the evidence set, the ledger export | Conforms · Conforms with qualification · Non-conformance · Not assessable · Not applicable (no operation in scope) |
| **Operational conformance** | Did execution match what was authorised — admissibility re-checked at dispatch, the autonomy budget debited on dispatch, abort channel available and tested, autonomy within envelope and budget, expiry honoured? | `dispatch.issued` and `dispatch.refused` records; abort demonstration record; autonomy monitor state; expiry and reversion records | Conforms · Conforms with qualification · Non-conformance · Not assessable |

### 7.2 Verdict definitions

| Verdict | Definition | What it requires of the report |
| --- | --- | --- |
| **Conforms** | The artefacts satisfy the dimension's question on the material available | The artefacts relied upon are cited |
| **Conforms with qualification** | The artefacts satisfy the question subject to a stated exception, gap, or boundary | The qualification is stated, together with what the qualification prevents the auditor from concluding |
| **Non-conformance** | The artefacts do not satisfy the question | The specific requirement failed is named, and the evidence of the failure is cited |
| **Not assessable** | The material required to answer the question is absent, or is not assessable from it | The absent material is named, and the dimension's question is left unanswered rather than answered weakly |
| **Not applicable** | The dimension does not arise for the operation in scope | The reason is stated, so that the absence of a finding is not read as a finding of conformance |

**AUD-5 — Not assessable is a finding.** A dimension that cannot be assessed is not a dimension that passed. Where a dimension is recorded as not assessable, the audit report states which of the four replay questions, and which enforcement points, the absence leaves unexamined.

**AUD-6 — Verdicts are per dimension.** A finding of non-conformance in one dimension does not imply non-conformance in another, and does not imply the operation was improper. An operation may be properly authorised, improperly executed, and fully recorded, and the report says so in those terms.

### 7.3 Dimension notes

#### 7.3.1 Authorisation conformance

| Aspect | Note |
| --- | --- |
| Primary test | Every consequential act traces to an engagement authorisation in force, to a rules-of-engagement profile at or below the ceiling, and to a named approval at the depth the collateral class required |
| Mechanically-assisted | The AD-1, AD-2, and ROE-1 checks are enforced in the implementation, so the profile and class conformance of a dispatched countermeasure can be re-verified mechanically from the card and the catalogue |
| Not mechanically assisted | Whether the engagement authorisation existed, was valid, and was correctly scoped; whether the approver read what they approved; whether the approval depth was right. These are documentary and are assessed from the artefacts and, where the audit requires it, from the person |
| Common non-conformance | An approval at the wrong depth; an operation that continued past the authorisation's expiry; a card whose authority fields were amended after approval rather than by a new authorisation |
| Third-party note | Authorisation conformance includes the per-target authorisation required by AUTH-6. A countermeasure directed at a third party without it is a non-conformance regardless of everything else being in order |

#### 7.3.2 Control conformance

| Aspect | Note |
| --- | --- |
| Primary test | The admissibility conditions were evaluated; the refusals were refusals rather than warnings; the rejections were recorded with the condition failed and the value that would have admitted the countermeasure |
| Mechanically-assisted | All of AD-1 to AD-13, the class ceilings, the attribution thresholds, and the budget fit are enforced in the implementation, and are re-runnable against the reconstructed card |
| Not mechanically assisted | Whether the candidate set was complete at the time; whether the operator's recorded reason for selecting a lower-ranked countermeasure is the real one; whether the deconfliction set consulted was current |
| Common non-conformance | A rejection recorded without a reason, which loses AD-13's purpose; a countermeasure dispatched that was never evaluated; a profile treated as advice rather than as a ceiling |
| Significance | This is the dimension in which the reference implementation is strongest, and correspondingly the dimension in which an audit can reach the firmest conclusions |

#### 7.3.3 Disclosure conformance

| Aspect | Note |
| --- | --- |
| Primary test | Claims carry a label and a source tier; confidence is separate from label; the authorising authority received what the engagement authorisation required; affected third parties were told where safety or legal consequences bore |
| Mechanically-assisted | The label, tier, and verification status are typed fields on the claim, and the claim cannot be constructed without a text, a bounded confidence, and a bounded derivation penalty. The vocabulary's value tables — thresholds, approval depths, class permissions, ceilings, and exposure normalisation — are fixed and tested. The taxonomy registry's internal consistency is tested, and a card's technique references to it are **not** validated (divergence D-6) |
| Not mechanically assisted | Whether the disclosure was adequate, timely, and candid; whether the authorising authority was in a position to understand it; whether a decision was made to disclose or to withhold, and on what grounds |
| Common non-conformance | A confidence value reported without a label; a claim recorded with a confidence but no provenance; a disclosure to a third party that omitted the collateral class of the action taken against them |
| Constitutional note | CON-8 and CON-11 place the disclosure obligation and the prohibition on concealment in the constitutional instrument. The audit may record whether a disclosure obligation was met; it may not authorise the concealment, and the audit does not create a duty to disclose where none exists |

#### 7.3.4 Evidence conformance

| Aspect | Note |
| --- | --- |
| Primary test | The record is sufficient to answer the four replay questions, and the ledger is internally consistent |
| Mechanically-assisted | The chain verification in §4 is fully mechanical, and the required-field presence in §5.2 is testable by inspection |
| Not mechanically assisted | Whether the recorded evidence is sufficient in substance rather than in form; whether the reasoning recorded is the reasoning held; whether the pre-registered contingency was genuinely pre-registered |
| Common non-conformance | A decision log that satisfies its author but not a reviewer; a card whose abort conditions were written after the outcome; an evidence set that was curated rather than recorded |
| Relationship to the other dimensions | This dimension is the substrate of the others. A non-conformance here reduces the strength of every conclusion that relies on the record, and the reduction should be stated where the conclusion is expressed |

#### 7.3.5 Operational conformance

| Aspect | Note |
| --- | --- |
| Primary test | The executed action matched the authorised action; admissibility was re-checked at dispatch against current world state; the abort channel was available and demonstrated; autonomy stayed within its envelope and budget; expiry was honoured |
| Mechanically-assisted | The budget fit (AD-11) is enforced in the admissibility path, and the budget is **debited on dispatch** by `caos/decision.py::dispatch`, which re-evaluates the admissibility algebra at dispatch time, spends nothing on a refusal, and writes a `dispatch.issued` or `dispatch.refused` record to the ledger. The card's armability, its expiry, its approval depth, its mandatory fields, and its technique-reference validity are enforced in the same evaluation. The abort path reverts the posture, consumes the remaining budget, and writes to the ledger |
| Not mechanically assisted | Whether the abort channel was genuinely usable by the operator on the day, and whether an automatic reversion occurred promptly. Master design HITL-5 requires automatic and unconditional reversion, and the implementation's reversion is a human-initiated command. The attestation limbs of the hybrid and human conditions — the irreversibility argument, the indirect-effect attestation, the deconfliction attestation, and the non-weaponisation attestation — are enforced in the sense that the engine refuses where they are absent, but their content is a human judgement and is not evaluated |
| Common non-conformance | An action dispatched at a time when the world state had changed since evaluation; an operation that continued past expiry because nothing checked; an autonomy grant that outlived its declared window |
| The dimension's weak point | The dimension's primary test — that autonomy stayed within its budget — is now evidenced by the record, because the dispatch record states the units spent and the remaining budget. What the record still does not establish is that the action taken in the estate corresponds to the dispatch that was recorded. That correspondence is a question about the deployment, and no implementation can answer it |
| Significance | This dimension is where the framework's design and the reference implementation are now closest, and it is the dimension an auditor should still examine most sceptically — because the mechanism now exists, and a mechanism that exists can be relied upon only if the deployment actually uses it |

---

## 9. What an Auditor May Conclude

### 8.1 Permitted conclusions

| # | Conclusion | Condition | Artefact basis |
| --- | --- | --- | --- |
| P-1 | The operation was authorised, within a profile, at an appropriate depth | The authorisation, the card's authority fields, and the approval record are present and consistent | Engagement authorisation; card; approval record |
| P-2 | The countermeasure dispatched was admissible against the card and profile in force | The admissibility evaluation is re-runnable and returns the same determination | Card, catalogue, `caos/roe.py` reconstruction |
| P-3 | The record is internally consistent with the append procedure, and conforms to the platform specification's record structure | Every recomputed digest and predecessor reference matches, the sequence is contiguous from 1, the body fields and canonical form are as specified, and the manifest agrees with the records | Ledger export; `caos/ledger.py` verification; `operational/platform-architecture-and-agent-containment.md` §11 |
| P-4 | The record is sufficient to reconstruct what was known, what was chosen, and what would have caused withdrawal | The required fields of §5.2 are present | Card; decision records; evidence set |
| P-5 | The engine refused, and the refusal was recorded with its reason | The refusal entry names the condition and the margin | Ledger refusal entries; `caos/roe.py` |
| P-6 | A specific requirement was not enforced by the implementation | The requirement appears in the procedural-only register in §3.13, and no enforcement was found | The register in §3 |
| P-11 | The implementation evaluates a requirement, and a named test demonstrates the behaviour | The register row in §3 names the function and the test, and both exist in the source | The register in §3; the implementation source and suite |
| P-7 | A confidence value was uncalibrated at the time | The card and the decision record record the value, and no calibration result existed at that date | The card; §6.2 |
| P-8 | The operator's own coverage was incomplete for the detected activity | The coverage assessment and the gap list in force at the time are present | Coverage assessment; detection gap list |
| P-9 | The operation diverged from what a reviewer with the same information would have decided | The divergence is recorded with its cause, per ERR-5 | The divergence record |
| P-10 | The audit is not able to answer a stated question | The missing material is named | The limits statement |

### 8.2 Impermissible conclusions

| # | Conclusion an auditor may not draw | Why not | What the auditor states instead |
| --- | --- | --- | --- |
| I-1 | That the operator was correct, or that the decision was the best available | The record shows the reasoning, not its quality | That the reasoning was as recorded, with its basis and confidence |
| I-2 | That the adversary was, or was not, the party the attribution named | Attribution is an estimate with a confidence, and the confidence is uncalibrated | The attribution assessment as recorded, with its candidate distribution, basis, and stated confidence |
| I-3 | That the framework's controls worked | An audit of one operation's record does not measure efficacy, and the measurement requirements are a separate matter | That the controls were applied as specified in this operation, as far as the record shows |
| I-4 | That the operator's estate was secure, or that no compromise occurred | The record is a record of decisions, not of the estate | The coverage the record shows, and the gaps it records |
| I-5 | That the ledger proves the recorded content was true | The chain establishes internal consistency, not truth | That the chain verifies, with the §4.4 and §4.5 limits stated |
| I-6 | That the chain's integrity establishes who wrote an entry | The chain carries no authorship evidence beyond the recorded actor field, which is itself part of the chain | That the entry records an actor, and that the chain is internally consistent |
| I-7 | That the engagement authorisation was lawful | The framework encodes authorisation structure, not legal judgement; master design LIM-10 records that legal advice is not embedded | That an authorisation with stated terms was in force and was relied upon |
| I-8 | That the confidence values meet the thresholds in any statistical sense | The thresholds are not calibrated; §6.2 | That the recorded value met the threshold as a rule of the framework |
| I-9 | That the absence of a finding is a finding of conformance | Absence of evidence is not evidence of absence, and the framework's ERR-3 treats silence as a condition to be explained | Not assessable, with the material that would have been needed named |
| I-10 | That no third party was affected | The record cannot establish what happened outside it | The collateral exposure as recorded, and the third-party dependencies as recorded |
| I-11 | That a conformity statement in this document certifies the set or any deployment | The set holds no certification, accreditation, or regulatory status | The specific findings of the specific audit, bounded by §9 |
| I-12 | That a compound or systemic weakness in the framework has been identified | An audit of a record does not test the framework's structure | The specific divergence, recorded as a divergence |
| I-13 | That the reference implementation is conformant with the framework | The register in §3 is a statement about what the code does and where the evidence is. The judgement that the code is conformant is a human one, and is not made in this document | The specific rows of §3, with the function and the test named for each, and the limits in §3.0 and §3.12 |
| I-14 | That the closed divergences in §3.11 were closed by the implementation conforming to the framework | Each closure was closed by a named instrument — a change to the code, a reconciliation of the requirement text, or a scoping. None of the three is a statement that the framework's requirement is satisfied in substance | The instrument, the test, and what the closure does and does not establish |
| I-15 | That a passing test suite establishes that the framework's requirements are met | A passing suite demonstrates that the tests pass. Whether the tests say what the requirements mean is a separate question, and one that only a re-derivation can answer | The suite result, the snapshot it was run against, and the register rows that depend on it |

### 8.3 On the impermissible conclusions in practice

| Pattern | Where it arises | Control |
| --- | --- | --- |
| The finding is stronger than the evidence | A chain that verifies being read as proof of truth | §4.4, §4.5, and I-5 |
| The auditor is asked to reassure | A request that the audit state that the operation was sound | §8.2, and the requirement that every conclusion cites the artefacts it rests on |
| A non-conformance is generalised | One operation's failure treated as a property of the framework | §7.2 AUD-6; the finding is per dimension and per operation |
| An uncalibrated value is treated as a measurement | A threshold met being described as a probability | §6.2, I-8, and CAL-I-1 |
| The audit's scope is widened | A question about the record being answered as a question about the world | §1.2 and §1.3 |

---

## 10. Known Limitations of the Audit Model

**LIM-AU1 — The audit model is documentary, not evidential.** It establishes what the record says, not what happened. Every finding in this document is a finding about the record, and it should be read with §1.2 in hand.

**LIM-AU2 — The ledger's integrity is internal.** Tamper evidence establishes that the exported ledger is not the product of the documented append procedure. It does not establish who altered it, whether it was altered at all as against a storage or export defect, or that the entries before the divergence are correct in their content.

**LIM-AU3 — There is no external anchoring.** The chain's first entry is trusted by fiat, and a party with write access to the whole ledger can rebuild a self-consistent chain. The consequence for an audit is that the finding available is internal consistency, and no stronger. See §4.5.

**LIM-AU4 — The reference implementation is a reference, not a certified product.** Conformance to the implementation establishes the behaviour of that implementation. It establishes nothing about any deployed system, about a deployment's configuration, or about the operator's practice.

**LIM-AU5 — The mechanically-enforced surface is a small fraction of the framework.** Master design LIM-14 records that the implementation does not verify conformance of produced documents to the prose requirements. This register quantifies the gap: nineteen requirement families are procedural only, and the enforced set is concentrated in the admissibility algebra, the scoring arithmetic, the class ceilings, the attribution thresholds, the budget fit, and the ledger chain. A report that presented only the enforced set would materially overstate the framework's assurance.

**LIM-AU6 — Confidence values are uncalibrated.** Every confidence in the record is an estimate, and no calibration programme exists. The thresholds that consume those estimates are conservative rules rather than measured boundaries. Master design LIM-2 records the same limitation, and §6.2 records the status.

**LIM-AU7 — The exclusion checks are only as good as the card data.** AD-5 and AUTH-6 are enforced against the authorised-target and third-party sets as recorded on the card. A card that records a third party as authorised is not caught by them. The checks reduce the risk of accidental reach; they do not detect a mis-recorded scope.

**LIM-AU8 — Replay cannot recover what was not recorded, and the record is not complete by design.** Some fields are deliberately absent from a record — for example, the reasoning that was not held, the evidence that was never seen, and the alternatives that were never generated. The absence of a field is sometimes informative, and a replay that treats an absent field as an empty one will misread the operation.

**LIM-AU9 — Replay is bounded by retention.** The reconstruction depends on source telemetry that may have been retained for a shorter period than the operation. Master design INT-10 requires retention periods to be stated, and the audit is bound by them.

**LIM-AU10 — The register is a statement about a settled codebase, and a finding still needs more than it.** The register in §3 was derived by inspection of the implementation and its test suite at the snapshot recorded in §3.0, and the implementation is now settled for this revision rather than moving under the auditor's hand. That removes one obstacle and leaves two. A finding still requires a fixed, identified snapshot of the implementation, a recorded run of the suite against that snapshot attached to the finding, and an independent re-run by a party other than the author of the code; §3.12 states each of the three and why each is needed. The synchronisers' `--check` mode gives a reproducible statement that the implementation agrees with the canonical documents, which is a different and weaker statement: it identifies no code, and it is not a test result. And a passing suite is not a finding that the framework's requirements are met; it is a finding that the tests pass.

**LIM-AU11 — The audit model measures bookkeeping, not effectiveness.** Master design DO-13 requires detection coverage, autonomous-action interception rate, false-positive cost, and residual risk to be measured and reported. Those measurements are the subject of the set's measurement requirements and the after-action report; the audit procedure does not produce them and does not stand in for them. An operation that passes every dimension of §7 may still have been a failure in outcome.

**LIM-AU12 — The set provides no third-party assurance route.** Nothing in this set is capable of being certified, accredited, or audited by an external body as a scheme, and this document is a procedure for an internal or invited reviewer, not a certification standard. An audit under this procedure is an audit of one operation's record by a party the operator trusts, and the operator's selection of that party is not itself audited here.

**LIM-AU13 — The framework cannot create authority.** Master design LIM-3 records that the policy engine enforces the authorisation it is given and cannot determine whether a countermeasure is lawful, proportionate, or right. The same applies to this procedure: it verifies that an authority was in force and relied upon, and it does not and cannot verify that the authority was proper.

**LIM-AU14 — Misattribution remains the dominant risk, and the audit does not reduce it.** Master design LIM-1 records that the framework bounds the consequence of misattribution through confidence thresholds, class asymmetry, and a preference for identity-independent countermeasures, and that it does not make misattribution less likely. An audit conducted after the fact cannot correct a misattribution either, and where the record shows that a countermeasure was selected on a contested attribution, the audit records that fact rather than resolving it.

**LIM-AU15 — This register covers the operational core, and the emergency path is registered elsewhere.** `caos/emergency.py` and `caos/emergency_console.py` implement the emergency shutdown and containment protocol, whose requirements are owned by `operational/emergency-shutdown-and-containment-protocol.md`; that document's §22.1 registers that protocol's own mechanically-enforced surface with the module, function, and test for each requirement it evaluates. Divergence D-8 is closed by that scoping rather than by removal. The consequence for an auditor is that this document's register and the emergency protocol's register together are the implementation's whole enforcement surface, and neither is a certification of it. A reader assessing the platform as a whole should read both, and should record the two snapshots together, because the two registers were derived at different moments.

**LIM-AU16 — The attestation limbs of the hybrid and human conditions are not demonstrated by tests.** Six card fields are consulted by the engine and are covered by no test at the 2026-10-20 snapshot: `irreversibility_argument`, `indirect_effect_attestation`, `non_weaponisation_attestation`, `deconfliction_attestation`, `deconfliction_map_current`, and `per_target_authorisations`. The first four are the attestation limbs of AD-3, AD-6, AD-10, and AD-12, and the last two are limbs of AD-5 and AD-10. The comparison limbs are demonstrated; the attestation limbs are exercised by the engine and are not demonstrated. A finding that rests on an attestation limb is qualified accordingly, and §3.12 records the gap.

**LIM-AU17 — A closed divergence records that a disagreement was settled, not that a requirement is met.** Each of D-1 to D-8 in §3.11 was closed by an instrument: a change to the implementation, a reconciliation of the requirement text with the implementation, or a scoping. None of those is a statement that the requirement is satisfied in substance, and the register does not read them as one. The one to watch is D-1, where the implementation now performs both limbs of AD-4 and the master design's row was amended to match; the amendment is a reconciliation, and the question of whether the amended text is the right specification is a question for the requirement's owner.

---

## 11. Summary

### 10.1 What this document establishes

| Point | Statement |
| --- | --- |
| The register is the concrete finding | The reference implementation enforces the admissibility algebra in full, the card's armability, the scoring arithmetic and the confidence propagation, the ceilings, the third-party exclusion, the attribution thresholds, the autonomy budget and the dispatch path, the ledger chain and its export, the catalogue and registry's integrity, the agreement between the set's two binding instruments, and the source-integrity states. Seventy-six rows, each naming the function that implements the requirement and the test that demonstrates it |
| The register is a statement, not a certification | It says what the code does and where the evidence is. **The judgement that the implementation is conformant with the framework remains a human one, and is not made here.** §3.0, §8.2, and LIM-AU10 carry the point, and §3.12 states what a finding would still need |
| All eight divergences are closed | D-1 to D-8 each carry a resolution, the instrument that carried it, and the test that demonstrates it, in §3.11. Five were closed by a change to the implementation, two by reconciling the requirement text with the implementation, and one by scoping. A closed divergence records that a disagreement was settled, not that a requirement is satisfied in substance — LIM-AU17 |
| The implementation is settled, and the drift check is reproducible | The suite stands at 364 tests with no failures, and both synchronisers' `--check` mode reports the implementation in agreement with the canonical documents. The register describes a codebase that is no longer moving, and §3.12 states the three things a finding would still need on top of that |
| The ledger can be verified by a third party | The procedure in §4 requires only the export, and the implementation provides both the portable export and an independent verifier that rebuilds and checks a chain from it. It produces a finding of internal consistency, not of authenticity, and §4.4 and §4.5 state why. The export is explicitly unsigned, and says so |
| Replay has a specification | Four questions, eighteen required fields, and eight steps. A replay that cannot answer the four is not a replay of the operation. The chain extraction, the verification, the admissibility re-run, and the dispatch record are mechanised; the reconstruction of what was known and what would have caused withdrawal is the auditor's work |
| Confidence is not calibrated | The framework's thresholds are conservative rules rather than measured boundaries, and §6.2 records the status and §6.5 the interim rule |
| The audit is bounded | §8 states the conclusions an auditor may draw and the conclusions they may not, and §9 states the seventeen limitations of the model itself. An audit that does not carry those limits is not an audit under this procedure |

### 10.2 Outstanding actions

The items closed at this revision — the divergence register, the dispatch path, the technique-reference validation, the contingency timestamp, the AD-4 set-containment limb, the subtractive confidence propagation, and the emergency protocol's scoping — are recorded in §3.11 and are not repeated here. What follows is what remains open.

| # | Action | Blocking | Priority |
| --- | --- | --- | --- |
| 1 | Fix an identified snapshot of the implementation, record it, run the suite against it, and attach the result to any finding that cites the register. §3.12 states the three things a finding needs: the snapshot, the recorded result, and an independent re-run | None — this is the first action an auditor performs | High |
| 2 | ~~Add tests for the six attestation fields~~ — **Closed at version 1.1.** `tests/test_attestations.py` demonstrates all six in both their failing and their passing state, and the corresponding register rows have moved from *Requires confirmation* to mechanically enforced. The action is retained in the register because a closed action that is removed is indistinguishable from an action that was never taken | Implementation owner | Closed |
| 3 | Put the two synchronisers under the unit-test suite, so that the failure path — what happens when a canonical document and its generated module disagree — is demonstrated rather than asserted. The drift check is executable, but it is not a test | Implementation owner | Medium |
| 4 | Refuse the construction of a decision record with an empty `known_at_the_time` or `pre_registered_contingency` field, so that AD-13's reporting discipline and OP-6's completeness requirement are enforced rather than assumed | Implementation owner | Medium |
| 5 | Amend master design §11 LIM-2 to point to §6 of this document rather than §5 | Master design revision | Medium |
| 6 | Amend set index §4 to point to §8 of this document rather than §5 for the statement of what the framework does not establish | Set index revision | Medium |
| 7 | Implement the periodic independent publication of the ledger's anchor artefact, so that the anchor can serve the purpose the verification report states for it. The artefact and the audit view exist; the publication does not | Platform owner | Medium |
| 8 | Specify the outcome definitions and the labelled outcome record required by §6.3, and open the calibration programme | Start of the calibration programme | Medium |
| 9 | Establish the review cadence for the register in §3, and re-issue it with the review date and the snapshot identifier, so that the register does not drift from the implementation it describes | Implementation change control | Low |
| 10 | Extend the ledger export's manifest to carry anything else a verifier needs to establish completeness without the card, and record the decision not to if the card cross-check in V-8 is preferred | Export format change | Low |
| 11 | Confirm the dispatch console and command-line surfaces, which are exposed and exercised by the function beneath them but are not separately under test | Implementation owner | Low |

---

*This was supported for MIA by Kilo (kilo-auto/free).*
