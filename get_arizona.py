import json

with open('/Users/olgabuchel/Downloads/Daily COVID-19 Cases by Zip Code.geojson', 'r') as outfile:
    data=json.load(outfile)
    da={"type":"FeatureCollection"}
    da["features"]=[]
    for el in data["features"]:
        if el["properties"]["date"]=="2020-07-05T10:15:00.000":
            print(el["properties"]["date"],el["properties"]["primary_city"])
            da["features"].append(el)
            print(el["properties"])
    with open('Arizona Zip Code1.json', 'w') as outfile0:
        json.dump(da,outfile0)
