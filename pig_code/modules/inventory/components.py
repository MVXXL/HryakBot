import asyncio
import datetime
import random


from ...core import *
from ...utils import *


def inventory_item_selected(item_id, lang) -> list:
    components = []
    if 'use' in Inventory.get_item_components(item_id):
        components.append(disnake.ui.Button(
            style=disnake.ButtonStyle.primary,
            label=locales['words']['use'][lang],
            custom_id=f'use_item:{item_id}',
            # emoji='✋',
        ))
    if 'sell' in Inventory.get_item_components(item_id):
        components.append(disnake.ui.Button(
            style=disnake.ButtonStyle.green,
            label=locales['words']['sell'][lang],
            custom_id=f'sell_item:{item_id}',
            # emoji='💰'
        ))
    return components