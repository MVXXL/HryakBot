import mysql.connector
from ...core import config


class Connection:

    @staticmethod
    def connect():
        connection = mysql.connector.connect(
            host=config.mysql_info['host'],
            port=config.mysql_info['port'],
            user=config.mysql_info['user'],
            password=config.mysql_info['password'],
            database=config.mysql_info['database'],
            charset='utf8'
        )
        return connection

    @staticmethod
    def make_request(query, commit: bool = True, fetch: bool = False):
        connection = Connection.connect()
        with connection.cursor() as cursor:
            cursor.execute(query)
            if commit:
                connection.commit()
            if fetch:
                return cursor.fetchone()[0]

# db = Connection()
# connection = db.connection
