from .....core import *
from .....utils import *


async def ate_and_poisoned(inter, item_id, update):
    lang = User.get_language(inter.author.id)
    User.remove_item(inter.author.id, item_id)
    await send_callback(inter, embed=eaten_and_poisoned(inter, lang),
                        components=[disnake.ui.Button(
                            label=Locales.Global.pay[lang],
                            custom_id='in;pay',
                            emoji='🪙',
                            style=disnake.ButtonStyle.primary
                        ), disnake.ui.Button(
                            label=Locales.Global.run_away[lang],
                            custom_id='in;run_away',
                            emoji='🏃‍♂️',
                        )],
                        ephemeral=True, edit_original_message=False)
    await update()
    interaction = await inter.client.wait_for('button_click')
    if interaction.component.custom_id == 'in;run_away':
        await interaction.response.defer()
        await inter.edit_original_message(embed=ran_away_from_doctor(inter, lang), components=[])
    if interaction.component.custom_id == 'in;pay':
        await interaction.response.defer()
        if Item.get_amount('coins', interaction.author.id) >= 5:
            await inter.edit_original_message(embed=payed_the_doctor(inter, lang), components=[])
        else:
            await inter.edit_original_message(embed=not_enough_money_for_doctor(inter, lang), components=[])


def eaten_and_poisoned(inter, lang) -> disnake.Embed:
    embed = generate_embed(
        title=Locales.ItemUsed.ate_poop_and_poisoned_title[lang],
        description=f"{Locales.ItemUsed.ate_poop_and_poisoned_desc[lang]}",
        prefix=Func.generate_prefix('🍽️'),
        inter=inter,
    )
    return embed


def ran_away_from_doctor(inter, lang) -> disnake.Embed:
    embed = generate_embed(
        title=Locales.PoopEaten.ran_away_and_not_payed_title[lang],
        description=f"{Locales.PoopEaten.ran_away_and_not_payed_desc[lang]}",
        prefix=Func.generate_prefix('🏃‍♂️'),
        inter=inter,
    )
    return embed


def payed_the_doctor(inter, lang) -> disnake.Embed:
    embed = generate_embed(
        title=Locales.PoopEaten.payed_to_doctor_title[lang],
        description=f"{Locales.PoopEaten.payed_to_doctor_desc[lang]}",
        prefix=Func.generate_prefix('🪙'),
        inter=inter,
    )
    return embed


def not_enough_money_for_doctor(inter, lang) -> disnake.Embed:
    embed = generate_embed(
        title=Locales.PoopEaten.not_enough_money_for_doctor_title[lang],
        description=f"{Locales.PoopEaten.not_enough_money_for_doctor_desc[lang]}",
        prefix=Func.generate_prefix('🪙'),inter=inter,
        color=utils_config.error_color
    )
    return embed
