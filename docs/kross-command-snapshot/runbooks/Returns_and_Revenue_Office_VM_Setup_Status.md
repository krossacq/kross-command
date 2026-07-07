# Returns and Revenue Office VM Setup Status

Last updated: 2026-07-07

## Completed

- Hetzner dedicated server ordered and activated.
- Server reinstalled from Ubuntu to Debian 13.
- Proxmox installed on Debian host.
- Proxmox dashboard reachable at the host IP on port `8006`.
- Private NAT bridge `vmbr1` created.
- Ubuntu VM created:
  - VM name: `returns-revenue-office`
  - private IP: `10.10.10.10`
  - SSH access path: Mac -> Proxmox host -> Ubuntu VM
- Ubuntu VM has internet access.
- Hermes installed inside the Ubuntu VM.
- Nous Portal setup completed for pilot testing.
- Proxmox host key-based SSH access verified from the Mac:
  - host IP: `65.109.93.216`
  - hostname: `kross-proxmox`
  - OS: Debian GNU/Linux 13 (trixie)
  - Proxmox: `pve-manager/9.2.4`
- VM verified from Proxmox:
  - VMID: `100`
  - name: `returns-revenue-office`
  - status: running
  - SSH port open at `10.10.10.10:22`
- Approved SSH aliases verified from Kross Command:
  - Proxmox host: `kross-proxmox` as `root`
  - Ubuntu VM: `returns-revenue-office-vm` as `sydne`
- Kross Agent profile created inside the Ubuntu VM:
  - Hermes profile: `krossagent`
  - profile SOUL: `/home/sydne/.hermes/profiles/krossagent/SOUL.md`
- Kross Agent workspace created inside the Ubuntu VM:
  - workspace: `/home/sydne/Returns-and-Revenue-Office/Kross-Agent-Workspace`
  - workspace instructions: `/home/sydne/Returns-and-Revenue-Office/Kross-Agent-Workspace/AGENTS.md`
  - repo clone: `/home/sydne/Returns-and-Revenue-Office/Kross-Agent-Workspace/kross-agent`
  - SOP snapshot: `/home/sydne/Returns-and-Revenue-Office/Kross-Agent-Workspace/Kross-Agent-SOPs`
  - SOP markdown files verified: `70`
- VM-local launcher created:
  - command path: `/home/sydne/.local/bin/krossagent`
  - usage: `krossagent "Read AGENTS.md and summarize your operating instructions."`
- Slack MVP communication channel completed:
  - Slack workspace: The Tax Mogul
  - Slack app: Kross Agent
  - Slack channel: `#returns-revenue-kross`
  - Slack channel ID: `C0BFT5J4V1A`
  - Slack gateway host path: `/opt/kross/slack-gateway`
  - Slack gateway service: `kross-slack-gateway`
  - Slack route: `#returns-revenue-kross` -> Proxmox host -> Returns and Revenue Office VM -> `krossagent`
  - Slack mention test passed.

## Final Pilot Setup Status

- Proxmox host SSH key access works through alias `kross-proxmox`.
- VM SSH access works through alias `returns-revenue-office-vm`.
- Kross Agent profile/workspace/SOP snapshot/launcher are present inside the VM.
- VM `krossagent` model provider configuration is complete.
- VM `krossagent` smoke test passed with non-client/sample instructions.
- Slack gateway is installed, running, and mapped to the Returns and Revenue Office Kross Agent VM.

Smoke test command:

```bash
krossagent "Read AGENTS.md and summarize your operating instructions. Also confirm whether you are Kross Agent or Kross Command, whether you are scoped only to Returns and Revenue Office, whether drafts require human approval, and whether you can see the SOP snapshot index path."
```

Result summary: provider was configured inside the VM, and the smoke test passed. Kross Agent confirmed the Returns and Revenue Office firm scope, the Kross Agent versus Kross Command boundary, human approval requirements, and access to the SOP snapshot/index path.

No provider secrets, API keys, OAuth codes, recovery codes, or passwords are stored in this runbook.

Slack tokens are stored only on the Proxmox host in:

```bash
/opt/kross/slack-gateway/.env
```

The Slack channel route file is stored on the Proxmox host in:

```bash
/opt/kross/slack-gateway/routes.json
```

## Pilot Readiness

The Returns and Revenue Office VM-based Kross Agent environment is ready for controlled pilot use, subject to the normal operational boundaries below:

1. Use the VM-scoped `krossagent` profile and workspace for Returns and Revenue Office only.
2. Use sample/non-client data for any additional dry runs unless live client work is explicitly authorized.
3. Require human approval before client-facing messages, operational updates, sends, or memory changes.
4. Keep provider credentials and secrets out of chat, runbooks, GitHub, and workspace files.
5. Use Slack only through approved firm channels mapped to the correct firm VM.
6. Do not allow Slack DMs or unmapped Slack channels to operate Kross Agent during the MVP.

## Remaining Optional Follow-Up

1. Run realistic non-client/sample workflow tests through Slack.
2. Create a recurring pilot support/checklist process if Returns and Revenue Office wants scheduled readiness checks.
3. Decide whether Slack DMs should remain blocked or be added later with explicit firm/user routing rules.

## SSH Access Pattern

From the Mac:

```bash
ssh -J root@PROXMOX_HOST_IP sydne@10.10.10.10
```

Approved aliases now available from Kross Command:

```bash
ssh kross-proxmox
ssh returns-revenue-office-vm
```

Verified host value:

```bash
ssh -J root@65.109.93.216 sydne@10.10.10.10
```

Do not write the host password or VM password in this file.

## Provider Rule

Returns and Revenue Office may use Sydne/Tax Mogul provider access as the pilot exception.

Future firms should provide and authorize their own model provider/subscription unless Tax Mogul offers a separate AI-included plan with usage tracking.

## Slack Provider/Billing Boundary

The Slack app is only the communication channel. Slack does not pay for the AI model.

For the MVP, each firm VM must have its own Kross Agent model provider configured inside that VM. That provider should belong to the firm unless Tax Mogul explicitly sells and tracks an AI-included plan.

The intended future-firm pattern is:

```text
One Kross Slack app
One private Slack channel per firm
One Kross Agent VM per firm
One firm-owned model provider/subscription per VM
```

This prevents another firm's Kross Agent usage from running on Tax Mogul's provider bill by default.
