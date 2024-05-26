import datetime
#from enums.jobType import JobType
#from shift import Shift


class Job: 
    def __init__(self, name, wage, tipped = False): 
        self.name = name
        self.wage = wage
        self.shifts = []
        self.tipped = tipped
    
    def addShift(self, start, end): 
        newShift = Shift(start, end)
        self.shifts.append(newShift)