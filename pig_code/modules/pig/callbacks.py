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
    add_weight_chances = {'add': 85, 'remove': 15}
    if Pig.get_weight(inter.author.id) < 20:
        add_weight_chances = {'add': 100, 'remove': 0}
    if Func.random_choice_with_probability(add_weight_chances) == 'add':
        weight_add = random.uniform(1, 10)
    else:
        weight_add = random.uniform(-5, -1)
    bot_guild = inter.client.get_guild(config.BOT_GUILD)
    if bot_guild is not None:
        if bot_guild.get_member(inter.author) is not None and weight_add > 0:
            weight_add *= 1.05
    pig_weight = Pig.get_weight(inter.author.id)
    pooped_poop = random.uniform(5 + round(pig_weight * .05), 20 + round(pig_weight * .15))
    print(Pig.get_buffs(inter.author.id))
    for item_buff, number in Pig.get_buffs(inter.author.id).items():
        if number > 0:
            buffs = Inventory.get_item_buffs(item_buff)
            pooped_poop *= buffs['pooping_boost']
            weight_add *= buffs['weight_boost']
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
        raise NoItemInInventory('knife', locales['meat']['no_knife_desc'])
    bacon_add = random.randrange(8, 16)
    Inventory.add_item(inter.author.id, 'lard', bacon_add)
    weight_lost = round(random.uniform(.2, .7) * bacon_add, 1)
    Pig.add_weight(inter.user.id, -weight_lost)
    Pig.set_last_meat(inter.author.id, Func.get_current_timestamp())
    await BotUtils.send_callback(inter, embed=embeds.pig_meat(inter, lang, bacon_add, weight_lost))


async def breed(inter, partner):
    await BotUtils.pre_command_check(inter)
    BotUtils.check_pig_breed_cooldown(inter.author)
    lang = User.get_language(inter.author.id)
    min_weight_to_breed = 50
    if partner == inter.author:
        raise breedWithYourself
    if partner.bot is True:
        raise BotAsPartnerbreed
    if Pig.get_weight(inter.author.id) < min_weight_to_breed:
        await BotUtils.send_callback(inter, embed=embeds.pig_is_too_small_for_breed(inter, lang, inter.author, min_weight_to_breed))
        return
    if Pig.get_weight(partner.id) < min_weight_to_breed:
        await BotUtils.send_callback(inter, embed=embeds.pig_is_too_small_for_breed(inter, lang, partner, min_weight_to_breed))
        return
    mini_pig_chances = {'fail': 50,
                        # 'pet_hryak_default': (Pig.get_weight(inter.author.id) + Pig.get_weight(partner.id)) / 1.5
                        }
    mini_pig = Func.random_choice_with_probability(mini_pig_chances)
    Pig.set_last_breed(inter.author.id, Func.get_current_timestamp())
    Pig.set_last_breed(partner.id, Func.get_current_timestamp())
    if mini_pig == 'fail':
        await BotUtils.send_callback(inter, embed=embeds.pig_breed_fail(inter, lang, partner))
    else:
        Pig.make_pregnant(partner.id, partner.id, mini_pig)
        await BotUtils.send_callback(inter, embed=embeds.pig_breed_ok(inter, lang, partner, mini_pig))


async def pig_rename(inter, name):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    name = name.replace('\'', '')
    Pig.rename(inter.author.id, name)
    await BotUtils.send_callback(inter, embed=embeds.pig_rename(inter, lang))
