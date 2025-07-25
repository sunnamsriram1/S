import time
import threading
import itertools
import sys
from colorama import Fore, Style, init

init(autoreset=True)

def print_name_slow(name, delay=0.1):
    sys.stdout.write(Fore.MAGENTA)
    for char in name:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print(Style.RESET_ALL)

def loading_spinner(duration=4):
    done = False

    def animate():
        for c in itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']):
            if done:
                break
            print(f'\r{Fore.YELLOW}{c} Loading... ', end='', flush=True)
            time.sleep(0.1)

    t = threading.Thread(target=animate)
    t.start()
    time.sleep(duration)
    done = True
    print(f'\r{Fore.GREEN}✅ Ready!{" " * 20}')
    time.sleep(0.5)

    print(f"{Fore.CYAN}⚙️  Coded by ", end='')
    print_name_slow("SUNNAM SRIRAM", delay=0.15)

# Run it
if __name__ == "__main__":
    loading_spinner(4)
