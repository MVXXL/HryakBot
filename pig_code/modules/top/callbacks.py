import asyncio
import datetime
import random

from ...core import *
from ...utils import *
from . import embeds
from . import components


async def top(inter, _global: bool = False):
    await Utils.pre_command_check(inter)
    lang = User.get_language(inter.user.id)

    if not _global and not inter.guild.chunked:
        await error_callbacks.bot_is_restarting(inter)
        return

    guild = None if _global else inter.guild
    exclude_users = utils_config.ignore_users_in_top

    async def exclude_bots(l):
        new_l = []
        for i in l:
            user = await User.get_user(inter.client, i)
            if not user.bot:
                new_l.append(i)
        return new_l

    order_by = "JSON_EXTRACT(pig, '$.weight')"
    weight_users = await exclude_bots(Tech.get_all_users(order_by=order_by, exclude_users=exclude_users,
                                                         guild=guild, limit=10))
    user_weight_position = Tech.get_user_position(inter.user.id, order_by=order_by, exclude_users=exclude_users,
                                                  guild=guild)
    order_by = "JSON_EXTRACT(inventory, '$.coins.amount')"
    coins_users = await exclude_bots(Tech.get_all_users(order_by=order_by, exclude_users=exclude_users,
                                                        guild=guild, limit=10))
    user_coins_position = Tech.get_user_position(inter.user.id, order_by=order_by, exclude_users=exclude_users,
                                                 guild=guild)
    order_by = "JSON_EXTRACT(inventory, '$.hollars.amount')"
    hollars_users = await exclude_bots(Tech.get_all_users(order_by=order_by, exclude_users=exclude_users,
                                                          guild=guild, limit=10))
    user_hollars_position = Tech.get_user_position(inter.user.id, order_by=order_by, exclude_users=exclude_users,
                                                   guild=guild)
    order_by = "JSON_EXTRACT(stats, '$.streak')"
    streak_users = await exclude_bots(Tech.get_all_users(order_by=order_by, exclude_users=exclude_users,
                                                          guild=guild, limit=10))
    user_streak_position = Tech.get_user_position(inter.user.id, order_by=order_by, exclude_users=exclude_users,
                                                   guild=guild)
    await Utils.pagination(inter, lang,
                           embeds={
                                  translate(Locales.Top.weight_top_title, lang): {
                                      'embed': await embeds.generate_top_embed(inter, lang,
                                                                               translate(Locales.Top.weight_top_title,
                                                                                         lang),
                                                                               translate(
                                                                                   Locales.Top.weight_top_desc,
                                                                                   lang),
                                                                               await embeds.generate_users_list(inter,
                                                                                                                weight_users,
                                                                                                                Pig.get_weight,
                                                                                                                key_word=translate(
                                                                                                                    Locales.Global.kg,
                                                                                                                    lang)),
                                                                               prefix_emoji='🐖',
                                                                               user_position=user_weight_position,
                                                                               thumbnail_url=await Func.get_image_temp_path_from_path_or_link(utils_config.image_links['top'])),
                                      'components': [await components.choose_user(inter, lang, weight_users)]},
                                  translate(Locales.Top.coins_top_title, lang): {
                                      'embed': await embeds.generate_top_embed(inter, lang,
                                                                               translate(Locales.Top.coins_top_title,
                                                                                         lang),
                                                                               translate(
                                                                                   Locales.Top.coins_top_desc,
                                                                                   lang),
                                                                               await embeds.generate_users_list(inter,
                                                                                                                coins_users,
                                                                                                                Item.get_amount,
                                                                                                                func_kwargs={
                                                                                                                    'item_id': 'coins'},
                                                                                                                key_word='🪙'),
                                                                               prefix_emoji='💰',
                                                                               user_position=user_coins_position,
                                                                               thumbnail_url=await Func.get_image_temp_path_from_path_or_link(utils_config.image_links['top'])),
                                      'components': [await components.choose_user(inter, lang, coins_users)]},
                                  translate(Locales.Top.hollars_top_title, lang): {
                                      'embed': await embeds.generate_top_embed(inter, lang,
                                                                               translate(Locales.Top.hollars_top_title,
                                                                                         lang),
                                                                               translate(
                                                                                   Locales.Top.hollars_top_desc,
                                                                                   lang),
                                                                               await embeds.generate_users_list(inter,
                                                                                                                hollars_users,
                                                                                                                Item.get_amount,
                                                                                                                func_kwargs={
                                                                                                                    'item_id': 'hollars'},
                                                                                                                key_word='💵'),
                                                                               prefix_emoji='💸',
                                                                               user_position=user_hollars_position,
                                                                               thumbnail_url=await Func.get_image_temp_path_from_path_or_link(utils_config.image_links['top'])),
                                      'components': [await components.choose_user(inter, lang, hollars_users)]},
                               translate(Locales.Top.streak_top_title, lang): {
                                   'embed': await embeds.generate_top_embed(inter, lang,
                                                                            translate(Locales.Top.streak_top_title,
                                                                                      lang),
                                                                            translate(
                                                                                Locales.Top.streak_top_desc,
                                                                                lang),
                                                                            await embeds.generate_users_list(inter,
                                                                                                             streak_users,
                                                                                                             Stats.get_streak,
                                                                                                             key_word='🔥'),
                                                                            prefix_emoji='🔥',
                                                                            user_position=user_streak_position,
                                                                            thumbnail_url=await Func.get_image_temp_path_from_path_or_link(
                                                                                utils_config.image_links['top'])),
                                   'components': [await components.choose_user(inter, lang, streak_users)]},
                              },
                           arrows=False,
                           categories=True)
