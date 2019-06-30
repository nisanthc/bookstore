import logging
from flask import request, abort
from flask_restful import Resource
from requests.exceptions import HTTPError
import jsonschema
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from books.manager.external_books import ExternalBooks
from books.manager.internal_books import InternalBooks
from books.validation.schema import post_schema
from books.validation.schema import get_schema
from books.validation.schema import patch_schema
from utils.custom_exception import ResourceNotAvailable

logger = logging.getLogger(__name__)


class ExternalBooksController(Resource):
    """
    This is a controller class for managing external books REST API

    """

    def get(self):
        """
        This is a GET method used to get the books by using filter name

        Request  :
                URL : /api/external-books/?name=A%20Game%20of%20Thrones
        Response : JSON
            [
                {
                "status_code": 200,
                "status": "success",
                "data": [
                    {
                        "name": "A Game of Thrones",
                        "isbn": "978-0553103540",
                        "authors": [
                            "George R. R. Martin"
                        ],
                        "number_of_pages": 694,
                        "publisher": "Bantam Books",
                        "country": "United States",
                        "release_date": "1996-08-01",
                    },
                    {
                        "name": "A Game of Thrones",
                        "isbn": "978-0553108033",
                        "authors": [
                            "George R. R. Martin"
                        ],
                        "number_of_pages": 768,
                        "publisher": "Bantam Books",
                        "country": "United States",
                        "release_date": "1999-02-02",
                    }
                }
            ]
        """

        try:
            logger.info("Entering get method")
            book_name = request.args.get('name', None)

            logger.info("Query param name is {}".format(book_name))
            ext_bk_obj = ExternalBooks()

            result = ext_bk_obj.get_books_by_name(book_name)

            logger.info("Return response :: {}".format(result))
            return result

        except HTTPError as err:
            logger.exception("External API Error : {}".format(err))
            abort(500, "External API Error")
        except Exception as err:
            logger.exception("Un-handled Error : {}".format(err))
            abort(500, "Internal Server Error")


