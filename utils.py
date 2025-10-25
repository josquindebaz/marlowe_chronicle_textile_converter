import datetime
import re

from babel.dates import format_date, format_datetime


def get_introduction_date(date):
    """Get date from text date"""

    (day, month, year,
     hour, minutes, seconds) = (re.search(r"(\d*)/\s*(\d*)/(\d{4})\s*(\d*):(\d*):(\d*)", date)
                                .group(1, 2, 3, 4, 5, 6))

    return datetime.datetime.combine(
        datetime.date(int(year), int(month), int(day)),
        datetime.time(int(hour), int(minutes), int(seconds))
    )


def dates_to_long_dates(block):
    """From dd/mm/yyyy to day month year"""

    dates = re.findall(r"[\s:](\d{1,2}/\s*\d{1,2}/\d{4})[^/]", block)

    for pattern in list(set(dates)):
        if (pattern == "00/00/0000"):
            print(pattern, "invalid date")
            continue
        day, month, year = pattern.split("/")
        date = datetime.date(int(year), int(month), int(day))
        long_date = format_date(date, format='long', locale='fr_FR.UTF-8')
        block = re.sub(pattern, long_date, block)

    return block


def datetime_to_long_datetime(date_time):
    """28/12/2024 23:4:53 to samedi 28 décembre 2024 23:04:53"""

    return format_datetime(date_time, "eeee d MMMM Y H:mm:ss", locale='fr_FR.UTF-8')


def harmonize_domain_url(block):
    block = re.sub("gspr.ehess.free.fr", "gspr-ehess.com", block)
    block = re.sub("92.243.27.161", "prosperologie.org", block)

    return block
