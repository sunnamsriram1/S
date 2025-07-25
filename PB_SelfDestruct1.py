#!/usr/bin/env python3
import os
import base64
import random
import string
from getpass import getpass
from cryptography.fernet import Fernet
from datetime import datetime

# Banner at the beginning
def show_banner():
    time_now = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    print("\n" + "═" * 55)
    print("★ Coded by     : SUNNAM_SRIRAM_1")
    print(f"★ India Time   : {time_now}")
    print("═" * 55 + "\n")

# Generate key from password
def generate_key(password: str) -> bytes:
    return base64.urlsafe_b64encode(password.ljust(32, '0')[:32].encode())

# Generate one-time password
def generate_otp(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# Encrypt and create self-running script
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

    # Log the operation
    with open("PB_encrypt_log.txt", "a") as log:
        log.write(f"[{datetime.now()}] 🔐 {output_file} encrypted from {input_file}\n")

# --- Main Execution ---
try:
    show_banner()

    input_file = input("📁 Enter file to encrypt (e.g., script.sh or script.py): ").strip()
    output_file = input("📁 Output encrypted file name: ").strip()

    otp_choice = input("🔁 Use one-time random password (OTP)? (y/n): ").strip().lower()
    use_otp = otp_choice == 'y'

    if use_otp:
        password = generate_otp()
        print(f"🔐 One-Time Password (OTP): {password}")
    else:
        password = getpass("🔐 Set encryption password: ").strip()
        confirm = getpass("🔐 Confirm password: ").strip()
        if confirm != password:
            print("❌ Passwords do not match!")
            exit(1)

    destruct_choice = input("💣 Enable self-destruct after run? (y/n): ").strip().lower()
    self_destruct = destruct_choice == "y"

    # Detect file type
    runtime = "python3" if input_file.endswith(".py") else "bash"

    encrypt_file(input_file, output_file, password, self_destruct, runtime, use_otp)
    print(f"\n✅ Encrypted saved to: {output_file}")
    print("📜 Log updated: PB_encrypt_log.txt")

except KeyboardInterrupt:
    print("\n❌ User aborted with Ctrl+C. Exiting safely.")
    exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
