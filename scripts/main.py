from shiftParser import updateEmployees, hoursIntoDf
from configPdfs import combineText
import pandas

from tipParser import tipsIntoDf

# update input file names
employeesTimePdf = '8-19-9-1 payroll.pdf'
employeeTipsPdf = '8-19 9-1 tips.pdf'
employeeSsnCsv = '080524-081824-employeeinfo.csv'

outputFileCsv = '081924_090124 - Payroll.csv'

# update output file names
employees = []

# parsing through each employee's hours
timeText = combineText('input/hoursPDFs/' + employeesTimePdf)
updateEmployees(timeText, employees)
dfEmployeesTime = hoursIntoDf(employees)

# grabs the ssn of all employees from past documents
df = pandas.read_csv('input/ssnCSVs/' + employeeSsnCsv, header=None)
df.columns = ["Employee Name", "Social Security #", "Pay Rate"]

# grab tips earned by each employedd
tipText = combineText('input/tipsPDFs/' + employeeTipsPdf)
dfTip = tipsIntoDf(tipText)

# merge tips and ssn into one csv
final = dfEmployeesTime.merge(df,on=['Employee Name'], how="left")
final = final.merge(dfTip,on=['Employee Name'], how="left")

# output to a csv
final.to_csv('output/' + outputFileCsv)

