from __future__ import annotations

import json
from pathlib import Path

from engine.conflict_detector import ConflictDetector
from engine.evaluator import PolicyEvaluator, framework_compliance
from engine.models import ComplianceReport, PolicyStatus
from engine.reconciliation import ReconciliationEngine
from engine.state import load_state
from policies.all_policies import build_registry
from reporting.markdown_reporter import MarkdownReporter

FIXTURES = Path(__file__).parent / "fixtures"


def _run_fixture(name: str):
    state = load_state(FIXTURES / name)
    evaluator = PolicyEvaluator(build_registry())
    return evaluator.evaluate(state)


def test_compliant_fixture_has_high_compliance() -> None:
    results = _run_fixture("compliant_state.json")
    summary = framework_compliance(results)

    assert all(score >= 100 for score in summary.values())


def test_non_compliant_fixture_contains_failures() -> None:
    results = _run_fixture("non_compliant_state.json")
    statuses = {result.status for result in results}

    assert PolicyStatus.NON_COMPLIANT in statuses


def test_conflict_fixture_produces_conflict_and_recommendation() -> None:
    results = _run_fixture("conflict_state.json")
    conflicts = ConflictDetector().detect(results)
    reconciled = ReconciliationEngine().reconcile(conflicts)

    assert len(reconciled) > 0
    assert any("pseudonymize" in item.recommendation.lower() for item in reconciled)


def test_markdown_report_contains_sections() -> None:
    results = _run_fixture("conflict_state.json")
    report_text = MarkdownReporter().render(
        report=ComplianceReport.now(
            results=results,
            conflicts=ReconciliationEngine().reconcile(ConflictDetector().detect(results)),
            framework_compliance=framework_compliance(results),
        )
    )
    assert "# Compliance Report" in report_text
    assert "## Conflict Summary" in report_text


def test_fixture_json_is_parseable() -> None:
    for fixture in FIXTURES.glob("*.json"):
        json.loads(fixture.read_text(encoding="utf-8"))
