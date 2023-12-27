from .connection import Connection
from ...core import *
from ...core.config import users_schema, shop_schema, promo_code_schema, guilds_schema, families_schema, trades_schema, items_schema
from .user import User
from .item import Item

class Tech:

    @staticmethod
    def create_table(columns, schema):
        try:
            Connection.make_request(f"CREATE TABLE {schema} ({columns[0]})", commit=False)
        except mysql.connector.errors.ProgrammingError:
            pass
        try:
            Connection.make_request(f"ALTER TABLE {schema} CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;", commit=False)
        except mysql.connector.errors.ProgrammingError:
            pass
        for column in columns[1:]:
            try:
                Connection.make_request(f"ALTER TABLE {schema} ADD COLUMN {column}", commit=False)
            except Exception as e:
                pass
                # print(e)

    @staticmethod
    def create_user_table():
        columns = [
            'id varchar(32) PRIMARY KEY UNIQUE',
            'created int DEFAULT 0',
            "pig json",
            "inventory json",
            "stats json",
            "events json",
            "buy_history json",
            "logs json",
            "rating json",
            "settings json"
            # "language varchar(10) DEFAULT 'en'",
            # 'premium boolean DEFAULT FALSE',
            # 'blocked boolean DEFAULT FALSE',
            # 'blocked_promocodes boolean DEFAULT FALSE',
            # "block_reason varchar(512) DEFAULT ''",
            # 'family varchar(20)'
        ]
        Tech.create_table(columns, users_schema)

    @staticmethod
    def create_shop_table():
        columns = ['id int AUTO_INCREMENT PRIMARY KEY UNIQUE',
                   'timestamp varchar(32)',
                   'data json',
                   # 'static_shop json',
                   # 'daily_shop json',
                   # 'case_shop json'
                   ]
        Tech.create_table(columns, shop_schema)

    @staticmethod
    def create_promo_code_table():
        columns = ['id varchar(32) PRIMARY KEY UNIQUE',
                   'created varchar(32)',
                   'users_used json',
                   'max_uses int',
                   'prise json',
                   'expires_in int',
                   'can_use varchar(32)',
                   ]
        Tech.create_table(columns, promo_code_schema)

    @staticmethod
    def create_guild_table():
        columns = ['id varchar(32) PRIMARY KEY UNIQUE',
                   'joined int',
                   'settings json',
                   ]
        Tech.create_table(columns, guilds_schema)

    @staticmethod
    def create_families_table():
        columns = ['id int AUTO_INCREMENT PRIMARY KEY UNIQUE',
                   'name varchar(32)',
                   'description varchar(512)',
                   'members json',
                   'bans json',
                   'requests json',
                   'image varchar(512)',
                   'private boolean DEFAULT FALSE',
                   'ask_to_join boolean DEFAULT FALSE'
                   ]
        Tech.create_table(columns, families_schema)

    @staticmethod
    def create_trades_table():
        columns = ['id varchar(32) PRIMARY KEY UNIQUE',
                   'data json',
                   ]
        Tech.create_table(columns, trades_schema)

    @staticmethod
    def create_items_table():
        columns = ['id varchar(32) PRIMARY KEY UNIQUE',
                   'name json',
                   'description json',
                   'type varchar(32)',
                   'skin_type varchar(32)',
                   'not_compatible_skins json',
                   'not_draw_skins json',
                   'emoji varchar(32)',
                   'inventory_type varchar(32)',
                   'rarity varchar(32)',
                   'image_file LONGBLOB',
                   'image_file_2 LONGBLOB',
                   'cooked_item_id varchar(32)',
                   'market_price int',
                   'market_price_currency varchar(32)',
                   'shop_category varchar(32)',
                   'shop_cooldown json',
                   'buffs json',
                   'salable bool',
                   'sell_price int',
                   'sell_price_currency varchar(32)',
                   'tradable bool',
                   'case_drops json',
                   'requirements json',
                   ]
        Tech.create_table(columns, items_schema)

    @staticmethod
    def get_all_users(order_by: str = None, include_where: str = None, exclude_users: list = None, limit: int = None, guild: disnake.Guild = None):
        """
        :type order_by: object
            Example: JSON_EXTRACT(inventory, '$.coins.amount')
        :param include_where:
            Example: JSON_EXTRACT(inventory, '$.coins.amount') > 0
        """
        if exclude_users is None:
            exclude_users = []
        exclude_users = [str(i) for i in exclude_users]
        id_list = []
        connection = Connection.connect()
        query = f'SELECT id FROM {users_schema}'
        if include_where is not None:
            query += f" WHERE {include_where}"
        if exclude_users is not None and exclude_users:
            if include_where is not None:
                query += ' AND'
            else:
                query += f' WHERE'
            query += f" id NOT IN {tuple(exclude_users if len(exclude_users) > 1 else exclude_users[0])}"
        if order_by is not None:
            query += f" ORDER BY {order_by} DESC"
        if limit is not None and guild is None:
            query += f" LIMIT {limit}"
        with connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            for i in results:
                id_list.append(i[0])
        print('----------------------------------')
        if guild is not None:
            members_ids = [str(m.id) for m in guild.members]
            print(len(members_ids))
            print(len(id_list))
            id_list = [i for i in id_list if i in members_ids]
            print('----------------------------------')
            if limit is not None:
                id_list = id_list[:limit]
        return id_list


    @staticmethod
    def get_user_position(user_id, order_by: str = None, include_where: str = None, exclude_users: list = None, guild: disnake.Guild = None):
        users = Tech.get_all_users(order_by=order_by, include_where=include_where, exclude_users=exclude_users, guild=guild)
        if str(user_id) in users:
            return users.index(str(user_id))

    # @staticmethod
    # @cached(TTLCache(maxsize=1000, ttl=600000))
    # def get_all_users_cached(order_by: str = None, include_where: str = None, exclude_users: tuple = None, limit: int = None, guild: disnake.Guild = None):
    #     return Tech.get_all_users(order_by, include_where, exclude_users, limit, guild)

    @staticmethod
    def get_all_guilds():
        id_list = []
        connection = Connection.connect()
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id FROM {guilds_schema}")
            results = cursor.fetchall()
            for i in results:
                id_list.append(i[0])
        return id_list

    # @staticmethod
    # def get_users_sorted_by(sort_key, sort_key_params: dict = None, number: int = 100000, exclude: list = None, guild=None):
    #     if exclude is None:
    #         exclude = []
    #     if sort_key_params is None:
    #         sort_key_params = {}
    #     exclude = [str(i) for i in exclude]
    #     users = Tech.get_all_users()
    #     users = [i for i in users if i not in exclude]
    #     if guild is not None:
    #         guild_members_ids = [str(i.id) for i in guild.members]
    #         users = [i for i in users if i in guild_members_ids]
    #     users = sorted(users, key=lambda x: sort_key(user_id=x, **sort_key_params))
    #     return users[::-1][:number]

    @staticmethod
    @cached(utils_config.db_caches['tech.__get_all_items'])
    def __get_all_items(requirements: tuple = None, exceptions: tuple = None):
        text_conditions = ''
        if requirements is None:
            requirements = []
        if exceptions is None:
            exceptions = []
        requirements = dict(requirements)
        for k, v in requirements.items():
            text_conditions += f'{k} {"=" if v not in [None, False, True] else "IS"} %s AND '
        if exceptions is None:
            text_conditions = text_conditions[:-5]
        exceptions = dict(exceptions)
        for k, v in exceptions.items():
            text_conditions += f'{k} {"!=" if v not in [None, False, True] else "IS NOT"} %s AND '
        text_conditions = text_conditions[:-5]
        result = Connection.make_request(
            f"SELECT id FROM {items_schema}{f' WHERE {text_conditions}' if text_conditions else ''}",
            commit=False,
            fetch=True,
            fetchall=True,
            params=tuple([i for i in requirements.values()] + [i for i in exceptions.values()]) if requirements or exceptions else None
        )
        result = [i[0] for i in result]
        return result

    @staticmethod
    def clear_get___all_items_cache(params):
        try:
            utils_config.db_caches['tech.__get_all_items'].pop(params)
        except KeyError:
            pass

    @staticmethod
    # @cached(utils_config.db_caches['tech.get_all_items'])
    def get_all_items(requirements: tuple = None, exceptions: tuple = None, user_id=None):
        """
        :type requirements: object
            Example: (("rarity", "3"),) - it will return only items with rarity=3
        :param exceptions:
            Example: (("type", "skin"),) - it will return everything except items with type=skin
        :param user_id:
            If user_id is specified, it will return items that are present in the user's inventory
        """
        result = Tech.__get_all_items(requirements, exceptions)
        if user_id is not None:
            result = [i for i in result if Item.get_amount(i, user_id) > 0]
            Tech.clear_get_all_items_cache((requirements, exceptions, user_id))
        return result

    @staticmethod
    def clear_get_all_items_cache(params):
        try:
            utils_config.db_caches['tech.get_all_items'].pop(params)
        except KeyError:
            pass

    @staticmethod
    async def fix_settings_structure_for_all_users():
        users = Tech.get_all_users()
        for user in users:
            Tech.fix_settings_structure(user)
            await asyncio.sleep(0.1)

    @staticmethod
    def fix_settings_structure(user_id):
        settings = User.get_settings(user_id)
        if settings is None:
            settings = {}
        for key, value in utils_config.user_settings.items():
            if key not in settings:
                settings[key] = value
        User.set_new_settings(user_id, settings)
