import logging
from utils.db_manager import DBManager
from utils.custom_exception import ResourceNotAvailable
from config.db_settings import databases

from books.entity.book import Book
from books.model.dao import BooksDAO

logger = logging.getLogger(__name__)


class InternalBooks(object):
    """
        This is the class for manager Internal book store
    """

    def __init__(self):

        self.db_obj = DBManager(databases['books'])
        self.dao_obj = BooksDAO(self.db_obj)

    def __get_books_by_filter(self, key, value):
        """
        :param book_id:
        :return:
        """
        search_func = {
            "all" : self.dao_obj.get_all_books,
            "id" : self.dao_obj.get_books_by_id,
            "name" : self.dao_obj.get_books_by_name,
            "publisher": self.dao_obj.get_books_by_publisher,
            "country": self.dao_obj.get_books_by_country,
            "release date": self.dao_obj.get_books_by_release_date,
        }

        result = search_func[key](value)

        for row in result:

            res_author = self.dao_obj.get_author_by_book_id(row['id'])
            author_list = [val['name'] for val in res_author]
            row.update({"authors": author_list})
            row["release_date"] = str(row["release_date"])

        return result

    @staticmethod
    def format_get_response(book_info):
        """
        :param book_info:
        :return:
        """
        response = {"status_code": 200,
                    "status": "success",
                    "data": []}
        if book_info:
            response.update({"data": book_info})

        return response

    def get_books(self, key, value):
        """
        :param key:
        :param value:
        :return:
        """
        try:
            logger.info("Entering get_books")
            result = self.__get_books_by_filter(key, value)
            if result and key == "id":
                result = result[0]
            logger.info("Exiting get_books")
            return self.format_get_response(result)

        except Exception as err:
            logger.exception(err)
            raise
        finally:
            self.db_obj.close()

    @staticmethod
    def format_insert_response( book_info):
        """
        :return:
        """
        response = {"status_code": 201,
                    "status": "success",
                    "data": []}

        book_info.pop("id")
        response["data"].append({"book": book_info})
        return response

    def __link_author_book(self, book_id, author_list):
        """
        :param book_id:
        :param author_list:
        :return:
        """

        for row in author_list:

            res_author = self.dao_obj.get_author(row)

            if res_author:
                author_id = res_author["author_id"]
            else:
                author_id = self.dao_obj.insert_into_author(row)

            self.dao_obj.insert_into_author_book(author_id, book_id)

    def insert_book(self, new_book):
        """
        This method used to insert new book
        :return:
        """
        try:
            logger.info("Entering insert_book")

            book_info = self.__get_books_by_filter("name", new_book["name"])

            if book_info:
                return self.format_insert_response(book_info[0])

            book_entity_obj = Book(new_book)
            book_id = self.dao_obj.insert_into_book(book_entity_obj)

            self.__link_author_book(book_id, book_entity_obj.authors)

            book_info = self.__get_books_by_filter("id", book_id)
            response = self.format_insert_response(book_info[0])

            self.db_obj.commit()

            logger.info("Exiting insert_book")
            return response

        except Exception as err:
            logger.exception(err)
            self.db_obj.rollback()
            raise
        finally:
            self.db_obj.close()

    @staticmethod
    def format_update_reponse(book_info):
        """
        :param book_info:
        :return:
        """
        response = {
            "status_code": 200,
            "status": "success",
            "message": "The book {} was updated successfully".format(book_info["name"])}

        response.update({"data":book_info})

        return response

    def patch_book(self, book_id, patch_book):
        """

        :return:
        """
        try:

            logger.info("Entering patch_book")
            book_info = self.__get_books_by_filter("id", book_id)
            if not book_info:
                raise ResourceNotAvailable("Given resource {} is not available".format(book_id))

            book_entity = Book(book_info[0])
            author_to_update = False
            for key, value in patch_book.items():
                setattr(book_entity, key, value)
                if key == "authors":
                    author_to_update = True

            self.dao_obj.update_into_book(book_id, book_entity )

            if author_to_update:
                self.dao_obj.delete_author_book(book_id)
                self.__link_author_book(book_id, patch_book["authors"])

            book_info = self.__get_books_by_filter("id", book_id)
            response = self.format_update_reponse(book_info[0])

            self.db_obj.commit()
            logger.info("Exiting patch_book")
            return response

        except Exception as err:
            self.db_obj.rollback()
            logger.exception(err)
            raise
        finally:
            self.db_obj.close()

    @staticmethod
    def format_delete_reponse(book_name):
        """
        :param book_name:
        :return:
        """

        response = {
                    "status_code": 200,
                    "status": "success",
                    "message": "The book {} was deleted successfully".format(book_name),
                    "data": []
                }
        return response

    def delete_book(self, book_id):
        """
        :param book_id:
        :return:
        """
        try:

            logger.info("Entering delete_book")
            book_info = self.__get_books_by_filter("id", book_id)
            if not book_info:
                raise ResourceNotAvailable("Given resource {} is not available".format(book_id))

            self.dao_obj.delete_author_book(book_id)
            self.dao_obj.delete_from_book(book_id)

            response = self.format_delete_reponse(book_info[0]["name"])

            self.db_obj.commit()
            logger.info("Exiting delete_book")
            return response

        except Exception as err:
            self.db_obj.rollback()
            logger.exception(err)
            raise
        finally:
            self.db_obj.close()

