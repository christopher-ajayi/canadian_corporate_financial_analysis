import json

RAW_FILE = "data/raw/CNQ_companyfacts.json"

with open(RAW_FILE, "r") as f:
    data = json.load(f)


for namespace in data["facts"]:

    print("\nNAMESPACE:", namespace)

    for tag in data["facts"][namespace].keys():

        if (
            "Revenue" in tag
            or "Income" in tag
            or "Profit" in tag
            or "Asset" in tag
            or "Liabil" in tag
            or "Cash" in tag
            or "Equity" in tag
        ):
            print(tag)