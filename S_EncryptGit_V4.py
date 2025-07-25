#!/usr/bin/env python3
import os
import base64
import hashlib
import shutil
import json
import subprocess
from getpass import getpass
from cryptography.fernet import Fernet
from tqdm import tqdm
from datetime import datetime
from colorama import Fore, init

init(autoreset=True)

ENCRYPTED_FOLDER = "ENCRYPTED_FILES"
PASSWORD_FILE = "ransom_password.txt"
GIT_REMOTE = "https://github.com/sunnamsriram1/Locked-Backup.git"

# ✅ Key Generator
def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

# ✅ Encrypt files
def encrypt_folder(folder_path, password):
    key = generate_key(password)
    if not os.path.exists(ENCRYPTED_FOLDER):
        os.makedirs(ENCRYPTED_FOLDER)

    files = []
    for root, _, filenames in os.walk(folder_path):
        for f in filenames:
            full_path = os.path.join(root, f)
            if os.path.isfile(full_path):
                files.append(full_path)

    print(f"\n🔐 Encrypting {len(files)} files from '{folder_path}'...\n")
    for file in tqdm(files):
        with open(file, "rb") as f:
            data = f.read()
        enc_data = key.encrypt(data)
        enc_name = base64.urlsafe_b64encode(os.urandom(12)).decode() + ".locked"
        with open(os.path.join(ENCRYPTED_FOLDER, enc_name), "wb") as f:
            f.write(enc_data)

    # ✅ Save password hash
    with open(PASSWORD_FILE, "w") as f:
        f.write(hashlib.sha256(password.encode()).hexdigest())
    print(Fore.YELLOW + "\n🔑 Password hash saved to ransom_password.txt")

# ✅ Decrypt files
def decrypt_files(password):
    key = generate_key(password)
    if not os.path.exists(ENCRYPTED_FOLDER):
        print(Fore.RED + "❌ ENCRYPTED_FILES folder not found!")
        return False

    for filename in os.listdir(ENCRYPTED_FOLDER):
        path = os.path.join(ENCRYPTED_FOLDER, filename)
        if not filename.endswith(".locked"):
            continue
        try:
            with open(path, "rb") as f:
                data = f.read()
            dec_data = key.decrypt(data)
            new_name = filename.replace(".locked", ".restored")
            with open(new_name, "wb") as f:
                f.write(dec_data)
        except:
            print(Fore.RED + f"⚠️ Failed to decrypt: {filename}")
            continue
    return True

# ✅ Upload to GitHub
def upload_to_github():
    if not os.path.exists(ENCRYPTED_FOLDER):
        print(Fore.RED + "❌ Nothing to upload. ENCRYPTED_FILES folder missing.")
        return
    print(Fore.GREEN + "\n🚀 Uploading encrypted files to GitHub...")

    os.chdir(ENCRYPTED_FOLDER)
    subprocess.call(["git", "init"])
    subprocess.call(["git", "checkout", "-b", "main"])
    subprocess.call(["git", "config", "user.email", "you@example.com"])
    subprocess.call(["git", "config", "user.name", "Sriram Encryptor"])
    subprocess.call(["git", "remote", "add", "origin", GIT_REMOTE])
    subprocess.call(["git", "add", "."])
    subprocess.call(["git", "commit", "-m", "Encrypted backup"])
    subprocess.call(["git", "push", "-u", "origin", "main", "--force"])

    print(Fore.CYAN + f"✅ Files pushed to GitHub: {GIT_REMOTE}")
    os.chdir("..")

# ✅ Main Menu
def main():
    if not os.path.exists(ENCRYPTED_FOLDER):
        print(Fore.CYAN + "📁 Enter folder path to encrypt:", end=" ")
        folder_path = input().strip()
        if not os.path.exists(folder_path):
            print(Fore.RED + "❌ Invalid folder path.")
            return
        password = getpass("🔑 Enter encryption password: ")
        encrypt_folder(folder_path, password)
        upload_to_github()
    else:
        # 🔓 Try Decrypting
        attempts = 3
        while attempts > 0:
            pwd = getpass("🔑 Enter password to decrypt: ")
            with open(PASSWORD_FILE, "r") as f:
                saved_hash = f.read().strip()
            if hashlib.sha256(pwd.encode()).hexdigest() == saved_hash:
                print(Fore.GREEN + "\n🔓 Decrypting files...\n")
                if decrypt_files(pwd):
                    print(Fore.GREEN + "\n✅ Decryption complete.")
                break
            else:
                attempts -= 1
                print(Fore.RED + "❌ Wrong password!")
        if attempts == 0:
            print(Fore.RED + "\n💣 Self-destruct logic not yet implemented.")

if __name__ == "__main__":
    main()
