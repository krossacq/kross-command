# Kross Slack Gateway

Socket Mode Slack gateway for routing firm Slack channels to firm-specific
Kross Agent VMs.

For the pilot:

- One Slack app: `Kross Agent`
- One private Slack channel: Returns and Revenue Office Kross channel
- One firm VM: `returns-revenue-office-vm`
- One firm-owned model provider configured inside that VM

The Slack app is only the communication channel. AI usage is billed through the
model provider configured inside the destination firm's VM.

## Server Files

Production pilot path:

```text
/opt/kross/slack-gateway
```

Required secret file:

```text
/opt/kross/slack-gateway/.env
```

Required non-secret route file:

```text
/opt/kross/slack-gateway/routes.json
```

## Environment

```bash
SLACK_BOT_TOKEN=xoxb-...
SLACK_APP_TOKEN=xapp-...
KROSS_ROUTES_FILE=/opt/kross/slack-gateway/routes.json
```

Do not commit `.env` or any Slack/OpenAI/provider token.

## Route Format

```json
{
  "C0123456789": {
    "firm_name": "Returns and Revenue Office",
    "vm_host": "sydne@10.10.10.10",
    "ssh_key": "/root/.ssh/kross_proxmox_to_returns_vm",
    "agent_command": "/home/sydne/.local/bin/krossagent-stdin",
    "workspace": "/home/sydne/Returns-and-Revenue-Office/Kross-Agent-Workspace"
  }
}
```

Each Slack channel maps to exactly one VM. This is the tenant boundary for the
Slack gateway MVP.

## Local Commands

Run manually on the Proxmox host:

```bash
cd /opt/kross/slack-gateway
./venv/bin/python gateway.py
```

With systemd:

```bash
systemctl status kross-slack-gateway
journalctl -u kross-slack-gateway -f
```

