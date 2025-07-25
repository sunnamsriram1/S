#!/usr/bin/env python3
import os
import base64
import hashlib
import json
import shutil
from getpass import getpass
from cryptography.fernet import Fernet
from datetime import datetime
from tqdm import tqdm
from colorama import Fore, init

init(autoreset=True)

# === CONFIG ===
ENCRYPTED_DIR = "ENCRYPTED_FILES"
PASSWORD_FILE = "ransom_password.txt"
GIT_REPO = "https://github.com/sunnamsriram1/Locked-Backup.git"

# === Generate Key from Password ===
def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

# === Save hashed password ===
def save_hashed_password(password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    with open(PASSWORD_FILE, "w") as f:
        f.write(hashed)
    print(f"{Fore.YELLOW}🔑 Password hash saved to {PASSWORD_FILE}")

# === Encrypt a single file ===
def encrypt_file(filepath, fernet, output_dir):
    with open(filepath, 'rb') as file:
        data = file.read()
    encrypted = fernet.encrypt(data)

    random_name = base64.urlsafe_b64encode(os.urandom(12)).decode() + ".locked"
    out_path = os.path.join(output_dir, random_name)
    with open(out_path, 'wb') as f:
        f.write(encrypted)

# === Encrypt entire folder ===
def encrypt_folder(folder, password):
    fernet = generate_key(password)

    if os.path.exists(ENCRYPTED_DIR):
        shutil.rmtree(ENCRYPTED_DIR)
    os.makedirs(ENCRYPTED_DIR)

    file_count = sum(len(files) for _, _, files in os.walk(folder))
    print(f"{Fore.GREEN}🔐 Encrypting {file_count} files from '{folder}'...\n")

    for root, _, files in os.walk(folder):
        for file in tqdm(files, desc="Encrypting"):
            full_path = os.path.join(root, file)
            encrypt_file(full_path, fernet, ENCRYPTED_DIR)

    save_hashed_password(password)
    print(f"{Fore.GREEN}✅ All files encrypted and saved to '{ENCRYPTED_DIR}'")

# === Create .gitignore ===
def create_gitignore():
    with open(".gitignore", "w") as f:
        f.write(f"{PASSWORD_FILE}\nkey.bin\nRESTORED_FILES/\n*.json\n")

# === GitHub Push ===
def push_to_github():
    print(f"\n{Fore.CYAN}🚀 Pushing encrypted files to GitHub repository...\n")
    create_gitignore()
    os.system("git init")
    os.system("git add .")
    os.system('git commit -m "🔐 Encrypted backup commit"')
    os.system("git branch -M main")
    os.system(f"git remote add origin {GIT_REPO}")
    os.system("git push -u origin main")
    print(f"{Fore.GREEN}✅ Files pushed to GitHub: {GIT_REPO}")

# === MAIN ===
def main():
    folder = input(f"{Fore.BLUE}📁 Enter folder path to encrypt: ").strip()
    if not os.path.exists(folder):
        print(f"{Fore.RED}❌ Folder not found.")
        return
    password = getpass(f"{Fore.MAGENTA}🔑 Enter encryption password: ").strip()
    encrypt_folder(folder, password)
    push_to_github()

if __name__ == "__main__":
    main()
