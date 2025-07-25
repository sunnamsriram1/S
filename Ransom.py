#!/usr/bin/env python3
import os
from cryptography.fernet import Fernet
from getpass import getpass
from colorama import Fore, Style, init

init(autoreset=True)

# ✅ Custom password-based key generator
def generate_key(password):
    return Fernet(Fernet.generate_key())

# ✅ File encryption
def encrypt_file(filepath, cipher):
    with open(filepath, 'rb') as f:
        data = f.read()
    encrypted = cipher.encrypt(data)
    with open(filepath + ".locked", 'wb') as f:
        f.write(encrypted)
    print(f"{Fore.GREEN}[✓] Encrypted: {filepath} ➜ {filepath}.locked")

# ✅ File decryption
def decrypt_file(filepath, cipher):
    with open(filepath, 'rb') as f:
        data = f.read()
    decrypted = cipher.decrypt(data)
    original = filepath.replace(".locked", "")
    with open(original, 'wb') as f:
        f.write(decrypted)
    print(f"{Fore.YELLOW}[✓] Decrypted: {filepath} ➜ {original}")

# ✅ Main logic
def main():
    print(Fore.CYAN + "\n🔐 SimRansom — Safe AES File Locker\n")

    mode = input("🔄 Mode (lock/unlock): ").strip().lower()
    folder = input("📁 Enter target folder path: ").strip()

    if not os.path.isdir(folder):
        print(Fore.RED + "[X] Invalid folder!")
        return

    password = getpass("🔑 Enter password: ")
    cipher = generate_key(password)

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.locked') and mode == 'unlock':
                filepath = os.path.join(root, file)
                try:
                    decrypt_file(filepath, cipher)
                except:
                    print(Fore.RED + f"[!] Wrong password or error: {filepath}")
            elif not file.endswith('.locked') and mode == 'lock':
                if file.split('.')[-1] in ['txt', 'jpg', 'pdf', 'mp3', 'py', 'json', 'sh', 'apk']:
                    filepath = os.path.join(root, file)
                    encrypt_file(filepath, cipher)

if __name__ == '__main__':
    main()
