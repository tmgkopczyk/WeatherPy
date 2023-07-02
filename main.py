# importing modules for use
import requests
import xmltodict
from csv import DictReader

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
