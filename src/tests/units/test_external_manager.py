import unittest
import requests
import pytest
from _pytest.monkeypatch import MonkeyPatch
from books.manager.external_books import ExternalBooks


class TestExternalBooks(unittest.TestCase):

    def test_get_books_by_name_no_name_match(self):

        obj = ExternalBooks()
        name = "no name"
        result = obj.get_books_by_name(name)

        assert result == {'status_code': 200, 'status': 'success', 'data': []}

    def test_get_books_by_name_with_name_match(self):

        obj = ExternalBooks()
        name = "The Mystery Knight"

        result = obj.get_books_by_name(name)
        assert result == {'status_code': 200, 'status': 'success', 'data': [{'name': 'The Mystery Knight', 'isbn': '978-0765360267', 'authors': ['George R. R. Martin'], 'number_of_pages': 416, 'publisher': 'Tor Fantasy', 'country': 'United States', 'release_date': '2011-03-29T00:00:00'}]}

    def test_get_books_with_execctions(self):

        monkeypatch = MonkeyPatch()
        def mock_get(url):
            raise Exception

        obj = ExternalBooks()
        monkeypatch.setattr(requests, "get", "mock_get")

        with pytest.raises(Exception):
            obj.get_books_by_name("no name")