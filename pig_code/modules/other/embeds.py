import asyncio
import datetime
import random

import disnake

from ...core import *
from ...utils import *


def profile(inter, lang, user: disnake.User = None) -> disnake.Embed:
    if user is None:
        user = inter.author
    embed = BotUtils.generate_embed(
        title=locales['profile']['profile_title'][lang].format(user=user.display_name),
        description=locales['profile']['profile_desc'][lang].format(balance=User.get_money(user.id)),
        prefix=Func.generate_prefix('🐽'),
        thumbnail_file=BotUtils.generate_user_pig(user.id),
        footer=Func.generate_footer(inter, user=user),
        footer_url=Func.generate_footer_url('user_avatar', user),
        timestamp=True,
        fields=[{'name': locales['profile']['pig_field_title'][lang],
                 'value': locales['profile']['pig_field_value'][lang].format(
                     pig_name=Pig.get_name(user.id),
                     weight=Pig.get_weight(user.id))}]
    )
    return embed


def promo_code_used(inter, lang, prise) -> disnake.Embed:
    items_received = '\n'.join(
        [f'{Func.generate_prefix(Inventory.get_item_emoji(k))}{Inventory.get_item_name(k, lang)} x{v}' for k, v in
         prise.items()])
    embed = BotUtils.generate_embed(title=locales["promo_code"]["promo_code_used_title"][lang],
                                    description=f'## {locales["promo_code"]["you_got_desc"][lang]}\n'
                                                f'```{items_received}```',
                                    prefix=Func.generate_prefix('🐷'),
                                    footer=Func.generate_footer(inter),
                                    timestamp=True,
                                    footer_url=Func.generate_footer_url('user_avatar', inter.author))
    return embed


