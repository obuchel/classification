import json

import numpy as np
import pandas as pd
import os
#from prep_canada_data import stage_latest                                                                                                                                          
#https://cdn.mbta.com/archive/archived_feeds.txt                                                                                                                                    
#date_of_analysis='3/5/21'                                                                                                                                                          
from datetime import date
#date_of_analysis='03/07/21'                                                                                                                                                        
date_of_analysis=date.today().strftime("%m/%d/%y")
print(date_of_analysis)

output_directory = 'output_france'
os.makedirs(output_directory + '/classification', exist_ok=True)

# Use canned CSV file, so we can compare results to earlier runs of the script.                                                                                                     
use_canned_file = False

data0=pd.read_csv("donnees-tests-covid19-labo-quotidien-2020-05-29-19h00.csv",sep=';',engine='python')
print(data0.columns)
df2=data0.groupby(["dep","jour"])["nb_pos"].sum().reset_index()
c1=['2020-05-14','2020-05-15','2020-05-16','2020-05-17','2020-05-18','2020-05-19','2020-05-20','2020-05-21','2020-05-22','2020-05-23','2020-05-24','2020-05-25','2020-05-26','2020-05-27','2020-05-28','2020-05-29']
df3=df2[np.isin(df2['jour'], c1, invert=True)]
print(df3)
df4=df3.rename(columns={'dep': 'Combined_Key', 'jour':'jour','nb_pos': 'P'})
data = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/406c6a23-e283-4300-9484-54e78c8ae675',sep=';',engine="python")
data=data[data['cl_age90']==0]
data["Combined_Key"]=data["dep"]
df_=data.groupby(["Combined_Key","jour"])["P"].sum().reset_index()
df=pd.concat([df4, df_])
e_dataframe = df.set_index("Combined_Key")
ids = df[["Combined_Key"]].to_dict('records')
recs = df["Combined_Key"].to_list()
print(ids)
e_dataframe0 = e_dataframe#drop(columns=['dep'])                                                                                                                                   
e_dataframe1 = pd.pivot_table(e_dataframe0, values='P', index=['jour'],columns=['Combined_Key'],aggfunc=np.sum)
print(e_dataframe0)
print(len(e_dataframe1.columns))
# 977 to Saint Barthélemy and 978 to Saint Martin
#975 (Saint-Pierre and Miquelon)
kkeys={'977':'Saint Barthélemy','978':'Saint Martin','975':'Saint-Pierre and Miquelon'}
with open("depatrements_avec_outre_mer.geojson","r") as fp:
    map_data=json.load(fp)
    for item in map_data["features"]:
        #'code': '971', 'nom'
        print(item["properties"])
        kkeys[item["properties"]["code"]]=item["properties"]["nom"]
e_dataframe10=e_dataframe1.rename(columns=kkeys).fillna(0)
print(e_dataframe10)



e_dataframe10.index = pd.to_datetime(e_dataframe10.index, dayfirst=True, format='%Y-%m-%d')
e_dataframe10.sort_index(inplace=True)
#df.drop('National Total', inplace=True, axis=1)
data2 = e_dataframe10[e_dataframe10.sum().sort_values(ascending=False).index].astype(int)
print(data2)
cols=list(data2.columns)
cols1=list([str(x).split(" ")[0] for x in data2.index])
kkd0=data2.sum(axis = 0, skipna = True).to_dict()


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
item0=0
arrs=[]
for item in data2.iterrows():
    it=0
    for el in item[1].values:
        if cols[it]!="data":#,ll[cols[it]])                                                                                                                                         
            if el<0:
                el=0
            arrs.append({"x":cols1[item0],"y":str(cols[it]),"z":int(el),"p":"France"})
        it+=1
    item0+=1
print(arrs)                                                                                                                                                                       
print(cols)                                                                                                                                                                       
print(cols1)                                                                                                                                                                      
#print(kkd)                                                                                                                                                                        
print(kkd0)  
with open("fire_france.json", "w") as fp:
    json.dump(arrs,fp)
