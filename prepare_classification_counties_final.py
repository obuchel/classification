import json

import numpy as np
import pandas as pd

output_directory = '/Users/olgabuchel/Downloads/DeckSample/classification_project'

kkeys=[]
arr=[]
nnn=7

def second_smallest(numbers):
    m1, m2 = int(), int()
    for x in numbers:
        if int(x) <= int(m1):
            m1, m2 = int(x), int(m1)
        elif int(x) < int(m2):
            m2 = int(x)
    return m2
def best_fit_slope(xs,ys):
    m = (((np.mean(xs)*np.mean(ys)) - np.mean(xs*ys)) /
         ((np.mean(xs)**2) - np.mean(xs**2)))
    return m

# Use canned CSV file, so we can compare results.
# Original:
#   data=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv')

data = pd.read_csv('data/time_series/time_series_covid19_confirmed_US.csv')
# remove more recent values, example data goes up to "5/22/20"
data = data.iloc[:, :133]
# print(data.tail())
assert data.columns[-1] == '5/22/20'
# import sys
# sys.exit(0)

e_dataframe=data.set_index("Combined_Key")
ids=data[["UID", "Combined_Key"]].to_dict('records')
recs=data["Combined_Key"].to_list()

e_dataframe0=e_dataframe.drop(columns=['UID','iso2','iso3','code3','FIPS','Admin2','Province_State','Country_Region','Lat','Long_'])
e_dataframe11=e_dataframe0.transpose()
e_dataframe1=e_dataframe11
dats=list(e_dataframe1.index)
#print(dats)
#dats=kkeys[1:]
dats2=[]
decimals=[]
elapsed_days=[]
ind=22
for el in dats:
   dats2.append(ind)
   dec=2020+(ind/366)
   elapsed_days.append(ind-20)
   decimals.append(dec)
   ind+=1

e_dataframe1.insert(0, "Day_Year",dats2, True)
e_dataframe1.insert(0, "Decimals",decimals, True)
e_dataframe1.insert(0, "Elapsed_days",elapsed_days, True)

tim=list(e_dataframe0.columns)
tim.pop(0)

ind4=0
aar=[]
aar1=[]


for name in e_dataframe1.columns[3:]:
    y50=e_dataframe1[name][len(e_dataframe1[name])-20:]
    y5=[y-e_dataframe1[name][len(e_dataframe1[name])-21] for y in y50]
    #print(max(y5))
    y=e_dataframe1[name]
    v=[]
    ind3=0
    for e in e_dataframe1[name]:
        if ind3<len(e_dataframe1[name])-2:
            v.append(int(e_dataframe1[name][ind3+1])-int(e))
        else:
            v.append(v[len(v)-1])
        ind3+=1
    x=e_dataframe1[e_dataframe1.columns[0]]    
    ind=0
    y1=[]
    for el in y:
        if ind>=1 and ind<=len(y)-2:
            y0=(int(y[ind+1])-int(y[ind-1]))/2
            y1.append(y0)
        elif ind==0:
            y0=(int(y[ind+1])-int(el))/2
            y1.append(y0)
        else:
            y0=(int(el)-int(y[ind-1]))/2
            y1.append(y0)
        ind +=1
    x2=x[9:]
    tim2=tim[4:len(tim)-5]
    print(tim2)
    '''
    y3=[]
    ind1=0
    for el in y1:
        if ind1>=5 and ind1<=len(y1)-5:
            y3.append(np.mean(y1[ind1-5:ind1+5]))      
        ind1 +=1
    '''
    y3=pd.DataFrame(y1,columns=["a"]).rolling(window=10).mean()['a'].to_list()[9:]
    print(y3)
    ys=y3[len(y3)-24:]
    xs=x[len(x)-29:len(x)-5] #last 24 days
    ind2=0
    start=[]
    start2=[]
    if int(np.max(y))>0:
        vv=[int(x) for x in y.to_list() if x!=min(y3)]
        start.append(y.to_list().index(vv[0]))
    else:
        start.append(0)
    threshold=1     
    if len(start)>0:
        #if name=="Ventura, California, US":
        #  print(v,y,v[len(v)-10:],np.mean(v[len(v)-10:]),name)
        #print(v[len(v)-10:],np.mean(v[len(v)-10]),name)
        max0=np.max(y3)
        min0=np.min(ys)
        if max0>0:
            ratio=y3[len(y3)-1]/max0
            if  ratio>=0.79:
                if int(np.mean(v[len(v)-10:]))>=threshold:  
                  color="red"
                  plt.title(name)
                else:
                  color="green"
                  plt.title(name)
            elif ratio<=0.1:
                if int(np.mean(v[len(v)-10:]))>=threshold:
                    ratio=ratio
                    #print(name,v)
                    plt.title(name)
                    color="yellow"
                    plt.plot(x2,y3,color="yellow")
                else:
                    ratio=ratio
                    plt.title(name)
                    color="green"
                    plt.plot(x2,y3,color="green")
            elif ratio>=0.4 and ratio<0.79:
                if int(np.mean(v[len(v)-10:]))>=threshold:
                  plt.plot(x2,y3,color="orange")
                  color="orange"
                  plt.title(name)
                else:
                  plt.plot(x2,y3,color="green")
                  color="green"
                  plt.title(name)
                #plt.savefig("classification_3days/7days_counties/"+name+"_orange.png")
            elif ratio>0.1 and ratio<0.4:
                if int(np.mean(v[len(v)-10:]))>=threshold:
                  plt.plot(x2,y3,color="yellow")
                  color="yellow"
                  plt.title(name)
                else:
                  color="green"
                  plt.plot(x2,y3,color="green")
                  plt.title(name)
            if name=="Ventura, California, US":
              print(np.mean(v[len(v)-10:]),v[len(v)-10:],color,ratio)
            with open(output_directory + '/classification/data_counties_' + str(ids[recs.index(name)]["UID"]) + '.json', 'w') as outfile:
                json.dump({"dates":tim2,"max_14":int(max(y5)),"max":int(max(y)),"value":y3,"time":tim,"original_values":v},outfile)
            aar.append({"color":color,"province":name.split(",")[0],"country":name.split(",")[1],"id":"new_id_"+str(ind4),"value1":ratio, "dates":tim2,"value":y3})
            aar1.append({"n":name,"id":ids[recs.index(name)]["UID"],"v":ratio,"c":color,"max":int(max(y5))})
            ind4+=1
        else:
            #print(name,y3)
            ratio=0
            color="green"
            with open(output_directory + str(ids[recs.index(name)]["UID"]) + '.json', 'w') as outfile:
                json.dump({"dates":tim2,"max_14":int(max(y5)),"max":int(max(y)),"value":y3,"time":tim,"original_values":v},outfile)
            aar.append({"color":color,"province":name.split(",")[0],"country":name.split(",")[1],"id":"new_id_"+str(ind4),"value1":ratio, "dates":tim2,"value":y3})
            aar1.append({"n":name,"id":ids[recs.index(name)]["UID"],"v":ratio,"c":color,"max":int(max(y5))})
            ind4+=1

with open('%s/classification/data_counties.json' % output_directory, 'w') as outfile:
    json.dump(aar,outfile)

with open('%s/classification/classification_ids_counties2.json' % output_directory, 'w') as outfile:
    json.dump(aar1,outfile)


