import re

# import libmrlwchrnck


class Referencer:
    """get url for source from database"""

    def __init__(self, date):
        self.urls = {}
        # self.urls = libmrlwchrnck.get_urls(date)

    def get_url(self, author, date, title):
        """take a known url or fetch it"""

        title = re.sub(r'(\s{2,})"$', "\\1", title).strip()

        if (author, date, title) in self.urls:
            url = self.urls[(author, date, title)]
        else:
            # url = libmrlwchrnck.get_url(author, date, title)
            url = "TODO"
            self.urls[(author, date, title)] = url

        return url
