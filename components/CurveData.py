import numpy as np

class CurveData:
    '''Curve Y vs. X'''
    __version = '0.0.2'

    def __init__(self,arrayX=[], arrayY=[]):
        if len(arrayX)!=len(arrayY):
            raise ValueError
        self.__X = np.array(arrayX)
        self.__Y = np.array(arrayY)

    @property
    def Version(self)->str:
        return self.__version    
    
    def changeData(self,arrayX, arrayY):
        if len(arrayX)!=len(arrayY):
            raise ValueError
        self.__X = np.array(arrayX)
        self.__Y = np.array(arrayY)

    @property
    def X(self)->np.ndarray:
        return self.__X

    @property
    def Y(self)->np.ndarray:
        return self.__Y