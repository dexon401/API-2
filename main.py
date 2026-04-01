import requests
import sys
from pprint import pprint
import get_bbox

STATIC_MAPS_API_KEY = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
STATIC_MAPS_URL = "https://static-maps.yandex.ru/v1"

GEOCODER_API_KEY = "8013b162-6b42-4997-9691-77b7074026e0"
GEOCODER_URL = "https://geocode-maps.yandex.ru/v1"

SEARCH_MAPS_API_KEY = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
SEARCH_MAPS_URL = "https://search-maps.yandex.ru/v1"

address = input("Введите адрес: ")

geocoder_params = {"apikey": GEOCODER_API_KEY, "geocode": address, "lang": "ru_RU", "format": "json"}

response = requests.get(GEOCODER_URL, params=geocoder_params)
if not response:
    print(response)
    print(GEOCODER_URL)
    print(geocoder_params)
    sys.exit()

json_response = response.json()

toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
toponym_pos = str(toponym["Point"]["pos"]).replace(" ", ",")    

params = {
    "apikey": SEARCH_MAPS_API_KEY,
    "text": "Аптека",
    "lang": "ru_RU",
    "type": "biz",
    "ll": toponym_pos
}

response = requests.get(SEARCH_MAPS_URL, params=params)
if not response:
    print(response)
    print(SEARCH_MAPS_URL)
    print(params)
    sys.exit()

json_response = response.json()

bbox = get_bbox.get_bbox(json_response["features"][:10])

list_of_apteks = []
for i in range(10):
    apteka = json_response["features"][i]
    apteka_dict = {}
    apteka_dict["coordinates"] = apteka["geometry"]["coordinates"]
    apteka_dict["work_hours"] = apteka["properties"]["CompanyMetaData"]["Hours"].get("Availabilities", [])[0].get("Intervals", [])
    apteka_dict
    list_of_apteks.append(apteka_dict)

pt = []
for apteka in list_of_apteks:
    coords = ",".join(map(str, list(apteka["coordinates"])))
    if apteka["work_hours"]:
        from_time = apteka["work_hours"][0]["from"]
        to_time = apteka["work_hours"][0]["to"]
        if (from_time in ['00:00:00', '00:00'] and to_time in ['23:59:59', '23:59', '00:00:00', '00:00']):
            pt.append(f"{coords},pmgnl")
        else:
            pt.append(f"{coords},pmbll")
    else:
        pt.append(f"{coords},pmgrl")

params = {
    "apikey": STATIC_MAPS_API_KEY,
    "ll": bbox["center"],
    "bbox": bbox["bbox"],
    "pt": "~".join(pt)
}

response = requests.get(STATIC_MAPS_URL, params=params)
if not response:
    print(response)
    print(STATIC_MAPS_URL)
    print(params)
    sys.exit()

with open("map.png", "wb") as file:
    file.write(response.content)
    print("Карта успешно сохранена в map.png!")