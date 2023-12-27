import disnake

from .connection import Connection
from ..functions import Func
from ...core import *
from ...core.config import users_schema


class User:

    @staticmethod
    def register_user_if_not_exists(user_id):
        if not User.exists(user_id):
            User.register(user_id)

    @staticmethod
    def register(user_id):
        stats = json.dumps(utils_config.user_stats)
        pig = utils_config.default_pig.copy()
        pig['genetic']['body'] = random.choice(utils_config.default_pig_body_genetic)
        pig['genetic']['eyes'] = random.choice(utils_config.default_pig_eyes_genetic)
        pig['genetic']['pupils'] = random.choice(utils_config.default_pig_pupils_genetic)
        pig['name'] = random.choice(utils_config.pig_names)
        pig = json.dumps(pig)
        Connection.make_request(
            f"INSERT INTO {users_schema} (id, created, pig, settings, inventory, stats, events, buy_history, rating) "
            f"VALUES ('{user_id}', '{Func.get_current_timestamp()}', %s, %s, '{'{}'}', '{stats}', '{'{}'}', '[]', '{'{}'}')",
            params=(pig, json.dumps(utils_config.user_settings))
        )
        User.add_item(user_id, 'common_case')
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
    @aiocache.cached(ttl=86400)
    async def get_user(client, user_id) -> disnake.User:
        user = client.get_user(int(user_id))
        if user is None:
            user = await client.fetch_user(int(user_id))
        return user

    @staticmethod
    async def get_name(client, user_id):
        user = await User.get_user(client, user_id)
        return user.display_name

    @staticmethod
    def get_pig(user_id):
        if type(user_id) is not list:
            result = Connection.make_request(
                f"SELECT pig FROM {users_schema} WHERE id = {user_id}",
                commit=False,
                fetch=True,
            )
            if result is not None:
                return json.loads(result)
            else:
                return {}
        else:
            user_ids = []
            for i in user_id:
                user_ids.append(int(i))
            result = Connection.make_request(
                f"SELECT pig FROM {users_schema} WHERE id IN {tuple(user_ids)}",
                commit=False,
                fetch=True,
                fetchall=True,
                fetch_first=False
            )
            if result is not None:
                final_result = {}
                for i, j in enumerate(result):
                    final_result[user_ids[i]] = json.loads(j[0])
                return final_result
            else:
                return {}

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

    # @staticmethod
    # def has_item(user_id, item_id):
    #     return item_id in inventory

    @staticmethod
    def add_item(user_id, item_id, amount: int = 1):
        inventory = User.get_inventory(str(user_id))
        amount = round(amount)
        if item_id in inventory:
            inventory[item_id]['amount'] += amount
        else:
            inventory[item_id] = {}
            # inventory[item_id]['item_id'] = item_id
            inventory[item_id]['amount'] = amount
        User.set_new_inventory(user_id, inventory)

    @staticmethod
    def set_item_amount(user_id, item_id, amount: int = 1):
        inventory = User.get_inventory(str(user_id))
        inventory[item_id] = {}
        inventory[item_id]['item_id'] = item_id
        inventory[item_id]['amount'] = amount
        User.set_new_inventory(user_id, inventory)

    @staticmethod
    def remove_item(user_id, item_id, amount: int = 1):
        User.add_item(user_id, item_id, -amount)

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
    # @cached(utils_config.db_caches['user.get_language'])
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
    def append_buy_history(user_id, item_id, amount):
        buy_history = User.get_buy_history(user_id)
        buy_history.append({item_id: Func.get_current_timestamp(), 'amount': amount})
        User.set_buy_history(user_id, buy_history)

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
        print(recent_items)
        for item in recent_items:
            if list(item.keys())[0] in items_:
                count += 1
        return count