def user_used_promocode(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(title=locales["promo_code"]["promo_code_used_error_title"][lang],
                                    description=f'{locales["promo_code"]["promo_code_used_error_desc"][lang]}',
                                    prefix=Func.generate_prefix('error'),
                                    footer=Func.generate_footer(inter),
                                    timestamp=True, color=utils_config.error_color,
                                    footer_url=Func.generate_footer_url('user_avatar', inter.author))
    return embed


def promocode_expired(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(title=locales["promo_code"]["promocode_expired_title"][lang],
                                    description=f'{locales["promo_code"]["promocode_expired_desc"][lang]}',
                                    prefix=Func.generate_prefix('error'),
                                    footer=Func.generate_footer(inter),
                                    timestamp=True, color=utils_config.error_color,
                                    footer_url=Func.generate_footer_url('user_avatar', inter.author))
    return embed


def cant_use_promocode(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(title=locales["promo_code"]["cant_use_promocode_title"][lang],
                                    description=f'{locales["promo_code"]["cant_use_promocode_desc"][lang]}',
                                    prefix=Func.generate_prefix('error'),
                                    footer=Func.generate_footer(inter),
                                    timestamp=True, color=utils_config.error_color,
                                    footer_url=Func.generate_footer_url('user_avatar', inter.author))
    return embed


def promocode_not_exist(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(title=locales["promo_code"]["promocode_not_exist_title"][lang],
                                    description=f'{locales["promo_code"]["promocode_not_exist_desc"][lang]}',
                                    prefix=Func.generate_prefix('error'),
                                    footer=Func.generate_footer(inter),
                                    timestamp=True, color=utils_config.error_color,
                                    footer_url=Func.generate_footer_url('user_avatar', inter.author))
    return embed


def promocode_used_too_many_times(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(title=locales["promo_code"]["promocode_used_too_many_times_title"][lang],
                                    description=f'{locales["promo_code"]["promocode_used_too_many_times_desc"][lang]}',
                                    prefix=Func.generate_prefix('error'),
                                    footer=Func.generate_footer(inter),
                                    timestamp=True, color=utils_config.error_color,
                                    footer_url=Func.generate_footer_url('user_avatar', inter.author))
    return embed


def stats(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(title=locales['stats']['title'][lang],
                                    description=f"```{locales['stats']['desc'][lang].format(pig_fed=Stats.get_pig_fed(inter.author.id), commands_used=Stats.get_total_commands_used(inter.author.id), money_earned=Stats.get_money_earned(inter.author.id), items_used=Stats.get_total_items_used(inter.author.id), items_sold=Stats.get_total_items_sold(inter.author.id))}```",
                                    prefix=Func.generate_prefix('📊'),
                                    footer=Func.generate_footer(inter),
                                    timestamp=True,
                                    footer_url=Func.generate_footer_url('user_avatar', inter.author))
    return embed


def report(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(title=locales['report']['title'][lang],
                                    description=f"{locales['report']['desc'][lang]}",
                                    prefix=Func.generate_prefix('scd'),
                                    footer=Func.generate_footer(inter),
                                    timestamp=True,
                                    footer_url=Func.generate_footer_url('user_avatar', inter.author))
    return embed


def transfer_money(inter, lang, user, amount) -> disnake.Embed:
    embed = BotUtils.generate_embed(title=locales['transfer_money']['scd_title'][lang],
                                    description=f"{locales['transfer_money']['scd_desc'][lang].format(money=amount, user=user.display_name)}",
                                    prefix=Func.generate_prefix('scd'),
                                    color=utils_config.success_color,
                                    timestamp=True,
                                    footer=Func.generate_footer(inter),
                                    footer_url=Func.generate_footer_url('user_avatar', inter.author))
    return embed


def cancel_sending_money(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(title=locales['transfer_money']['cancel_title'][lang],
                                    description=f"{locales['transfer_money']['cancel_desc'][lang]}",
                                    prefix=Func.generate_prefix('🪙'),
                                    timestamp=True,
                                    footer=Func.generate_footer(inter),
                                    color=utils_config.error_color,
                                    footer_url=Func.generate_footer_url('user_avatar', inter.author))
    return embed


def set_language(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(title=locales['set_language']['scd_title'][lang],
                                    description=locales['set_language']['scd_desc'][
                                        lang],
                                    prefix=Func.generate_prefix('scd'),
                                    timestamp=True,
                                    footer=Func.generate_footer(inter),
                                    footer_url=Func.generate_footer_url('user_avatar', inter.author))
    return embed


def set_join_message(inter, lang, channel, message) -> disnake.Embed:
    embed = BotUtils.generate_embed(title=locales['join_message_set']['scd_title'][lang].format(channel=channel),
                                    description=locales['join_message_set']['scd_desc'][
                                        lang].format(message=message).format(user=inter.author.mention),
                                    prefix=Func.generate_prefix('scd'),
                                    timestamp=True,
                                    footer=Func.generate_footer(inter),
                                    footer_url=Func.generate_footer_url('user_avatar', inter.author))
    return embed


def reset_join_message(inter, lang) -> disnake.Embed:
    embed = BotUtils.generate_embed(title=locales['join_message_reset']['scd_title'][lang],
                                    prefix=Func.generate_prefix('scd'),
                                    timestamp=True,
                                    footer=Func.generate_footer(inter),
                                    footer_url=Func.generate_footer_url('user_avatar', inter.author))
    return embed


def guild_info(client: disnake.Client, guild_id: int, lang) -> disnake.Embed:
    guild = client.get_guild(int(guild_id))
    embed = disnake.Embed(title=guild.name, color=utils_config.main_color)
    embed.add_field(name=locales['words']['owner'][lang],
                    value=f'{guild.owner.mention}')
    embed.add_field(name=locales["words"]['created'][lang],
                    value=f'<t:{round(guild.created_at.timestamp())}:D>\n'
                          f'<t:{round(guild.created_at.timestamp())}:R>')
    icon_value = locales["words"]['no_icon'][lang]
    if guild.icon is not None:
        icon_value = f'[{locales["words"]["click"][lang]}]({guild.icon.url})'
        embed.set_thumbnail(url=guild.icon.url)
    embed.add_field(name=locales["words"]['icon'][lang],
                    value=f'{icon_value}')
    channels_value = f'{locales["words"]["total"][lang]}: **{len(guild.channels)}**\n'
    if len(guild.categories) > 0:
        channels_value += f'{locales["words"]["category"][lang]}: **{len(guild.categories)}**\n'
    if len(guild.text_channels) > 0:
        channels_value += f'{locales["words"]["text"][lang]}: **{len(guild.text_channels)}**\n'
    if len(guild.voice_channels) > 0:
        channels_value += f'{locales["words"]["voice"][lang]}: **{len(guild.voice_channels)}**\n'
    if len(guild.stage_channels) > 0:
        channels_value += f'{locales["words"]["stage"][lang]}: **{len(guild.stage_channels)}**\n'
    if len(guild.stage_channels) > 0:
        channels_value += f'{locales["words"]["forum"][lang]}: **{len(guild.stage_channels)}**\n'
    embed.add_field(
        name=f'{locales["words"]["channels"][lang]}',
        value=channels_value
    )
    embed.add_field(
        name=f'{locales["words"]["members"][lang]}',
        value=f'{locales["words"]["total"][lang]}: **{guild.member_count}**\n'
              f'{locales["words"]["users"][lang]}: **{len([m for m in guild.members if not m.bot])}**\n'
              f'{locales["words"]["bots"][lang]}: **{len([m for m in guild.members if m.bot])}**'
    )
    integration_roles_count = 0
    for role in guild.roles:
        if role.is_bot_managed():
            integration_roles_count += 1
    roles_text = f'{locales["words"]["total"][lang]}: **{len(guild.roles) - 1}**\n'
    if integration_roles_count > 0:
        roles_text += f'{locales["words"]["bot_roles"][lang]}: **{integration_roles_count}**\n'
    if guild.premium_subscriber_role is not None:
        roles_text += f'{locales["words"]["premium"][lang]}: **{guild.premium_subscriber_role.mention}**\n'
    embed.add_field(
        name=f'{locales["words"]["roles"][lang]}',
        value=roles_text
    )
    # if extended:
    #     animated_emojis = [e for e in guild.emojis if e.animated]
    #     if len(guild.emojis) > 0:
    #         emojis_value = f'{random.choice([e for e in guild.emojis if not e.animated])} {locales["total"][lang]}: **{len(guild.emojis)}**\n'
    #         if len(animated_emojis) > 0:
    #             emojis_value += f'{random.choice(animated_emojis)} {locales["animated"][lang]}: **{len(animated_emojis)}**\n'
    #         if len(guild.stickers) > 0:
    #             emojis_value += f'{emojis["sticker"]} {locales["stickers"][lang]}: **{len(guild.stickers)}**'
    #     else:
    #         emojis_value = f'*{locales["no_emojis"][lang]}*'
    #     embed.add_field(
    #         name=f'{locales["emojis"][lang]}',
    #         value=emojis_value
    #     )
    embed.set_footer(text=f'ID: {guild_id}')
    return embed
