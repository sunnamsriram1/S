#!/usr/bin/env python3
import os
import sys
import shutil
import zipfile
import hashlib
import hmac
import time
import secrets
from getpass import getpass
from pathlib import Path
from cryptography.fernet import Fernet

# ========= CONFIG =========
PASSWORD_HASH = "c2a9b10c14f80c6d3ebff080123b6b11f7e032f46f57ae8c20b9b13d2a2e08a2"  # password: sriram123
MAX_ATTEMPTS = 3
DATA_DIR = Path("./SecureData")       # Folder to store encrypted files
TEMP_DIR = Path("./__tempstore__")    # Temporary files before zip
ENC_FILE = DATA_DIR / "encrypted_store.dat"
DRY_RUN = False
FILE_TYPES = [".jpg", ".png", ".mp4", ".pdf", ".txt", ".csv", ".apk"]
# ==========================

def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()

def constant_time_check(pwd: str) -> bool:
    return hmac.compare_digest(sha256_hex(pwd), PASSWORD_HASH)

def secure_overwrite_file(path: Path, passes=2):
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
            secure_overwrite_file(path)
            path.unlink(missing_ok=True)
    elif path.is_dir():
        for item in path.glob("**/*"):
            destroy_path(item)
        if not DRY_RUN:
            path.rmdir()

def self_destruct():
    print("\n🚨 Too many wrong attempts! Destroying data...\n")
    destroy_path(DATA_DIR)
    destroy_path(TEMP_DIR)
    destroy_path(Path(__file__))
    print("💣 Self-destruct complete. All data and script deleted.")
    sys.exit(1)

def ask_password():
    try:
        return getpass("🔐 Enter Password: ")
    except:
        return input("🔐 Enter Password: ")

def collect_files():
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir(parents=True)

    print("📦 Collecting target files to secure...")
    count = 0
    for root, _, files in os.walk("."):
        if str(TEMP_DIR.resolve()) in root or str(DATA_DIR.resolve()) in root:
            continue
        for file in files:
            ext = Path(file).suffix.lower()
            if ext in FILE_TYPES:
                src = Path(root) / file
                dst = TEMP_DIR / Path(file).name
                try:
                    shutil.copy2(src, dst)
                    print(f"✅ Collected: {src}")
                    count += 1
                except:
                    print(f"❌ Failed to copy: {src}")
    print(f"🔐 Total files collected: {count}")
    return count

def zip_temp_files(zip_path: Path):
    print(f"\n📁 Zipping files into: {zip_path}")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in TEMP_DIR.iterdir():
            zipf.write(file, arcname=file.name)
    print("✅ Zipped successfully.")

def encrypt_file(input_file: Path, output_file: Path, key: bytes):
    print(f"\n🔒 Encrypting zip file → {output_file}")
    with open(input_file, "rb") as f:
        data = f.read()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    with open(output_file, "wb") as ef:
        ef.write(encrypted)
    print("✅ Encrypted and saved.")

def generate_key():
    key_path = DATA_DIR / "fernet.key"
    key = Fernet.generate_key()
    key_path.write_bytes(key)
    print(f"🔑 Fernet key saved to: {key_path}")
    return key

def main():
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        pwd = ask_password()
        if constant_time_check(pwd):
            print("✅ Access granted.\n")
            break
        else:
            attempts += 1
            print(f"❌ Wrong password. Attempts left: {MAX_ATTEMPTS - attempts}")
            time.sleep(1)
    else:
        self_destruct()

    # Make secure storage dir
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Collect files to temp
    file_count = collect_files()
    if file_count == 0:
        print("⚠️ No files found to secure.")
        return

    # Create zip
    zip_path = DATA_DIR / "data.zip"
    zip_temp_files(zip_path)

    # Encrypt
    key = generate_key()
    encrypt_file(zip_path, ENC_FILE, key)

    # Clean up
    if zip_path.exists():
        zip_path.unlink()
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)

    print("\n✅ All files securely zipped and encrypted.")
    print("📂 Encrypted file: ", ENC_FILE)
    print("🗝️  Decryption key saved as: ", DATA_DIR / "fernet.key")

if __name__ == "__main__":
    main()

