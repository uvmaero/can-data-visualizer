from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
from multiprocessing import Process, Manager, Queue
import sched, time, threading, can

# This program is the literal devil. You have been warned. I don't know what's going on



def display(name,q):
    app2 = QtGui.QApplication([])

    win2 = pg.GraphicsWindow(title="*SCREAMING*")
    win2.resize(1000,600)
    win2.setWindowTitle('It just works')
    p2 = win2.addPlot(title="This is a plot of CAN data")
    curve = p2.plot(pen='y')
    x_np = []
    y_np = []
    def update(curve,q,x,y):
        item = q.get()
        y.append(item[1])
        x.append(item[0])
        if len(x) >= 200:
            del x[0]
            del y[0]
        
        print(x)
        curve.setData(x,y)
        
        
        


    timer = QtCore.QTimer()
    timer.timeout.connect(lambda: update(curve,q,x_np,y_np))
    timer.start(0)

    QtGui.QApplication.instance().exec_()

def io(running,q):
    t = 0
    bus = can.Bus(interface='socketcan',channel='vcan0',receive_own_messages=True)
    while running.is_set():
        for message in bus:
            s=list(message.data)[0]
            t += 1
            q.put([t,s])
    print("Done")


q = Queue()

run = threading.Event()
run.set()

t = threading.Thread(target=io, args=(run,q))
t.start()

p = Process(target=display, args=('bob',q))
p.start()