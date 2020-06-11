
import numpy as np
import urllib.request as urllib2
import bz2
import pandas as pd
import json
import os
from os import listdir
from os.path import isfile, join
import json
onlyfiles = [f for f in listdir('/Users/olgabuchel/Downloads/2020-rki-archive-master/data/0_archived/') if isfile(join('/Users/olgabuchel/Downloads/2020-rki-archive-master/data/0_archived/', f))]
date_of_analysis='6/9/20'

output_directory = 'output_germany'
os.makedirs(output_directory + '/classification', exist_ok=True)

# Use canned CSV file, so we can compare results to earlier runs of the script.
use_canned_file = False
'''
with bz2.open('/Users/olgabuchel/Downloads/2020-rki-archive-master/data/0_archived/'+onlyfiles[-3], "r") as bzinput:
    print(bzinput)
    lines = []
    for i, line in enumerate(bzinput):
        if i == 10: break
        tweets = json.loads(line)
        lines.append(tweets)
'''
'''
filename0 = "/Users/olgabuchel/Downloads/2020-rki-archive-master/data/2_parsed/data_2020-06-08-02-30.json"
with open(filename0, 'r') as file:
    print(json.load(file)[0])
'''
#print(onlyfiles)




filename = "/Users/olgabuchel/Downloads/2020-03-27-12-00_dump.csv.bz2"
import bz2
import csv
from functools import partial

class BZ2_CSV_LineReader(object):
    def __init__(self, filename, buffer_size=4*1024):
        self.filename = filename
        self.buffer_size = buffer_size

    def readlines(self):
        with open(self.filename, 'rb') as file:
            for row in csv.reader(self._line_reader(file)):
                yield row

    def _line_reader(self, file):
        buffer = ''
        decompressor = bz2.BZ2Decompressor()
        reader = partial(file.read, self.buffer_size)

        for bindata in iter(reader, b''):
            block = decompressor.decompress(bindata).decode('utf-8')
            buffer += block
            if '\n' in buffer:
                lines = buffer.splitlines(True)
                if lines:
                    buffer = '' if lines[-1].endswith('\n') else lines.pop()
                    for line in lines:
                        yield line

lk_keys={}                        
main_df=pd.DataFrame()
main_df2=pd.DataFrame()
if __name__ == '__main__':
    for el in onlyfiles:
        if ".csv" in el:
            #print(el)
            bz2_csv_filename = '/Users/olgabuchel/Downloads/2020-rki-archive-master/data/0_archived/'+el
            all_rows=[]
            kkeys=[]
            ind=0
            for row in BZ2_CSV_LineReader(bz2_csv_filename).readlines():
                if ind>0:
                    if row[kkeys.index("Bundesland")]+", "+row[kkeys.index("Landkreis")] not in list(lk_keys.keys()):
                        lk_keys[row[kkeys.index("Bundesland")]+", "+row[kkeys.index("Landkreis")]]=str(row[kkeys.index("IdLandkreis")])
                    #print(kkeys)
                    #Bundesland         Landkreis Altersgruppe Geschlecht  ...            Meldedatum IdLandkreis
                    try:
                        row[0]=row[kkeys.index("Bundesland")]+", "+row[kkeys.index("Landkreis")]
                        #row[kkeys.index("Datenstand")]=row[kkeys.index("Datenstand")].split(" ")[0].replace(",","")
                        row[kkeys.index("Datenstand")]=el.split("-")[2]+"-"+el.split("-")[1]+"-"+el.split("-")[0]
                        all_rows.append(row)
                    except:
                        #print(kkeys,row)
                        continue
                else:
                    kkeys=row
                ind+=1
            kkeys[0]="Combined_Key"    
            df = pd.DataFrame(all_rows, columns=kkeys)
            df['AnzahlFall']=pd.to_numeric(df["AnzahlFall"])
            #df.loc[:,'Datenstand'] = el.split("-")[0]+"-"+el.split("-")[1]+"-"+el.split("-")[2]
            #print(df)
            df0=df.groupby(['Combined_Key','Datenstand'])['AnzahlFall'].sum().reset_index()
            main_df=pd.concat([main_df,df0])
        elif ".json" in el:
            bz2_csv_filename = '/Users/olgabuchel/Downloads/2020-rki-archive-master/data/0_archived/'+el
            all_rows=[]
            kkeys1=[]
            ind=0
            with open(bz2_csv_filename) as file1:
                data=json.load(file1)
                for row in data[0]["features"]:
                    if ind==0:
                        kkeys1=list(data[0]["features"][0]["attributes"].keys())
                        kkeys1[0]="Combined_Key"
                    ind+=1    
                    arr=list(row["attributes"].values())
                    try:
                        if arr[kkeys1.index("Bundesland")]+", "+arr[kkeys1.index("Landkreis")] not in list(lk_keys.keys()):
                            lk_keys[arr[kkeys1.index("Bundesland")]+", "+arr[kkeys1.index("Landkreis")]]=str(arr[kkeys1.index("IdLandkreis")])
                        arr[0]=arr[kkeys1.index("Bundesland")]+", "+arr[kkeys1.index("Landkreis")]
                        arr[kkeys1.index("Datenstand")]=el.split("-")[2]+"-"+el.split("-")[1]+"-"+el.split("-")[0]
                        all_rows.append(arr)
                    except:
                        print("missed")
                        #print(kkeys1,arr)
                        continue
            df = pd.DataFrame(all_rows, columns=kkeys1)
            df['AnzahlFall']=pd.to_numeric(df["AnzahlFall"])
            df0=df.groupby(['Combined_Key','Datenstand'])['AnzahlFall'].sum().reset_index()
            main_df2=pd.concat([main_df2,df0])

