from collections import deque
import random
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def animate(i):
    data = pd.read_csv('data.csv')
    x = data['time_1'].tolist()
    y1 = data['data_1'].tolist()
    arbid_1 = data['arbid_1'].tolist()

    while x[0]<(x[-1]-30):
        del x[0]
        del y1[0]

    plt.cla() #clear old lines
    plt.plot(x, y1, label='Data 1')
    
    #plt.plot(x, y2, label='Data 2')

    plt.legend(loc='upper left') #static location of legend
    plt.tight_layout() #keeps things on screen


ani = FuncAnimation(plt.gcf(), animate, interval=100)

plt.style.use('fivethirtyeight')
plt.show()
