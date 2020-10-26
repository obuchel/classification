


import json
import pandas as pd
names={'םהוש': 'Shoham','בייה תמור':'Ramat Hovav','בגנב-הרערע':"Ar'ara Banegev",'רוכרכ-הנח סדרפ':'Pardes Hana - Karkur','השנמ יפלא':'Menashe','היברג-לא הקאב':'baka al rarbiya',"(גוש חלב) ג'ש":"Jish (Gush Halav)","בקעי בכוכ":"Zih'ron Ya'akov","תיליע ןיעידומ":"Hevel Modi'in","ופי - ביבא לת":"Tel Aviv - Yafo","ןונד ’חייש":'Sheikh Danun',
'בייה תמור':'Rumat Heib','בגנב-הרערע':"Ar'arat an-Naqab",
'רוכרכ-הנח סדרפ': 'Pardes Hanna-Karkur','השמ רוצ': 'Tsur Moshe',
"ןרוצ-המידק": 'Kadima Zoran','(טבש)ענאצ-א תאריידוק': "Qderat a'Sana",
'רס-א רצק': "Qasr al-Sir",'הרפע':'Ofra',
'םירפא ץע':'Ets Efraim','רייזוע':'Uzeir',
'ןובלייע':'Eilabun',"אבוקנ ןיע":'Ein Naqquba',
'איינק ןיע':'Ein Qiniyye',"ילע":'Eli',
'לאונמע':'Emanuel','איפסע':'Isfiya',
"(טבש) דעייוו‘ג ובא":"Abu Jwei'ad",
"(טבש) תאנירוק ובא":'Abu Qrenat',"(טבש) העייבור ובא":'Abu Rebiya',
'(טבש) קייקור ובא':'Abu Rukik','לולת ובא':'Abu Tulul',
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
"בקעי בכוכ":"Kokhav Ya'aqov","הר’גא‘גח-שאבט-היבעכ":"Ka'abiyye-Tabbash-Hajajre",
'ד“בח רפכ':'Kfar Habad',"הלבייקומ":'Muqeible',
'םימודא הלעמ':"Ma'ale Adumim",'לילגה ףונ':'Nof Hagalil',
'םלוס':'Sulam',"(טבש) דייס":'AlSayid Tribe','המלס':'Salama'}

muni={}
munis=[]
with open("municipalities9.json","r") as fp:
    muni=json.load(fp)
    for el in muni["features"]:
        munis.append(el["properties"]["MUN_ENG"])
data=[]
kkeys={}
with open("cities.json","r") as fp:
    data=json.load(fp)
    for el in data:
        mm=[x.lower() for x in munis]
        if el['english_name'].lower() in mm:
            print(el['english_name'].lower())
            kk=mm.index(el['english_name'].lower())
            kkeys[el["semel_yeshuv"]]=mm[kk]
        else:    
            kkeys[el["semel_yeshuv"]]=el['english_name']#shem_napa
    
    
print(kkeys)    

main_data=pd.read_csv("israeli-covid-cases.csv")
print(main_data["cityCode"].unique())
main_data["district"]=main_data["cityCode"].astype(str).map(kkeys)

print(main_data["district"].unique())
print(munis)
