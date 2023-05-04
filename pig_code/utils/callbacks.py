import asyncio
import datetime
import random

import discord_webhook
import disnake
from disnake import Localized
from disnake.ext import commands

from .bot_utils import BotUtils
from ..core import config
from ..core import utils_config
from ..core.bot_locale import locales
from ..core.errors import *
from .functions import *
from .embeds import *
from .db_api.user import *


class Callbacks:


    @staticmethod
    async def profile(inter, lang):
        await Callbacks.send_callback(inter, embed=Embeds.profile(inter, lang))

    @staticmethod
    async def pig_feed(inter, lang):
        if random.randrange(6) != 0:
            weight_add = random.uniform(1, 10)
        else:
            weight_add = random.uniform(-8, -1)
        weight_add = round(weight_add, 1)
        Pig.add_weight(inter.user.id, 0, weight_add)
        Pig.set_last_feed(inter.author.id, 0, int(datetime.datetime.now().timestamp()))
        await Callbacks.send_callback(inter, embed=Embeds.pig_feed(inter, lang, weight_add))

    @staticmethod
    async def pig_rename(inter, lang, name):
        Pig.rename(inter.author.id, 0, name)
        await Callbacks.send_callback(inter, embed=Embeds.pig_rename(inter, lang))

    @staticmethod
    async def set_language(inter, lang):
        User.set_language(inter.author.id, lang)
        await Callbacks.send_callback(inter, embed=Embeds.set_language(inter, lang))

    @staticmethod
    async def error(error, lang, inter):
        text_error = str(type(error)).split('.')[-1].split('\'')[0]
        sec_footer_part = text_error
        error_text = error.args[0].lower()
        if 'unknown interaction' in error_text:
            sec_footer_part = f'/{Func.get_command_name_and_options(inter)[0]}'
        footer_text = f'{inter.author} ・ {sec_footer_part}'
        print(error)
        if 'pigfeedcooldown' in error_text:
            await Callbacks.send_callback(inter, embed=Embeds.generate_embed(
                title=locales['error_callbacks']['pig_feed_cooldown_title'][lang],
                description=locales['error_callbacks']['pig_feed_cooldown_desc'][lang].format(pig=Pig.get_name(inter.author.id, 0), timestamp=Pig.get_time_of_next_feed(inter.author.id, 0)),
                footer=footer_text,
                footer_url=Func.generate_footer_url('user_avatar', inter.author),
                prefix=Func.generate_prefix(inter.guild, '🍖')
            ))






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


    @staticmethod
    async def send_callback(inter,
                            content: str = '',
                            embed: disnake.Embed = None,
                            ephemeral: bool = False,
                            send_to_dm: bool = False,
                            edit_original_message: bool = True,
                            ctx_message: bool = False,
                            components: list = None,
                            files: list = None):
        if components is None:
            components = []
        if files is None:
            files = []
        message = None
        if not send_to_dm:
            try:
                if ctx_message:
                    await inter.response.defer(ephemeral=ephemeral)
                    message = await inter.channel.send(content, embed=embed, components=components, files=files)
                elif type(inter) == disnake.Message:
                    message = await inter.edit(content, embed=embed, components=components, files=files)
                else:
                    try:
                        if edit_original_message:
                            await inter.response.defer(ephemeral=ephemeral)
                    except disnake.errors.InteractionResponded:
                        pass
                    try:
                        if edit_original_message:
                            message = await inter.edit_original_message(content=content, embed=embed,
                                                                        components=components,
                                                                        files=files)
                        else:
                            message = await inter.response.send_message(content, embed=embed, ephemeral=ephemeral,
                                                                        components=components, files=files)
                    except disnake.HTTPException:
                        await inter.channel.send()
                        message = await inter.response.send_message(content, embed=embed, ephemeral=ephemeral,
                                                                    components=components, files=files)
            except:
                pass
        else:
            await inter.author.send(content, embed=embed, components=components, files=files)
        return message

