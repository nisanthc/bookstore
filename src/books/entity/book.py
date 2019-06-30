
class Book(object):

    def __init__(self, book_dict):

        self._name = book_dict.get("name", None)
        self._authors = book_dict.get("authors", None)
        self._isbn = book_dict.get("isbn", None)
        self._number_of_pages = book_dict.get("number_of_pages", None)
        self._publisher = book_dict.get("publisher", None)
        self._country = book_dict.get("country", None)
        self._release_date = book_dict.get("release_date", None)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, val):
        self._name = val

    @property
    def authors(self):
        return self._authors

    @authors.setter
    def authors(self, val):
        self._author = val

    @property
    def isbn(self):
        return self._isbn

    @isbn.setter
    def isbn(self, val):
        self._isbn = val

    @property
    def number_of_pages(self):
        return self._number_of_pages

    @number_of_pages.setter
    def number_of_pages(self, val):
        self._number_of_pages = val

    @property
    def publisher(self):
        return self._publisher

    @publisher.setter
    def publisher(self, val):
        self._publisher = val

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, val):
        self._country = val

    @property
    def release_date(self):
        return self._release_date

    @release_date.setter
    def release_date(self, val):
        self._release_date = val
