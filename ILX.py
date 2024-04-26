import pyvisa



def config(gpib_address="GPIB0::12::INSTR"):

    rm = pyvisa.ResourceManager()
    ilx = rm.open_resource(gpib_address)
    print(ilx.query("*idn?"))
    return ilx



if __name__ == '__main__':
    config()
    