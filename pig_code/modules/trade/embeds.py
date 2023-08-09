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
            field_value = Locales.Top.weight_top_field_value[lang].format(name=Pig.get_name(user_id),
                                                                          weight=Pig.get_weight(user_id))
        elif top_type == 'money':
            field_value = Locales.Top.money_top_field_value[lang].format(money=User.get_money(user_id))
        elif top_type == 'likes':
            field_value = Locales.Top.likes_top_field_value[lang].format(likes=len(User.get_likes(user_id)))
        fields.append({'name': f'{i + 1}. {await User.get_name(inter.client, user_id)}',
                       'value': f'```{field_value}```', 'inline': True})
    return fields


async def weight_top(inter, lang, users) -> disnake.Embed:
    fields = await generate_fields(inter, users, 'weight', lang)
    embed = generate_embed(
        title=Locales.Top.weight_top_title[lang],
        prefix=Func.generate_prefix('🐷'),
        inter=inter,
        fields=fields,
        # thumbnail_url=BotUtils.build_pig((('hat', 'cylinder'), ))
    )
    return embed


async def money_top(inter, lang, users) -> disnake.Embed:
    fields = await generate_fields(inter, users, 'money', lang)
    embed = generate_embed(
        title=Locales.Top.money_top_title[lang],
        prefix=Func.generate_prefix('💰'),
        inter=inter,
        fields=fields
    )
    return embed

async def likes_top(inter, lang, users) -> disnake.Embed:
    fields = await generate_fields(inter, users, 'likes', lang)
    embed = generate_embed(
        title=Locales.Top.likes_top_title[lang],
        prefix=Func.generate_prefix('❤️'),
        inter=inter,
        fields=fields
    )
    return embed
