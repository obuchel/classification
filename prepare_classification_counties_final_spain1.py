#https://raw.githubusercontent.com/montera34/escovid19data/master/data/output/covid19-provincias-spain_consolidated.csv
#https://raw.githubusercontent.com/rejcom/maps/master/okresy_kraje.json czech republic
import pandas as pd
import seaborn as sns
import json
import numpy as np
import os
numb=10
from datetime import date
#date_of_analysis='03/07/21'                                                                                                                                                      
date_of_analysis=date.today().strftime("%m/%d/%y")
print(date_of_analysis)

output_directory="output1_spain"

#date_of_analysis='03/06/21'
#https://github.com/montera34/escovid19data/blob/master/data/output/covid19-ccaa-spain_consolidated.csv
#https://raw.githubusercontent.com/montera34/escovid19data/master/data/output/covid19-ccaa-spain_consolidated.csv

new_keys={'Albacete': 'AB', 'Alicante/Alacant': 'A', 'Almería': 'AL', 'Asturias': 'O', 'Badajoz': 'BA', 'Barcelona': 'B', 'Bizkaia': 'BI', 'Burgos': 'BU', 'Cantabria': 'S', 'Castellón/Castelló': 'CS', 'Ceuta': 'CE', 'Ciudad Real': 'CR', 'Cuenca': 'CU', 'Cáceres': 'CC', 'Cádiz': 'CA', 'Córdoba': 'CO', 'Gipuzkoa': 'SS', 'Girona': 'GI', 'Granada': 'GR', 'Guadalajara': 'GU', 'Huelva': 'H', 'Huesca': 'HU', 'Jaén': 'J', 'León': 'LE', 'Lleida': 'L', 'Lugo': 'LU', 'Madrid': 'M', 'Melilla': 'ML', 'Murcia': 'MU', 'Málaga': 'MA', 'Navarra': 'NA', 'Ourense': 'OR', 'Palencia': 'P', 'Pontevedra': 'PO', 'Salamanca': 'SA', 'Santa Cruz de Tenerife': 'TF', 'Segovia': 'SG', 'Sevilla': 'SE', 'Soria': 'SO', 'Tarragona': 'T', 'Teruel': 'TE', 'Toledo': 'TO', 'Valencia/València': 'V', 'Valladolid': 'VA', 'Zamora': 'ZA', 'Zaragoza': 'Z', 'Araba/Álava': 'VI', 'Ávila': 'AV','Rioja, La':'LO','Palmas, Las':'CN','Balears, Illes':'PM','Coruña, A':'C','País Vasco':'PV'}
#['Albacete' 'Alicante/Alacant' 'Almería' 'Araba/Álava' 'Asturias' 'Ávila''Badajoz' 'Balears, Illes' 'Barcelona' 'Bizkaia' 'Burgos' 'Cáceres''Cádiz' 'Cantabria' 'Castellón/Castelló' 'Ceuta' 'Ciudad Real' 'Córdoba' 'Coruña, A' 'Cuenca' 'Gipuzkoa' 'Girona' 'Granada' 'Guadalajara' 'Huelva' 'Huesca' 'Jaén' 'León' 'Lleida' 'Lugo' 'Madrid' 'Málaga' 'Melilla' 'Murcia' 'Navarra' 'Ourense' 'Palencia' 'Palmas, Las' 'Pontevedra' 'Rioja, La' 'Salamanca' 'Santa Cruz de Tenerife' 'Segovia' 'Sevilla' 'Soria' 'Tarragona' 'Teruel' 'Toledo' 'Valencia/València' 'Valladolid''Zamora' 'Zaragoza']



