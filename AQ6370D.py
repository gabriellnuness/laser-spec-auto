#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :   AQ6370D.py
@Time    :   2024/02/06 20:49:41
@Author  :   Roney D. Silva
@Contact :   roneyddasilva@gmail.com
"""
from inspect import Traceback
from pathlib import Path
import pyvisa
from numpy import asfarray, column_stack
import matplotlib.pyplot as plt
from time import sleep  # função para verificar o status byte do aparelho


class Trace(object):
    def __init__(self, trace_name: str):
        """__init__ class with trace's variables as wavelength and power
        Args:
            trace_name: a string of name of trace. TRA for trace A, TRB for trace B and etc. This OSA have 8 traces, so we have TRA, TRB, ... TRH.
        """
        super(Trace, self).__init__()
        self.trace_name = trace_name


# class Traces(Trace):
#     def __init__(self, trace_name: str):
#         """__init__ class with trace's variables as wavelength and power
#         Args:
#             trace_name: a string of name of trace. TRA for trace A, TRB for trace B and etc. This OSA have 8 traces, so we have TRA, TRB, ... TRH.
#         """
#         super(Traces, self).__init__(trace_name)
#         self.trace_name = trace_name
#         self = Trace(trace_name)


class AQ6370D(Trace):
    """
    AQ6370D Classe AQ6370D com GPIB

    _extended_summary_

    Args:
        object: _description_
    """

    def __init__(self, center=1550, gpib_address="GPIB0::1::INSTR", span=None):
        """
        __init__ constructor of AQ6370D Advantest
        Args:
            gpib_address: Defaults to 'GPIB0::8::INSTR'.
        """
        # super(AQ6370D, self).__init__()
        rm = pyvisa.ResourceManager("@py")
        # rm = pyvisa.ResourceManager()
        # print(rm.list_resources())
        self.osa = rm.open_resource(gpib_address)  # osa livre
        # self.osa.chunk_size = 65535  # comunitaiton setup
        self.osa.timeout = 200_000  # comunitaiton setup
        # self.osa.read_termination = "\r\n"  # comunitaiton setup
        self.check_error()
        if center != None:
            self.set_center(center)
        if span != None:
            self.set_span(span)

        self.y_unit_dic = {0: "dBm", 1: "nW", 2: "dBm/nm", 3: "nW/nm"}
        self.get_y_unit()

    def get_y_unit(self):
        self.y_unit = self.y_unit_dic[int(self.osa.query(":DISPlay:TRACE:Y1:UNIT?"))]

    def set_y_unit(self, unit="DBM/NM"):
        self.osa.write(":DISPLAY:TRACE:Y1:UNIT " + unit)
        self.get_y_unit()

    def set_resolution(self, resolution="20pm"):
        """set_resolution Set measurement resolution
        Args:
            resolution. Defaults to '20pm'.
        """
        self.osa.write(":SENSE:BANDWIDTH:RESOLUTION " + resolution)
        self.resolution = self.osa.query(":sense:bandwidth?")
        print("current resolution ", self.resolution)

    def set_sensitivity(self,sensitivity:str):
        """set_sensitivity

        Args:
            sensitivity: NHLD -> Normal hold
                NAUT -> Normal auto
                NORMAL -> Normal
                HIGH1 -> HIGH1 or HIGH1/CHOP
                HIGH2 -> HIGH2 or HIGH2/CHOP
                HIGH3 -> HIGH3 or HIGH3/CHOP
        """
        self.osa.write(":SENSE:SENSE "+sensitivity)

    def simple_sweep(self, trace="tra"):
        """
            simple_sweep() performs a data acquisition and updates the wavelength_NM variables with wavelength and optical_power_dbm with dbm power.
        Args:
                trace: a string with trance name trX with X a letter of trace. For example, trc for trace C.
                    Defaults to trace A.
        """

        self.osa.write(":INITIATE")  # make a sigle measurement
        # self.checkSTB(1)
        self.read(trace=trace)

    def read(self, trace="tra"):
        """
            Read () performs a data acquisition and updates the wavelength_NM variables with wavelength and optical_power_dbm with dbm power.
        Args:
                trace: a string with trance name trX with X a letter of trace. For example, trc for trace C.
                    Defaults to trace A.
        """
        # self.checkSTB(1)
        self.x = self.osa.query(":TRACE:X? " + trace)  # get wavelength
        self.y = self.osa.query(":TRACE:Y? " + trace)  # get optical power
        # remove reader
        # x = x[10:]
        # y = y[10:]
        # convert to numpy arrays
        self.wavelength_m = asfarray(self.x.split(","))
        self.optical_power_dbm = asfarray(self.y.split(","))

    def set_span(self, span: float, unit="M"):
        """
        set_span Set span of reads

        Args:
            span: float of wavelength center in meters or hz
            unit: The unit of span. Can be [M, HZ]. Defaults to 'M'.
        """
        self.span = span
        self.osa.write(":SENSE:WAVELENGTH:SPAN " + str(span) + str(unit))

    def set_center(self, center: float, unit="M"):
        """
        set_center Set center of measurement


        Args:
            center: float of wavelength center in meters or hz
            unit: The unit of center. Can be [M, HZ]. Defaults to 'M'.
        """
        self.center = center
        self.osa.write(":SENSE:WAVELENGTH:CENTER " + str(center) + unit)

    def check_error(self):
        self.error = self.osa.query(":SYSTEM:ERROR?")
        if int(self.error) != 0:
            print(self.error)

    def close(self):
        '''close Close serial comunication
        '''
        self.osa.close()