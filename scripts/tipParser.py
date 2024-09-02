import pandas
import re

""" 
    Parse through a document to create a list of employees and their tips
Argument: 
    text: extracted text from PDF 

Return: 
    dataframe: list of each employee's name and their tip amount 
"""
def tipsIntoDf(text): 

    EMPLOYEE_EXPR = re.compile(r'\d+ - [a-zA-Z ]+')  
    nameEmploySearch = re.findall(EMPLOYEE_EXPR, text)

    TIP_TOTAL_EXPR = re.compile(r'Employee Total[ ]+(?:\d*\,?\d+\.\d{2}%?[ ]+){8}')
    tipSearch = re.findall(TIP_TOTAL_EXPR, text)

    employeesTipsLists = []
    for i in range(len(nameEmploySearch)): 
        row = []

        fullName = nameEmploySearch[i].split(" - ")
        row.append(fullName[1].title())

        separateValues = tipSearch[i].split("  ")
        row.append(separateValues[6])

        employeesTipsLists.append(row)

    dfEmployeesTips = pandas.DataFrame(employeesTipsLists, columns = ["Employee Name", "Tips"])

    return dfEmployeesTips