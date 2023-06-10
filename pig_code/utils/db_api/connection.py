import mysql.connector
from mysql.connector import pooling

from ...core import *
from .pool import pool


class Connection:

    @staticmethod
    def connect():
        # connection = mysql.connector.connect(
        #     host=config.mysql_info['host'],
        #     port=config.mysql_info['port'],
        #     user=config.mysql_info['user'],
        #     password=config.mysql_info['password'],
        #     database=config.mysql_info['database'],
        #     charset='utf8'
        # )
        # return connection
        return pool.get_connection()

    @staticmethod
    def make_request(query, params: tuple = None, commit: bool = True, fetch: bool = False, fetch_first: bool = True, fetchall=False):
        connection = Connection.connect()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, params)
                if commit:
                    connection.commit()
                if fetch:
                    if fetchall:
                        return cursor.fetchall()
                    result = cursor.fetchone()
                    if fetch_first:
                        return result[0]
                    else:
                        return result
        finally:
            connection.close()
