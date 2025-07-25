#!/usr/bin/env python3
import os
import sys
import glob
import shutil
import hashlib
import hmac
import time
import secrets

# ========================= CONFIG =========================
# Set this to sha256("YourPassword") hash
PASSWORD_HASH = "c2a9b10c14f80c6d3ebff080123b6b11f7e032f46f57ae8c20b9b13d2a2e08a2"  # password: sriram123

MAX_ATTEMPTS = 3
DRY_RUN = False  # ✅ Set to False for real deletion

# Files/folders to destroy (edit as needed)
APP_PATHS = [
    "./secret.txt",
    "./data.db",
    "./my_folder",  # example folder
    "/data/data/com.termux/files/home/secret_folder"  # Termux path
]
# ==========================================================


def sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def constant_time_check(pwd: str) -> bool:
    return hmac.compare_digest(sha256_hex(pwd), PASSWORD_HASH)


def secure_overwrite_file(path: str, passes: int = 1):
    try:
        size = os.path.getsize(path)
        with open(path, "r+b", buffering=0) as f:
            for _ in range(passes):
                f.seek(0)
                f.write(secrets.token_bytes(size))
                f.flush()
                os.fsync(f.fileno())
    except Exception as e:
        print(f"[!] Overwrite failed for {path}: {e}")


def destroy_path(path: str):
    if not os.path.exists(path):
        return

    if os.path.isfile(path):
        if not DRY_RUN:
            secure_overwrite_file(path, passes=2)
            try:
                os.remove(path)
            except Exception as e:
                print(f"[!] Could not remove file {path}: {e}")
        print(f"🗑️  FILE {'(dry-run) ' if DRY_RUN else ''}deleted: {path}")

    elif os.path.isdir(path):
        if not DRY_RUN:
            for root, dirs, files in os.walk(path, topdown=False):
                for name in files:
                    fpath = os.path.join(root, name)
                    try:
                        secure_overwrite_file(fpath, passes=2)
                        os.remove(fpath)
                    except Exception as e:
                        print(f"[!] Could not remove file {fpath}: {e}")
                for name in dirs:
                    dpath = os.path.join(root, name)
                    try:
                        os.rmdir(dpath)
                    except Exception as e:
                        print(f"[!] Could not remove dir {dpath}: {e}")
            try:
                os.rmdir(path)
            except Exception as e:
                print(f"[!] Could not remove dir {path}: {e}")
        print(f"🗑️  DIR  {'(dry-run) ' if DRY_RUN else ''}deleted: {path}")


def self_destruct():
    print("\n💣  Too many wrong attempts! Triggering self-destruct...\n")
    for p in APP_PATHS:
        matched = glob.glob(p)
        if not matched:
            matched = [p]
        for item in matched:
            destroy_path(item)

    print("💥  App dismantled.")
    sys.exit(1)


def ask_password():
    try:
        import getpass
        return getpass.getpass("🔐 Enter Password: ")
    except Exception:
        return input("🔐 Enter Password: ")


def main():
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        pwd = ask_password()
        if constant_time_check(pwd):
            print("✅ Access granted.")
            return

        attempts += 1
        left = MAX_ATTEMPTS - attempts
        print(f"❌ Wrong password. Attempts left: {left}")
        time.sleep(1)

    self_destruct()


if __name__ == "__main__":
    main()
