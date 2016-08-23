import time

def channel_initial_setting(vehicle):
    vehicle.channels = {'1':1500, '2':1500, '3':1500, '4':1500, '5':1100, '6':1500, '7':1500, '8':1500}


def yaw_right(vehicle, speed, duration):
    if duration < 0:
        duration = 0
    if (speed >= 1100 or speed <= 1900):
        vehicle.channels.overrides = {'1':1500, '2':1500, '3':1500, '4':1500, '5':1100, '6':speed, '7':1500, '8':1500}
        time.sleep(duration)
    else:
        print("Speed should in the region of [1100, 1900]" )

def throttle_forward(vehicle, speed, duration):
    speed = 3000 - speed #reverse the control direction due to the channel calibration
    if duration < 0:
        duration = 0
    if (speed >= 1100 or speed <= 1900):
        vehicle.channels.overrides = {'1':1500, '2':1500, '3':1500, '4':speed, '5':1100, '6':1500, '7':1500, '8':1500}
        time.sleep(duration)
    else:
        print("Speed should in the region of [1100, 1900]" )

def strafe_right(vehicle, speed, duration):
    if duration < 0:
        duration = 0
    if (speed >= 1100 or speed <= 1900):
        vehicle.channels.overrides = {'1':1500, '2':1500, '3':1500, '4':1500, '5':1100, '6':1500, '7':speed, '8':1500}
        time.sleep(duration)
    else:
        print("Speed should in the region of [1100, 1900]" )

def ascend(vehicle, speed, duration):
    if duration < 0:
        duration = 0
    if (speed >= 1100 or speed <= 1900):
        vehicle.channels.overrides = {'1':1500, '2':1500, '3':speed, '4':1500, '5':1100, '6':1500, '7':1500, '8':1500}
        time.sleep(duration)
    else:
        print("Speed should in the region of [1100, 1900]" )