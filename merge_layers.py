

import json
data0={"type":"FeatureCollection"}
data0["features"]=[]
data4={"type":"FeatureCollection"}
data4["features"]=[]
with open("ARG_adm3.json", "r") as read_file:
    data=json.load(read_file)
    #data0=data
    for el in data["features"]:
        if el["properties"]["NAME_2"]!="Mor\u00f3n":
            data0["features"].append(el)

with open("ARG3.geojson", "r") as read_file:
    data2=json.load(read_file)
    for el in data2["features"]:
        #print(el)
        if el["properties"]["sag"]=="ARBA - Gerencia de Servicios Catastrales" and el["properties"]["nam"] in ["Morón","Ituzaingó","Hurlingham"]:
            el["properties"]["NAME_1"]="Buenos Aires"
            el["properties"]["NAME_2"]=el["properties"]["nam"]
            el["properties"]["ID_2"]="abr_"+str(["Morón","Ituzaingó","Hurlingham"].index(el["properties"]["nam"]))
            data0["features"].append(el)
print(data0)

with open("ARG_adm3_1.json", "w") as write_file:
    json.dump(data0,write_file)

'''    
with open("ARG_adm3_3.json", "w") as write_file:
    json.dump(data4,write_file)
'''
