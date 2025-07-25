import requests

def fetch_remote_key():
    try:
        url = "https://raw.githubusercontent.com/sunnamsriram1/unlock-key/main/key.json"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get("remote_password")
        else:
            print("❌ Invalid response:", response.status_code)
            return None
    except Exception as e:
        print("❌ Could not fetch remote key:", str(e))
        return None
