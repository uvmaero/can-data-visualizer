import can
import csv
import random
import time
import asyncio

#create a bus instance

arbid_x=int(input('Arbitration id? '))
mult=float(input('Multiplier? '))

bus = can.Bus(interface='socketcan',
              channel='vcan0',
              receive_own_messages=True)

# send a message
#message = can.Message(arbitration_id=123, is_extended_id=True,
#                      data=[0x11, 0x22, 0x33])
#bus.send(message, timeout=0.2)

#csvfile setup
x_value = 0
data_1 = 0
arbid_1 = 0

fieldnames = ['time_1', 'data_1', 'arbid_1']


csv_file=open('data.csv', 'w')
csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
csv_writer.writeheader()
csv_file.close()

#loop and write
while True:
    with open('data.csv', 'a') as csv_file:
        message = bus.recv()	#wait until a message is received
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        try:
            info = {
                'time_1': message.timestamp,
                'data_1': mult*message.data[0],
                'arbid_1': message.arbitration_id,
            }
            if message.arbitration_id == arbid_x:
                csv_writer.writerow(info)
                print(message.timestamp, message.data[0], message.arbitration_id)
        except:
            print('no byte')
    #c = '{0:f} {1:x} {2:x} '.format(message.timestamp, message.arbitration_id, message.dlc)
    #s=''
    #for i in range(message.dlc ):
    #    s +=  '{0:x} '.format(message.data[i])
    #    print(' {}'.format(s))
