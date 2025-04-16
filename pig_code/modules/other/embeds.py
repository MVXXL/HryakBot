from ...utils import *
from ...utils.discord_utils import generate_embed
from ...core import *



def promo_code_used(inter, lang, prise) -> discord.Embed:
    items_received = DisUtils.get_items_in_str_list(prise, lang)
    embed = generate_embed(title=translate(Locale.PromoCode.promo_code_used_title, lang),
                           description=f'## {translate(Locale.PromoCode.you_got_desc, lang)}\n'
                                       f'```{items_received}```',
                           prefix=Func.generate_prefix('🐷'),
                           inter=inter)
    return embed


def transfer_dm_notification(inter, lang, amount) -> discord.Embed:
    embed = generate_embed(title=translate(Locale.SendMoney.event_title, lang),
                           description=translate(Locale.SendMoney.event_desc, lang,
                                                 {'user': inter.user.display_name, 'money': amount}),
                           prefix=Func.generate_prefix('💸'),
                           inter=inter)
    return embed


def user_used_promocode(inter, lang) -> discord.Embed:
    embed = generate_embed(title=translate(Locale.PromoCode.promo_code_used_error_title, lang),
                           description=f'{translate(Locale.PromoCode.promo_code_used_error_desc, lang)}',
                           prefix=Func.generate_prefix('error'), color=utils_config.error_color,
                           inter=inter)
    return embed


def promocode_expired(inter, lang) -> discord.Embed:
    embed = generate_embed(title=translate(Locale.PromoCode.promocode_expired_title, lang),
                           description=f'{translate(Locale.PromoCode.promocode_expired_desc, lang)}',
                           prefix=Func.generate_prefix('error'),
                           footer=Func.generate_footer(inter), color=utils_config.error_color,
                           inter=inter)
    return embed


def cant_use_promocode(inter, lang) -> discord.Embed:
    embed = generate_embed(title=translate(Locale.PromoCode.cant_use_promocode_title, lang),
                           description=f'{translate(Locale.PromoCode.cant_use_promocode_desc, lang)}',
                           prefix=Func.generate_prefix('error'), color=utils_config.error_color,
                           inter=inter)
    return embed


def promocode_not_exist(inter, lang) -> discord.Embed:
    embed = generate_embed(title=translate(Locale.PromoCode.promocode_not_exist_title, lang),
                           description=f'{translate(Locale.PromoCode.promocode_not_exist_desc, lang)}',
                           prefix=Func.generate_prefix('error'),
                           footer=Func.generate_footer(inter), color=utils_config.error_color,
                           inter=inter)
    return embed


def promocode_used_too_many_times(inter, lang) -> discord.Embed:
    embed = generate_embed(title=translate(Locale.PromoCode.promocode_used_too_many_times_title, lang),
                           description=f'{translate(Locale.PromoCode.promocode_used_too_many_times_desc, lang)}',
                           prefix=Func.generate_prefix('error'),
                           footer=Func.generate_footer(inter), color=utils_config.error_color,
                           inter=inter)
    return embed


def report(inter, lang) -> discord.Embed:
    embed = generate_embed(title=translate(Locale.Report.title, lang),
                           description=f"{translate(Locale.Report.desc, lang)}",
                           prefix=Func.generate_prefix('scd'),
                           inter=inter)
    return embed


def transfer_money(inter, lang, user, amount, currency) -> discord.Embed:
    embed = generate_embed(title=translate(Locale.SendMoney.scd_title, lang),
                           description=f"{translate(Locale.SendMoney.scd_desc, lang, {'money': amount, 'user': user.display_name, 'currency_emoji': Item.get_emoji(currency)})}",
                           prefix=Func.generate_prefix('scd'),
                           color=utils_config.success_color,
                           inter=inter)
    return embed


def cancel_sending_money(inter, lang) -> discord.Embed:
    embed = generate_embed(title=translate(Locale.SendMoney.cancel_title, lang),
                           description=f"{translate(Locale.SendMoney.cancel_desc, lang)}",
                           prefix=Func.generate_prefix('🪙'),
                           timestamp=True,
                           inter=inter)
    return embed


def set_language(inter, lang) -> discord.Embed:
    embed = generate_embed(title=translate(Locale.SetLanguage.scd_title, lang),
                           description=translate(Locale.SetLanguage.scd_desc, lang),
                           prefix=Func.generate_prefix('scd'),
                           inter=inter)
    return embed


def set_join_message(inter, lang, channel, message) -> discord.Embed:
    embed = generate_embed(title=translate(Locale.JoinMessageSet.scd_title, lang, {'channel': channel}),
                           description=translate(Locale.JoinMessageSet.scd_desc,
                                                 lang, {'message': message, 'user': inter.user.mention}),
                           prefix=Func.generate_prefix('scd'),
                           inter=inter)
    return embed


def reset_join_message(inter, lang) -> discord.Embed:
    embed = generate_embed(title=translate(Locale.JoinMessageReset.scd_title, lang),
                           prefix=Func.generate_prefix('scd'),
                           inter=inter)
    return embed


async def wardrobe_item_preview(inter, item_id, lang) -> discord.Embed:
    user_skins = Pig.get_skin(inter.user.id, 'all')
    preview_options = Pig.set_skin_to_options(user_skins, item_id)
    embed = generate_embed(
        title=translate(Locale.WardrobeItemPreview.title, lang, {'item': Item.get_name(item_id, lang)}),
        description=translate(Locale.WardrobeItemPreview.desc, lang, {'item': Item.get_name(item_id, lang)}),
        prefix=Func.generate_prefix('👁️'),
        inter=inter,
        thumbnail_url=await DisUtils.generate_user_pig(inter.user.id,
                                                    preview_items={k: v for k, v in preview_options.items() if
                                                                   k not in user_skins or user_skins[k] != v}),
    )
    return embed
