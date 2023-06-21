import asyncio
import datetime
import random

from .....core import *
from .....utils import *
from . import embeds
from . import components


async def case_used(inter, lang, case):
    # Pig.add_buff(inter.author.id, 'laxative', 1)
    if case == 'common_case':
        item_types = ['skin']
        chances = {
            '2': 30,
            '3': 68,
            '4': 2,
            '5': .1
        }
    elif case == 'rare_case':
        item_types = ['skin']
        chances = {
            '3': 25,
            '4': 73,
            '5': 2
        }
    else:
        return
    probable_items = {}
    for t in item_types:
        probable_items.update(Func.get_items_by_key(items, 'type', t))
    item_rarity = Func.random_choice_with_probability(chances)
    probable_items = Func.get_items_by_key(probable_items, 'rarity', item_rarity)
    probable_items = Inventory.get_items_obtainable_in_cases(probable_items)
    items_received = {Func.random_choice_with_probability({i: 1 for i in probable_items}): 1}
    for item, amount in items_received.items():
        Inventory.add_item(inter.author.id, item, amount)
    await BotUtils.send_callback(inter, embed=embeds.case_used(inter, lang, items_received),
                                 ephemeral=True, edit_original_message=False)
