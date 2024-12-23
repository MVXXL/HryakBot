from ....utils import *
from .special import *


async def item_remove(inter, item_id, update):
    User.remove_item(inter.user.id, item_id)
    # await update()


async def use_laxative(inter, item_id, update):
    User.remove_item(inter.user.id, item_id)
    Pig.add_buff(inter.user.id, 'laxative', 1)
    return {'pig': Pig.get_name(inter.user.id), 'step': Pig.get_buff_amount(inter.user.id, 'laxative')}


async def use_compound_feed(inter, item_id, update):
    User.remove_item(inter.user.id, item_id)
    Pig.add_buff(inter.user.id, 'compound_feed', 1)
    return {'pig': Pig.get_name(inter.user.id), 'step': Pig.get_buff_amount(inter.user.id, 'compound_feed')}


async def use_activated_charcoal(inter, item_id, update):
    User.remove_item(inter.user.id, item_id)
    Pig.add_buff(inter.user.id, 'activated_charcoal', 1)
    return {}


async def use_milk(inter, item_id, update):
    User.remove_item(inter.user.id, item_id)
    Pig.set_buffs(inter.user.id, {})
    return {}


async def cook(inter, item_id, update):
    lang = User.get_language(inter.user.id)
    if Item.get_amount('grill', inter.user.id) <= 0:
        await error_callbacks.no_item(inter, 'grill',
                                      description=translate(Locales.ErrorCallbacks.no_mangal_to_cook, inter.user.id),
                                      thumbnail_url=await Item.get_image_path('grill'), edit_original_response=False,
                                      ephemeral=True)
        return
    modal_interaction, amount = await modals.get_item_amount(inter,
                                                             translate(Locales.InventoryItemCookModal.title, lang),
                                                             translate(Locales.InventoryItemCookModal.label, lang),
                                                             max_amount=Item.get_amount(item_id, inter.user.id))
    if amount is False:
        return
    if Item.get_amount(item_id, inter.user.id) <= 0:
        await error_callbacks.not_enough_items(inter, item_id, thumbnail_url=await Item.get_image_path(item_id))
        return
    User.remove_item(inter.user.id, item_id, amount)
    User.add_item(inter.user.id, Item.get_cooked_item_id(item_id), amount)
    await send_callback(modal_interaction, ephemeral=True,
                        embed=generate_embed(
                            title=translate(Locales.InventoryItemCooked.title, lang,
                                            {'item': Item.get_name(item_id, lang)}),
                            description=f"- {translate(Locales.InventoryItemCooked.desc, lang, {'item': Item.get_name(item_id, lang), 'amount': amount})}",
                            prefix=Func.generate_prefix('scd'),
                            inter=modal_interaction), edit_original_response=False)
    await update()


async def sell(inter, item_id, update):
    lang = User.get_language(inter.user.id)
    modal_interaction, amount = await modals.get_item_amount(inter,
                                                             translate(Locales.InventoryItemSellModal.title, lang),
                                                             translate(Locales.InventoryItemSellModal.label, lang),
                                                             max_amount=Item.get_amount(item_id, inter.user.id))
    User.clear_get_inventory_cache(inter.user.id)
    if amount is False:
        return
    if Item.get_amount(item_id, inter.user.id) < amount:
        await error_callbacks.not_enough_items(modal_interaction, item_id,
                                               thumbnail_url=await Item.get_image_path(item_id))
        return
    money_received = Item.get_sell_price(item_id) * amount
    Stats.add_money_earned(inter.user.id, money_received)
    Stats.add_items_sold(inter.user.id, item_id, amount)
    User.remove_item(inter.user.id, item_id, amount)
    User.add_item(inter.user.id, 'coins', money_received)
    await send_callback(modal_interaction, ephemeral=True,
                        embed=generate_embed(
                            title=translate(Locales.InventoryItemSold.title, lang,
                                            {'item': Item.get_name(item_id, lang)}),
                            description=f"- {translate(Locales.InventoryItemSold.desc, lang, {'item': Item.get_name(item_id, lang), 'amount': amount, 'money': money_received})}",
                            prefix=Func.generate_prefix('scd'),
                            inter=modal_interaction), edit_original_response=False)
    await update()


def cook_comp():
    return {'label': {'en': 'Cook',
                      'ru': 'Приготовить'},
            'color': discord.ButtonStyle.primary,
            'options': ['modal'],
            'func': cook}


def sell_comp():
    return {'label': {'en': 'Sell',
                      'ru': 'Продать'},
            'color': discord.ButtonStyle.green,
            'options': ['modal'],
            'func': sell}


def case_comp():
    return {'label': {'en': 'Open',
                      'ru': 'Открыть'},
            'color': discord.ButtonStyle.primary,
            'func': case.case_used}


