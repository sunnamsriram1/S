import subprocess
import json

def get_ip_info():
    try:
        # Use torsocks with curl to get IP info JSON
        result = subprocess.run(
            ['torsocks', 'curl', '-s', 'https://ipwhois.app/json/'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            print(f"❌ Error: {result.stderr.strip()}")
            return

        data = json.loads(result.stdout)

        if data.get("success", True):  # Some APIs return "success": False on error
            print("🌐 Tor IP Info:")
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

if __name__ == "__main__":
    get_ip_info()
