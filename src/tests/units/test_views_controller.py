import pytest
import json

from _pytest.monkeypatch import MonkeyPatch
from requests.exceptions import HTTPError
from utils.custom_exception import ResourceNotAvailable

from routes import app as app1
from books.manager.external_books import ExternalBooks
from books.manager.internal_books import InternalBooks


@pytest.fixture(scope="session")
def app(request):
    """Session-wide test `Flask` application."""

    app = app1.test_client()

    # Establish an application context before running the tests.
    ctx = app1.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}


class TestExternalController(object):

    def test_get_method_valid(self, app):
        monkeypatch = MonkeyPatch()

        def mock_get_books_by_name(name, param):
            mocked_response = {
                "status_code": 200,
                "status": "success",
                "data": {
                    "id": 10,
                    "name": "Jungle book",
                    "isbn": "123456",
                    "number_of_pages": 400,
                    "publisher": "No Books",
                    "country": "UK States",
                    "release_date": "2019-01-20",
                    "authors": [
                        "John Doe",
                        "Martin",
                        "Jeo",
                        "kelin"
                    ]
                }
            }
            return mocked_response

        monkeypatch.setattr(ExternalBooks, "get_books_by_name", mock_get_books_by_name)

        response = app.get('/api/external-books/?name=games', headers=headers)

        assert response.status_code == 200

    def test_get_with_no_name(self, app):
        monkeypatch = MonkeyPatch()

        def mock_get_books_by_name(name, param):
            mocked_response = {
                "status_code": 200,
                "status": "success",
                "data": {
                    "id": 10,
                    "name": "Jungle book",
                    "isbn": "123456",
                    "number_of_pages": 400,
                    "publisher": "No Books",
                    "country": "UK States",
                    "release_date": "2019-01-20",
                    "authors": [
                        "John Doe",
                        "Martin",
                        "Jeo",
                        "kelin"
                    ]
                }
            }
            return mocked_response

        response = app.get('/api/external-books/', headers=headers)

        monkeypatch.setattr(ExternalBooks, "get_books_by_name", mock_get_books_by_name)

        assert response.status_code == 200

    def test_get_method_with_exceptions(self, app):
        monkeypatch = MonkeyPatch()

        def mock_get_books_by_name(name, param):
            raise Exception

        monkeypatch.setattr(ExternalBooks, "get_books_by_name", mock_get_books_by_name)

        response = app.get('/api/external-books/?name=games', headers=headers)

        assert response.status_code == 500

    def test_get_method_with_http_exceptions(self, app):
        monkeypatch = MonkeyPatch()

        def mock_get_books_by_name(name, param):
            raise HTTPError

        monkeypatch.setattr(ExternalBooks, "get_books_by_name", mock_get_books_by_name)

        response = app.get('/api/external-books/?name=games', headers=headers)

        assert response.status_code == 500


