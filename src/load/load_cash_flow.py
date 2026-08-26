import pandas as pd

from database_db_core.connection import get_db_engine


def load_cash_flow(
    cash_flow,
    company_id
):

    engine = get_db_engine()


    # Add company id
    cash_flow["company_id"] = company_id


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
    cash_flow["fiscal_year"] = (
        cash_flow["fiscal_year"].astype(int)
    )

    date_lookup["fiscal_year"] = (
        date_lookup["fiscal_year"].astype(int)
    )


    # Attach date_id
    cash_flow = cash_flow.merge(
        date_lookup,
        on="fiscal_year",
        how="left"
    )


    # Select final columns
    final_df = cash_flow[
        [
            "company_id",
            "date_id",
            "operating_cash_flow",
            "investing_cash_flow",
            "financing_cash_flow",
            "free_cash_flow"
        ]
    ]


    # Remove duplicate records
    existing = pd.read_sql(
        """
        SELECT
            company_id,
            date_id
        FROM analytics.fact_cash_flow
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


    # Load only new records
    if not final_df.empty:

        final_df.to_sql(
            "fact_cash_flow",
            engine,
            schema="analytics",
            if_exists="append",
            index=False
        )

        print(
            "Cash flow loaded successfully"
        )

    else:

        print(
            "No new cash flow records to load"
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
        RAW_FILE
    )

    from transform_cash_flow import (
        create_cash_flow,
        CASH_FLOW_METRICS
    )

    sys.path.append(
    str(PROJECT_ROOT)
    )

    from config.companies import COMPANIES


    with open(RAW_FILE, "r") as file:
        data = json.load(file)


    all_financials = []


    for metric in CASH_FLOW_METRICS:

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


    cash_flow = create_cash_flow(
        financial_data
    )


    company = COMPANIES["CNQ"]


    load_cash_flow(
        cash_flow,
        company["company_id"]
    )    