import RPi.GPIO
from pump_watcher import SumpPump


class RpiGpioPump(SumpPump):
    """Pump monitor using the RPi.GPIO library"""

    def __init__(self, on_pin):
        super(RpiGpioPump, self).__init__(on_pin)

        # GPIO Mode (BOARD / BCM)
        RPi.GPIO.setmode(RPi.GPIO.BOARD)

        # pull-down resistor to avoid false triggers
        # RPi.GPIO.setup(on_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        RPi.GPIO.setup(on_pin, RPi.GPIO.IN)
        RPi.GPIO.add_event_detect(on_pin, RPi.GPIO.BOTH, callback=self.event, bouncetime=500)

    def get_status(self, pin):
        return RPi.GPIO.input(pin)

    def cleanup(self):
        RPi.GPIO.cleanup()
