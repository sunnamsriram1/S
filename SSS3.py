import os
import time
import base64
import random
import string
import shutil
import json
import hashlib
import threading
import itertools
from getpass import getpass
from datetime import datetime
from cryptography.fernet import Fernet
from tqdm import tqdm
from colorama import Fore, init
import sys

init(autoreset=True)

# === Constants ===
LOG_FILE = "log.txt"
KEY_FILE = "key.bin"
PASSWORD_FILE = "password.txt"
ENCRYPTED_DIR = "ENCRYPTED_FILES"
RESTORED_DIR = "RESTORED_FILES"
FILENAME_MAP = "filemap.json"
DESTRUCT_TIMER_MIN = 1
WRONG_ATTEMPTS_ALLOWED = 3

# === Fireworks Spinner ===
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
#if __name__ == "__main__":
#    loading_spinner(4)

# === Utility ===
def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)
    return key

def load_key():
    return open(KEY_FILE, 'rb').read()

def save_password(password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    with open(PASSWORD_FILE, "w") as f:
        f.write(hashed)

def check_password(input_pwd):
    try:
        with open(PASSWORD_FILE, "r") as f:
            stored_hash = f.read().strip()
            return hashlib.sha256(input_pwd.encode()).hexdigest() == stored_hash
    except:
        return False

def random_name(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# === Encryption ===
def encrypt_files(folder, key):
    os.makedirs(ENCRYPTED_DIR, exist_ok=True)
    file_map = {}
    fernet = Fernet(key)
    files_to_encrypt = []

    for root, _, files in os.walk(folder):
        for name in files:
            files_to_encrypt.append(os.path.join(root, name))

    print("\n🔐 Encrypting:")
    spinner_with_fireworks(2)
    for orig_path in tqdm(files_to_encrypt):
        try:
            with open(orig_path, 'rb') as f:
                data = f.read()
            encrypted_data = fernet.encrypt(data)
            randname = random_name()
            with open(os.path.join(ENCRYPTED_DIR, randname), 'wb') as f:
                f.write(encrypted_data)
            file_map[randname] = os.path.basename(orig_path)
        except Exception as e:
            log(f"❌ Failed to encrypt {orig_path}: {e}")

    with open(FILENAME_MAP, 'w') as f:
        json.dump(file_map, f)

    log(f"🔐 Encrypted {len(files_to_encrypt)} files from {folder}")
    print("✅ Encryption complete.")

# === Decryption ===
def decrypt_files(key):
    if not os.path.exists(FILENAME_MAP):
        print("❗ File map not found.")
        return

    with open(FILENAME_MAP, 'r') as f:
        file_map = json.load(f)

    os.makedirs(RESTORED_DIR, exist_ok=True)
    fernet = Fernet(key)
    print("\n🔓 Decrypting:")
    spinner_with_fireworks(2)
    for randname, orig_name in tqdm(file_map.items()):
        encrypted_path = os.path.join(ENCRYPTED_DIR, randname)
        try:
            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = fernet.decrypt(encrypted_data)
            with open(os.path.join(RESTORED_DIR, orig_name), 'wb') as f:
                f.write(decrypted_data)
        except Exception as e:
            log(f"❌ Failed to decrypt {randname}: {e}")

    log(f"✅ Restored {len(file_map)} files.")
    print("✅ All files restored.")

# === Self-destruct ===
def self_destruct():
    for path in [ENCRYPTED_DIR, RESTORED_DIR, FILENAME_MAP, PASSWORD_FILE, KEY_FILE]:
        try:
            if os.path.isdir(path):
                shutil.rmtree(path)
            elif os.path.exists(path):
                os.remove(path)
        except:
            pass
    log("💥 Self-destruct triggered.")
    print("\n💣 Too many wrong attempts or timeout. Self-destructing...")
    print("🧨 All data and files permanently deleted.")

# === Main Logic ===
def main():
    spinner_with_fireworks(4)
    reveal_name_effect(name)

    if not os.path.exists(KEY_FILE):
        print("🛡️ First time setup.")
        password = getpass("🔐 Set a new password: ")
        confirm = getpass("🔐 Confirm password: ")
        if password != confirm:
            print("❌ Passwords do not match. Exiting.")
            return
        key = generate_key()
        save_password(password)
        folder = input("📂 Enter full path of folder to secure: ").strip()
        if not os.path.isdir(folder):
            print("❌ Invalid folder path.")
            return
        encrypt_files(folder, key)
        print("✅ Setup complete.")
        return

    print(f"⏳ You have {DESTRUCT_TIMER_MIN} minutes to enter password...")
    timeout = DESTRUCT_TIMER_MIN * 60
    start = time.time()
    password = None
    while (time.time() - start) < timeout:
        try:
            password = getpass("🔓 Enter password: ")
            break
        except:
            pass
        time.sleep(1)
    else:
        print("\n⏰ Time expired.")
        self_destruct()
        return

    for attempt in range(WRONG_ATTEMPTS_ALLOWED):
        if check_password(password):
            key = load_key()
            decrypt_files(key)
            return
        else:
            print(f"❌ Wrong password ({attempt + 1}/{WRONG_ATTEMPTS_ALLOWED})")
            if attempt < WRONG_ATTEMPTS_ALLOWED - 1:
                password = getpass("🔓 Enter password: ")

    self_destruct()

if __name__ == "__main__":
    main()
