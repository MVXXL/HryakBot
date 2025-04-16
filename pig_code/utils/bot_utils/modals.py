import discord.ui

from ...core import *
from . import error_callbacks
from ..functions import translate


async def get_item_amount(inter, title, label, max_amount: int = None, delete_response: bool = False):
    lang = User.get_language(user_id=inter.user.id)
    custom_id = f'modal;get_item_amount{random.randrange(1000)}'
    modal = discord.ui.Modal(title=title, custom_id=custom_id)
    modal.add_item(discord.ui.TextInput(
        label=label,
        placeholder=translate(Locales.Global.you_have_amount, lang, {'max_amount': max_amount}),
        custom_id="amount",
        style=discord.TextStyle.short,
        max_length=7,
        required=True
    ))
    await inter.response.send_modal(modal)
    interaction = await inter.client.wait_for(
        "interaction",
        check=lambda i: i.data.get('custom_id') == custom_id and i.user.id == inter.user.id,
        timeout=300,
    )
    amount = interaction.data['components'][0]['components'][0]['value']
    if not str(amount).isdigit():
        await error_callbacks.modal_input_is_not_number(interaction)
        return False
    if int(amount) > max_amount:
        amount = max_amount
    if delete_response:
        await interaction.response.defer(ephemeral=True)
        # await interaction.delete_original_response()
    return interaction, int(amount)


# class GetItemAmountModal(discord.ui.Modal):
#     def __init__(self, inter, item_id, func, label, title, max_amount: int = None):
#         self.inter = inter
#         self.item_id = item_id
#         self.func = func
#         self.lang = User.get_language(user_id=inter.user.id)
#         self.max_amount = max_amount
#         if self.max_amount is None:
#             self.max_amount = Item.get_amount(item_id, inter.user.id)
#         components = [
#             discord.ui.TextInput(
#                 label=translate(label, self.lang) if type(label) == dict else label,
#                 placeholder=translate(Locales.Global.you_have_amount, self.lang, {'max_amount':self.max_amount}),
#                 custom_id="amount",
#                 style=discord.TextInputStyle.short,
#                 max_length=10,
#                 required=True
#             )
#         ]
#         super().__init__(title=translate(title, self.lang) if type(title) == dict else title, components=components)
#
#     async def callback(self, inter: discord.ModalInteraction):
#         if not inter.text_values['amount'].isdigit():
#             await error_callbacks.modal_input_is_not_number(inter)
#         else:
#             if int(inter.text_values['amount']) > self.max_amount:
#                 inter.text_values['amount'] = self.max_amount
#             await self.func(inter, self.item_id, int(inter.text_values['amount']))


# class GetAmountToDonate(discord.ui.Modal):
#     def __init__(self, inter):
#         self.inter = inter
#         self.lang = User.get_language(user_id=inter.user.id)
#         components = [
#             discord.ui.TextInput(
#                 label='Type an amount to donate',
#                 # placeholder='',
#                 custom_id="amount",
#                 style=discord.TextInputStyle.short,
#                 max_length=7,
#                 required=True
#             )
#         ]
#         super().__init__(title='Donation page', components=components)
#
#     async def callback(self, inter: discord.ModalInteraction):
#         if not inter.text_values['amount'].isdigit():
#             await error_callbacks.modal_input_is_not_number(inter)
#         else:
#             if int(inter.text_values['amount']) > self.max_amount:
#                 inter.text_values['amount'] = self.max_amount
#             await self.func(inter, self.item_id, int(inter.text_values['amount']))


async def get_amount_of_hollars_to_donate(inter, delete_response: bool = False):
    lang = User.get_language(user_id=inter.user.id)
    modal = discord.ui.Modal(title=translate(Locales.PremiumShop.get_amount_of_hollars_modal_title, lang),
                             custom_id='get_amount_of_hollars_to_donate')
    modal.add_item(discord.ui.TextInput(
        label=translate(Locales.PremiumShop.get_amount_of_hollars_modal_label, lang),
        placeholder=translate(Locales.PremiumShop.get_amount_of_hollars_modal_placeholder, lang),
        custom_id="amount",
        style=discord.TextStyle.short,
        max_length=7,
        required=True
    ))
    await inter.response.send_modal(modal)
    interaction = await inter.client.wait_for(
        "interaction",
        check=lambda i: i.data.get('custom_id') == "get_amount_of_hollars_to_donate" and i.user.id == inter.user.id,
        timeout=300,
    )
    amount = interaction.data['components'][0]['components'][0]['value']
    if not amount.isdigit():
        await error_callbacks.modal_input_is_not_number(inter)
        return False
    if delete_response:
        await interaction.response.defer(ephemeral=True)
        # await interaction.delete_original_response()
    return interaction, int(amount)
