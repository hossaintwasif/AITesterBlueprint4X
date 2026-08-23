import re
from pathlib import Path

import streamlit as st

from config_store import load_config, get_setting
from jira_client import fetch_ticket, JiraError, AuthenticationError, NotFoundError, ConnectionError
from llm_client import generate, LLMError

st.set_page_config(page_title="Jira Test Case Generator", page_icon="🧪", layout="centered")

# === Template loading ===
BASE_DIR = Path(__file__).parent
TEMPLATE_DIR = BASE_DIR.parent / "templates"


@st.cache_data
def load_template(name: str = "testcase_creator.md") -> str:
    path = TEMPLATE_DIR / name
    if not path.exists():
        return ""
    return path.read_text()


def build_prompt(ticket: dict, template: str) -> str:
    """Merge ticket details into the test case template with a system prefix."""
    desc = ticket["description"] or ""
    ac = ticket.get("acceptance_criteria", "")
    requirements = desc
    if ac:
        requirements += f"\n\nAcceptance Criteria:\n{ac}"

    # Estimate number of test cases based on requirement complexity
    word_count = len(requirements.split())
    num = max(3, min(10, word_count // 40))

    prompt = template.replace("[NUMBER]", str(num))
    prompt = prompt.replace("[PASTE REQUIREMENTS HERE]", requirements)

    # Prepend system instruction for small models that tend to ramble
    system_prefix = (
        "INSTRUCTION: You are a test case generator. Output ONLY a markdown table "
        "with these exact columns: Test ID, Description, Pre-conditions, Steps, Expected Result, Priority. "
        "No preamble, no closing notes, no extra columns. Output NOTHING but the table.\n\n"
    )
    return system_prefix + prompt


def clean_output(text: str) -> str:
    """Strip markdown code fences, ensure proper table format, clean whitespace."""
    text = text.strip()

    # Remove markdown code fences if present
    if text.startswith("```"):
        text = text.split("\n", 1)[-1] if "\n" in text else text
    if text.endswith("```"):
        text = text.rsplit("\n```", 1)[0] if "\n```" in text else text

    lines = [l.strip() for l in text.split("\n") if l.strip()]

    # Filter out empty pipe-only lines and non-table lines (preamble/notes)
    table_lines = [l for l in lines if l.startswith("|") and len(l) > 3]

    if not table_lines:
        return text  # return as-is if no table found

    # Check if we have a header row followed by a separator row
    has_header = len(table_lines) >= 2 and all(
        c.strip() in ("---", ":---", "---:", ":---:", "===") or set(c.strip()) <= {"-", ":"}
        for c in table_lines[1].split("|")[1:-1]
    )
    has_sep = len(table_lines) >= 2 and all(
        c.strip().replace("-", "").replace(":", "") == ""
        for c in table_lines[1].split("|")[1:-1]
    )

    if not has_sep:
        # No separator row found — build proper table
        # First line is data; prepend header and separator
        cols = ["Test ID", "Description", "Pre-conditions", "Steps", "Expected Result", "Priority"]
        header = "| " + " | ".join(cols) + " |"
        sep = "|" + "|".join([" --- " for _ in cols]) + "|"
        if has_header:
            # First line might be a header without separator — skip it
            table_lines = table_lines[1:]
        return "\n".join([header, sep] + table_lines)

    return "\n".join(table_lines)


# === Session state init ===
if "messages" not in st.session_state:
    st.session_state.messages = []

# === Sidebar ===
with st.sidebar:
    st.markdown("## ⚙️ Quick Info")
    config = load_config()
    provider = config.get("llm_provider", "ollama")
    st.caption(f"**LLM Provider:** {provider.upper()}")
    st.caption(f"**Model:** gemma3:1b" if provider == "ollama" else "**Model:** llama-3.1-8b-instant")
    jira_url = config.get("jira_url", "")
    st.caption(f"**Jira:** {jira_url or 'Not configured'}")

    if not jira_url or not config.get("jira_email"):
        st.warning("Configure Jira in Settings →")

    st.markdown("---")
    st.markdown("[Settings](settings)")

# === Title ===
st.title("🧪 Jira Test Case Generator")
st.caption("Type a Jira ticket key and I'll generate test cases using the local LLM.")

# === Chat history ===
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# === Chat input ===
if prompt_text := st.chat_input("Ask me to create test cases for a Jira ticket..."):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt_text})
    with st.chat_message("user"):
        st.markdown(prompt_text)

    # Parse Jira key
    match = re.search(r"\b[A-Z]+-\d+\b", prompt_text)
    if not match:
        reply = (
            "I couldn't find a Jira ticket key in your message. "
            "Please include one like `PROJ-123` or `QA-102`.\n\n"
            "Example: \"Create test cases for **QA-102**\""
        )
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
    else:
        ticket_key = match.group(0)

        with st.chat_message("assistant"):
            try:
                # Step 1: Fetch ticket
                with st.status(f"Fetching ticket **{ticket_key}** from Jira...", expanded=True) as status:
                    ticket = fetch_ticket(ticket_key)
                    status.update(
                        label=f"Fetched **{ticket_key}**: {ticket['summary']}",
                        state="complete",
                        expanded=False,
                    )

                # Step 2: Load template
                template = load_template()
                if not template:
                    reply = "Template `testcase_creator.md` not found in `templates/` folder."
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.markdown(reply)
                else:
                    # Step 3: Build prompt
                    prompt = build_prompt(ticket, template)

                    # Step 4: Generate test cases
                    with st.status("Generating test cases...", expanded=True) as status:
                        raw_result = generate(prompt)
                        result = clean_output(raw_result)
                        status.update(
                            label="Test cases generated!",
                            state="complete",
                            expanded=False,
                        )

                    # Step 5: Render result
                    reply = f"### {ticket_key}: {ticket['summary']}\n\n{result}"
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                    st.markdown(reply)

            except (AuthenticationError, ConnectionError) as e:
                reply = (
                    f"❌ **Configuration Error:** {e}\n\n"
                    "Go to the [Settings](settings) page to fix this."
                )
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.error(e)

            except NotFoundError as e:
                reply = f"❌ {e}"
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.error(e)

            except JiraError as e:
                reply = f"❌ **Jira Error:** {e}"
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.error(e)

            except LLMError as e:
                reply = (
                    f"❌ **LLM Error:** {e}\n\n"
                    "Try switching providers in the [Settings](settings) page."
                )
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.error(e)

            except Exception as e:
                reply = f"❌ **Unexpected Error:** {e}"
                st.session_state.messages.append({"role": "assistant", "content": reply})
                st.error(e)
