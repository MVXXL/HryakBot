from ...core import *
from ...utils import *


async def shop_item_selected(item_id, lang, category: str = None, page: int = 1) -> list:
    components = []
    components.append(discord.ui.Button(
        style=discord.ButtonStyle.green,
        label=translate(Locales.Global.buy, lang),
        custom_id=f'buy;{item_id};{category};{page}',
    ))
    if (await Item.get_type(item_id)).startswith('skin'):
        components.append(discord.ui.Button(
            style=discord.ButtonStyle.primary,
            label=translate(Locales.Global.preview, lang),
            custom_id=f'preview_skin;{item_id};{category};{page}',
        ))
    components.append(discord.ui.Button(
        style=discord.ButtonStyle.grey,
        label='↩️',
        custom_id=f'back_to_inventory;shop;{category};{page}',
    ))
    return components
