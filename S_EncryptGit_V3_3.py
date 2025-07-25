#!/usr/bin/env python3
import os
import time
import base64
import hashlib
import random
import string
import json
import shutil
from datetime import datetime
from getpass import getpass
from cryptography.fernet import Fernet
from tqdm import tqdm
from colorama import Fore, init

init(autoreset=True)

# ✅ SETTINGS
GITHUB_USERNAME = "sunnamsriram1"
GITHUB_REPO = "Locked-Backup"
GITHUB_TOKEN = "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"
LOCKED_FOLDER = "locked_files"

# ✅ Create key from password
def generate_key(password):
    return Fernet(base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest()))

# ✅ Encrypt a file
def encrypt_file(file_path, fernet, output_folder):
    with open(file_path, 'rb') as f:
        data = f.read()
    encrypted = fernet.encrypt(data)
    rand_name = ''.join(random.choices(string.ascii_letters + string.digits, k=12)) + ".locked"
    enc_path = os.path.join(output_folder, rand_name)
    with open(enc_path, 'wb') as f:
        f.write(encrypted)
    return rand_name

# ✅ Walk & encrypt folder
def encrypt_folder(target_folder, fernet):
    if not os.path.exists(LOCKED_FOLDER):
        os.makedirs(LOCKED_FOLDER)
    encrypted_files = []
    for root, _, files in os.walk(target_folder):
        for file in files:
            full_path = os.path.join(root, file)
            enc_name = encrypt_file(full_path, fernet, LOCKED_FOLDER)
            encrypted_files.append(enc_name)
    return encrypted_files

# ✅ Git Upload Function
def push_to_github():
    if not os.path.exists(".git"):
        os.system("git init")
        os.system(f"git remote add origin https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO}.git")
    os.system("git add locked_files/*.locked")
    os.system('git config user.email "you@example.com"')
    os.system('git config user.name "AutoLocker"')
    os.system(f'git commit -m "🔐 Encrypted files backup"')
    push_cmd = f'git push https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{GITHUB_REPO}.git main'
    os.system(push_cmd)

# ✅ Main Flow
def main():
    print(Fore.CYAN + "🔐 S Secure Locker v6")
    folder = input(Fore.YELLOW + "📁 Target folder to encrypt: ").strip()
    if not os.path.isdir(folder):
        print(Fore.RED + "❌ Invalid folder!")
        return
    password = getpass("🔑 Set encryption password: ")
    fernet = generate_key(password)
    
    print(Fore.GREEN + "\n🔄 Encrypting files...")
    files = encrypt_folder(folder, fernet)
    
    print(Fore.BLUE + f"\n✅ Encrypted {len(files)} files. Uploading to GitHub...\n")
    push_to_github()
    
    print(Fore.GREEN + "✅ Backup complete: https://github.com/{}/{}\n".format(GITHUB_USERNAME, GITHUB_REPO))

if __name__ == "__main__":
    main()
