

from numpyencoder import NumpyEncoder
import json
import numpy as np
from shapely.geometry import Point, Polygon
import pandas as pd
import geopandas as gpd
main_data0=pd.read_csv("israeli-covid-cases_coords.csv")
#print(main_data0)
kl=main_data0[main_data0["coords"].isna()==False]
k3=kl.groupby(["district","coords"]).count()
kkeys={}
for el in list(k3.iterrows()):
    #print(el)
    kkeys[el[0][0]]=el[0][1]
#print(kkeys)    
data=gpd.read_file("municipalities10.json")
'''
coords3={[34.978611 ,31.083056]:"רס-א רצק'",
[34.695939 ,30.977242]:"'גאדה ריב",
[34.916111 ,31.284444]: 'דייס לא',
[34.864 ,31.26]:"(טבש) קייקור ובא",
         "(טבש) דעייוו'ג ובא":[31.178502,34.745967]}
'''


dss=[]
mmls={}
for ele in list(data.iterrows()):
    kk=[]
    for el in list(kkeys.keys()):
        arr=kkeys[el].split("_")
        p1=Point(float(arr[1]),float(arr[0]))
        poly=ele[1]["geometry"]
        if poly.contains(p1)==True:
            kk.append(el)
            mmls[el]=ele[1]["MUN_ENG"]
    if len(kk)==0:
        kk.append("")
    dss.append(kk)
    
print(dss)            
data["district"]=dss            
print(mmls)            

dists=[]
for ele in list(main_data0.iterrows()):
    try:
        dists.append(mmls[ele[1]["district"]])
    except:
        try:
            tt=coords[ele[1]["City_Name"]]
            dists.append(str(tt[0])+"_"+str(tt[1]))
        except:    
            dists.append("MISSED")             
            print("MISSED", ele[1]["coords"])
    #mmls[ele[1]]
main_data0["map_districts"]=dists

main_table=main_data0[main_data0["map_districts"]!="MISSED"]
print(main_table["map_districts"].unique())
final=main_table.groupby(["map_districts","Date"])['Cumulative_verified_cases'].sum().reset_index()
name="Tel Aviv - Yafo"
print(final[final["map_districts"]==name]["Cumulative_verified_cases"])
print(main_table[main_table["map_districts"]==name]["Cumulative_verified_cases"])
pivoted_table=pd.pivot_table(final, values='Cumulative_verified_cases', index=['map_districts'],columns=['Date'], aggfunc=np.sum)
print(pivoted_table)
llk=list(pivoted_table.columns)
#print(llk[-14])

two_weeks={}
two_weeks_arrs={}
for item in list(pivoted_table.iterrows()):
    l=[int(x) if "<15" not in x else 15 for x in list(item[1].values)]
    two_weeks[item[0]]=l[-1]-l[-15]
    l2=l[-15:][::-1]
    print(l2)
    l3=[]
    ind=0
    for x in l2:
        if ind<len(l2)-1:
            y=x-l2[ind+1]
            l3.append(y)
            ind+=1    
    print(l3)
    two_weeks_arrs[item[0]]=l3
print(two_weeks)    
print(two_weeks_arrs)

with open("municipalities10.json","r") as fp:                                                                                               
    #json.dump(data,fp,separators=(', ', ': '), ensure_ascii=False,cls=NumpyEncoder)    
    data2=json.load(fp)
    for item in data2["features"]:
        item["properties"]["name"]=item["properties"]["MUN_ENG"]
        try:
            item["properties"]["value"]=two_weeks[item["properties"]["MUN_ENG"]]
        except:
            item["properties"]["value"]=0
        try:    
            item["properties"]["values"]=two_weeks_arrs[item["properties"]["MUN_ENG"]]
        except:
            item["properties"]["values"]=0
        print(item["properties"])
    with open("municipalities_new.json","w") as fp:
        json.dump(data2,fp,separators=(', ', ': '), ensure_ascii=False,cls=NumpyEncoder)  

