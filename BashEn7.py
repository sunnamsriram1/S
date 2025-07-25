import base64
import os
from getpass import getpass
from cryptography.fernet import Fernet
from hashlib import sha256

def generate_key(password: str) -> bytes:
    return base64.urlsafe_b64encode(sha256(password.encode()).digest())

def encrypt_bash_file(input_file: str, output_file: str, password: str):
    # Read original bash code
    with open(input_file, 'r') as f:
        original_code = f.read()

    # Add copyright line at top
    final_code = "# 🔐 Encrypted & coded by Sriram\n" + original_code

    # Encrypt using Fernet
    key = generate_key(password)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(final_code.encode())

    # Create executable bash file
    with open(output_file, 'w') as f:
        f.write(f'''#!/data/data/com.termux/files/usr/bin/bash
echo -e "🔑 Enter password:"
read -s password
KEY=$(echo -n "$password" | openssl dgst -sha256 -binary | base64 | cut -b1-43 | tr '+/' '-_')
ENCODED_KEY=$(printf '%-44s' "$KEY" | tr ' ' '=')
SCRIPT=$(tail -n +9 "$0" | base64 -d | openssl enc -d -aes-256-cbc -pbkdf2 -pass pass:$password 2>/dev/null)
if [ -z "$SCRIPT" ]; then
    echo "❌ Incorrect password!"
    exit 1
fi
echo "$SCRIPT" > /data/data/com.termux/files/usr/tmp/tmp_run.sh
chmod +x /data/data/com.termux/files/usr/tmp/tmp_run.sh
bash /data/data/com.termux/files/usr/tmp/tmp_run.sh
rm /data/data/com.termux/files/usr/tmp/tmp_run.sh
exit 0
''')

        # Write encrypted content as base64
        os.system("mkdir -p /data/data/com.termux/files/usr/tmp")
        encrypted_base64 = base64.b64encode(encrypted).decode()
        f.write(f"\n{encrypted_base64}")

    os.chmod(output_file, 0o755)
    print(f"✅ Encrypted file saved as: {output_file}")

if __name__ == "__main__":
    input_file = input("📂 Enter bash file to encrypt: ").strip()
    if not os.path.isfile(input_file):
        print("❌ File not found.")
        exit(1)

    output_file = input("💾 Enter output encrypted file name (e.g., SqlTor5.1.sh.enc.sh): ").strip()
    password = getpass("🔐 Set encryption password: ")
    encrypt_bash_file(input_file, output_file, password)
