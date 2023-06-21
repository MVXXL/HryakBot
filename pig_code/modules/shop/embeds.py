import asyncio
import datetime
import random

from ...core import *
from ...utils import *


def shop_item_selected(inter, item_id, lang) -> disnake.Embed:
    skin_type = Inventory.get_item_skin_type(item_id)
    preview_options = utils_config.default_pig['skins'].copy()
    preview_options[skin_type] = item_id
    embed = BotUtils.generate_embed(
        title=locales['wardrobe_item_selected']['title'][lang].format(item=Inventory.get_item_name(item_id, lang)),
        description=locales['wardrobe_item_selected']['desc'][lang].format(
            amount=Inventory.get_item_amount(inter.author.id, item_id),
            type=Inventory.get_item_type(item_id, lang),
        ),
        prefix=Func.generate_prefix(Inventory.get_item_emoji(item_id)),
        footer=Func.generate_footer(inter),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        timestamp=True,
        thumbnail_file=Func.build_pig(tuple(preview_options.items()),
                                      tuple(utils_config.default_pig['genetic'].items())),
        fields=[{'name': f"📋 ⟩ {locales['words']['description'][lang]}",
                 'value': f"*{Inventory.get_item_description(item_id, lang)}*"}]
    )
    return embed


def shop_item_bought(inter, item_id, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['shop_item_bought']['title'][lang].format(item=Inventory.get_item_name(item_id, lang)),
        description=locales['shop_item_bought']['desc'][lang],
        prefix=Func.generate_prefix('scd'),
        timestamp=True,
        footer=Func.generate_footer(inter),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
    )
    return embed

def item_cooldown(inter, item_id, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['error_callbacks']['shop_buy_cooldown_title'][lang],
        description=locales['error_callbacks']['shop_buy_cooldown_desc'][lang].format(item=Inventory.get_item_name(item_id, lang), timestamp=Shop.get_timestamp_of_new_item(inter.author.id, item_id)),
        prefix=Func.generate_prefix('scd'),
        timestamp=True,
        footer=Func.generate_footer(inter),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
    )
    return embed

# def inventory_item_sold(inter, item_id, amount, money_received, lang) -> disnake.Embed:
#     embed = BotUtils.generate_embed(
#         title=locales['inventory_item_sold']['title'][lang].format(item=Inventory.get_item_name(item_id, lang)),
#         description=f"- {locales['inventory_item_sold']['desc'][lang].format(item=Inventory.get_item_name(item_id, lang), amount=amount, money=money_received)}",
#         prefix=Func.generate_prefix('scd'),
#         footer=Func.generate_footer(inter, second_part='item_sold'),
#         footer_url=Func.generate_footer_url('user_avatar', inter.author),
#     )
#     return embed
