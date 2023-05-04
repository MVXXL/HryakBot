import asyncio
import datetime
import random


from .....core import *
from .....utils import *
from . import embeds
from . import components


async def ate_and_poisoned(inter):
    lang = User.get_language(inter.author.id)
    await BotUtils.send_callback(inter, embed=embeds.ate_and_poisoned(inter, lang),
                                 components=[components.pay(lang), components.run_away(lang)],
                                 ephemeral=True, edit_original_message=False)
    interaction = await inter.client.wait_for('button_click')
    if interaction.component.custom_id == 'run_away':
        await interaction.response.defer()
        await inter.edit_original_message(embed=embeds.ran_away_from_doctor(inter, lang), components=[])
    if interaction.component.custom_id.split(':')[0] == 'pay':
        await interaction.response.defer()
        amount_to_pay = int(interaction.component.custom_id.split(':')[1])
        if User.get_money(interaction.author.id) >= amount_to_pay:
            await inter.edit_original_message(embed=embeds.payed_the_doctor(inter, lang), components=[])
        else:
            await inter.edit_original_message(embed=embeds.not_enough_money_for_doctor(inter, lang), components=[])

