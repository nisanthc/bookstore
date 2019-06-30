import pytest
from _pytest.monkeypatch import MonkeyPatch
from books.manager.internal_books import InternalBooks
from utils.db_manager import DBManager
from config.db_settings import databases


@pytest.fixture
def setup_database_data():
    db_obj = DBManager(databases['books'])

    cleanup_query = [
        "delete from author_book",
        "delete from book",
        "delete from author"
    ]
    for query in cleanup_query:
        db_obj.processquery(query=query)

    setup_query = [
        "INSERT INTO `author` VALUES (2,'John Doe','2019-06-28 18:50:11'),(3,'Martin','2019-06-28 19:33:14'),(4,'Jeo','2019-06-29 00:37:02'),(5,'kelin','2019-06-29 01:37:16')",
        "INSERT INTO `book` VALUES (10,'Jungle book','123456',400,'No Books','UK States','2019-01-20','2019-06-29 01:24:16','2019-06-29 01:50:13')",
        "INSERT INTO `author_book` VALUES (14,10,2),(15,10,3),(16,10,4),(17,10,5)"
    ]
    for query in setup_query:
        db_obj.processquery(query=query)

    db_obj.commit()
    db_obj.close()


class TestInternalBooks():
    test_data = [
        (
            ("id", 97),
            (
                {
                    "status_code": 200,
                    "status": "success",
                    "data": []
                }
            )
        ),
        (
            ("name", "no name"),
            (
                {
                    "status_code": 200,
                    "status": "success",
                    "data": []
                }
            )
        ),
        (
            ("publisher", "empty publisher"),
            (
                {
                    "status_code": 200,
                    "status": "success",
                    "data": []
                }
            )
        ),
        (
            ("country", "mars"),
            (
                {
                    "status_code": 200,
                    "status": "success",
                    "data": []
                }
            )
        ),
        (
            ("release date", "2030-12-12"),
            (
                {
                    "status_code": 200,
                    "status": "success",
                    "data": []
                }
            )

        )
    ]

    @pytest.mark.parametrize("input_data, expected_data", test_data)
    def test_get_books_no_data(self, input_data, expected_data):
        obj = InternalBooks()
        result = obj.get_books(input_data[0], input_data[1])

        assert result == expected_data

    def test_get_all_books_with_data(self, setup_database_data):
        obj = InternalBooks()
        result = obj.get_books("all", None)

        assert result == {'status_code': 200, 'status': 'success', 'data': [
            {'id': 10, 'name': 'Jungle book', 'number_of_pages': 400, 'publisher': 'No Books', 'country': 'UK States',
             'release_date': '2019-01-20',  'isbn': '123456', 'authors': ['John Doe', 'Martin', 'Jeo', 'kelin']}]}

    def test_get_books_with_data(self, setup_database_data):
        obj = InternalBooks()
        result = obj.get_books("id", 10)
        assert result == {'status_code': 200, 'status': 'success',
                          'data': {'id': 10, 'name': 'Jungle book', 'isbn': '123456', 'number_of_pages': 400,
                                   'publisher': 'No Books', 'country': 'UK States', 'release_date': '2019-01-20',
                                   'authors': ['John Doe', 'Martin', 'Jeo', 'kelin']}}

    def test_insert_new_book(self, setup_database_data):
        new_book = {'name': 'Game of thorns', 'isbn': '978-0553103540', 'authors': ['Mukund', 'Sherk', "Jeo"],
                    'number_of_pages': 450, 'publisher': 'Martin Books', 'country': 'UK', 'release_date': '2018-09-10'}
        obj = InternalBooks()
        result = obj.insert_book(new_book)

        assert result == {'status_code': 201, 'status': 'success', 'data': [{'book': {'name': 'Game of thorns',
                                                                                      'isbn': '978-0553103540',
                                                                                      'number_of_pages': 450,
                                                                                      'publisher': 'Martin Books',
                                                                                      'country': 'UK',
                                                                                      'release_date': '2018-09-10',
                                                                                      'authors': ['Mukund', 'Sherk',
                                                                                                  'Jeo']}}]}

    def test_insert_existing_book(self, setup_database_data):
        existing_book = {'name': 'Jungle book', 'isbn': '123456', 'number_of_pages': 400, 'publisher': 'No Books',
                         'country': 'UK States', 'release_date': "2019-11-20", 'authors': ['Martin', "Jeo"]}
        obj = InternalBooks()
        result = obj.insert_book(existing_book)

        assert result == {'status_code': 201, 'status': 'success', 'data': [{'book': {'name': 'Jungle book', 'isbn': '123456', 'number_of_pages': 400, 'publisher': 'No Books', 'country': 'UK States', 'release_date': '2019-01-20', 'authors': ['John Doe', 'Martin', 'Jeo', 'kelin']}}]}

    def test_patch_book(self, setup_database_data):
        book_id = 10
        patch_book = {'name': 'Jungle book', 'authors': ['John Doe', 'Martin', 'Jeo', 'kelin'], 'publisher': 'No Books',
                      'country': 'UK States', 'isbn': '123456', 'number_of_pages': 400, 'release_date': '2019-01-20'}
        obj = InternalBooks()
        result = obj.patch_book(book_id, patch_book)
        assert result == {'status_code': 200, 'status': 'success',
                          'message': 'The book Jungle book was updated successfully',
                          'data': {'id': 10, 'name': 'Jungle book', 'isbn': '123456', 'number_of_pages': 400,
                                   'publisher': 'No Books', 'country': 'UK States', 'release_date': '2019-01-20',
                                   'authors': ['John Doe', 'Martin', 'Jeo', 'kelin']}}

    def test_patch_book_resource_not_available(self, setup_database_data):
        book_id = 10000
        patch_book = {'name': 'Jungle book', 'authors': ['John Doe', 'Martin', 'Jeo', 'kelin'], 'publisher': 'No Books',
                      'country': 'UK States', 'isbn': '123456', 'number_of_pages': 400, 'release_date': '2019-01-20'}
        obj = InternalBooks()

        with pytest.raises(Exception):
            obj.patch_book(book_id, patch_book)

    def test_delete_book(self, setup_database_data):
        book_id = 10
        obj = InternalBooks()

        result = obj.delete_book(book_id)

        assert result == {'status_code': 200, 'status': 'success',
                          'message': 'The book Jungle book was deleted successfully', 'data': []}

    def test_delete_book_resource_not_available(self, setup_database_data):
        book_id = 10000
        obj = InternalBooks()

        with pytest.raises(Exception):
            obj.delete_book(book_id)

    def test_get_books_raise_exceptions(self):
        monkeypatch = MonkeyPatch()

        def mock_format_get_response(result):
            raise Exception

        obj = InternalBooks()
        monkeypatch.setattr(InternalBooks, "format_get_response", mock_format_get_response)

        with pytest.raises(Exception):
            obj.get_books("id", 10)

    def test_insert_books_raise_exceptions(self):
        monkeypatch = MonkeyPatch()

        new_book = {'name': 'Game of error', 'isbn': '978-0553103540', 'authors': ['Mukund', 'Sherk', "Jeo"],
                    'number_of_pages': 450, 'publisher': 'Martin Books', 'country': 'UK', 'release_date': '2018-09-10'}

        def mock_format_insert_response(result):
            raise Exception

        obj = InternalBooks()
        monkeypatch.setattr(InternalBooks, "format_insert_response", mock_format_insert_response)

        with pytest.raises(Exception):
            obj.insert_book(new_book)
