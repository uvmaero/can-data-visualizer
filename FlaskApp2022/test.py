from flask import Flask
import can

can.rc['interface'] = 'socketcan'
can.rc['channel'] = 'vcan0' # vcan0 for virtual can, can0 for live data
can.rc['bitrate'] = 500000
bus = can.interface.Bus()


for message in bus:
	print(f'{message}')
