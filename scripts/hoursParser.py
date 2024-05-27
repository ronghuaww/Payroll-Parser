import re
import datetime
from parsedData.employee import Employee
from parsedData.shift import Shift
from parsedData.enums.jobType import findJobName
from difflib import get_close_matches

TIME_EXPR = r'\d{1,2}:\d{2}[a-zA-Z]{2}'
DATE_EXPR = r'\d{1,2}/\d{1,2}/\d{4}'

HRS_NUM_EXPR = r'\d+?\.\d+'

""" Obtain the name and address of the establishment. 

Argument: extracted text from PDF 

Return: an list of various data 
    Index 0: name of the establishment 
    Index 1: address of the establishment
    Index 2: starting index of this string relative to text 
    Index 3: ending index of this string relative to text
"""
def nameAddress(text): 
    NAME_ADDR_EXPR = re.compile(r'[a-zA-Z. &]+ - [a-zA-Z. &\d]+')

    nameAddrSearch = NAME_ADDR_EXPR.search(text)
    nameAddr = nameAddrSearch.group().split(" - ")
    return [nameAddr[0], nameAddr[1], \
            nameAddrSearch.start(), nameAddrSearch.end()]


def __addingShifts(shifts, employee, extended=False): 
    TIME_DATE_FORMAT = '%I:%M%p %m/%d/%Y'

    for i in range(len(shifts)): 
        job = employee.addJob(findJobName(shifts[i]))

        shiftTimes = re.findall(TIME_EXPR, shifts[i])
        shiftDate = re.findall(DATE_EXPR, shifts[i]) 
        hrs = re.findall(HRS_NUM_EXPR, shifts[i])

        # make hours and date into one string to parse into later 
        startTimeDate = shiftTimes[0] + " " + shiftDate[0]
        endTimeDate = shiftTimes[1] + " " + shiftDate[0]

        if extended: 
            endTimeDate = shiftTimes[1] + " " + shiftDate[1]

        start = datetime.datetime.strptime(startTimeDate, TIME_DATE_FORMAT)
        end = datetime.datetime.strptime(endTimeDate, TIME_DATE_FORMAT)

        # add the shift to a given employee
        newShift = Shift(start, end, float(hrs[0]))
        job.addShift(newShift)


def updateEmployees(text, employees): 
    # finding the nearest employee name 
    EMPLOYEE_EXPR = re.compile(r'\d+ - [a-zA-Z ]+')

    # format for shifts under one date
    LINE_1_EXPR = r'[a-zA-Z ]+ \d+ - [a-zA-Z* ]+ ' + TIME_EXPR + ' ' + DATE_EXPR
    LINE_2_EXPR = r'\n[a-zA-Z ]+' + HRS_NUM_EXPR + '[ ]+' + TIME_EXPR
    SHIFTS_EXPR = re.compile(LINE_1_EXPR + LINE_2_EXPR)

    # format for shifts under two different dates 
    SHIFTS_EXTEND_EXPR = re.compile(LINE_1_EXPR + LINE_2_EXPR + ' ' + DATE_EXPR)

    # ending section indicator 
    EMPLOY_SECTION_END_EXPR = re.compile('Total Hours Worked This Pay Period')
    END_OF_DOC_INDEX = 163

    while len(text) > END_OF_DOC_INDEX: 
        nameEmploySearch = EMPLOYEE_EXPR.search(text)
        nameEmploy = nameEmploySearch.group().split(" - ")[1]

        employee = Employee(nameEmploy)
        employees.append(employee)

        # finding the employee's shift information section
        employEndSearch = EMPLOY_SECTION_END_EXPR.search(text)
        employSection = text[nameEmploySearch.end():employEndSearch.end()]

        # idenifying all the shifts
        shifts = re.findall(SHIFTS_EXPR, employSection)
        shiftsExtend = re.findall(SHIFTS_EXTEND_EXPR, employSection)

        # removing any duplicating shifts
        for i in range(len(shiftsExtend)): 
            shifts.remove(get_close_matches(shiftsExtend[i], shifts, 1)[0]) 

        __addingShifts(shifts, employee)
        __addingShifts(shiftsExtend, employee, True)

        # move down the starting point of the text
        text = text[employEndSearch.end():]


