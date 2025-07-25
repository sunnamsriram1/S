import os
import shutil
import getpass
import pyAesCrypt
from mega import Mega

BUFFER_SIZE = 64 * 1024

def zip_folder(folder_path):
    zip_file = "temp.zip"
    shutil.make_archive("temp", 'zip', folder_path)
    return zip_file

def encrypt_file(file_path, password):
    encrypted_file = file_path + ".aes"
    pyAesCrypt.encryptFile(file_path, encrypted_file, password, BUFFER_SIZE)
    os.remove(file_path)
    return encrypted_file

def upload_to_mega(email, password, file_path):
    mega = Mega()
    m = mega.login(email, password)
    m.upload(file_path)
    print("✅ File uploaded to MEGA successfully.")

def main():
    print("🔐 Cloud Folder Encrypted Uploader")
    folder_path = input("📁 Enter full folder path to upload: ").strip()
    if not os.path.exists(folder_path):
        print("❌ Folder not found.")
        return

    email = input("📧 Enter your MEGA email: ").strip()
    mega_pass = getpass.getpass("🔑 MEGA password: ")
    enc_pass = getpass.getpass("🔐 Set encryption password: ")

    print("🗜️ Zipping folder...")
    zip_file = zip_folder(folder_path)

    print("🔐 Encrypting zipped file...")
    encrypted_file = encrypt_file(zip_file, enc_pass)

    print("☁️ Uploading to MEGA...")
    upload_to_mega(email, mega_pass, encrypted_file)

    os.remove(encrypted_file)
    print("✅ Done: Encrypted file uploaded and cleaned.")

if __name__ == "__main__":
    main()
