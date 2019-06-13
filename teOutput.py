#! /usr/bin/env python
import sys
from PyPDF2 import PdfFileReader

#load file
filename = sys.argv[1]

#add start and end characters
startChar = sys.argv[2]
endChar = sys.argv[3]

pdf = PDFFileReader(filename, 'rb')

allText = []

def runPage(currentPage):
    page = pdf.getPage(currentPage)

    text = page.extractText().encode('UTF-8')

    #split by line here?

    cleanText = startChar + re.sub("[^a-zA-Z ]+","",text).upper() + endChar

    #append to array
    allText.append(cleanText)

def writeText():
	#write everything to a single text file
	#same name as the loaded pdf

while (pdf.numPages > currentPage):
    runPage(currentPage)
    currentPage += 1

writeText()
