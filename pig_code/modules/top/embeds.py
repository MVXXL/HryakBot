import asyncio
import datetime
import random

import disnake

from ...core import *
from ...utils import *


async def generate_fields(inter, users, top_type, lang,  users_number: int = 10):
    fields = []
    for i, user_id in enumerate(users[:users_number]):
        field_value = 'None'
        if top_type == 'weight':
            field_value = locales['top']['weight_top_field_value'][lang].format(name=Pig.get_name(user_id), weight=Pig.get_weight(user_id))
        elif top_type == 'money':
            field_value = locales['top']['money_top_field_value'][lang].format(money=User.get_money(user_id))
        fields.append({'name': f'{i + 1}. {await User.get_name(inter.client, user_id)}',
                       'value': f'```{field_value}```', 'inline': True})
    return fields

async def weight_top(inter, lang) -> disnake.Embed:
    users = User.get_users_sorted_by('pig', 'weight', exclude=utils_config.ignore_users_in_top)
    fields = await generate_fields(inter, users, 'weight', lang)
    embed = BotUtils.generate_embed(
        title=locales['top']['weight_top_title'][lang],
        prefix=Func.generate_prefix('🐷'),
        footer=Func.generate_footer(inter, user=inter.author),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        fields=fields
    )
    return embed

async def money_top(inter, lang) -> disnake.Embed:
    users = User.get_users_sorted_by('money', exclude=utils_config.ignore_users_in_top)
    fields = await generate_fields(inter, users, 'money', lang)
    print(fields)
    embed = BotUtils.generate_embed(
        title=locales['top']['money_top_title'][lang],
        prefix=Func.generate_prefix('💰'),
        footer=Func.generate_footer(inter, user=inter.author),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        fields=fields
    )
    return embed
