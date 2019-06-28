import wiringpi
import pump_watcher


class WiringPiPump(pump_watcher.AbstractPump):
    """Pump monitor using the Wiring Pi GPIO library"""

    def __init__(self, pin):
        super(WiringPiPump, self).__init__(pin)

        # wiringpi.wiringPiSetupGpio()
        wiringpi.wiringPiSetupPhys()

        wiringpi.pinMode(pin, wiringpi.GPIO.INPUT)
        wiringpi.pullUpDnControl(pin, wiringpi.GPIO.PUD_OFF)    # use external pull-down resistor
        wiringpi.wiringPiISR(pin, wiringpi.GPIO.INT_EDGE_BOTH, self.event)

        # set debounce_timeout_ms=500 ???

    def get_status(self, pin):
        return wiringpi.digitalRead(pin)
