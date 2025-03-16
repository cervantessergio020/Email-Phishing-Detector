import openai
import json
import os
from dotenv import load_dotenv
from urlscan import submit_scan, get_scan_result, analyze_scan_data  # Import from urlscan1.py

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_openai_response(prompt, model="gpt-4o-mini"):
    client = openai.OpenAI(api_key=OPENAI_API_KEY)  # Use the hardcoded API key

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

def create_prompt(user_input, url_data=None):
    prompt = (
        "Analyze the likelihood that the following email is a phishing attempt on a scale from 0-100, "
        "where a higher score means it is legitimate and a lower score means it is a phishing attempt.\n\n"
        "Step 1: Evaluate the email structure (urgency, impersonation, lack of personalization, threats, etc.).\n"
        "Step 2: Analyze the URL included in the email, supplementing the analysis with the following scan results:\n"
    )
    
    prompt = prompt + "Email text:\n" + user_input + "\n\n"

    if url_data:
        prompt += (
            f"- URL Scan Status: {url_data.get('status', 'N/A')}\n"
            f"- Malicious: {url_data.get('malicious', False)}\n"
            f"- Blacklisted: {url_data.get('blacklisted', False)}\n"
            f"- IP Address: {url_data.get('server_info', {}).get('ip', 'N/A')}\n"
            f"- ASN: {url_data.get('server_info', {}).get('asn', 'N/A')}\n"
            f"- Country: {url_data.get('server_info', {}).get('country', 'N/A')}\n\n"
        )
    else:
        prompt += "- No URL provided or scan data unavailable.\n\n"

    prompt += (
        "Provide a single numerical score (0-100) on the first line.\n"
        "Follow this with a detailed explanation covering:\n"
        "- Email structure analysis\n"
        "- URL technical details (if available)\n"
        "- Final assessment on whether the email should be trusted or treated as phishing."
    )

    return prompt

def analyze_email(user_email, user_url):
    url_data = None
    
    if user_url:
        print("\nSubmitting URL scan request...")
        scan_uuid, result_api = submit_scan(user_url)  # Submit scan

        if scan_uuid:
            print(f"Scan submitted successfully! UUID: {scan_uuid}")
            scan_data = get_scan_result(scan_uuid)  # Retrieve results
            
            if scan_data:
                url_data = analyze_scan_data(scan_data)  # Extract useful scan info
                print("Scan analysis complete:", json.dumps(url_data, indent=4))
            else:
                print("Failed to retrieve scan data.")
        else:
            print("Failed to submit scan.")

    response = get_openai_response(create_prompt(user_email, url_data))
    return response

if __name__ == "__main__":
    user_email = input("Enter the email text to analyze: ").strip()
    
    user_url = input("Enter URL to scan (or press Enter to skip): ").strip()
    response = analyze_email(user_email, user_url)

    print("\nPhishScan Result:\n", response)  