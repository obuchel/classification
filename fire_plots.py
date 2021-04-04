import pandas as pd
import geopandas as gpd
import json
data=pd.read_csv("https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/data_concelhos_new.csv")
print(data)
#with open("COVID_Concelhos_ConcelhosDetalhes.json","r") as fp:
print(data.columns)
data22=gpd.read_file("COVID_Concelhos_ConcelhosDetalhes.json")
#print(data2)
#Concelho  Distrito

data3=data.copy().merge(data22, left_on='concelho', right_on='Concelho')
data4=data3[["concelho","Distrito"]]
ll=dict(data4.values)

#https://obuchel.github.io/classification/COVID_Concelhos_ConcelhosDetalhes.json
#"Concelho":"ALBERGARIA-A-VELHA","Distrito":"AVEIRO"
#data            concelho  confirmados_14
data["data"]=pd.to_datetime(data["data"],format="%d-%m-%Y")
data2=data.pivot(index='data', columns='concelho', values='confirmados_14')
cols=list(data2.columns)
cols1=list(data["data"].unique())
print(len(cols))
item0=0
arrs=[]
for item in data2.fillna(0).iterrows():
    it=0
    for el in item[1].values:
        arrs.append({"x":str(cols1[item0]),"y":cols[it],"z":int(el),"p":ll[cols[it]]})
        it+=1
    item0+=1
print(arrs)    
print(cols)
print(cols1)
print(data2)
print(ll.values())
with open("fire.json", "w") as fp:
    json.dump(arrs,fp)
