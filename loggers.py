from urllib.request import urlopen

class HealthChecks:
    """Ping a HealthChecks.io URL for each event"""

    def __init__(self, url, test_mode=False):
        """
        Setup a logger with the specified URL

        :param url: the URL to log to on each event
        """
        self.url = url
        self.test_mode = test_mode

    def log(self, event):
        """
        Log the event to the specified URL via GET method

        :param event: the event
        """
        print("Logging to %s:" % self.url)
        print("Event: %s" % event)

        if not self.test_mode:
            urlopen(self.url)

class ThingSpeak:
    """ThingSpeak channel used to log pump on/off events"""

    def __init__(self, api_key, test_mode=False):
        """
        Setup a ThingSpeak channel with the specified API key

        Args:
            api_key - write API key to update the channel
            test_mode - enable/disable logging to the remote service
        """
        self.api_key = api_key
        self.test_mode = test_mode

    def log(self, event):
        """
        Log the event to the ThingSpeak channel (timestamp is inferred by ThingSpeak)

        :arg
            event - a list of fields to log. Can be empty.
        :return url used to log to ThingSpeak (includes API key and list of fields)
        """

        url = "https://api.thingspeak.com/update?api_key=" + self.api_key
        for i, field in enumerate(event):
            url += "&field%d=%s" % (i + 1, field)
        if not self.test_mode:
            urlopen(url)

        return url


class ConsoleLogger:
    def log(self, event):
        print("Event: %s" % event)


class AlarmClock:
    """Logger that allows alarms to be attached for specific events"""

    def __init__(self):
        """
        Initialise an AlarmClock
        """
        self.events = []
        self.alarms = []

    def add_alarm(self, trigger, alarm):
        """
        Add an an alarm and trigger to the alarm clock.

        :param trigger: a function that takes a list of events, and returns True or False
        :param alarm: a function invoked if the trigger is met
        """
        self.alarms.append((trigger, alarm))

    def log(self, event):
        self.events.append(event)

        for trigger, alarm in self.alarms:
            if trigger(self.events):
                alarm()
