import asyncio
import datetime

import discord_webhook
import disnake
from disnake import Localized
from disnake.ext import commands

from ..core import config
from ..core import utils_config
from ..core.bot_locale import locales
from ..core.errors import *
from .functions import *
from .db_api import *


class BotUtils:

    @staticmethod
    async def pre_command_check(inter, ephemeral=False, defer=True):
        if defer:
            await inter.response.defer(ephemeral=ephemeral)
        User.register_user_if_not_exists(inter.author.id)
        Pig.create_pig_if_no_pigs(inter.author.id)
        if User.is_blocked(inter.author.id):
            raise UserInBlackList

    @staticmethod
    def check_pig_feed_cooldown(user: disnake.User):
        if Pig.get_last_feed(user.id, 0) is not None:
            if int(datetime.datetime.now().timestamp()) - Pig.get_last_feed(user.id,
                                                                            0) < utils_config.pig_feed_cooldown:
                raise PigFeedCooldown

    @staticmethod
    def generate_embeds_list_from_fields(fields: list, title: str = '', description: str = '', color=utils_config.main_color):
        embeds = []
        create_embed = lambda: BotUtils.generate_embed(title=title, color=color, description=description)
        embed = create_embed()
        for i, field in enumerate(fields):
            embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])
            if i >= 24:
                embeds.append(embed)
                embed = create_embed()
        embeds.append(embed)
        return embeds

    @staticmethod
    def generate_select_components_for_pages(options: list, custom_id, placeholder):
        components = []
        generated_options = []
        for i, option in enumerate(options):
            # embed.add_field(name=field['name'], value=field['value'], inline=field['inline'])
            generated_options.append(disnake.SelectOption(
                label=option['label'],
                value=option['value'],
                emoji=option['emoji'],
                description=option['description']
            ))
            if i >= 24:
                components.append(disnake.ui.Select(options=generated_options, custom_id=custom_id, placeholder=placeholder))
                generated_options = []
        components.append(disnake.ui.Select(options=generated_options, custom_id=custom_id, placeholder=placeholder))
        return components

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
            except Exception as e:
                print(e)
        else:
            await inter.author.send(content, embed=embed, components=components, files=files)
        return message

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
    async def pagination(client,
                         inter,
                         lang: str,
                         embeds: list,
                         components: list = None,
                         timeout: int = 1200,
                         page_label_footer: bool = True,
                         ctx_message: bool = False,
                         everyone_can_click: bool = False,
                         hide_button: bool = True):
        if components is None:
            components = [[]]
        pagination_components = []
        current_page = 1
        if len(embeds) > 1:
            pagination_components.append(
                disnake.ui.Button(
                    style=disnake.ButtonStyle.primary,
                    emoji='◀',
                    custom_id='previous',
                )
            )
            pagination_components.append(disnake.ui.Button(
                style=disnake.ButtonStyle.primary,
                emoji='▶',
                custom_id='next',
            ))
        if hide_button:
            pagination_components.append(BotUtils.generate_hide_button())
        if Func.get_list_dim(components) == 2:
            components = [[components[i], pagination_components] for i in range(len(components))]
        else:
            components = [[components, pagination_components] for _ in range(len(components))]
        components = Func.remove_empty_lists_from_list(components)
        if page_label_footer:
            for i, embed in enumerate(embeds):
                second_footer_part = f'{locales["words"]["page"][lang]}: {i + 1}' if len(embeds) > 1 else 'com_name'
                embed.set_footer(
                    text=Func.generate_footer(inter, second_part=second_footer_part),
                    icon_url=Func.generate_footer_url('user_avatar', inter.author))
        message = await BotUtils.send_callback(inter, embed=embeds[current_page - 1],
                                               components=components[0],
                                               ctx_message=ctx_message, ephemeral=False)

        def check(interaction):
            if message is not None:
                right_message = message.id == interaction.message.id
                return right_message
        while True:

            try:
                interaction = await client.wait_for('button_click', check=check, timeout=timeout)
                if not everyone_can_click and not inter.author.id == interaction.author.id:
                    await BotUtils.send_callback(interaction,
                                                 embed=BotUtils.generate_embed(
                                                     prefix=Func.generate_prefix('❌'),
                                                     color=utils_config.error_color,
                                                     title=locales['pagination']['wrong_user_title'][lang],
                                                     description=locales['pagination']['wrong_user_desc'][
                                                         lang],
                                                     footer=Func.generate_footer(interaction,
                                                                                 second_part='NotYourMessage'),
                                                     footer_url=Func.generate_footer_url('user_avatar',
                                                                                         interaction.author)),
                                                 edit_original_message=False,
                                                 ephemeral=True)
                    continue
            except asyncio.exceptions.TimeoutError as e:
                while True:
                    interaction = await client.wait_for('button_click', check=check)
                    if interaction.component.custom_id == 'hide':
                        await message.delete()
                        return
            if interaction.component.custom_id in ['next', 'previous', 'hide']:
                await interaction.response.defer(ephemeral=True)
            if interaction.component.custom_id == 'next':
                current_page = Func.get_changed_page_number(len(embeds), current_page, 1)
                await BotUtils.send_callback(interaction if not ctx_message else message,
                                             embed=embeds[current_page - 1],
                                             components=components[current_page - 1])
            elif interaction.component.custom_id == 'previous':
                current_page = Func.get_changed_page_number(len(embeds), current_page, -1)
                await BotUtils.send_callback(interaction if not ctx_message else message,
                                             embed=embeds[current_page - 1],
                                             components=components[current_page - 1])
            elif interaction.component.custom_id == 'hide':
                return

    @staticmethod
    def generate_hide_button():
        hide_button = disnake.ui.Button(
            style=disnake.ButtonStyle.red,
            emoji='⛔',
            custom_id='hide',
        )
        return hide_button



    # @staticmethod
    # def make_color(color: str) -> int:
    #     if not color:
    #         color = 0
    #     else:
    #         try:
    #             color = int(color.replace('#', '').replace('0x', ''), 16)
    #         except:
    #             color = 0
    #     return color

    # @staticmethod
    # def send_start_message(client, webhook_url):
    #     if type(client) == commands.bot.InteractionBot:
    #         username = client.user.name
    #         avatar_url = client.user.avatar.url
    #         # user = client.user
    #     else:
    #         username = 'Unknown'
    #         avatar_url = ''
    #         # user = username
    #     webhook = discord_webhook.DiscordWebhook(url=webhook_url,
    #                                              content=config.start_text,
    #                                              username=username,
    #                                              avatar_url=avatar_url)
    #     webhook.execute()
    #

    # @staticmethod
    # async def pre_command(inter, servers_data, black_list, ephemeral=True, defer=True, only_lang=False):
    #     if not only_lang:
    #         if defer:
    #             await inter.response.defer(ephemeral=ephemeral)
    #         if str(inter.author.id) in black_list['users'] and inter.author.id != inter.bot.owner_id:
    #             raise UserInBlackList
    #         if str(inter.guild.id) in black_list['guilds'] and inter.author.id != inter.bot.owner_id:
    #             raise GuildInBlackList
    #     lang = servers_data[str(inter.guild.id)]['lang']
    #     return lang
    #
    # # @staticmethod
    # # async def get_webhook_link(client, channel_id, self_url=True):
    # #     channel = client.get_channel(channel_id)
    # #     if channel is not None:
    # #         for webhook in await channel.webhooks():
    # #             if not self_url and requests.get(webhook.url).status_code == 200:
    # #                 return webhook.url
    # #             elif str(client.user.id) == str(webhook.user.id):
    # #                 return webhook.url
    # #         else:
    # #             webhook = await channel.create_webhook(name=client.user.name,
    # #                                                    avatar=await client.user.avatar.read())
    # #             return webhook.url
    #
    # @staticmethod
    # def get_command_name_and_options(ctx):
    #     try:
    #         sub_commands_types = ['OptionType.sub_command', 'OptionType.sub_command_group',
    #                               'ApplicationCommandType.chat_input']
    #         if ctx.data.options and str(ctx.data.options[0].type) == sub_commands_types[1]:
    #             if ctx.data.options[0].options and str(ctx.data.options[0].options[0].type) == sub_commands_types[0]:
    #                 command_text = f'{ctx.data.name} {ctx.data.options[0].name} {ctx.data.options[0].options[0].name}'
    #                 options = ctx.data.options[0].options[0].options
    #             else:
    #                 command_text = f'{ctx.data.name} {ctx.data.options[0].name}'
    #                 options = ctx.data.options[0].options
    #         elif ctx.data.options and str(ctx.data.options[0].type) == sub_commands_types[0]:
    #             command_text = f'{ctx.data.name} {ctx.data.options[0].name}'
    #             options = ctx.data.options[0].options
    #         else:
    #             command_text = f'{ctx.data.name}'
    #             options = ctx.data.options
    #     except:
    #         command_text, options = ctx.data.name, ctx.data.options
    #     return command_text, options
    #
    # @staticmethod
    # def generate_ephemeral_arg(default_value='true'):
    #     return commands.Param(
    #                   name=Localized(data=locales['ephemeral_var']['name']),
    #                   description=Localized(
    #                       data=locales['ephemeral_var']['description']),
    #                   choices=['✅ True', '❌ False'], default=default_value)
    #
    # @staticmethod
    # def str_to_bool(target):
    #     return True if target.lower() in ['✅ true', 'true', '✅', 'yes', 'да', 'так'] else False
    #
    # @staticmethod
    # def translate_permissions(perms, lang):
    #     missing_perms = []
    #     for perm in perms:
    #         if perm in locales['permissions']:
    #             missing_perms.append(locales['permissions'][perm][lang])
    #         else:
    #             missing_perms.append(perm.replace('_', ' ').capitalize())
    #     return missing_perms
    #
    # @staticmethod
    # def change_page(total_pages, cur_page, differ):
    #     if differ > 0:
    #         if cur_page + differ > total_pages:
    #             cur_page = 1
    #         else:
    #             cur_page += differ
    #     elif differ < 0:
    #         if cur_page + differ < 1:
    #             cur_page = total_pages
    #         else:
    #             cur_page += differ
    #     return cur_page
    #
    # @staticmethod
    # def gen_footer(inter, frst_part='user', sec_part='com_name'):
    #     separator = ' ・ '
    #     if sec_part == 'com_name':
    #         sec_part, options = Func.get_command_name_and_options(inter)
    #         sec_part = f'/{sec_part}'
    #     if frst_part == 'user':
    #         frst_part = inter.author
    #     if not frst_part or not sec_part:
    #         separator = ''
    #     footer = f'{frst_part}{separator}{sec_part}'
    #     return footer
    #
    # @staticmethod
    # def cut_name(name, length, dots=True):
    #     if len(name) > length + 3:
    #         if dots:
    #             name = name[:length - 3] + '...'
    #         else:
    #             name = name[:length]
    #     return name
    #
    # # @staticmethod
    # # def cooldown(inter, rate, per, pro_rate=None, pro_per=None, bucket_type=commands.BucketType.user):
    # #     now = datetime.datetime.now()
    # #     command_name, options = Func.get_command_name_and_options(inter)
    # #     user = data.cooldowns.get((inter.author.id, command_name))
    # #     pro_rate = pro_rate or rate
    # #     pro_per = pro_per or per
    # #     rate = pro_rate if inter.author.id in data.premium_list else rate
    # #     per = pro_per if inter.author.id in data.premium_list else per
    # #     if user and 'time' in user:
    # #         if (now - user['time']).total_seconds() < per:
    # #             if user['rate'] >= rate - 1:
    # #                 dif = per - (now.timestamp() - user['time'].timestamp())
    # #                 raise commands.errors.CommandOnCooldown(rate, dif, bucket_type)
    # #             else:
    # #                 user['rate'] += 1
    # #     else:
    # #         data.cooldowns[(inter.author.id, command_name)] = {
    # #             'rate': 1,
    # #             'time': now
    # #         }
    #
    # @staticmethod
    # def cooldown(inter, rate, per, pro_rate=None, pro_per=None, bucket_type=commands.BucketType.user):
    #     now = datetime.datetime.now()
    #     command_name, options = Func.get_command_name_and_options(inter)
    #     if command_name not in data.cooldowns:
    #         data.cooldowns[command_name] = {}
    #     if inter.author.id not in data.cooldowns[command_name]:
    #         data.cooldowns[command_name][inter.author.id] = {}
    #     if 'rate' not in data.cooldowns[command_name][inter.author.id]:
    #         data.cooldowns[command_name][inter.author.id]['rate'] = 1
    #     user = data.cooldowns[command_name].get(inter.author.id)
    #     pro_rate = rate if pro_rate is None else pro_rate
    #     pro_per = per if pro_per is None else pro_per
    #     rate = pro_rate if str(inter.author.id) in data.premium_list['users'] else rate
    #     per = pro_per if str(inter.author.id) in data.premium_list['users'] else per
    #     if inter.author.id == inter.client.owner.id:
    #         per = 0
    #     change_time = True
    #     if 'time' in user:
    #         if prev_time := user['time']:
    #             if (now - prev_time).total_seconds() < per:
    #                 if data.cooldowns[command_name][inter.author.id]['rate'] >= rate - 1:
    #                     dif = per - (now.timestamp() - prev_time.timestamp())
    #                     raise commands.errors.CommandOnCooldown(rate, dif, bucket_type)
    #                 else:
    #                     change_time = False
    #     data.cooldowns[command_name][inter.author.id]['rate'] += 1
    #     if change_time:
    #         data.cooldowns[command_name][inter.author.id]['rate'] = 0
    #         data.cooldowns[command_name][inter.author.id]['time'] = now
    #
    # @staticmethod
    # def get_prefix(guild, prefix='scd', sep='・'):
    #     if prefix is None:
    #         return ''
    #     emojis = Func.get_emojis(guild)
    #     prefix_emoji = prefix
    #     if prefix == 'scd':
    #         prefix_emoji = emojis["check_mark"]
    #     elif prefix == 'error':
    #         prefix_emoji = emojis["x"]
    #     elif prefix == 'warn':
    #         prefix_emoji = emojis["warn"]
    #     prefix = f'{prefix_emoji}{sep}'
    #     return prefix

    #
    # @staticmethod
    # async def send_command_use_webhook(client, inter):
    #     color = config.main_color
    #     if inter.author.id != client.owner_id:
    #         color = config.default_avatars[int(inter.author.default_avatar.key)]['hex']
    #     options_text = ''
    #     raw_options_text = ''
    #     command_text, options = Func.get_command_name_and_options(inter)
    #     discohook_embed = discord_webhook.DiscordEmbed(title='Command used',
    #                                                    description=f'**User:** {inter.author}\n'
    #                                                                f'**Guild:** `{inter.guild}`\n'
    #                                                                f'**Channel:** `{inter.channel}`\n'
    #                                                                f'**Command:** `{command_text}`\n',
    #                                                    color=color)
    #     for i, option in enumerate(options):
    #         value = option.value
    #         if type(value) == disnake.Member or type(value) == disnake.User:
    #             value = value.id
    #         options_text += f'{option.name}: `{Func.cut_name(value, 20)}`\n'
    #         raw_options_text += f'{option.name}: {Func.cut_name(value, 500)} '
    #     if options_text:
    #         discohook_embed.add_embed_field(name='Options',
    #                                         value=f'{options_text}')
    #     discohook_embed.add_embed_field(name='Raw command',
    #                                     value=f'```/{command_text} {raw_options_text}```',
    #                                     inline=False)
    #     if inter.data.target is not None:
    #         discohook_embed.add_embed_field(name='Target',
    #                                         value=f'{inter.data.target}')
    #     discohook_embed.set_footer(
    #         text=f'Guild ID: {inter.guild.id}\nChannel ID: {inter.channel.id}\nUser ID: {inter.author.id}')
    #     await Func.send_webhook_embed(config.command_use_webhook, discohook_embed, str(inter.client.user), inter.client.user.avatar.url)
    #
    #
    # @staticmethod
    # def numerate_list_to_text(elements_list: list) -> str:
    #     text = ''
    #     for i, j in enumerate(elements_list):
    #         text += f'**{i + 1}.** {j.capitalize()}\n'
    #     return text
    #
    #
    # @staticmethod
    # async def send_webhook_embed(url: str, embed, username=None, avatar_url=None):
    #     webhook = discord_webhook.DiscordWebhook(url=url, username=username, avatar_url=avatar_url)
    #     webhook.add_embed(embed)
    #     while True:
    #         webhook_ex = webhook.execute()
    #         if webhook_ex.status_code == 200:
    #             break
    #         else:
    #             await asyncio.sleep(webhook_ex.json()['retry_after'] / 1000 + .2)
    #
    #
    # @staticmethod
    # def get_emojis(guild):
    #     emojis = config.emojis
    #     if not guild.default_role.permissions.use_external_emojis:
    #         emojis = config.unicode_emojis
    #     return emojis
    #
    #
    # @staticmethod
    # async def send_guild_join_log_message(client, guild):
    #     emojis = Func.get_emojis(guild)
    #     embed = discord_webhook.DiscordEmbed(title='Bot Joined The Guild',
    #                                          description=f'',
    #                                          color=config.main_color)
    #     if guild.icon is not None:
    #         embed.set_thumbnail(url=guild.icon.url)
    #     embed.add_embed_field(name='Name', value=str(guild))
    #     embed.add_embed_field(name='Owner',
    #                           value=f'{guild.owner.mention}')
    #     embed.add_embed_field(name='Created',
    #                           value=f'<t:{round(guild.created_at.timestamp())}:D>\n'
    #                                 f'<t:{round(guild.created_at.timestamp())}:R>')
    #     embed.add_embed_field(
    #         name=f'Members',
    #         value=f'{emojis["members"]} Total: **{guild.member_count}**\n'
    #               f'{emojis["member"]} Users: **{len([m for m in guild.members if not m.bot])}**\n'
    #               f'{emojis["bot"]} Bots: **{len([m for m in guild.members if m.bot])}**'
    #     )
    #     embed.set_footer(text=f'Guild ID: {guild.id} | Owner ID: {guild.owner_id}')
    #     await Func.send_webhook_embed(config.guild_join_webhook, embed,
    #                                   username=str(client.user), avatar_url=client.user.avatar.url)
