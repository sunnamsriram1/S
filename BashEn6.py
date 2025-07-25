import base64
import getpass
import os

print("🔐 Bash File Encryptor (Termux-safe)")
bash_file = input("📄 Enter bash file path: ").strip()
password = getpass.getpass("🔑 Enter password to encrypt: ").strip()

# Read original bash script
with open(bash_file, 'r') as f:
    content = f.read()

# XOR encrypt
enc = ''.join(chr(ord(c) ^ ord(password[i % len(password)])) for i, c in enumerate(content))
b64_enc = base64.b64encode(enc.encode()).decode()

# Output encrypted .enc.py runner file
out_file = bash_file + ".enc.py"
with open(out_file, 'w') as f:
    f.write(f"""#!/usr/bin/env python3
import base64
import getpass
import tempfile
import subprocess
import os

encrypted_data = \"\"\"{b64_enc}\"\"\"

password = getpass.getpass("🔑 Enter password: ").strip()
try:
    decoded = base64.b64decode(encrypted_data).decode()
    decrypted = ''.join(chr(ord(c) ^ ord(password[i % len(password)])) for i, c in enumerate(decoded))
except Exception as e:
    print("❌ Decryption failed!")
    exit(1)

# Write to temporary bash file
with tempfile.NamedTemporaryFile(delete=False, suffix=".sh", mode='w') as tmp:
    tmp.write(decrypted)
    tmp_path = tmp.name

os.chmod(tmp_path, 0o755)
subprocess.run(["bash", tmp_path])
os.remove(tmp_path)
""")

print(f"✅ Encrypted executable Python file saved: {out_file}")
