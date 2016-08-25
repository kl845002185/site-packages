from dronekit import connect, VehicleMode
import time


class MotionControl:
    def __init__(self, vehicle):
        self.motion_stack = []
        self.DEFAULT_CHANNEL_OVERRIDES = {
            '1': 1500, '2': 1500, '3': 1500, '4': 1500,
            '5': 1100, '6': 1500, '7': 1500, '8': 1500
        }  # Channel 3, 4, 6, 7 are for basic motions control
        vehicle.channels.overrides = self.DEFAULT_CHANNEL_OVERRIDES
        self.in_recall = False

    @staticmethod
    def arm(vehicle, mode_string):
        print "Arming motors"
        vehicle.armed = True
        vehicle.mode = VehicleMode(mode_string)
        print " Armed: %s" % vehicle.armed

    def stop(self, vehicle, *arg):
        __temp = {
            'Motion Name': 'Stop',
            'Speed(%)': 1500,
            'Duration(s)': 0
        }
        # print(__temp)
        if not self.in_recall:
            self.motion_stack.append(__temp)
        vehicle.channels.overrides = self.DEFAULT_CHANNEL_OVERRIDES

    def yaw(self, vehicle, speed, duration):  # Positive speed is yaw right
        __temp = {
            'Motion Name': 'Yaw',
            'Speed(%)': speed,
            'Duration(s)': duration
        }
        speed = speed * 4 + 1500
        if duration < 0:
            duration = 0
        if (1100 <= speed <= 1900):
            print(__temp)
            if not self.in_recall:
                self.motion_stack.append(__temp)
            # vehicle.channels.overrides == self.DEFAULT_CHANNEL_OVERRIDES
            vehicle.channels.overrides['6'] = speed
            time.sleep(duration)
            self.stop(vehicle)
        else:
            raise ValueError("Yaw speed region is [-100, 100]")

    def throttle(self, vehicle, speed, duration):  # Positive speed is throttle forward
        __temp = {
            'Motion Name': 'Throttle',
            'Speed(%)': speed,
            'Duration(s)': duration
        }
        speed = speed * 4 + 1500
        speed = 3000 - speed # reverse the control direction due to the channel calibration
        if duration < 0:
            duration = 0
        if (1100 <= speed <= 1900):
            print(__temp)
            if not self.in_recall:
                self.motion_stack.append(__temp)
            # vehicle.channels.overrides == self.DEFAULT_CHANNEL_OVERRIDES
            vehicle.channels.overrides['4'] = speed
            time.sleep(duration)
            self.stop(vehicle)
        else:
            raise ValueError("Throttle speed region is [-100, 100]")

    def strafe(self, vehicle, speed, duration):  # Positive speed is strafe right
        __temp = {
            'Motion Name': 'Strafe',
            'Speed(%)': speed,
            'Duration(s)': duration
        }
        if duration < 0:
            duration = 0
        speed = speed * 4 + 1500
        if (1100 <= speed <= 1900):
            print(__temp)
            if not self.in_recall:
                self.motion_stack.append(__temp)
            # vehicle.channels.overrides == self.DEFAULT_CHANNEL_OVERRIDES
            vehicle.channels.overrides['7'] = speed
            time.sleep(duration)
            self.stop(vehicle)
        else:
            raise ValueError("Strafe speed region is [-100, 100]")

    def pitch(self, vehicle, speed, duration):  # Positive speed is pitch ascend
        __temp = {
            'Motion Name': 'Pitch',
            'Speed(%)': speed,
            'Duration(s)': duration
        }
        if duration < 0:
            duration = 0
        speed = speed * 4 + 1500
        if (1100 <= speed <= 1900):
            print(__temp)
            # vehicle.channels.overrides == self.DEFAULT_CHANNEL_OVERRIDES
            vehicle.channels.overrides['3'] = speed
            time.sleep(duration)
            self.stop(vehicle)
        else:
            raise ValueError("Pitch speed region is [-100, 100]")

    def motions_recall(self, vehicle, motion_stack):
        self.in_recall = True
        print("Recalling")
        __get_motion = {
            'Stop': self.stop,
            'Yaw': self.yaw,
            'Throttle': self.throttle,
            'Strafe': self.strafe,
        }
        while len(motion_stack):
            last_motion = motion_stack[-1]
            __get_motion.get(last_motion['Motion Name'], self.stop)\
                (vehicle, -last_motion['Speed(%)'], last_motion['Duration(s)'])
            motion_stack.pop()
        self.in_recall = False