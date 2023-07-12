from ...core import *
from ...utils import *


def shop_item_selected(user_id, item_id, lang) -> list:
    components = []
    components.append(disnake.ui.Button(
        style=disnake.ButtonStyle.green,
        label=Locales.Global.buy[lang],
        custom_id=f'buy:{item_id}',
    ))
    if Inventory.get_item_type(item_id).startswith('skin'):
        components.append(disnake.ui.Button(
            style=disnake.ButtonStyle.primary,
            label=Locales.Global.preview[lang],
            custom_id=f'preview_skin:{item_id}',
        ))
    components.append(disnake.ui.Button(
        style=disnake.ButtonStyle.grey,
        label='↩️',
        custom_id=f'back_to_inventory:shop',
    ))
    return components
