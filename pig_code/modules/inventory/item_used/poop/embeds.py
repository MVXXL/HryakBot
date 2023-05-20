import asyncio
import datetime
import random

from .....core import *
from .....utils import *


def eaten_and_poisoned(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['item_used']['ate_poop_and_poisoned_title'][lang],
        description=f"{locales['item_used']['ate_poop_and_poisoned_desc'][lang]}",
        prefix=Func.generate_prefix('🍽️'),
        footer=Func.generate_footer(inter, second_part='poop_eaten'),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
    )
    return embed


def ran_away_from_doctor(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['poop_eaten']['ran_away_and_not_payed_title'][lang],
        description=f"{locales['poop_eaten']['ran_away_and_not_payed_desc'][lang]}",
        prefix=Func.generate_prefix('🏃‍♂️'),
        footer=Func.generate_footer(inter, second_part='ran_away'),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
    )
    return embed


def payed_the_doctor(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['poop_eaten']['payed_to_doctor_title'][lang],
        description=f"{locales['poop_eaten']['payed_to_doctor_desc'][lang]}",
        prefix=Func.generate_prefix('🪙'),
        footer=Func.generate_footer(inter, second_part='payed'),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
    )
    return embed


def not_enough_money_for_doctor(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['poop_eaten']['not_enough_money_for_doctor_title'][lang],
        description=f"{locales['poop_eaten']['not_enough_money_for_doctor_desc'][lang]}",
        prefix=Func.generate_prefix('🪙'),
        footer=Func.generate_footer(inter, second_part='no_money'),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        color=utils_config.error_color
    )
    return embed
