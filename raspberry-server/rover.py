from Robot import Robot
from sensor_array import Sensor_array
import time
import atexit
class Rover(object):
    """Documentation for Rover
    """
    def __init__(self):
        super(Rover, self).__init__()
        self.motors = Robot()
        self.power = 200
        self.time_step = 0.2  # sime in seconds
        self.random_time = 10
        self.velocity = None
        self.sensor_array = Sensor_array([21,19,13],[20,16,12])
        self.colision_distance = 30
        atexit.register(self.stop)

    def run(self):
        prev = time.time()
        self.prev_random = prev
        self.sensor_array.start_thread()
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
                turning = self.turn(turning)
            elif max(self.distances) > 3000:
                self.motors.backward(self.power,1)
            else:
                self.motors.forward(self.power)
            if (time.time()-self.prev_random) > self.random_time:
                self.motors.backward(self.power, self.time_step)
                self.turn(0)
                self.prev_random = time.time()
                
    def turn(self, turning):
        if self.distances[1] < self.colision_distance:
            self.motors.backward(self.power, self.time_step)
        if self.distances[0] < self.distances[2]:
            self.motors.right(self.power/2,0.5)
        else:
            self.motors.left(self.power/2,0.5)
        self.prev_random = time.time()
        return 0

    def stop(self):
	self.motors.stop()
	self.sensor_array.stop_thread()

if __name__ == "__main__":
    rover = Rover()
    rover.run()
