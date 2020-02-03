# can-data-visualizer
A simple Python web utility to plot CANbus data in real time.

In the current implementation, `can-plotter.py` continuously plots, clears, and re-plots the data, which is inefficient and can lag when plotting data from popular IDs... but it's also the only way I've gotten it to work. I don't see how FuncAnimation can work because the CAN message reception is stuck in a `for` loop.

Resources that may help in the future:
https://github.com/ceyzeriat/joystick/
https://github.com/lorenzschmid/dynplot
