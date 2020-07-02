



import json

import numpy as np
import pandas as pd
import os
from prep_canada_data import stage_latest


date_of_analysis='7/1/20'

output_directory = 'output_canada'
os.makedirs(output_directory + '/classification', exist_ok=True)

# Use canned CSV file, so we can compare results to earlier runs of the script.
use_canned_file = False
'''
if use_canned_file:
    data = pd.read_csv('data/time_series/time_series_covid19_confirmed_US.csv')
    assert data.columns[-1] == date_of_analysis
else:
    # Original:
    data = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
'''
dates=["25-01-2020","26-01-2020","27-01-2020","28-01-2020","29-01-2020","30-01-2020","31-01-2020"]
for x in range(2,8):
    if x<10:
        x="0"+str(x)
    for y in range(1,32):
        if y<10:
            y="0"+str(y)
        if str(y)+"-"+str(x)+"-"+"2020" not in ["30-02-2020","31-02-2020","31-04-2020","31-06-2020"]:    
            dates.append(str(y)+"-"+str(x)+"-"+"2020")
dates0=dates[:len(dates)-(31-int(date_of_analysis.split("/")[1]))]        


data={}
with open('canadian_keys.json', 'r') as outfile:
    data=json.load(outfile)
    
#e_dataframe = data.set_index("Combined_Key")
ids = list(data.values())[1:]
recs = list(data.keys())[1:]
#data["Combined_Key"].to_list()
#canadian_keys.json
#print(ids)
#print(recs)


# stage latest Canada HR-level data for later processing
latest_ca_df = stage_latest()
#print(latest_ca_df)
assert latest_ca_df.index.names == ['Combined_Key']

e_dataframe0 = latest_ca_df
print(e_dataframe0)
#e_dataframe.drop(columns=['UID','iso2','iso3','code3','FIPS','Admin2','Province_State','Country_Region','Lat','Long_'])
#print(e_dataframe0.columns.tolist())
df = e_dataframe0.reindex(columns=dates0)
print(df)
e_dataframe1 = df.transpose()
print(e_dataframe1)
#print(df)

#compression_opts = dict(method='zip',archive_name='canadian_data.csv')  
#e_dataframe0.to_csv("canadian_data.csv", sep=',', header=True,encoding='utf-8')  



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
    print(df)

add_day_columns(e_dataframe1)

if False:
    # show intermediate result and abortthe script right here
    print(e_dataframe1.iloc[10:, :5])
    import sys
    sys.exit(0)

tim = dates#list(e_dataframe0.columns)
#tim.pop(0)

ind4 = 0
aar = []
aar1 = []
counties = e_dataframe1.columns[3:]
#print(counties)

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
    values = e_dataframe1[name].cumsum()
    print(name,list(values))
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
    print(pd.DataFrame(y1, columns=["a"]).rolling(window=7).mean()['a'].to_list())
    y3 = pd.DataFrame(y1, columns=["a"]).rolling(window=7).mean()['a'].to_list()[6:]
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
        if max0 > 0:
            ratio = y3[-1] / max0
            recent_mean = int(np.mean(original_values[-10:]))
            color = classify(ratio, recent_mean, threshold)
        else:
            #print(name,y3)
            ratio=0
            color="green"
        if name in recs:    
            with open(output_directory + '/classification/data_counties_'+str(ids[recs.index(name)])+'.json', 'w') as outfile:
                json.dump({"dates":tim2,"max_14":int(max(y5)),"max":int(max(y)),"value":y3,"time":tim,"original_values":original_values},outfile)
            #aar.append({"color":color,"province":name.split(",")[0],"country":name.split(",")[1],"id":"new_id_"+str(ind4),"value1":ratio, "dates":tim2,"value":y3})
            aar1.append({"n":name,"id":ids[recs.index(name)],"v":ratio,"c":color,"max":int(max(y5))})
        ind4+=1


# with open('classification/data_counties.json', 'w') as outfile:
#    json.dump(aar,outfile)
aar1[0]["date"]=date_of_analysis
# this file is used by the map
with open(output_directory + '/classification/classification_ids_provinces2.json', 'w') as outfile:
    json.dump(aar1, outfile)


