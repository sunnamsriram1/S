#!/usr/bin/env python3
import os
import sys
import shutil
import hashlib
import hmac
import time
import secrets
from getpass import getpass
from pathlib import Path

# ========== CONFIG ==========
PASSWORD_HASH = "c2a9b10c14f80c6d3ebff080123b6b11f7e032f46f57ae8c20b9b13d2a2e08a2"  # password: sriram123
MAX_ATTEMPTS = 3
DATA_DIR = Path("./SecureData")  # Safe storage folder
DRY_RUN = False  # False means real deletion
# ============================

TARGET_EXTENSIONS = [".jpg", ".jpeg", ".png", ".mp4", ".mkv", ".pdf", ".txt", ".csv", ".apk"]

def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def constant_time_check(pwd: str) -> bool:
    return hmac.compare_digest(sha256_hex(pwd), PASSWORD_HASH)

def collect_files():
    if not DATA_DIR.exists():
        DATA_DIR.mkdir(parents=True)

    print("📁 Searching files to store securely...")
    count = 0
    for root, dirs, files in os.walk("."):
        if str(DATA_DIR.resolve()) in str(Path(root).resolve()):
            continue  # Skip our own storage folder

        for f in files:
            ext = Path(f).suffix.lower()
            if ext in TARGET_EXTENSIONS:
                full_path = Path(root) / f
                dest = DATA_DIR / Path(f).name
                try:
                    shutil.copy2(full_path, dest)
                    print(f"✅ Copied: {full_path} → {dest}")
                    count += 1
                except Exception as e:
                    print(f"❌ Failed: {full_path}: {e}")
    print(f"\n🔐 Total files securely stored: {count}")

def secure_overwrite_file(path: Path, passes=1):
    try:
        size = path.stat().st_size
        with open(path, "r+b", buffering=0) as f:
            for _ in range(passes):
                f.seek(0)
                f.write(secrets.token_bytes(size))
                f.flush()
                os.fsync(f.fileno())
    except Exception as e:
        print(f"[!] Overwrite failed for {path}: {e}")

def destroy_path(path: Path):
    if not path.exists():
        return
    if path.is_file():
        print(f"🧹 Deleting file: {path}")
        if not DRY_RUN:
            secure_overwrite_file(path, 2)
            try:
                path.unlink()
                print(f"✅ File deleted: {path}")
            except:
                print(f"❌ Couldn't delete: {path}")
    elif path.is_dir():
        print(f"🧹 Deleting folder: {path}")
        for child in path.glob("**/*"):
            destroy_path(child)
        if not DRY_RUN:
            try:
                path.rmdir()
                print(f"✅ Folder deleted: {path}")
            except:
                print(f"❌ Couldn't delete folder: {path}")

def self_destruct():
    print("\n🚨 Too many wrong attempts! Starting self-destruction...\n")
    time.sleep(1)
    destroy_path(DATA_DIR)
    destroy_path(Path(__file__))  # Delete this script file
    print("\n💣 All data and code destroyed. Exiting...\n")
    sys.exit(1)

def ask_password():
    try:
        return getpass("🔐 Enter Password: ")
    except:
        return input("🔐 Enter Password: ")

def main():
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        pwd = ask_password()
        if constant_time_check(pwd):
            print("✅ Access granted.")
            break
        else:
            attempts += 1
            left = MAX_ATTEMPTS - attempts
            print(f"❌ Wrong password. Attempts left: {left}\n")
            time.sleep(1)
    else:
        self_destruct()

    # If password correct, collect and store files
    collect_files()

if __name__ == "__main__":
    main()
