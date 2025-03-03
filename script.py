import requests 
import pandas as pd 
import time
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")

HIBP_API_KEY = API_KEY
HEADERS = {
    "hibp-api-key": HIBP_API_KEY,
    "User-Agent": "BreachedAccounts",
    "Accept": "application/json"
}

EMAILS = [
    "sample@email.com"

]

CSV_FILENAME = "results.csv"

def email_breach_check(email):
    url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false"

    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 400:
        return[]
    else:
        print(F"Error for {email}: {response.status_code}, {response.text}")
        return None

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
