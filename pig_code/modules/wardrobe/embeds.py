import asyncio
import datetime
import random

from ...core import *
from ...utils import *


def wardrobe_item_selected(inter, item_id, lang) -> disnake.Embed:
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


def wardrobe_item_wear(inter, item_id, lang) -> disnake.Embed:
    skin_type = Inventory.get_item_skin_type(item_id)
    preview_options = Pig.get_skin(inter.author.id, 'all')
    preview_options[skin_type] = Pig.get_skin(inter.author.id, skin_type)
    embed = BotUtils.generate_embed(
        title=locales['wardrobe_item_wear']['title'][lang].format(item=Inventory.get_item_name(item_id, lang)),
        description=random.choice(locales['wardrobe_item_wear']['desc_list'][lang]).format(
            item=Inventory.get_item_name(item_id, lang)),
        prefix=Func.generate_prefix('scd'),
        footer=Func.generate_footer(inter),
        timestamp=True,
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        thumbnail_file=BotUtils.generate_user_pig(inter.author.id),
    )
    return embed


def wardrobe_item_remove(inter, item_id, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['wardrobe_item_remove']['title'][lang].format(item=Inventory.get_item_name(item_id, lang)),
        description=locales['wardrobe_item_remove']['desc'][lang].format(item=Inventory.get_item_name(item_id, lang)),
        prefix=Func.generate_prefix('scd'),
        footer=Func.generate_footer(inter),
        timestamp=True,
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        thumbnail_file=BotUtils.generate_user_pig(inter.author.id),
    )
    return embed


def wardrobe_item_preview(inter, item_id, lang) -> disnake.Embed:
    skin_type = Inventory.get_item_skin_type(item_id)
    preview_options = Pig.get_skin(inter.author.id, 'all')
    preview_options[skin_type] = item_id
    embed = BotUtils.generate_embed(
        title=locales['wardrobe_item_preview']['title'][lang].format(item=Inventory.get_item_name(item_id, lang)),
        description=locales['wardrobe_item_preview']['desc'][lang].format(item=Inventory.get_item_name(item_id, lang)),
        prefix=Func.generate_prefix('👁️'),
        footer=Func.generate_footer(inter),
        timestamp=True,
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        thumbnail_file=Func.build_pig(tuple(preview_options.items()),
                                      tuple(Pig.get_genetic(inter.author.id, 'all').items())),
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
