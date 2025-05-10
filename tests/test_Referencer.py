import unittest
from datetime import date
from unittest.mock import MagicMock, call

from Referencer import Referencer, get_url_from_database, get_urls_from_database


class TestReferencer(unittest.TestCase):
    def test_get_url_from_database(self):
        mock_database = unittest.mock.MagicMock()
        mock_cursor = MagicMock()
        mock_database.cursor.return_value = mock_cursor

        expected_result = "example.com"
        mock_cursor.fetchone.return_value = [expected_result]

        author = "author"
        db_date = "2025-01-01"
        title = "title"

        result = get_url_from_database(mock_database, author, date.fromisoformat(db_date), title)

        self.assertEqual(result, expected_result)
        mock_cursor.execute.assert_called_once_with(
            'SELECT `m_url` FROM `tbl_texte` WHERE `m_date` >= %s AND `m_date` <= %s AND `m_auteur` = %s AND `m_titre` = %s',
            (db_date, f'{db_date} 23:59:59', author, title)),

    def test_get_urls_from_database(self):
        mock_database = MagicMock()
        mock_cursor = MagicMock()
        mock_database.cursor.return_value = mock_cursor

        db_date = "2025-01-01"
        author = "author"
        title = "title"
        url = "example.com"

        expected_result = {(author, db_date, title): url}
        mock_cursor.fetchall.return_value = [(author, title, url)]

        result = get_urls_from_database(mock_database, date.fromisoformat(db_date))

        self.assertEqual(result, expected_result)
        mock_cursor.execute.assert_called_once_with(
            'SELECT `m_auteur`, `m_titre`, `m_url` FROM `tbl_texte` WHERE `m_date` >= %s AND `m_date` <= %s',
            (db_date, f'{db_date} 23:59:59'))

    def test_get_url_returns_known_url(self):
        marlowe_date = "01/01/2025"
        db_date = "2025-01-01"
        author = "author"
        title = "title"

        referencer = Referencer(None, date.fromisoformat(db_date))
        referencer.urls[(author, db_date, title)] = "example.com"

        result = referencer.get_url(author, marlowe_date, title)

        self.assertEqual(result, "example.com")

    def test_get_url_returns_empty_when_no_url(self):
        mock_database = MagicMock()
        mock_cursor = MagicMock()
        mock_database.cursor.return_value = mock_cursor

        expected_result = ""
        mock_cursor.fetchone.return_value = [expected_result]

        marlowe_date = "01/01/2025"
        db_date = "2025-01-01"

        referencer = Referencer(mock_database, date.fromisoformat(db_date))

        author = "author"
        title = "title"

        result = referencer.get_url(author, marlowe_date, title)

        self.assertEqual(result, expected_result)
        mock_cursor.execute.assert_has_calls([
            call('SELECT `m_auteur`, `m_titre`, `m_url` FROM `tbl_texte` WHERE `m_date` >= %s AND `m_date` <= %s',
                 (db_date, f'{db_date} 23:59:59')),
            call(
                'SELECT `m_url` FROM `tbl_texte` WHERE `m_date` >= %s AND `m_date` <= %s AND `m_auteur` = %s AND `m_titre` = %s',
                (db_date, f'{db_date} 23:59:59', author, title))])

    def test_get_url_returns_url_fetched_in_db(self):
        mock_database = MagicMock()
        mock_cursor = MagicMock()
        mock_database.cursor.return_value = mock_cursor

        expected_result = "example.com"
        mock_cursor.fetchone.return_value = [expected_result]

        marlowe_date = "01/01/2025"
        db_date = "2025-01-01"

        referencer = Referencer(mock_database, date.fromisoformat(db_date))

        author = "author"
        title = "title"

        result = referencer.get_url(author, marlowe_date, title)

        self.assertEqual(result, expected_result)
        mock_cursor.execute.assert_has_calls(
            [call('SELECT `m_auteur`, `m_titre`, `m_url` FROM `tbl_texte` WHERE `m_date` >= %s AND `m_date` <= %s',
                  (db_date, f'{db_date} 23:59:59')),
             call(
                 'SELECT `m_url` FROM `tbl_texte` WHERE `m_date` >= %s AND `m_date` <= %s AND `m_auteur` = %s AND `m_titre` = %s',
                 (db_date, f'{db_date} 23:59:59', author, title))]
        )

    def test_Referencer_constructor_calls_get_urls_from_database(self):
        mock_database = MagicMock()
        mock_cursor = MagicMock()
        mock_database.cursor.return_value = mock_cursor

        db_date = "2025-01-01"
        author = "author"
        title = "title"
        url = "example.com"

        expected_result = {(author, db_date, title): url}
        mock_cursor.fetchall.return_value = [(author, title, url)]

        referencer = Referencer(mock_database, date.fromisoformat(db_date))

        self.assertEqual(referencer.urls, expected_result)
        mock_cursor.execute.assert_called_once_with(
            'SELECT `m_auteur`, `m_titre`, `m_url` FROM `tbl_texte` WHERE `m_date` >= %s AND `m_date` <= %s',
            (db_date, f'{db_date} 23:59:59'))
