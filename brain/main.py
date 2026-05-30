import sys
import os
import requests
from dotenv import load_dotenv

load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from voice.listen import listen_to_user
from voice.speak import speak
from automation.monitor import get_system_metrics
# Import the multi-agent orchestration pipeline
from agents.security_crew import run_security_analysis_crew

OLLAMA_URL = os.getenv("OLLAMA_API_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("DAISY_MODEL", "llama3")
CHAT_HISTORY = []

def query_daisy_brain(new_prompt):
    """Handles standard short conversation conversational window context mapping."""
    global CHAT_HISTORY
    context_history = ""
    for exchange in CHAT_HISTORY[-2:]:
        context_history += f"User: {exchange['user']}\nAssistant: {exchange['assistant']}\n"
        
    full_system_prompt = (
        f"You are Daisy, an advanced cybersecurity workspace assistant. Keep responses brief.\n\n"
        f"{context_history}User: {new_prompt}\nAssistant:"
    )
    
    try:
        response = requests.post(OLLAMA_URL, json={"model": MODEL_NAME, "prompt": full_system_prompt, "stream": False})
        if response.status_code == 200:
            reply = response.json().get("response", "").strip()
            CHAT_HISTORY.append({"user": new_prompt, "assistant": reply})
            return reply
        return "Friction detected on backend communication lines."
    except Exception as e:
        return f"Core connection failure: {str(e)}"

def start_daisy_pipeline():
    """Runs the central voice interface with live telemetry hook triggers."""
    speak("Advanced security crew modules integrated successfully.")
    print("[Daisy Core] Systems fully synchronized. Awaiting input...")
    
    while True:
        user_speech = listen_to_user()
        if not user_speech:
            continue
            
        user_speech_lower = user_speech.lower()
        
        if "exit" in user_speech_lower or "shutdown" in user_speech_lower:
            speak("Powering down operations. Goodbye.")
            break
            
        elif "hardware" in user_speech_lower or "system status" in user_speech_lower:
            speak("Scanning system resource profiles.")
            print(get_system_metrics())
            
        # VOICE TRIGGER: Multi-agent security audit hook
        elif "run security audit" in user_speech_lower or "check logs" in user_speech_lower:
            speak("Accessing active authentication log records and deploying crew agents.")
            print("\n[Daisy Core] Reading live entries from /var/log/auth.log...")
            
            # Read real Ubuntu auth logs dynamically
            try:
                with open("/var/log/auth.log", "r") as log_file:
                    # Capture the last 15 lines of log history
                    live_logs = "".join(log_file.readlines()[-15:])
                if not live_logs.strip():
                    live_logs = "Log file is currently empty. No active anomalies recorded."
            except PermissionError:
                live_logs = "Error: Insufficient permissions to parse log files. Ensure script runs via sudo env hooks."
                print(f"[Warning] {live_logs}")
            
            print("[Daisy Core] Handing live metrics down to Multi-Agent Crew...")
            speak("Data dispatched. The forensics analyst is building a baseline profile.")
            
            # Run the multi-agent task workflow sequentially
            crew_report = run_security_analysis_crew(live_logs)
            
            print("\n================ CREW REMEDIATION REPORT ================")
            print(crew_report)
            print("=========================================================\n")
            
            speak("Analysis sequence complete. The mitigation playbook is ready in your terminal.")
            
        else:
            ai_response = query_daisy_brain(user_speech)
            print(f"\nDaisy: {ai_response}")
            speak(ai_response)

if __name__ == "__main__":
    start_daisy_pipeline()
