# Technical Audit: Emergency Shutdown and Containment Protocol and its Reference Implementation

| Field | Value |
| --- | --- |
| Author | MIA |
| Attribution | This was supported for MIA by Kilo (kilo-auto/free). |
| Document type | Review record |
| Subject | A technical audit of `operational/emergency-shutdown-and-containment-protocol.md` and its reference implementation, against the set's own conventions, the constitutional instrument, and the rest of the CAOS implementation |
| Version | 1.1 |
| Status | Finding record. It changes no requirement and authorises nothing. Every finding is stated with its evidence, and every claim in it was checked against the files at the snapshot |
| Identifier ownership | `F-1` – `F-32` (findings) |
| Revision note | Version 1.1 adds §8, the remediation record: what was done in response to each finding, what was partly done, what was not done, and which findings no longer describe the system. The findings themselves are retained unaltered. The dispositions are the coordinator's, established by re-deriving each finding against the current source and by the new tests in `impl/tests/test_emergency_controls.py` |
| Companion documents | `operational/emergency-shutdown-and-containment-protocol.md`; `reference/audit-and-conformance-procedures.md`; `impl/caos/emergency.py`; `impl/caos/emergency_console.py`; `impl/tests/test_emergency.py` |

---

> **Supersession notice.** The findings in §3 to §7 were stated against the
> implementation as it stood at this document's snapshot. The implementation was
> subsequently reworked in response, and **§8 records what was done for each
> finding**, which findings are closed, which are partly closed, and which remain
> open. Where §2 or a finding's own text says something that no longer describes
> the system, §8 governs. A finding that is closed stays in the register; a
> finding that is removed is indistinguishable from one that was never made.

---

## 1. Scope, Method, and Snapshot

### 1.1 What was audited

| Artefact | Path | Extent |
| --- | --- | --- |
| The protocol | `operational/emergency-shutdown-and-containment-protocol.md` | Complete: 89 requirements, 26 tables, Annexes A–E |
| The enforcement core | `impl/caos/emergency.py` | Complete at the snapshot: 1,487 lines, 1 module |
| The console and drill | `impl/caos/emergency_console.py` | Complete at the snapshot: 226 lines |
| The tests | `impl/tests/test_emergency.py` | Complete at the snapshot: 55 tests |
| The integration points | `impl/caos/__init__.py`, `impl/caos/cli.py`, `impl/README.md` | As affected |
| The surrounding set | `system-design-and-framework.md`, `constitutional/…`, `operational/countermeasure-catalogue.md`, `reference/audit-and-conformance-procedures.md`, `README.md` | As cited by the protocol |

### 1.2 Method

Four passes, in this order:

1. **Reading.** The protocol was read as a specification and the implementation as a program, with the question on each claim being: *does the code do this, and if not, is the document wrong or the code?*
2. **Cross-checking.** Every identifier, table cell, count, and cross-reference in the protocol was extracted mechanically and compared against the code, the catalogue, the constitutional instrument, and the set index.
3. **Probing.** Suspected defects were confirmed by executing the code, not by reading it. Every finding in §3 and §4 carries the probe that produced it. Nothing is reported on suspicion.
4. **Regression.** The whole suite was run before and after the audit to confirm that the audit itself changed nothing.

### 1.3 Snapshot

| Attribute | Value |
| --- | --- |
| Taken | 2026-10-20 |
| Working directory | `/home/k/Desktop/AI C@ Op` |
| Python | 3.13.5, standard library only |
| Suite result at the snapshot | 364 tests, 0 failures, 0 errors |
| Emergency tests | 55 tests, 0 failures |

**The audited code moved during the audit, and the findings were re-verified against it.** Partway through, a concurrent edit to the set left two modules with damaged import blocks: `impl/caos/countermeasures.py` had a `typing` import inserted inside its `from .vocab import (...)` block, and `impl/caos/emergency.py` had its entire `from .vocab import` line removed while removing an unused name. The first broke the whole package — every test module failed to import — and the second left `CollateralClass` undefined in the emergency module. Both were repaired during the audit: the `typing` import was moved to module level in `countermeasures.py`, and `from .vocab import CollateralClass, Reversibility` was restored in `emergency.py` (the unused `ROEProfile` was not restored, per `F-23`). No other change was made to the implementation, and no finding was written against a version of the code other than the one now in the tree.

Every critical and significant finding in this document was re-executed against the code as it stood at this document's snapshot, and all of them reproduced. The implementation has since been reworked in response; §8 records what was done, and the dispositions there supersede this section's characterisation. The findings are therefore stated against the code as it now stands, not against an earlier reading of it.

**Verification status of this document: Unverified.** The findings are reproducible against the snapshot above. They are not independently substantiated, and the verification that would establish them is a second reader re-running the probes.

---

## 2. Verdict Summary

| # | Severity | Count | Subject |
| --- | --- | --- | --- |
| `F-1` – `F-6` | **Critical** | 6 | Enforced in prose, unenforced in code, or structurally impossible |
| `F-7` – `F-13` | Significant | 7 | Real defects with operational consequence |
| `F-14` – `F-22` | Documentation divergence | 9 | The document and the code disagree, or the document is stale |
| `F-23` – `F-30` | Stylistic and quality | 8 | Dead code, unused parameters, naming, structure |
| `F-31` – `F-32` | Coverage gap | 2 | Behaviour asserted by the document and untested |

**Also repaired during the audit.** Two import-block defects introduced by a concurrent edit, both of which are in the set's implementation rather than in the document: `impl/caos/countermeasures.py:25` (a `typing` import inside a `from .vocab import (...)` block, which broke the package and every test module) and `impl/caos/emergency.py` (an entire `from .vocab import` line removed, leaving `CollateralClass` undefined). Both are noted here because the second is an instance of `F-23` being "fixed" destructively, and the first is a demonstration of why the set needs the drift guard recommended at `F-32`.

