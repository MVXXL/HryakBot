from ...core import *
from ...utils import *
from . import embeds
from . import components


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
    for item_buff, number in Pig.get_buffs(inter.author.id).items():
        if number > 0:
            buffs = Item.get_buffs(item_buff)
            if item_buff in ['laxative']:
                Pig.remove_buff(inter.author.id, item_buff)
            pooped_poop *= buffs['pooping']
            weight_add *= buffs['weight']
    tf = Func.check_consecutive_timestamps(Pig.get_feed_history(inter.author.id)[-40:],
                                           6 * 3600, 4 * 3600
                                           # utils_config.pig_feed_cooldown * 1.5, utils_config.pig_feed_cooldown
                                           )
    if tf > len(utils_config.anti_bot_decreases) - 1:
        tf = len(utils_config.anti_bot_decreases) - 1
    weight_add *= 1 - utils_config.anti_bot_decreases[tf] / 100
    pooped_poop *= 1 - utils_config.anti_bot_decreases[tf] / 100
    pooped_poop = round(pooped_poop)
    weight_add = round(weight_add, 1)
    User.add_item(inter.author.id, 'poop', pooped_poop)
    Pig.add_weight(inter.user.id, weight_add)
    Pig.set_last_feed(inter.author.id, Func.get_current_timestamp())
    await send_callback(inter, embed=embeds.pig_feed(inter, lang, weight_add, pooped_poop))


async def meat(inter):
    await BotUtils.pre_command_check(inter)
    BotUtils.check_pig_meat_cooldown(inter.author)
    lang = User.get_language(inter.author.id)
    if Item.get_amount('knife', inter.author.id) <= 0:
        raise NoItemInInventory('knife', Locales.Meat.no_knife_desc)
    bacon_add = random.randrange(8, 16)
    User.add_item(inter.author.id, 'lard', bacon_add)
    weight_lost = round(random.uniform(.2, .7) * bacon_add, 1)
    Pig.add_weight(inter.user.id, -weight_lost)
    Pig.set_last_meat(inter.author.id, Func.get_current_timestamp())
    await send_callback(inter, embed=embeds.pig_meat(inter, lang, bacon_add, weight_lost))


async def pig_rename(inter, name):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    for i in ['*', '`']:
        name = name.replace(i, '')
    if not name:
        name = 'Hryak'
    Pig.rename(inter.author.id, name)
    await send_callback(inter, embed=embeds.pig_rename(inter, lang))
