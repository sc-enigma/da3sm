import numpy as np
import matplotlib.pyplot as plt

from BETCalculator import BETCalculator
from Linearize import Linearize
from DumpUtils import dump_selection, dump_linearization

class TCurveCalculator:
    ''' Class for area calculation using t curve method '''
    __version = '0.0.2'
    
    def __init__(self, pp0, ads):
        self.__pp0 = pp0
        self.__ads = ads
     
    def __dump(self):
        dump_selection(self.__pp0, self.__ads, self.__ids_selection)
        dump_linearization(self.__t, self.__ads_truncated, self.__s_t, self.__i_t, 't', 'ads')

        print("as     %2.2f m^2/g" % self.__SSA)
        print("as_ext %2.2f m^2/g" % self.__as_ext)
        print("as_mic  %2.2f m^2/g" % self.__as_mic)
    
    def run(self, doDump=True):
        self.__ids_selection = np.array(self.__pp0 > 0.2) * np.array(self.__pp0 < 0.5)
        self.__pp0_truncated = self.__pp0[self.__ids_selection]
        self.__ads_truncated = self.__ads[self.__ids_selection]

        # BET calculation
        area_calculator = BETCalculator(self.__pp0, self.__ads)
        area_calculator.run(doDump=False)
        self.__SSA = area_calculator.getSSA()

        # t curve method calculation
        self.__pp0_log = np.log10(self.__pp0_truncated)
        self.__t = np.sqrt((13.99 / (0.034 - self.__pp0_log)))

        self.__s_t, self.__i_t, r2 = Linearize(self.__t, self.__ads_truncated)
        self.__as_ext = 15.47 * self.__s_t
        self.__V_mic = 0.001547 * self.__i_t
        self.__as_mic = self.__SSA - self.__as_ext

        # dump output           
        if doDump:
            self.__dump()
         
    def getAsMic(self):
        return abs(self.__as_mic)
    
    def getVMic(self):
        return abs(self.__V_mic)
    