main_df3=pd.concat([main_df,main_df2])
df4=main_df3.groupby(['Combined_Key','Datenstand'])['AnzahlFall'].sum().reset_index()
print(df4.columns)
df4.set_index('Datenstand')
pivoted_table=df4.pivot(index='Combined_Key', columns='Datenstand', values='AnzahlFall')
#print(pivoted_table)
#print(pivoted_table.columns)

'''
DatetimeIndex(['2020-01-04', '2020-02-04', '2020-03-04', '2020-03-27',
               '2020-03-28', '2020-03-30', '2020-03-31', '2020-04-04',
               '2020-04-13', '2020-04-14', '2020-04-15', '2020-04-16',
               '2020-04-17', '2020-04-18', '2020-04-19', '2020-04-20',
               '2020-04-21', '2020-04-22', '2020-04-23', '2020-04-24',
               '2020-04-25', '2020-04-26', '2020-04-27', '2020-04-28',
               '2020-05-04', '2020-06-04', '2020-07-04', '2020-08-04',
               '2020-09-04', '2020-10-04', '2020-11-04', '2020-12-04'],
              dtype='datetime64[ns]', name='Datenstand', freq=None)

'''

dates=["10-03-2020","11-03-2020","12-03-2020","13-03-2020","14-03-2020","15-03-2020","16-03-2020","17-03-2020","18-03-2020","19-03-2020","20-03-2020","21-03-2020","22-03-2020","23-03-2020","24-03-2020","25-03-2020","26-03-2020","27-03-2020","28-03-2020","29-03-2020","30-03-2020","31-03-2020"]
for x in range(4,7):
    if x<10:
        x="0"+str(x)
    for y in range(1,32):
        if y<10:
            y="0"+str(y)
        if str(y)+"-"+str(x)+"-"+"2020" not in ["31-04-2020"]:    
            dates.append(str(y)+"-"+str(x)+"-"+"2020")
dates0=dates[:len(dates)-(31-int(date_of_analysis.split("/")[1]))]

#e_dataframe0 = df4
#print(e_dataframe0)
#e_dataframe.drop(columns=['UID','iso2','iso3','code3','FIPS','Admin2','Province_State','Country_Region','Lat','Long_'])
#print(e_dataframe0.columns.tolist())
e_dataframe1 = pivoted_table.reindex(columns=dates0).transpose()#.set_index('Datenstand')
#print(df8)
#print(lk_keys)
data=lk_keys

'''
with open('german_keys.json', 'r') as outfile:                                                                                                                                     
    data=json.load(outfile)
print(data)    
'''

#e_dataframe = data.set_index("Combined_Key")
ids = list(data.values())
recs = list(data.keys())


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
    values0 = e_dataframe1[name].fillna(0).tolist()
    #print(name,list(values))
    values=[]
    ind10=0
    print(int(np.max(values0)))
    for en in values0:
        if ind10>values0.index(int(np.max(values0))):
            values.append(int(np.max(values0)))
        else:
            values.append(en)
        ind10+=1
    print(values)    
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
    #print(pd.DataFrame(y1, columns=["a"]).rolling(window=7).mean()['a'].to_list())
    y3 = pd.DataFrame(y1, columns=["a"]).rolling(window=7).mean()['a'].to_list()[6:]
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
        recent_mean = int(np.mean(original_values[-10:]))
        color = classify(ratio, recent_mean, threshold)
    else:
            #print(name,y3)                                                                                                                                                         
        ratio=0
        color="green"
    if name in recs:
            #print(name,color)
        with open(output_directory + '/classification/data_counties_'+str(ids[recs.index(name)])+'.json', 'w') as outfile:
            json.dump({"dates":tim2,"max_14":int(max(y5)),"max":int(max(y)),"value":y3,"time":tim,"original_values": original_values},outfile)
            #aar.append({"color":color,"province":name.split(",")[0],"country":name.split(",")[1],"id":"new_id_"+str(ind4),"value1":ratio, "dates":tim2,"value":y3})                
        aar1.append({"n":name,"id":ids[recs.index(name)],"v":ratio,"c":color,"max":int(max(y5))})
    else:
        print("not"+name,color)
    ind4+=1


# with open('classification/data_counties.json', 'w') as outfile:                                                                                                                   
#    json.dump(aar,outfile)                                                                                                                                                         
#aar1[0]["Datenstand"]=date_of_analysis
# this file is used by the map
print(recs,ids)
with open(output_directory + '/classification/classification_ids_provinces2.json', 'w') as outfile:
    json.dump(aar1, outfile)    
