#!/usr/bin/env python3
import itertools
import sys
import time
import threading
import os
import datetime
import pytz
from colorama import Fore, init

init(autoreset=True)

# 🔁 Spinner
spinner = itertools.cycle(["🔹", "🔷", "🔶", "🔸", "🔺"])
done = False

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

# ⏳ Spinner Function
def spinner_with_loading(duration=3):
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

# 🕒 India Time Banner
def show_banner(coded_by="SUNNAM SRIRAM"):
    india_timezone = pytz.timezone('Asia/Kolkata')
    current_time = datetime.datetime.now(india_timezone).strftime("%Y-%m-%d %I:%M:%S %p")
    
    print(Fore.LIGHTYELLOW_EX + "┌" + "─" * 46 + "┐")
    print(Fore.LIGHTGREEN_EX + "│" + f"   Coded by     : {Fore.WHITE}{coded_by}".ljust(45) + Fore.LIGHTGREEN_EX + "│")
    print(Fore.LIGHTGREEN_EX + "│" + f"   India Time    : {Fore.WHITE}{current_time}".ljust(45) + Fore.LIGHTGREEN_EX + "│")
    print(Fore.LIGHTGREEN_EX + "│" + f"   Status        : {Fore.GREEN}✅ Successfully Loaded!".ljust(45) + Fore.LIGHTGREEN_EX + "│")
    print(Fore.LIGHTYELLOW_EX + "└" + "─" * 46 + "┘")

# 🔰 Main
if __name__ == "__main__":
    clear_screen()
    spinner_with_loading()
    show_banner()
