#!/usr/bin/env python3
import os
import base64
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

# Encrypt and create self-running script
def encrypt_file(input_file, output_file, password, self_destruct=False, runtime="bash"):
    key = generate_key(password)
    fernet = Fernet(key)

    with open(input_file, 'rb') as f:
        data = f.read()

    encrypted = fernet.encrypt(data).decode()
    destruct_line = f"rm -- \"$0\"" if self_destruct else ""

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
echo '# 🔐 Encrypted & coded by Sriram' >> $tmp_file
chmod +x $tmp_file
{runtime} $tmp_file
rm $tmp_file
{destruct_line}
"""
    with open(output_file, 'w') as f:
        f.write(script)

    os.chmod(output_file, 0o755)

# --- Main Execution ---
try:
    show_banner()

    input_file = input("📁 Enter file to encrypt (e.g., script.sh or script.py): ").strip()
    output_file = input("📁 Output encrypted file name: ").strip()
    password = getpass("🔐 Set encryption password: ").strip()
    destruct_choice = input("💣 Enable self-destruct after run? (y/n): ").strip().lower()
    self_destruct = destruct_choice == "y"

    # Detect file type
    runtime = "python3" if input_file.endswith(".py") else "bash"

    encrypt_file(input_file, output_file, password, self_destruct, runtime)
    print(f"✅ Encrypted saved to: {output_file}")

except KeyboardInterrupt:
    print("\n❌ User aborted with Ctrl+C. Exiting safely.")
    exit(1)
except Exception as e:
    print(f"\n❌ Error: {e}")
