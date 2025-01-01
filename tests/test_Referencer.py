from Referencer import Referencer


def test_get_url():
    referencer = Referencer("2025-01-01")
    referencer.urls[("author", "date", "title")] = "any url"

    result = referencer.get_url("author", "date", "title")

    assert result == "any url"