#'date', 'province', 'ine_code', 'ccaa', 'new_cases', 'PCR', 'TestAc','activos', 'hospitalized', 'intensive_care', 'deceased','cases_accumulated', 'cases_accumulated_PCR', 'recovered', 'num_casos','num_casos_prueba_pcr', 'num_casos_prueba_test_ac','num_casos_prueba_otras', 'num_casos_prueba_desconocida', 'poblacion','cases_per_cienmil', 'intensive_care_per_1000000','deceassed_per_100000', 'hospitalized_per_100000', 'cases_14days','cases_7days', 'cases_PCR_14days', 'cases_PCR_7days', 'daily_cases','daily_cases_avg7', 'daily_cases_PCR', 'daily_cases_PCR_avg7','daily_deaths', 'daily_deaths_inc', 'daily_deaths_avg3','daily_deaths_avg7', 'deaths_last_week', 'source_name', 'source','comments', 'provincia_iso'
#date,provincia_iso,new_cases
'''
data2=pd.read_csv("spain_old.csv")
print(data2)

#data2["provincia_iso"]=data2["province"].map(new_keys)
data2["Combined_Key"]=data2["provincia_iso"]
for i in data2[["provincia_iso","num_casos"]].iterrows():
    print(i[1])


#print(data2["Combined_Key"].unique())
#print(data2)

df_=data2.fillna(0)
#.groupby(["Combined_Key","date"])["cases_accumulated_PCR"].sum().reset_index()
#print(df_)

e_dataframe_ = df_.set_index("Combined_Key")
#ids = df_[["Combined_Key"]].to_dict('records')
#recs = df_["Combined_Key"].to_list()

# stage latest Canada HR-level data for later processing
#latest_ca_df = stage_latest()
#print(latest_ca_df)
#assert latest_ca_df.index.names == ['Combined_Key']
#print(latest_ca_df)

e_dataframe0_ = e_dataframe_#.drop(columns=['dep'])
e_dataframe1_ = pd.pivot_table(e_dataframe0_, values='num_casos', index=['fecha'],columns=['Combined_Key'],aggfunc=np.sum)
#print(e_dataframe0.columns)
final=e_dataframe1_
print(final)
print(final.index)
'''

'''
df11 = data2["date"].str.contains("2020-04-15")
today1 = data2[df11]
dates1=data2["date"].unique()
total1 = today1[["provincia_iso"]]
print(total1)
for date in dates1:
  day1 = data2[ data2["date"].str.contains(date) ]
  #print(day1)
  reports1 = list(day1["new_cases"])
  total1[date]=reports1
'''
#print(total1)
#https://raw.githubusercontent.com/montera34/escovid19data/master/data/output/covid19-provincias-spain_consolidated.csv     
#"date","province","ine_code","ccaa","new_cases" https://cnecovid.isciii.es/covid19/resources/casos_diagnostico_provincia.csv
data=pd.read_csv("https://raw.githubusercontent.com/montera34/escovid19data/master/data/output/covid19-provincias-spain_consolidated.csv",sep=",")         
#data=pd.read_csv("https://cnecovid.isciii.es/covid19/resources/datos_provincias.csv",sep=",")
print(data[data['province']=="Madrid"].columns)
#df=data[data['province']=="Huesca"]['num_casos2'].to_list()
#print(df)
#print(data[data['province']=="Navarra"][['num_casos','num_casos_prueba_pcr', 'num_casos_prueba_test_ac','num_casos_prueba_ag', 'num_casos_prueba_elisa','num_casos_prueba_desconocida', 'num_casos_cum1', 'num_casos2']])
#df.to_csv("madrid.csv")
#print(data[['new_cases',"num_casos"]])

e_dataframe1 = pd.pivot_table(data, values='num_casos2', index=['date'],columns=['province'],aggfunc=np.sum).fillna(0)
print(e_dataframe1['Madrid'])

e_dataframe = e_dataframe1.T
#total.set_index("province")
ids = data[["province"]].to_dict('records')
recs = data["province"].to_list()
print(recs)
print(e_dataframe)

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


#add_day_columns(e_dataframe1)
#print(e_dataframe1)


if False:
    # show intermediate result and abortthe script right here
    print(e_dataframe1.iloc[10:, :5])
    import sys
    sys.exit(0)

tim =data["date"].unique().tolist()#final.index.to_list()+data["fecha"].unique().tolist() 
#tim.pop(0)
print(tim)
ind4 = 0
aar = []
aar1 = []
counties = e_dataframe1.columns.to_list()

