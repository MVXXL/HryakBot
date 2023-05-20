import asyncio
import datetime
import random

from ...core import *
from ...utils import *


def shop_item_selected(user_id, item_id, lang) -> list:
    components = []
    components.append(disnake.ui.Button(
        style=disnake.ButtonStyle.green,
        label=locales['words']['buy'][lang],
        custom_id=f'buy:{item_id}',
        # emoji='✋',
    ))
    if Inventory.get_item_type(item_id).startswith('skin'):
        components.append(disnake.ui.Button(
            style=disnake.ButtonStyle.primary,
            label=locales['words']['preview'][lang],
            custom_id=f'preview_shop_skin:{item_id}',
            # emoji='✋',
        ))
    components.append(disnake.ui.Button(
        style=disnake.ButtonStyle.grey,
        label='↩️',
        custom_id=f'back_to_inventory:shop',
        # emoji='💰'
    ))
    return components
