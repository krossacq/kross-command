from __future__ import annotations

import json
import logging
import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


LOG_LEVEL = os.environ.get("KROSS_LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger("kross-slack-gateway")


ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[A-Za-z]")
MENTION_RE = re.compile(r"<@[A-Z0-9]+>")


@dataclass(frozen=True)
class FirmRoute:
    firm_name: str
    vm_host: str
    ssh_key: str
    agent_command: str
    workspace: str | None = None

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "FirmRoute":
        return cls(
            firm_name=str(payload["firm_name"]),
            vm_host=str(payload["vm_host"]),
            ssh_key=str(payload["ssh_key"]),
            agent_command=str(payload["agent_command"]),
            workspace=str(payload["workspace"]) if payload.get("workspace") else None,
        )


def load_routes() -> dict[str, FirmRoute]:
    route_file = Path(os.environ.get("KROSS_ROUTES_FILE", "/opt/kross/slack-gateway/routes.json"))
    if not route_file.exists():
        logger.warning("Route file does not exist: %s", route_file)
        return {}
    raw = json.loads(route_file.read_text(encoding="utf-8"))
    routes = {channel_id: FirmRoute.from_dict(route) for channel_id, route in raw.items()}
    logger.info("Loaded %s Slack channel route(s)", len(routes))
    return routes


def slack_text_to_prompt(text: str, bot_user_id: str | None) -> str:
    prompt = text or ""
    if bot_user_id:
        prompt = prompt.replace(f"<@{bot_user_id}>", "")
    prompt = MENTION_RE.sub("", prompt)
    return prompt.strip()


def clean_agent_output(output: str) -> str:
    text = ANSI_RE.sub("", output)
    lines: list[str] = []
    skip_prefixes = (
        "Query:",
        "Initializing agent",
        "Resume this session with:",
        "Session:",
        "Duration:",
        "Messages:",
    )
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith(skip_prefixes):
            continue
        if set(stripped) <= {"─", "╭", "╮", "╰", "╯", "│", " "}:
            continue
        if stripped in {"⚕ Hermes", "Hermes"}:
            continue
        lines.append(line.rstrip())
    cleaned = "\n".join(lines).strip()
    return cleaned or "Kross Agent completed, but did not return visible text."


def run_kross_agent(route: FirmRoute, prompt: str) -> str:
    ssh_cmd = [
        "ssh",
        "-i",
        route.ssh_key,
        "-o",
        "BatchMode=yes",
        "-o",
        "StrictHostKeyChecking=accept-new",
        "-o",
        "ConnectTimeout=15",
        route.vm_host,
        route.agent_command,
    ]
    logger.info("Routing Slack prompt to %s via %s", route.firm_name, route.vm_host)
    completed = subprocess.run(
        ssh_cmd,
        input=prompt,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=int(os.environ.get("KROSS_AGENT_TIMEOUT_SECONDS", "180")),
        check=False,
    )
    output = clean_agent_output(completed.stdout)
    if completed.returncode != 0:
        logger.error("Kross Agent exited with code %s: %s", completed.returncode, output)
        return (
            f"Kross Agent could not complete that request for {route.firm_name}. "
            "The technical team needs to review the VM gateway logs."
        )
    return output


load_dotenv("/opt/kross/slack-gateway/.env")

SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN", "")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN", "")
if not SLACK_BOT_TOKEN.startswith("xoxb-"):
    raise RuntimeError("SLACK_BOT_TOKEN is missing or invalid")
if not SLACK_APP_TOKEN.startswith("xapp-"):
    raise RuntimeError("SLACK_APP_TOKEN is missing or invalid")

ROUTES = load_routes()
APP = App(token=SLACK_BOT_TOKEN, request_verification_enabled=False)
BOT_USER_ID: str | None = None


@APP.event("app_mention")
def handle_app_mention(event, say):
    channel_id = event.get("channel")
    route = ROUTES.get(channel_id)
    if route is None:
        say(
            text=(
                "This Slack channel is not mapped to a Kross Agent VM yet. "
                "Ask Tax Mogul support to finish the channel-to-agent route."
            ),
            thread_ts=event.get("ts"),
        )
        return

    prompt = slack_text_to_prompt(event.get("text", ""), BOT_USER_ID)
    if not prompt:
        say(text="What would you like Kross Agent to help with?", thread_ts=event.get("ts"))
        return

    say(text=f"Routing this to Kross Agent for {route.firm_name}...", thread_ts=event.get("ts"))
    response = run_kross_agent(route, prompt)
    say(text=response[:39000], thread_ts=event.get("ts"))


@APP.event("message")
def handle_direct_message(event, say):
    if event.get("bot_id") or event.get("subtype"):
        return
    if event.get("channel_type") != "im":
        return
    prompt = slack_text_to_prompt(event.get("text", ""), BOT_USER_ID)
    if not prompt:
        return
    say(
        text=(
            "Kross Agent DMs are not routed in this pilot yet. "
            "Please use the approved private firm channel."
        )
    )


def main() -> None:
    global BOT_USER_ID
    auth = APP.client.auth_test()
    BOT_USER_ID = auth.get("user_id")
    logger.info("Kross Slack Gateway connected as bot user %s", BOT_USER_ID)
    SocketModeHandler(APP, SLACK_APP_TOKEN).start()


if __name__ == "__main__":
    main()
