from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]


# transformed output location
OUTPUT_FOLDER = PROJECT_ROOT / "data" / "processed"


income_file = OUTPUT_FOLDER / "income_statement.csv"
balance_file = OUTPUT_FOLDER / "balance_sheet.csv"
cash_file = OUTPUT_FOLDER / "cash_flow.csv"


# Load files
income = pd.read_csv(income_file)
balance = pd.read_csv(balance_file)
cash = pd.read_csv(cash_file)


coverage = pd.DataFrame()


# Companies from all statements
company_ids = set()

for df in [income, balance, cash]:
    if "company_id" in df.columns:
        company_ids.update(df["company_id"].unique())


coverage = pd.DataFrame({
    "company_id": list(company_ids)
})


# Income coverage
coverage["income_statement"] = coverage["company_id"].apply(
    lambda x: "YES" if x in income["company_id"].values else "NO"
)


# Balance coverage
coverage["balance_sheet"] = coverage["company_id"].apply(
    lambda x: "YES" if x in balance["company_id"].values else "NO"
)


# Cash flow coverage
coverage["cash_flow"] = coverage["company_id"].apply(
    lambda x: "YES" if x in cash["company_id"].values else "NO"
)


# Missing income metrics
income_metrics = [
    "revenue",
    "gross_profit",
    "operating_income",
    "net_income"
]


missing_metrics = []


for company_id in coverage["company_id"]:

    company_income = income[
        income["company_id"] == company_id
    ]

    missing = []

    for metric in income_metrics:

        if metric not in company_income.columns:
            missing.append(metric)

        elif company_income[metric].isna().all():
            missing.append(metric)


    missing_metrics.append(
        ", ".join(missing)
        if missing
        else "None"
    )


coverage["missing_income_metrics"] = missing_metrics


# Save report

report_file = (
    PROJECT_ROOT /
    "data" /
    "processed" /
    "company_coverage_report.csv"
)


coverage.to_csv(
    report_file,
    index=False
)


print("========================")
print("COMPANY COVERAGE REPORT")
print("========================")

print(coverage)


print("\nSaved:")
print(report_file)