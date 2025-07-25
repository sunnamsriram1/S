#!/usr/bin/env python3
import os
import requests
import pytz
import datetime
from colorama import Fore, init
from time import sleep

# 🔰 Auto Clear Terminal
os.system('clear')

# 🟢 Color Reset
init(autoreset=True)

# 📁 Log File Path
LOG_FILE = "sa1_log.txt"

# 🌍 Info
coded_by = "SUNNAM SRIRAM"
india_timezone = pytz.timezone('Asia/Kolkata')
current_time = datetime.datetime.now(india_timezone).strftime("%Y-%m-%d %I:%M:%S %p")

# 📍 Location
district = "West Godavari"
mandal = "Buttayagudem"
post_office = "Doramamidi"
village = "Pedhajedipudi"

# 🌤️ Weather Fallback Locations
preferred_locations = [
    village, post_office, mandal, district, "Eluru"
]

# 🌐 Weather Checker
def get_weather(loc):
    try:
        url = f"https://wttr.in/{loc}?format=1"
        res = requests.get(url, timeout=4)
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

# 🔌 Internet Status
def is_online():
    try:
        requests.get("https://www.google.com", timeout=3)
        return True
    except:
        return False

# 🔊 Play sound alert (Termux only)
def play_alert():
    os.system("termux-media-player play /system/media/audio/ui/Effect_Tick.ogg 2>/dev/null")

# 📥 Command Logger
def log_command(cmd):
    with open(LOG_FILE, "a") as f:
        now = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
        f.write(f"[{now}] {cmd}\n")

# ✅ Status + Weather
weather = get_weather_with_fallback(preferred_locations)
online_status = is_online()
status_text = f"{Fore.GREEN}🟢 ONLINE" if online_status else f"{Fore.RED}🔴 OFFLINE"

# 🖥️ Banner Display
banner = f"""
┌────────────────────────────────────────────────────────┐
│   Coded by     : {Fore.WHITE}{coded_by}
│   India Time   : {Fore.YELLOW}{current_time}
│   District     : {Fore.CYAN}{district}
│   Mandal       : {Fore.CYAN}{mandal}
│   Post Office  : {Fore.CYAN}{post_office}
│   Village      : {Fore.CYAN}{village}
│   Weather      : {Fore.GREEN if '°' in weather else Fore.RED}{weather}
│   Status       : {status_text}
└────────────────────────────────────────────────────────┘
"""

print(banner)

# 🔔 Optional Termux Alert
if online_status:
    play_alert()
    os.system("termux-toast -b green -c black '🟢 ONLINE - Awaiting Command' 2>/dev/null")
else:
    os.system("termux-toast -b red -c white '🔴 OFFLINE - Check Network' 2>/dev/null")

# 💬 Command Input Loop
while True:
    try:
        user_input = input(f"📥 Enter command or 'exit': {Fore.YELLOW}")
        if user_input.lower() == "exit":
            print(Fore.CYAN + "🚪 Exiting. Logged session saved.")
            break
        os.system(user_input)
        log_command(user_input)
    except KeyboardInterrupt:
        print(Fore.RED + "\n⛔ Interrupted by user. Exiting.")
        break
