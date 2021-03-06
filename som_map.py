import pandas as pd
import SimpSOM as sps
from sklearn.cluster import KMeans
import numpy as np



net = sps.somNet(20, 20, train, PBC=True)
net.train(0.01, 20000)
net.save('filename_weights')
net.nodes_graph(colnum=0)
net.diff_graph()
