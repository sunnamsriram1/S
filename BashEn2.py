from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from hashlib import sha256
import os

# 🔒 Key generator (uses password)
def get_key(password):
    return sha256(password.encode()).digest()

# 🔐 AES Encryption
def encrypt_file(file_path, password):
    with open(file_path, 'rb') as f:
        data = f.read()

    key = get_key(password)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Pad to 16 bytes
    while len(data) % 16 != 0:
        data += b' '

    encrypted = cipher.encrypt(data)

    enc_file = file_path + '.enc'
    with open(enc_file, 'wb') as f:
        f.write(iv + encrypted)

    print(f"✅ File encrypted: {enc_file}")

# 🔓 AES Decryption
def decrypt_file(enc_path, password):
    with open(enc_path, 'rb') as f:
        iv = f.read(16)
        encrypted = f.read()

    key = get_key(password)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(encrypted)

    dec_file = enc_path.replace('.enc', '.dec.sh')
    with open(dec_file, 'wb') as f:
        f.write(decrypted.rstrip(b' '))

    print(f"✅ File decrypted: {dec_file}")

# 🧑‍💻 User Interaction
def main():
    print("🛡️ Bash File Encryptor & Decryptor")
    print("1. Encrypt")
    print("2. Decrypt")
    choice = input("Select (1/2): ")

    path = input("📁 Enter file path: ").strip()
    if not os.path.isfile(path):
        print("❌ File not found!")
        return

    password = input("🔑 Enter password: ")

    if choice == '1':
        encrypt_file(path, password)
    elif choice == '2':
        decrypt_file(path, password)
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
