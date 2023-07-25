# importing modules for use
from dataclasses import dataclass

import requests
from requests import get

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

# get_site_by_name parses the data of a station from a CSV file and returns it as a dataclass
def get_site_by_name(site_name: str, province: str):
    # make a GET request to Environment Canada's web server to retrieve the CSV file containing all the weather stations
    body = get("https://dd.weather.gc.ca/citypage_weather/docs/site_list_en.csv")
    # parse the CSV file into a Python list
    sites = parse_site_csv(body.text)
    # for each site in the file
    for i in range(len(sites)):
        site = sites[i]
        # if the current site's name and province code match the provided variables, then return the file
        if site.siteName.strip().upper() == site_name.strip().upper() and site.province.strip().upper() == province.strip().upper():
            return site
        # otherwise, continue
        else:
            continue
    # if the requested site cannot be found, raise an error message
    else:
        raise ValueError("No site with this name found. Please check to see if you spelled it correctly, or are requesting data for the proper site.")

# get_weather returns the XML data located at the provided URL as a Python dict
def get_weather(url: str):
    # make a GET request to retrieve the XML data from the provided URL
    body = get(url).content
    # convert the XML file into a Python dict
    return parse_weather_xml(body)

# get_site_url builds and returns the URL of the page that hosts the requested XML data
def get_site_url(site_name: str, province: str):
    # get the dataclass corresponding to the site name and province provided
    site = get_site_by_name(site_name,province)
    # build the URL for the hosted XML data of the station
    url = build_site_url(site.code,site.province)
    # return the url
    return url

# build_site_url returns the URL of the hosted XML data of the site using the provided site code and province
def build_site_url(site_code: str, province: str):
    return f"http://dd.weather.gc.ca/citypage_weather/xml/{province}/{site_code}_e.xml"