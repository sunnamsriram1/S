import itertools
import sys
import time
from colorama import Fore, init

init(autoreset=True)

name = "SUNNAM SRIRAM"
done = False

def spinner_with_name(duration=5):
    global done
    spinner = itertools.cycle(name)  # Spinner characters = your name

    def animate():
        while not done:
            char = next(spinner)
            sys.stdout.write(f'\r{Fore.YELLOW}{char} Loading... ')
            sys.stdout.flush()
            time.sleep(0.1)

    import threading
    t = threading.Thread(target=animate)
    t.start()

    time.sleep(duration)
    done = True
    sys.stdout.write(f'\r{Fore.GREEN}✅ Done!{" " * 20}\n')

spinner_with_name()
