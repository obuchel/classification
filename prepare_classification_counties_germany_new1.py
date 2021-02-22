import numpy as np
import urllib.request as urllib2
import bz2
import pandas as pd
import json
import os
from os import listdir
from os.path import isfile, join
import json
from datetime import datetime
import matplotlib.pyplot as plt

date_of_analysis='02/21/21'

output_directory = 'output_germany'
os.makedirs(output_directory + '/classification', exist_ok=True)

# Use canned CSV file, so we can compare results to earlier runs of the script.
use_canned_file = False


data={}
with open('german_names.json', 'r') as outfile:                                                        
    data=json.load(outfile) 
    print(data)
#import urllib2
#'16077': {'name': 'LK Altenburger Land', 'state': 'Thüringen'

#rename column
#https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rl-crowdsource-by-ags.csv
url = 'https://raw.githubusercontent.com/jgehrcke/covid-19-germany-gae/master/cases-rl-crowdsource-by-ags.csv'
#response = urllib2.urlopen(url)
cr = pd.read_csv(url)
cr["time_iso8601"]=pd.DataFrame([x.split("T")[0] for x in list(cr["time_iso8601"])])
#cr["time_iso8601"].str.split("T")[0]
df=cr.rename(columns={'time_iso8601': 'date'}).drop(['sum_cases'], axis=1)
'''
for el in list(df.columns):
    if el!="date":
        df=df.rename(columns={el: data[el]["state"]+", "+data[el]["name"]})
'''
print(df)

    

e_dataframe0 = df.transpose()
#print(e_dataframe0.index)
#print(e_dataframe0)
#e_dataframe.drop(columns=['UID','iso2','iso3','code3','FIPS','Admin2','Province_State','Country_Region','Lat','Long_'])
#print(e_dataframe0.columns.tolist())
e_dataframe1 =df
#pivoted_table.reindex(columns=dates0)#.transpose()#.set_index('Datenstand')
#print(e_dataframe1,main_df3)
#print(df8)
#print(lOAOAk_keys)
#data=lk_keys

'''
with open('german_keys.json', 'r') as outfile:                                                                                                                                     
    data=json.load(outfile)
print(data)    
'''

#e_dataframe = data.set_index("Combined_Key")
ids = list(df.columns)[1:]
print(ids)
recs = ids


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


tim = list(cr["time_iso8601"])
#[x.replace("0      ","") for x in list(df["date"])]
#0      
tim.pop(0)
print(tim)   

ind4 = 0
aar = []
aar1 = []
counties = list(e_dataframe0.index)[1:]
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
    
    values = e_dataframe1[name].fillna(0).tolist()
    print(name,list(values))
    num_rows = len(values)
    y50 = values[-14:]
    y5 = [y - values[len(values)-14] for y in y50]
    # print(max(y5))                                                                                                                                                                
    y = values
    original_values = compute_original_values(values)
    x = e_dataframe1[e_dataframe1.columns[0]]
    y1 = interpolate(y)
    x2 = x[9:]
    tim2 = tim[4 : -5]
    #print(pd.DataFrame(y1, columns=["a"]).rolling(window=7).mean()['a'].to_list())
    y3 = pd.DataFrame(y1, columns=["a"]).rolling(window=10).mean()['a'].to_list()[9:]
    ys = y3[-24:]
    xs = x[-29:-5]  # last 24 days                                                                                                                                                   
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
    #print(original_values)
    if max0 > 0:
        ratio = y3[-1] / max0
        recent_mean = int(np.mean(original_values[-14:]))
        color = classify(ratio, recent_mean, threshold)
    else:
            #print(name,y3)                                                                                                                                                         
        ratio=0
        color="green"
    print(name)    
    if name in recs:
        print(name,color)
        '''
        plt.title(name)
        plt.plot(x2,y3,color=color)
        plt.show()
        '''
        with open(output_directory + '/classification/data_counties_'+str(ids[recs.index(name)])+'.json', 'w') as outfile:
            json.dump({"dates":tim2,"max_14":int(max(y5)),"max":int(max(y)),"value":y3,"time":tim,"original_values": original_values},outfile)
            #aar.append({"color":color,"province":name.split(",")[0],"country":name.split(",")[1],"id":"new_id_"+str(ind4),"value1":ratio, "dates":tim2,"value":y3})                
        aar1.append({"n":name,"id":ids[recs.index(name)],"v":ratio,"c":color,"max":int(max(y5))})
    else:
        print("not"+name,color)
    ind4+=1


# with open('classification/data_counties.json', 'w') as outfile:                                                                                                                   
#    json.dump(aar,outfile)                                                                                                                                                         
aar1[0]["date"]=date_of_analysis
# this file is used by the map
#print(recs,ids)
print(aar1)
with open(output_directory + '/classification/classification_ids_provinces2.json', 'w') as outfile:
    json.dump(aar1, outfile)    

