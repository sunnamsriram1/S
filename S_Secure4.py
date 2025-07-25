~/S $ cat S_Secure4.py
#!/usr/bin/env python3
import os
import time
import base64
import random
import string
import shutil
import json
from getpass import getpass
from datetime import datetime
from cryptography.fernet import Fernet

# === Constants ===
LOG_FILE = "log.txt"
KEY_FILE = "key.bin"
PASSWORD_FILE = "password.txt"
ENCRYPTED_DIR = "ENCRYPTED_FILES"
RESTORED_DIR = "RESTORED_FILES"
FILENAME_MAP = "filemap.json"
DESTRUCT_TIMER_MIN = 1
WRONG_ATTEMPTS_ALLOWED = 3

# === Utility ===
def log(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")

def show_timer(seconds):
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        timer = f"{mins:02d}:{secs:02d}"
        print(f"⏳ Time left to enter password: {timer}", end="\r")
        time.sleep(1)
        seconds -= 1
    print()

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, 'wb') as f:
        f.write(key)
    return key

def load_key():
    return open(KEY_FILE, 'rb').read()

def save_password(password):
    with open(PASSWORD_FILE, "w") as f:
        f.write(base64.b64encode(password.encode()).decode())

def check_password(input_pwd):
    try:
        with open(PASSWORD_FILE, "r") as f:
            stored = base64.b64decode(f.read().encode()).decode()
            return input_pwd == stored
    except:
        return False

def random_name(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# === Encryption ===
def encrypt_files(folder, key):
    os.makedirs(ENCRYPTED_DIR, exist_ok=True)
    file_map = {}
    fernet = Fernet(key)
    count = 0

    for root, _, files in os.walk(folder):
        for name in files:
            orig_path = os.path.join(root, name)
            try:
                with open(orig_path, 'rb') as f:
                    data = f.read()
                encrypted_data = fernet.encrypt(data)
                randname = random_name()
                with open(os.path.join(ENCRYPTED_DIR, randname), 'wb') as f:
                    f.write(encrypted_data)
                file_map[randname] = name
                count += 1
            except Exception as e:
                log(f"❌ Failed to encrypt {name}: {e}")

    with open(FILENAME_MAP, 'w') as f:
        json.dump(file_map, f)

    log(f"🔐 Encrypted {count} files from {folder}")
    print(f"🔐 Encrypted {count} files.")

# === Decryption ===
def decrypt_files(key):
    if not os.path.exists(FILENAME_MAP):
        print("❗ File map not found.")
        return
    with open(FILENAME_MAP, 'r') as f:
        file_map = json.load(f)

    os.makedirs(RESTORED_DIR, exist_ok=True)
    fernet = Fernet(key)
    count = 0

    for randname, orig_name in file_map.items():
        encrypted_path = os.path.join(ENCRYPTED_DIR, randname)
        try:
            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = fernet.decrypt(encrypted_data)
            with open(os.path.join(RESTORED_DIR, orig_name), 'wb') as f:
                f.write(decrypted_data)
            count += 1
        except Exception as e:
            log(f"❌ Failed to decrypt {randname}: {e}")

    log(f"✅ Restored {count} files.")
    print(f"✅ All files restored.")

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
    print("B💥💥M Too many wrong attempts. Self-destructing...")
    print("🧨 All data and files permanently deleted.")

# === Main Logic ===
def main():
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

    # Self-destruct countdown
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

    # Validate password
    for attempt in range(WRONG_ATTEMPTS_ALLOWED):
        if check_password(password):
            key = load_key()
            print("\n🔓 Decrypting files...")
            decrypt_files(key)
            return
        else:
            print(f"❌ Wrong password ({attempt + 1}/{WRONG_ATTEMPTS_ALLOWED})")
            if attempt < WRONG_ATTEMPTS_ALLOWED - 1:
                password = getpass("🔓 Enter password: ")

    self_destruct()

if __name__ == "__main__":
    main()
