import numpy as np
from Info import Info
from CurveData import CurveData

class ASAP2400file(Info):
    __version = '0.0.2'

    def __init__(self,filename):
        info = self.readInfo(filename)
        self.__timep0,self.__p0,self.__timeads,self.__p,self.__FullIsotherm = self.readData(filename)
                
        maxPP0Index = np.argmax(self.__FullIsotherm.X)

        self.__pp0ads = self.__FullIsotherm.X[:maxPP0Index+1]
        self.__adsUptake = self.__FullIsotherm.Y[:maxPP0Index+1]
        self.__pp0des = self.__FullIsotherm.X[maxPP0Index:]
        self.__desUptake = self.__FullIsotherm.Y[maxPP0Index:]

        super().__init__(info)
    
    @staticmethod
    def readInfo(filename):
        current = '' # Current line
        with open(filename,'r') as ASAP:
            # Header reading
            LineNumber  = 0
            Titles = ['Micromeritics Instrument Corporation','Texture Research Laboratory']

            current = ASAP.readline().strip()
            LineNumber += 1

            if not current in Titles:
                print(f'File {filename} could not be read')
                return {}
                        
            current = ASAP.readline().strip()
            LineNumber += 1
            FileType = ' '.join(current.split()[0:3])
            
            current = ASAP.readline()
            LineNumber += 1

            current = ASAP.readline().strip()
            LineNumber += 1
            ASAPDataFile = ''.join(current.split()[2:4])
            AnalysisStartDate =' '.join(current.split()[5:7])
            
            current = ASAP.readline().strip()
            LineNumber += 1
            SampleID = current[10:52].strip()
            AnalysisFinishDate = ' '.join(current[52:].split()[1:3])
            
            current = ASAP.readline().strip()
            LineNumber += 1
            Submitter = current[10:52].strip()
            ReportDate = ' '.join(current[52:].split()[1:3])

            current = ASAP.readline().strip()
            LineNumber += 1
            Operator = current[10:52].strip()
            Weight = float(current[52:].split()[2])
                        
            current = ASAP.readline().strip()
            LineNumber += 1
            StationNumber = int(current[15:24].strip())
            EquilibrationInterval = int(current[40:46].strip())
            FreeSpace = float(current[52:].split()[2])
        
        return {
            'Version':FileType,
            'Data':ASAPDataFile,
            'Start':AnalysisStartDate,
            'Finish':AnalysisFinishDate,
            'SampleID':SampleID,
            'Report':ReportDate,
            'Submitter':Submitter,
            'Operator':Operator,
            'Weight':Weight,
            'Station':StationNumber,
            'Equilibration, sec':EquilibrationInterval,
            'Free Space':FreeSpace}

    @staticmethod
    def readData(filename):
        # Isotherm and measurement data readings
            
        # Possible title of the header of the file
        
        
        with open(filename,'r') as ASAP: 
            current = '' # Current line  
            dummy = [] # Dummy list variable     
            linesMeasurements = []
            InFileHeader = False
            InAnalysisLog = False
                        
            FileTitles = ['Micromeritics Instrument Corporation','Texture Research Laboratory']
            AnalysisTitles = ['ANALYSIS LOG']
            BETTitles = ['BET SURFACE AREA REPORT']
            DataStartAfterLog = 4
            current = ASAP.readline().strip()
            LineNumber = 1

            while not(current in BETTitles) :
                # If on the top of the page, skip

                if current in FileTitles:
                    InFileHeader = True
                    InAnalysisLog = False
                    current = ASAP.readline().strip()
                    LineNumber += 1
                    continue
                # If still on the top, skip

                if InFileHeader and not(current in AnalysisTitles):
                    current = ASAP.readline().strip()
                    LineNumber += 1
                    continue
                
                if current in AnalysisTitles:
                        InFileHeader = False
                        InAnalysisLog = True
                        AnalysisLogHeaderStart = LineNumber
                        current = ASAP.readline().strip()
                        LineNumber += 1
                        continue
                
                if InAnalysisLog:
                    if LineNumber < AnalysisLogHeaderStart + DataStartAfterLog:
                        current = ASAP.readline().strip()
                        LineNumber += 1
                        continue
                    elif current != '':
                        linesMeasurements.append(current)
                        current = ASAP.readline().strip()
                        LineNumber += 1
                        continue
                    else:
                        current = ASAP.readline().strip()
                        LineNumber += 1
                        continue
                                   
        p0 = []
        pp0 = []
        timep0 = []
        timeads = []
        ads = []
        p = []
        
        for point in linesMeasurements:
            dummy = point.split()
            if len(dummy)==2:
                timep0.append(dummy[0])
                p0.append(float(dummy[1]))
            if len(dummy)==4:
                pp0.append(float(dummy[0]))
                p.append(float(dummy[1]))
                ads.append(float(dummy[2]))
                timeads.append(dummy[3])
        
        return timep0,p0,timeads,p,CurveData(pp0,ads)

    @property
    def AdsPP0(self):
        return self.__pp0ads
    
    @property
    def DesPP0(self):
        return self.__pp0des

    @property
    def AdsUptake(self):
        return self.__adsUptake
    
    @property
    def DesUptake(self):
        return self.__desUptake

    @property
    def FullPP0(self):
        return self.__FullIsotherm.X

    @property
    def FullUptake(self):
        return self.__FullIsotherm.Y

    @property
    def Version(self)->str:
        return self.__version 