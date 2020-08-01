


#/Users/olgabuchel/Downloads/28_day.csv - last 28 days
#OBJECTID	Place	תאריך	שעות שהייה	x	y
#1276117	פינסקר - מרכז מקצועי - שירותי בריאות כללית - ראשון לציון	28/6/2020	08:00 - 10:30	34.80713460000000	31.968514200000100
#/Users/olgabuchel/Downloads/IRSL.csv - historical dates grouped
#	City	Population as of 2018	Number of tests so far	Verified patients discovered so far	Number of recoverers	The growth rate of verified patients in the last 3 days	The number of verified patients added in the last 3 days	Actual morbidity rate ** per 100,000	dates
#https://imoh.maps.arcgis.com/apps/webappviewer/index.html?id=20ded58639ff4d47a2e2e36af464c36e&locale=he&/
#/Users/olgabuchel/Downloads/coordinates.csv 
#prepare_classification_counties_israel2.py
#'IL': ('Israel', (34.2654333839, 29.5013261988, 35.8363969256, 33.2774264593)),
#['9657', 'אבו תלול', '2022', '56', '0', '0', '0.0', '0', '0', '2020-06-27']
import csv
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import os
city_names=pd.read_csv('translate_city_names.csv')
#print(city_names)
data=pd.read_csv('output6.csv')
print(data)
date_of_analysis='7/26/20' 
'''
'שוהם': 'שהם'
df4=pd.pivot_table(df2,index=[list(df.columns)[2]],columns=list(df.columns)[1],values=["OBJECTID"],aggfunc=np.sum)
'''

output_directory = 'output_israel'
os.makedirs(output_directory + '/classification', exist_ok=True)


e_dataframe0=data.transpose()

ids = list(data.columns)[1:]
#list(df2.Place.unique())  
recs = ids
#print(ids)
#print(e_dataframe0)
e_dataframe1 = data
def add_day_columns(df):
    """Add columns Elapsed_days, Decimals, Day_Year to df."""
    dats = list(df.index)
    #print(dats)
    dats2 = []
    decimals = []
    elapsed_days = []
    ind = 35
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

tim = data["dates"].to_list()
#list(df[list(df.columns)[2]].unique())
print(tim)
#tim.pop(0)

ind4 = 0
aar = []
aar1 = []
counties = recs
print(counties)
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

#print(df4.columns)
names={'שוהם': 'Shoham','רומת הייב':'Ramat Hovav','ערערה-בנגב':"Ar'ara Banegev",'פרדס חנה-כרכור':'Pardes Hana - Karkur','אלפי מנשה':'Menashe','באקה אל-גרביה':'baka al rarbiya',"ג'ש (גוש חלב)":"Jish (Gush Halav)","כוכב יעקב":"Zih'ron Ya'akov","מודיעין עילית":"Hevel Modi'in","תל אביב - יפו":"Tel Aviv - Yafo","שייח’ דנון":'Sheikh Danun',
'רומת הייב':'Rumat al-Heib','ערערה-בנגב':"Ar'arat an-Naqab",
'פרדס חנה-כרכור': 'Pardes Hanna-Karkur','צור משה': 'Tsur Moshe',
"קדימה-צורן": 'Kadima Zoran','(קודייראת א-צאנע(שבט': "Qderat a'Sana",
'קצר א-סר': "Qasr al-Sir",'עפרה':'Ofra',
'עץ אפרים':'Ets Efraim','עוזייר':'Uzeir',
'עיילבון':'Eilabun',"עין נקובא":'Ein Naqquba',
'עין קנייא':'Ein Qiniyye',"עלי":'Eli',
'עמנואל':'Emanuel','עספיא':'Isfiya',
"(אבו ג‘ווייעד (שבט":"Abu Jwei'ad",
"(אבו קורינאת (שבט":'Abu Qrenat',"(אבו רובייעה (שבט":'Abu Rebiya',
'(אבו רוקייק (שבט':'Abu Rukik','אבו תלול':'Abu Talul',
'אבטין':'Ibtin','אום בטין':'Umm Batin',
'אורנית':'Oranit','אחוזת ברק':'Ahuzat Barak',
'(אטרש (שבט':'Atrash Tribe','אל סייד':'al-Sayyid',
'אלון שבות':'Alon Shvut','אלעזר':'Elazar',
'אלפי מנשה':'','אלקנה':'Elkana',
'(אעצם (שבט':"A'sam Tribe",'אפרת':'Efrat',
"אריאל":'Ariel','באקה אל-גרביה':'Baqa al-Gharbiyye',
'ביר הדאג’':'Beit Hadag',"בית אל":'Beit El',"בית אריה":'Beit Aryeh-Ofarim',
"בית חשמונאי":'Beit Hashmonai',"ביתר עילית":'Beitar Illit',
'ברכה':'Har Brakha','גבעת אלה':'Givat Ela','גבעת זאב':"Giv'at Ze'ev",
"דייר אל-אסד":'Dir el-Asad',"יהוד":'Yehud',
"כוכב יעקב":"Kochav Ya'akov","כעביה-טבאש-חג‘אג’רה":"Ka'abiyye-Tabbash-Hajajre",
'כפר חב“ד':'Kfar Habad',"מוקייבלה":'Muqeible',
'מעלה אדומים':"Ma'ale Adumim",'נוף הגליל':'Nof Hagalil',
'סולם':'Sulam',"(סייד (שבט":'AlSayid Tribe','סלמה':'Salama'}
print(city_names)
with open("/Users/olgabuchel/Downloads/israel-municipalities-polygons-master/municipalities.geojson","r") as json_file:
    dd=json.load(json_file)
    for el in dd["features"]:
        #{'MUN_HEB': 'דרום השרון', 'MUN_ENG': 'Drom Hasharon'}
        print(el["properties"])
        names[el["properties"]["MUN_HEB"]]=el["properties"]["MUN_ENG"]
