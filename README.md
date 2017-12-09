# gettemp2
Similar to gettemp, let's use a 1602 display to show polled DS18B sensor data.

[gettemp](https://github.com/kenkl/gettemp) uses some ideas developed a couple years ago using some code developed to use the 1602 character LCD to display the data retrieved from remote sensors attached to network-connected Arduino-like devices. They expose their data via http/JSON, making it easy to parse and display. I'm finally getting 'round to posting that code here.

The 1602 is connected to the RPi with the [Sparkfun Serial LCD backpack](https://www.sparkfun.com/products/258), making the connection very simple (one wire).

To do this requires that we sacrifice serial-console connectivity to the RPi. That's okay - I very rarely feel the need to use it. Using raspi-config - Interfacing Options, Serial. Disable the login shell over serial, but leave hardware serial enabled.

Once serial-console is disabled, ~~/dev/ttyAMA0~~ /dev/serial0 (this changed with RPi0 and Stretch) is available to shove data to. To do that, I've got a class - SerLCD - which is based on [badams](https://github.com/badams)' [SerLCD class](https://github.com/badams/SerLCD). I've made some changes to it (backlight control, positioning, etc.). Maybe I'll fork his thing later. For now, be aware that SerLCD here is subtly different than badams' version.

SerLCD needs pyserial which, in turn, needs pip to install. So:

```
sudo apt-get install python-pip
sudo pip install pyserial
```

The physical layout of the serial-enabled LCD connection to RPi is quite simple:

![alt text](https://raw.githubusercontent.com/kenkl/gettemp2/master/rpi_serlcd_basic_bb_sm.png "SerialLCD hookup to RPi")

And the traditional action-shot (coming soon):

(action-shot.jpg)


