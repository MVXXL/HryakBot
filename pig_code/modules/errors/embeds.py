import asyncio
import datetime
import random

from ...core import *
from ...utils import *


def default_error_response(inter, title, description, footer, prefix: str = '❌', color: str = utils_config.error_color) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=title,
        description=description,
        prefix=Func.generate_prefix(prefix),
        footer=footer,
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        color=color
    )
    return embed


def not_enough_money(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['error_callbacks']['not_enough_money_title'][lang],
        description=f"{locales['error_callbacks']['not_enough_money_desc'][lang]}",
        prefix=Func.generate_prefix('❌'),
        footer=Func.generate_footer(inter, second_part='no_money'),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        color=utils_config.error_color
    )
    return embed


def no_item(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['error_callbacks']['no_item_title'][lang],
        description=f"{locales['error_callbacks']['no_item_desc'][lang]}",
        prefix=Func.generate_prefix('❌'),
        footer=Func.generate_footer(inter, second_part='no_item'),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        color=utils_config.error_color
    )
    return embed


def wrong_component_clicked(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['error_callbacks']['wrong_component_clicked_title'][lang],
        description=f"{locales['error_callbacks']['wrong_component_clicked_desc'][lang]}",
        prefix=Func.generate_prefix('error'),
        footer=Func.generate_footer(inter, second_part='wrong_page'),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        color=utils_config.error_color
    )
    return embed


def modal_input_is_not_number(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(
        title=locales['error_callbacks']['modal_input_is_not_number_title'][lang],
        description=f"{locales['error_callbacks']['modal_input_is_not_number_desc'][lang]}",
        prefix=Func.generate_prefix('error'),
        footer=Func.generate_footer(inter, second_part='not_number'),
        footer_url=Func.generate_footer_url('user_avatar', inter.author),
        color=utils_config.error_color
    )
    return embed
