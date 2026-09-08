import re
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))

from config_store import load_config, get_setting  # noqa: E402
from jira_client import (  # noqa: E402
    JiraError,
    AuthenticationError,
    ConnectionError,
    NotFoundError,
)
from llm_client import LLMError, SchemaValidationError  # noqa: E402
from pipeline import run_pipeline  # noqa: E402

st.set_page_config(page_title="AI Test Plan Agent", page_icon="🧪", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("## ⚙️ Status")
    config = load_config()
    jira_url = config.get("jira_base_url", "")
    groq_key = config.get("groq_api_key", "")
    st.caption(f"**Jira:** {jira_url or 'Not configured'}")
    st.caption(f"**Groq:** {'Configured' if groq_key else 'Missing API key'}")
    st.caption(f"**Model:** {config.get('groq_model', 'openai/gpt-oss-120b')}")
    if not jira_url or not config.get("jira_email") or not config.get("jira_api_token"):
        st.warning("Configure Jira in Settings →")
    if not groq_key:
        st.warning("Configure Groq in Settings →")
    st.markdown("---")
    st.page_link("pages/settings.py", label="⚙️ Settings", icon="⚙️")
    st.markdown("---")
    st.caption("BLAST pipeline: fetch → normalize → generate → deliver")

st.title("🧪 AI Test Plan Agent")
st.caption(
    "Type a natural-language request — I'll fetch the Jira issue and generate a traceable test plan automatically."
)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt_text := st.chat_input("e.g. Fetch KAN-1 from Jira and create a test plan"):
    st.session_state.messages.append({"role": "user", "content": prompt_text})
    with st.chat_message("user"):
        st.markdown(prompt_text)

    match = re.search(r"\b[A-Z][A-Z0-9]*-\d+\b", prompt_text)
    if not match:
        reply = (
            "I couldn't find a Jira issue key in your message. "
            "Please include one like `KAN-1`.\n\n"
            "Example: \"Fetch **KAN-1** from Jira and create a test plan\""
        )
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
    else:
        key = match.group(0).upper()
        try:
            with st.status(
                f"Fetching **{key}** from Jira and generating the test plan...",
                expanded=True,
            ) as status:
                result = run_pipeline(key)
                status.update(
                    label=f"Test plan ready for **{key}** — confidence: {result['confidence']}",
                    state="complete",
                    expanded=False,
                )

            reply = result["markdown"]
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.markdown(reply)
                st.download_button(
                    "⬇️ Download Test Plan (Markdown)",
                    data=result["markdown"],
                    file_name=f"test_plan_{result['key']}.md",
                    mime="text/markdown",
                )
                st.caption(f"Saved to `{result['md_path']}`")

        except AuthenticationError as e:
            reply = f"❌ **Configuration Error:** {e}\n\nGo to the [Settings](settings) page to fix this."
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.error(reply)

        except ConnectionError as e:
            reply = f"❌ **Connection Error:** {e}"
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.error(reply)

        except NotFoundError as e:
            reply = f"❌ {e}"
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.error(reply)

        except JiraError as e:
            reply = f"❌ **Jira Error:** {e}"
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.error(reply)

        except (LLMError, SchemaValidationError) as e:
            reply = f"❌ **LLM Error:** {e}"
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.error(reply)

        except Exception as e:
            reply = f"❌ **Unexpected Error:** {e}"
            st.session_state.messages.append({"role": "assistant", "content": reply})
            with st.chat_message("assistant"):
                st.error(reply)
