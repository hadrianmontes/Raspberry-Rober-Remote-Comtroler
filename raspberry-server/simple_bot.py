from Robot import Robot
import board

class LineSensor(object):
    """Documentation for LineSensor
    """
    def __init__(self, pin):
        super(LineSensor, self).__init__()
        self.pin = pin
        board.pin.GPIO.setup(self.pin.id, board.pin.GPIO.IN)
    @property
    def value(self):
        return self.pin.value()

class LineFollower(object):
    """Documentation for Rover
    """
    def __init__(self):
        self.motors = Robot(left_trim=95, right_trim=95, stop_at_exit=True, )
        self.timestep = 0.02
        self.power = 20
        self.line_sensor = LineSensor(board.D4)
        
    def run(self):
        while True:
            if self.line_sensor.value:
                self.motors.forward(self.power, self.timestep)
                self.motors.right(self.power, self.timestep)
            else:
                self.motors.left(self.power, self.timestep)
                
if __name__ == '__main__':
    line = LineFollower()
    line.run()