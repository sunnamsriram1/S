#!/usr/bin/env python3
import os, time, subprocess, requests
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

LOG_DIR = os.path.expanduser("~/tor_nmap_logs")
os.makedirs(LOG_DIR, exist_ok=True)

def restart_tor():
    print(Fore.YELLOW+ "🔄 Restarting Tor service...")
    os.system("pkill tor >/dev/null 2>&1")
    os.system("tor &")
    time.sleep(10)

def get_tor_ip():
    try:
        r = requests.get("https://check.torproject.org/api/ip", proxies={
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }, timeout=10)
        return r.json().get("IP")
    except:
        return None

def nmap_tor_scan(target):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(LOG_DIR, f"scan_{target.replace('.', '_')}_{timestamp}.txt")
    print(Fore.CYAN + f"📡 Scanning target via Tor: {target}")
    cmd = f"proxychains4 nmap -Pn -sS -T3 -n {target} -oN {log_path}"
    os.system(cmd)
    print(Fore.GREEN + f"✔️ Scan finished. Log saved to {log_path}")

def main():
    print(Fore.MAGENTA + "\n🛡️ TOR NMAP TOOL - Secure Anonymous Scanner")
    targets = input(Fore.BLUE + "📥 Enter targets (comma-separated IPs or domains): ").split(',')

    for target in targets:
        target = target.strip()
        restart_tor()
        tor_ip = get_tor_ip()
        if tor_ip:
            print(Fore.GREEN + f"🧅 Tor IP: {tor_ip}")
            nmap_tor_scan(target)
        else:
            print(Fore.RED + "⚠️ Failed to fetch Tor IP. Skipping scan.")

if __name__ == "__main__":
    main()
