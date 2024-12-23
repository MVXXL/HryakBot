import AaioAsync
import discord

from .connection import Connection
from ..functions import Func, translate
from ...core import *
from ...core.config import users_schema
from .history import History



class User:

    @staticmethod
    def register_user_if_not_exists(user_id):
        if not User.exists(user_id):
            User.register(user_id)

    @staticmethod
    def register(user_id):
        stats = json.dumps(utils_config.default_stats)
        pig = utils_config.default_pig.copy()
        body = random.choice(utils_config.default_pig_body_genetic)
        pig['genetic']['body'] = body
        pig['genetic']['tail'] = body
        pig['genetic']['left_ear'] = body
        pig['genetic']['right_ear'] = body
        pig['genetic']['nose'] = body
        eyes = random.choice(utils_config.default_pig_eyes_genetic)
        pig['genetic']['right_eye'] = eyes
        pig['genetic']['left_eye'] = eyes
        pupils = random.choice(utils_config.default_pig_pupils_genetic)
        pig['genetic']['right_pupil'] = pupils
        pig['genetic']['left_pupil'] = pupils
        pig['name'] = 'Hryak'
        pig = json.dumps(pig)
        Connection.make_request(
            f"INSERT INTO {users_schema} (id, created, pig, settings, inventory, stats, events, history, rating, orders) "
            f"VALUES ('{user_id}', '{Func.get_current_timestamp()}', %s, %s, '{'{}'}', '{stats}', '{'{}'}', %s, '{'{}'}', '{'{}'}')",
            params=(pig, json.dumps(utils_config.user_settings), json.dumps(utils_config.default_history))
        )
        User.add_item(user_id, 'common_case')

    @staticmethod
    def exists(user_id):
        result = Connection.make_request(
            f"SELECT EXISTS(SELECT 1 FROM {users_schema} WHERE id = {user_id})",
            commit=False,
            fetch=True
        )
        return bool(result)

    @staticmethod
    @aiocache.cached(ttl=86400)
    async def get_user(client, user_id) -> discord.User:
        user = client.get_user(int(user_id))
        if user is None:
            user = await client.fetch_user(int(user_id))
        return user

    @staticmethod
    async def get_name(client, user_id):
        user = await User.get_user(client, user_id)
        return user.display_name

    @staticmethod
    @cached(utils_config.db_caches['user.get_inventory'])
    def get_inventory(user_id: str):
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
    def clear_get_inventory_cache(user_id):
        Func.clear_cache('user.get_inventory', (str(user_id),))

    @staticmethod
    def set_item_amount(user_id, item_id, amount: int = 1):
        inventory = User.get_inventory(str(user_id))
        inventory[item_id] = {}
        inventory[item_id]['item_id'] = item_id
        inventory[item_id]['amount'] = amount
        User.set_new_inventory(user_id, inventory)

    @staticmethod
    def add_item(user_id, item_id, amount: int = 1, log: bool = True):
        inventory = User.get_inventory(str(user_id))
        amount = round(amount)
        if item_id in inventory:
            inventory[item_id]['amount'] += amount
        else:
            inventory[item_id] = {}
            inventory[item_id]['amount'] = amount
        User.set_new_inventory(user_id, inventory)
        if log:
            Func.add_log('item_generated',
                         user_id=user_id,
                         item_id=item_id,
                         amount=amount)

    @staticmethod
    def remove_item(user_id, item_id, amount: int = 1, log: bool = True):
        User.add_item(user_id, item_id, -amount, log=False)
        if log:
            Func.add_log('item_burned',
                         user_id=user_id,
                         item_id=item_id,
                         amount=amount)

    @staticmethod
    def transfer_item(from_user_id, to_user2_id, item_id, amount: int = 1):
        User.remove_item(from_user_id, item_id, amount, log=False)
        User.add_item(to_user2_id, item_id, amount, log=False)
        Func.add_log('item_transfer',
                     from_user_id=from_user_id,
                     to_user2_id=to_user2_id,
                     item_id=item_id,
                     amount=amount)

    @staticmethod
    def set_new_inventory(user_id, new_inventory):
        new_inventory = json.dumps(new_inventory, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {users_schema} SET inventory = %s WHERE id = {user_id}",
            params=(new_inventory,)
        )
        User.clear_get_inventory_cache(user_id)

    @staticmethod
    @cached(utils_config.db_caches['user.get_settings'])
    def get_settings(user_id: str):
        result = Connection.make_request(
            f"SELECT settings FROM {users_schema} WHERE id = {user_id}",
            commit=False,
            fetch=True
        )
        if result is not None:
            return json.loads(result)
        else:
            return {}

    @staticmethod
    def clear_get_settings_cache(user_id):
        Func.clear_cache('user.get_settings', (str(user_id),))

    @staticmethod
    def set_new_settings(user_id, new_settings):
        new_settings = json.dumps(new_settings, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {users_schema} SET settings = %s WHERE id = {user_id}",
            params=(new_settings,)
        )
        User.clear_get_settings_cache(user_id)

    @staticmethod
    def set_language(user_id, language):
        settings = User.get_settings(str(user_id))
        settings['language'] = language
        User.set_new_settings(user_id, settings)

    @staticmethod
    def get_language(user_id):
        settings = User.get_settings(str(user_id))
        return settings['language']

    @staticmethod
    def get_registration_timestamp(user_id):
        result = Connection.make_request(
            f"SELECT created FROM {users_schema} WHERE id = {user_id}",
            commit=False,
            fetch=True
        )
        return int(result)

    @staticmethod
    def get_age(user_id):
        return Func.get_current_timestamp() - User.get_registration_timestamp(user_id)

    @staticmethod
    def set_family(user_id, family_id: str):
        settings = User.get_settings(str(user_id))
        settings['family'] = family_id
        User.set_new_settings(user_id, settings)

    @staticmethod
    def get_family(user_id):
        settings = User.get_settings(str(user_id))
        return settings['family']

    @staticmethod
    def set_block(user_id, block: bool, reason: str = None):
        settings = User.get_settings(str(user_id))
        settings['blocked'] = block
        User.set_block_reason(user_id, reason)
        User.set_new_settings(user_id, settings)

    @staticmethod
    def is_blocked(user_id):
        settings = User.get_settings(str(user_id))
        return settings['blocked']

    @staticmethod
    def set_block_reason(user_id, reason: str):
        settings = User.get_settings(str(user_id))
        settings['block_reason'] = reason
        User.set_new_settings(user_id, settings)

    @staticmethod
    def get_block_reason(user_id):
        settings = User.get_settings(str(user_id))
        return settings['block_reason']

    # @staticmethod
    # def set_block_promocodes(user_id, block: bool):
    #     block = 1 if block else 0
    #     Connection.make_request(
    #         f"UPDATE {users_schema} SET blocked_promocodes = '{block}' WHERE id = {user_id}"
    #     )

    # @staticmethod
    # # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    # def is_blocked_promocodes(user_id):
    #     result = Connection.make_request(
    #         f"SELECT blocked_promocodes FROM {users_schema} WHERE id = {user_id}",
    #         commit=False,
    #         fetch=True
    #     )
    #     return bool(result)

    @staticmethod
    def get_rating(user_id):
        result = Connection.make_request(
            f"SELECT rating FROM {users_schema} WHERE id = {user_id}",
            commit=False,
            fetch=True,
        )
        if result is not None:
            return json.loads(result)
        else:
            return {}

    @staticmethod
    def set_new_rating(user_id, new_rating):
        new_rating = json.dumps(new_rating, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {users_schema} SET rating = '{new_rating}' WHERE id = {user_id}"
        )

    @staticmethod
    def append_rate(user_id, rated_by_id, rate):
        rating = User.get_rating(user_id)
        if str(rated_by_id) not in rating:
            rating[str(rated_by_id)] = {}
        rating[str(rated_by_id)]['rate_timestamp'] = Func.get_current_timestamp()
        rating[str(rated_by_id)]['rate'] = rate
        User.set_new_rating(user_id, rating)

    # @staticmethod
    # def append_comment(user_id, rated_by_id, comment):
    #     rating = User.get_rating(user_id)
    #     if str(rated_by_id) not in rating:
    #         rating[str(rated_by_id)] = {}
    #     rating[str(rated_by_id)]['comment_timestamp'] = Func.get_current_timestamp()
    #     rating[str(rated_by_id)]['comment'] = comment
    #     User.set_new_rating(user_id, rating)
    #
    # @staticmethod
    # def get_comments(user_id):
    #     rating = User.get_rating(user_id)
    #     rating = {k: v for k, v in rating.items() if 'comment' in v}
    #     rating = sorted(rating, key=rating['comment_timestamp'])
    #     return rating

    # @staticmethod
    # def get_comment(user_id, commentator_id):
    #     rating = User.get_rating(user_id)
    #     if str(commentator_id) not in rating:
    #         if
    #         rating[str(commentator_id)] = {}
    #     return rating

    @staticmethod
    def get_rate_number(user_id, rater_id):
        rating = User.get_rating(user_id)
        rate = 0
        if str(rater_id) in rating:
            if 'rate' in rating[str(rater_id)]:
                rate = rating[str(rater_id)]['rate']
        return rate

    @staticmethod
    def get_rating_total_number(user_id):
        rating = User.get_rating(user_id)
        number = 0
        for rater_id in rating:
            number += User.get_rate_number(user_id, rater_id)
        return number

    @staticmethod
    def get_recent_bought_items(user_id, seconds):
        current_time = datetime.datetime.now()
        recent_items = []
        for item in History.get_shop_history(user_id):
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

    @staticmethod
    def get_orders(user_id):
        result = Connection.make_request(
            f"SELECT orders FROM {users_schema} WHERE id = {user_id}",
            commit=False,
            fetch=True,
        )
        if result is not None:
            return json.loads(result)
        else:
            return {}

    @staticmethod
    def set_new_orders(user_id, new_orders):
        new_orders = json.dumps(new_orders, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {users_schema} SET orders = '{new_orders}' WHERE id = {user_id}"
        )

    @staticmethod
    async def create_new_order(user_id, order_id: str, items: dict, platform: str = 'aaio'):
        orders = User.get_orders(user_id)
        orders[order_id] = {'status': 'in_process',
                            'items': items,
                            'platform': platform,
                            'timestamp': Func.get_current_timestamp()}
        User.set_new_orders(user_id, orders)

    @staticmethod
    def order_exists(user_id, order_id: str):
        orders = User.get_orders(user_id)
        if order_id in orders:
            return orders[order_id]

    @staticmethod
    def get_order(user_id, order_id: str):
        orders = User.get_orders(user_id)
        if order_id in orders:
            return orders[order_id]

    @staticmethod
    def get_order_db_status(user_id, order_id: str):
        order = User.get_order(user_id, order_id)
        return order['status']

    @staticmethod
    def get_order_items(user_id, order_id: str):
        order = User.get_order(user_id, order_id)
        return order['items']

    @staticmethod
    def get_order_platform(user_id, order_id: str):
        order = User.get_order(user_id, order_id)
        return order['platform']

    @staticmethod
    async def get_order_info(order_id: str):
        try:
            info = await utils_config.aaio.getorderinfo(order_id)
            return info
        except:
            return

    @staticmethod
    async def get_order_status(order_id: str):
        # return 'success'
        info = await User.get_order_info(order_id)
        if info is None:
            return 'not_exists'
        return info.status

    @staticmethod
    def delete_order(user_id, order_id):
        orders = User.get_orders(user_id)
        if order_id in orders:
            orders.pop(order_id)
        User.set_new_orders(user_id, orders)


