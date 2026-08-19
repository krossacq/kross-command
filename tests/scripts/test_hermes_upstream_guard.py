from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


SCRIPT = Path(__file__).parents[2] / "automation/hermes_upstream_guard.py"
SPEC = importlib.util.spec_from_file_location("hermes_upstream_guard", SCRIPT)
assert SPEC and SPEC.loader
guard = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = guard
SPEC.loader.exec_module(guard)


def test_assessment_status_blocks_failures() -> None:
    assessment = guard.Assessment(upstream_sha="a" * 40, previous_sha=None)
    assert assessment.status == "CANDIDATE_PASSED"
    assessment.warnings.append("review")
    assert assessment.status == "READY_FOR_REVIEW"
    assessment.failures.append("blocked")
    assert assessment.status == "BLOCKED"


def test_sensitive_file_detection_is_narrow() -> None:
    assert guard.is_sensitive_file(Path(".env"))
    assert guard.is_sensitive_file(Path(".env.production"))
    assert guard.is_sensitive_file(Path("routes.json"))
    assert not guard.is_sensitive_file(Path(".env.example"))
    assert not guard.is_sensitive_file(Path("README.md"))


def test_secret_scanner_flags_credentials_but_not_examples(tmp_path: Path) -> None:
    overlay = tmp_path / "integrations/slack_gateway"
    overlay.mkdir(parents=True)
    (overlay / "README.md").write_text("SLACK_BOT_TOKEN=xoxb-...\n", encoding="utf-8")
    assert guard.scan_overlay_for_secrets(tmp_path) == []

    (overlay / "leak.txt").write_text("xoxb-123456789012345678901234\n", encoding="utf-8")
    findings = guard.scan_overlay_for_secrets(tmp_path)
    assert findings == ["Possible credential material in integrations/slack_gateway/leak.txt"]


def test_safe_remove_rejects_candidate_root(tmp_path: Path) -> None:
    root = tmp_path / "candidates"
    root.mkdir()
    try:
        guard.safe_remove_candidate(root, root)
    except RuntimeError as exc:
        assert "refusing to remove" in str(exc)
    else:
        raise AssertionError("candidate root removal should be rejected")


def test_kross_source_revision_is_stable_for_snapshot(tmp_path: Path) -> None:
    (tmp_path / "KROSS_COMMAND.md").write_text("Kross\n", encoding="utf-8")
    first = guard.kross_source_revision(tmp_path)
    second = guard.kross_source_revision(tmp_path)
    assert first == second
    assert first.startswith("snapshot:")
