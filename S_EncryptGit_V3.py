#!/usr/bin/env python3
import os
import base64
import hashlib
from cryptography.fernet import Fernet
from getpass import getpass
from tqdm import tqdm
from colorama import Fore, init
from datetime import datetime
import shutil
import subprocess

init(autoreset=True)

# 📁 Constants
ENCRYPTED_DIR = "ENCRYPTED_FILES"
GITHUB_REPO = "https://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@github.com/sunnamsriram1/Locked-Backup.git"
USER_NAME = "Sriram"
USER_EMAIL = "sunnamsriram1@gmail.com"
PASSWORD_HASH_FILE = "ransom_password.txt"

# 🔐 Key from password
def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

# 🔐 Encrypt a file
def encrypt_file(filepath, fernet, output_dir):
    with open(filepath, 'rb') as file:
        data = file.read()
    encrypted = fernet.encrypt(data)

    filename = os.path.basename(filepath)
    enc_filename = base64.urlsafe_b64encode(os.urandom(9)).decode() + ".locked"
    with open(os.path.join(output_dir, enc_filename), 'wb') as f:
        f.write(encrypted)

# 🚀 Push to GitHub
def push_to_github():
    os.chdir(ENCRYPTED_DIR)
    subprocess.run(["git", "init"])
    subprocess.run(["git", "config", "user.name", USER_NAME])
    subprocess.run(["git", "config", "user.email", USER_EMAIL])
    subprocess.run(["git", "checkout", "-b", "main"])
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Encrypted backup"])
    subprocess.run(["git", "remote", "add", "origin", GITHUB_REPO])
    subprocess.run(["git", "push", "-u", "origin", "main", "--force"])
    print(Fore.GREEN + f"✅ Files pushed to GitHub: https://github.com/sunnamsriram1/Locked-Backup\n")

# 📦 Main
def main():
    folder = input(Fore.CYAN + "📁 Enter folder path to encrypt: ").strip()
    password = getpass(Fore.YELLOW + "🔑 Enter encryption password: ")

    fernet = generate_key(password)
    os.makedirs(ENCRYPTED_DIR, exist_ok=True)

    file_list = []
    for root, _, files in os.walk(folder):
        for file in files:
            file_list.append(os.path.join(root, file))

    print(Fore.MAGENTA + f"\n🔐 Encrypting {len(file_list)} files from '{folder}'...\n")
    for filepath in tqdm(file_list, desc="Encrypting", ncols=90):
        encrypt_file(filepath, fernet, ENCRYPTED_DIR)

    # Save password hash
    with open(PASSWORD_HASH_FILE, 'w') as f:
        f.write(hashlib.sha256(password.encode()).hexdigest())
    print(Fore.YELLOW + "🔑 Password hash saved to ransom_password.txt")

    print(Fore.CYAN + "\n🚀 Uploading encrypted files to GitHub...")
    push_to_github()

if __name__ == "__main__":
    main()
