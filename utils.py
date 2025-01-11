import datetime
import re


def get_introduction_date(date):
    """Get date from text date"""

    (day, month, year,
     hour, minutes, seconds) = (re.search(r"(\d*)/\s*(\d*)/(\d{4})\s*(\d*):(\d*):(\d*)", date)
                                .group(1, 2, 3, 4, 5, 6))

    return datetime.datetime.combine(
        datetime.date(int(year), int(month), int(day)),
        datetime.time(int(hour), int(minutes), int(seconds))
    )


def enhance_date_output(block):
    """From dd/mm/yyyy to day month year"""

    # locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    dates = re.findall(r"[\s:](\d{1,2}/\s*\d{1,2}/\d{4})[^/]", block)

    for pattern in list(set(dates)):
        day, month, year = pattern.split("/")
        date = datetime.date(int(year), int(month), int(day))
        block = re.sub(pattern, date.strftime("%-d %B %Y"), block)

    return block
