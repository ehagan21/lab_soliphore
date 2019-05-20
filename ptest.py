import PyPDF2
pdfFileObj = open('mreport.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pdfReader.numPages
pageObj = pdfReader.getPage(75)
print(pageObj.extractText().encode('UTF_8'))
