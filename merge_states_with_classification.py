import json
import pandas as pd

fps=pd.read_csv("state_fps.csv",sep="	")[["FIPS","Name"]].set_index("FIPS")
fps0=fps.to_dict("index")
#print(fps0)
fips={}
for item in list(fps0.keys()):
    fips[item]=str(fps0[item]["Name"])

print(fips)

#us_counties_colors.json
#us_states_colors.json
colors={"red":3,"yellow":2,"green":1,"darkgreen":1}
with open("us_counties_colors_10.json","r") as fp:
    data=json.load(fp)
    for item in list(data.keys()):
        print(item)
        print(len(list(data[item].keys())))
#states5.json

with open("counties5.json","r") as fp:
    geo=json.load(fp)
    for item in geo["features"]:
        #print(data["840"+str(item["properties"]["GEOID"])])
        try:
            #item["properties"]["Name"]=fips[int(item["properties"]["STATEFP"])]
            #item["properties"]["values"]=[colors[x[0]] for x in list(data[item["properties"]["Name"]].values())]
            vals=[colors[x[0]] for x in list(data["840"+str(item["properties"]["GEOID"])].values())]
            ind=0
            for el in vals:
                item["properties"][str(ind)]=str(vals[ind])
                ind+=1
            #print(item["properties"])
        except:
            print(item)
            continue
print(geo)            
with open("counties_colors2_10.json","w") as fp:
    json.dump(geo,fp)

'''    
#print(list(data["Alabama"].keys()))
with open("counties_dates.json","w") as fp:
    json.dump(list(data["Alabama"].keys()),fp)
'''
