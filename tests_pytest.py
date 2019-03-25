import pytest

# from dummy_sensor import DummySensor
from hcsr04_sensor import Hcsr04Sensor
from unittest.mock import patch, Mock


@pytest.fixture
# @patch('dummy_sensor.DummySensor')
# def sensor(MockDummySensor):
def sensor():
    # use an actual GPIO sensor (will only work on a Raspberry Pi with RPi.GPIO installed
    my_sensor = Hcsr04Sensor

    # use a DummySensor
    #     my_sensor = DummySensor()

    # use a mock object based on a DummySensor
    # my_sensor = MockDummySensor()
    # my_sensor.distance.return_value = 42

    return my_sensor


def test_functionIsNotNone(sensor):
    assert sensor.distance() is not None


def test_value(sensor):
    assert sensor.distance() >= 0


def test_value(sensor):
    assert sensor.distance() == 42
