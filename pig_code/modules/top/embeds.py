import asyncio
import datetime
import random

import disnake

from ...core import *
from ...utils import *


async def generate_fields(inter, users, top_type, lang):
    fields = []
    for i, user_id in enumerate(users):
        field_value = 'None'
        if top_type == 'weight':
            field_value = locales['top']['weight_top_field_value'][lang].format(name=Pig.get_name(user_id),
                                                                                weight=Pig.get_weight(user_id))
        elif top_type == 'money':
            field_value = locales['top']['money_top_field_value'][lang].format(money=User.get_money(user_id))
        fields.append({'name': f'{i + 1}. {await User.get_name(inter.client, user_id)}',
                       'value': f'```{field_value}```', 'inline': True})
    return fields


async def weight_top(inter, lang, users) -> disnake.Embed:
    fields = await generate_fields(inter, users, 'weight', lang)
    embed = BotUtils.generate_embed(
        title=locales['top']['weight_top_title'][lang],
        prefix=Func.generate_prefix('🐷'),
        footer=Func.generate_footer(inter, user=inter.author),
        timestamp=True,
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        fields=fields
    )
    return embed


async def money_top(inter, lang, users) -> disnake.Embed:
    fields = await generate_fields(inter, users, 'money', lang)
    embed = BotUtils.generate_embed(
        title=locales['top']['money_top_title'][lang],
        prefix=Func.generate_prefix('💰'),
        footer=Func.generate_footer(inter, user=inter.author),
        timestamp=True,
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        fields=fields
    )
    return embed
