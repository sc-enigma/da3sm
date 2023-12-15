class Info:
    ''' Base class. Experiment description '''
    __version = '0.0.2'
    
    def __init__(self,Info):
        self.__info = Info
    
    def readInfo(self)->dict:
        return self.__info
    
    def changeInfo(self, newInfo):
        self.__info = newInfo

    @property
    def Version(self)->str:
        return self.__version