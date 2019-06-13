from PyPDF2 import PdfFileReader
import re
import time

currentPage = 0

#def text_extractor(path):
    #with open(path, 'rb') as f:
pdf = PdfFileReader("/home/pi/lab/con.pdf", 'rb')
#pdf = PdfFileReader("mreport.pdf", 'rb')

def runPage(currentPage):
    #get the page
    page = pdf.getPage(currentPage)

    #encode the page and extract the text
    text = page.extractText().encode('utf-8')

    #save the text after adding start and end characters and using a regex to remove all non alpha, and uppercase
    cleanText = '<' + re.sub("[^a-zA-Z ]+","", text).upper() + '>'
    print(cleanText)

#if __name__ == '__main__':
    #path = "mreport.pdf"
    #text_extractor(path)

while (pdf.numPages > currentPage):
    runPage(currentPage)
    currentPage += 1
    time.sleep(2)
