# Based in the class by
# Tony DiCola
# License: MIT License https://opensource.org/licenses/MIT
import time
import atexit
import time
from adafruit_motorkit import MotorKit
import board

class Robot(object):
    def __init__(self, left_trim=0, right_trim=0,
                 stop_at_exit=True):
        """Create an instance of the robot.  Can specify the following optional
        parameters:
         - addr: The I2C address of the motor HAT, default is 0x60.
         - left_id: The ID of the left motor, default is 1.
         - right_id: The ID of the right motor, default is 2.
         - left_trim: Amount to offset the speed of the left motor, can be positive
                      or negative and use useful for matching the speed of both
                      motors.  Default is 0.
         - right_trim: Amount to offset the speed of the right motor (see above).
         - stop_at_exit: Boolean to indicate if the motors should stop on program
                         exit.  Default is True (highly recommended to keep this
                         value to prevent damage to the bot on program crash!).
        """
        # Initialize motor HAT and left, right motor.
        self._mh = MotorKit(i2c=board.I2C())
        self._left = self._mh.motor1
        self._right = self._mh.motor2
        self._left_trim = left_trim
        self._right_trim = right_trim
        # Start with motors turned off.
        # self._left.run(Adafruit_MotorHAT.RELEASE)
        # self._right.run(Adafruit_MotorHAT.RELEASE)
        # Configure all motors to stop at program exit if desired.
        if stop_at_exit:
            atexit.register(self.stop)
            

    def _left_speed(self, speed):
        """Set the speed of the left motor, taking into account its trim offset.
        """
        assert abs(speed) <= 255, 'Speed must be a value between 0 to 255 inclusive!'
        sign = 1 if speed > 0 else -1
        speed = abs(speed)
        if speed != 0:
            speed = self._left_trim + (speed)*(255-self._left_trim)/255
        self._left.throttle = sign*speed/255

    def _right_speed(self, speed):
        """Set the speed of the left motor, taking into account its trim offset.
        """
        assert abs(speed) <= 255, 'Speed must be a value between 0 to 255 inclusive!'
        sign = 1 if speed > 0 else -1
        speed = abs(speed)
        if speed != 0:
            speed = self._right_trim + (speed)*(255-self._right_trim)/255# Constrain speed to 0-255 after trimming.
        self._right.throttle = sign*speed/255

    def stop(self):
        """Stop all movement."""
        self._left_speed(0)
        self._right_speed(0)

    def forward(self, speed, seconds=None):
        """Move forward at the specified speed (0-255).  Will start moving
        forward and return unless a seconds value is specified, in which
        case the robot will move forward for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        self._left_speed(speed)
        self._right_speed(speed)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def backward(self, speed, seconds=None):
        """Move backward at the specified speed (0-255).  Will start moving
        backward and return unless a seconds value is specified, in which
        case the robot will move backward for that amount of time and then stop.
        """
        # Set motor speed and move both backward.
        self._left_speed(-speed)
        self._right_speed(-speed)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def right(self, speed, seconds=None):
        """Spin to the right at the specified speed.  Will start spinning and
        return unless a seconds value is specified, in which case the robot will
        spin for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        self._left_speed(speed)
        self._right_speed(-speed)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def left(self, speed, seconds=None):
        """Spin to the left at the specified speed.  Will start spinning and
        return unless a seconds value is specified, in which case the robot will
        spin for that amount of time and then stop.
        """
        # Set motor speed and move both forward.
        self._left_speed(-speed)
        self._right_speed(speed)
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()

    def custom(self,vx,vy,seconds=None):
        # if vy < 0:
        # Set motor speed and move both forward.
        # v1 +v2 = vx
        # v1 - v2 = vy
        
        v1=int((vy+vx)/2)
        v2=int((vx-vy/2))
        self._left_speed(v1)
        self._right_speed(v2)
        
        # If an amount of time is specified, move for that time and then stop.
        if seconds is not None:
            time.sleep(seconds)
            self.stop()
