#!/usr/bin/env python3
import os
import shutil
import subprocess
from getpass import getpass
from colorama import Fore, Style, init

init(autoreset=True)

# ✅ Settings
GITHUB_USERNAME = "sunnamsriram1"
REPO_NAME = "S"
LOCAL_REPO = "/data/data/com.termux/files/home/GIT_PUSH_S"
SOURCE_FOLDER = "/data/data/com.termux/files/home/S"
REPO_URL = f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

# ✅ Ask for GitHub token securely
token_file = "githubtoken.txt"
if os.path.exists(token_file):
    with open(token_file) as f:
        GITHUB_TOKEN = f.read().strip()
else:
    GITHUB_TOKEN = getpass("🔑 Enter your GitHub Token: ").strip()
    with open(token_file, "w") as f:
        f.write(GITHUB_TOKEN)

AUTH_REPO_URL = f"https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"

# ✅ Clone if not already cloned
if not os.path.exists(LOCAL_REPO):
    print(Fore.CYAN + "🔁 Cloning repository from GitHub...")
    os.system(f"git clone {AUTH_REPO_URL} {LOCAL_REPO}")
else:
    print(Fore.YELLOW + "📁 Repo already cloned. Skipping clone step.")

# ✅ Copy files
print(Fore.CYAN + f"📂 Copying files from {SOURCE_FOLDER} ...")
for file in os.listdir(SOURCE_FOLDER):
    src = os.path.join(SOURCE_FOLDER, file)
    dst = os.path.join(LOCAL_REPO, file)
    try:
        if os.path.isfile(src):
            shutil.copy2(src, dst)
        elif os.path.isdir(src) and file != ".git":
            shutil.copytree(src, dst, dirs_exist_ok=True)
    except Exception as e:
        print(Fore.RED + f"❌ Error copying {file}: {e}")

# ✅ Git commit and push
print(Fore.CYAN + "➕ Adding all files...")
os.chdir(LOCAL_REPO)
os.system("git init")  # ✅ Ensure it's a git repo
os.system("git add .")

print(Fore.CYAN + "📝 Committing changes...")
os.system('git commit -m "🔐 Auto backup from Termux"')

print(Fore.CYAN + "☁️ Pushing to GitHub...")
push_result = os.system(f"git push {AUTH_REPO_URL} main")

if push_result == 0:
    print(Fore.GREEN + "✅ Push successful.")
else:
    print(Fore.RED + "❌ Push failed. Please check your GitHub token or repo name.")
