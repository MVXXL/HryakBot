import cProfile

from . import config
from .imports import *



shops_emojis = {
    'daily_shop': '🎨',
    'case_shop': '📦',
    'consumables_shop': '💊',
    'tools_shop': '🔪',
    'premium_skins_shop': '💵',
    'coins_shop': '🪙',
    'donation_shop': '🍩',
}

donate_coins_prices = {  # coins: real_currency
    'ru': {  # RUB
        750: 25.00,
        1550: 49.00,
        3300: 99.00,
        7200: 199.00,
        20000: 499.00,
    },
    'en': {  # USD
        750: 0.25,
        1550: 0.49,
        3300: 0.99,
        7200: 1.99,
        20000: 4.99,
    }}

language_currencies = {
    'ru': 'RUB',
    'en': 'USD'
}

amount_of_hollars_per_unit_of_real_currency = {
    'RUB': 1,
    'USD': 50,
    'UAH': 2
}

currency_to_usd = {
    'RUB': 90,
    'USD': 1,
    'UAH': 40
}

currency_symbols = {
    'RUB': '₽',
    'USD': '$',
    'UAH': '₴ (UAH)'
}

payment_methods_for_languages = {
    'ru': ['donatello'],
    'en': []
}

guild_settings = {'allow_say': False}
user_settings = {'language': 'en', 'blocked': False, 'block_reason': None, 'isolated': False, 'isolation_level': 0}
emotions_erase_cords = {'sad': [(668, 904, 855, 849, 734, 740),
                                (917, 842, 1150, 917, 1085, 734)],
                        'happy': [(695, 970, 865, 970, 865, 1030, 695, 1030),
                                  (1115, 985, 900, 985, 900, 1030, 1110, 1030)],
                        'angry': [(604, 498, 394, 658, 762, 832), (758, 842, 1220, 670, 840, 546)],
                        'sus': [(760, 786, 1268, 786, 1018, 426)],
                        'dont_care': [(328, 774, 732, 782, 654, 444),
                                      (760, 786, 1268, 786, 1018, 426)]}

ignore_users_in_top = [715575898388037676]

trade_data = {}

# embed colors
main_color = 0xc7604c
error_color = 0xc94312
warn_color = 0xe0bb36
success_color = 0x2fc256
premium_color = 0x61dfff

pig_ages = {
    0: '1',
    20: '2',
    50: '3',
    100: '4',
    300: '5',
    500: '6',
    1000: '7',
}

rarity_colors = {
    '1': 0x858784,
    '2': 0x45ff4b,
    '3': 0x4d9aff,
    '4': 0xc14dff,
    '5': 0xff3d33,
    '6': 0xffee54,
    'custom': 0xa8ffd5,
    'star': 0x17fffb,
    'exclusive': 0xffeb8a,
}

db_caches = {
    'user.get_inventory': TTLCache(maxsize=1000, ttl=600000),
    'user.get_settings': TTLCache(maxsize=1000, ttl=600000),
    'item.get_data': TTLCache(maxsize=1000, ttl=600000),
    'item.get_emoji': TTLCache(maxsize=1000, ttl=600000),
    'tech.__get_all_items': TTLCache(maxsize=1000, ttl=600000),
    'tech.get_all_items': TTLCache(maxsize=1000, ttl=600000)
}

pig_names = [
    {'en': ['Sleepy', 'Angry', 'Kind', 'Crazy', 'Drunk', 'High', 'Big', 'Stinky', 'Fat', 'Thin', 'Funny', 'Smart',
            'Dumb', 'Sexy', 'Chubby', 'Small', 'Large'],
     'ru': ['Грязный', 'Крутой', 'Сухой', 'Мокрый', 'Обкуренный', 'Мертвый', 'Вонючий', 'Сладкий', 'Непробиваемый',
            'Толстый', 'Тонкий', 'Смешной', 'Умный', 'Глупый', 'Сексуальный', 'Пухлый', 'Маленький', 'Большой']},
    {'en': ['Pig', 'Meat', 'Maxim', 'John', 'Jack', 'Chris', 'Anthony'],
     'ru': ['Хряк', 'Свин', 'Шашлык', 'Максим', 'Антон', 'Александр', 'Иван', 'Матвей', 'Даниил', 'Денис', 'Кирилл',
            'Дмитрий', 'Артем', 'Алексей', 'Егор', 'Станислав', 'Роман', 'Виктор', 'Илья', 'Никита', 'Владимир',
            'Михаил']},
]
