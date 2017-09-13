from Robot import Robot
from orientation_sensor import Orientaion_sensor
from sensor_array import Sensor_array
import threading
import time
import atexit

class Rover(object):
    """Documentation for Rover
    """
    def __init__(self, tty="/dev/ttyUSB0", power=250, random_time=5,
                 time_step=0.1, sensor_array=[[21,19,13],[20,16,12]],):
        super(Rover, self).__init__()
        self.motors = Robot()
        self.power = power
        self.time_step = time_step  # sime in seconds
        self.random_time = random_time
        self.velocity = None
        self.colision_distance = 30
        self.orientation_sensor = Orientaion_sensor(tty=tty)
        self._log = []
        self._threaded_log = False
        self._status = ""
        atexit.register(self.stop)
        self.sensor_array = Sensor_array(*sensor_array)

    def rotate(self, angle, power_multiplication=0.5):
        """
        Rotate a given angle, in degrees
        """
        if angle < 0:
            return self._rotate_left(angle, power_multiplication)
        else:
            return self._rotate_right(angle, power_multiplication)

    def _rotate_left(self, angle, power_multiplication, timelimit=10):
        initial_angle = self.orientation_sensor.phi
        self._status = "rotating left {}".format(int(angle))
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
        return 1

    def _rotate_right(self, angle, power_multiplication, timelimit=10):
        initial_angle = self.orientation_sensor.phi
        self._status = "rotating right {}".format(int(angle))
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
        return 1

    def turn(self, turning, angle=30):
        if self.distances[1] < self.colision_distance:
            self.motors.backward(self.power, 5*self.time_step)
        if self.distances[2] < self.distances[0]:
            signo = 1
            # self.motors.right(self.power/2,0.5)
        else:
            signo = -1
            # self.motors.left(self.power/2,0.5)
        rotated = self.rotate(angle*signo)
        if not rotated:
            rotated = self.rotate(-angle*signo)
        if not rotated:
            self.motors.backward(self.power, 5*self.time_step)
        self.prev_random = time.time()
        return 0

    def stop(self):
        self.motors.stop()
        self.sensor_array.stop_thread()
        self._stop_log()

    def _update_log(self, visual=True):
        entry = (self._status,
                 self.orientation_sensor.phi,
                 self.sensor_array.distances)
        self._log.append(entry)
        if visual:
            print entry

    def _maintain_log(self):
        while self._threaded_log:
            self._update_log(True)
            time.sleep(0.5)

    def _start_log(self):
        self._threaded_log = True
        self.thread = threading.Thread(target=self._maintain_log)
        self.thread.start()

    def _stop_log(self):
        self._threaded_log = False

if __name__ == "__main__":
    rover = Rover()
    # rover.run()
