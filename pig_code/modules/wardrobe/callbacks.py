import asyncio
import datetime
import random

from ...core import *
from ...utils import *
from . import embeds
from . import components
from .. import errors


async def wardrobe(inter, client):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    await BotUtils.inventory_embed(client, inter, lang, inventory_type='wardrobe')
    # item_fields = []
    # options = []
    # for item in User.get_inventory(inter.author.id):
    #     if Inventory.get_item_type(item).split(':')[0] == 'skin':
    #         item_label_without_prefix = f'{Inventory.get_item_name(item, lang)} x{Inventory.get_item_amount(inter.author.id, item)}'
    #         item_fields.append(
    #             {'name': f'{Func.generate_prefix(Inventory.get_item_emoji(item))}{item_label_without_prefix}',
    #              'value': f'{locales["words"]["description"][lang]}: *{Inventory.get_item_description(item, lang)}*\n'
    #                       f'{locales["words"]["type"][lang]}: `{Inventory.get_item_type(item, lang)}`',
    #              'inline': False})
    #         options.append(
    #             {'label': item_label_without_prefix,
    #              'value': f'{item}',
    #              'emoji': Inventory.get_item_emoji(item),
    #              'description': Inventory.get_item_description(item, lang)
    #              }
    #         )
    # embeds = BotUtils.generate_embeds_list_from_fields(item_fields,
    #                                                    description='' if item_fields else
    #                                                    locales['wardrobe']['wardrobe_empty_desc'][lang],
    #                                                    title=f"{Func.generate_prefix('📦')}{locales['wardrobe']['wardrobe_title'][lang]}")
    # components = BotUtils.generate_select_components_for_pages(options, 'wardrobe_item_select',
    #                                                            locales['wardrobe']['select_item_placeholder'][
    #                                                                lang])
    # await BotUtils.pagination(client, inter, lang, embeds=embeds, components=components if options else None,
    #                           hide_button=False)


async def wardrobe_item_selected(inter, item_id, message: disnake.Message = None):
    lang = User.get_language(inter.author.id)
    await BotUtils.send_callback(inter if message is None else message,
                                 embed=embeds.wardrobe_item_selected(inter, item_id, lang),
                                 components=components.wardrobe_item_selected(inter.author.id, item_id, lang)
                                 )


async def wardrobe_item_wear(inter, item_id, message: disnake.Message = None):
    lang = User.get_language(inter.author.id)
    Pig.set_skin(inter.author.id, 0, item_id)
    await BotUtils.send_callback(inter if message is None else message,
                                 embed=embeds.wardrobe_item_wear(inter, item_id, lang),
                                 edit_original_message=False,
                                 ephemeral=True
                                 )
    await wardrobe_item_selected(inter, item_id, inter.message)


async def wardrobe_item_remove(inter, item_id, message: disnake.Message = None):
    lang = User.get_language(inter.author.id)
    Pig.remove_skin(inter.author.id, 0, Inventory.get_item_skin_type(item_id))
    await BotUtils.send_callback(inter if message is None else message,
                                 embed=embeds.wardrobe_item_remove(inter, item_id, lang),
                                 edit_original_message=False,
                                 ephemeral=True
                                 )
    await wardrobe_item_selected(inter, item_id, inter.message)


async def wardrobe_item_preview(inter, item_id, message: disnake.Message = None):
    lang = User.get_language(inter.author.id)
    await BotUtils.send_callback(inter if message is None else message,
                                 embed=embeds.wardrobe_item_preview(inter, item_id, lang),
                                 edit_original_message=False,
                                 ephemeral=True
                                 )
    await wardrobe_item_selected(inter, item_id, inter.message)
