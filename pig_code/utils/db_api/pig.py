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
        Pig.replace_pig(user_id, fixed_pig)

    @staticmethod
    def create_pig_if_no_pig(user_id):
        if not User.get_pig(user_id):
            Pig.create(user_id)

    @staticmethod
    def replace_pig(user_id, new_pig):
        new_pig = json.dumps(new_pig, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {users_schema} SET pig = '{new_pig}' WHERE id = {user_id}"
        )

    @staticmethod
    def add_buff(user_id, buff, amount):
        pig = User.get_pig(user_id)
        if buff in pig['buffs']:
            pig['buffs'][buff] += amount
        else:
            pig['buffs'][buff] = amount
        Pig.replace_pig(user_id, pig)

    @staticmethod
    def remove_buff(user_id, buff, amount):
        pig = User.get_pig(user_id)
        if buff in pig['buffs']:
            pig['buffs'][buff] -= amount
        Pig.replace_pig(user_id, pig)

    @staticmethod
    def get_buff_value(user_id, buff):
        pig = User.get_pig(user_id)
        if buff in pig['buffs']:
            return pig['buffs'][buff]
        return 0

    @staticmethod
    def create(user_id, name: str = 'Hryak'):
        pig = utils_config.default_pig.copy()
        pig['genetic']['body'] = random.choice(utils_config.default_pig_body_genetic)
        pig['genetic']['eyes'] = random.choice(utils_config.default_pig_eyes_genetic)
        pig['genetic']['pupils'] = random.choice(utils_config.default_pig_pupils_genetic)
        pig['name'] = name
        Pig.replace_pig(user_id, pig)

    @staticmethod
    def rename(user_id, name: str):
        pig = User.get_pig(user_id)
        pig['name'] = name
        Pig.replace_pig(user_id, pig)

    @staticmethod
    def set_genetic(user_id, key, value):
        pig = User.get_pig(user_id)
        pig['genetic'][key] = value
        Pig.replace_pig(user_id, pig)

    @staticmethod
    def get_genetic(user_id, key):
        pig = User.get_pig(user_id)
        if key == 'all':
            return pig['genetic']
        if key in pig['genetic']:
            return pig['genetic'][key]

    @staticmethod
    def get_name(user_id):
        pig = User.get_pig(user_id)
        return pig['name']

    @staticmethod
    def set_skin(user_id, skin):
        pig = User.get_pig(user_id)
        pig['skins'][items[skin]['type'].split(':')[1]] = skin
        Pig.replace_pig(user_id, pig)

    @staticmethod
    def remove_skin(user_id, skin_type):
        pig = User.get_pig(user_id)
        pig['skins'][skin_type] = None
        Pig.replace_pig(user_id, pig)

    @staticmethod
    def get_skin(user_id, key):
        pig = User.get_pig(user_id)
        if key == 'all':
            return pig['skins']
        if key in pig['skins']:
            return pig['skins'][key]

    @staticmethod
    def set_last_feed(user_id, timestamp):
        pig = User.get_pig(user_id)
        pig['last_feed'] = timestamp
        Pig.replace_pig(user_id, pig)

    @staticmethod
    def get_last_feed(user_id):
        pig = User.get_pig(user_id)
        return pig['last_feed']


    @staticmethod
    def get_time_to_next_feed(user_id):
        last_feed = Pig.get_last_feed(user_id)
        feed_cooldown = utils_config.pig_feed_cooldown if not User.has_premium(
            user_id) else utils_config.premium_pig_feed_cooldown
        if last_feed is None:
            return -1
        next_feed = last_feed + feed_cooldown - Func.get_current_timestamp()
        return next_feed if next_feed > 0 else -1

    @staticmethod
    def get_time_of_next_feed(user_id):
        if Pig.get_time_to_next_feed(user_id) == -1:
            return Func.get_current_timestamp()
        return Func.get_current_timestamp() + Pig.get_time_to_next_feed(user_id)

    @staticmethod
    def set_last_meat(user_id, timestamp):
        pig = User.get_pig(user_id)
        pig['last_meat'] = timestamp
        Pig.replace_pig(user_id, pig)

    @staticmethod
    def get_last_meat(user_id):
        pig = User.get_pig(user_id)
        return pig['last_meat']


    @staticmethod
    def get_time_to_next_meat(user_id):
        last_meat = Pig.get_last_meat(user_id)
        meat_cooldown = utils_config.pig_meat_cooldown if not User.has_premium(
            user_id) else utils_config.premium_pig_meat_cooldown
        if last_meat is None:
            return -1
        next_meat = last_meat + meat_cooldown - Func.get_current_timestamp()
        return next_meat if next_meat > 0 else -1

    @staticmethod
    def get_time_of_next_meat(user_id):
        if Pig.get_time_to_next_meat(user_id) == -1:
            return Func.get_current_timestamp()
        return Func.get_current_timestamp() + Pig.get_time_to_next_meat(user_id)

    @staticmethod
    def add_weight(user_id, weight: float):
        pig = User.get_pig(user_id)
        pig['weight'] += weight
        pig['weight'] = round(pig['weight'], 1)
        if pig['weight'] <= .1:
            pig['weight'] = .1
        pig = json.dumps(pig, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {users_schema} SET pig = '{pig}' WHERE id = {user_id}"
        )

    @staticmethod
    def get_weight(user_id):
        pig = User.get_pig(user_id)
        return pig['weight']
