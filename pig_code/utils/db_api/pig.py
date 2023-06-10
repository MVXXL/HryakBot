import datetime
import json
import random

import mysql.connector

from .connection import Connection
from .user import User
from .tech import Tech
from ..functions import Func
from ...core import *
from ...core.config import users_schema


class Pig:

    @staticmethod
    def fix_pig_structure_for_all_users():
        users = Tech.get_all_users()
        for user in users:
            Pig.fix_pig_structure(user)
        # Connection.make_request(
        #     "UPDATE users SET stats = JSON_SET(stats, '$.commands_used', JSON_OBJECT());"
        # )

    @staticmethod
    def fix_pig_structure(user_id):
        pig = User.get_pig(user_id)
        fixed_pig = pig
        for key in utils_config.default_pig:
            if key not in pig:
                pig[key] = utils_config.default_pig[key]
            if type(pig[key]) == dict:
                for i in utils_config.default_pig[key]:
                    if i not in pig[key]:
                        pig[key][i] = utils_config.default_pig[key][i]
        pig['weight'] = round(pig['weight'], 1)
        # for key in utils_config.default_pig['skins']:
        #     if key not in pig['skins']:
        #         pig['skins'][key] = utils_config.default_pig['skins'][key]
        # for key in utils_config.default_pig['genetic']:
        #     if key not in pig['genetic']:
        #         pig['genetic'][key] = utils_config.default_pig['genetic'][key]
        # for key in utils_config.default_pig['skins']:
        #     if key not in pig['skins']:
        #         pig['skins'][key] = utils_config.default_pig['skins'][key]
        Pig.update_pig(user_id, fixed_pig)

    @staticmethod
    def create_pig_if_no_pig(user_id):
        if not User.get_pig(user_id):
            Pig.create(user_id)

    @staticmethod
    def update_pig(user_id, new_pig):
        new_pig = json.dumps(new_pig, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {users_schema} SET pig = '{new_pig}' WHERE id = {user_id}"
        )

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_buffs(user_id):
        pig = User.get_pig(user_id)
        return pig['buffs']

    @staticmethod
    def add_buff(user_id, buff, amount):
        pig = User.get_pig(user_id)
        if buff in pig['buffs']:
            pig['buffs'][buff] += amount
        else:
            pig['buffs'][buff] = amount
        Pig.update_pig(user_id, pig)

    @staticmethod
    def remove_buff(user_id, buff, amount):
        pig = User.get_pig(user_id)
        if buff in pig['buffs']:
            pig['buffs'][buff] -= amount
        Pig.update_pig(user_id, pig)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_buff_value(user_id, buff):
        pig = User.get_pig(user_id)
        if buff in pig['buffs']:
            return pig['buffs'][buff]
        return 0

    @staticmethod
    def create(user_id, name: str = None):
        pig = utils_config.default_pig.copy()
        pig['genetic']['body'] = random.choice(utils_config.default_pig_body_genetic)
        pig['genetic']['eyes'] = random.choice(utils_config.default_pig_eyes_genetic)
        pig['genetic']['pupils'] = random.choice(utils_config.default_pig_pupils_genetic)
        if name is None:
            pig['name'] = random.choice(utils_config.pig_names)
        else:
            pig['name'] = name
        Pig.update_pig(user_id, pig)

    @staticmethod
    def rename(user_id, name: str):
        pig = User.get_pig(user_id)
        pig['name'] = name
        Pig.update_pig(user_id, pig)

    @staticmethod
    def set_genetic(user_id, key, value):
        pig = User.get_pig(user_id)
        pig['genetic'][key] = value
        Pig.update_pig(user_id, pig)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_genetic(user_id, key):
        pig = User.get_pig(user_id)
        if key == 'all':
            return pig['genetic']
        if key in pig['genetic']:
            return pig['genetic'][key]

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_name(user_id):
        pig = User.get_pig(user_id)
        return pig['name']

    @staticmethod
    def set_skin(user_id, skin):
        pig = User.get_pig(user_id)
        pig['skins'][items[skin]['type'].split(':')[1]] = skin
        Pig.update_pig(user_id, pig)

    @staticmethod
    def remove_skin(user_id, skin_type):
        pig = User.get_pig(user_id)
        pig['skins'][skin_type] = None
        Pig.update_pig(user_id, pig)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_skin(user_id, key):
        pig = User.get_pig(user_id)
        if key == 'all':
            return pig['skins']
        if key in pig['skins']:
            return pig['skins'][key]

    @staticmethod
    def _set_last_action(user_id, timestamp, action):
        pig = User.get_pig(user_id)
        pig[action] = timestamp
        Pig.update_pig(user_id, pig)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def _get_last_action(user_id, action):
        pig = User.get_pig(user_id)
        return pig[action]

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def _get_time_to_next_action(user_id, action):
        last_action = Pig._get_last_action(user_id, action)
        cooldown = 100000
        match action:
            case 'last_feed':
                cooldown = utils_config.pig_feed_cooldown
            case 'last_meat':
                cooldown = utils_config.pig_meat_cooldown
            case 'last_breed':
                cooldown = utils_config.pig_breed_cooldown
        if last_action is None:
            return -1
        next_action = last_action + cooldown - Func.get_current_timestamp()
        return next_action if next_action > 0 else -1

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def _get_time_of_next_action(user_id, action):
        if Pig._get_time_to_next_action(user_id, action) == -1:
            return Func.get_current_timestamp()
        return Func.get_current_timestamp() + Pig._get_time_to_next_action(user_id, action)

    @staticmethod
    def set_last_feed(user_id, timestamp):
        Pig._set_last_action(user_id, timestamp, 'last_feed')

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_last_feed(user_id):
        return Pig._get_last_action(user_id, 'last_feed')

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_time_to_next_feed(user_id):
        return Pig._get_time_to_next_action(user_id, 'last_feed')

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_time_of_next_feed(user_id):
        return Pig._get_time_of_next_action(user_id, 'last_feed')

    @staticmethod
    def set_last_meat(user_id, timestamp):
        Pig._set_last_action(user_id, timestamp, 'last_meat')

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_last_meat(user_id):
        return Pig._get_last_action(user_id, 'last_meat')

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_time_to_next_meat(user_id):
        return Pig._get_time_to_next_action(user_id, 'last_meat')

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_time_of_next_meat(user_id):
        return Pig._get_time_of_next_action(user_id, 'last_meat')

    @staticmethod
    def set_last_breed(user_id, timestamp):
        Pig._set_last_action(user_id, timestamp, 'last_breed')

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_last_breed(user_id):
        return Pig._get_last_action(user_id, 'last_breed')

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_time_to_next_breed(user_id):
        return Pig._get_time_to_next_action(user_id, 'last_breed')

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_time_of_next_breed(user_id):
        return Pig._get_time_of_next_action(user_id, 'last_breed')

    @staticmethod
    def add_weight(user_id, weight: float):
        pig = User.get_pig(user_id)
        pig['weight'] += weight
        pig['weight'] = round(pig['weight'], 1)
        if pig['weight'] <= .1:
            pig['weight'] = .1
        Pig.update_pig(user_id, pig)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_weight(user_id):
        pig = User.get_pig(user_id)
        return pig['weight']

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def make_pregnant(user_id, pregnant_by_id, pregnant_with_id):
        pig = User.get_pig(user_id)
        pig['pregnant_time'] = Func.get_current_timestamp()
        pig['pregnant_with'] = pregnant_with_id
        pig['pregnant_by'] = pregnant_by_id
        pig['pregnancy_duration'] = items[pregnant_with_id]['pregnancy_duration']
        Pig.update_pig(user_id, pig)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def disable_pregnant(user_id):
        pig = User.get_pig(user_id)
        pig['pregnant_time'] = None
        Pig.update_pig(user_id, pig)
