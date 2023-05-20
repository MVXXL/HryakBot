import datetime
import json

import mysql.connector

from .connection import Connection
from ...core import *
from ..functions import Func
from ...core.config import users_schema, shop_schema


class Shop:

    # @staticmethod
    # def add_daily_items(daily_items):
    #     daily_items = json.dumps(daily_items, ensure_ascii=False)
    #     Connection.make_request(
    #         f"UPDATE {shop_schema} SET inventory = '{daily_items}' WHERE id = {user_id}"
    #     )

    # @staticmethod
    # def set_daily_shop(daily_items):
    #     daily_items = json.dumps(daily_items, ensure_ascii=False)
    #     Connection.make_request(
    #         f"UPDATE {shop_schema} SET inventory = '{daily_items}' WHERE id = {user_id}"
    #     )

    @staticmethod
    def get_last_static_shop():
        result = Connection.make_request(
            f"SELECT static_shop FROM {shop_schema} ORDER BY id DESC LIMIT 1",
            commit=False,
            fetch=True
        )
        if result is not None:
            return json.loads(result)

    @staticmethod
    def get_last_daily_shop():
        result = Connection.make_request(
            f"SELECT daily_shop FROM {shop_schema} ORDER BY id DESC LIMIT 1",
            commit=False,
            fetch=True
        )
        if result is not None:
            return json.loads(result)

    @staticmethod
    def get_last_update_timestamp():
        result = Connection.make_request(
            f"SELECT update_timestamp FROM {shop_schema} ORDER BY id DESC LIMIT 1",
            commit=False,
            fetch=True,
            fetch_first=False
        )
        if result is not None:
            return int(result[0])

    @staticmethod
    def add_shop_state(daily_shop):
        daily_shop = json.dumps(daily_shop, ensure_ascii=False)
        Connection.make_request(
            f"INSERT INTO {shop_schema} (update_timestamp, static_shop, daily_shop) "
            f"VALUES ('{Func.get_current_timestamp()}', "
            f"'{json.dumps(list(Func.get_items_by_key(items, 'method_of_obtaining', 'shop:always').keys()), ensure_ascii=False)}', "
            f"'{daily_shop}')"
        )
