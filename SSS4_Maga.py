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
import zipfile
from getpass import getpass
from datetime import datetime
from cryptography.fernet import Fernet
from tqdm import tqdm
from colorama import Fore, Style, init
import sys
import pyAesCrypt
from mega import Mega  # Ensure mega.py is properly installed

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
BUFFER_SIZE = 64 * 1024

# === Fancy loading ===
def print_name_slow(name, delay=0.1):
    sys.stdout.write(Fore.MAGENTA)
    for char in name:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print(Style.RESET_ALL)

def spinner_with_fireworks(duration=4):
    done = False
    def animate():
        for c in itertools.cycle(['✫', '🌟', '💥', '🎇', '🎆']):
            if done: break
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

def zip_and_encrypt(output_zip, enc_password):
    zip_path = output_zip + ".zip"
    enc_path = zip_path + ".aes"
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for root, _, files in os.walk(ENCRYPTED_DIR):
            for file in files:
                zipf.write(os.path.join(root, file), arcname=file)
    pyAesCrypt.encryptFile(zip_path, enc_path, enc_password, BUFFER_SIZE)
    os.remove(zip_path)
    return enc_path

def upload_to_mega(email, password, filepath):
    print("☁️ Connecting to MEGA...")
    mega = Mega()
    m = mega.login(email, password)
    filename = os.path.basename(filepath)
    print(f"🚀 Uploading {filename}...")
    m.upload(filepath)
    print("✅ Upload successful.")
    log(f"☁️ Uploaded {filename} to MEGA")

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
    print("🪸 All data and files permanently deleted.")

def main():
    spinner_with_fireworks(4)

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

        cloud = input("☁️ Upload to MEGA cloud? (y/n): ").strip().lower()
        if cloud == 'y':
            enc_password = getpass("🔐 Set encryption password for zip: ")
            encrypted_file = zip_and_encrypt("secure_backup", enc_password)
            email = input("📧 Enter your MEGA email: ")
            mega_pass = getpass("🔑 MEGA password: ")
            upload_to_mega(email, mega_pass, encrypted_file)
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
