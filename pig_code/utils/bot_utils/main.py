import aiohttp.client_exceptions
import disnake.abc

from ..functions import Func
from ..db_api import *
from ...core import *


async def send_callback(inter,
                        content: str = '',
                        embed: disnake.Embed = None,
                        ephemeral: bool = False,
                        send_to_dm: disnake.User = None,
                        edit_original_message: bool = True,
                        ctx_message: bool = False,
                        components: list = None,
                        files: list = None,
                        retries: int = 3):
    if components is None:
        components = []
    if files is None:
        files = []
    for _ in range(retries):
        message = None
        if not send_to_dm:
            try:
                if ctx_message:
                    try:
                        await inter.response.defer(ephemeral=ephemeral)
                    except Exception as e:
                        pass
                    if type(inter) == disnake.TextChannel:
                        channel = inter
                    else:
                        channel = inter.channel
                    message = await channel.send(content, embed=embed, components=components, files=files)
                elif type(inter) in [disnake.Message, disnake.InteractionMessage]:
                    if edit_original_message:
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
                            extra_kwargs = {}
                            if embed is not None:
                                extra_kwargs['embed'] = embed
                            message = await inter.response.send_message(content, ephemeral=ephemeral,
                                                                        components=components, files=files, **extra_kwargs)
                    except disnake.HTTPException as e:
                        print(e)
                        message = await inter.response.send_message(content, embed=embed, ephemeral=ephemeral,
                                                                    components=components, files=files)

            except aiohttp.client_exceptions.ClientOSError as e:
                print(e)
                await asyncio.sleep(1)
                continue
            except ValueError as e:
                if embed.thumbnail.url is not None and embed.thumbnail.url.startswith('attachment://'):
                    if embed.thumbnail.url is not None:
                        embed.set_thumbnail(file=disnake.File(f'{config.TEMP_FOLDER_PATH}/{embed.thumbnail.url.split("://")[1]}'))
                    if embed.image.url is not None:
                        embed.set_image(file=disnake.File(f'{config.TEMP_FOLDER_PATH}/{embed.thumbnail.url.split("://")[1]}'))
                await asyncio.sleep(.5)
                continue
            except Exception as e:
                raise e
                print('-', e)
        else:
            try:
                message = await send_to_dm.send(content, embed=embed, components=components, files=files)
            except Exception as e:
                # raise e
                print(e)
        return message


def generate_embed(title: str = None,
                   description: str = None,
                   color=utils_config.main_color,
                   prefix: str = None,
                   image_url: str = None,
                   image_file: str = None,
                   thumbnail_url: str = None,
                   thumbnail_file: str = None,
                   footer: str = None,
                   footer_url: str = None,
                   fields: list = None,
                   timestamp=True,
                   inter=None) -> disnake.Embed:
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
    embed = disnake.Embed(
        title=f'{prefix}{title}',
        description=description,
        color=color,
        timestamp=timestamp
    )
    if image_url is not None:
        embed.set_image(image_url)
    if thumbnail_url is not None:
        embed.set_thumbnail(url=thumbnail_url)
    elif thumbnail_file is not None:
        embed.set_thumbnail(file=disnake.File(fp=thumbnail_file))
    elif image_file is not None:
        embed.set_image(file=disnake.File(fp=image_file))
    if footer_url is None and inter is not None:
        footer_url = Func.generate_footer_url('user_avatar', inter.author)
    if footer is not None:
        embed.set_footer(text=footer, icon_url=footer_url)
    elif inter is not None:
        embed.set_footer(text=Func.generate_footer(inter), icon_url=footer_url)
    for field in fields:
        embed.add_field(field['name'] if 'name' in field else None,
                        field['value'] if 'value' in field else None,
                        inline=field['inline'] if 'inline' in field else None)
    return embed


async def send_webhook_embed(url: str, embed=None, content: str = None, username=None, avatar_url=None,
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
            print('Webhook send error', e)
            await asyncio.sleep(1)
            continue


# def translate(locales, lang, format_options: dict = None):
#     translated_text = 'translation_error'
#     if type(locales) == dict:
#         if lang not in locales:
#             lang = 'en'
#         if lang not in locales:
#             lang = list(locales)[0]
#         translated_text = locales[lang]
#     elif type(locales) == str:
#         translated_text = locales
#     if format_options is not None:
#         for k, v in format_options.items():
#             translated_text = translated_text.replace('{'+k+'}', str(v))
#     return translated_text

