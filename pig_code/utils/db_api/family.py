import random

from .connection import Connection
from .tech import Tech
from .user import User
from ..functions import Func
from ...core import *
from ...core.config import families_schema


class Family:
    pass

    @staticmethod
    def create(name, owner_id, description: str = '', image: str = '',
               private: bool = False, ask_to_join: bool = False):
        private = 1 if private else 0
        ask_to_join = 1 if ask_to_join else 0
        while True:
            family_id = random.randrange(10000, 99999)
            if Family.exists(family_id):
                continue
            Connection.make_request(
                f"INSERT INTO {families_schema} (id, name, description, image, private, ask_to_join, members, bans, requests) "
                f"VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                params=(family_id, name, description, image, private, ask_to_join, '{}', '{}', '{}')
            )
            Family.add_member(family_id, owner_id, 'owner')
            break
        return family_id

    @staticmethod
    def delete(family_id):
        Connection.make_request(f"DELETE FROM {families_schema} WHERE id = {family_id}")

    @staticmethod
    def update_members(family_id, new_family):
        new_family = json.dumps(new_family, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {families_schema} SET members = %s WHERE id = {family_id}", (new_family,)
        )

    @staticmethod
    def add_member(family_id, user_id, role: str = 'member'):
        print(family_id)
        members = Family.get_members(int(family_id))
        members[str(user_id)] = {'role': role}
        Family.update_members(family_id, members)
        User.set_family(user_id, family_id)

    @staticmethod
    def remove_member(family_id, user_id):
        members = Family.get_members(int(family_id))
        print(user_id)
        print(members)
        members.pop(str(user_id))
        Family.update_members(family_id, members)
        User.set_family(user_id, None)

    @staticmethod
    def get_member_role(family_id, user_id):
        member = Family.get_member(int(family_id), user_id)
        if member is not None:
            return member['role']

    @staticmethod
    def get_member(family_id, user_id):
        members = Family.get_members(int(family_id))
        if str(user_id) in members:
            return members[str(user_id)]

    @staticmethod
    def get_owner(family_id):
        members = Family.get_members(int(family_id))
        for member in members:
            if members[member]['role'] == 'owner':
                return member

    @staticmethod
    def update_member(family_id, user_id, role):
        members = Family.get_members(int(family_id))
        if user_id in members:
            Family.add_member(family_id, user_id, role)

    @staticmethod
    def get_members(family_id):
        result = Connection.make_request(
            f"SELECT members FROM {families_schema} WHERE id = {family_id}",
            commit=False,
            fetch=True,
        )
        if result is not None:
            return json.loads(result)
        else:
            return {}

    @staticmethod
    def exists(family_id):
        result = Connection.make_request(
            f"SELECT EXISTS(SELECT 1 FROM {families_schema} WHERE id = %s)", params=(family_id,),
            commit=False,
            fetch=True
        )
        return bool(result)

    @staticmethod
    def is_private(family_id):
        result = Connection.make_request(
            f"SELECT private FROM {families_schema} WHERE id = {family_id}",
            commit=False,
            fetch=True
        )
        return bool(result)

    @staticmethod
    def set_private(family_id, private: bool):
        private = 1 if private else 0
        Connection.make_request(
            f"UPDATE {families_schema} SET premium = '{private}' WHERE id = {family_id}"
        )

    @staticmethod
    def is_ask_to_join(family_id):
        result = Connection.make_request(
            f"SELECT ask_to_join FROM {families_schema} WHERE id = {family_id}",
            commit=False,
            fetch=True
        )
        return bool(result)

    @staticmethod
    def set_ask_to_join(family_id, ask_to_join: bool):
        ask_to_join = 1 if ask_to_join else 0
        Connection.make_request(
            f"UPDATE {families_schema} SET premium = '{ask_to_join}' WHERE id = {family_id}"
        )

    @staticmethod
    def get_name(family_id):
        result = Connection.make_request(
            f"SELECT name FROM {families_schema} WHERE id = {family_id}",
            commit=False,
            fetch=True
        )
        return result

    @staticmethod
    def set_name(family_id, name: str):
        Connection.make_request(
            f"UPDATE {families_schema} SET name = %s WHERE id = {family_id}", params=(name, )
        )

    @staticmethod
    def get_description(family_id):
        result = Connection.make_request(
            f"SELECT description FROM {families_schema} WHERE id = {family_id}",
            commit=False,
            fetch=True
        )
        return result

    @staticmethod
    def set_description(family_id, description: str):
        Connection.make_request(
            f"UPDATE {families_schema} SET description = %s WHERE id = {family_id}", params=(description, )
        )

    @staticmethod
    def get_image(family_id):
        result = Connection.make_request(
            f"SELECT image FROM {families_schema} WHERE id = {family_id}",
            commit=False,
            fetch=True
        )
        return result

    @staticmethod
    def set_image(family_id, url: str):
        Connection.make_request(
            f"UPDATE {families_schema} SET image = %s WHERE id = {family_id}", params=(url, )
        )

    @staticmethod
    def get_requests(family_id):
        result = Connection.make_request(
            f"SELECT requests FROM {families_schema} WHERE id = {family_id}",
            commit=False,
            fetch=True,
        )
        if result is not None:
            return json.loads(result)
        else:
            return {}

    @staticmethod
    def get_request_timestamp(family_id, user_id):
        _requests = Family.get_requests(family_id)
        if str(user_id) in _requests:
            return _requests[str(user_id)]['timestamp']

    @staticmethod
    def update_requests(family_id, new_requests):
        new_requests = json.dumps(new_requests, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {families_schema} SET requests = %s WHERE id = {family_id}", (new_requests,)
        )

    @staticmethod
    def add_request(family_id, user_id):
        _requests = Family.get_requests(int(family_id))
        _requests[str(user_id)] = {}
        _requests[str(user_id)]['timestamp'] = Func.get_current_timestamp()
        Family.update_requests(family_id, _requests)

    @staticmethod
    def remove_request(family_id, user_id):
        _requests = Family.get_requests(int(family_id))
        if str(user_id) in _requests:
            _requests.pop(str(user_id))
            Family.update_requests(family_id, _requests)

    # @staticmethod
    # def register(guild_id):
    #     settings = json.dumps(utils_config.guild_settings)
    #     Connection.make_request(
    #         f"INSERT INTO {guilds_schema} (id, joined, settings) "
    #         f"VALUES ('{guild_id}', '{Func.get_current_timestamp()}', '{settings}')"
    #     )
    #
    # @staticmethod
    # def exists(guild_id):
    #     result = Connection.make_request(
    #         f"SELECT EXISTS(SELECT 1 FROM {guilds_schema} WHERE id = {guild_id})",
    #         commit=False,
    #         fetch=True
    #     )
    #     return bool(result)
    #
    # @staticmethod
    # def fix_settings_structure_for_all_guilds():
    #     guilds = Tech.get_all_guilds()
    #     for guild in guilds:
    #         Guild.fix_settings_structure(guild)
    #
    # @staticmethod
    # def fix_settings_structure(guild_id):
    #     settings = Guild.get_settings(guild_id)
    #     if settings is None:
    #         settings = {}
    #     for key, value in utils_config.guild_settings.items():
    #         if key not in settings:
    #             settings[key] = value
    #     Guild.set_settings(guild_id, settings)
    #
    # @staticmethod
    # # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    # def get_settings(guild_id):
    #     result = Connection.make_request(
    #         f"SELECT settings FROM {guilds_schema} WHERE id = {guild_id}",
    #         commit=False,
    #         fetch=True,
    #     )
    #     if result is not None:
    #         return json.loads(result)
    #     else:
    #         return {}
    #
    # @staticmethod
    # def set_settings(guild_id, new_settings):
    #     new_settings = json.dumps(new_settings, ensure_ascii=False)
    #     Connection.make_request(
    #         f"UPDATE {guilds_schema} SET settings = %s WHERE id = {guild_id}", (new_settings, )
    #     )
    #
    # @staticmethod
    # def set_join_channel(guild_id, channel_id):
    #     settings = Guild.get_settings(guild_id)
    #     settings['join_channel'] = channel_id
    #     Guild.set_settings(guild_id, settings)
    #
    # @staticmethod
    # def join_channel(guild_id):
    #     settings = Guild.get_settings(guild_id)
    #     return settings['join_channel']
    #
    # @staticmethod
    # def set_join_message(guild_id, message):
    #     settings = Guild.get_settings(guild_id)
    #     settings['join_message'] = message
    #     Guild.set_settings(guild_id, settings)
    #
    # @staticmethod
    # def join_message(guild_id):
    #     settings = Guild.get_settings(guild_id)
    #     return settings['join_message']
    #
    # @staticmethod
    # # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    # def joined(guild_id):
    #     result = Connection.make_request(
    #         f"SELECT joined FROM {guilds_schema} WHERE id = {guild_id}",
    #         commit=False,
    #         fetch=True,
    #     )
    #     if result is not None:
    #         return json.loads(result)
    #     else:
    #         return {}
