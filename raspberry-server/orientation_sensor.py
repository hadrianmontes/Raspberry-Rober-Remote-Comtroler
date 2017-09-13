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
        self._initialized = False
        self._init_connection()

    def _init_connection(self):
        self.serial = serial.Serial(self.tty, baudrate=self.baud,
                                    timeout=0)
        print("Stating orientation Sensor, please wait 10s")
        time.sleep(5)
        self.serial.writelines(["w"])
        time.sleep(5)
        print("Sensor initialized, waiting for the measures to stabilize")
        time.sleep(5)
        print("Fully initialized")
        self._initialized = True
        return

    def _read_phi(self, tries=10000):
        # Flush old values
        self.serial.flushInput()
        # Try until a read is done
        for _ in xrange(tries):
            line = self.serial.readline()
            if line:
                try:
                    return float(line.split()[1])
                except (ValueError, IndexError):
                    continue
        else:
            raise(IOError("Conexion with device has been lost"))

    def stop(self):
        """
        Stops the comunication with the remote sensor
        """
        self.serial.close()
        self._initialized = False

    def restart(self):
        """Restart he conection with the remote sensor. If que conexion was
        already closed it calls the initilization again
        """
        if self.initialized:
            self.stop()
        self._init_connection()

    @property
    def phi(self):
        return self._read_phi() % 360

    @property
    def initialized(self):
        return self._initialized
