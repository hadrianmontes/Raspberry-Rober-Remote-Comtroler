from distance_sensor import Distance_Sensor


class Sensor_array(object):
    """Documentation for Sensor_array
    
    """
    def __init__(self, triggers, echoes):
        super(Sensor_array, self).__init__()
        self.triggers = triggers
        self.echoes = echoes
        self.sensors = []
        for trigger, echo in zip(triggers, echoes):
            self.sensors.append(Distance_Sensor(trigger, echo))

if __name__=="__main__":
    sensor_array = Sensor_array([21,19,13],[20,16,12])