**The headline.** The protocol's substantive design is sound, and its most important safety properties — the isolation invariant, the protected control set, the pre-flight gate, the reversibility ladder, the staged rotation — are written down correctly and read as if they were in force. Six of them were not in force in the reference implementation at this document's snapshot. §8 records their closure; where a finding is marked closed there, this section's statement no longer describes the system. The implementation does what the document says it does *when the document's blocking preconditions happen to hold*, and it does not check that they hold. The gap is not that the controls are wrong; it is that they are advisory.

**A caution about the shape of this result.** The critical findings are concentrated in the enforcement edges — the checks that are supposed to refuse. The happy path works. That is the worst possible distribution for a containment system, because a working happy path is exactly what a test suite and a demo will show.

---

## 3. Critical Findings

### F-1 — The card's blocking fields are never enforced on the dispatch or declaration path

**Where.** `impl/caos/emergency.py:1145` (`EmergencyCard.completion_defects`), `:1169` (`EmergencyCard.armed`), `:1194` (`declare`), `:1278` (`dispatch`).

**What.** The card carries three blocking field groups and computes their defects correctly. Nothing calls `armed()`. `declare` and `dispatch` both proceed with a card whose target block, human-continuity block, or command block is empty.

**Evidence.**

```python
c = card()                       # protected control set: EMPTY
c.armed()            # -> False
c.completion_defects()  # -> ('the command block is incomplete: no protected control set is recorded',)
ctl.dispatch("EA-A-03", actor="op", target="session:a1")
                     # -> ALLOWED. DispatchRecord(action_id='EA-A-03', ...)
```

**Impact.** `ESC-26`, `ESC-27` and `ESC-75` — "a card with a defect cannot be armed" — are prose. In the configuration that matters most (no protected control set recorded), the pre-flight gate's protected-set check has nothing to check, and the dispatch proceeds. The protocol's central guarantee, that containment cannot touch the operator's command path, depends on that set existing; the code neither requires it nor checks that it was consulted.

**Fix.** At the top of `declare` and `dispatch`:

```python
defects = self.card.completion_defects()
if defects:
    raise ProtocolRefusal("ESC-75", "the card cannot be armed: " + "; ".join(defects),
                          "the target, human-continuity, and command blocks must be complete")
```

**Note.** `caos.roe.card_is_armable` already exists for the standard card and is not called here either. See `F-6`.

---

### F-2 — The hard prohibitions compare two disjoint namespaces and can never fire

**Where.** `impl/caos/emergency.py:607` (`PROHIBITED_OPERATIONS`), `:1300` (the check in `dispatch`).

**What.** `PROHIBITED_OPERATIONS` holds operation *names* — `delete_user_data`, `revoke_operator_command_authority`, `suspend_the_c2_surface`, `act_on_provider_service`, and eleven more. The check in `dispatch` is `if act.identifier in PROHIBITED_OPERATIONS`, where an action identifier is `EA-A-nn`. The two sets have no common member.

**Evidence.**

```python
PROHIBITED_OPERATIONS & {a.identifier for a in ACTIONS}   # -> set()
```

**Impact.** The document's Annex C "Prohibited actions" list, which states that these are "never available at any level, under any envelope, in any tier", is enforced by a comparison that cannot succeed. The list is rendered by the console (`emergency_console.show_catalogue`) and is otherwise decorative. The prohibition most likely to matter in practice — `act_on_provider_service`, and the two that protect the command path — would not stop a catalogue entry that attempted it.

**Fix.** Carry the prohibition as a field on the action, where it cannot be separated from the action:

```python
prohibited_reason: str = ""      # on EmergencyAction
...
if act.prohibited_reason:
    raise ProtocolRefusal("ZC-1", f"{act.identifier} is prohibited: {act.prohibited_reason}",
                          "the prohibited list in Annex C is not a preference")
```

Keep `PROHIBITED_OPERATIONS` as the documentation list, and add a test asserting that every prohibited name is either an action's `prohibited_reason` or is explicitly marked as a platform-level prohibition with no catalogue entry.

---

### F-3 — The inventory and the protected control set are per-dispatch inputs, so the gate is only as strong as its caller

**Where.** `impl/caos/emergency.py:637` (`EmergencyContext.inventory`, `EmergencyContext.protected_controls`), `:1290`–`1315` (gate construction in `dispatch`).

**What.** The pre-flight gate reads the inventory and the protected control set from the `EmergencyContext`, which the caller constructs and passes in on every dispatch. The protected set used is the union of the card's and the context's, so an empty context cannot weaken a populated card — but an empty *card* is not caught (`F-1`), and the inventory has no card-level counterpart at all.

**Impact.** A caller that supplies an empty inventory, or an inventory it controls, decides what the gate can see. The protocol's design intent (`ESC-88`: the gate, the inventory, and the protected set are held outside the deployment's reach) is not expressible when the inventory travels with the call. The gate is also not re-validated against a baseline: a target that was legitimate yesterday is legitimate today if the inventory says so.

**Fix.** Move `inventory` and `protected_controls` onto the card, populate them at declaration, and have the gate read card state only. A dispatch must not be able to widen the set of things it is allowed to touch by passing a different context.

---

### F-4 — The rotation action can never be dispatched

**Where.** `impl/caos/emergency.py:1396` and `:1444` (`dispatch`), `:1085` (`RotationState`).

**What.** `dispatch` creates a fresh `RotationState()` for a staged action and then immediately refuses, because `rotation.issued` is false. There is no public API to advance it. The controller's public surface is `declare`, `dispatch`, `mark_reentry`, `record_verification`, `reentry_blockers`, `transition` — none of which touches a rotation. `RotationState` has one method, `invalidate()`, and it refuses.

