from rover import Rover
import time
from numpy.random import normal

class Rover_IA(Rover):
    """Creates the IA to control the Rover

    """
    def __init__(self, **kwargs):
        super(Rover_IA, self).__init__(**kwargs)

    def run(self):
        prev = time.time()
        self.prev_random = prev
        self.sensor_array.start_thread()
        self._start_log()
        self.sensor_array.measure_distances()
        prev_distances = self.sensor_array.distances
        turning = 0
        while True:
            self.distances = self.sensor_array.distances
            print self.distances
            if (time.time()-prev) > self.time_step:
                self.velocity = (self.distances[1]-prev_distances[1])/(time.time()-prev)
                prev = time.time()
                prev_distances = self.distances[:]
            if min(self.distances) < self.colision_distance:
                try:
                    angle = abs(normal(30,15))
                    turning = self.turn(turning, angle=angle)
                except IOError:
                    self.orientation_sensor.restart()
            elif max(self.distances) > 3000:
                self.motors.backward(self.power,1)
            else:
                self.motors.forward(self.power)
            if (time.time()-self.prev_random) > self.random_time:
                self.motors.backward(self.power, 5*self.time_step)
                try:
                    angle = abs(normal(30,15))
                    self.turn(0, angle=angle)
                except IOError:
                    self.orientation_sensor.restart()
                self.prev_random = time.time()
