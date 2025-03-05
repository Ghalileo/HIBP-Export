import requests 
import pandas as pd 
import time
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")

HIBP_API_KEY = api_key
HEADERS = {
    "hibp-api-key": HIBP_API_KEY,
    "User-Agent": "BreachedAccounts",
    "Accept": "application/json"
}

EMAILS = [
    "sample@email.com"

]

CSV_FILENAME = "results.csv"

# Api Call
def email_breach_check(email, max_retries=3, delay=2):
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false"

    for attempt in range(max_retries):
        response = requests.get(url, headers=HEADERS)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 400:
            return[]
        elif response.status_code == 429:
            wait_time = delay * (attempt + 1)
            print(F'Rate Limit Hit! Attempting in {wait_time} seconds...')
            time.sleep(wait_time)
        else:
            print(F"Error for {email}: {response.status_code}, {response.text}")
            return None

# Save Results
def save_response_results(results):
    data = []

    for email, breaches in results.items():
        if breaches:
            for breach in breaches:
                data.append({
                    "Email": email,
                    "Breach Name": breach.get("Name", "N/A"),
                    "Breach Date": breach.get("BreachDate", "Unknown Date"),
                    "Exposed Data": ", ".join(breach.get("DataClasses", ["Unknown"])),
                    "Details": breach.get("Description", "N/A")
                })

        else:
            data.append({
                "Email": email,
                "Breach Name": "No Breach Data",
                "Breach Date": "N/A",
                "Exposed Data": "N/A",
                "Details": "N/A"
            })

    df = pd.DataFrame(data)

    df.to_csv(CSV_FILENAME, index=False, encoding="utf-8")
    print(f"Results saved to {CSV_FILENAME}")

def main():
    results = {}
    for email in EMAILS:
        breaches = email_breach_check(email)
        results[email] = breaches if breaches is not None else []

        if breaches:
            print(f'\n {email} has been compromised in the following breaches:')
            for breach in breaches:
                breach_date = breach.get("BreachDate") if breach.get("BreachDate") else "Unknown Date"
                print(f'    - {breach.get('Name', 'Unknown')}  ({breach.get('BreachDate', 'N/A')})')

        else:
            print(f'    {email} has not been found in any breaches')

        time.sleep(2)

        save_response_results(results)
        print(f"\n Results saved to {CSV_FILENAME}")

if __name__ == "__main__":
    main()
