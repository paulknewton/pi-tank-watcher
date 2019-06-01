import pytest
import tank_watcher
import loggers as ts
from unittest.mock import Mock


class DummySensor:
    """Dummy sensor to return sample readings. Values are hard-coded. Once values are all read, the sensor starts from the beginning."""

    def __init__(self):
        self.noisy = False  # use quiet readings by default

        self.noisy_readings = [38.1165, 37.3386, 38.8385, 39.9032, 37.8083, 37.3966, 39.888, 38.1475, 38.0824, 38.8795,
                               39.8011, 38.748, 38.253,
                               39.9832, 37.7506, 37.0587, 37.5136, 37.3538, 38.8457, 38.0296]
        self.quiet_readings = [37.8113, 37.1223, 37.3066, 37.9734, 37.045, 37.5932, 37.4391, 37.6167, 37.0225, 37.8271,
                               37.806, 37.3737, 37.777, 37.8919, 37.0741, 37.636, 37.2062, 37.4314, 37.7108, 37.6957]

        self.iter = None
        self.reset_iterator()

    def reset_iterator(self):
        if self.noisy:
            self.iter = iter(self.noisy_readings)
        else:
            self.iter = iter(self.quiet_readings)

    def distance(self):
        try:
            return next(self.iter)
        except StopIteration:  # if reached end of readings, jump to the start
            self.reset_iterator()
            return self.distance()

    def set_noisy(self, noise):
        self.noisy = noise
        self.reset_iterator()


class DummyStore:
    """Dummy logging storage. Logged items are appended to an array."""

    def __init__(self):
        self.readings = []

    def get_logged_readings(self):
        return self.readings.copy()

    def get_last_reading(self):
        try:
            last_reading = self.readings[len(self.readings) - 1]
        except IndexError:
            last_reading = 0
        return last_reading

    def log(self, event):
        self.readings.append(event)


@pytest.fixture
# @patch('dummy_sensor.DummySensor')
# def sensor(MockDummySensor):
def setup():
    # use an actual GPIO sensor (will only work on a Raspberry Pi with RPi.GPIO installed
    # my_sensor = Hcsr04Sensor

    # use a mock object based on a DummySensor
    # my_sensor = MockDummySensor()
    # my_sensor.distance.return_value = 42

    return DummySensor(), DummyStore()


def test_mock_objects(setup):
    """Test the dummy sensor/logger are working"""
    sensor, logger = setup

    reading = sensor.distance()
    assert reading == 37.8113

    assert logger.get_last_reading() == 0
    num_readings = len(logger.get_logged_readings())
    logger.log(reading)
    assert logger.get_last_reading() == reading
    assert len(logger.get_logged_readings()) - num_readings == 1


def test_quiet_sensor(setup):
    """Test the tank watcher function with quiet readings"""
    sensor, store = setup
    tank_watcher.log_water_depth(sensor, store, 205)

    assert store.get_last_reading() == [167.36]


def test_noisy_sensor(setup):
    """Test the tank watcher function with noisy readings"""
    sensor, store = setup
    sensor.set_noisy(True)
    tank_watcher.log_water_depth(sensor, store, 205)

    assert store.get_last_reading() == [166.93]


def test_thing_speak_simple():
    """Test the ThingSpeak channel class (event with single field)"""
    channel = ts.ThingSpeak("myapi", test_mode=True)
    assert channel.log(["hello"]) == "https://api.thingspeak.com/update?api_key=myapi&field1=hello"


def test_thing_speak_multiple():
    """Test the ThingSpeak channel class (event with multiple fields)"""
    channel = ts.ThingSpeak("myapi", test_mode=True)
    assert channel.log(
        ["hello", "goodbye"]) == "https://api.thingspeak.com/update?api_key=myapi&field1=hello&field2=goodbye"


def test_thing_speak_empty():
    """Test the ThingSpeak channel class (empty event)"""
    channel = ts.ThingSpeak("myapi", test_mode=True)
    assert channel.log([]) == "https://api.thingspeak.com/update?api_key=myapi"


def test_multiple_loggers(setup):
    sensor, logger = setup
    l1 = Mock(logger)
    l2 = Mock(logger)

    tank_watcher.log_water_depth(sensor, [l1, l2], 205)

    l1.log.assert_called_once_with([167.36])
    l2.log.assert_called_once_with([167.36])
