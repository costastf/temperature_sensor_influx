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

import urequests
import machine
import esp
import time

headers = {'Accept': 'text/plain',
           'Connection': 'close',
           'Content-type': 'application/octet-stream'}

location = configuration.get('location')
position = configuration.get('position')
submit_interval = configuration.get('submit_interval')


def main():
    submit_interval = configuration.get('submit_interval')
    exception_timeout = configuration.get('exception_reset_timeout')
    influx_endpoint = configuration.get('influx_endpoint')
    try:
        temperature, humidity = sensor.measure()
        fields = (u'sensors,',
                  u'location={location}'.format(location=location),
                  u',position={position}'.format(position=position),
                  u' ',
                  u'temperature={temp}'.format(temp=temperature),
                  u',humidity={humidity}'.format(humidity=humidity))
        # building influxdb point protocol measurement.
        # See https://docs.influxdata.com/influxdb/v1.2/write_protocols/line_protocol_tutorial/
        point = ''.join(fields)
        response = urequests.post(influx_endpoint,
                                  data=point,
                                  headers=headers)
        response.close()
        print('Submitted :{}'.format(point))
        print('Sleeping deeply for {} seconds'.format(submit_interval))
        # deep sleep argument in microseconds
        esp.deepsleep(submit_interval * 1000000)
    except Exception as e:
        print(('Caught exception, {}'
               'resetting in {} seconds...').format(e, exception_timeout))
        time.sleep(exception_timeout)
        machine.reset()

if __name__ == '__main__':
    main()
