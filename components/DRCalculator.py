import numpy as np
import matplotlib.pyplot as plt

from Linearize import Linearize
from DumpUtils import dump_selection, dump_linearization
from Constants import Navogadro, Vmolar, omega_N2

class DRCalculator:
    ''' Class for area calculation using DR method '''
    __version = '0.0.2'
    
    def __init__(self, pp0, ads):
        self.__pp0 = pp0
        self.__ads = ads
    
    def __dump(self):
        dump_selection(self.__pp0, self.__ads, self.__ids_selection)
        dump_linearization(self.__pp0_log2_f, self.__ads_log_f, self.__s, self.__i, 'pp0_log2_f', 'ads_log_f')

        print("as     %2.2f m^2/g" % self.__SSA)
        print("V_mic  %2.2f m^2/g" % self.__V_mic)
    
    def run(self, doDump = True):
        self.__ids_selection = np.array(self.__pp0 > 0) * np.array(self.__pp0 < 0.09)
        pp0_truncated = self.__pp0[self.__ids_selection]
        ads_truncated = self.__ads[self.__ids_selection]

        self.__pp0_log2_f = np.log(1/pp0_truncated)**2
        self.__ads_log_f = np.log(ads_truncated/22.414)

        self.__s, self.__i, r2 = Linearize(self.__pp0_log2_f, self.__ads_log_f)
        self.__SSA = np.exp(self.__i) * Navogadro * omega_N2 / Vmolar
        self.__V_mic = np.exp(self.__i) * 0.001547

        if doDump:
            self.__dump()
            
    def getSSA(self):
        return abs(self.__SSA)
    
    def getVMic(self):
        return abs(self.__V_mic)
    
