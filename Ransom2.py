import os
import base64
from cryptography.fernet import Fernet, InvalidToken
from getpass import getpass
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# Banner
print(Fore.CYAN + "\n🔓 S Decryptor — Safe File Restore Tool")
print(Fore.YELLOW + """------------------------------------------
🔐 Note: Only original password used for encryption will work.
💥 Wrong password or corrupted files can't be restored.
------------------------------------------""")

# Password
password = getpass(Fore.BLUE + "\n🔑 Enter decryption password: ")
key_file = "key.bin"

# Load or generate key
if os.path.exists(key_file):
    with open(key_file, "rb") as f:
        key = f.read()
else:
    key = base64.urlsafe_b64encode(password.encode().ljust(32, b"0"))
    with open(key_file, "wb") as f:
        f.write(key)

dec = Fernet(key)

# Folder to decrypt
folder = input(Fore.GREEN + "\n📁 Enter folder to restore (default=current): ")
if folder.strip() == "":
    folder = os.getcwd()

success = 0
failures = 0
fail_log = "fail_log.txt"

with open("log.txt", "a") as log:
    log.write(f"\n[📥 Start Decryption: {datetime.now()}] Folder: {folder}\n")

    for root, dirs, files in os.walk(folder):
        for filename in files:
            if filename.endswith(".locked"):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, "rb") as f:
                        encrypted = f.read()
                    decrypted = dec.decrypt(encrypted)
                    original_name = filename[:-7]  # remove .locked
                    restored_path = os.path.join(root, original_name)
                    with open(restored_path, "wb") as f:
                        f.write(decrypted)
                    os.remove(filepath)
                    print(Fore.GREEN + f"[+] Restored: {restored_path}")
                    success += 1
                except InvalidToken:
                    print(Fore.RED + f"[!] Failed to decrypt {filename}: Invalid password or corrupted file")
                    with open(fail_log, "a") as flog:
                        flog.write(f"[InvalidToken] {filepath}\n")
                    failures += 1
                except Exception as e:
                    print(Fore.RED + f"[!] Error in {filename}: {str(e)}")
                    with open(fail_log, "a") as flog:
                        flog.write(f"[Exception] {filepath} => {str(e)}\n")
                    failures += 1

    log.write(f"[✔️ Decryption Done: {datetime.now()}] Restored: {success}, Failed: {failures}\n")

print(Fore.CYAN + f"\n✅ Done. Restored: {success}, Failed: {failures}")
if failures:
    print(Fore.YELLOW + f"⚠️ See fail_log.txt for details.")

