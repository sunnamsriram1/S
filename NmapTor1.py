#!/usr/bin/env python3
import os
import sys
import time
import random
import threading
import requests
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# Config
LOG_FILE = "nmap_tor_log.txt"
PROXY = "socks5h://127.0.0.1:9050"
CHECK_IP_URL = "https://check.torproject.org/api/ip"

# Rainbow Title
def rainbow(text):
    colors = [31, 33, 32, 36, 34, 35]
    for i, char in enumerate(text):
        sys.stdout.write(f"\033[1;{colors[i % len(colors)]}m{char}\033[0m")
        sys.stdout.flush()
        time.sleep(0.02)
    print()

# Spinner
def loading_spinner(stop_event, msg="Connecting via Tor..."):
    spinner = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{Fore.YELLOW}{spinner[i % len(spinner)]} {msg}")
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)
    print("\r", end="")

# Tor IP checker
def get_tor_ip():
    try:
        response = requests.get(CHECK_IP_URL, proxies={'http': PROXY, 'https': PROXY}, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data['IP'], data['IsTor']
    except:
        pass
    return None, False

# Restart Tor
def restart_tor():
    print(Fore.YELLOW + "🔄 Restarting Tor service...")
    os.system("tor &")
    time.sleep(5)

# Run Nmap with ProxyChains
def run_nmap(target):
    cmd = f"proxychains4 nmap -sT -Pn -n --script ssl-cert {target}"
    print(Fore.CYAN + f"[~] Running Nmap on {target} with proxychains...\n")
    os.system(cmd)

# Log
def write_log(ip, target):
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{datetime.now()}] TorIP: {ip} → Target: {target}\n")

# Main
def main():
    os.system("clear")
    rainbow("🌐 TORMAP — Smart Tor + ProxyChains + Nmap Tool")
    print(Fore.GREEN + "🛡️ Secure & Anonymous Scanning with Auto IP Rotation\n")

    restart_tor()

    # Connect via Tor
    stop_event = threading.Event()
    spinner = threading.Thread(target=loading_spinner, args=(stop_event,))
    spinner.start()

    tor_ip, is_tor = get_tor_ip()
    stop_event.set()
    spinner.join()

    if tor_ip and is_tor:
        print(Fore.GREEN + f"[✓] Connected via Tor: {tor_ip}")
    else:
        print(Fore.RED + "[✗] Failed to connect via Tor")
        return

    # Target input
    target = input(Fore.YELLOW + "\n🔍 Enter Target Domain/IP: ").strip()

    if not target:
        print(Fore.RED + "[!] No target entered.")
        return

    # Scan with Nmap via proxychains
    run_nmap(target)

    # Log
    write_log(tor_ip, target)

    print(Fore.MAGENTA + f"\n📝 Scan log saved to {LOG_FILE}")
    print(Fore.BLUE + f"🔚 Done at {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}")
    print(Style.BRIGHT + Fore.CYAN + "💡 Tool by SRIRAM")

if __name__ == "__main__":
    main()
