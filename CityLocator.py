import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request


def query_coordinates(city):
    """ Query coordinates to Nominatim API"""

    params = urllib.parse.urlencode({"q": city, "format": "json", "limit": 1})
    url = "http://nominatim.openstreetmap.org/search?%s" % params

    try:
        with urllib.request.urlopen(url) as response:
            answer = response.read()

        location = json.loads(answer.decode())
        latitude = location[0]['lat']
        longitude = location[0]['lon']

        time.sleep(1) # make sure not to spam Nominatim API

        return [latitude, longitude]

    except urllib.error.URLError as e:
        print(f"Problem with Nominatim: {city}: {e}")
        return [0, 0]


class CityLocator:
    """Store town coordinates"""

    def __init__(self, file="city_coordinates.json"):
        self.cities = {}
        self.coordinates_file = file
        self.read_file()

    def read_file(self):
        """read json file"""

        if not os.path.isfile(self.coordinates_file):
            path_for_tests = os.path.join("../", self.coordinates_file)
            if not os.path.isfile(path_for_tests):
                return
            else:
                self.coordinates_file = path_for_tests

        with open(self.coordinates_file) as handle:
            coordinates = json.load(handle)

        for item in coordinates.items():
            self.cities[item[0]] = [item[1][0], item[1][1]]

    def get_coordinates(self, city):
        """return latitude and longitude of given city"""

        if city not in self.cities:
            latitude, longitude = query_coordinates(city)
            self.cities[city] = [latitude, longitude]
            self.save_coordinates(city, latitude, longitude)

        return self.cities[city]

    def save_coordinates(self, city, latitude, longitude):
        """write city coordinates in json file"""

        self.cities[city] = [latitude, longitude]

        with open(self.coordinates_file, 'w', encoding='utf8') as handle:
            str_ = json.dumps(self.cities, indent=4, sort_keys=True, ensure_ascii=False)
            handle.write(str_)
