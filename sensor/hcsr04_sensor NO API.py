#! /usr/bin/python3

import RPi.GPIO as GPIO
import time, random, statistics
from urllib.request import urlopen
 
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)
 
# GPIO Pins connected to sensor
GPIO_TRIGGER = 23
GPIO_ECHO = 24
 
#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

# sensor dimensions (to convert reading to water depth)
SENSOR_HEIGHT = 205  # height of the sensor above an empty tank

class Hcsr04Sensor:
    def distance(self):
        #return random.random() * 5 + 30
    
        time.sleep(3)
        
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)
 
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)

        StartTime = time.time()
        StopTime = time.time()

        # save StartTime (after start of echo pulse)
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()

        # save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()

        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2

        return distance


if __name__ == '__main__':
    try:
        sensor = Hcsr04Sensor()
        
        # read sensor multiple times to get a stable reading (calculate mean)
        num_measures = 20
        samples = []
        for i in range(0, num_measures):
            samples.append(sensor.distance())
            print ("Measured Distance = %.1f cm" % samples[i])
       
        # remove outliers
        stdev = statistics.stdev(samples)
        print("-- stdev = %f" % stdev)
        median = statistics.median(samples)
        print("median = %f" % median)

        clean_data = [x for x in samples if (x > median - 1 * stdev)]
        clean_data = [x for x in clean_data if (x < median + 1 * stdev)]
        print("-- len samples = %d; len clean_data = %d" % (len(samples), len(clean_data)))
        
        # calculate mean measurement
        print("Avg. measurement (incl. outliers) = %.1f cm" % statistics.mean(samples))
        clean_measure = statistics.mean(clean_data)
        print("Avg. measurement (excl. outliers) = %.1f cm" % clean_measure)

        water_depth = SENSOR_HEIGHT - clean_measure
        print("Water depth = %.1f cm" % water_depth)

        urlopen("https://api.thingspeak.com/update?api_key=PUT_YOUR_THINGSPEAK_CHANNEL_WRITE_API_HERE&field1=%d" % water_depth)

    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
