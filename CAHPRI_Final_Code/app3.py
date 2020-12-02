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
            # delay system to ensure stability3
            print(data)
            time.sleep(.1)


# Landing Page
@app.route('/')
def index():
    return render_template('layout.html')

# throttle position landing page
@app.route('/throttle')
def throttleTemp():
    return render_template('throttle.html')

@app.route('/throttleData')
def throttleData():
    return Response(get_message_value(0x037, 7), mimetype='text/event-stream')

@app.route('/faults')
def faultData():
    print("faults")
    return Response(get_message_value(0x079, 0), mimetype='text/event-stream')

if __name__ == '__main__':
	application.run(debug==True, threaded=True)
