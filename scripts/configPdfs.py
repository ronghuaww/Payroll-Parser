from pypdf import PdfReader

def combineText(PDFName): 
    # combined text from all pages into one large string
    reader = PdfReader(PDFName)

    text = ''
    for i in range(len(reader.pages)): 
        text += reader.pages[i].extract_text()
    
    return text