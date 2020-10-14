import math
import json
import pandas as pd
import numpy as np
from datetime import date, datetime
from shapely.geometry import shape, Point
from numpyencoder import NumpyEncoder

data1_=pd.read_csv("/Users/olgabuchel/Downloads/data_isr.csv")
data2_=pd.read_csv("/Users/olgabuchel/Downloads/data_isr2.csv")
#data2_=pd.read_csv("/Users/olgabuchel/Downloads/data_isr.csv")
#print(data0[["x","y"]])

data0=pd.concat([data1_,data2_]).drop_duplicates()
#data0_.groupby(["x","y",list(data0_.columns)[1]]).count().reset_index()
data90={'type': 'FeatureCollection','features': []};


#print(data0.columns)

all_data=[]
all_names=[]
data={}
dates=[]
with open("municipalities.json","r") as fp:
    data=json.load(fp)
    ind=0
    for item in data0.iterrows():
        point=Point(item[1]["x"],item[1]["y"])
        point1=Point(item[1]["y"],item[1]["x"])
        tt=item[1][list(data0.columns)[1]]#.split("/")
        #print(tt)
        date=item[1][list(data0.columns)[1]]
        #print(date)
        #datetime(2020,int(tt[1]),int(tt[0]))
        if date not in dates:
            dates.append(date)
        #print(item[1])
        name=""
        name_eng=""
        for el in data["features"]:
            polygon = shape(el['geometry'])            
            if polygon.contains(point):
                name += el["properties"]["MUN_HEB"]
                name_eng += el["properties"]["MUN_HEB"]+", "+el["properties"]["MUN_ENG"]
                el["properties"]["name"]=name_eng
            elif polygon.contains(point1):
                #print("YEEESSSSSSSSS")
                name += el["properties"]["MUN_HEB"]
                name_eng += el["properties"]["MUN_HEB"]+", "+el["properties"]["MUN_ENG"]
                el["properties"]["name"]=name_eng
        if name_eng == "":    
            name_eng0=''
            point2=Point(item[1]["y"],item[1]["x"])
            data90["features"].append({'type': 'Feature','geometry': {'type': 'Point','coordinates':[item[1]["x"],item[1]["y"]]},'properties': {'name': name_eng0,'value':1}});
        all_data.append([name_eng,name_eng,date])
        ind +=1
#print(dates)        
data3=pd.DataFrame(all_data,columns=["name_eng","name1","date"])
data5=data3.groupby(["name_eng","date"])["name1"].count().reset_index()
#print(sum(data5["name1"].to_list()))
data4=pd.pivot_table(data5, index='name_eng', values="name1",columns='date', aggfunc=np.sum)[["30/9/2020","1/10/2020","2/10/2020","3/10/2020","4/10/2020","5/10/2020","6/10/2020","7/10/2020","8/10/2020","9/10/2020","10/10/2020","11/10/2020","12/10/2020","13/10/2020"]]
#print(data4.columns)

kkeys={}
kkeys1={}
for item in data4.iterrows():
    print(item[0],np.sum([0 if math.isnan(x) else x for x in list(item[1].values)]))
    kkeys[item[0]]=sum([0 if math.isnan(x) else x for x in list(item[1].values)])
    kkeys1[item[0]]=[0 if math.isnan(x) else x for x in list(item[1].values)]
vals=[]
for item in data["features"]:
    if "name" in list(item["properties"].keys()):
        item["properties"]["name"]=item["properties"]["MUN_HEB"]+", "+item["properties"]["MUN_ENG"]
        item["properties"]["value"]=kkeys[item["properties"]["name"]]
        item["properties"]["values"]=kkeys1[item["properties"]["name"]]
    else:
        item["properties"]["name"]=item["properties"]["MUN_HEB"]+", "+item["properties"]["MUN_ENG"]
        item["properties"]["value"]=0
        item["properties"]["values"]=0
    #print(item["properties"])
    vals.append(item["properties"]["value"])
#print(vals)    
#print(sum(vals))
with open("municipalities_new.json","w") as fp:
    json.dump(data,fp,separators=(', ', ': '), ensure_ascii=False,cls=NumpyEncoder)
#print(kkeys)

print(data90)
with open("dots_new.json","w") as fp:
    json.dump(data90,fp,separators=(', ', ': '), ensure_ascii=False,cls=NumpyEncoder)
