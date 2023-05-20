import asyncio
import datetime
import random

from ...core import *
from ...utils import *
from . import embeds
from . import components
from .. import errors
from ..inventory.callbacks import inventory_embed
from ..inventory.embeds import inventory_item_selected


async def wardrobe(inter):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    await inventory_embed(inter, lang, inventory_type='wardrobe')


async def wardrobe_item_selected(inter, item_id, message: disnake.Message = None):
    lang = User.get_language(inter.author.id)
    await BotUtils.send_callback(inter if message is None else message,
                                 embed=inventory_item_selected(inter, item_id, lang, 'wardrobe'),
                                 components=components.wardrobe_item_selected(inter.author.id, item_id, lang)
                                 )


async def wardrobe_item_wear(inter, item_id, message: disnake.Message = None):
    lang = User.get_language(inter.author.id)
    Pig.set_skin(inter.author.id, item_id)
    await BotUtils.send_callback(inter if message is None else message,
                                 embed=embeds.wardrobe_item_wear(inter, item_id, lang),
                                 edit_original_message=False,
                                 ephemeral=True
                                 )
    await wardrobe_item_selected(inter, item_id, inter.message)


async def wardrobe_item_remove(inter, item_id, message: disnake.Message = None):
    lang = User.get_language(inter.author.id)
    Pig.remove_skin(inter.author.id, Inventory.get_item_skin_type(item_id))
    await BotUtils.send_callback(inter if message is None else message,
                                 embed=embeds.wardrobe_item_remove(inter, item_id, lang),
                                 edit_original_message=False,
                                 ephemeral=True
                                 )
    await wardrobe_item_selected(inter, item_id, inter.message)


async def wardrobe_item_preview(inter, item_id, message: disnake.Message = None,
                                update_item_selected_embed: bool = True):
    lang = User.get_language(inter.author.id)
    await BotUtils.send_callback(inter if message is None else message,
                                 embed=embeds.wardrobe_item_preview(inter, item_id, lang),
                                 edit_original_message=False,
                                 ephemeral=True
                                 )
    if update_item_selected_embed:
        await wardrobe_item_selected(inter, item_id, inter.message)
