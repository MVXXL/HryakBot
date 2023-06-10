import asyncio
import datetime
import random

from ...core import *
from ...utils import *
from . import embeds
from . import components
from .. import errors


async def help(inter):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    await BotUtils.pagination(inter, lang, embeds=[
        embeds.basic_help(inter, lang)
    ], hide_button=False)
