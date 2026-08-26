import pandas as pd

from daytascape_db_core.connection import get_db_engine

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

sys.path.append(
    str(PROJECT_ROOT)
)

from config.companies import COMPANIES


def load_income_statement(
    income_statement,
    company_id
):

    engine = get_db_engine()


    # Add company id
    income_statement["company_id"] = company_id


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


    # Ensure matching data types
    income_statement["fiscal_year"] = (
        income_statement["fiscal_year"].astype(int)
    )


    # Attach date_id
    income_statement = income_statement.merge(
        date_lookup,
        on="fiscal_year",
        how="left"
    )


    # Select final columns
    final_df = income_statement[
        [
            "company_id",
            "date_id",
            "revenue",
            "gross_profit",
            "operating_income",
            "net_income",
            "currency"
        ]
    ]


    # Remove rows without date mapping
    final_df = final_df.dropna(
        subset=["date_id"]
    )


    # Load into database
    # Check existing records
    existing = pd.read_sql(
        """
        SELECT
            company_id,
            date_id
        FROM analytics.fact_income_statement
        """,
        engine
    )


    # Keep only new records
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


    if not final_df.empty:

        final_df.to_sql(
            "fact_income_statement",
            engine,
            schema="analytics",
            if_exists="append",
            index=False
        )

        print(
            "Income statement loaded successfully"
        )

    else:

        print(
            "No new income statement records to load"
        )


if __name__ == "__main__":

    import json
    import sys
    from pathlib import Path


    PROJECT_ROOT = Path(__file__).resolve().parents[2]


    sys.path.append(
        str(PROJECT_ROOT / "python" / "transform")
    )


    from transform_sec_data import (
        extract_metric,
        METRICS,
        RAW_FILE
    )


    from transform_financial_statements import (
        create_income_statement
    )


    # Load raw SEC data
    with open(RAW_FILE, "r") as file:
        data = json.load(file)


    all_financials = []


    # Extract metrics
    for metric in METRICS:

        df = extract_metric(
            data,
            metric
        )

        if not df.empty:
            all_financials.append(df)


    financial_data = pd.concat(
        all_financials,
        ignore_index=True
    )


    # Transform
    company = COMPANIES["CNQ"]

    load_income_statement(
        income_statement,
        company["company_id"]
    )


    # Load
    load_income_statement(
        income_statement
    )