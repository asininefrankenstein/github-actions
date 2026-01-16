#!/usr/bin/env python3
"""
Advanced Summary Generation Script for GitHub Actions

This script parses test output from various frameworks and generates
rich Markdown summaries for GitHub Actions step summaries.

Supported formats:
- JUnit XML (pytest, Java, etc.)
- pytest JSON (--json-report)
- Go test output (-v)
- npm/Jest output
- TAP (Test Anything Protocol)
- Generic text output

Usage:
    python generate_summary.py --format junit --file results.xml
    python generate_summary.py --format auto --file output.txt --title "My Tests"
    python generate_summary.py --passed 10 --failed 2 --title "Manual Results"
"""

import argparse
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


# Maximum size for GitHub Actions step summary (1 MiB)
MAX_SUMMARY_SIZE = 1048576
# Leave buffer for formatting
SAFE_SUMMARY_SIZE = 1000000


@dataclass
class TestCase:
    """Represents a single test case."""
    name: str
    classname: str = ""
    status: str = "passed"  # passed, failed, skipped, error
    duration: float = 0.0
    message: str = ""
    output: str = ""


@dataclass
class TestSummary:
    """Aggregated test summary data."""
    title: str = "Test Results"
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    errors: int = 0
    total: int = 0
    duration: float = 0.0
    test_cases: list = field(default_factory=list)
    raw_output: str = ""
    format_detected: str = "unknown"
    timestamp: str = ""

    def calculate_totals(self) -> None:
        """Calculate total from components if not set."""
        if self.total == 0:
            self.total = self.passed + self.failed + self.skipped + self.errors

    @property
    def status(self) -> str:
        """Overall status based on failures/errors."""
        if self.failed > 0 or self.errors > 0:
            return "failed"
        elif self.passed > 0:
            return "passed"
        return "unknown"

    @property
    def pass_rate(self) -> float:
        """Calculate pass rate percentage."""
        if self.total == 0:
            return 0.0
        return (self.passed / self.total) * 100


def parse_junit_xml(file_path: str) -> TestSummary:
    """Parse JUnit XML format (pytest, Java, etc.)."""
    summary = TestSummary(format_detected="junit")

    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        # Handle both single testsuite and testsuites root
        if root.tag == "testsuites":
            testsuites = root.findall(".//testsuite")
        elif root.tag == "testsuite":
            testsuites = [root]
        else:
            testsuites = []

        for ts in testsuites:
            summary.total += int(ts.get("tests", 0))
            summary.failed += int(ts.get("failures", 0))
            summary.errors += int(ts.get("errors", 0))
            summary.skipped += int(ts.get("skipped", 0))
            summary.duration += float(ts.get("time", 0))

            # Parse individual test cases
            for tc in ts.findall(".//testcase"):
                test_case = TestCase(
                    name=tc.get("name", "unknown"),
                    classname=tc.get("classname", ""),
                    duration=float(tc.get("time", 0)),
                )

                failure = tc.find("failure")
                error = tc.find("error")
                skipped = tc.find("skipped")

                if failure is not None:
                    test_case.status = "failed"
                    test_case.message = failure.get("message", "")
                    test_case.output = failure.text or ""
                elif error is not None:
                    test_case.status = "error"
                    test_case.message = error.get("message", "")
                    test_case.output = error.text or ""
                elif skipped is not None:
                    test_case.status = "skipped"
                    test_case.message = skipped.get("message", "")
                else:
                    test_case.status = "passed"

                summary.test_cases.append(test_case)

        summary.passed = summary.total - summary.failed - summary.errors - summary.skipped

    except ET.ParseError as e:
        raise ValueError(f"Failed to parse JUnit XML: {e}")

    return summary


