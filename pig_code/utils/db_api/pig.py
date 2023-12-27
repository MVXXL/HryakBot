import time

from .connection import Connection
from .tech import Tech
from .user import User
from ..functions import Func
from ...core import *
from ...core.config import users_schema
from .item import Item


class Pig:

    @staticmethod
    async def fix_pig_structure_for_all_users():
        users = Tech.get_all_users()
        for user in users:
            Pig.fix_pig_structure(user)
            await asyncio.sleep(0.1)
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
            f"UPDATE {users_schema} SET pig = %s WHERE id = {user_id}", (new_pig,)
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
    def remove_buff(user_id, buff, amount: int = 1):
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
    def set_skin(user_id, item_id):
        pig = User.get_pig(user_id)
        pig['skins'][Item.get_skin_type(item_id)] = item_id
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
        pig[f'{action}_history'].append(timestamp)
        Pig.update_pig(user_id, pig)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def _get_last_action(user_id, action):
        pig = User.get_pig(user_id)
        last_action = None
        if len(pig[f'{action}_history']) > 0:
            last_action = pig[f'{action}_history'][-1]
        return last_action

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def _get_action_history(user_id, action):
        pig = User.get_pig(user_id)
        return pig[f'{action}_history']

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def _get_time_to_next_action(user_id, action):
        last_action = Pig._get_last_action(user_id, action)
        cooldown = 1000000
        if action == 'feed':
            cooldown = utils_config.pig_feed_cooldown
        if action == 'meat':
            cooldown = utils_config.pig_meat_cooldown
        if action == 'breed':
            cooldown = utils_config.pig_breed_cooldown
        # primal_cooldown = cooldown
        # cont = True
        # while cont:
        #     for i in range(
        #             Func.check_consecutive_timestamps(Pig._get_action_history(user_id, action)[-30:], 5, cooldown * 1.5,
        #                                               cooldown)):
        #         cooldown += cooldown // 2
        #     if Func.check_consecutive_timestamps(Pig._get_action_history(user_id, action)[-30:], 5, cooldown * 1.5,
        #                                          cooldown) == 0 or \
        #             cooldown > 12 * 3600:
        #         cont = False
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
        Pig._set_last_action(user_id, timestamp, 'feed')

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_last_feed(user_id):
        return Pig._get_last_action(user_id, 'feed')

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_feed_history(user_id):
        return Pig._get_action_history(user_id, 'feed')

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_time_to_next_feed(user_id):
        return Pig._get_time_to_next_action(user_id, 'feed')

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_time_of_next_feed(user_id):
        return Pig._get_time_of_next_action(user_id, 'feed')

    @staticmethod
    def set_last_meat(user_id, timestamp):
        Pig._set_last_action(user_id, timestamp, 'meat')

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_last_meat(user_id):
        return Pig._get_last_action(user_id, 'meat')

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_meat_history(user_id):
        return Pig._get_action_history(user_id, 'meat')

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_time_to_next_meat(user_id):
        return Pig._get_time_to_next_action(user_id, 'meat')

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_time_of_next_meat(user_id):
        return Pig._get_time_of_next_action(user_id, 'meat')

    @staticmethod
    def set_last_breed(user_id, timestamp):
        Pig._set_last_action(user_id, timestamp, 'breed')

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_last_breed(user_id):
        return Pig._get_last_action(user_id, 'breed')

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_breed_history(user_id):
        return Pig._get_action_history(user_id, 'breed')

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_time_to_next_breed(user_id):
        return Pig._get_time_to_next_action(user_id, 'breed')

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_time_of_next_breed(user_id):
        return Pig._get_time_of_next_action(user_id, 'breed')

    @staticmethod
    def add_weight(user_id, weight: float):
        pig = User.get_pig(user_id)
        pig['weight'] += weight
        pig['weight'] = round(pig['weight'], 1)
        if pig['weight'] <= .1:
            pig['weight'] = .1
        Pig.update_pig(user_id, pig)

    @staticmethod
    def get_weight(user_id):
        if type(user_id) != list:
            pig = User.get_pig(user_id)
            return pig['weight']
        else:
            weight = 0
            pigs = User.get_pig(user_id)
            for pig in pigs.values():
                weight += pig['weight']
            return weight

    @staticmethod
    def age(user_id, lang=None):
        weight = Pig.get_weight(user_id)
        max_age = '1'
        for age in utils_config.pig_ages:
            if weight >= age:
                max_age = utils_config.pig_ages[age]
            else:
                break
        if lang is None:
            return max_age
        else:
            return Locales.PigAges[max_age][lang]

    # @staticmethod
    # # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    # def make_pregnant(user_id, pregnant_by_id, pregnant_with_id):
    #     pig = User.get_pig(user_id)
    #     pig['pregnant_time'] = Func.get_current_timestamp()
    #     pig['pregnant_with'] = pregnant_with_id
    #     pig['pregnant_by'] = pregnant_by_id
    #     pig['pregnancy_duration'] = items[pregnant_with_id]['pregnancy_duration']
    #     Pig.update_pig(user_id, pig)
    #
    # @staticmethod
    # # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    # def pregnant_by(user_id):
    #     pig = User.get_pig(user_id)
    #     return pig['pregnant_by']
    #
    # @staticmethod
    # # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    # def pregnant_time(user_id):
    #     pig = User.get_pig(user_id)
    #     return pig['pregnant_time']
    #
    # @staticmethod
    # # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    # def pregnant_with(user_id):
    #     pig = User.get_pig(user_id)
    #     return pig['pregnant_with']
    #
    # @staticmethod
    # # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    # def pregnancy_duration(user_id):
    #     pig = User.get_pig(user_id)
    #     return pig['pregnancy_duration']
    #
    # @staticmethod
    # # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    # def disable_pregnant(user_id):
    #     pig = User.get_pig(user_id)
    #     pig['pregnant_time'] = None
    #     Pig.update_pig(user_id, pig)
    #
    # @staticmethod
    # # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    # def is_pregnant(user_id):
    #     pig = User.get_pig(user_id)
    #     if pig['pregnant_time'] is not None:
    #         return True
    #     return False
