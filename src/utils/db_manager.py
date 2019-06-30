from mysql import connector
import mysql.connector


class DBManager(object):
    """
        This DBManager class is the wrapper for mysql.connector

    """

    def __init__(self, config_dict):
        """
        Intialize the connection variables
        :param config_dict:
        """

        self.host = config_dict['host']
        self.user = config_dict['username']
        self.password = config_dict['password']
        self.database = config_dict['database']
        self.port = config_dict["port"]
        self.connect = None
        self.cursor = None
        self.__get_connection()

    def __get_connection(self):
        """
        Get the Mysql DB connections
        :return:
        """
        self.connect = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port
        )

    def __get_cursor(self):
        """
        Get Cursor
        :return:
        """
        self.cursor = self.connect.cursor(dictionary=True)

    def processquery(self, query, args=None, count=0, fetch=False):
        """
        This method is used to execute the query
        :param query:
        :param args:
        :param fetch:
        :return:
        """
        self.__get_cursor()

        self.cursor.execute(query, args)

        if fetch:
            if count == 1:
                result = self.cursor.fetchone()
            else:
                result = self.cursor.fetchall()
        else:
            result = self.cursor.lastrowid

        return result

    def commit(self):
        """
        Commit the transaction
        :return:
        """
        if self.connect:
            self.connect.commit()

    def rollback(self):
        """
        Rollback the transaction
        :return:
        """
        if self.connect:
            self.connect.rollback()

    def close(self):
        """
        Close the cursor and connection
        :return:
        """
        if self.cursor:
            self.cursor.close()
        if self.connect:
            self.connect.close()