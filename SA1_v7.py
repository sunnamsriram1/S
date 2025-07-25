#!/usr/bin/env python3
import os
import requests
import pytz
import datetime
from colorama import Fore, init

# 🔰 Auto Clear Terminal (Linux/Termux/Unix compatible)
os.system('clear')

# 🟢 Auto Color Reset
init(autoreset=True)

# 🌍 Base Info
coded_by = "SUNNAM SRIRAM"
india_timezone = pytz.timezone('Asia/Kolkata')
current_time = datetime.datetime.now(india_timezone).strftime("%Y-%m-%d %I:%M:%S %p")

# 📍 Location Details
district = "West Godavari"
mandal = "Buttayagudem"
post_office = "Doramamidi"
village = "Pedhajedipudi"

# 🌤️ Preferred fallback locations for weather
preferred_locations = [
    village,
    post_office,
    mandal,
    district,
    "Eluru"  # Capital fallback
]

# 🌐 Weather Fetcher with Fallback
def get_weather(loc):
    try:
        url = f"https://wttr.in/{loc}?format=1"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return res.text.strip()
    except:
        return None
    return None

def get_weather_with_fallback(locations):
    for loc in locations:
        weather = get_weather(loc)
        if weather:
            if "Unknown location" not in weather:
                return f"{loc} — {weather}"
    # If all failed (unknown or no net)
    if is_connected():
        return "Weather Unavailable 🌐"
    else:
        return "Weather Offline ❌"

# 🌐 Internet connectivity checker
def is_connected():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except:
        return False

# 🛰️ Weather Report
weather_report = get_weather_with_fallback(preferred_locations)

# 🧾 Final Banner Output
banner = f"""
┌────────────────────────────────────────────────────────┐
│   Coded by     : {Fore.WHITE}{coded_by}
│   India Time   : {Fore.YELLOW}{current_time}
│   District     : {Fore.CYAN}{district}
│   Mandal       : {Fore.CYAN}{mandal}
│   Post Office  : {Fore.CYAN}{post_office}
│   Village      : {Fore.CYAN}{village}
│   Weather      : {Fore.GREEN}{weather_report}
│   Status       : {Fore.BLUE}🛰️ System Online — Awaiting Command
└────────────────────────────────────────────────────────┘
"""

print(banner)
