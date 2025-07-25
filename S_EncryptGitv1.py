#!/usr/bin/env python3
import os
import hashlib
import base64
import shutil
import json
import random
import string
from getpass import getpass
from cryptography.fernet import Fernet
from tqdm import tqdm
from datetime import datetime
from colorama import Fore, init

init(autoreset=True)

ENCRYPTED_FOLDER = "ENCRYPTED_FILES"
PASSWORD_FILE = "ransom_password.txt"
GIT_REPO = "https://github.com/sunnamsriram1/Locked-Backup.git"
GIT_FOLDER = "S"  # Local git folder
GIT_BRANCH = "master"  # Use 'main' only if already created in GitHub

# ✅ Key generator from password
def generate_key(password):
    hashed = hashlib.sha256(password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(hashed))

# ✅ Encrypt a single file
def encrypt_file(filepath, key, out_folder):
    with open(filepath, 'rb') as f:
        data = f.read()
    encrypted_data = key.encrypt(data)

    random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + ".locked"
    out_path = os.path.join(out_folder, random_name)

    with open(out_path, 'wb') as f:
        f.write(encrypted_data)

# ✅ Save hashed password
def save_password_hash(password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    with open(PASSWORD_FILE, 'w') as f:
        f.write(hashed)
    print(Fore.YELLOW + f"🔑 Password hash saved to {PASSWORD_FILE}")

# ✅ Encrypt folder
def encrypt_folder(folder_path, password):
    if not os.path.exists(folder_path):
        print(Fore.RED + "❌ Folder does not exist.")
        return

    os.makedirs(ENCRYPTED_FOLDER, exist_ok=True)
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    print(Fore.CYAN + f"🔐 Encrypting {len(files)} files from '{folder_path}'...\n")

    key = generate_key(password)

    for f in tqdm(files, desc="Encrypting"):
        encrypt_file(f, key, ENCRYPTED_FOLDER)

    save_password_hash(password)
    print(Fore.GREEN + f"✅ All files encrypted and saved to '{ENCRYPTED_FOLDER}'")

# ✅ Push to GitHub
def push_to_github():
    print(Fore.CYAN + "\n🚀 Pushing encrypted files to GitHub repository...\n")

    os.makedirs(GIT_FOLDER, exist_ok=True)
    os.system(f"rm -rf {GIT_FOLDER}/*")  # Clean previous
    for f in os.listdir(ENCRYPTED_FOLDER):
        shutil.copy(os.path.join(ENCRYPTED_FOLDER, f), GIT_FOLDER)

    os.chdir(GIT_FOLDER)
    os.system("git init")
    os.system('git config user.email "sunnamsriram1@proton.me"')
    os.system('git config user.name "Sriram Backup Bot"')
    os.system("git remote add origin " + GIT_REPO)
    os.system(f"git checkout -b {GIT_BRANCH}")
    os.system("git add .")
    os.system('git commit -m "🔐 Encrypted backup @ ' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '"')
    os.system(f"git push -u origin {GIT_BRANCH} --force")

    print(Fore.GREEN + f"\n✅ Files pushed to GitHub: {GIT_REPO}")

# ✅ Main
if __name__ == "__main__":
    folder_path = input(Fore.CYAN + "📁 Enter folder path to encrypt: ").strip()
    password = getpass(Fore.YELLOW + "🔑 Enter encryption password: ").strip()

    encrypt_folder(folder_path, password)
    push_to_github()
