import os
import sys
from crewai import Agent, Task, Crew, Process, LLM

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Prevent cloud fallback errors
os.environ["OPENAI_API_KEY"] = "NA"

local_llm = LLM(
    model="ollama/llama3",
    base_url="http://localhost:11434"
)

log_auditor = Agent(
    role='Senior Log Forensics Analyst',
    goal='Identify unauthorized authentication vectors and anomalous access footprints.',
    backstory='An elite cybersecurity incident responder specializing in analyzing system auth.log files.',
    verbose=True,
    allow_delegation=False,
    llm=local_llm
)

hardening_expert = Agent(
    role='Linux Infrastructure Security Hardening Engineer',
    goal='Provide definitive remediation patterns, firewall rules, and security policies.',
    backstory='A veteran system administrator who hardens mission-critical Linux environments against active threats.',
    verbose=True,
    allow_delegation=False,
    llm=local_llm
)

def run_security_analysis_crew(incident_raw_data):
    """Orchestrates sequential collaboration between the auditor and hardening advisor."""
    audit_task = Task(
        description=f"Analyze this raw system security log metadata for indicators of compromise:\n\n{incident_raw_data}",
        expected_output="A summary pinpointing malicious IP addresses, failed user attempts, and threat severity.",
        agent=log_auditor
    )
    
    mitigation_task = Task(
        description="Take the analyst's findings and write the exact Ubuntu Linux commands needed to mitigate this threat.",
        expected_output="A brief step-by-step mitigation guide containing actionable bash commands (e.g., iptables, ufw). Keep it concise.",
        agent=hardening_expert
    )
    
    security_crew = Crew(
        agents=[log_auditor, hardening_expert],
        tasks=[audit_task, mitigation_task],
        process=Process.sequential,
        verbose=True
    )
    
    return str(security_crew.kickoff())
