from CityLocator import CityLocator, query_coordinates


def test_can_read_file():
    city_locator = CityLocator("../city_coordinates.json")

    assert len(city_locator.cities) > 0

def test_can_get_existing_coordinates():
    city_locator = CityLocator("../city_coordinates.json")

    result = city_locator.get_coordinates("Paris")

    assert result == ['48.8566101', '2.3514992']

def test_can_query_coordinates():
    result = query_coordinates("Paris")

    assert result == ['48.8588897', '2.3200410217200766']