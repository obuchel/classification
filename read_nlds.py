import geopandas as gpd

url="http://ec2-35-153-102-199.compute-1.amazonaws.com/elastic/NLD_adm2-1.json"

df = gpd.read_file(url)
print(df)
df.drop('geometry',axis=1).to_csv(r'nlds.csv') 
