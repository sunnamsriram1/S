from mega import Mega
import os

# ✅ Enter your MEGA login credentials
EMAIL = 'toradx6@gmail.com'
PASSWORD = 'Abcde33@Toradx6@'

# 📁 Enter path to file you want to upload
FILE_PATH = '/data/data/com.termux/files/home/my_secret_file.txt'

# 🔐 Login to MEGA
mega = Mega()
print("🔐 Logging into MEGA...")
m = mega.login(EMAIL, PASSWORD)

# 📤 Upload the file
if os.path.exists(FILE_PATH):
    print(f"📤 Uploading file: {FILE_PATH}")
    uploaded_file = m.upload(FILE_PATH)
    file_url = m.get_upload_link(uploaded_file)
    print("✅ Upload complete!")
    print("🔗 File URL:", file_url)
else:
    print("❌ File not found.")
