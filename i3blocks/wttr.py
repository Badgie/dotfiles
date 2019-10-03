import json
from urllib import request
from urllib.error import URLError

wet_descriptors = {"rain", "showers", "show", "sleet"}


def get_weather_data(url: str) -> str:
    try:
        response = request.urlopen(url, timeout=5).read().decode("UTF-8")
    except URLError:
        return "Error getting weather"

    if response is None:
        return "Weather response was null"

    return str(response)


def get_precipitation(desc: str, data: dict) -> str:
    # If any 'wet' descriptor is a substring of the weather description, show precipitation
    if any(x in desc.lower() for x in wet_descriptors):
        return data["current_condition"][0]["precipMM"] + "mm "
    else:
        return ""


def format_line(data: str) -> str:
    weather = json.loads(data)
    weather_description = str(weather["current_condition"][0]["weatherDesc"][0]["value"])
    precipitation = get_precipitation(weather_description, weather)
    temperature = weather["current_condition"][0]["temp_C"]
    humidity = weather["current_condition"][0]["humidity"]
    wind_direction = weather["current_condition"][0]["winddir16Point"]
    wind = "{0:.2f}".format(int(weather["current_condition"][0]["windspeedKmph"]) / 3.6)

    return f"{weather_description}, {precipitation}{temperature}C {humidity}%RH {wind_direction}{wind}m/s"


if __name__ == '__main__':
    print(format_line(get_weather_data("https://www.wttr.in?format=j1")))

