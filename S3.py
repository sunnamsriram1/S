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

# ========== CONFIG ==========
DATA_DIR = Path("./SecureData")
TEMP_DIR = Path("./__tempstore__")
ENC_FILE = DATA_DIR / "encrypted_store.dat"
KEY_FILE = DATA_DIR / "fernet.key"
SCRIPT_FILE = Path(__file__)
FILE_TYPES = [".jpg", ".png", ".mp4", ".pdf", ".txt", ".csv", ".apk"]

MAX_ATTEMPTS = 3
DRY_RUN = False  # False = delete for real
# ============================

# Password will be generated AFTER encryption
PASSWORD_HASH = None  # Will be set dynamically


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
    print("\n🚨 Too many wrong attempts! Starting self-destruction...\n")
    destroy_path(DATA_DIR)
    destroy_path(TEMP_DIR)
    destroy_path(SCRIPT_FILE)
    print("💣 All data and code destroyed. Exiting...\n")
    sys.exit(1)


def collect_files():
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)
    TEMP_DIR.mkdir(parents=True)

    print("📦 Collecting files...")
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
    key = Fernet.generate_key()
    KEY_FILE.write_bytes(key)
    print(f"🔑 Fernet key saved to: {KEY_FILE}")
    return key


def prompt_and_set_password():
    global PASSWORD_HASH
    print("\n🔐 Set a new password to protect this data.")
    while True:
        pwd1 = getpass("New Password: ")
        pwd2 = getpass("Confirm Password: ")
        if pwd1 != pwd2:
            print("❗Passwords do not match. Try again.")
        elif len(pwd1.strip()) < 4:
            print("❗Password too short. Use at least 4 characters.")
        else:
            break
    PASSWORD_HASH = sha256_hex(pwd1)
    with open(DATA_DIR / "password.hash", "w") as f:
        f.write(PASSWORD_HASH)
    print("✅ Password saved.")


def load_password():
    global PASSWORD_HASH
    try:
        with open(DATA_DIR / "password.hash", "r") as f:
            PASSWORD_HASH = f.read().strip()
    except:
        print("❌ Password file missing.")
        sys.exit(1)


def ask_password_and_verify():
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        pwd = getpass("🔐 Enter Password: ")
        if constant_time_check(pwd):
            print("✅ Access granted.\n")
            return True
        else:
            attempts += 1
            print(f"❌ Wrong password. Attempts left: {MAX_ATTEMPTS - attempts}")
            time.sleep(1)
    self_destruct()


def main():
    # Check first run
    if not (DATA_DIR / "password.hash").exists():
        print("🛡️  First time setup...")
        DATA_DIR.mkdir(exist_ok=True, parents=True)
        count = collect_files()
        if count == 0:
            print("⚠️  No target files found.")
            return
        zip_path = DATA_DIR / "data.zip"
        zip_temp_files(zip_path)
        key = generate_key()
        encrypt_file(zip_path, ENC_FILE, key)
        os.remove(zip_path)
        shutil.rmtree(TEMP_DIR)
        prompt_and_set_password()
        print("\n🎉 Setup complete. Your files are securely encrypted.\n")
        return

    # Already setup — ask password
    load_password()
    ask_password_and_verify()
    print("📂 Encrypted File:", ENC_FILE)
    print("🗝️  Key File:", KEY_FILE)


if __name__ == "__main__":
    main()

