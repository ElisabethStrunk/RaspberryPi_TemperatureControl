#!/usr/bin/env python3

import time
from w1thermsensor import W1ThermSensor
sensor = W1ThermSensor()


def get_temperature():
    return sensor.get_temperature()


if __name__ == '__main__':
    while True:
        temperature = get_temperature()
        print("The temperature is %s celsius" % temperature)
        time.sleep(1)