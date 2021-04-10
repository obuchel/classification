from sktime.datasets.base import load_italy_power_demand
import pandas as pd
data = pd.read_csv("/Users/olgabuchel/downloads/decksample/classification_project/canada/toronto/toronto_data.csv").fillna(0)
data2 = load_italy_power_demand()
import numpy as np
import matplotlib.pyplot as plt 

#print(data.columns)


# Reshape the data so each series is a column and call the dataframe.corr() function 
distance_matrix = data.corr()
#print(distance_matrix.columns)
#print(pd.concat([series for series in data['dim_0'].values], axis=1).corr())


from sktime.distances.elastic_cython import dtw_distance

# Italy Power Demand time series are loaded in a pd.Series format.
# The dtw_distance function expects series to be shaped as a (l, m) array, 
# where l=length of series, m=# dimensions           
series_list = list(distance_matrix.columns)
print(series_list)
for i in range(len(series_list)):
    length = len(data[series_list[i]])
    series_list[i] = data[series_list[i]].values.reshape((length, 1))
print(series_list)    

# Initialize distance matrix
n_series = len(list(distance_matrix.columns))
distance_matrix = np.zeros(shape=(n_series, n_series))

# Build distance matrix
for i in range(n_series):
    for j in range(n_series):
        #x = distance_matrix[list(distance_matrix.columns)[i]]
        #y = list(distance_matrix.columns)[j]
        x = series_list[i]
        y = series_list[j]
        if i != j:
            dist = dtw_distance(x, y)
            distance_matrix[i, j] = dist
print(distance_matrix)            
            
from scipy.cluster.hierarchy import single, complete, average, ward, dendrogram

def hierarchical_clustering(dist_mat, method='complete'):
    if method == 'complete':
        Z = complete(distance_matrix)
    if method == 'single':
        Z = single(distance_matrix)
    if method == 'average':
        Z = average(distance_matrix)
    if method == 'ward':
        Z = ward(distance_matrix)
    
    fig = plt.figure(figsize=(16, 8))
    dn = dendrogram(Z)
    plt.title(f"Dendrogram for {method}-linkage with correlation distance")
    plt.show()    
    return Z

linkage_matrix = hierarchical_clustering(distance_matrix)
from scipy.cluster.hierarchy import fcluster

# select maximum number of clusters
cluster_labels = fcluster(linkage_matrix, 5, criterion='maxclust')
print(np.unique(cluster_labels))
print(len(list(cluster_labels)))
print(len(list(data.columns)))
print(list(cluster_labels))
print(list(data.columns))    
'''
#>> 4 unique clusters
cluster_labels = fcluster(linkage_matrix, 4, criterion='maxclust')
print(np.unique(cluster_labels))
#>> 10 unique clusters

# hand-select an appropriate cut-off on the dendrogram
cluster_labels = fcluster(linkage_matrix, 600, criterion='distance')
#/Users/olgabuchel/Downloads/DeckSample/classification_project/time_clustering.py print(cluster_labels)
print(np.unique(cluster_labels))
#>> 3 unique clusters
cluster_labels = fcluster(linkage_matrix, 800, criterion='distance')
print(np.unique(cluster_labels))
#>> 2 unique clusters

#/Users/olgabuchel/Downloads/DeckSample/classification_project/time_clustering.py
#/Users/olgabuchel/Sites/to_Olha/visualization_working_june27/twitter/text_analysis/nlp_course/machine_learning_examples-master/unsupervised_class/hcluster.py
#/Users/olgabuchel/myAnaconda/data/movies/prepare_classification3.py
#https://towardsdatascience.com/how-to-apply-hierarchical-clustering-to-time-series-a5fe2a7d8447

print(data)
#https://github.com/gedeck/practical-statistics-for-data-scientists
#https://towardsdatascience.com/5-free-books-to-learn-statistics-for-data-science-768d27b8215
'''
