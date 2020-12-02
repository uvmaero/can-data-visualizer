# CAHPRI
# Missy, Kelley, George
# CS121 Final Project
# May 1, 2020
# can_logger file that interfaces with CAN bus to collect and send
# messages to vehicle. 

# imports
import mysql.connector
import json
import datetime
import time
import can
import matplotlib
import matplotlib.pyplot
import matplotlib.animation as animation

# create CAN interface
# See Source 2
can.rc['interface'] = 'socketcan'
can.rc['channel'] = 'can0' # vcan0 for virtual, can0 for live
can.rc['bitrate'] = 500000
bus = can.interface.Bus()

# default can_ID for testing data
can_ID = 0x0C0

# read CAN bus for data and return message if id matches request
def get_can_message(id, bit):
    for message in bus:
        if message.arbitration_id == id:
            data = message.data[bit]
            return data

# store information into SQL database
def store_data(canID):
    #load database credentials
    credentials = json.load(open("credentials.json", "r"))

    #connect to database
    database = mysql.connector.connect(
            host=credentials["host"],
            user=credentials["user"],
            passwd=credentials["password"],
            database=credentials["database"]
            )

    # create cursor to execute database commands
    cursor = database.cursor()

    # sql insert statement
    insert_sql = "INSERT INTO `can_data` (`timestamp`, `canID`, `msg`) VALUES (%s,%s,%s);"

    # get time
    now = datetime.datetime.now()

    # get CAN message
    msg = get_can_message(canID)

    # print to display
    print(msg)

    # insert into database
    data = (now,canID, msg)
    cursor.execute(insert_sql,data)

    # commit inser to databse
    database.commit()

    # close database connection
    cursor.close()
    database.close()

    # sleep
    #time.sleep(0.25)

# If using GUI, the graph function is helpful to see data being ploted
def graph(x1, y1):
   # draw the axis data:
   ax.clear()
   ax.plot(x1,y1)

   # format graph
   plt.xticks(rotation=45, ha='right')
   plt.subplots_adjust(bottom=0.30)
   plt.title('Test table')
   plt.xlabel('Time')
   plt.ylabel('CAN data')

# call for graph generation every second
#ani = animation.FuncAnimation(fig, store_data, fargs=(x1,y1), interval=1000)

#fig.show() --> generates an image of the graph, usually in GUI window
#save_html(plt, "templates/main.html") #save fig to main.html
