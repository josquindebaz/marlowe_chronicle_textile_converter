import json
import os


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

    def get_coord(self, town):
        """return latitude and longitude of given city"""

        if town not in self.cities:
            return None

        return self.cities[town]

    def save_coord(self, town, latitude, longitude):
        """write city coordinates in json file"""

        self.cities[town] = [latitude, longitude]

        with open(self.coordinates_file, 'w', encoding='utf8') as handle:
            str_ = json.dumps(self.cities,
                              indent=4,
                              sort_keys=True,
                              ensure_ascii=False)
            handle.write(str_)
