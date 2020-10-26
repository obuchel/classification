
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
            tt=coords[ele[1]["city"]]
            dists.append(str(tt[0])+"_"+str(tt[1]))
        except:    
            dists.append("MISSED")             
            print("MISSED", ele[1]["coords"])
    #mmls[ele[1]]
main_data0["map_districts"]=dists

main_table=main_data0[main_data0["map_districts"]!="MISSED"]
print(main_table["map_districts"].unique())
final=main_table.groupby(["map_districts","date"])['cumulativeVerified'].sum().reset_index()
name="Tel Aviv - Yafo"
print(final[final["map_districts"]==name]["cumulativeVerified"])
print(main_table[main_table["map_districts"]==name]["cumulativeVerified"])
pivoted_table=pd.pivot_table(final, values='cumulativeVerified', index=['map_districts'],columns=['date'], aggfunc=np.sum)
print(pivoted_table)
llk=list(pivoted_table.columns)
#print(llk[-14])

two_weeks={}
two_weeks_arrs={}
for item in list(pivoted_table.iterrows()):
    l=list(item[1].values)
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
