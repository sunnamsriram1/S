#!/usr/bin/env python3
import os
import sys
import time
import json
import subprocess
import itertools
import threading
import psutil

# 🎨 Colors
rainbow_colors = [
    '\033[38;5;196m', '\033[38;5;202m', '\033[38;5;226m',
    '\033[38;5;46m', '\033[38;5;21m', '\033[38;5;93m', '\033[38;5;201m'
]
reset = '\033[0m'

# 🌈 Rainbow Banner
def rainbow_banner(text):
    print()
    for i, char in enumerate(text):
        color = rainbow_colors[i % len(rainbow_colors)]
        print(f"{color}{char}", end='', flush=True)
        time.sleep(0.02)
    print(reset + '\n')

# ⌨️ Typewriter Effect
def typewriter(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# ➿ Marquee Scroll
def marquee(text, width=40, speed=0.1, repeat=1):
    space = " " * width
    text = space + text + space
    for _ in range(repeat * len(text)):
        print('\r' + text[:width], end='', flush=True)
        text = text[1:] + text[0]
        time.sleep(speed)
    print()

# 🔁 Spinner (Fixed)
def loading_spinner(duration=5):
    done = [False]

    def animate():
        for c in itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']):
            if done[0]:
                break
            print(f'\r{c} Loading...', end='', flush=True)
            time.sleep(0.1)
        print('\r✅ Done!        ')

    t = threading.Thread(target=animate)
    t.start()
    time.sleep(duration)
    done[0] = True
    t.join()

# 🔰 Intro
def show_intro_banner():
    os.system("clear")
    rainbow_banner("🔥 __SUNNAM SRIRAM__ - __SUNNAM_SRIRAM__ 🔥")
    typewriter(">> Advanced Terminal Interface Loading...\n")
    marquee("🚀 BOYRAM | Coded by | GitHub: sunnamsriram1 🚀", speed=0.07)
    loading_spinner(3)
    print("\n🎉 Welcome to the Script, Commander!\n")

# 🔃 Get Tor PID
def get_tor_pid():
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if 'tor' in proc.info['name'].lower():
            return proc.info['pid']
    return None

# 🔁 Refresh Tor Circuit
def refresh_tor_circuit():
    tor_pid = get_tor_pid()
    if tor_pid:
        os.system(f"kill -HUP {tor_pid}")
        print("🔄 [✓] Tor circuit refreshed.")
    else:
        print("❌ [!] Tor process not found. Please start Tor using `tor`.")

# 🌐 IP Info
def get_ip_info():
    try:
        result = subprocess.run(
            ['torsocks', 'curl', '-s', 'https://ipwhois.app/json/'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            print(f"❌ Error: {result.stderr.strip()}")
            return

        data = json.loads(result.stdout)
        if data.get("success", True):
            print("\n🌐 Tor IP Info:")
            print(f"🧭 IP Address : {data.get('ip', 'N/A')}")
            print(f"🌍 Country    : {data.get('country', 'N/A')} ({data.get('country_code', 'N/A')})")
            print(f"🏙  City       : {data.get('city', 'N/A')}")
            print(f"📌 Region     : {data.get('region', 'N/A')}")
            print(f"⏰ Timezone   : {data.get('timezone', 'N/A')}")
            print(f"🏢 ISP        : {data.get('isp', 'N/A')}")
            print(f"🛰  Org        : {data.get('org', 'N/A')}")
            print(f"📶 ASN        : {data.get('asn', 'N/A')}")
        else:
            print(f"⚠️ Failed to fetch IP info: {data.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"❗ Exception: {e}")

# 🧠 Main
def main():
    CHANGE_INTERVAL = 60
    show_intro_banner()
    print("🛡️ Tor IP Auto-Changer + IP Info Script Started...\n")
    try:
        while True:
            get_ip_info()
            refresh_tor_circuit()
            print(f"⏳ Waiting {CHANGE_INTERVAL} sec before next IP change...\n")
            time.sleep(CHANGE_INTERVAL)
    except KeyboardInterrupt:
        print("\n[✋] Script manually stopped by user.")

if __name__ == "__main__":
    main()
