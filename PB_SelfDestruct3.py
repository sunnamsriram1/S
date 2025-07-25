#!/usr/bin/env python3
import os
import base64
import random
import string
from getpass import getpass
from cryptography.fernet import Fernet
from datetime import datetime
from colorama import init, Fore, Style

# Initialize Colorama
init(autoreset=True)

# Banner
def show_banner():
    time_now = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    print("\n" + "═" * 55)
    print(Fore.CYAN + "★ Coded by     : SUNNAM_SRIRAM_1")
    print(Fore.MAGENTA + f"★ India Time   : {time_now}")
    print("═" * 55 + "\n")

# Key generator
def generate_key(password: str) -> bytes:
    return base64.urlsafe_b64encode(password.ljust(32, '0')[:32].encode())

# OTP generator
def generate_otp(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Encrypt & create script
def encrypt_file(input_file, output_file, password, self_destruct=False, runtime="bash", use_otp=False):
    key = generate_key(password)
    fernet = Fernet(key)

    with open(input_file, 'rb') as f:
        data = f.read()

    encrypted = fernet.encrypt(data).decode()
    destruct_line = f"rm -- \"$0\"" if self_destruct else ""

    header_comment = "# 🔐 Encrypted & coded by Sriram"

    script = f"""#!/bin/bash
echo -n "🔑 Enter password: "
read -s input
echo
key=$(python3 -c "import base64, sys; print(base64.urlsafe_b64encode(sys.argv[1].ljust(32, '0')[:32].encode()).decode())" "$input")
tmp_file=$(mktemp)
if ! python3 -c "from cryptography.fernet import Fernet; import sys; print(Fernet(sys.argv[1].encode()).decrypt(b'''{encrypted}''').decode())" "$key" > $tmp_file 2>/dev/null; then
    echo "❌ Incorrect password or decryption failed!"
    exit 1
fi
echo '{header_comment}' >> $tmp_file
chmod +x $tmp_file
{runtime} $tmp_file
rm $tmp_file
{destruct_line}
"""
    with open(output_file, 'w') as f:
        f.write(script)

    os.chmod(output_file, 0o755)

    with open("PB_encrypt_log.txt", "a") as log:
        log.write(f"[{datetime.now()}] 🔐 {output_file} encrypted from {input_file}\n")

    print(Fore.GREEN + f"✅ {input_file} encrypted successfully → {output_file}")

# Decrypt encrypted .sh
def decrypt_script(encrypted_file, output_file):
    with open(encrypted_file, 'r') as f:
        lines = f.readlines()

    enc_line = ""
    for line in lines:
        if "b'''" in line and "''')" in line:
            enc_line = line.split("b'''")[1].split("'''")[0]
            break

    if not enc_line:
        print(Fore.RED + "❌ Could not find encrypted content in the file.")
        return

    password = getpass(Fore.YELLOW + "🔑 Enter password to decrypt: ")
    key = generate_key(password)

    try:
        fernet = Fernet(key)
        decrypted = fernet.decrypt(enc_line.encode()).decode()
        with open(output_file, 'w') as out:
            out.write(decrypted)
            out.write("\n# 🔐 Encrypted & coded by Sriram\n")
        print(Fore.GREEN + f"✅ Decrypted content saved to: {output_file}")
    except Exception as e:
        print(Fore.RED + f"❌ Decryption failed: {e}")

# --- Main ---
try:
    show_banner()

    print(Fore.CYAN + "🔄 Choose mode:")
    print(Fore.YELLOW + " 1. Encrypt file")
    print(Fore.YELLOW + " 2. Encrypt with OTP")
    print(Fore.YELLOW + " 3. Decrypt encrypted script\n")

    choice = input(Fore.BLUE + ">>> ").strip()

    if choice == "1":
        input_file = input("📁 Enter file to encrypt: ").strip()
        output_file = input("📁 Output encrypted file name: ").strip()
        password = getpass("🔐 Set encryption password: ").strip()
        confirm = getpass("🔐 Confirm password: ").strip()
        if confirm != password:
            print(Fore.RED + "❌ Passwords do not match!")
            exit(1)
        self_destruct = input("💣 Enable self-destruct after run? (y/n): ").strip().lower() == "y"
        runtime = "python3" if input_file.endswith(".py") else "bash"
        encrypt_file(input_file, output_file, password, self_destruct, runtime)

    elif choice == "2":
        input_file = input("📁 Enter file to encrypt: ").strip()
        output_file = input("📁 Output encrypted file name: ").strip()
        password = generate_otp()
        print(Fore.CYAN + f"🔐 One-Time Password (OTP): {Fore.YELLOW}{password}")
        self_destruct = input("💣 Enable self-destruct after run? (y/n): ").strip().lower() == "y"
        runtime = "python3" if input_file.endswith(".py") else "bash"
        encrypt_file(input_file, output_file, password, self_destruct, runtime, use_otp=True)

    elif choice == "3":
        encrypted_file = input("📄 Enter encrypted .sh file: ").strip()
        output_file = input("📁 Save decrypted output to: ").strip()
        decrypt_script(encrypted_file, output_file)

    else:
        print(Fore.RED + "❌ Invalid option!")

except KeyboardInterrupt:
    print(Fore.RED + "\n❌ User aborted. Exiting.")
except Exception as e:
    print(Fore.RED + f"\n❌ Error: {e}")
