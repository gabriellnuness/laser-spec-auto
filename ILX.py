import pyvisa
from time import sleep

class ilx:    

    def __init__(self, gpib_address="GPIB0::12::INSTR",
                 temperature_limit=40,
                 temperature=25.0,
                 current_limit=200.0,
                 current=0.0):
        
        rm = pyvisa.ResourceManager()
        self.laser = rm.open_resource(gpib_address)
        print(self.laser.query("*idn?"))


        self.configure(temperature_limit=temperature_limit, temperature=temperature, current_limit=current_limit, current=current)


    def configure(self, temperature_limit, temperature, current_limit, current):
        # turning off controller as the default initialization
        self.temperature_off()
        self.current_off()
        self.laser.write("TEC:MODE T")
        self.laser.write("LAS:MODE ILBW") # set output to low bandwidth
        self.laser.write("LAS:RAN 5") # sets laser output drive current range to 500 mA
        sleep(1)
        self.set_current(current_limit=current_limit, current=current)
        sleep(1)
        self.set_temperature(temperature_limit=temperature_limit, temperature=temperature)
        self.temperature_on()
        sleep(0.1)
        self.temperature_off()
        sleep(0.1)
        self.temperature_on()
        sleep(0.1)



    def set_temperature(self, temperature=25.0, temperature_limit=40.0):
        self.laser.write(f"TEC:LIM:THI {temperature_limit}")
        self.laser.write(f"TEC:T {temperature}")

    def set_current(self, current=0.0, current_limit=500.0):
        self.laser.write(f"LAS:LIM: {current_limit}")
        self.laser.write(f"LAS:LDI {current}")

    def temperature_on(self):
        self.laser.write("TEC:OUT 1")

    def temperature_off(self):
        self.laser.write("TEC:OUT 0")

    def current_on(self):
        if int(self.laser.query("TEC:OUT?")[0]) == 0:
            raise ValueError('Temperature controller is off!')
        else:
            self.laser.write("LAS:OUT 1")

    def current_off(self):
        self.laser.write("LAS:OUT 0")





if __name__ == '__main__':
    ilx()
    