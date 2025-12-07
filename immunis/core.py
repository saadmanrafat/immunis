import json
from pathlib import Path

import requests

from .schemas import SystemStatus
from .config import settings

DB_FILE = Path("system_status.json")


def set_status(status: SystemStatus):
    with DB_FILE.open("w") as f:
        json.dump(status.model_dump(), f, indent=2)


def get_status() -> SystemStatus:
    if not DB_FILE.exists():
        set_status(SystemStatus())

    with DB_FILE.open("r") as f:
        data = json.load(f)
        return SystemStatus.model_validate(data)


def send_log_to_datadog(prompt: str, score: int, is_attack: bool):
    """Sends a structured log to the Datadog Log Intake API."""
    if settings.datadog_api_key is None:
        print("Datadog API key not configured, skipping log.")
        return
    api_key = settings.datadog_api_key.get_secret_value()
    url = settings.datadog_site
    headers = {
        "DD-API-KEY": api_key,
        "Content-Type": "application/json",
    }
    payload = [
        {
            "ddsource": "immunis-cli",
            "service": "guard-dog-service",
            "message": f"Prompt analyzed: {prompt[:100]}...",
            "status": True if is_attack else False,
            "attack_score": score,
            "is_attack": is_attack,
            "prompt_full_text": prompt,
        }
    ]
    try:
        requests.post(url, headers=headers, json=payload, timeout=2)
    except requests.RequestException:
        raise
