#!/usr/bin/env python3
import itertools
import sys
import time
import threading
from colorama import Fore, Style, init

init(autoreset=True)

# 🌟 Name and spinner setup
name = "SUNNAM SRIRAM"
spinner = itertools.cycle(["🌑", "🌓", "🌕", "🌗"])  # Moon phase spinner
done = False

# 🔄 Spinner function
def spinner_with_name(duration=5):
    global done
    def animate():
        while not done:
            char = next(spinner)
            sys.stdout.write(f'\r{Fore.CYAN} {char} Loading...')
            sys.stdout.flush()
            time.sleep(0.2)
    t = threading.Thread(target=animate)
    t.start()
    time.sleep(duration)
    done = True
    sys.stdout.write('\r' + ' ' * 30 + '\r')  # Clear line

# ✨ Reveal name function
def reveal_name(name):
    print(Fore.MAGENTA + "✨ Welcome to My World:")
    for char in name:
        print(Fore.GREEN + char, end=' ', flush=True)
        time.sleep(0.2)
    print("\n" + Fore.YELLOW + "✅ Name revealed successfully!")

# 🔁 Run both
if __name__ == "__main__":
    spinner_with_name(5)
    reveal_name(name)

