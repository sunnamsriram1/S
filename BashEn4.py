import base64
import getpass
import os

# 🔐 USER INPUT
bash_file = input("📁 Enter Bash file to encrypt (e.g., SqlTor5.3.sh): ").strip()

# ✅ CHECK FILE EXISTS
if not os.path.exists(bash_file):
    print("❌ File not found:", bash_file)
    exit()

# 📄 READ AND ENCRYPT
with open(bash_file, "rb") as f:
    data = f.read()

encoded = base64.b64encode(data).decode()

# 🔐 PASSWORD (OPTIONAL)
password = getpass.getpass("🔑 Set password to lock this script: ").strip()

# ✅ OUTPUT PYTHON SCRIPT WITH ENCRYPTED BASH
output_file = bash_file + ".enc.sh"

with open(output_file, "w") as out:
    out.write(f"""#!/data/data/com.termux/files/usr/bin/bash
# 🔐 Auto Decrypting Bash Runner (Encrypted by BashEn.py)

read -sp "🔑 Enter password: " input_pw
echo
if [ "$input_pw" != "{password}" ]; then
  echo "❌ Incorrect password!"
  exit 1
fi

# 📦 Decrypt and Run Encrypted Bash Script
encoded_script=\"""{encoded}\"""

temp_file="/data/data/com.termux/files/usr/tmp/tmp_run.sh"
mkdir -p "$(dirname "$temp_file")"
echo "$encoded_script" | base64 -d > "$temp_file"
chmod +x "$temp_file"
bash "$temp_file"
rm -f "$temp_file"
""")

# ✅ DONE
os.chmod(output_file, 0o755)
print("✅ Encrypted Bash file saved as:", output_file)
