# can-data-visualizer
A simple Python web utility to plot CANbus data in real time.

In this first implementation, `can-rw.py` listens to vcan0 data and writes new message contents to a csv file called `data.csv` using the Python `csv` library. Then, `can-plotter.py` uses Matplotlib to graph the data in real-time.
