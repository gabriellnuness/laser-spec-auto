# minimal example to read spectrum

import matplotlib.pyplot as plt
from AQ6370D import AQ6370D
from ILX import ilx
from time import sleep
import pandas as pd


# configuring optical spectrum analyzer
osa = AQ6370D(gpib_address="GPIB0::1::INSTR", center=1540e-9, span=200e-9)
osa.set_sensitivity("NAUT")

# configuring laser controller
laser = ilx(gpib_address="GPIB0::12::INSTR")
laser.temperature_on()
laser.current_on()


osa.read() # bug, it must be called first otherwise the variables are not created
plt.figure()
# setting current and temperature in laser controller
for current in range(0, 500+50, 50):
    print(f"current = {current} mA")
    laser.set_current(current=current)    # sleep(0.5)
    sleep(1)

    # reading data
    wavelength_m = osa.wavelength_m
    power_dbm = osa.optical_power_dbm
    osa.simple_sweep()
    osa.read()

    # saving data
    filename = f"M5_{current}mA".replace(".", "_")
    df = pd.DataFrame({'wavelength [m]': wavelength_m,
                  'optical power [dbm]': power_dbm,
                  'current [mA]': current})
    df.to_csv("output/" + filename + ".csv", index=False)

    # plt.close("all")
    # plt.figure()
    # plt.plot(wavelength_m*1e9, power_dbm)
    # plt.show(block=False)




laser.current_off()


