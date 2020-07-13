

import geopandas as gpd
import matplotlib.pyplot as plt
import libpysal as lp
import pysal as ps
districts=gpd.read_file("berlin.geojson")
w_queen=ps.lib.weights.KNN.from_dataframe(districts,k=2)
#print(w_queen.neighbors)
print(list(w_queen[2]))
w_queen[0].plot(districts)
#http://darribas.org/gds19/content/labs/lab_05.html
