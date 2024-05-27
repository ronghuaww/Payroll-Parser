from pypdf import PdfReader
from hoursParser import updateEmployees

reader = PdfReader('payrollPDFs/demoHours.pdf')
numPages = len(reader.pages)

# combined text from all pages into one large string
text = ''
for i in range(len(reader.pages)): 
    text += reader.pages[i].extract_text()

employees = []
updateEmployees(text, employees)

for i in employees: 
    print(i.name())

    for j in i.jobsList(): 
        print(j.totalHours())



