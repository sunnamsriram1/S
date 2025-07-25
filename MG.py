#!/usr/bin/env python3
import os
import getpass
import random
import string
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from mega import Mega
import shutil

# 📦 Random filename generator
def random_filename(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# 🔐 AES Encrypt a file
def encrypt_file(input_file, password, output_file):
    key = password.ljust(32, '0')[:32].encode('utf-8')  # 32-byte key
    cipher = AES.new(key, AES.MODE_EAX)
    with open(input_file, 'rb') as f:
        data = f.read()
    ciphertext, tag = cipher.encrypt_and_digest(data)
    with open(output_file, 'wb') as f:
        f.write(cipher.nonce)
        f.write(tag)
        f.write(ciphertext)

# 📁 Encrypt entire folder
def encrypt_folder(folder_path, password, enc_folder):
    if not os.path.exists(enc_folder):
        os.makedirs(enc_folder)
    for root, _, files in os.walk(folder_path):
        for file in files:
            orig_path = os.path.join(root, file)
            enc_name = random_filename() + ".enc"
            enc_path = os.path.join(enc_folder, enc_name)
            encrypt_file(orig_path, password, enc_path)
            print(f"🔒 Encrypted: {file} → {enc_name}")

# ☁️ Upload to MEGA
def upload_to_mega(email, password, folder):
    print("☁️ Logging into MEGA...")
    mega = Mega()
    m = mega.login(email, password)
    for file in os.listdir(folder):
        file_path = os.path.join(folder, file)
        if os.path.isfile(file_path):
            print(f"📤 Uploading {file}...")
            m.upload(file_path)
    print("✅ Upload complete!")

# 🚀 Main Execution
def main():
    print("\n🔐 S MEGA Encrypted Cloud Uploader")
    folder = input("📁 Enter folder path to backup: ").strip()
    if not os.path.isdir(folder):
        print("❌ Invalid folder.")
        return
    passwd = getpass.getpass("🔑 Set encryption password: ")
    mega_email = input("📧 MEGA email: ").strip()
    mega_pass = getpass.getpass("🔑 MEGA password: ")

    enc_folder = os.path.join("/data/data/com.termux/files/home/S", ".encrypted_upload")
    encrypt_folder(folder, passwd, enc_folder)
    upload_to_mega(mega_email, mega_pass, enc_folder)

    # Cleanup
    shutil.rmtree(enc_folder)
    print("🧹 Local encrypted files deleted.")

if __name__ == "__main__":
    main()
