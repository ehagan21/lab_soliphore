#! /usr/bin/env python
import sys
import re
from PyPDF2 import PdfFileReader

#load file
filename = sys.argv[1]

#add start and end characters
startChar = sys.argv[2]
endChar = sys.argv[3]

pdf = PdfFileReader(filename, 'rb')

allText = []

currentPage = 0

def runPage(currentPage):
    page = pdf.getPage(currentPage)

    text = page.extractText().encode('UTF-8')

    allLines = text.splitlines()

    for line in allLines:
        cleanText = startChar + re.sub("[^a-zA-Z ]+"," ",line).upper() + endChar + '\n'
        #append to array
        allText.append(cleanText)

def writeText():
    #write everything to a single text file
    #same name as the loaded pdf
    name = filename.strip('pdf') + 'txt'
    f = open(name, 'w')

    for line in allText:
        f.write(line)
    f.close()

while (pdf.numPages > currentPage):
    runPage(currentPage)
    currentPage += 1

writeText()
