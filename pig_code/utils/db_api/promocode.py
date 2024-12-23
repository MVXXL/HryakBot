from .connection import Connection
from ..functions import *
from ...core import *
from ...core.config import promocode_schema


class PromoCode:

    @staticmethod
    def exists(code: str):
        result = Connection.make_request(
            f"SELECT EXISTS(SELECT 1 FROM {promocode_schema} WHERE id = '{code}')",
            commit=False,
            fetch=True
        )
        return bool(result)

    @staticmethod
    def create(max_uses, prise, lifespan: int = None, can_use: str = None, code: str = None):
        prise = json.dumps(prise)
        if code is None:
            code = ''.join([random.choice(string.ascii_letters +
                                          string.digits) for _ in range(12)])
        Connection.make_request(
            f"INSERT INTO {promocode_schema} (id, created, max_uses, users_used, prise, can_use, expires_in) "
            f"VALUES ('{code}', '{Func.get_current_timestamp()}', '{max_uses}', '[]', %s, %s, %s)",
            params=(prise, can_use, lifespan)
        )
        return code

    @staticmethod
    def delete(code: str):
        Connection.make_request(
            f"DELETE FROM {promocode_schema} WHERE id = '{code}'"
        )

    @staticmethod
    def get_prise(code: str):
        result = Connection.make_request(
            f"SELECT prise FROM {promocode_schema} WHERE id = '{code}'",
            commit=False,
            fetch=True
        )
        return json.loads(result)

    @staticmethod
    def used_times(code: str):
        users_used = PromoCode.get_users_used(code)
        return len(users_used)

    @staticmethod
    def get_user_used_times(code: str, user_id):
        users_used = PromoCode.get_users_used(code)
        return users_used.count(str(user_id))

    @staticmethod
    def max_uses(code: str):
        result = Connection.make_request(
            f"SELECT max_uses FROM {promocode_schema} WHERE id = '{code}'",
            commit=False,
            fetch=True
        )
        return result

    @staticmethod
    def created(code: str):
        result = Connection.make_request(
            f"SELECT created FROM {promocode_schema} WHERE id = '{code}'",
            commit=False,
            fetch=True
        )
        return int(result)

    @staticmethod
    def get_users_used(code: str) -> list:
        result = Connection.make_request(
            f"SELECT users_used FROM {promocode_schema} WHERE id = '{code}'",
            commit=False,
            fetch=True
        )
        if result is not None:
            return json.loads(result)
        else:
            return []

    @staticmethod
    def can_use(code: str):
        result = Connection.make_request(
            f"SELECT can_use FROM {promocode_schema} WHERE id = '{code}'",
            commit=False,
            fetch=True
        )
        return result

    @staticmethod
    def expires_in(code: str):
        result = Connection.make_request(
            f"SELECT expires_in FROM {promocode_schema} WHERE id = '{code}'",
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
            f"UPDATE {promocode_schema} SET users_used = '{new_users}' WHERE id = '{code}'"
        )
