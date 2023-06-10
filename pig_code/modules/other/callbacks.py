import asyncio
import datetime
import random

from ...core import *
from ...utils import *
from . import embeds
from . import components
from .. import errors


async def pre_command_check(inter, ephemeral=False, defer=True):
    if defer:
        await inter.response.defer(ephemeral=ephemeral)
    User.register_user_if_not_exists(inter.author.id)
    Pig.create_pig_if_no_pig(inter.author.id)
    if User.is_blocked(inter.author.id):
        raise UserInBlackList
    # if not Stats.get_language_changed(inter.author.id):
    #     pass


async def profile(inter, user: disnake.User = None, pre_command_check: bool = True,
                  edit_original_message: bool = True, ephemeral: bool = False):
    if pre_command_check:
        await BotUtils.pre_command_check(inter, ephemeral=ephemeral)
    lang = User.get_language(inter.author.id)
    if user is None:
        user = inter.author
    User.register_user_if_not_exists(user.id)
    Pig.create_pig_if_no_pig(user.id)
    await BotUtils.send_callback(inter, embed=embeds.profile(inter, lang, user), ephemeral=ephemeral,
                                 edit_original_message=edit_original_message)


async def stats(inter):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    await BotUtils.send_callback(inter, embed=embeds.stats(inter, lang))


async def promocode(inter, code):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    if not PromoCode.exists(code):
        await BotUtils.send_callback(inter, embed=embeds.promocode_not_exist(inter, lang))
        return
    if PromoCode.used_times(code) >= PromoCode.max_uses(code):
        await BotUtils.send_callback(inter, embed=embeds.promocode_used_too_many_times(inter, lang))
        return
    print(PromoCode.created(code) + PromoCode.expires_in(code), Func.get_current_timestamp())
    if PromoCode.created(code) + PromoCode.expires_in(code) < Func.get_current_timestamp() and PromoCode.expires_in(
            code) != -1:
        await BotUtils.send_callback(inter, embed=embeds.promocode_expired(inter, lang))
        return
    if PromoCode.get_user_used_times(code, inter.author.id) > 0:
        await BotUtils.send_callback(inter, embed=embeds.user_used_promocode(inter, lang))
        return
    # if PromoCode.get_user_used_times(code, inter.author.id) > 0:
    #     await BotUtils.send_callback(inter, embed=embeds.user_used_promocode(inter, lang))
    #     return
    if User.is_blocked_promocodes(inter.author.id) and PromoCode.can_use(code) == 'everyone_except_blocked':
        await BotUtils.send_callback(inter, embed=embeds.cant_use_promocode(inter, lang))
        return
    prise = PromoCode.get_prise(code)
    for item in prise:
        if item == 'coins':
            User.add_money(inter.author.id, prise[item])
        elif item == 'weight':
            Pig.add_weight(inter.author.id, prise[item])
        else:
            Inventory.add_item(inter.author.id, item, prise[item])
    PromoCode.add_users_used(code, inter.author.id)
    await BotUtils.send_callback(inter, embed=embeds.promo_code_used(inter, lang, prise))


async def transfer_money(inter, user, amount):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    User.register_user_if_not_exists(user.id)
    Pig.create_pig_if_no_pig(user.id)
    pigs_weight_dif = Pig.get_weight(inter.author.id) - Pig.get_weight(user.id)
    commission = round(pigs_weight_dif * .35)
    if commission < 5:
        commission = 5
    if commission > 65:
        commission = 65
    amount = abs(amount)
    amount_with_commission = round(amount * ((100 - commission) / 100))
    if amount > User.get_money(inter.author.id):
        raise NoMoney
    confirmation = await BotUtils.confirm_message(inter, lang,
                                                  description=locales['transfer_money']['confirm_description'][
                                                      lang].format(money=amount, user=user.display_name,
                                                                   commission=commission,
                                                                   money_with_commission=amount_with_commission))
    if not confirmation:
        await BotUtils.send_callback(inter, embed=embeds.cancel_sending_money(inter, lang))
        return
    User.add_money(user.id, amount_with_commission)
    User.add_money(inter.author.id, -amount)
    Events.add(user.id, title=locales['transfer_money']['event_title'],
               description=locales['transfer_money']['event_desc'], expires_in=60 * 60 * 24,
               description_format={'user': inter.author.display_name, 'money': amount_with_commission},
               event_id='money_transfer')
    await BotUtils.send_callback(inter, embed=embeds.transfer_money(inter, lang, user, amount_with_commission))


async def report(inter, text, attachment):
    await BotUtils.pre_command_check(inter)
    discohook_embed = discord_webhook.DiscordEmbed(title='Bug Report', color=utils_config.main_color,
                                                   description=text)
    webhook = discord_webhook.DiscordWebhook(content='<@&1106676277143949444>', url=config.REPORT_WEBHOOK,
                                             username='Bug Report')
    if attachment is not None:
        discohook_embed.set_image(url=attachment.url)
    discohook_embed.set_footer(text=f'ID: {inter.author.id}')
    webhook.add_embed(discohook_embed)
    webhook.execute()
    lang = User.get_language(inter.author.id)
    await BotUtils.send_callback(inter, embed=embeds.report(inter, lang))


async def say(inter, text):
    await BotUtils.pre_command_check(inter, ephemeral=True)
    if not inter.channel.permissions_for(inter.author).mention_everyone:
        text = text.replace('@everyone', '`@everyone`').replace('@here', '`@here`')
    text.replace('\\\\', '\n')

    await inter.channel.send(text)
    message = await BotUtils.send_callback(inter, text)
    await message.delete()


async def set_language(inter, lang):
    await BotUtils.pre_command_check(inter, language_check=False)
    lang = [i for i in bot_locale.full_names if bot_locale.full_names[i] == lang][0]
    User.set_language(inter.author.id, lang)
    Stats.set_language_changed(inter.author.id, True)
    await BotUtils.send_callback(inter, embed=embeds.set_language(inter, lang))


async def set_join_message(inter, channel, message):
    await BotUtils.pre_command_check(inter, language_check=False)
    lang = User.get_language(inter.author.id)
    Guild.set_join_channel(inter.guild.id, channel.id)
    Guild.set_join_message(inter.guild.id, message)
    await BotUtils.send_callback(inter, embed=embeds.set_join_message(inter, lang, channel, message))


async def reset_join_message(inter):
    await BotUtils.pre_command_check(inter, language_check=False)
    lang = User.get_language(inter.author.id)
    Guild.set_join_channel(inter.guild.id, None)
    Guild.set_join_message(inter.guild.id, None)
    await BotUtils.send_callback(inter, embed=embeds.reset_join_message(inter, lang))


async def guild_info(inter, guild_id: int):
    lang = User.get_language(inter.author.id)
    await BotUtils.send_callback(inter, embed=embeds.guild_info(inter.client, int(guild_id), lang))
