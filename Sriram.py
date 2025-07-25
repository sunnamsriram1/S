#!/usr/bin/env python3
import time
import threading
import itertools
from colorama import Fore, Style, init

init(autoreset=True)

# ✅ Loading Spinner Function
def loading_spinner(duration=4):
    done = False

    def animate():
        for c in itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']):
            if done:
                break
            print(f'\r{Fore.YELLOW}{c} Loading...', end='', flush=True)
            time.sleep(0.1)

    t = threading.Thread(target=animate)
    t.start()
    time.sleep(duration)
    done = True
    print(f'\r{Fore.GREEN}✅ Ready!            ')
    print(f'{Fore.CYAN}⚙️  Coded by SunnamSriram')

# ✅ Run Spinner for demo
if __name__ == "__main__":
    loading_spinner(4)
