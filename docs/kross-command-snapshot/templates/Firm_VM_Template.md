# Firm VM Template

Use one VM per firm.

## VM Naming

Recommended pattern:

```text
firm-slug-office
```

Examples:

```text
returns-revenue-office
example-tax-office
```

## Default VM Resources

Pilot defaults:

- OS: Ubuntu Server 24.04 LTS
- CPU: 4 cores
- RAM: 16 GB
- Disk: 150 GB
- Network: private Proxmox bridge/NAT unless public exposure is intentionally designed

Adjust based on firm usage.

## Required Agent Setup

Each firm VM needs:

- Hermes installed
- dedicated Hermes profile for that firm's Kross Agent
- firm-specific workspace
- firm-specific `SOUL.md`
- firm-specific `AGENTS.md`
- Kross Agent SOP snapshot
- firm access inventory
- firm-owned model provider access by default

## Isolation Rule

Never reuse:

- another firm's workspace
- another firm's credentials
- another firm's provider account
- another firm's client data
- another firm's browser session
