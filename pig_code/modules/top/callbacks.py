import asyncio
import datetime
import random

from ...core import *
from ...utils import *
from . import embeds
from . import components


async def top(inter, server_only: bool = False):
    await Botutils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    weight_users = User.get_users_sorted_by('pig', 'weight', exclude=utils_config.ignore_users_in_top)
    money_users = User.get_users_sorted_by('money', exclude=utils_config.ignore_users_in_top)
    if server_only:
        weight_users = Botutils.filter_users(inter.client, weight_users, inter.guild.id)
        money_users = Botutils.filter_users(inter.client, money_users, inter.guild.id)
    weight_users = weight_users[:10]
    money_users = money_users[:10]
    await Botutils.pagination(inter, lang,
                              embeds={
                                  Locales.Top.weight_top_title[lang]: {
                                      'embed': await embeds.weight_top(inter, lang, weight_users),
                                      'components': [await components.choose_user(inter, lang, weight_users)]},
                                  Locales.Top.money_top_title[lang]: {
                                      'embed': await embeds.money_top(inter, lang, money_users),
                                      'components': [await components.choose_user(inter, lang, money_users)]}
                              },
                              arrows=False,
                              categories=True)
