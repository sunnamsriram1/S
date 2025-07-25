#!/usr/bin/env python3
import os
import time
import subprocess
from colorama import Fore, Style, init
from datetime import datetime

init(autoreset=True)

def banner():
    print(Fore.CYAN + Style.BRIGHT + "\n🌐 TORMAP — Smart Tor + ProxyChains + Nmap Tool")
    print(Fore.YELLOW + "🛡️ Secure & Anonymous Scanning with Auto IP Rotation\n")

def is_tor_running():
    try:
        result = os.popen("pgrep tor").read().strip()
        return bool(result)
    except:
        return False

def restart_tor():
    if is_tor_running():
        print(Fore.GREEN + "[✓] Tor is already running.")
    else:
        print(Fore.YELLOW + "🔄 Starting Tor service...")
        os.system("tor &")
        time.sleep(5)

def get_tor_ip():
    try:
        ip = subprocess.check_output(
            ['proxychains4', 'curl', '-s', 'https://ifconfig.me'],
            stderr=subprocess.DEVNULL
        ).decode().strip()
        return ip
    except:
        return None

def run_nmap(target, log_file):
    print(Fore.BLUE + f"🔍 Scanning {target} via Nmap over Tor...")
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    command = f"proxychains4 nmap -sS -Pn -n -T4 {target}"
    result = os.popen(command).read()
    print(Fore.GREEN + result)

    with open(log_file, "a") as log:
        log.write(f"\n[{timestamp}] {target}\n")
        log.write(result)
        log.write("\n" + "="*50 + "\n")

def main():
    banner()
    restart_tor()

    ip = get_tor_ip()
    if not ip:
        print(Fore.RED + "[✗] Failed to connect via Tor (proxychains4 or Tor issue)")
        return

    print(Fore.GREEN + f"[✓] Connected via Tor IP: {ip}")
    
    target = input(Fore.CYAN + "🌐 Enter target (domain/IP): ").strip()
    if not target:
        print(Fore.RED + "[✗] No target provided. Exiting.")
        return

    log_file = "nmap_tormap_logs.txt"
    run_nmap(target, log_file)

    print(Fore.YELLOW + "\n📁 Results saved to:", log_file)

if __name__ == "__main__":
    main()
