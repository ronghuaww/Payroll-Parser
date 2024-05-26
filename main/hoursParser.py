from pypdf import PdfReader
import re
import datetime
from parsedData.employee import Employee
from parsedData.shift import Shift

from difflib import get_close_matches


reader = PdfReader('payrollPDFs/demoHours.pdf')
numPages = len(reader.pages)

text = ''
for i in range(len(reader.pages)): 
    text += reader.pages[i].extract_text()


# obtain the name and address of the establishment 
nameAddrExpr = re.compile(r'[a-zA-Z. &]+ - [a-zA-Z. &\d]+')
nameAddrSearch = nameAddrExpr.search(text)
nameAddr = nameAddrSearch.group().split(" - ")
name = nameAddr[0]
address = nameAddr[1]

print('Name:', name)
print('Address:', address)




# move down the starting point of the text
text = text[nameAddrSearch.end():]






# finding the nearest employee name 
EmployeeExpr = re.compile(r'\d+ - [a-zA-Z ]+')
nameEmploySearch = EmployeeExpr.search(text)
nameEmploy = nameEmploySearch.group().split(" - ")[1]

# find the end of the employee section 
employEndExpr = re.compile('Total Hours Worked This Pay Period')
employEndSearch = employEndExpr.search(text)

# one's data sections
employSection = text[nameEmploySearch.end():employEndSearch.end()]

timeExpr = r'\d{1,2}:\d{2}[a-zA-Z]{2}'
dateExpr = r'\d{1,2}/\d{1,2}/\d{4}'

# shift format for one date
lineOneExpr = r'[a-zA-Z ]+ \d+ - [a-zA-Z* ]+ ' + timeExpr + ' ' + dateExpr
lineTwoExpr = r'\n[a-zA-Z ]+\d*.\d+[ ]+' + timeExpr
shiftExpr = re.compile(lineOneExpr + lineTwoExpr)
shifts = re.findall(shiftExpr, employSection)

# shift format that holds two different dates 
shiftExtendExpr = re.compile(lineOneExpr + lineTwoExpr + ' ' + dateExpr)
shiftsExtend = re.findall(shiftExtendExpr, employSection)

# removing these duplicating shifts
for i in range(len(shiftsExtend)): 
    shifts.remove(get_close_matches(shiftsExtend[i], shifts, 1)[0]) 


shiftTemp = []

for i in range(len(shifts)): 
    shiftTimes = re.findall(timeExpr, shifts[i])
    shiftDate = re.findall(dateExpr, shifts[i]) 

    toTimeDateFormat = '%I:%M%p %m/%d/%Y'
    startTimeDate = shiftTimes[0] + " " + shiftDate[0]
    endTimeDate = shiftTimes[1] + " " + shiftDate[0]

    start = datetime.datetime.strptime(startTimeDate, toTimeDateFormat)
    end = datetime.datetime.strptime(endTimeDate, toTimeDateFormat)

    newShift = Shift(start, end)
    shiftTemp.append(newShift)




########### name and address only for first page, skip these index in later pages 

# find the name of people 



