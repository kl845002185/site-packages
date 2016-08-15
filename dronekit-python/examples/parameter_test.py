from dronekit import connect, VehicleMode
import time

connection = False
index = '0'
connection_string = '/dev/ttyACM'
# connection_string = '/dev/tty.usbmodem'

while not connection:
    try:
        vehicle = connect(connection_string + index, wait_ready = True)
        print ("Connect to " + connection_string + index)
        connection = True
    except:
        print ("Cannot connect to " + connection_string + index)
        index = str(int(index) + 1)
    if index.__len__() >= 3:
        exit()

vehicle.mode = VehicleMode("ALT_HOLD")

# vehicle = connect('/dev/tty.usbmodem1', wait_ready = True) # '/dev/tty.usbmodem0'
# vehicle = connect('/dev/ttyACM0', wait_ready = True) # '/dev/tty.usbmodem0'

def print_basic_vehicle_parameters(vehicle):
    print "Vehicle state:"
    print " %s" % vehicle.attitude
    print " Velocity: %s" % vehicle.velocity
    print " %s" % vehicle.battery
    print " Last Heartbeat: %s" % vehicle.last_heartbeat
    print " Heading: %s" % vehicle.heading
    print " Groundspeed: %s" % vehicle.groundspeed
    print " Airspeed: %s" % vehicle.airspeed
    print " Mode: %s" % vehicle.mode.name
    print " Is Armable?: %s" % vehicle.is_armable


# Get some vehicle attributes (state)
print_basic_vehicle_parameters(vehicle)

@vehicle.on_attribute('velocity')
def attitude_listener(self, name, msg):
    print '---%s' % (msg)
    time.sleep(1)

while True:
    pass

# Close vehicle object before exiting script
vehicle.close()
print("Completed")
