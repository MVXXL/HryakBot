from ...core import *
from ...utils import *
from . import embeds
from . import components


async def feed(inter):
    await Utils.pre_command_check(inter)
    lang = User.get_language(inter.user.id)
    ready_to_feed = Pig.is_ready_to_feed(inter.user.id)
    if not ready_to_feed:
        await error_callbacks.default_error_callback(inter,
                                                     title=translate(Locales.ErrorCallbacks.pig_feed_cooldown_title,
                                                                     lang),
                                                     description=translate(
                                                         Locales.ErrorCallbacks.pig_feed_cooldown_desc, lang,
                                                         {'pig': Pig.get_name(inter.user.id),
                                                          'timestamp': Pig.get_time_of_next_feed(inter.user.id)}),
                                                     color=utils_config.main_color, prefix_emoji='🍖')
        return
    Stats.add_pig_fed(inter.user.id, 1)
    buffs_to_give = await Utils.calculate_buff_multipliers(inter.client, inter.user.id, use_buffs=True)

    add_weight_chances = {'add': 100 - buffs_to_give['vomit_chance'] * 100, 'remove': buffs_to_give['vomit_chance'] * 100}
    vomit = Func.random_choice_with_probability(add_weight_chances) == 'remove'

    pooped_amount = 0
    if not vomit:
        weight_add = random.uniform(1, 10)
        weight_add *= buffs_to_give['weight']

        pooped_amount = random.uniform(5, 15)
        pooped_amount *= buffs_to_give['pooping']
    else:
        weight_add = random.uniform(-5, -1)
    if pooped_amount < 0:
        pooped_amount = 0

    weight_add = round(weight_add, 1)
    pooped_amount = round(pooped_amount)

    Pig.add_weight(inter.user.id, weight_add)
    User.add_item(inter.user.id, 'poop', pooped_amount)
    History.add_feed_to_history(inter.user.id, Func.get_current_timestamp())
    if Func.get_current_timestamp() - History.get_last_streak_timestamp(inter.user.id) >= utils_config.streak_timeout:
        Stats.add_streak(inter.user.id)
        History.add_streak_to_history(inter.user.id, Func.get_current_timestamp(), 'feed')
    await send_callback(inter, embed=await embeds.feed(inter, lang, weight_add, pooped_amount, vomit))


async def butcher(inter):
    await Utils.pre_command_check(inter)
    lang = User.get_language(inter.user.id)
    ready_to_butcher = Pig.is_ready_to_butcher(inter.user.id)
    if not ready_to_butcher:
        await error_callbacks.default_error_callback(inter,
                                                     title=translate(Locales.ErrorCallbacks.pig_butcher_cooldown_title,
                                                                     lang),
                                                     description=translate(
                                                         Locales.ErrorCallbacks.pig_butcher_cooldown_desc, lang,
                                                         {'pig': Pig.get_name(inter.user.id),
                                                          'timestamp': Pig.get_time_of_next_butcher(inter.user.id)}),
                                                     color=utils_config.main_color, prefix_emoji='🥓')
        return
    if Item.get_amount('knife', inter.user.id) <= 0:
        await error_callbacks.no_item(inter, 'knife', description=translate(Locales.Butcher.no_knife_desc,
                                                                            User.get_language(inter.user.id)),
                                      thumbnail_url=await Item.get_image_path('knife'))
        return
    lard_add = random.randrange(8, 16)
    User.add_item(inter.user.id, 'lard', lard_add)
    weight_lost = round(random.uniform(.2, .7) * lard_add, 1)
    Pig.add_weight(inter.user.id, -weight_lost)
    History.add_butcher_to_history(inter.user.id, Func.get_current_timestamp())
    await send_callback(inter, embed=await embeds.butcher(inter, lang, lard_add, weight_lost))


async def rename(inter, name):
    await Utils.pre_command_check(inter)
    lang = User.get_language(inter.user.id)
    for i in ['*', '`']:
        name = name.replace(i, '')
    if not name:
        name = 'Hryak'
    Pig.rename(inter.user.id, name)
    await send_callback(inter, embed=embeds.rename(inter, lang))
