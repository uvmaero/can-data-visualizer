import can, multiprocessing, time
from PyQt5 import QtWidgets, QtCore
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import sys  # We need sys so that we can pass argv to QApplication
import os

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)
        self.x = list(range(0,2))
        self.y = list(range(0,2))
        self.graphWidget.setBackground('w')
        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line =  self.graphWidget.plot(self.x, self.y, pen=pen)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(50)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()
    
    def update_plot_data(self):

        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.
        self.y = self.y[1:]  # Remove the first 
        self.y.append()  # Add a new random value.

        self.data_line.setData(self.x, self.y)  # Update the data.





def can_reader(q):
    bus = can.Bus(interface='socketcan',channel='vcan0',receive_own_messages=True)
    for message in bus:
        data=list(message.data)
        #print(message.data.hex())
        q.put(data)

def can_printer(q):
    while True:
        print(q.get())
    #app = QtWidgets.QApplication(sys.argv)
    #w = MainWindow()
    #w.show()
    #sys.exit(app.exec_())

def main():
    q = multiprocessing.Queue()
    p1=multiprocessing.Process(target=can_reader, args=(q,))
    p2=multiprocessing.Process(target=can_printer, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print("done")

main()