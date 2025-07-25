import datetime
import pytz
import platform
import requests
import os
import time
import psutil
import speedtest
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Constants
DEVELOPER = "SUNNAM_SRIRAM_1"
GITHUB_URL = "https://github.com/sunnamsriram1"

# Colors
class Colors:
    HEADER = Fore.RED + Style.BRIGHT
    SUBHEADER = Fore.YELLOW + Style.BRIGHT
    TEXT = Fore.WHITE + Style.BRIGHT
    HIGHLIGHT = Fore.GREEN + Style.BRIGHT
    RESET = Style.RESET_ALL

# Divider
def divider(char="=", length=60):
    return Colors.HEADER + char * length + Colors.RESET

# Banner
def show_banner():
    print(divider())
    print(f"{Colors.SUBHEADER}>> Sriram_S".ljust(20) + f"{Colors.TEXT}{GITHUB_URL}")
    print(divider())

# Developer + Time
def show_coder_info():
    india_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    formatted_time = india_time.strftime("%A, %d %B %Y | %I:%M:%S %p")
    print(f"{Colors.SUBHEADER}Coded By      : {Colors.TEXT}{DEVELOPER}")
    print(f"{Colors.HIGHLIGHT}India Time     : {Colors.TEXT}{formatted_time}")
    print(divider("-"))

# Public IP and Country
def get_public_ip_and_country():
    try:
        res = requests.get("https://ipinfo.io/json", timeout=5).json()
        ip = res.get("ip", "Unknown")
        country = res.get("country", "Unknown")
        region = res.get("region", "Unknown")
        city = res.get("city", "Unknown")
        print(f"{Colors.HIGHLIGHT}Public IP      : {Colors.TEXT}{ip}")
        print(f"{Colors.HIGHLIGHT}Location        : {Colors.TEXT}{city}, {region}, {country}")
    except Exception as e:
        print(f"{Colors.HIGHLIGHT}Public IP      : {Colors.RED}Unavailable ({e})")

# Tor IP (if using Tor)
def get_tor_ip():
    try:
        proxies = {
            'http': 'socks5h://127.0.0.1:9050',
            'https': 'socks5h://127.0.0.1:9050'
        }
        tor_ip = requests.get("https://api.ipify.org", proxies=proxies, timeout=10).text
        print(f"{Colors.HIGHLIGHT}Tor IP         : {Colors.TEXT}{tor_ip}")
    except Exception as e:
        print(f"{Colors.HIGHLIGHT}Tor IP         : {Colors.RED}Not Available ({e})")

# OS Info
def show_system_info():
    print(f"{Colors.HIGHLIGHT}OS             : {Colors.TEXT}{platform.system()} {platform.release()}")
    print(f"{Colors.HIGHLIGHT}Architecture   : {Colors.TEXT}{platform.machine()}")
    print(f"{Colors.HIGHLIGHT}Python Version : {Colors.TEXT}{platform.python_version()}")

# Uptime and Load
def show_uptime_and_load():
    try:
        uptime_seconds = float(open('/proc/uptime').read().split()[0])
        uptime_str = time.strftime('%Hh %Mm %Ss', time.gmtime(uptime_seconds))
        load_avg = os.getloadavg()
        print(f"{Colors.HIGHLIGHT}Uptime         : {Colors.TEXT}{uptime_str}")
        print(f"{Colors.HIGHLIGHT}Load Average   : {Colors.TEXT}{load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}")
    except Exception as e:
        print(f"{Colors.HIGHLIGHT}Uptime/Load    : {Colors.RED}Unavailable ({e})")

# RAM Usage
def show_ram_usage():
    mem = psutil.virtual_memory()
    used = mem.used / (1024 ** 3)
    total = mem.total / (1024 ** 3)
    percent = mem.percent
    print(f"{Colors.HIGHLIGHT}RAM Usage      : {Colors.TEXT}{used:.2f} GB / {total:.2f} GB ({percent}%)")

# Disk Info
def show_disk_info():
    disk = psutil.disk_usage('/')
    used = disk.used / (1024 ** 3)
    total = disk.total / (1024 ** 3)
    percent = disk.percent
    print(f"{Colors.HIGHLIGHT}Disk Usage     : {Colors.TEXT}{used:.2f} GB / {total:.2f} GB ({percent}%)")

# Speed Test
def run_speed_test():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()
        download = st.download() / 1_000_000  # Mbps
        upload = st.upload() / 1_000_000
        ping = st.results.ping
        print(f"{Colors.HIGHLIGHT}Download Speed : {Colors.TEXT}{download:.2f} Mbps")
        print(f"{Colors.HIGHLIGHT}Upload Speed   : {Colors.TEXT}{upload:.2f} Mbps")
        print(f"{Colors.HIGHLIGHT}Ping           : {Colors.TEXT}{ping:.0f} ms")
    except Exception as e:
        print(f"{Colors.HIGHLIGHT}Speed Test     : {Colors.RED}Unavailable ({e})")

# Main Runner
def main():
    show_banner()
    show_coder_info()
    show_system_info()
    get_public_ip_and_country()
    get_tor_ip()
    show_uptime_and_load()
    show_ram_usage()
    show_disk_info()
    run_speed_test()
    print(divider())

if __name__ == "__main__":
    main()
