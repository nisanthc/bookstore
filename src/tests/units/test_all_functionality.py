import pytest
import json


from routes import app as app1
from config.db_settings import databases
from utils.db_manager import DBManager


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


headers = {'Accept': 'application/json', 'Content-Type': 'application/json'}


class TestExtController(object):

    def test_get_method_by_name(self, app):

        response = app.get('/api/external-books/?name=The Hedge Knight', headers=headers)

        assert response.status_code == 200

    def test_get_method_by_no_name(self, app):

        response = app.get('/api/external-books/', headers=headers)

        assert response.status_code == 200


class TestIntController(object):

    def test_get_method_by_name(self, app, setup_database_data):

        response = app.get('/api/v1/books/?name=Jungle book', headers=headers)
        expected = {
                    "status_code": 200,
                    "status": "success",
                    "data": [{
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
                    }]
                }
        assert response.status_code == 200
        assert json.loads(response.data) == expected

    def test_get_method_by_id(self, app, setup_database_data):

        response = app.get('/api/v1/books/10', headers=headers)
        expected = {
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
        assert response.status_code == 200
        assert json.loads(response.data) == expected

    def test_get_method_by_publisher(self, app, setup_database_data):

        response = app.get('/api/v1/books/?publisher=No Books', headers=headers)
        expected = {
                    "status_code": 200,
                    "status": "success",
                    "data": [{
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
                    }]
                }
        assert response.status_code == 200
        assert json.loads(response.data) == expected

    def test_get_method_by_country(self, app, setup_database_data):

        response = app.get('/api/v1/books/?country=UK States', headers=headers)
        expected = {
                    "status_code": 200,
                    "status": "success",
                    "data": [{
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
                    }]
                }
        assert response.status_code == 200
        assert json.loads(response.data) == expected

    def test_get_method_by_release_date(self, app, setup_database_data):

        response = app.get('/api/v1/books/?release data=2019-01-20', headers=headers)
        expected = {
                    "status_code": 200,
                    "status": "success",
                    "data": [{
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
                    }]
                }
        assert response.status_code == 200
        assert json.loads(response.data) == expected

    def test_post_method(self, app, setup_database_data):

        new_book = {
                    "name": "Game of thorns",
                    "isbn" : "978-0553103540",
                    "authors": ["Mukund", "Sherk"],
                    "number_of_pages": 450,
                    "publisher": "Martin Books",
                    "country": "UK",
                    "release_date": "2018-09-10"
                    }
        data = json.dumps(new_book)

        response = app.post('/api/v1/books/', headers=headers, data=data)

        expected = {
                    "status_code": 201,
                    "status": "success",
                    "data": [
                        {
                            "book": {
                                "name": "Game of thorns",
                                "isbn": "978-0553103540",
                                "number_of_pages": 450,
                                "publisher": "Martin Books",
                                "country": "UK",
                                "release_date": "2018-09-10",
                                "authors": [
                                    "Mukund",
                                    "Sherk"
                                        ]
                                    }
                                }
                            ]
                        }
        assert response.status_code == 200
        assert json.loads(response.data) == expected

    def test_patch_method(self, app, setup_database_data):

        patch_data = {
                    "name": "Davinci code",
                    "authors": ["Leo","Tata","Ratan"],
                    "publisher": "Code Books",
                    "country": "UK States",
                    "isbn" : "123-456575",
                    "number_of_pages" : 700,
                    "release_date": "2019-01-20"
                }

        expected = {
                    "status_code": 200,
                    "status": "success",
                    "message": "The book Davinci code was updated successfully",
                    "data": {
                        "id": 10,
                        "name": "Davinci code",
                        "isbn": "123-456575",
                        "number_of_pages": 700,
                        "publisher": "Code Books",
                        "country": "UK States",
                        "release_date": "2019-01-20",
                        "authors": [
                            "Leo",
                            "Tata",
                            "Ratan"
                        ]
                    }
                }

        data = json.dumps(patch_data)
        response = app.patch('/api/v1/books/10', headers=headers, data=data)
        assert response.status_code == 200
        assert json.loads(response.data) == expected

    def test_delete_method(self, app, setup_database_data):

        expected = {
                    "status_code": 200,
                    "status": "success",
                    "message": "The book Jungle book was deleted successfully",
                    "data": []
                }
        response = app.delete('/api/v1/books/10', headers=headers)
        assert response.status_code == 200
        assert json.loads(response.data) == expected

    def test_patch_method_with_400(self, app, setup_database_data):

        patch_data = {
                    "name": "Davinci code",
                    "authors": ["Leo","Tata","Ratan"],
                    "publisher": "Code Books",
                    "country": "UK States",
                    "isbn" : "123-456575",
                    "number_of_pages" : 700,
                    "release_date": "2019-01-20"
                }

        data = json.dumps(patch_data)
        response = app.patch('/api/v1/books/', headers=headers, data=data)
        assert response.status_code == 400

    def test_delete_method_with_404(self, app, setup_database_data):

        response = app.delete('/api/v1/books/', headers=headers)
        assert response.status_code == 400

    def test_patch_method_with_400(self, app, setup_database_data):

        patch_data = {
                    "name": "Davinci code",
                    "authors": ["Leo","Tata","Ratan"],
                    "publisher": "Code Books",
                    "country": "UK States",
                    "isbn" : "123-456575",
                    "number_of_pages" : 700,
                    "release_date": "2019-01-20"
                }

        data = json.dumps(patch_data)
        response = app.patch('/api/v1/books/99999', headers=headers, data=data)
        assert response.status_code == 404

    def test_delete_method_with_404(self, app, setup_database_data):

        response = app.delete('/api/v1/books/9999999', headers=headers)
        assert response.status_code == 404

    def test_patch_method_with_unsupported_contenttype(self, app, setup_database_data):

        patch_data = {
                    "name": "Davinci code",
                    "authors": ["Leo","Tata","Ratan"],
                    "publisher": "Code Books",
                    "country": "UK States",
                    "isbn" : "123-456575",
                    "number_of_pages" : 700,
                    "release_date": "2019-01-20"
                }

        expected = {
                    "status_code": 200,
                    "status": "success",
                    "message": "The book Davinci code was updated successfully",
                    "data": {
                        "id": 10,
                        "name": "Davinci code",
                        "isbn": "123-456575",
                        "number_of_pages": 700,
                        "publisher": "Code Books",
                        "country": "UK States",
                        "release_date": "2019-01-20",
                        "authors": [
                            "Leo",
                            "Tata",
                            "Ratan"
                        ]
                    }
                }

        headers['Content-Type'] = "text/plain"
        data = json.dumps(patch_data)
        response = app.patch('/api/v1/books/99999', headers=headers, data=data)
        assert response.status_code == 400

    def test_post_method_with_unsupported_contenttype(self, app, setup_database_data):

        new_book = {
            "name": "Game of thorns",
            "isbn": "978-0553103540",
            "authors": ["Mukund", "Sherk"],
            "number_of_pages": 450,
            "publisher": "Martin Books",
            "country": "UK",
            "release_date": "2018-09-10"
        }
        data = json.dumps(new_book)

        headers['Content-Type'] = "text/plain"
        response = app.post('/api/v1/books/', headers=headers, data=data)
        assert response.status_code == 400


