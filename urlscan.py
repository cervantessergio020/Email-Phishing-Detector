import requests
import json
import time
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("URLSCAN_API_KEY")

SCAN_URL = "https://urlscan.io/api/v1/scan/"
RESULT_URL = "https://urlscan.io/api/v1/result/"

def submit_scan(target_url):
    headers = {
        "API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "url": target_url,
        "visibility": "public"  # Change to "private" or "unlisted" if needed
    }

    response = requests.post(SCAN_URL, headers=headers, json=data)
    if response.status_code == 200:
        scan_data = response.json()
        return scan_data.get("uuid"), scan_data.get("api")
    else:
        print("Error submitting scan:", response.json())
        return None, None

def get_scan_result(scan_uuid):
    time.sleep(10)  # Initial wait before polling
    result_endpoint = f"{RESULT_URL}{scan_uuid}/"

    for _ in range(12):  # Retry for up to 1 minute
        response = requests.get(result_endpoint)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            time.sleep(5)  # Wait and retry
        else:
            print("Error fetching scan result:", response.json())
            return None
    return None

def analyze_scan_data(scan_data):
    if not scan_data:
        return {"status": "error", "message": "No scan data retrieved."}

    malicious = scan_data.get("verdicts", {}).get("overall", {}).get("malicious", False)
    blacklisted = scan_data.get("verdicts", {}).get("urlscan", {}).get("score", 0) > 50

    output = {
        "status": "safe" if not malicious and not blacklisted else "unsafe",
        "malicious": malicious,
        "blacklisted": blacklisted,
        "server_info": {
            "ip": scan_data.get("page", {}).get("ip"),
            "asn": scan_data.get("page", {}).get("asn"),
            "country": scan_data.get("page", {}).get("country"),
        }
    }
    return output

def main():
    target_url = input("Enter URL to scan: ").strip()
    scan_uuid, result_api = submit_scan(target_url)

    if scan_uuid:
        print("Scan submitted. UUID:", scan_uuid)
        scan_data = get_scan_result(scan_uuid)

        if scan_data:
            analysis = analyze_scan_data(scan_data)
            print(json.dumps(analysis, indent=4))
        else:
            print("Failed to retrieve scan data.")
    else:
        print("Failed to submit scan.")

if __name__ == "__main__":
    main()
