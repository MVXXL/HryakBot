import discord.ui

from pig_code.core import *
from pig_code.utils import error_callbacks
from pig_code.utils.functions import translate


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
