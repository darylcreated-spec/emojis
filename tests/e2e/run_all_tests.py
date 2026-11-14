#!/usr/bin/env python3
"""
PeelOff E2E Test Suite Runner & Reporting Engine
Executes opaque-box test suites across Tiers 1-4, tracks progressive testability,
generates colorized terminal tables, and outputs test_summary.json and test_report.md.
"""

import os
import sys
import json
import time
import argparse
import unittest
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional

# Ensure project root is in sys.path
WORKSPACE_DIR = os.path.normpath(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
if WORKSPACE_DIR not in sys.path:
    sys.path.insert(0, WORKSPACE_DIR)

from tests.e2e.test_helpers import set_strict_mode, is_strict_mode, get_workspace_path

# ANSI terminal formatting
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
DIM = "\033[2m"
RESET = "\033[0m"


class TestCaseRecord:
    """Telemetry record for an individual test execution."""

    def __init__(self, test_id: str, tier: int, feature: str, description: str):
        self.test_id = test_id
        self.tier = tier
        self.feature = feature
        self.description = description
        self.status = "PENDING"  # PASS, FAIL, ERROR, SKIP
        self.duration = 0.0
        self.message = ""
        self.traceback = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "test_id": self.test_id,
            "tier": self.tier,
            "feature": self.feature,
            "description": self.description,
            "status": self.status,
            "duration_seconds": round(self.duration, 4),
            "message": self.message,
        }


class PeelOffTestResult(unittest.TestResult):
    """Custom TestResult collecting detailed execution metrics and supporting strict mode gating."""

    def __init__(self, strict: bool = False, verbose: bool = False):
        super().__init__()
        self.strict = strict
        self.verbose = verbose
        self.records: List[TestCaseRecord] = []
        self._current_start_time: float = 0.0

    def _extract_tier_and_feature(self, test: unittest.TestCase) -> tuple[int, str]:
        module_name = test.__class__.__module__
        class_name = test.__class__.__name__
        method_name = test._testMethodName

        # Tier detection
        if "tier1" in module_name:
            tier = 1
        elif "tier2" in module_name:
            tier = 2
        elif "tier3" in module_name:
            tier = 3
        elif "tier4" in module_name:
            tier = 4
        else:
            tier = 1

        # Feature detection (F1 through F10)
        feature = "Cross"
        if tier == 4:
            feature = "RealWorld"
        elif tier == 3:
            feature = "Cross"
        else:
            import re
            m = re.search(r"(?:TestTier\d+F|test_(?:t\d+_)?f)(\d+)", f"{class_name}_{method_name}")
            if m:
                f_num = int(m.group(1))
                if 1 <= f_num <= 10:
                    feature = f"F{f_num}"
            else:
                for i in range(10, 0, -1):
                    tag = f"F{i}"
                    if tag in class_name or f"f{i}" in method_name.lower():
                        feature = tag
                        break

        return tier, feature

    def startTest(self, test: unittest.TestCase):
        super().startTest(test)
        self._current_start_time = time.perf_counter()
        if self.verbose:
            sys.stdout.write(f"  {test._testMethodName} ... ")
            sys.stdout.flush()

    def addSuccess(self, test: unittest.TestCase):
        super().addSuccess(test)
        duration = time.perf_counter() - self._current_start_time
        tier, feature = self._extract_tier_and_feature(test)
        desc = test.shortDescription() or test._testMethodName

        record = TestCaseRecord(test.id(), tier, feature, desc)
        record.status = "PASS"
        record.duration = duration
        self.records.append(record)

        if self.verbose:
            sys.stdout.write(f"{GREEN}PASS{RESET} ({duration:.3f}s)\n")
            sys.stdout.flush()

    def addFailure(self, test: unittest.TestCase, err):
        super().addFailure(test, err)
        duration = time.perf_counter() - self._current_start_time
        tier, feature = self._extract_tier_and_feature(test)
        desc = test.shortDescription() or test._testMethodName

        record = TestCaseRecord(test.id(), tier, feature, desc)
        record.status = "FAIL"
        record.duration = duration
        record.message = str(err[1])
        record.traceback = self._exc_info_to_string(err, test)
        self.records.append(record)

        if self.verbose:
            sys.stdout.write(f"{RED}FAIL{RESET} ({duration:.3f}s)\n")
            sys.stdout.flush()

    def addError(self, test: unittest.TestCase, err):
        super().addError(test, err)
        duration = time.perf_counter() - self._current_start_time
        tier, feature = self._extract_tier_and_feature(test)
        desc = test.shortDescription() or test._testMethodName

        record = TestCaseRecord(test.id(), tier, feature, desc)
        record.status = "ERROR"
        record.duration = duration
        record.message = str(err[1])
        record.traceback = self._exc_info_to_string(err, test)
        self.records.append(record)

        if self.verbose:
            sys.stdout.write(f"{RED}ERROR{RESET} ({duration:.3f}s)\n")
            sys.stdout.flush()

    def addSkip(self, test: unittest.TestCase, reason: str):
        super().addSkip(test, reason)
        duration = time.perf_counter() - self._current_start_time
        tier, feature = self._extract_tier_and_feature(test)
        desc = test.shortDescription() or test._testMethodName

        record = TestCaseRecord(test.id(), tier, feature, desc)
        record.duration = duration
        record.message = reason

        if self.strict:
            record.status = "FAIL"
            # Promote to failure in strict mode
            self.failures.append((test, reason))
            if self.verbose:
                sys.stdout.write(f"{RED}FAIL [STRICT SKIP PROMOTED]{RESET} ({reason})\n")
                sys.stdout.flush()
        else:
            record.status = "SKIP"
            if self.verbose:
                sys.stdout.write(f"{YELLOW}SKIP{RESET} ({reason})\n")
                sys.stdout.flush()

        self.records.append(record)


