#! /usr/bin/env python
import serial
import time
import json
from newsapi import NewsApiClient

#loading credentials
with open('config.json') as json_data_file:
    data = json.load(json_data_file)

#serial port information
port = "/dev/ttyACM0"
rate = 115200
ser = serial.Serial(port,rate)
if ser.isOpen():
    print('success')

#test string
string1 = b'finally'

#Init
news_key = data["api_key"]
newsapi = NewsApiClient(api_key=news_key)

top_headlines = newsapi.get_top_headlines(language='en', country ='us')
#all_articles = newsapi.get_everything(q='flag', language = 'en', sort_by='relevancy')

#for item in all_articles["articles"]:
#   ser.write(item["title"].encode('utf-8')

for item in top_headlines["articles"]:
    xstring = item["title"].encode('utf-8')
    hlist = (xstring.split('/n/r'))

print(xstring)

ser.write(xstring)

while True:
    if (ser.in_waiting>0):
        a = ser.readline()
        print(a)
        for i in range(len(hlist)):
            print(hlist[i])
            ser.write(hlist[i])
            time.sleep(1)

