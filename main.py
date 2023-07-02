# importing modules for use
import requests
import xmltodict
from csv import DictReader

# get_site_by_name returns a Python dict containing the data of a weather station if site name and province code variables match a station in a list
def get_site_by_name(site_name, province):
    body = requests.get("https://dd.weather.gc.ca/citypage_weather/docs/site_list_en.csv").text
    sites = parse_site_csv(body)
    # for each site in the Python list
    for i in range(len(sites)):
        site = sites[i]
        # if the current site name and province code match what the user provided
        if site["siteName"].strip().upper() == site_name.strip().upper() and site["province"].strip().upper() == province.strip().upper():
            return site
        # if it doesn't
        else:
            continue
    # otherwise, return an error message
    else:
        return "No site with this name found."

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
                {
                    "siteName":site["English Names"],
                    "province":site["Province Codes"],
                    "latitude":float(site["Latitude"][:-1]),
                    "longitude":-1 * float(site["Latitude"][:-1])
                }
            )
        # otherwise
        else:
            # continue
            continue
    # return the list
    return sites
