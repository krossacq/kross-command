# Returns and Revenue Office VM Setup Status

Last updated: 2026-07-06

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

## Current Next Steps

1. Configure Kross Agent profile inside the Ubuntu VM.
2. Create the VM Kross Agent workspace.
3. Clone/pull the `krossacq/kross-agent` snapshot.
4. Copy SOP snapshot into the VM workspace.
5. Add Kross Agent `SOUL.md` and `AGENTS.md`.
6. Test `krossagent` can read workspace instructions.
7. Switch VM provider from free Nous model to the intended OpenAI/ChatGPT provider if needed.
8. Add Slack communication after the VM-based Kross Agent is stable.

## SSH Access Pattern

From the Mac:

```bash
ssh -J root@PROXMOX_HOST_IP sydne@10.10.10.10
```

Do not write the host password or VM password in this file.

## Provider Rule

Returns and Revenue Office may use Sydne/Tax Mogul provider access as the pilot exception.

Future firms should provide and authorize their own model provider/subscription unless Tax Mogul offers a separate AI-included plan with usage tracking.
