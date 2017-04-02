from distance_sensor import Distance_Sensor
import threading
import time

class Sensor_array(object):
    """Documentation for Sensor_array
    
    """
    def __init__(self, triggers, echoes):
        super(Sensor_array, self).__init__()
        self.triggers = triggers
        self.echoes = echoes
        self.sensors = []
        self.distances=[]
        self.measure = False
        for trigger, echo in zip(triggers, echoes):
            self.sensors.append(Distance_Sensor(trigger, echo))
            self.distances.append(None)
        self.mean_measure()
        self.thread = None

    def mean_measure(self):
        distances = []
        for sensor in self.sensors:
            distances.append(sensor.mean_distance())
        self.distances = distances

    def measure_distances(self):
        distances = []
        for sensor in self.sensors:
            distances.append(sensor.measure_backend())
            time.sleep(0.01)
        self.distances = distances
        
    def start_thread(self):
        self.measure = True
        self.thread = threading.Thread(target=self.main_routine)
        self.thread.start()

    def stop_thread(self):
        self.measure = False

    def main_routine(self):
        while self.measure:
            self.mean_measure()
            time.sleep(0.01)

if __name__=="__main__":
    sensor_array = Sensor_array([21,19,13],[20,16,12])