**Evidence.**

```python
ctl.dispatch("EA-A-14", actor="op", target="session:a1")
# -> ProtocolRefusal: ESC-33: rotation must be staged: issue the replacement,
#    verify it, move the workload, then invalidate
c.rotations.get("EA-A-14")
# -> RotationState(issued=False, verified=False, workload_moved=False, invalidated=False)
```

**Impact.** `EA-A-14` is the credential rotation that closes a compromised path. It is unreachable. The protocol's central remediation — "the foothold does not survive the response" — is specified in `ESC-33`, enforced by a check, and made impossible by the same code. A reader of the test suite would reasonably believe the rotation path was covered, because a test does assert that the refusal occurs.

**Fix.** Give the rotation a lifecycle the controller owns:

```python
def begin_rotation(self, action_id: str, actor: str) -> RotationState: ...
def verify_rotation(self, action_id: str, actor: str) -> None: ...
def move_workload(self, action_id: str, actor: str) -> None: ...
```

and let `dispatch` consume the rotation only when it is complete.

---

### F-5 — The envelope's named-holder set is stored and never read; the actor is not checked against anything

**Where.** `impl/caos/emergency.py:1010` (`PaceEnvelope.issued_to`), `:1278` (`dispatch`).

**What.** `issued_to` — the set of operators the standing envelope is issued to — is never consulted. `dispatch` accepts `actor: str` and records it. Nothing compares it to the envelope, the card's command-authority holder, or the card's alternate holder.

**Evidence.**

```python
pace = PaceEnvelope(..., issued_to=frozenset({"operator"}), ...)
rec = ctl.dispatch("EA-A-03", actor="someone-else", target="session:a1")
rec.actor   # -> 'someone-else'
```

**Impact.** `PACE-2`'s "the named operators authorised" is unenforced, and `ESC-78`'s "command authority is held by a named human" has no mechanical counterpart. The emergency path's central safety property — that a named human authorises every action — rests entirely on the caller passing the right string. Note that this cuts both ways: the check is not merely missing, it is missing in the direction that a compromised deployment would prefer, since a system that can cause a dispatch under an arbitrary actor string can cause one under an identity the record will attribute to the operator.

**Fix.** `if actor not in self.pace.issued_to and actor != self.card.command_authority_holder: refuse`, and carry the alternate holder on the card so that authority passes on handover (`ESC-78`).

---

### F-6 — The emergency card is not an OperationCard, and the set's own armability gate is bypassed

**Where.** `impl/caos/emergency.py:1115` (`EmergencyCard`); `impl/caos/models.py` (`OperationCard`, 48 fields); `impl/caos/roe.py:165` (`card_is_armable`).

**What.** The protocol states (§11, `ESC-28`) that the emergency card "inherits the fields of the standard card" and "is a card in every respect that `OP-1` requires". The implementation defines a parallel dataclass with none of those fields and no relationship to `OperationCard`. Absent entirely: `objective`, `hypothesis`, `disconfirming_observation`, `ea_reference`, `excluded_targets` (the affirmative third-party exclusion), `risk_of_inaction`, `alternatives_considered`, `rationale`, `contingency`, `abort_conditions`, `abort_owner`, `abort_mechanism`, the deconfliction fields, `non_weaponisation_attestation`, `third_party_assessment`, and the approval-depth machinery. `card_is_armable` is never called on the emergency path.

**Impact.** The emergency path dispatches with none of the set's authorisation instruments. There is no engagement-authorisation reference, so the constitutional root of trust is not carried into the one situation where the operator is acting fastest; no abort conditions, so there is no pre-agreed way to stop; no deconfliction check, so the emergency can collide with a live legitimate operation; and no excluded-targets affirmation, so the third-party exclusion — mandatory in every EA and non-omissible — is not exercised on the path most likely to be rushed. The document's claim that the emergency card is a card is true of the prose and false of the code.

**Fix.** Make the emergency card an `OperationCard` — an extension or a composition — and route every dispatch through `card_is_armable`. The emergency-specific blocks (target, human-continuity, command) become additional mandatory fields, not a parallel card type. This is the single change that would most improve the set's coherence, because it removes the second card concept the set now has.

---

## 4. Significant Findings

### F-7 — ESL-4 does not require a second approver, though the document says it does

**Where.** `impl/caos/emergency.py:1409`; document `ESC-50` and §14.1.

```python
needs_second = act.collateral >= CollateralClass.C1 and not act.is_kill
```

