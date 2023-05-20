import asyncio
import datetime
import random

from ...core import *
from ...utils import *


def wardrobe_item_selected(user_id, item_id, lang) -> list:
    components = []
    if Pig.get_skin(user_id, Inventory.get_item_skin_type(item_id)) != item_id:
        components.append(disnake.ui.Button(
            style=disnake.ButtonStyle.primary,
            label=locales['words']['wear'][lang],
            custom_id=f'wear_skin:{item_id}',
            # emoji='✋',
        ))
        components.append(disnake.ui.Button(
            style=disnake.ButtonStyle.primary,
            label=locales['words']['preview'][lang],
            custom_id=f'preview_skin:{item_id}',
            # emoji='✋',
        ))
    else:
        components.append(disnake.ui.Button(
            style=disnake.ButtonStyle.primary,
            label=locales['words']['remove_cloth'][lang],
            custom_id=f'remove_skin:{item_id}',
            # emoji='✋',
        ))
    components.append(disnake.ui.Button(
        style=disnake.ButtonStyle.grey,
        label='↩️',
        custom_id=f'back_to_inventory:wardrobe',
        # emoji='💰'
    ))
    return components
