import time

import requests

from config_store import get_setting

OPENAI_BASE = "https://api.openai.com/v1"


class LLMError(Exception):
    pass


class SchemaValidationError(LLMError):
    pass


def _api_key() -> str:
    key = get_setting("openai_api_key").strip()
    if not key:
        raise LLMError(
            "OpenAI API key not configured. Add it in the Settings page."
        )
    return key


def _model() -> str:
    return get_setting("openai_model").strip() or "gpt-4o-mini"


def _call(messages: list[dict], temperature: float, max_tokens: int, json_mode: bool) -> dict:
    payload = {
        "model": _model(),
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    retries = 3
    for attempt in range(1, retries + 1):
        try:
            resp = requests.post(
                f"{OPENAI_BASE}/chat/completions",
                json=payload,
                headers={
                    "Authorization": f"Bearer {_api_key()}",
                    "Content-Type": "application/json",
                },
                timeout=180,
            )
        except requests.exceptions.Timeout:
            raise LLMError("OpenAI request timed out.")
        except requests.exceptions.ConnectionError:
            raise LLMError("Cannot reach OpenAI API. Check your network.")

        if resp.status_code == 429:
            if attempt < retries:
                time.sleep(2 ** attempt)
                continue
            raise LLMError("OpenAI rate limit hit. Try again shortly.")

        if resp.status_code == 400 and json_mode and "response_format" in str(resp.text):
            payload.pop("response_format", None)
            json_mode = False
            continue

        if resp.status_code in (401, 403):
            raise LLMError(
                f"OpenAI rejected the API key ({resp.status_code}). Check the key in Settings."
            )

        if not resp.ok:
            raise LLMError(f"OpenAI error {resp.status_code}: {resp.text[:300]}")

        return resp.json()
    raise LLMError("Unreachable state in retry loop.")


def generate(messages: list[dict], temperature: float = 0.2, max_tokens: int = 8192, json_mode: bool = False) -> str:
    data = _call(messages, temperature, max_tokens, json_mode)
    message = data["choices"][0]["message"]
    content = (message.get("content") or "").strip()
    if not content and message.get("reasoning"):
        raise LLMError(
            "Model spent the entire token budget on reasoning without producing output. "
            "Increase max_tokens and retry."
        )
    if not content:
        raise LLMError("OpenAI returned an empty response.")
    return content


def test_connection() -> str:
    return generate(
        [{"role": "user", "content": "Reply with exactly: pong"}],
        temperature=0,
        max_tokens=256,
    )
