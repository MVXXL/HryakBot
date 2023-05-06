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
        description=f'- {weight_changed_description.format(pig=Pig.get_name(inter.author.id, 0), mass=abs(weight_changed))}\n'
                    f'- {pooped_poop_description.format(pig=Pig.get_name(inter.author.id, 0), poop=pooped_poop)}\n\n'
                    f"*{locales['feed']['total_pig_weight'][lang].format(weight=Pig.get_weight(inter.author.id, 0))}*",
        prefix=Func.generate_prefix('🐷'),
        footer=Func.generate_footer(inter),
        thumbnail_file=BotUtils.generate_user_pig(inter.author.id),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
    )
    return embed


def pig_rename(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['rename']['scd_title'][lang].format(pig=Pig.get_name(inter.author.id, 0)),
        prefix=Func.generate_prefix('🐷'),
        footer=Func.generate_footer(inter),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
    )
    return embed
