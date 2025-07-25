#!/usr/bin/env python3
import os
import sys
import getpass
import tempfile
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2
from mega import Mega

# === CONFIG ===
SALT = b'some_salt_value_123'  # Keep this static for decryption
BUFFER_SIZE = 64 * 1024  # 64KB chunks

def encrypt_file(file_path, password):
    key = PBKDF2(password, SALT, dkLen=32)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CFB, iv)

    file_name = os.path.basename(file_path)
    enc_file_path = tempfile.mktemp(suffix=".enc")

    with open(file_path, "rb") as f_in, open(enc_file_path, "wb") as f_out:
        f_out.write(iv)  # Write IV first
        while chunk := f_in.read(BUFFER_SIZE):
            f_out.write(cipher.encrypt(chunk))

    return enc_file_path

def upload_to_mega(email, password, file_path):
    print("🔐 Logging in to MEGA...")
    mega = Mega()
    m = mega.login(email, password)
    print("☁️  Uploading file to MEGA cloud...")
    m.upload(file_path)
    print("✅ Upload complete.")

def main():
    print("🔐 Cloud Encrypted Uploader Tool")
    input_file = input("📁 Enter file path to encrypt & upload: ").strip()
    if not os.path.isfile(input_file):
        print("❌ Invalid file path.")
        return

    # Secure password input
    password = getpass.getpass("🔑 Set encryption password: ")

    # Encrypt
    print("🔐 Encrypting file...")
    encrypted_file = encrypt_file(input_file, password)
    print(f"✅ Encrypted file created: {encrypted_file}")

    # MEGA login
    email = input("📧 Enter your MEGA email: ").strip()
    mega_pass = getpass.getpass("🔐 Enter your MEGA password: ")

    upload_to_mega(email, mega_pass, encrypted_file)

    # Delete temp encrypted file
    os.remove(encrypted_file)
    print("🧹 Temporary file deleted.")

if __name__ == "__main__":
    main()
