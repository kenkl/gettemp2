#!/usr/bin/env python

import urllib
import json
from time import sleep, strftime
from datetime import datetime

from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageDraw, ImageFont

url = "http://ardu1.kenkl.org/"
url2 = "http://esp1.kenkl.org/temp"
oled = ssd1306(port=1, address=0x3C)
font = ImageFont.truetype('/home/pi/gettemp2/C&C Red Alert [INET].ttf', 12)

def gettimestr():
    timenow = datetime.now().strftime('%H:%M')
    return timenow

if __name__ == '__main__':
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
    llvl = response['lightlevel']
    esptemp = response2['temp']

    #build the output
    zero = 'Last update: ' + gettimestr()
    one = 'ESP1:  ' + str(esptemp) +' '
    two = 'Datacentre:  ' + str(ddc) 
    three = 'Outside:  ' + str(dout) + ' '
    four = 'Light Level:  ' + str(llvl) + ' '

    with canvas(oled) as draw:
        draw.text((0, 0), zero, font=font, fill=255)
        draw.text((0, 14), one, font=font, fill=255)
        draw.text((0, 26), two, font=font, fill=255)
        draw.text((0, 38), three, font=font, fill=255)
        draw.text((0, 50), four, font=font, fill=255)
 


