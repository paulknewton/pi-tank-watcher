from urllib.request import urlopen

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

        Args:
            event - a list of fields to log. Can be empty.
        """

        url = "https://api.thingspeak.com/update?api_key=" + self.api_key
        for i in range(0, len(event)):
            url += "&field%d=%s" % (i + 1, event[i])
        if not self.test_mode:
            urlopen(url)

        return url
