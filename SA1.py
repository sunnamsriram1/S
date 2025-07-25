#!/usr/bin/env python3
import itertools
import sys
import time
import threading
import os
from colorama import Fore, Style, init

init(autoreset=True)

# 🌟 Fancy spinner characters
spinner = itertools.cycle(["🔹", "🔷", "🔶", "🔸", "🔺"])
done = False

# 🎬 Cinematic clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# 🔄 Spinner thread
def spinner_with_loading(duration=4):
    global done
    def animate():
        while not done:
            symbol = next(spinner)
            sys.stdout.write(f'\r{Fore.CYAN} {symbol} Initializing...')
            sys.stdout.flush()
            time.sleep(0.2)
    t = threading.Thread(target=animate)
    t.start()
    time.sleep(duration)
    done = True
    sys.stdout.write('\r' + ' ' * 40 + '\r')

# ✨ Reveal name with spacing and delay
def reveal_name(name):
    print(Fore.YELLOW + Style.BRIGHT + "\n✨ Coded by :\n")
    for char in name:
        print(Fore.GREEN + Style.BRIGHT + char, end=' ', flush=True)
        time.sleep(0.15)
    print(Fore.LIGHTMAGENTA_EX + "\n\n🎉 Successfully Loaded!\n")

# 🧠 Main Runner
if __name__ == "__main__":
    clear_screen()
    spinner_with_loading(5)
    reveal_name("SUNNAM SRIRAM")
