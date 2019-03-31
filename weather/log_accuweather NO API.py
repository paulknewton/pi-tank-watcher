#! /usr/bin/python3
# Read current home weather conditions from accuweather (via the accuweather API)
# and log them to my ThingSpeak.com channel
#

import json
import requests

# accuweather
accuApiKey = "PUT_YOUR_ACCUWEATHER_API_KEY_HERE"
locationKey = "1037757"  # niederdonven
weatherUrl = "http://dataservice.accuweather.com/currentconditions/v1/" + locationKey + "?apikey=" + accuApiKey + "&details=true"

# thingspeak
thingSpeakApi = "PUT_YOUR_THINGSPEAK_CHANNEL_WRITE_API_HERE"

if __name__ == '__main__':
    # weather_data = json.load(open("sample-accuweather.json", "r"))[0]
    weather_data = requests.get(weatherUrl).json()[0]

    temperature = weather_data['Temperature']['Metric']['Value']
    humidity = weather_data['RelativeHumidity']
    pressure = weather_data['Pressure']['Metric']['Value']
    rain = weather_data['Precip1hr']['Metric']['Value']

    print("Temperature=%d Humidity=%d Pressure=%d Rain=%d" % (temperature, humidity, pressure, rain))

    # log some data to thingspeak channel
    requests.get(
        "https://api.thingspeak.com/update?api_key=%s&field1=%d&field2=%d&field3=%d&field4=%d" % (
        thingSpeakApi, temperature, humidity, pressure, rain))
