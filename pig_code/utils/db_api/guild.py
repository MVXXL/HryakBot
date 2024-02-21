from .connection import Connection
from .tech import Tech
from ..functions import Func
from ...core import *
from ...core.config import guilds_schema


class Guild:

    @staticmethod
    def register_guild_if_not_exists(guild_id):
        if not Guild.exists(guild_id):
            Guild.register(guild_id)

    @staticmethod
    def register(guild_id):
        executemany = False
        if type(guild_id) == list:
            executemany = True
            guild_id = tuple([(guild,) for guild in guild_id])
        settings = json.dumps(utils_config.guild_settings)
        Connection.make_request(
            f"INSERT{' IGNORE' if executemany else ''} INTO {guilds_schema} (id, joined, settings) "
            f"VALUES (%s, '{Func.get_current_timestamp()}', '{settings}')",
            params=guild_id,
            executemany=executemany
        )

    @staticmethod
    def exists(guild_id):
        result = Connection.make_request(
            f"SELECT EXISTS(SELECT 1 FROM {guilds_schema} WHERE id = {guild_id})",
            commit=False,
            fetch=True
        )
        return bool(result)

    @staticmethod
    async def fix_settings_structure_for_all_guilds():
        guilds = Tech.get_all_guilds()
        for guild in guilds:
            Guild.fix_settings_structure(guild)
            await asyncio.sleep(.1)

    @staticmethod
    def fix_settings_structure(guild_id):
        settings = Guild.get_settings(guild_id)
        if settings is None:
            settings = {}
        for key, value in utils_config.guild_settings.items():
            if key not in settings:
                settings[key] = value
        Guild.set_settings(guild_id, settings)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_settings(guild_id):
        result = Connection.make_request(
            f"SELECT settings FROM {guilds_schema} WHERE id = {guild_id}",
            commit=False,
            fetch=True,
        )
        if result is not None:
            return json.loads(result)
        else:
            return {}

    @staticmethod
    def set_settings(guild_id, new_settings):
        new_settings = json.dumps(new_settings, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {guilds_schema} SET settings = %s WHERE id = {guild_id}", (new_settings, )
        )

    @staticmethod
    def set_join_channel(guild_id, channel_id):
        settings = Guild.get_settings(guild_id)
        settings['join_channel'] = channel_id
        Guild.set_settings(guild_id, settings)

    @staticmethod
    def join_channel(guild_id):
        settings = Guild.get_settings(guild_id)
        return settings['join_channel']

    @staticmethod
    def set_join_message(guild_id, message):
        settings = Guild.get_settings(guild_id)
        settings['join_message'] = message
        Guild.set_settings(guild_id, settings)

    @staticmethod
    def join_message(guild_id):
        settings = Guild.get_settings(guild_id)
        return settings['join_message']

    @staticmethod
    def is_say_allowed(guild_id):
        settings = Guild.get_settings(guild_id)
        return settings['allow_say']

    @staticmethod
    def allow_say(guild_id, allow: bool = True):
        settings = Guild.get_settings(guild_id)
        settings['allow_say'] = allow
        Guild.set_settings(guild_id, settings)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def joined(guild_id):
        result = Connection.make_request(
            f"SELECT joined FROM {guilds_schema} WHERE id = {guild_id}",
            commit=False,
            fetch=True,
        )
        if result is not None:
            return json.loads(result)
        else:
            return {}
