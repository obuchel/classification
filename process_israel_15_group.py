

from numpyencoder import NumpyEncoder
import json
import numpy as np
from shapely.geometry import Point, Polygon
import pandas as pd
import geopandas as gpd
main_data0=pd.read_csv("israeli-covid-cases_coords.csv")
main_data0["Cumulative_verified_cases"]=[int(x.replace("<","")) for x in main_data0["Cumulative_verified_cases"].to_list()]
#print(main_data0)
kl=main_data0[main_data0["coords"].isna()==False]
k3=kl.groupby(["district","coords"]).count()
kkeys={}
for el in list(k3.iterrows()):
    #print(el)
    kkeys[el[0][0]]=el[0][1]
#print(kkeys)    
data=gpd.read_file("municipalities11.json")
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
    l=[int(x) for x in list(item[1].values)]
    two_weeks[item[0]]=l[-1]-l[-15]
    l2=l[-15:]#[::-1]
    #print(item[0],l2)
    l3=[]
    ind=0
    for x in l2:
        if ind<len(l2)-1:
            y=l2[ind+1]-x
            l3.append(y)
            ind+=1    
    print(l3)
    two_weeks_arrs[item[0]]=l3
'''
print(two_weeks)
print(two_weeks["Kohav Yair"])
print(two_weeks["Ramat Gan"])
print(two_weeks_arrs["Kohav Yair"])
print(two_weeks_arrs["Ramat Gan"])
'''



with open("municipalities11.json","r") as fp:                                                                                               
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


main_table2=main_data0[main_data0["map_districts"]=="MISSED"]
final2=main_table2.groupby(["City_Name","Date"])['Cumulative_verified_cases'].sum().reset_index()
pivoted_table2=pd.pivot_table(final2, values='Cumulative_verified_cases', index=['City_Name'],columns=['Date'], aggfunc=np.sum)
print(pivoted_table2)


two_weeks_dots={}
for city in pivoted_table2.iterrows():
    ll=[int(x) for x in city[1].values[-15:][::-1]]
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
        print(item)
        continue
        #print(item,two_weeks_dots[item],dot_coords[item])
print(dot_json)    
with open("dots_new.json","w") as fp:                                                                                                                                              
    json.dump(dot_json,fp,separators=(', ', ': '), ensure_ascii=False,cls=NumpyEncoder)   

pivoted_table.to_csv("pivoted_israel.csv")
