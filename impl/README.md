# CAOS Reference Implementation

| Field | Value |
| --- | --- |
| Author | MIA |
| Attribution | This was supported for MIA by Kilo (kilo-auto/free). |
| Version | 1.0 |
| Language | Python 3.11 or later; standard library only, no external dependencies |
| Purpose | The executable statement of the decision-support model, the admissibility algebra, the Ledger, the Watchfloor, and the proving ground |
| Status | Reference implementation. It is the work of the named human author, assisted as above; it is not claimed to have been written by an AI system acting independently |

---

## 1. What this is

The documentation set states the model. This package is the model, running.

It contains the parts of the framework that can be reduced to deterministic rules and therefore *should* be reduced to deterministic rules: the admissibility algebra, the scoring and confidence model, the authorisation ledger, the countermeasure catalogue, the adversary taxonomy, and the operator console. It contains none of the parts that depend on human judgement, because those belong to the people.

The implementation is deliberately not a security product. It does not detect attacks, it does not touch a network, and it does not talk to any adversary's systems. It is the reasoning surface that a human operator works against, and the audit surface that a reviewer works against afterwards.

---

## 2. Layout

| Module | Responsibility | Owns |
| --- | --- | --- |
| `caos/canonical.py` | The canonical JSON form | One definition of the bytes every digest is computed over, shared by the model and the Ledger |
| `caos/vocab.py` | The controlled vocabulary | Claim labels, source tiers, verification statuses, collateral classes C0–C3, autonomy classes AC-0–AC-4, ROE profiles R0–R5, countermeasure classes CM-A–CM-G, reversibility categories, attribution dependencies, approval depths, attribution thresholds |
| `caos/models.py` | The core data model | `Claim`, `Signal`, `ThreatAssessment`, `Countermeasure`, `AutonomyGrant`, `OperationCard`, `DecisionRecord`, `AdmissibilityFailure` |
| `caos/taxonomy_data.py` | The generated technique registry | The seventy-seven techniques, read from `operational/adversary-ai-taxonomy-and-threat-model.md` by `tools/sync_taxonomy.py`. Do not edit by hand |
| `caos/taxonomy.py` | The adversary taxonomy registry | Categories AAT-1 to AAT-10, seventy-seven techniques, the identity-dependence split, and the coverage assessment function |
| `caos/countermeasures.py` | The countermeasure catalogue | OCC-01 to OCC-43 with full metadata, and the technique-binding lookup |
| `caos/catalogue_data.py` | The generated catalogue data | The forty-three entries, read from `operational/countermeasure-catalogue.md` by `tools/sync_catalogue.py`. Do not edit by hand |
| `caos/scoring.py` | The scoring and confidence model | Threat score, effective threat, residual risk, risk-adjusted priority, confidence propagation, the score breakdown |
| `caos/roe.py` | The admissibility engine | AD-1 to AD-12, the informative refusal, and the card-armability precondition |
| `caos/decision.py` | The selection algorithm | Candidate generation, admissibility filtering, ranking, the selection record, the counterfactual comparison |
| `caos/ledger.py` | The Ledger | The append-only hash chain, verification, anchoring, export, replay |
| `caos/watchfloor.py` | The operator console | The watchboard, triage, card view, ROE gate, countermeasure console, decision space, autonomy monitor, abort, replay, audit |
| `caos/proving_ground.py` | The exercise harness | The adversary archetypes, the seeded simulator, the coverage evaluation, the exercise rubric |
| `caos/emergency.py` | The emergency containment core | The severity ladder, the emergency state machine, the zero-collateral pre-dispatch checks, the protected control set, the PACE envelope, the kill-verification gate, and the re-entry criteria |
| `caos/emergency_console.py` | The emergency console | The synthetic containment drill, the emergency action catalogue, and the rendered pre-dispatch checks |
| `caos/demo.py` | The synthetic estate | A fictional card, four synthetic signals, and a populated Ledger, used by the CLI and the tests |
| `caos/cli.py` | The command-line entry point | The console commands |
| `tools/sync_catalogue.py` | The catalogue synchroniser | Parses `operational/countermeasure-catalogue.md` and writes `caos/catalogue_data.py`, so that the executable catalogue cannot drift from the written one |
| `tests/test_attestations.py` | The attestation limbs | The six card fields the hybrid and human conditions consult |
| `tests/test_emergency_controls.py` | The emergency controls | The armability, authority, prohibition, second-approver, rotation, level and re-entry gates |
| `tests/test_branches.py` | The branches a code review found untested | The withheld entry, the flag-and-direction guard, the protected scope, the authority paths, the ledger failure, the export validation, the abort attribution, the score ceiling |
| `tests/test_sync_tools.py` | The synchronisers' failure paths | A duplicate identifier, a missing entry, an unreadable row, a missing library, an undefined category |
| `tests/test_class_mapping.py` | The class-to-category join | The catalogue's bindings against the taxonomy's categories |
| `tools/sync_taxonomy.py` | The taxonomy synchroniser | Parses `operational/adversary-ai-taxonomy-and-threat-model.md` and writes `caos/taxonomy_data.py`, so that the executable technique registry cannot drift from the written one |

