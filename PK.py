import subprocess

# Read SQLMap commands from file
with open("Pk.txt", "r") as file:
    commands = file.readlines()

# Execute each command
for cmd in commands:
    cmd = cmd.strip()
    if cmd:
        print(f"\n[+] Running: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, check=True, text=True)
        except subprocess.CalledProcessError as e:
            print(f"[!] Error executing: {cmd}\n{e}")
