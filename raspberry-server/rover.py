from Robot import Robot
from sensor_array import Sensor_array
import time

class Rover(object):
    """Documentation for Rover
    """
    def __init__(self):
        super(Rover, self).__init__()
        self.motors = Robot()
        self.power = 100
        self.time_step = 0.1  # sime in seconds
        self.velocity = None
        self.sensor_array = Sensor_array([21,19,13],[20,16,12])
        self.sensor_array.start_thread()
        self.colision_distance = 30

    def run(self):
        prev = time.time()
        prev_distances = self.sensor_array.distances
        turning = 0
        while True:
            self.distances = self.sensor_array.distances
            print self.distances
            if (time.time()-prev) > self.time_step:
                self.motors.forward(self.power)
                self.velocity = (self.distances[1]-prev_distances[1])/(time.time()-prev)
                prev = time.time()
                prev_distances = self.distances[:]
            if any(self.distances < self.colision_distance):
                turning = self.turn(turning)

    def turn(self, turning):
        if self.distances[1] < self.colision_distance:
            self.motors.backward(self.power, self.time_step)
        if self.distances[0] < self.distances[2]:
            self.motors.right(self.power/2.,self.time_step)
        else:
            self.motors.left(self.power/2.,self.time_step)
        return 0

rover = Rover()
rover.run()
