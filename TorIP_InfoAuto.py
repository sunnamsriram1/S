import os
import time
import subprocess
import json
import psutil

# Change IP every 60 seconds (you can adjust)
CHANGE_INTERVAL = 60

def get_tor_pid():
    """Find Tor process PID"""
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if 'tor' in proc.info['name']:
            return proc.info['pid']
    return None

def refresh_tor_circuit():
    """Send SIGHUP to Tor process to rotate IP"""
    tor_pid = get_tor_pid()
    if tor_pid:
        os.system(f"kill -HUP {tor_pid}")
        print("🔄 [✓] Tor circuit refreshed.")
    else:
        print("❌ [!] Tor process not found. Please start Tor using `tor`.")

def get_ip_info():
    """Use torsocks + curl to get IP details via ipwhois.app"""
    try:
        result = subprocess.run(
            ['torsocks', 'curl', '-s', 'https://ipwhois.app/json/'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode != 0:
            print(f"❌ Error: {result.stderr.strip()}")
            return None

        data = json.loads(result.stdout)

        if data.get("success", True):
            print("\n🌐 Tor IP Info:")
            print(f"🧭 IP Address : {data.get('ip', 'N/A')}")
            print(f"🌍 Country    : {data.get('country', 'N/A')} ({data.get('country_code', 'N/A')})")
            print(f"🏙  City       : {data.get('city', 'N/A')}")
            print(f"📌 Region     : {data.get('region', 'N/A')}")
            print(f"⏰ Timezone   : {data.get('timezone', 'N/A')}")
            print(f"🏢 ISP        : {data.get('isp', 'N/A')}")
            print(f"🛰  Org        : {data.get('org', 'N/A')}")
            print(f"📶 ASN        : {data.get('asn', 'N/A')}")
        else:
            print(f"⚠️ Failed to fetch IP info: {data.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"❗ Exception: {e}")

def main():
    print("🛡️ Tor IP Auto-Changer + IP Info Script Started...\n")
    try:
        while True:
            get_ip_info()
            refresh_tor_circuit()
            print(f"⏳ Waiting {CHANGE_INTERVAL} sec before next IP change...\n")
            time.sleep(CHANGE_INTERVAL)
    except KeyboardInterrupt:
        print("\n[✋] Script manually stopped by user.")

if __name__ == "__main__":
    main()
