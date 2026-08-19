#!/usr/bin/env python3
"""Install or refresh the Kross Hermes upstream guard on macOS."""

from __future__ import annotations

import argparse
import os
import plistlib
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Sequence


LABEL = "com.taxmogul.kross-command-hermes-guard"
SOURCE_PATHS = (
    "KROSS_COMMAND.md",
    "docs/kross-command-snapshot",
    "integrations/slack_gateway",
    "docker/SOUL.md",
)


def build_plist(guard_root: Path) -> dict[str, object]:
    return {
        "Label": LABEL,
        "ProgramArguments": [
            "/usr/bin/python3",
            str(guard_root / "runtime/hermes_upstream_guard.py"),
            "--repo",
            str(guard_root / "runtime/kross-source"),
            "--state-dir",
            str(guard_root),
        ],
        "EnvironmentVariables": {
            "PATH": (
                f"{Path.home()}/.local/bin:/opt/homebrew/bin:/usr/local/bin:"
                "/usr/bin:/bin:/usr/sbin:/sbin"
            )
        },
        "StartCalendarInterval": {"Hour": 6, "Minute": 17},
        "RunAtLoad": True,
        "ProcessType": "Background",
        "LowPriorityIO": True,
        "ThrottleInterval": 300,
        "StandardOutPath": str(guard_root / "logs/launchd.out.log"),
        "StandardErrorPath": str(guard_root / "logs/launchd.err.log"),
    }


def copy_source_snapshot(repo: Path, runtime: Path) -> None:
    for relative in SOURCE_PATHS:
        if not (repo / relative).exists():
            raise RuntimeError(f"required Kross source path is missing: {relative}")

    temporary_root = Path(tempfile.mkdtemp(prefix="kross-source-", dir=runtime))
    snapshot = temporary_root / "kross-source"
    snapshot.mkdir()
    try:
        for relative in SOURCE_PATHS:
            source = repo / relative
            destination = snapshot / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source.is_dir():
                shutil.copytree(source, destination)
            else:
                shutil.copy2(source, destination)

        installed = runtime / "kross-source"
        previous = runtime / "kross-source.previous"
        if previous.exists():
            shutil.rmtree(previous)
        if installed.exists():
            installed.replace(previous)
        snapshot.replace(installed)
        if previous.exists():
            shutil.rmtree(previous)
    finally:
        shutil.rmtree(temporary_root, ignore_errors=True)


def install(repo: Path, profile_home: Path) -> Path:
    if not (repo / ".git").exists():
        raise RuntimeError(f"not a git repository: {repo}")
    guard_root = profile_home / "security/hermes-upstream-guard"
    runtime = guard_root / "runtime"
    logs = guard_root / "logs"
    runtime.mkdir(parents=True, exist_ok=True)
    logs.mkdir(parents=True, exist_ok=True)

    guard_source = repo / "automation/hermes_upstream_guard.py"
    guard_target = runtime / "hermes_upstream_guard.py"
    shutil.copy2(guard_source, guard_target)
    guard_target.chmod(0o755)
    copy_source_snapshot(repo, runtime)

    launch_agents = Path.home() / "Library/LaunchAgents"
    launch_agents.mkdir(parents=True, exist_ok=True)
    plist_path = launch_agents / f"{LABEL}.plist"
    with plist_path.open("wb") as handle:
        plistlib.dump(build_plist(guard_root), handle, sort_keys=False)

    service = f"gui/{os.getuid()}/{LABEL}"
    domain = f"gui/{os.getuid()}"
    subprocess.run(["launchctl", "bootout", service], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["launchctl", "bootstrap", domain, str(plist_path)], check=True)
    return plist_path


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument(
        "--profile-home",
        type=Path,
        default=Path.home() / ".hermes/profiles/krosscommand",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    plist_path = install(args.repo.expanduser().resolve(), args.profile_home.expanduser().resolve())
    print(f"Installed {LABEL}: {plist_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
