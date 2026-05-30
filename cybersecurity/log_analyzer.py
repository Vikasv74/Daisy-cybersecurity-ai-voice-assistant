import re
import os

def analyze_auth_logs(log_path="/var/log/auth.log"):
    """
    Parses the Ubuntu authentication log to find failed login attempts,
    extract suspicious IP addresses, and flag potential brute-force attacks.
    """
    print(f"[Daisy Log Analyzer] Reading security events from: {log_path}")
    
    # Check if the log file exists
    if not os.path.exists(log_path):
        return f"[Daisy Info] Log file {log_path} not found. Ensure rsyslog is running."

    # Regular expression patterns to find common SSH/auth failures and IPs
    failed_pattern = re.compile(r"Failed password for invalid user|Failed password for .* from (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})")
    ip_pattern = re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b")

    failed_count = 0
    suspicious_ips = set()
    recent_alerts = []

    try:
        with open(log_path, "r") as file:
            # Read lines from bottom/end to get the most recent incidents first
            lines = file.readlines()
            
            for line in lines[-1000:]:  # Scan the last 1000 system log entries
                if "Failed" in line or "failure" in line.lower():
                    failed_count += 1
                    
                    # Try to extract an IP address from the malicious event line
                    found_ips = ip_pattern.findall(line)
                    for ip in found_ips:
                        if ip != "127.0.0.1": # Exclude your own local machine loops
                            suspicious_ips.add(ip)
                            
                    # Save a snapshot of the last 3 critical log details
                    if len(recent_alerts) < 3:
                        recent_alerts.append(line.strip())

        # Generate structural summary analysis report
        summary = f"\n=== Daisy Security Intelligence Report ===\n"
        summary += f"[*] Total Logins Failed: {failed_count}\n"
        summary += f"[*] Suspicious IPs Flagged: {list(suspicious_ips) if suspicious_ips else 'None detected'}\n"
        
        # Flag a brute force warning if failures cross a threshold limit
        if failed_count > 5:
            summary += f"[CRITICAL WARNING] Potential SSH Brute-Force Activity Detected!\n"
            
        if recent_alerts:
            summary += "\n[!] Recent Log Event Samples:\n"
            for alert in recent_alerts:
                summary += f"  - {alert}\n"
                
        return summary

    except PermissionError:
        return "[Daisy Error] Access Denied. Linux system logs require elevated root privileges. Run with 'sudo'."
    except Exception as e:
        return f"[Daisy Error] Could not read logs: {str(e)}"

if __name__ == "__main__":
    # Test running our analyzer module
    report = analyze_auth_logs()
    print(report)
