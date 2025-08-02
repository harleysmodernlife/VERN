"""
VERN GUI (Streamlit, Modern, Full-Featured)
-------------------------------------------
Interactive GUI for VERN with real-time streaming output, config controls, agent/persona selection, tool/plugin management, onboarding, logs, and documentation.
"""

import streamlit as st
from mvp.llm_router import get_llm_backend
from mvp.orchestrator import orchestrator_respond
from mvp.ollama_llm import call_ollama
import yaml
import os

st.set_page_config(page_title="VERN", layout="wide")
st.title("VERN - AI OS")

# Sidebar navigation
sidebar_options = [
    "Chat",
    "Config",
    "Agents",
    "Tools/Plugins",
    "Onboarding",
    "Logs/Debug",
    "Profile/Persona",
    "Documentation"
]
selected_page = st.sidebar.radio("Navigation", sidebar_options)

# Load config for model/provider selection
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '../../config/agent_backends.yaml')
def load_llm_config():
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)
LLM_CONFIG = load_llm_config()
current_backend = LLM_CONFIG.get('default', 'ollama-qwen3:0.6b')
if 'backends' in LLM_CONFIG and current_backend in LLM_CONFIG['backends']:
    current_model = LLM_CONFIG['backends'][current_backend]['model']
    current_provider = LLM_CONFIG['backends'][current_backend]['provider']
else:
    first_backend = list(LLM_CONFIG['backends'].keys())[0]
    current_model = LLM_CONFIG['backends'][first_backend]['model']
    current_provider = LLM_CONFIG['backends'][first_backend]['provider']
    current_backend = first_backend

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_id = "default_user"

if selected_page == "Chat":
    st.subheader("Chat with VERN")
    user_input = st.text_input("You:", "")
    if st.button("Send") and user_input:
        provider, model = get_llm_backend()
        if provider == "ollama":
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("VERN", "Streaming LLM output:"))
            response_stream = call_ollama(user_input, model=model, stream=True)
            streamed = ""
            chat_box = st.empty()
            for token in response_stream:
                streamed += token
                chat_box.markdown(f"**VERN:** {streamed}")
            st.session_state.chat_history.append(("VERN", streamed))
        else:
            response = orchestrator_respond(user_input, context={}, agent_status=None, user_id=user_id, verbose=True)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("VERN", response))
    st.subheader("Chat History")
    for speaker, msg in st.session_state.chat_history:
        st.markdown(f"**{speaker}:** {msg}")

elif selected_page == "Config":
    st.subheader("Model/Provider Selection")
    backend_options = list(LLM_CONFIG['backends'].keys())
    selected_backend = st.selectbox("Select LLM Backend", backend_options, index=backend_options.index(current_backend))
    if st.button("Save Backend Selection"):
        LLM_CONFIG['default'] = selected_backend
        with open(CONFIG_PATH, 'w') as f:
            yaml.dump(LLM_CONFIG, f)
        st.success(f"Backend changed to {selected_backend}. Please restart CLI/GUI to apply changes.")
    st.write("Current Model:", LLM_CONFIG['backends'][selected_backend]['model'])
    st.write("Current Provider:", LLM_CONFIG['backends'][selected_backend]['provider'])
    st.write("Edit config/agent_backends.yaml for advanced options.")

elif selected_page == "Agents":
    st.subheader("Agent/Persona Selection")
    agent_options = [
        "research", "finance", "health", "admin", "learning", "social", "environment", "legal",
        "creativity", "career", "travel", "security", "archetype", "emergent", "knowledge_broker_context_lookup",
        "knowledge_broker_cross_cluster_query", "id10t_monitor"
    ]
    selected_agent = st.selectbox("Select Agent Cluster", agent_options)
    persona_options = ["default", "coach", "medic", "mindfulness"]
    selected_persona = st.selectbox("Select Persona (Health/Wellness)", persona_options)
    st.write(f"Selected Agent: {selected_agent}")
    st.write(f"Selected Persona: {selected_persona}")
    st.info("Agent/persona selection is for future advanced workflows.")

