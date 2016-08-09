from dronekit import connect, VehicleMode

try:
    vehicle = connect('/dev/ttyACM0', wait_ready = True) # '/dev/tty.usbmodem0'
    print ("connect to /dev/ttyACM0")
except:
    try:
        vehicle = connect('/dev/ttyACM1', wait_ready = True) # '/dev/tty.usbmodem1'
        print ("connect to /dev/ttyACM1")
    except:
        vehicle = connect('/dev/ttyACM2', wait_ready = True) # '/dev/tty.usbmodem2'
        print ("connect to /dev/ttyACM2")

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

# Close vehicle object before exiting script
vehicle.close()
print("Completed")