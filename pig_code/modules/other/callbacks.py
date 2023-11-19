from ...core import *
from ...utils import *
from . import embeds
from . import components
from ...utils import User, send_callback


async def profile(inter, user: disnake.User = None, pre_command_check: bool = True,
                  edit_original_message: bool = True, ephemeral: bool = False, _components: list = None,
                  info: list = None):
    if pre_command_check:
        await BotUtils.pre_command_check(inter, ephemeral=ephemeral)
    lang = User.get_language(inter.author.id)
    if info is None:
        info = ['user', 'pig']
    if user is None:
        user = inter.author
    User.register_user_if_not_exists(user.id)
    if _components is None:
        _components = []
        _components += [disnake.ui.Button(
            emoji='👍',
            custom_id=f'like;{user.id}',
            style=disnake.ButtonStyle.blurple,
            disabled=True if User.get_rate_number(user.id, inter.author.id) == 1 else False),
            disnake.ui.Button(
                emoji='👎',
                custom_id=f'dislike;{user.id}',
                style=disnake.ButtonStyle.blurple,
                disabled=True if User.get_rate_number(user.id, inter.author.id) == -1 else False
            )
        ]
    await send_callback(inter, embed=BotUtils.profile_embed(inter, lang, user, info), ephemeral=ephemeral,
                        edit_original_message=edit_original_message, components=_components)


async def view(inter, user: disnake.User = None):
    await BotUtils.pre_command_check(inter)
    # lang = User.get_language(inter.author.id)
    if user is None:
        user = inter.author
    User.register_user_if_not_exists(user.id)
    await send_callback(inter, embed=generate_embed(timestamp=False,
                                                    image_file=BotUtils.generate_user_pig(user.id)))


async def stats(inter):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    await BotUtils.pagination(inter, lang, {
        Locales.Stats.base_stats[lang]: embeds.base_stats(inter, lang),
        Locales.Stats.commands_stats[lang]: embeds.commands_stats(inter, lang),
        Locales.Stats.sell_stats[lang]: embeds.sell_stats(inter, lang)
    }, categories=True, arrows=False, embed_thumbnail_file=BotUtils.generate_user_pig(inter.author.id))


async def promocode(inter, code):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    if not PromoCode.exists(code):
        await send_callback(inter, embed=embeds.promocode_not_exist(inter, lang))
        return
    if PromoCode.used_times(code) >= PromoCode.max_uses(code):
        await send_callback(inter, embed=embeds.promocode_used_too_many_times(inter, lang))
        return
    if PromoCode.created(code) + PromoCode.expires_in(code) < Func.get_current_timestamp() and PromoCode.expires_in(
            code) != -1:
        await send_callback(inter, embed=embeds.promocode_expired(inter, lang))
        return
    if PromoCode.get_user_used_times(code, inter.author.id) > 0:
        await send_callback(inter, embed=embeds.user_used_promocode(inter, lang))
        return
    # if PromoCode.get_user_used_times(code, inter.author.id) > 0:
    #     await send_callback(inter, embed=embeds.user_used_promocode(inter, lang))
    #     return
    # if User.is_blocked_promocodes(inter.author.id) and PromoCode.can_use(code) == 'everyone_except_blocked':
    #     await send_callback(inter, embed=embeds.cant_use_promocode(inter, lang))
    #     return
    prise = PromoCode.get_prise(code)
    for item in prise:
        if item == 'coins':
            User.add_item(inter.author.id, 'coins', prise[item])
        elif item == 'weight':
            Pig.add_weight(inter.author.id, prise[item])
        else:
            User.add_item(inter.author.id, item, prise[item])
    PromoCode.add_users_used(code, inter.author.id)
    await send_callback(inter, embed=embeds.promo_code_used(inter, lang, prise))


