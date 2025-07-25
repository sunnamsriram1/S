#!/usr/bin/env python3
#!/data/data/com.termux/files/usr/bin/python3

import os
import requests
import pytz
import datetime
from colorama import Fore, init

# 🎨 Initialize color
init(autoreset=True)

# 🧹 Clear Terminal
os.system('clear')

# 👨‍💻 Developer Info
coded_by = "SUNNAM SRIRAM"
india_timezone = pytz.timezone('Asia/Kolkata')
current_time = datetime.datetime.now(india_timezone).strftime("%Y-%m-%d %I:%M:%S %p")

# 📍 Location Info
district = "West Godavari"
mandal = "Buttayagudem"
post_office = "Doramamidi"
village = "Pedhajedipudi"

# 🔁 Location preference for weather
preferred_locations = [
    village,
    post_office,
    mandal,
    district,
    "Eluru"
]

# 🌐 Check internet status
def check_internet():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except:
        return False

# ☁️ Get weather data
def get_weather(loc):
    try:
        url = f"https://wttr.in/{loc}?format=1"
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            return res.text.strip()
    except:
        pass
    return None

# 🔁 Try all locations
def get_weather_with_fallback(locations):
    for loc in locations:
        weather = get_weather(loc)
        if weather and "Unknown location" not in weather:
            return f"{loc} — {weather}"
    return "Weather Offline ❌"

# 🌐 Set status based on internet
if check_internet():
    weather_report = get_weather_with_fallback(preferred_locations)
    status_line = f"{Fore.GREEN}🛰️ System Online"
else:
    weather_report = "Weather Offline ❌"
    status_line = f"{Fore.RED}📴 System Offline"

# 🖨️ Print final display
banner = f"""
┌────────────────────────────────────────────────────────┐
│   Coded by     : {Fore.WHITE}{coded_by}
│   India Time   : {Fore.YELLOW}{current_time}
│   District     : {Fore.CYAN}{district}
│   Mandal       : {Fore.CYAN}{mandal}
│   Post Office  : {Fore.CYAN}{post_office}
│   Village      : {Fore.CYAN}{village}
│   Weather      : {Fore.GREEN}{weather_report}
│   Status       : {status_line}
└────────────────────────────────────────────────────────┘
"""

print(banner)
