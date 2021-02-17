

import json

import numpy as np
import pandas as pd
import os
#from prep_canada_data import stage_latest
#https://cdn.mbta.com/archive/archived_feeds.txt
date_of_analysis='02/17/21'


output_directory = 'output1_netherlands'
os.makedirs(output_directory + '/classification', exist_ok=True)

# Use canned CSV file, so we can compare results to earlier runs of the script.
use_canned_file = False

#Import data from source
data = pd.read_json('https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_cumulatief.json')
#print(data['Date_of_report'])
kkeys0={}
for item in data.iterrows():
    if item[1]["Municipality_code"]!=None and item[1]["Municipality_code"] not in list(kkeys0.keys()):
        kkeys0[item[1]["Municipality_code"]]=item[1]["Municipality_name"]+", "+item[1]["Province"]

print(kkeys0)
df1 = data['Date_of_report'].str.contains("2020-04-15") 
today = data[df1]

#Getting list of dates over which reports have been made:
dates = data['Date_of_report'].unique()

#scratch
today['Total_reported']

#scratch, good for visuals
data.head()

#reformating file to create JHU-style dataframe
total = today[ ['Province','Municipality_code']]
total["Combined_Key"]=total["Municipality_code"]
total

for date in dates:
    try:
        day = data[ data['Date_of_report'].str.contains(date) ]
        reports = day['Total_reported'].to_list()
        total[date] = reports
    except:
        continue
#total["Combined"]=total["Municipality_name"]+", "+total["Province"]
#scratch
print(total)

kkeys={}
for el in list(total.columns):
    if el not in ['Combined_Key']:
        kkeys[el]=str(el).split(" ")[0]
    else:
        kkeys[el]=el

print(kkeys)        
df1=total.rename(columns=kkeys)
print(df1)


'''

if use_canned_file:
    data = pd.read_csv('data/time_series/time_series_covid19_confirmed_US.csv')
    assert data.columns[-1] == date_of_analysis
else:
    # Original:
    data = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')

print(data)    
'''    
e_dataframe = df1.set_index("Combined_Key")
ids = df1[["Combined_Key"]].to_dict('records')
recs = df1["Combined_Key"].to_list()

# stage latest Canada HR-level data for later processing
#latest_ca_df = stage_latest()
#print(latest_ca_df)
#assert latest_ca_df.index.names == ['Combined_Key']
#print(latest_ca_df)

e_dataframe0 = e_dataframe.drop(columns=['Province','Municipality_code'])
e_dataframe1 = e_dataframe0.transpose()
print(e_dataframe0)



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

tim = list(e_dataframe0.columns)
tim.pop(0)

ind4 = 0
aar = []
aar1 = []
counties = e_dataframe1.columns[3:]


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
    print(name)
    if name!=None:
        values = e_dataframe1[name][90:]
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

            print(name,color,ratio,recent_mean0,int(max(y5)))    
            with open(output_directory + '/classification/data_counties_'+str(ids[recs.index(name)]["Combined_Key"])+'.json', 'w') as outfile:
                json.dump({"dates":tim2[90:],"max_14": int(max(y5)-min(y5)),"max":int(max(y)),"value":y3,"time":tim[90:],"original_values":original_values},outfile)
                #aar.append({"color":color,"province":name.split(",")[0],"country":name.split(",")[1],"id":"new_id_"+str(ind4),"value1":ratio, "dates":tim2,"value":y3})
                aar1.append({"n":kkeys0[name],"id":ids[recs.index(name)]["Combined_Key"],"v":ratio,"c":color,"max":int(max(y5)-min(y5))})
            ind4+=1


# with open('classification/data_counties.json', 'w') as outfile:
#    json.dump(aar,outfile)
aar1[0]["date"]=date_of_analysis
# this file is used by the map
with open(output_directory + '/classification/classification_ids_counties2.json', 'w') as outfile:
    json.dump(aar1, outfile)
