import numpy as np
import matplotlib.pyplot as plt

def main():
    fig, ax = plt.subplots()
    cs = ax.contour(np.random.random((10,10)))

    callback = ContourCallback(cs)
    plt.setp(cs.collections, picker=5)
    fig.canvas.mpl_connect('pick_event', callback)

    plt.show()

class ContourCallback(object):
    def __init__(self, cs):
        self.lookup = dict(zip(cs.collections, cs.levels))
        print(cs.collections)
    def __call__(self, event):
        print(self.lookup[event.artist])

main()