---

## 3. Running it

The package is standard-library only. It runs from the directory that contains it:

```bash
cd "/home/k/Desktop/AI C@ Op/impl"
python3 -m caos.cli watchboard
python3 -m caos.cli triage
python3 -m caos.cli card OC-2026-014
python3 -m caos.cli cm OC-2026-014
python3 -m caos.cli roe OC-2026-014 OCC-34
python3 -m caos.cli options OC-2026-014
python3 -m caos.cli autonomy OC-2026-014
python3 -m caos.cli select OC-2026-014 OCC-10 --confirm
python3 -m caos.cli replay OC-2026-014
python3 -m caos.cli audit
python3 -m caos.cli abort OC-2026-014 "the service degraded below its floor"
python3 -m caos.cli catalogue --class Detect
python3 -m caos.cli techniques
python3 -m caos.cli exercise --archetype "social-engineering swarm" --steps 20
python3 -m caos.cli emergency drill
python3 -m caos.cli emergency catalogue
```

Every command operates on the synthetic estate in `caos/demo.py`. The estate is fictional, and no command contacts anything.

### Keeping the catalogue in step with the document

The countermeasure catalogue is written in `operational/countermeasure-catalogue.md`, and that document is authoritative. The executable copy is generated from it:

```bash
cd "/home/k/Desktop/AI C@ Op/impl"
python3 tools/sync_catalogue.py          # regenerate caos/catalogue_data.py
python3 tools/sync_catalogue.py --check  # report drift, write nothing
python3 tools/sync_taxonomy.py           # regenerate caos/taxonomy_data.py
python3 tools/sync_taxonomy.py --check   # report drift, write nothing
```

The synchronisers are strict: a metadata value either does not recognise is an error rather than a default, and a missing entry is an error rather than an omission. A silently defaulted countermeasure attribute, or a technique that silently fails to import, is exactly the divergence the tools exist to prevent. Run `--check` on both in any process that verifies the implementation against the set.

Two documents are canonical, and the split is deliberate. The countermeasure catalogue is canonical for the catalogue's entries, and the taxonomy document is canonical for the technique list; the technique library is canonical for the per-technique indicators, detection methods, technique-level bindings, and external-mapping verification status. The generated modules hold only what their canonical document holds.

### Tests

```bash
cd "/home/k/Desktop/AI C@ Op/impl"
python3 -m unittest discover -s tests -t .
```

The suite covers the controlled vocabulary, the scoring model, each of the twelve admissibility conditions in both its failing and passing state, the six attestation fields the hybrid and human conditions consult, the card-armability preconditions, the selection algorithm, the dispatch path, the counterfactual comparison, the Ledger's chain, canonicalisation and tamper detection against the platform specification's own worked example, the source integrity states, the console views, the emergency containment path, the proving ground, and the cross-document binding consistency between the catalogue and the technique library. It uses the standard library's `unittest` so that it runs anywhere Python does.

---

## 4. What the implementation enforces, and what it does not

This mirrors the register in `../reference/audit-and-conformance-procedures.md` §3.

### Mechanically enforced

