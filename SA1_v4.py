import requests
import pytz
import datetime
from colorama import Fore, init

init(autoreset=True)

# ✅ Updated Location Details
coded_by = "SUNNAM SRIRAM"
district = "West Godavari"
mandal = "Buttayagudem"
post = "Doramamidi"
village = "Pedhajedipudi"
location = village  # For weather query

# ✅ Time Handling
india_timezone = pytz.timezone('Asia/Kolkata')
current_time = datetime.datetime.now(india_timezone).strftime("%Y-%m-%d %I:%M:%S %p")

# ✅ Weather Fetch Function
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

# ✅ Get live weather report
weather_report = get_weather(location)

# ✅ Final Banner Output
banner = f"""
┌────────────────────────────────────────────────────────┐
│   Coded by     : {Fore.WHITE}{coded_by}
│   India Time   : {Fore.YELLOW}{current_time}
│   District     : {Fore.CYAN}{district}
│   Mandal       : {Fore.CYAN}{mandal}
│   Post Office  : {Fore.CYAN}{post}
│   Village      : {Fore.CYAN}{village}
│   Weather      : {Fore.GREEN}{weather_report}
│   Status       : {Fore.BLUE}🛰️ System Online — Awaiting Command
└────────────────────────────────────────────────────────┘
"""

# ✅ Show banner
print(banner)
