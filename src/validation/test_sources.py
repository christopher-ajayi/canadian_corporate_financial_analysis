import json
import os


RAW_FOLDER = "data/raw"


for file in os.listdir(RAW_FOLDER):

    if file.endswith(".json"):

        path = os.path.join(RAW_FOLDER, file)

        with open(path, "r") as f:
            data = json.load(f)

        facts = data.get("facts", {})

        print("\n", file)
        print("Available namespaces:")
        print(list(facts.keys()))