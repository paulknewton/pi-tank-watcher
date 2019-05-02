#! /usr/bin/python3

import statistics
import time
from urllib.request import urlopen
import argparse


# SENSOR_HEIGHT = 205  # height of the sensor above an empty tank


class Hcsr04Sensor:
    def __init__(self, gpio_trigger, gpio_echo):
        # GPIO Pins connected to sensor
        self.gpio_trigger = gpio_trigger
        self.gpio_echo = gpio_echo

        # GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)

        # set GPIO direction (IN / OUT)
        GPIO.setup(self.gpio_trigger, GPIO.OUT)
        GPIO.setup(self.gpio_echo, GPIO.IN)

    def distance(self):
        # return random.random() * 5 + 30

        time.sleep(3)

        # set Trigger to HIGH
        GPIO.output(self.gpio_trigger, True)

        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(self.gpio_trigger, False)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime (after start of echo pulse)
        while GPIO.input(self.gpio_echo) == 0:
            StartTime = time.time()

        # save time of arrival
        while GPIO.input(self.gpio_echo) == 1:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

        return distance


class ThingSpeak:

    def __init__(self, api_key):
        self.api_key = api_key

    def store(self, water_depth):
        urlopen(
            "https://api.thingspeak.com/update?api_key=" + self.api_key + "&field1=%d" % water_depth)


def log_water_depth(sensor, data_store, sensor_height):
    """Read sensor multiple times to get a stable reading (calculate mean) and log to the logger store. Readings are taken 20 times. Outliers > median +/- 1 std dev are discarded. Arithmetic mean of the remaining samples is calculated to 2 decimal places."""
    num_measures = 20
    samples = []
    for i in range(0, num_measures):
        samples.append(sensor.distance())
        print("Measured Distance = %.1f cm" % samples[i])

    # remove outliers
    stdev = statistics.stdev(samples)
    print("-- stdev = %f" % stdev)
    median = statistics.median(samples)
    print("-- median = %f" % median)
    clean_data = [x for x in samples if (x > median - 1 * stdev)]
    clean_data = [x for x in clean_data if (x < median + 1 * stdev)]
    print("-- len samples = %d; len clean_data = %d" % (len(samples), len(clean_data)))

    # calculate mean measurement
    print("Avg. measurement (incl. outliers) = %.2f cm" % statistics.mean(samples))
    clean_measure = statistics.mean(clean_data)
    print("Avg. measurement (excl. outliers) = %.2f cm" % clean_measure)
    water_depth = round(sensor_height - clean_measure, 2)  # log to 2 decimal places

    print("Logging water depth = %s cm" % water_depth)
    data_store.store(water_depth)


if __name__ == '__main__':
    # read command-line args
    parser = argparse.ArgumentParser(
        description="Monitor water depth in a rainwater tank using a HC-SR04 ultrasound sensor")
    parser.add_argument("thing_speak_api", help="API key to write new sensor readings to thingspeak.com channel")
    parser.add_argument("sensor_height", help="Height of the sensor above an empty tank", type=float)
    args = parser.parse_args()
    print(args)

    try:
        import RPi.GPIO as GPIO
        hcsr04_sensor = Hcsr04Sensor(23, 24)
        thing_speak = ThingSpeak(args.thing_speak_api)

        log_water_depth(hcsr04_sensor, thing_speak, args.sensor_height)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
