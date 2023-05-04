import asyncio
import datetime
import random

from ...core import *
from ...utils import *


def inventory_item_selected(inter, item_id, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['inventory_item_selected']['title'][lang].format(item=Inventory.get_item_name(item_id, lang)),
        description=locales['inventory_item_selected']['desc'][lang].format(
            amount=Inventory.get_item_amount(inter.author.id, item_id),
            type=locales['words'][Inventory.get_item_type(item_id)][lang],
            cost=Inventory.get_item_cost(item_id)
        ),
        prefix=Func.generate_prefix(Inventory.get_item_emoji(item_id)),
        footer=Func.generate_footer(inter, second_part=item_id),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        thumbnail_url=Inventory.get_item_image_url(item_id),
        fields=[{'title': f"📋 ⟩ {locales['words']['description'][lang]}",
                 'value': f"*{Inventory.get_item_description(item_id, lang)}*"}]
    )
    return embed


def inventory_item_sold(inter, item_id, amount, money_received, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['inventory_item_sold']['title'][lang].format(item=Inventory.get_item_name(item_id, lang)),
        description=f"- {locales['inventory_item_sold']['desc'][lang].format(item=Inventory.get_item_name(item_id, lang), amount=amount, money=money_received)}",
        prefix=Func.generate_prefix('scd'),
        footer=Func.generate_footer(inter, second_part='item_sold'),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
    )
    return embed
