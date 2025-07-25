#!/usr/bin/env python3
import os
import time
import pyAesCrypt
from getpass import getpass
from mega.mega import Mega  # ✅ FIXED
import shutil

BUFFER_SIZE = 64 * 1024

def zip_folder(folder_path):
    zip_path = folder_path.rstrip("/").split("/")[-1] + ".zip"
    shutil.make_archive(zip_path.replace(".zip", ""), 'zip', folder_path)
    return zip_path

def encrypt_file(file_path, password):
    encrypted_path = file_path + ".aes"
    pyAesCrypt.encryptFile(file_path, encrypted_path, password, BUFFER_SIZE)
    os.remove(file_path)
    return encrypted_path

def upload_to_mega(email, password, file_path):
    mega = Mega()
    m = mega.login(email, password)
    print("☁️ Uploading to MEGA...")
    m.upload(file_path)
    print("✅ Upload complete.")

def main():
    print("🔐 Cloud Folder Encrypted Uploader")
    folder = input("📁 Enter full folder path to upload: ").strip()
    if not os.path.isdir(folder):
        print("❌ Invalid folder path.")
        return

    email = input("📧 Enter your MEGA email: ").strip()
    cloud_pass = getpass("🔑 MEGA password: ")
    enc_pass = getpass("🔐 Set encryption password: ")

    print("🗜️ Zipping folder...")
    zip_file = zip_folder(folder)

    print("🔐 Encrypting zipped file...")
    encrypted_file = encrypt_file(zip_file, enc_pass)

    upload_to_mega(email, cloud_pass, encrypted_file)

    print(f"🔏 File uploaded: {encrypted_file}")
    print("💡 To decrypt later: use the same password you set now.")

if __name__ == "__main__":
    main()