#print(final)
'''
with open("municipalities_new.json","w") as fp:
    json.dump(data,fp,separators=(', ', ': '), ensure_ascii=False,cls=NumpyEncoder)
 
with open("dots_new.json","w") as fp:
    json.dump(data90,fp,separators=(', ', ': '), ensure_ascii=False,cls=NumpyEncoder)






["Ba'ana" 'Abu Gosh' 'No Jurisdiction' 'Abu Snan' 'Zvulun' 'Even Yehuda'
 'Um Al-Fahem' 'Ofakim' 'Or Yehuda' 'Or Akiva' 'Azor' 'El Kasum' 'Eilat'
 'Iksal' 'Elyahin' "I'eblin" "Bnei Shim'on" 'Ashdod' 'Bukata' 'Ashkelon'
 "Be'er Ya'akov" "Be'er Sheva" "Bu'eyne-Nujidat" 'Bir Al-Maksur' 'Bet Jan'
 'Beit Dagan' 'Gezer' "Bet She'an" 'Emek Hefer' 'Basma' 'Beit Shemesh'
 'Bnei Brak' 'Bnei Ayish' "Binyamina - Giv'at Ada" 'Basmat Tivon' 'Zarzir'
 'Bat Yam' "Hagalil Hatah'ton" 'Gedera' 'Brener' "Giva'at shmuel" 'Tamra'
 "Giv'atayim" 'Julis' "Jdeyde-Ma'ker" "Hagilbo'a" 'Drom Hasharon'
 'Gan Yavne' 'Daburiya' 'Dimona' 'Gane Tikva' 'Jiser A-Zarka'
 'Jish (Gush Halav)' 'jat' 'Dalyat Al-Carmel' 'Dir Al-Asad' 'Deir Hana'
 'Emek Yizrael' 'Hod Hasharon' 'Neve Midbar' 'Hertseliya' 'Zemer'
 "Zih'ron Ya'akov" 'Hadera' 'Holon' 'Hura' 'Hurfeish' 'Haifa'
 'Hatsor Haglilit' 'Harish' 'Tverya (Tiberias)' 'Tuba - Zangariya'
 "Tur'an" 'Taybe' 'Tirat Karmel' 'Yanuh - Jat' "Yavne'el" 'Yavne'
 'Nahal Sorek' 'Yehud - Monoson' "Yafi'a" 'Menashe' "Yokne'am Ilit"
 'Yeroham' 'Yerushalayim (Jerusalem)' 'Yirka' 'Kabul' 'Kawkab Abu Al-Hija'
 'Mishad' 'Kseyfe' 'Kohav Yair' "Kisrah - Smi'a" 'Kafar Bara'
 "Ka'abiya-Tabash-Hajajre" 'Nahef' 'Kfar Yasif' 'Kfar  Vradim' 'Emek Lod'
 'Kafar Kama' 'Kfar Yona' 'Kfar Kana' 'Kfar Manda' 'Natsrat (Nazareth)'
 'Bustan Al-Marj' 'Kfar Saba' 'Kafar Kasem' 'Kfar Tavor' 'Kafar kara'
 'Karmiel' 'Lehavim' 'Lod' "Hevel Modi'in" 'Lakiye' 'Mrar'
 'Mevaseret Tsiyon' 'Majd Al-krum' 'Majdel Shams' "Migdal Ha'emek"
 "Modi'in - Makabim-Re'ut" 'Mazkeret Batya' "Mazra'a" 'Meitar' "Mas'ade"
 "Mi'ilya" "Ma'alot-Tarshiha" 'Mitspe Ramon' 'Shafir' 'Misgav' 'Nahariya'
 'Natsrat Ilit' 'Hof Ashkelon' 'Nes Tsiyona' 'Nesher' 'Netivot' 'Netanya'
 'Savyon' "Sah'nin" 'Rajar' 'Al-Batuf' 'Omer' 'Ilabun' 'Ilut' 'Eyn Mahel'
 "Ma'te Yehuda" 'Eyn Kinya' 'Ako (Acre)' 'Fasuta' 'Ossfiya' 'Afula'
 'Arabe' 'Pardesiya' 'Arad' "Ar'ara" "Ar'ara Banegev" 'Hof Hacarmel'
 'furaydis' "Pki'in - Buke'a" "Ra'me" 'Pardes Hana - Karkur' 'Petah Tikva'
 'Lev Hasharon' 'Tsfat' 'Kadima - Tsoran' 'Kalanswa' 'Katsrin'
 'Kiryat Ono' 'Kiryat Ata' 'Kiryat Gat' 'Kiryat Biyalik' "Kiryat Tiv'on"
 'Kiryat Yam' "Kiryat Ye'arim" 'Kiryat Motskin' "Kiryat Mal'ahi"
 'Kiryat Ekron' 'Kiryat Shmona' "Rosh Ha'ayin" 'Rosh Pina'
 'Rishon Letsiyon' 'Rahat' 'Rehovot' 'Reyne' 'Rehasim' 'Ramla' 'Ramat Gan'
 'Ramat Yishay' 'Shoham' 'Ramat Hasharon' "Ra'anana" 'Segev-Shalom'
 'Sderot' "Ma'te Asher" 'Shlomi' "Sha'ab" 'Shfaram' 'Tel Aviv - Yafo'
 'Tel Mond' 'Tel Sheva' 'Merhavim']






Index(['Unnamed: 0', 'uid', 'city', 'cityCode', 'date', 'cumulativeVerified',
       'cumulativeRecovered', 'cumulativeDeaths', 'cumulativeTests',
       'cumulativeDiagnostics', 'district', 'coords', 'map_districts'],
      dtype='object')



Unnamed: 0                              7418
uid                                     7397
city                                  אשקלון
cityCode                                7100
date                              2020-06-19
cumulativeVerified                       292
cumulativeRecovered                      258
cumulativeDeaths                          -1
cumulativeTests                        14449
cumulativeDiagnostics                  13348
district                            ASHQELON
coords                   31.665944_34.559466

'''
main_table2=main_data0[main_data0["map_districts"]=="MISSED"]
final2=main_table2.groupby(["City_Name","Date"])['Cumulative_verified_cases'].sum().reset_index()
pivoted_table2=pd.pivot_table(final2, values='Cumulative_verified_cases', index=['City_Name'],columns=['Date'], aggfunc=np.sum)
print(pivoted_table2)


