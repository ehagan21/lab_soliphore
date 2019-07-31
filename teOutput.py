###############################################
# This file is used to transform PDFs into text files
# formatted correctly for the flag semaphore modules
# which require a start and end character
# When calling this python script, it has three parameters
# the pdf file name, it will output the same name as a txt
# the desired start character, and the desired end character
# these should match what is used on the arduino for differentiating between
# different modules

#! /usr/bin/env python
import sys
import re
from PyPDF2 import PdfFileReader
import textwrap

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
        cleanText = re.sub("[^a-zA-Z ]+"," ",line).upper()
	wrapper = textwrap.TextWrapper(width=50)
        
        #wraps the text to be 256 characters long
        shortTexts = wrapper.wrap(text=cleanText)

        #add start and end characters to text
        for element in shortTexts:
            added = startChar + element + endChar
            #append to array
            allText.append(added)

def writeText():
    #write everything to text file
    name = filename.strip('pdf') + 'txt'
    f = open(name, 'w')

    for line in allText:
        f.write(line+ '\n')
    f.close()

while (pdf.numPages > currentPage):
    runPage(currentPage)
    currentPage += 1

writeText()