class TestInternalBooksController():

    def test_get_method_by_id(self, app):
        monkeypatch = MonkeyPatch()

        def mock_get_books(key, value, param):
            return

        monkeypatch.setattr(InternalBooks, "get_books", mock_get_books)

        response = app.get("/api/v1/books/1", headers=headers)

        assert response.status_code == 200

    def test_get_method_by_all(self, app):
        monkeypatch = MonkeyPatch()

        def mock_get_books(key, value, param):
            return

        monkeypatch.setattr(InternalBooks, "get_books", mock_get_books)

        response = app.get("/api/v1/books/", headers=headers)

        assert response.status_code == 200

    def test_get_method_by_name(self, app):
        monkeypatch = MonkeyPatch()

        def mock_get_books(key, value, param):
            return

        monkeypatch.setattr(InternalBooks, "get_books", mock_get_books)

        response = app.get("/api/v1/books/?,name=game", headers=headers)

        assert response.status_code == 200

    def test_get_method_with_no_name(self, app):
        monkeypatch = MonkeyPatch()

        def mock_get_books(key, value, param):
            raise ValueError

        monkeypatch.setattr(InternalBooks, "get_books", mock_get_books)

        response = app.get("/api/v1/books/?,name=game", headers=headers)

        assert response.status_code == 400

    def test_get_method_with_exceptions(self, app):
        monkeypatch = MonkeyPatch()

        def mock_get_books(key, value, param):
            raise Exception

        monkeypatch.setattr(InternalBooks, "get_books", mock_get_books)

        response = app.get("/api/v1/books/?,name=game", headers=headers)

        assert response.status_code == 500

    def test_post_method_sucess(self, app):
        monkeypatch = MonkeyPatch()

        def mock_insert_book(data, param):
            return

        monkeypatch.setattr(InternalBooks, "insert_book", mock_insert_book)

        data = {
            "name": "My First Book2",
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-11-23"
        }
        response = app.post("/api/v1/books/", headers=headers, data=json.dumps(data))

        assert response.status_code == 200

    def test_post_method_no_bookname(self, app):
        monkeypatch = MonkeyPatch()

        def mock_insert_book(data, param):
            return

        monkeypatch.setattr(InternalBooks, "insert_book", mock_insert_book)

        data = {
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-11-23"
        }
        response = app.post("/api/v1/books/", headers=headers, data=json.dumps(data))

        assert response.status_code == 400

    def test_post_method_with_incorrect_date(self, app):
        monkeypatch = MonkeyPatch()

        def mock_insert_book(data, param):
            return

        monkeypatch.setattr(InternalBooks, "insert_book", mock_insert_book)

        data = {
            "name": "book name 1",
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "201923"
        }
        response = app.post("/api/v1/books/", headers=headers, data=json.dumps(data))

        assert response.status_code == 400

    def test_post_method_with_value_error(self, app):
        monkeypatch = MonkeyPatch()

        def mock_insert_book(data, param):
            raise ValueError

        monkeypatch.setattr(InternalBooks, "insert_book", mock_insert_book)

        data = {
            "name": "book name 1",
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-10-23"
        }
        response = app.post("/api/v1/books/", headers=headers, data=json.dumps(data))

        assert response.status_code == 400

    def test_post_method_with_exception(self, app):
        monkeypatch = MonkeyPatch()

        def mock_insert_book(data, param):
            raise Exception

        monkeypatch.setattr(InternalBooks, "insert_book", mock_insert_book)

        data = {
            "name": "book name 1",
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-10-23"
        }
        response = app.post("/api/v1/books/", headers=headers, data=json.dumps(data))

        assert response.status_code == 500

    def test_patch_method_sucess(self, app):
        monkeypatch = MonkeyPatch()

        def mock_patch_book(book_id, data, param):
            return

        monkeypatch.setattr(InternalBooks, "patch_book", mock_patch_book)

        data = {
            "name": "My First Book2",
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-11-23"
        }
        response = app.patch("/api/v1/books/10", headers=headers, data=json.dumps(data))

        assert response.status_code == 200

    def test_post_method_no_bookname(self, app):
        monkeypatch = MonkeyPatch()

        def mock_patch_book(book_id, data, param):
            return

        monkeypatch.setattr(InternalBooks, "patch_book", mock_patch_book)

        data = {
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-11-23"
        }
        response = app.patch("/api/v1/books/10", headers=headers, data=json.dumps(data))

        assert response.status_code == 200

    def test_post_method_with_incorrect_date(self, app):
        monkeypatch = MonkeyPatch()

        def mock_patch_book(book_id, data, param):
            return

        monkeypatch.setattr(InternalBooks, "patch_book", mock_patch_book)

        data = {
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-23"
        }
        response = app.patch("/api/v1/books/10", headers=headers, data=json.dumps(data))

        assert response.status_code == 400

    def test_patch_method_with_no_resource_id(self, app):
        monkeypatch = MonkeyPatch()

        def mock_patch_book(book_id, data, param):
            return

        monkeypatch.setattr(InternalBooks, "patch_book", mock_patch_book)

        data = {
            "name": "book name 1",
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "201923"
        }
        response = app.patch("/api/v1/books/", headers=headers, data=json.dumps(data))

        assert response.status_code == 400

    def test_post_method_with_value_error(self, app):
        monkeypatch = MonkeyPatch()

        def mock_patch_book(book_id, data, param):
            raise ValueError

        monkeypatch.setattr(InternalBooks, "patch_book", mock_patch_book)

        data = {
            "name": "book name 1",
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-10-23"
        }
        response = app.patch("/api/v1/books/10", headers=headers, data=json.dumps(data))

        assert response.status_code == 400

    def test_post_method_with_exception(self, app):
        monkeypatch = MonkeyPatch()

        def mock_patch_book(book_id, data, param):
            raise Exception

        monkeypatch.setattr(InternalBooks, "patch_book", mock_patch_book)

        data = {
            "name": "book name 1",
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-10-23"
        }
        response = app.patch("/api/v1/books/10", headers=headers, data=json.dumps(data))

        assert response.status_code == 500

    def test_post_method_sucess(self, app):
        monkeypatch = MonkeyPatch()

        def mock_insert_book(data, param):
            return

        monkeypatch.setattr(InternalBooks, "insert_book", mock_insert_book)

        data = {
            "name": "My First Book2",
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-11-23"
        }
        response = app.post("/api/v1/books/", headers=headers, data=json.dumps(data))

        assert response.status_code == 200

    def test_post_method_no_bookname(self, app):
        monkeypatch = MonkeyPatch()

        def mock_insert_book(data, param):
            return

        monkeypatch.setattr(InternalBooks, "insert_book", mock_insert_book)

        data = {
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-11-23"
        }
        response = app.post("/api/v1/books/", headers=headers, data=json.dumps(data))

        assert response.status_code == 400

    def test_post_method_with_incorrect_date(self, app):
        monkeypatch = MonkeyPatch()

        def mock_insert_book(data, param):
            return

        monkeypatch.setattr(InternalBooks, "insert_book", mock_insert_book)

        data = {
            "name": "book name 1",
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "201923"
        }
        response = app.post("/api/v1/books/", headers=headers, data=json.dumps(data))

        assert response.status_code == 400

    def test_post_method_with_value_error(self, app):
        monkeypatch = MonkeyPatch()

        def mock_insert_book(data, param):
            raise ValueError

        monkeypatch.setattr(InternalBooks, "insert_book", mock_insert_book)

        data = {
            "name": "book name 1",
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-10-23"
        }
        response = app.post("/api/v1/books/", headers=headers, data=json.dumps(data))

        assert response.status_code == 400

    def test_post_method_with_exception(self, app):
        monkeypatch = MonkeyPatch()

        def mock_insert_book(data, param):
            raise Exception

        monkeypatch.setattr(InternalBooks, "insert_book", mock_insert_book)

        data = {
            "name": "book name 1",
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-10-23"
        }
        response = app.post("/api/v1/books/", headers=headers, data=json.dumps(data))

        assert response.status_code == 500

    def test_patch_method_sucess(self, app):
        monkeypatch = MonkeyPatch()

        def mock_patch_book(book_id, data, param):
            return

        monkeypatch.setattr(InternalBooks, "patch_book", mock_patch_book)

        data = {
            "name": "My First Book2",
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-11-23"
        }
        response = app.patch("/api/v1/books/10", headers=headers, data=json.dumps(data))

        assert response.status_code == 200

    def test_patch_method_no_bookname(self, app):
        monkeypatch = MonkeyPatch()

        def mock_patch_book(book_id, data, param):
            return

        monkeypatch.setattr(InternalBooks, "patch_book", mock_patch_book)

        data = {
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-11-23"
        }
        response = app.patch("/api/v1/books/10", headers=headers, data=json.dumps(data))

        assert response.status_code == 200

    def test_patch_method_with_incorrect_date(self, app):
        monkeypatch = MonkeyPatch()

        def mock_patch_book(book_id, data, param):
            return

        monkeypatch.setattr(InternalBooks, "patch_book", mock_patch_book)

        data = {
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-23"
        }
        response = app.patch("/api/v1/books/10", headers=headers, data=json.dumps(data))

        assert response.status_code == 400

    def test_patch_method_with_no_resource_id(self, app):
        monkeypatch = MonkeyPatch()

        def mock_patch_book(book_id, data, param):
            return

        monkeypatch.setattr(InternalBooks, "patch_book", mock_patch_book)

        data = {
            "name": "book name 1",
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "201923"
        }
        response = app.patch("/api/v1/books/", headers=headers, data=json.dumps(data))

        assert response.status_code == 400

    def test_patch_method_with_value_error(self, app):
        monkeypatch = MonkeyPatch()

        def mock_patch_book(book_id, data, param):
            raise ValueError

        monkeypatch.setattr(InternalBooks, "patch_book", mock_patch_book)

        data = {
            "name": "book name 1",
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-10-23"
        }
        response = app.patch("/api/v1/books/10", headers=headers, data=json.dumps(data))

        assert response.status_code == 400

    def test_patch_method_with_exception(self, app):
        monkeypatch = MonkeyPatch()

        def mock_patch_book(book_id, data, param):
            raise Exception

        monkeypatch.setattr(InternalBooks, "patch_book", mock_patch_book)

        data = {
            "name": "book name 1",
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-10-23"
        }
        response = app.patch("/api/v1/books/10", headers=headers, data=json.dumps(data))

        assert response.status_code == 500

    def test_patch_method_with_resource_not_available(self, app):
        monkeypatch = MonkeyPatch()

        def mock_patch_book(book_id, data, param):
            raise ResourceNotAvailable("Given resource 10000 is not available")

        monkeypatch.setattr(InternalBooks, "patch_book", mock_patch_book)

        data = {
            "name": "book name 1",
            "isbn": "999-234343535",
            "authors": ["John Doe", "Martin"],
            "number_of_pages": 350,
            "publisher": "Acme Books",
            "country": "United States",
            "release_date": "2019-10-23"
        }
        response = app.patch("/api/v1/books/10000", headers=headers, data=json.dumps(data))

        assert response.status_code == 404

    def test_delete_method_sucess(self, app):
        monkeypatch = MonkeyPatch()

        def mock_delete_book(book_id, param):
            return

        monkeypatch.setattr(InternalBooks, "delete_book", mock_delete_book)

        response = app.delete("/api/v1/books/10", headers=headers)

        assert response.status_code == 200

    def test_delete_method_with_no_resource_id(self, app):
        monkeypatch = MonkeyPatch()

        def mock_delete_book(book_id, param):
            return

        monkeypatch.setattr(InternalBooks, "delete_book", mock_delete_book)

        response = app.delete("/api/v1/books/", headers=headers)

        assert response.status_code == 400

    def test_delete_method_with_value_error(self, app):
        monkeypatch = MonkeyPatch()

        def mock_delete_book(book_id, para):
            raise ValueError

        monkeypatch.setattr(InternalBooks, "delete_book", mock_delete_book)

        response = app.delete("/api/v1/books/10", headers=headers)

        assert response.status_code == 400

    def test_delete_method_with_exception(self, app):
        monkeypatch = MonkeyPatch()

        def mock_delete_book(book_id, param):
            raise Exception

        monkeypatch.setattr(InternalBooks, "delete_book", mock_delete_book)

        response = app.delete("/api/v1/books/10", headers=headers)

        assert response.status_code == 500

    def test_delete_method_with_exception(self, app):
        monkeypatch = MonkeyPatch()

        def mock_delete_book(book_id, param):
            raise Exception

        monkeypatch.setattr(InternalBooks, "delete_book", mock_delete_book)

        response = app.delete("/api/v1/books/10", headers=headers)

        assert response.status_code == 500

    def test_delete_method_with_resource_not_available(self, app):
        monkeypatch = MonkeyPatch()

        def mock_delete_book(book_id, param):
            raise ResourceNotAvailable("Given resource 10000 is not available")

        monkeypatch.setattr(InternalBooks, "delete_book", mock_delete_book)

        response = app.delete("/api/v1/books/10000", headers=headers)

        assert response.status_code == 404