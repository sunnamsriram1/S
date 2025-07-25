from base64 import b64encode
import getpass

print("🔐 Bash File Encryptor")
bash_file = input("📄 Enter bash file path (e.g. SqlTor5.1.sh): ").strip()
password = getpass.getpass("🔑 Enter password to encrypt: ").strip()

with open(bash_file, 'r') as f:
    content = f.read()

# XOR Encryption with password
encrypted = ''.join(chr(ord(c) ^ ord(password[i % len(password)])) for i, c in enumerate(content))
b64_encrypted = b64encode(encrypted.encode()).decode()

output_file = bash_file + ".enc.sh"
with open(output_file, 'w') as f:
    f.write(f"""#!/data/data/com.termux/files/usr/bin/bash
echo -n "🔑 Enter password: "
read -s pw
echo
if [ "$pw" != "{password}" ]; then
    echo "❌ Incorrect password!"
    exit 1
fi
decoded=$(echo "{b64_encrypted}" | base64 -d)
decrypted=""
for ((i=0; i<${{#decoded}}; i++)); do
    c=${{decoded:$i:1}}
    k=${{pw:$((i%${{#pw}})):1}}
    decrypted+=$(printf "%b" "$(printf '\\\\x%02x' $(( $(printf "%d" "'$c") ^ $(printf "%d" "'$k") )) )")
done

tmpfile="/data/data/com.termux/files/usr/tmp/tmp_run.sh"
mkdir -p "$(dirname "$tmpfile")"
echo "$decrypted" > "$tmpfile"
chmod +x "$tmpfile"
bash "$tmpfile"
rm -f "$tmpfile"
""")

print(f"✅ Encrypted file saved as: {output_file}")
