# importing modules for use
from dataclasses import dataclass
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
