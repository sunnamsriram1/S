import os
import sys
import time
import itertools
import threading

# ANSI Rainbow Colors (256-color codes)
rainbow_colors = [
    '\033[38;5;196m', '\033[38;5;202m', '\033[38;5;226m',
    '\033[38;5;46m', '\033[38;5;21m', '\033[38;5;93m', '\033[38;5;201m'
]
reset = '\033[0m'

# Clear screen
os.system('clear')

# 🌈 Rainbow Text Banner
def rainbow_banner(text):
    print()
    for i, char in enumerate(text):
        color = rainbow_colors[i % len(rainbow_colors)]
        print(f"{color}{char}", end='')
        sys.stdout.flush()
        time.sleep(0.03)
    print(reset + '\n')

# 🖋️ Typewriter Animation
def typewriter(text, delay=0.05):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

# 🎞️ Marquee Scrolling Text
def marquee(text, width=40, speed=0.1, repeat=1):
    space = " " * width
    text = space + text + space
    for _ in range(repeat * len(text)):
        print('\r' + text[:width], end='')
        text = text[1:] + text[0]
        time.sleep(speed)
    print()

# ⏳ Loading Spinner (non-blocking)
def loading_spinner(duration=5):
    done = False
    def animate():
        for c in itertools.cycle(['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']):
            if done:
                break
            print(f'\r{c} Loading...', end='', flush=True)
            time.sleep(0.1)

    t = threading.Thread(target=animate)
    t.start()
    time.sleep(duration)
    done = True
    time.sleep(0.3)
    print('\r✅ Done!        ')

# 🧠 Final Banner with All Effects
def full_banner():
    rainbow_banner("🔥 __SUNNAM SRIRAM__ - __SUNNAM_SRIRAM__ 🔥")
    typewriter(">> Advanced Terminal Interface Loading...\n")
    marquee("🚀 BOYRAM | Coded by | GitHub: sunnamsriram1 🚀", speed=0.07)
    loading_spinner(4)
    print("\n🎉 Welcome to the Script, Commander!\n")

# 🔥 RUN IT
if __name__ == "__main__":
    full_banner()
