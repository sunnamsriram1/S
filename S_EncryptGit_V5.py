#!/usr/bin/env python3
import os
import base64
import hashlib
import random
import string
import shutil
from getpass import getpass
from datetime import datetime
from cryptography.fernet import Fernet
from tqdm import tqdm

# 📁 Constants
ENCRYPTED_DIR = "ENCRYPTED_FILES"
GITHUB_REPO = "https://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@github.com/sunnamsriram1/Locked-Backup.git"
USER_NAME = "Sriram"
USER_EMAIL = "sunnamsriram1@gmail.com"
PASSWORD_HASH_FILE = "ransom_password.txt"

# 🔐 Generate Fernet key from password
def generate_key(password):
    return Fernet(base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest()))

# 🔐 Encrypt files
def encrypt_folder(folder_path, password):
    key = generate_key(password)
    if not os.path.exists(ENCRYPTED_DIR):
        os.makedirs(ENCRYPTED_DIR)

    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    print(f"\n🔐 Encrypting {len(files)} files from '{folder_path}'...\n")

    for file in tqdm(files):
        filepath = os.path.join(folder_path, file)
        with open(filepath, 'rb') as f:
            data = f.read()
        encrypted_data = key.encrypt(data)

        enc_name = ''.join(random.choices(string.ascii_letters + string.digits + "-_", k=16)) + ".locked"
        with open(os.path.join(ENCRYPTED_DIR, enc_name), 'wb') as f:
            f.write(encrypted_data)

    # Save password hash
    with open(PASSWORD_HASH_FILE, 'w') as f:
        f.write(hashlib.sha256(password.encode()).hexdigest())

    print(f"\n🔑 Password hash saved to {PASSWORD_HASH_FILE}")

# ☁️ Upload to GitHub
def upload_to_github():
    print("\n🚀 Uploading encrypted files to GitHub...")

    os.chdir(ENCRYPTED_DIR)
    os.system("git init")
    os.system("git checkout -b main")
    os.system(f'git config user.name "{USER_NAME}"')
    os.system(f'git config user.email "{USER_EMAIL}"')
    os.system("git add .")
    os.system('git commit -m "Encrypted backup"')
    os.system(f"git remote add origin {GITHUB_REPO}")
    os.system("git push -u origin main --force")

    print("✅ Files pushed to GitHub: https://github.com/sunnamsriram1/Locked-Backup.git\n")

# 🔓 Decrypt files
def decrypt_files(password):
    if not os.path.exists(PASSWORD_HASH_FILE):
        print("❌ Password file not found.")
        return False
    with open(PASSWORD_HASH_FILE, 'r') as f:
        stored_hash = f.read().strip()

    if hashlib.sha256(password.encode()).hexdigest() != stored_hash:
        print("❌ Wrong password!")
        return False

    key = generate_key(password)
    if not os.path.exists(ENCRYPTED_DIR):
        print("❌ No encrypted folder found!")
        return False

    print("\n🔓 Decrypting files...\n")
    for filename in os.listdir(ENCRYPTED_DIR):
        path = os.path.join(ENCRYPTED_DIR, filename)
        with open(path, 'rb') as f:
            encrypted_data = f.read()
        try:
            data = key.decrypt(encrypted_data)
        except Exception:
            print(f"❌ Decryption failed for {filename}")
            continue
        original_name = "DECRYPTED_" + filename.replace(".locked", ".txt")
        with open(original_name, 'wb') as f:
            f.write(data)
    print("\n✅ Decryption completed!\n")
    return True

# 🔁 Main
def main():
    if not os.path.exists(PASSWORD_HASH_FILE):
        folder = input("📁 Enter folder path to encrypt: ").strip()
        if not os.path.exists(folder):
            print("❌ Folder not found.")
            return
        pwd = getpass("🔑 Enter encryption password: ")
        encrypt_folder(folder, pwd)
        upload_to_github()
    else:
        pwd = getpass("🔑 Enter password to decrypt: ")
        if decrypt_files(pwd):
            print("✅ Done.")
        else:
            print("❌ Decryption failed.")

if __name__ == "__main__":
    main()
