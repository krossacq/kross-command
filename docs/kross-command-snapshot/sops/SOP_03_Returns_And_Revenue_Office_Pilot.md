# SOP 03: Returns And Revenue Office Pilot

Version: 0.1
Owner: Tax Mogul Bureau
Applies to: Kross Command

## Purpose

Define the active pilot setup for Returns and Revenue Office.

## Current Status

Returns and Revenue Office has:

- Hetzner dedicated server
- Debian 13 host
- Proxmox installed
- Ubuntu VM named `returns-revenue-office`
- private VM IP `10.10.10.10`
- internet access confirmed
- Hermes installed inside the VM
- initial Nous Portal setup completed

## Next Steps

1. Finish Kross Agent profile setup inside the VM.
2. Add Kross Agent `SOUL.md`.
3. Add Kross Agent workspace `AGENTS.md`.
4. Clone/pull the Kross Agent snapshot repo.
5. Copy SOP snapshot into the VM workspace.
6. Test Kross Agent can read and summarize its operating instructions.
7. Decide whether to switch provider from the free Nous model to OpenAI/ChatGPT OAuth for pilot usage.
8. Add Slack after VM Kross Agent behavior is stable.

## Pilot Exception

Returns and Revenue Office may use Sydne/Tax Mogul provider access because it is Sydne's own tax office.

Future firms should authorize their own provider access unless a separate AI-included plan is created.

## Acceptance Criteria

The pilot is ready for testing when Kross Agent can run inside the VM, read its workspace instructions, retrieve its SOP snapshot, and answer within Returns and Revenue Office boundaries.
