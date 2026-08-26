from pathlib import Path
import sys


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(str(PROJECT_ROOT))


from config.companies import COMPANIES
from python.extract.extract_sec_data import extract_company_facts


NEW_COMPANIES = [
    "BNS",
    "CM",
    "NA",
    "MFC",
    "SLF",
    "EMP.A",
    "MRU",
    "ATD",
    "CTC.A",
    "AC",
    "CAE",
    "BBD.B",
    "GIB.A",
    "OTEX",
    "AEM"
]


for ticker in NEW_COMPANIES:

    print(f"Starting {ticker}...")

    try:

        extract_company_facts(
            cik=COMPANIES[ticker]["cik"],
            ticker=ticker
        )

    except Exception as e:

        print(
            f"{ticker} skipped: {e}"
        )

        continue