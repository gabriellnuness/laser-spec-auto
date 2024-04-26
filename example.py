# minimal example to read spectrum

from matplotlib.pyplot import *
from AQ6370D import AQ6370D
import ILX
from time import sleep
import numpy as np

# configuring optical spectrum analyzer
osa = AQ6370D(gpib_address="GPIB0::1::INSTR", center=1540e-9, span=200e-9)
osa.set_sensitivity("NAUT")

# configuring laser controller
ilx = ILX.config(gpib_address="GPIB0::12::INSTR")
ilx.write("TEC:OUT 0")
ilx.write("LAS:OUT 0")
ilx.write("TEC:MODE T")
ilx.write("TEC:LIM:THI 40.0")
ilx.write("TEC:T 25.5")
ilx.write("LAS:MODE ILBW")
ilx.write("LAS:LIM: 500.0")
ilx.write("LAS:RAN 5")
ilx.write("LAS:LDI 130.0") # set current

ilx.write("TEC:OUT 1")
sleep(0.1)
ilx.write("TEC:OUT 0")
sleep(0.1)
ilx.write("TEC:OUT 1")
ilx.write("LAS:OUT 1")



# setting current and temperature in laser controller
for current in range(0,500+50,50):
    print(current)
    # sleep(1)
    ilx.write(f"LAS:LDI {current}") # set current
    # sleep(0.5)
    # ilx.write("LAS:OUT 1")
    sleep(5)
ilx.write("LAS:OUT 0")



# reading data
osa.simple_sweep(trace="tra")

wavelength_m = osa.wavelength_m
power_dbm = osa.optical_power_dbm


figure()
plot()
plot(wavelength_m*1e9, power_dbm)
show()





# close communications
osa.close()


