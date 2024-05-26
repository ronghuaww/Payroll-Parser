from pypdf import PdfReader
import re
import datetime
from parsedData.employee import Employee
from parsedData.shift import Shift
from parsedData.enums.jobType import JobType, findJobName

from difflib import get_close_matches


TIME_EXPR = r'\d{1,2}:\d{2}[a-zA-Z]{2}'
DATE_EXPR = r'\d{1,2}/\d{1,2}/\d{4}'


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

employee = Employee(nameEmploy)

# find the end of the employee section 
employEndExpr = re.compile('Total Hours Worked This Pay Period')
employEndSearch = employEndExpr.search(text)

# one employee's shifts sections
employSection = text[nameEmploySearch.end():employEndSearch.end()]

# shift format for one date
LINE_1_EXPR = r'[a-zA-Z ]+ \d+ - [a-zA-Z* ]+ ' + TIME_EXPR + ' ' + DATE_EXPR
LINE_2_EXPR = r'\n[a-zA-Z ]+\d*.\d+[ ]+' + TIME_EXPR
shiftExpr = re.compile(LINE_1_EXPR + LINE_2_EXPR)
shifts = re.findall(shiftExpr, employSection)

# shift format that holds two different dates 
shiftExtendExpr = re.compile(LINE_1_EXPR + LINE_2_EXPR + ' ' + DATE_EXPR)
shiftsExtend = re.findall(shiftExtendExpr, employSection)

# removing these duplicating shifts
for i in range(len(shiftsExtend)): 
    shifts.remove(get_close_matches(shiftsExtend[i], shifts, 1)[0]) 


def addingEmployeeShifts(shifts, employee, extended=False): 
    for i in range(len(shifts)): 
        job = employee.addJob(findJobName(shifts[i]))

        shiftTimes = re.findall(TIME_EXPR, shifts[i])
        shiftDate = re.findall(DATE_EXPR, shifts[i]) 

        TIME_DATE_FORMAT = '%I:%M%p %m/%d/%Y'
        startTimeDate = shiftTimes[0] + " " + shiftDate[0]
        endTimeDate = shiftTimes[1] + " " + shiftDate[0]

        if extended: 
            endTimeDate = shiftTimes[1] + " " + shiftDate[1]

        start = datetime.datetime.strptime(startTimeDate, TIME_DATE_FORMAT)
        end = datetime.datetime.strptime(endTimeDate, TIME_DATE_FORMAT)

        newShift = Shift(start, end)
        job.addShift(newShift)

addingEmployeeShifts(shifts, employee)
addingEmployeeShifts(shiftsExtend, employee, True)


print(employee.totalJobHours(JobType.MANAGER))
