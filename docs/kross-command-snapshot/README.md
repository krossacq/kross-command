# Kross Command Snapshot

Kross Command is the bureau-level setup, infrastructure, deployment, and support agent for The Tax Mogul Bureau.

This snapshot is separate from Kross Agent.

## Difference Between Kross Command And Kross Agent

Kross Command:

- builds and maintains Kross Agent environments
- helps create Proxmox/VM setups
- manages setup runbooks and deployment templates
- supports firm onboarding infrastructure
- helps troubleshoot Kross Agent environments
- may support multiple firm environments through approved support access

Kross Agent:

- lives inside one firm's workspace/VM
- helps that firm with tax office operations
- drafts call summaries, messages, tasks, memory updates, and data-entry staging
- must stay scoped to one firm/client context

## Snapshot Contents

- `profile/SOUL.md`: Kross Command persona and operating boundaries
- `workspace/AGENTS.md`: workspace-level instructions
- `runbooks/`: infrastructure and pilot setup runbooks
- `templates/`: VM and access inventory templates
- `sops/`: Kross Command operating SOPs

## Current Pilot

The active pilot is Returns and Revenue Office.

Current target architecture:

```text
Hetzner dedicated server
-> Debian 13
-> Proxmox VE
-> Ubuntu VM: returns-revenue-office
-> Hermes
-> Kross Agent for Returns and Revenue Office
-> Slack channel: #returns-revenue-kross
```

## Slack MVP

The first Slack MVP is live for Returns and Revenue Office:

- Slack app: Kross Agent
- Slack channel: `#returns-revenue-kross`
- Gateway service: `kross-slack-gateway`
- Route pattern: Slack channel -> Proxmox -> firm VM -> firm `krossagent`

Future firms should use the same communication pattern while powering the
agent from their own model provider/subscription by default.

## Model Provider Rule

Returns and Revenue Office may use Sydne/Tax Mogul provider access as the pilot exception.

Future firms should use their own approved AI/model provider subscription by default unless Tax Mogul Bureau creates a separate AI-included plan with usage tracking.

## Security Rule

Do not store credentials, API keys, OAuth tokens, MFA codes, recovery codes, passwords, or client-sensitive tax documents in this repo.
