import asyncio
import datetime
import random

from ...core import *
from ...utils import *


def pig_feed(inter, lang, weight_changed: float, pooped_poop: int) -> disnake.Embed:
    weight_changed_description = ''
    pooped_poop_description = random.choice(locales['feed']['pig_pooped_desc_list'][lang])
    if weight_changed > 0:
        weight_changed_description = random.choice(locales['feed']['feed_scd_desc_list'][lang])
    elif weight_changed < 0:
        weight_changed_description = random.choice(locales['feed']['feed_fail_desc_list'][lang])
    embed = BotUtils.generate_embed(
        title=locales['feed']['feed_title'][lang],
        description=f'- {weight_changed_description.format(pig=Pig.get_name(inter.author.id), mass=abs(weight_changed))}\n'
                    f'- {pooped_poop_description.format(pig=Pig.get_name(inter.author.id), poop=pooped_poop)}\n\n'
                    f"*{locales['feed']['total_pig_weight'][lang].format(weight=Pig.get_weight(inter.author.id))}*",
        prefix=Func.generate_prefix('🐷'),
        footer=Func.generate_footer(inter),
        thumbnail_file=BotUtils.generate_user_pig(inter.author.id),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
    )
    return embed

def pig_meat(inter, lang, bacon_add: int, weight_lost: float) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['meat']['meat_title'][lang],
        description=f'- {random.choice(locales["meat"]["meat_desc_list"][lang]).format(pig=Pig.get_name(inter.author.id), meat=bacon_add)}\n'
                    f'- {random.choice(locales["meat"]["weight_lost_desc_list"][lang]).format(pig=Pig.get_name(inter.author.id), weight_lost=weight_lost)}\n\n'
                    f"*{locales['meat']['total_pig_weight'][lang].format(weight=Pig.get_weight(inter.author.id))}*",
        prefix=Func.generate_prefix('🐷'),
        footer=Func.generate_footer(inter),
        thumbnail_file=BotUtils.generate_user_pig(inter.author.id),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
    )
    return embed

def no_knife_for_meat(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=f'{locales["meat"]["no_knife_title"][lang]}',
        description=locales["meat"]["no_knife_desc"][lang],
        prefix=Func.generate_prefix('🔪'),
        footer=Func.generate_footer(inter),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
    )
    return embed

def pig_rename(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['rename']['scd_title'][lang].format(pig=Pig.get_name(inter.author.id)),
        prefix=Func.generate_prefix('🐷'),
        footer=Func.generate_footer(inter),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
    )
    return embed
