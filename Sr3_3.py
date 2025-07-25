import itertools
import sys
import time
import threading
from colorama import Fore, init

init(autoreset=True)

name = "SUNNAM SRIRAM"
done = False

def spinner_with_name(duration=5):
    global done
    spinner = itertools.cycle(name)

    def animate():
        while not done:
            char = next(spinner)
            sys.stdout.write(f'\r{Fore.CYAN}🔄 {char} Loading... ')
            sys.stdout.flush()
            time.sleep(0.1)

    t = threading.Thread(target=animate)
    t.start()

    time.sleep(duration)
    done = True

    # 🧹 Clear spinner line and move to new line
    sys.stdout.write('\r' + ' ' * 50 + '\r\n')
    sys.stdout.flush()

def reveal_name(name):
    print(Fore.YELLOW + "✨ Welcome to My World:\n")
    for char in name:
        print(Fore.GREEN + char, end=' ', flush=True)
        time.sleep(0.2)
    print("\n")  # Final new line

# 🌀 Run animation and name reveal
spinner_with_name(5)
reveal_name(name)
