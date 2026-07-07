# SOP 04: Slack Channel To Firm VM Routing

## Purpose

Create a repeatable, secure Slack communication path from a private firm Slack
channel to that firm's Kross Agent VM.

This SOP preserves the core Kross Agent boundary:

```text
Slack app = communication channel
Firm VM = agent runtime
Firm model provider = AI billing/power source
```

## Scope

Use this SOP after:

- the firm's VM exists,
- the VM has a working `krossagent` launcher,
- the VM has a configured firm-owned model provider, and
- SSH from the Proxmox host to the VM works by key.

## Required Inputs

- Slack workspace name
- Firm private Slack channel name
- Slack channel ID
- Firm name
- VM private SSH host, such as `sydne@10.10.10.10`
- Proxmox-to-VM SSH key path
- VM Kross Agent command path
- VM Kross Agent workspace path

Do not store Slack tokens, OpenAI/API keys, passwords, OAuth codes, or recovery
codes in GitHub, Slack, runbooks, or workspace files.

## Human Setup Steps

1. Create the firm's private Slack channel.
2. Invite the approved firm users.
3. Invite the `Kross Agent` Slack app to the channel.
4. Confirm the Slack app has a bot token and app-level Socket Mode token stored
   securely on the Proxmox host.
5. Confirm the firm VM model provider is configured inside the firm VM and is
   owned by the firm unless an AI-included Tax Mogul plan is explicitly used.

## Gateway Route

Add one route per approved firm channel in:

```bash
/opt/kross/slack-gateway/routes.json
```

Example:

```json
{
  "C0123456789": {
    "firm_name": "Example Tax Firm",
    "vm_host": "firmuser@10.10.10.20",
    "ssh_key": "/root/.ssh/kross_proxmox_to_example_firm_vm",
    "agent_command": "/home/firmuser/.local/bin/krossagent-stdin",
    "workspace": "/home/firmuser/Example-Firm/Kross-Agent-Workspace"
  }
}
```

Each channel must map to exactly one firm VM for the MVP.

## Validation

After adding the route:

1. Restart the gateway:

   ```bash
   systemctl restart kross-slack-gateway
   ```

2. Confirm service health:

   ```bash
   systemctl status kross-slack-gateway --no-pager
   ```

3. In the firm's private Slack channel, mention Kross Agent:

   ```text
   @Kross Agent Read AGENTS.md and summarize your operating instructions in 5 bullets.
   ```

4. Confirm Kross Agent answers from the correct firm VM.
5. Confirm the response reflects the correct firm scope and does not identify as
   Kross Command.

## MVP Boundaries

- Only approved mapped channels may operate Kross Agent.
- Slack DMs are blocked unless a future routing rule explicitly permits them.
- Unmapped channels must receive a setup-required message.
- Client-facing sends, memory updates, software actions, and tax workflow
  changes remain drafts until human approval.
- The gateway must not route one firm's Slack channel to another firm's VM.

## Future Firm Billing Rule

For future firms, Kross Command must confirm that the firm's Kross Agent VM uses
that firm's own model provider/subscription before enabling Slack production
use.

Tax Mogul may use its own provider only for:

- internal testing,
- Returns and Revenue Office pilot use, or
- a separately priced AI-included plan with usage tracking and explicit approval.

