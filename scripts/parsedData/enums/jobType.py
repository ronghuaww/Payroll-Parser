from enum import Enum

class JobType(Enum):
    MANAGER = 1
    HOST = 2
    PACKERS = 3
    SERVER = 4
    BARTENDER = 5
    BUSSER = 6
    KITCHEN = 7
    COOK = 8

def findJobName(text): 
    # match needs python 10 or higher
    match text: 
        case text if "Manager" in text: 
            return JobType.MANAGER
        
        case text if "Host" in text: 
            return JobType.HOST
        
        case text if "Packer" in text: 
            return JobType.PACKERS       

        case text if "Server" in text:
            return JobType.SERVER
        
        case text if "Bartender" in text:
            return JobType.BARTENDER
        
        case text if "Busser" in text:
            return JobType.BUSSER
        
        case text if "Kitchen" in text: 
            return JobType.KITCHEN
        
        case text if "Cook" in text: 
            return JobType.COOK