| Requirement | Enforced by | Demonstrated by |
| --- | --- | --- |
| AD-1 Profile class and floor | `roe._check_ad1` | `tests/test_roe.py::AD1ProfileClassTests` |
| AD-2 Collateral class ceiling | `roe._check_ad2` | `tests/test_roe.py::AD2CollateralTests` |
| AD-3 Reversibility floor | `roe._check_ad3` | `tests/test_roe.py::AD3ReversibilityTests` |
| AD-4 Target containment | `roe._check_ad4` | `tests/test_roe.py::AD4TargetContainmentTests` |
| AD-5 Third-party exclusion | `roe._check_ad5` | `tests/test_roe.py::AD5ThirdPartyTests` |
| AD-6 Human beings not the object | `roe._check_ad6`, and a construction guard in `models.Countermeasure` | `tests/test_roe.py::AD6HumanBeingsTests` |
| AD-7 Autonomy class ceiling | `roe._check_ad7` | `tests/test_roe.py::AD7AutonomyTests` |
| AD-8 Countermeasure confidence floor | `roe._check_ad8` | `tests/test_roe.py::AD8ConfidenceTests` |
| AD-9 Attribution dependency satisfied | `roe._check_ad9` | `tests/test_roe.py::AD9AttributionTests` |
| AD-10 Deconfliction passed | `roe._check_ad10` | `tests/test_roe.py::AD10DeconflictionTests` |
| AD-11 Autonomy budget available | `roe._check_ad11` | `tests/test_roe.py::AD11BudgetTests` |
| AD-12 Non-weaponisation | `roe._check_ad12`, and a construction guard in `models.Countermeasure` | `tests/test_roe.py::AD12NonWeaponisationTests` |
| AD-13 Inadmissibility is informative | `roe.AdmissibilityResult.failures` | `tests/test_roe.py::InformativeFailureTests` |
| G-3/G-4 Card armability precondition | `roe.card_is_armable` | `tests/test_roe.py::CardArmabilityTests` |
| INT-3 Attribution thresholds by collateral class | `vocab.attribution_threshold`, applied in `roe._check_ad9` | `tests/test_vocab.py::AttributionThresholdTests` |
| ROE-1 Profile ceiling | `roe._check_ad1` | `tests/test_roe.py::AD1ProfileClassTests` |
| Effective approval depth | `vocab.required_approvals`, reached through `models.OperationCard.approval_gap` and checked by `roe.card_is_armable` | `tests/test_vocab.py::ApprovalDepthTests` |
| SCORE-1 to SCORE-5 scoring formulas | `scoring.threat_score`, `effective_threat`, `residual_risk`, `risk_adjusted_priority`, `propagate_confidence` | `tests/test_scoring.py` |
| DO-12 Ledger tamper evidence | `ledger.Ledger.verify`, `ledger.Ledger.anchor` | `tests/test_ledger.py::LedgerChainTests` |
| Reversal ordering and the reverse digest chain | `ledger.Ledger.from_export` | `tests/test_ledger.py::LedgerRoundTripTests` |
| Catalogue boundaries | construction guards in `models.Countermeasure` | `tests/test_catalogue.py::CatalogueIntegrityTests` |
| Taxonomy binding integrity | `taxonomy.TECHNIQUES` cross-checked against the catalogue | `tests/test_catalogue.py::TaxonomyIntegrityTests` |
| Catalogue entry metadata matches the written catalogue | `tools/sync_catalogue.py --check` | `tools/sync_catalogue.py` |
| AD-3 reversibility argument required where the effect is irreversible | `roe._check_ad3` | `tests/test_roe.py::AD3ReversibilityTests`, `tests/test_attestations.py::AD3IrreversibilityArgumentTests` |
| AD-6 indirect-effect attestation where the techniques operate on people | `roe._check_ad6` | `tests/test_roe.py::AD6HumanBeingsTests`, `tests/test_attestations.py::AD6IndirectEffectTests` |
| AD-10 deconfliction attestation where the map is degraded | `roe._check_ad10` | `tests/test_roe.py::AD10DeconflictionTests`, `tests/test_attestations.py::AD10DeconflictionAttestationTests` |
| AD-12 non-weaponisation declaration or attestation | `roe._check_ad12` | `tests/test_roe.py::AD12NonWeaponisationTests`, `tests/test_attestations.py::AD12NonWeaponisationTests` |
| AD-5 per-target authorisation, shared-tenancy assessment, and refusal of a Withheld entry | `roe._check_ad5` | `tests/test_roe.py::AD5ThirdPartyTests`, `tests/test_attestations.py::AD5PerTargetAuthorisationTests` |
| AD-4 set containment where the countermeasure names its targets | `roe._check_ad4` | `tests/test_roe.py::AD4SetContainmentTests` |
| The engine fails closed: an unrecorded confidence is a refusal, not a permission | `roe.EvaluationContext` defaults | `tests/test_attestations.py::FailClosedDefaultTests` |
| Subtractive confidence propagation | `scoring.propagate_confidence` | `tests/test_scoring.py::ConfidencePropagationTests` |
| Emergency severity ladder, state machine, zero-collateral checks, protected control set, kill verification, staged rotation, re-entry | `emergency` module | `tests/test_emergency.py` |
| Dispatch re-checks admissibility, debits the autonomy budget, and records the outcome | `decision.dispatch` | `tests/test_decision.py::DispatchTests` |
| A card citing a technique the registry does not carry cannot be armed | `models.OperationCard.unknown_techniques` | `tests/test_roe.py::CardArmabilityTests` |
| The five-state source integrity vocabulary, and that a missing source is not a negative finding | `vocab.IntegrityState`, `models.Signal.integrity_state` | `tests/test_watchfloor.py::IntegrityStateTests` |
| The Ledger's digest computation, canonicalisation, and the platform document's own worked example | `ledger.canonical_bytes`, `ledger.Ledger` | `tests/test_ledger.py::WorkedExampleTests` |
| The catalogue's category bindings and the library's technique-level bindings agree, and are bounded against growth | `taxonomy.TECHNIQUES`, `countermeasures.CATALOGUE` | `tests/test_bindings.py` |

