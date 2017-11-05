

class BBCON:

    def __init__(self):
        self.behaviors = [] #En liste av alle behavior objektene som brukes av BBCON
        self.active_behaviors = [] #En liste med de aktive behavior objektene
        self.sensobs = [] #En liste av alle sensorobjektene som brukes av BBCON
        self.motobs = [] #En liste ac alle motor objektene som brukes av BBCON
        self.arbitrator = Arbitrator() #Arbitratoren som skal løse requests fra behaviors

        #Andre variabler kan være current_timestep, inaktive behaviors og roboten selv


    def add_behavior(self,behavior):
        if behavior not in behavior:
            self.behaviors.append(behavior)

    def add_sensob(self,sensor):
        if sensor not in self.sensobs:
            self.sensobs.append(sensor)

    def activate_behavior(self,behavior):
        if behavior not in self.active_behaviors:
            behavior.active_flag = True
            self.active_behaviors.append(behavior)

    def deactivate_behavior(self,behavior):
        if behavior in self.active_behaviors:
            behavior.active_flag = False
            self.active_behaviors.remove(behavior)

    def run_one_timestep(self):
        #Update sensobs
        #Update behaviors
        #Call arbitrator.choose_action
        #Update motobs
        #Pause
        #Rest sensobs
        pass



