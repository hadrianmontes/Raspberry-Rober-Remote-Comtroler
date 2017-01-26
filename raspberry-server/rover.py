from Robot import Robot
from distance_sensor import Distance_Sensor
from random import choice
import time

class Rover(object):
    """Documentation for Rover
    """
    def __init__(self):
        super(Rover, self).__init__()
        self.motors = Robot()
        self.distance_sensor = Distance_Sensor(18, 4)
        self.power = 50
        self.time_step = 0.2  # sime in seconds
        self.velocity = None

    def run(self):
        prev = time.time()
        prev_distance = self.distance_sensor.mean_distance()
        turning = 0
        while True:
            distance = self.distance_sensor.mean_distance()
            print distance
            if (time.time()-prev) < self.time_step:
                self.motors.forward(50)
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
            self.motors.right(50)
        elif turning == -1:
            self.motors.left(50)
        return turning

rover = Rover()
rover.run()
