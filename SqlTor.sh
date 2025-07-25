#!/data/data/com.termux/files/usr/bin/bash

# Colors
GREEN="\033[1;32m"
RED="\033[1;31m"
RESET="\033[0m"

# IP fetch command
get_tor_ip() {
    echo -ne "${GREEN}[IP] Checking Tor exit IP...${RESET} "
    torsocks curl -s https://ifconfig.me || echo -e "${RED}Failed to fetch IP${RESET}"
}

# Banner
echo -e "${GREEN}🛡️  SQLMap via Tor Auto-Runner with URL List + IP Check + Logging${RESET}"

# Check Tor status
if ! pgrep -x tor > /dev/null; then
    echo -e "${GREEN}[+] Starting Tor service...${RESET}"
    tor & sleep 5
else
    echo -e "${GREEN}[✓] Tor is already running${RESET}"
fi

# Ask for input file
read -p "📁 Enter path to URL list file (one URL per line): " url_file
if [[ ! -f "$url_file" ]]; then
    echo -e "${RED}[!] File not found: $url_file${RESET}"
    exit 1
fi

# Ask for additional SQLMap options
read -p "⚙️  Enter extra SQLMap options (e.g. --dbs --current-user), or press Enter to skip: " extra_options

# Create logs folder
mkdir -p logs

# Loop through each URL
while IFS= read -r target; do
    if [[ -z "$target" ]]; then
        continue
    fi

    echo -e "\n${GREEN}🔍 Target: $target${RESET}"
    
    # Log file name based on URL
    logfile="logs/$(echo $target | sed 's|https\?://||; s|[/?=&]|\_|g').log"

    # Get current Tor IP
    echo -n "➡️  Tor IP before scan: "
    get_tor_ip

    # Run SQLMap
    echo -e "${GREEN}🚀 Launching SQLMap on $target...${RESET}"
    python3 sqlmap/sqlmap.py -u "$target" \
      --tor \
      --tor-type=SOCKS5 \
      --tor-port=9050 \
      --check-tor \
      --proxy="socks5://127.0.0.1:9050" \
      --random-agent \
      --delay=3 \
      --timeout=30 \
      --retries=2 \
      --batch \
      $extra_options | tee "$logfile"

    # Tor IP after scan
    echo -n "⬅️  Tor IP after scan: "
    get_tor_ip

    echo -e "${GREEN}📝 Output saved to: $logfile${RESET}"
    echo -e "----------------------------------------------"

done < "$url_file"
