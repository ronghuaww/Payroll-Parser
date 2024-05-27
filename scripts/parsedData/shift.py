import datetime
import math

class Shift: 
    def __init__(self, start, end, hrs): 
        self.__start = start
        self.__end = end 
        self.__hrs = hrs

    def __str__(self): 
        return str(self.__start) + " " + str(self.__end)
    
    def hrs(self): 
        return self.__hrs
