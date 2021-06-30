import pandas as pd
import geopandas as gpd
import geopy
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import matplotlib.pyplot as plt
import folium
from folium.plugins import FastMarkerCluster
import json

locator = Nominatim(user_agent="myGeocoder")
location = locator.geocode("Άνδρου,Greece")
print(location.address)
print("Latitude = {}, Longitude = {}".format(location.latitude, location.longitude))

temp={"type":"FeatureCollection","features":[]}
arr=[ 'Βορ. Τομ. Αθηνών', 'Δυτ. Τομ Αθηνών',   'Κεντρ. τομ. Αθηνών', 'Νότ. Τομ. Αθηνών', 'Πύλες και αυτοβούλως','Υπό διερεύνηση', 'Ανατολική Αττική']
#[ 'Βορ. Τομ. Αθηνών', 'Δυτ. Τομ Αθηνών',   'Κεντρ. τομ. Αθηνών', 'Λήμνου', 'Νότ. Τομ. Αθηνών', 'Πύλες και αυτοβούλως','Τήνου', 'Υπό διερεύνηση', 'Ανατολική Αττική']
#[ 'Βορ. Τομ. Αθηνών', 'Δυτ. Τομ Αθηνών',  'Θάσου', 'Θήρας', 'Ιθάκης', 'Ικαρίας', 'Καλύμνου', 'Κεντρ. τομ. Αθηνών', 'Λήμνου', 'Νότ. Τομ. Αθηνών', 'Πύλες και αυτοβούλως','Τήνου', 'Υπό διερεύνηση','Σύρου', 'Ρόδου','Καρπάθου-Κάσου', 'Ανατολική Αττική']
#[ 'Άνδρου',   'Βορ. Τομ. Αθηνών', 'Δυτ. Τομ Αθηνών',  'Θάσου', 'Θήρας', 'Ιθάκης', 'Ικαρίας', 'Καλύμνου', 'Κεντρ. τομ. Αθηνών', 'Κω', 'Λήμνου', 'Μήλου', 'Μυκόνου', 'Νάξου', 'Νότ. Τομ. Αθηνών', 'Πάρου', 'Πύλες και αυτοβούλως', 'Σποράδων','Τήνου', 'Υπό διερεύνηση','Σύρου', 'Ρόδου','Καρπάθου-Κάσου', 'Ανατολική Αττική']
for item in arr:
    try:
        location = locator.geocode(item+", Greece")
        temp0={'type': 'Feature','geometry':{'type': 'Point','coordinates': [location.longitude, location.latitude]},'properties': {'title': item}}
        temp["features"].append(temp0)
        print(temp0)
    except:
        print(item)
with open("dots_greece.json","w") as fp:
    json.dump(temp,fp)    
