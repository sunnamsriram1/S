#!/data/data/com.termux/files/usr/bin/bash

# Colors
GREEN="\033[1;32m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
BLUE="\033[1;34m"
RESET="\033[0m"
clear
echo -e "${GREEN}🛡️  Advanced SQLMap + Tor Auto Scanner v5.1${RESET}"

# Start Tor if not already
if ! pgrep -x tor > /dev/null; then
    echo -e "${YELLOW}[+] Starting Tor service...${RESET}"
    tor & sleep 5
else
    echo -e "${GREEN}[✓] Tor already running${RESET}"
fi

# Input: URL list file
read -p "📁 URL list file (one per line): " url_file
url_list=()

if [[ -f "$url_file" ]]; then
    mapfile -t url_list < <(grep -v '^\s*$' "$url_file")
else
    echo -e "${RED}[!] File not found: $url_file${RESET}"
    read -p "🌐 Enter a single URL to scan manually: " single_url
    [[ -z "$single_url" ]] && echo -e "${RED}[!] No URL entered. Exiting.${RESET}" && exit 1
    url_list+=("$single_url")
fi

# Extra SQLMap options
read -p "⚙️  Extra SQLMap options (e.g. --dbs --current-user): " extra_options

# Create output dirs
mkdir -p logs
mkdir -p "$HOME/tmp"
csv_file="$HOME/.local/share/sqlmap/output/results-$(date +%d%m%Y_%I%M%p).csv"
echo "Target URL,Place,Parameter,Technique(s),Note(s)" > "$csv_file"

# Tor IP before
echo -ne "➡️  Tor IP before: "
torsocks curl -s https://ifconfig.me | tee "$HOME/tmp/tor_before_ip.txt"

# Loop
total=${#url_list[@]}
success=0
vulnerable=0
failed=0

count=0
for url in "${url_list[@]}"; do
    count=$((count + 1))
    echo -e "\n${YELLOW}[${count}/${total}] Target: ${url}${RESET}"

    log_name=$(echo "$url" | sed 's|https\?://||; s|[/?=&]|_|g')
    log_file="logs/${log_name}.log"

    echo -e "${BLUE}🚀 Running SQLMap...${RESET}"
    start_time=$(date +%s)

    scan_output=$(torsocks python3 sqlmap/sqlmap.py -u "$url" \
        --crawl=2 \
        --random-agent \
        --timeout=30 \
        --delay=3 \
        --retries=2 \
        --batch \
        --output-dir="$HOME/.local/share/sqlmap/output" \
        $extra_options 2>&1)

    echo "$scan_output" | tee "$log_file"
    end_time=$(date +%s)
    duration=$((end_time - start_time))

    # Result Analysis
    if echo "$scan_output" | grep -q "is vulnerable"; then
        echo -e "${GREEN}[✓] Vulnerability Found${RESET}"
        vulnerable=$((vulnerable + 1))
        echo "$url,GET,param,BETU,Vulnerable" >> "$csv_file"
        success=$((success + 1))
    elif echo "$scan_output" | grep -q "parameter\|testing"; then
        echo -e "${BLUE}[✓] Scan Completed${RESET}"
        echo "$url,GET,param,?,Clean" >> "$csv_file"
        success=$((success + 1))
    else
        echo -e "${RED}[✗] Scan Failed or Blocked${RESET}"
        echo "$url,?,?,-,Skipped or Failed" >> "$csv_file"
        failed=$((failed + 1))
    fi

    echo -e "📝 Log saved: ${log_file}"
    echo -ne "⬅️  Tor IP after: "
    torsocks curl -s https://ifconfig.me

    # Rotate Tor & Delay
    echo -e "${BLUE}🔁 Rotating Tor IP...${RESET}"
    pkill -HUP tor
    sleep 5

    if [ "$duration" -lt 20 ]; then
        delay=10
    else
        delay=15
    fi
    echo -e "${YELLOW}⏱️  Sleeping ${delay}s before next scan...${RESET}"
    sleep $delay
    echo "-----------------------------------------------"
done

# 📊 Final Smart Summary
echo -e "\n${GREEN}✅ All scans complete.${RESET}"
echo -e "📄 CSV Summary: ${csv_file}"

echo -e "\n🔔 ${YELLOW}FINAL SUMMARY:${RESET}"
echo -e "🧩 Targets Scanned: ${total}"
echo -e "${GREEN}✅ Successful: ${success}${RESET}"
echo -e "${YELLOW}⚠️ Vulnerable: ${vulnerable}${RESET}"
echo -e "${RED}❌ Skipped or Failed: ${failed}${RESET}"
echo -e "📁 Logs saved to: logs/"