def parse_pytest_json(file_path: str) -> TestSummary:
    """Parse pytest JSON report format."""
    summary = TestSummary(format_detected="pytest-json")

    try:
        with open(file_path, "r") as f:
            data = json.load(f)

        # Handle pytest-json-report format
        if "summary" in data:
            s = data["summary"]
            summary.passed = s.get("passed", 0)
            summary.failed = s.get("failed", 0)
            summary.skipped = s.get("skipped", 0)
            summary.errors = s.get("error", 0)
            summary.total = s.get("total", 0)
            summary.duration = data.get("duration", 0)

            # Parse test cases
            for test in data.get("tests", []):
                test_case = TestCase(
                    name=test.get("nodeid", "unknown"),
                    status=test.get("outcome", "unknown"),
                    duration=test.get("duration", 0),
                )

                if "call" in test and test["call"].get("longrepr"):
                    test_case.output = test["call"]["longrepr"]

                summary.test_cases.append(test_case)

        # Handle pytest-report-log format
        elif isinstance(data, list):
            for entry in data:
                if entry.get("$report_type") == "TestReport":
                    outcome = entry.get("outcome", "")
                    if outcome == "passed":
                        summary.passed += 1
                    elif outcome == "failed":
                        summary.failed += 1
                    elif outcome == "skipped":
                        summary.skipped += 1

            summary.calculate_totals()

    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse pytest JSON: {e}")

    return summary


def parse_go_test(file_path: str) -> TestSummary:
    """Parse Go test verbose output."""
    summary = TestSummary(format_detected="go")

    with open(file_path, "r") as f:
        content = f.read()

    summary.raw_output = content

    # Parse individual test results
    for match in re.finditer(r"--- (PASS|FAIL|SKIP): (\S+) \(([0-9.]+)s\)", content):
        status_map = {"PASS": "passed", "FAIL": "failed", "SKIP": "skipped"}
        status = status_map.get(match.group(1), "unknown")

        test_case = TestCase(
            name=match.group(2),
            status=status,
            duration=float(match.group(3)),
        )

        if status == "passed":
            summary.passed += 1
        elif status == "failed":
            summary.failed += 1
        elif status == "skipped":
            summary.skipped += 1

        summary.test_cases.append(test_case)

    # Parse overall duration
    duration_match = re.search(r"(?:ok|FAIL)\s+\S+\s+([0-9.]+)s", content)
    if duration_match:
        summary.duration = float(duration_match.group(1))

    summary.calculate_totals()
    return summary


def parse_npm_test(file_path: str) -> TestSummary:
    """Parse npm/Jest test output."""
    summary = TestSummary(format_detected="npm")

    with open(file_path, "r") as f:
        content = f.read()

    summary.raw_output = content

    # Jest format: "Tests: X passed, Y failed, Z skipped, W total"
    tests_match = re.search(
        r"Tests:\s*"
        r"(?:(\d+)\s+passed)?"
        r"(?:,?\s*(\d+)\s+failed)?"
        r"(?:,?\s*(\d+)\s+skipped)?"
        r"(?:,?\s*(\d+)\s+total)?",
        content,
    )

    if tests_match:
        summary.passed = int(tests_match.group(1) or 0)
        summary.failed = int(tests_match.group(2) or 0)
        summary.skipped = int(tests_match.group(3) or 0)
        summary.total = int(tests_match.group(4) or 0)

    # Parse duration
    duration_match = re.search(r"Time:\s*([0-9.]+)\s*s", content)
    if duration_match:
        summary.duration = float(duration_match.group(1))

    # Parse individual test suites
    for match in re.finditer(r"(PASS|FAIL)\s+(\S+)", content):
        test_case = TestCase(
            name=match.group(2),
            status="passed" if match.group(1) == "PASS" else "failed",
        )
        summary.test_cases.append(test_case)

    summary.calculate_totals()
    return summary


def parse_tap(file_path: str) -> TestSummary:
    """Parse TAP (Test Anything Protocol) output."""
    summary = TestSummary(format_detected="tap")

    with open(file_path, "r") as f:
        content = f.read()

    summary.raw_output = content

    # Parse plan
    plan_match = re.search(r"^1\.\.(\d+)", content, re.MULTILINE)
    if plan_match:
        summary.total = int(plan_match.group(1))

    # Parse test results
    for match in re.finditer(r"^(ok|not ok)\s+(\d+)\s*-?\s*(.*)$", content, re.MULTILINE):
        status = "passed" if match.group(1) == "ok" else "failed"
        name = match.group(3).strip()

        # Check for SKIP or TODO directives
        if "# SKIP" in name:
            status = "skipped"
            name = name.replace("# SKIP", "").strip()
        elif "# TODO" in name:
            status = "skipped"
            name = name.replace("# TODO", "").strip()

        if status == "passed":
            summary.passed += 1
        elif status == "failed":
            summary.failed += 1
        else:
            summary.skipped += 1

        test_case = TestCase(name=name or f"Test {match.group(2)}", status=status)
        summary.test_cases.append(test_case)

    summary.calculate_totals()
    return summary


