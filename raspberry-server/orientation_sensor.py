import serial
import time

class Orientaion_sensor(object):
    """
    Creates an interface to connect with an aruduino with a 6 axis
    giroscope by serial connection. Now it only detects the phi angle.
    Input
    --------------------
    tty: (optional) tty where the arduino is connected.
         preset value='/dev/ttyUSB0'
    baud: (option) baud rate of the serial connection.
         preset value = 115200

    """
    def __init__(self, tty="/dev/ttyUSB0", baud=115200):
        super(Orientaion_sensor, self).__init__()
        self.tty = tty
        self.baud = baud
        # Initiate the serial connection
        self.serial = serial.Serial(self.tty, baudrate=self.baud,
                                    timeout=0)
        self._init_connection()

    def _init_connection(self):
        print "Stating orientation Sensor, please wait 10s"
        time.sleep(5)
        self.serial.writelines(["w"])
        time.sleep(5)
        print "Sensor initialized, waiting for the measures to stabilize"
        time.sleep(5)
        print "Fully initialized"
        return

    def _read_phi(self):
        # Flush old values
        self.serial.flushInput()
        # Try until a read is done
        while True:
            line = self.serial.readline()
            if line:
                return float(line.split()[1])

    @property
    def phi(self):
        return self._read_phi() % 360

