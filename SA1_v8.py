#!/data/data/com.termux/files/usr/bin/python3

import os
import requests
import pytz
import datetime
from colorama import Fore, init

# 🔰 Clear Terminal
os.system('clear')

# 🟢 Auto Color Reset
init(autoreset=True)

# 🧠 Coder Info
coded_by = "SUNNAM SRIRAM"
india_timezone = pytz.timezone('Asia/Kolkata')
current_time = datetime.datetime.now(india_timezone).strftime("%Y-%m-%d %I:%M:%S %p")

# 📍 Location Details
district = "West Godavari"
mandal = "Buttayagudem"
post_office = "Doramamidi"
village = "Pedhajedipudi"

# 🌤️ Preferred Locations
preferred_locations = [
    village,
    post_office,
    mandal,
    district,
    "Eluru"  # fallback
]

# 🌐 Check if Internet is Available
def check_internet():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except:
        return False

# 🌤️ Weather Fetch with Fallback
def get_weather(loc):
    try:
        url = f"https://wttr.in/{loc}?format=1"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return res.text.strip()
    except:
        pass
    return None

def get_weather_with_fallback(locations):
    for loc in locations:
        weather = get_weather(loc)
        if weather and "Unknown location" not in weather:
            return f"{loc} — {weather}"
    return "Weather Offline ❌"

# 🛰️ Get Final Weather & System Status
if check_internet():
    weather_report = get_weather_with_fallback(preferred_locations)
    system_status = f"{Fore.BLUE}🛰️ System Online"
else:
    weather_report = "Weather Offline ❌"
    system_status = f"{Fore.RED}📴 System Offline"

# 🧾 Final Output
banner = f"""
┌────────────────────────────────────────────────────────┐
│   Coded by     : {Fore.WHITE}{coded_by}
│   India Time   : {Fore.YELLOW}{current_time}
│   District     : {Fore.CYAN}{district}
│   Mandal       : {Fore.CYAN}{mandal}
│   Post Office  : {Fore.CYAN}{post_office}
│   Village      : {Fore.CYAN}{village}
│   Weather      : {Fore.GREEN}{weather_report}
│   Status       : {system_status}
└────────────────────────────────────────────────────────┘
"""

print(banner)
