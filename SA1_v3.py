import requests
import pytz
import datetime
from colorama import Fore, init

init(autoreset=True)

coded_by = "SUNNAM SRIRAM"
location = "Hyderabad"  # You can change this
india_timezone = pytz.timezone('Asia/Kolkata')
current_time = datetime.datetime.now(india_timezone).strftime("%Y-%m-%d %I:%M:%S %p")

def get_weather(loc):
    try:
        url = f"https://wttr.in/{loc}?format=1"
        res = requests.get(url)
        if res.status_code == 200:
            return res.text.strip()
        else:
            return "Weather Unavailable 🌐"
    except:
        return "Weather Offline ❌"

weather_report = get_weather(location)

# 🧾 Final Banner Output
banner = f"""
┌──────────────────────────────────────────────┐
│   Coded by     : {Fore.WHITE}{coded_by}
│   India Time   : {Fore.YELLOW}{current_time}
│   Location     : {Fore.MAGENTA}{location}
│   Weather      : {Fore.GREEN}{weather_report}
│   Status       : {Fore.BLUE}🛰️ System Online — Awaiting
└──────────────────────────────────────────────┘
"""
print(banner)
