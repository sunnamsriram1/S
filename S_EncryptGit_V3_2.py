#!/usr/bin/env python3
import os, base64, hashlib, shutil, random, string
from cryptography.fernet import Fernet
from getpass import getpass
from datetime import datetime
from tqdm import tqdm
import subprocess

# Constants
ENCRYPTED_DIR = "ENCRYPTED_FILES"
GITHUB_REPO = "https://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@github.com/sunnamsriram1/Locked-Backup.git"
USER_NAME = "Sriram"
USER_EMAIL = "sunnamsriram1@gmail.com"
PASSWORD_HASH_FILE = "ransom_password.txt"
MAX_ATTEMPTS = 3

# Banner
def banner():
    print("\n🔐 S_EncryptGit_V6 – Secure Folder Encryptor + GitHub Backup")
    print("🔒 Author: Sriram | 🌐 Uploads to: Locked-Backup GitHub\n")

# Generate key from password
def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

# Encrypt single file
def encrypt_file(filepath, fernet, output_folder):
    with open(filepath, 'rb') as f:
        data = f.read()
    encrypted = fernet.encrypt(data)
    new_name = ''.join(random.choices(string.ascii_letters + string.digits, k=16)) + ".locked"
    with open(os.path.join(output_folder, new_name), 'wb') as f:
        f.write(encrypted)

# Encrypt folder files
def encrypt_folder(folder, password):
    if not os.path.exists(ENCRYPTED_DIR):
        os.makedirs(ENCRYPTED_DIR)

    fernet = generate_key(password)
    all_files = []

    for root, dirs, files in os.walk(folder):
        # Skip .git folders
        if '.git' in root:
            continue
        for file in files:
            all_files.append(os.path.join(root, file))

    print(f"\n🔐 Encrypting {len(all_files)} files from '{folder}'...\n")
    for filepath in tqdm(all_files):
        try:
            encrypt_file(filepath, fernet, ENCRYPTED_DIR)
        except Exception as e:
            print(f"❌ Failed: {filepath} ({e})")

    with open(PASSWORD_HASH_FILE, 'w') as f:
        f.write(hashlib.sha256(password.encode()).hexdigest())
    print(f"\n🔑 Password hash saved to {PASSWORD_HASH_FILE}\n")

# Decrypt files
def decrypt_files(password):
    key = generate_key(password)
    success = 0
    for file in os.listdir(ENCRYPTED_DIR):
        path = os.path.join(ENCRYPTED_DIR, file)
        if os.path.isdir(path) or not file.endswith(".locked"):
            continue
        try:
            with open(path, 'rb') as f:
                data = f.read()
            decrypted = key.decrypt(data)
            with open(path[:-7], 'wb') as f:
                f.write(decrypted)
            os.remove(path)
            success += 1
        except Exception:
            continue
    return success

# GitHub Upload
def upload_to_github():
    try:
        os.chdir(ENCRYPTED_DIR)
        subprocess.run(["git", "init"], check=True)
        subprocess.run(["git", "config", "user.name", USER_NAME], check=True)
        subprocess.run(["git", "config", "user.email", USER_EMAIL], check=True)
        subprocess.run(["git", "checkout", "-b", "main"], check=True)
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Encrypted backup"], check=True)
        subprocess.run(["git", "remote", "add", "origin", GITHUB_REPO], check=True)
        subprocess.run(["git", "push", "-f", "origin", "main"], check=True)
        print(f"\n✅ Files pushed to GitHub: https://github.com/sunnamsriram1/Locked-Backup\n")
    except Exception as e:
        print(f"❌ GitHub upload failed: {e}\n")

# Main function
def main():
    banner()
    if not os.path.exists(ENCRYPTED_DIR) or not os.listdir(ENCRYPTED_DIR):
        folder = input("📁 Enter folder path to encrypt: ").strip()
        password = getpass("🔑 Enter encryption password: ")
        encrypt_folder(folder, password)
        print("🚀 Uploading encrypted files to GitHub...")
        upload_to_github()
    else:
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            pwd = getpass("🔑 Enter password to decrypt: ")
            hash_check = hashlib.sha256(pwd.encode()).hexdigest()
            with open(PASSWORD_HASH_FILE) as f:
                correct_hash = f.read().strip()
            if hash_check == correct_hash:
                print("\n🔓 Decrypting files...\n")
                count = decrypt_files(pwd)
                print(f"✅ Decrypted {count} files.\n")
                return
            else:
                attempts += 1
                print(f"❌ Wrong password ({attempts}/{MAX_ATTEMPTS})\n")

        print("💥 Maximum attempts reached! Self-destructing encrypted files...\n")
        shutil.rmtree(ENCRYPTED_DIR)

if __name__ == "__main__":
    main()
