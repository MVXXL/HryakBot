import datetime
import functools
import json

import mysql.connector

from .connection import Connection
from ..functions import Func
from ...core import *
from ...core.config import users_schema


# from .stats import Stats


class User:

    @staticmethod
    def register_user_if_not_exists(user_id):
        if not User.exists(user_id):
            User.register(user_id)

    @staticmethod
    def register(user_id):
        stats = json.dumps(utils_config.stats)
        Connection.make_request(
            f"INSERT INTO {users_schema} (id, pig, inventory, stats, events, buy_history) "
            f"VALUES ('{user_id}', '{'{}'}', '{'{}'}', '{stats}', '{'{}'}', '[]')"
        )
        # Stats.fix_stats_structure(user_id)

    @staticmethod
    def exists(user_id):
        result = Connection.make_request(
            f"SELECT EXISTS(SELECT 1 FROM {users_schema} WHERE id = {user_id})",
            commit=False,
            fetch=True
        )
        return bool(result)

    @staticmethod
    @aiocache.cached(ttl=6000)
    async def get_user(client, user_id):
        user = await client.fetch_user(int(user_id))
        return user

    @staticmethod
    async def get_name(client, user_id):
        user = await User.get_user(client, user_id)
        return user.display_name

    @staticmethod
    def get_users_sorted_by(column, json_key: str = None, number: int = 100000, exclude: list = None):
        if exclude is None:
            exclude = []
        exclude = [str(i) for i in exclude]
        if json_key is None:
            result = Connection.make_request(
                f"SELECT id FROM {users_schema} ORDER BY {column} ASC;",
                fetch=True, commit=False, fetchall=True
            )
        else:
            result = Connection.make_request(
                f"SELECT id FROM {users_schema} ORDER BY JSON_EXTRACT({column}, '$.{json_key}') ASC;",
                fetch=True, commit=False, fetchall=True
            )
        result = [i[0] for i in result if i[0] not in exclude]
        return result[::-1][:number]

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
            f"UPDATE {users_schema} SET money = money + {round(amount)} WHERE id = {user_id}"
        )

    @staticmethod
    def set_money(user_id, amount: int):
        Connection.make_request(
            f"UPDATE {users_schema} SET money = {amount} WHERE id = {user_id}"
        )

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_pig(user_id):
        result = Connection.make_request(
            f"SELECT pig FROM {users_schema} WHERE id = {user_id}",
            commit=False,
            fetch=True,
        )
        if result is not None:
            return json.loads(result)
        else:
            return {}

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
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
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
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
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_language(user_id):
        try:
            result = Connection.make_request(
                f"SELECT language FROM {users_schema} WHERE id = {user_id}",
                commit=False,
                fetch=True,
            )
            return result
        except TypeError:
            return 'en'

    @staticmethod
    def set_block(user_id, block: bool):
        block = 1 if block else 0
        Connection.make_request(
            f"UPDATE {users_schema} SET blocked = '{block}' WHERE id = {user_id}"
        )

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
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
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_block_reason(user_id):
        result = Connection.make_request(
            f"SELECT block_reason FROM {users_schema} WHERE id = {user_id}",
            commit=False,
            fetch=True
        )
        return result

    @staticmethod
    def set_block_promocodes(user_id, block: bool):
        block = 1 if block else 0
        Connection.make_request(
            f"UPDATE {users_schema} SET blocked_promocodes = '{block}' WHERE id = {user_id}"
        )

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def is_blocked_promocodes(user_id):
        result = Connection.make_request(
            f"SELECT blocked_promocodes FROM {users_schema} WHERE id = {user_id}",
            commit=False,
            fetch=True
        )
        return bool(result)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_buy_history(user_id):
        result = Connection.make_request(
            f"SELECT buy_history FROM {users_schema} WHERE id = {user_id}",
            commit=False,
            fetch=True,
        )
        if result is not None:
            return json.loads(result)
        else:
            return {}

    @staticmethod
    def set_buy_history(user_id, new_history):
        new_history = json.dumps(new_history, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {users_schema} SET buy_history = '{new_history}' WHERE id = {user_id}"
        )

    @staticmethod
    def append_buy_history(user_id, item_id):
        buy_history = User.get_buy_history(user_id)
        buy_history.append({item_id: Func.get_current_timestamp()})
        User.set_buy_history(user_id, buy_history)

    @staticmethod
    def get_recent_bought_items(user_id, seconds):
        current_time = datetime.datetime.now()
        recent_items = []
        for item in User.get_buy_history(user_id):
            for key, value in item.items():
                timestamp = datetime.datetime.fromtimestamp(value)
                time_diff = current_time - timestamp
                if time_diff.total_seconds() < seconds:
                    recent_items.append({key: value})
        return recent_items

    @staticmethod
    def get_count_of_recent_bought_items(user_id, seconds, items_):
        count = 0
        recent_items = User.get_recent_bought_items(user_id, seconds)
        for item in recent_items:
            if list(item.keys())[0] in items_:
                count += 1
        return count