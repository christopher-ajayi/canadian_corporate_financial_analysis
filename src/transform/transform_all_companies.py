import json
from pathlib import Path
import sys
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(str(PROJECT_ROOT))


from config.companies import COMPANIES

from python.transform.transform_sec_data import (
    extract_metric,
    extract_instant_metric,
    METRICS
)

from python.transform.transform_financial_statements import (
    create_income_statement
)

from python.transform.transform_balance_sheet import (
    create_balance_sheet
)

from python.transform.transform_cash_flow import (
    create_cash_flow
)


RAW_FOLDER = PROJECT_ROOT / "data" / "raw"


all_income = []
all_balance = []
all_cash = []



for ticker, company in COMPANIES.items():

    raw_file = RAW_FOLDER / f"{ticker}_companyfacts.json"


    if not raw_file.exists():

        print(f"{ticker}: file not found")
        continue



    print(f"Processing {ticker}...")


    with open(raw_file, "r") as file:

        data = json.load(file)



    all_financials = []



    for metric_name, tags in METRICS.items():


        df = extract_metric(
            data,
            metric_name,
            tags
        )


        if not df.empty:

            all_financials.append(df)



        if metric_name in [
            "assets",
            "liabilities",
            "cash",
            "equity"
        ]:


            df_instant = extract_instant_metric(
                data,
                metric_name,
                tags
            )


            if not df_instant.empty:

                all_financials.append(df_instant)




    if not all_financials:

        print(f"{ticker}: no financial data")
        continue




    financial_data = pd.concat(
        all_financials,
        ignore_index=True
    )



    print("\nDEBUG METRICS:")
    print(financial_data["metric"].unique())



    income = create_income_statement(
        financial_data,
        company["company_id"]
    )


    balance = create_balance_sheet(
        financial_data,
        company["company_id"]
    )


    cash = create_cash_flow(
        financial_data,
        company["company_id"]
    )



    if not income.empty:

        all_income.append(income)



    if not balance.empty:

        all_balance.append(balance)



    if not cash.empty:

        all_cash.append(cash)




# ============================
# COMBINE RESULTS
# ============================


income_statement = (
    pd.concat(all_income, ignore_index=True)
    if all_income
    else pd.DataFrame()
)



balance_sheet = (
    pd.concat(all_balance, ignore_index=True)
    if all_balance
    else pd.DataFrame()
)



cash_flow = (
    pd.concat(all_cash, ignore_index=True)
    if all_cash
    else pd.DataFrame()
)



# ============================
# ADD STANDARD CURRENCY COLUMN
# ============================

if not income_statement.empty:

    income_statement["currency"] = "CAD"


if not balance_sheet.empty:

    balance_sheet["currency"] = "CAD"


if not cash_flow.empty:

    cash_flow["currency"] = "CAD"



# ============================
# OUTPUT CHECKS
# ============================


print("\n===== INCOME STATEMENT =====")

if not income_statement.empty:

    print(income_statement.head())
    print(income_statement.shape)

else:

    print("No income statement data available")




print("\n===== BALANCE SHEET =====")

if not balance_sheet.empty:

    print(balance_sheet.head())
    print(balance_sheet.shape)

else:

    print("No balance sheet data available")




print("\n===== CASH FLOW =====")

if not cash_flow.empty:

    print(cash_flow.head())
    print(cash_flow.shape)

else:

    print("No cash flow data available")




OUTPUT_FOLDER = PROJECT_ROOT / "data" / "processed"

OUTPUT_FOLDER.mkdir(
    parents=True,
    exist_ok=True
)



income_statement.to_csv(
    OUTPUT_FOLDER / "income_statement.csv",
    index=False
)



balance_sheet.to_csv(
    OUTPUT_FOLDER / "balance_sheet.csv",
    index=False
)



cash_flow.to_csv(
    OUTPUT_FOLDER / "cash_flow.csv",
    index=False
)



print("\nProcessed files saved.")