import asyncio
import datetime
import random
from typing import Literal

from ...core import *
from ...utils import *
from . import embeds
from . import item_used
from . import components
from .. import errors


async def inventory(inter):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    await inventory_embed(inter, lang)


async def inventory_embed(inter, lang: str = None, message: disnake.Message = None,
                          include_only: list = None,
                          not_include: list = None,
                          inventory_type: Literal['inventory', 'wardrobe'] = 'inventory'):
    if not_include is None:
        not_include = []
    if include_only is None:
        include_only = []
    if lang is None:
        lang = User.get_language(inter.author.id)
    item_fields = []
    options = []
    if inventory_type == 'wardrobe' and not include_only:
        include_only = ['skin']
    if inventory_type == 'inventory' and not not_include:
        not_include = ['skin']
    inventory_items = User.get_inventory(inter.author.id)
    inventory_items = Func.get_items_by_types(inventory_items, include_only, not_include)
    inventory_items = dict(sorted(inventory_items.items(), key=lambda x: items[x[0]]['type']))
    for item in inventory_items:
        if Inventory.get_item_amount(inter.author.id, item) > 0:
            field_value = f'{locales["words"]["rarity"][lang]}: {Inventory.get_item_rarity(item, lang)}'
            if inventory_type == 'inventory':
                field_value += f'\n{locales["words"]["cost_per_item"][lang]}: {Inventory.get_item_cost(item)} 🪙'
            elif inventory_type == 'wardrobe':
                field_value += f'\n{locales["words"]["type"][lang]}: {Inventory.get_item_type(item, lang)}'
            item_label_without_prefix = f'{Func.cut_text(Inventory.get_item_name(item, lang), 15)} x{Inventory.get_item_amount(inter.author.id, item)}'
            item_fields.append(
                {
                    'name': f'{Func.generate_prefix(Inventory.get_item_emoji(item), backticks=True)}{item_label_without_prefix}',
                    'value': f'```{field_value}```',
                    'inline': False})
            options.append(
                {'label': item_label_without_prefix,
                 'value': f'{item}',
                 'emoji': Inventory.get_item_emoji(item),
                 'description': Func.cut_text(Inventory.get_item_description(item, lang), 100)
                 }
            )
    inventory_empty_desc = ''
    custom_components_id = ''
    title = ''
    if inventory_type == 'inventory':
        inventory_empty_desc = locales['inventory']['inventory_empty_desc'][lang]
        custom_components_id = 'inventory_item_select'
        title = f"{Func.generate_prefix('📦')}{locales['inventory']['inventory_title'][lang]}"
    elif inventory_type == 'wardrobe':
        inventory_empty_desc = locales['wardrobe']['wardrobe_empty_desc'][lang]
        custom_components_id = 'wardrobe_item_select'
        title = f"{Func.generate_prefix('📦')}{locales['wardrobe']['wardrobe_title'][lang]}"
    page_embeds = BotUtils.generate_embeds_list_from_fields(Func.field_inline_alternation(item_fields),
                                                            description='' if item_fields else inventory_empty_desc,
                                                            title=title, fields_for_one=7)
    page_components = BotUtils.generate_select_components_for_pages(options, custom_components_id,
                                                                    locales['inventory']['select_item_placeholder'][
                                                                        lang], fields_for_one=7)
    embed_thumbnail_file = None
    category_choose_component = []
    if inventory_type == 'wardrobe':
        embed_thumbnail_file = BotUtils.generate_user_pig(inter.author.id)
        category_choose_component = components.skins_category_choose_components(inter.author.id, lang)
    elif inventory_type == 'inventory':
        embed_thumbnail_file = 'bin/images/inventory_thumbnail.png'
    await BotUtils.pagination(inter if message is None else message, lang, embeds=page_embeds,
                              return_if_starts_with=['back_to_inventory', 'wardrobe_category_choose'],
                              components=page_components if options else None,
                              components_for_every_page=category_choose_component,
                              hide_button=False, embed_thumbnail_file=embed_thumbnail_file)


async def inventory_item_selected(inter, item_id, message: disnake.Message = None):
    lang = User.get_language(inter.author.id)
    await BotUtils.send_callback(inter if message is None else message,
                                 embed=embeds.inventory_item_selected(inter, item_id, lang),
                                 components=components.inventory_item_selected(item_id, lang))


async def inventory_item_sold(inter, item_id, amount):
    lang = User.get_language(inter.author.id)
    if amount > Inventory.get_item_amount(inter.author.id, item_id):
        amount = Inventory.get_item_amount(inter.author.id, item_id)
    Inventory.remove_item(inter.author.id, item_id, amount)
    money_received = Inventory.get_item_cost(item_id) * amount
    Stats.add_money_earned(inter.author.id, money_received)
    Stats.add_items_sold(inter.author.id, item_id, amount)
    User.add_money(inter.author.id, money_received)
    await BotUtils.send_callback(inter, ephemeral=True,
                                 embed=embeds.inventory_item_sold(inter, item_id, amount, money_received, lang))
    if Inventory.get_item_amount(inter.author.id, item_id) == 0:
        await inventory_embed(inter, lang, inter.message)
    else:
        await inventory_item_selected(inter, item_id, inter.message)


