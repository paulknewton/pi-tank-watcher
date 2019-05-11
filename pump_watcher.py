#! /usr/bin/python3

import argparse
import datetime
import random

import loggers

PUMP_ON = 1
PUMP_OFF = 0


class SumpPump:
    """Monitor of a sump pump. Logs when pump is activated/de-activated"""

    def __init__(self, on_pin, test_mode=False):
        """Setup a pump watcher on the specific GPIO pin"""
        self.switch_pin = on_pin
        self.test_mode = test_mode

        if not test_mode:
            # GPIO Mode (BOARD / BCM)
            GPIO.setmode(GPIO.BOARD)
            # GPIO.setup(on_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(on_pin, GPIO.IN)

        # list of loggers (to allow >1)
        self.loggers = []

    def event(self, pin):
        """Switch on. Log event to the channel (1=pump on; 0 = pump_off; -1=undefined"""
        status = -1
        if not self.test_mode:
            status = GPIO.input(pin)
        print("Change status on pin %d --> %s" % (pin, status))

        for l in self.loggers:
            if l:  # ignore empty loggers
                l.log([status])

    def add_listener(self, logger):
        """Add a listener to be called when the pump is enabled/disabled. Can add multiple listeners to be called in sequence."""
        print("Registering listener")
        self.loggers.append(logger)

        if not self.test_mode:
            GPIO.add_event_detect(self.switch_pin, GPIO.BOTH, self.event)


def gen_random_samples(length):
    """
    Generate random sample data for the pump. Simulate occasional lost readings.

    :param length: number of entries to generate
    :return list of lists of the form [[timestamp, sample_id, 0/1]...]
    """
    data = []

    ts = datetime.datetime.utcnow()
    sample_id = 1
    while sample_id <= length:

        # get a PUMP_ON event
        event = gen_mainly_on()
        if (event == PUMP_ON):
            # timestamp is assumed to be at least 45 mins since last PUMP_OFF + random(100 minutes)
            ts += datetime.timedelta(0, 45 * 60) + datetime.timedelta(0, random.randint(0, 100 * 60))
            data.append([ts.strftime("%Y-%m-%d %H:%M:%S UTC"), sample_id, event])
            sample_id += 1
        else:
            #print("missed pump PUMP_ON")
            pass

        event = gen_mainly_off()
        if (event == PUMP_OFF):
            # pump is assumed to be on for random(10 minutes)
            ts = ts + datetime.timedelta(0, random.randint(0, 10 * 60))
            data.append((ts.strftime("%Y-%m-%d %H:%M:%S UTC"), sample_id, event))
            sample_id += 1
        else:
            #print("missed pump PUMP_OFF")
            pass

    # events are potentially appended in pairs, meaning we may exceed the requested length
    return data[:length]


def gen_random_event(threshold):
    """Generate a random event (PUMP_ON or PUMP_OFF). The event is chosen randomly, but the threshold defines the probability. 1 means always off, 0 means always on.
    :param threshold: the value used to determine the generated event type. Values < threshold = PUMP_OFF; Values >= threshold = PUMP_ON
    :return:
    """
    r = random.random()
    if r >= threshold:
        return PUMP_ON
    else:
        return PUMP_OFF


def gen_mainly_on():
    """Generate an event - most likely a PUMP_ON event."""
    return gen_random_event(0.2)


def gen_mainly_off():
    """Generate an event - most likely a PUMP_OFF event."""
    return gen_random_event(0.8)


if __name__ == '__main__':
    # read command-line args
    parser = argparse.ArgumentParser(
        description="Monitor the on/off switching of a sump pump")
    parser.add_argument("gpio_pin", help="GPIO pin connected to the pump", type=int)
    parser.add_argument("--thingspeak", dest="thing_speak_api",
                        help="API key to write new sensor readings to thingspeak.com channel")
    args = parser.parse_args()
    print(args)

    import RPi.GPIO as GPIO

    pump = SumpPump(args.gpio_pin)
    pump_channel = None

    # add a logger to ThingSpeak if defined, otherwise print to console
    if args.thing_speak_api:
        # print("adding ThingSpeak channel (API key %s" % args.thing_speak_api)
        pump_channel = loggers.ThingSpeak(args.thing_speak_api)
    else:
        # print("adding console channel")
        pump_channel = ConsoleLogger()

    pump.add_listener(pump_channel)

    # prevents script from exiting
    input("Hit any key to exit")
    GPIO.cleanup()
