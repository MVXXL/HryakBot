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
SDC_TOKEN = get_env('SDC_TOKEN')
BOTICORD_TOKEN = get_env('BOTICORD_TOKEN')
VERSION = '1.0'
TEST = True
ADMIN_GUILDS = get_env('TEST_ADMIN_GUILDS', list) if TEST else get_env('ADMIN_GUILDS', list)
TEST_GUILDS = get_env('TEST_GUILDS', list)
BOT_GUILD = int(get_env('BOT_GUILD'))
LOGS_PATH = get_env('LOGS_PATH')
TEST_LOGS_PATH = get_env('TEST_LOGS_PATH')
LOGS_PATH = LOGS_PATH if not TEST else TEST_LOGS_PATH

# webhooks
START_CHANNEL_WEBHOOK = get_env('START_CHANNEL_WEBHOOK')
DEBUGGER_WEBHOOK = get_env('DEBUGGER_WEBHOOK')
REPORT_WEBHOOK = get_env('REPORT_WEBHOOK')

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
promo_code_schema = 'promo_codes' if not TEST else 'test_promo_codes'

TOKEN = TOKEN if not TEST else TEST_TOKEN
