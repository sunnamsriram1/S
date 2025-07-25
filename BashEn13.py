from cryptography.fernet import Fernet
from getpass import getpass
import base64

# 🔐 Encrypted & coded by Sriram

def generate_key(password: str) -> bytes:
    return base64.urlsafe_b64encode(password.ljust(32, '0')[:32].encode())

def encrypt_file(input_file, output_file, password, runtime):
    key = generate_key(password)
    fernet = Fernet(key)

    with open(input_file, 'rb') as f:
        data = f.read()

    encrypted = fernet.encrypt(data).decode()

    with open(output_file, 'w') as f:
        f.write(f'''#!/data/data/com.termux/files/usr/bin/bash
echo -n "🔑 Enter password: "
read -s input
echo
key=$(python3 -c "import base64, sys; print(base64.urlsafe_b64encode(sys.argv[1].ljust(32, '0')[:32].encode()).decode())" "$input")
tmp_file=$(mktemp)

if ! python3 -c "from cryptography.fernet import Fernet; import sys; print(Fernet(sys.argv[1].encode()).decrypt(b'{encrypted}').decode())" "$key" > $tmp_file 2>/dev/null; then
    echo "❌ Incorrect password or decryption failed!"
    exit 1
fi
echo '# 🔐 Encrypted & coded by Sriram' >> $tmp_file
chmod +x $tmp_file
{runtime} $tmp_file
rm $tmp_file
''')

# 📥 Inputs
input_file = input("📁 Enter file to encrypt (e.g., script.sh or script.py): ").strip()
output_file = input("📁 Output encrypted file name: ").strip()
password = getpass("🔐 Set encryption password: ").strip()

# 🧠 Runtime detect
if input_file.endswith('.py'):
    runtime = "python3"
elif input_file.endswith('.sh'):
    runtime = "bash"
else:
    runtime = input("⚙️ Enter runtime command to execute this file (e.g., bash/python3): ").strip()

encrypt_file(input_file, output_file, password, runtime)
print(f"✅ Encrypted saved to: {output_file}")
