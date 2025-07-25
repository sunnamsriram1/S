#!/usr/bin/env python3
import os
from mega import Mega
from getpass import getpass

def show_banner():
    print("S MEGA Uploader — Encrypted Cloud Backup")
    print("🔐 Securely Upload Folders or Files to MEGA\n")

def main():
    show_banner()

    # Step 1: Get credentials
    email = input("📧 Enter MEGA Email: ").strip()
    password = getpass("🔑 Enter MEGA Password: ").strip()

    # Step 2: Login
    print("\n🔗 Logging in to MEGA...")
    try:
        mega = Mega()
        m = mega.login(email, password)
        print("✅ Login successful!\n")
    except Exception as e:
        print("❌ Login failed:", str(e))
        return

    # Step 3: Choose file or folder
    path = input("📁 Enter full path to file or folder to upload: ").strip()
    if not os.path.exists(path):
        print("❌ Path not found.")
        return

    try:
        if os.path.isfile(path):
            print(f"📤 Uploading file: {os.path.basename(path)}")
            m.upload(path)
            print("✅ File uploaded successfully!")

        elif os.path.isdir(path):
            files = os.listdir(path)
            print(f"📤 Uploading {len(files)} files from folder: {path}")
            for fname in files:
                full_path = os.path.join(path, fname)
                if os.path.isfile(full_path):
                    print(f"  ↪️ Uploading: {fname}...")
                    m.upload(full_path)
            print("✅ All files uploaded successfully!")

        else:
            print("❌ Invalid file/folder path.")

    except Exception as e:
        print("❌ Upload failed:", str(e))

if __name__ == "__main__":
    main()
