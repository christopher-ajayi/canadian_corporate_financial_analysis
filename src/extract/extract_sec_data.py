from pathlib import Path
import requests
import os
import json
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[3]
ENV_PATH = BASE_DIR / ".env"

print("ENV PATH:", ENV_PATH)
print("ENV EXISTS:", ENV_PATH.exists())

load_dotenv(ENV_PATH)

print("SEC USER AGENT:", os.getenv("SEC_USER_AGENT"))


headers = {
    "User-Agent": os.getenv("SEC_USER_AGENT")
}


def extract_company_facts(cik, ticker):
    """
    Extract company facts from SEC API
    """

    url = (
        f"https://data.sec.gov/api/xbrl/companyfacts/"
        f"CIK{cik}.json"
    )

    response = requests.get(
        url,
        headers=headers
    )

    response.raise_for_status()

    data = response.json()

    # Save raw response
    file_path = (
        f"data/raw/{ticker}_companyfacts.json"
    )

    with open(file_path, "w") as file:
        json.dump(
            data,
            file,
            indent=4
        )

    print(
        f"{ticker} extracted successfully"
    )


# Test company
if __name__ == "__main__":

    extract_company_facts(
        cik="0001019034",
        ticker="CNQ"
    )