"""Markdown report generation for compliance outputs."""

from __future__ import annotations

from collections import defaultdict

from engine.models import ComplianceReport


class MarkdownReporter:
    """Render compliance reports to markdown text."""

    def render(self, report: ComplianceReport) -> str:
        """Render full markdown report."""

        lines: list[str] = [
            "# Compliance Report",
            "",
            f"Generated at: {report.generated_at.isoformat()}",
            f"Policies evaluated: {report.evaluation_count}",
            "",
            "## Framework Compliance Summary",
            "",
            "| Framework | Compliance |",
            "|---|---:|",
        ]

        for framework, score in sorted(report.framework_compliance.items()):
            lines.append(f"| {framework} | {score}% |")

        lines.extend(["", "## Control Evaluation", ""])
        by_component = defaultdict(list)
        for result in report.results:
            by_component[result.component].append(result)

        for component, results in sorted(by_component.items()):
            lines.extend(
                [
                    f"### {component}",
                    "",
                    "| Control | Framework | Status | Severity | Evidence |",
                    "|---|---|---|---|---|",
                ]
            )
            for result in results:
                safe_evidence = result.evidence.replace("\n", " ")
                lines.append(
                    f"| {result.control_id} | {result.framework} | {result.status.value} | "
                    f"{result.severity.value} | {safe_evidence} |"
                )
            lines.append("")

        lines.extend(["## Conflict Summary", ""])

        if not report.conflicts:
            lines.append("No conflicts detected.")
            return "\n".join(lines)

        for conflict in report.conflicts:
            lines.extend(
                [
                    f"### {conflict.conflict_id}",
                    "",
                    f"- Component: {conflict.component}",
                    f"- Frameworks: {conflict.frameworks[0]} vs {conflict.frameworks[1]}",
                    f"- Type: {conflict.conflict_type}",
                    f"- Severity: {conflict.severity.value}",
                    f"- Summary: {conflict.summary}",
                    f"- Recommendation: {conflict.recommendation}",
                    "",
                ]
            )

        return "\n".join(lines)
