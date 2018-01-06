#!/usr/bin/env python

import urllib
import json
#import SerLCD
from time import sleep, strftime
from datetime import datetime

from oled.device import ssd1306, sh1106
from oled.render import canvas
from PIL import ImageDraw, ImageFont

url = "http://ardu1.kenkl.org/"
url2 = "http://esp1.kenkl.org/temp"
bll = 'FULL'
#slcd = SerLCD.SerLCD()
oled = ssd1306(port=1, address=0x3C)
font = ImageFont.truetype('C&C Red Alert [INET].ttf', 12)

def gettimestr():
    timenow = datetime.now().strftime('%H:%M')
    return timenow

if __name__ == '__main__':
    #slcd.Backlight(bll)
    #slcd.Clear() // do we need to clear the screen every time any more?
    #slcd.lcdPosition(0,15)
    #slcd.Text('.')
        
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
    one = 'E:  ' + str(esptemp) +' '
    two = 'D:  ' + str(ddc) 
    three = 'O:  ' + str(dout) + ' '
    four = 'LL: ' + str(llvl) + ' '

    '''
    slcd.lcdPosition(0,10)
    slcd.Text(zero)
    slcd.lcdPosition(0,0)
    slcd.Text(one)
    slcd.lcdPosition(1,0)
    slcd.Text(two)
    slcd.lcdPosition(0,15)
    slcd.Text(' ')
    '''

    with canvas(oled) as draw:
        draw.text((0, 0), zero, font=font, fill=255)
        draw.text((0, 14), one, font=font, fill=255)
        draw.text((0, 26), two, font=font, fill=255)
        draw.text((0, 38), three, font=font, fill=255)
        draw.text((0, 50), four, font=font, fill=255)
        #draw.text((0, 50), network('eth0'), font=font2, fill=255)
        #draw.text((0, 50), getipaddr(), font=font2, fill=255)
 


