





# coding: utf-8

# In[144]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_rows', 100)
pd.options.display.max_rows = 999
pd.set_option('display.max_colwidth', 200)
import glob
import tqdm
import mysql.connector as mysql
import time
city_names=pd.read_csv('translate_city_names.csv')
city_names.set_index('original',drop=True,inplace=True)
city_names_dict = city_names.to_dict()['translation']

data_folder = 'Other/*.xlsx'
files = glob.glob(data_folder)
print(files)
xls = pd.ExcelFile(files[0])
names = xls.sheet_names
df = pd.read_excel(files[0],skiprows=4,sheet_name=names[0]).dropna(axis='columns')
df.columns = ['City',
'Population as of 2018',
"Number of tests so far",
"Verified patients discovered so far",
"Number of recoverers",
"The growth rate of verified patients in the last 3 days",
"The number of verified patients added in the last 3 days",
"Actual morbidity rate ** per 100,000"]

lst_files = []
for ind , f in enumerate(files): 
    xls = pd.ExcelFile(f)
    names = xls.sheet_names
    sheet_name = 'כלל הארץ לפרסום'
    df = pd.read_excel(f,skiprows=4,sheet_name=sheet_name).dropna(axis='columns')
    #print(ind)
    df.columns=['City',
    'Population as of 2018',
    "Number of tests so far",
    "Verified patients discovered so far",
    "Number of recoverers",
    "The growth rate of verified patients in the last 3 days",
    "The number of verified patients added in the last 3 days",
    "Actual morbidity rate ** per 100,000"]
    #df['file_number'] = ind
    date_str = f[6:-5].split('_')
    date_str2 = f"{date_str[1]}/{date_str[0]}/{date_str[2]}"
    print(date_str,f)
    try:
        df['dates'] = pd.to_datetime(date_str2)
        print("1")
        print(date_str2)
    except:
        df['dates'] = date_str2
        print("2")
        print(date_str2)    
    #df['file_name'] = f
    lst_files.append(df)
df_all = pd.concat(lst_files)
df_all.sort_values(by='dates')
df_all.reset_index(inplace=True,drop=True)

df_all.to_csv('ISRL.csv')


# In[143]:


df_all.City.nunique()

