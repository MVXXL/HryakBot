import asyncio
import datetime
import random

from ...core import *
from ...utils import *
from . import embeds
from . import components
from .. import errors


async def duel(inter, opponent, bet):
    await BotUtils.pre_command_check(inter)
    lang = User.get_language(inter.author.id)
    User.register_user_if_not_exists(opponent.id)
    if opponent == inter.author:
        raise PlayWithYourselfDuel
    if opponent.bot is True:
        raise BotAsOpponentDuel
    message = await BotUtils.send_callback(inter,
                                           embed=embeds.personal_duel_invite(inter, lang, opponent, bet),
                                           components=components.invite_components(lang))
    dm_message = await BotUtils.send_callback(inter, send_to_dm=opponent,
                                              components=components.duel_message_url(lang, message.jump_url) if message is not None else None,
                                              embed=embeds.personal_dm_duel_invite(inter, lang, bet))
    if dm_message is None:
        message = await BotUtils.send_callback(inter, opponent.mention,
                                               embed=embeds.personal_duel_invite(inter, lang, opponent, bet),
                                               components=components.invite_components(lang))

    def check(interaction):
        if message is not None:
            right_message = message.id == interaction.message.id
            return right_message and opponent.id == interaction.author.id

    try:
        interaction = await inter.client.wait_for('button_click', check=check, timeout=120)
    except asyncio.exceptions.TimeoutError:
        await BotUtils.send_callback(message, embed=embeds.duel_canceled(inter, lang, opponent, 'no_response'))
        return
    if interaction.component.custom_id == 'in:accept':
        await interaction.response.defer(ephemeral=True)
        if User.get_money(inter.author.id) < bet:
            await BotUtils.send_callback(interaction,
                                         embed=embeds.duel_canceled(inter, lang, inter.author, 'no_money_for_bet'))
            return
        if User.get_money(opponent.id) < bet:
            await BotUtils.send_callback(interaction,
                                         embed=embeds.duel_canceled(inter, lang, opponent, 'no_money_for_bet'))
            return
        chances = {}
        for member in [inter.author, opponent]:
            chances[member] = 100
            chances[member] += Pig.get_weight(member.id) / 2
            if Pig.get_time_to_next_feed(member.id) == -1:
                chances[member] += 20
        chances = Func.calculate_probabilities(chances, 1)
        winner = Func.random_choice_with_probability(chances)
        money_earned = int(round(bet * 1.7))
        User.add_money(inter.author.id, -bet)
        User.add_money(opponent.id, -bet)
        User.add_money(winner.id, money_earned)
        for i in range(7):
            await BotUtils.send_callback(interaction, embed=embeds.fight_is_starting(inter, lang, opponent, 7 - i,
                                                                                     list(chances.values())))
            await asyncio.sleep(1)
        await BotUtils.send_callback(interaction, embed=embeds.fight_is_going(inter, lang, opponent,
                                                                              random.choice(utils_config.fight_gifs)))
        await asyncio.sleep(11)
        await BotUtils.send_callback(interaction, embed=embeds.user_won(inter, lang, winner, money_earned,
                                                                        random.choice(utils_config.win_gifs)))
    elif interaction.component.custom_id == 'in:reject':
        await BotUtils.send_callback(interaction, embed=embeds.duel_canceled(inter, lang, opponent, 'opponent_reject'))
