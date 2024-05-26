from pypdf import PdfReader
import re
import datetime
from parsedData.employee import Employee
from difflib import get_close_matches

test = Employee("te", "te")
print("EM", test)


reader = PdfReader('payrollPDFs/demoHours.pdf')
numPages = len(reader.pages)
text = reader.pages[0].extract_text()


# obtain the name and address of the establishment 
firstPage = reader.pages[0]
nameAddrFind = re.search(r'[a-zA-Z.\d]+ - [a-zA-Z.\d]+', firstPage.extract_text())
spiltnameAddr = nameAddrFind.string.split(" - ")
name = spiltnameAddr[0]
address = spiltnameAddr[1]

print('Name:', name)
print('Address:', address)





namingExpr = r'\d+ - [a-zA-Z ]+'
n = re.findall(namingExpr, text)


def removeOccupations(n): 
    occupations = ['Kitchen', 'Server', 'Busser', 'Manager', 'Host']
    for i in occupations: 
        if i in n: 
            return False
    return True
        
filtered = filter(removeOccupations, n)
for s in filtered:
    print("uhh", s)



# ThuIN No Schedule 103 - Kitchen 10:54am 5/9/2024
# OUT No Schedule  5.40 4:18pm

# FriIN No Schedule 101 - *Server Tbl 3:17pm 5/10/2024
# OUT No Schedule  7.72 11:00pm estela flores On Time
timeExpr = r'\d{1,2}:\d{2}[a-zA-Z]{2}'
dateExpr = r'\d{1,2}/\d{1,2}/\d{4}'

firstHrLineExpr = r'[a-zA-Z ]+ \d+ - [a-zA-Z* ]+ ' + timeExpr + ' ' + dateExpr
secHrLineExpr = r'\n[a-zA-Z ]+\d*.\d+[ ]+' + timeExpr
shiftExpr = re.compile(firstHrLineExpr + secHrLineExpr)
t = re.findall(shiftExpr, text)
print(t)
print(len(t))

shiftTimes = re.findall(timeExpr, t[0])
print("shift", shiftTimes)

shiftDates = re.findall(dateExpr, t[0])
print("shiftDate", shiftDates)


# timeStamps = re.findall(timeExpr, text)
# print(timeStamps)

# dateStamps = re.findall(dateExpr, text)
# print(dateStamps)


# FriIN No Schedule 103 - Kitchen 8:13am 5/10/2024
# OUT Sat No Schedule  15.83 12:03am 5/11/2024

# MonIN No Schedule 101 - *Server Tbl 10:30am 5/6/2024
# OUT Tue Mgr Clock Out  28.78 3:16pm 5/7/2024 estela flores On Time

# overlaps w prev list 
hourOverlapExpr = re.compile(firstHrLineExpr + secHrLineExpr + ' ' + dateExpr)
y = re.findall(hourOverlapExpr, text)
print(y)

print("close", get_close_matches(y[0], t, 1))


t.remove(get_close_matches(y[0], t, 1)[0]) 
print(t)


startTime = datetime.datetime.strptime(shiftTimes[0] + " " + shiftDates[0], "%I:%M%p %m/%d/%Y")
print("datetime", startTime)



########### name and address only for first page, skip these index in later pages 

# find the name of people 



