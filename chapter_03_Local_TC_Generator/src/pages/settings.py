import streamlit as st
from config_store import load_config, save_config
from jira_client import test_connection as test_jira_connection, AuthenticationError, ConnectionError, JiraError
from llm_client import test_ollama, test_groq

st.set_page_config(page_title="Settings — Jira Test Case Generator", page_icon="⚙️", layout="centered")

st.title("⚙️ Settings")

# Load current config
config = load_config()

# === Jira Settings ===
st.subheader("🔗 Jira Connection")
jira_url = st.text_input("Jira URL", value=config.get("jira_url", ""), placeholder="https://your-org.atlassian.net")
jira_email = st.text_input("Jira Email", value=config.get("jira_email", ""), placeholder="you@example.com")
jira_token = st.text_input("Jira API Token", value=config.get("jira_api_token", ""), type="password")

if st.button("Test Jira Connection"):
    # Temporarily save to test
    save_config({**config, "jira_url": jira_url, "jira_email": jira_email, "jira_api_token": jira_token})
    try:
        name = test_jira_connection()
        st.success(f"Connected as **{name}**")
    except AuthenticationError:
        st.error("Authentication failed. Check email and API token.")
    except ConnectionError:
        st.error(f"Cannot reach {jira_url}. Check the URL.")
    except JiraError as e:
        st.error(str(e))

st.markdown("---")

# === LLM Settings ===
st.subheader("🤖 LLM Provider")
provider = st.radio(
    "Select LLM provider",
    options=["ollama", "groq"],
    index=0 if config.get("llm_provider", "ollama") == "ollama" else 1,
    format_func=lambda x: f"Ollama (local, gemma3:1b)" if x == "ollama" else "Groq (cloud)",
    help="Ollama runs locally. Groq is the cloud fallback.",
)

groq_key = ""
if provider == "groq":
    groq_key = st.text_input(
        "Groq API Key",
        value=config.get("groq_api_key", ""),
        type="password",
        help="Get your key at https://console.groq.com/keys",
    )

col1, col2 = st.columns(2)
with col1:
    if st.button("Test Ollama"):
        if test_ollama():
            st.success("Ollama is running!")
        else:
            st.error("Cannot reach Ollama at localhost:11434")

with col2:
    if st.button("Test Groq"):
        save_config({**config, "groq_api_key": groq_key})
        if test_groq():
            st.success("Groq API key is valid!")
        else:
            st.error("Invalid Groq API key or network error")

st.markdown("---")

# === Save ===
if st.button("💾 Save Settings", type="primary"):
    new_config = {
        "jira_url": jira_url,
        "jira_email": jira_email,
        "jira_api_token": jira_token,
        "llm_provider": provider,
        "groq_api_key": groq_key if provider == "groq" else config.get("groq_api_key", ""),
    }
    save_config(new_config)
    st.success("Settings saved! Go back to [Chat](/) to start generating test cases.")
    st.balloons()

# === Current config display ===
st.markdown("---")
st.caption("Settings are stored in `config.json` (git-ignored). Credentials from `.env` seed the initial values.")
