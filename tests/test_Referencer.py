import unittest
from unittest.mock import MagicMock

from Referencer import Referencer, get_url_from_database


class TestReferencer(unittest.TestCase):
    def test_get_url_from_database(self):
        mock_database = unittest.mock.MagicMock()
        mock_cursor = MagicMock()
        mock_database.cursor.return_value = mock_cursor

        expected_result = "any url"
        mock_cursor.fetchone.return_value = [expected_result]

        author = "author"
        date = "2025-01-01"
        title = "title"

        result = get_url_from_database(mock_database, author, date, title)

        self.assertEqual(result, expected_result)
        mock_cursor.execute.assert_called_once_with(
            'SELECT `m_url` FROM `tbl_texte` WHERE `m_date` >= %s AND `m_date` <= %s AND `m_auteur` = %s AND `m_titre` = %s',
            ('2025-01-01', '2025-01-01 23:59:59', 'author', 'title')),

    def test_get_url_returns_known_url(self):
        referencer = Referencer(None, "2025-01-01")
        referencer.urls[("author", "date", "title")] = "any url"

        result = referencer.get_url("author", "date", "title")

        self.assertEqual(result, "any url")

    def test_get_url_returns_empty_when_no_url(self):
        mock_database = MagicMock()
        mock_cursor = MagicMock()
        mock_database.cursor.return_value = mock_cursor

        expected_result = ""
        mock_cursor.fetchone.return_value = [expected_result]

        date = "01/01/2025"
        referencer = Referencer(mock_database, date)

        author = "author"
        title = "title"

        result = referencer.get_url(author, date, title)

        self.assertEqual(result, expected_result)
        mock_cursor.execute.assert_called_once_with(
            'SELECT `m_url` FROM `tbl_texte` WHERE `m_date` >= %s AND `m_date` <= %s AND `m_auteur` = %s AND `m_titre` = %s',
            ('2025-01-01', '2025-01-01 23:59:59', 'author', 'title'))

    def test_get_url_returns_url_fetched_in_db(self):
        mock_database = MagicMock()
        mock_cursor = MagicMock()
        mock_database.cursor.return_value = mock_cursor

        expected_result = "any url"
        mock_cursor.fetchone.return_value = [expected_result]

        date = "01/01/2025"
        referencer = Referencer(mock_database, date)

        author = "author"
        title = "title"

        result = referencer.get_url(author, date, title)

        self.assertEqual(result, expected_result)
        mock_cursor.execute.assert_called_once_with(
            'SELECT `m_url` FROM `tbl_texte` WHERE `m_date` >= %s AND `m_date` <= %s AND `m_auteur` = %s AND `m_titre` = %s',
            ('2025-01-01', '2025-01-01 23:59:59', 'author', 'title'))
