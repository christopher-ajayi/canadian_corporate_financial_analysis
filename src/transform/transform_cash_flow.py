import pandas as pd


def create_cash_flow(financial_data, company_id):

    cash = financial_data[
        financial_data["metric"].isin(
            [
                "operating_cash_flow",
                "investing_cash_flow",
                "financing_cash_flow"
            ]
        )
    ].copy()


    if cash.empty:
        raise ValueError(
            "No cash flow metrics found"
        )


    cash = (
        cash
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


    cash = cash.rename(
        columns={
            "operating_cash_flow": "operating_cash_flow",
            "investing_cash_flow": "investing_cash_flow",
            "financing_cash_flow": "financing_cash_flow"
        }
    )


    # Ensure required columns exist

    if "operating_cash_flow" not in cash.columns:
        cash["operating_cash_flow"] = None


    if "investing_cash_flow" not in cash.columns:
        cash["investing_cash_flow"] = None


    if "financing_cash_flow" not in cash.columns:
        cash["financing_cash_flow"] = None


    # Calculate free cash flow
    cash["free_cash_flow"] = (
        cash["operating_cash_flow"]
        +
        cash["investing_cash_flow"]
    )


    cash["company_id"] = company_id

    cash["currency"] = "CAD"


    return cash[
        [
            "company_id",
            "fiscal_year",
            "operating_cash_flow",
            "investing_cash_flow",
            "financing_cash_flow",
            "free_cash_flow",
            "currency"
        ]
    ]