item_components = {
    'laxative': {'use': {'label': {'en': 'Use',
                                   'ru': 'Использовать'},
                         'color': discord.ButtonStyle.primary,
                         'func': use_laxative,
                         'callback': {'title': {'en': 'You used laxative',
                                                'ru': 'Вы использовали слабительное'},
                                      'description': {
                                          'en': '***{pig}** will produce more manure next **{step}** feedings*',
                                          'ru': '***{pig}** будет давать больше навоза следующие **{step}** кормёжек*'},
                                      'prefix': '💊'
                                      },
                         # 'sell'
                         }},
    'compound_feed': {'use': {'label': {'en': 'Use',
                                        'ru': 'Использовать'},
                              'color': discord.ButtonStyle.primary,
                              'func': use_compound_feed,
                              'callback': {'title': {'en': 'You used compound feed',
                                                     'ru': 'Вы использовали комбикорм'},
                                           'description': {
                                               'en': '***{pig}** will gain more weight next **{step}** feedings*',
                                               'ru': '***{pig}** будет набирать больше веса следующие **{step}** кормёжек*'},
                                           'prefix': '🥕'
                                           },
                              # 'sell'
                              }},
    'milk': {'use': {'label': {'en': 'Use',
                               'ru': 'Использовать'},
                     'color': discord.ButtonStyle.primary,
                     'func': use_milk,
                     'callback': {'title': {'en': 'Your pig drank milk',
                                            'ru': 'Хряк выпил молоко'},
                                  'description': {
                                      'en': '*All buffs have been removed from your pig*',
                                      'ru': '*Все баффы были сброшены с вашего Хряка*'},
                                  'prefix': '🥛'
                                  },
                     }},
    'activated_charcoal': {'use': {'label': {'en': 'Use',
                                             'ru': 'Использовать'},
                                   'color': discord.ButtonStyle.primary,
                                   'func': use_activated_charcoal,
                                   'callback': {'title': {'en': 'The boar ate activated charcoal',
                                                          'ru': 'Хряк съел активированный уголь'},
                                                'description': {
                                                    'en': '*Your pig swallowed all the pills with little desire, now he is less likely to vomit for the next 24 hours*',
                                                    'ru': '*Хряк с не особым желанием проглотил все таблетки, теперь его с меньшей вероятностью будет тошнить следующие сутки*'},
                                                'prefix': '💊'
                                                },
                                   }},
    'poop': {'use': {'label': {'en': 'Eat',
                               'ru': 'Съесть'},
                     'color': discord.ButtonStyle.primary,
                     'func': poop.eat},
             # 'sell': sell_comp()
             },
    'lard': {
        'cook': cook_comp(),
        # 'sell': sell_comp()
    },
    'barbecue': {'eat': {'label': {'en': 'Eat',
                                   'ru': 'Съесть'},
                         'color': discord.ButtonStyle.primary,
                         'func': item_remove,
                         'callback': {'title': {'en': 'You ate barbecue',
                                                'ru': 'Вы съели шашлык'},
                                      'description': {
                                          'en': '*You feel guilty for biting off a piece of your pig*',
                                          'ru': '*Вы чувствуете вину за то что откусили кусочек своего хряка*'},
                                      'prefix': '🍖'
                                      }},
                 # 'sell': sell_comp()
                 },
    'beer': {'eat': {'label': {'en': 'Drink',
                               'ru': 'Выпить'},
                     'color': discord.ButtonStyle.primary,
                     'func': item_remove,
                     'callback': {'title': {'en': 'You drank a beer',
                                            'ru': 'Вы выпили пиво'},
                                  'description': {
                                      'en': '*You feel a little intoxicated and joyful*',
                                      'ru': '*Вы чувствуете небольшое опьянение и радость*'},
                                  'prefix': '🍻'
                                  }}},
    'whiskey': {'eat': {'label': {'en': 'Drink',
                                  'ru': 'Выпить'},
                        'color': discord.ButtonStyle.primary,
                        'func': item_remove,
                        'callback': {'title': {'en': 'You drank a whiskey',
                                               'ru': 'Вы выпили виски'},
                                     'description': {
                                         'en': '*You feel a little warmth inside of you*',
                                         'ru': '*Вы чувствуете небольшое тепло внутри себя*'},
                                     'prefix': '🥃'
                                     }}},
    'vodka': {'eat': {'label': {'en': 'Drink',
                                'ru': 'Выпить'},
                      'color': discord.ButtonStyle.primary,
                      'func': item_remove,
                      'callback': {'title': {'en': 'You drank a vodka',
                                             'ru': 'Вы выпили водку'},
                                   'description': {
                                       'en': '*You got so drunk that you started singing the song "Blue Tractor" loudly*',
                                       'ru': '*Вы настолько опьянели что начали громко петь песню "Синий трактор"*'},
                                   'prefix': '🥴'
                                   }}},
    # 'common_case': {'open': case_comp()},
    # 'rare_case': {'open': case_comp()}
}

for item in Tech.get_all_items():
    if item not in item_components:
        item_components[item] = {}
        if Item.get_type(item) == 'case':
            item_components[item] = {'open': case_comp()}
            continue
    if Item.is_salable(item):
        item_components[item]['sell'] = sell_comp()
