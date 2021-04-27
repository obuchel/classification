#https://data.mesaaz.gov/api/views/bcxg-q9nz/rows.csv?accessType=DOWNLOAD
#https://data.mesaaz.gov/Fire-and-Medical/Daily-COVID-19-Cases-by-Zip-Code/bcxg-q9nz/data
import csv
import json
from datetime import datetime
import numpy as np
import pandas as pd
import os
import time, calendar, pandas as pd
import wget    

def to_posix_ts(d: datetime, utc:bool=True) -> float:
    print(d)
    tt=d.timetuple()
    return (calendar.timegm(tt) if utc else time.mktime(tt)) + round(d.microsecond/1000000, 0)

#from prep_canada_data import stage_latest

#date_of_analysis='03/07/21'
from datetime import date
#date_of_analysis='03/07/21'
date_of_analysis=date.today().strftime("%m/%d/%y")
print(date_of_analysis)

def pd_timestamp_from_datetime(d: datetime) -> pd.Timestamp:
        return pd.to_datetime(to_posix_ts(d), unit='s')

    
output_directory = 'output_arizona'
os.makedirs(output_directory + '/classification', exist_ok=True)

# Use canned CSV file, so we can compare results to earlier runs of the script.
use_canned_file = False
'''
url = 'https://data.mesaaz.gov/api/views/bcxg-q9nz/rows.csv?accessType=DOWNLOAD'
#wget.download(url, '../Daily_COVID-19_Cases_by_Zip_Code.csv')
os.system("mv ../Daily_COVID-19_Cases_by_Zip_Code.csv /Users/olgabuchel/.Trash/Daily_COVID-19_Cases_by_Zip_Code.csv")
os.system("wget "+url+" --no-check-certificate")
os.system("mv rows.csv?accessType=DOWNLOAD ../Daily_COVID-19_Cases_by_Zip_Code.csv")
'''
data = pd.read_csv('../Daily_COVID-19_Cases_by_Zip_Code.csv', delimiter=',',error_bad_lines=False,quoting=csv.QUOTE_MINIMAL)
'''
with open('../Daily_COVID-19_Cases_by_Zip_Code.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in spamreader:
        print(', '.join(row))
'''


#/abuchel/Downloads/Daily_COVID-19_Cases_by_Zip_Code.csv')
data["dates"]=data.apply(lambda row: str(row.Date).split(" ")[0], axis=1)
#data.sort_values(by=['dates'])
data["Combined_Key"]=data["Zip Code"]
data["m"]=pd.to_datetime(data["dates"]).dt.month
data["y"]=pd.to_datetime(data["dates"]).dt.year
data["d"]=pd.to_datetime(data["dates"]).dt.day
data["date1"]=pd.to_datetime(data["dates"],format='%m/%d/%Y')
#pd.Timestamp(year=data["y"], month=data["m"], day=data["d"], hour=12)
print(data["d"])
#[x.replace("/","") for x in data["dates"].to_list()]
data=data.sort_values(by='date1',ascending=True)
df=data.sort_values(by='date1',ascending=True)#pd.pivot_table(data,index=["dates"],columns='Combined_Key',values=["Confirmed Cases Count"],aggfunc=np.sum)
#print(df["dates"].unique())
df4=df.fillna(0)
print(df4)
'''
groupby Date', 'Zip Code', 'Primary City 'Confirmed Cases Count'
Index(['Row ID', 'Year', 'Month', 'Date', 'Zip Code', 'Primary City',
       'Confirmed Cases Category', 'Confirmed Cases Count', 'Population',
       'Population Density', 'Confirmed Case Rate per 100,000 People',
       'Geometry'],
      dtype='object')

'''

e_dataframe0=pd.pivot_table(data,index=["dates"],columns='Combined_Key',values=["Confirmed Cases Count"],aggfunc=np.sum)    
e_dataframe = df4.set_index("Combined_Key")
ids = data[["Combined_Key","Primary City"]].to_dict('records')
recs = data["Combined_Key"].to_list()

# stage latest Canada HR-level data for later processing
#latest_ca_df = stage_latest()
#print(latest_ca_df)
#assert latest_ca_df.index.names == ['Combined_Key']
#print(latest_ca_df)

#e_dataframe0 = e_dataframe.drop(columns=['UID','iso2','iso3','code3','FIPS','Admin2','Province_State','Country_Region','Lat','Long_'])
e_dataframe1 = pd.pivot_table(df4,index=["dates"],columns='Combined_Key',values=["Confirmed Cases Count"],aggfunc=np.sum).fillna(0)
#print(e_dataframe1)
print(ids)
#print(recs)


def add_day_columns(df):
    """Add columns Elapsed_days, Decimals, Day_Year to df."""
    dats = list(df.index)
    #print(dats)
    dats2 = []
    decimals = []
    elapsed_days = []
    ind = 106
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
print(e_dataframe1)


if False:
    # show intermediate result and abortthe script right here
    print(e_dataframe1.iloc[10:, :5])
    import sys
    sys.exit(0)

tim = list(df.dates.unique())
print(tim)
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
    values = e_dataframe1[name]
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
            color="darkseagreen"

        #print(ids[recs.index(name0)]["Combined_Key"])#,name0,color,ratio,recent_mean0,int(max(y5)),str(ids[recs.index(name)]["Combined_Key"]))
        try:
            print(tim2,y3,tim,original_values)
            with open(output_directory + '/classification/data_counties_'+str(ids[recs.index(name0)]["Combined_Key"]).replace(" ","_")+'.json', 'w') as outfile:
                json.dump({"dates":tim2,"max_14": int(max(y5)-min(y5)),"max":int(max(y)),"value":y3,"time":tim,"original_values":original_values},outfile)
                #aar.append({"color":color,"province":name.split(",")[0],"country":name.split(",")[1],"id":"new_id_"+str(ind4),"value1":ratio, "dates":tim2,"value":y3})
            aar1.append({"n":name,"id":ids[recs.index(name0)]["Combined_Key"].replace(" ","_"),"v":ratio,"c":color,"max":int(max(y5)-min(y5)),"t":int(max(y))})
        except:
            continue
        ind4+=1


# with open('classification/data_counties.json', 'w') as outfile:
#    json.dump(aar,outfile)
aar1[0]["date"]=date_of_analysis
# this file is used by the map
with open(output_directory + '/classification/classification_ids_counties2.json', 'w') as outfile:
    json.dump(aar1, outfile)
print(df)
#print(print(data.sort_values(by='date1',ascending=True)))
