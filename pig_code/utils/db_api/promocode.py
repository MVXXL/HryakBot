import datetime
import json
import string

import mysql.connector

from .connection import Connection
from .user import User
from .tech import Tech
from ..functions import *
from ...core import *
from ...core.config import promo_code_schema


class PromoCode:

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def exists(code: str):
        result = Connection.make_request(
            f"SELECT EXISTS(SELECT 1 FROM {promo_code_schema} WHERE id = '{code}')",
            commit=False,
            fetch=True
        )
        return bool(result)

    @staticmethod
    def create(max_uses, prise, expires_in: int = None, can_use: str = None, code: str = None):
        prise = json.dumps(prise)
        if code is None:
            code = ''.join([random.choice(string.ascii_letters +
                                          string.digits) for _ in range(12)])
        Connection.make_request(
            f"INSERT INTO {promo_code_schema} (id, created, max_uses, users_used, prise, can_use, expires_in) "
            f"VALUES ('{code}', '{Func.get_current_timestamp()}', '{max_uses}', '[]', '{prise}', '{can_use}', '{expires_in}')"
        )
        return code

    @staticmethod
    def delete(code: str):
        Connection.make_request(
            f"DELETE FROM {promo_code_schema} WHERE id = '{code}'"
        )

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_prise(code: str):
        # Connection.make_request(
        #     f"INSERT INTO {promo_code_schema} (id, created, max_uses, prise) "
        #     f"VALUES ('{code}', '{Func.get_current_timestamp()}', '{max_uses}', '{prise}')"
        # )
        result = Connection.make_request(
            f"SELECT prise FROM {promo_code_schema} WHERE id = '{code}'",
            commit=False,
            fetch=True
        )
        return json.loads(result)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def used_times(code: str):
        users_used = PromoCode.get_users_used(code)
        return len(users_used)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_user_used_times(code: str, user_id):
        users_used = PromoCode.get_users_used(code)
        return users_used.count(str(user_id))

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def max_uses(code: str):
        result = Connection.make_request(
            f"SELECT max_uses FROM {promo_code_schema} WHERE id = '{code}'",
            commit=False,
            fetch=True
        )
        return result

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def created(code: str):
        result = Connection.make_request(
            f"SELECT created FROM {promo_code_schema} WHERE id = '{code}'",
            commit=False,
            fetch=True
        )
        return int(result)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_users_used(code: str) -> list:
        result = Connection.make_request(
            f"SELECT users_used FROM {promo_code_schema} WHERE id = '{code}'",
            commit=False,
            fetch=True
        )
        if result is not None:
            return json.loads(result)
        else:
            return []

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def can_use(code: str):
        result = Connection.make_request(
            f"SELECT can_use FROM {promo_code_schema} WHERE id = '{code}'",
            commit=False,
            fetch=True
        )
        return result

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def expires_in(code: str):
        result = Connection.make_request(
            f"SELECT expires_in FROM {promo_code_schema} WHERE id = '{code}'",
            commit=False,
            fetch=True
        )
        return result

    @staticmethod
    def add_users_used(code: str, user_id):
        users_used = PromoCode.get_users_used(code)
        users_used.append(str(user_id))
        PromoCode.set_new_users_used(code, users_used)

    @staticmethod
    def set_new_users_used(code: str, new_users: list):
        new_users = json.dumps(new_users, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {promo_code_schema} SET users_used = '{new_users}' WHERE id = '{code}'"
        )
