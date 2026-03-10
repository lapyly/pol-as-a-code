"""CLI for the policy-as-code reconciliation engine."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from engine.conflict_detector import ConflictDetector
from engine.evaluator import PolicyEvaluator, framework_compliance
from engine.models import ComplianceReport
from engine.reconciliation import ReconciliationEngine
from engine.state import load_state
from policies.all_policies import build_registry
from reporting.markdown_reporter import MarkdownReporter


def configure_logging(debug: bool) -> None:
    """Configure default logging."""

    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )


def run(state_path: Path, output_path: Path | None, output_format: str) -> str:
    """Run the full compliance analysis pipeline and return report content."""

    state = load_state(state_path)
    registry = build_registry()
    evaluator = PolicyEvaluator(registry)
    results = evaluator.evaluate(state)

    detector = ConflictDetector()
    conflicts = detector.detect(results)
    reconciled = ReconciliationEngine().reconcile(conflicts)

    report = ComplianceReport.now(
        results=results,
        conflicts=reconciled,
        framework_compliance=framework_compliance(results),
    )

    if output_format == "json":
        payload = {
            "generated_at": report.generated_at.isoformat(),
            "evaluation_count": report.evaluation_count,
            "framework_compliance": report.framework_compliance,
            "results": [result.__dict__ for result in report.results],
            "conflicts": [conflict.__dict__ for conflict in report.conflicts],
        }
        content = json.dumps(payload, default=str, indent=2)
    else:
        content = MarkdownReporter().render(report)

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")

    return content


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Policy-as-Code Reconciliation Engine")
    parser.add_argument("--state", required=True, type=Path, help="Path to infrastructure state JSON")
    parser.add_argument("--output", type=Path, help="Output file path")
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug logs")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    configure_logging(args.debug)
    content = run(args.state, args.output, args.format)
    if not args.output:
        print(content)


if __name__ == "__main__":
    main()
