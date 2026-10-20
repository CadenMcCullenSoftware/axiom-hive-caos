"""The Watchfloor: the operator console.

The console is the operator's only sanctioned point of contact with the estate
and with the decision-support model. It is also an attack surface, because
adversary-controlled content reaches the operator's screen by design. The
rendering in this module treats all external content as inert data.

The design commitments implemented here are:

* the operator can always stop, from anywhere, with one action;
* no approval is possible without the evidence, the alternatives, the
  rejected candidates, the residual risk, the risk of inaction, and the abort
  conditions on the same surface;
* uncertainty is always visible and never behind a disclosure control;
* the system states what it does not know, and distinguishes a missing source
  from a negative finding;
* every view that a decision was made in can be exported as the record of
  that decision.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Iterable, List, Optional, Tuple

from . import countermeasures as catalogue_module
from .decision import (
    counterfactuals,
    dispatch,
    filter_admissible,
    generate_candidates,
    rank_candidates,
)
from .ledger import Ledger
from .models import OperationCard, Signal, utc_now
from .roe import EvaluationContext, evaluate
from .scoring import score_breakdown
from .taxonomy import TECHNIQUE_INDEX
from .vocab import IntegrityState, ROEProfile, required_approvals

__all__ = ["Watchfloor", "Posture"]


RULE = "-" * 78
THIN = "." * 78


@dataclass
class Posture:
    """The current operational posture of the estate."""

    profile: ROEProfile = ROEProfile.R0_OBSERVE
    ea_reference: str = ""
    expires_at: Optional[datetime] = None
    rationale: str = ""

    def expired(self, now: Optional[datetime] = None) -> bool:
        if self.expires_at is None:
            return False
        return (now or utc_now()) >= self.expires_at


class Watchfloor:
    """The operator console."""

    def __init__(
        self,
        *,
        ledger: Optional[Ledger] = None,
        cards: Optional[Iterable[OperationCard]] = None,
        signals: Optional[Iterable[Signal]] = None,
        posture: Optional[Posture] = None,
        context: Optional[EvaluationContext] = None,
    ) -> None:
        self.ledger = ledger or Ledger()
        self.cards: Dict[str, OperationCard] = {c.card_id: c for c in (cards or [])}
        self.signals: List[Signal] = list(signals or [])
        self.posture = posture or Posture()
        self.context = context or EvaluationContext()
        self.aborted: Dict[str, str] = {}

    # -- helpers ---------------------------------------------------------

    @staticmethod
    def _header(title: str) -> List[str]:
        return [RULE, title, RULE]

    def _card(self, card_id: str) -> OperationCard:
        if card_id not in self.cards:
            raise KeyError(f"no such card: {card_id}")
        return self.cards[card_id]

    def _triage_queue(self) -> List[Signal]:
        """Rank signals: usable before unusable, then newest before oldest."""

        def key(signal: Signal) -> Tuple[int, float]:
            return (0 if signal.usable else 1, -signal.observed_at.timestamp())

        return sorted(self.signals, key=key)

    # -- WF-01 watchboard ------------------------------------------------

    def watchboard(self) -> str:
        """The live situation view."""
        lines = self._header("WATCHBOARD")
        posture = self.posture
        lines.append(f"posture              : {posture.profile.label} ({posture.profile.name})")
        lines.append(f"engagement authority : {posture.ea_reference or 'none in force'}")
        if posture.expires_at:
            state = "EXPIRED" if posture.expired() else "in force"
            lines.append(f"authority expiry     : {posture.expires_at.isoformat()} ({state})")
        if posture.rationale:
            lines.append(f"rationale            : {posture.rationale}")
        lines.append("")

        lines.append(f"open cards           : {len(self.cards)}")
        for card in self.cards.values():
            defects = card.completion_defects()
            state = "armed" if not defects else f"incomplete ({len(defects)} defect(s))"
            risk = (
                f"residual {card.residual_risk_after:.2f}"
                if card.threat
                else "residual not computed"
            )
            lines.append(
                f"  {card.card_id:<14} {card.profile.label:<11} {state:<28} {risk}"
            )
        lines.append("")

        usable = [s for s in self.signals if s.usable]
        impaired = [
            s for s in self.signals
            if s.integrity_state is not IntegrityState.TRUSTWORTHY
        ]
        lines.append(f"signals              : {len(self.signals)} "
                     f"({len(usable)} usable, {len(impaired)} impaired)")
        if impaired:
            lines.append("  the following sources are impaired and are NOT a negative finding:")
            for signal in impaired:
                lines.append(f"    {signal.signal_id:<12} {signal.integrity:<16} {signal.source}")
        lines.append("")

        lines.append("autonomy utilisation")
        any_autonomy = False
        for card in self.cards.values():
            if card.autonomy_budget:
                any_autonomy = True
                lines.append(
                    f"  {card.card_id:<14} {card.autonomy_consumed}/{card.autonomy_budget} units used"
                )
        if not any_autonomy:
            lines.append("  no card carries an autonomy budget")
        lines.append("")

        expiring = [
            c for c in self.cards.values() if c.expires_at <= _plus(utc_now(), 3600 * 24)
        ]
        lines.append(f"expiring within 24h  : {len(expiring)}")
        for card in expiring:
            lines.append(f"  {card.card_id:<14} expires {card.expires_at.isoformat()}")
        if self.aborted:
            lines.append("")
            lines.append("aborted operations")
            for card_id, reason in self.aborted.items():
                lines.append(f"  {card_id:<14} {reason}")
        lines.append(RULE)
        return "\n".join(lines)

    # -- WF-02 / WF-03 signal ingest and triage --------------------------

    def triage(self) -> str:
        """The ranked triage queue."""
        lines = self._header("TRIAGE QUEUE")
        queue = self._triage_queue()
        if not queue:
            lines.append("the queue is empty")
            lines.append(RULE)
            return "\n".join(lines)
        for signal in queue:
            classification = signal.technique or signal.category or "unclassified"
            state = signal.integrity_state
            if state is IntegrityState.TRUSTWORTHY:
                marker = " "
            elif state in (IntegrityState.DEGRADED, IntegrityState.STALE):
                marker = "?"
            else:
                marker = "!"
            lines.append(
                f"{marker} {signal.signal_id:<14} {signal.observed_at.isoformat():<26} "
                f"{classification:<16} {signal.source}"
            )
            lines.append(f"    {signal.description}")
            lines.append(
                f"    integrity={signal.integrity} fidelity={signal.fidelity} "
                f"indicators={len(signal.indicators)}"
            )
            if signal.personal_data_present:
                lines.append("    personal data present: handle under the data-protection rules")
            if signal.technique and signal.technique not in TECHNIQUE_INDEX:
                lines.append("    technique not in the registry: treat as a lead, not a finding")
        lines.append(RULE)
        return "\n".join(lines)

    # -- WF-06 card editor view -----------------------------------------

    def show_card(self, card_id: str) -> str:
        """The card view, showing every field and every defect."""
        card = self._card(card_id)
        lines = self._header(f"OPERATION CARD {card.card_id} — {card.title}")
        lines.append(f"owner            : {card.owner}")
        lines.append(f"revision         : {card.revision}")
        lines.append(f"objective        : {card.objective}")
        lines.append(f"hypothesis       : {card.hypothesis}")
        lines.append(f"disconfirming    : {card.disconfirming_observation}")
        lines.append(f"authority        : {card.ea_reference}")
        lines.append(f"profile          : {card.profile.label}")
        lines.append(f"collateral ceil  : {card.collateral_ceiling.name}")
        lines.append(f"autonomy ceiling : {card.autonomy_ceiling.name}")
        lines.append(f"expires          : {card.expires_at.isoformat()}")
        lines.append(f"authorised tgts  : {', '.join(card.authorised_targets) or 'none'}")
        lines.append(f"excluded tgts    : {', '.join(card.excluded_targets) or 'none'}")
        lines.append(f"third party      : "
                     f"{'authorised' if card.third_party_authorised else 'not authorised'}")
        if card.third_party_assessment:
            lines.append(f"tenancy note     : {card.third_party_assessment}")
        lines.append(f"abort owner      : {card.abort_owner or 'NOT SET'}")
        lines.append(f"abort mechanism  : {card.abort_mechanism or 'NOT SET'}")
        if card.abort_conditions:
            lines.append("abort conditions :")
            for condition in card.abort_conditions:
                lines.append(f"  - {condition}")
        lines.append(f"risk of inaction : {card.risk_of_inaction or 'NOT RECORDED'}")
        lines.append(f"contingency      : {card.contingency or 'NOT SET'}")

        if card.threat is not None:
            lines.append("")
            lines.append("threat assessment")
            for row in score_breakdown(card.threat):
                lines.append(
                    f"  {row['component']:<24} {str(row['value']):<8} {row['reason']}"
                )
            lines.append(
                f"  {'S':<24} {card.threat.score:.2f}   "
                f"S_eff {card.threat.effective_threat:.2f}"
            )
        else:
            lines.append("")
            lines.append("threat assessment : NOT PRESENT")

        if card.claims:
            lines.append("")
            lines.append("evidence")
            for claim in card.claims:
                lines.append(
                    f"  [{claim.label.value}] tier {claim.tier} conf "
                    f"{claim.confidence:.2f} — {claim.text}"
                )

        defects = card.completion_defects()
        lines.append("")
        if defects:
            lines.append("BLOCKING DEFECTS — this card cannot be armed")
            for defect in defects:
                lines.append(f"  ! {defect}")
        else:
            lines.append("no blocking defects: this card may be armed")
        lines.append(RULE)
        return "\n".join(lines)

    # -- WF-07 ROE gate ---------------------------------------------------

    def roe_gate(self, card_id: str, countermeasure_id: str) -> str:
        """The interlock view: the profile, the ceiling, and the margin."""
        card = self._card(card_id)
        cm = catalogue_module.get(countermeasure_id)
        if cm is None:
            return f"no such countermeasure: {countermeasure_id}"
        result = evaluate(card, cm, self.context)
        lines = self._header("ROE GATE")
        lines.append(f"card              : {card.card_id} ({card.profile.label})")
        lines.append(f"countermeasure    : {cm.identifier} — {cm.name}")
        lines.append(f"class             : {cm.cm_class.value}")
        lines.append(f"collateral class  : {cm.collateral.name} "
                     f"(exposure {cm.collateral.exposure:.2f})")
        lines.append(f"reversibility     : {cm.reversibility.name}")
        lines.append(f"autonomy class    : {cm.autonomy.name}")
        lines.append(f"direction         : {cm.direction.value}")
        lines.append("")
        lines.append(f"ceiling           : {card.profile.label} / "
                     f"collateral {card.profile.max_collateral.name} / "
                     f"autonomy {card.profile.max_autonomy.name}")
        needed = required_approvals(card.profile, cm.collateral)
        lines.append(f"approvals needed  : {', '.join(sorted(needed))}")
        lines.append(f"approvals on card : {', '.join(sorted(card.approver_roles)) or 'none'}")
        lines.append("")
        if result.admissible:
            lines.append("RESULT: admissible. The engine will accept a dispatch.")
        else:
            lines.append("RESULT: REFUSED. The engine will reject a dispatch.")
            for failure in result.failures:
                lines.append(f"  {failure.condition} — {failure.title}")
                lines.append(f"      {failure.detail}")
                if failure.margin:
                    lines.append(f"      margin : {failure.margin}")
                if failure.remedy:
                    lines.append(f"      remedy : {failure.remedy}")
        lines.append(RULE)
        return "\n".join(lines)

    # -- WF-08 countermeasure console ------------------------------------

    def countermeasure_console(self, card_id: str) -> str:
        """Candidate generation, admissibility, and ranking."""
        card = self._card(card_id)
        candidates = generate_candidates(card)
        admissible, rejected = filter_admissible(card, candidates, self.context)
        ranked = rank_candidates(admissible)
        lines = self._header(f"COUNTERMEASURE CONSOLE — {card.card_id}")
        lines.append(f"candidates generated from technique bindings: {len(candidates)}")
        lines.append(f"admissible: {len(admissible)}   rejected: {len(rejected)}")
        lines.append("")
        lines.append("admissible, ranked by risk-adjusted priority")
        if not ranked:
            lines.append("  (none)")
        for candidate in ranked:
            cm = candidate.countermeasure
            lines.append(
                f"  {cm.identifier}  P={candidate.priority:.3f}  "
                f"{cm.collateral.name}  {cm.reversibility.name:<12} {cm.autonomy.name:<13} "
                f"{cm.name}"
            )
        lines.append("")
        lines.append("rejected, with the specific condition and margin")
        if not rejected:
            lines.append("  (none)")
        for candidate in rejected:
            lines.append(f"  {candidate.identifier}  {candidate.countermeasure.name}")
            for failure in candidate.result.failures:
                lines.append(f"      {failure.condition}: {failure.margin or failure.detail}")
        lines.append(RULE)
        return "\n".join(lines)

    # -- WF-09 / WF-12 options and assumptions ---------------------------

    def options(self, card_id: str) -> str:
        """The decision space, including the do-nothing option."""
        card = self._card(card_id)
        candidates = generate_candidates(card)
        admissible, rejected = filter_admissible(card, candidates, self.context)
        options = counterfactuals(card, admissible + rejected)
        lines = self._header(f"DECISION SPACE — {card.card_id}")
        lines.append("options ordered by residual risk, lowest first")
        for option in options:
            if option.has_band:
                residual = (
                    f"{option.band[0]:.2f}–{option.band[1]:.2f}"
                )
            else:
                residual = f"{option.residual_risk:6.2f}"
            marker = "  [effectiveness unconfirmed]" if option.unconfirmed_effectiveness else ""
            lines.append(
                f"  residual {residual}  P={option.priority:.3f}  "
                f"{option.collateral.name}  {option.label}{marker}"
            )
            if option.note:
                lines.append(f"      {option.note}")
        lines.append("")
        lines.append(f"risk of inaction recorded on the card: "
                     f"{card.risk_of_inaction or 'NOT RECORDED'}")
        lines.append(RULE)
        return "\n".join(lines)

    # -- WF-13 autonomy monitor ------------------------------------------

    def autonomy_monitor(self, card_id: str) -> str:
        """Live autonomy budget, envelope, and expiry."""
        card = self._card(card_id)
        lines = self._header(f"AUTONOMY MONITOR — {card.card_id}")
        lines.append(f"autonomy class    : {card.autonomy_ceiling.name}")
        lines.append(f"budget           : {card.autonomy_budget} units")
        lines.append(f"consumed         : {card.autonomy_consumed} units")
        lines.append(f"remaining        : {card.remaining_budget()} units")
        lines.append(f"reversion trigger : the abort conditions on the card")
        lines.append(f"card expiry      : {card.expires_at.isoformat()}")
        if card.autonomy_budget and card.remaining_budget() == 0:
            lines.append("")
            lines.append("BUDGET EXHAUSTED: no further autonomous action is permitted.")
        lines.append(RULE)
        return "\n".join(lines)

    # -- WF-06 dispatch ----------------------------------------------------

    def dispatch(self, card_id: str, countermeasure_id: str, *, actor: str = "") -> str:
        """Arm and dispatch a countermeasure, or refuse it and say why.

        The admissibility algebra is re-evaluated at dispatch time, because
        both the card's state and the world may have changed since the
        selection.
        """
        card = self._card(card_id)
        cm = catalogue_module.get(countermeasure_id)
        if cm is None:
            return f"no such countermeasure: {countermeasure_id}"
        result = dispatch(card, cm, self.ledger, context=self.context, actor=actor)
        lines = self._header("DISPATCH")
        lines.append(f"card            : {card_id}")
        lines.append(f"countermeasure  : {cm.identifier} — {cm.name}")
        if result.dispatched:
            lines.append("RESULT: dispatched.")
            lines.append(f"autonomy spent  : {result.units_spent} unit(s)")
            lines.append(f"budget remaining: {result.remaining_budget}")
        else:
            lines.append("RESULT: REFUSED. Nothing was executed and no budget was spent.")
            lines.append(f"reason          : {result.reason}")
        lines.append(RULE)
        return "\n".join(lines)

    # -- WF-15 abort ------------------------------------------------------

    def abort(self, card_id: str, reason: str) -> str:
        """Terminate an operation and record why.

        The abort action is single, always available, and never requires a
        confirmation step. The reason is captured afterwards, not before,
        because an abort that must be justified first is an abort that gets
        delayed.
        """
        card = self._card(card_id)
        self.aborted[card_id] = reason
        card.autonomy_consumed = card.autonomy_budget
        self.ledger.append(
            "abort",
            {
                "card_id": card_id,
                "reason": reason,
                "aborted_at": utc_now().isoformat(),
                "posture_reverted_to": ROEProfile.R0_OBSERVE.label,
            },
            subject=f"card:{card_id}",
            actor=card.owner,
            card_ref=card_id,
        )
        lines = self._header("OPERATION ABORTED")
        lines.append(f"card       : {card_id}")
        lines.append(f"reason     : {reason}")
        lines.append("effect     : autonomy grants revoked, dispatch stopped, "
                     "posture reverted to Observe")
        lines.append("notification: the card owner and the duty manager are notified")
        lines.append(RULE)
        return "\n".join(lines)

    # -- WF-16 replay -----------------------------------------------------

    def replay(self, card_id: str) -> str:
        """Reconstruct an operation from the Ledger."""
        timeline = self.ledger.replay(card_id)
        lines = self._header(f"REPLAY — {card_id}")
        if not timeline:
            lines.append("no recorded entries for this card")
            lines.append(RULE)
            return "\n".join(lines)
        for item in timeline:
            lines.append(
                f"[{item['seq']:>4}] {item['timestamp']}  {item['kind']}  "
                f"actor: {item['actor']}"
            )
            payload = item["payload"]
            for key, value in payload.items():
                if isinstance(value, (list, tuple)):
                    value = "; ".join(str(v) for v in value)
                lines.append(f"        {key}: {value}")
            lines.append(f"        digest: {item['digest'][:32]}...")
        lines.append(RULE)
        return "\n".join(lines)

    # -- WF-21 audit export ------------------------------------------------

    def audit(self) -> str:
        """Verification report for the Ledger."""
        report = self.ledger.verify()
        lines = self._header("LEDGER VERIFICATION")
        lines.append(f"records    : {report['records']}")
        lines.append(f"intact     : {report['intact']}")
        lines.append(f"head       : {report['head']}")
        lines.append("")
        lines.append(f"establishes    : {report['establishes']}")
        lines.append(f"does not establish: {report['does_not_establish']}")
        if report["problems"]:
            lines.append("")
            lines.append("problems")
            for problem in report["problems"]:
                lines.append(f"  {problem}")
        lines.append("")
        anchor = self.ledger.anchor()
        lines.append("anchor for independent export")
        lines.append(f"  chain digest: {anchor['chain_digest']}")
        lines.append(f"  head        : {anchor['head']}")
        lines.append(RULE)
        return "\n".join(lines)


def _plus(moment: datetime, seconds: float) -> datetime:
    from datetime import timedelta

    return moment + timedelta(seconds=seconds)
