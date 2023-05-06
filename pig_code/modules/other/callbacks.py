import asyncio
import datetime
import random

from ...core import *
from ...utils import *
from . import embeds
from . import components
from .. import errors


async def profile(inter, user: disnake.User = None):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    User.register_user_if_not_exists(user.id)
    Pig.create_pig_if_no_pigs(user.id)
    await BotUtils.send_callback(inter, embed=embeds.profile(inter, lang, user))

async def set_language(inter, lang):
    await BotUtils.pre_command_check(inter)
    lang = [i for i in bot_locale.full_names if bot_locale.full_names[i] == lang][0]
    User.set_language(inter.author.id, lang)
    await BotUtils.send_callback(inter, embed=embeds.set_language(inter, lang))
