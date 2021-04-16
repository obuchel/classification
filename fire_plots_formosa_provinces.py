import pandas as pd
import json
import geopandas as gpd
data_1=pd.read_csv("/Users/olgabuchel/Downloads/Covid19Casos.csv", index_col=0)
data_=data_1[data_1['clasificacion_resumen']=="Confirmado"]
print(data_["residencia_provincia_nombre"].unique())
data_["ind"]=data_['residencia_departamento_nombre']+", "+data_['residencia_provincia_nombre']
data=data_.groupby(['fecha_diagnostico','ind']).count().reset_index()

print(data.index)
data2=pd.pivot_table(data=data,index="fecha_diagnostico",columns='ind', values='sexo').fillna(0)
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

item0=0
arrs=[]
for item in data2.iterrows():
    it=0
    for el in item[1].values:
        if cols[it]!="data":#,ll[cols[it]])
            if el<0:
                el=0
            #print(cols1[item0])
            #if str(cols[it]).split(", ")[0]!="SIN ESPECIFICAR":
            arrs.append({"x":cols1[item0],"y":str(cols[it]).split(", ")[0],"z":int(el),"p":cols[it].split(", ")[1]})
        it+=1
    item0+=1
print(arrs)    
#print(cols)
#print(cols1)

with open("fire_argentina_provinces.json", "w") as fp:
    json.dump(arrs,fp)

