#/Users/olgabuchel/Downloads/covid_jpn_prefecture.csv.xls
#https://www.kaggle.com/lisphilar/covid19-dataset-in-japan?select=covid_jpn_prefecture.csv
#https://github.com/deldersveld/topojson/blob/master/countries/japan/jp-prefectures.json
#jp-prefectures.json

import pandas  as pd
import json
import os
from datetime import date
#from prep_canada_data import stage_latest                                                                                                                                           
#https://cdn.mbta.com/archive/archived_feeds.txt                                                                                                                                     
#date_of_analysis='03/07/21'                                                                                                                                                         
date_of_analysis=date.today().strftime("%m/%d/%y")
print(date_of_analysis)
arr=[]
with open("JPN_adm1.json","r") as fp:
    data=json.load(fp)
    for item in data["features"]:
        arr.append(item["properties"]["NAME_1"])
print(arr)

data2=pd.read_csv("/Users/olgabuchel/Downloads/covid_jpn_prefecture.csv")
for el in list(data2["Prefecture"].unique()):
    try:
        print(arr.index(el),el)
    except:
        print("--   "+el)
        continue
print(data2)
#Date Prefecture  Positive
e_dataframe1=data2.pivot(index='Date', columns='Prefecture', values='Positive')
#print(data_all)
output_directory = 'output'
os.makedirs(output_directory + '/classification', exist_ok=True)
e_dataframe = e_dataframe1.transpose()#data.set_index("Combined_Key")
ids = list(e_dataframe1.columns)#data[["UID", "Combined_Key"]].to_dict('records')
recs = ids#data["Combined_Key"].to_list()

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

tim = list(e_dataframe1.index)
tim.pop(0)
print(tim)
ind4 = 0
aar = []
aar1 = []
counties = e_dataframe1.columns
print(counties)
