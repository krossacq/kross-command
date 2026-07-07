# SOP 01: Firm VM Deployment Runbook

Version: 0.1
Owner: Tax Mogul Bureau
Applies to: Kross Command

## Purpose

Define the repeatable high-level process for deploying a firm VM for Kross Agent.

## Standard Architecture

```text
Hetzner dedicated server
-> Debian host
-> Proxmox VE
-> one Ubuntu VM per firm
-> one Kross Agent profile/workspace per firm VM
```

## Deployment Steps

1. Confirm the firm is approved for Kross Agent setup.
2. Confirm VM name and firm slug.
3. Create or clone the firm VM in Proxmox.
4. Assign resources based on the current VM template.
5. Configure private networking.
6. Install or verify Ubuntu.
7. Confirm SSH access.
8. Install required base packages.
9. Install Hermes.
10. Configure the firm-specific Kross Agent profile.
11. Add `SOUL.md` and `AGENTS.md`.
12. Add the Kross Agent SOP snapshot.
13. Configure model provider access according to the firm-owned provider rule.
14. Test the agent can read workspace instructions.
15. Complete launch readiness checks before live client work.

## Safety Rules

- Do not reuse another firm's workspace.
- Do not reuse another firm's credentials.
- Do not reuse another firm's model provider account.
- Do not expose the VM publicly unless network security is intentionally designed.
- Do not process live client data until launch readiness passes.

## Acceptance Criteria

This SOP is working when a new firm VM can be created and prepared for Kross Agent using documented, repeatable steps.
