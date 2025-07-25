import os
import time
import subprocess
import psutil

# Set the interval for IP change in seconds
CHANGE_INTERVAL = 3  # Change IP every 60 seconds

def get_tor_pid():
    """Get the PID of the running Tor process"""
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if 'tor' in proc.info['name']:
            return proc.info['pid']
    return None

def refresh_tor_circuit():
    """Send SIGHUP to Tor to request new circuit (new IP)"""
    tor_pid = get_tor_pid()
    if tor_pid:
        os.system(f"kill -HUP {tor_pid}")
        print("[✓] Tor circuit refreshed.")
    else:
        print("[!] Tor process not found.")

def get_current_ip():
    """Get current Tor-exit IP address"""
    try:
        result = subprocess.check_output(["torsocks", "curl", "-s", "https://ifconfig.me"])
        return result.decode().strip()
    except Exception as e:
        return f"Error: {e}"

def main():
    print("🛡️ Tor IP Auto-Changer Script Started...")
    while True:
        current_ip = get_current_ip()
        print(f"[🌐] Current IP: {current_ip}")
        refresh_tor_circuit()
        time.sleep(CHANGE_INTERVAL)

if __name__ == "__main__":
    main()
