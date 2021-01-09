



#https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv
import numpy as np
import urllib.request as urllib2
import bz2
import pandas as pd
import json
import os
from os import listdir
from os.path import isfile, join
import json
import csv
import unicodecsv
import matplotlib.pyplot as plt
#onlyfiles = [f for f in listdir('/Users/olgabuchel/Downloads/2020-rki-archive-master/data/0_archived/') if isfile(join('/Users/olgabuchel/Downloads/2020-rki-archive-master/data/0_archived/', f))]
date_of_analysis='01/08/21'
import wget

url = 'https://sisa.msal.gov.ar/datos/descargas/covid-19/files/Covid19Casos.csv'
 
wget.download(url, '../Covid19Casos.csv')



output_directory = 'output_argentina'
os.makedirs(output_directory + '/classification', exist_ok=True)

url='../Covid19Casos.csv'
all_data=[]
kkeys=[]
lists={}
#with open(url, 'r', encoding='utf-16', newline='') as csvfile:
#url='/UOBsers/olgabuchel/Downloads/Covid19Casos-2.csv'
with open(url, 'r', encoding='utf-8', newline='') as csvfile:

    lines = csv.reader(csvfile, delimiter = ',', quotechar = '"')
    ind=0
    for line in lines:
        if ind>0:
            #print(line[len(line)-5])
            if line[len(line)-5]=="Confirmado" and line[len(line)-3]!="":
                all_data.append(line)
            if line[5]+", "+line[6] not in list(lists.values()):
                #if line[len(line)-4]+"_"+line[len(line)-2]=="0":
                #lists[line[len(line)-4]+"_"+line[len(line)-2]]=line[5]+", "+line[6]
                lists[line[len(line)-4]+"_"+line[len(line)-2]]=line[5]+", "+line[6]
                #else:
                #print(lists[line[len(line)-4]+"_"+line[len(line)-2]],line[5]+", "+line[6])
        else:
            kkeys=line
        ind+=1
print(lists)
'''
['id_evento_caso', 'sexo', 'edad', 'edad_años_meses', 'residencia_pais_nombre', 'residencia_provincia_nombre', 'residencia_departamento_nombre', 'carga_provincia_nombre', 'fecha_inicio_sintomas', 'fecha_apertura', 'sepi_apertura', 'fecha_internacion', 'cuidado_intensivo', 'fecha_cui_intensivo', 'fallecido', 'fecha_fallecimiento', 'asistencia_respiratoria_mecanica', 'carga_provincia_id', 'origen_financiamiento', 'Clasificacion', 'clasificacion_resumen', 'residencia_provincia_id', 'fecha_diagnostico', 'residencia_departamento_id', 'ultima_actualizacion']
['672064', 'M', '52', 'Años', 'Argentina', 'Buenos Aires', 'Florencio Varela', 'Buenos Aires', '2020-05-29', '', '44', '', 'NO', '', 'NO', '', 'NO', '06', 'Público', 'Caso Descartado', 'Descartado', '06', '2020-06-01', '274', '2020-06-08']
'''

id='residencia_departamento_id' #'residencia_provincia_id'
idds=[]
for el in all_data:
    idds.append(list(lists.keys())[list(lists.values()).index(el[5]+", "+el[6])])
print(idds)


e_dataframe0=pd.DataFrame(all_data,columns=kkeys)
df=pd.DataFrame(idds,columns=["idd"])
e_dataframe0["idd"]=df['idd']
#e_dataframe0["residencia_provincia_id"].astype(str).add('_').add(e_dataframe0[id]).astype(str)
#print(e_dataframe0['fecha_diagnostico'])
#print(e_dataframe0['fecha_apertura'])
#print(e_dataframe0['sepi_apertura'])
#print(e_dataframe0['residencia_departamento_id'])
df4=e_dataframe0[['idd','residencia_pais_nombre', 'residencia_provincia_nombre','residencia_departamento_nombre', 'carga_provincia_nombre','fecha_diagnostico','fecha_apertura','fecha_inicio_sintomas']]
print(df4)
df0=df4.groupby(['idd','fecha_diagnostico']).count().reset_index()#name="count")
print(df0)
#df0['ID1'] = range(1, len(df0.index)+1)
df2=df0
#.set_index(['fecha_apertura'])
#print(df2)
df3=df2.drop(['residencia_provincia_nombre','residencia_departamento_nombre', 'carga_provincia_nombre','fecha_apertura','fecha_inicio_sintomas'], axis=1)
print(df2['fecha_diagnostico'])
#idx = pd.MultiIndex.from_arrays([df0['ID1'],[df0['residencia_provincia_id'],df0['residencia_pais_nombre'],df0['residencia_provincia_nombre'],df0['fecha_apertura'],df0['count']]])
pivoted_table=pd.pivot_table(data=df3,index='idd', columns='fecha_diagnostico', values='residencia_pais_nombre',margins=False, dropna=False) #aggfunc={'residencia_pais_nombre':'sum'}
e_dataframe1=pivoted_table.transpose()
print(e_dataframe1)
ids = list(lists.keys())
print(ids)
recs = list(lists.values())
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
    #print(df)                                                                                                                                                                                     

