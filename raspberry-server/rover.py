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
        self.power = 250
        self.time_step = 0.1  # sime in seconds
        self.random_time = 5
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
                self.motors.backward(self.power, 5*self.time_step)
                self.turn(0)
                self.prev_random = time.time()

    def rotate(self, angle, power_multiplication=0.5):
        """
        Rotate a given angle, in degrees
        """
        if angle < 0:
            self._rotate_left(angle, power_multiplication)
        else:
            self._rotate_right(angle, power_multiplication)

    def _rotate_left(self, angle, power_multiplication, timelimit=10):
        initial_angle = self.orientation_sensor.phi
        print "rotating"
        print initial_angle
        rotated = 0
        start = time.time()
        while abs(rotated) < abs(angle):
            current = self.orientation_sensor.phi
            rotated = (initial_angle-current) % 360
            if rotated > 270:
                rotated = 0
            self.motors.left(int(self.power*power_multiplication))
            if (time.time() -start) > timelimit:
                self.motors.stop()
                return 0
        self.motors.stop()
        print self.orientation_sensor.phi
        print rotated
        return 1

    def _rotate_right(self, angle, power_multiplication, timelimit=10):
        initial_angle = self.orientation_sensor.phi
        print "rotating"
        print initial_angle
        rotated = 0
        start = time.time()
        while abs(rotated) < abs(angle):
            current = self.orientation_sensor.phi
            rotated = (current-initial_angle) % 360
            if rotated > 270:
                rotated = 0
            self.motors.right(int(self.power*power_multiplication))
            if (time.time() -start) > timelimit:
                self.motors.stop()
                return 0

        self.motors.stop()
        print self.orientation_sensor.phi
        print rotated
        return 1

    def turn(self, turning):
        if self.distances[1] < self.colision_distance:
            self.motors.backward(self.power, 5*self.time_step)
        if self.distances[2] < self.distances[0]:
            # self.motors.right(self.power/2,0.5)
            self.rotate(30)
        else:
            # self.motors.left(self.power/2,0.5)
            self.rotate(-30)
        self.prev_random = time.time()
        return 0

    def stop(self):
        self.motors.stop()
        self.sensor_array.stop_thread()

if __name__ == "__main__":
    rover = Rover()
    # rover.run()
