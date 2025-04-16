import os
from dotenv import load_dotenv
from .imports import *

load_dotenv()


def get_env(key, value_type=None):
    value = os.getenv(key)
    if value_type:
        if value_type == list:
            return eval(value)
        return value_type(value)
    return value


TOKEN = get_env('TOKEN')
TEST_TOKEN = get_env('TEST_TOKEN')
TEST = True
HOSTING_TYPE = 'pc' if not TEST else None
ADMIN_GUILDS = get_env('ADMIN_GUILDS', list)
TEST_GUILDS = get_env('TEST_GUILDS', list)
PUBLIC_TEST_GUILDS = get_env('PUBLIC_TEST_GUILDS', list)
DEVELOPER_USERNAME = get_env('DEVELOPER_USERNAME')

SDC_TOKEN = get_env('SDC_TOKEN')  # https://bots.server-discord.com/
IMGBB_TOKEN = get_env('IMGBB_TOKEN')  # https://api.imgbb.com/
THUMBSNAP_TOKEN = get_env('THUMBSNAP_TOKEN')  # https://thumbsnap.com/
BOTICORD_TOKEN = get_env('BOTICORD_TOKEN')  # https://boticord.top/

# github version
GITHUB_PUBLIC_VERSION = True  # don't change this line

# support guild config

RU_BOT_GUILD_ID = int(get_env('RU_BOT_GUILD'))
EN_BOT_GUILD_ID = int(get_env('EN_BOT_GUILD'))

BOT_GUILDS = {RU_BOT_GUILD_ID: {'type': 'ru.main',
                                'url': get_env('RU_BOT_GUILD_URL'),
                                'guild_count_channel': int(get_env('RU_BOT_STATS_CHANNEL')),
                                # id of a channel (has to be a voice channel)
                                'halyava_channel': int(get_env('RU_BOT_HALYAVA_CHANNEL')),  # id of a channel
                                'not_verified_role': int(get_env('RU_NOT_VERIFIED_ROLE'))},  # id of a role
              EN_BOT_GUILD_ID: {'type': 'en.main',
                                'url': get_env('EN_BOT_GUILD_URL')}}

BOT_AUTH_LINK = get_env('BOT_AUTH_LINK')

BOT_STATS_CHANNEL = int(get_env('RU_BOT_STATS_CHANNEL'))  # id of a channel (has to be a voice channel)
BOT_HALYAVA_CHANNEL = int(get_env('RU_BOT_HALYAVA_CHANNEL'))  # id of a channel

# users
PROMOCODERS = get_env('PROMOCODERS', list)  # users who are able to create promocodes
HALYAVERS = get_env('HALYAVERS', list)  # users who are able to give rewards in "halyava" channel

# paths
TEMP_FOLDER_PATH = get_env('TEMP_FOLDER_PATH')
IMAGES_FOLDER_PATH = f'bin/images'
INIT_DATA_PATH = get_env('INIT_DATA_PATH')
LOGS_PATH = get_env('LOGS_PATH') if not TEST else get_env('TEST_LOGS_PATH')

# webhooks
DEBUGGER_WEBHOOK = get_env('DEBUGGER_WEBHOOK')
REPORT_WEBHOOKS = get_env('REPORT_WEBHOOKS', list)

# db
mysql_info = {
    'host': get_env('DB_HOST'),
    'port': get_env('DB_PORT', int),
    'user': get_env('DB_USER'),
    'password': get_env('DB_PASSWORD'),
    'database': get_env('DB_NAME') if not TEST else get_env('TEST_DB_NAME')
}

if TEST:
    TOKEN = TEST_TOKEN
else:
    TOKEN = TOKEN

# ------------------ not private --------------------

from hryak.config import users_schema, promocodes_schema, shop_schema, guilds_schema
from hryak import setters

hryak.db_api.pool.create_pool(
    host=mysql_info['host'],
    port=mysql_info['port'],
    user=mysql_info['user'],
    password=mysql_info['password'],
    database=mysql_info['database']
)
setters.set_logs_path(LOGS_PATH)
setters.set_test_mode(TEST)
setters.set_bot_guilds(BOT_GUILDS)
setters.set_temp_folder_path(TEMP_FOLDER_PATH)
if TEST:
    setters.set_pig_feed_cooldown(5)
    setters.set_pig_butcher_cooldown(15)
    setters.set_streak_timeout(30)

# embed colors
main_color = 0xc7604c
error_color = 0xc94312
warn_color = 0xe0bb36
success_color = 0x2fc256
premium_color = 0x61dfff