add_day_columns(e_dataframe1)

if False:
    # show intermediate result and abortthe script right here                                                                                                                                      
    #print(e_dataframe1.iloc[10:, :5])                                                                                                                                                             
    import sys
    sys.exit(0)


tim = list(pivoted_table.columns)                                                                                                                                                             
#tim.pop(0)                                                                                                                                                                                        

ind4 = 0
aar = []
aar1 = []
counties = e_dataframe1.columns[3:]
print(counties)


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
        if recent_mean >= threshold:
            color = "red"

        else:
            color = "green"
    elif ratio <= 0.1:
        if recent_mean >= threshold:
            color = "yellow"
        else:
            color = "green"
    elif ratio >= 0.4 and ratio < 0.79:
        if recent_mean >= threshold:
            color = "orange"
        else:
            color = "green"
    elif ratio > 0.1 and ratio < 0.4:
        if recent_mean >= threshold:
            color = "yellow"
        else:
            color = "green"
    assert color is not None
    return color

for name in counties:
    values = e_dataframe1[name].fillna(0).cumsum().tolist()
    if name=="120":
        print(values)
    num_rows = len(values)
    y50 = values[-14:]
    y5 = [y - values[-15] for y in y50]
    # print(max(y5))                                                                                                                                                                              
    y = values
    original_values = compute_original_values(values)
    x = e_dataframe1[e_dataframe1.columns[0]]
    y1 = interpolate(y)
    x2 = x[9:]
    tim2 = tim[4 : -5]
    y3 = pd.DataFrame(y1, columns=["a"]).rolling(window=10).mean()['a'].to_list()[9:]
    ys = y3[-24:]
    xs = x[-29:-5]  # last 24 days
    #print(y,y3,x2)
    ind2 = 0
    start = []
    start2 = []
    if int(np.max(y)) > 0:
        vv = [int(x) for x in y if x != min(y3)]
        start.append(y.index(vv[0]))
    else:
        start.append(0)
    #print(start)                                                                                                                                                                                  
    threshold = 1
    #if len(start) > 0:                                                                                                                                                                            
    max0 = np.max(y3)
    min0 = np.min(ys)
    if max0 > 0:
        ratio = y3[-1] / max0
        recent_mean = int(np.mean(original_values[-10:]))
        color = classify(ratio, recent_mean, threshold)
    else:
            #print(name,y3)                                                                                                                                                                       
        ratio=0
        color="green"
    if name in ids:
        print(name,color)
        '''                      
        import matplotlib.pyplot as plt
        plt.title(lists[name])
        plt.plot(x2,y3,color=color)
        plt.savefig(name+".png")
        plt.show()
        '''
        
        #print(name)
        #print(ids.index(name))
        #print(ids[ids.index(name)])
        with open(output_directory + '/classification/data_counties_'+str(ids[ids.index(name)])+'.json', 'w') as outfile:
            print(tim2[14:],y3[14:],original_values[15:],tim[15:])
            json.dump({"dates":tim2[14:],"max_14":int(max(y5)),"max":int(max(y)),"value":y3[14:],"time":tim[15:],"original_values": original_values[15:]},outfile)
            #aar.append({"color":color,"province":name.split(",")[0],"country":name.split(",")[1],"id":"new_id_"+str(ind4),"value1":ratio, "dates":tim2,"value":y3})                
        aar1.append({"n":lists[name],"id":ids[ids.index(name)],"v":ratio,"c":color,"max":int(max(y5))})
    else:
        print("not"+name,color)
    ind4+=1


# with open('classification/data_counties.json', 'w') as outfile:                                                                                                                   
#    json.dump(aar,outfile)                                                                                                                                                         
#aar1[0]["Datenstand"]=date_of_analysis
# this file is used by the map
aar1[0]["date"]=date_of_analysis
with open(output_directory + '/classification/classification_ids_provinces2.json', 'w') as outfile:
    json.dump(aar1, outfile)    
