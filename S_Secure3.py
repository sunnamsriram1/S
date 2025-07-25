#!/usr/bin/env python3
import os
import sys
import time
import base64
import json
import shutil
import getpass
from cryptography.fernet import Fernet

# 💾 Secure storage paths
CONFIG_FILE = "secure_config.json"
ENCRYPTED_DIR = "ENCRYPTED_FILES"
RESTORED_DIR = "RESTORED_FILES"
LOG_FILE = "secure_log.txt"

# 🛡️ Supported file types
ALLOWED_EXTENSIONS = ['.txt', '.pdf', '.mp4', '.jpg', '.png', '.py', '.json', '.csv', '.docx', '.log', '.html']

def log(msg):
    with open(LOG_FILE, "a") as logf:
        logf.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

def is_allowed_file(file):
    return any(file.endswith(ext) for ext in ALLOWED_EXTENSIONS)

def generate_key(password):
    return base64.urlsafe_b64encode(password.encode().ljust(32, b'0'))

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE) as f:
        return json.load(f)

def encrypt_file(file_path, dest_folder, fernet, original_name_map):
    with open(file_path, 'rb') as f:
        data = f.read()
    encrypted_data = fernet.encrypt(data)
    hidden_name = base64.urlsafe_b64encode(os.urandom(12)).decode().rstrip("=")
    out_path = os.path.join(dest_folder, hidden_name)
    with open(out_path, 'wb') as f:
        f.write(encrypted_data)
    original_name_map[hidden_name] = os.path.basename(file_path)
    return hidden_name

def decrypt_file(encrypted_path, out_dir, fernet, original_name_map):
    file_name = os.path.basename(encrypted_path)
    original_name = original_name_map.get(file_name, f"unknown_{file_name}")
    with open(encrypted_path, 'rb') as f:
        data = f.read()
    try:
        decrypted_data = fernet.decrypt(data)
    except:
        return None
    with open(os.path.join(out_dir, original_name), 'wb') as f:
        f.write(decrypted_data)
    return original_name

def select_files():
    print("\n📂 Enter full paths of files to secure (comma-separated):")
    files = input("Files: ").strip().split(',')
    selected = []
    for f in files:
        f = f.strip()
        if os.path.isfile(f) and is_allowed_file(f):
            selected.append(f)
        else:
            print(f"⚠️ Skipped: {f}")
    return selected

def setup():
    print("🛡️ First time setup.")
    password = getpass.getpass("🔐 Set a new password: ")
    key = generate_key(password)
    fernet = Fernet(key)

    os.makedirs(ENCRYPTED_DIR, exist_ok=True)

    files = select_files()
    if not files:
        print("⚠️ No valid files selected.")
        return

    name_map = {}
    for file in files:
        encrypt_file(file, ENCRYPTED_DIR, fernet, name_map)

    config = {
        "key": base64.b64encode(key).decode(),
        "map": name_map
    }
    save_config(config)
    print(f"✅ Encrypted {len(name_map)} files.")
    log(f"Encrypted {len(name_map)} files during setup.")

def unlock():
    config = load_config()
    if not config:
        print("❌ Not initialized. Run the script to set up.")
        return
    attempts = 3
    while attempts > 0:
        password = getpass.getpass("🔐 Enter password: ")
        key = generate_key(password)
        try:
            fernet = Fernet(key)
            fernet.decrypt(fernet.encrypt(b'test'))  # check key format
            if base64.b64encode(key).decode() == config["key"]:
                print("✅ Access granted.")
                break
            else:
                raise Exception()
        except:
            attempts -= 1
            print(f"❌ Wrong password. Attempts left: {attempts}")
            if attempts == 0:
                print("💣 Too many attempts. Self destructing...")
                shutil.rmtree(ENCRYPTED_DIR, ignore_errors=True)
                os.remove(CONFIG_FILE)
                log("Self destruct triggered.")
                sys.exit()

    os.makedirs(RESTORED_DIR, exist_ok=True)
    count = 0
    for file in os.listdir(ENCRYPTED_DIR):
        path = os.path.join(ENCRYPTED_DIR, file)
        original = decrypt_file(path, RESTORED_DIR, fernet, config["map"])
        if original:
            count += 1
            print(f"🔓 Restored: {original}")
    print(f"✅ Total restored: {count}")
    log(f"Decrypted {count} files.")

def main():
    if not os.path.exists(CONFIG_FILE):
        setup()
    else:
        unlock()

if __name__ == "__main__":
    main()