async def inventory_item_cooked(inter, item_id, amount):
    lang = User.get_language(inter.author.id)
    if amount > Inventory.get_item_amount(inter.author.id, item_id):
        amount = Inventory.get_item_amount(inter.author.id, item_id)
    Inventory.remove_item(inter.author.id, item_id, amount)
    Inventory.add_item(inter.author.id, Inventory.get_item_cooked_id(item_id), amount)
    await BotUtils.send_callback(inter, ephemeral=True,
                                 embed=embeds.inventory_item_cooked(inter, item_id, amount, lang))
    if Inventory.get_item_amount(inter.author.id, item_id) == 0:
        await inventory_embed(inter, lang, inter.message)
    else:
        await inventory_item_selected(inter, item_id, inter.message)


async def inventory_item_used(inter, item_id: str):
    lang = User.get_language(inter.author.id)
    Inventory.remove_item(inter.author.id, item_id, 1)
    Stats.add_items_used(inter.author.id, item_id)
    await inventory_item_selected(inter, item_id, inter.message)
    if item_id == 'poop':
        await random.choice([item_used.poop.callbacks.ate_and_poisoned])(inter, lang)
    elif item_id == 'laxative':
        await item_used.laxative.callbacks.laxative_used(inter, lang)
    elif item_id in Func.get_items_by_key(items, 'type', 'case'):
        await item_used.case.callbacks.case_used(inter, lang, item_id)
    if Inventory.get_item_amount(inter.author.id, item_id) == 0:
        await inventory_embed(inter, lang, inter.message)


# class ActionItemModal(disnake.ui.Modal):
#     def __init__(self, inter, item_id):
#         self.inter = inter
#         self.item_id = item_id
#         lang = User.get_language(user_id=inter.author.id)
#         components = [
#             disnake.ui.TextInput(
#                 label=locales['inventory_item_sell_modal']['label'][lang],
#                 placeholder=locales['inventory_item_sell_modal']['placeholder'][lang].format(
#                     max_amount=Inventory.get_item_amount(inter.author.id, item_id)),
#                 custom_id="amount",
#                 style=disnake.TextInputStyle.short,
#                 max_length=10,
#                 required=True
#             ),
#         ]
#         super().__init__(title=locales['inventory_item_sell_modal']['title'][lang], components=components)
#
#     async def callback(self, inter: disnake.ModalInteraction):
#         if not inter.text_values['amount'].isdigit():
#             await errors.callbacks.modal_input_is_not_number(inter)
#         else:
#             await inventory_item_sold(inter, self.item_id, int(inter.text_values['amount']))

class SellItemModal(disnake.ui.Modal):
    def __init__(self, inter, item_id):
        self.inter = inter
        self.item_id = item_id
        lang = User.get_language(user_id=inter.author.id)
        components = [
            disnake.ui.TextInput(
                label=locales['inventory_item_sell_modal']['label'][lang],
                placeholder=locales['inventory_item_sell_modal']['placeholder'][lang].format(
                    max_amount=Inventory.get_item_amount(inter.author.id, item_id)),
                custom_id="amount",
                style=disnake.TextInputStyle.short,
                max_length=10,
                required=True
            ),
        ]
        super().__init__(title=locales['inventory_item_sell_modal']['title'][lang], components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        if not inter.text_values['amount'].isdigit():
            await errors.callbacks.modal_input_is_not_number(inter)
        else:
            await inventory_item_sold(inter, self.item_id, int(inter.text_values['amount']))


class CookItemModal(disnake.ui.Modal):
    def __init__(self, inter, item_id):
        self.inter = inter
        self.item_id = item_id
        lang = User.get_language(user_id=inter.author.id)
        components = [
            disnake.ui.TextInput(
                label=locales['inventory_item_cook_modal']['label'][lang],
                placeholder=locales['inventory_item_cook_modal']['placeholder'][lang].format(
                    max_amount=Inventory.get_item_amount(inter.author.id, item_id)),
                custom_id="amount",
                style=disnake.TextInputStyle.short,
                max_length=10,
                required=True
            ),
        ]
        super().__init__(title=locales['inventory_item_cook_modal']['title'][lang], components=components)

    async def callback(self, inter: disnake.ModalInteraction):
        if not inter.text_values['amount'].isdigit():
            await errors.callbacks.modal_input_is_not_number(inter)
        else:
            await inventory_item_cooked(inter, self.item_id, int(inter.text_values['amount']))
