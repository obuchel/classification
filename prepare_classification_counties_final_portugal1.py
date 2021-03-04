#https://coronavirus-Aportugal-esriportugal.hub.arcgis.com/datasets/covid19-concelhosdiarios/data?showData=true
#https://covid19ireland-geohive.hub.arcgis.com/datasets/d9be85b30d7748b5b7c09450b8aede63_0/data?geometry=-21.779%2C51.133%2C5.160%2C55.710&orderBy=CountyName
#https://services1.arcgis.com/eNO7HHeQ3rUcBllm/arcgis/rest/services/Covid19CountyStatisticsHPSCIreland/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json
import requests
import pandas as pd
import json
import numpy as np
import os
import math
from datetime import datetime
import matplotlib.pyplot as plt
date_of_analysis='3/3/21'

output_directory = 'output_portugal_municipalities'
os.makedirs(output_directory + '/classification', exist_ok=True)
import datetime
'''
source = requests.get("https://opendata.arcgis.com/datasets/d9be85b30d7748b5b7c09450b8aede63_0.geojson").json()
print(source)
dd=[]
for el in source["features"]:
    #print(el["properties"])
    dd.append([el["properties"]['CountyName'],el["properties"]['ConfirmedCovidCases'],str(el["properties"]['TimeStamp']).split(" ")[0],el["properties"]['TimeStamp']])
print(dd)

#str(datetime.datetime.fromtimestamp(el["properties"]['TimeStamp']/1000).isoformat()).split("T")[0].replace("-","/"),
ddata=pd.DataFrame(dd,columns=['CountyName','date','ConfirmedCovidCases','TimeStamp'])

ddata['date'] =pd.to_datetime(ddata.date)
ddata.sort_values(by='date')
print(ddata)
'''

#{'OBJECTID': 2000, 'ORIGID': 24, 'CountyName': 'Westmeath', 'PopulationCensus16': 88770, 'TimeStamp': 1589500800000, 'IGEasting': 238362, 'IGNorthing': 255966, 'Lat': 53.5524, 'Long': -7.4219, 'UGI': 'http://data.geohive.ie/resource/county/2ae19629-144c-13a3-e055-000000000001', 'ConfirmedCovidCases': 655, 'PopulationProportionCovidCases': 737.861890278247, 'ConfirmedCovidDeaths': None, 'ConfirmedCovidRecovered': None, 'Shape__Area': 5208705730.30273, 'Shape__Length': 422669.332716032}
#read json
#https://services1.arcgis.com/eNO7HHeQ3rUcBllm/arcgis/rest/services/Covid19CountyStatisticsHPSCIreland/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json
dates=["10-03-2020","11-03-2020","12-03-2020","13-03-2020","14-03-2020","15-03-2020","16-03-2020","17-03-2020","18-03-2020","19-03-2020","20-03-2020","21-03-2020","22-03-2020","23-03-2020","24-03-2020","25-03-2020","26-03-2020","27-03-2020","28-03-2020","29-03-2020","30-03-2020","31-03-2020"]
for x in range(4,13):
    if x<10:
        x="0"+str(x)
    for y in range(1,32):
        if y<10:
            y="0"+str(y)
        if str(y)+"-"+str(x)+"-"+"2020" not in ["31-04-2020","31-06-2020","31-09-2020","31-11-2020"]:    
            dates.append(str(y)+"-"+str(x)+"-"+"2020")
for x in range(1,4):
    if x<10:
        x="0"+str(x)
    for y in range(1,32):
        if y<10:
            y="0"+str(y)
        if str(y)+"-"+str(x)+"-"+"2021" not in ["29-02-2021","30-02-2021","31-02-2021","31-04-2021","31-06-2021","31-09-2021","31-11-2021"]:
            dates.append(str(y)+"-"+str(x)+"-"+"2021")
            
dates0=dates[:len(dates)-(31-int(date_of_analysis.split("/")[1]))]
print(dates0)
data=pd.read_csv("/Users/olgabuchel/Downloads/data_concelhos_new.csv")
#print(data)
#X          Y  OBJECTID           Concelho  ConfirmadosAcumulado  Recuperados  Obitos                 Data  Dicofre
#OBJECTID  Dico            Concelho  Distrito  ConfirmadosAcumulado_Conc  Recuperados_Conc  Obitos_Conc               Data_Conc  SHAPE_Length  SHAPE_Area
#data            concelho  confirmados_14  confirmados_1  incidencia  ... population_65_mais densidade_populacional  densidade_1 densidade_2 densidade_3
#data,concelho,confirmados_14,confirmados_1,incidencia,incidencia_categoria,incidencia_risco,tendencia_incidencia,tendencia_categoria,tendencia_desc,casos_14dias,ars,distrito,dicofre,area,population,population_65_69,population_70_74,population_75_79,population_80_84,population_85_mais,population_80_mais,population_75_mais,population_70_mais,population_65_mais,densidade_populacional,densidade_1,densidade_2,densidade_3


data["date"]=[str(x).split(" ")[0].split("-")[2]+"-"+str(x).split(" ")[0].split("-")[1]+"-"+str(x).split(" ")[0].split("-")[0] for x in data["data"]]
data["FID"]=data["dicofre"]
#print(data)
data2=data.groupby(['dicofre','date'])["confirmados_1"].sum().reset_index()
df4=data2.pivot(index='dicofre', columns='date', values='confirmados_1')

