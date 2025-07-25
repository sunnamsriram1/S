#!/usr/bin/env python3
import os
import base64
import getpass
import datetime

# Banner
def show_banner():
    banner = f"""
═══════════════════════════════════════════════════════
★ Coded by     : SUNNAM_SRIRAM_1
★ India Time   : {datetime.datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')}
═══════════════════════════════════════════════════════
"""
    print(banner)

# Encrypt file contents
def encrypt_content(content, password):
    encoded = base64.b64encode(content.encode()).decode()
    decryptor = f'''#!/usr/bin/env python3
import base64
import getpass
import os

# 🔐 Encrypted & coded by Sriram

try:
    password = getpass.getpass("🔑 Enter password: ")
    if password != "{password}":
        print("❌ Wrong password!")
        exit(1)
    code = base64.b64decode("{encoded}").decode()
    exec(code, {{}})
except Exception as e:
    print("❌ Error:", e)
'''
    return decryptor

# Process single file
def process_file(file_path, password):
    if not os.path.isfile(file_path):
        print(f"❌ File not found: {file_path}")
        return
    try:
        with open(file_path, "r") as f:
            content = f.read()
        encrypted_code = encrypt_content(content, password)
        output_file = f"enc_{os.path.basename(file_path)}"
        with open(output_file, "w") as out:
            out.write(encrypted_code)
        print(f"✅ Encrypted: {file_path} ➜ {output_file}")
    except Exception as e:
        print(f"❌ Failed to encrypt {file_path}: {e}")

# Main
def main():
    show_banner()
    print("🔄 Choose mode:\n 1. Enter multiple files\n 2. Encrypt all in folder")
    choice = input(">>> ").strip()

    if choice == "1":
        files = input("📁 Enter file names (comma-separated): ").split(",")
        files = [f.strip() for f in files if os.path.isfile(f.strip())]
        if not files:
            print("❌ No valid files found.")
            return
    elif choice == "2":
        folder = input("📁 Enter folder path: ").strip()
        if not os.path.isdir(folder):
            print("❌ Invalid folder.")
            return
        supported_exts = (".sh", ".py", ".txt", ".json", ".zip")
        files = [os.path.join(folder, f) for f in os.listdir(folder)
                 if os.path.isfile(os.path.join(folder, f)) and f.endswith(supported_exts)]
        if not files:
            print("❌ No valid files found in folder.")
            return
    else:
        print("❌ Invalid option.")
        return

    password = getpass.getpass("🔐 Set encryption password: ")
    for file_path in files:
        process_file(file_path, password)

if __name__ == "__main__":
    main()
