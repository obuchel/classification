import pandas as pd
import json
import geopandas as gpd
#data_1=pd.read_csv("../Covid19Casos.csv", index_col=0)
#print(data_1.columns)
#print(data_['clasificacion_resumen'].unique())#'clasificacion', 'clasificacion_resumen'
#data_=data_1[data_1['clasificacion_resumen']=="Confirmado"]
#data=data_.groupby(['fecha_diagnostico','residencia_provincia_nombre']).count().reset_index()
#print(data)
#data2=pd.pivot_table(data=data,index="fecha_diagnostico",columns='residencia_provincia_nombre', values='sexo').fillna(0)
#print(data2)


df = pd.read_csv('https://raw.githubusercontent.com/Sandbird/covid19-Greece/master/regions.csv')#.set_index("Województwo")
kk=df.index
#df=df.T
print(df)
#date               region cases
pivoted_table=pd.pivot_table(data=df,index='date', columns='region', values='cases',margins=False, dropna=False) #aggfunc={'residencia_pais_nombre':'sum'}
#print(pivoted_table)
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
'''
pivoted_table["data"]=pd.to_datetime(pivoted_table.index,format="%Y-%m-%d")
#data            concelho  confirmados_14
data2=pivoted_table
#print(data2)
#print(data2.columns)

print(data2.columns)
for item in data2.columns:
    if item!="data":
        data2[item]=data2[item].diff().fillna(0)
print(data2)


#data.pivot(index='data', columns='concelho', values='confirmados_14')
cols=list(data2.columns)


cols1=list([str(x) for x in data2.index])
kkd0=data2.sum(axis = 0, skipna = True).to_dict()

item0=0
arrs=[]
for item in data2.iterrows():
    it=0
    for el in item[1].values:
        if cols[it]!="data":#,ll[cols[it]])
            print(el)
            if el<0:
                el=0
            arrs.append({"x":cols1[item0],"y":str(cols[it]),"z":int(el),"p":"Greece"})
            print({"x":cols1[item0],"y":str(cols[it]),"z":int(el),"p":"Greece"})
        it+=1
    item0+=1
print(arrs)    
#print(cols)
#print(cols1)
#print(kkd)
#print(kkd0)
with open("fire_Greece.json", "w") as fp:
    json.dump(arrs,fp)

print(data2.columns)

