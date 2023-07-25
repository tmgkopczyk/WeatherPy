# importing modules for use
from dataclasses import dataclass

@dataclass
class WeatherStation:
    code: str
    name: str
    province: str
    longitude: float
    latitude: float

# get_weather_by_site_name returns the data of a weather station from the name that the user provides
def get_weather_by_site_name(site_name: str, province: str):
    # get the URL of the station using the site name and province provided
    url = get_site_url(site_name, province)
    # return the XML data of the weather station using the URL provided as a Python dict
    return get_weather(url)

# get weather_by_site_code returns the data of a weather station from the site code that the user provides
def get_weather_by_site_code(site_code: str, province: str):
    # build the weather station URL using the provided variables
    url = build_site_url(site_code,province)
    # return the XML data of the weather station using the URL provided as a Python dict
    return get_weather(url)
