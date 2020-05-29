import json

import numpy as np
import pandas as pd
import os

output_directory = 'output'
os.makedirs(output_directory + '/classification', exist_ok=True)

# Use canned CSV file, so we can compare results to earlier runs of the script.
use_canned_file = True

if use_canned_file:
    data = pd.read_csv('data/time_series/time_series_covid19_confirmed_US.csv')
    assert data.columns[-1] == '5/27/20'
else:
    # Original:
    data = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')

e_dataframe = data.set_index("Combined_Key")
ids = data[["UID", "Combined_Key"]].to_dict('records')
recs = data["Combined_Key"].to_list()

e_dataframe0 = e_dataframe.drop(columns=['UID','iso2','iso3','code3','FIPS','Admin2','Province_State','Country_Region','Lat','Long_'])
e_dataframe1 = e_dataframe0.transpose()


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

if False:
    # show intermediate result and abortthe script right here
    print(e_dataframe1.iloc[10:, :5])
    import sys
    sys.exit(0)

tim = list(e_dataframe0.columns)
tim.pop(0)

ind4 = 0
aar = []
aar1 = []
counties = e_dataframe1.columns[3:]
for name in counties:
    y50 = e_dataframe1[name][len(e_dataframe1[name]) - 20 :]
    y5 = [y - e_dataframe1[name][len(e_dataframe1[name]) - 21] for y in y50]
    # print(max(y5))
    y = e_dataframe1[name]
    v = []
    ind3 = 0
    for e in e_dataframe1[name]:
        if ind3 < len(e_dataframe1[name]) - 2:
            v.append(int(e_dataframe1[name][ind3 + 1]) - int(e))
        else:
            v.append(v[len(v) - 1])
        ind3 += 1
    x = e_dataframe1[e_dataframe1.columns[0]]
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
    x2 = x[9:]
    tim2 = tim[4 : len(tim) - 5]
    y3 = pd.DataFrame(y1, columns=["a"]).rolling(window=10).mean()['a'].to_list()[9:]
    ys = y3[len(y3) - 24 :]
    xs = x[len(x) - 29 : len(x) - 5]  # last 24 days
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
        if max0 > 0:
            ratio = y3[len(y3) - 1] / max0
            if ratio >= 0.79:
                if int(np.mean(v[len(v) - 10 :])) >= threshold:
                    color = "red"
                else:
                    color = "green"
            elif ratio <= 0.1:
                if int(np.mean(v[len(v) - 10 :])) >= threshold:
                    color = "yellow"
                else:
                    color = "green"
            elif ratio >= 0.4 and ratio < 0.79:
                if int(np.mean(v[len(v) - 10 :])) >= threshold:
                    color = "orange"
                else:
                    color = "green"
            elif ratio > 0.1 and ratio < 0.4:
                if int(np.mean(v[len(v) - 10 :])) >= threshold:
                    color = "yellow"
                else:
                  color="green"
            with open('classification/data_counties_'+str(ids[recs.index(name)]["UID"])+'.json', 'w') as outfile:
                json.dump({"dates":tim2,"max_14":int(max(y5)),"max":int(max(y)),"value":y3,"time":tim,"original_values":v},outfile)
            #aar.append({"color":color,"province":name.split(",")[0],"country":name.split(",")[1],"id":"new_id_"+str(ind4),"value1":ratio, "dates":tim2,"value":y3})
            aar1.append({"n":name,"id":ids[recs.index(name)]["UID"],"v":ratio,"c":color,"max":int(max(y5))})
            ind4+=1
        else:
            #print(name,y3)
            ratio=0
            color="green"
            with open(output_directory + '/classification/data_counties_'+str(ids[recs.index(name)]["UID"])+'.json', 'w') as outfile:
                json.dump({"dates":tim2,"max_14":int(max(y5)),"max":int(max(y)),"value":y3,"time":tim,"original_values":v},outfile)
            #aar.append({"color":color,"province":name.split(",")[0],"country":name.split(",")[1],"id":"new_id_"+str(ind4),"value1":ratio, "dates":tim2,"value":y3})
            aar1.append({"n":name,"id":ids[recs.index(name)]["UID"],"v":ratio,"c":color,"max":int(max(y5))})
            ind4+=1


# with open('classification/data_counties.json', 'w') as outfile:
#    json.dump(aar,outfile)

# this file is used by the map
with open(output_directory + '/classification/classification_ids_counties2.json', 'w') as outfile:
    json.dump(aar1, outfile)
