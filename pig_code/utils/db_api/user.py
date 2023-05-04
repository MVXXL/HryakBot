import json

import mysql.connector

from .connection import Connection
from ...core.config import users_schema

class User:

    @staticmethod
    def register_user_if_not_exists(user_id):
        if not User.exists(user_id):
            User.register(user_id)

    @staticmethod
    def register(user_id):
        Connection.make_request(
            f"INSERT INTO {users_schema} (id, pigs, inventory) "
            f"VALUES ('{user_id}', '{'[]'}', '{'{}'}')"
        )

    @staticmethod
    def exists(user_id):
        result = Connection.make_request(
            f"SELECT EXISTS(SELECT 1 FROM {users_schema} WHERE id = {user_id})",
            commit=False,
            fetch=True
        )
        return bool(result)
        # with connection.cursor() as cursor:
        #     cursor.execute(f"SELECT EXISTS(SELECT 1 FROM users WHERE id = {user_id})")
        #     result = cursor.fetchone()[0]
        #     return bool(result)

    @staticmethod
    def get_money(user_id):
        result = Connection.make_request(
            f"SELECT money FROM {users_schema} WHERE id = {user_id}",
            commit=False,
            fetch=True
        )
        return result

    @staticmethod
    def add_money(user_id, amount: int):
        Connection.make_request(
            f"UPDATE {users_schema} SET money = money + {amount} WHERE id = {user_id}"
        )

    @staticmethod
    def get_pigs(user_id):
        result = Connection.make_request(
            f"SELECT pigs FROM {users_schema} WHERE id = {user_id}",
            commit=False,
            fetch=True
        )
        if result is not None:
            return json.loads(result)
        else:
            return {}

    @staticmethod
    def get_inventory(user_id):
        result = Connection.make_request(
            f"SELECT inventory FROM {users_schema} WHERE id = {user_id}",
            commit=False,
            fetch=True
        )
        if result is not None:
            return json.loads(result)
        else:
            return {}

    @staticmethod
    def set_premium(user_id, premium: bool):
        premium = 1 if premium else 0
        Connection.make_request(
            f"UPDATE {users_schema} SET premium = '{premium}' WHERE id = {user_id}"
        )

    @staticmethod
    def has_premium(user_id):
        result = Connection.make_request(
            f"SELECT premium FROM {users_schema} WHERE id = {user_id}",
            commit=False,
            fetch=True
        )
        return bool(result)

    @staticmethod
    def set_language(user_id, language: bool):
        Connection.make_request(
            f"UPDATE {users_schema} SET language = '{language}' WHERE id = {user_id}"
        )

    @staticmethod
    def get_language(user_id):
        result = Connection.make_request(
            f"SELECT language FROM {users_schema} WHERE id = {user_id}",
            commit=False,
            fetch=True
        )
        return result

    @staticmethod
    def set_block(user_id, block: bool):
        block = 1 if block else 0
        Connection.make_request(
            f"UPDATE {users_schema} SET blocked = '{block}' WHERE id = {user_id}"
        )


    @staticmethod
    def is_blocked(user_id):
        result = Connection.make_request(
            f"SELECT blocked FROM {users_schema} WHERE id = {user_id}",
            commit=False,
            fetch=True
        )
        return bool(result)

    @staticmethod
    def set_block_reason(user_id, reason: str):
        Connection.make_request(
            f"UPDATE {users_schema} SET block_reason = '{reason}' WHERE id = {user_id}"
        )

    @staticmethod
    def get_block_reason(user_id):
        result = Connection.make_request(
            f"SELECT block_reason FROM {users_schema} WHERE id = {user_id}",
            commit=False,
            fetch=True
        )
        return result
