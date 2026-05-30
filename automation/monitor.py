import psutil
import shutil

def get_system_metrics():
    """
    Gathers core hardware metrics from the Ubuntu operating system 
    and packages them into a clean text report for Daisy.
    """
    print("[Daisy Monitor] Scanning system hardware metrics...")
    
    # 1. CPU Usage
    cpu_usage = psutil.cpu_percent(interval=1) # Checks utilization over 1 second
    
    # 2. RAM/Memory Usage
    memory = psutil.virtual_memory()
    ram_usage = memory.percent
    
    # 3. Disk Space Usage
    # Passing "/" checks the primary Linux storage partition root
    total, used, free = shutil.disk_usage("/")
    disk_usage_pct = (used / total) * 100

    # 4. Active Processes Counter
    process_count = len(psutil.pids())

    # Build the structural system health summary report
    report = "\n=== Daisy System Status Dashboard ===\n"
    report += f"[+] CPU Utilization:  {cpu_usage}%\n"
    report += f"[+] RAM Utilization:  {ram_usage}%\n"
    report += f"[+] Primary Disk Space: {disk_usage_pct:.1f}% used\n"
    report += f"[+] Active Processes:   {process_count} running\n"
    
    # Add a smart threshold warning for Daisy to flag
    if cpu_usage > 85:
        report += "[!] WARNING: Abnormal CPU usage detected! System is under heavy load.\n"
    if ram_usage > 90:
        report += "[!] WARNING: Critical Memory depletion! Close background tasks.\n"
        
    return report

def get_top_heavy_processes():
    """
    Finds and lists the top 3 processes consuming the most memory.
    """
    print("[Daisy Monitor] Scanning for resource-heavy processes...")
    processes = []
    
    # Iterate through all running processes
    for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            
    # Sort them so the highest memory users are first
    processes = sorted(processes, key=lambda x: x['memory_percent'], reverse=True)
    
    proc_summary = "\n--- Top 3 Resource Heavy Processes ---\n"
    for p in processes[:3]:
        proc_summary += f"  - PID: {p['pid']} | Name: {p['name']} | RAM: {p['memory_percent']:.1f}%\n"
        
    return proc_summary

if __name__ == "__main__":
    # Test our hardware gathering functions
    print(get_system_metrics())
    print(get_top_heavy_processes())
