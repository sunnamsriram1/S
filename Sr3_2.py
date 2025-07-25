import itertools
import sys
import time
import threading
from colorama import Fore, init

init(autoreset=True)

# 💬 Name to spin and reveal
name = "SUNNAM SRIRAM"
done = False

def spinner_with_name(duration=5):
    global done
    spinner = itertools.cycle(name)  # Cycle through name characters

    def animate():
        while not done:
            char = next(spinner)
            sys.stdout.write(f'\r{Fore.CYAN}🔄 {char} Loading...')
            sys.stdout.flush()
            time.sleep(0.1)

    t = threading.Thread(target=animate)
    t.start()

    # Spinner duration
    time.sleep(duration)
    done = True

    # Clear spinner line properly
    sys.stdout.write('\r' + ' ' * 50 + '\r')
    sys.stdout.flush()
    print()  # 🔁 Ensure new line after spinner ends

def reveal_name(name):
    print(Fore.YELLOW + "✨ Welcome to My World:\n")
    for char in name:
        print(Fore.GREEN + char, end=' ', flush=True)
        time.sleep(0.2)
    print("\n")  # ✅ Print TWO newlines to avoid overlapping prompt

# 🔁 Run both
spinner_with_name(5)
reveal_name(name)