class PeelOffTestRunner:
    """CLI Test Runner discovering test suites, executing tests, and producing dual reports."""

    def __init__(
        self,
        tier: Optional[int] = None,
        feature: Optional[str] = None,
        strict: bool = False,
        verbose: bool = False,
        json_path: Optional[str] = None,
        report_path: Optional[str] = None,
    ):
        self.tier = tier
        self.feature = feature.upper() if feature else None
        self.strict = strict
        self.verbose = verbose
        self.json_path = json_path or get_workspace_path("tests", "e2e", "test_summary.json")
        self.report_path = report_path or get_workspace_path("tests", "e2e", "test_report.md")

        if self.strict:
            set_strict_mode(True)

    def discover_suite(self) -> unittest.TestSuite:
        """Discover and filter test cases based on CLI arguments."""
        loader = unittest.TestLoader()
        e2e_dir = get_workspace_path("tests", "e2e")

        tier_file_map = {
            1: "test_tier1_feature_coverage.py",
            2: "test_tier2_boundary_corner.py",
            3: "test_tier3_cross_feature.py",
            4: "test_tier4_real_world.py",
        }

        suites_to_load = []
        if self.tier is not None:
            if self.tier in tier_file_map:
                suites_to_load.append(tier_file_map[self.tier])
            else:
                raise ValueError(f"Invalid tier {self.tier}. Valid tiers are 1, 2, 3, 4.")
        else:
            suites_to_load = list(tier_file_map.values())

        full_suite = unittest.TestSuite()
        for filename in suites_to_load:
            module_path = os.path.join(e2e_dir, filename)
            if os.path.exists(module_path):
                module_name = f"tests.e2e.{filename[:-3]}"
                try:
                    mod_suite = loader.loadTestsFromName(module_name)
                    full_suite.addTests(mod_suite)
                except Exception as exc:
                    print(f"{RED}Error loading module {module_name}: {exc}{RESET}")

        # Apply feature filtering if requested
        if self.feature:
            import re
            m = re.match(r"^F?(\d+)$", self.feature.strip(), re.IGNORECASE)
            if m:
                feat_num = m.group(1)
                feat_pattern = re.compile(
                    rf"(?:Tier\d+F{feat_num}(?!\d)|_f{feat_num}(?:_|[A-Z]|$))",
                    re.IGNORECASE,
                )
            else:
                feat_pattern = re.compile(
                    rf"(?<![a-zA-Z0-9]){re.escape(self.feature.strip())}(?![0-9])",
                    re.IGNORECASE,
                )

            filtered_suite = unittest.TestSuite()
            for test in self._flatten_suite(full_suite):
                test_id = test.id()
                class_name = test.__class__.__name__
                if feat_pattern.search(class_name) or feat_pattern.search(test_id):
                    filtered_suite.addTest(test)
            return filtered_suite

        return full_suite

    def _flatten_suite(self, suite: unittest.TestSuite) -> List[unittest.TestCase]:
        tests = []
        for item in suite:
            if isinstance(item, unittest.TestSuite):
                tests.extend(self._flatten_suite(item))
            elif isinstance(item, unittest.TestCase):
                tests.append(item)
        return tests

    def run(self) -> int:
        """Execute test run, print summary table, generate reports, and return exit code."""
        print(f"\n{BOLD}{CYAN}========================================================================================{RESET}")
        print(f"{BOLD}{CYAN}               PeelOff Trinidad & Tobago Sticker Redesign E2E Test Suite               {RESET}")
        print(f"{BOLD}{CYAN}========================================================================================{RESET}")
        mode_str = f"{RED}STRICT (Release Gate){RESET}" if self.strict else f"{GREEN}PROGRESSIVE (Dev Mode){RESET}"
        print(f" Execution Mode: {mode_str}")
        if self.tier:
            print(f" Filter Tier:    Tier {self.tier}")
        if self.feature:
            print(f" Filter Feature: {self.feature}")
        print(f" Timestamp:      {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}\n")

        suite = self.discover_suite()
        total_discovered = suite.countTestCases()
        print(f" Discovered {BOLD}{total_discovered}{RESET} test cases.\n")

        result = PeelOffTestResult(strict=self.strict, verbose=self.verbose)
        start_time = time.perf_counter()
        suite.run(result)
        total_duration = time.perf_counter() - start_time

        # Print colorized summary table
        self._print_summary_table(result, total_duration)

        # Generate test_summary.json and test_report.md
        summary_data = self._generate_summary_data(result, total_duration)
        self._write_json_summary(summary_data)
        self._write_markdown_report(summary_data)

        # Compute exit code
        passed = len([r for r in result.records if r.status == "PASS"])
        failed = len([r for r in result.records if r.status in ("FAIL", "ERROR")])
        skipped = len([r for r in result.records if r.status == "SKIP"])

        if failed > 0:
            print(f"\n{BOLD}{RED}OVERALL STATUS: FAILED ({failed} failures/errors, {skipped} skipped){RESET}")
            return 1
        elif self.strict and skipped > 0:
            print(f"\n{BOLD}{RED}OVERALL STATUS: FAILED ({skipped} skips treated as failures in strict mode){RESET}")
            return 1
        else:
            print(f"\n{BOLD}{GREEN}OVERALL STATUS: PASSED ({passed} passed, {skipped} skipped){RESET}")
            return 0

    def _print_summary_table(self, result: PeelOffTestResult, total_duration: float):
        print(f"{BOLD}----------------------------------------------------------------------------------------{RESET}")
        print(f"{BOLD}{'Tier / Feature Category':<45} {'Total':>7} {'Pass':>7} {'Fail':>7} {'Skip':>7} {'Time':>9}{RESET}")
        print(f"{BOLD}----------------------------------------------------------------------------------------{RESET}")

        # Tier 1 breakdown by feature
        t1_records = [r for r in result.records if r.tier == 1]
        if t1_records:
            t1_pass = len([r for r in t1_records if r.status == "PASS"])
            t1_fail = len([r for r in t1_records if r.status in ("FAIL", "ERROR")])
            t1_skip = len([r for r in t1_records if r.status == "SKIP"])
            t1_time = sum(r.duration for r in t1_records)
            print(f"{BOLD}Tier 1: Feature Coverage (Category-Part.){RESET}       {len(t1_records):>7} {GREEN}{t1_pass:>7}{RESET} {RED if t1_fail else DIM}{t1_fail:>7}{RESET} {YELLOW if t1_skip else DIM}{t1_skip:>7}{RESET} {t1_time:>8.2f}s")

            feature_names = {
                "F1": "Cultural Reference Guide",
                "F2": "Authentic Motion Primitives",
                "F3": "Individualized Rig Mapping",
                "F4": "Micro-Motion Hold & Frames",
                "F5": "Production Asset Generation",
                "F6": "Automated Animation Verifier",
                "F7": "Web App Animated Integration",
                "F8": "WhatsApp Manifest Alignment",
                "F9": "Comprehensive E2E Test Suite",
                "F10": "Adversarial Coverage Hardening",
            }

            for fid in [f"F{i}" for i in range(1, 11)]:
                f_recs = [r for r in t1_records if r.feature == fid]
                if f_recs:
                    f_pass = len([r for r in f_recs if r.status == "PASS"])
                    f_fail = len([r for r in f_recs if r.status in ("FAIL", "ERROR")])
                    f_skip = len([r for r in f_recs if r.status == "SKIP"])
                    f_time = sum(r.duration for r in f_recs)
                    label = f"  {fid}: {feature_names.get(fid, fid)}"
                    skip_note = " (Pending)" if f_skip == len(f_recs) else ""
                    print(f"{label:<45} {len(f_recs):>7} {GREEN}{f_pass:>7}{RESET} {RED if f_fail else DIM}{f_fail:>7}{RESET} {YELLOW if f_skip else DIM}{f_skip:>7}{RESET} {f_time:>8.2f}s{skip_note}")

        # Tier 2
        t2_records = [r for r in result.records if r.tier == 2]
        if t2_records:
            t2_pass = len([r for r in t2_records if r.status == "PASS"])
            t2_fail = len([r for r in t2_records if r.status in ("FAIL", "ERROR")])
            t2_skip = len([r for r in t2_records if r.status == "SKIP"])
            t2_time = sum(r.duration for r in t2_records)
            print(f"{BOLD}Tier 2: Boundary & Corner Cases (BVA){RESET}         {len(t2_records):>7} {GREEN}{t2_pass:>7}{RESET} {RED if t2_fail else DIM}{t2_fail:>7}{RESET} {YELLOW if t2_skip else DIM}{t2_skip:>7}{RESET} {t2_time:>8.2f}s")

        # Tier 3
        t3_records = [r for r in result.records if r.tier == 3]
        if t3_records:
            t3_pass = len([r for r in t3_records if r.status == "PASS"])
            t3_fail = len([r for r in t3_records if r.status in ("FAIL", "ERROR")])
            t3_skip = len([r for r in t3_records if r.status == "SKIP"])
            t3_time = sum(r.duration for r in t3_records)
            print(f"{BOLD}Tier 3: Cross-Feature Interactions{RESET}            {len(t3_records):>7} {GREEN}{t3_pass:>7}{RESET} {RED if t3_fail else DIM}{t3_fail:>7}{RESET} {YELLOW if t3_skip else DIM}{t3_skip:>7}{RESET} {t3_time:>8.2f}s")

        # Tier 4
        t4_records = [r for r in result.records if r.tier == 4]
        if t4_records:
            t4_pass = len([r for r in t4_records if r.status == "PASS"])
            t4_fail = len([r for r in t4_records if r.status in ("FAIL", "ERROR")])
            t4_skip = len([r for r in t4_records if r.status == "SKIP"])
            t4_time = sum(r.duration for r in t4_records)
            print(f"{BOLD}Tier 4: Real-World Workflows & Pipelines{RESET}      {len(t4_records):>7} {GREEN}{t4_pass:>7}{RESET} {RED if t4_fail else DIM}{t4_fail:>7}{RESET} {YELLOW if t4_skip else DIM}{t4_skip:>7}{RESET} {t4_time:>8.2f}s")

        # Grand Total
        total_count = len(result.records)
        total_pass = len([r for r in result.records if r.status == "PASS"])
        total_fail = len([r for r in result.records if r.status in ("FAIL", "ERROR")])
        total_skip = len([r for r in result.records if r.status == "SKIP"])

        print(f"{BOLD}========================================================================================{RESET}")
        print(f"{BOLD}{'TOTAL':<45} {total_count:>7} {GREEN}{total_pass:>7}{RESET} {RED if total_fail else DIM}{total_fail:>7}{RESET} {YELLOW if total_skip else DIM}{total_skip:>7}{RESET} {total_duration:>8.2f}s{RESET}")
        print(f"{BOLD}========================================================================================{RESET}")

    def _generate_summary_data(self, result: PeelOffTestResult, total_duration: float) -> Dict[str, Any]:
        total_count = len(result.records)
        passed = len([r for r in result.records if r.status == "PASS"])
        failed = len([r for r in result.records if r.status in ("FAIL", "ERROR")])
        skipped = len([r for r in result.records if r.status == "SKIP"])

        failures_list = []
        for r in result.records:
            if r.status in ("FAIL", "ERROR"):
                failures_list.append({
                    "test_id": r.test_id,
                    "tier": r.tier,
                    "feature": r.feature,
                    "description": r.description,
                    "message": r.message,
                    "traceback": r.traceback,
                })

        by_tier = {}
        for t in [1, 2, 3, 4]:
            t_recs = [r for r in result.records if r.tier == t]
            if t_recs:
                by_tier[f"tier_{t}"] = {
                    "total": len(t_recs),
                    "passed": len([r for r in t_recs if r.status == "PASS"]),
                    "failed": len([r for r in t_recs if r.status in ("FAIL", "ERROR")]),
                    "skipped": len([r for r in t_recs if r.status == "SKIP"]),
                    "duration_seconds": round(sum(r.duration for r in t_recs), 3),
                }

        by_feature = {}
        for i in range(1, 11):
            fid = f"F{i}"
            f_recs = [r for r in result.records if r.feature == fid]
            if f_recs:
                by_feature[fid] = {
                    "total": len(f_recs),
                    "passed": len([r for r in f_recs if r.status == "PASS"]),
                    "failed": len([r for r in f_recs if r.status in ("FAIL", "ERROR")]),
                    "skipped": len([r for r in f_recs if r.status == "SKIP"]),
                    "duration_seconds": round(sum(r.duration for r in f_recs), 3),
                }

        return {
            "version": "1.0.0",
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "strict_mode": self.strict,
            "filter_tier": self.tier,
            "filter_feature": self.feature,
            "summary": {
                "total": total_count,
                "passed": passed,
                "failed": failed,
                "skipped": skipped,
                "duration_seconds": round(total_duration, 3),
                "status": "FAILED" if failed > 0 or (self.strict and skipped > 0) else "PASSED",
                "exit_code": 1 if failed > 0 or (self.strict and skipped > 0) else 0,
            },
            "by_tier": by_tier,
            "by_feature": by_feature,
            "failures": failures_list,
            "tests": [r.to_dict() for r in result.records],
        }

    def _write_json_summary(self, data: Dict[str, Any]):
        dir_name = os.path.dirname(self.json_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _write_markdown_report(self, data: Dict[str, Any]):
        dir_name = os.path.dirname(self.report_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        s = data["summary"]
        lines = [
            "# PeelOff E2E Test Suite Execution Report",
            f"**Timestamp**: {data['timestamp']}  ",
            f"**Execution Mode**: {'STRICT' if data['strict_mode'] else 'PROGRESSIVE'}  ",
            f"**Overall Status**: **{s['status']}** (Exit Code {s['exit_code']})  ",
            f"**Total Duration**: {s['duration_seconds']:.2f} seconds  ",
            "",
            "## Summary Metrics",
            f"- **Total Tests Executed**: {s['total']}",
            f"- **Passed**: {s['passed']}",
            f"- **Failed / Errors**: {s['failed']}",
            f"- **Skipped (Pending Milestones)**: {s['skipped']}",
            "",
            "## Results by Tier",
            "| Tier | Name | Total | Passed | Failed | Skipped | Duration |",
            "|---|---|---|---|---|---|---|",
        ]

        tier_names = {
            "tier_1": "Tier 1: Feature Coverage",
            "tier_2": "Tier 2: Boundary & Corner Cases",
            "tier_3": "Tier 3: Cross-Feature Interactions",
            "tier_4": "Tier 4: Real-World Scenarios",
        }

        for t_key, t_data in data.get("by_tier", {}).items():
            name = tier_names.get(t_key, t_key)
            lines.append(
                f"| {t_key.replace('tier_', 'Tier ')} | {name} | {t_data['total']} | {t_data['passed']} | {t_data['failed']} | {t_data['skipped']} | {t_data['duration_seconds']}s |"
            )

        lines.extend([
            "",
            "## Results by Feature (Tier 1 & 2)",
            "| Feature | Name | Total | Passed | Failed | Skipped |",
            "|---|---|---|---|---|---|",
        ])

        feature_names = {
            "F1": "Cultural Reference Guide",
            "F2": "Authentic Motion Primitives",
            "F3": "Individualized Rig Mapping",
            "F4": "Micro-Motion Hold & Frames",
            "F5": "Production Asset Generation",
            "F6": "Automated Animation Verifier",
            "F7": "Web App Animated Integration",
            "F8": "WhatsApp Manifest Alignment",
            "F9": "Comprehensive E2E Test Suite",
            "F10": "Adversarial Coverage Hardening",
        }

        for f_key, f_data in data.get("by_feature", {}).items():
            fname = feature_names.get(f_key, f_key)
            lines.append(
                f"| {f_key} | {fname} | {f_data['total']} | {f_data['passed']} | {f_data['failed']} | {f_data['skipped']} |"
            )

        if data.get("failures"):
            lines.extend([
                "",
                "## Failures & Defects",
            ])
            for idx, fl in enumerate(data["failures"], 1):
                lines.extend([
                    f"### {idx}. {fl['test_id']}",
                    f"- **Feature**: {fl['feature']} (Tier {fl['tier']})",
                    f"- **Description**: {fl['description']}",
                    f"- **Message**: `{fl['message']}`",
                    "```",
                    fl["traceback"][:500] if fl["traceback"] else fl["message"],
                    "```",
                    "",
                ])

        with open(self.report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


def main():
    parser = argparse.ArgumentParser(
        description="PeelOff E2E Test Suite CLI Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--tier",
        type=int,
        choices=[1, 2, 3, 4],
        help="Run tests only for the specified Tier (1: Feature Coverage, 2: Boundary, 3: Cross, 4: Real-World)",
    )
    parser.add_argument(
        "--feature",
        type=str,
        help="Filter tests by feature identifier (F1 through F10)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Strict gating mode: treat progressive skips as failures (for Milestone M5 release)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output showing individual test method execution",
    )
    parser.add_argument(
        "--json",
        type=str,
        dest="json_path",
        help="Output path for machine-readable test summary JSON (default: tests/e2e/test_summary.json)",
    )
    parser.add_argument(
        "--report",
        type=str,
        dest="report_path",
        help="Output path for Markdown test execution report (default: tests/e2e/test_report.md)",
    )

    args = parser.parse_args()

    runner = PeelOffTestRunner(
        tier=args.tier,
        feature=args.feature,
        strict=args.strict,
        verbose=args.verbose,
        json_path=args.json_path,
        report_path=args.report_path,
    )

    try:
        exit_code = runner.run()
        sys.exit(exit_code)
    except ValueError as exc:
        print(f"{RED}Argument Error: {exc}{RESET}")
        sys.exit(2)
    except Exception as exc:
        print(f"{RED}Execution Error: {exc}{RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
