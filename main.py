from geopy.geocoders import Nominatim
from requests import get
from xmltodict import parse
from csv import DictReader
from geopy import distance

def get_user_coordinates(user_location: str):
    geolocator = Nominatim(user_agent="tmgkopczyk@gmail.com")
    user_coordinates = geolocator.geocode(user_location)
    return user_coordinates.latitude, user_coordinates.longitude

def get_weather_by_site_name(site_name: str, province: str):
    url = get_site_url(site_name, province)
    return get_weather(url)

def get_weather_by_user_location(user_location: str):
    lat, lon = get_user_coordinates(user_location)
    sites = get_ec_sites_list()
    closest = closest_site(sites, lat, lon)
    return get_weather_by_site_code(closest["Codes"], closest["Province Codes"])

def get_weather_by_site_code(site_code: str, province: str):
    url = build_site_url(site_code, province)
    return get_weather(url)

def get_site_by_name(site_name: str, province: str):
    body = get("http://dd.weather.gc.ca/citypage_weather/xml/siteList.xml").text.encode("iso-8859-1").decode("utf-8")
    sites = parse_site_xml(body)
    for site in sites:
        if site["siteName"].strip().upper() == site_name.strip().upper() and site["province"].strip().upper() == province.strip().upper():
            return site
        else:
            continue
    return NameError("No site with this name found.")

def get_weather(url):
    body = get(url)
    return parse_weather_xml(body)

def get_site_url(site_name: str, province: str):
    site = get_site_by_name(site_name, province)
    url = build_site_url(site["code"], site["province"])
    return url

def build_site_url(site_code: str, province: str):
    return f"http://dd.weather.gc.ca/citypage_weather/xml/{province}/{site_code}_e.xml"

def parse_site_xml(xml):
    json = parse(xml)
    sites = []
    for site in json["siteList"]["site"]:
        sites.append(
            {
                "siteName": site["nameEn"],
                "code": site["@code"],
                "province": site["provinceCode"]
            }
        )
    return sites

def parse_weather_xml(xml):
    json = parse(xml.text)
    weather_root = json["siteData"]
    weather = {
        "temperature": 'N/A',
        "temperatureUnit": 'N/A',
        "conditions": 'N/A',
        "warnings": [],
        "forecasts": [],
        "relativeHumidityPercent": 0,
        "windSummary": 'N/A',
        "windChillSummary": 'N/A'
    }

    current_conditions = weather_root["currentConditions"]
    if current_conditions:
        temperature = current_conditions["temperature"]
        weather["conditions"] = current_conditions["condition"]
        weather["temperature"] = float(temperature["#text"])
        weather["temperatureUnit"] = temperature["@units"]

    if weather_root["forecastGroup"].get("forecast"):
        for forecast in weather_root["forecastGroup"]["forecast"]:
            pop = forecast["abbreviatedForecast"]["pop"]
            weather["forecasts"].append({
                "period": forecast["period"]["#text"],
                "temperature": forecast["temperatures"]["textSummary"],
                "pop": f"{pop['#text'] if pop.get('#text') else 0}{pop['@units']}",
                "popSummary": forecast["precipitation"]["textSummary"],
                "cloudPopSummary": forecast["cloudPrecip"]["textSummary"],
                "relativeHumidityPercent":f'{forecast["relativeHumidity"]["#text"]}{forecast["relativeHumidity"]["@units"]}',
                "windSummary": forecast["winds"].get("textSummary") if forecast.get("winds") and forecast["winds"].get("textSummary") else "N/A",
                "windChillSummary": forecast["windChill"].get("textSummary") if forecast.get("windChill") and forecast["winds"].get("textSummary") else "N/A",
                "summary": forecast["abbreviatedForecast"]["textSummary"],
                "fullSummary": forecast["textSummary"]
            })
        try:
            for warning in weather_root["warnings"]:
                if weather_root["warnings"][warning]:
                    try:
                        weather["warnings"].append({
                            "description": weather_root["warnings"][warning]["@description"],
                            "priority": weather_root["warnings"][warning]["@priority"]
                        })
                    except TypeError:
                        continue
                else:
                    continue
        except TypeError:
            pass
    return weather

def get_ec_sites_list():
    sites = []
    response = get("https://dd.weather.gc.ca/citypage_weather/docs/site_list_en.csv")
    sites_csv_string = response.text.encode("iso-8859-1").decode("utf-8")
    sites_reader = DictReader(sites_csv_string.splitlines()[1:])
    for site in sites_reader:
        if site["Province Codes"] != "HEF":
            site["Latitude"] = float(site["Latitude"][:-1])
            site["Longitude"] = -1 * float(site["Longitude"][:-1])
            sites.append(site)
        else:
            continue
    return sites


def closest_site(site_list, lat, lon):
    def site_distance(site):
        return distance.distance((lat, lon), (site["Latitude"], site["Longitude"]))

    closest = min(site_list, key=site_distance)
    return closest


def main():
    weather_by_location = get_weather_by_user_location("14 Wiltshire Circle, Ottawa, ON")
    print(weather_by_location["forecasts"][0]["fullSummary"])


if __name__ == "__main__":
    main()
