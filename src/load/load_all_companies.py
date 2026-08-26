import sys
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

from database_db_core.connection import get_db_engine


def add_date_id(df, engine):

    dates = pd.read_sql(
        """
        SELECT 
            date_id,
            fiscal_year
        FROM analytics.dim_date
        """,
        engine
    )

    # Match data types
    df["fiscal_year"] = df["fiscal_year"].astype(int)
    dates["fiscal_year"] = dates["fiscal_year"].astype(int)

    df = df.merge(
        dates,
        on="fiscal_year",
        how="left"
    )

    missing_dates = df[df["date_id"].isna()]

    if not missing_dates.empty:
        print("Missing date mappings:")
        print(missing_dates)

    return df



def remove_duplicates(df):

    before = len(df)

    df = (
        df
        .sort_values(
            [
                "company_id",
                "date_id"
            ]
        )
        .drop_duplicates(
            subset=[
                "company_id",
                "date_id"
            ],
            keep="last"
        )
    )

    after = len(df)

    print(
        f"Duplicates removed: {before - after}"
    )

    return df



def load_table(df, table_name, engine):

    df.to_sql(
        table_name,
        engine,
        schema="analytics",
        if_exists="append",
        index=False
    )

    print(
        f"{table_name} loaded successfully"
    )



if __name__ == "__main__":

    from python.transform.transform_all_companies import (
        income_statement,
        balance_sheet,
        cash_flow
    )


    engine = get_db_engine()


    # Add date keys

    income_statement = add_date_id(
        income_statement,
        engine
    )

    balance_sheet = add_date_id(
        balance_sheet,
        engine
    )

    cash_flow = add_date_id(
        cash_flow,
        engine
    )


    # Remove duplicate company/year records

    income_statement = remove_duplicates(
        income_statement
    )

    balance_sheet = remove_duplicates(
        balance_sheet
    )

    cash_flow = remove_duplicates(
        cash_flow
    )


    # Select final columns

    income_statement = income_statement[
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


    balance_sheet = balance_sheet[
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


    cash_flow = cash_flow[
        [
            "company_id",
            "date_id",
            "operating_cash_flow",
            "investing_cash_flow",
            "financing_cash_flow",
            "free_cash_flow",
            "currency"
        ]
    ]


    load_table(
        income_statement,
        "fact_income_statement",
        engine
    )


    load_table(
        balance_sheet,
        "fact_balance_sheet",
        engine
    )


    load_table(
        cash_flow,
        "fact_cash_flow",
        engine
    )