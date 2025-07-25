#!/usr/bin/env python3
import os
import sys
import time
import threading
import requests
from datetime import datetime
from colorama import Fore, Style, init

# Init colorama
init(autoreset=True)

# Tor IP check endpoint
TOR_IP_CHECK_URL = "https://check.torproject.org/api/ip"

# Rainbow text effect
def rainbow_text(text):
    colors = [31, 33, 32, 36, 34, 35]
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        sys.stdout.write(f"\033[1;{color}m{char}\033[0m")
        sys.stdout.flush()
        time.sleep(0.03)
    print()

# Typewriter animation
def typewriter(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# Spinner animation during IP fetch
def spinner_animation(stop_event):
    spinner = ['⠋','⠙','⠹','⠸','⠼','⠴','⠦','⠧','⠇','⠏']
    i = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{Fore.YELLOW}{spinner[i % len(spinner)]} Connecting via Tor...")
        sys.stdout.flush()
        i += 1
        time.sleep(0.1)
    print("\r", end="")

# Get current Tor IP
def get_tor_ip():
    try:
        response = requests.get(TOR_IP_CHECK_URL, proxies={
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data['IP'], data['IsTor']
    except:
        return None, False
    return None, False

# Main logic
def main():
    os.system("clear")
    rainbow_text("🌈  BOYR4M TOR TOOL 🌐")
    print('\a')  # Terminal beep
    typewriter("🔐 Checking secure connection via Tor...\n", 0.03)

    stop_event = threading.Event()
    thread = threading.Thread(target=spinner_animation, args=(stop_event,))
    thread.start()

    ip, is_tor = get_tor_ip()

    stop_event.set()
    thread.join()

    print()  # newline
    if ip and is_tor:
        print(f"{Fore.GREEN}[✓] Tor IP Detected: {ip}")
        print(f"{Fore.CYAN}[🔒] You are safely connected through Tor ✅")
    else:
        print(f"{Fore.RED}[✗] Tor connection failed or not detected")
        print(f"{Fore.YELLOW}[!] Check Tor status or proxychains config")

    print(f"{Fore.MAGENTA}⏱️ Time: {datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}")
    print(f"{Fore.BLUE}👨‍💻 Tool by: SUNNAM_SRIRAM_1")

# Run the program
if __name__ == "__main__":
    main()