print(counties)

def compute_original_values(values):
    result = []
    ind3 = 0
    for e in values:
        if ind3 < num_rows - 1:
            result.append(int(values[ind3 + 1]) - int(e))
        else:
            print("")
            #result.append(result[-1])
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
        if recent_mean > threshold:
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
#counties.append('NA')
#counties.append('ML')
#counties.append('CN')


#print(counties, data["provincia_iso"].unique())

#print(e_dataframe1)
for name in counties:
    try:
        values = np.cumsum(e_dataframe1[name].fillna(0)).tolist()
        #np.cumsum(final[name].to_list()+e_dataframe1[name].to_list()).tolist()#[0]]
        print(values)
    
        #print(len(values))
        last=values[len(values)-1]

        num_rows = len(values)
        y50 = values[-14:]
        y5 = [y - values[-14] for y in y50]
        y = values
        original_values = compute_original_values(values)
        x = e_dataframe1[e_dataframe1.columns[0]]
        y1 = interpolate(y)
        x2 = x[9:]
        tim2 = tim[4 : -5]
        y3 = pd.DataFrame(y1, columns=["a"]).rolling(window=10).mean()['a'].to_list()[9:]
        #print(y3)
        ys = y3[-24:]
        xs = x[-29:-5]  # last 24 days
        ind2 = 0
        start = []
        start2 = []
        #print(y)
        if int(np.max(y)) > 0:
            vv = [int(x) for x in y if x != min(y3)]
            #print(vv)
            start.append(y.index(vv[0]))
        else:
            start.append(0)
        threshold = 1
        if len(start) > 0:
            max0 = np.max(y3)
            min0 = np.min(ys)
            recent_mean0=0
            if max0 > 0:
                ratio = y3[-1] / max0
                recent_mean = int(np.mean(original_values[-14:]))
                recent_mean0 += recent_mean
                #if recent_mean > threshold:
                color = classify(ratio, recent_mean, threshold)
                #else:
                #    color = "green"
            else:
                print(name,y3)
                ratio=0
                color="darkgreen"
            if name!="nan":
                print(name,color,ratio,recent_mean0,values)
                print(len(tim2),len(y3),len(tim[9:]),len(original_values[8:]))
                with open(output_directory + '/classification/data_counties_'+new_keys[str(ids[recs.index(name)]["province"])]+'.json', 'w') as outfile:
                    json.dump({"dates":tim2,"max_14": int(max(y5)-min(y5)),"max":int(np.max(y)),"value":y3,"time":tim[9:],"original_values":original_values[8:]},outfile)
        #aar.append({"color":color,"province":name.split(",")[0],"country":name.split(",")[1],"id":"new_id_"+str(ind4),"value1":ratio, "dates":tim2,"value":y3})
                aar1.append({"n":name,"id":new_keys[ids[recs.index(name)]["province"]],"v":ratio,"c":color,"max":int(max(y5)-min(y5))})
            else:
                with open(output_directory + '/classification/data_counties_NA.json', 'w') as outfile:
                    json.dump({"dates":tim2,"max_14": int(max(y5)-min(y5)),"max":int(np.max(y)),"value":y3,"time":tim[9:],"original_values":original_values[8:]},outfile)
                aar1.append({"n":"NA","id":"NA","v":ratio,"c":color,"max":int(max(y5)-min(y5))})
            ind4+=1
    except:
        continue


# with open('classification/data_counties.json', 'w') as outfile:
#    json.dump(aar,outfile)
aar1[0]["date"]=date_of_analysis
print(aar1)
# this file is used by the map
with open(output_directory + '/classification/classification_ids_counties2.json', 'w') as outfile:
    json.dump(aar1, outfile)

#print(final.index)
#print(tim)


'''
with open("ESP_adm2.json","r") as fp:
    dd=json.load(fp)
    for it in dd["features"]:
        print(it["properties"]["NAME_2"])
'''
