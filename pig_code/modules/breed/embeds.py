import asyncio
import datetime
import random

import disnake

from ...core import *
from ...utils import *


def pig_breed_ok(inter, lang, became_pregnant, mini_pig) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title='OK',
        description=f'{became_pregnant.display_name}, {Inventory.get_item_name(mini_pig, lang)}',
        prefix=Func.generate_prefix('🐷'),
        footer=Func.generate_footer(inter),
        thumbnail_file=BotUtils.generate_user_pig(inter.author.id),
        timestamp=True,
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
    )
    return embed


def pig_breed_fail(inter, lang, partner) -> disnake.Embed:
    # print(123132, Pig.get_time_of_next_breed(inter.author.id), Func.get_current_timestamp())
    embed = BotUtils.generate_embed(
        title=locales['breed']['fail_title'][lang],
        description=locales['breed']['fail_desc'][lang].format(pig=Pig.get_name(inter.author.id), partner=Pig.get_name(partner.id), retry=Pig.get_time_of_next_breed(inter.author.id)),
        prefix=Func.generate_prefix('🔞'),
        footer=Func.generate_footer(inter),
        thumbnail_file=BotUtils.generate_user_pig(inter.author.id, eye_emotion='sad'),
        timestamp=True,
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
    )
    return embed

def pig_is_too_small_for_breed(inter, lang, user: disnake.User, min_weight_to_breed) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['breed']['not_enough_weight_title'][lang],
        description=locales['breed']['not_enough_weight_desc'][lang].format(pig=Pig.get_name(user.id), weight=min_weight_to_breed),
        prefix=Func.generate_prefix('🐷'),
        footer=Func.generate_footer(inter),
        thumbnail_file=BotUtils.generate_user_pig(inter.author.id, eye_emotion='sad'),
        timestamp=True,
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
    )
    return embed

def personal_breed_invite(inter, lang, user: disnake.User) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['breed']['invite_title'][lang],
        description=locales['breed']['personal_invite_desc'][lang].format(partner=user.display_name,
                                                                         user=inter.author.display_name),
        prefix=Func.generate_prefix('🔞'),
        footer=Func.generate_footer(inter, user=inter.client.user),
        footer_url=Func.generate_footer_url('user_avatar', inter.client.user),
        timestamp=True
    )
    return embed

def breed_canceled(inter, lang, user: disnake.User, reason: str) -> disnake.Embed:
    description = ''
    if reason == 'partner_reject':
        description = locales['breed']['partner_reject_desc'][lang].format(user=user.display_name)
    elif reason == 'no_response':
        description = locales['breed']['no_response_desc'][lang].format(user=user.display_name)
    embed = BotUtils.generate_embed(
        title=locales['breed']['breed_canceled_title'][lang],
        description=description,
        prefix=Func.generate_prefix('🔞'),
        footer=Func.generate_footer(inter, user=inter.client.user),
        footer_url=Func.generate_footer_url('user_avatar', inter.client.user),
        timestamp=True
    )
    return embed


def pregnancy(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title='Pregnancy status',
        description=f'Вы беременны ребёнком: **{Pig.pregnant_with(inter.author.id)}**\n'
                    f'Отец: {Pig.get_name(Pig.pregnant_by(inter.author.id))} ({inter.author.display_name})',
        prefix=Func.generate_prefix('🤰'),
        footer=Func.generate_footer(inter, user=inter.client.user),
        footer_url=Func.generate_footer_url('user_avatar', inter.client.user),
        timestamp=True
    )
    return embed
