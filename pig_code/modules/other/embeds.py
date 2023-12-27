from ...core import *
from ...utils import *





def promo_code_used(inter, lang, prise) -> disnake.Embed:
    items_received = BotUtils.get_items_in_str_list(prise, lang)
    embed = generate_embed(title=Locales.PromoCode.promo_code_used_title[lang],
                           description=f'## {Locales.PromoCode.you_got_desc[lang]}\n'
                                       f'```{items_received}```',
                           prefix=Func.generate_prefix('🐷'),
                           inter=inter)
    return embed


def transfer_dm_notification(inter, lang, amount) -> disnake.Embed:
    embed = generate_embed(title=Locales.TransferMoney.event_title[lang],
                           description=Locales.TransferMoney.event_desc[lang].format(
                               user=inter.author.display_name, money=amount),
                           prefix=Func.generate_prefix('💸'),
                           inter=inter)
    return embed


def user_used_promocode(inter, lang) -> disnake.Embed:
    embed = generate_embed(title=Locales.PromoCode.promo_code_used_error_title[lang],
                           description=f'{Locales.PromoCode.promo_code_used_error_desc[lang]}',
                           prefix=Func.generate_prefix('error'), color=utils_config.error_color,
                           inter=inter)
    return embed


def promocode_expired(inter, lang) -> disnake.Embed:
    embed = generate_embed(title=Locales.PromoCode.promocode_expired_title[lang],
                           description=f'{Locales.PromoCode.promocode_expired_desc[lang]}',
                           prefix=Func.generate_prefix('error'),
                           footer=Func.generate_footer(inter), color=utils_config.error_color,
                           inter=inter)
    return embed


def cant_use_promocode(inter, lang) -> disnake.Embed:
    embed = generate_embed(title=Locales.PromoCode.cant_use_promocode_title[lang],
                           description=f'{Locales.PromoCode.cant_use_promocode_desc[lang]}',
                           prefix=Func.generate_prefix('error'), color=utils_config.error_color,
                           inter=inter)
    return embed


def promocode_not_exist(inter, lang) -> disnake.Embed:
    embed = generate_embed(title=Locales.PromoCode.promocode_not_exist_title[lang],
                           description=f'{Locales.PromoCode.promocode_not_exist_desc[lang]}',
                           prefix=Func.generate_prefix('error'),
                           footer=Func.generate_footer(inter), color=utils_config.error_color,
                           inter=inter)
    return embed


def promocode_used_too_many_times(inter, lang) -> disnake.Embed:
    embed = generate_embed(title=Locales.PromoCode.promocode_used_too_many_times_title[lang],
                           description=f'{Locales.PromoCode.promocode_used_too_many_times_desc[lang]}',
                           prefix=Func.generate_prefix('error'),
                           footer=Func.generate_footer(inter), color=utils_config.error_color,
                           inter=inter)
    return embed


def base_stats(inter, lang) -> disnake.Embed:
    embed = generate_embed(title=Locales.Stats.base_stats[lang],
                           description=f"```{Locales.Stats.base_stats_desc[lang].format(pig_fed=Stats.get_pig_fed(inter.author.id), commands_used=Stats.get_total_commands_used(inter.author.id), money_earned=Stats.get_money_earned(inter.author.id), items_sold=Stats.get_total_items_sold(inter.author.id))}```",
                           prefix=Func.generate_prefix('📊'),
                           inter=inter)
    return embed


def commands_stats(inter, lang) -> disnake.Embed:
    commands_stats = Stats.get_commands_stats(inter.author.id)
    description = '\n'.join([f'{j} - /{i}' for i, j in Func.sort_by_values(commands_stats, reverse=True).items()])
    embed = generate_embed(title=Locales.Stats.commands_stats[lang],
                           description=f"```{Locales.Stats.commands_stats_desc[lang]}\n{description}```",
                           prefix=Func.generate_prefix('📊'),
                           inter=inter)
    return embed


def sell_stats(inter, lang) -> disnake.Embed:
    commands_stats = Stats.get_items_sold_stats(inter.author.id)
    description = '\n'.join([f'{Item.get_emoji(i)} {Item.get_name(i, lang)}: {j}' for i, j in
                             Func.sort_by_values(commands_stats, reverse=True).items()])
    embed = generate_embed(title=Locales.Stats.sell_stats[lang],
                           description=f"```{Locales.Stats.sell_stats_desc[lang] if description else Locales.Stats.no_stats[lang]}\n{description}```",
                           prefix=Func.generate_prefix('📊'),
                           inter=inter)
    return embed


def report(inter, lang) -> disnake.Embed:
    embed = generate_embed(title=Locales.Report.title[lang],
                           description=f"{Locales.Report.desc[lang]}",
                           prefix=Func.generate_prefix('scd'),
                           inter=inter)
    return embed


def transfer_money(inter, lang, user, amount) -> disnake.Embed:
    embed = generate_embed(title=Locales.TransferMoney.scd_title[lang],
                           description=f"{Locales.TransferMoney.scd_desc[lang].format(money=amount, user=user.display_name)}",
                           prefix=Func.generate_prefix('scd'),
                           color=utils_config.success_color,
                           inter=inter)
    return embed


