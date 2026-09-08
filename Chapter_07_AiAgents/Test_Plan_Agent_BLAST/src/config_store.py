import json
import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"
CONFIG_PATH = ROOT_DIR / "config.json"

DEFAULTS = {
    "jira_base_url": "",
    "jira_email": "",
    "jira_api_token": "",
    "groq_api_key": "",
    "groq_model": "openai/gpt-oss-120b",
}


def load_config() -> dict:
    load_dotenv(ENV_PATH)

    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = json.load(f)
    else:
        config = {}

    env_map = {
        "jira_base_url": "JIRA_BASE_URL",
        "jira_email": "JIRA_Email",
        "jira_api_token": "JIRA_API_TOKEN",
        "groq_api_key": "GROQ_API_KEY",
        "groq_model": "GROQ_MODEL",
    }
    for key, env_var in env_map.items():
        if not config.get(key):
            config[key] = os.getenv(env_var, DEFAULTS[key])

    return config


def save_config(config: dict) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def get_setting(key: str) -> str:
    return load_config().get(key, DEFAULTS.get(key, ""))
