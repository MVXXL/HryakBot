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
                        message = await inter.response.send_message(content, embed=embed, ephemeral=ephemeral,
                                                                    components=components, files=files)
                except disnake.HTTPException:
                    await inter.channel.send()
                    message = await inter.response.send_message(content, embed=embed, ephemeral=ephemeral,
                                                                components=components, files=files)
        except Exception as e:
            # raise e
            print(e)
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
                             file_content=None):
    webhook = discord_webhook.DiscordWebhook(content=content, url=url, username=username, avatar_url=avatar_url)
    if file_content is not None:
        webhook.add_file(filename='webhook.txt', file=file_content)
    if embed is not None:
        webhook.add_embed(embed)
    while True:
        webhook_ex = webhook.execute()
        if webhook_ex.status_code == 200:
            break
        else:
            await asyncio.sleep(webhook_ex.json()['retry_after'] / 1000 + .2)


def generate_user_pig(user_id, eye_emotion: str = None):
    return Func.build_pig(tuple(Pig.get_skin(user_id, 'all').items()),
                          tuple(Pig.get_genetic(user_id, 'all').items()),
                          eye_emotion=eye_emotion)