for name in counties:
    name0=name[1]
    #print(name)
    if "קטן מ-15" not in e_dataframe1[name].to_list():
        values = e_dataframe1[name]
        if name in list(names.keys()):
            name0=names[name]
        else:    
            name0=name
        num_rows = len(values)
        y50 = values[-14:]
        #print(y50)
        y5 = [y - values[len(values)-15] for y in y50]
        y = values
        original_values = compute_original_values(values)
        #print(original_values)
        
        x = e_dataframe1[e_dataframe1.columns[0]]
        y1 = interpolate(y)
        #print(x,y1)
    
        x2 = x[6:]
        tim2 = tim[3 : -4]
        #print(tim2)
        y3 = pd.DataFrame(y1, columns=["a"]).rolling(window=7).mean()['a'].to_list()[6:]
        ys = y3[-12:]
        xs = x[-9:-4]  # last 24 days
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

            #print(name[1],color,ratio,recent_mean0,int(max(y5)))#,str(ids[recs.index(name)]["Combined_Key"]))
            #print(y5)
            #print(y3)
            #print(y)
            '''     
            plt.title(name[1])                                                                                                                                           
            plt.plot(x2,y3,color=color)                                                                                                                                      
            #plt.savefig(name[1]+".png")                                                                                                                                         
            plt.show()
            '''          
                    
            try:        
                with open(output_directory + '/classification/data_counties_'+str(name0)+'.json', 'w') as outfile:
                    json.dump({"dates":tim2,"max_14": int(max(y5)-min(y5)),"max":int(max(y)),"value":y3,"time":tim,"original_values":original_values},outfile)
                #aar.append({"color":color,"province":name.split(",")[0],"country":name.split(",")[1],"id":"new_id_"+str(ind4),"value1":ratio, "dates":tim2,"value":y3})
                aar1.append({"n":name0,"id":name0,"v":ratio,"c":color,"max":int(max(y5)-min(y5)),"t":int(max(y))})
            except:
                continue
            ind4+=1
            

# with open('classification/data_counties.json', 'w') as outfile:
#    json.dump(aar,outfile)
print(aar1)
aar1[0]["date"]=date_of_analysis
# this file is used by the map
with open(output_directory + '/classification/classification_ids_counties2.json', 'w') as outfile:
    json.dump(aar1, outfile)



print(names)
