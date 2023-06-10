import asyncio
import datetime
import random

from ...core import *
from ...utils import *
from . import embeds
from . import components
from .. import errors


async def top(inter, server_only: bool = False):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    weight_users = User.get_users_sorted_by('pig', 'weight', exclude=utils_config.ignore_users_in_top)
    money_users = User.get_users_sorted_by('money', exclude=utils_config.ignore_users_in_top)
    if server_only:
        weight_users = BotUtils.filter_users(inter.client, weight_users, inter.guild.id)
        money_users = BotUtils.filter_users(inter.client, money_users, inter.guild.id)
    weight_users = weight_users[:10]
    money_users = money_users[:10]
    await BotUtils.pagination(inter, lang, embeds=[
        await embeds.weight_top(inter, lang, weight_users),
        await embeds.money_top(inter, lang, money_users)
    ], components=[
        [await components.choose_user(inter, lang, weight_users)],
        [await components.choose_user(inter, lang, money_users)]
    ], hide_button=False)
