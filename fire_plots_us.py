import pandas as pd
import json
import geopandas as gpd
data_=pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv", index_col=0)
#print(data)
data9=data_.T
data=data9.drop(['iso2', 'iso3', 'code3', 'FIPS', 'Admin2', 'Province_State','Country_Region', 'Lat', 'Long_', 'Combined_Key'])
print(data.index)
data0=pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv")
data10=data0[["UID","Province_State"]].reset_index(drop=True)
data11=data0[["UID","Admin2"]].reset_index(drop=True)
ll=dict(data10.values)
ll2=dict(data11.values)
print(ll)
data["data"]=pd.to_datetime(data.index,format="%m/%d/%y")
#data            concelho  confirmados_14
data2=data
print(data2.columns)
for item in data2.columns:
    if item!="data":
        data2[item]=data2[item].diff()
print(data2)
#data.pivot(index='data', columns='concelho', values='confirmados_14')
cols=list(data2.columns)
cols1=list([str(x).split(" ")[0] for x in data2.index])

item0=0
arrs=[]
for item in data2.fillna(0).iterrows():
    it=0
    for el in item[1].values:
        if cols[it]!="data":#,ll[cols[it]])
            if el<0:
                el=0
            arrs.append({"x":str(cols1[item0]),"y":str(ll2[cols[it]]),"z":int(el),"p":ll[cols[it]]})
        it+=1
    item0+=1
print(arrs)    
#print(cols)
#print(cols1)

with open("fire1.json", "w") as fp:
    json.dump(arrs,fp)
