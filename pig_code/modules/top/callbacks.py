import asyncio
import datetime
import random

from ...core import *
from ...utils import *
from . import embeds
from . import components
from .. import errors


async def top(inter):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    await BotUtils.pagination(inter, lang, embeds=[
        await embeds.weight_top(inter, lang),
        await embeds.money_top(inter, lang)
    ], components=[
        [await components.choose_user(inter, lang, User.get_users_sorted_by('pig', 'weight', number=10,
                                                                            exclude=utils_config.ignore_users_in_top))],
        [await components.choose_user(inter, lang, User.get_users_sorted_by('money', number=10,
                                                                            exclude=utils_config.ignore_users_in_top))]
    ], hide_button=False)

