from Robot import Robot
from random import choice
from sensor_array import Sensor_array
import time

class Rover(object):
    """Documentation for Rover
    """
    def __init__(self):
        super(Rover, self).__init__()
        self.motors = Robot()
        self.power = 200
        self.time_step = 0.2  # sime in seconds
        self.velocity = None
        self.sensor_array = Sensor_array([21,19,13],[20,16,12])
#        self.sensor_array.start_thread()

    def run(self):
        prev = time.time()
	self.sensor_array.mean_measure()
        prev_distance = min(self.sensor_array.distances)
        turning = 0
        while True:
            self.sensor_array.mean_measure()
            distance = min(self.sensor_array.distances)
	    print self.sensor_array.distances
            if (time.time()-prev) > self.time_step:
                self.motors.forward(self.power)
                self.velocity = (distance-prev_distance)/(time.time()-prev)
                prev = time.time()
                prev_distance = distance
            if turning !=0 and distance < 30:
                turning = self.turn(turning)
            elif distance < 20:
                turning = self.turn(turning)
            else:
                turning = 0

    def turn(self, turning):
        if turning == 0:
            turning = choice([-1,1])
        if turning == 1:
            self.motors.right(self.power)
        elif turning == -1:
            self.motors.left(self.power)
        return turning

rover = Rover()
rover.run()
