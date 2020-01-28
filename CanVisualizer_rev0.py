#!/usr/bin/python3

# AERO 
# December 2019

# Multipurpose Can Visualizer for real time display.

# demo script to see how to interface with can-utils

import time
import can

bustype ='socketcan'
channel = 'vcan0'

def producer(id):
    bus = can.interface.Bus(channel=channel, bustype=bustype)
    for i in range(10):
        msg = can.Message(arbitration_id=0xc0ffee, data=[id,i,0,1,3,1,4,1], is_extended_id=False)
        bus.send(msg)

    time.sleep(1)


producer(10)