async def send_money(inter, user, amount, message=None):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    User.register_user_if_not_exists(user.id)
    amount = abs(amount)
    commission = BotUtils.get_commission(inter.author, user)
    amount_with_commission = BotUtils.get_amount_with_commission_to_remove(amount, commission)
    if amount_with_commission > Item.get_amount('coins', inter.author.id):
        raise NoMoney
    confirmation = await BotUtils.confirm_message(inter, lang,
                                                  description=Locales.TransferMoney.confirm_description[
                                                      lang].format(money=amount, user=user.display_name,
                                                                   commission=commission,
                                                                   money_with_commission=amount_with_commission))
    if not confirmation:
        await send_callback(inter, embed=embeds.cancel_sending_money(inter, lang))
        return
    User.add_item(user.id, 'coins', amount)
    User.add_item(inter.author.id, 'coins', -amount_with_commission)
    title = f'{translate(Locales.TransferMoney.event_title, lang)}'
    description = translate(Locales.TransferMoney.event_desc, lang,
                            format_options={'user': inter.author.display_name, 'money': amount})
    if message is not None:
        description += f'\n\n> {Locales.Global.message[lang]}: *{message}*'
    await BotUtils.send_notification(inter, user, title, description,
                                     prefix='💸', send_to_dm=True, create_command_notification=True,
                                     notification_id='money_transfer')
    # await send_callback(inter, user.mention, ctx_message=True)
    # dm_message = await send_callback(inter, send_to_dm=user,
    #                                  embed=generate_embed(title, description,
    #                                                       inter=inter))
    # if dm_message is None:
    #     Events.add(user.id, title=title,
    #                description=description, expires_in=100 * 3600,
    #                description_format={'user': inter.author.display_name, 'money': amount},
    #                event_id='money_transfer')
    await send_callback(inter, embed=embeds.transfer_money(inter, lang, user, amount))


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
    await send_callback(inter, embed=embeds.report(inter, lang))


async def idea(inter, description, anonymous):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    channel = inter.client.get_channel(config.BOT_IDEAS_CHANNEL)
    await channel.create_thread(
        name=f'Идея от {inter.author}' if not anonymous else f'Крутая идея #{str(inter.author.id)[-5:]}',
        content=description, applied_tags=[channel.get_tag_by_name('Другое')]
        # files=[attachment.to_file()]
    )
    await send_callback(inter, embed=generate_embed(title=Locales.Idea.title[lang],
                                                    description=f"{Locales.Idea.desc[lang]}",
                                                    prefix=Func.generate_prefix('scd'),
                                                    inter=inter))


async def say(inter, text):
    await BotUtils.pre_command_check(inter, ephemeral=True)
    if not Guild.is_say_allowed(inter.guild.id):
        lang = User.get_language(inter.author.id)
        await error_callbacks.default_error_callback(inter, Locales.Say.not_allowed_title[lang],
                                                     Locales.Say.not_allowed_desc[lang])
        return
    if not inter.channel.permissions_for(inter.author).mention_everyone:
        text = text.replace('@everyone', '`@everyone`').replace('@here', '`@here`')
    text.replace('\\\\', '\n')

    await inter.channel.send(text)
    message = await send_callback(inter, text)
    await message.delete()


async def set_language(inter, lang):
    await BotUtils.pre_command_check(inter, language_check=False)
    lang = [i for i in bot_locale.full_names if bot_locale.full_names[i] == lang][0]
    User.set_language(inter.author.id, lang)
    Stats.set_language_changed(inter.author.id, True)
    await send_callback(inter, embed=embeds.set_language(inter, lang))


async def set_join_message(inter, channel, message):
    await BotUtils.pre_command_check(inter, language_check=False)
    lang = User.get_language(inter.author.id)
    Guild.set_join_channel(inter.guild.id, channel.id)
    Guild.set_join_message(inter.guild.id, message)
    await send_callback(inter, embed=embeds.set_join_message(inter, lang, channel, message))


async def reset_join_message(inter):
    await BotUtils.pre_command_check(inter, language_check=False)
    lang = User.get_language(inter.author.id)
    Guild.set_join_channel(inter.guild.id, None)
    Guild.set_join_message(inter.guild.id, None)
    await send_callback(inter, embed=embeds.reset_join_message(inter, lang))


async def settings_say(inter, allow: bool):
    await BotUtils.pre_command_check(inter, language_check=False)
    lang = User.get_language(inter.author.id)
    Guild.allow_say(inter.guild.id, allow)
    await send_callback(inter, embed=generate_embed(Locales.SettingsSay.scd_title[lang],
                                                    Locales.SettingsSay.scd_desc[lang],
                                                    prefix=Func.generate_prefix('✅'),
                                                    inter=inter))


async def skin_preview(inter, item_id, message: disnake.Message = None):
    lang = User.get_language(inter.author.id)
    item_id = Item.clean_id(item_id)
    not_compatible_skins = BotUtils.get_not_compatible_skins(inter.author.id, item_id)
    if not_compatible_skins:
        await error_callbacks.not_compatible_skin(inter, item_id, not_compatible_skins, message)
        return
    await send_callback(inter if message is None else message,
                        embed=embeds.wardrobe_item_preview(inter, item_id, lang),
                        edit_original_message=False,
                        ephemeral=True
                        )
