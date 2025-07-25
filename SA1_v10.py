#!/usr/bin/env python3
import os
import requests
import pytz
import datetime
from colorama import Fore, init
import time
import platform

# ✅ Init & Clear
init(autoreset=True)
os.system('clear' if os.name == 'posix' else 'cls')

# ✅ Base Info
coded_by = "SUNNAM SRIRAM"
india_timezone = pytz.timezone('Asia/Kolkata')
current_time = datetime.datetime.now(india_timezone).strftime("%Y-%m-%d %I:%M:%S %p")

# ✅ Location Details
district = "West Godavari"
mandal = "Buttayagudem"
post_office = "Doramamidi"
village = "Pedhajedipudi"

# ✅ Weather Location Preference
preferred_locations = [
    village,
    post_office,
    mandal,
    district,
    "Eluru"
]

# ✅ Log File
log_file = "SA1_log.txt"
def log_event(msg):
    with open(log_file, "a") as f:
        f.write(f"[{current_time}] {msg}\n")

# ✅ Sound Alert
def play_alert():
    try:
        if platform.system() == "Linux":
            os.system('termux-vibrate -d 200')
            os.system('termux-toast "🔔 Status changed"')
        print('\a', end='')  # Bell alert
    except:
        pass

# ✅ Internet Check
def check_online():
    try:
        requests.get("https://google.com", timeout=5)
        return True
    except:
        return False

# ✅ Weather Fetch
def get_weather(loc):
    try:
        url = f"https://wttr.in/{loc}?format=1"
        res = requests.get(url, timeout=5)
        if res.status_code == 200 and "Unknown location" not in res.text:
            return f"{loc} — {res.text.strip()}"
    except:
        return None
    return None

def get_weather_with_fallback(locations):
    for loc in locations:
        weather = get_weather(loc)
        if weather:
            return weather
    return "Weather Offline ❌"

# ✅ Determine Status
is_online = check_online()
status_text = "🟢 ONLINE" if is_online else "🔴 OFFLINE"
status_color = Fore.GREEN if is_online else Fore.RED

# ✅ Play alert & log
log_event(f"System {status_text}")
play_alert()

# ✅ Weather Report
weather_report = get_weather_with_fallback(preferred_locations)

# ✅ Banner Output
banner = f"""
┌────────────────────────────────────────────────────────┐
│   Coded by     : {Fore.WHITE}{coded_by}
│   India Time   : {Fore.YELLOW}{current_time}
│   District     : {Fore.CYAN}{district}
│   Mandal       : {Fore.CYAN}{mandal}
│   Post Office  : {Fore.CYAN}{post_office}
│   Village      : {Fore.CYAN}{village}
│   Weather      : {Fore.GREEN}{weather_report}
│   Status       : {status_color}{status_text}
└────────────────────────────────────────────────────────┘
"""

print(banner)

# ✅ Command Input
try:
    user_cmd = input(Fore.YELLOW + "📥 Enter command or 'exit': ")
    if user_cmd.strip().lower() != 'exit':
        os.system(user_cmd)
except KeyboardInterrupt:
    print(Fore.RED + "\nCancelled by user.")
