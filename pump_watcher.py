#! /usr/bin/python3

import argparse
import thing_speak as ts


class SumpPump:
    """Monitor of a sump pump. Logs when pump is activated/de-activated"""

    def __init__(self, on_pin):
        """Setup a pump on the specific GPIO pin"""
        self.switch_pin = on_pin

        # GPIO Mode (BOARD / BCM)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(on_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    @staticmethod
    def on(channel):
        """Switch on. Log event to the channel"""
        print("switch on")
        channel.log([1])

    @staticmethod
    def off(channel):
        """Switch off. Log event to the channel"""
        print("switch off")
        channel.log([0])

    def listen(self, channel):
        """Start listening to the pump"""
        print("starting listener")
        try:
            GPIO.wait_for_edge(self.switch_pin, GPIO.FALLING)
            self.on(channel)

            GPIO.wait_for_edge(self.switch_pin, GPIO.RISING)
            self.off(channel)

        except KeyboardInterrupt:
            GPIO.cleanup()


if __name__ == '__main__':
    # read command-line args
    parser = argparse.ArgumentParser(
        description="Monitor the on/off switching of a sump pump")
    parser.add_argument("thing_speak_api", help="API key to write new sensor readings to thingspeak.com channel")
    parser.add_argument("gpio_pin", help="GPIO pin connected to the pump", type=int)
    args = parser.parse_args()
    print(args)

    import RPi.GPIO as GPIO

    pump = SumpPump(args.gpio_pin)
    pump_channel = ts.ThingSpeak(args.thing_speak_api)

    pump.listen(pump_channel)
