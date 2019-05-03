#! /usr/bin/python3
# Read current home weather conditions from accuweather (via the accuweather API)
# and log them to my ThingSpeak.com channel
#

import argparse
import requests

if __name__ == '__main__':
    # read command-line args
    parser = argparse.ArgumentParser(
        description="Read current home weather conditions from accuweather (via the accuweather API) and log them to my ThingSpeak.com channel")
    parser.add_argument("thing_speak_api", help="API key to write new sensor readings to thingspeak.com channel")
    parser.add_argument("accuweather_api", help="API key to read weather data from accuweather")
    parser.add_argument("location_key", help="Accuweather location to retrieve weather data")
    args = parser.parse_args()
    print(args)

    # locationKey = "1037757"  # niederdonven
    weatherUrl = "http://dataservice.accuweather.com/currentconditions/v1/" + args.location_key + "?apikey=" + args.accuweather_api + "&details=true"
    weather_data = requests.get(weatherUrl).json()[0]

    temperature = weather_data['Temperature']['Metric']['Value']
    humidity = weather_data['RelativeHumidity']
    pressure = weather_data['Pressure']['Metric']['Value']
    rain = weather_data['Precip1hr']['Metric']['Value']

    print("Temperature=%d Humidity=%d Pressure=%d Rain=%d" % (temperature, humidity, pressure, rain))

    # log some data to thingspeak channel
    requests.get(
        "https://api.thingspeak.com/update?api_key=%s&field1=%d&field2=%d&field3=%d&field4=%d" % (
            args.thing_speak_api, temperature, humidity, pressure, rain))
