import streamlit as st
import sys
import os

# Appending the project root directory so we can import our other backend modules cleanly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from automation.monitor import get_system_metrics, get_top_heavy_processes
from cybersecurity.log_analyzer import analyze_auth_logs

# Configure the web browser tab details
st.set_page_config(page_title="Daisy Assistant Hub", page_icon="🌼", layout="wide")

st.title("🌼 Daisy — Cybersecurity & Automation Assistant")
st.markdown("---")

# Create a clean side-by-side layout (Left Column for AI Chat, Right Column for System Health)
col1, col2 = st.columns([1, 1])

with col1:
    st.header("💬 Interactive AI Workspace")
    
    # Initialize chat state session memory if it doesn't exist yet
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "System online. How can I assist your security infrastructure today?"}]

    # Display chat historical message logs
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Handle user text input interaction box
    if user_input := st.chat_input("Ask Daisy a question or give an automation directive..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
            
        # Simulating Daisy processing voice/text commands internally
        with st.chat_message("assistant"):
            response = f"I received your request: '{user_input}'. Integration with Ollama is active."
            st.write(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

with col2:
    st.header("📊 Infrastructure Health & SIEM Alerts")
    
    # Button to force update diagnostic status metrics on click
    if st.button("🔄 Trigger Live Diagnostics Scan"):
        st.success("Diagnostics Complete!")
    
    # --- HARDWARE METRICS SECTION ---
    st.subheader("⚙️ Core Hardware Metrics")
    try:
        # Fetch the metrics generated from Phase 15 code logic
        metrics_summary = get_system_metrics()
        process_summary = get_top_heavy_processes()
        
        st.code(metrics_summary, language="text")
        st.code(process_summary, language="text")
    except Exception as e:
        st.error(f"Could not load hardware metrics: {e}")

    st.markdown("---")

    # --- CYBERSECURITY LOGS SECTION ---
    st.subheader("🛡️ Linux Authentication Log Parser (SIEM)")
    try:
        # Fetch log records from Phase 14 script logic
        # Reading auth.log requires system privileges; reads simulation if permissions are locked
        log_report = analyze_auth_logs()
        st.code(log_report, language="text")
    except Exception as e:
        st.info("Log access restricted or unreadable via local user portal.")