two_weeks_dots={}
for city in pivoted_table2.iterrows():
    ll=[int(x) if "<15" not in x else 15 for x in city[1].values[-15:][::-1]]
    if sum(ll)>=0:
        #print(ll,city[0])
        two_weeks_dots[city[0]]=ll[0]-ll[-1]
        
print(two_weeks_dots)
dot_coords={}
#main_table2=main_data0[main_data0["map_districts"]=="MISSED"]
for item in main_table2.iterrows():
    if item[1]["City_Name"] not in list(dot_coords.keys()): 
        #print(item[1]["city"],item[1]["coords"])
        coord_pair=str(item[1]["coords"]).split("_")
        if len(coord_pair)>1:
            dot_coords[item[1]["City_Name"]]=[coord_pair[1],coord_pair[0]]



dot_json={"type": "FeatureCollection","features": []}

for item in list(two_weeks_dots.keys()):
    #print(item,two_weeks_dots[item],dot_coords[item])
    try:
        temp={"type": "Feature","properties":{"name":item,"value":two_weeks_dots[item]},"geometry":{ "type": "Point","coordinates":dot_coords[item]}}
        dot_json["features"].append(temp)
    except:
        continue
        #print(item,two_weeks_dots[item],dot_coords[item])
print(dot_json)    
with open("dots_new.json","w") as fp:                                                                                                                                               
    json.dump(dot_json,fp,separators=(', ', ': '), ensure_ascii=False,cls=NumpyEncoder)   
'''
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "dbh": 5
      },
      "geometry": {
        "type": "Point",
        "coordinates": [
          -79.93345,
          40.46111
        ]
      }
    }
  ]
}


'''
