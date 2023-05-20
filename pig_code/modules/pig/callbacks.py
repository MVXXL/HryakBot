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
    Stats.add_pig_fed(inter.author.id, 1)
    if random.randrange(6) != 0:
        weight_add = random.uniform(1, 10)
    else:
        weight_add = random.uniform(-5, -1)
    pig_weight = Pig.get_weight(inter.author.id)
    pooped_poop = random.uniform(5 + round(pig_weight * .05), 20 + round(pig_weight * .15))
    if Pig.get_buff_value(inter.author.id, 'laxative') > 0:
        Pig.remove_buff(inter.author.id, 'laxative', 1)
        pooped_poop *= items['laxative']['pooping_boost']
    pooped_poop = round(pooped_poop)
    weight_add = round(weight_add, 1)
    Inventory.add_item(inter.author.id, 'poop', pooped_poop)
    Pig.add_weight(inter.user.id, weight_add)
    Pig.set_last_feed(inter.author.id, Func.get_current_timestamp())
    await BotUtils.send_callback(inter, embed=embeds.pig_feed(inter, lang, weight_add, pooped_poop))

async def meat(inter):
    await BotUtils.pre_command_check(inter)
    BotUtils.check_pig_meat_cooldown(inter.author)
    lang = User.get_language(inter.author.id)
    if Inventory.get_item_amount(inter.author.id, 'knife') <= 0:
        await BotUtils.send_callback(inter, embed=embeds.no_knife_for_meat(inter, lang))
        return
    bacon_add = random.randrange(2, 8)
    Inventory.add_item(inter.author.id, 'lard', bacon_add)
    weight_lost = round(random.uniform(.5, 1) * bacon_add, 1)
    # pig_weight = Pig.get_weight(inter.author.id)
    # pooped_poop = random.uniform(5 + round(pig_weight * .05), 20 + round(pig_weight * .15))
    # if Pig.get_buff_value(inter.author.id, 'laxative') > 0:
    #     Pig.remove_buff(inter.author.id, 'laxative', 1)
    #     pooped_poop *= items['laxative']['pooping_boost']
    # pooped_poop = round(pooped_poop)
    # weight_add = round(weight_add, 1)
    # Inventory.add_item(inter.author.id, 'poop', pooped_poop)
    Pig.add_weight(inter.user.id, -weight_lost)
    Pig.set_last_meat(inter.author.id, Func.get_current_timestamp())
    await BotUtils.send_callback(inter, embed=embeds.pig_meat(inter, lang, bacon_add, weight_lost))


async def pig_rename(inter, name):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    Pig.rename(inter.author.id, name)
    await BotUtils.send_callback(inter, embed=embeds.pig_rename(inter, lang))
