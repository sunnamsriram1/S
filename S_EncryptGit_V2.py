#!/usr/bin/env python3
import os
import base64
import hashlib
import shutil
import random
import string
import subprocess
from datetime import datetime
from getpass import getpass
from cryptography.fernet import Fernet
from tqdm import tqdm
from colorama import Fore, init

init(autoreset=True)

# 🔐 Hash Key Generator
def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

# 🔁 Random filename generator
def random_name(length=16):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# 🔒 Encrypt single file
def encrypt_file(file_path, fernet, output_dir):
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        encrypted = fernet.encrypt(data)
        rand_name = random_name() + ".locked"
        with open(os.path.join(output_dir, rand_name), 'wb') as ef:
            ef.write(encrypted)
        return rand_name
    except Exception as e:
        print(Fore.RED + f"[!] Failed: {file_path} — {e}")
        return None

# 🧠 GitHub Upload
def upload_to_github(folder, token, username, repo):
    os.chdir(folder)
    subprocess.run(["git", "init"])
    subprocess.run(["git", "checkout", "-b", "main"])
    subprocess.run(["git", "remote", "add", "origin", f"https://{token}@github.com/{username}/{repo}.git"])
    subprocess.run(["git", "add", "."])
    commit_msg = f"🔐 Encrypted backup @ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    subprocess.run(["git", "commit", "-m", commit_msg])
    subprocess.run(["git", "push", "--force", "origin", "main"])

# 🎯 Main Logic
def main():
    folder = input(Fore.CYAN + "📁 Enter folder path to encrypt: ").strip()
    if not os.path.isdir(folder):
        print(Fore.RED + "[X] Invalid folder path!")
        return

    password = getpass(Fore.YELLOW + "🔑 Enter encryption password: ").strip()
    fernet = generate_key(password)

    out_dir = "ENCRYPTED_FILES"
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    os.makedirs(out_dir)

    # 🔍 Get all files recursively
    all_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            all_files.append(os.path.join(root, file))

    print(Fore.GREEN + f"\n🔐 Encrypting {len(all_files)} files from '{folder}'...\n")
    for f in tqdm(all_files, desc="Encrypting"):
        encrypt_file(f, fernet, out_dir)

    # 💾 Save hash for reference
    with open("ransom_password.txt", "w") as pf:
        pf.write(hashlib.sha256(password.encode()).hexdigest())
    print(Fore.YELLOW + "🔑 Password hash saved to ransom_password.txt")

    # 🔼 Upload to GitHub
    print(Fore.CYAN + "\n🚀 Uploading encrypted files to GitHub...")

    GITHUB_USERNAME = "sunnamsriram1"
    GITHUB_TOKEN = "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"
    GITHUB_REPO = "Locked-Backup"

    upload_to_github(out_dir, GITHUB_TOKEN, GITHUB_USERNAME, GITHUB_REPO)
    print(Fore.GREEN + f"\n✅ Files pushed to GitHub: https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO}")

if __name__ == "__main__":
    main()
