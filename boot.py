# -*- coding: utf-8 -*-
# Micropython wemos d1 mini with SHT30 temperature sensor on influxdb
# Copyright (C) 2017  Costas Tyfoxylos
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()
import network
import time
import ujson
import gc
from drivers import SHT30

gc.collect()

# load configuration
configuration = ujson.loads(open('configuration.json').read())
ssid = configuration.get('network_ssid')
password = configuration.get('network_password')

# network initializing
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(ssid, password)
print('Waiting for network...',)
while not wifi.isconnected():
    time.sleep(1)
    print('.',)
print('Network connected')

# sensor intializing
sensor = SHT30()
while not sensor.is_present():
    time.sleep(1)
print('Sensor active')
