import csv

startDate = "061024"
endDate = "062324"

with open('061024_062324 - HW Payroll.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    
    writer.writerow(["Company Name: HW"])
    writer.writerow(["Payroll Report"])
    writer.writerow(["For the period from 06/10/2024 to 06/23/2024"])


    writer.writerow(["Employee Name", "Social Security #", "Pay Type", "Pay Rate", "Regular Hrs", "OT Hrs", "Tips", "Total"])

