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
ser = serial.Serial(port,rate, timeout = 0)
headlines = []

#Init
news_key = data["api_key"]
newsapi = NewsApiClient(api_key=news_key)

top_headlines = newsapi.get_top_headlines(language='en', country ='us')
#all_articles = newsapi.get_everything(q='flag', language = 'en', sort_by='relevancy')

def sanitize():
    for item in top_headlines["articles"]:
        xstring = item["title"].encode('utf-8')
        hlist = re.sub("[^a-zA-Z ]+", "", xstring)
        message = '<' + hlist.upper() + '>'
        headlines.append(message)
        #print(message)

#keeps track of which headline we should be playing
position = 0

sanitize()

if (ser.in_waiting>0):
    ser.write('A')

def exit_handler():
    print("closing application")
    ser.flushOutput()
    ser.close()

#START THE LOOPING DATA SENT
try:
    while True:
        if (ser.out_waiting>0):
            time.sleep(2)
        elif (ser.in_waiting>0):
            data = ser.read()
            print(headlines[position])
            ser.write(headlines[position])

        #loop through the headlines to play all necessary
            #if (position < len(headlines)-1):
            if (position < 2):
                position += 1
            else:
                position = 0
                print('done')
                #break

except KeyboardInterrupt:
    #cleanup
    exit_handler()

except:
    exit_handler()
