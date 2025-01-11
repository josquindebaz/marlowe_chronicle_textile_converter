import datetime

import utils


def test_format_date():
    block = 'The dates 26/ 1/2005, 28/12/2024, 3/ 1/2025, and 03/01/2025 are fine'
    expected = 'The dates 26 janvier 2005, 28 décembre 2024, 3 janvier 2025, and 3 janvier 2025 are fine'

    result = utils.dates_to_long_dates(block)

    assert result == expected


def test_format_introduction_date():
    introduction_date = " 3/ 1/2025 23:7:2 "

    result = utils.get_introduction_date(introduction_date)

    assert result == datetime.datetime(2025, 1, 3, 23, 7, 2)


def test_datetime_to_full_datetime():
    date = datetime.datetime(2025, 1, 3, 23, 7, 2)

    result = utils.datetime_to_long_datetime(date)

    assert result == "vendredi 3 janvier 2025 23:07:02"


def test_harmonize_domain_url_change_gspr_free():
    content = "Voici un lien http://gspr.ehess.free.fr/ à consulter."
    expected = 'Voici un lien http://gspr-ehess.com/ à consulter.'

    result = utils.harmonize_domain_url(content)

    assert result == expected


def test_harmonize_domain_url_change_prosperologie_ip():
    content = "Voici un lien http://92.243.27.161 à consulter."
    expected = 'Voici un lien http://prosperologie.org à consulter.'

    result = utils.harmonize_domain_url(content)

    assert result == expected
