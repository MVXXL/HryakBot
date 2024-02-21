from .connection import Connection
from .item import Item
from .tech import Tech
from .user import User
from ..functions import Func
from ...core import *
from ...core.config import shop_schema


class Shop:

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
    def get_data(shop_id=None):
        if shop_id is None:
            query = f"SELECT data FROM {shop_schema} ORDER BY id DESC LIMIT 1"
        else:
            query = f"SELECT data FROM {shop_schema} WHERE id = {shop_id}"
        result = Connection.make_request(
            query,
            commit=False,
            fetch=True
        )
        if result is not None:
            return json.loads(result)

    @staticmethod
    def get_static_shop(shop_id=None):
        data = Shop.get_data(shop_id)
        return data['static_shop']

    @staticmethod
    def get_daily_shop(shop_id=None):
        data = Shop.get_data(shop_id)
        return data['daily_shop']

    @staticmethod
    def get_case_shop(shop_id=None):
        data = Shop.get_data(shop_id)
        return data['case_shop']

    @staticmethod
    def get_coins_shop(shop_id=None):
        data = Shop.get_data(shop_id)
        return data['coins_shop']

    @staticmethod
    def get_premium_skins_shop(shop_id=None):
        data = Shop.get_data(shop_id)
        return data['premium_skins_shop']

    @staticmethod
    def get_update_timestamp(shop_id=None):
        if shop_id is None:
            query = f"SELECT timestamp FROM {shop_schema} ORDER BY id DESC LIMIT 1"
        else:
            query = f"SELECT timestamp FROM {shop_schema} WHERE id = {shop_id}"
        result = Connection.make_request(
            query,
            commit=False,
            fetch=True,
            fetch_first=False
        )
        if result[0] is not None:
            return int(result[0])

    @staticmethod
    def add_shop_state():
        data = {
            'static_shop': [],
            'daily_shop': Shop.generate_shop_daily_items(),
            'case_shop': [],
            'coins_shop': ['coins.a=500.p=25.c=hollars',
                           'coins.a=1050.p=50.c=hollars',
                           'coins.a=2300.p=100.c=hollars',
                           'coins.a=4800.p=200.c=hollars',
                           'coins.a=12500.p=500.c=hollars'],
            'premium_skins_shop': [],
            # 'premium_sub_shop': {}
        }
        # print(33123, Tech.get_all_items((('shop_category', 'premium_skins'),)))
        for i in ["laxative", "knife", "grill"]:
            data['static_shop'].append(f'{i}.a={1}.p={Item.get_market_price(i)}.c={Item.get_market_price_currency(i)}')
        for i in ["common_case", "rare_case"]:
            data['case_shop'].append(f'{i}.a={1}.p={Item.get_market_price(i)}.c={Item.get_market_price_currency(i)}')
        for i in sorted(Tech.get_all_items((('shop_category', 'premium_skins'),))):
            data['premium_skins_shop'].append(f'{i}.a={1}.p={Item.get_market_price(i)}.c={Item.get_market_price_currency(i)}')
        Connection.make_request(
            f"INSERT INTO {shop_schema} (timestamp, data) "
            f"VALUES ('{Func.get_current_timestamp()}', %s)",
            params=(json.dumps(data),)
        )

    @staticmethod
    def generate_shop_daily_items():
        daily_shop = []
        for key in utils_config.daily_shop_items_types.keys():
            if key == 'other':
                exceptions = []
                daily_shop_items_types_copy = utils_config.daily_shop_items_types.copy()
                daily_shop_items_types_copy.pop('other')
                for i in daily_shop_items_types_copy:
                    exceptions.append(('skin_type', i))
                exceptions = tuple(exceptions)
                for i in random.sample(Tech.get_all_items(requirements=(('shop_category', 'daily'),),
                                                          exceptions=exceptions),
                                       utils_config.daily_shop_items_types[key]):
                    daily_shop.append(f'{i}.a={1}.p={Item.get_market_price(i)}.c={Item.get_market_price_currency(i)}')
            else:
                for i in random.sample(
                        Tech.get_all_items(requirements=(('shop_category', 'daily'), ('skin_type', key))),
                        utils_config.daily_shop_items_types[key]):
                    daily_shop.append(f'{i}.a={1}.p={Item.get_market_price(i)}.c={Item.get_market_price_currency(i)}')
        return daily_shop

    @staticmethod
    def is_item_in_cooldown(user_id, item_id):
        cooldown_once_for, cooldown_in = Item.get_shop_cooldown(item_id)
        if cooldown_once_for is not None and User.get_count_of_recent_bought_items(user_id, cooldown_in,
                                                                                   [Item.clean_id(item_id)]) >= cooldown_once_for:
            return True
        return False

    @staticmethod
    def get_timestamp_of_cooldown_pass(user_id, item_id):
        cooldown_once_for, cooldown_in = Item.get_shop_cooldown(item_id)
        if cooldown_once_for is None:
            return
        history = User.get_recent_bought_items(user_id, cooldown_in)
        if not history:
            return
        return Func.get_current_timestamp() + (Item.get_shop_cooldown(item_id)[1] - (
                Func.get_current_timestamp() - list(history[0].values())[0]))
