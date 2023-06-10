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


async def shop(inter):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    page_embeds = []
    page_components = []
    options = []
    for category, value in {'static_shop': Shop.get_last_static_shop(),
                            'daily_shop': Shop.get_last_daily_shop()}.items():
        item_fields = []
        options = []
        for item in value:
            item_fields.append(
                {
                    'name': f'{Func.generate_prefix(Inventory.get_item_emoji(item), backticks=True)}{Inventory.get_item_name(item, lang)}',
                    'value': f'```{locales["words"]["price"][lang]}: {Inventory.get_item_shop_price(item)} 🪙\n'
                             f'{locales["words"]["rarity"][lang]}: {Inventory.get_item_rarity(item, lang)}\n'
                             f'{locales["words"]["type"][lang]}: {Inventory.get_item_type(item, lang)}```',
                    'inline': False})
            options.append(
                {'label': Inventory.get_item_name(item, lang),
                 'value': f'{item}',
                 'emoji': Inventory.get_item_emoji(item),
                 'description': Func.cut_text(Inventory.get_item_description(item, lang), 100)
                 }
            )
        page_embeds += BotUtils.generate_embeds_list_from_fields(item_fields,
                                                                 description='' if item_fields else
                                                                 locales['shop']['shop_empty_desc'][lang],
                                                                 title=locales['shop'][f'{category}_title'][lang])
        page_components += BotUtils.generate_select_components_for_pages(options, 'shop_item_select',
                                                                         locales['inventory'][
                                                                             'select_item_placeholder'][
                                                                             lang])
    await BotUtils.pagination(inter, lang, embeds=page_embeds,
                              components=page_components if options else None,
                              hide_button=False, embed_thumbnail_file='bin/images/shop_thumbnail.png')


async def shop_item_selected(inter, item_id, message: disnake.Message = None):
    lang = User.get_language(inter.author.id)
    await BotUtils.send_callback(inter if message is None else message,
                                 embed=inventory_item_selected(inter, item_id, lang, 'shop'),
                                 components=components.shop_item_selected(inter.author.id, item_id, lang)
                                 )


async def shop_item_buy(inter, item_id):
    lang = User.get_language(inter.author.id)
    if User.get_money(inter.author.id) < Inventory.get_item_shop_price(item_id):
        await errors.callbacks.not_enough_money(inter)
        return
    User.add_money(inter.author.id, -Inventory.get_item_shop_price(item_id))
    Inventory.add_item(inter.author.id, item_id)
    await BotUtils.send_callback(inter, edit_original_message=False, ephemeral=True,
                                 embed=embeds.shop_item_bought(inter, item_id, lang))

# async def shop_skin_preview(inter, item_id, message: disnake.Message = None):
#     lang = User.get_language(inter.author.id)
#     await BotUtils.send_callback(inter if message is None else message,
#                                  embed=inventory_item_selected(inter, item_id, lang, 'shop'),
#                                  components=components.shop_item_selected(inter.author.id, item_id, lang)
#                                  )


# async def wardrobe_item_wear(inter, item_id, message: disnake.Message = None):
#     lang = User.get_language(inter.author.id)
#     Pig.set_skin(inter.author.id, 0, item_id)
#     await BotUtils.send_callback(inter if message is None else message,
#                                  embed=embeds.wardrobe_item_wear(inter, item_id, lang),
#                                  edit_original_message=False,
#                                  ephemeral=True
#                                  )
#     await wardrobe_item_selected(inter, item_id, inter.message)


# async def wardrobe_item_remove(inter, item_id, message: disnake.Message = None):
#     lang = User.get_language(inter.author.id)
#     Pig.remove_skin(inter.author.id, 0, Inventory.get_item_skin_type(item_id))
#     await BotUtils.send_callback(inter if message is None else message,
#                                  embed=embeds.wardrobe_item_remove(inter, item_id, lang),
#                                  edit_original_message=False,
#                                  ephemeral=True
#                                  )
#     await wardrobe_item_selected(inter, item_id, inter.message)
#
#
# async def wardrobe_item_preview(inter, item_id, message: disnake.Message = None):
#     lang = User.get_language(inter.author.id)
#     await BotUtils.send_callback(inter if message is None else message,
#                                  embed=embeds.wardrobe_item_preview(inter, item_id, lang),
#                                  edit_original_message=False,
#                                  ephemeral=True
#                                  )
#     await wardrobe_item_selected(inter, item_id, inter.message)
