import can
import asyncio
import matplotlib.pyplot as plt
from dynplot import dynplot
from matplotlib.animation import FuncAnimation

arbid_x=int(input('Arbitration id? '),16)
mult=float(input('Multiplier? '))

bus = can.Bus(interface='socketcan',
              channel='vcan0',
              receive_own_messages=True)

time_1=[0]
data_1=[0]
arbid_1=[0]

dplt=dynplot()
for message in bus:
    if message.arbitration_id == arbid_x:
        #print(message.timestamp, message.data[0], message.arbitration_id)
    
        time_1.append(message.timestamp)
        data_1.append(mult*message.data[0])
        arbid_1.append(message.arbitration_id)

        plt.cla()
        plt.plot(time_1,data_1)
        plt.style.use('fivethirtyeight')
        plt.show(block=False)
        plt.pause(0.00001)
    
        while time_1[0]<(time_1[-1]-30):
            del time_1[0]
            del data_1[0]
            del arbid_1[0]
        

##def animate(i):
##    while time_1[0]<(time_1[-1]-30):
##        del time_1[0]
##        del data_1[0]
##        del arbid_1[0]
##
##    plt.cla() #clear old lines
##    plt.plot(time_1, data_1, label='Data 1')
##    
##    #plt.plot(x, y2, label='Data 2')
##
##    plt.legend(loc='upper left') #static location of legend
##    plt.tight_layout() #keeps things on screen
##
##
##ani = FuncAnimation(plt.gcf(), animate, interval=100)
##
##plt.style.use('fivethirtyeight')
##plt.show()
