import os
import zipfile
import shutil
import hashlib
import getpass
import hmac
from cryptography.fernet import Fernet

BASE_DIR = os.path.expanduser("~/APP")
TARGET_FOLDER = os.path.join(BASE_DIR, "FILES_TO_SECURE")
ENCRYPTED_FILE = os.path.join(BASE_DIR, "secure_data.enc")
ZIP_FILE = os.path.join(BASE_DIR, "secure_data.zip")
PASSWORD_HASH_FILE = os.path.join(BASE_DIR, "password.hash")
KEY_FILE = os.path.join(BASE_DIR, "secret.key")

EXTENSIONS = ('.jpg', '.jpeg', '.png', '.mp4', '.mp3', '.txt', '.pdf', '.csv', '.apk')

def sha256(text): return hashlib.sha256(text.encode()).hexdigest()
def check_password(user_input, stored_hash): return hmac.compare_digest(sha256(user_input), stored_hash)
def generate_key(): return Fernet.generate_key()

def encrypt_file(input_file, output_file, key):
    with open(input_file, 'rb') as f: data = f.read()
    encrypted = Fernet(key).encrypt(data)
    with open(output_file, 'wb') as f: f.write(encrypted)

def delete_all():
    print("\n🚨 Too many wrong attempts! Starting self-destruction...\n")
    for root, dirs, files in os.walk(BASE_DIR, topdown=False):
        for f in files:
            path = os.path.join(root, f)
            try:
                os.remove(path)
                print(f"🧹 Deleted: {path}")
            except: pass
        for d in dirs:
            try:
                os.rmdir(os.path.join(root, d))
            except: pass
    print("💣 All data and code destroyed.\n")
    exit()

def collect_files(folder):
    collected = []
    for root, _, files in os.walk(folder):
        for f in files:
            if f.endswith(EXTENSIONS):
                collected.append(os.path.join(root, f))
    return collected

def zip_files(files, zip_path):
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for f in files:
            arcname = os.path.relpath(f, TARGET_FOLDER)
            zipf.write(f, arcname)

def setup():
    print("🛡️  First time setup...")
    files = collect_files(TARGET_FOLDER)
    print(f"📦 Collecting files...\n🔐 Total files collected: {len(files)}")
    if not files:
        print("⚠️  No target files found.")
        return

    zip_files(files, ZIP_FILE)
    key = generate_key()
    with open(KEY_FILE, 'wb') as f: f.write(key)
    encrypt_file(ZIP_FILE, ENCRYPTED_FILE, key)
    os.remove(ZIP_FILE)

    pwd = input("🔑 Set your password: ")
    with open(PASSWORD_HASH_FILE, 'w') as f: f.write(sha256(pwd))
    print("✅ Setup complete. Encrypted file saved.\n")

def verify_password():
    if not os.path.exists(PASSWORD_HASH_FILE):
        print("❌ No password hash. Run first-time setup.")
        exit()
    with open(PASSWORD_HASH_FILE) as f:
        saved = f.read()
    tries = 3
    while tries > 0:
        pwd = input("🔐 Enter password: ")
        if check_password(pwd, saved):
            print("✅ Access granted.\n")
            return True
        tries -= 1
        print(f"❌ Wrong password. {tries} attempts left.")
    delete_all()

def main():
    os.makedirs(BASE_DIR, exist_ok=True)
    os.makedirs(TARGET_FOLDER, exist_ok=True)
    if not os.path.exists(ENCRYPTED_FILE):
        setup()
    else:
        verify_password()

if __name__ == "__main__":
    main()
