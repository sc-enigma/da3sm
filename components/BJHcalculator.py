import numpy as np
import matplotlib.pyplot as plt

class BJHcalculator:
    def __init__(self, pp0, uptake):
        self.__AN2        = 9.53                    # Rc = - 9.53 / ln(P/P0) [angstrem]
        self.__D_liq      = 0.0015467998750517348
        
        self.__pp0        = np.array(pp0)
        self.__uptake     = np.array(uptake)
        self.__nbPoints   = len(pp0)
        
        self.__uptake    *= self.__D_liq
    
    def __init_arrays(self, length):
        # temporary data
        self.__Vd_current = 0.0
        self.__Rc         = -self.__AN2 / np.log(self.__pp0)  

        # internal data
        self.__Rc_upper   = np.zeros(length)
        self.__Rc_bottom  = np.zeros(length)
        self.__D_avg      = np.zeros(length)
        self.__LP         = np.zeros(length)
        self.__pore_ids   = []
        
    def __average(self, a, b):
        return (a + b) * a * b / (a * a + b * b)
    
    # thickness of wall. Толщина пленки для уравнения Кельвина
    def __TwHalsey(self, val, scale=3.54, numerator=-5, power=0.333):
        return scale * np.power(numerator / np.log(val), power)

    def __process_new_pore(self, idx):
        # Rc = -AN2 / np.log(pp0)
        # P_avg = exp( -AN2 / Davg )
        
        self.__pore_ids.append(idx)
        
        self.__Rc_upper[idx] = self.__Rc[idx]
        self.__Rc_bottom[idx] = self.__Rc[idx + 1]
        self.__D_avg[idx] = 2.0 * self.__average(self.__Rc_upper[idx], self.__Rc_bottom[idx])   
    
        P_avg = np.exp(-2.0 * self.__AN2 / self.__D_avg[idx])
        deltaTw = self.__TwHalsey(P_avg) - self.__TwHalsey(self.__pp0[idx + 1])
        Vc = self.__uptake[idx] - self.__uptake[idx + 1] - self.__Vd_current
        CSA = np.pi * (0.5 * self.__D_avg[idx] + deltaTw) ** 2
        self.__LP[idx] = Vc / CSA
        
        delta_tw = self.__TwHalsey(self.__pp0[idx]) - self.__TwHalsey(self.__pp0[idx + 1])
        
        for idx_pore in self.__pore_ids: 
            self.__D_avg[idx_pore] += 2.0 * deltaTw
            self.__Rc_upper[idx_pore] += delta_tw
            if idx_pore != idx:
                self.__Rc_bottom[idx_pore] += delta_tw

    def __update_no_new_pore(self, idx):
        SA_wall = 0.0
        for idx_pore in self.__pore_ids:
             SA_wall += np.pi * self.__D_avg[idx_pore] * self.__LP[idx_pore]
        Vc = self.__uptake[idx] - self.__uptake[idx + 1]
        delta_Tw = Vc / SA_wall
        
        for idx_pore in self.__pore_ids:
            self.__D_avg[idx_pore]      += 2.0 * delta_Tw
            self.__Rc_upper[idx_pore]  += delta_Tw
            self.__Rc_bottom[idx_pore] += delta_Tw
    
    def __iter_step(self, idx):
        delta_tw = self.__TwHalsey(self.__pp0[idx]) - self.__TwHalsey(self.__pp0[idx + 1])
        
        Vc = self.__uptake[idx] - self.__uptake[idx + 1]
            
        self.__Vd_current = 0.0
        for idx_pore in self.__pore_ids:
            self.__Vd_current += np.pi * (delta_tw + self.__D_avg[idx_pore]) * delta_tw * self.__LP[idx_pore]
        
        is_last_pore = idx == self.__nbPoints - 2
        
        if (Vc  > self.__Vd_current and not is_last_pore):
            self.__process_new_pore(idx)       # new pore
        else:
            self.__update_no_new_pore(idx)     # no new pore
    
    def run(self, doDump=True):
        self.__init_arrays(self.__nbPoints)
        self.__process_new_pore(0)
        
        idx_last = self.__nbPoints - 2
        for idx_point in range(1, idx_last):
            self.__iter_step(idx_point)
        
        self.__update_no_new_pore(idx_last)
        if doDump:
            self.dumpResult()
    
    def getResult(self):
        D_upper = 2.0 * self.__Rc_upper[self.__pore_ids]
        D_bottom = 2.0 * self.__Rc_bottom[self.__pore_ids]
        d_D_log = np.log10(D_upper) - np.log10(D_bottom)
        D_avg = self.__D_avg[self.__pore_ids] *  1.125
        
        V_inc = np.pi * self.__LP[self.__pore_ids] * (self.__D_avg[self.__pore_ids]**2) * 0.25
        return D_avg * 0.1, V_inc / d_D_log
    
    def dumpResult(self):
        D_avg, d_V_inc = self.getResult()
        plt.plot(D_avg, d_V_inc, color='k')
        plt.scatter(D_avg, d_V_inc, color='k')
        plt.semilogx()
        plt.xlabel('$D_{average}$ [nm]')
        plt.ylabel('$d$ $V_{inc}$  /  $d$ $ln(D_{average})$')
        xticks = [10, 25, 50, 100]
        plt.xticks(xticks, [str(tick) for tick in xticks])
        plt.show()
        