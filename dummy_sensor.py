class DummySensor:

    def distance(self):
        return 34.2


if __name__ == '__main__':
    sensor = DummySensor()
    print(sensor.distance())
