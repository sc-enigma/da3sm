import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import Akima1DInterpolator as Akima

from ASAP2400file import ASAP2400file
from Linearize import Linearize
from BETCalculator import BETCalculator
from DumpUtils import dump_selection, dump_linearization

class AlphaSCalculator:
    ''' Class for area calculation using alpha s method '''
    __version = '0.0.2'
    
    def __init__(self, pp0_ref, ads_ref, pp0_sample, ads_sample):
        self.__pp0_ref = pp0_ref
        self.__ads_ref = ads_ref
        self.__pp0_sample = pp0_sample
        self.__ads_sample = ads_sample
    
    def __dump(self):
        print("as     %2.2f m^2/g" % self.SSA_sample)
        print("as_mic  %2.2f m^2/g" % self.as_mic)
        print("v_mic %2.2f cm^3/g" % self.v_mic)
        
    def run(self, doDump=True):        
        interp_ref = Akima(self.__pp0_ref, self.__ads_ref)        
        scale_ref = 1.0 / interp_ref(0.4)
        
        # alpha s selection
        alphas_prep = interp_ref(self.__pp0_sample) * scale_ref
        ids_selection = np.array(alphas_prep > 0.5)*np.array(alphas_prep < 1.0)
        
        if doDump:
            print('alpha s selection')
            dump_selection(alphas_prep, self.__ads_sample, ids_selection, '$alpha_{s}$', '$ads_{sample}$')
        self.__alphas = alphas_prep[ids_selection]
        self.__ads_sample_alphas = self.__ads_sample[ids_selection]

        # alpha s lineariztion
        s_alphas, i_alphas, r2 = Linearize(self.__alphas, self.__ads_sample_alphas)
        if doDump:
            print('alpha s lineariztion')
            dump_linearization(self.__alphas, self.__ads_sample_alphas, s_alphas, i_alphas, '$alpha_{s}$', '$ads_{sample alpha s}$')
        
        # BET calculation for reference
        if doDump:
            print('BET calculation for reference')
        area_calculator_ref = BETCalculator(self.__pp0_ref, self.__ads_ref)
        area_calculator_ref.run(doDump)
        SSA_ref = area_calculator_ref.getSSA()
        
        # BET calculation for sample
        if (doDump):
            print('BET calculation for sample')
        area_calculator_sample = BETCalculator(self.__pp0_sample, self.__ads_sample)
        area_calculator_sample.run(doDump)
        self.SSA_sample = area_calculator_sample.getSSA()
        
        # Alpha s calculation
        self.as_ext = s_alphas * SSA_ref
        self.v_mic = 0.001547 * i_alphas
        self.as_mic = self.SSA_sample - self.as_ext
        
        if (doDump):
            self.__dump()

    def getAsMic(self):
        return self.as_mic
        
    def getVMic(self):
        return self.v_mic
        