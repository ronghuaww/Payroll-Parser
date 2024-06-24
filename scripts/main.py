from pypdf import PdfReader
from shiftParser import updateEmployees

reader = PdfReader('payrollPDFs/demoHours.pdf')
numPages = len(reader.pages)

# combined text from all pages into one large string
text = ''
for i in range(len(reader.pages)): 
    text += reader.pages[i].extract_text()

employees = []
updateEmployees(text, employees)

    
new_list = sorted(employees, key=lambda x: x.jobsList()[0].type().value, reverse=True)


for i in employees: 
    print(i.name())

    for j in i.jobsList(): 
        print(j.type().value)
        print(j.totalHours())
