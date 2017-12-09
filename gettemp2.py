#!/usr/bin/env python
# ttthing - grabbing JSON from ardu1 to display temps on 16x2 display remotely. 
# ttthing3 - let's grab from multple sensors

import urllib
import json
import time
import signal
import sys
import SerLCD
from time import sleep, strftime
from datetime import datetime
from subprocess import *

# let's use the internal feeds. externals commented out as reminders
#url = "http://poeslaw.dyndns.org/ardu1"
#url2 = "http://poeslaw.dyndns.org/esp1"
url = "http://ardu1.kenkl.org/"
url2 = "http://esp1.kenkl.org/temp"
bll = 'FULL'
slcd = SerLCD.SerLCD()

def exit_gracefully(signum, frame):
    # let's restore the original signal handlers
    signal.signal(signal.SIGTERM, original_sigterm)
    signal.signal(signal.SIGINT, original_sigint)
    signal.signal(signal.SIGHUP, original_sighup)

    # clean up gracefully here. bail when done.
    slcd.Clear()
    slcd.Text('Shutting down...')
    sleep(4)
    slcd.Clear()
    slcd.Backlight('OFF')
    sys.exit(0)

    #just in case we do something during cleanup that means we *shouldn't" exit, we want our handler to stay intact.
    signal.signal(signal.SIGTERM, exit_gracefully)
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGHUP, exit_gracefully)

# Run a command outside Python
def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output

# My BETTER way of getting IP address for a connected interface on RPi
def getipaddr():
    #we'll look for eth0 first, then wlan0. add others here if you care
    eth = run_cmd("ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1")
    wlan = run_cmd("ip addr show wlan0 | grep inet | awk '{print $2}' | cut -d/ -f1")
    if len(eth) <> 0:
        eth = eth[:-1] #awk's print leaves a stray linefeed. strip.
        return eth
    if len(wlan) <> 0:
        wlan = wlan[:-1] #awk's print leaves a stray linefeed. strip.
        return wlan

    fakeaddy = "No net. Sorry."
    return fakeaddy

if __name__ == '__main__':
    #store original SIGs to trap, then redirect them. 
    original_sigterm = signal.getsignal(signal.SIGTERM)
    original_sigint = signal.getsignal(signal.SIGINT)
    original_sighup = signal.getsignal(signal.SIGHUP)
    signal.signal(signal.SIGTERM, exit_gracefully)
    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGHUP, exit_gracefully)

    for i in range(1, 3):
        slcd.Backlight(bll)
        sleep(0.5)
    slcd.Clear()
    slcd.Text('gettemp2')
    slcd.lcdPosition(1,0)
    slcd.Text('09-Dec-2017')
    sleep(4)

    slcd.Clear()

    while True:
        slcd.lcdPosition(0,15)
        slcd.Text('.')
        #sleep(1)        
        # Lets get the reading from ardu1. The sensors are weird and require a warmup; the first read after
        # idle time can be a little random. So, double-tap them..
        # ... or maybe not. the DHT11 is a little clunky, the DS18B20 is only off on the first pull. deal with it.
        #webresponse = urllib.urlopen(url)
        #webdata = webresponse.read()
        #sleep(3)
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
        one = 'D:' + str(ddc) +'C LL:' + str(llvl) + ' '
        #two = 'Outside: ' + str(dout) +'C '
        two = 'E:' + str(esptemp) + 'C O:' + str(dout) + 'C '

        slcd.lcdPosition(0,0)
        slcd.Text(one)
        slcd.lcdPosition(1,0)
        slcd.Text(two)
        slcd.lcdPosition(0,15)
        slcd.Text(' ')
        sleep(37)


