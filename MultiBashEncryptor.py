from cryptography.fernet import Fernet
from getpass import getpass
from datetime import datetime
import base64
import os

# Banner info
def show_banner():
    now = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
    print("═══════════════════════════════════════════════════════")
    print("★ Coded by     : SUNNAM_SRIRAM_1")
    print(f"★ India Time   : {now}")
    print("═══════════════════════════════════════════════════════\n")

# Key generation
def generate_key(password: str) -> bytes:
    return base64.urlsafe_b64encode(password.ljust(32, '0')[:32].encode())

# Encryption function
def encrypt_file(input_file, output_file, password, runtime, self_destruct):
    key = generate_key(password)
    fernet = Fernet(key)

    with open(input_file, 'rb') as f:
        data = f.read()
    
    encrypted = fernet.encrypt(data).decode()

    now = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

    with open(output_file, 'w') as f:
        f.write(f'''#!/bin/bash
# 🔐 Encrypted & coded by Sriram

echo -n "🔑 Enter password: "
read -s input
echo
key=$(python3 -c "import base64, sys; print(base64.urlsafe_b64encode(sys.argv[1].ljust(32, '0')[:32].encode()).decode())" "$input")
tmp_file=$(mktemp)
if ! python3 -c "from cryptography.fernet import Fernet; import sys; print(Fernet(sys.argv[1].encode()).decrypt(b'{encrypted}').decode())" "$key" > $tmp_file 2>/dev/null; then
    echo "❌ Incorrect password or decryption failed!"
    exit 1
fi
echo -e "═══════════════════════════════════════════════════════"
echo -e "★ Coded by     : SUNNAM_SRIRAM_1"
echo -e "★ India Time   : {now}"
echo -e "═══════════════════════════════════════════════════════"
chmod +x $tmp_file
{runtime} $tmp_file
''')
        if self_destruct:
            f.write("rm -- \"$0\"\n")
        f.write("rm $tmp_file\n")

# Main code
if __name__ == "__main__":
    try:
        show_banner()
        input_list = input("📁 Enter files to encrypt (comma-separated): ").strip().split(",")
        input_files = [file.strip() for file in input_list if file.strip()]
        password = getpass("🔐 Set encryption password: ").strip()
        self_destruct = input("💣 Enable self-destruct after run? (y/n): ").strip().lower() == 'y'

        for file_path in input_files:
            if not os.path.isfile(file_path):
                print(f"❌ Skipped: '{file_path}' not found.")
                continue
            ext = file_path.split(".")[-1]
            runtime = "python3" if ext == "py" else "bash"
            output_name = "enc_" + os.path.basename(file_path)
            encrypt_file(file_path, output_name, password, runtime, self_destruct)
            print(f"✅ Encrypted: {file_path} ➜ {output_name}")

    except KeyboardInterrupt:
        print("\n🛑 Cancelled by user.")
