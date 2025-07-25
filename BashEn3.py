import base64
import os

# 🔢 Prompt user
input_file = input("📁 Enter bash (.sh) file to encrypt: ").strip()

# ✅ Check if file exists
if not os.path.exists(input_file):
    print("❌ File not found!")
    exit(1)

# 📖 Read contents
with open(input_file, "rb") as f:
    encoded = base64.b64encode(f.read()).decode()

# 📤 Output file
output_file = input_file + ".enc.sh"

# 🖊️ Write self-decrypting bash file
with open(output_file, "w") as f:
    f.write(f"""#!/data/data/com.termux/files/usr/bin/bash
# 🔐 Self-decrypting Bash Script
# 🚫 Obfuscated using Base64

# (Optional) Password check
read -sp "🔑 Enter password: " pass
echo
if [ "$pass" != "1234" ]; then
    echo "❌ Wrong password!"
    exit 1
fi

# 🔽 Decrypt and execute
encoded_script="{encoded}"
echo "$encoded_script" | base64 -d | bash
""")

# ✅ Make output file executable
os.system(f"chmod +x {output_file}")

print(f"\n✅ Encrypted script saved as: {output_file}")
print(f"▶️ Run with: bash {output_file}")