def cancel_sending_money(inter, lang) -> disnake.Embed:
    embed = generate_embed(title=Locales.TransferMoney.cancel_title[lang],
                           description=f"{Locales.TransferMoney.cancel_desc[lang]}",
                           prefix=Func.generate_prefix('🪙'),
                           timestamp=True,
                           inter=inter)
    return embed


def set_language(inter, lang) -> disnake.Embed:
    embed = generate_embed(title=Locales.SetLanguage.scd_title[lang],
                           description=Locales.SetLanguage.scd_desc[
                               lang],
                           prefix=Func.generate_prefix('scd'),
                           inter=inter)
    return embed


def set_join_message(inter, lang, channel, message) -> disnake.Embed:
    embed = generate_embed(title=Locales.JoinMessageSet.scd_title[lang].format(channel=channel),
                           description=Locales.JoinMessageSet.scd_desc[
                               lang].format(message=message).format(user=inter.author.mention),
                           prefix=Func.generate_prefix('scd'),
                           inter=inter)
    return embed


def reset_join_message(inter, lang) -> disnake.Embed:
    embed = generate_embed(title=Locales.JoinMessageReset.scd_title[lang],
                           prefix=Func.generate_prefix('scd'),
                           inter=inter)
    return embed


async def wardrobe_item_preview(inter, item_id, lang) -> disnake.Embed:
    skin_type = Item.get_skin_type(item_id)
    preview_options = Pig.get_skin(inter.author.id, 'all')
    preview_options[skin_type] = item_id
    embed = generate_embed(
        title=Locales.WardrobeItemPreview.title[lang].format(item=Item.get_name(item_id, lang)),
        description=Locales.WardrobeItemPreview.desc[lang].format(item=Item.get_name(item_id, lang)),
        prefix=Func.generate_prefix('👁️'),
        inter=inter,
        thumbnail_file=await BotUtils.build_pig(tuple(preview_options.items()),
                                      tuple(Pig.get_genetic(inter.author.id, 'all').items())),
    )
    return embed
    # def guild_info(client: disnake.Client, guild_id: int, lang) -> disnake.Embed:
    #     guild = client.get_guild(int(guild_id))
    #     embed = disnake.Embed(title=guild.name, color=utils_config.main_color)
    #     embed.add_field(name=Locales.Global.owner[lang],
    #                     value=f'{guild.owner.mention}')
    #     embed.add_field(name=locales["words"]['created'][lang],
    #                     value=f'<t:{round(guild.created_at.timestamp())}:D>\n'
    #                           f'<t:{round(guild.created_at.timestamp())}:R>')
    #     icon_value = locales["words"]['no_icon'][lang]
    #     if guild.icon is not None:
    #         icon_value = f'[{locales["words"]["click"][lang]}]({guild.icon.url})'
    #         embed.set_thumbnail(url=guild.icon.url)
    #     embed.add_field(name=locales["words"]['icon'][lang],
    #                     value=f'{icon_value}')
    #     channels_value = f'{locales["words"]["total"][lang]}: **{len(guild.channels)}**\n'
    #     if len(guild.categories) > 0:
    #         channels_value += f'{locales["words"]["category"][lang]}: **{len(guild.categories)}**\n'
    #     if len(guild.text_channels) > 0:
    #         channels_value += f'{locales["words"]["text"][lang]}: **{len(guild.text_channels)}**\n'
    #     if len(guild.voice_channels) > 0:
    #         channels_value += f'{locales["words"]["voice"][lang]}: **{len(guild.voice_channels)}**\n'
    #     if len(guild.stage_channels) > 0:
    #         channels_value += f'{locales["words"]["stage"][lang]}: **{len(guild.stage_channels)}**\n'
    #     if len(guild.stage_channels) > 0:
    #         channels_value += f'{locales["words"]["forum"][lang]}: **{len(guild.stage_channels)}**\n'
    #     embed.add_field(
    #         name=f'{locales["words"]["channels"][lang]}',
    #         value=channels_value
    #     )
    #     embed.add_field(
    #         name=f'{locales["words"]["members"][lang]}',
    #         value=f'{locales["words"]["total"][lang]}: **{guild.member_count}**\n'
    #               f'{locales["words"]["users"][lang]}: **{len([m for m in guild.members if not m.bot])}**\n'
    #               f'{locales["words"]["bots"][lang]}: **{len([m for m in guild.members if m.bot])}**'
    #     )
    #     integration_roles_count = 0
    #     for role in guild.roles:
    #         if role.is_bot_managed():
    #             integration_roles_count += 1
    #     roles_text = f'{locales["words"]["total"][lang]}: **{len(guild.roles) - 1}**\n'
    #     if integration_roles_count > 0:
    #         roles_text += f'{locales["words"]["bot_roles"][lang]}: **{integration_roles_count}**\n'
    #     if guild.premium_subscriber_role is not None:
    #         roles_text += f'{locales["words"]["premium"][lang]}: **{guild.premium_subscriber_role.mention}**\n'
    #     embed.add_field(
    #         name=f'{locales["words"]["roles"][lang]}',
    #         value=roles_text
    #     )
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
