from __future__ import print_function
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import can
can.rc['interface'] = 'socketcan'
can.rc['channel'] = 'vcan0' # vcan0 for virtual can, can0 for live data
can.rc['bitrate'] = 500000
bus = can.interface.Bus()

def sendData(arb_id, info):

    msg = can.Message(arbitration_id=int(arb_id,16),
                      data= info,
                      is_extended_id=True)

    try:
        bus.send(msg)
        print("Message sent on {}".format(bus.channel_info))
    except can.CanError:
        print("Message NOT sent")

def getData():
    for message in bus:
        if message.arbitration_id == 0x0C0:
            data = message.data[0]
            print(data)

if __name__ == '__main__':
    sendData('1c', [0,25,0,1,3,4,1])
    getData();

