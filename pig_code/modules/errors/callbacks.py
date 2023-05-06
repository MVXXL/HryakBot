import asyncio
import datetime
import random


from ...core import *
from ...utils import *
from . import embeds
from . import components


async def error(error, inter):
    lang = User.get_language(inter.author.id)
    text_error = str(type(error)).split('.')[-1].split('\'')[0]
    sec_footer_part = text_error
    footer_text = f'{inter.author} ・ {sec_footer_part}'
    if type(error) == errors.PigFeedCooldown:
        await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(
            title=locales['error_callbacks']['pig_feed_cooldown_title'][lang],
            description=locales['error_callbacks']['pig_feed_cooldown_desc'][lang].format(
                pig=Pig.get_name(inter.author.id, 0), timestamp=Pig.get_time_of_next_feed(inter.author.id, 0)),
            footer=footer_text,
            footer_url=Func.generate_footer_url('user_avatar', inter.author),
            prefix=Func.generate_prefix('🍖')
        ))
    elif type(error) == errors.PaginationWrongUser:
        await BotUtils.send_callback(inter,
                                     embed=BotUtils.generate_embed(
                                         title=locales['pagination']['wrong_user_title'][lang],
                                         description=locales['pagination']['wrong_user_desc'][
                                             lang]),
                                     edit_original_message=False,
                                     ephemeral=True)
    elif type(error) == errors.NotUserComponentClicked:
        await BotUtils.send_callback(inter,
                                     embed=BotUtils.generate_embed(
                                         title=locales['pagination']['wrong_user_title'][lang],
                                         description=locales['pagination']['wrong_user_desc'][
                                             lang]),
                                     edit_original_message=False,
                                     ephemeral=True)
        # await BotUtils.send_callback(inter, embed=BotUtils.generate_embed(
        #     title=locales['error_callbacks']['pig_feed_cooldown_title'][lang],
        #     description=locales['error_callbacks']['pig_feed_cooldown_desc'][lang].format(
        #         pig=Pig.get_name(inter.author.id, 0), timestamp=Pig.get_time_of_next_feed(inter.author.id, 0)),
        #     footer=footer_text,
        #     footer_url=Func.generate_footer_url('user_avatar', inter.author),
        #     prefix=Func.generate_prefix('🍖')
        # ))
    else:
        raise error

    # if type(error) == commands.errors.CommandOnCooldown:
    #     retry = locales["retry_in_s"][lang].format(round(error.retry_after,
    #                                                      1)) if error.retry_after < 60 else f'{locales["retry"][lang]} <t:{round(datetime.datetime.now().timestamp() + error.retry_after)}:R>'
    #     await Func.send_callback(inter, title=f"{locales['error_titles']['cooldown'][lang]}",
    #                              description=f'*{retry}*', prefix='warn', color=config.warn_color,
    #                              footer=footer_text, footer_url=footer_image)
    # elif type(error) == commands.errors.MissingPermissions:
    #     perms = Func.translate_permissions(error.missing_permissions, lang)
    #     await Func.send_callback(inter, title=f"{locales['error_titles']['missing_perms'][lang]}",
    #                              description=Func.numerate_list_to_text(perms), color=config.error_color,
    #                              footer=footer_text, footer_url=footer_image, prefix='error')
    # elif type(error) == commands.errors.BotMissingPermissions:
    #     perms = Func.translate_permissions(error.missing_permissions, lang)
    #     await Func.send_callback(inter, title=f"{locales['error_titles']['bot_missing_perms'][lang]}",
    #                              description=Func.numerate_list_to_text(perms), color=config.error_color,
    #                              footer=footer_text, footer_url=footer_image, prefix='error')
    # elif type(error) == commands.errors.NotOwner:
    #     await Func.send_callback(inter, title=f"{locales['error_titles']['not_owner'][lang]}",
    #                              color=config.error_color,
    #                              footer=footer_text, footer_url=footer_image, prefix='error')
    # elif type(error) == commands.errors.GuildNotFound:
    #     await Func.send_callback(inter,
    #                              title=f"{locales['error_titles']['guild_not_found'][lang].format(f'*{error.argument}*')}",
    #                              color=config.error_color,
    #                              footer=footer_text, footer_url=footer_image, prefix='error')
    # # elif type(error) == commands.errors.BadColourArgument:
    # #     await Func.send_response(inter, 'error', title=f"{locales['error_titles']['unknown_color'][lang]}",
    # #                              color=config.error_color,
    # #                              footer=footer_text, footer_url=footer_image, prefix='error')
    # # elif type(error) == commands.errors.MessageNotFound:
    # #     await Func.send_response(inter, 'error', title=f"{locales['error_titles']['unknown_message'][lang]}",
    # #                              color=config.error_color,
    # #                              footer=footer_text, footer_url=footer_image, prefix='error')
    # elif 'userinblacklist' in error_text:
    #     description = ''
    #     if data.black_list['users'][str(inter.author.id)]['reason'] is not None:
    #         description = f"*- {locales['reason'][lang]}:* {data.black_list['users'][str(inter.author.id)]['reason']}"
    #     await Func.send_callback(inter, 'error', title=f"{locales['error_titles']['user_blocked'][lang]}", description=description,
    #                              footer=footer_text, footer_url=footer_image, prefix='error')
    # elif 'guildinblacklist' in error_text:
    #     description = ''
    #     if data.black_list['guilds'][str(inter.guild.id)]['reason'] is not None:
    #         description = f"*- {locales['reason'][lang]}:* {data.black_list['guilds'][str(inter.author.id)]['reason']}"
    #     await Func.send_callback(inter, title=f"{locales['error_titles']['guild_blocked'][lang]}", description=description,
    #                              footer=footer_text, footer_url=footer_image, prefix='error')
    # elif 'notpremiumuser' in error_text:
    #     await Func.send_callback(inter, title=f"{locales['error_titles']['not_premium'][lang]}",
    #                              description=locales['error_descs']['not_premium'][lang],
    #                              footer=footer_text, footer_url=footer_image, prefix='💎', color=config.premium_color)
    # # elif 'templatenotfound' in error_text:
    # #     await Func.send_response(inter, 'error', title=locales['error_titles']['unknown_template'][lang],
    # #                              footer=footer_text, footer_url=footer_image, prefix='error')
    # # elif 'nicknamesnotfound' in error_text:
    # #     await Func.send_response(inter, 'error',
    # #                              title=locales['error_titles']["nicknames_not_found"][lang],
    # #                              footer=footer_text, footer_url=footer_image, prefix='error')
    # # elif 'noemojis' in error_text:
    # #     await Func.send_response(inter, 'warn', title=locales['error_titles']['no_emojis'][lang],
    # #                              footer=footer_text, footer_url=footer_image, prefix='error')
    # # elif 'badroletoadd' in error_text:
    # #     await Func.send_response(inter, 'error', title=locales['error_titles']['bad_role'][lang],
    # #                              footer=footer_text, footer_url=footer_image, prefix='error')
    # # elif 'toproleerror' in error_text:
    # #     role_id = error_text.split('`')[1].split()[1]
    # #     guild_id = error_text.split('`')[1].split()[0]
    # #     guild = inter.client.get_guild(int(guild_id))
    # #     role = guild.get_role(int(role_id))
    # #     await Func.send_response(inter, 'error',
    # #                              title=locales['check_role_to_add']['position_error'][lang].format(role),
    # #                              image_url=config.image_resources['replace_role'],
    # #                              footer=footer_text, footer_url=footer_image, prefix='error')
    # # elif 'unknown interaction' in error_text:
    # #     await Func.send_response(inter, 'error', title=f"{locales['unknown_interaction_error_title'][lang]}",
    # #                              description=f"{locales['unknown_interaction_error_desc'][lang]}", send_to_dm=True,
    # #                              footer=footer_text, footer_url=footer_image, prefix='error')
    # # elif 'missing permissions' in error_text:
    # #     await Func.send_response(inter, 'error', title=f"{locales['error_titles']['bot_missing_perms'][lang]}",
    # #                              footer=footer_text, footer_url=footer_image, prefix='error')
    # # elif 'unknown emoji' in error_text:
    # #     await Func.send_response(inter, 'error', title=f"{locales['unknown_emoji_error'][lang]}",
    # #                              footer=footer_text, footer_url=footer_image, prefix='error')
    # # elif 'unsupported image type' in error_text:
    # #     await Func.send_response(inter, 'error', title=f"{locales['unsupported_image_type_error'][lang]}",
    # #                              footer=footer_text, footer_url=footer_image, prefix='error')
    # # elif 'asset exceeds maximum size' in error_text:
    # #     await Func.send_response(inter, 'error', title=f"{locales['asset_exceeds_maximum_size_error'][lang]}",
    # #                              footer=footer_text, footer_url=footer_image, prefix='error')
    # # elif 'maximum number of emojis reached' in error_text:
    # #     await Func.send_response(inter, 'error', title=f"{locales['maximum_number_of_emojis_reached_error'][lang]}",
    # #                              footer=footer_text, footer_url=footer_image, prefix='error')
    # # elif 'unknown server template' in error_text:
    # #     await Func.send_response(inter, 'error', title=f"{locales['unknown_template_error'][lang]}",
    # #                              footer=footer_text, footer_url=footer_image, prefix='error')
    # # elif 'invalid destination language' in error_text:
    # #     await Func.send_response(inter, 'error', title=f"{locales['invalid_destination_language_error'][lang]}",
    # #                              footer=footer_text, footer_url=footer_image, prefix='error')
    # elif 'cannot send messages to this user' in error_text:
    #     await Func.send_callback(inter, title=f"{locales['error_titles']['cannot_send_dm'][lang]}",
    #                              description=f'*- {locales["error_descs"]["cannot_send_dm"][lang]}*',
    #                              footer=footer_text, footer_url=footer_image, prefix='error', color=config.error_color)
    # else:
    #     await Func.send_callback(inter, title=f"{locales['error_titles']['error'][lang]}",
    #                              color=config.error_color,
    #                              description=locales['unknown_error']['description'][lang],
    #                              footer=footer_text, footer_url=footer_image, prefix='error')
    #     error_by = ''
    #     more_info = ''
    #     if inter is not None:
    #         try:
    #             error_by += f'**Guild:** `{inter.guild.name}`|`[{inter.guild.id}]`\n'
    #         except:
    #             pass
    #         error_by += f'**User:** <@{inter.user.id}>|`[{inter.user.id}]`\n'
    #     try:
    #         command_text, options = Func.get_command_name_and_options(inter)
    #         if inter is None:
    #             exc_type, exc_obj, exc_tb = sys.exc_info()
    #             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    #             more_info = f'**Function:** `{traceback.extract_tb(sys.exc_info()[-1], 1)[0][2]}`\n' \
    #                         f'**File:** `{fname}`\n' \
    #                         f'**Line:** `{exc_tb.tb_lineno}`\n'
    #         else:
    #             more_info = f'**Cog:** `{inter.application_command.cog_name}`\n' \
    #                         f'**Command:** `{command_text}`\n'
    #     except AttributeError:
    #         pass
    #     description = f'{error_by}' \
    #                   f'{more_info}' \
    #                   f'**Error:** `{type(error)}`\n' \
    #                   f'```{error}```'
    #     discohook_embed = discord_webhook.DiscordEmbed(title='Debugger',
    #                                                    description=description,
    #                                                    color=config.error_color)
    #     await Func.send_webhook_embed(config.DEBUGGER_WEBHOOK, discohook_embed, username=str(inter.client.user),
    #                                   avatar_url=inter.client.user.avatar.url)

async def not_enough_money(inter):
    lang = User.get_language(inter.author.id)
    await BotUtils.send_callback(inter, embed=embeds.not_enough_money(inter, lang), ephemeral=True,
                                 edit_original_message=False)


async def no_item(inter):
    lang = User.get_language(inter.author.id)
    await BotUtils.send_callback(inter, embed=embeds.no_item(inter, lang), ephemeral=True,
                                 edit_original_message=False)


async def wrong_component_clicked(inter):
    lang = User.get_language(inter.author.id)
    await BotUtils.send_callback(inter, embed=embeds.wrong_component_clicked(inter, lang),
                                 edit_original_message=False, ephemeral=True)


async def modal_input_is_not_number(inter):
    lang = User.get_language(inter.author.id)
    await BotUtils.send_callback(inter, embed=embeds.modal_input_is_not_number(inter, lang),
                                 edit_original_message=False, ephemeral=True)
