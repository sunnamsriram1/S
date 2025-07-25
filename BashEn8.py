import base64
from getpass import getpass

# 🔐 Encrypted & coded by Sriram

def encrypt_bash_file(input_file, output_file, password):
    with open(input_file, 'rb') as f:
        data = f.read()
    encoded_data = base64.b64encode(data).decode()

    with open(output_file, 'w') as f:
        f.write(f'''#!/bin/bash
echo -n "🔑 Enter password: "
read -s input
echo
if [[ "$input" != "{password}" ]]; then
    echo "❌ Incorrect password!"
    exit 1
fi
tmp_file=$(mktemp)
echo '{encoded_data}' | base64 -d > $tmp_file
echo '# 🔐 Encrypted & coded by Sriram' >> $tmp_file
chmod +x $tmp_file
bash $tmp_file
rm $tmp_file
''')

input_file = input("📁 Enter bash file to encrypt (e.g., script.sh): ").strip()
output_file = input("📁 Enter output encrypted file (e.g., script.sh.enc.sh): ").strip()
password = getpass("🔐 Set encryption password: ").strip()

encrypt_bash_file(input_file, output_file, password)
print(f"✅ Encrypted bash saved to: {output_file}")
