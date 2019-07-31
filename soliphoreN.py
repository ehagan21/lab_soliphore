#! /usr/bin/env python
import serial
import time
import json
import re
import atexit
import textwrap
from newsapi import NewsApiClient

#loading credentials
with open('/home/pi/lab/config.json') as json_data_file:
    data = json.load(json_data_file)

print('loaded json')

#serial port information
port = "/dev/ttyACM0"
port2 = "/dev/ttyACM1"
rate = 115200
ser = serial.Serial(port,rate, timeout = 1)
#ser2 = serial.Serial(port2, rate, timeout=1)

#time between sending serial information
timeBetween = 1

print('connected serial')
headlines = []

#Init
news_key = data["api_key"]
newsapi = NewsApiClient(api_key=news_key)

top_headlines = newsapi.get_top_headlines(language='en', country ='us')

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
        wrapper = textwrap.TextWrapper(width=50)
        shorten = wrapper.wrap(text=hlist)
        message = '[' + shorten[0].upper() + ']'
        headlines.append(message)
        print(message)

def exit_handler():
    print("closing application")
    ser.reset_output_buffer()
    ser.close()

sanitize()

#if (ser.in_waiting>0):
#    inData = ser.readline()
#    if (inData == 'waiting'):
#       ser.write('A')
#       print('connected')
    #reset the Arduino here?

#loading text files, remember to check start and end characters for documents
A1 = fileload(data["1A"])
A2 = fileload(data["2A"])
A3 = fileload(data["3A"])
A4 = fileload(data["4A"])
A5 = fileload(data["5A"])
B1 = fileload(data["1B"])
B2 = fileload(data["2B"])
B3 = fileload(data["3B"])
B4 = fileload(data["4B"])
B5 = fileload(data["5B"])

#counters, this should be in a function and private/local but not working
ap1 = 0
ap2 = 0
ap3 = 0
ap4 = 0
ap5 = 0

bp1 = 0
bp2 = 0
bp3 = 0
bp4 = 0
bp5 = 0

#START THE LOOPING DATA SENT
try:
    while True:
        if (ser.out_waiting>0):         #this should be if both ports are occupied, pause, otherwise if only one is keep going
             print('occupado')
             time.sleep(2)
        elif (ser.in_waiting>0):
            sdata = ser.readline()
            print(sdata)

            #s2data = ser2.readline()
            #if ("waiting in s2data):
            #    ser2.write('A')
            #    print('connected2')
            #    ser2.reset_input_buffer()
            #elif (("calibrating" in s2data) or ("calibrated" in s2data)):
            #    print("give arduino2 a second")

            if ("waiting" in sdata):
                ser.write('A')
                print('connected')
                ser.reset_input_buffer()
	    elif(("calibrating" in sdata) or ("calibrated" in sdata)):
                print('give arduino a second')
            elif ("NEXT" in sdata): #or ("NEXT" in s2data):
                print(sdata)
                ser.reset_input_buffer
                #ser2.reset_input_buffer

                #tower is written from the bottom to the top
                print(A5[ap5])
                print(A4[ap4])
                print(A3[ap3])
                print(A2[ap2])
                print(A1[ap1])

                print(B5[bp5])
                print(B4[bp4])  #email?
                print(B3[bp3])
                print(B2[bp2])
                print(B1[bp1])

                print ('sending serial')
                ser.write(A5[ap5])
                ser.write(A4[ap4])
                ser.write(A3[ap3])
                ser.write(A2[ap2])
                ser.write(A1[ap1])

                #ser2.write(B5[ap5])
                #ser2.write(B4[bp4])
		#ser2.write(B3[bp3])
		#ser2.write(B2[bp2])
		#ser2.write(B1[bp1])

                print ('signal sent')
                now = time.time()
		while (timeBetween > (time.time() - now)):
                    if(ser.in_waiting > 0):
                        check = ser.read()
                    #if (ser2.is_waiting > 0):
                    #    check2 = ser2.read()

                    #if ("waiting" in check2):
                        #ser2.write("A")
                    if("waiting" in check):
                        ser.write("A")

                print("awake again")

                #run a calibration and wait for it to finish
                if ((ap1 > 0) and (ap1 % 10 == 0)):
                    print("calibrating")
                    ser.write('&')

                if (ap1 < len(A1)-1):
                     ap1 += 1
                else:
                     ap1 = 0

	        if (ap2 < len(A2)-1):
                    ap2 += 1
                else:
                   ap2 = 0

                if (ap3 < len(A3)-1):
                    ap3 += 1
                else:
                    ap3 = 0

                if (ap4 < len(A4)-1):
                    ap4 += 1
                else:
                    ap4 = 0

                if (ap5 < len(A5)-1):
                    ap5 += 1
                else:
                    ap5 = 0

                if (bp1 < len(B1)-1):
                    bp1 += 1
                else:
                    bp1 = 0

                if (bp2 < len(B2)-1):
                    bp2 += 1
                else:
                    bp2 = 0

                if (bp3 < len(B3)-1):
                    bp3 += 1
                else:
                    bp3 = 0

                if (bp4 < len(B4) - 1):
                    bp4 += 1
                else:
                    bp4 = 0

                if (bp5 < len(B5)-1):
                    bp5 += 1
                else:
                    bp5 = 0

                print("A values are " + str(ap1) + ", " + str(ap2) + ", " + str(ap3) + ", " + str(ap4) + ", " + str(ap5))
                print("B values are " + str(bp1) + ", " + str(bp2) + ", " + str(bp3) + ", " + str(bp4) + ", " + str(bp5))

except KeyboardInterrupt:
    #cleanup
    print('keyboard close')
    exit_handler()

except Exception as e:
    print (e)
    exit_handler()
