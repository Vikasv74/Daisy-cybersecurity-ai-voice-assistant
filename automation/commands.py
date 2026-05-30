import subprocess
import os

# IMPORTANT: Safety Allowlist (Only allow specific safe tools to run)
ALLOWLISTED_COMMANDS = {
    "firefox": ["firefox"],
    "calculator": ["gnome-calculator"],
    "text editor": ["gedit"],
    "system stats": ["top", "-b", "-n", "1"]
}

def execute_automation_command(action_key):
    """
    Safely executes an application or system instruction if it's on the allowlist.
    """
    action_key = action_key.lower().strip()
    
    if action_key in ALLOWLISTED_COMMANDS:
        print(f"[Daisy Automation] Executing safe command for: '{action_key}'...")
        try:
            # Run the command in the background so it doesn't freeze Daisy
            subprocess.Popen(ALLOWLISTED_COMMANDS[action_key], 
                             stdout=subprocess.DEVNULL, 
                             stderr=subprocess.DEVNULL)
            return f"Successfully launched {action_key}."
        except Exception as e:
            return f"Failed to execute {action_key}: {str(e)}"
    else:
        print(f"[Daisy Security Warning] Blocked attempt to run unauthorized action: '{action_key}'")
        return "Action denied. That command is not on my safety allowlist."

def read_safe_file(file_path):
    """
    Safely reads allowed files (e.g., standard logs or project notes).
    """
    # Prevent directory traversal attacks (don't let it read system files like /etc/passwd)
    if ".." in file_path or file_path.startswith("/"):
        return "Access denied: Cannot read files outside the project scope."
        
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    else:
        return "File not found."

if __name__ == "__main__":
    # Test launching Firefox safely
    print(execute_automation_command("firefox"))
    
    # Test an unauthorized command attempt
    print(execute_automation_command("rm -rf /"))
