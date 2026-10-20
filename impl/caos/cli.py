"""Command-line entry point for the Watchfloor.

The console is deliberately plain text. A watchfloor that needs a graphics
stack to be legible is a watchfloor that will not be legible on the terminal
an operator actually has at 02:00.
"""

from __future__ import annotations

import argparse
import sys

from . import __version__
from .countermeasures import CATALOGUE, by_class
from .decision import filter_admissible, generate_candidates, rank_candidates, select
from .demo import DEMO_CARD_ID, build_demo
from .proving_ground import (
    RUBRIC,
    Archetype,
    Scenario,
    evaluate_detection,
    run_scenario,
)
from .taxonomy import CATEGORIES, TECHNIQUES
from .vocab import CMClass
from typing import Optional, Sequence


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="caos",
        description=(
            "CAOS — Counter-Adversary Operations System. The operator console for "
            "human-in-the-loop operations against adversarial AI."
        ),
    )
    parser.add_argument("--version", action="version", version=f"caos {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("watchboard", help="the live situation view")

    sub.add_parser("triage", help="the ranked triage queue")

    p_card = sub.add_parser("card", help="show an operation card")
    p_card.add_argument("card_id", nargs="?", default=DEMO_CARD_ID)

    p_roe = sub.add_parser("roe", help="the ROE gate for a countermeasure")
    p_roe.add_argument("card_id", nargs="?", default=DEMO_CARD_ID)
    p_roe.add_argument("countermeasure_id")

    p_cm = sub.add_parser("cm", help="the countermeasure console")
    p_cm.add_argument("card_id", nargs="?", default=DEMO_CARD_ID)

    p_opt = sub.add_parser("options", help="the decision space, including inaction")
    p_opt.add_argument("card_id", nargs="?", default=DEMO_CARD_ID)

    p_auto = sub.add_parser("autonomy", help="the autonomy monitor")
    p_auto.add_argument("card_id", nargs="?", default=DEMO_CARD_ID)

    p_replay = sub.add_parser("replay", help="reconstruct an operation from the ledger")
    p_replay.add_argument("card_id", nargs="?", default=DEMO_CARD_ID)

    sub.add_parser("audit", help="verify the ledger and produce an anchor")

    p_abort = sub.add_parser("abort", help="terminate an operation")
    p_abort.add_argument("card_id", nargs="?", default=DEMO_CARD_ID)
    p_abort.add_argument("reason", nargs="?", default="operator abort")

    p_select = sub.add_parser("select", help="select and record a countermeasure")
    p_select.add_argument("card_id", nargs="?", default=DEMO_CARD_ID)
    p_select.add_argument("countermeasure_id")
    p_select.add_argument(
        "--confirm",
        action="store_true",
        help="record the decision; without it, the selection is only previewed",
    )
    p_select.add_argument("--actor", default="operator-1")
    p_select.add_argument("--dissent", default="")

    p_dispatch = sub.add_parser(
        "dispatch", help="arm and dispatch a countermeasure under a card"
    )
    p_dispatch.add_argument("card_id", nargs="?", default=DEMO_CARD_ID)
    p_dispatch.add_argument("countermeasure_id")
    p_dispatch.add_argument("--actor", default="operator-1")

    p_emerg = sub.add_parser(
        "emergency", help="the emergency containment path: catalogue or drill"
    )
    p_emerg.add_argument(
        "view",
        nargs="?",
        default="drill",
        choices=["catalogue", "drill"],
        help="catalogue renders the emergency action catalogue; drill runs a "
        "synthetic containment drill",
    )

    p_cat = sub.add_parser("catalogue", help="list the countermeasure catalogue")
    p_cat.add_argument(
        "--class",
        dest="cm_class",
        choices=[c.value for c in CMClass],
        help="restrict to one countermeasure class",
    )

    sub.add_parser("techniques", help="list the adversary taxonomy")

    p_ex = sub.add_parser("exercise", help="run a proving-ground scenario")
    p_ex.add_argument(
        "--archetype",
        choices=[a.value for a in Archetype],
        default=Archetype.SOCIAL_SWARM.value,
    )
    p_ex.add_argument("--seed", type=int, default=20261020)
    p_ex.add_argument("--steps", type=int, default=12)
    p_ex.add_argument(
        "--rubric", action="store_true", help="print the exercise scoring rubric"
    )

    return parser


def _show_card(floor, card_id: str) -> str:
    """Render a card, or say plainly that there is no such card."""
    try:
        return floor.show_card(card_id)
    except KeyError:
        known = ", ".join(sorted(floor.cards)) or "none"
        return f"no such card: {card_id}\nknown cards: {known}"


def _cmd_catalogue(args: argparse.Namespace) -> str:
    lines = ["-" * 78, "COUNTERMEASURE CATALOGUE", "-" * 78]
    if args.cm_class:
        entries = by_class(CMClass(args.cm_class))
    else:
        entries = list(CATALOGUE)
    current_class = None
    for entry in entries:
        if entry.cm_class is not current_class:
            current_class = entry.cm_class
            lines.append("")
            lines.append(f"{current_class.value.upper()}")
        lines.append(
            f"  {entry.identifier}  {entry.collateral.name}  "
            f"{entry.reversibility.name:<11} {entry.autonomy.name:<13} "
            f"{entry.name}"
        )
        lines.append(
            f"      direction: {entry.direction.value}; "
            f"minimum profile: {entry.min_profile.label}; "
            f"attribution: {entry.attribution_dependency.value}"
        )
        lines.append(
            f"      residual reduction {entry.residual_reduction:.2f} at confidence "
            f"{entry.effectiveness_confidence:.2f} (estimate, not calibrated)"
        )
    lines.append("-" * 78)
    return "\n".join(lines)


def _cmd_techniques(_: argparse.Namespace) -> str:
    lines = ["-" * 78, "ADVERSARY AI TAXONOMY (AAT)", "-" * 78]
    for category_id, category in CATEGORIES.items():
        lines.append("")
        lines.append(f"{category_id}  {category['name']}")
        lines.append(f"  scope: {category['scope']}")
        lines.append(
            f"  dominant detection signal: {category['dominant_detection_signal']}"
        )
        lines.append(
            f"  dominant countermeasure class: {category['dominant_countermeasure_class']}"
        )
        for tech in TECHNIQUES:
            if tech.category == category_id:
                lines.append(
                    f"    {tech.identifier}  {tech.name}  [attribution: "
                    f"{tech.attribution_note}; expected time to detect: {tech.mttd}]"
                )
    lines.append("-" * 78)
    return "\n".join(lines)


def _cmd_exercise(args: argparse.Namespace) -> str:
    if args.rubric:
        lines = ["-" * 78, "EXERCISE RUBRIC", "-" * 78]
        for dimension, description, weight in RUBRIC:
            lines.append(f"  {dimension} (weight {weight}): {description}")
        lines.append("-" * 78)
        return "\n".join(lines)

    archetype = Archetype(args.archetype)
    scenario = Scenario(
        name=f"proving-ground:{archetype.value}",
        archetype=archetype,
        steps=args.steps,
        seed=args.seed,
    )
    signals = run_scenario(scenario)
    report = evaluate_detection(signals, scenario.detected)
    lines = ["-" * 78, "PROVING GROUND", "-" * 78]
    lines.append(f"scenario    : {scenario.name}")
    lines.append(f"seed       : {scenario.seed}")
    lines.append(f"signals    : {report.signals}")
    lines.append(
        f"techniques exercised: {', '.join(sorted(report.techniques_exercised))}"
    )
    lines.append(
        f"detected            : {', '.join(sorted(report.techniques_detected)) or 'none'}"
    )
    lines.append(
        f"missed              : {', '.join(sorted(report.techniques_missed)) or 'none'}"
    )
    lines.append(f"coverage            : {report.coverage_percentage:.1f}%")
    lines.append("")
    lines.append("findings")
    for finding in report.findings:
        lines.append(f"  - {finding}")
    lines.append("")
    lines.append("the exercise is a test of the operator and the interlock, not the tools")
    lines.append("-" * 78)
    return "\n".join(lines)


def _cmd_select(floor, args: argparse.Namespace) -> str:
    card = floor.cards[args.card_id]
    candidates = generate_candidates(card)
    admissible, _rejected = filter_admissible(card, candidates, floor.context)
    ranked = rank_candidates(admissible)
    match = [c for c in ranked if c.identifier == args.countermeasure_id]
    if not match:
        in_catalog = [c for c in candidates if c.identifier == args.countermeasure_id]
        if in_catalog:
            return floor.roe_gate(args.card_id, args.countermeasure_id)
        return (
            f"{args.countermeasure_id} is neither a bound candidate nor admissible.\n"
            "Run 'cm' to see the candidate set and why each candidate was rejected."
        )
    candidate = match[0]
    if not args.confirm:
        return (
            floor.roe_gate(args.card_id, args.countermeasure_id)
            + "\n\nPREVIEW ONLY. Re-run with --confirm to record the decision."
        )
    record = select(
        card,
        candidate,
        alternatives=tuple(c.identifier for c in ranked),
        dissent=args.dissent,
        actor=args.actor,
        context=floor.context,
    )
    floor.ledger.append("decision", record.as_payload())
    lines = [
        "-" * 78,
        "DECISION RECORDED",
        "-" * 78,
        f"record id  : {record.record_id}",
        f"card       : {record.card_id}",
        f"choice     : {record.choice}",
        f"authority  : {record.authority_relied_on}",
        f"residual   : {record.residual_risk:.3f}",
        f"contingency: {record.pre_registered_contingency}",
        "-" * 78,
    ]
    return "\n".join(lines)


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)
    floor = build_demo()

    if args.command == "watchboard":
        print(floor.watchboard())
    elif args.command == "triage":
        print(floor.triage())
    elif args.command == "card":
        print(_show_card(floor, args.card_id))
    elif args.command == "roe":
        print(floor.roe_gate(args.card_id, args.countermeasure_id))
    elif args.command == "cm":
        print(floor.countermeasure_console(args.card_id))
    elif args.command == "options":
        print(floor.options(args.card_id))
    elif args.command == "autonomy":
        print(floor.autonomy_monitor(args.card_id))
    elif args.command == "replay":
        print(floor.replay(args.card_id))
    elif args.command == "audit":
        print(floor.audit())
    elif args.command == "abort":
        print(floor.abort(args.card_id, args.reason))
    elif args.command == "dispatch":
        print(floor.dispatch(args.card_id, args.countermeasure_id, actor=args.actor))
    elif args.command == "select":
        print(_cmd_select(floor, args))
    elif args.command == "emergency":
        from .emergency_console import run_drill, show_catalogue

        print(show_catalogue() if args.view == "catalogue" else run_drill())
    elif args.command == "catalogue":
        print(_cmd_catalogue(args))
    elif args.command == "techniques":
        print(_cmd_techniques(args))
    elif args.command == "exercise":
        print(_cmd_exercise(args))
    else:  # pragma: no cover - argparse enforces the choice
        parser.error(f"unknown command: {args.command}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
