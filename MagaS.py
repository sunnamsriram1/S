import os
import time
from getpass import getpass
from mega import Mega
import asyncio
import types

...

@types.coroutine  # Use this instead of @asyncio.coroutine


def banner():
    print("\n===============================")
    print("🗂️  S MEGA Uploader — Encrypted Cloud Backup")
    print("===============================\n")

# 🔐 User Credentials
EMAIL = "toradx6@gmail.com"
PASSWORD = "Abcde33@"  # Replace with a secure method if needed

# 🔐 Prompt for file/folder to upload
def upload_to_mega(path_to_upload):
    banner()
    print("🔐 Logging in to MEGA...")
    mega = Mega()
    m = mega.login(EMAIL, PASSWORD)

    if os.path.isdir(path_to_upload):
        print(f"📁 Uploading folder: {path_to_upload}")
        m.upload(path_to_upload, None)
    elif os.path.isfile(path_to_upload):
        print(f"📄 Uploading file: {path_to_upload}")
        m.upload(path_to_upload, None)
    else:
        print("❌ Invalid file or folder path.")
        return

    print("✅ Upload complete.")

# 🔁 Main
if __name__ == "__main__":
    path = input("📂 Enter full path of file/folder to upload: ").strip()
    upload_to_mega(path)
