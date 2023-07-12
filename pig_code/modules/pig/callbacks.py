from ...core import *
from ...utils import *
from . import embeds
from . import components


async def pig_feed(inter):
    await Botutils.pre_command_check(inter)
    Botutils.check_pig_feed_cooldown(inter.author)
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
    for item_buff, number in Pig.get_buffs(inter.author.id).items():
        if number > 0:
            buffs = Inventory.get_item_buffs(item_buff)
            if item_buff in ['laxative']:
                Pig.remove_buff(inter.author.id, item_buff)
            pooped_poop *= buffs['pooping_boost']
            weight_add *= buffs['weight_boost']
    pooped_poop = round(pooped_poop)
    weight_add = round(weight_add, 1)
    User.add_item(inter.author.id, 'poop', pooped_poop)
    Pig.add_weight(inter.user.id, weight_add)
    Pig.set_last_feed(inter.author.id, Func.get_current_timestamp())
    await send_callback(inter, embed=embeds.pig_feed(inter, lang, weight_add, pooped_poop))


async def meat(inter):
    await Botutils.pre_command_check(inter)
    Botutils.check_pig_meat_cooldown(inter.author)
    lang = User.get_language(inter.author.id)
    if Inventory.get_item_amount(inter.author.id, 'knife') <= 0:
        raise NoItemInInventory('knife', Locales.Meat.no_knife_desc)
    bacon_add = random.randrange(8, 16)
    User.add_item(inter.author.id, 'lard', bacon_add)
    weight_lost = round(random.uniform(.2, .7) * bacon_add, 1)
    Pig.add_weight(inter.user.id, -weight_lost)
    Pig.set_last_meat(inter.author.id, Func.get_current_timestamp())
    await send_callback(inter, embed=embeds.pig_meat(inter, lang, bacon_add, weight_lost))


async def pig_rename(inter, name):
    await Botutils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    name = name.replace('\'', '')
    Pig.rename(inter.author.id, name)
    await send_callback(inter, embed=embeds.pig_rename(inter, lang))
