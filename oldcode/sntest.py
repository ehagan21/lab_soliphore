#! /usr/bin/env python
import serial
from newsapi import NewsApiClient

port = "/dev/ttyACM0"
rate = 115200

ser = serial.Serial(port,rate)
if ser.isOpen():
    print('success')

string1 = b'finally'

#while 1:
#    if(ser.in_waiting>0):
#        line = ser.readline()
#        print(line)
#        ser.write(b'test')
#Init
newsapi = NewsApiClient(api_key='7820df480a45465c9a641bd4722df738')

top_headlines = newsapi.get_top_headlines(language='en', country ='us')
#all_articles = newsapi.get_everything(q='flag', language = 'en', sort_by='relevancy')

#for item in all_articles["articles"]:
#   ser.write(item["title"].encode('utf-8')

for item in top_headlines["articles"]:
    xstring = item["title"].encode('utf-8')

while True:
    if (ser.in_waiting>0):
        line = ser.readline()
        print(line)

    for item in top_headlines["articles"]:
        xstring = item["title"].encode('utf-8')
        #print(xstring)
        ser.write(xstring)
