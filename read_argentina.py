import json

with open('/Users/olgabuchel/Downloads/ArgentinaCountisAndProvinces (1).json') as json_file:
    data = json.load(json_file)
    for el in data["features"]:
        print(el["properties"])
