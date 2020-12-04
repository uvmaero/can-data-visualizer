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

from flask import Flask, render_template, request, Response, json, jsonify

app = Flask(__name__)

can.rc['interface'] = 'socketcan'
can.rc['channel'] = 'vcan0' # vcan0 for virtual, can0 for live
can.rc['bitrate'] = 500000
bus = can.interface.Bus()
data = 0

# Generate json_dump file for data. This uses external script "can_logger"
def get_message_value(can_id, bit):
    # print("get message")
    # print("can")
    # while True:
    # print("help me")
    for message in bus:
        if message.arbitration_id == can_id:
            data = message.data[bit]
            # print(f"yay {data}")
            json_data = f'"time":0,"value":{data}'
            # return f'data:{json_data}\n\n'
            print(json_data)
            # print(message.data)
            return json_data  
        else:
            data=0

    # msg = can.Message(is_extended_id=False,arbitration_id=can_id)
    # print(msg)
    # print(bytearray.decode(msg.data))
    
    # json_data = json.dumps(
    #         {"time":datetime.now().strftime('%H:%M:%S'), "value":data})
    # json_data = f'"time":0,"value":{data}'
    # # return f'data:{json_data}\n\n'
    # print(json_data)
    # return json_data    
    # yield json_data

    # delay system to ensure stability3
    print(json_data)
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
    # print("faults")
    event = 'data:{"value":1}\n\n'
    data_return = 'data:{'+str(get_message_value(0x079, 0))+'}\n\n'
    # return Response(get_message_value(0x079, 0), mimetype='text/event-stream')
    # return Response('data:{"value":1}\n\n', mimetype='text/event-stream')
    return Response(data_return, mimetype='text/event-stream')


if __name__ == '__main__':
    # while True:
    #     data_return = 'data:{'+str(get_message_value(0x079, 0))+'}\n\n'
    #     print(data_return)
    #     time.sleep(0.01)
    
	app.run(threaded=True)
