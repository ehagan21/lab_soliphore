#! /usr/bin/env python
import serial
import time
import json
import re
from newsapi import NewsApiClient

#loading credentials
with open('/home/pi/lab/config.json') as json_data_file:
    data = json.load(json_data_file)

#serial port information
port = "/dev/ttyACM0"
rate = 115200
ser = serial.Serial(port,rate)
headlines = []

if ser.isOpen():
    print('success')
    ser.write('A')

#Init
news_key = data["api_key"]
newsapi = NewsApiClient(api_key=news_key)

top_headlines = newsapi.get_top_headlines(language='en', country ='us')
#all_articles = newsapi.get_everything(q='flag', language = 'en', sort_by='relevancy')

def sanitize():
    for item in top_headlines["articles"]:
        xstring = item["title"].encode('utf-8')
        hlist = re.sub("[^a-zA-Z ]+", "", xstring)
        message = '<' + hlist + '>'
        headlines.append(message)
        print(message)


#keeps track of which headline we should be playing
position = 0

sanitize()

#START THE LOOPING DATA SENT
while True:
    if (ser.in_waiting>0):
        data = ser.read()
        data_left = ser.inWaiting()
        print(data_left)
        print(headlines[position])
        ser.write(headlines[position])
        time.sleep(5)

        #loop through the headlines to play all necessary
        if (position < len(headlines)):
            position += 1
        else:
            print('done')
            break
