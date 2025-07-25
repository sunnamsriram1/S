from cryptography.fernet import Fernet
from getpass import getpass
import os
import base64
import tempfile

def generate_key(password: str) -> bytes:
    return base64.urlsafe_b64encode(password.encode().ljust(32, b'#'))

def encrypt_file(input_file, output_file, password):
    with open(input_file, 'rb') as f:
        data = f.read()

    # Add Sriram signature to script
    signature = "# 🔐 Encrypted & coded by Sriram\n".encode('utf-8')
    if signature not in data:
        data += b"\n" + signature

    key = generate_key(password)
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted)

    print(f"\n✅ Encrypted bash saved to: {output_file}")

def decrypt_and_run(encrypted_file, password):
    key = generate_key(password)
    fernet = Fernet(key)
    try:
        with open(encrypted_file, 'rb') as f:
            encrypted = f.read()
        decrypted = fernet.decrypt(encrypted)
    except Exception:
        print("❌ Incorrect password or corrupted file!")
        return

    with tempfile.NamedTemporaryFile(delete=False, suffix=".sh", mode='wb') as tmp:
        tmp.write(decrypted)
        tmp_path = tmp.name

    os.chmod(tmp_path, 0o700)
    print("🔓 Running decrypted script...")
    os.system(f"bash {tmp_path}")
    os.remove(tmp_path)

def main():
    print("🔐 Secure Bash Encryptor/Runner by Sriram")
    choice = input("📌 Choose [e]ncrypt or [r]un: ").strip().lower()

    if choice == 'e':
        input_file = input("📁 Enter bash file to encrypt (e.g., script.sh): ").strip()
        output_file = input("💾 Enter output file (e.g., script.enc): ").strip()
        password = getpass("🔐 Set encryption password: ").strip()
        encrypt_file(input_file, output_file, password)
    elif choice == 'r':
        encrypted_file = input("📁 Enter encrypted file (e.g., script.enc): ").strip()
        password = getpass("🔑 Enter password to run script: ").strip()
        decrypt_and_run(encrypted_file, password)
    else:
        print("❌ Invalid choice!")

if __name__ == "__main__":
    main()
