import re
from datetime import date


def get_url_from_database(database, author, day, title):
    if not database:
        return ""

    cursor = database.cursor()
    day = day.isoformat()
    end_of_the_day = f"{day} 23:59:59"
    request = "SELECT `m_url` FROM `tbl_texte` WHERE `m_date` >= %s AND `m_date` <= %s AND `m_auteur` = %s AND `m_titre` = %s"

    try:
        cursor.execute(request, (day, end_of_the_day, author, title))
        result = cursor.fetchone()[0]
    except:
        print("issue with ", [author, day, title])
        return ""

    return result


def get_urls_from_database(database, day):
    if not database:
        return {}

    cursor = database.cursor()
    day = day.isoformat()
    end_of_the_day = f"{day} 23:59:59"

    request = "SELECT `m_auteur`, `m_titre`, `m_url` FROM `tbl_texte` WHERE `m_date` >= %s AND `m_date` <= %s"
    cursor.execute(request, (day, end_of_the_day))
    data = cursor.fetchall()

    return {
        (item[0], day, item[1]): item[2]
        for item in data
    }


class Referencer:
    """
    get url for source from database
    constructor has a date format day as parameter
    get_url has a string format day as parameter
    """

    def __init__(self, database, day):
        self.urls = {}
        self.database = database

        self.urls = get_urls_from_database(self.database, day)

    def get_url(self, author, string_formated_day, title):
        """
        returns a known url or fetch it from database given as property
        for a given day 01/01/2025
        """

        title = re.sub(r'(\s{2,})"$', "\\1", title).strip()

        string_formated_day = "-".join(reversed(string_formated_day.split("/")))

        if (author, string_formated_day, title) not in self.urls:
            self.urls[(author, string_formated_day, title)] = get_url_from_database(self.database, author,
                                                                                    date.fromisoformat(
                                                                                        string_formated_day),
                                                                                    title)

        return self.urls[(author, string_formated_day, title)]
