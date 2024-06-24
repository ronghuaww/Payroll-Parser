from pypdf import PdfReader
import re

reader = PdfReader('payrollPDFs/demoTips.pdf')
numPages = len(reader.pages)

# combined text from all pages into one large string
text = ''
for i in range(len(reader.pages)): 
    text += reader.pages[i].extract_text()


TIP_TOTAL_EXPR = re.compile(r'Employee Total[ ]+(\d+?\.\d+%?[ ]+){8}')
tipSearch = TIP_TOTAL_EXPR.search(text)

print(text)
#print("ed--------", tipSearch.group(), "--")

for i in tipSearch: 
    print (i)

# 6,315.09 Employee Total  2,499.55  449.10  370.94  100.00 14.57%  920.04  449.10  370.94  0.00
#  0.00 Employee Total  0.00  0.00  0.00  0.00 0.00%  0.00  0.00  0.00  0.00


#print(text)