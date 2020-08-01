


import json
import pandas as pd
import numpy as np

all_items=[]
with open("grouped_israelian_cities2.json","r") as json_file:
    data=json.load(json_file)
    ll=list(data.keys())
    for el in ll:
        for item in data[el]:
            item.append(el)
            all_items.append(item)
df=pd.DataFrame(all_items,columns=["OBJECTID","x","y","name_j","date","name"]).drop_duplicates()
#[1840928, 34.7848764, 31.8105932, 'בצל ירוק - גדרה', '17/7/2020', 'Gedera']
print(df["date"])
df["date"] = pd.to_datetime(df["date"],format='%d/%m/%Y').dt.date
df1=df.sort_values(by='date')

table = pd.pivot_table(df1, values='OBJECTID', index=['date'],columns=['name'], aggfunc='count').reset_index()
print(table.columns)
table["date"] = pd.to_datetime(table["date"], errors='coerce')
#table[table['name'] == 'name']
#df[(df['Delivery Date'].dt.year == 1970) | (df['Delivery Date'] >= sixmonthago)]
table1=table[(table['date'].dt.month >= 7) & (table['date'].dt.day > 9)]
print(table1)
names={'םהוש': 'Shoham','בייה תמור':'Ramat Hovav','בגנב-הרערע':"Ar'ara Banegev",'רוכרכ-הנח סדרפ':'Pardes Hana - Karkur','השנמ יפלא':'Menashe','היברג-לא הקאב':'baka al rarbiya',"(גוש חלב) ג'ש":"Jish (Gush Halav)","בקעי בכוכ":"Zih'ron Ya'akov","תיליע ןיעידומ":"Hevel Modi'in","ופי - ביבא לת":"Tel Aviv - Yafo","ןונד ’חייש":'Sheikh Danun',
'בייה תמור':'Rumat al-Heib','בגנב-הרערע':"Ar'arat an-Naqab",
'רוכרכ-הנח סדרפ': 'Pardes Hanna-Karkur','השמ רוצ': 'Tsur Moshe',
"ןרוצ-המידק": 'Kadima Zoran','(טבש)ענאצ-א תאריידוק': "Qderat a'Sana",
'רס-א רצק': "Qasr al-Sir",'הרפע':'Ofra',
'םירפא ץע':'Ets Efraim','רייזוע':'Uzeir',
'ןובלייע':'Eilabun',"אבוקנ ןיע":'Ein Naqquba',
'איינק ןיע':'Ein Qiniyye',"ילע":'Eli',
'לאונמע':'Emanuel','איפסע':'Isfiya',
"(טבש) דעייוו‘ג ובא":"Abu Jwei'ad",
"(טבש) תאנירוק ובא":'Abu Qrenat',"(טבש) העייבור ובא":'Abu Rebiya',
'(טבש) קייקור ובא':'Abu Rukik','לולת ובא':'Abu Talul',
'ןיטבא':'Ibtin','ןיטב םוא':'Umm Batin',
'תינרוא':'Oranit','קרב תזוחא':'Ahuzat Barak',
'(טבש) שרטא':'Atrash Tribe','דייס לא':'al-Sayyid',
'תובש ןולא':'Alon Shvut','רזעלא':'Elazar',
       'אלקנה':'Elkana',
'(טבש) םצעא':"A'sam Tribe",'תרפא':'Efrat',
"לאירא":'Ariel','היברג-לא הקאב':'Baqa al-Gharbiyye',
'גאדה ריב’':'Beit Hadag',"לא תיב":'Beit El',"הירא תיב":'Beit Aryeh-Ofarim',
"יאנומשח תיב":'Beit Hashmonai',"תיליע רתיב":'Beitar Illit',
'הכרב':'Har Brakha','הלא תעבג':'Givat Ela','באז תעבג':"Giv'at Ze'ev",
"דסא-לא רייד":'Dir el-Asad',"דוהי":'Yehud',
"בקעי בכוכ":"Kochav Ya'akov","הר’גא‘גח-שאבט-היבעכ":"Ka'abiyye-Tabbash-Hajajre",
'ד“בח רפכ':'Kfar Habad',"הלבייקומ":'Muqeible',
'םימודא הלעמ':"Ma'ale Adumim",'לילגה ףונ':'Nof Hagalil',
'םלוס':'Sulam',"(טבש) דייס":'AlSayid Tribe','המלס':'Salama'}

all_recs={}
all_recs0=[]
for el in list(table1.columns):
    if el in list(names.values()):
        print(list(names.keys())[list(names.values()).index(el)])
        print(table1[el].fillna(0).cumsum().to_list())
        all_recs[list(names.keys())[list(names.values()).index(el)]]=table1[el].fillna(0).cumsum().to_list()
        all_recs0.append(el)
kkeys0={}
with open("municipalitiesL.geojson","r") as json_file:
    data=json.load(json_file)
    print(data["features"][0]['properties'])
    #'MUN_HEB': 'דרום השרון', 'MUN_ENG'
    for el in data["features"]:
        if el["properties"]["MUN_ENG"] not in list(kkeys0.keys()):
            kkeys0[el["properties"]["MUN_ENG"]]=el["properties"]["MUN_HEB"]
for el in list(table1.columns):
    if el in list(kkeys0.keys()) and el not in all_recs0:
        all_recs[kkeys0[el]]=table1[el].fillna(0).cumsum().to_list()
print(all_recs)        
print(table1.date)        
data2=pd.read_csv("output3.csv")

data2.dates2=data2.dates.append(table1.date.dt.date)
print(data2.dates2.to_string())
all_dates=[]
for el in data2.dates2:
    all_dates.append(str(el))
print(all_dates)
print(data2)
main_arr={'dates':all_dates}
for el in list(data2.columns)[1:]:
    #print(el,data2[el].to_list())
    main_data=data2[el].to_list()
    last_value=main_data[len(main_data)-1]
    if el in list(all_recs.keys()):
        arr=[int(x+last_value) for x in all_recs[el]]
        print(main_data+arr)
        main_arr[el]=main_data+arr
    else:
        ll=len(all_recs[list(all_recs.keys())[0]])
        arr0=list(np.zeros(ll))
        print(last_value,arr0)
        arr=[int(x)+int(last_value) for x in arr0]
        print(main_data+arr)
        main_arr[el]=main_data+arr
        #main_arr.append(main_data+arr)
df=pd.DataFrame(main_arr)
print(df)
print(data2.columns)        
print(len(main_arr))
df.to_csv (r'output6.csv', index = False, header=True)



    
#print(all_recs)
        #table1[el].fillna(0).cumsum().to_list()