class InternalBooksController(Resource):
    """
    This is a controller class for managing internal books REST API

    """

    def get(self, id=None):
        """
        This is the GET method used to get
            1) All books details or
            2) Particular book details

        Request :
            URL : POST http://localhost:8080/api/v1/books

        Response:
                {
                    "status_code": 200,
                    "status": "success",
                    "data": [
                        {
                            "id": 6,
                            "name": "My First Book",
                            "isbn": null,
                            "number_of_pages": 350,
                            "publisher": "Acme Books",
                            "country": "United States",
                            "release_date": "2019-11-23",
                            "authors": [
                                "John Doe"
                            ]
                        },
                        {
                            "id": 9,
                            "name": "My First Book2",
                            "isbn": null,
                            "number_of_pages": 350,
                            "publisher": "Acme Books",
                            "country": "United States",
                            "release_date": "2019-11-23",
                            "authors": [
                                "John Doe",
                                "Martin"
                            ]
                        }
                    ]
                }
        """

        try:
            logger.info("Entering get method")
            if id:
                key = "id"
                value = id
            else:
                value = None
                for query in get_schema:
                    value = request.args.get(query, None)
                    if value:
                        key = query
                        break
                else:
                    key = "all"

            logger.info("Query param name is {} {}".format(key, value))
            int_bk_obj = InternalBooks()

            result = int_bk_obj.get_books(key, value)

            logger.info("Return response :: {}".format(result))
            return result

        except ValueError as err:
            logger.exception("Value Error : {}".format(err))
            abort(400, "Query param: name is missing")

        except Exception as err:
            logger.exception("Un-handled Error : {}".format(err))
            abort(500, "Internal Server Error")

    def post(self):
        """
        This is the POST method used to insert new book
        Request:
            URL : POST http://localhost:8080/api/v1/books
            Param Data :
                  "book":
                   {
                        "name": "My First Book",
                        "isbn": "123-3213243567",
                        "authors": [
                            "John Doe"
                        ],
                        "number_of_pages": 350,
                        "publisher": "Acme Books",
                        "country": "United States",
                        "release_date": "2019-08-01",
                   }

        Response:
            [
                "status_code": 201,
                "status": "success",
                "data": [
                    "book": {
                        "name": "My First Book",
                        "isbn": "123-3213243567",
                        "authors": [
                            "John Doe"
                        ],
                        "number_of_pages": 350,
                        "publisher": "Acme Books",
                        "country": "United States",
                        "release_date": "2019-08-01",
                    },
                ]
             ]

        """
        try:
            logger.info("Entering InternalBooksController POST method")
            if not request.content_type == 'application/json':
                raise ValidationError("Given content type : {} is not acceptable."
                                      " Accepted content type is application/json ".format(request.content_type))

            request_data = request.get_json()
            validate(request_data, post_schema, format_checker=jsonschema.FormatChecker())

            int_bk_obj = InternalBooks()

            result = int_bk_obj.insert_book(request_data)

            return result

            logger.info("Existing InternalBooksController POST method")
        except ValueError as err:
            logger.exception("Value Error :: {}".format(err))
            abort(400, str(err))

        except ValidationError as err:
            logger.exception("Validation Error :: {}".format(err))
            abort(400, err.message)

        except Exception as err:
            logger.exception("Un-handled Exception :: {}".format(err))
            abort(500, "Internal Server Error")

    def patch(self, id=None):
        """
        This is the UPDATE method used to Update the existing book
        Request :
                URL : http://127.0.0.1:5000/api/v1/books/9
        Response:
                {
                    "status_code": 200,
                    "status": "success",
                    "message": "The book My First Book was updated successfully",
                    "data": {
                        "id": 1,
                        "name": "My First Updated Book",
                        "isbn": "123-3213243567",
                        "authors": [
                            "John Doe"
                        ],
                        "number_of_pages": 350,
                        "publisher": "Acme Books Publishing",
                        "country": "United States",
                        "release_date": "2019-01-01"
                    }
                }
        """
        try:
            logger.info("Entering InternalBooksController PATCH method")

            if not request.content_type == 'application/json':
                raise ValidationError("Given content type : {} is not acceptable."
                                      " Accepted content type is application/json ".format(request.content_type))

            if not id:
                raise ValidationError("Resource id is not given")

            request_data = request.get_json()
            validate(request_data, patch_schema, format_checker=jsonschema.FormatChecker())

            int_bk_obj = InternalBooks()

            result = int_bk_obj.patch_book(id, request_data)

            return result

            logger.info("Existing InternalBooksController PATCH method")
        except ValueError as err:
            logger.exception("Value Error :: {}".format(err))
            abort(400, str(err))

        except ValidationError as err:
            logger.exception("Validation Error :: {}".format(err))
            abort(400, err.message)

        except ResourceNotAvailable as err:
            logger.exception("Resource Not Exists :: {}".format(err))
            abort(404, err.args[0])

        except Exception as err:
            logger.exception("Un-handled Exception :: {}".format(err))
            abort(500, "Internal Server Error")

    def delete(self, id=None):

        try:
            logger.info("Entering InternalBooksController DELETE method")

            if not id:
                raise ValidationError("Resource id is not given")

            int_bk_obj = InternalBooks()

            result = int_bk_obj.delete_book(id)

            return result

            logger.info("Existing InternalBooksController DELETE method")

        except ValueError as err:
            logger.exception("Value Error :: {}".format(err))
            abort(400, str(err))

        except ValidationError as err:
            logger.exception("Validation Error :: {}".format(err))
            abort(400, err.message)

        except ResourceNotAvailable as err:
            logger.exception("Resource Not Exists :: {}".format(err))
            abort(404, err.args[0])

        except Exception as err:
            logger.exception("Un-handled Exception :: {}".format(err))
            abort(500, "Internal Server Error")
