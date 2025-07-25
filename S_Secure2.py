#!/usr/bin/env python3
import os
import shutil
import base64
import json
import time
from getpass import getpass
from cryptography.fernet import Fernet
from hashlib import sha256

# === CONFIG ===
SOURCE_DIR = "./FILES_TO_SECURE"
SECURE_DIR = "./APP_SECURE"
ENCRYPTED_DIR = os.path.join(SECURE_DIR, "ENCRYPTED_FILES")
RESTORED_DIR = os.path.join(SECURE_DIR, "RESTORED_FILES")
FILEMAP_PATH = os.path.join(SECURE_DIR, "filemap.json")
KEY_FILE = os.path.join(SECURE_DIR, "key.bin")
PASSWORD_HASH_FILE = os.path.join(SECURE_DIR, "password.hash")
MAX_ATTEMPTS = 3

EXTENSIONS = [".txt", ".pdf", ".jpg", ".png", ".mp4", ".py", ".csv", ".json", ".html", ".docx", ".log"]

# === HELPERS ===
def get_key(password):
    return sha256(password.encode()).digest()

def generate_key(password):
    return base64.urlsafe_b64encode(get_key(password))

def save_password(password):
    with open(PASSWORD_HASH_FILE, "w") as f:
        f.write(sha256(password.encode()).hexdigest())

def verify_password(password):
    if not os.path.exists(PASSWORD_HASH_FILE):
        return False
    with open(PASSWORD_HASH_FILE) as f:
        return f.read() == sha256(password.encode()).hexdigest()

def encrypt_files(password):
    os.makedirs(ENCRYPTED_DIR, exist_ok=True)
    fernet = Fernet(generate_key(password))
    filemap = {}

    for root, _, files in os.walk(SOURCE_DIR):
        for filename in files:
            if not any(filename.endswith(ext) for ext in EXTENSIONS):
                continue

            full_path = os.path.join(root, filename)
            with open(full_path, "rb") as f:
                data = f.read()

            encrypted_data = fernet.encrypt(data)
            masked_name = base64.urlsafe_b64encode(os.urandom(16)).decode("utf-8")[:16]
            enc_path = os.path.join(ENCRYPTED_DIR, masked_name)

            with open(enc_path, "wb") as f:
                f.write(encrypted_data)

            filemap[masked_name] = filename

    with open(FILEMAP_PATH, "w") as f:
        json.dump(filemap, f)

    print(f"🔐 Encrypted {len(filemap)} files.")

def decrypt_files(password):
    if not os.path.exists(FILEMAP_PATH):
        print("❌ File map missing. Cannot decrypt.")
        return

    os.makedirs(RESTORED_DIR, exist_ok=True)
    fernet = Fernet(generate_key(password))

    with open(FILEMAP_PATH) as f:
        filemap = json.load(f)

    for masked_name, original_name in filemap.items():
        enc_path = os.path.join(ENCRYPTED_DIR, masked_name)
        out_path = os.path.join(RESTORED_DIR, original_name)

        try:
            with open(enc_path, "rb") as f:
                encrypted_data = f.read()

            decrypted_data = fernet.decrypt(encrypted_data)

            with open(out_path, "wb") as f:
                f.write(decrypted_data)

            print(f"✅ Restored: {original_name}")
        except Exception as e:
            print(f"❌ Failed to restore {original_name}: {e}")

# === SELF-DESTRUCT ===
def self_destruct():
    print("\n💣 Too many wrong attempts! Starting self-destruction...")
    time.sleep(1)

    for dirpath in [SECURE_DIR, SOURCE_DIR]:
        if os.path.exists(dirpath):
            print(f"🧹 Deleting: {dirpath}")
            shutil.rmtree(dirpath)
    print("✅ All secure data destroyed.")
    exit()

# === MAIN LOGIC ===
def main():
    if not os.path.exists(PASSWORD_HASH_FILE):
        print("🛡️ First time setup.")
        password = getpass("🔐 Set a new password: ")
        save_password(password)
        encrypt_files(password)
        return

    attempts = MAX_ATTEMPTS
    while attempts > 0:
        password = getpass("🔐 Enter password: ")
        if verify_password(password):
            print("✅ Password correct. Decrypting files...")
            decrypt_files(password)
            return
        else:
            attempts -= 1
            print(f"❌ Wrong password. Attempts left: {attempts}")

    self_destruct()

if __name__ == "__main__":
    main()
