import asyncio
import datetime
import random

import disnake

from ...core import *
from ...utils import *
from . import embeds
from . import components


async def trade_embed(inter, trade_id, lang):
    user1 = await Trades.get_user(inter.client, trade_id, 0)
    user2 = await Trades.get_user(inter.client, trade_id, 1)
    user1_data = Trades.get_user_data(trade_id, 0)
    user2_data = Trades.get_user_data(trade_id, 1)
    return generate_embed(
        f'{Func.generate_prefix("💰")}Торговля',
        # f'Торговля между {await User.get_name(inter.client, list(data)[0])} и '
        # f'{await User.get_name(inter.client, list(data)[1])}',
        fields=[{'name': user1.display_name,
                 'value': f'```{"Нету предметов" if not user1_data else BotUtils.get_items_in_str_list(user1_data, lang)}```',
                 'inline': True},
                {'name': user2.display_name,
                 'value': f'```{"Нету предметов" if not user2_data else BotUtils.get_items_in_str_list(user2_data, lang)}```',
                 'inline': True}],
        thumbnail_file='bin/images/trade.png',
        footer_url=inter.client.user.avatar.url,
        footer='Hryak'
    )



async def trade(inter, user1, user2, trade_id: str = None, pre_command_check=True):
    if pre_command_check:
        await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    if user1 == user2:
        await error_callbacks.default_error_callback(inter, Locales.ErrorCallbacks.cant_trade_with_yourself_title[lang],
                                                     Locales.ErrorCallbacks.cant_trade_with_yourself_desc[lang])
        return
    if user2.bot:
        await error_callbacks.default_error_callback(inter, Locales.ErrorCallbacks.bot_as_trade_user_title[lang],
                                                     Locales.ErrorCallbacks.bot_as_trade_user_desc[lang])
        return
    if trade_id is None:
        m = await send_callback(inter, 'Загрузка...')
        trade_id = str(m.id)
    add_item_component = disnake.ui.StringSelect(placeholder='Добавить предмет',
                                                 custom_id='add_to_trade',
                                                 options=[disnake.SelectOption(label='Деньги',
                                                                               value=f'coins:{trade_id}'),
                                                          disnake.SelectOption(label='Инвентарь',
                                                                               value=f'inventory:{trade_id}'),
                                                          disnake.SelectOption(label='Гардероб',
                                                                               value=f'wardrobe:{trade_id}')
                                                          ])
    if not Trades.exists(trade_id):
        Trades.create_trade(trade_id, user1.id, user2.id)
        await send_callback(inter, embed=await trade_embed(inter, trade_id, lang),
                            components=[add_item_component])
    else:
        await send_callback(inter.client.get_message(int(trade_id)), embed=await trade_embed(inter, trade_id, lang),
                            components=[add_item_component])
