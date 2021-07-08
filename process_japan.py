#/Users/olgabuchel/Downloads/covid_jpn_prefecture.csv.xls
#https://www.kaggle.com/lisphilar/covid19-dataset-in-japan?select=covid_jpn_prefecture.csv
#https://github.com/deldersveld/topojson/blob/master/countries/japan/jp-prefectures.json
#jp-prefectures.json
import numpy as np
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

data2=pd.read_csv("/Users/olgabuchel/Downloads/covid_jpn_prefecture.csv.xls")
print(data2)
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
output_directory = 'output_japan'
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
    values = e_dataframe1[name]
    num_rows = len(values)
    y50 = values[-15:]
    y5 = [y - values[-15] for y in y50]
    y = values
    original_values = compute_original_values(values)
    x = e_dataframe1[e_dataframe1.columns[0]]
    y1 = interpolate(y)
    x2 = x[9:]
    tim2 = tim[3 : -4]
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
        with open(output_directory + '/classification/data_counties_'+str(ids[recs.index(name)])+'.json', 'w') as outfile:
            json.dump({"dates":tim2,"max_14": int(max(y5)-min(y5)),"max":int(max(y)),"value":y3,"time":tim,"original_values":original_values},outfile)
        #aar.append({"color":color,"province":name.split(",")[0],"country":name.split(",")[1],"id":"new_id_"+str(ind4),"value1":ratio, "dates":tim2,"value":y3})                    
        aar1.append({"n":name,"id":ids[recs.index(name)],"v":ratio,"c":color,"max":int(max(y5)-min(y5))})
        ind4+=1


# with open('classification/data_counties.json', 'w') as outfile:                                                                                                                   
#    json.dump(aar,outfile)                                                                                                                                                         
aar1[0]["date"]=date_of_analysis
# this file is used by the map                                                                                                                                                      
with open(output_directory + '/classification/classification_ids_counties2.json', 'w') as outfile:
    json.dump(aar1, outfile)


################################################################################################


cols=list(e_dataframe1.columns)
cols1=list([str(x) for x in e_dataframe1.index])
kkd0=e_dataframe1.sum(axis = 0, skipna = True).to_dict()
#argentina_population.csv                                                                                                                                                           
#data13=pd.read_csv("argentina_population.csv")
#data13["Population (2013)1"]=[int(str(x).replace(",","")) for x in data13["Population (2013)"].to_list()]
#kkd=data13[["Province/District","Population (2013)1"]].set_index("Province/District").to_dict()["Population (2013)1"]
'''
all=[]
for item in list(kkd0.keys()):
    try:
        all.append([item,kkd0[item],kkd[item],kkd0[item]/kkd[item]])
    except:
        all.append([item,kkd0[item],0,kkd0[item]])

dd=pd.DataFrame(all,columns=["Province","Cases","Population","Ratio"])
dd0=dd.sort_values(by=['Ratio'], ascending=False)
print(dd0)
print(dd0["Province"].to_list())
'''

e_dataframe2=e_dataframe1

for item in cols:
    e_dataframe2[item]=e_dataframe1[item].diff().fillna(0).to_list()


item0=0
arrs=[]
for item in e_dataframe2.iterrows():
    it=0
    for el in item[1].values:
        if cols[it]!="data":#,ll[cols[it]])                                                                                                                                        
            if el<0:
                el=0
            arrs.append({"x":cols1[item0],"y":str(cols[it]),"z":int(el),"p":"Japan"})
        it+=1
    item0+=1
print(arrs)                                                                                                                                                                       
print(cols)                                                                                                                                                                       
#print(cols1)                                                                                                                                                                      
#print(kkd)                                                                                                                                                                        
#print(kkd0)                                                                                                                                                                       
with open("fire_japan.json", "w") as fp:
    json.dump(arrs,fp)

print(e_dataframe2)
