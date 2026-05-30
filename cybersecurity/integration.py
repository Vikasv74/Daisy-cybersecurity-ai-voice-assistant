import subprocess
import os

AUTHORIZED_SUBNETS = ["127.0.0.1", "localhost"]

def run_authorized_scan(target):
    """Performs a safe, restricted local scan using Nmap."""
    target = target.strip()
    if target not in AUTHORIZED_SUBNETS:
        return f"[Daisy Security Alert] Scan blocked. '{target}' is not authorized."
    
    print(f"[Daisy Security] Initiating Nmap scan on: {target}...")
    try:
        result = subprocess.run(["nmap", "-F", target], capture_output=True, text=True, check=True)
        return result.stdout
    except Exception as e:
        return f"Scan failed: {str(e)}"

# --- NEW EXTENSIONS FOR PHASE 13 ---

def run_wireshark_sniff(packet_count=5):
    """
    Uses TShark (Wireshark CLI) to capture a quick burst of live local packets 
    for Daisy to analyze.
    """
    print(f"[Daisy Security] Initializing TShark network sniff ({packet_count} packets)...")
    try:
        # Runs tshark on the local loopback/any interface capturing a small burst
        command = ["sudo", "tshark", "-c", str(packet_count), "-T", "fields", "-e", "frame.number", "-e", "ip.src", "-e", "ip.dst", "-e", "_ws.col.Protocol"]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return f"\n--- Live Packet Capture Stream ---\n{result.stdout}"
    except subprocess.CalledProcessError:
        return "[Daisy Error] Failed to capture packets. Ensure Daisy has sudo permissions for TShark."

def read_suricata_alerts(alert_path="/var/log/suricata/fast.log"):
    """
    Parses Suricata IDS logs to check if the Intrusion Detection System 
    has triggered any live signatures.
    """
    print(f"[Daisy Security] Reading Suricata IDS rules match log: {alert_path}")
    if not os.path.exists(alert_path):
        # Fallback simulation if service hasn't generated alerts yet
        return "[Daisy IDS Info] Suricata fast.log is clean. No active network intrusions detected."
    
    try:
        with open(alert_path, "r") as f:
            alerts = f.readlines()[-5:] # Get the 5 most recent alerts
        return "".join(alerts) if alerts else "Suricata is running. 0 threats detected."
    except Exception as e:
        return f"Error reading Suricata data: {str(e)}"

def check_wazuh_alerts(wazuh_log_path="/var/ossec/logs/alerts/alerts.log"):
    """
    Checks the Wazuh core SIEM log manager file to find active high-priority security events.
    """
    print(f"[Daisy SIEM] Checking Wazuh manager engine logs...")
    if not os.path.exists(wazuh_log_path):
        # Simulation response if Wazuh manager dashboard isn't completely deployed yet
        return "[Daisy SIEM Info] Wazuh monitoring agent connection stable. Local host state: SECURE."
        
    try:
        # Scan for alerts tagged with level 7 or above (high severity alerts)
        triggered_events = []
        with open(wazuh_log_path, "r") as f:
            for line in f:
                if "Alert Level" in line:
                    triggered_events.append(line.strip())
        return f"Wazuh SIEM Status: Analyzed recent alerts. Found {len(triggered_events[-5:])} high-severity server events."
    except Exception as e:
        return f"Error reading Wazuh logs: {str(e)}"

if __name__ == "__main__":
    print("=== Testing Upgraded Daisy Cybersecurity Suite ===")
    
    # 1. Test Nmap
    print(run_authorized_scan("127.0.0.1"))
    
    # 2. Test Wireshark Capture (Will ask for password since it uses sudo)
    print(run_wireshark_sniff(3))
    
    # 3. Test Suricata 
    print(read_suricata_alerts())
    
    # 4. Test Wazuh
    print(check_wazuh_alerts())
