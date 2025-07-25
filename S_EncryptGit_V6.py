#!/usr/bin/env python3
import os
import time
import base64
import random
import string
import shutil
import hashlib
import json
import requests
from getpass import getpass
from datetime import datetime
from cryptography.fernet import Fernet
from colorama import Fore, init
from tqdm import tqdm

init(autoreset=True)

ENCRYPTED_DIR = "ENCRYPTED_FILES"
RESTORE_DIR = "RESTORED"
LOG_FILE = "log.txt"
PASS_FILE = "ransom_password.txt"
MAX_ATTEMPTS = 3

GITHUB_TOKEN = "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"
GITHUB_REPO = "sunnamsriram1/Locked-Backup"

# 🔐 Generate Fernet Key from password
def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return base64.urlsafe_b64encode(key)

# 🔐 Save hashed password
def save_password_hash(password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    with open(PASS_FILE, "w") as f:
        f.write(hashed)

# 🔒 Verify entered password
def check_password(password):
    if not os.path.exists(PASS_FILE):
        return False
    hashed = hashlib.sha256(password.encode()).hexdigest()
    with open(PASS_FILE, "r") as f:
        return f.read().strip() == hashed

# 📁 Setup folders
def prepare_folders():
    os.makedirs(ENCRYPTED_DIR, exist_ok=True)
    os.makedirs(RESTORE_DIR, exist_ok=True)

# 📝 Logging
def log_event(event):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {event}\n")

# 🔐 Encrypt all files in folder
def encrypt_folder(folder_path, password):
    key = Fernet(generate_key(password))
    prepare_folders()
    for root, dirs, files in os.walk(folder_path):
        for file in tqdm(files, desc="Encrypting"):
            filepath = os.path.join(root, file)
            try:
                with open(filepath, 'rb') as f:
                    data = f.read()
                encrypted_data = key.encrypt(data)

                random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=12)) + ".locked"
                with open(os.path.join(ENCRYPTED_DIR, random_name), 'wb') as f:
                    f.write(encrypted_data)
            except Exception as e:
                print(Fore.RED + f"[✗] Failed: {file}")

# 🔓 Decrypt only valid .locked files
def decrypt_files(password):
    key = Fernet(generate_key(password))
    prepare_folders()
    success = 0
    for filename in os.listdir(ENCRYPTED_DIR):
        path = os.path.join(ENCRYPTED_DIR, filename)
        if not os.path.isfile(path) or not filename.endswith(".locked"):
            continue
        try:
            with open(path, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = key.decrypt(encrypted_data)

            original_name = filename.replace(".locked", "") + ".restored"
            with open(os.path.join(RESTORE_DIR, original_name), 'wb') as f:
                f.write(decrypted_data)
            success += 1
        except Exception:
            print(Fore.RED + f"[✗] Failed to decrypt {filename}")
    print(Fore.GREEN + f"🔓 Decrypted {success} files.")
    return success > 0

# ☁️ Upload encrypted files to GitHub
def upload_to_github():
    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }
    for filename in os.listdir(ENCRYPTED_DIR):
        filepath = os.path.join(ENCRYPTED_DIR, filename)
        if not os.path.isfile(filepath):
            continue
        with open(filepath, 'rb') as f:
            content = base64.b64encode(f.read()).decode()

        url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{filename}"
        data = {
            "message": f"Add {filename}",
            "content": content
        }
        response = requests.put(url, headers=headers, json=data)
        if response.status_code == 201:
            print(Fore.GREEN + f"[✓] Uploaded {filename}")
        else:
            print(Fore.RED + f"[✗] Failed to upload {filename}: {response.status_code}")

# 🧠 Main logic
def main():
    prepare_folders()
    print(Fore.CYAN + "🔐 Secure Folder Encryptor + GitHub Backup (v6)")

    if not os.path.exists(PASS_FILE):
        password = getpass("🔑 Set new password: ")
        save_password_hash(password)
        folder = input("📁 Enter folder path to encrypt: ").strip()
        encrypt_folder(folder, password)
        upload_to_github()
        log_event("Encryption complete.")
    else:
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            pwd = getpass("🔑 Enter password to decrypt: ")
            if check_password(pwd):
                print(Fore.YELLOW + "🔓 Decrypting files...")
                if decrypt_files(pwd):
                    log_event("Decryption success.")
                else:
                    log_event("No valid files decrypted.")
                break
            else:
                attempts += 1
                print(Fore.RED + f"[✗] Wrong password ({attempts}/{MAX_ATTEMPTS})")
                log_event("Wrong password attempt.")
        else:
            print(Fore.RED + "💣 Max attempts reached! Deleting encrypted data...")
            shutil.rmtree(ENCRYPTED_DIR, ignore_errors=True)
            log_event("Self-destruct triggered due to wrong attempts.")

if __name__ == "__main__":
    main()
