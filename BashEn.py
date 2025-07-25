from cryptography.fernet import Fernet
import os

def generate_key():
    return Fernet.generate_key()

def save_key(key, key_file):
    with open(key_file, 'wb') as f:
        f.write(key)

def load_key(key_file):
    with open(key_file, 'rb') as f:
        return f.read()

def encrypt_bash_file(input_file, output_file, key_file):
    key = generate_key()
    save_key(key, key_file)
    fernet = Fernet(key)

    with open(input_file, 'rb') as f:
        data = f.read()

    encrypted_data = fernet.encrypt(data)

    with open(output_file, 'wb') as f:
        f.write(encrypted_data)

    print(f"\n[✓] File Encrypted: {output_file}")
    print(f"[🔑] Key saved to: {key_file}\n")

def decrypt_and_run(enc_file, key_file):
    try:
        key = load_key(key_file)
        fernet = Fernet(key)

        with open(enc_file, 'rb') as f:
            encrypted_data = f.read()

        decrypted_data = fernet.decrypt(encrypted_data)

        temp_file = "/tmp/temp_bash_script.sh"
        with open(temp_file, 'wb') as f:
            f.write(decrypted_data)

        os.system(f"chmod +x {temp_file} && bash {temp_file}")
        os.remove(temp_file)

        print("\n[✓] Decrypted and Executed Successfully\n")
    except Exception as e:
        print(f"\n[✗] Error: {e}\n")

def main():
    print("🛡️  Bash File Encryptor & Runner (AES-256)")
    print("------------------------------------------")
    print("1. 🔐 Encrypt a bash file")
    print("2. ▶️  Decrypt and run an encrypted file")
    choice = input("👉 Select option (1 or 2): ")

    if choice == '1':
        input_file = input("📄 Enter bash file to encrypt (e.g., SqlTor5.3.sh): ").strip()
        output_file = input("📁 Enter name for encrypted file (e.g., output.sh.enc): ").strip()
        key_file = input("🔑 Enter key filename to save (e.g., mykey.key): ").strip()
        encrypt_bash_file(input_file, output_file, key_file)

    elif choice == '2':
        enc_file = input("📁 Enter encrypted file name (e.g., output.sh.enc): ").strip()
        key_file = input("🔑 Enter key file name (e.g., mykey.key): ").strip()
        decrypt_and_run(enc_file, key_file)

    else:
        print("⚠️  Invalid option selected.")

if __name__ == "__main__":
    main()
