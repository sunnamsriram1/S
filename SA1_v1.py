#!/usr/bin/env python3
import itertools
import sys
import time
import threading
import os
import datetime
import pytz
from colorama import Fore, Style, init

init(autoreset=True)

# 🌀 Stylish diamond spinner
spinner = itertools.cycle(["🔹", "🔷", "🔶", "🔸", "🔺"])
done = False

# 🎬 Clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ⏳ Spinner animation
def spinner_with_loading(duration=4):
    global done
    def animate():
        while not done:
            symbol = next(spinner)
            sys.stdout.write(f'\r{Fore.CYAN}{symbol} Initializing... Please wait')
            sys.stdout.flush()
            time.sleep(0.2)
    t = threading.Thread(target=animate)
    t.start()
    time.sleep(duration)
    done = True
    sys.stdout.write('\r' + ' ' * 50 + '\r')

# 🕒 India Time + Banner
def show_banner(coded_by="SUNNAM SRIRAM"):
    india_timezone = pytz.timezone('Asia/Kolkata')
    current_time = datetime.datetime.now(india_timezone).strftime("%Y-%m-%d %I:%M:%S %p")
    banner = f"""
{Fore.LIGHTYELLOW_EX}┌──────────────────────────────────────────────┐
{Fore.LIGHTGREEN_EX}│   Coded by     : {Fore.WHITE}{coded_by}
{Fore.LIGHTGREEN_EX}│   India Time    : {Fore.WHITE}{current_time}
{Fore.LIGHTGREEN_EX}│   Status        : {Fore.GREEN}✅ Successfully Loaded!
{Fore.LIGHTYELLOW_EX}└──────────────────────────────────────────────┘
"""
    print(banner)

# 🧠 Main
if __name__ == "__main__":
    clear_screen()
    spinner_with_loading(5)
    show_banner()
