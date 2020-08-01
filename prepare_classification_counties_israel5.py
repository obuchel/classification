import json
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import pandas as pd

point = Point(0.5, 0.5)
polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
print(polygon.contains(point))
data=pd.read_csv("/Users/olgabuchel/Downloads/28_day.csv")

kkeys={}
with open("/Users/olgabuchel/Downloads/israel-municipalities-polygons-master/municipalities.geojson","r") as json_file:
    dd=json.load(json_file)
    for el in dd["features"]:
        for item in el["geometry"]["coordinates"]:
            an_array=item
            array_of_tuples = map(tuple, an_array)
            polygon=Polygon(array_of_tuples)
            for it in data.iterrows():
                print(it)
                point=Point(it[1]["x"],it[1]["y"])
                if polygon.contains(point)==True:
                    if el["properties"]["MUN_ENG"] not in list(kkeys.keys()):
                        kkeys[el["properties"]["MUN_ENG"]]=[[it[1]["OBJECTID"],it[1]["x"],it[1]["y"],it[1]["Place"],it[1]["תאריך"]]]
                    else:
                        kkeys[el["properties"]["MUN_ENG"]].append([it[1]["OBJECTID"],it[1]["x"],it[1]["y"],it[1]["Place"],it[1]["תאריך"]])
print(kkeys)
with open("grouped_israelian_cities2.json","w") as json_file:
    json.dump(kkeys,json_file)
