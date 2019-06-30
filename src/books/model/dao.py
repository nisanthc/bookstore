from datetime import datetime

class BooksDAO(object):

    def __init__(self, db_obj):
        self.db_obj = db_obj

    def get_all_books(self, all= None):

        query = "select book_id as id,name,isbn,number_of_pages,publisher,country,release_date \
                        from book"
        result = self.db_obj.processquery(query, fetch=True)
        return result

    def get_books_by_id(self, book_id):

        query = "select book_id as id,name,isbn,number_of_pages,publisher,country,release_date \
                        from book where book_id = %s"
        args = (book_id,)
        result = self.db_obj.processquery(query, args, fetch=True)
        return result

    def get_books_by_name(self, name):

        query = "select book_id as id,name,isbn,number_of_pages,publisher,country,release_date \
                        from book where name = %s"
        args = (name, )
        result = self.db_obj.processquery(query, args, fetch=True)
        return result

    def get_books_by_publisher(self, publisher):

        query = "select book_id as id,name,isbn,number_of_pages,publisher,country,release_date \
                        from book where publisher = %s"
        args = (publisher, )
        result = self.db_obj.processquery(query, args, fetch=True)
        return result

    def get_books_by_country(self, country):

        query = "select book_id as id,name,isbn,number_of_pages,publisher,country,release_date \
                        from book where country = %s"
        args = (country, )
        result = self.db_obj.processquery(query, args, fetch=True)
        return result

    def get_books_by_release_date(self, relaase_date):

        query = "select book_id as id,name,isbn,number_of_pages,publisher,country,release_date \
                        from book where release_date = %s"
        args = (relaase_date, )
        result = self.db_obj.processquery(query, args, fetch=True)
        return result

    def get_author(self, author_name):

        query = "select * from author where name = %s"
        args = (author_name, )
        result = self.db_obj.processquery(query, args, count=1, fetch=True)
        return result

    def get_author_by_book_id(self, book_id):

        query = "select name from author a join author_book b using(author_id) \
                    where book_id=%s"
        args = (book_id,)
        result = self.db_obj.processquery(query, args, fetch=True)
        return result

    def insert_into_book(self, book_entity):
        """
        """

        query = "insert into book " \
                "(name, isbn, number_of_pages, publisher, country, release_date, \
                    created_datetime) " \
                "values (%s, %s, %s, %s, %s, %s, %s)"
        args = (book_entity.name, book_entity.isbn, book_entity.number_of_pages,
                book_entity.publisher, book_entity.country, book_entity.release_date,
                datetime.now())
        book_id = self.db_obj.processquery(query=query, args=args)

        return book_id

    def insert_into_author(self, author_name):

        query = "insert into author (name, created_datetime) " \
                "values (%s, %s)"
        args = (author_name, datetime.now())

        author_id = self.db_obj.processquery(query=query, args=args)
        return author_id

    def insert_into_author_book(self, author_id, book_id):

        query = "insert into author_book (author_id, book_id) " \
                "values (%s, %s)"
        args = (author_id, book_id)

        author_book_id = self.db_obj.processquery(query=query, args=args)
        return author_book_id

    def update_into_book(self, book_id, book_entity):

        query = "update book set name = %s, isbn = %s, \
                                number_of_pages = %s,publisher = %s,\
                                country = %s, release_date = %s, modified_datetime = %s \
                                where book_id = %s"
        args = (book_entity.name, book_entity.isbn, book_entity.number_of_pages,
                book_entity.publisher, book_entity.country, book_entity.release_date,
                 datetime.now(), book_id)

        book_id = self.db_obj.processquery(query=query, args=args)
        return book_id

    def delete_author_book(self, book_id):

        query = "delete from author_book where book_id = %s"
        args = (book_id,)
        self.db_obj.processquery(query=query, args=args)

    def delete_from_book(self, book_id):

        query = "delete from book where book_id = %s"
        args = (book_id,)
        self.db_obj.processquery(query=query, args=args)
