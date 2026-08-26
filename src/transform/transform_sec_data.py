import json
import pandas as pd


RAW_FILE = "data/raw/CNQ_companyfacts.json"


METRICS = {
    "revenue": [
        "Revenue",
        "Revenues"
    ],

    "gross_profit": [
        "GrossProfit"
    ],

    "operating_income": [
        "OperatingIncomeLoss",
        "OperatingIncome"
    ],

    "net_income": [
        "ProfitLoss",
        "NetIncomeLoss",
        "ProfitLossAttributableToOwnersOfParent"
    ],

    "assets": [
        "Assets"
    ],

    "liabilities": [
        "Liabilities"
    ],

    "cash": [
        "CashAndCashEquivalents",
        "CashAndCashEquivalentsAtCarryingValue"
    ],

    "operating_cash_flow": [
        "CashFlowsFromUsedInOperatingActivities",
        "NetCashProvidedByUsedInOperatingActivities"
    ]
}



def get_units(metric):

    units = metric.get("units", {})

    if not units:
        return None, None

    unit_name = next(iter(units))

    return unit_name, units[unit_name]



def find_metric(data, possible_tags):
    """
    Search all available accounting namespaces
    """

    facts = data.get("facts", {})


    for namespace, namespace_data in facts.items():

        for tag in possible_tags:

            if tag in namespace_data:

                return tag, namespace_data[tag]


    return None, None



def valid_filing(item):

    return (
        item.get("form") in [
            "10-K",
            "40-F"
        ]
    )



def extract_metric(data, metric_name, tags):

    tag, metric = find_metric(
        data,
        tags
    )


    if metric is None:

        print(f"{metric_name} not found")

        return pd.DataFrame()



    unit_name, records_source = get_units(metric)


    if records_source is None:

        return pd.DataFrame()



    records = []


    for item in records_source:


        if (
            valid_filing(item)
            and item.get("start") is not None
            and item.get("end") is not None
            and item.get("fp") == "FY"
        ):


            records.append(
                {
                    "metric": metric_name,
                    "source_tag": tag,
                    "period_start": item["start"],
                    "period_end": item["end"],
                    "value": item["val"],
                    "currency": unit_name,
                    "fiscal_year": item["end"][:4],
                    "filing_form": item["form"],
                    "filed_date": item["filed"]
                }
            )


    df = pd.DataFrame(records)


    if df.empty:

        return df



    df["filed_date"] = pd.to_datetime(
        df["filed_date"]
    )


    return (
        df
        .sort_values("filed_date")
        .drop_duplicates(
            subset=[
                "metric",
                "period_end"
            ],
            keep="last"
        )
    )



def extract_instant_metric(data, metric_name, tags):


    tag, metric = find_metric(
        data,
        tags
    )


    if metric is None:

        print(f"{metric_name} not found")

        return pd.DataFrame()



    unit_name, records_source = get_units(metric)


    if records_source is None:

        return pd.DataFrame()



    records = []


    for item in records_source:


        if (
            valid_filing(item)
            and item.get("end") is not None
        ):


            records.append(
                {
                    "metric": metric_name,
                    "source_tag": tag,
                    "period_end": item["end"],
                    "value": item["val"],
                    "currency": unit_name,
                    "fiscal_year": item["end"][:4],
                    "filing_form": item["form"],
                    "filed_date": item["filed"]
                }
            )


    df = pd.DataFrame(records)


    if df.empty:

        return df



    df["filed_date"] = pd.to_datetime(
        df["filed_date"]
    )


    return (
        df
        .sort_values("filed_date")
        .drop_duplicates(
            subset=[
                "metric",
                "period_end"
            ],
            keep="last"
        )
    )



if __name__ == "__main__":


    with open(RAW_FILE, "r") as file:

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



    if all_financials:


        financial_data = pd.concat(
            all_financials,
            ignore_index=True
        )


        print(financial_data.head(20))

        print("\nShape:")
        print(financial_data.shape)

        print("\nMetrics:")
        print(financial_data["metric"].unique())

        print("\nSources:")
        print(financial_data["source_tag"].unique())

        print("\nCurrencies:")
        print(financial_data["currency"].unique())


    else:

        print("No financial data extracted")