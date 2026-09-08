import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config_store import load_config, save_config  # noqa: E402
from jira_client import (  # noqa: E402
    test_connection as test_jira_connection,
    JiraError,
    AuthenticationError,
    ConnectionError,
)
from llm_client import test_connection as test_groq_connection, LLMError  # noqa: E402

st.set_page_config(page_title="Settings — AI Test Plan Agent", page_icon="⚙️", layout="centered")

st.title("⚙️ Settings")
st.caption("Configure Jira and Groq. Both connection tests run against the values typed below (saved first).")

config = load_config()

st.subheader("🔗 Jira Connection")
jira_base_url = st.text_input(
    "Jira Base URL",
    value=config.get("jira_base_url", ""),
    placeholder="https://your-org.atlassian.net",
    help="The API base URL, e.g. https://hossaintwasif98-jira.atlassian.net",
)
jira_email = st.text_input(
    "Jira Email",
    value=config.get("jira_email", ""),
    placeholder="you@example.com",
)
jira_token = st.text_input(
    "Jira API Token",
    value=config.get("jira_api_token", ""),
    type="password",
    help="Create one at https://id.atlassian.com/manage-profile/security/api-tokens",
)

if st.button("🔌 Test Jira Connection"):
    save_config(
        {
            **config,
            "jira_base_url": jira_base_url,
            "jira_email": jira_email,
            "jira_api_token": jira_token,
        }
    )
    try:
        name = test_jira_connection()
        st.success(f"Jira connected as **{name}**")
    except AuthenticationError:
        st.error("Authentication failed. Check email and API token.")
    except ConnectionError as e:
        st.error(str(e))
    except JiraError as e:
        st.error(str(e))

st.markdown("---")

st.subheader("🤖 Groq (LLM)")
groq_key = st.text_input(
    "Groq API Key",
    value=config.get("groq_api_key", ""),
    type="password",
    help="Get your key at https://console.groq.com/keys",
)
groq_model = st.text_input(
    "Groq Model",
    value=config.get("groq_model", "openai/gpt-oss-120b"),
    help="Default: openai/gpt-oss-120b",
)

if st.button("🔌 Test Groq Connection"):
    save_config({**config, "groq_api_key": groq_key, "groq_model": groq_model})
    try:
        reply = test_groq_connection()
        st.success(f"Groq connected — model replied: **{reply}**")
    except LLMError as e:
        st.error(str(e))

st.markdown("---")

if st.button("💾 Save Settings", type="primary"):
    save_config(
        {
            "jira_base_url": jira_base_url,
            "jira_email": jira_email,
            "jira_api_token": jira_token,
            "groq_api_key": groq_key,
            "groq_model": groq_model,
        }
    )
    st.success("Settings saved! Go back to the chat to generate test plans.")
    st.balloons()

st.markdown("---")
st.caption(
    "Settings persist in `config.json` (git-ignored). Values from `.env` seed the defaults. "
    "Credentials are never sent anywhere except Jira and Groq."
)
