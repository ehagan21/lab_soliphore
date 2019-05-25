from PyPDF2 import PdfFileReader
import re

def text_extractor(path):
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        
        #get the first page
        page = pdf.getPage(3)
        print(page)
        print('Page type: {}'.format(str(type(page))))

        text = page.extractText().encode('utf-8')
        cleanText = re.sub("[^a-zA-Z ]+","", text)
        print(cleanText)

if __name__ == '__main__':
    path = "mreport.pdf"
    text_extractor(path)
