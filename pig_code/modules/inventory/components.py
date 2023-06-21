import asyncio
import datetime
import random

from ...core import *
from ...utils import *


def inventory_item_selected(item_id, lang) -> list:
    components = []
    if 'use' in Inventory.get_item_components(item_id):
        label = locales['words']['use'][lang]
        if Inventory.get_item_type(item_id) == 'case':
            label = locales['words']['open'][lang]
        components.append(disnake.ui.Button(
            style=disnake.ButtonStyle.primary,
            label=label,
            custom_id=f'use_item:{item_id}',
            # emoji='✋',
        ))
    if 'cook' in Inventory.get_item_components(item_id):
        components.append(disnake.ui.Button(
            style=disnake.ButtonStyle.primary,
            label=locales['words']['cook'][lang],
            custom_id=f'cook_item:{item_id}',
            # emoji='✋',
        ))
    if 'sell' in Inventory.get_item_components(item_id):
        components.append(disnake.ui.Button(
            style=disnake.ButtonStyle.green,
            label=locales['words']['sell'][lang],
            custom_id=f'sell_item:{item_id}',
            # emoji='💰'
        ))
    components.append(disnake.ui.Button(
        style=disnake.ButtonStyle.grey,
        label='↩️',
        custom_id=f'back_to_inventory:inventory',
        # emoji='💰'
    ))
    return components


def skins_category_choose_components(user_id, lang) -> list:
    components = []
    generated_options = []

    inventory = User.get_inventory(user_id)
    inventory = Func.get_items_by_types(inventory, ['skin'])
    types = set()
    for item_id in inventory:
        types.add(Inventory.get_item_type(item_id))
    generated_options.append(disnake.SelectOption(
        label=locales['words']['all_skins'][lang],
        value='skin:all',
        # emoji=option['emoji'],
        # description=option['description']
    ))
    for t in types:
        generated_options.append(disnake.SelectOption(
            label=locales['item_types'][t][lang],
            value=t,
            # emoji=option['emoji'],
            # description=option['description']
        ))
    if generated_options:
        components.append(disnake.ui.Select(options=generated_options, custom_id='wardrobe_category_choose',
                                            placeholder=locales['inventory']['select_category_placeholder'][lang]))
    return components

