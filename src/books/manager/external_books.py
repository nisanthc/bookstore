import requests
import logging

from config.external_config import EXTERNAL_BOOKS_URL

logger = logging.getLogger(__name__)


class ExternalBooks(object):
    """
    This is a class for managing external books
    """

    @staticmethod
    def filter_format(res_dict, name):
        """
        This is a static method for filtering and formating the response
        :param res_dict:
        :param name:
        :return: data
        """

        data = []
        for row in res_dict:
            if row['name'] == name or not name:
                temp_dict = {
                    "name": row['name'],
                    "isbn": row['isbn'],
                    "authors": row['authors'],
                    "number_of_pages": row['numberOfPages'],
                    "publisher": row['publisher'],
                    "country": row['country'],
                    "release_date": row['released'],
                }

                data.append(temp_dict)
        return data

    def get_books_by_name(self, book_name):
        """
        This is the method for calling external API and filter the response by name
        :param name:
        :return: response_dict
        """
        try:
            logger.info("Entering get_books_by_name")

            pagesize = 50
            page_no = 1
            data = []

            while True:

                param = "?page={}&pageSize={}".format(page_no, pagesize)
                response = requests.get(EXTERNAL_BOOKS_URL + param)

                if response.status_code == 200:

                    res_dict = response.json()
                    filter_response = self.filter_format(res_dict, book_name)
                    if filter_response:
                        data.extend(filter_response)

                page_no += 1

                if len(res_dict) < pagesize:
                    break

            res = {'status_code': 200,
                   'status': 'success',
                   'data': data}

            logger.info("Exiting get_books_by_name")
            return res

        except Exception as err:
            logger.exception(err)
            raise

