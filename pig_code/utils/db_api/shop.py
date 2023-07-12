from .connection import Connection
from .inventory import Inventory
from .user import User
from ..functions import Func
from ...core import *
from ...core.config import shop_schema


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
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_last_static_shop():
        result = Connection.make_request(
            f"SELECT static_shop FROM {shop_schema} ORDER BY id DESC LIMIT 1",
            commit=False,
            fetch=True
        )
        if result is not None:
            return json.loads(result)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_last_daily_shop():
        result = Connection.make_request(
            f"SELECT daily_shop FROM {shop_schema} ORDER BY id DESC LIMIT 1",
            commit=False,
            fetch=True
        )
        if result is not None:
            return json.loads(result)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_last_case_shop():
        result = Connection.make_request(
            f"SELECT case_shop FROM {shop_schema} ORDER BY id DESC LIMIT 1",
            commit=False,
            fetch=True
        )
        if result is not None:
            return json.loads(result)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
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
        static_shop = json.dumps(list(Func.get_items_by_key(items, 'method_of_obtaining', 'shop:always').keys()),
                                 ensure_ascii=False)
        case_shop = json.dumps(list(Func.get_items_by_key(items, 'method_of_obtaining', 'shop:cases').keys()),
                               ensure_ascii=False)
        print(case_shop)
        Connection.make_request(
            f"INSERT INTO {shop_schema} (update_timestamp, static_shop, daily_shop, case_shop) "
            f"VALUES ('{Func.get_current_timestamp()}', '{static_shop}', '{daily_shop}', '{case_shop}')"
        )

    @staticmethod
    def is_item_in_cooldown(user_id, item_id):
        cooldown_once_for, cooldown_in = Inventory.get_item_buy_cooldown(item_id)
        if cooldown_once_for is not None and User.get_count_of_recent_bought_items(user_id, cooldown_in,
                                                                                   [item_id]) >= cooldown_once_for:
            return True
        return False

    @staticmethod
    def get_timestamp_of_new_item(user_id, item_id):
        cooldown_once_for, cooldown_in = Inventory.get_item_buy_cooldown(item_id)
        if cooldown_once_for is None:
            return
        history = User.get_recent_bought_items(user_id, cooldown_in)
        if not history:
            return
        return Func.get_current_timestamp() + (Inventory.get_item_buy_cooldown(item_id)[1] - (
                Func.get_current_timestamp() - list(history[0].values())[0]))
