import asyncio
import datetime
import random

from ...core import *
from ...utils import *


def default_error_response(inter, title, description, footer, prefix: str = '❌', timestamp: bool = False,
                           color: str = utils_config.error_color) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=title,
        description=description,
        prefix=Func.generate_prefix(prefix),
        footer=footer,
        timestamp=True if timestamp else None,
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        color=color
    )
    return embed


def bot_as_opponent_duel(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['error_callbacks']['bot_as_opponent_duel_title'][lang],
        description=locales['error_callbacks']['bot_as_opponent_duel_desc'][lang],
        timestamp=True,
        prefix=Func.generate_prefix('❌'),
        footer=Func.generate_footer(inter),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        color=utils_config.error_color
    )
    return embed


def cant_play_with_yourself_duel(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['error_callbacks']['cant_play_with_yourself_duel_title'][lang],
        description=locales['error_callbacks']['cant_play_with_yourself_duel_desc'][lang],
        timestamp=True,
        prefix=Func.generate_prefix('❌'),
        footer=Func.generate_footer(inter),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        color=utils_config.error_color
    )
    return embed

def bot_as_partner_breed(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['error_callbacks']['bot_as_partner_breed_title'][lang],
        description=locales['error_callbacks']['bot_as_partner_breed_desc'][lang],
        timestamp=True,
        prefix=Func.generate_prefix('❌'),
        footer=Func.generate_footer(inter),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        color=utils_config.error_color
    )
    return embed


def cant_breed_with_yourself(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['error_callbacks']['cant_breed_with_yourself_title'][lang],
        description=locales['error_callbacks']['cant_breed_with_yourself_desc'][lang],
        timestamp=True,
        prefix=Func.generate_prefix('❌'),
        footer=Func.generate_footer(inter),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        color=utils_config.error_color
    )
    return embed


def not_enough_money(inter, lang, description: str = None) -> disnake.Embed:
    description = locales['error_callbacks']['not_enough_money_desc'][lang] if description is None else description
    embed = BotUtils.generate_embed(
        title=locales['error_callbacks']['not_enough_money_title'][lang],
        description=description,
        timestamp=True,
        prefix=Func.generate_prefix('❌'),
        footer=Func.generate_footer(inter),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        color=utils_config.error_color
    )
    return embed


def no_item(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['error_callbacks']['no_item_title'][lang],
        description=f"{locales['error_callbacks']['no_item_desc'][lang]}",
        prefix=Func.generate_prefix('❌'),
        timestamp=True,
        footer=Func.generate_footer(inter),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        color=utils_config.error_color
    )
    return embed


def wrong_component_clicked(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['error_callbacks']['wrong_component_clicked_title'][lang],
        description=f"{locales['error_callbacks']['wrong_component_clicked_desc'][lang]}",
        prefix=Func.generate_prefix('error'),
        timestamp=True,
        footer=Func.generate_footer(inter),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        color=utils_config.error_color
    )
    return embed


def modal_input_is_not_number(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['error_callbacks']['modal_input_is_not_number_title'][lang],
        description=f"{locales['error_callbacks']['modal_input_is_not_number_desc'][lang]}",
        prefix=Func.generate_prefix('error'),
        timestamp=True,
        footer=Func.generate_footer(inter),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        color=utils_config.error_color
    )
    return embed
