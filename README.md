# Daisy: AI Cybersecurity Voice Assistant 🚀

Daisy is an interactive, voice-activated local AI Cybersecurity Assistant designed to act as an automated Security Operations Center (SOC) companion. By combining modular local language models with an advanced multi-agent orchestration framework, Daisy can ingest system data, process interactive voice or text commands, and coordinate autonomous agents to handle threat intelligence and system hardening workflows.

## 🧠 Core Features & Architecture
* **Interactive Dashboard UI:** A clean, local web portal built using **Streamlit** to monitor conversations, agent states, and system analytics.
* **Local Intelligence Array:** Interfaces directly with local open-source models via **Ollama**, featuring a local vector database (**ChromaDB**) for context preservation.
* **Multi-Agent Cybersecurity Crew:** Uses **CrewAI** to orchestrate an autonomous team of specialized security personas:
  * *Senior Log Forensics Analyst:* Scans, parses, and identifies malicious footprints inside complex server and firewall logs.
  * *Linux Hardening Engineer:* Generates robust, actionable mitigation blueprints and script compliance checklists based on detected incidents.
* **Voice Integration Pipeline:** Equipped with local speech-to-text and text-to-speech loops for hands-free interaction.
* **Containerized Deployment Ready:** Configured with `Dockerfile` and `docker-compose.yml` assets for isolated deployment.

## 🛠️ Tech Stack
* **Languages:** Python
* **AI Frameworks:** CrewAI, Ollama, ChromaDB
* **Frontend Dashboard:** Streamlit
* **Infrastructure:** Docker, Linux CLI, Git

## 📋 How to Run Local Environment
1. Ensure **Ollama** is running locally with your chosen model.
2. Install dependencies: `pip install -r requirements.txt`
3. Launch the dashboard: `streamlit run app.py`
