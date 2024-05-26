import datetime

class Shift: 
    def __init__(self, start, end): 
        self.start = start
        self.end = end 

    def __str__(self): 
        return str(self.start) + " " + str(self.end)
    
    def calcHrs(self): 
        timeDiff = self.end - self.start
        timeDiffSeconds = timeDiff.total_seconds()
        hrSeconds = datetime.timedelta(hours=1).total_seconds()
        return timeDiffSeconds / hrSeconds
