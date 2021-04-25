


import json
import numpy as np
import pandas as pd
import os
from datetime import date
date_of_analysis=date.today().strftime("%m/%d/%y")
print(date_of_analysis)

output_directory = 'output'
os.makedirs(output_directory + '/classification', exist_ok=True)
# Use canned CSV file, so we can compare results to earlier runs of the script.
use_canned_file = False
pop=pd.read_csv('US_population.csv').set_index("State")
population=pop.to_dict("index")
if use_canned_file:
    data = pd.read_csv('data/time_series/time_series_covid19_confirmed_US.csv')
    assert data.columns[-1] == date_of_analysis
else:
    # Original:
    #data = pd.read_csv('data/time_series/time_series_covid19_confirmed_US.csv')
    data0 = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')
#date          state  fips   cases  deaths 2020-01-21
#data0["date"]=pd.to_datetime(data0["date"],format="%Y-%m-%d")
data=data0.drop(columns=['Combined_Key','iso2','iso3','code3','FIPS','Admin2','Province_State','Country_Region','Lat','Long_']).set_index("UID")

#pd.pivot_table(data0, values='cases', index=["date"],columns=['state'], aggfunc=np.sum).fillna(0)

#tim=list(data.columns)

e_dataframe = data
#pd.pivot_table(data0, values='cases', index=["Combined_Key"],columns=['date'], aggfunc=np.sum).fillna(0)
#data_.reset_index()
ids = list(data.index)
#[["Province_State"]].to_dict('records')
recs = ids
#data["Province_State"].to_list()
print(recs)


e_dataframe0 = e_dataframe#.drop(columns=['UID','iso2','iso3','code3','FIPS','Admin2','Combined_Key','Country_Region','Lat','Long_'])
e_dataframe1=e_dataframe0.transpose()
e_dataframe1.columns=recs
date_range = pd.date_range('01/19/2020',periods=66,freq='W')
#df = pd.DataFrame({'week': date_range})
e_dataframe1["date"]=pd.to_datetime(list(e_dataframe1.index))
e_dataframe1["week_start"] = e_dataframe1["date"] - pd.TimedeltaIndex((e_dataframe1["date"].dt.dayofweek+1+7)%7, "D")
e_dataframe1["week_start"]=e_dataframe1["week_start"].astype(str)
#[i for i in range(len(lst)) if lst[i]=='Alice']
#e_dataframe1["week_start"]=[e_dataframe1["week_start"].to_list()[i]+" w"+str(i) for i in range(len(e_dataframe1["week_start"].to_list()))]
e_dataframe1 = e_dataframe1.groupby('week_start').sum().reset_index()
print(e_dataframe1)
#e_dataframe1["date"] = pd.to_datetime(e_dataframe1.index) - pd.to_timedelta(7, unit='d')

#print(e_dataframe1)


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

#tim = list(e_dataframe0.columns)
#tim.pop(0)

ind4 = 0
aar = []
aar1 = []
counties = recs
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

def classify1(y3, recent_mean,name):
    N0 = 10
    F0=0.5
    F1=0.2
    current_average=recent_mean
    #np.mean(v[-14:])
    if (current_average<F0*N0) or (current_average< N0 and current_average< np.max(y3)*F0):
        #print("green",name)
        color="green"
    elif (current_average<1.5*N0 and current_average<np.max(y3)*F0) or (current_average<np.max(y3)*F1):
        #print("yellow",name)
        color="yellow"
    else:
        #print("red",name)
        color="red"
    return color



all_states0={}
all_states={}
all_dates=list(e_dataframe1["week_start"].unique())
#print(all_dates)

all_dates0=list(e_dataframe.columns)

for item in all_dates[2:]:
    #print(item)
    rm=all_dates[all_dates.index(item):]
    #print(e_dataframe0.drop(columns=rm))                                                                                                                                             print(rm)
    #e_dataframe1 = e_dataframe0.drop(columns=rm).transpose()
    st=list(e_dataframe1["week_start"]).index(item)

    dr=[e_dataframe1.index[i] for i in range(len(all_dates)) if i>=st]
    e_dataframe1_=e_dataframe1.drop(dr)
    #print(e_dataframe1_)    
    #modDfObj = dfObj.drop([dfObj.index[0] , dfObj.index[1]])
    tim=[all_dates[i] for i in range(len(all_dates)) if i<=st]
    #e_dataframe1["week_start"].to_list()
    #print(tim)
    
    for name in counties:
        values = e_dataframe1_[name]
        #print(values)                
        num_rows = len(values)
        y50 = values[-1:]
        #y5 = [y - values[-1] for y in y50]
        y = values
        original_values = compute_original_values(values)
        x = e_dataframe1[e_dataframe1.columns[0]]
        y1 = interpolate(y)
        x2 = x[9:]
        tim2 = tim#[3 : -4]
        y3 = y1#pd.DataFrame(y1, columns=["a"]).rolling(window=7).mean()['a'].to_list()[6:]
        ys = y3[-1:]
        xs = x[-1:-1]  # last 24 days
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
                recent_mean = int(np.mean(original_values[-1:]))
                recent_mean0 += recent_mean
                #if recent_mean > threshold:
                color = classify1(y3, recent_mean,name)
                #classify(ratio, recent_mean, threshold)
                #else:
                #    color = "green"
            else:
                #print(name,y3)
                ratio=0
                color="darkgreen"
            if name not in list(all_states.keys()):    
                all_states[name]={}
                all_states0[name]={}
                #print(recent_mean/population[name]["Population"]*100)
                all_states0[name][item]=[color,recent_mean0]
                #print(all_states0[name])
                #all_states[name][item]=[color,recent_mean0,population[name]["Population"],(recent_mean0/population[name]["Population"])*100000]
            else:
                all_states0[name][item]=[color,recent_mean0]
                #all_states[name][item]=[color,recent_mean0,population[name]["Population"],(recent_mean0/population[name]["Population"])*100000]                
                #print(item,name,color,ratio,recent_mean0,int(max(y5)))

            ind4+=1
print(all_states0)


with open("us_counties_colors_week.json","w") as fp:
    json.dump(all_states0,fp)
with open("us_counties_colors_full_week.json","w") as fp:
    json.dump(all_states,fp)
all_k=[]
with open("dates_week.json","w") as fp:
    json.dump(all_dates,fp)
'''

for item in list(all_states.keys()):
    for item2 in list(all_states[item].keys()):
        all_states[item][item2].append(item)
        all_states[item][item2].append(item2)
        all_k.append(all_states[item][item2])
final=pd.DataFrame(all_k,columns=["class","mean_cases","population","ratio","state","date"])
final2=final.sort_values(by=['ratio'], ascending=True)
final2.to_csv("us_states_rankings.csv")
final3=final2[final2["date"]=="2021-04-20"].set_index("state")
#print(final3)
final3.to_csv("us_states_rankings_last.csv")
'''
'''
 0    1        2         3
yellow  520  4921532  0.010566
yellow  520  4921532  0.010566  Alabama  2020-02-20
# with open('classification/data_counties.json', 'w') as outfile:
#    json.dump(aar,outfile)
aar1[0]["date"]=date_of_analysis
# this file is used by the map
with open(output_directory + '/classification/classification_ids_counties2.json', 'w') as outfile:
    json.dump(aar1, outfile)
'''
