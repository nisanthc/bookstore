from flask import Flask
from flask_restful import Api
import logging.config

from books.views.controller import ExternalBooksController
from books.views.controller import InternalBooksController

from config.logger_setting import DICT_CONFIG
logging.config.dictConfig(DICT_CONFIG)

app = Flask(__name__)
api = Api(app)

api.add_resource(ExternalBooksController, '/api/external-books/')
api.add_resource(InternalBooksController, '/api/v1/books/','/api/v1/books/<id>' )

if __name__ == '__main__':
    app.run(port=8080)
