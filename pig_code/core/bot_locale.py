import re
import string

from disnake import Locale
from googletrans import Translator

from . import config

valid_discord_locales = ['en', 'ru']

full_names = {'en': 'English',
              'ru': 'Russian | Pусский',
              'uk': 'Ukrainian | Українська'}

big_texts = {

}

locales = {
    'set_language': {'description': {Locale.en_US: 'Change bot language',
                                     Locale.ru: 'Изменить язык бота'},
                     'language_var_name': {Locale.en_US: 'language',
                                           Locale.ru: 'язык'},
                     'scd_title': {'en': 'New bot language: **English**',
                                   'ru': 'Новый язык бота: **Русский**'},
                     'scd_desc': {'en': 'Now the bot will speak the freedom language 🦅🦅',
                                  'ru': 'Теперь бот будет говорить на великом и могучем 💪'}
                     },
    'profile': {'description': {Locale.en_US: 'View your profile',
                                Locale.ru: 'Посмотреть свой профиль'},
                'profile_title': {'en': 'User\'s profile',
                                  'ru': 'Профиль игрока'},
                'profile_desc': {'en': 'Balance: **{balance}** 🪙',
                                 'ru': 'Баланс: **{balance}** 🪙'},
                'pig_field_title': {'en': 'Pig',
                                    'ru': 'Свинтус'},
                'pig_field_value': {'en': 'Pig name: **{pig_name}**\n'
                                          'Weight: **{weight}** kg',
                                    'ru': 'Имя хряка: **{pig_name}**\n'
                                          'Вес: **{weight}** кг'}
                },
    'inventory': {'description': {Locale.en_US: 'View your inventory',
                                  Locale.ru: 'Посмотреть свой инвентарь'},
                  'inventory_title': {'en': 'Inventory',
                                      'ru': 'Инвентарь'},
                  'inventory_empty_desc': {'en': '*Your inventory is empty*',
                                           'ru': '*Ваш инвентарь пуст*'},
                  'select_item_placeholder': {'en': 'Choose item',
                                              'ru': 'Выберите предмет'}
                  },
    'inventory_item_selected': {'title': {'en': '{item}',
                                          'ru': '{item}'},
                                'desc': {'en': 'Amount: **{amount}**\n'
                                               'Type: **{type}**\n'
                                               'Price/pcs: `{cost}` 🪙\n',
                                         'ru': 'Количество: **{amount}**\n'
                                               'Тип: **{type}**\n'
                                               'Цена/шт: `{cost}` 🪙\n'}
                                },
    'inventory_item_sell_modal': {'label': {'en': 'Amount of items to sell',
                                            'ru': 'Количество предметов для продажи'},
                                  'placeholder': {'en': 'You have: {max_amount}',
                                                  'ru': 'У вас есть: {max_amount}'},
                                  'title': {'en': 'Item selling',
                                            'ru': 'Продажа'
                                            }},
    'inventory_item_sold': {'title': {'en': 'Item sold',
                                      'ru': 'Предмет продан'},
                            'desc': {'en': 'You sold **{item} x{amount}** and received **{money}** 🪙',
                                     'ru': 'Вы продали **{item} x{amount}** и получили **{money}** 🪙'}
                            },
    'feed': {'description': {Locale.en_US: 'Feed your pig',
                             Locale.ru: 'Накормить своего хряка'},
             'feed_title': {'en': 'You fed your pig',
                            'ru': 'Вы покормили своего хряка'},
             'feed_scd_desc_list': {'en': ['**{pig}** recovered by **{mass}** kg'],
                                    'ru': ['**{pig}** поправился на **{mass}** кг']},
             'feed_fail_desc_list': {'en': ['Your **{pig}** vomited and he lost **{mass}** kg'],
                                     'ru': ['Вашего **{pig}** стошнило и он похудел на **{mass}** кг']},
             'pig_pooped_desc_list': {'en': ['**{pig}** pooped and you got **{poop}** 💩'],
                                      'ru': ['**{pig}** покакал и вы получили **{poop}** 💩']},
             'total_pig_weight': {'en': 'Weight of your pig: **{weight}** kg',
                                  'ru': 'Масса твоего хряка: **{weight}** кг'}
             },
    'rename': {'description': {Locale.en_US: 'Rename your pig',
                               Locale.ru: 'Переименовать своего хряка'},
               'name_var_name': {Locale.en_US: 'name',
                                 Locale.ru: 'имя'},
               'name_var_desc': {Locale.en_US: 'New name for pig',
                                 Locale.ru: 'Новое имя для свинтуса'},
               'scd_title': {'en': 'New pig name: {pig}',
                             'ru': 'Новое имя хряка: {pig}'},
               },
    'pagination': {
        'wrong_user_title': {'en': 'Hey, it\'s not your message',
                             'ru': 'Эй, это не твоё сообщение'},
        'wrong_user_desc': {'en': 'You can\'t just take and flip through other people\'s pages',
                            'ru': 'Ты не можешь просто взять и листать чужие страницы'},
    },
    'item_used': {'ate_poop_and_poisoned_title': {'en': 'You ate poop',
                                                  'ru': 'Вы сьели какаху'},
                  'ate_poop_and_poisoned_desc': {
                      'en': 'You ate poop. You liked its taste, but unfortunately you got poisoned\n\n'
                            '*- A doctor came to you and cured you, but now he asks 5 🪙 for treatment*',
                      'ru': 'Вы сьели какашку. Вам понравился её вкус, но к сожалению вы отравились\n\n'
                            '*- К вам пришёл доктор и вылечил вас, но теперь он просит 5 🪙 за лечение*'}
                  },
    'words': {
        'page': {'en': 'Page',
                 'ru': 'Страница'},
        'cost': {'en': 'Cost',
                 'ru': 'Цена'},
        'cost_per_item': {'en': 'Price/pc',
                          'ru': 'Цена/шт'},
        'type': {'en': 'Type',
                 'ru': 'тип'},
        'amount': {'en': 'Amount',
                   'ru': 'Кол-во'},
        'description': {'en': 'Description',
                        'ru': 'Описание'},
        'resource': {'en': 'Resource',
                     'ru': 'Ресурс'},
        'use': {'en': 'Use',
                'ru': 'Использовать'},
        'sell': {'en': 'Sell',
                 'ru': 'Продать'},
        'run_away': {'en': 'Run away',
                     'ru': 'Сбежать'},
        'pay': {'en': 'Pay',
                'ru': 'Заплатить'}
    },
    'error_callbacks': {
        'pig_feed_cooldown_title': {'en': 'Your pig is not yet hungry',
                                    'ru': 'Ваш хряк ещё не голоден'},
        'pig_feed_cooldown_desc': {'en': '**{pig}** gets hungry **<t:{timestamp}:R>**',
                                   'ru': '**{pig}** проголодается **<t:{timestamp}:R>**'},
        'wrong_component_clicked_title': {'en': "It's not your message",
                                          'ru': 'Это не ваше сообщение'},
        'wrong_component_clicked_desc': {'en': "You can't push other people's buttons",
                                         'ru': 'Ты не можешь нажимать на чужие кнопки'},
        'not_enough_money_title': {'en': 'Not enough money',
                                   'ru': 'Не достаточно денег'},
        'not_enough_money_desc': {'en': "You don't have enough money to pay",
                                  'ru': 'У вас не достаточно денег, чтобы заплатить'},
        'no_item_title': {'en': "You don't have this item",
                                   'ru': 'У вас нету этого предмета'},
        'no_item_desc': {'en': "*Unfortunately, you couldn't find this item in your storage*",
                                  'ru': '*К сожалению, вы не смогли найти этот предмет у себя в хранилище*'},
        'modal_input_is_not_number_title': {'en': 'Неверный ввод',
                                            'ru': 'Неверный ввод'},
        'modal_input_is_not_number_desc': {
            'en': "What you entered does not look like a number, but it would be better a number",
            'ru': 'То что ты ввёл не похоже на число, а лучше бы это было числом'},
    },
    'other': {
        'not_enough_money_for_doctor_title': {'en': 'Not enough money',
                                              'ru': 'Недостаточно средств'},
        'not_enough_money_for_doctor_desc': {'en': "You don't have enough money to pay the doctor\n\n"
                                                   '*- Doctor takes pity on a beggar like you and just walks away*',
                                             'ru': 'У вас не хватает денег, чтобы заплатить доктору\n\n'
                                                   '*- Доктор жалеет такого нищего как вы и просто уходит*'},
        'ran_away_and_not_payed_title': {'en': 'You ran away',
                                         'ru': 'Вы сбежали'},
        'ran_away_and_not_payed_desc': {'en': "*You were able to escape. There doesn't seem to be anyone behind*",
                                        'ru': '*Вы смогли сбежать. Кажется никого позади нету*'},
        'payed_to_doctor_title': {'en': 'You paid the doctor',
                                  'ru': 'Вы заплатили доктору'},
        'payed_to_doctor_desc': {'en': '*The doctor took the money and left*',
                                 'ru': '*Доктор взял деньги и уехал*'},
    }
}
