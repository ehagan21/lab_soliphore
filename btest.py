#! /usr/bin/env python
import serial
import time
import json
import re
import atexit
from newsapi import NewsApiClient
from PyPDF2 import PdfFileReader

#loading credentials
with open('/home/pi/lab/config.json') as json_data_file:
    data = json.load(json_data_file)

#serial port information
port = "/dev/ttyACM0"
rate = 115200
ser = serial.Serial(port,rate, timeout = 1)
headlines = []

#Init
news_key = data["api_key"]
newsapi = NewsApiClient(api_key=news_key)
file = data["con"]

top_headlines = newsapi.get_top_headlines(language='en', country ='us')
#all_articles = newsapi.get_everything(q='flag', language = 'en', sort_by='relevancy')

#tracking where in the headlines array to send data
position = 0

#tracking which page of the pdf the system is interpreting
currentPage = 0

#this should occur inside a function, trying to figure out scope
pdf = PdfFileReader(file , 'rb')

def sanitize():
    for item in top_headlines["articles"]:
        xstring = item["title"].encode('utf-8')
        hlist = re.sub("[^a-zA-Z ]+", "", xstring)
        message = '<' + hlist.upper() + '>'
        headlines.append(message)
        print(message)

def runPage(currentPage):
    #scope question here as well
    page = pdf.getPage(currentPage)

    #encode the page and extract the text
    text = page.extractText().encode('utf-8')

    #save the text after adding new start and end character and using regex to remove all non alpha, convert to uppercase
    cleanText = '!' + re.sub("[^a-zA-Z ]+","",text).upper() + '?'
    print(cleanText)

def exit_handler():
    print("closing application")
    ser.flushOutput()
    ser.close()

sanitize()

#move this, just testing
while (pdf.numPages > currentPage):
    runPage(currentPage)
    currentPage += 1
    time.sleep(2)

if (ser.in_waiting>0):
    inData = ser.readline()
    if (inData == 'waiting'):
       ser.write('A')

#START THE LOOPING DATA SENT
try:
    while True:
        if (ser.out_waiting>0):
            time.sleep(2)
        elif (ser.in_waiting>0):
            data = ser.readline()
            if (data == 'waiting'):
                ser.write('A')
            else:
                print(data)
                ser.write(headlines[position])

        #loop through the headlines to play all necessary
            if (position < len(headlines)-1):
                position += 1
            else:
                position = 0
                #break

except KeyboardInterrupt:
    #cleanup
    exit_handler()

except:
    exit_handler()
