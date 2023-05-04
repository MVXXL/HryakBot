import asyncio
import datetime
import random

import discord_webhook
import disnake
from disnake import Localized
from disnake.ext import commands

from ..core import config
from ..core import utils_config
from ..core.bot_locale import locales
from ..core.errors import *
from .functions import *
from .db_api.user import *
from .db_api.pig import *
from .bot_utils import BotUtils


class Embeds:

    @staticmethod
    def generate_embed(title: str = None,
                       description: str = None,
                       color=utils_config.main_color,
                       prefix: str = None,
                       image_url: str = None,
                       thumbnail_url: str = None,
                       footer: str = None,
                       footer_url: str = None,
                       fields: list = None,
                       timestamp=None) -> disnake.Embed:
        if fields is None:
            fields = []
        if timestamp:
            timestamp = datetime.datetime.now()
        title = '' if title is None else title
        prefix = '' if prefix is None else prefix
        embed = disnake.Embed(
            title=f'{prefix}{title}',
            description=description,
            color=color,
            timestamp=timestamp
        )
        if image_url is not None:
            embed.set_image(image_url)
        if thumbnail_url is not None:
            embed.set_thumbnail(thumbnail_url)
        if footer is not None:
            embed.set_footer(text=footer, icon_url=footer_url)
        for field in fields:
            embed.add_field(field['title'] if 'title' in field else None,
                            field['value'] if 'value' in field else None,
                            inline=field['inline'] if 'inline' in field else None)
        return embed

    @staticmethod
    def profile(inter, lang) -> disnake.Embed:
        embed = Embeds.generate_embed(
            title=locales['profile']['profile_title'][lang],
            description=locales['profile']['profile_desc'][lang].format(balance=User.get_money(inter.author.id)),
            prefix=Func.generate_prefix(inter.guild, '🐽'),
            thumbnail_url=inter.author.avatar.url,
            footer=Func.generate_footer(inter, 'user', 'com_name'),
            footer_url=Func.generate_footer_url('user_avatar', inter.author),
            fields=[{'title': locales['profile']['pig_field_title'][lang],
                     'value': locales['profile']['pig_field_value'][lang].format(
                         pig_name=Pig.get_name(inter.author.id, 0),
                         weight=Pig.get_weight(inter.author.id, 0))}]
        )
        return embed

    @staticmethod
    def pig_feed(inter, lang, weight_changed) -> disnake.Embed:
        description = ''
        if weight_changed > 0:
            description = random.choice(locales['feed']['feed_scd_desc_list'][lang])
        if weight_changed < 0:
            description = random.choice(locales['feed']['feed_fail_desc_list'][lang])
        embed = Embeds.generate_embed(
            title=locales['feed']['feed_title'][lang],
            description=f'- {description.format(pig=Pig.get_name(inter.author.id, 0), mass=abs(weight_changed))}\n\n'
                        f"*{locales['feed']['total_pig_weight'][lang].format(weight=Pig.get_weight(inter.author.id, 0))}*",
            prefix=Func.generate_prefix(inter.guild, '🐷'),
            footer=Func.generate_footer(inter, 'user', 'com_name'),
            footer_url=Func.generate_footer_url('user_avatar', inter.author),
        )
        return embed

    @staticmethod
    def pig_rename(inter, lang) -> disnake.Embed:
        embed = Embeds.generate_embed(
            title=locales['rename']['scd_title'][lang].format(pig=Pig.get_name(inter.author.id, 0)),
            prefix=Func.generate_prefix(inter.guild, '🐷'),
            footer=Func.generate_footer(inter, 'user', 'com_name'),
            footer_url=Func.generate_footer_url('user_avatar', inter.author),
        )
        return embed

    @staticmethod
    def set_language(inter, lang) -> disnake.Embed:
        embed = Embeds.generate_embed(title=locales['set_language']['scd_title'][lang],
                                      description=locales['set_language']['scd_desc'][
                                          lang],
                                      prefix=Func.generate_prefix(inter.guild, '✅'),
                                      footer=Func.generate_footer(inter),
                                      footer_url=Func.generate_footer_url('user_avatar', inter.author))
        return embed
