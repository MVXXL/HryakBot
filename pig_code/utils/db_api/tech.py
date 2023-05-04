import random

import mysql.connector

from .user import *
from .connection import Connection
from ...core.config import users_schema


class Tech:

    @staticmethod
    def create_table():
        columns = [
            'id varchar(32) PRIMARY KEY UNIQUE',
            'money int DEFAULT 0',
            "pigs json",
            "inventory json",
            "language varchar(10) DEFAULT 'en'",
            'premium boolean DEFAULT FALSE',
            'blocked boolean DEFAULT FALSE',
            "block_reason varchar(1000) DEFAULT ''"
        ]
        try:
            Connection.make_request(f"CREATE TABLE {users_schema} ({columns[0]});", commit=False)
        except mysql.connector.errors.ProgrammingError:
            pass
        for column in columns[1:]:
            try:
                Connection.make_request(f"ALTER TABLE {users_schema} ADD COLUMN {column}", commit=False)
            except:
                pass

    @staticmethod
    def get_all_users():
        id_list = []
        connection = Connection.connect()
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id FROM {users_schema}")
            results = cursor.fetchall()
            for i in results:
                id_list.append(i[0])
        return id_list
# # User.register_user(1)
# print(User.is_blocked(1))
# User.set_block(1, False)
# User.set_premium(1, False)
# # Pig.create(1)
# # Pig.rename(1, 0, 'Hui')
# # Pig.add_weight(1, 0, 10)
# # Pig.rename(1, 1, 'Hui')
# # Pig.kill(1, 0)
# print(User.get_pigs(1))
# # print(User.has_premium(1))
