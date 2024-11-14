import numpy as np
import os
from ..service import*

class Material:
    """
    Свойства материала
    =====

    Данные о свойствах используемых материалов размещаются в блоке global variables файла kordat

    Attributes
    ----------
    name : str
        имя материала
        
    T : np.ndarray
        Массив значений температуры для аппроксимации температурной зависимости свойств [К]
        
    LAM : np.ndarray
        Массив значений теплопроводности материала [Вт/м2*К]
        
    HC : np.ndarray
        Массив значений теплоемкости материала [Дж/кг*К]
        
    RO : np.ndarray
        Массив значений плотности материала [кг/м3]

    tlam : str
        Имя массива значений теплопроводности в kordat
        
    thc : str
        Имя массива значений теплоемкости в kordat
        
    trho : str
        Имя массива значений плотности в kordat
        

    Methods
    ----------
    rebuild_data
        Перестраивает блок переменных материала для kordat

    """
    def __init__(
        self,
        name: str,
        T: np.ndarray,
        LAM: np.ndarray,
        HC: np.ndarray,
        RO: np.ndarray
    ):
        self.name = name
        self.T = T
        self.LAM = LAM
        self.HC = HC
        self.RO = RO
        
        self.tlam = "_tlam_"+self.name
        self.thc = "_thc_"+self.name
        self.tro = "_tro_"+self.name

        self.__globals__ = []

        self.rebuild_data()

    def __write_data__(self, path: str = ""):
        """
        Записать блок переменных для kordat
        
        Arguments
        ----------
        path : str
            Полный путь к файлу зоны задания
        """
        if path == "":
            path = os.path.join("./"+self.name+".txt")

        write_data(self.__globals__,path)

    def rebuild_data(self):
        self.tlam = "_tlam_"+self.name
        self.thc = "_thc_"+self.name
        self.tro = "_tro_"+self.name

        self.__globals__ = []        

        # tlam
        self.__globals__.append(self.tlam+"(1:2,1:"+str(len(self.LAM))+") =")
        [self.__globals__.append('\t'+str(t)+","+str(var)+",") for t,var in zip(self.T,self.LAM)]
        self.__globals__[-1] = '\t'+str(self.T[-1])+","+str(self.LAM[-1])+";"
        
        # thc
        self.__globals__.append(self.thc+"(1:2,1:"+str(len(self.HC))+") =")
        [self.__globals__.append('\t'+str(t)+","+str(var)+",") for t,var in zip(self.T,self.HC)]
        self.__globals__[-1] = '\t'+str(self.T[-1])+","+str(self.HC[-1])+";"
        
        # tro
        self.__globals__.append(self.tro+"(1:2,1:"+str(len(self.RO))+") =")
        [self.__globals__.append('\t'+str(t)+","+str(var)+",") for t,var in zip(self.T,self.RO)]
        self.__globals__[-1] = '\t'+str(self.T[-1])+","+str(self.RO[-1])+";"

        self.__globals__.insert(0, "!!bb Properties "+self.name)
        self.__globals__.append("!!eb Properties "+self.name)