def parse_generic(file_path: str) -> TestSummary:
    """Parse generic text output looking for common patterns."""
    summary = TestSummary(format_detected="generic")

    with open(file_path, "r") as f:
        content = f.read()

    summary.raw_output = content

    # Try various patterns
    patterns = [
        # "X passed, Y failed"
        (r"(\d+)\s+(?:tests?\s+)?passed", "passed"),
        (r"(\d+)\s+(?:tests?\s+)?failed", "failed"),
        (r"(\d+)\s+(?:tests?\s+)?skipped", "skipped"),
        (r"(\d+)\s+(?:tests?\s+)?errors?", "errors"),
        # "passed: X, failed: Y"
        (r"passed:\s*(\d+)", "passed"),
        (r"failed:\s*(\d+)", "failed"),
        (r"skipped:\s*(\d+)", "skipped"),
    ]

    for pattern, attr in patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            setattr(summary, attr, int(match.group(1)))

    # Try to find total
    total_match = re.search(r"(\d+)\s+(?:tests?\s+)?total", content, re.IGNORECASE)
    if total_match:
        summary.total = int(total_match.group(1))
    else:
        summary.calculate_totals()

    # Try to find duration
    duration_match = re.search(r"(?:time|duration|took):\s*([0-9.]+)\s*s", content, re.IGNORECASE)
    if duration_match:
        summary.duration = float(duration_match.group(1))

    return summary


def detect_format(file_path: str) -> str:
    """Auto-detect the test output format."""
    path = Path(file_path)

    # Check file extension
    if path.suffix == ".xml":
        return "junit"
    elif path.suffix == ".json":
        # Check content to distinguish JSON types
        try:
            with open(file_path, "r") as f:
                content = f.read(1000)
            if '"summary"' in content:
                return "pytest-json"
        except Exception:
            pass
        return "pytest-json"

    # Check content
    try:
        with open(file_path, "r") as f:
            first_lines = "".join(f.readline() for _ in range(10))

        if first_lines.strip().startswith("<?xml"):
            return "junit"
        if first_lines.strip().startswith("{"):
            return "pytest-json"
        if "=== RUN" in first_lines or "--- PASS" in first_lines:
            return "go"
        if "Tests:" in first_lines or "PASS " in first_lines:
            return "npm"
        if re.search(r"^1\.\.\d+", first_lines, re.MULTILINE):
            return "tap"

    except Exception:
        pass

    return "generic"


