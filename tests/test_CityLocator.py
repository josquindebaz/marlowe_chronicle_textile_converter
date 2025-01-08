from CityLocator import CityLocator


def test_can_read_file():
    city_locator = CityLocator("../city_coordinates.json")

    assert len(city_locator.cities) > 0

def test_can_get_coord():
    city_locator = CityLocator("../city_coordinates.json")

    result = city_locator.get_coord("Paris")

    assert result == ['48.8566101', '2.3514992']
