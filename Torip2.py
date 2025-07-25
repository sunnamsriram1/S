import os
import time
import subprocess
import psutil

# Time between IP changes (in seconds)
CHANGE_INTERVAL = 60  # Change every 60 seconds

def get_tor_pid():
    """Get the PID of the Tor process"""
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if 'tor' in proc.info['name']:
            return proc.info['pid']
    return None

def refresh_tor_circuit():
    """Send SIGHUP to Tor to refresh the circuit (get new IP)"""
    tor_pid = get_tor_pid()
    if tor_pid:
        os.system(f"kill -HUP {tor_pid}")
        print("[✓] Tor circuit refreshed.")
    else:
        print("[!] Tor process not found.")

def get_current_ip():
    """Fetch current IP using torsocks and curl (retry once if needed)"""
    for attempt in range(2):  # Try twice
        try:
            result = subprocess.check_output(
                ["torsocks", "curl", "-s", "https://ifconfig.me"],
                stderr=subprocess.DEVNULL
            )
            return result.decode().strip()
        except subprocess.CalledProcessError:
            time.sleep(2)  # Wait before retry
    return "Error: Unable to fetch IP"

def main():
    print("🛡️ Tor IP Auto-Changer Script Started...\n")
    try:
        while True:
            current_ip = get_current_ip()
            print(f"[🌐] Current IP: {current_ip}")
            refresh_tor_circuit()
            time.sleep(CHANGE_INTERVAL)
    except KeyboardInterrupt:
        print("\n[✋] Script stopped by user.")

if __name__ == "__main__":
    main()
