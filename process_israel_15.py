


#https://github.com/Arturiko/israel-cities/blob/master/JsonPropertiesWithoutIDs.json



import json
import pandas as pd
import numpy as np

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

municipalities={}
with open("municipalities.json","r") as fp:
    municipalities=json.load(fp)
    for el in municipalities["features"]:
        print(el["properties"])
        municipalities[el["properties"]["MUN_ENG"]]=el["properties"]["MUN_HEB"]


coords3={"'קצר א-סר":[31.083056, 34.978611],
"ביר הדאג'":[30.977242, 34.695939],
'אל סייד' :[31.284444, 34.916111],
"אבו רוקייק (שבט)":[31.26, 34.864],
"אבו ג'ווייעד (שבט)":[31.178502,34.745967]}

muni={}
munis=[]
with open("municipalities10.json","r") as fp:
    muni=json.load(fp)
    for el in muni["features"]:
        munis.append(el["properties"]["MUN_ENG"])
        #el["properties"]["MUN_HEB"]=municipalities[el["properties"]["MUN_ENG"]]
    #print(muni)
    '''
    with open("municipalities10.json","w") as fp1:
        json.dump(muni,fp1)
    '''
coords={"ABU RUBEI'A":[35.207778,36.520833], 
'ABU QUREINAT':[31.103056,34.951944], 
'ABU TULUL':[31.142053,34.914358], 
'ATRASH':[31.261274,34.97548], 
"A'SAM":[31.295816,34.903102], 
'EFRAT':[31.658,35.1531], 
"BU'EINE-NUJEIDAT":[32.807411,35.367278], 
'BET EL':[31.943765,35.222549], 
'SHEIKH DANNUN':[32.991667,35.147778], 
'QUDEIRAT AS-SANI':[31.293107,35.10564], 
'QADIMA-ZORAN':[32.277778,34.915278], 
'ZUR YIZHAQ':[32.241047,34.997378], 
"PEQI'IN (BUQEI'A)":[32.974167,35.331389], 
'GHAJAR':[33.272778,35.623056], 
'SAYYID':[31.284444,34.916111], 
'SAKHNIN':[32.866667,35.3], 
'SAJUR':[32.931667,35.319722], 
'MAJDAL SHAMS':[33.266667,35.766667], 
'MAJD AL-KURUM':[32.920556,35.252778], 
"KA'ABIYYE-TABBASH-HA":[32.749383,35.183672], 
'KAOKAB ABU AL-HIJA':[32.831389,35.248611], 
'YEHUD-MONOSON':[32.028381,34.879617], 
'YANUH-JAT':[32.982778,35.244167], 
'HARISH':[32.459167,35.042778], 
'HAWASHLA':[31.083056,34.978611], 
'JAAT':[32.399444,35.036667], 
'JISH(GUSH HALAV)':[33.026111,35.445278], 
'JISR AZ-ZARQA':[32.538056,34.912222],  
'GANNE MODIIN':[31.929556,35.01675], 
'JALJULYE':[32.15353,34.9518],  
'JUDEIDE-MAKER':[32.933333,35.141389], 
'JULIS':[32.944167,35.185833],  
'BEIT JANN':[32.965278,35.379444]}


'''
{"ABU RUBEI'A":"35.207778_36.520833", 
'ABU QUREINAT':"31.103056_34.951944", 
'ABU TULUL':"31.142053_34.914358", 
'ATRASH':"31.261274_34.97548", 
"A'SAM":"31.295816_34.903102", 
'EFRAT':"31.658_35.1531", 
"BU'EINE-NUJEIDAT":"32.807411_35.367278", 
'BET EL':"31.943765_35.222549", 
'SHEIKH DANNUN':"32.991667_35.147778", 
'QUDEIRAT AS-SANI':"31.293107_35.10564", 
'QADIMA-ZORAN':"32.277778_34.915278", 
'ZUR YIZHAQ':"32.241047_34.997378", 
"PEQI'IN (BUQEI'A)":"32.974167_35.331389", 
'GHAJAR':"33.272778_35.623056", 
'SAYYID':"31.284444_34.916111", 
'SAKHNIN':"32.866667_35.3", 
'sajur':"32.931667_35.319722", 
'MAJDAL SHAMS':"33.266667_35.766667", 
'MAJD AL-KURUM':"32.920556_35.252778", 
"KA'ABIYYE-TABBASH-HA":"32.749383_35.183672", 
'KAOKAB ABU AL-HIJA':"32.831389_35.248611", 
'YEHUD-MONOSON':"32.028381_34.879617", 
'YANUH-JAT':"32.982778_35.244167", 
'harish':"32.459167_35.042778", 
'HAWASHLA':"31.083056_34.978611", 
'JAAT':"32.399444_35.036667", 
'JISH(GUSH HALAV)':"33.026111_35.445278", 
'JISR AZ-ZARQA':"32.538056_34.912222", 
'GANNE MODIIN':"31.929556_35.01675", 
'JALJULYE':"32.15353_34.9518", 
'JUDEIDE-MAKER':"32.933333_35.141389", 
'julis':"32.944167_35.185833", 
'BEIT JANN':"32.965278_35.379444"}
'''

dd=pd.read_csv("https://raw.githubusercontent.com/yuvadm/geolocations-il/master/cities.csv")
for el in list(dd.iterrows()):
    coords[el[1]["City"]]=[el[1]["Latitude"],el[1]["Longitude"]]
print(coords)    


coords2={}
data=[]
kkeys={}
names={}
with open("cities.json","r") as fp:
    data=json.load(fp)
    print("length")
    print(len(data))
    for el in data:
        try:
            #print(el)
            try:
                ll=coords[el["name"]]
            except:
                ll=coords[el["english_name"]]
                #ll=coords[el["english_name"]]
            coords2[el["semel_yeshuv"]]=str(ll[0])+"_"+str(ll[1])
        except:
            print("missed")
            print(el)
        names[el["name"]]=el["semel_yeshuv"]
        mm=[x.lower() for x in munis]
        if el['english_name'].lower() in mm:
            #print(el['english_name'].lower())
            kk=mm.index(el['english_name'].lower())
            kkeys[el["semel_yeshuv"]]=el['english_name']
        else:
            #shem_napa 
            kkeys[el["semel_yeshuv"]]=el['english_name']#shem_napa


print(coords2)
print(len(muni["features"]))
main_data=pd.read_csv("israeli-covid-cases.csv")
print(len(list(main_data["cityCode"].unique())))
main_data["district"]=main_data["cityCode"].astype(str).map(kkeys)
main_data["coords"]=main_data["cityCode"].astype(str).map(coords2)
#print(main_data["cityCode"].unique())
#main_data.fillna(0)
print(main_data[main_data["coords"]==0])
print(main_data["coords"].unique())
print(len(muni["features"]))
main_data.to_csv("israeli-covid-cases_coords.csv")

#dd=pd.read_csv("https://raw.githubusercontent.com/yuvadm/geolocations-il/master/cities.csv")
#print(len(list(dd["City"].map(names).unique())))


main_data0=pd.read_csv("israeli-covid-cases_coords.csv")
kl=main_data0[main_data0["coords"].isna()==True]
print(kl["district"].unique())
print(kl["city"].unique())

#print(main_data0["coords"].isna())
