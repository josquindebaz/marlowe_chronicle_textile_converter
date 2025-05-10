from datetime import datetime


def get_url_from_database(database, author, day, title):
    """
    returns url from given database, author, day (in date format) and title
    """

    if not database:
        return ""

    cursor = database.cursor()
    day = day.isoformat()
    request = "SELECT `m_url` FROM `tbl_texte` WHERE `m_date` >= %s AND `m_date` <= %s AND `m_auteur` = %s AND `m_titre` = %s"

    cursor.execute(request, (day, f"{day} 23:59:59", author, title))
    result = cursor.fetchone()

    if not result:
        return ""

    return result[0]


def get_urls_from_database(database, day):
    """
    returns all url from given database ad day (in date format)
    """

    if not database:
        return {}

    cursor = database.cursor()
    day = day.isoformat()
    request = "SELECT `m_auteur`, `m_titre`, `m_url` FROM `tbl_texte` WHERE `m_date` >= %s AND `m_date` <= %s"
    cursor.execute(request, (day, f"{day} 23:59:59"))

    return {
        (item[0], day, item[1]): item[2]
        for item in cursor.fetchall()
    }


class Referencer:
    """
    get url for source from database
    constructor has a date format day as parameter
    get_url has a string format day as parameter
    """

    def __init__(self, database, day):
        self._database = database
        self._urls = get_urls_from_database(self._database, day)

    def get_url(self, author, string_formated_day, title):
        """
        returns a known url or fetch it from database given as property
        for a given day 01/01/2025
        """

        day = datetime.strptime(string_formated_day, "%d/%m/%Y").date()
        iso_day = day.isoformat()
        item_identifier = (author, iso_day, title)

        if item_identifier not in self._urls:
            self._urls[item_identifier] = (
                get_url_from_database(self._database, author, day, title)
            )

        return self._urls[item_identifier]
