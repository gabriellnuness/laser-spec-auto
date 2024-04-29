# minimal example to read spectrum

import matplotlib.pyplot as plt
from AQ6370D import AQ6370D
from ILX import ilx
from time import sleep
import pandas as pd

# experimental data
experiment = 1
fiber = "m5"
pump_laser = "980nm"
length = 10.66 # m


# configuring optical spectrum analyzer
osa = AQ6370D(gpib_address="GPIB0::1::INSTR", center=1540e-9, span=100e-9)
osa.set_sensitivity("NAUT")
osa.set_resolution(resolution="50pm") #20pm 50pm
osa.set_sweep_points()

# configuring laser controller
laser = ilx(gpib_address="GPIB0::12::INSTR")
laser.temperature_on()
laser.current_on()

plt.figure()
# setting current and temperature in laser controller
for current in range(0, 500+50, 100):
    print(f"current = {current} mA")
    laser.set_current(current=current)    # sleep(0.5)
    sleep(1)

    # reading data
    osa.simple_sweep()
    osa.read()
    wavelength_m = osa.wavelength_m
    power_dbm = osa.optical_power_dbm
    resolution = float(osa.osa.query(":sense:bandwidth?"))
    osa.osa.write(":calculate")
    sleep(0.3)
    power_integrated_dbm = float(osa.osa.query(":calculate:data?"))

    # saving data
    filename = f"experiment_{experiment}_{fiber}_{pump_laser}_{current}mA_{round(power_integrated_dbm,2)}dBm"
    filename = filename.replace(".", "_")
    filename = filename.replace("-", "neg")

    df = pd.DataFrame({'wavelength [m]': wavelength_m,
                  'optical power [dbm]': power_dbm,
                  'current [mA]': current,
                  'total optical power [dBm]': power_integrated_dbm,
                  'optical resolution [m]': resolution})
    df.to_csv("output/" + filename + ".csv", index=False)

    plt.plot(wavelength_m*1e9, power_dbm)
    plt.show(block=False)
    plt.pause(0.1)



laser.current_off()
input("Press Enter to exit...")

laser.laser.close()
osa.osa.close()

