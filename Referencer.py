import re


def get_url_from_database(database, author, date, title):
    if not database:
        return ""

    cursor = database.cursor()
    end_of_the_day = f"{date} 23:59:59"
    request = "SELECT `m_url` FROM `tbl_texte` WHERE `m_date` >= %s AND `m_date` <= %s AND `m_auteur` = %s AND `m_titre` = %s"
    try:
        cursor.execute(request, (date, end_of_the_day, author, title))
        result = cursor.fetchone()[0]
    except:
        print("issue with ", [author, date, title])
        result = ""

    return result


def get_urls_from_database(database, date):
    if not database:
        return {}

    cursor = database.cursor()
    end_of_the_day = f"{date} 23:59:59"

    request = "SELECT `m_auteur`, `m_titre`, `m_url` FROM `tbl_texte` WHERE `m_date` >= %s AND `m_date` <= %s"
    cursor.execute(request, (date, end_of_the_day))
    data = cursor.fetchall()

    return {
        (item[0], date, item[1]): item[2]
        for item in data
    }

class Referencer:
    """get url for source from database"""

    def __init__(self, database, date):
        self.urls = {}
        self.database = database
        date = "-".join(reversed(date.split("/")))

        self.urls = get_urls_from_database(self.database, date)

    def get_url(self, author, date, title):
        """returns a known url or fetch it from database"""
        title = re.sub(r'(\s{2,})"$', "\\1", title).strip()

        date = "-".join(reversed(date.split("/")))

        if (author, date, title) not in self.urls:
            self.urls[(author, date, title)] = get_url_from_database(self.database, author, date, title)

        return self.urls[(author, date, title)]