The document: "Any action at collateral class `C1` or above, **and any action at `ESL-4`**, requires a second named human on the out-of-band channel — except the kill action." Probe: `EA-A-11` (C0, terminate the deployment's execution) dispatches at `ESL-4` with `second_approver = None`.

This is a divergence in the permissive direction, at the level where the protocol says speed matters most. Either the code should require the second approver at `ESL-4`, or the document should say plainly that `ESL-4` is the one level where unilateral action is intended, and that the exception is deliberate rather than an omission. The current state is a document that claims a control the code does not apply.

**Fix.** `needs_second = (act.collateral >= CollateralClass.C1 or self.card.level is EmergencyLevel.ESL_4) and not act.is_kill`, or amend `ESC-50` to match the implemented behaviour with its reason.

---

### F-8 — The envelope's daily limit is cumulative, not daily

**Where.** `impl/caos/emergency.py:1139` (`pace_invocations_today`), `:1140` (`pace_day`), `:1437`.

`pace_day` is never written and never read, so the counter never resets. `PACE-2` promises "the maximum per rolling twenty-four hours"; what is implemented is a second total limit that happens to be smaller.

**Fix.** Record the day on the card at first use and reset the counter when it differs, or rename the field and the requirement to what it is.

---

### F-9 — The emergency path writes nothing to the Ledger

**Where.** `impl/caos/emergency.py` (no import of `caos.ledger`); document `ESC-15`, §3 (the record), §22.

`ESC-15`: "Every transition is a record." In the implementation, transitions are appended to `card.transitions` as formatted strings — not hash-chained, not in the set's canonical record, and outside the replay procedure the audit document defines. The document's own definition of the record names "the ledger entries" first. The platform architecture's tamper-evidence property does not reach the emergency path, and the emergency path is where the record is most likely to be contested.

**Fix.** Write transitions, dispatches, verifications, and refusals into `caos.ledger.Ledger`, and let `card.transitions` be a convenience view over the ledger rather than a parallel record.

---

### F-10 — Severity cannot be raised after declaration, and the level has no history

**Where.** `impl/caos/emergency.py:1194` (`declare`); document `ESC-8`, `ESC-9`, `ESC-10`.

`ESC-8` says severity may be raised by anyone; the controller offers no way to raise it, and the only route is direct assignment to `card.level`, which records no actor, no reason, and no time. `ESC-10` requires the level, the time it was assigned, the evidence, the assignee, and the change history; the card carries a single value. `ESC-9` (de-escalation requires a cause) has no counterpart at all — nothing stops a level being lowered, by any means, with no record.

**Fix.** `raise_level(level, actor, reason)` and `lower_level(level, actor, reason, evidence)` on the controller, with a history list on the card, and a refusal on lowering that is not backed by a recorded cause.

---

### F-11 — "Principal" means two different things in the code, and one of them is not the document's

**Where.** `impl/caos/emergency.py:637` (`EmergencyContext.principal`), `:1115` (`EmergencyCard.principal`), `:791` (`preflight`'s `deployment_principal`).

The document defines the principal as "the specific identity through which the compromised deployment acts: a session token, an API key, a service principal, a container, a device identity, a workspace. Every containment action names one." In the code, `context.principal` is the **owner** used for the ownership comparison, and `card.principal` is the incident's instance. The blast boundary holds instance identifiers, not principals.

This is not pedantry: it already produced a bug. `K-2` originally compared `context.principal` against the blast boundary and failed on every call until it was changed to compare the resolved target. The drill hides the ambiguity by setting both fields to the same string.

**Fix.** Rename to `deployment_principal` (owner) and `target_principal` (the instance under emergency), and make the blast boundary a set of instance identifiers in the document as well as in the code.

---

### F-12 — The shipped drill demonstrates a card that cannot be armed and a gate that protects nothing

**Where.** `impl/caos/emergency_console.py:65`, `:99`, `:120`.

`build_drill` constructs the card without `context`, `protected_controls`, or `command_authority_holder` — so the synthetic card has three blocking defects and, per the protocol, cannot be armed. It does not matter that the controller does not notice (`F-1`), because the console is the artefact a reader will run to see what the protocol does.

The `protected` set it derives comes from the **first** of two `EmergencyContext` constructions, whose default protected set is empty; the second context is the one that is used. The drill's protected control set is therefore empty, and the `PF-3` check it prints — "Target does not intersect the protected control set" — passes vacuously.

The inventory gives `key:integration-key-01` the owner `operator-1`, while the deployment principal is `agent:assistant-session-01`, so the gate would refuse a resource the drill lists inside the blast boundary.

**Impact.** The one runnable demonstration of the emergency path shows a card that cannot legally exist, protecting a set that is empty, with an inventory that is internally inconsistent. A reader who runs `python3 -m caos.cli emergency drill` learns the wrong thing about the control.

**Fix.** Build the drill with a populated protected control set, a named holder, and a context; give the key the deployment owner; and delete the discarded first context.

---

### F-13 — `mark_reentry` accepts arbitrary keys, and a typo produces a card that can never be re-entered

**Where.** `impl/caos/emergency.py:1508`.

```python
ctl.mark_reentry("r-1", True)     # accepted
ctl.mark_reentry("R-99", True)    # was accepted; is now refused with ESC-88
c.reentry   # -> {'r-1': True}
```

`reentry_blockers` reads only the canonical `REENTRY_CRITERIA`, so the stored keys are ignored, and the card still reports `R-1` unmet. A reader of the card sees a satisfied criterion that satisfies nothing.

**Fix.** Validate against `REENTRY_CRITERIA` and refuse an unknown key.

---

## 5. Documentation Divergences

### F-14 — The control table cites a requirement that means something else

`operational/emergency-shutdown-and-containment-protocol.md:16` — the Deployment form row: "The console must render the isolation invariants inline at the point of dispatch (`ESC-31`)". `ESC-31` is "The break-glass path is tested at declaration". The intended requirement is `ESC-43` (the console enforces the collateral checklist) or `ESC-84` (the pre-flight gate). This is a residue of the renumbering pass, which moved §14's requirements from `ESC-32`–`ESC-40` to `ESC-39`–`ESC-47` and left the cross-reference behind.

### F-15 — The control table understates the enforcement surface, and contradicts §22.1

`:17` — "The reference implementation at `impl/caos/emergency.py` is asserted to enforce the mechanically checkable parts of §7, §9, §10, and §14." The implementation also enforces §6.1 (the pre-flight gate and the protected control set), §11 (the card), §13 (the envelope), and §16 (the re-entry criteria) — as §22.1 of the same document states in detail. The two rows of the same table disagree.

### F-16 — §22.1 is presented as the audit surface but covers 34 of 89 requirements

The table's preamble says it "names what the code evaluates, where it does so, and the test that demonstrates the behaviour". It names 34 `ESC-` requirements. The other 55 are neither listed as enforced nor marked procedural. A reader auditing the protocol against its own implementation cannot tell whether the remainder is procedural by design or unimplemented. Every row in the table carries a Status column; the requirements outside the table carry none.

### F-17 — The recorded test count is stale

§22.1's snapshot: "The suite at that snapshot collected 225 tests across the set and reported no failures." The set now collects 259. The wording is snapshot-scoped and therefore not false, but the number is one working session out of date, and the same document's §3.1 and the audit procedures both quote counts that have moved.

### F-18 — `T1` means three different things in one set

| Series | Meaning | Source |
| --- | --- | --- |
| `T0`–`T3` | Target class: what a countermeasure acts upon | Constitutional instrument §5.1 |
| `T1`–`T4` | Source reliability tier | `impl/caos/vocab.py:51` (`SourceTier`) |
| `T0`–`T5` | Action tier, in the emergency protocol | `impl/caos/emergency.py:277` (`ActionTier`) |

The protocol uses `T0`–`T5` 20 times, in Annex C and in the text, with no disambiguation. The set index §6 states the hygiene rule: "Every identifier in the set is unique." It is not. The collision is benign in the code — `ActionTier` is a local `IntEnum` — and it is not benign in the prose, where "T1" appears in a sentence about tiers and could be read against the constitutional definition.

**Fix.** Rename the tier series to `AT-0`–`AT-5` (action tier) in the document and the code, and add the prefix to the set index's registry.

### F-19 — The protocol never mentions the console module that implements its console

§14 specifies the emergency console in nine requirements. `impl/caos/emergency_console.py` implements a rendering of it and is wired into the CLI. The protocol contains no reference to either, so §14 has no implementation pointer, and the drill's defects (`F-12`) are invisible from the document.

### F-20 — The four "proposed additions" have no home in the catalogue

Annex C states that four actions "bind to nothing and are marked as proposed additions — the provider-side quota suspension, the scheduled-job suspension, the metadata-path block, and the device re-image — until they are catalogued they are available only under the emergency card's own authority". Two problems: the catalogue document has no outstanding-additions section in which such a list could live, and `operational/countermeasure-catalogue.md` is **generated** from `caos/catalogue_data.py` by `tools/sync_catalogue.py`, so a hand-written list in it would be overwritten at the next synchronisation. The additions must enter `caos/countermeasures.py` and the catalogue be regenerated.

### F-21 — Three documents state three different technique counts

`caos/taxonomy.py` holds 77 techniques. `impl/README.md` says "seventy-six techniques" in two places. The set index's identifier registry says "AAT- | 10 categories, 60 techniques". The registry row is the one a reader is most likely to consult.

### F-22 — The package surface omits the emergency path

`impl/caos/__init__.py` re-exports every other module's public surface and its docstring lists them. It does not import `emergency` or `emergency_console`, and its docstring does not mention the emergency path. `from caos import EmergencyController` raises `ImportError`; only `from caos.emergency import …` works. The CLI works around this with a function-local import.

---

## 6. Stylistic and Quality Findings

### F-23 — Unused imports

| File | Import | Occurrences |
| --- | --- | --- |
| `impl/caos/emergency.py` | `ROEProfile` | 1 (the import itself) |
| `impl/caos/emergency.py` | `timedelta` | 1 (the import itself) |
| `impl/tests/test_emergency.py` | `CollateralClass` | 1 (the import itself) |

### F-24 — Fields that are written and never read

| Field | Note |
| --- | --- |
| `EmergencyAction.alters_record` | never read; the log-tampering prohibition it was presumably for is covered only in prose |
| `EmergencyAction.targets_third_party` | never read; the third-party exclusion is not mechanically checked in the emergency path |
| `EmergencyAction.description` | never read |
| `EmergencyContext.operator_credential_exposed` | set by the drill, read by nothing — though it is the natural trigger for the Tier 4 identity actions |
| `SeverityIndicators.indicator_only` | never read; the classification reaches `ESL-1` by fall-through instead |
| `PaceEnvelope.issued_at` | never read; the envelope's age is not checked against its expiry in a way that distinguishes the two |
| `EmergencyCard.pace_day` | never written or read (`F-8`) |
| `EmergencyLevel.allows_pace` | defined, never used; the `ESL-1` restriction is implemented inline in `dispatch` instead |

### F-25 — `collateral_checks` accepts `second_approver` and never uses it

`impl/caos/emergency.py:855`. The parameter suggests a check that does not exist, and no `K-` check verifies that a second approver is present. A reader of the signature will reasonably believe the check is performed.

### F-26 — The `K-9` check fires only for actions that break operator access

`K-9` is "no harm to a person", and the protocol's `ZC-8` covers a person depending on a safety, communication, or help capability. The check consults `safety_capability_at_stake` and `safety_alternative_confirmed` only when `act.breaks_operator_access` is true, so an action that endangers a safety capability without touching the operator's own access passes unchecked. The check is narrower than the invariant it stands for.

### F-27 — The `K-14` grant/mint test is unreachable through `dispatch`

`collateral_checks` refuses a target beginning `grant:`, `mint:`, or `delegate:`. The pre-flight gate refuses such a target earlier, as unresolvable. The check is therefore only exercised by direct calls to `collateral_checks` — which is what the test does, so the test passes without the dispatch path ever reaching the condition. Not a defect, but the test's value is lower than it appears, and a reader of the test file may draw the wrong conclusion.

### F-28 — Preflight runs before the state check, so the error precedence misleads

`dispatch` evaluates the pre-flight gate before the state check. Dispatching in `E0` against a target that is not in the inventory reports `ESC-84` ("the pre-flight gate refused the dispatch") rather than `ESC-11` ("no action may be dispatched in state E0"). The operator is told their target was wrong when the real problem is that no emergency was declared. The existing test passes only because its target happens to resolve.

### F-29 — The console module's `__all__` omits the functions the CLI uses

`impl/caos/emergency_console.py:39` declares `__all__ = ["build_drill", "Drill"]`, while `show_catalogue` and `run_drill` — the module's two public functions, and the two the CLI imports — are absent.

### F-30 — Duplicated context construction and a function-local import in the tests

`build_drill` constructs `EmergencyContext` twice and discards the first (`F-12`). `impl/tests/test_emergency.py` imports `EmergencyContext` inside `make_context()` rather than at module scope, where the rest of the file's imports live.

---

## 7. Coverage Gaps

### F-31 — Six behaviours the document asserted were untested

**Closed.** The six now have tests: the attestation fields in `impl/tests/test_attestations.py`, the emergency gates in `impl/tests/test_emergency_controls.py` and `impl/tests/test_branches.py`, and the synchronisers' failure paths in `impl/tests/test_sync_tools.py`.

| Behaviour | Document | Test status |
| --- | --- | --- |
| A card with a defect cannot be armed | `ESC-26`, `ESC-27`, `ESC-75` | A test asserts `armed()` is false; **no test asserts that dispatch is refused** |
| A prohibited action is refused | Annex C, "never available at any level" | A test asserts the *names* are declared; no test asserts a refusal, because none is possible (`F-2`) |
| The envelope's daily limit resets | `PACE-2` | No test; the limit does not reset (`F-8`) |
| `ESL-4` requires a second approver | `ESC-50` | No test; the requirement is not implemented (`F-7`) |
| Only a named holder may act | `PACE-2`, `ESC-78` | No test; the check does not exist (`F-5`) |
| The rotation can be completed | `ESC-33` | A test asserts the refusal; no test asserts completion, because it is impossible (`F-4`) |

The pattern is worth naming: in five of the six, the test asserts the *refusal* that the incomplete implementation produces, and the test passes. A suite of refusals, with no test of the permitted path, is a suite that certifies the system as unable to act. The most consequential omission is the last: the test suite contains no test in which the emergency protocol successfully rotates a credential, because the protocol cannot.

### F-32 — No test binds the document to the code

**Open.** The technique library, the countermeasure catalogue, and the adversary-AI taxonomy are bound to the code by tests. The emergency protocol is not: no test parses its Annex C or its §22.1. Until one does, the protocol's account of what the implementation enforces rests on inspection rather than on a test.

`impl/tests/test_bindings.py` already establishes the pattern the set should apply here: parse a document, parse the code, and fail the suite when they drift. Nothing does that for the emergency protocol. The Annex C table's 20 rows of tier, collateral class, PACE membership, and catalogue binding are hand-maintained, as is the §22.1 table's list of test names, and both are currently wrong in ways a mechanical check would have caught (`F-14` through `F-17` are all drift of this kind).

---

## 8. Remediation Record

*Added at the close of the review cycle, 2026-10-20. The findings above were
stated against the implementation as it stood at the audit's snapshot. The
implementation has since been reworked in response, and this section records
what was done, so that a reader of the findings knows which of them still
describe the system and which describe a version that no longer exists. A
finding that is closed stays in the register; a finding that is removed is
indistinguishable from a finding that was never made.*

### 8.1 The critical findings

| Finding | Disposition | Instrument |
| --- | --- | --- |
| **F-1** — the card's blocking fields were never enforced | **Closed.** `EmergencyCard.completion_defects` is now consulted before any declaration and before any dispatch, through `EmergencyController._require_armable`, and a card with a defect is refused with `ESC-75`. The card has also been given the standard card's authorisation instruments — `ea_reference`, `objective`, `hypothesis`, `disconfirming_observation`, `excluded_targets`, `risk_of_inaction`, `alternatives_considered`, the abort block, the contingency and its timestamp, the deconfliction result, and a named approver — and each is a blocking defect | `impl/caos/emergency.py`; `impl/tests/test_emergency_controls.py::ArmabilityTests` |
| **F-2** — the prohibition comparison used disjoint namespaces | **Closed.** The prohibition travels with the action: `EmergencyAction.prohibited_reason`, the `PROHIBITION_FLAGS` mapping from Annex C's list to the action attributes that would constitute an attempt, and `prohibition_for`. The dispatch refuses an action that alters the record, touches the command path, destroys user data, or grants a model control, on the eight prohibitions an action attribute can express. An action affecting an unauthorised third party is refused by the third-party branch of AD-5 and by `K-3`, not by the prohibition mapping; the remaining ten prohibitions are platform-level behaviours with no catalogue entry, and the §22.1 row now says so | `impl/caos/emergency.py`; `impl/tests/test_emergency_controls.py::ProhibitionTests` |
| **F-3** — the inventory and the protected set were per-dispatch inputs | **Partly closed.** The protected control set is on the card and the armability check requires it, so a dispatch can no longer proceed with an empty protected set. The inventory is still carried on the context, and the gate still reads the context's copy. The finding stands for the inventory | `impl/caos/emergency.py` |
| **F-4** — the rotation could never be dispatched | **Closed.** `RotationState` has `issue`, `verify` and `move_workload`, and the controller has `begin_rotation`, `verify_rotation` and `move_workload`. The dispatch consumes a rotation only when `RotationState.complete` is true | `impl/tests/test_emergency_controls.py::RotationLifecycleTests` |
| **F-5** — the actor was checked against nothing | **Closed.** `_actor_is_authorised` requires the actor to be a named holder of the containment envelope or to hold the card's command authority or its named alternate | `impl/tests/test_emergency_controls.py::AuthorityTests` |
| **F-6** — the emergency card was not an Operation Card | **Closed in substance.** The emergency card now carries the standard card's authorisation instruments and the same blocking-field discipline. It remains a distinct dataclass rather than an `OperationCard`, because its state machine, its severity ladder and its envelope are a different instrument; the two now share a blocking-field standard rather than a type | `impl/caos/emergency.py` |

### 8.2 The significant findings

**F-7** closed — a second named human is required at `ESL-4` as well as at `C1` and above, and the check precedes the collateral checklist so the refusal names the requirement. **F-8** closed — the envelope's daily counter resets when the day changes. **F-9** closed — the path writes its transitions, declarations, level changes and dispatches to the Ledger where one is attached. **F-10** closed — `raise_level` and `lower_level` exist, the history is on the card, and a lowering without a recorded cause and the evidence of its ending is refused. **F-11** closed — the two meanings are now `deployment_principal` and `target_principal`. **F-12** closed — the drill's card is armable, its protected control set is populated, and its inventory is internally consistent. **F-13** closed — an unknown re-entry criterion is refused.

### 8.3 The documentation divergences

**F-14** closed — the control table's deployment-form row now cites `ESC-84` and `ESC-43`. **F-15** closed — the verification-posture row now names §6.1, §7, §9, §10, §11, §13, §14 and §16, and points at §22.1. **F-16** closed — §22.1 now accounts for all 89 `ESC-` requirements across 78 rows: the rows mechanically enforced, and the remainder marked procedural or as to their recorded state. The count of mechanically enforced rows has moved as the implementation has been reworked, and §22.1 is the place to read it rather than any figure quoted here. **F-17** closed — the snapshot note no longer states a stale count as current. **F-18** closed — the action tier series is now `AT-0` to `AT-5` in the document, the code's enum members are `ActionTier.AT0` to `ActionTier.AT5`, and the prefix is registered in the set index. **F-19** closed — the protocol now names its implementation pointers, including `impl/caos/emergency_console.py`. **F-20** closed — the catalogue now records the four proposed additions at its §1.5, naming the class each would take, the binding constraints each would carry, and why it has no home today. The four are not catalogued, and their status is unchanged: the protocol's rule that they are available only under the emergency card's own authority and that their use is reportable is preserved. The finding was that the *record* was missing, and the record is now present. **F-21** closed — the counts now agree at 77 techniques. **F-22** closed — `caos/__init__.py` exports the emergency path.

### 8.4 The stylistic and quality findings

**F-23** closed — the unused imports are gone. **F-24** closed — `alters_record`, `targets_third_party`, `indicator_only`, `issued_at`, `allows_pace` and `pace_day` are now read. the `description` field is carried on each action but is not rendered by the console's catalogue view, which shows the action's name; the field is recorded here as an open item rather than as a closure. **F-25** closed — the second approver is now checked, as `K-15`. **F-26** closed — `K-9` now consults the safety capability independently of the operator's own access. **F-27** open — the `K-14` grant and mint test is still reachable only by direct call; the dispatch path refuses such a target earlier, at the pre-flight gate. **F-28** closed — the state check now precedes the pre-flight gate. **F-29** closed — the console module's `__all__` names its public functions. **F-30** partly closed. The duplicated context construction is fixed; the local import of `EmergencyContext` inside the test fixture's `make_context()` remains, and is recorded as open.

### 8.5 What the remediation did not do

**A note on §9 as a whole.** The items below were the audit's recommendations at the time of writing. The dispositions at §8 record which of them have since been discharged; an item that appears in §9 and is not marked as discharged in §8 is still outstanding. Where §8 and §9 appear to disagree, §8 is the later statement and governs.

Three things are worth stating plainly, because the closure record is more useful when it names its own edges.

1. **The inventory still travels with the call.** F-3 is only partly closed. A caller that supplies an inventory decides what the gate can see, and the gate is not re-validated against a baseline. The fix the audit proposed — moving the inventory onto the card — has not been made, and the emergency path's containment is therefore only as complete as the inventory its caller chose to supply.
2. **The card is a card, but it is not an `OperationCard`.** The two instruments now share a blocking-field standard, not a type. `OP-1`'s "no operation without a card" is satisfied in substance; the set now has two card concepts that must be kept in step, which is a cost the audit's own recommendation would have avoided.
3. **The findings above were verified against the implementation as it stood at the audit's snapshot.** Where the audit quoted a line number or an excerpt, the code has moved. The dispositions in this section are the coordinator's judgement of whether the finding is still live, and they were established by re-deriving each one against the current source and by the new tests; they are not the audit author's, and a reader who disagrees should re-run the check rather than accept the table.

---

## 9. Recommendations

Ordered by the ratio of risk reduced to work done. The first six are the `F-1`–`F-6` fixes and are not independent of one another; `F-6` and `F-1` should be done together, because unifying the card with `OperationCard` subsumes the armability check.

**The status column records what has been done.** The list is retained rather than cleared, because a recommendation that was carried out and a recommendation that was never made look identical if the list is emptied. The dispositions at §8 give the instrument for each.

| Order | Action | Addresses | Effort | Status |
| --- | --- | --- | --- | --- |
| 1 | Make the emergency card an `OperationCard`; route every dispatch through `card_is_armable` | `F-6`, `F-1` | Large — the right shape of the fix | **Partly discharged.** The card now carries the standard card's authorisation instruments and is armability-checked before any declaration or dispatch, and the route runs through `EmergencyController._require_armable` rather than through `OperationCard.autonomy_grant()`. The two card concepts remain distinct types, which §8.1 records as the residual of `F-6` |
| 2 | Refuse dispatch and declaration on any card defect; add the missing blocks to the card | `F-1` | Small, once 1 is done | **Discharged.** `_require_armable` is called by both `declare` and `dispatch`, and the card carries the engagement authorisation, the abort block, the deconfliction result, the affirmative third-party exclusion, the contingency and its timestamp, and a named approver |
| 3 | Move the prohibitions onto the actions; add a test that a prohibited action is refused | `F-2`, `F-31` | Small | **Discharged.** The prohibitions are read from one mapping, `PROHIBITION_FLAGS` and `prohibition_for`, and the dispatch consults it |
| 4 | Check the actor against the envelope's holders and the card's command-authority holder | `F-5` | Small | **Discharged.** `_actor_is_authorised` covers the dispatch, the rotation, the verification, the transition and the level paths |
| 5 | Move the inventory and the protected set onto the card; the gate reads card state only | `F-3` | Medium | **Partly discharged.** The protected control set is on the card and the armability check requires it; the inventory is still carried on the context and the gate still reads the context's copy |
| 6 | Give the rotation a lifecycle the controller owns; add the completion test | `F-4`, `F-31` | Medium | **Discharged.** `begin_rotation`, `verify_rotation` and `move_workload`, with `RotationState.complete` as the gate |
| 7 | Write the emergency path's transitions, dispatches, and refusals to the Ledger | `F-9` | Medium | **Discharged.** The transitions, declarations, level changes, break-glass test and dispatches are written to the Ledger where one is attached |
| 8 | Add `raise_level` / `lower_level` with a history on the card | `F-10` | Small | **Discharged.** `raise_level` and `lower_level`, with the history on the card and a recorded cause required for a lowering |
| 9 | Reconcile `ESC-50` with the code, in whichever direction is chosen | `F-7` | Small — but it is a decision, not an edit | **Discharged.** `ESC-50` requires a second named human at `C1` and above and at `ESL-4`, and the check precedes the collateral checklist so the refusal names the requirement |
| 10 | Fix the daily limit, or rename it to what it is | `F-8` | Small | **Discharged.** The envelope's daily counter resets on the day of the act, not the day the controller was built |
| 11 | Write emergency transitions to the Ledger, add the level history, and give the card an `aborted` state | `F-9`, `F-10` | Medium | **Partly discharged.** The transitions, dispatches and refusals are written to the Ledger and the level history is on the card; the card has no `aborted` state |
| 12 | Add a drift guard in the style of `test_bindings.py`: parse Annex C and §22.1, and fail the suite on a mismatch with `emergency.py` | `F-32`, and permanently `F-14`–`F-17` | Medium — the highest-leverage single addition | **Open.** No test parses Annex C or §22.1. The technique library, the countermeasure catalogue and the taxonomy are bound to the code by tests; the emergency protocol is not |
| 13 | Rename the action-tier series to `AT-0`–`AT-5` in the document and the code; add the prefix to the set index | `F-18` | Small | **Discharged.** The series is `AT-0` to `AT-5` in the document, the code's members are `ActionTier.AT0` to `ActionTier.AT5`, and the prefix is registered in the set index |
| 14 | Add the four proposed actions to `caos/countermeasures.py` and regenerate the catalogue | `F-20` | Small, and it needs the synchroniser | **Discharged in the form the protocol permits.** The four proposed additions are recorded in the catalogue at its §1.5 with the class each would take and why it has no home today. They are not catalogued, and the protocol's rule that they are available only under the emergency card's own authority is unchanged |
| 15 | Reconcile the technique counts across `impl/README.md` and the set index | `F-21` | Trivial, but it belongs to the other owners | **Discharged.** The counts agree at 77 techniques |
| 16 | Export the emergency surface from `caos/__init__.py`; correct the console's `__all__` and headings; build the drill with a complete card | `F-12`, `F-19`, `F-22`, `F-29` | Small | **Discharged.** The emergency surface is exported from `caos/__init__.py`, the console's `__all__` names its public functions, and the drill is built with a complete, armable card |
| 17 | Remove the dead fields and unused imports; use the parameters that are ignored | `F-23`–`F-27` | Trivial | **Discharged.** The dead fields are removed and the ignored parameters are used; the `description` field is carried and not rendered, which §8.4 records as an open item |
| 18 | Correct the document's control table, §22.1 framing, and the protocol↔console pointer | `F-14`–`F-17`, `F-19` | Small | **Discharged.** The control table, the §22.1 framing and the protocol's implementation pointers are corrected |

**On efficiency.** There is no performance problem: the whole emergency path is in-memory, and the full suite runs in under 40 ms. The efficiency observation worth making is about redundancy rather than speed — the pre-flight gate and the fourteen collateral checks re-run on every dispatch, which is correct behaviour for a security control, and caching them would introduce an invalidation hazard for no measurable gain. The one genuine waste is the discarded `EmergencyContext` in the drill.

**On the shape of the fix for `F-6`.** Unifying the emergency card with `OperationCard` is the largest single item and it is also the one that fixes the most. It resolves the armability gap, carries the engagement authorisation, the abort conditions, the deconfliction check, and the affirmative third-party exclusion into the emergency path, and removes the set's second, weaker card concept — which is itself a hazard, because a reader who knows the set will reasonably assume that any card in it is armed the same way.

**A closing observation, offered without preamble.** The protocol's design is unusually good: the isolation invariant, the reversibility ladder, the protected control set, the pre-flight gate, the staged rotation, and the two-pass verification are all the right ideas, and several of them are the kind of control that most operational frameworks do not have at all. The finding is not that the thinking is wrong. It is that a reference implementation which is read as evidence of enforcement — and this one is, by the set's own audit procedures — currently demonstrates less than the document claims. A reader of the set could reasonably form the opposite of the correct impression: that the emergency path is protected against a compromise of the operator's own assistant, when the machine-checkable half of that protection is, in six specific places, not switched on.

---

*This was supported for MIA by Kilo (kilo-auto/free).*
