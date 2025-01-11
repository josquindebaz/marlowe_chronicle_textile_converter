import datetime

import utils


def test_format_date():
    block = 'The dates 26/ 1/2005, 28/12/2024, 3/ 1/2025, and 03/01/2025 are fine'
    expected = 'The dates 26 January 2005, 28 December 2024, 3 January 2025, and 3 January 2025 are fine'

    result = utils.enhance_date_output(block)

    assert result == expected


def test_format_introduction_date():
    introduction_date = " 3/ 1/2025 23:7:2 "

    result = utils.get_introduction_date(introduction_date)

    assert result == datetime.datetime(2025, 1, 3, 23, 7, 2)