elif selected_page == "Tools/Plugins":
    st.subheader("Tool/Plugin Management")
    from mvp.plugin_registry import get_all_mcp_tools
    all_tools = get_all_mcp_tools()
    tool_options = [t["name"] for t in all_tools]
    tool_labels = {t["name"]: t["description"] for t in all_tools}
    if "enabled_tools" not in st.session_state:
        st.session_state.enabled_tools = set(tool_options)
    enabled_tools = st.multiselect(
        "Enable/Disable Tools",
        tool_options,
        default=list(st.session_state.enabled_tools),
        format_func=lambda x: f"{x} - {tool_labels.get(x, '')}"
    )
    st.session_state.enabled_tools = set(enabled_tools)
    st.write("Enabled Tools:", list(st.session_state.enabled_tools))
    st.success("Tool/plugin enable/disable state is now persistent for this session.")
    st.info("Tool/plugin management now uses dynamic discovery from the MCP registry.")

elif selected_page == "Onboarding":
    st.subheader("Onboarding & Accessibility")
    st.markdown("""
    Welcome to VERN!  
    - Use the Chat tab to interact with VERN.
    - Use Config to change models/providers.
    - Use Agents and Tools/Plugins to explore advanced features.
    - Accessibility: Adjust font size, color scheme, and enable screen reader support in your browser.
    - For help, see Documentation or ask in the Community.
    """)
    # Onboarding checklist
    if "onboarding_checklist" not in st.session_state:
        st.session_state.onboarding_checklist = {
            "Read the README": False,
            "Configured .env": False,
            "Tested a plugin/tool": False,
            "Joined the Community": False,
            "Reviewed Security Guidelines": False
        }
    st.markdown("#### Onboarding Checklist")
    for item in st.session_state.onboarding_checklist:
        checked = st.checkbox(item, value=st.session_state.onboarding_checklist[item], key=f"onboard_{item}")
        st.session_state.onboarding_checklist[item] = checked
    if all(st.session_state.onboarding_checklist.values()):
        st.success("Onboarding complete! You're ready to use VERN.")
    # Feedback form
    st.markdown("#### Feedback")
    feedback = st.text_area("Share your feedback, suggestions, or issues here:", key="onboarding_feedback")
    if st.button("Submit Feedback"):
        if feedback.strip():
            if "feedback_log" not in st.session_state:
                st.session_state.feedback_log = []
            st.session_state.feedback_log.append(feedback.strip())
            st.success("Thank you for your feedback!")
        else:
            st.warning("Please enter feedback before submitting.")

elif selected_page == "Logs/Debug":
    st.subheader("Logs & Debug Panel")
    st.write("Recent logs and errors will appear here (feature coming soon).")
    st.info("Download/export logs for troubleshooting (future feature).")

    st.markdown("### Diagnostics: Plugin/Tool Health Checks")
    import requests
    import json

    MCP_URL = "http://127.0.0.1:6277"
    def test_tool(tool, params):
        try:
            resp = requests.post(f"{MCP_URL}/tools/{tool}/invoke", json={"input": params}, timeout=5)
            resp.raise_for_status()
            result = resp.json().get("result", "")
            return "PASS" if result else f"FAIL: {result}"
        except Exception as e:
            return f"ERROR: {e}"

    # Only test enabled tools
    tool_tests = {
        "get_weather": {"location": "Austin"},
        "add_event": {"title": "Test Event", "date": "2025-08-01"},
        "list_events": {},
        "fileops_list_files": {"directory": "."},
        "fileops_read_file": {"path": "README.md"},
        "chromadb_query": {"query": "test", "top_k": 1}
    }
    enabled_tools = list(st.session_state.get("enabled_tools", tool_tests.keys()))
    for tool in enabled_tools:
        params = tool_tests.get(tool, {})
        status = test_tool(tool, params)
        st.write(f"Tool `{tool}`: {status}")

elif selected_page == "Profile/Persona":
    st.subheader("Profile Visualization")
    st.write("Archetype resonance, persona, and recent context will be visualized here (feature coming soon).")
    st.info("Profile visualization and feedback tracking are planned for future releases.")

elif selected_page == "Documentation":
    st.subheader("Documentation & Help")
    st.markdown("""
    - [README.md](./README.md)
    - [QUICKSTART.md](./QUICKSTART.md)
    - [AGENT_GUIDES/README.md](./AGENT_GUIDES/README.md)
    - [PROJECT_OVERVIEW.md](./PROJECT_OVERVIEW.md)
    - [KNOWN_ISSUES_AND_GOTCHAS.md](./KNOWN_ISSUES_AND_GOTCHAS.md)
    - [SECURITY_AND_GIT_GUIDELINES.md](./SECURITY_AND_GIT_GUIDELINES.md)
    """)
    st.info("Documentation is always up to date. For troubleshooting, see README and Known Issues.")

st.caption("Powered by VERN | Streaming LLM output enabled | Ollama backend | Modern GUI | All features staged for first release.")
