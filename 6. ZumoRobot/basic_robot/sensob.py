

class Sensob:


    def __init__(self):
        self.associated_sensors = [] #List of SensorWrappers
        self.value = 0

    #Updates one time for each timestep
    def update(self):
        #Fetch relevant sensor values from the sensor wrapper
        #Convert ionto sensob value
        pass
