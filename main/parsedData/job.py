import datetime
#from enums.jobType import JobType
#from shift import Shift

try:
    from shift import Shift
except ImportError:
    from .shift import Shift


class Job: 
    def __init__(self, type): 
        self.__type = type
        self.__wage = 0
        self.__shifts = []
    
    def addShift(self, shift): 
        self.__shifts.append(shift)
    
    def type(self): 
        return self.__type
    
    def totalHours(self): 
        total = 0
        for shift in self.__shifts: 
            total += shift.calcHrs()
        return total 
    