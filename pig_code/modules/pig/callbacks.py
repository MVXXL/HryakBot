import asyncio
import datetime
import random


from ...core import *
from ...utils import *
from . import embeds
from . import components
from .. import errors


async def pig_feed(inter):
    await BotUtils.pre_command_check(inter)
    BotUtils.check_pig_feed_cooldown(inter.author)
    lang = User.get_language(inter.author.id)
    if random.randrange(6) != 0:
        weight_add = random.uniform(1, 10)
    else:
        weight_add = random.uniform(-5, -1)
    weight_add = round(weight_add, 1)
    pooped_poop = random.randrange(5, 20)
    Inventory.add_item(inter.author.id, 'poop', pooped_poop)
    Pig.add_weight(inter.user.id, 0, weight_add)
    Pig.set_last_feed(inter.author.id, 0, int(datetime.datetime.now().timestamp()))
    await BotUtils.send_callback(inter, embed=embeds.pig_feed(inter, lang, weight_add, pooped_poop))


async def pig_rename(inter, name):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    Pig.rename(inter.author.id, 0, name)
    await BotUtils.send_callback(inter, embed=embeds.pig_rename(inter, lang))


