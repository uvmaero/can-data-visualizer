# CAHPRI
# Missy, Kelley, George
# CS121 Final Project
# May 1, 2020
# Flask web app to serve as interface for the website. The various app route functions will
# get data from an external script and render html templates with live data.

#imports
import json
import random
import time
import can
from datetime import datetime

from flask import Flask, render_template, request, Response

app = Flask(__name__)

can.rc['interface'] = 'socketcan'
can.rc['channel'] = 'vcan0' # vcan0 for virtual, can0 for live
can.rc['bitrate'] = 500000
bus = can.interface.Bus()
data = 0

# Generate json_dump file for data. This uses external script "can_logger"
def get_message_value(can_id, bit):
        while True:
            for message in bus:
                if message.arbitration_id == can_id:
                    data = message.data[bit]
                else:
                    data=0
            
            json_data = json.dumps(
                    {'time':datetime.now().strftime('%H:%M:%S'), 'value': data})
            yield f"data:{json_data}\n\n"
            # delay system to ensure stability
            time.sleep(.1)


# Landing Page
@app.route('/')
def index():
    return render_template('layout.html')

# ride Height template and Data Streams
@app.route('/rideHeight')
def rideHeightTemp():
    return render_template("rideHeight.html")

@app.route('/rideHeightData1')
def rideHeightData1():
    # values are hardcoded here since they will never change. 
    return Response(get_message_value(0x032, 0), mimetype='text/event-stream')

@app.route('/rideHeightData2')
def rideHeightData2():
    return Response(get_message_value(0x032, 2), mimetype='text/event-stream')

@app.route('/rideHeightData3')
def rideHeightData3():
    return Response(get_message_value(0x01C, 2), mimetype='text/event-stream')

@app.route('/rideHeightData4')
def rideHeightData4():
    return Response(get_message_value(0x01C, 4), mimetype='text/event-stream')

# throttle position landing page
@app.route('/throttle')
def throttleTemp():
    return render_template('throttle.html')

@app.route('/throttleData')
def throttleData():
    return Response(get_message_value(0x037, 7), mimetype='text/event-stream')

# steering position landing page
@app.route('/steer')
def steerTemp():
    return render_template('steer.html')

@app.route('/steerData')
def steerData():
    return Response(get_message_value(0x01C, 1), mimetype='text/event-stream')

@app.route('/faults')
def faultData():
    return Response(get_message_value(0x079, 0))

if __name__ == '__main__':
	application.run(debug==True, threaded=True)
