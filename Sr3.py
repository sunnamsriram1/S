
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
    sys.stdout.write('\r' + ' ' * 30 + '\r')  # Clear line

def reveal_name(name):
    print(Fore.YELLOW + "✨ Welcome to My World:")
    for char in name:
        print(Fore.GREEN + char, end=' ', flush=True)
        time.sleep(0.2)
    #print(Fore.GREEN + "\n✅ Name displayed successfully!")

# 🔁 Run both
spinner_with_name(5)
reveal_name(name)
