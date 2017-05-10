# Temperature and humidity measuring published on influxdb
A micropython project for wemos d1 mini with wemos SHT30 sensor publishing values to an influxdb instance


The implementation of the sensor is taken from here [SHT30](https://github.com/rsc1975/micropython-sht30) 

In order to use this an influxdb server must be set up and a database created. 
The one used for this project, [influxdb](https://hub.docker.com/_/influxdb/) has been setup to run on docker.
 
This project does not use authentication since it is build for a local deployment. If this does not 
work for you, edit accordingly. 

This assumes that you are using a linux box and was done on one running 
ubuntu.

# Physical Connection

The sensor is just stacked on top of the wemos d1. Keep in mind that it picks
 up temperature from the board so the reading is not true if used without 
 some form of insulation. Even with insulation the sensor picks up a lot of 
 heat from the board so the code puts the board in deepsleep instead of a 
 while loop. The board waking from deep sleep reconnects to the wifi, to the 
 mqtt sends the message, disconnects and sleeps again. For the board to wake 
 up from deep sleep a connection has to be made between gpio16 (D0) and RST.
 
# Configuration
 
 Rename configuration_sample.json to configuration.json and edit accordingly.
  Everything else should just work out of the box.

To load this project the wemos d1 needs to be running micropython and you 
could probably use ampy.

# Flashing micropython

Required tools:
    
   [esptool](https://github.com/espressif/esptool)    
   [micropython](http://micropython.org/download) # Firmware for ESP8266 
   boards, get latest.  
  
  
  With the board connected to a usb port of your linux box assuming that the 
  port is ttyUSB0 (check with dmesg after connecting to see what is assigned)
    
    esptool.py --port /dev/ttyUSB0 erase_flash
    esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266-20170108-v1.8.7.bin
   
   
# Loading the project

Required tools:

   [ampy](https://github.com/adafruit/ampy)
   
    export AMPY_PORT=/dev/ttyUSB0
    ampy put drivers/
    ampy put configuration.json 
    ampy put main.py 
    ampy put boot.py 

# Cheching output

    You should see measurements in your influxdb instance setup on 
    configuration.