import datetime
import json

import mysql.connector

from .connection import Connection
from .user import User
from .tech import Tech
from ..functions import *
from ...core import *
from ...core.config import users_schema


class Inventory:

    # @staticmethod
    # def fix_items_in_inventory_for_all_users():
    #     users = Tech.get_all_users()
    #     for user in users:
    #         Inventory.fix_item_structure_for_inventory(user)
    #
    # @staticmethod
    # def fix_item_structure_for_inventory(user_id):
    #     inventory = User.get_inventory(user_id)
    #     for item in inventory.keys():
    #         Inventory.fix_item_structure(user_id, item)
    #
    # @staticmethod
    # def fix_item_structure(user_id, item_id):
    #     inventory = User.get_inventory(user_id)
    #     if item_id in inventory:
    #         for i in required_options:
    #             inventory[item_id]['item'][i] = Func.get_item_by_id(item_id)[i]
    #         Inventory.set_new_inventory(user_id, inventory)

    @staticmethod
    def set_item_amount(user_id, item_id, amount: int = 1):
        inventory = User.get_inventory(user_id)
        inventory[item_id] = {}
        inventory[item_id]['item_id'] = item_id
        inventory[item_id]['amount'] = amount
        Inventory.set_new_inventory(user_id, inventory)

    @staticmethod
    def add_item(user_id, item_id, amount: int = 1):
        inventory = User.get_inventory(user_id)
        if item_id in inventory:
            inventory[item_id]['amount'] += amount
        else:
            inventory[item_id] = {}
            inventory[item_id]['item_id'] = item_id
            inventory[item_id]['amount'] = amount
        Inventory.set_new_inventory(user_id, inventory)

    @staticmethod
    def remove_item(user_id, item_id, amount: int = 1):
        inventory = User.get_inventory(user_id)
        if item_id in inventory:
            if inventory[item_id]['amount'] - amount <= 0:
                inventory.pop(item_id)
            else:
                inventory[item_id]['amount'] -= amount
        Inventory.set_new_inventory(user_id, inventory)

    @staticmethod
    def set_new_inventory(user_id, new_inventory):
        new_inventory = json.dumps(new_inventory, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {users_schema} SET inventory = '{new_inventory}' WHERE id = {user_id}"
        )

    @staticmethod
    def get_item_data(item_id):
        if item_id in items:
            return items[item_id]

    @staticmethod
    def get_item_name(item_id, lang):
        if 'name' in items[item_id]:
            return items[item_id]['name'][lang]

    @staticmethod
    def get_item_description(item_id, lang):
        if 'desc' in items[item_id]:
            return items[item_id]['desc'][lang]

    @staticmethod
    def get_item_components(item_id):
        if 'components' in items[item_id]:
            return items[item_id]['components']
        return []

    @staticmethod
    def get_item_type(item_id, lang: str = None):
        if 'type' in items[item_id]:
            if lang is not None:
                return locales['item_types'][items[item_id]['type']][lang]
            return items[item_id]['type']

    @staticmethod
    def get_item_main_type(item_id, lang: str = None):
        item_type = Inventory.get_item_type(item_id).split(':')[0]
        if lang is not None:
            return item_type[lang]
        return item_type

    @staticmethod
    def item_is_skin(item_id):
        if Inventory.get_item_type(item_id).split(":")[0] == 'skin':
            return True
        return False

    @staticmethod
    def get_item_skin_type(item_id):
        if Inventory.item_is_skin(item_id):
            skin_type = Inventory.get_item_type(item_id).split(":")[1]
            return skin_type

    @staticmethod
    def get_item_image_url(item_id):
        if 'image_url' in items[item_id]:
            return items[item_id]['image_url']

    @staticmethod
    def get_item_image_file(item_id):
        if 'image_file' in items[item_id]:
            return items[item_id]['image_file']

    @staticmethod
    def get_item_cost(item_id):
        if 'cost' in items[item_id]:
            return items[item_id]['cost']

    @staticmethod
    def get_item_shop_price(item_id):
        if 'shop_price' in items[item_id]:
            return items[item_id]['shop_price']

    @staticmethod
    def get_item_method_of_obtaining(item_id):
        if 'method_of_obtaining' in items[item_id]:
            return items[item_id]['method_of_obtaining']

    @staticmethod
    def get_item_rarity(item_id, lang: str = None):
        if 'rarity' in items[item_id]:
            if lang is not None:
                return locales['item_rarities'][items[item_id]['rarity']][lang]
            return items[item_id]['rarity']

    @staticmethod
    def get_item_emoji(item_id):
        if 'emoji' in items[item_id]:
            return items[item_id]['emoji']

    @staticmethod
    def get_item_amount(user_id, item_id):
        inventory = User.get_inventory(user_id)
        if item_id in inventory:
            return inventory[item_id]['amount']
        return 0