### Procedural only

The following requirements are not mechanically enforced, because they require a person, a process, or a fact that cannot be derived from the card's state. They are listed so that a reader knows the boundary of the code.

- Whether the engagement authorisation is itself lawful. The engine checks that a card cites one; it cannot check that the authorisation is valid, current, or correctly granted.
- Whether the attribution assessment is correct. The engine checks the confidence against the threshold; it cannot check the reasoning behind the confidence.
- Whether the risk of inaction recorded on the card is the operator's genuine assessment.
- Whether the approver read the card, understood it, and could have changed the decision.
- Whether the abort conditions are the right ones for the situation.
- Whether the shared-tenancy assessment is truthful.
- Whether the operator's judgement in selecting one countermeasure over another was sound.
- Whether the framework's limits, as recorded in the set's limitation registers, are respected in practice.

---

## 5. The boundary of the code

The implementation refuses, by construction, to hold a countermeasure that targets a human being or that uses a model to attack a model. `models.Countermeasure.__post_init__` raises on either. This is not a policy applied at runtime to a countermeasure someone else built; it is a refusal to let such an object exist, so that the catalogue cannot drift into the territory the framework excludes.

The same reasoning applies to the Ledger: `ledger.Ledger.verify` states both what an intact chain establishes and what it does not. An intact chain is evidence that the recorded sequence has not been altered since it was written. It is not evidence that the recorded decisions were correct, and it is not protection against an attacker with write access to the whole chain — the stated mitigation is external anchoring, implemented by `ledger.Ledger.anchor`.

---

## 6. Adapting it

The catalogue, the taxonomy, and the profiles are data, not code, and are the intended extension points. To adapt the framework to a different estate:

1. Edit `operational/countermeasure-catalogue.md` to add or amend catalogue entries, then run `python3 tools/sync_catalogue.py` to regenerate `caos/catalogue_data.py`. The entry data is **not** written in `caos/countermeasures.py`, which converts the generated data into the executable model. The construction guards in `caos/models.py` will refuse an entry that breaches the boundary; a countermeasure with a different collateral profile is added by amending the entry's metadata in the document, not by weakening the guard.
2. Edit `caos/taxonomy.py` to add techniques, and add the corresponding bindings to the catalogue entries. `tests/test_catalogue.py` checks that every technique binding resolves, so a dangling binding fails the suite.
3. Edit `caos/vocab.py` to change a profile, a class, or a threshold. Every such change is a change to the authorisation model and should be recorded as a governed event under the set's change-control rules.
4. Do not weaken the guards in `models.py` or `roe.py` to make a new countermeasure admissible. If a countermeasure cannot be made admissible, the correct response is a new authorisation, not a weaker rule.

---

*This was supported for MIA by Kilo (kilo-auto/free).*
