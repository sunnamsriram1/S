#!/usr/bin/env python3
import os
import base64
import hashlib
from cryptography.fernet import Fernet
from getpass import getpass
from colorama import Fore, init

init(autoreset=True)

# ✅ Real password-based key generator
def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    return Fernet(base64.urlsafe_b64encode(key))

# ✅ Encrypt file
def encrypt_file(filepath, cipher):
    with open(filepath, 'rb') as f:
        data = f.read()
    encrypted = cipher.encrypt(data)
    with open(filepath + ".locked", 'wb') as f:
        f.write(encrypted)
    os.remove(filepath)
    print(f"{Fore.GREEN}[✓] Encrypted: {filepath}")

# ✅ Decrypt file
def decrypt_file(filepath, cipher):
    with open(filepath, 'rb') as f:
        data = f.read()
    try:
        decrypted = cipher.decrypt(data)
        original = filepath.replace(".locked", "")
        with open(original, 'wb') as f:
            f.write(decrypted)
        os.remove(filepath)
        print(f"{Fore.YELLOW}[✓] Decrypted: {filepath}")
    except Exception as e:
        print(f"{Fore.RED}[!] Failed to decrypt {filepath}: {str(e)}")

# ✅ Main
def main():
    print(Fore.CYAN + "\n🔐 SimRansom — Termux Safe File Locker\n")

    mode = input("🔄 Mode (lock/unlock): ").strip().lower()
    folder = input("📁 Enter target folder path: ").strip()

    if not os.path.isdir(folder):
        print(Fore.RED + "[X] Invalid folder path!")
        return

    password = getpass("🔑 Enter password: ")
    cipher = generate_key(password)

    count = 0
    for root, dirs, files in os.walk(folder):
        for file in files:
            filepath = os.path.join(root, file)
            if mode == "lock":
                if not file.endswith(".locked") and file.split('.')[-1] in ['txt', 'jpg', 'pdf', 'mp3', 'py', 'json', 'sh', 'apk']:
                    encrypt_file(filepath, cipher)
                    count += 1
            elif mode == "unlock":
                if file.endswith(".locked"):
                    decrypt_file(filepath, cipher)
                    count += 1
    print(Fore.CYAN + f"\n✅ Total files processed: {count}")

if __name__ == '__main__':
    main()
