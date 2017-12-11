#!/usr/bin/env python

import urllib
import json
import SerLCD
from time import sleep, strftime
from datetime import datetime

url = "http://ardu1.kenkl.org/"
url2 = "http://esp1.kenkl.org/temp"
bll = 'FULL'
slcd = SerLCD.SerLCD()

def gettimestr():
    timenow = datetime.now().strftime('%H:%M')
    return timenow

if __name__ == '__main__':
    slcd.Backlight(bll)
    #slcd.Clear() // do we need to clear the screen every time any more?
    slcd.lcdPosition(0,15)
    slcd.Text('.')
        
    webresponse = urllib.urlopen(url)
    webdata = webresponse.read()
    webresponse2 = urllib.urlopen(url2)
    webdata2 = webresponse2.read()

    # Just in case... JSON needs double-quotes. Ardu1 does okay, but this should be standard-practice
    webdata = webdata.replace("'", '"')
    response = json.loads(webdata)
    webdata2 = webdata2.replace("'", '"')
    response2 = json.loads(webdata2)

    #parse the data
    ddc = response['datacentre']
    dout = response['outside']
    esptemp = response2['temp']

    #build the output
    zero = gettimestr()
    one = 'E:' + str(esptemp) +' '
    two = 'D:' + str(ddc) + '  O:' + str(dout) + ' '

    slcd.lcdPosition(0,10)
    slcd.Text(zero)
    slcd.lcdPosition(0,0)
    slcd.Text(one)
    slcd.lcdPosition(1,0)
    slcd.Text(two)
    slcd.lcdPosition(0,15)
    slcd.Text(' ')

