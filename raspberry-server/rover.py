from Robot import Robot
from sensor_array import Sensor_array
from orientation_sensor import Orientaion_sensor
import time
import atexit
class Rover(object):
    """Documentation for Rover
    """
    def __init__(self, tty="/dev/ttyUSB0"):
        super(Rover, self).__init__()
        self.motors = Robot()
        self.power = 200
        self.time_step = 0.1  # sime in seconds
        self.random_time = 10
        self.velocity = None
        self.sensor_array = Sensor_array([21,19,13],[20,16,12])
        self.colision_distance = 30
        self.orientation_sensor = Orientaion_sensor(tty=tty)
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

    def rotate(self, angle, power_multiplication=.75):
        """
        Rotate a given angle, in degrees
        """
        if angle < 0:
            self._rotate_left(angle, power_multiplication)
        else:
            self._rotate_left(angle, power_multiplication)

    def _rotate_left(self, angle, power_multiplication):
        initial_angle = self.orientation_sensor.phi
        angle = abs(angle) % 360
        print "rotating"
        print initial_angle
        while (initial_angle-self.orientation_sensor.phi) % 360 < angle:
            self.motors.left(self.power*power_multiplication)
        self.motors.stop()
        print self.orientation_sensor.phi
        print (initial_angle-self.orientation_sensor.phi) % 360

    def _rotate_right(self, angle, power_multiplication):
        initial_angle = self.orientation_sensor.phi
        angle = abs(angle) % 360
        print "rotating"
        print initial_angle
        while (self.orientation_sensor.phi-initial_angle) % 360 < angle:
            self.motors.left(self.power*power_multiplication)
        self.motors.stop()
        print self.orientation_sensor.phi
        print (self.orientation_sensor.phi-initial_angle) % 360

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
    # rover.run()
