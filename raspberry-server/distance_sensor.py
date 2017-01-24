import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

class Distance_Sensor(object):
    """
    Creates an interface to use with the distance sensor
    hc-sr04
    """
    def __init__(self,trigger, echo):
        super(Distance_Sensor, self).__init__()
        self.trigger = trigger
        self.echo = echo
        self.setup(trigger, echo)

    def setup(self, trigger, echo):
        try:
            GPIO.setup(self.trigger, GPIO.OUT)
            GPIO.setup(self.echo, GPIO.IN)
        except:
            GPIO.cleanup()
            self.setup()
        # Give 0.5 seccond to the sensor to start working
        time.sleep(0.5)

    def distance(self, counter=0):
        dist = self.measure_backend()
        if dist > 3000 and counter < 3:
            dist = self.distance(counter+1)
        return dist

    def measure_backend(self):
        # Send the trigger pulse
        GPIO.output(self.trigger, True)
        time.sleep(0.00001)
        GPIO.output(self.trigger, False)
        while GPIO.input(self.echo) == 0:
            start = time.time()
        while GPIO.input(self.echo) == 1:
            end = time.time()
        duration = end-start
        distance = duration * 17150
        return distance

    def stop(self):
        GPIO.cleanup()
