import numpy as np
import matplotlib.pyplot as plt

from scipy.interpolate import Akima1DInterpolator as Akima

from Linearize import Linearize
from Constants import Navogadro, Vmolar, omega_N2

class BETCalculator:
    ''' Class for area calculation using BET method '''
    __version = '0.0.2'
    
    def __init__(self, pp0, ads):
        self.__pp0_inp = pp0
        self.__ads_inp = ads
        
    def __truncate_data_roquerol(self):
        # Taking all points below 0.3 p/p°
        BETrange = self.__pp0_inp < 0.3
        pp0BET = self.__pp0_inp[BETrange]
        adsBET = self.__ads_inp[BETrange]

        # Finding the right bound to calculate BET range
        self.__indRouquerol = np.argmax(adsBET*(1-pp0BET))
        
        # Taking the points until "indRouquerol" including
        self.__pp0_roquerol = pp0BET[:self.__indRouquerol+1]
        self.__ads_roquerol = adsBET[:self.__indRouquerol+1]
        
    
    def __dump(self):
        print(f'Удельная поверхность {self.__SSAbest:.2f} кв.м/г')
        print(f'Константа С {self.__C_best:.2f}')
            
        # Plotting results
        BETrange = self.__pp0_inp < 0.3
        pp0BET = self.__pp0_inp[BETrange]
        adsBET = self.__ads_inp[BETrange]
        
        # Points for calculating the surface area
        x = self.__pp0_roquerol[self.__idx_best_point:]
        y = 1/(self.__ads_roquerol[self.__idx_best_point:]*(1/x-1))

        #Points that are below the best range
        x_below_best_point = pp0BET[:self.__idx_best_point]
        y_below_best_point = 1/(adsBET[:self.__idx_best_point]*(1/x_below_best_point-1))

        #Points that are on the right from the Rouquerol
        x_higher_Rouquerol = pp0BET[self.__indRouquerol+1:]
        y_higher_Rouquerol = 1/(adsBET[self.__indRouquerol+1:]*(1/x_higher_Rouquerol-1))

        # The BET plot
        s,i,r2 = Linearize(x,y)
        x_graphic = np.linspace(0,np.max(pp0BET))

        fig = plt.figure()
        ax = fig.add_subplot(111)

        ax.plot(x,y,'go')
        ax.plot(x_graphic,s*x_graphic+i, 'k')
        ax.plot(x_below_best_point,y_below_best_point,'r*')
        ax.plot(x_higher_Rouquerol,y_higher_Rouquerol,'r*')

        ax.set_xlim(left=0)
        ax.set_ylim(bottom=0)
        ax.set_xlabel("Относительное давление p/p°")
        ax.set_ylabel("Переменная БЭТ, $\mathrm{г/н.см^3}$")

        textstr = '\n'.join((
            r'Удельная поверхность %.2f $\mathrm{м^2/г}$' % (self.__SSAbest,),
            r'Константа С %.2f' % (self.__C_best,)))

        props = dict(boxstyle='square', facecolor='white', alpha=0.0)
        ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=10,
                verticalalignment='top', bbox=props)
        plt.show()
    
    def run(self, doDump = True):
        self.__truncate_data_roquerol()
        
        # Isotherm interpolator
        interp = Akima(self.__pp0_roquerol, self.__ads_roquerol)

        # Auxiliary: length of arrays for results
        Nresults = np.shape(self.__pp0_roquerol)[0]-1

        # Here we put all values for deltas between the monolayer capacity 
        # from BET equation and the adsorption uptake at the point where 
        # the monolayer capacity should be achieved 
        absDelta = np.empty(Nresults)

        # Here we put the p/p° where the monolayer capacity should be achieved 
        pp0mono =  np.empty(Nresults)

        # Arrays for the results
        SSA = np.empty(Nresults)
        C = np.empty(Nresults)
        R2 = np.empty(Nresults)

        # Calculating specific surface area, C and R2 for each array
        for idx in range(Nresults):
            x = self.__pp0_roquerol[idx:]
            y = 1/(self.__ads_roquerol[idx:]*(1/x-1))

            s,i,r2 = Linearize(x,y)

            C[idx] = s/i+1
            R2[idx] = r2
            nmBET = 1/(s+i)
            SSA[idx] = nmBET * Navogadro * omega_N2 / Vmolar

            pp0mono[idx]=1/(np.sqrt(C[idx])+1)
            nm = interp(pp0mono[idx])
            absDelta[idx] = abs(nm - nmBET)
        else:
            # The monolayer p/p° should be within our range
            # For calculation we take IUPAC'2015 compliant points only
            isIUPAC = pp0mono > self.__pp0_roquerol[:-1] 

            # The best specific surface area
            self.__idx_best_point = np.argmin(absDelta[isIUPAC])
            self.__SSAbest = SSA[self.__idx_best_point]
            self.__C_best = C[self.__idx_best_point]
            
        if doDump:
            self.__dump()
            
    def getSSA(self):
        return self.__SSAbest

