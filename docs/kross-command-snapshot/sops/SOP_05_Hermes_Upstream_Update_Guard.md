# SOP 05 — Hermes Upstream Update Guard

## Purpose

Keep Kross Command aware of Hermes upstream releases without allowing an
untested release to modify the live Tax Mogul environment.

## Schedule

The macOS LaunchAgent `com.taxmogul.kross-command-hermes-guard` runs daily at
06:17 local time and once when loaded. It is independent of the Hermes gateway,
so the watcher still runs if Hermes cron or the gateway is unavailable.

macOS does not grant background LaunchAgents access to the user's `Documents`
folder. The installed runtime and a credential-free Kross overlay snapshot live
under the Kross Command profile's guard directory. Refresh that snapshot after
changing Kross-owned overlays or security policies.

## Behavior

1. Fetch the official `NousResearch/hermes-agent` `main` branch.
2. Exit silently when the upstream commit is unchanged.
3. Export a disposable candidate when upstream changes.
4. Overlay only Kross-owned documentation and Slack gateway files.
5. Validate required Hermes paths, compile the Slack gateway, scan the overlay
   for credentials, confirm security-policy markers, and audit the live Hermes
   runtime.
6. Record critical upstream paths that changed and write a compatibility report.
7. Preserve the live Hermes checkout. The watcher never deploys or restarts it.

## Reports

Reports and candidate trees are stored under:

```text
~/.hermes/profiles/krosscommand/security/hermes-upstream-guard/
```

`latest.md` is the current report. Only the three newest candidates are kept.

## Status meanings

- `CANDIDATE_PASSED`: deterministic guard checks passed and no critical paths changed.
- `READY_FOR_REVIEW`: no blocking failure, but upstream touched a critical path or
  the live runtime has an advisory requiring review.
- `BLOCKED`: candidate construction, Kross contracts, security policy, credential
  scanning, or another required check failed.

None of these statuses deploy automatically. Before promotion, run the complete
Hermes tests, dependency audits, Kross Promptfoo suite, and a canary deployment
with rollback available.

## Manual commands

```bash
python3 automation/install_hermes_upstream_guard.py

launchctl kickstart -k gui/$(id -u)/com.taxmogul.kross-command-hermes-guard
launchctl print gui/$(id -u)/com.taxmogul.kross-command-hermes-guard

python3 automation/hermes_upstream_guard.py \
  --repo "$PWD" \
  --force
```

## Failure response

Do not run `hermes update` against production to clear a guard failure. Review
`latest.md`, repair or reconcile the isolated candidate, run all promotion gates,
and deploy only from an approved Kross release with a current backup.
