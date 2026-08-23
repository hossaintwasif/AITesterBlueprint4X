import requests
from config_store import get_setting


class LLMError(Exception):
    pass


OLLAMA_BASE = "http://localhost:11434"
OLLAMA_MODEL = "gemma3:1b"
GROQ_BASE = "https://api.groq.com/openai/v1"
GROQ_MODEL = "llama-3.1-8b-instant"


def generate(prompt: str, provider: str | None = None) -> str:
    """
    Generate text from the LLM.

    Tries Ollama first (unless provider explicitly set to "groq").
    Falls back to Groq if Ollama is unavailable.
    """
    if provider is None:
        provider = get_setting("llm_provider") or "ollama"

    # Try Ollama unless user explicitly chose Groq
    if provider != "groq":
        try:
            return _call_ollama(prompt)
        except (LLMError, requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            pass  # fall through to Groq

    # Fallback to Groq
    return _call_groq(prompt)


def _call_ollama(prompt: str) -> str:
    """Call local Ollama API."""
    try:
        resp = requests.post(
            f"{OLLAMA_BASE}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
            },
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("response", "").strip()
    except requests.exceptions.ConnectionError:
        raise LLMError("Ollama is not running. Start it with `ollama serve` or switch to Groq.")
    except requests.exceptions.Timeout:
        raise LLMError("Ollama timed out. The model may be too large or the prompt too complex.")
    except requests.exceptions.RequestException as e:
        raise LLMError(f"Ollama error: {e}")


def _call_groq(prompt: str) -> str:
    """Call Groq cloud API."""
    api_key = get_setting("groq_api_key")
    if not api_key:
        raise LLMError(
            "Groq API key not configured. Add it in Settings or ensure Ollama is running."
        )

    try:
        resp = requests.post(
            f"{GROQ_BASE}/chat/completions",
            json={
                "model": GROQ_MODEL,
                "messages": [{"role": "user", "content": prompt}],
            },
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.exceptions.Timeout:
        raise LLMError("Groq request timed out.")
    except requests.exceptions.RequestException as e:
        raise LLMError(f"Groq error: {e}")


def test_ollama() -> bool:
    """Check if Ollama is reachable."""
    try:
        resp = requests.get(f"{OLLAMA_BASE}/api/tags", timeout=5)
        return resp.ok
    except requests.exceptions.RequestException:
        return False


def test_groq() -> bool:
    """Check if Groq API key is valid."""
    api_key = get_setting("groq_api_key")
    if not api_key:
        return False
    try:
        resp = requests.get(
            f"{GROQ_BASE}/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10,
        )
        return resp.ok
    except requests.exceptions.RequestException:
        return False
