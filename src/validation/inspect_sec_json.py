import json


file_path = "data/raw/CNQ_companyfacts.json"


with open(file_path, "r") as file:
    data = json.load(file)


revenue = data["facts"]["us-gaap"]["Revenues"]

print(revenue.keys())

print(revenue["units"].keys())

print(revenue["units"]["USD"][0])

for item in revenue["units"]["USD"]:
    if item["form"] == "10-K" and item["fp"] == "FY":
        print(
            item["fy"],
            item["val"],
            item["filed"]
        )
for item in revenue["units"]["USD"]:
    if item["form"] == "10-K" and item["fp"] == "FY":
        print(item)
