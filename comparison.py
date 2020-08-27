#!/usr/bin/env python
# coding: utf-8
# ### Reading NyTimes data
# In[76]:
#importing libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
#from IPython.display import HTML
# In[77]:
#from IPython.display import display
from matplotlib.colors import LogNorm
#loading New York Times data from the webpage
nytimesdata = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv")#.fillna(0)
nytimesdata["id"]=nytimesdata["county"]+", "+nytimesdata["state"]#and nytimesdata["county"]!="Salt Lake"
nytimesdata0=nytimesdata[(nytimesdata["state"]=="Massachusetts")].groupby(["state","county","id","date"])["cases"].sum().reset_index()

nytimesdata2=nytimesdata0.pivot(index='id',columns='date',values='cases').fillna(0)
#sns.heatmap(nytimesdata2, annot=True)
n3=nytimesdata2
log_norm = LogNorm(vmin=n3.min().min()+1, vmax=n3.max().max())
#.style.background_gradient(cmap='Blues')
#print(nytimesdata2.style.background_gradient(cmap='Blues'))
#print(n3)
ax = sns.heatmap(n3,vmin=1,fmt="d",cmap="YlGnBu",norm=LogNorm())
plt.savefig("MA.png")
plt.show()

#!/usr/bin/env python
# coding: utf-8

# ### Reading NyTimes data

# In[76]:


#importing libraries
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
#from IPython.display import HTML
# In[77]:
#from IPython.display import display
from matplotlib.colors import LogNorm
#loading New York Times data from the webpage
nytimesdata = pd.read_csv("https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv")#.fillna(0)
nytimesdata["id"]=nytimesdata["county"]+", "+nytimesdata["state"]#& nytimesdata["county"]!="Salt Lake"
nytimesdata0=nytimesdata[(nytimesdata["state"]=="Massachusetts")].groupby(["state","county","id","date"])["cases"].sum().reset_index()

nytimesdata2=nytimesdata0.pivot(index='id',columns='date',values='cases').fillna(0)
#sns.heatmap(nytimesdata2, annot=True)
n3=nytimesdata2
#log_norm = LogNorm(vmin=n3.min().min()+1, vmax=n3.max().max())
#.style.background_gradient(cmap='Blues')
#print(nytimesdata2.style.background_gradient(cmap='Blues'))
#print(n3)
fig, ax = plt.subplots(figsize=(20,20))
sns.heatmap(n3,vmin=1, linewidths=.5,fmt="d",cmap="YlGnBu",norm=LogNorm(),ax=ax)
plt.savefig("NYT_MA.png")
plt.show()


jhudata = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv").fillna(0)
#Province_State
jhudata0=jhudata[(jhudata["Province_State"]=="Massachusetts")].set_index('Combined_Key')
n4=jhudata0
#UID,iso2,iso3,code3,FIPS,Admin2,Province_State,Country_Region,Lat,Long_,Combined_Key
n5=n4.drop(['UID', 'iso2','iso3','code3','FIPS','Admin2','Province_State','Country_Region','Lat','Long_'], axis=1)
print(n5)
fig, ax = plt.subplots(figsize=(20,20))
sns.heatmap(n5,vmin=1, linewidths=.5,fmt="d",cmap="YlGnBu",norm=LogNorm(),ax=ax)
plt.savefig("JHU_MA.png")
plt.show()
