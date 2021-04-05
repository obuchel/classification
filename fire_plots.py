import pandas as pd
import json
import geopandas as gpd
data=pd.read_csv("https://raw.githubusercontent.com/dssg-pt/covid19pt-data/master/data_concelhos_new.csv")
#print(data)
data0=gpd.read_file("COVID_Concelhos_ConcelhosDetalhes.json")
data10=data0[["Concelho","Distrito"]].reset_index(drop=True)
ll=dict(data10.values)
data["data"]=pd.to_datetime(data['data'],format="%d-%m-%Y")
#data            concelho  confirmados_14
data2=data.pivot(index='data', columns='concelho', values='casos_14dias')
cols=list(data2.columns)
cols1=list([str(x).split(" ")[0] for x in data2.index])

item0=0
arrs=[]
for item in data2.fillna(0).iterrows():
    it=0
    for el in item[1].values:
        #print(el)#,ll[cols[it]])
        arrs.append({"x":str(cols1[item0]),"y":cols[it],"z":int(el),"p":ll[cols[it]]})
        it+=1
    item0+=1
print(arrs)    
print(cols)
print(cols1)
print(data[['casos_14dias','confirmados_14']])
with open("fire_x1.json", "w") as fp:
    json.dump(arrs,fp)
