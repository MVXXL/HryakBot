import os.path

import aiohttp.client_exceptions
import discord.abc

from ..functions import Func, translate
from ..db_api import *
from ...core import *


async def send_callback(inter,
                        content: str = '',
                        embed: discord.Embed = None,
                        ephemeral: bool = False,
                        send_to_dm: discord.User = None,
                        edit_original_response: bool = True,
                        edit_followup: bool = False,
                        ctx_message: bool = False,
                        components: list = None,
                        attachments: list = None,
                        retries: int = 3):
    view = discord.ui.View()
    components = components or []
    if isinstance(inter,
                  discord.interactions.Interaction) and inter.is_user_integration() and not inter.is_guild_integration():
        content = translate(Locales.user_install_content, User.get_language(inter.user.id)) + '\n' + content
    for component in components:
        view.add_item(component)
    if attachments is None:
        attachments = []
    if embed is not None:
        if embed.thumbnail.url is not None and not embed.thumbnail.url.startswith(
                ('http://', 'https://', 'attachment://')):
            original_embed_thumbnail_path = embed.thumbnail.url
            attachments.append(discord.File(embed.thumbnail.url, filename=os.path.basename(embed.thumbnail.url)))
            embed.set_thumbnail(url=f'attachment://{os.path.basename(embed.thumbnail.url)}')
        if embed.image.url is not None and not embed.image.url.startswith(('http://', 'https://', 'attachment://')):
            original_embed_image_path = embed.thumbnail.url
            attachments.append(discord.File(embed.image.url, filename=os.path.basename(embed.image.url)))
            embed.set_image(url=f'attachment://{os.path.basename(embed.image.url)}')
    for _ in range(retries):
        m = None
        if not send_to_dm:
            try:
                if ctx_message:
                    try:
                        await inter.response.defer(ephemeral=ephemeral)
                    except Exception as e:
                        pass
                    if type(inter) == discord.TextChannel:
                        channel = inter
                    else:
                        channel = inter.channel
                    m = await channel.send_message(content, embed=embed, view=view, attachments=attachments)
                elif edit_followup:
                    await inter.followup.edit_message(inter.message.id, content=content, embed=embed,
                                                      view=view,
                                                      attachments=attachments)
                elif type(inter) in [discord.Message, discord.InteractionMessage]:
                    if edit_original_response:
                        m = await inter.edit(content=content, embed=embed, view=view, attachments=attachments)
                else:
                    try:
                        if edit_original_response:
                            await inter.response.defer(ephemeral=ephemeral)
                    except discord.errors.InteractionResponded as e:
                        pass
                    try:
                        if edit_original_response:
                            try:
                                m = await inter.edit_original_response(content=content, embed=embed,
                                                                             view=view,
                                                                             attachments=attachments)
                            except Exception as e:
                                print(e)
                        else:
                            extra_kwargs = {}
                            if embed is not None:
                                extra_kwargs['embed'] = embed
                            m = await inter.response.send_message(content, ephemeral=ephemeral,
                                                                        view=view, files=attachments,
                                                                        **extra_kwargs)
                    except discord.HTTPException as e:
                        print(e)
                        m = await inter.response.send_message(content, embed=embed, ephemeral=ephemeral,
                                                                    view=view, files=attachments)

            except aiohttp.client_exceptions.ClientOSError as e:
                print(e)
                await asyncio.sleep(1)
                continue
            except ValueError as e:
                print(e)
                if embed.thumbnail.url is not None and embed.thumbnail.url.startswith('attachment://'):
                    if embed.thumbnail.url is not None:
                        for n, file in enumerate(attachments):
                            if file.filename == embed.thumbnail.url.split('://')[1]:
                                attachments.pop(n)
                                attachments.append(discord.File(original_embed_thumbnail_path,
                                                                filename=os.path.basename(
                                                                    original_embed_thumbnail_path)))
                        embed.set_thumbnail(url=f'attachment://{os.path.basename(original_embed_thumbnail_path)}')
                if embed.image.url is not None and embed.image.url.startswith('attachment://'):
                    if embed.image.url is not None:
                        for n, file in enumerate(attachments):
                            if file.filename == embed.image.url.split('://')[1]:
                                attachments.pop(n)
                                attachments.append(discord.File(original_embed_image_path,
                                                                filename=os.path.basename(
                                                                    original_embed_image_path)))
                        embed.set_thumbnail(url=f'attachment://{os.path.basename(original_embed_image_path)}')
                await asyncio.sleep(.5)
                continue
            except Exception as e:
                raise e
        else:
            try:
                m = await send_to_dm.send(content, embed=embed, view=view, files=attachments)
            except Exception as e:
                print(e)
        return m


def generate_embed(title: str = None,
                   description: str = None,
                   color=utils_config.main_color,
                   prefix: str = None,
                   image_url: str = None,
                   thumbnail_url: str = None,
                   footer: str = None,
                   footer_url: str = None,
                   fields: list = None,
                   timestamp: bool = True,
                   inter=None) -> discord.Embed:
    if fields is None:
        fields = []
    if timestamp is True:
        timestamp = datetime.datetime.now()
    elif not timestamp:
        timestamp = None
    elif timestamp is not None:
        timestamp = datetime.datetime.fromtimestamp(timestamp)
    title = '' if title is None else title
    prefix = '' if prefix is None else prefix
    embed = discord.Embed(
        title=f'{prefix}{title}',
        description=description,
        color=color,
        timestamp=timestamp
    )
    if image_url is not None:
        embed.set_image(url=image_url)
    if thumbnail_url is not None:
        embed.set_thumbnail(url=thumbnail_url)
    if footer_url is None and inter is not None:
        footer_url = Func.generate_footer_url('user_avatar', inter.user)
    if footer is not None:
        embed.set_footer(text=footer, icon_url=footer_url)
    elif inter is not None:
        embed.set_footer(text=Func.generate_footer(inter), icon_url=footer_url)
    for field in fields:
        embed.add_field(name=field['name'] if 'name' in field else None,
                        value=field['value'] if 'value' in field else None,
                        inline=field['inline'] if 'inline' in field else None)
    return embed


async def send_webhook(url: str, embed=None, content: str = None, username=None, avatar_url=None,
                       file_name: str = 'webhook.txt', file_content=None, retries: int = 3):
    webhook = discord_webhook.DiscordWebhook(content=content, url=url, username=username, avatar_url=avatar_url)
    if file_content is not None:
        webhook.add_file(filename=file_name, file=file_content)
    if embed is not None:
        webhook.add_embed(embed)
    for i in range(retries):
        try:
            webhook_ex = webhook.execute()
            if webhook_ex.status_code == 200:
                break
            elif webhook_ex.status_code == 429:
                await asyncio.sleep(webhook_ex.json()['retry_after'] / 1000 + .2)
            else:
                break
        except requests.exceptions.SSLError as e:
            print('! Webhook send error', e)
            await asyncio.sleep(1)
            continue
