
#https://www.arcgis.com/sharing/rest/content/items/b5e7488e117749c19881cce45db13f7e/data
#https://data.mesaaz.gov/Fire-and-Medical/Daily-COVID-19-Cases-by-Zip-Code/bcxg-q9nz/data
import json

import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
#from prep_canada_data import stage_latest
date_of_analysis='10/17/20'
#xls = pd.ExcelFile('/home/abuchel/Downloads/Folkhalsomyndigheten_Covid19.xlsx')
df = pd.read_excel(r'/Users/olgabuchel/Downloads/Folkhalsomyndigheten_Covid19 (11).xlsx', sheet_name='Antal per dag region')
print(df)
df["dates"]=[str(l).split("T")[0] for l in list(df.Statistikdatum.unique())]
output_directory = 'output_sweden'
os.makedirs(output_directory + '/classification', exist_ok=True)
'''
# Use canned CSV file, so we can compare results to earlier runs of the script.
use_canned_file = False
data = pd.read_csv('/Users/olgabuchel/Downloads/Daily_COVID-19_Cases_by_Zip_Code.csv')
data["dates"]=data.apply(lambda row: str(row.Date).split(" ")[0], axis=1)
data["Combined_Key"]=data["Zip Code"]
df=data#pd.pivot_table(data,index=["dates"],columns='Combined_Key',values=["Confirmed Cases Count"],aggfunc=np.sum)
df4=df.fillna(0)
print(df4)

Index(['Statistikdatum', 'Totalt_antal_fall', 'Blekinge', 'Dalarna', 'Gotland',
       'Gävleborg', 'Halland', 'Jämtland_Härjedalen', 'Jönköping', 'Kalmar',
       'Kronoberg', 'Norrbotten', 'Skåne', 'Stockholm', 'Sörmland', 'Uppsala',
       'Värmland', 'Västerbotten', 'Västernorrland', 'Västmanland',
       'Västra_Götaland', 'Örebro', 'Östergötland'],
      dtype='object')
'''

e_dataframe0=df.transpose()

#pd.pivot_table(data,index=["dates"],columns='Combined_Key',values=["Confirmed Cases Count"],aggfunc=np.sum)    

#e_dataframe = df4.set_index("Combined_Key")
ids = list(df.columns)[2:-1]
#data[["Combined_Key","Primary City"]].to_dict('records')
recs = list(df.columns)[2:-1]

# stage latest Canada HR-level data for later processing
#latest_ca_df = stage_latest()
#print(latest_ca_df)
#assert latest_ca_df.index.names == ['Combined_Key']
#print(latest_ca_df)

#e_dataframe0 = e_dataframe.drop(columns=['UID','iso2','iso3','code3','FIPS','Admin2','Province_State','Country_Region','Lat','Long_'])
e_dataframe1 = df
#pd.pivot_table(df4,index=["dates"],columns='Combined_Key',values=["Confirmed Cases Count"],aggfunc=np.sum).fillna(0)
#print(e_dataframe1)
#print(ids)
#print(recs)


def add_day_columns(df):
    """Add columns Elapsed_days, Decimals, Day_Year to df."""
    dats = list(df.index)
    #print(dats)
    dats2 = []
    decimals = []
    elapsed_days = []
    ind = 35
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
#print(e_dataframe1)


if False:
    # show intermediate result and abortthe script right here
    print(e_dataframe1.iloc[10:, :5])
    import sys
    sys.exit(0)

tim = list(df.dates)
#print(tim)
tim.pop(0)

ind4 = 0
aar = []
aar1 = []
counties = ids
print(counties)
#e_dataframe1.columns[3:]


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
    name0=name[1]
    values = e_dataframe1[name].cumsum()
    #print(values)        
    num_rows = len(values)
    y50 = values[-14:]
    #print(y50)
    y5 = [y - values[len(values)-14] for y in y50]
    y = values
    original_values = compute_original_values(values)
    x = e_dataframe1[e_dataframe1.columns[0]]
    y1 = interpolate(y)
    x2 = x[9:]
    tim2 = tim[4 : -5]
    #print(tim2)
    y3 = pd.DataFrame(y1, columns=["a"]).rolling(window=10).mean()['a'].to_list()[9:]
    ys = y3[-24:]
    xs = x[-29:-5]  # last 24 days
    ind2 = 0
    start = []
    start2 = []
    if int(np.max(y)) > 0:
        vv = [int(x) for x in y.to_list() if x != min(y3)]
        start.append(y.to_list().index(vv[0]))
    else:
        start.append(0)
    threshold = 1
    if len(start) > 0:
        max0 = np.max(y3)
        min0 = np.min(ys)
        recent_mean0=0
        if max0 > 0:
            ratio = y3[-1] / max0
            recent_mean = int(np.mean(original_values[-11:]))
            recent_mean0 += recent_mean
            #if recent_mean > threshold:
            color = classify(ratio, recent_mean, threshold)
            #else:
            #    color = "green"
        else:
            #print(name,y3)
            ratio=0
            color="darkseagreen"

        print(ids[recs.index(name)],color,ratio,recent_mean0,int(max(y5)))#,str(ids[recs.index(name)]["Combined_Key"]))
        print(y5)
        print(y3)
        print(y)
        '''
        plt.title(name)                                                                                                                                           
        plt.plot(x2,y3,color=color)                                                                                                                                      
        plt.savefig(name+".png")                                                                                                                                         
        plt.show()          
        '''
        try:        
            with open(output_directory + '/classification/data_counties_'+str(ids[recs.index(name)])+'.json', 'w') as outfile:
                json.dump({"dates":tim2,"max_14": int(max(y5)-min(y5)),"max":int(max(y)),"value":y3,"time":tim,"original_values":original_values},outfile)
                #aar.append({"color":color,"province":name.split(",")[0],"country":name.split(",")[1],"id":"new_id_"+str(ind4),"value1":ratio, "dates":tim2,"value":y3})
            aar1.append({"n":name,"id":ids[recs.index(name)],"v":ratio,"c":color,"max":int(max(y5)-min(y5)),"t":int(max(y))})
        except:
            continue
        ind4+=1


# with open('classification/data_counties.json', 'w') as outfile:
#    json.dump(aar,outfile)
print(aar1)
aar1[0]["date"]=date_of_analysis
# this file is used by the map
with open(output_directory + '/classification/classification_ids_counties2.json', 'w') as outfile:
    json.dump(aar1, outfile)