def parse_results(file_path: str, format_type: str = "auto") -> TestSummary:
    """Parse test results from file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Results file not found: {file_path}")

    if format_type == "auto":
        format_type = detect_format(file_path)

    parsers = {
        "junit": parse_junit_xml,
        "pytest-json": parse_pytest_json,
        "go": parse_go_test,
        "npm": parse_npm_test,
        "tap": parse_tap,
        "generic": parse_generic,
    }

    parser = parsers.get(format_type, parse_generic)
    return parser(file_path)


def format_duration(seconds: float) -> str:
    """Format duration in human-readable format."""
    if seconds < 1:
        return f"{seconds * 1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.2f}s"
    else:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.1f}s"


def truncate_text(text: str, max_lines: int = 100) -> tuple[str, bool]:
    """Truncate text to maximum lines, return (text, was_truncated)."""
    lines = text.split("\n")
    if max_lines > 0 and len(lines) > max_lines:
        truncated = "\n".join(lines[:max_lines])
        return truncated, True
    return text, False


def generate_markdown(
    summary: TestSummary,
    show_details: bool = False,
    show_passed: bool = False,
    max_details_lines: int = 100,
    include_badge: bool = True,
) -> str:
    """Generate Markdown summary."""
    lines = []

    # Title
    lines.append(f"## {summary.title}")
    lines.append("")

    # Badge
    if include_badge:
        if summary.status == "passed":
            badge = ":white_check_mark: **Passed**"
        elif summary.status == "failed":
            badge = ":x: **Failed**"
        else:
            badge = ":grey_question: **Unknown**"
        lines.append(f"**Status:** {badge}")
        lines.append("")

    # Summary table
    if summary.total > 0:
        lines.append("| Metric | Count |")
        lines.append("|--------|-------|")
        lines.append(f"| :white_check_mark: Passed | {summary.passed} |")
        lines.append(f"| :x: Failed | {summary.failed} |")
        if summary.errors > 0:
            lines.append(f"| :boom: Errors | {summary.errors} |")
        if summary.skipped > 0:
            lines.append(f"| :fast_forward: Skipped | {summary.skipped} |")
        lines.append(f"| **Total** | **{summary.total}** |")
        lines.append("")

        # Duration
        if summary.duration > 0:
            lines.append(f"**Duration:** {format_duration(summary.duration)}")
            lines.append("")

        # Pass rate
        lines.append(f"**Pass Rate:** {summary.pass_rate:.1f}%")
        lines.append("")

        # Format detected
        if summary.format_detected != "unknown":
            lines.append(f"*Format: {summary.format_detected}*")
            lines.append("")
    else:
        lines.append("> :warning: No test results found")
        lines.append("")

    # Failed test details
    failed_cases = [tc for tc in summary.test_cases if tc.status in ("failed", "error")]
    if failed_cases and show_details:
        lines.append("### Failed Tests")
        lines.append("")
        for tc in failed_cases[:20]:  # Limit to first 20
            name = tc.name
            if tc.classname:
                name = f"{tc.classname}::{tc.name}"
            lines.append(f"- :x: `{name}`")
            if tc.message:
                # Truncate long messages
                message = tc.message[:200] + "..." if len(tc.message) > 200 else tc.message
                lines.append(f"  - {message}")
        if len(failed_cases) > 20:
            lines.append(f"- ... and {len(failed_cases) - 20} more failures")
        lines.append("")

    # Passed test details (optional)
    if show_passed:
        passed_cases = [tc for tc in summary.test_cases if tc.status == "passed"]
        if passed_cases:
            lines.append("### Passed Tests")
            lines.append("")
            for tc in passed_cases[:50]:  # Limit to first 50
                name = tc.name
                if tc.classname:
                    name = f"{tc.classname}::{tc.name}"
                duration_str = f" ({format_duration(tc.duration)})" if tc.duration > 0 else ""
                lines.append(f"- :white_check_mark: `{name}`{duration_str}")
            if len(passed_cases) > 50:
                lines.append(f"- ... and {len(passed_cases) - 50} more passed")
            lines.append("")

    # Raw output
    if summary.raw_output and show_details:
        lines.append("### Output")
        lines.append("")
        lines.append("```")
        output, was_truncated = truncate_text(summary.raw_output, max_details_lines)
        lines.append(output)
        if was_truncated:
            original_lines = len(summary.raw_output.split("\n"))
            lines.append(f"\n... (truncated, showing {max_details_lines} of {original_lines} lines)")
        lines.append("```")
        lines.append("")

    result = "\n".join(lines)

    # Ensure we don't exceed GitHub's limit
    if len(result.encode("utf-8")) > SAFE_SUMMARY_SIZE:
        # Truncate by removing details progressively
        lines_to_keep = []
        current_size = 0
        for line in lines:
            line_size = len(line.encode("utf-8")) + 1  # +1 for newline
            if current_size + line_size > SAFE_SUMMARY_SIZE - 100:  # Leave room for truncation message
                break
            lines_to_keep.append(line)
            current_size += line_size
        lines_to_keep.append("")
        lines_to_keep.append("> :warning: Output truncated due to size limits")
        result = "\n".join(lines_to_keep)

    return result


def write_github_outputs(summary: TestSummary) -> None:
    """Write outputs to GITHUB_OUTPUT if available."""
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a") as f:
            f.write(f"status={summary.status}\n")
            f.write(f"passed={summary.passed}\n")
            f.write(f"failed={summary.failed}\n")
            f.write(f"skipped={summary.skipped}\n")
            f.write(f"total={summary.total}\n")
            f.write(f"duration={summary.duration}\n")
            f.write(f"pass_rate={summary.pass_rate:.1f}\n")


def write_step_summary(markdown: str) -> None:
    """Write to GITHUB_STEP_SUMMARY if available."""
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_file:
        with open(summary_file, "a") as f:
            f.write(markdown)
            f.write("\n")


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate GitHub Actions test summaries",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Input source
    parser.add_argument(
        "--file", "-f",
        help="Path to test results file",
    )
    parser.add_argument(
        "--format", "-t",
        choices=["auto", "junit", "pytest-json", "go", "npm", "tap", "generic"],
        default="auto",
        help="Test output format (default: auto-detect)",
    )

    # Manual input
    parser.add_argument("--passed", type=int, help="Number of passed tests (manual input)")
    parser.add_argument("--failed", type=int, help="Number of failed tests (manual input)")
    parser.add_argument("--skipped", type=int, help="Number of skipped tests (manual input)")
    parser.add_argument("--errors", type=int, help="Number of test errors (manual input)")
    parser.add_argument("--duration", type=float, help="Test duration in seconds (manual input)")

    # Output options
    parser.add_argument(
        "--title",
        default="Test Results",
        help="Title for the summary (default: Test Results)",
    )
    parser.add_argument(
        "--show-details",
        action="store_true",
        help="Show detailed test output",
    )
    parser.add_argument(
        "--show-passed",
        action="store_true",
        help="Show list of passed tests",
    )
    parser.add_argument(
        "--max-lines",
        type=int,
        default=100,
        help="Maximum lines in details section (default: 100, 0 for unlimited)",
    )
    parser.add_argument(
        "--no-badge",
        action="store_true",
        help="Don't show status badge",
    )

    # Output destination
    parser.add_argument(
        "--output", "-o",
        help="Write markdown to file instead of stdout",
    )
    parser.add_argument(
        "--github-summary",
        action="store_true",
        help="Write to GITHUB_STEP_SUMMARY (automatic in Actions)",
    )
    parser.add_argument(
        "--github-outputs",
        action="store_true",
        help="Write to GITHUB_OUTPUT (automatic in Actions)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output raw data as JSON instead of markdown",
    )

    args = parser.parse_args()

    # Parse or construct summary
    if args.file:
        try:
            summary = parse_results(args.file, args.format)
        except Exception as e:
            sys.stderr.write(f"Error parsing results: {e}\n")
            return 1
    else:
        # Manual input mode
        summary = TestSummary(
            passed=args.passed or 0,
            failed=args.failed or 0,
            skipped=args.skipped or 0,
            errors=args.errors or 0,
            duration=args.duration or 0,
            format_detected="manual",
        )
        summary.calculate_totals()

    summary.title = args.title
    summary.timestamp = datetime.now().isoformat()

    # JSON output mode
    if args.json:
        output = json.dumps({
            "title": summary.title,
            "status": summary.status,
            "passed": summary.passed,
            "failed": summary.failed,
            "skipped": summary.skipped,
            "errors": summary.errors,
            "total": summary.total,
            "duration": summary.duration,
            "pass_rate": summary.pass_rate,
            "format": summary.format_detected,
            "timestamp": summary.timestamp,
            "test_cases": [
                {
                    "name": tc.name,
                    "classname": tc.classname,
                    "status": tc.status,
                    "duration": tc.duration,
                    "message": tc.message,
                }
                for tc in summary.test_cases
            ],
        }, indent=2)
        print(output)
        return 0 if summary.status != "failed" else 1

    # Generate markdown
    markdown = generate_markdown(
        summary,
        show_details=args.show_details,
        show_passed=args.show_passed,
        max_details_lines=args.max_lines,
        include_badge=not args.no_badge,
    )

    # Output destinations
    if args.output:
        with open(args.output, "w") as f:
            f.write(markdown)
    elif args.github_summary or os.environ.get("GITHUB_STEP_SUMMARY"):
        write_step_summary(markdown)
    else:
        print(markdown)

    # Write GitHub outputs if requested or in Actions environment
    if args.github_outputs or os.environ.get("GITHUB_OUTPUT"):
        write_github_outputs(summary)

    # Return non-zero if tests failed
    return 0 if summary.status != "failed" else 1


if __name__ == "__main__":
    sys.exit(main())
