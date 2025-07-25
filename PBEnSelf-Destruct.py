from cryptography.fernet import Fernet
from getpass import getpass
import base64
import os
import datetime
import pytz
from colorama import init, Fore

# Initialize colorama
init(autoreset=True)

# 🔐 Encrypted & coded by Sriram
def generate_key(password: str) -> bytes:
    return base64.urlsafe_b64encode(password.ljust(32, '0')[:32].encode())

def print_banner():
    coded_by = "SUNNAM_SRIRAM_1"
    india_timezone = pytz.timezone('Asia/Kolkata')
    current_time = datetime.datetime.now(india_timezone).strftime("%Y-%m-%d %I:%M:%S %p")
    print(Fore.RED + "═" * 55)
    print(Fore.YELLOW + f"★ Coded by     : {Fore.WHITE}{coded_by}")
    print(Fore.YELLOW + f"★ India Time   : {Fore.GREEN}{current_time}")
    print(Fore.RED + "═" * 55)

def encrypt_file(input_file, output_file, password, runtime="bash", self_destruct=False):
    key = generate_key(password)
    fernet = Fernet(key)

    with open(input_file, 'rb') as f:
        data = f.read()

    encrypted = fernet.encrypt(data).decode()
    destruct_line = 'rm -- "$0"' if self_destruct else ''

    with open(output_file, 'w') as f:
        f.write(f'''#!/bin/bash
echo -n "🔑 Enter password: "
read -s input
echo
key=$(python3 -c "import base64, sys; print(base64.urlsafe_b64encode(sys.argv[1].ljust(32, '0')[:32].encode()).decode())" "$input")
tmp_file=$(mktemp)
if ! python3 -c "from cryptography.fernet import Fernet; import sys; print(Fernet(sys.argv[1].encode()).decrypt(b'{encrypted}').decode())" "$key" > $tmp_file 2>/dev/null; then
    echo "❌ Incorrect password or decryption failed!"
    rm $tmp_file
    exit 1
fi
echo '# 🔐 Encrypted & coded by Sriram' >> $tmp_file
chmod +x $tmp_file
clear
python3 -c "import datetime, pytz; from colorama import init, Fore; init(autoreset=True); print(Fore.RED + '═'*55); print(Fore.YELLOW + '★ Coded by     : ' + Fore.WHITE + 'SUNNAM_SRIRAM_1'); print(Fore.YELLOW + '★ India Time   : ' + Fore.GREEN + datetime.datetime.now(pytz.timezone('Asia/Kolkata')).strftime('%Y-%m-%d %I:%M:%S %p')); print(Fore.RED + '═'*55)"
{runtime} $tmp_file
rm $tmp_file
{destruct_line}
''')

    os.chmod(output_file, 0o755)

# 📥 Inputs
input_file = input("📁 Enter file to encrypt (e.g., script.sh or script.py): ").strip()
output_file = input("📁 Output encrypted file name: ").strip()
password = getpass("🔐 Set encryption password: ").strip()
runtime = "python3" if input_file.endswith(".py") else "bash"
choice = input("💣 Enable self-destruct after run? (y/n): ").strip().lower()
self_destruct = choice == "y"

encrypt_file(input_file, output_file, password, runtime, self_destruct)
print_banner()
print(f"✅ Encrypted saved to: {output_file}")
