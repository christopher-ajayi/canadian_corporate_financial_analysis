import pandas as pd


def create_income_statement(financial_data, company_id):

    income_metrics = [
        "revenue",
        "gross_profit",
        "operating_income",
        "net_income"
    ]

    df = financial_data[
        financial_data["metric"].isin(income_metrics)
    ].copy()


    if df.empty:
        return pd.DataFrame()


    df = df[
        [
            "metric",
            "value",
            "fiscal_year"
        ]
    ]


    df = df.pivot_table(
        index="fiscal_year",
        columns="metric",
        values="value",
        aggfunc="first"
    ).reset_index()


    df["company_id"] = company_id


    # Ensure missing columns exist
    for col in [
        "revenue",
        "gross_profit",
        "operating_income",
        "net_income"
    ]:
        if col not in df.columns:
            df[col] = None


    return df[
        [
            "company_id",
            "fiscal_year",
            "revenue",
            "gross_profit",
            "operating_income",
            "net_income"
        ]
    ]