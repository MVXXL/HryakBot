import asyncio
import datetime
import random

from ...core import *
from ...utils import *
from . import embeds
from . import components


async def top(inter, _global: bool = False):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    guild = None if _global else inter.guild
    exclude_users = utils_config.ignore_users_in_top
    order_by = "JSON_EXTRACT(pig, '$.weight')"
    weight_users = Tech.get_all_users(order_by=order_by, exclude_users=exclude_users,
                                      guild=guild, limit=10)
    user_weight_position = Tech.get_user_position(inter.author.id, order_by=order_by, exclude_users=exclude_users, guild=guild)
    order_by = "JSON_EXTRACT(inventory, '$.coins.amount')"
    coins_users = Tech.get_all_users(order_by=order_by, exclude_users=exclude_users,
                                      guild=guild, limit=10)
    user_coins_position = Tech.get_user_position(inter.author.id, order_by=order_by, exclude_users=exclude_users, guild=guild)
    order_by = "JSON_EXTRACT(inventory, '$.hollars.amount')"
    hollars_users = Tech.get_all_users(order_by=order_by, exclude_users=exclude_users,
                                      guild=guild, limit=10)
    user_hollars_position = Tech.get_user_position(inter.author.id, order_by=order_by, exclude_users=exclude_users, guild=guild)
    print('============================')
    await BotUtils.pagination(inter, lang,
                              embeds={
                                  Locales.Top.weight_top_title[lang]: {
                                      'embed': await embeds.generate_top_embed(inter, lang,
                                                                               translate(Locales.Top.weight_top_title,
                                                                                         lang),
                                                                               translate(
                                                                                   Locales.Top.weight_top_description,
                                                                                   lang),
                                                                               await embeds.generate_users_list(inter,
                                                                                                                weight_users,
                                                                                                                Pig.get_weight,
                                                                                                                key_word=translate(
                                                                                                                    Locales.Global.kg,
                                                                                                                    lang)),
                                                                               prefix='🐖', user_position=user_weight_position,
                                                                               thumbnail_file=Func.get_image_path_from_link(
                                                                                   utils_config.image_links['top'])),
                                      'components': [await components.choose_user(inter, lang, weight_users)]},
                                  Locales.Top.coins_top_title[lang]: {
                                      'embed': await embeds.generate_top_embed(inter, lang,
                                                                               translate(Locales.Top.coins_top_title,
                                                                                         lang),
                                                                               translate(
                                                                                   Locales.Top.coins_top_description,
                                                                                   lang),
                                                                               await embeds.generate_users_list(inter,
                                                                                                                coins_users,
                                                                                                                Item.get_amount,
                                                                                                                func_kwargs={
                                                                                                                    'item_id': 'coins'},
                                                                                                                key_word='🪙'),
                                                                               prefix='💰', user_position=user_coins_position,
                                                                               thumbnail_file=Func.get_image_path_from_link(
                                                                                   utils_config.image_links['top'])),
                                      'components': [await components.choose_user(inter, lang, coins_users)]},
                                  Locales.Top.hollars_top_title[lang]: {
                                      'embed': await embeds.generate_top_embed(inter, lang,
                                                                               translate(Locales.Top.hollars_top_title,
                                                                                         lang),
                                                                               translate(
                                                                                   Locales.Top.hollars_top_description,
                                                                                   lang),
                                                                               await embeds.generate_users_list(inter,
                                                                                                                hollars_users,
                                                                                                                Item.get_amount,
                                                                                                                func_kwargs={
                                                                                                                    'item_id': 'hollars'},
                                                                                                                key_word='💵'),
                                                                               prefix='💸', user_position=user_hollars_position,
                                                                               thumbnail_file=Func.get_image_path_from_link(
                                                                                   utils_config.image_links['top'])),
                                      'components': [await components.choose_user(inter, lang, hollars_users)]},
                              },
                              arrows=False,
                              categories=True)
