import json
import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import text


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(
    str(PROJECT_ROOT)
)

sys.path.append(
    str(PROJECT_ROOT / "python" / "transform")
)


from database_db_core.connection import get_db_engine

from config.companies import COMPANIES

from transform_sec_data import (
    extract_instant_metric
)

from transform_balance_sheet import (
    create_balance_sheet
)


BALANCE_SHEET_METRICS = [
    "Assets",
    "Liabilities",
    "StockholdersEquity",
    "CashAndCashEquivalentsAtCarryingValue",
    "LongTermDebtCurrent",
    "LongTermDebtNoncurrent"
]


def load_balance_sheet(
    balance_sheet,
    company_id
):

    engine = get_db_engine()


    with engine.connect() as conn:

        print(
            conn.execute(
                text(
                    "SELECT current_database();"
                )
            ).scalar()
        )


    balance_sheet["company_id"] = company_id


    # Get date mapping
    date_lookup = pd.read_sql(
        """
        SELECT
            date_id,
            fiscal_year
        FROM analytics.dim_date
        """,
        engine
    )


    balance_sheet["fiscal_year"] = (
        balance_sheet["fiscal_year"]
        .astype(int)
    )

    
    balance_sheet = balance_sheet.merge(
        date_lookup,
        on="fiscal_year",
        how="left"
    )


    final_df = balance_sheet[
        [
            "company_id",
            "date_id",
            "total_assets",
            "total_liabilities",
            "shareholders_equity",
            "cash",
            "total_debt",
            "currency"
        ]
    ]


    # Prevent duplicates
    existing = pd.read_sql(
        """
        SELECT
            company_id,
            date_id
        FROM analytics.fact_balance_sheet
        """,
        engine
    )


    final_df = final_df.merge(
        existing,
        on=[
            "company_id",
            "date_id"
        ],
        how="left",
        indicator=True
    )


    final_df = final_df[
        final_df["_merge"] == "left_only"
    ]


    final_df = final_df.drop(
        columns="_merge"
    )


    if final_df.empty:

        print(
            "No new balance sheet records to load"
        )

    else:

        final_df.to_sql(
            "fact_balance_sheet",
            engine,
            schema="analytics",
            if_exists="append",
            index=False
        )


        print(
            "Balance sheet loaded successfully"
        )



if __name__ == "__main__":


    company = COMPANIES["CNQ"]


    with open(
        company["raw_file"],
        "r"
    ) as file:

        data = json.load(file)



    all_financials = []


    for metric in BALANCE_SHEET_METRICS:


        df = extract_instant_metric(
            data,
            metric
        )


        if not df.empty:

            all_financials.append(df)



    if not all_financials:

        raise ValueError(
            "No balance sheet metrics extracted from SEC data"
        )



    financial_data = pd.concat(
        all_financials,
        ignore_index=True
    )


    print(financial_data.head())

    print(
        financial_data["metric"].unique()
    )


    # Transform
    balance_sheet = create_balance_sheet(
        financial_data
    )


    print(
        balance_sheet.head()
    )


    # Load
    load_balance_sheet(
        balance_sheet,
        company["company_id"]
    )