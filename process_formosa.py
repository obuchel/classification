import pandas as pd
import geopandas as gpd

data=pd.read_csv("/Users/olgabuchel/Downloads/SUMMARY FORMOSA COVID/POSTIVES DETAIL AS OF 31_3_21-Table 1.csv")
print(data["PLACE OF ORIGIN"].unique())
data2=gpd.read_file("https://obuchel.github.io/classification/ARG_states.json")
print(data2)
kkeys={"SANTA CRUZ":[-48.807812,-69.972077],"JUJUY":[-24.196037,-65.291536],"SANTA  CRUZ":[-48.807812,-69.972077]}
ll=[]
for el in data["PLACE OF ORIGIN"].unique():
    #print(el.lower())
    for item in data2.iterrows():
        if el.lower()==item[1]["NAME_1"].lower():
            #print(item[1]["geometry"].centroid)
            llk=item[1]["geometry"].centroid.coords[0]
            if el not in list(kkeys.keys()):
                kkeys[el]=[llk[0],llk[1]]
        else:
            if el not in ll and el not in list(kkeys.keys()):
                ll.append(el)
#print(kkeys)
#print(ll)
data3=pd.read_csv("formosa_coords.csv",quotechar="'")
print(data3)
for item in data3.iterrows():
    kkeys[item[1]["City"]]=[item[1]["lat"],item[1]["long"]]
print(kkeys)
data["time"]=pd.to_datetime(data["DATE"],format="%m/%d/%y").dt.strftime('%s')
data["coords_lat"]=[kkeys[x][0] for x in data["PLACE OF ORIGIN"]]
data["coords_long"]=[kkeys[x][1] for x in data["PLACE OF ORIGIN"]]
data["coords_lat1"]=[-26.17753 for x in data["PLACE OF ORIGIN"]]
data["coords_long1"]=[-58.17814 for x in data["PLACE OF ORIGIN"]]
data.to_csv("formosa_data.csv")
