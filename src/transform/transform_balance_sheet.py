import pandas as pd


def create_balance_sheet(financial_data, company_id):

    balance = financial_data[
        financial_data["metric"].isin(
            [
                "assets",
                "liabilities",
                "cash",
                "equity",
                "debt"
            ]
        )
    ].copy()


    if balance.empty:
        raise ValueError(
            "No balance sheet metrics found"
        )


    # Convert metrics into columns
    balance = (
        balance
        .pivot_table(
            index=[
                "fiscal_year"
            ],
            columns="metric",
            values="value",
            aggfunc="last"
        )
        .reset_index()
    )


    # Rename columns
    balance = balance.rename(
        columns={
            "assets": "total_assets",
            "liabilities": "total_liabilities",
            "equity": "shareholders_equity",
            "debt": "total_debt",
            "cash": "cash"
        }
    )


    # Ensure required columns exist

    if "total_assets" not in balance.columns:
        balance["total_assets"] = None


    if "total_liabilities" not in balance.columns:
        balance["total_liabilities"] = None


    if "cash" not in balance.columns:
        balance["cash"] = None


    if "shareholders_equity" not in balance.columns:
        balance["shareholders_equity"] = None


    if "total_debt" not in balance.columns:
        balance["total_debt"] = None


    # Add company identifier
    balance["company_id"] = company_id


    # Standard currency field used across all statements
    balance["currency"] = "CAD"


    return balance[
        [
            "company_id",
            "fiscal_year",
            "total_assets",
            "total_liabilities",
            "shareholders_equity",
            "total_debt",
            "cash",
            "currency"
        ]
    ]