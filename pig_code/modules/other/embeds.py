from ...utils import *
from ...utils.discord_utils import generate_embed
from ...core import *



async def promo_code_used(inter, lang, prise) -> discord.Embed:
    items_received = await DisUtils.get_items_in_str_list(prise, lang)
    embed = generate_embed(title=translate(Locales.PromoCode.promo_code_used_title, lang),
                           description=f'## {translate(Locales.PromoCode.you_got_desc, lang)}\n'
                                       f'```{items_received}```',
                           prefix=Func.generate_prefix('🐷'),
                           inter=inter)
    return embed


async def transfer_dm_notification(inter, lang, amount) -> discord.Embed:
    embed = generate_embed(title=translate(Locales.SendMoney.event_title, lang),
                           description=translate(Locales.SendMoney.event_desc, lang,
                                                 {'user': inter.user.display_name, 'money': amount}),
                           prefix=Func.generate_prefix('💸'),
                           inter=inter)
    return embed


async def user_used_promocode(inter, lang) -> discord.Embed:
    embed = generate_embed(title=translate(Locales.PromoCode.promo_code_used_error_title, lang),
                           description=f'{translate(Locales.PromoCode.promo_code_used_error_desc, lang)}',
                           prefix=Func.generate_prefix('error'), color=config.error_color,
                           inter=inter)
    return embed


async def promocode_expired(inter, lang) -> discord.Embed:
    embed = generate_embed(title=translate(Locales.PromoCode.promocode_expired_title, lang),
                           description=f'{translate(Locales.PromoCode.promocode_expired_desc, lang)}',
                           prefix=Func.generate_prefix('error'),
                           footer=Func.generate_footer(inter), color=config.error_color,
                           inter=inter)
    return embed


async def cant_use_promocode(inter, lang) -> discord.Embed:
    embed = generate_embed(title=translate(Locales.PromoCode.cant_use_promocode_title, lang),
                           description=f'{translate(Locales.PromoCode.cant_use_promocode_desc, lang)}',
                           prefix=Func.generate_prefix('error'), color=config.error_color,
                           inter=inter)
    return embed


async def promocode_not_exist(inter, lang) -> discord.Embed:
    embed = generate_embed(title=translate(Locales.PromoCode.promocode_not_exist_title, lang),
                           description=f'{translate(Locales.PromoCode.promocode_not_exist_desc, lang)}',
                           prefix=Func.generate_prefix('error'),
                           footer=Func.generate_footer(inter), color=config.error_color,
                           inter=inter)
    return embed


async def promocode_used_too_many_times(inter, lang) -> discord.Embed:
    embed = generate_embed(title=translate(Locales.PromoCode.promocode_used_too_many_times_title, lang),
                           description=f'{translate(Locales.PromoCode.promocode_used_too_many_times_desc, lang)}',
                           prefix=Func.generate_prefix('error'),
                           footer=Func.generate_footer(inter), color=config.error_color,
                           inter=inter)
    return embed


async def report(inter, lang) -> discord.Embed:
    embed = generate_embed(title=translate(Locales.Report.title, lang),
                           description=f"{translate(Locales.Report.desc, lang)}",
                           prefix=Func.generate_prefix('scd'),
                           inter=inter)
    return embed


async def transfer_money(inter, lang, user, amount, currency) -> discord.Embed:
    embed = generate_embed(title=translate(Locales.SendMoney.scd_title, lang),
                           description=f"{translate(Locales.SendMoney.scd_desc, lang, {'money': amount, 'user': user.display_name, 'currency_emoji': await Item.get_emoji(currency)})}",
                           prefix=Func.generate_prefix('scd'),
                           color=config.success_color,
                           inter=inter)
    return embed


async def cancel_sending_money(inter, lang) -> discord.Embed:
    embed = generate_embed(title=translate(Locales.SendMoney.cancel_title, lang),
                           description=f"{translate(Locales.SendMoney.cancel_desc, lang)}",
                           prefix=Func.generate_prefix('🪙'),
                           timestamp=True,
                           inter=inter)
    return embed


async def set_language(inter, lang) -> discord.Embed:
    embed = generate_embed(title=translate(Locales.SetLanguage.scd_title, lang),
                           description=translate(Locales.SetLanguage.scd_desc, lang),
                           prefix=Func.generate_prefix('scd'),
                           inter=inter)
    return embed


async def set_join_message(inter, lang, channel, message) -> discord.Embed:
    embed = generate_embed(title=translate(Locales.JoinMessageSet.scd_title, lang, {'channel': channel}),
                           description=translate(Locales.JoinMessageSet.scd_desc,
                                                 lang, {'message': message, 'user': inter.user.mention}),
                           prefix=Func.generate_prefix('scd'),
                           inter=inter)
    return embed


async def reset_join_message(inter, lang) -> discord.Embed:
    embed = generate_embed(title=translate(Locales.JoinMessageReset.scd_title, lang),
                           prefix=Func.generate_prefix('scd'),
                           inter=inter)
    return embed


async def wardrobe_item_preview(inter, item_id, lang) -> discord.Embed:
    user_skins = await Pig.get_skin(inter.user.id, 'all')
    preview_options = await Pig.set_skin_to_options(user_skins, item_id)
    embed = generate_embed(
        title=translate(Locales.WardrobeItemPreview.title, lang, {'item': await Item.get_name(item_id, lang)}),
        description=translate(Locales.WardrobeItemPreview.desc, lang, {'item': await Item.get_name(item_id, lang)}),
        prefix=Func.generate_prefix('👁️'),
        inter=inter,
        thumbnail_url=await DisUtils.generate_user_pig(inter.user.id,
                                                    preview_items={k: v for k, v in preview_options.items() if
                                                                   k not in user_skins or user_skins[k] != v}),
    )
    return embed
