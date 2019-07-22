#! /usr/bin/env python
import serial
import time
import json
import re
import atexit
from newsapi import NewsApiClient

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

top_headlines = newsapi.get_top_headlines(language='en', country ='us')
#all_articles = newsapi.get_everything(q='flag', language = 'en', sort_by='relevancy')

#load text file into python, save text in a list to be sent to raspberry pi
def fileload(filename):
    text_file = open(filename, "r")
    lines = text_file.read().splitlines()
    text_file.close()
    return lines

def sanitize():
    for item in top_headlines["articles"]:
        xstring = item["title"].encode('utf-8')
        hlist = re.sub("[^a-zA-Z ]+", "", xstring)

        #keep in mind this is the start and end character, determine which pair the message goes to
        message = '<' + hlist.upper() + '>'
        headlines.append(message)
        #print(message)

def exit_handler():
    print("closing application")
    ser.flushOutput()
    ser.close()

sanitize()

if (ser.in_waiting>0):
    inData = ser.readline()
    if (inData == 'waiting'):
       ser.write('A')

#loading text files, remember to check start and end characters for documents
twitter = fileload(data["twitterRuling"])
con = fileload(data["con"])
mReport = fileload(data["mreport"])

#function to advance lists, not working
def advance(aPos, length):
    print aPos, length
    if (aPos) <  length:
        aPos = aPos + 1
    else:
        aPos = 0

p = 0
tP = 0
cP = 0
mP = 0

#START THE LOOPING DATA SENT
try:
    while True:
        if (ser.out_waiting>0):
            #how long to delay for asynchronous?
            time.sleep(2)
        elif (ser.in_waiting>0):
            data = ser.readline()
            if (data == 'waiting'):
                ser.write('A')
            else:
                #ser.write(headlines[p])
                print(headlines[p])
                print(con[cP])
                print(twitter[tP])
                print(mReport[mP])
                time.sleep(2)
                #ser.write(twitter[tP])
                #print (twitter[tPosition])

                if (tP < len(twitter)-1):
                     tP += 1
                else:
                     tP = 0

	        if (p < len(headlines)-1):
                    p += 1
                else:
                    p = 0

                if (cP < len(con)-1):
                    cP += 1
                else:
                    cP = 0

                if (mP < len(mReport)-1):
                    mP += 1
                else:
                    mP = 0

except KeyboardInterrupt:
    #cleanup
    print('keyboard close')
    exit_handler()

except Exception as e:
    print (e)
    exit_handler()
