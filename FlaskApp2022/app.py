from flask import Flask
import can
app = Flask(__name__)

can.rc['interface'] = 'socketcan'
can.rc['channel'] = 'vcan0' # vcan0 for virtual can, can0 for live data
can.rc['bitrate'] = 500000
bus = can.interface.Bus()

@app.route('/')
def hello_world():
	return 'Hello, World! Welcome to the future home of the can data visualizer!'



@app.route('/rawdata')
def show_data():
	while True:
		count = 0
		try:
			for message in bus:
				count += 1
				print(f'{message}')
				return f'{count}'
		except:
			return 'An error has been raised'
