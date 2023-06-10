import json

import mysql.connector

from .connection import Connection
from ...core import *
from ...core.config import users_schema
from .tech import Tech


class Stats:

    @staticmethod
    def fix_stats_structure_for_all_users():
        users = Tech.get_all_users()
        for user in users:
            Stats.fix_stats_structure(user)

    @staticmethod
    def fix_stats_structure(user_id):
        stats = Stats.get_stats(user_id)
        if stats is None:
            stats = {}
        for key, value in utils_config.stats.items():
            if key not in stats:
                stats[key] = value
        Stats.set_stats(user_id, stats)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_stats(user_id):
        result = Connection.make_request(
            f"SELECT stats FROM {users_schema} WHERE id = {user_id}",
            commit=False,
            fetch=True,
        )
        if result is not None:
            return json.loads(result)
        else:
            return {}

    @staticmethod
    def set_stats(user_id, new_stats):
        new_stats = json.dumps(new_stats, ensure_ascii=False)
        Connection.make_request(
            f"UPDATE {users_schema} SET stats = '{new_stats}' WHERE id = {user_id}"
        )

    @staticmethod
    def add_pig_fed(user_id, amount: int = 1):
        stats = Stats.get_stats(user_id)
        stats['pig_fed'] += amount
        Stats.set_stats(user_id, stats)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_pig_fed(user_id):
        stats = Stats.get_stats(user_id)
        return stats['pig_fed']

    @staticmethod
    def add_money_earned(user_id, amount: int = 1):
        stats = Stats.get_stats(user_id)
        stats['money_earned'] += amount
        Stats.set_stats(user_id, stats)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_money_earned(user_id):
        stats = Stats.get_stats(user_id)
        return stats['money_earned']

    @staticmethod
    def add_commands_used(user_id, command, amount: int = 1):
        stats = Stats.get_stats(user_id)
        if command in stats['commands_used']:
            stats['commands_used'][command] += amount
        else:
            stats['commands_used'][command] = amount
        Stats.set_stats(user_id, stats)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_commands_used(user_id, command):
        stats = Stats.get_stats(user_id)
        if command in stats['commands_used']:
            return stats['commands_used'][command]
        return 0

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_total_commands_used(user_id):
        stats = Stats.get_stats(user_id)
        total_commands_used = 0
        for i in stats['commands_used']:
            total_commands_used += stats['commands_used'][i]
        return total_commands_used

    @staticmethod
    def add_items_used(user_id, item, amount: int = 1):
        stats = Stats.get_stats(user_id)
        if item in stats['items_used']:
            stats['items_used'][item] += amount
        else:
            stats['items_used'][item] = amount
        Stats.set_stats(user_id, stats)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_items_used(user_id, item):
        stats = Stats.get_stats(user_id)
        if item in stats['items_used']:
            return stats['items_used'][item]
        return 0

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_total_items_used(user_id):
        stats = Stats.get_stats(user_id)
        total_items_used = 0
        for i in stats['items_used']:
            total_items_used += stats['items_used'][i]
        return total_items_used

    @staticmethod
    def add_items_sold(user_id, item, amount: int = 1):
        stats = Stats.get_stats(user_id)
        if item in stats['items_sold']:
            stats['items_sold'][item] += amount
        else:
            stats['items_sold'][item] = amount
        Stats.set_stats(user_id, stats)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_items_sold(user_id, item):
        stats = Stats.get_stats(user_id)
        if item in stats['items_sold']:
            return stats['items_sold'][item]
        return 0

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_total_items_sold(user_id):
        stats = Stats.get_stats(user_id)
        total_items_sold = 0
        for i in stats['items_sold']:
            total_items_sold += stats['items_sold'][i]
        return total_items_sold

    @staticmethod
    def set_language_changed(user_id, language_changed: bool):
        stats = Stats.get_stats(user_id)
        stats['language_changed'] = language_changed
        Stats.set_stats(user_id, stats)

    @staticmethod
    # @cached(TTLCache(maxsize=utils_config.db_api_cash_size, ttl=utils_config.db_api_cash_ttl))
    def get_language_changed(user_id):
        stats = Stats.get_stats(user_id)
        return stats['language_changed']
