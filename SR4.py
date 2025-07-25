import itertools
import sys
import time
import threading
from colorama import Fore, init
import random

init(autoreset=True)

# 💬 Your Name
name = "SUNNAM SRIRAM"
done = False

# 🎨 Gradient colors (pick randomly per character)
colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA, Fore.LIGHTRED_EX, Fore.LIGHTBLUE_EX]

# 🎆 Firework emojis
fireworks = ['🎆', '✨', '🎇', '💥', '🔥']

# 🔁 Spinner with fireworks & name characters
def spinner_with_fireworks(duration=5):
    global done
    spinner = itertools.cycle(name)

    def animate():
        while not done:
            char = next(spinner)
            color = random.choice(colors)
            fire = random.choice(fireworks)
            sys.stdout.write(f'\r{color}{fire} Loading {char}... {fire}')
            sys.stdout.flush()
            time.sleep(0.15)

    t = threading.Thread(target=animate)
    t.start()
    time.sleep(duration)
    done = True
    sys.stdout.write('\r' + ' ' * 40 + '\r')  # Clear line

# ✨ Reveal each character with gradient + emoji
def reveal_name_effect(name):
    print(Fore.YELLOW + "\n✨ Final Reveal:\n")
    for char in name:
        color = random.choice(colors)
        emoji = random.choice(fireworks)
        sys.stdout.write(f'{color}{emoji} {char} ')
        sys.stdout.flush()
        time.sleep(0.25)
    print(Fore.LIGHTGREEN_EX + "\n\n✅ Display complete! 🔐")

# 🚀 Run the full animation
spinner_with_fireworks(duration=5)
reveal_name_effect(name)
