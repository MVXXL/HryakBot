import random

from .....core import *
from .....utils import *


async def eat(inter, item_id, update):
    lang = User.get_language(inter.user.id)
    User.remove_item(inter.user.id, item_id)
    scenario = random.randrange(4)
    if scenario == 0:
        await send_callback(inter, embed=eaten_and_poisoned(inter, lang),
                            components=[discord.ui.Button(
                                label=translate(Locales.Global.pay, lang),
                                custom_id='in;pay',
                                emoji='🪙',
                                style=discord.ButtonStyle.primary
                            ), discord.ui.Button(
                                label=translate(Locales.Global.run_away, lang),
                                custom_id='in;run_away',
                                emoji='🏃‍♂️',
                            )],
                            ephemeral=True, edit_original_response=False)
        await update(edit_followup=True)
        interaction = await inter.client.wait_for('interaction')
        if interaction.data.get('custom_id') == 'in;run_away':
            await interaction.response.defer()
            await inter.edit_original_response(embed=ran_away_from_doctor(inter, lang), view=None)
        elif interaction.data.get('custom_id') == 'in;pay':
            await interaction.response.defer()
            if Item.get_amount('coins', interaction.user.id) >= 5:
                await inter.edit_original_response(embed=payed_the_doctor(inter, lang), view=None)
            else:
                await inter.edit_original_response(embed=not_enough_money_for_doctor(inter, lang), view=None)
    elif scenario == 1:
        await send_callback(inter, embed=generate_embed(
            title=translate(Locales.ItemUsed.ate_poop_and_dizzy_title, lang),
            description=f"{translate(Locales.ItemUsed.ate_poop_and_dizzy_desc, lang)}",
            prefix=Func.generate_prefix('🍽️'),
            inter=inter,
        ), ephemeral=True, edit_original_response=False)
        await update(edit_followup=True)
    elif scenario == 2:
        await send_callback(inter, embed=generate_embed(
            title=translate(Locales.ItemUsed.ate_poop_and_dizzy_title, lang),
            description=f"{translate(Locales.ItemUsed.ate_poop_and_question_desc, lang)}",
            prefix=Func.generate_prefix('🍽️'),
            inter=inter,
        ), ephemeral=True, edit_original_response=False)
        await update(edit_followup=True)
    elif scenario == 3:
        await send_callback(inter, embed=generate_embed(
            title=translate(Locales.ItemUsed.ate_poop_and_dad_title, lang),
            description=f"{translate(Locales.ItemUsed.ate_poop_and_dad_desc, lang)}",
            prefix=Func.generate_prefix('🍽️'),
            inter=inter,
        ), ephemeral=True, edit_original_response=False)
        await update(edit_followup=True)

def eaten_and_poisoned(inter, lang) -> discord.Embed:
    embed = generate_embed(
        title=translate(Locales.ItemUsed.ate_poop_and_poisoned_title, lang),
        description=f"{translate(Locales.ItemUsed.ate_poop_and_poisoned_desc, lang)}",
        prefix=Func.generate_prefix('🍽️'),
        inter=inter,
    )
    return embed


def ran_away_from_doctor(inter, lang) -> discord.Embed:
    embed = generate_embed(
        title=translate(Locales.PoopEaten.ran_away_and_not_payed_title, lang),
        description=f"{translate(Locales.PoopEaten.ran_away_and_not_payed_desc, lang)}",
        prefix=Func.generate_prefix('🏃‍♂️'),
        inter=inter,
    )
    return embed


def payed_the_doctor(inter, lang) -> discord.Embed:
    embed = generate_embed(
        title=translate(Locales.PoopEaten.payed_to_doctor_title, lang),
        description=f"{translate(Locales.PoopEaten.payed_to_doctor_desc, lang)}",
        prefix=Func.generate_prefix('🪙'),
        inter=inter,
    )
    return embed


def not_enough_money_for_doctor(inter, lang) -> discord.Embed:
    embed = generate_embed(
        title=translate(Locales.PoopEaten.not_enough_money_for_doctor_title, lang),
        description=f"{translate(Locales.PoopEaten.not_enough_money_for_doctor_desc, lang)}",
        prefix=Func.generate_prefix('🪙'), inter=inter,
        color=utils_config.error_color
    )
    return embed
