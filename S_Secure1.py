import os
import sys
import time
import shutil
import getpass
import zipfile
import base64
import hashlib
import random
import string
import json
from cryptography.fernet import Fernet

BASE_DIR = os.path.expanduser("~/APP_SECURE")
FILES_DIR = os.path.join(BASE_DIR, "FILES_TO_SECURE")
ENCRYPTED_FILE = os.path.join(BASE_DIR, "vault.enc")
PASSWORD_HASH_FILE = os.path.join(BASE_DIR, ".pwhash")
KEY_FILE = os.path.join(BASE_DIR, ".vault.key")
LOG_FILE = os.path.join(BASE_DIR, "activity.log")

ALLOWED_EXTENSIONS = [".txt", ".pdf", ".csv", ".mp4", ".png", ".jpg", ".jpeg",
                      ".json", ".html", ".docx", ".log", ".py", ".sh", ".apk"]

# ---------------- LOGGING ------------------
def log_event(event):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{time.ctime()}] {event}\n")

# ---------------- PASSWORD ------------------
def sha256_hex(text):
    return hashlib.sha256(text.encode()).hexdigest()

def password_setup():
    password = getpass.getpass("🔑 Set your password: ")
    with open(PASSWORD_HASH_FILE, 'w') as f:
        f.write(sha256_hex(password))
    log_event("Password set")

def verify_password():
    if not os.path.exists(PASSWORD_HASH_FILE):
        print("⚠️ No password found. Please run first time setup.")
        sys.exit(1)

    with open(PASSWORD_HASH_FILE) as f:
        saved_hash = f.read().strip()

    for attempt in range(3):
        password = getpass.getpass("🔐 Enter password: ")
        if sha256_hex(password) == saved_hash:
            log_event("Password accepted")
            return password
        else:
            print(f"❌ Wrong password. Attempts left: {2 - attempt}")
            log_event("Wrong password attempt")

    print("\n💣 Too many failed attempts. Self-destruction initiated...")
    log_event("Self-destruct initiated")
    time.sleep(5)
    destroy_all()
    sys.exit()

# ---------------- ENCRYPTION ------------------
def generate_key(password):
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def encrypt_file_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data)

def decrypt_file_data(data, key):
    fernet = Fernet(key)
    return fernet.decrypt(data)

# ------------- FILE COLLECTION -----------------
def collect_files():
    collected = []
    for root, _, files in os.walk(FILES_DIR):
        for file in files:
            ext = os.path.splitext(file)[-1]
            if ext in ALLOWED_EXTENSIONS:
                full_path = os.path.join(root, file)
                collected.append(full_path)
    return collected

# ------------ ZIPPING ------------------------
def create_hidden_zip(file_list, zip_path):
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for filepath in file_list:
            rand_name = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            zipf.write(filepath, arcname=rand_name)
    log_event(f"{len(file_list)} files added to hidden zip.")

# ------------- DESTRUCT ---------------------
def destroy_all():
    print("🧨 Deleting all data...")
    for path in [ENCRYPTED_FILE, PASSWORD_HASH_FILE, KEY_FILE, LOG_FILE]:
        try:
            os.remove(path)
            print(f"✅ Deleted: {path}")
        except: pass

    try:
        shutil.rmtree(FILES_DIR)
        print(f"✅ Deleted folder: {FILES_DIR}")
    except: pass

    log_event("All data destroyed")

# ------------ REMOTE UNLOCK --------------------
def remote_unlock(password_path):
    if os.path.exists(password_path):
        with open(password_path) as f:
            remote_pwd = f.read().strip()
        if sha256_hex(remote_pwd) == open(PASSWORD_HASH_FILE).read().strip():
            print("🔓 Remote unlock successful!")
            return remote_pwd
    return None

# ------------- MAIN ---------------------------
def first_time_setup():
    os.makedirs(BASE_DIR, exist_ok=True)
    os.makedirs(FILES_DIR, exist_ok=True)

    files = collect_files()
    if not files:
        print("⚠️ No files to secure. Place files in:", FILES_DIR)
        return

    zip_path = os.path.join(BASE_DIR, "vault.zip")
    create_hidden_zip(files, zip_path)

    password_setup()
    password = getpass.getpass("🔐 Confirm password for encryption: ")
    key = generate_key(password)

    with open(zip_path, 'rb') as f:
        encrypted_data = encrypt_file_data(f.read(), key)
    with open(ENCRYPTED_FILE, 'wb') as ef:
        ef.write(encrypted_data)

    os.remove(zip_path)
    shutil.rmtree(FILES_DIR)
    print("🔒 Files secured & encrypted.")
    log_event("Vault created and secured.")

def unlock_vault():
    password = verify_password()
    key = generate_key(password)

    with open(ENCRYPTED_FILE, 'rb') as ef:
        data = decrypt_file_data(ef.read(), key)

    zip_out = os.path.join(BASE_DIR, "vault_out.zip")
    with open(zip_out, 'wb') as f:
        f.write(data)

    extract_dir = os.path.join(BASE_DIR, "RESTORED_FILES")
    os.makedirs(extract_dir, exist_ok=True)

    with zipfile.ZipFile(zip_out, 'r') as zipf:
        zipf.extractall(extract_dir)
    os.remove(zip_out)

    print(f"📁 Files restored to: {extract_dir}")
    log_event("Vault successfully unlocked.")

def main():
    os.makedirs(BASE_DIR, exist_ok=True)

    # Remote unlock first
    remote_pwd_file = os.path.join(BASE_DIR, "remote_key.txt")
    remote_pwd = remote_unlock(remote_pwd_file)
    if remote_pwd:
        key = generate_key(remote_pwd)
        with open(ENCRYPTED_FILE, 'rb') as ef:
            decrypted = decrypt_file_data(ef.read(), key)
        with open("vault_remote.zip", 'wb') as f:
            f.write(decrypted)
        print("📦 Vault unlocked remotely as 'vault_remote.zip'")
        return

    if not os.path.exists(ENCRYPTED_FILE):
        print("🛡️  First time setup...")
        first_time_setup()
    else:
        unlock_vault()

if __name__ == "__main__":
    main()
