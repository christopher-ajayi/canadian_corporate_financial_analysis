import requests
import json
from pathlib import Path
import sys


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(
    str(PROJECT_ROOT)
)


from config.companies import COMPANIES


HEADERS = {
    "User-Agent": "database financial research your_email@example.com"
}


RAW_FOLDER = (
    PROJECT_ROOT /
    "data" /
    "raw"
)


RAW_FOLDER.mkdir(
    exist_ok=True
)


def extract_companyfacts(ticker, company):

    cik = company.get("cik")

    if not cik:
        print(
            ticker,
            "NO CIK"
        )
        return


    cik = cik.zfill(10)


    url = (
        f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json"
    )


    print(
        f"Downloading {ticker}..."
    )


    response = requests.get(
        url,
        headers=HEADERS
    )


    if response.status_code != 200:

        print(
            ticker,
            "SKIPPED",
            response.status_code
        )

        return


    data = response.json()


    file_path = (
        RAW_FOLDER /
        f"{ticker}_companyfacts.json"
    )


    with open(
        file_path,
        "w"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


    print(
        ticker,
        "saved"
    )



if __name__ == "__main__":

    for ticker, company in COMPANIES.items():

        extract_companyfacts(
            ticker,
            company
        )
