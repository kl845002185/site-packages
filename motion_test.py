from dronekit import connect, VehicleMode
import sys
import time
import urllib2
from pymavlink import mavutil
from datetime import datetime


# TASK: Set up option parsing to get connection string
import argparse
parser = argparse.ArgumentParser(description='Basic motion test for the BLueROV. ')
parser.add_argument('--connect',
                   help="Vehicle connection target string. If not specified, SITL automatically started and used.")
args = parser.parse_args()

connection_string = args.connect
sitl = None
connection_to_vehicle = True

connection = False
index = '0'
connection_string = '/dev/ttyACM'
# connection_string = '/dev/tty.usbmodem'

# TASK: Start SITL if connection_to_vehicle is False
# TASK: Connect to UDP endpoint (and wait for default attributes to accumulate)
if not connection_to_vehicle:
    import dronekit_sitl
    sitl = dronekit_sitl.start_default()
    connection_string = sitl.connection_string()
    vehicle = connect(connection_string, wait_ready = True)
else:
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


'''
#Create a message listener for all messages.
@vehicle.on_message('*')
def listener(self, name, message):
    print 'message: %s' % message
'''


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


def arm_and_takeoff(aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """
    print "Basic pre-arm checks"
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print " Waiting for vehicle to initialise..."
        time.sleep(1)
    print "Arming motors"
    # Copter should arm in GUIDED mode
    # vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True
    '''
    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print " Waiting for arming..."
        time.sleep(1)
    '''
    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt
        # Break and return from function just below target altitude.
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95:
            print "Reached target altitude"
            break
        time.sleep(1)


def send_ned_velocity(velocity_x, velocity_y, velocity_z, duration):

    msg = vehicle.message_factory.set_position_target_local_ned_encode(
        0,              # time_boot_ms (not used)
        0, 0,           # target system, target component
        mavutil.mavlink.MAV_FRAME_LOCAL_NED, # frame
        0b0000111111000111, # type_mask (only speeds enabled)
        0, 0, 0,        # x, y, z positions (not used)
        velocity_x, velocity_y, velocity_z, # x, y, z velocity in m/s
        0, 0, 0,        # x, y, z acceleration (not supported yet, ignored in GCS_Mavlink)
        0, 0)           # yaw, yaw_rate (not supported yet, ignored in GCS_Mavlink)

    # send command to vehicle on 1 Hz cycle
    for x in range(0,duration):
        vehicle.send_mavlink(msg)
        time.sleep(1)


def condition_yaw(heading, relative=False):

    if relative:
        is_relative = 1 #yaw relative to direction of travel
    else:
        is_relative = 0 #yaw is an absolute angle
    # create the CONDITION_YAW command using command_long_encode()
    msg = vehicle.message_factory.command_long_encode(
        0, 0,           # target system, target component
        mavutil.mavlink.MAV_CMD_CONDITION_YAW, #command
        0,              # confirmation
        heading,        # param 1, yaw in degrees
        0,              # param 2, yaw speed deg/s
        1,              # param 3, direction -1 ccw, 1 cw
        is_relative,    # param 4, relative offset 1, absolute angle 0
        0, 0, 0)        # param 5 ~ 7 not used
    # send command to vehicle
    vehicle.send_mavlink(msg)


def square_path(DURATION):

    # Set up velocity vector to map to each direction.
    # vx > 0 => fly North, vx < 0 => fly South
    NORTH = 0.5
    SOUTH = -0.5
    # Note for vy: vy > 0 => fly East, vy < 0 => fly West
    EAST = 0.5
    WEST = -0.5
    # Note for vz: vz < 0 => ascend, vz > 0 => descend
    UP = -0.2
    DOWN = 0.2

    print("SQUARE path using SET_POSITION_TARGET_LOCAL_NED and velocity parameters")
    print("Yaw 180 absolute (South)")
    condition_yaw(180)
    print("Velocity South & up")
    send_ned_velocity(SOUTH, 0, UP, DURATION)
    send_ned_velocity(0, 0, 0, 1)
    print("Yaw 270 absolute (West)")
    condition_yaw(270)
    print("Velocity West & down")
    send_ned_velocity(0, WEST, DOWN, DURATION)
    send_ned_velocity(0, 0, 0, 1)
    print("Yaw 0 absolute (North)")
    condition_yaw(0)
    print("Velocity North")
    send_ned_velocity(NORTH, 0, 0, DURATION)
    send_ned_velocity(0, 0, 0, 1)
    print("Yaw 90 absolute (East)")
    condition_yaw(90)
    print("Velocity East")
    send_ned_velocity(0, EAST, 0, DURATION)
    send_ned_velocity(0, 0, 0, 1)


# TASK: Get all vehicle attributes (state)
print_basic_vehicle_parameters(vehicle)
print "Arming motors"
vehicle.armed = True
print " Armed: %s" % vehicle.armed


# TASK: Supervise the volatge and avoid over-discharging
minimum_voltage = 0
@vehicle.on_attribute('battery')
def attitude_listener(self, name, msg):
    print '---%s' % (msg)
    time.sleep(3)
    if vehicle.battery.voltage < minimum_voltage:
        vehicle.mode = VehicleMode("LAND")
        vehicle.close()
        print "Battery volatge too low."
        exit()


# TASK: Stay in a stable attitude underwater
original_attitude = vehicle.location.global_relative_frame.alt - 0.3
arm_and_takeoff(original_attitude)


'''
#Confirm vehicle armed before attempting to start
while (not vehicle.armed):
    print " Waiting for arming..."
    time.sleep(1)
'''


# TASK: Square path using velocity
square_path(1)  # DURITION


vehicle.close()
print "Finished all the tasks"
