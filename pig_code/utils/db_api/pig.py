import datetime
import json

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

    @staticmethod
    def fix_pig_structure(user_id):
        pigs = User.get_pigs(user_id)
        fixed_pigs = pigs
        for pig_id in range(len(pigs)):
            for key in utils_config.default_pig:
                if key not in pigs[pig_id]:
                    pigs[pig_id][key] = utils_config.default_pig[key]
            pigs[pig_id]['weight'] = round(pigs[pig_id]['weight'], 1)
            for key in utils_config.default_pig['skins']:
                if key not in pigs[pig_id]['skins']:
                    pigs[pig_id]['skins'][key] = utils_config.default_pig['skins'][key]
            for key in utils_config.default_pig['genetic']:
                if key not in pigs[pig_id]['genetic']:
                    pigs[pig_id]['genetic'][key] = utils_config.default_pig['genetic'][key]
        Pig.replace_pigs(user_id, fixed_pigs)

    @staticmethod
    def create_pig_if_no_pigs(user_id):
        if not User.get_pigs(user_id):
            Pig.create(user_id)

    @staticmethod
    def replace_pigs(user_id, new_pigs):
        new_pigs = json.dumps(new_pigs, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {users_schema} SET pigs = '{new_pigs}' WHERE id = {user_id}"
        )

    @staticmethod
    def create(user_id, name: str = 'Hryak'):
        pigs = User.get_pigs(user_id)
        pigs.append(utils_config.default_pig)
        pigs[len(pigs) - 1]['name'] = name
        pigs = json.dumps(pigs, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {users_schema} SET pigs = '{pigs}' WHERE id = {user_id}"
        )

    @staticmethod
    def kill(user_id, pig_id):
        pigs = User.get_pigs(user_id)
        pigs.pop(pig_id)
        pigs = Func.correct_dict_id_order(pigs)
        pigs = json.dumps(pigs, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {users_schema} SET pigs = '{pigs}' WHERE id = {user_id}"
        )

    @staticmethod
    def rename(user_id, pig_id, name: str):
        pigs = User.get_pigs(user_id)
        pigs[pig_id]['name'] = name
        pigs = json.dumps(pigs, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {users_schema} SET pigs = '{pigs}' WHERE id = {user_id}"
        )

    @staticmethod
    def get_name(user_id, pig_id):
        pigs = User.get_pigs(user_id)
        return pigs[pig_id]['name']

    @staticmethod
    def get_genetic(user_id, pig_id, key):
        pigs = User.get_pigs(user_id)
        if key == 'all':
            return pigs[pig_id]['genetic']
        return pigs[pig_id]['genetic'][key]

    @staticmethod
    def set_skin(user_id, pig_id, skin):
        pigs = User.get_pigs(user_id)
        pigs[pig_id]['skins'][items[skin]['type'].split(':')[1]] = skin
        Pig.replace_pigs(user_id, pigs)

    @staticmethod
    def remove_skin(user_id, pig_id, skin_type):
        pigs = User.get_pigs(user_id)
        pigs[pig_id]['skins'][skin_type] = None
        Pig.replace_pigs(user_id, pigs)

    @staticmethod
    def get_skin(user_id, pig_id, key):
        pigs = User.get_pigs(user_id)
        if key == 'all':
            return pigs[pig_id]['skins']
        return pigs[pig_id]['skins'][key]

    @staticmethod
    def set_last_feed(user_id, pig_id, timestamp):
        pigs = User.get_pigs(user_id)
        pigs[pig_id]['last_feed'] = timestamp
        pigs = json.dumps(pigs, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {users_schema} SET pigs = '{pigs}' WHERE id = {user_id}"
        )

    @staticmethod
    def get_last_feed(user_id, pig_id):
        pigs = User.get_pigs(user_id)
        return pigs[pig_id]['last_feed']

    @staticmethod
    def get_time_to_next_feed(user_id, pig_id):
        last_feed = Pig.get_last_feed(user_id, pig_id)
        feed_cooldown = utils_config.pig_feed_cooldown if not User.has_premium(user_id) else utils_config.premium_pig_feed_cooldown
        if last_feed is None:
            return -1
        next_feed = last_feed + feed_cooldown - int(datetime.datetime.now().timestamp())
        return next_feed if next_feed > 0 else -1

    @staticmethod
    def get_time_of_next_feed(user_id, pig_id):
        if Pig.get_time_to_next_feed(user_id, pig_id) == -1:
            return int(datetime.datetime.now().timestamp())
        return int(datetime.datetime.now().timestamp()) + Pig.get_time_to_next_feed(user_id, pig_id)

    @staticmethod
    def add_weight(user_id, pig_id, weight: float):
        pigs = User.get_pigs(user_id)
        pigs[pig_id]['weight'] += weight
        pigs[pig_id]['weight'] = round(pigs[pig_id]['weight'], 1)
        if pigs[pig_id]['weight'] <= .1:
            pigs[pig_id]['weight'] = .1
        pigs = json.dumps(pigs, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {users_schema} SET pigs = '{pigs}' WHERE id = {user_id}"
        )

    @staticmethod
    def get_weight(user_id, pig_id):
        pigs = User.get_pigs(user_id)
        return pigs[pig_id]['weight']
