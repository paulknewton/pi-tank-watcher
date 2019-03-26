import unittest
from unittest import TestCase


import dummy_sensor


class TestSensor(TestCase):
    def test_functionIsNotNone(self):
        self.assertIsNotNone(dummy_sensor.distance())

    def test_value(self):
        self.assertEqual(dummy_sensor.distance(), 34.2)
