import PyPDF2
pdfFileObj = open('mreport.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pdfReader.numPages
page = pdfReader.getPage(75)
text = page.extractText()
print(text.encode('UTF_8')
