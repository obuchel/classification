#https://static.data.gouv.fr/resources/donnees-relatives-aux-resultats-des-tests-virologiques-covid-19/20200829-191505/sp-pos-quot-dep-2020-08-29-19h15.csv
#https://www.data.gouv.fr/fr/datasets/r/406c6a23-e283-4300-9484-54e78c8ae675
#https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements-avec-outre-mer.geojson
#https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-resultats-des-tests-virologiques-covid-19-france/#_
#https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-resultats-des-tests-virologiques-covid-19/#_


import json

import numpy as np
import pandas as pd
import os
#from prep_canada_data import stage_latest
#https://cdn.mbta.com/archive/archived_feeds.txt
date_of_analysis='2/5/21'


output_directory = 'output1_france'
os.makedirs(output_directory + '/classification', exist_ok=True)

# Use canned CSV file, so we can compare results to earlier runs of the script.
use_canned_file = False

data0=pd.read_csv("donnees-tests-covid19-labo-quotidien-2020-05-29-19h00.csv",sep=';',engine='python')
print(data0.columns)
df2=data0.groupby(["dep","jour"])["nb_pos"].sum().reset_index()
c1=['2020-05-14','2020-05-15','2020-05-16','2020-05-17','2020-05-18','2020-05-19','2020-05-20','2020-05-21','2020-05-22','2020-05-23','2020-05-24','2020-05-25','2020-05-26','2020-05-27','2020-05-28','2020-05-29']
df3=df2[np.isin(df2['jour'], c1, invert=True)]

#df3['jour']=df3['jour'].dt.date.to_string().replace("\n1","").replace("\n2","")
df4=df3.rename(columns={'dep': 'Combined_Key', 'jour':'jour','nb_pos': 'P'})
#dep;jour;clage_covid;nb_test;nb_pos;nb_test_h;nb_pos_h;nb_test_f;nb_pos_f

if use_canned_file:
    data = pd.read_csv('data/time_series/time_series_covid19_confirmed_US.csv',sep=';', engine='python')
    assert data.columns[-1] == date_of_analysis
else:
    # Original:
    data = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/406c6a23-e283-4300-9484-54e78c8ae675',sep=';',engine="python")
#print(data.columns)
data=data[data['cl_age90']==0]
data["Combined_Key"]=data["dep"]
df_=data.groupby(["Combined_Key","jour"])["P"].sum().reset_index()
df=pd.concat([df4, df_])
#print(df4.columns,df_.columns,df.columns)

e_dataframe = df.set_index("Combined_Key")
ids = df[["Combined_Key"]].to_dict('records')
recs = df["Combined_Key"].to_list()
print(ids)
# stage latest Canada HR-level data for later processing
#latest_ca_df = stage_latest()
#print(latest_ca_df)
#assert latest_ca_df.index.names == ['Combined_Key']
#print(latest_ca_df)

e_dataframe0 = e_dataframe#drop(columns=['dep'])
e_dataframe1 = pd.pivot_table(e_dataframe0, values='P', index=['jour'],columns=['Combined_Key'],aggfunc=np.sum)
print(e_dataframe0)
print(e_dataframe1)

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
#print(e_dataframe1)


if False:
    # show intermediate result and abortthe script right here
    print(e_dataframe1.iloc[10:, :5])
    import sys
    sys.exit(0)

tim = list(e_dataframe0["jour"].unique())
tim.pop(0)
print("time")
print(tim)
ind4 = 0
aar = []
aar1 = []
counties = e_dataframe1.columns[3:]
print("counties")
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

for name in counties:
    values = np.cumsum(e_dataframe1[name].fillna(0))[90:]
    #print(values)
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
            color="darkgreen"

        print(name,color,ratio,recent_mean0,values,tim)    
        with open(output_directory + '/classification/data_counties_'+str(ids[recs.index(name)]["Combined_Key"])+'.json', 'w') as outfile:
            json.dump({"dates":tim2[90:],"max_14": int(max(y5)-min(y5)),"max":np.max(y),"value":y3,"time":tim[90:],"original_values":original_values},outfile)
        #aar.append({"color":color,"province":name.split(",")[0],"country":name.split(",")[1],"id":"new_id_"+str(ind4),"value1":ratio, "dates":tim2,"value":y3})
        aar1.append({"n":name,"id":ids[recs.index(name)]["Combined_Key"],"v":ratio,"c":color,"max":int(max(y5)-min(y5))})
        ind4+=1


# with open('classification/data_counties.json', 'w') as outfile:
#    json.dump(aar,outfile)
aar1[0]["date"]=date_of_analysis
# this file is used by the map
with open(output_directory + '/classification/classification_ids_counties2.json', 'w') as outfile:
    json.dump(aar1, outfile)

