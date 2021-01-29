from . import EELS_controller

__author__ = "Yves Auad"

class EELS_Spectrometer(EELS_controller.EELSController):

    def __init__(self):
        super().__init__()

    def set_val(self, val, which):
        if abs(val)<32767:
            if val < 0:
                val = abs(val)
            else:
                val = 0xffff - val
            string = which+' 0,'+hex(val)[2:6]+'\r'
            print(string)
            return None
        else:
            logging.info("***EELS SPECTROMETER***: Attempt to write a value out of range.")
