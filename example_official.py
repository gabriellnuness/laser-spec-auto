#
# Yokogawa AQ63XX OSA sample program (PyVISA)
# Remote Interface = GPIB
#
# This sample program requires pyvisa.
#
# AQ63XX Setting: [SYSTEM]<REMOTE INTERFACE> = "GP-IB"
# GPIB Address = 1
#
import pyvisa

def left(text, n):
    return text[:n]


if '__main__' == __name__: # execute only if run as a script

    # open OSA (GPIB address = 1)
    rm = pyvisa.ResourceManager()
    osa = rm.open_resource("GPIB0::1")

    # Get *IDN query
    a = osa.query("*IDN?")
    print(a)

    # Set command mode = AQ637X/AQ638X mode
    osa.write("CFORM1")

    # single sweep
    osa.write("*CLS; :init")

    #wait until sweep complete
    while True:
        a = osa.query(":stat:oper:even?")
        if left(a,1) == "1":
            break
    print("sweep complete")

    # Measure spectrum width
    a = osa.query(":calc:cat swth; :calc; :calc:data?")
    print(a)

    # close osa
    osa.close()

    
    
    


