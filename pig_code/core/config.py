import os
from dotenv import load_dotenv

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
PUBLIC_TEST_TOKEN = get_env('PUBLIC_TEST_TOKEN')
TEST = True
PUBLIC_TEST = False
HOSTING_TYPE = 'pc'
ADMIN_GUILDS = get_env('ADMIN_GUILDS', list)
TEST_GUILDS = get_env('TEST_GUILDS', list)
PUBLIC_TEST_GUILDS = get_env('PUBLIC_TEST_GUILDS', list)
DEVELOPER_USERNAME = get_env('DEVELOPER_USERNAME')

SDC_TOKEN = get_env('SDC_TOKEN')  # https://bots.server-discord.com/
IMGBB_TOKEN = get_env('IMGBB_TOKEN')  # https://api.imgbb.com/
THUMBSNAP_TOKEN = get_env('THUMBSNAP_TOKEN')  # https://thumbsnap.com/
BOTICORD_TOKEN = get_env('BOTICORD_TOKEN')  # https://boticord.top/

# github version
GITHUB_PUBLIC_VERSION = False  # don't change this line

# support guild config

RU_BOT_GUILD_ID = int(get_env('RU_BOT_GUILD'))
EN_BOT_GUILD_ID = int(get_env('EN_BOT_GUILD'))

BOT_GUILDS = {RU_BOT_GUILD_ID: {'type': 'ru.main',
                                'url': get_env('RU_BOT_GUILD_URL'),
                                'guild_count_channel': int(get_env('RU_BOT_STATS_CHANNEL')),  # id of a channel (has to be a voice channel)
                                'halyava_channel': int(get_env('RU_BOT_HALYAVA_CHANNEL')),  # id of a channel
                                'not_verified_role': int(get_env('RU_NOT_VERIFIED_ROLE'))},  # id of a role
              EN_BOT_GUILD_ID: {'type': 'en.main',
                                'url': get_env('EN_BOT_GUILD_URL')}}

BOT_AUTH_LINK = get_env('BOT_AUTH_LINK')

BOT_STATS_CHANNEL = int(get_env('RU_BOT_STATS_CHANNEL'))  # id of a channel (has to be a voice channel)
BOT_HALYAVA_CHANNEL = int(get_env('RU_BOT_HALYAVA_CHANNEL'))  # id of a channel

# users
PROMOCODERS = get_env('PROMOCODERS', list)  # users who are able to create promocodes
HALYAVERS = get_env('HALYAVERS', list)  # users who are able to give prises in "halyava" channel

# paths
TEMP_FOLDER_PATH = get_env('TEMP_FOLDER_PATH')
IMAGE_FOLDER_PATH = f'bin/images'
INIT_DATA_PATH = get_env('INIT_DATA_PATH') if not PUBLIC_TEST else get_env('TEST_INIT_DATA_PATH')
LOGS_PATH = get_env('LOGS_PATH') if not TEST else get_env('TEST_LOGS_PATH')

# aaio | https://aaio.so/
AAIO_API_KEY = get_env('AAIO_API_KEY')
AAIO_MERCHANT_ID = get_env('AAIO_MERCHANT_ID')
AAIO_SECRET1 = get_env('AAIO_SECRET1')
AAIO_SECRET2 = get_env('AAIO_SECRET2')

# webhooks
START_CHANNEL_WEBHOOK = get_env('START_CHANNEL_WEBHOOK')
DEBUGGER_WEBHOOK = get_env('DEBUGGER_WEBHOOK')
REPORT_WEBHOOKS = get_env('REPORT_WEBHOOKS', list)

# db
mysql_info = {
    'host': get_env('DB_HOST'),
    'port': get_env('DB_PORT', int),
    'user': get_env('DB_USER'),
    'password': get_env('DB_PASSWORD'),
    'database': get_env('DB_NAME')
}

users_schema = 'users' if not TEST else 'test_users'
guilds_schema = 'guilds' if not TEST else 'test_guilds'
shop_schema = 'shop' if not TEST else 'test_shop'
promocode_schema = 'promo_codes' if not TEST else 'test_promo_codes'

if PUBLIC_TEST:
    TOKEN = PUBLIC_TEST_TOKEN
elif TEST:
    TOKEN = TEST_TOKEN
else:
    TOKEN = TOKEN
