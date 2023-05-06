import asyncio
import datetime
import random

from ...core import *
from ...utils import *
from . import embeds
from . import item_used
from . import components
from .. import errors


async def inventory(inter, client):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    await BotUtils.inventory_embed(client, inter, lang)
    # item_fields = []
    # options = []
    # for item in User.get_inventory(inter.author.id):
    #     if items[item]['type'].split(':')[0] not in ['skin']:
    #         item_label_without_prefix = f'{Inventory.get_item_name(item, lang)} x{Inventory.get_item_amount(inter.author.id, item)}'
    #         item_fields.append(
    #             {'name': f'{Func.generate_prefix(Inventory.get_item_emoji(item))}{item_label_without_prefix}',
    #              'value': f'{locales["words"]["description"][lang]}: *{Inventory.get_item_description(item, lang)}*\n'
    #                       f'{locales["words"]["type"][lang]}: `{Inventory.get_item_cost(item)}` 🪙',
    #              'inline': False})
    #         options.append(
    #             {'label': item_label_without_prefix,
    #              'value': f'{item}',
    #              'emoji': Inventory.get_item_emoji(item),
    #              'description': Inventory.get_item_description(item, lang)
    #              }
    #         )
    # embeds = BotUtils.generate_embeds_list_from_fields(item_fields, description='' if item_fields else
    # locales['inventory']['inventory_empty_desc'][lang],
    #                                                    title=f"{Func.generate_prefix('📦')}{locales['inventory']['inventory_title'][lang]}")
    # components = BotUtils.generate_select_components_for_pages(options, 'inventory_item_select',
    #                                                            locales['inventory']['select_item_placeholder'][
    #                                                                lang])
    # await BotUtils.pagination(client, inter, lang, embeds=embeds, components=components if options else None,
    #                           hide_button=False)


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
    User.add_money(inter.author.id, money_received)
    await BotUtils.send_callback(inter, ephemeral=True,
                                 embed=embeds.inventory_item_sold(inter, item_id, amount, money_received, lang))
    await inventory_item_selected(inter, item_id, inter.message)


async def inventory_item_used(inter, item_id):
    Inventory.remove_item(inter.author.id, item_id, 1)
    await inventory_item_selected(inter, item_id, inter.message)
    match item_id:
        case 'poop': await random.choice([item_used.poop.callbacks.ate_and_poisoned])(inter)


class SellItemModal(disnake.ui.Modal):
    def __init__(self, inter, item_id):
        self.inter = inter
        self.item_id = item_id
        lang = User.get_language(user_id=inter.author.id)
        components = [
            disnake.ui.TextInput(
                label=locales['inventory_item_sell_modal']['label'][lang],
                placeholder=locales['inventory_item_sell_modal']['placeholder'][lang].format(max_amount=Inventory.get_item_amount(inter.author.id, item_id)),
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
