# importing modules for use
import requests
import xmltodict
from csv import DictReader
from dataclasses import dataclass

@dataclass
class WeatherStation:
    code: str
    name: str
    province: str
    longitude: float
    latitude: float

# get_weather_by_site_name returns weather data for the site specified
def get_weather_by_site_name(site_name, province):
    # get the url of the site
    url = get_site_url(site_name,province)
    # return the data from the url
    return url

# get_site_url returns a URL that hosts the XML data of a site
def get_site_url(site_name,province):
    # return a Python dict for the site name and province provided
    site = get_site_by_name(site_name,province)
    # construct a URL from the site data retrieved
    url = build_site_url(site.code,site.province)
    return url

# build_site_url builds the URL of the XML data of a weather station from the user provided site code and province
def build_site_url(site_code,province):
    return f"http://dd.weather.gc.ca/citypage_weather/xml/{province}/{site_code}_e.xml"

# get_site_by_name returns a Python dict containing the data of a weather station if site name and province code variables match a station in a list
def get_site_by_name(site_name, province):
    body = requests.get("https://dd.weather.gc.ca/citypage_weather/docs/site_list_en.csv").text
    sites = parse_site_csv(body)
    # for each site in the Python list
    for i in range(len(sites)):
        site = sites[i]
        # if the current site name and province code match what the user provided
        if site.name.strip().upper() == site_name.strip().upper() and site.province.strip().upper() == province.strip().upper():
            return site
        # if it doesn't
        else:
            continue
    # otherwise, return an error message
    else:
        raise ValueError("The values provided do not match a specific site in the list. Are you sure you spelled them correctly?")

# parse_site_csv takes a CSV file and converts into a Python list
def parse_site_csv(csv_file):
    sites = []
    sites_reader = DictReader(csv_file.splitlines()[1:])
    # for each site in the CSV file
    for site in sites_reader:
        # if the site's province code is not HEF
        if site["Province Codes"] != "HEF":
            # then append the site's data to the list
            sites.append(
                WeatherStation(
                    code=site["Codes"],
                    name=site["English Names"],
                    province=site["Province Codes"],
                    longitude=-1 * float(site["Latitude"][:-1]),
                    latitude=float(site["Latitude"][:-1])
                )
            )
        # otherwise
        else:
            # continue
            continue
    # return the list
    return sites

site = get_site_by_name("Ottawa (Kanata - Orleans)","ON")
print(site)