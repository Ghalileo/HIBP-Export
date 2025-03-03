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
    else
        print(F"Error for {email}: {response.status_code}, {response.text}")
        return None


