import sys
from pathlib import Path
import requests


PROJECT_ROOT = Path(__file__).resolve().parents[1]

sys.path.append(
    str(PROJECT_ROOT)
)


from config.companies import COMPANIES


HEADERS = {
    "User-Agent": "DaytaScape financial research your_email@example.com"
}


for ticker, company in COMPANIES.items():

    if "cik" not in company:
        print(ticker, "NO CIK")
        continue


    cik = company["cik"].zfill(10)


    url = (
        f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    )


    response = requests.get(
        url,
        headers=HEADERS
    )


    if response.status_code == 200:
        print(
            ticker,
            "AVAILABLE"
        )

    else:
        print(
            ticker,
            "NOT AVAILABLE",
            response.status_code
        )