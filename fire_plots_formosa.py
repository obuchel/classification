import pandas as pd
import json
import geopandas as gpd
data_=pd.read_csv("/Users/olgabuchel/Downloads/Covid19Casos.csv", index_col=0)
print(data_["residencia_provincia_nombre"].unique())
data=data_.groupby(['fecha_diagnostico','residencia_provincia_nombre']).count().reset_index()
print(data)
data2=pd.pivot_table(data=data,index="fecha_diagnostico",columns='residencia_provincia_nombre', values='sexo').fillna(0)
print(data2)

'''
pivoted_table=pd.pivot_table(data=df3,index='idd', columns='fecha_diagnostico', values='residencia_pais_nombre',margins=False, dropna=False) #aggfunc={'residencia_pais_nombre':'sum'}    
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
'''
#data.pivot(index='data', columns='concelho', values='confirmados_14')
cols=list(data2.columns)
cols1=list([str(x).split(" ")[0] for x in data2.index])
kkd0=data2.sum(axis = 0, skipna = True).to_dict()
#argentina_population.csv
data13=pd.read_csv("argentina_population.csv")
data13["Population (2013)1"]=[int(str(x).replace(",","")) for x in data13["Population (2013)"].to_list()]
kkd=data13[["Province/District","Population (2013)1"]].set_index("Province/District").to_dict()["Population (2013)1"]

all=[]
for item in list(kkd0.keys()):
    try:
        all.append([item,kkd0[item],kkd[item],kkd0[item]/kkd[item]])
    except:
        all.append([item,kkd0[item],0,kkd0[item]])

dd=pd.DataFrame(all,columns=["Province","Cases","Population","Ratio"])
dd0=dd.sort_values(by=['Ratio'], ascending=False)
print(dd0)
print(dd0["Province"].to_list())
item0=0
arrs=[]
for item in data2.iterrows():
    it=0
    for el in item[1].values:
        if cols[it]!="data":#,ll[cols[it]])
            if el<0:
                el=0
            arrs.append({"x":cols1[item0],"y":str(cols[it]),"z":int(el),"p":"Argentina"})
        it+=1
    item0+=1
#print(arrs)    
#print(cols)
#print(cols1)
print(kkd)
with open("fire_argentina.json", "w") as fp:
    json.dump(arrs,fp)

