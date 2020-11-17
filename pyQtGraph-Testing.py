from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from multiprocessing import Process, Manager, Queue
import sched, time, threading, can

class Superplot():
    def __init__(self,name):
        self.name = name
        self.x = list(range(0,2))
        self.y = list(range(0,2))

    def start(self):
        self.q = Queue()
        self.p = Process(target=self.run)
        self.p.start()
        return self.q

    def join(self):
        self.p.join()

    def _update(self):
        
        item = self.q.get()
        print(item)
        print(self.q.qsize())
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.
        self.y = self.y[1:]  # Remove the first 
        self.y.append(item[0])  # Add a new random value.
        self.curve.setData(self.x, self.y)  # Update the data.

    def run(self):
        app = QtGui.QApplication([])

        win = pg.GraphicsWindow(title="Basic plotting examples")
        win.resize(1000,600)
        win.setWindowTitle('pyqtgraph example: Plotting')
        plot = win.addPlot(title=self.name)
        self.curve = plot.plot(pen='y')

        timer = QtCore.QTimer()
        timer.timeout.connect(self._update)
        timer.start(50)

        app.exec_()

bus = can.Bus(interface='socketcan',channel='vcan0',receive_own_messages=True)
def io(q):
    for message in bus:
        data=list(message.data)
        print(message.data.hex())
        q.put(data[::2])
    

# create the plot
s = Superplot("somePlot")
# get the queue used to exchange data
q = s.start()

# start IO thread
t = threading.Thread(target=io, args=(q,))
t.start()


print("Waiting for IO thread to join...")
t.join()
print("Waiting for graph window process to join...")
s.join()
print("Process joined successfully. C YA !")