e_dataframe0=df4
e_dataframe1 = df4.transpose()
#.reindex(columns=dates0).transpose()
#print(e_dataframe1)
ids = data[["FID","concelho"]].to_dict('records')
recs = data["FID"].to_list()
print(recs)
def add_day_columns(df):
    """Add columns Elapsed_days, Decimals, Day_Year to df."""
    dats = list(df.index)
    # print(dats)
    dats2 = []
    decimals = []
    elapsed_days = []
    ind = 22
    for el in dats:
        dats2.append(ind)
        dec = 2020 + (ind / 366)
        elapsed_days.append(ind - 20)
        decimals.append(dec)
        ind += 1
    df.insert(0, "Day_Year", dats2, True)
    df.insert(0, "Decimals", decimals, True)
    df.insert(0, "Elapsed_days", elapsed_days, True)


add_day_columns(e_dataframe1)

print(e_dataframe1)
if False:
    # show intermediate result and abortthe script right here
    print(e_dataframe1.iloc[10:, :5])
    import sys
    sys.exit(0)

tim = list(e_dataframe0.columns)
tim.pop(0)

ind4 = 0
aar = []
aar1 = []
counties = e_dataframe1.columns[3:]


def compute_original_values(values):
    result = []
    ind3 = 0
    for e in values:
        if ind3 < num_rows - 2:
            result.append(int(values[ind3 + 1]) - int(e))
        else:
            result.append(result[-1])
        ind3 += 1
    return result


def interpolate(y):
    if math.isnan(y[len(y)-1])==True:
        y[len(y)-1]=y[len(y)-2]
    ind = 0
    y1 = []
    for el in y:
        if ind >= 1 and ind <= len(y) - 2:
            y0 = (int(y[ind + 1]) - int(y[ind - 1])) / 2
            y1.append(y0)
        elif ind == 0:
            y0 = (int(y[ind + 1]) - int(el)) / 2
            y1.append(y0)
        else:
            y0 = (int(el) - int(y[ind - 1])) / 2
            y1.append(y0)
        ind += 1
    return y1


def classify(ratio, recent_mean, threshold):
    color = None
    if ratio >= 0.79:
        #if recent_mean >= threshold:
        color = "red"
        #else:        
    elif ratio <= 0.04:
        #if recent_mean >= threshold:
        color = "green"
    elif ratio >= 0.4 and ratio < 0.79:
        #if recent_mean >= threshold:
        color = "orange"
    elif ratio > 0.04 and ratio < 0.4:
        color = "yellow"
    else:
        color = "green"
    assert color is not None
    return color

for name in counties:
    #e_dataframe1[name]=e_dataframe1[name].update(pd.Series([e_dataframe1[name][len(e_dataframe1[name])-16],e_dataframe1[name][len(e_dataframe1[name])-16]], index=[len(e_dataframe1[name])-15, 2]))
    values0=[x for x in e_dataframe1[name]]#.replace(len(e_dataframe1[name])-15,e_dataframe1[name][len(e_dataframe1[name])-16])
    values_=[0]
    indd=0
    for en in values0:
        if indd==121:
            en=e_dataframe1[name][len(e_dataframe1[name])-16]
            values_.append(en)
        else:
            values_.append(en)
        indd+=1
    print(values_)
    values=np.cumsum(values_)
    #values=np.cumsum(e_dataframe1[name])
    print(values)
    #print(e_dataframe1[name][len(e_dataframe1[name])-15],len(e_dataframe1[name])-15,e_dataframe1[name][len(e_dataframe1[name])-16])
    #print(values)
    num_rows = len(values)
    y50 = values[-2:]
    y5 = [y - values[-2] for y in y50]
    print(y5)
    y = values
    original_values = values_
    print(original_values)
    #compute_original_values(values)
    x = e_dataframe1[e_dataframe1.columns[0]].to_list()
    y1 = interpolate(y)    
    x2 = ["2020-11-10"]+x#[3:]
    tim2 = tim#[1 : -2]
    y3 = pd.DataFrame(y1, columns=["a"]).rolling(window=1).mean()['a'].to_list()#[3:]
    y3=[x if x>0 else 0 for x in y3]
    ys = y3[-24:]
    xs = x[-29:-5]  # last 24 days
    ind2 = 0
    start = []
    start2 = []
    if int(np.max(y)) > 0:
        vv = [int(x) for x in y if x != min(y3)]
        try:
            start.append(y.index(vv[0]))
        except:
            start.append(0)
            #continue
    else:
        start.append(0)
    threshold = 1
    if len(start) > 0:
        max0 = np.max(y3)
        min0 = np.min(ys)
        #if max0 > 0:
        ratio = y3[-1] / max0
        recent_mean = int(np.mean(original_values[-1:]))   
        #if ratio>0 and recent_mean>0:
        color = classify(ratio, recent_mean, threshold)
        
        #elif ratio==0 and recent_mean==0:
        #    color = "green"
        #else:
        #print(name,y3)
        #ratio=0
        if math.isnan(ratio)==True:
            ratio=0
        #color="green"
        print(recent_mean,ratio,name,color)
        plt.title(name)
        plt.plot(x2,y3,color=color)
        #plt.show()    
        with open(output_directory + '/classification/data_counties_'+str(ids[recs.index(name)]["FID"])+'.json', 'w') as outfile:
            json.dump({"dates":tim2,"max_14":int(max(y5)),"max":int(max(y)),"value":y3,"time":tim,"original_values":original_values[1:]},outfile)
        #aar.append({"color":color,"province":name.split(",")[0],"country":name.split(",")[1],"id":"new_id_"+str(ind4),"value1":ratio, "dates":tim2,"value":y3})
        
        aar1.append({"n":name,"id":ids[recs.index(name)]["FID"],"v":ratio,"c":color,"max":int(max(y5))})
        ind4+=1

plt.show()
# with open('classification/data_counties.json', 'w') as outfile:
#    json.dump(aar,outfile)
aar1[0]["date"]=date_of_analysis
# this file is used by the map
with open(output_directory + '/classification/classification_ids_counties2.json', 'w') as outfile:
    json.dump(aar1, outfile)
