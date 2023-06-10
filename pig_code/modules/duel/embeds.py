import asyncio
import datetime
import random

import disnake

from ...core import *
from ...utils import *


def personal_duel_invite(inter, lang, user: disnake.User, bet) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['duel']['invite_title'][lang],
        description=locales['duel']['personal_invite_desc'][lang].format(opponent=user.display_name,
                                                                         user=inter.author.display_name, bet=bet),
        prefix=Func.generate_prefix('⚔️'),
        footer=Func.generate_footer(inter, user=inter.client.user),
        footer_url=Func.generate_footer_url('user_avatar', inter.client.user),
        timestamp=True
    )
    return embed


def personal_dm_duel_invite(inter, lang, bet: int) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['duel']['invite_title'][lang],
        description=locales['duel']['personal_invite_dm_desc'][lang].format(user=inter.author.display_name, bet=bet),
        prefix=Func.generate_prefix('⚔️'),
        footer=Func.generate_footer(inter, user=inter.client.user),
        footer_url=Func.generate_footer_url('user_avatar', inter.client.user),
        timestamp=True
    )
    return embed


def duel_canceled(inter, lang, user: disnake.User, reason: str) -> disnake.Embed:
    description = ''
    if reason == 'opponent_reject':
        description = locales['duel']['opponent_reject_desc'][lang].format(user=user.display_name)
    elif reason == 'no_money_for_bet':
        description = locales['duel']['no_money_for_bet_desc'][lang].format(user=user.display_name)
    elif reason == 'no_response':
        description = locales['duel']['no_response_desc'][lang].format(user=user.display_name)
    embed = BotUtils.generate_embed(
        title=locales['duel']['duel_canceled_title'][lang],
        description=description,
        prefix=Func.generate_prefix('⚔️'),
        footer=Func.generate_footer(inter, user=inter.client.user),
        footer_url=Func.generate_footer_url('user_avatar', inter.client.user),
        timestamp=True
    )
    return embed


def fight_is_starting(inter, lang, user: disnake.User, time_to_start: int, chances) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['duel']['fight_will_start_in'][lang].format(time_to_start=time_to_start),
        description=f'# **{Pig.get_name(inter.author.id)}** *vs* **{Pig.get_name(user.id)}**',
        prefix=Func.generate_prefix('⚔️'),
        footer=Func.generate_footer(inter, user=inter.client.user),
        footer_url=Func.generate_footer_url('user_avatar', inter.client.user),
        timestamp=True,
        fields=[{'name': f'{Pig.get_name(inter.author.id)}',
                 'value': locales['duel']['fight_starting_field_value'][lang].format(
                     weight=Pig.get_weight(inter.author.id), chance=chances[0]),
                 'inline': True},
                {'name': f'{Pig.get_name(user.id)}',
                 'value': locales['duel']['fight_starting_field_value'][lang].format(weight=Pig.get_weight(user.id),
                                                                                     chance=chances[1]),
                 'inline': True
                 },
                ]
    )
    return embed


def fight_is_going(inter, lang, user: disnake.User, gif) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['duel']['fight_is_going_title'][lang],
        description=f'# **{Pig.get_name(inter.author.id)}** *vs* **{Pig.get_name(user.id)}**',
        image_url=gif,
        prefix=Func.generate_prefix('⚔️'),
        footer=Func.generate_footer(inter, user=inter.client.user),
        footer_url=Func.generate_footer_url('user_avatar', inter.client.user),
        timestamp=True
        # fields=[{'name': 'Maxim',
        #          'value': '```Weight: 200 kg\n'
        #                   'Win chance: 70 %```',
        #          'inline': True},
        #         {'name': 'Neiro',
        #          'value': '```Weight: 100 kg\n'
        #                   'Win chance: 30 %```',
        #          'inline': True
        #          },
        #         ]
    )
    return embed


def user_won(inter, lang, user: disnake.User, money_earned, gif) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['duel']['fight_ended_title'][lang],
        description=locales['duel']['fight_ended_desc'][lang].format(user=user.display_name, money_earned=money_earned),
        image_url=gif,
        prefix=Func.generate_prefix('🎉'),
        footer=Func.generate_footer(inter, user=inter.client.user),
        footer_url=Func.generate_footer_url('user_avatar', inter.client.user),
        timestamp=True
        # fields=[{'name': 'Maxim',
        #          'value': '```Weight: 200 kg\n'
        #                   'Win chance: 70 %```',
        #          'inline': True},
        #         {'name': 'Neiro',
        #          'value': '```Weight: 100 kg\n'
        #                   'Win chance: 30 %```',
        #          'inline': True
        #          },
        #         ]
    )
    return embed
