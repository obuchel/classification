
#https://imoh.maps.arcgis.com/apps/webappviewer/index.html?id=20ded58639ff4d47a2e2e36af464c36e&locale=he&/

import math
import json
import pandas as pd
import numpy as np
from datetime import date, datetime
from shapely.geometry import shape, Point
from numpyencoder import NumpyEncoder

data1_=pd.read_csv("/Users/olgabuchel/Downloads/data_isr.csv")
data2_=pd.read_csv("/Users/olgabuchel/Downloads/data_isr4.csv")
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
        tt=item[1][list(data0.columns)[1]]#.split("/")
        print(type(item[1]["x"]),float(35.064731016755104))
        if item[1]["x"]==float(35.064731016755104):
            #print("changed")
            x=float(35.07)
        elif item[1]["x"]==float(34.848257303237915):
            x=float(34.9)
            #print("changed")
        elif item[1]["x"]==float(34.84655141830444):
            x=float(34.9)
        else:
            x=item[1]["x"]
            #print("changed")
        point=Point(x,item[1]["y"])
        point1=Point(item[1]["y"],x)
        date=item[1][list(data0.columns)[1]]
        if date not in dates:
            dates.append(date)
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
            data90["features"].append({'type': 'Feature','geometry': {'type': 'Point','coordinates':[x,item[1]["y"]]},'properties': {'name': name_eng0,'value':1}});
        all_data.append([name_eng,name_eng,date])
        ind +=1
#print(dates)        
data3=pd.DataFrame(all_data,columns=["name_eng","name1","date"])
data5=data3.groupby(["name_eng","date"])["name1"].count().reset_index()
#print(sum(data5["name1"].to_list()))
data4=pd.pivot_table(data5, index='name_eng', values="name1",columns='date', aggfunc=np.sum)[["5/10/2020","6/10/2020","7/10/2020","8/10/2020","9/10/2020","10/10/2020","11/10/2020","12/10/2020","13/10/2020","14/10/2020","15/10/2020","16/10/2020","17/10/2020","18/10/2020"]]
#print(data4.columns)

kkeys={}
kkeys1={}
all_vals=[]
for item in data4.iterrows():
    #print(item[0],np.sum([0 if math.isnan(x) else x for x in list(item[1].values)]))
    kkeys[item[0]]=sum([0 if math.isnan(x) else x for x in list(item[1].values)])
    kkeys1[item[0]]=[0 if math.isnan(x) else x for x in list(item[1].values)]
vals=[]
for item in data["features"]:
    if "name" in list(item["properties"].keys()):
        item["properties"]["name"]=item["properties"]["MUN_HEB"]+", "+item["properties"]["MUN_ENG"]
        item["properties"]["value"]=kkeys[item["properties"]["name"]]
        all_vals.append(item["properties"]["value"])
        item["properties"]["values"]=kkeys1[item["properties"]["name"]]
    else:
        item["properties"]["name"]=item["properties"]["MUN_HEB"]+", "+item["properties"]["MUN_ENG"]
        item["properties"]["value"]=0
        item["properties"]["values"]=0
    #print(item["properties"])
    vals.append(item["properties"]["value"])
print(sum(all_vals))    
#print(sum(vals))
with open("municipalities_new.json","w") as fp:
    json.dump(data,fp,separators=(', ', ': '), ensure_ascii=False,cls=NumpyEncoder)
#print(kkeys)

#print(data90)
with open("dots_new.json","w") as fp:
    json.dump(data90,fp,separators=(', ', ': '), ensure_ascii=False,cls=NumpyEncoder)
