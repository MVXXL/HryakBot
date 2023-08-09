from .user import User
from ..functions import *
from ...core import *


class Inventory:

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_item_data(item_id):
        if item_id in items:
            return items[item_id]

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_item_local_data(user_id, item_id):
        inventory = User.get_inventory(user_id)
        if item_id in inventory:
            return User.get_inventory(user_id)[item_id]

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_item_name(item_id, lang):
        if 'name' in items[item_id]:
            return items[item_id]['name'][lang]

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_item_description(item_id, lang):
        if 'desc' in items[item_id]:
            return items[item_id]['desc'][lang]

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_item_components(item_id):
        if 'components' in items[item_id]:
            return items[item_id]['components']
        return []

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_item_type(item_id, lang: str = None):
        if 'type' in items[item_id]:
            if lang is not None:
                return Locales.ItemTypes[items[item_id]['type']][lang]
            return items[item_id]['type']

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_item_main_type(item_id, lang: str = None):
        item_type = Inventory.get_item_type(item_id).split(':')[0]
        if lang is not None:
            return item_type[lang]
        return item_type

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def item_is_skin(item_id):
        if Inventory.get_item_type(item_id).split(":")[0] == 'skin':
            return True
        return False

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_item_skin_type(item_id):
        if Inventory.item_is_skin(item_id):
            skin_type = Inventory.get_item_type(item_id).split(":")[1]
            return skin_type

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_item_image_url(item_id):
        if 'image_url' in items[item_id]:
            return items[item_id]['image_url']

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_item_image_file(item_id):
        if 'image_file' in items[item_id]:
            return items[item_id]['image_file']

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_item_cost(item_id):
        if 'cost' in items[item_id]:
            return items[item_id]['cost']

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_item_shop_price(item_id):
        if 'shop_price' in items[item_id]:
            return items[item_id]['shop_price']

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_item_method_of_obtaining(item_id):
        if 'method_of_obtaining' in items[item_id]:
            return items[item_id]['method_of_obtaining']

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_item_rarity(item_id, lang: str = None):
        if 'rarity' in items[item_id]:
            if lang is not None:
                return Locales.ItemRarities[items[item_id]['rarity']][lang]
            return items[item_id]['rarity']

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_item_emoji(item_id):
        if 'emoji' in items[item_id]:
            return items[item_id]['emoji']

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_item_cooked_id(item_id):
        if 'cooked' in items[item_id]:
            return items[item_id]['cooked']

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_item_amount(user_id, item_id):
        inventory = User.get_inventory(user_id)
        if item_id in inventory:
            return inventory[item_id]['amount']
        return 0

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def is_skin(item_id):
        if Inventory.get_item_type(item_id).startswith('skin'):
            return True
        return False

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_item_buffs(item_id):
        possible_buffs = ['weight_boost', 'pooping_boost']
        buffs = {}
        for buff in possible_buffs:
            if buff in items[item_id]:
                buffs[buff] = items[item_id][buff]
            else:
                buffs[buff] = 1
        return buffs

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_item_buy_cooldown(item_id):
        if 'cooldown' in items[item_id]:
            return tuple(items[item_id]['cooldown'].items())[0]
        return None, None

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def is_item_obtainable_in_cases(item_id):
        pass

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_items_obtainable_in_cases(items_: dict):
        items_ = Func.get_items_by_key(Func.get_items_by_key(items_, 'method_of_obtaining', 'shop:daily'), 'type',
                                       'skin')
        return items_
