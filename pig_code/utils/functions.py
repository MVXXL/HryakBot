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
from ..core.items import items, required_options


class Func:

    @staticmethod
    def correct_dict_id_order(my_dict: dict):
        new_dict = {}
        for i, key in enumerate(my_dict.keys()):
            new_dict[str(i)] = my_dict[key]
        return new_dict


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
    # async def pagination(client, ctx, text, color, page_name: str = 'Page', ctx_message=False, hide_button=True,
    #                      timeout=1200, embeds=None, footer=None, footer_url=None, title=None):
    #     if not text:
    #         return
    #     pages = embeds
    #     current_page = 1
    #     if pages is None:
    #         if type(text) == str:
    #             pages = []
    #             pages_count = 0
    #             embed_len = 0
    #             description = ''
    #             for line in text.split('-|-'):
    #                 embed_len += len(line + '\n')
    #                 if embed_len < 3890:
    #                     description += line + '\n'
    #                 else:
    #                     pages_count += 1
    #                     embed = disnake.Embed(
    #                         title=f'{page_name}: {pages_count}',
    #                         description=description,
    #                         color=color
    #                     )
    #                     embed.set_footer(text=f'{page_name}: {pages_count}')
    #                     pages.append(embed)
    #                     embed_len = 0
    #                     description = ''
    #                     description += line + '\n'
    #             if description:
    #                 pages_count += 1
    #                 embed = disnake.Embed(
    #                     title=f'{page_name}: {pages_count}',
    #                     description=description,
    #                     color=color
    #                 )
    #                 embed.set_footer(text=f'{page_name}: {pages_count}')
    #                 pages.append(embed)
    #         elif type(text) == list:
    #             pages = text
    #     components = []
    #     if len(pages) > 1:
    #         components = [
    #             disnake.ui.Button(
    #                 style=disnake.ButtonStyle.primary,
    #                 emoji='◀',
    #                 custom_id='previous'
    #             ),
    #             disnake.ui.Button(
    #                 style=disnake.ButtonStyle.primary,
    #                 emoji='▶',
    #                 custom_id='next'
    #             )
    #         ]
    #     else:
    #         for i in range(len(pages)):
    #             fixed_embed = pages[i]
    #             fixed_embed.title = None
    #             fixed_embed.remove_footer()
    #             if title is not None:
    #                 fixed_embed.title = title
    #             pages[i] = fixed_embed
    #     if hide_button and ctx_message:
    #         components.append(disnake.ui.Button(
    #             style=disnake.ButtonStyle.red,
    #             emoji='⛔',
    #             custom_id='hide'
    #         ))
    #     message = await Func.send_response(ctx, embed=pages[current_page - 1],
    #                                             components=components,
    #                                             ctx_message=ctx_message, ephemeral=False,
    #                                             footer=footer, footer_url=footer_url)
    #     while True:
    #         def check(interaction):
    #             if message is not None:
    #                 return message.id == interaction.message.id
    #
    #         try:
    #             interaction = await client.wait_for('button_click', check=check, timeout=timeout)
    #         except asyncio.exceptions.TimeoutError as e:
    #             await Func.send_response(message if type(message) == disnake.Message else ctx,
    #                                           embed=pages[current_page - 1],
    #                                           components=components[-1] if hide_button and ctx_message else [],
    #                                           footer=footer, footer_url=footer_url)
    #             del pages
    #             while True:
    #                 interaction = await client.wait_for('button_click', check=check)
    #                 if interaction.component.custom_id == 'hide':
    #                     await message.delete()
    #                     return
    #         await interaction.response.defer(ephemeral=True)
    #         if interaction.component.custom_id == 'next':
    #             current_page = Func.change_page(len(pages), current_page, 1)
    #             await Func.send_response(interaction if not ctx_message else message, embed=pages[current_page - 1],
    #                                           components=components, footer=footer, footer_url=footer_url)
    #         elif interaction.component.custom_id == 'previous':
    #             current_page = Func.change_page(len(pages), current_page, -1)
    #             await Func.send_response(interaction if not ctx_message else message, embed=pages[current_page - 1],
    #                                           components=components, footer=footer, footer_url=footer_url)
    #         elif interaction.component.custom_id == 'hide':
    #             await message.delete()
    #             return

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
    @staticmethod
    def get_command_name_and_options(ctx):
        try:
            sub_commands_types = ['OptionType.sub_command', 'OptionType.sub_command_group',
                                  'ApplicationCommandType.chat_input']
            if ctx.data.options and str(ctx.data.options[0].type) == sub_commands_types[1]:
                if ctx.data.options[0].options and str(ctx.data.options[0].options[0].type) == sub_commands_types[0]:
                    command_text = f'{ctx.data.name} {ctx.data.options[0].name} {ctx.data.options[0].options[0].name}'
                    options = ctx.data.options[0].options[0].options
                else:
                    command_text = f'{ctx.data.name} {ctx.data.options[0].name}'
                    options = ctx.data.options[0].options
            elif ctx.data.options and str(ctx.data.options[0].type) == sub_commands_types[0]:
                command_text = f'{ctx.data.name} {ctx.data.options[0].name}'
                options = ctx.data.options[0].options
            else:
                command_text = f'{ctx.data.name}'
                options = ctx.data.options
        except:
            command_text, options = ctx.data.name, ctx.data.options
        return command_text, options
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

    @staticmethod
    def get_item_index_by_id_from_inventory(inventory, item):
        for i, element in enumerate(inventory):
            if element['item']['id'] == item:
                return i

    # @staticmethod
    # def get_item_by_id(item):
    #     for i, element in enumerate(items):
    #         if element['id'] == item:
    #             return element

    @staticmethod
    def get_index_by_item(inventory, item):
        for i, element in enumerate(inventory):
            if element['item'] == item:
                return i

    @staticmethod
    def generate_footer(inter, first_part: str = 'user', second_part: str = 'com_name'):
        separator = ' ・ '
        if second_part == 'com_name':
            second_part, options = Func.get_command_name_and_options(inter)
            second_part = f'/{second_part}'
        if first_part == 'user':
            first_part = inter.author
        if not first_part or not second_part:
            separator = ''
        footer = f'{first_part}{separator}{second_part}'
        return footer

    @staticmethod
    def generate_footer_url(footer_url, user: disnake.User = None):
        if footer_url == 'user_avatar' and user is not None:
            if user.avatar is not None:
                footer_url = user.avatar.url
            else:
                footer_url = f'https://cdn.discordapp.com/embed/avatars/{user.default_avatar.key}.png'
        else:
            return None
        return footer_url

    @staticmethod
    def generate_prefix(prefix: str = 'scd', sep: str = '・'):
        if prefix is None:
            return ''
        prefix_emoji = prefix
        if prefix == 'scd':
            prefix_emoji = '✅'
        elif prefix == 'error':
            prefix_emoji = '❌'
        elif prefix == 'warn':
            prefix_emoji = '⚠️'
        prefix = f'{prefix_emoji}{sep}'
        return prefix

    @staticmethod
    def convert_hours_to_seconds(hours):
        return hours * 60 ** 2

    @staticmethod
    def get_changed_page_number(total_pages, cur_page, differ):
        if differ > 0:
            if cur_page + differ > total_pages:
                cur_page = 1
            else:
                cur_page += differ
        elif differ < 0:
            if cur_page + differ < 1:
                cur_page = total_pages
            else:
                cur_page += differ
        return cur_page

    @staticmethod
    def _dim(lst):
        if not type(lst) == list:
            return []
        try:
            return [len(lst)] + Func._dim(lst[0])
        except IndexError:
            return [len(lst)]

    @staticmethod
    def get_list_dim(lst):
        return len(Func._dim(lst))

    # @staticmethod
    # def is_2d_list(lst):
    #     if isinstance(lst, list) and len(lst) > 0:
    #         return all(isinstance(i, list) for i in lst) and all(len(i) > 0 for i in lst)
    #     return False
    #
    # @staticmethod
    # def is_3d_list(lst):
    #     if isinstance(lst, list) and len(lst) > 0:
    #         if isinstance(lst[0], list) and len(lst[0]) > 0:
    #             return isinstance(lst[0][0], list)
    #     return False
    #
    @staticmethod
    def remove_empty_lists_from_list(lst):
        new_lst = []
        if Func.get_list_dim(lst) == 2:
            new_lst = []
            for i in lst:
                if i:
                    new_lst.append(i)
        elif Func.get_list_dim(lst) == 3:
            new_lst = []
            for i in lst:
                if i:
                    new_lst.append([])
                    for j in i:
                        if j:
                            new_lst[lst.index(i)].append(j)
        return new_lst

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
    #     emojis = utils_config.emojis
    #     if not guild.default_role.permissions.use_external_emojis:
    #         emojis = utils_config.unicode_emojis
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


